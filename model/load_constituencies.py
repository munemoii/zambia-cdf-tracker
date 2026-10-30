#!/usr/bin/env python3
"""Load constituencies.csv (name,province) into cdf.db under a delimitation set.
Usage: python3 load_constituencies.py [csv_path] [set_label]
Defaults: constituencies.csv, current-156.
Verifies per-province counts against the ECZ totals before committing."""
import csv, sqlite3, sys, pathlib

HERE = pathlib.Path(__file__).parent
csv_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "constituencies.csv"
set_label = sys.argv[2] if len(sys.argv) > 2 else "current-156"

EXPECTED_156 = {"Copperbelt": 22, "Eastern": 20, "Southern": 20, "Western": 19,
                "Central": 15, "Luapula": 15, "Northern": 13, "Lusaka": 12,
                "North-Western": 12, "Muchinga": 8}

rows = list(csv.DictReader(csv_path.open()))
counts = {}
for r in rows:
    counts[r["province"]] = counts.get(r["province"], 0) + 1

if set_label == "current-156":
    assert counts == EXPECTED_156, f"Province count mismatch:\n got {counts}\n expected {EXPECTED_156}"
    assert len(rows) == 156, f"Expected 156 rows, got {len(rows)}"

con = sqlite3.connect(HERE / "cdf.db")
cur = con.cursor()
set_id = cur.execute("SELECT id FROM delimitation_sets WHERE label=?", (set_label,)).fetchone()[0]
prov = {name: pid for pid, name in cur.execute("SELECT id,name FROM provinces")}
cur.execute("DELETE FROM constituencies WHERE set_id=?", (set_id,))
for r in rows:
    cur.execute("INSERT INTO constituencies(name,province_id,set_id) VALUES(?,?,?)",
                (r["name"].strip(), prov[r["province"].strip()], set_id))
con.commit()
print(f"Loaded {len(rows)} constituencies into set '{set_label}':")
for p in sorted(counts):
    print(f"  {p}: {counts[p]}")
con.close()
