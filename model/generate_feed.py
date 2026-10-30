#!/usr/bin/env python3
"""Generate the dashboard's data.js feed from cdf.db.

Usage: python3 generate_feed.py [out_path ...]
Default out: the live dashboard's data.js (../files/cdf-dashboard/data.js).

Rules:
- A budget year appears in `movement` only when the FULL display set exists
  (released amount + released %, utilisation %, project amount/count/share).
  Partial years stay out, so the page honestly shows "Not published".
- `delivered` tiles come from reported_metrics with status='current' for the
  six tile metrics; presentation text lives in TILE_MAP below.
- meta dates are the generation date (the feed is generated right after a
  source check / database update)."""
import sqlite3, json, sys, pathlib, datetime

HERE = pathlib.Path(__file__).parent
DB = HERE / "cdf.db"
DEFAULT_OUT = HERE.parent / "files" / "cdf-dashboard" / "data.js"

TILE_MAP = [  # (metric, title, desc, plus_suffix)
    ("classroom_blocks_built",       "Classroom blocks built",        "Plus hundreds rehabilitated across constituencies", True),
    ("school_desks_procured",        "School desks procured",         "So no child sits on the floor", True),
    ("health_facilities_built",      "Health facilities built",       "Bringing care closer to families", False),
    ("maternity_annexes_built",      "Maternity annexes",             "Built alongside health facilities", False),
    ("secondary_boarding_bursaries", "Secondary boarding bursaries",  "Split equally between boys and girls", False),
    ("skills_bursaries",             "Skills development bursaries",  "For learners in skills training", False),
]

def fmt_date_long(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"

def main():
    outs = [pathlib.Path(p) for p in sys.argv[1:]] or [DEFAULT_OUT]
    con = sqlite3.connect(DB)
    c = con.cursor()

    today = datetime.date.today()
    today_long = f"{today.day} {today.strftime('%B %Y')}"

    years = [{"year": y, "per": p} for y, p in
             c.execute("SELECT budget_year, per_constituency_m FROM budget_years ORDER BY budget_year")]
    seats = c.execute("""SELECT COUNT(*) FROM constituencies k JOIN delimitation_sets s ON s.id=k.set_id
                         WHERE s.label='current-156'""").fetchone()[0]
    provinces = [{"name": n, "seats": n_seats} for n, n_seats in c.execute(
        """SELECT p.name, COUNT(*) FROM constituencies k
           JOIN provinces p ON p.id=k.province_id JOIN delimitation_sets s ON s.id=k.set_id
           WHERE s.label='current-156' GROUP BY p.name ORDER BY COUNT(*) DESC, p.name ASC""")]

    def metric(name, year=None):
        q = "SELECT value FROM reported_metrics WHERE metric=? AND status='current'"
        args = [name]
        if year is not None:
            q += " AND budget_year=?"
            args.append(year)
        r = c.execute(q, args).fetchone()
        return r[0] if r else None

    movement = {}
    c2 = con.cursor()
    flow_years = [r[0] for r in c.execute(
        "SELECT DISTINCT budget_year FROM disbursements WHERE constituency_id IS NULL AND component='all'").fetchall()]
    for yr in flow_years:
        released = c2.execute("""SELECT amount_m FROM disbursements WHERE budget_year=? AND constituency_id IS NULL
                                AND component='all' ORDER BY id DESC LIMIT 1""", (yr,)).fetchone()[0]
        vals = {
            "released": released,
            "releasedPct": metric("released_pct_of_allocation", yr),
            "util": metric("utilisation_pct", yr),
            "projAmt": metric("community_projects_approved_amount", yr),
            "projCount": metric("community_projects_approved_count", yr),
            "projPct": metric("community_projects_share_of_allocation_pct", yr),
        }
        if all(v is not None for v in vals.values()):
            movement[yr] = {k: (int(v) if float(v).is_integer() else v) for k, v in vals.items()}

    delivered = []
    for mname, title, desc, plus in TILE_MAP:
        v = metric(mname)
        if v is None:
            continue
        v = int(v)
        delivered.append({"value": f"{v:,}{'+' if plus else ''}", "title": title, "desc": desc})

    news = [{"date": fmt_date_long(d), "source": s, "title": t, "text": x}
            for d, s, t, x in c.execute("SELECT item_date, source_label, title, text FROM news_items ORDER BY item_date DESC")]

    data = {
        "meta": {"snapshotDate": today_long, "lastChecked": today_long},
        "years": years, "seats": seats, "provinces": provinces,
        "movement": movement, "delivered": delivered, "news": news,
    }
    body = ("// Zambia CDF Tracker — data file. GENERATED from cdf.db by generate_feed.py.\n"
            "// Do not edit by hand: update the database, then re-run the generator.\n"
            "window.CDF_DATA = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n")
    for o in outs:
        o.write_text(body)
        print("wrote", o)
    con.close()

if __name__ == "__main__":
    main()
