# Zambia CDF Tracking Model — Phase 1

Built 30 October 2026. A SQLite database that holds everything the CDF
dashboard shows today, structured for constituency- and project-level tracking.

## Files
- `schema.sql` — table definitions and the design rules (provenance first)
- `build_db.py` — rebuilds `cdf.db` from scratch and seeds all current data
  (sources, budget years, disbursements, reported metrics, loans, news)
- `load_constituencies.py` — loads a constituency CSV into a delimitation
  set; refuses the 156 set unless per-province counts match ECZ totals exactly
- `constituencies.csv` — the current 156, by province (ECZ-based)
- `constituencies-226.csv` — the full 2026 delimitation set of 226 (ECZ)
- `cdf.db` — the built database

## What's in the database (verified 2026-10-30)
- 10 sources, every figure linked to one
- 6 budget years (2021–2026); rate × seats = total reconciles for all years
- 382 constituencies: 156 current + 226 delimitation, per-province counts
  matching ECZ published totals for both sets
- 5 disbursement records (2024–2026), 32 reported metrics, 1 loans record,
  5 news items — including BOTH conflicting "delivered" sets (Sept 2025 MLGRD
  = `current`, displayed on the dashboard by Caleb's decision; June 2026
  MLGRD briefing = `alternative`, kept for provenance)
- `projects` table is ready and empty — Phase 3 fills it

## Judgement calls recorded in the data
- Itezhi-Tezhi and Chirundu are filed under Southern Province (the ECZ
  electoral assignment), though both districts were administratively moved
  to Central in 2012. Noted on the rows themselves.
- Chama North / Chama South are filed under Eastern, matching ECZ schedules
  after Chama's realignment from Muchinga. Noted on the rows.

## Rebuild / reload
```
python3 build_db.py
python3 load_constituencies.py constituencies.csv current-156
python3 load_constituencies.py constituencies-226.csv delimitation-2026-226
```

## Next (Phase 2)
Generate a JSON feed from cdf.db and rewire the dashboard to read it.
Decision needed from Caleb at that point: Git-based feed (also unlocks
automatic Netlify publishing) vs Supabase.
