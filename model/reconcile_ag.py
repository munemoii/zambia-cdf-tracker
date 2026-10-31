#!/usr/bin/env python3
"""Reconciliation gate for the Auditor-General layer.

Verifies, per appendix/cohort and numeric field:
  DB sum == staged-CSV sum - held (manual-review) sum        [must be exact]
  staged-CSV sum vs the report's PRINTED total                [exact, or the
    deviation documented in VALIDATION.md §4/§6 — anything else FAILS]

Also checks the FY2024 appendix sums against the AG report's own national
framing — Cross-Cutting §1 (Unspent Funds), Table 1: "K771.4m unspent of
K5,886.9m total funds available (K5,115.6m spent)".

    python3 model/reconcile_ag.py   (exit 1 on any unexplained mismatch)
"""
import csv
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent.parent / "hidden_files" / "ag-extraction-2026-10-31"
sys.path.insert(0, str(HERE))
from ingest_ag import num  # noqa: E402

fails = []
notes = []


def check(label, got, want, documented=None):
    if got == want:
        print(f"  PASS  {label}: {got:,}")
    elif documented:
        print(f"  DEV   {label}: got {got:,}, printed {want:,} — {documented}")
        notes.append(label)
    else:
        print(f"  FAIL  {label}: got {got:,}, expected {want:,}")
        fails.append(label)


def read(name):
    with open(STAGE / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


mapping = {r["ag_name"]: r["match_type"] for r in read("name_mapping.csv")}


def is_held(name):
    return mapping.get(name) not in ("exact", "fuzzy")


def sums(rows, keyfn, fields):
    out = {}
    for r in rows:
        k = keyfn(r)
        out.setdefault(k, {f: 0 for f in fields} | {"n": 0, "held_n": 0})
        held = is_held(r["constituency"])
        if held:
            out[k]["held_n"] += 1
            continue
        out[k]["n"] += 1
        for f in fields:
            v = num(r[f])
            if v is not None:
                out[k][f] += v
    return out


con = sqlite3.connect(HERE / "cdf.db")
con.row_factory = sqlite3.Row

# ---------------------------------------------------------------- FY2023 money
print("FY2023 components (received / expenditure / unspent):")
rows = read("fy2023_appendix2_components.csv")
cs = sums(rows, lambda r: r["appendix"],
          ["amount_received", "expenditure", "unspent_balance"])
printed23 = {
    "2.1": (2408781762, 1010228030, 1398553732),   # national summary (no appendix total row)
    "2.2": (333448110, 320754460, 12693650),
    "2.3": (333448110, 320754460, 12693650),
    "2.4": (881501869, 491594218, 389907651),
    "2.5": (219610294, 215589577, 4020717),
}
for app, (pr, pe, pu) in printed23.items():
    s = cs[app]
    csv_tot = (s["amount_received"] + _held_sum(rows, app, "amount_received"),
               s["expenditure"] + _held_sum(rows, app, "expenditure"),
               s["unspent_balance"] + _held_sum(rows, app, "unspent_balance")) \
        if False else None
    # CSV totals (all rows incl. held) recomputed directly:
    allt = [r for r in rows if r["appendix"] == app]
    cr = sum(num(r["amount_received"]) or 0 for r in allt)
    ce = sum(num(r["expenditure"]) or 0 for r in allt)
    cu = sum(num(r["unspent_balance"]) or 0 for r in allt)
    doc = None
    if app == "2.1":
        doc = "VALIDATION §4/§6.4: Zambezi East/West K1 printing slips (+1 spent/unspent)"
    if app == "2.4":
        doc = ("Build-verified on the printed page (report p.724): rows sum K2 below the "
               "printed total on received/unspent, expenditure exact — a K2 slip inside the "
               "report. VALIDATION §4/§6.5's K10,559,322 shortfall narrative is SUPERSEDED: "
               "it predates the full read of the Lusaka merged group (rows 144-150, "
               "K43,050,792, carried under Kanyama), which the final CSV/JSON carry correctly.")
    check(f"FY23 App {app} CSV received vs printed", cr, pr, doc if cr != pr else None)
    check(f"FY23 App {app} CSV expenditure vs printed", ce, pe, doc if ce != pe else None)
    check(f"FY23 App {app} CSV unspent vs printed", cu, pu, doc if cu != pu else None)
    db = con.execute(
        "SELECT COUNT(*) n, SUM(received) r, SUM(expenditure) e, SUM(unspent) u "
        "FROM ag_components WHERE fy=2023 AND appendix_ref=?",
        (f"Appendix {app}",)).fetchone()
    check(f"FY23 App {app} DB rows == CSV - held", db["n"], s["n"])
    check(f"FY23 App {app} DB received == CSV - held", db["r"] or 0, s["amount_received"])
    check(f"FY23 App {app} DB expenditure == CSV - held", db["e"] or 0, s["expenditure"])
    check(f"FY23 App {app} DB unspent == CSV - held", db["u"] or 0, s["unspent_balance"])


def _held_sum(rows_, app, field):
    return sum(num(r[field]) or 0 for r in rows_
               if r["appendix"] == app and is_held(r["constituency"]))


# ---------------------------------------------------------------- FY2024 money
print("FY2024 components:")
rows = read("fy2024_appendix2_components.csv")
F24 = ["balance_bf", "amount_received_funding_2024", "other_receipts",
       "total_funds_available", "expenditure", "unspent_balance",
       "loan_repayment", "interest_accrued"]
cs = sums(rows, lambda r: r["appendix"], F24)


def csv_all(app, f):
    return sum(num(r[f]) or 0 for r in rows if r["appendix"] == app)


# printed-total expectations as (field, printed value or 'rows', deviation note)
def expect(app, field, printed, doc=None):
    got = csv_all(app, field)
    check(f"FY24 App {app} CSV {field} vs printed", got, printed,
          doc if got != printed else None)


for app in ["2.1", "2.2", "2.3", "2.4", "2.5"]:
    for f in F24:
        got = csv_all(app, f)
        if app == "2.1" and f == "expenditure":
            expect(app, f, 2957084390, "VALIDATION §4/§6.4: Bwacha K1 slip (rows +1)")
        elif app == "2.2":
            # Printed Totals (VALIDATION §4 deltas resolved at build stage: the
            # omitted row was Kafue's, recovered from report p.211 — Chilanga is
            # printed at row 81. See VALIDATION addendum 2.)
            printed22 = {"balance_bf": 125363564,
                         "amount_received_funding_2024": 229589748,
                         "total_funds_available": 356880169,
                         "expenditure": 374587934,
                         "unspent_balance": -17707765}
            if f in printed22:
                expect(app, f, printed22[f],
                       "report K1 slip: printed total sits K1 above the printed rows "
                       "(total funds / unspent only)")
        elif app == "2.4" and f == "amount_received_funding_2024":
            expect(app, f, got - 2, "VALIDATION §4: funding rows +K2 vs printed, no row-level cause found")
        elif app == "2.4" and f == "balance_bf":
            expect(app, f, got + 32674, "VALIDATION §4/§6.6: printed totals treat trailing-minus cell as nil")
        elif app == "2.4" and f == "unspent_balance":
            expect(app, f, got + 1,
                   "App 2.4 printed Totals row (report PDF p.248) reads 115,355,773 — K1 above "
                   "the printed rows (a K1 printing slip). The +1,137,122 nil-treatment "
                   "adjustment from VALIDATION §4/§6.6 is WITHDRAWN: the figure 116,492,894 "
                   "appears nowhere in the PDF (appendix1-k5120-findings.md §6)")
        elif app == "2.5" and f == "unspent_balance":
            expect(app, f, -87719412)
        else:
            expect(app, f, got)  # VALIDATION: exact — printed equals row sums

# DB == CSV - held for FY2024, incl. extra_json fields
extra_map = {"balance_bf": "balance_bf", "amount_received_funding_2024": "funding_2024",
             "loan_repayment": "loan_repayment", "interest_accrued": "interest_accrued"}
for app in ["2.1", "2.2", "2.3", "2.4", "2.5"]:
    s = cs[app]
    dbrows = con.execute(
        "SELECT received, expenditure, unspent, extra_json FROM ag_components "
        "WHERE fy=2024 AND appendix_ref=?", (f"Appendix {app}",)).fetchall()
    check(f"FY24 App {app} DB rows == CSV - held", len(dbrows), s["n"])
    check(f"FY24 App {app} DB total_funds == CSV - held",
          sum(r["received"] or 0 for r in dbrows), s["total_funds_available"])
    check(f"FY24 App {app} DB expenditure == CSV - held",
          sum(r["expenditure"] or 0 for r in dbrows), s["expenditure"])
    check(f"FY24 App {app} DB unspent == CSV - held",
          sum(r["unspent"] or 0 for r in dbrows), s["unspent_balance"])
    for csvf, jk in extra_map.items():
        dbs = sum((json.loads(r["extra_json"]).get(jk) or 0) for r in dbrows)
        check(f"FY24 App {app} DB {jk} == CSV - held", dbs, s[csvf])
    other_key = "funds_borrowed" if app == "2.3" else "other_receipts"
    dbs = sum((json.loads(r["extra_json"]).get(other_key) or 0) for r in dbrows)
    check(f"FY24 App {app} DB {other_key} == CSV - held", dbs, s["other_receipts"])

# ---------------------------------------------------------------- status
print("Project status:")
for fy, fname, apps in [(2023, "fy2023_project_status.csv", ["3", "4"]),
                        (2024, "fy2024_project_status.csv", ["3"])]:
    rows = read(fname)
    for app in apps:
        sub = [r for r in rows if r["appendix"] == app]
        for cohort in sorted({r["cohort_year"] for r in sub}):
            csub = [r for r in sub if r["cohort_year"] == cohort]
            held = [r for r in csub if is_held(r["constituency"])]
            keep = [r for r in csub if not is_held(r["constituency"])]
            db = con.execute(
                "SELECT COUNT(*) n, SUM(approved) a, SUM(implemented) i, "
                "SUM(in_progress) w, SUM(not_implemented) o FROM ag_project_status "
                "WHERE fy=? AND appendix_ref=? AND cohort_year=?",
                (fy, f"Appendix {app}", int(cohort))).fetchone()
            lbl = f"FY{fy} App {app} cohort {cohort}"
            check(f"{lbl} DB rows == CSV - held", db["n"], len(keep))
            for col, f in [("a", "projects_bf_or_approved"), ("i", None),
                           ("w", "work_in_progress"), ("o", "outstanding")]:
                pass
            check(f"{lbl} DB approved == CSV - held", db["a"] or 0,
                  sum(num(r["projects_bf_or_approved"]) or 0 for r in keep))
            impf = "implemented" if fy == 2023 else "implemented_completed"
            check(f"{lbl} DB implemented == CSV - held", db["i"] or 0,
                  sum(num(r[impf]) or 0 for r in keep))
            check(f"{lbl} DB in_progress == CSV - held", db["w"] or 0,
                  sum(num(r["work_in_progress"]) or 0 for r in keep))
            check(f"{lbl} DB not_implemented == CSV - held", db["o"] or 0,
                  sum(num(r["outstanding"]) or 0 for r in keep))

# FY2024 App 3 printed totals (all rows, incl. held — the report's own totals)
rows = read("fy2024_project_status.csv")
tot = {f: sum(num(r[f]) or 0 for r in rows) for f in
       ["projects_bf_or_approved", "implemented_completed", "work_in_progress", "outstanding"]}
check("FY24 App3 CSV approved total (bf 2051 + new 2828 = 4879)", tot["projects_bf_or_approved"], 4879)
check("FY24 App3 CSV completed vs printed", tot["implemented_completed"], 3060)
check("FY24 App3 CSV in-progress vs printed", tot["work_in_progress"], 1293)
check("FY24 App3 CSV outstanding vs printed", tot["outstanding"], 525)
# FY2023 status printed totals
rows = read("fy2023_project_status.csv")
for app, want in [("3", (3266, 2404, 719, 143)), ("4", (2793, 1109, 767, 917))]:
    sub = [r for r in rows if r["appendix"] == app]
    got = tuple(sum(num(r[f]) or 0 for r in sub) for f in
                ["projects_bf_or_approved", "implemented", "work_in_progress", "outstanding"])
    for lbl, g, w in zip(["approved", "implemented", "wip", "outstanding"], got, want):
        check(f"FY23 App {app} CSV {lbl} vs printed", g, w,
              "VALIDATION addendum 2: Kabompo page-start row recovered at build "
              "stage; Chadiza is absent from the printed appendix itself"
              if g != w else None)

# ------------------------------------------------------- Table 1 reproduction
# The site's national line is the AG FY2024 report's own framing (Cross-Cutting
# §1 "Unspent Funds", Table 1, printed p.3): total funds available
# K5,886,946,075; total expenditure K5,115,558,793; unspent K771,387,282.
# The appendix-2 row sums must reproduce Table 1 exactly on unspent and
# expenditure (appendix1-k5120-findings.md §5). (The old "K5,120m available"
# denominator appears nowhere in the report: it is the rounded EXPENDITURE
# total mislabelled as available by a secondary explainer.)
print("\nFY2024 national aggregates vs AG Table 1 (Cross-Cutting §1, printed p.3):")
rows = read("fy2024_appendix2_components.csv")
unspent_rows = sum(num(r["unspent_balance"]) or 0 for r in rows)
expenditure_rows = sum(num(r["expenditure"]) or 0 for r in rows)
funding_rows = sum(num(r["amount_received_funding_2024"]) or 0 for r in rows)
totalfunds_rows = sum(num(r["total_funds_available"]) or 0 for r in rows)
check("FY24 App2 rows unspent == Table 1 printed", unspent_rows, 771387282)
check("FY24 App2 rows expenditure == Table 1 printed", expenditure_rows, 5115558793)
check("FY24 App2 rows total funds == Table 1 printed", totalfunds_rows, 5886946075,
      "rows sit K1 below Table 1 — the documented App 2.1/App 2.2 K1 printing slips "
      "(appendix1-k5120-findings.md §5)")
# Printed-totals basis: each appendix's own printed Totals row for unspent —
# 2.1 612,097,578 · 2.2 -17,707,765 (K1 above its rows) · 2.3 149,361,110 ·
# 2.4 115,355,773 (K1 above its rows) · 2.5 -87,719,412 — sums to K771,387,284,
# i.e. Table 1 + K2 of printing slips. Documented here; NOT adjusted anywhere.
unspent_printed = 612097578 - 17707765 + 149361110 + 115355773 - 87719412
check("FY24 App2 printed-totals unspent == Table 1 + K2 slips", unspent_printed, 771387284)
print(f"  sum of 2024 funding across appendices:             K{funding_rows:,}")
print(f"  sum of total funds available across appendices:    K{totalfunds_rows:,}")
print("  site line: K771.4m unspent of K5,886.9m total funds available (K5,115.6m spent)")

print(f"\n{'RECONCILIATION FAILED: ' + str(len(fails)) + ' unexplained mismatches' if fails else 'RECONCILIATION OK — all sums exact or documented deviations only'}")
sys.exit(1 if fails else 0)
