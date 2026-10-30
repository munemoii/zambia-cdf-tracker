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
DEFAULT_OUTS = [HERE.parent / "site" / "data.js",
                HERE.parent.parent / "files" / "cdf-dashboard" / "data.js"]

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
    outs = [pathlib.Path(p) for p in sys.argv[1:]] or DEFAULT_OUTS
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

    import re as _re_news
    def _slugify_news(name):
        s = name.lower().replace("&", "and")
        return _re_news.sub(r"[^a-z0-9]+", "-", s).strip("-")
    news = []
    _used_slugs = set()
    for d, s, t, x, u, nid in c.execute("SELECT ni.item_date, ni.source_label, ni.title, ni.text, src.url, ni.id FROM news_items ni LEFT JOIN sources src ON src.id = ni.source_id ORDER BY ni.item_date DESC, ni.id DESC"):
        slug = _slugify_news(t)
        if slug in _used_slugs:
            slug = f"{slug}-{nid}"
        _used_slugs.add(slug)
        news.append({"date": fmt_date_long(d), "source": s, "title": t, "text": x, "url": u,
                     "page": f"developments/{slug}.html"})


    # --- loans & bursaries (the people-facing CDF components) ---
    def _mrow(name):
        return c.execute("SELECT value, unit, as_of, definition_note FROM reported_metrics "
                         "WHERE metric = ? AND status = 'current' ORDER BY as_of DESC LIMIT 1", (name,)).fetchone()
    def _tile(name, title, desc_fmt):
        r = _mrow(name)
        if not r:
            return None
        v, unit, as_of, note = r
        return {"value": f"{v:,.0f}", "title": title, "desc": desc_fmt(as_of)}
    people = {
        "bursaries": [t for t in [
            _tile("secondary_bursary_beneficiaries_cumulative", "Secondary bursary beneficiaries",
                  lambda a: f"All secondary bursaries since 2022 — figure as of {fmt_date_long(a) if a else '2026'}"),
            _tile("skills_beneficiaries_cumulative", "Skills bursary beneficiaries",
                  lambda a: f"All skills development beneficiaries since 2022 — as of {fmt_date_long(a) if a else '2026'}"),
        ] if t],
        "boarding": [t for t in [
            _tile("secondary_boarding_bursaries", "Secondary boarding bursaries",
                  lambda a: "Boarding only — MLGRD, September 2025"),
            _tile("skills_bursaries", "Skills development bursaries",
                  lambda a: "MLGRD, September 2025"),
        ] if t],
        "loans": None,
    }
    _sb, _sk = _mrow("secondary_bursary_beneficiaries_cumulative"), _mrow("skills_beneficiaries_cumulative")
    if _sb and _sk:
        people["bursaryBars"] = [{"label": "Secondary bursaries", "value": _sb[0]},
                                 {"label": "Skills bursaries", "value": _sk[0]}]
    bl = c.execute("SELECT budget_year, loans_due_m, loans_recovered_m, recovery_pct FROM bursaries_loans "
                   "ORDER BY budget_year DESC LIMIT 1").fetchone()
    rec = [{"year": y, "pct": p} for y, p in c.execute(
        "SELECT budget_year, value FROM reported_metrics WHERE metric = 'loan_recovery_pct' AND status = 'current' ORDER BY budget_year")]
    s21 = _mrow("loan_recovery_pct_since_2021")
    if bl:
        people["loans"] = {"year": bl[0], "dueM": bl[1], "recoveredM": bl[2], "recoveryPct": bl[3],
                           "series": rec, "since2021Pct": (s21[0] if s21 else None)}

    # --- utilisation & the rural lens ---
    def _mval(name):
        r = _mrow(name)
        return r[0] if r else None
    _y2025 = next((y for y in years if y["year"] == 2025), None)
    util = {
        "cascade": {"year": 2025,
                    "allocatedM": (round(_y2025["per"] * 156, 1) if _y2025 else None),
                    "releasedM": movement.get(2025, {}).get("released"),
                    "releasedPct": movement.get(2025, {}).get("releasedPct"),
                    "utilisedPct": movement.get(2025, {}).get("util")},
        "ag": {"audited": _mval("projects_total_audited"), "completed": _mval("projects_completed"),
               "notStarted": _mval("projects_not_started"), "unspentM": _mval("unspent_amount"),
               "availableM": 5120},
        "provinces": [],
    }
    for _pid, _pname in c.execute("SELECT id, name FROM provinces ORDER BY name").fetchall():
        _rows = dict(c.execute(
            "SELECT p.status, COUNT(*) FROM projects p JOIN constituencies cc ON cc.id = p.constituency_id "
            "WHERE cc.province_id = ? GROUP BY p.status", (_pid,)).fetchall())
        _total = sum(_rows.values())
        if not _total:
            continue
        _comp = _rows.get("completed", 0)
        _under = _rows.get("ongoing", 0) + _rows.get("in_progress", 0)
        _appr = _rows.get("approved", 0) + _rows.get("funded", 0)
        _ctx = c.execute("SELECT rural_pct, urban_pct FROM province_context WHERE province_id = ?", (_pid,)).fetchone()
        util["provinces"].append({
            "name": _pname, "tracked": _total, "completed": _comp, "underway": _under,
            "approved": _appr, "other": _total - _comp - _under - _appr,
            "completedPct": round(_comp / _total * 100, 1),
            "ruralPct": (_ctx[0] if _ctx else None), "urbanPct": (_ctx[1] if _ctx else None)})
    util["provinces"].sort(key=lambda x: (x["ruralPct"] is None, -(x["ruralPct"] or 0)))
    _rel = {r[0]: r[1] for r in c.execute("SELECT budget_year, amount_m FROM disbursements WHERE component = 'all'")}
    _cnotes = {2024: "Releases per the Auditor-General's 2024 report — barely half the allocation moved that year.",
               2025: "The last complete year: the full chain is published.",
               2026: "Cumulative releases reported by June 2026 — the year is still running."}
    util["cascadeYears"] = []
    for _y in years:
        _yr = _y["year"]; _alloc = round(_y["per"] * 156, 1); _r = _rel.get(_yr)
        util["cascadeYears"].append({
            "year": _yr, "allocatedM": _alloc, "releasedM": _r,
            "releasedPct": (movement.get(_yr, {}).get("releasedPct") or (round(_r / _alloc * 100) if _r else None)),
            "utilisedPct": (movement.get(_yr, {}).get("util") if _yr == 2025 else None),
            "note": _cnotes.get(_yr, "No release figure published for this year.")})
    util["groups"] = []
    for _label, _test in (("Rural provinces", lambda r: r is not None and r >= 70),
                          ("Urban provinces", lambda r: r is not None and r <= 25),
                          ("In between", lambda r: r is not None and 25 < r < 70)):
        _mem = [p for p in util["provinces"] if _test(p["ruralPct"])]
        _tp = sum(p["tracked"] for p in _mem); _cp = sum(p["completed"] for p in _mem)
        util["groups"].append({"label": _label, "provinces": len(_mem), "projects": _tp,
                               "completed": _cp, "pct": round(_cp / _tp * 100, 1) if _tp else 0})
    import re as _re
    _CATS = [("Water & sanitation", r"water|borehole|reticulation|ablution|toilet|sanitation|hand ?pump|kiosk"),
             ("Health", r"clinic|health|maternity|hospital|mortuary|medical|laborator"),
             ("Education", r"classroom|school|crb|dormitor|desk|teacher|student|library|college|skills centre|textbook"),
             ("Roads & bridges", r"road|bridge|culvert|drainage|footbridge|grading|streetlight|street light"),
             ("Police & security", r"police|security|prison")]
    def _cat(n):
        n = n.lower()
        for _l, _p in _CATS:
            if _re.search(_p, n):
                return _l
        return "Other community works"
    _mix = {}
    for _name, _rural in c.execute(
            "SELECT p.name, pc.rural_pct FROM projects p JOIN constituencies k ON k.id = p.constituency_id "
            "JOIN province_context pc ON pc.province_id = k.province_id").fetchall():
        _grp = "rural" if _rural >= 70 else ("urban" if _rural <= 25 else None)
        if not _grp:
            continue
        _mix.setdefault(_cat(_name), {"rural": 0, "urban": 0})[_grp] += 1
    _rt = sum(v["rural"] for v in _mix.values()); _ut = sum(v["urban"] for v in _mix.values())
    util["typeMix"] = [{"cat": k, "ruralN": v["rural"], "urbanN": v["urban"],
                        "ruralPct": round(v["rural"] / _rt * 100, 1), "urbanPct": round(v["urban"] / _ut * 100, 1)}
                       for k, v in sorted(_mix.items(), key=lambda kv: -(kv[1]["rural"] + kv[1]["urban"]))]

    # --- project tracking (all provinces; "pilot" kept as the Lusaka slice) ---
    projects_block = None
    pilot = None
    proj_rows = c.execute("""SELECT pr.id, pr.name, k.name, pr.ward, pr.component, pr.category,
                                    pr.contractor, pr.budget_m, pr.status, pr.completion_pct,
                                    pr.photo_url, pr.photo_credit, pr.note,
                                    s.publisher, s.title, s.url, pr.funding_year, pv.name
                             FROM projects pr
                             JOIN constituencies k ON k.id = pr.constituency_id
                             JOIN provinces pv ON pv.id = k.province_id
                             LEFT JOIN sources s ON s.id = pr.source_id
                             ORDER BY pv.name, k.name, pr.name""").fetchall()
    if proj_rows:
        from collections import Counter, defaultdict
        import re as _re
        def _slug(nm):
            return _re.sub(r"[^a-z0-9]+", "-", nm.lower().replace("&", "and")).strip("-")
        by_prov = defaultdict(lambda: defaultdict(list))
        for r in proj_rows:
            by_prov[r[17]][r[2]].append({
                "id": r[0], "url": f"projects/{r[0]}-{_slug(r[1])}.html",
                "name": r[1], "ward": r[3], "component": r[4], "category": r[5],
                "contractor": r[6], "budgetM": round(r[7], 4) if r[7] is not None else None,
                "status": r[8], "completionPct": r[9],
                "photo": ({"url": r[10], "credit": r[11]} if r[10] else None),
                "note": r[12],
                "source": {"publisher": r[13], "title": r[14], "url": r[15]},
                "fundingYear": r[16],
            })
        prov_objs = []
        for pname in sorted(by_prov):
            consts = []
            total = 0
            fy = Counter()
            for nm in sorted(by_prov[pname]):
                items = by_prov[pname][nm]
                total += len(items)
                for i in items:
                    if i["fundingYear"]:
                        fy[i["fundingYear"]] += 1
                consts.append({"name": nm, "url": f"constituencies/{_slug(nm)}.html", "count": len(items),
                               "budgetM": round(sum(i["budgetM"] or 0 for i in items), 2),
                               "statusCounts": dict(Counter(i["status"] for i in items)),
                               "projects": items})
            prov_objs.append({"name": pname, "province": pname, "totalProjects": total,
                              "fundingYears": {str(y): fy[y] for y in sorted(fy)},
                              "fundingYearKnown": sum(fy.values()),
                              "constituencies": consts})
        prov_objs.sort(key=lambda p: -p["totalProjects"])
        all_fy = Counter(r[16] for r in proj_rows if r[16])
        projects_block = {"provinces": prov_objs, "totalProjects": len(proj_rows),
                          "fundingYears": {str(y): all_fy[y] for y in sorted(all_fy)},
                          "fundingYearKnown": sum(all_fy.values())}
        pilot = next((p for p in prov_objs if p["name"] == "Lusaka"), None)

    data = {
        "meta": {"snapshotDate": today_long, "lastChecked": today_long},
        "years": years, "seats": seats, "provinces": provinces,
        "movement": movement, "delivered": delivered, "news": news, "pilot": pilot, "projects": projects_block, "people": people, "utilisation": util,
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
