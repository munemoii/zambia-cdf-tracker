#!/usr/bin/env python3
"""Ingest the staged Auditor-General per-constituency extraction into cdf.db.

Source of truth: the staged, validated CSVs in
  hidden_files/ag-extraction-2026-10-31/  (see VALIDATION.md there).
Every value is verbatim from the official AG report PDFs; blanks in the CSVs
are blank AS PRINTED and are stored as NULL (never zero-filled).

Name joining: name_mapping.csv — match_type 'exact', 'fuzzy' and 'approved'
rows are ingested. 'approved' rows are manual-review mappings Caleb confirmed
on 2026-10-31 via delegated judgment ("I will trust your judgment") — see
APPROVALS.md in the staging folder; every row ingested through one carries the
approval in its flags JSON so the audit trail shows it was confirmed, not
assumed. Remaining 'manual-review' names (Lukulu — its proof test failed, see
APPROVALS.md) are skipped entirely and itemised in
held_mappings_build_note.md in the staging folder (Caleb's rule, 2026-10-31).

Rerunnable: both AG tables are dropped and recreated inside one transaction.
    python3 model/ingest_ag.py
"""
import csv
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # model/
REPO = HERE.parent                               # site-repo/
GOAL = REPO.parent                               # zambia-cdf-dashboard-website/
STAGE = GOAL / "hidden_files" / "ag-extraction-2026-10-31"
DB = HERE / "cdf.db"

DOC23 = ("Report of the Auditor General on the Constituency Development Fund "
         "for the Financial Year Ended 31st December 2023")
URL23 = "https://acazambia.org/wp-content/uploads/2025/01/2023-CDF-Report.pdf"
DOC24 = ("Report of the Auditor General on the Constituency Development Fund "
         "for the Financial Year Ended 31st December 2024")
URL24 = "https://www.ago.gov.zm/wp-content/uploads/CDF-Report-2024.pdf"


def num(v):
    """Parse a CSV money/count cell: '' -> None, '(x)' -> -x, 'x -' -> -x,
    '#DIV/0!' (printed in the report itself) -> None."""
    if v is None:
        return None
    s = str(v).strip().replace(",", "")
    if s in ("", "#DIV/0!"):
        return None
    if s.startswith("(") and s.endswith(")"):
        return -int(float(s[1:-1]))
    if s.endswith("-"):
        return -int(float(s[:-1].strip()))
    return int(float(s))


def pct(v):
    n = num(v)
    return n


def page(v):
    s = str(v).strip()
    return int(s) if s else None


def read_csv(name):
    with open(STAGE / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    mapping = {}
    for r in read_csv("name_mapping.csv"):
        mapping[r["ag_name"]] = (r["tracker_name"], r["match_type"])

    con = sqlite3.connect(DB)
    cur = con.cursor()
    tracker = {name: cid for cid, name in cur.execute(
        "SELECT id, name FROM constituencies WHERE set_id = 1")}

    def resolve(ag_name):
        """-> (constituency_id, match_type) or (None, match_type/None)."""
        if ag_name not in mapping:
            return None, "unmapped"
        tname, mtype = mapping[ag_name]
        if mtype not in ("exact", "fuzzy", "approved"):
            return None, mtype
        if tname not in tracker:
            return None, "tracker-missing"
        return tracker[tname], mtype

    APPROVAL_FLAG = ("name confirmed 2026-10-31: manual-review mapping approved "
                     "on Caleb's delegated judgment (APPROVALS.md)")

    def add_provenance(flags, mtype):
        if mtype == "approved":
            flags["name_match"] = APPROVAL_FLAG
        return flags

    held = []          # (dataset, ag_name, proposed_tracker, rows)
    held_count = {}

    def note_held(dataset, ag_name):
        key = (dataset, ag_name)
        held_count[key] = held_count.get(key, 0) + 1

    cur.execute("BEGIN")
    cur.execute("DROP TABLE IF EXISTS ag_components")
    cur.execute("DROP TABLE IF EXISTS ag_project_status")
    cur.execute("""
        CREATE TABLE ag_components (
          id INTEGER PRIMARY KEY,
          fy INTEGER NOT NULL,
          constituency_id INTEGER NOT NULL REFERENCES constituencies(id),
          component_label_as_printed TEXT NOT NULL,
          received INTEGER,
          expenditure INTEGER,
          unspent INTEGER,
          unspent_pct INTEGER,
          extra_json TEXT NOT NULL DEFAULT '{}',
          flags TEXT NOT NULL DEFAULT '{}',
          source_doc TEXT NOT NULL,
          appendix_ref TEXT NOT NULL,
          source_url TEXT NOT NULL
        )""")
    cur.execute("""
        CREATE TABLE ag_project_status (
          id INTEGER PRIMARY KEY,
          fy INTEGER NOT NULL,
          constituency_id INTEGER NOT NULL REFERENCES constituencies(id),
          cohort_year INTEGER NOT NULL,
          approved INTEGER,
          implemented INTEGER,
          in_progress INTEGER,
          not_implemented INTEGER,
          flags TEXT NOT NULL DEFAULT '{}',
          source_doc TEXT NOT NULL,
          appendix_ref TEXT NOT NULL,
          source_url TEXT NOT NULL
        )""")

    stats = {}

    # ---------------- components FY2023 ----------------
    rows = read_csv("fy2023_appendix2_components.csv")
    n_in = 0
    for r in rows:
        cid, mtype = resolve(r["constituency"])
        if cid is None:
            note_held("fy2023_appendix2_components", r["constituency"])
            continue
        flags = {"note": r["note"]} if r["note"].strip() else {}
        flags = add_provenance(flags, mtype)
        extra = {"pdf_page": page(r["source_page_pdf"])}
        cur.execute(
            "INSERT INTO ag_components(fy,constituency_id,component_label_as_printed,"
            "received,expenditure,unspent,unspent_pct,extra_json,flags,source_doc,"
            "appendix_ref,source_url) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (2023, cid, r["component"], num(r["amount_received"]),
             num(r["expenditure"]), num(r["unspent_balance"]), pct(r["unspent_pct"]),
             json.dumps(extra), json.dumps(flags), DOC23,
             f"Appendix {r['appendix']}", URL23))
        n_in += 1
    stats["fy2023_components"] = (n_in, len(rows))

    # ---------------- components FY2024 ----------------
    rows = read_csv("fy2024_appendix2_components.csv")
    n_in = 0
    for r in rows:
        cid, mtype = resolve(r["constituency"])
        if cid is None:
            note_held("fy2024_appendix2_components", r["constituency"])
            continue
        flags = {"note": r["note"]} if r["note"].strip() else {}
        flags = add_provenance(flags, mtype)
        extra = {
            "balance_bf": num(r["balance_bf"]),
            "funding_2024": num(r["amount_received_funding_2024"]),
            "loan_repayment": num(r["loan_repayment"]),
            "interest_accrued": num(r["interest_accrued"]),
            "pdf_page": page(r["source_page_pdf"]),
        }
        # Appendix 2.3's third money column is headed "Funds Borrowed" in print
        # (the extractor mapped it onto other_receipts) — keep its true label.
        if r["appendix"] == "2.3":
            extra["funds_borrowed"] = num(r["other_receipts"])
        else:
            extra["other_receipts"] = num(r["other_receipts"])
        cur.execute(
            "INSERT INTO ag_components(fy,constituency_id,component_label_as_printed,"
            "received,expenditure,unspent,unspent_pct,extra_json,flags,source_doc,"
            "appendix_ref,source_url) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (2024, cid, r["component"], num(r["total_funds_available"]),
             num(r["expenditure"]), num(r["unspent_balance"]), pct(r["unspent_pct"]),
             json.dumps(extra), json.dumps(flags), DOC24,
             f"Appendix {r['appendix']}", URL24))
        n_in += 1
    stats["fy2024_components"] = (n_in, len(rows))

    # ---------------- project status FY2023 ----------------
    rows = read_csv("fy2023_project_status.csv")
    n_in = 0
    for r in rows:
        cid, mtype = resolve(r["constituency"])
        if cid is None:
            note_held("fy2023_project_status", r["constituency"])
            continue
        flags = {"first_column_label": r["first_column_label"]}
        if r["note"].strip():
            flags["note"] = r["note"]
        flags = add_provenance(flags, mtype)
        cur.execute(
            "INSERT INTO ag_project_status(fy,constituency_id,cohort_year,approved,"
            "implemented,in_progress,not_implemented,flags,source_doc,appendix_ref,"
            "source_url) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (2023, cid, int(r["cohort_year"]), num(r["projects_bf_or_approved"]),
             num(r["implemented"]), num(r["work_in_progress"]),
             num(r["outstanding"]), json.dumps(flags), DOC23,
             f"Appendix {r['appendix']}", URL23))
        n_in += 1
    stats["fy2023_status"] = (n_in, len(rows))

    # ---------------- project status FY2024 ----------------
    rows = read_csv("fy2024_project_status.csv")
    n_in = 0
    for r in rows:
        cid, mtype = resolve(r["constituency"])
        if cid is None:
            note_held("fy2024_project_status", r["constituency"])
            continue
        flags = {"first_column_label": r["first_column_label"]}
        if r["note"].strip():
            flags["note"] = r["note"]
        flags = add_provenance(flags, mtype)
        cur.execute(
            "INSERT INTO ag_project_status(fy,constituency_id,cohort_year,approved,"
            "implemented,in_progress,not_implemented,flags,source_doc,appendix_ref,"
            "source_url) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (2024, cid, int(r["cohort_year"]), num(r["projects_bf_or_approved"]),
             num(r["implemented_completed"]), num(r["work_in_progress"]),
             num(r["outstanding"]), json.dumps(flags), DOC24,
             f"Appendix {r['appendix']}", URL24))
        n_in += 1
    stats["fy2024_status"] = (n_in, len(rows))

    con.commit()

    # ---------------- held-mappings note ----------------
    lines = [
        "# AG build — held name mappings (NOT ingested)",
        "",
        "Build: model/ingest_ag.py, 2026-10-31. Per Caleb's rule, only exact/fuzzy",
        "name matches — and manual-review mappings Caleb has approved — are",
        "ingested. On 2026-10-31 Caleb delegated judgment on the 22 held mappings;",
        "21 were approved (match_type 'approved' in name_mapping.csv, provenance in",
        "APPROVALS.md and in each ingested row's flags). Every staged CSV row whose",
        "AG constituency name is still a manual-review mapping (or unmapped) was",
        "skipped in full — no AG data is rendered for a constituency from a name",
        "that has not been confirmed.",
        "",
        "| Dataset | AG name (as printed) | Proposed tracker name | Rows held |",
        "|---|---|---|---|",
    ]
    for (dataset, ag_name), cnt in sorted(held_count.items()):
        prop = mapping.get(ag_name, ("—", ""))[0]
        lines.append(f"| {dataset} | {ag_name} | {prop} | {cnt} |")
    covered = {r[0] for r in cur.execute(
        "SELECT DISTINCT constituency_id FROM ag_components UNION "
        "SELECT DISTINCT constituency_id FROM ag_project_status")}
    allc = cur.execute(
        "SELECT id, name FROM constituencies WHERE set_id = 1 ORDER BY name").fetchall()
    missing = [n for cid, n in allc if cid not in covered]
    lines += ["", f"Tracker constituencies with AG data ingested: {len(covered)} of {len(allc)}.",
              "", "Tracker constituencies with NO AG rows ingested (no audited-record "
              "section is rendered for these):", ""]
    lines += [f"- {n}" for n in missing]
    (STAGE / "held_mappings_build_note.md").write_text("\n".join(lines) + "\n")

    for k, (a, b) in stats.items():
        print(f"{k}: ingested {a} of {b} staged rows (held {b - a})")
    print(f"held rows total: {sum(held_count.values())} across "
          f"{len(held_count)} dataset/name pairs")
    print(f"constituencies covered: {len(covered)} of {len(allc)}")
    con.close()


if __name__ == "__main__":
    sys.exit(main())
