#!/usr/bin/env python3
"""Generic per-province CDF project ingest.

Reads model/expansion/<slug>/projects.csv + sources.csv (Lusaka pilot schema),
validates hard, and (with --commit) inserts into model/cdf.db.
Conventions (from the live DB): projects.constituency_id -> constituencies.id
(set_id=1), amounts stored as budget_m = kwacha / 1e6.
Dry-run by default. Constituency names must match the ECZ set for the province;
categories/statuses from the fixed vocabularies; sources matched by URL.
"""
import csv, sqlite3, sys, os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(ROOT, "cdf.db")
CATS = {"administration", "education", "equipment", "health", "infrastructure",
        "markets", "recreation", "roads", "sanitation", "security", "water"}
STATUSES = {"completed", "ongoing", "approved", "stalled"}
COMPONENTS = {"community", "empowerment", "bursary", "admin", "administration", ""}

def main():
    slug = sys.argv[1]
    commit = "--commit" in sys.argv
    folder = os.path.join(ROOT, "expansion", slug)
    con = sqlite3.connect(DB)
    prov = con.execute("SELECT id, name FROM provinces WHERE lower(replace(name,'-',''))=?",
                       (slug.replace("-", ""),)).fetchone()
    if not prov:
        sys.exit(f"no province matches slug {slug}")
    pid, pname = prov
    const_ids = {r[1]: r[0] for r in con.execute(
        "SELECT id, name FROM constituencies WHERE set_id=1 AND province_id=?", (pid,))}
    existing_src_by_url = {r[1]: r[0] for r in con.execute("SELECT id, url FROM sources")}
    existing_proj = {(r[0].strip().lower(), r[1]) for r in con.execute(
        "SELECT p.name, c.name FROM projects p JOIN constituencies c ON c.id=p.constituency_id")}

    with open(os.path.join(folder, "sources.csv"), newline="", encoding="utf-8") as f:
        src_rows = list(csv.DictReader(f))
    src_key_to_row, problems = {}, []
    for s in src_rows:
        if not s["url"].startswith("http"):
            problems.append(f"source {s['source_key']}: bad url")
        src_key_to_row[s["source_key"]] = s

    with open(os.path.join(folder, "projects.csv"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ok, seen = [], set()
    for i, r in enumerate(rows, 1):
        tag = f"row {i} ({r.get('name','?')[:40]})"
        if r["constituency"] not in const_ids:
            problems.append(f"{tag}: constituency '{r['constituency']}' not in {pname} ECZ set"); continue
        if r["category"] not in CATS:
            problems.append(f"{tag}: bad category '{r['category']}'"); continue
        if r["status"] not in STATUSES:
            problems.append(f"{tag}: bad status '{r['status']}'"); continue
        if r["component"] not in COMPONENTS:
            problems.append(f"{tag}: bad component '{r['component']}'"); continue
        if r["source_key"] not in src_key_to_row:
            problems.append(f"{tag}: unknown source_key '{r['source_key']}'"); continue
        amt = (r["budget_kwacha"] or "").replace(",", "").strip()
        if amt:
            try: float(amt)
            except ValueError:
                problems.append(f"{tag}: non-numeric budget '{r['budget_kwacha']}'"); continue
        key = (r["name"].strip().lower(), r["constituency"])
        if key in existing_proj:
            problems.append(f"{tag}: already in DB (duplicate)"); continue
        if key in seen:
            problems.append(f"{tag}: duplicate within file"); continue
        seen.add(key)
        ok.append(r)
    per_const = {}
    for r in ok:
        per_const[r["constituency"]] = per_const.get(r["constituency"], 0) + 1
    print(json.dumps({"province": pname, "rows_in_file": len(rows), "rows_ok": len(ok),
                      "problems": problems, "per_constituency": per_const}, indent=1))
    if problems or not commit:
        print("DRY RUN — nothing written" if not problems else "VALIDATION FAILED — nothing written")
        return
    key_to_id = {}
    for s in src_rows:
        if s["url"] in existing_src_by_url:
            key_to_id[s["source_key"]] = existing_src_by_url[s["url"]]
        else:
            cur = con.execute("INSERT INTO sources (publisher, title, url, published_date, note) VALUES (?,?,?,?,?)",
                              (s["publisher"], s["title"], s["url"], s["published_date"] or None, None))
            key_to_id[s["source_key"]] = cur.lastrowid
    for r in ok:
        amt = (r["budget_kwacha"] or "").replace(",", "").strip()
        con.execute("""INSERT INTO projects (name, constituency_id, ward, component, category, contractor,
                       budget_m, disbursed_m, status, completion_pct, start_date, target_date,
                       source_id, note, photo_url, photo_credit, funding_year)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (r["name"].strip(), const_ids[r["constituency"]], r["ward"] or None,
                     {"admin": "administration"}.get(r["component"], r["component"] or "community"),
                     r["category"], r["contractor"] or None,
                     (float(amt) / 1e6) if amt else None, None, r["status"],
                     int(r["completion_pct"]) if (r["completion_pct"] or "").strip().isdigit() else None,
                     None, None, key_to_id[r["source_key"]], None,
                     r["photo_url"] or None, r["photo_credit"] or None, None))
    con.commit()
    print(f"COMMITTED {len(ok)} projects for {pname}")

if __name__ == "__main__":
    main()
