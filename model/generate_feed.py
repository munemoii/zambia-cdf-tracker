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
import sqlite3, json, sys, pathlib, datetime, re

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
    released_by_year = {}
    c2 = con.cursor()
    flow_years = [r[0] for r in c.execute(
        "SELECT DISTINCT budget_year FROM disbursements WHERE constituency_id IS NULL AND component='all'").fetchall()]
    for yr in flow_years:
        released = c2.execute("""SELECT amount_m FROM disbursements WHERE budget_year=? AND constituency_id IS NULL
                                AND component='all' ORDER BY id DESC LIMIT 1""", (yr,)).fetchone()[0]
        released_by_year[yr] = released
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

    # Release figures published without the full movement chain (a 2024
    # release total from the Auditor-General's report, via Zambian
    # Economist; a cumulative mid-year figure
    # for 2026): the Money page glance table shows these in its Released
    # column with the label below, while the flow dashboard stays
    # movement-gated. Update the label when a newer figure supersedes one.
    _released_labels = {
        2024: "Auditor-General's 2024 report, via Zambian Economist",
        2026: "cumulative to June 2026 — the year is still running",
    }
    released_only = {}
    for yr, amt in released_by_year.items():
        if yr in movement:
            continue
        alloc = c.execute("SELECT total_m FROM budget_years WHERE budget_year=?", (yr,)).fetchone()
        if alloc is None:
            continue
        released_only[yr] = {
            "released": (int(amt) if float(amt).is_integer() else amt),
            "releasedPct": round(amt / alloc[0] * 100),
            "label": _released_labels.get(yr, ""),
        }

    # Prove It (roadmap item 3, 2026-11-04): the recorded source behind each
    # year's national release figure — the same disbursements row the flow
    # figures above are read from — so the Money page can print the receipt
    # (publisher, document, date, link) beside the figures it publishes.
    flow_sources = {}
    for yr in flow_years:
        srow = c2.execute("""SELECT s.publisher, s.title, s.published_date, s.url
                             FROM disbursements d LEFT JOIN sources s ON s.id = d.source_id
                             WHERE d.budget_year=? AND d.constituency_id IS NULL AND d.component='all'
                             ORDER BY d.id DESC LIMIT 1""", (yr,)).fetchone()
        if srow and srow[0]:
            flow_sources[str(yr)] = {"publisher": srow[0], "title": srow[1],
                                     "date": srow[2], "url": srow[3]}

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
               "notStarted": _mval("projects_not_started"), "inProgress": _mval("projects_in_progress"), "unspentM": _mval("unspent_amount"),
               # AG FY2024 report, Cross-Cutting §1 (Unspent Funds), Table 1:
               # total funds available K5,886,946,075; expenditure K5,115,558,793;
               # unspent K771,387,282. (The old 5120 was the rounded expenditure
               # total mislabelled as available by a secondary explainer.)
               "availableM": 5886.9, "spentM": 5115.6},
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
    _cnotes = {2024: "Releases per the Auditor-General's 2024 report, via Zambian Economist — barely half the allocation moved that year.",
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
                                    s.publisher, s.title, s.url, pr.funding_year, pv.name,
                                    s.published_date
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
                "source": {"publisher": r[13], "title": r[14], "url": r[15], "date": r[18]},
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

    # --- the tracked record (national status mix for the analytics sections) ---
    _status_counts = dict(c.execute("SELECT status, COUNT(*) FROM projects GROUP BY status").fetchall())
    _rec_total = sum(_status_counts.values())
    record = {
        "total": _rec_total,
        "statuses": _status_counts,
        "completedPct": round(_status_counts.get("completed", 0) / _rec_total * 100, 1) if _rec_total else 0,
        "approvedPct": round((_status_counts.get("approved", 0) + _status_counts.get("funded", 0)) / _rec_total * 100, 1) if _rec_total else 0,
        "withPhoto": c.execute("SELECT COUNT(*) FROM projects WHERE photo_url IS NOT NULL AND photo_url <> ''").fetchone()[0],
        "constituencies": c.execute("SELECT COUNT(DISTINCT constituency_id) FROM projects").fetchone()[0],
        "provinces": c.execute("SELECT COUNT(DISTINCT k.province_id) FROM projects pr JOIN constituencies k ON k.id = pr.constituency_id").fetchone()[0],
    }

    # --- constituency data feed (2026-11-04): per-constituency audit,
    # published and held figures, emitted by this generator as its own
    # slim feed (site/cards.js) and consumed by the Gap Map, so the map
    # does not have to load the full data.js. Same generator, same run,
    # same database as the record block above — the feed can never drift
    # from the figures the pages display. (The public constituency
    # share-card download that first used this feed was removed on
    # 2026-11-04 at Caleb's direction; the feed stays for the Gap Map.)
    # Published buckets follow the site's status mapping: completed
    # includes completed_unused; in progress is ongoing + in_progress;
    # approved includes funded (the paper stage, per the funding rule).
    # Held counts come from the expansion held.csv files — the tracker's
    # held pile — attributed by exact constituency name; rows whose
    # constituency cell is blank or names more than one constituency are
    # left unattributed.
    from collections import Counter as _Counter, defaultdict as _defaultdict
    import csv as _csv, glob as _glob
    def _cslug(nm):
        return re.sub(r"[^a-z0-9]+", "-", nm.lower().replace("&", "and")).strip("-")
    _held = _Counter()
    for _hf in _glob.glob(str(HERE / "expansion" / "*" / "held.csv")):
        with open(_hf, encoding="utf-8", errors="replace", newline="") as _fh:
            for _row in _csv.DictReader(_fh):
                _held[(_row.get("constituency") or "").strip().lower()] += 1
    _pubs = _defaultdict(list)
    for _cid, _pub in c.execute(
            "SELECT pr.constituency_id, s.publisher FROM projects pr "
            "JOIN sources s ON s.id = pr.source_id WHERE s.publisher IS NOT NULL "
            "GROUP BY pr.constituency_id, s.publisher "
            "ORDER BY pr.constituency_id, COUNT(*) DESC, s.publisher ASC"):
        _pubs[_cid].append(_pub)
    cards = {}
    for _cid, _nm, _pv in c.execute(
            "SELECT k.id, k.name, pv.name FROM constituencies k "
            "JOIN provinces pv ON pv.id = k.province_id "
            "JOIN delimitation_sets s ON s.id = k.set_id AND s.label = 'current-156' "
            "ORDER BY pv.name, k.name").fetchall():
        _ag = c.execute(
            "SELECT SUM(approved), SUM(implemented), SUM(in_progress), SUM(not_implemented) "
            "FROM ag_project_status WHERE fy = 2024 AND constituency_id = ?", (_cid,)).fetchone()
        _audit = None
        if _ag and _ag[0] is not None:
            _audit = {"audited": _ag[0], "completed": _ag[1] or 0,
                      "inProgress": _ag[2] or 0, "neverStarted": _ag[3] or 0}
        _sc = dict(c.execute(
            "SELECT status, COUNT(*) FROM projects WHERE constituency_id = ? "
            "GROUP BY status", (_cid,)).fetchall())
        cards[_cslug(_nm)] = {
            "name": _nm, "province": _pv, "audit": _audit,
            "published": {
                "named": sum(_sc.values()),
                "completed": _sc.get("completed", 0) + _sc.get("completed_unused", 0),
                "inProgress": _sc.get("ongoing", 0) + _sc.get("in_progress", 0),
                "approved": _sc.get("approved", 0) + _sc.get("funded", 0),
                "stalled": _sc.get("stalled", 0),
                "notStated": _sc.get("unknown", 0),
                "held": _held.get(_nm.lower(), 0),
            },
            "publishers": _pubs.get(_cid, []),
        }

    data = {
        "meta": {"snapshotDate": today_long, "lastChecked": today_long},
        "years": years, "seats": seats, "provinces": provinces,
        "movement": movement, "releasedOnly": released_only, "flowSources": flow_sources, "delivered": delivered, "news": news, "pilot": pilot, "projects": projects_block, "people": people, "utilisation": util, "record": record,
    }
    body = ("// Zambia CDF Tracker — data file. GENERATED from cdf.db by generate_feed.py.\n"
            "// Do not edit by hand: update the database, then re-run the generator.\n"
            "window.CDF_DATA = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n")
    for o in outs:
        o.write_text(body)
        print("wrote", o)

    cards_body = ("// Zambia CDF Tracker — constituency data feed (Gap Map). GENERATED from cdf.db by generate_feed.py.\n"
                  "// Do not edit by hand: update the database, then re-run the generator.\n"
                  "window.CDF_CARDS = " + json.dumps(cards, indent=1, ensure_ascii=False) + ";\n")
    cards_out = HERE.parent / "site" / "cards.js"
    cards_out.write_text(cards_body)
    print("wrote", cards_out)

    # --- the Publishing League (roadmap item 5, 2026-11-04): councils
    # ranked on the record they THEMSELVES publish, derived entirely from
    # projects -> sources -> publisher. A project is credited to a council
    # only when the publisher string on its source names that council:
    #   * the string's head (before any "(" qualifier or " / " suffix)
    #     is itself a council name — "Chienge Town Council (Ministry of
    #     Local Government and Rural Development, Provincial Local
    #     Government Officer)", "Chipata City Council / MLGRD Eastern
    #     Province", "Kitwe City Council (Facebook page, ...)".
    #   * tender notices a council posted on the national e-procurement
    #     portal — "ZPPA e-GP (Kitwe City Council)" — are the council's
    #     own publications on a national platform, credited to it.
    #   * two recorded judgement calls in _LG_OVERRIDE (see the build
    #     log): a mirror of a council's own social posts is credited to
    #     that council, and a spelling variant is merged.
    # Everything else (Parliament and constituency offices, the ministry
    # and its provincial offices, provincial administrations, ZANIS,
    # news outlets, portal mirrors that name no council) is NOT a
    # council publication: those projects stay out of every council's
    # row and are counted, by publisher class, in `excluded` so the page
    # can state exactly how much of the record councils did not publish.
    import re as _lre
    _LG_OVERRIDE = {
        "findglocal (mirror of Luanshya Municipal Council social posts)":
            "Luanshya Municipal Council",
        "Shangombo Town Council": "Shang'ombo Town Council",
    }
    def _lg_council(pub):
        if pub in _LG_OVERRIDE:
            return _LG_OVERRIDE[pub]
        m = _lre.match(r"^ZPPA e-(?:GP|procurement) \((.+ Council)\)$", pub or "")
        if m:
            return m.group(1)
        head = _lre.split(r"\s\(| / ", pub or "", maxsplit=1)[0].strip()
        if _lre.match(r"^.+ (Town|Municipal|City) Council$", head):
            return head
        return None
    _LG_EXCLUDED_CLASS = {
        "National Assembly of Zambia": "Parliament and constituency offices",
        "National Assembly of Zambia (Committee on Local Government Accounts)": "Parliament and constituency offices",
        "National Assembly of Zambia (Parliament)": "Parliament and constituency offices",
        "Munali Parliamentary Constituency Office (National Assembly constituency office page, mirrored on govserv.org)": "Parliament and constituency offices",
        "Katuba Constituency Information & Publicity Desk (via govserv.org mirror)": "Parliament and constituency offices",
        "Ministry of Local Government and Rural Development - Provincial Local Government Office North-Western": "The ministry and its provincial offices",
        "Ministry of Local Government and Rural Development (MLGRD)": "The ministry and its provincial offices",
        "Ministry of Local Government and Rural Development - Provincial Local Government Officer, Central Province (hosted by Mumbwa Town Council)": "The ministry and its provincial offices",
        "Ministry of Local Government and Rural Development": "The ministry and its provincial offices",
        "Ministry of Local Government and Rural Development (PLGO Western Province) via Limulunga Town Council": "The ministry and its provincial offices",
        "Provincial Local Government Office, Southern Province (via Siavonga Town Council)": "The ministry and its provincial offices",
        "Eastern Province Provincial Administration (ZANIS)": "Provincial administrations and the government news agency (ZANIS)",
        "Lusaka Provincial Administration (ZANIS)": "Provincial administrations and the government news agency (ZANIS)",
        "Northern Provincial Administration": "Provincial administrations and the government news agency (ZANIS)",
        "Lusaka Provincial Administration": "Provincial administrations and the government news agency (ZANIS)",
        "Zambia News and Information Services (ZANIS)": "Provincial administrations and the government news agency (ZANIS)",
        "Africa Press (ZANIS report)": "Provincial administrations and the government news agency (ZANIS)",
        "Muchinga Provincial Administration": "Provincial administrations and the government news agency (ZANIS)",
        "Muchinga Province Provincial Administration (ZANIS)": "Provincial administrations and the government news agency (ZANIS)",
        "ZANIS": "Provincial administrations and the government news agency (ZANIS)",
        "Zambia Monitor (reporting Lusaka City Council statement by Asst PR Manager Nyambe Bulumba)": "News outlets republishing council statements",
        "ZPPA e-procurement via Tender Impulse mirror (notice 13147414)": "Procurement-portal mirrors that name no council",
        "ZPPA e-procurement via Tender Impulse mirror (notice 13146735)": "Procurement-portal mirrors that name no council",
    }
    def _lg_datekey(d):
        if not d:
            return (0, 0, 0)
        parts = d.split("-")
        try:
            y = int(parts[0])
            mo = int(parts[1]) if len(parts) > 1 else 12
            da = int(parts[2]) if len(parts) > 2 else 31
            return (y, mo, da)
        except ValueError:
            return (0, 0, 0)
    _lg = {}
    _lg_excl = {}
    for _pub, _n, _comp, _stn, _fyn, _amn, _latest in c.execute(
            """SELECT s.publisher, COUNT(*),
                      SUM(pr.status IN ('completed', 'completed_unused')),
                      SUM(pr.status IS NOT NULL AND pr.status <> 'unknown'),
                      SUM(pr.funding_year IS NOT NULL),
                      SUM(pr.budget_m IS NOT NULL),
                      NULL
               FROM projects pr JOIN sources s ON s.id = pr.source_id
               GROUP BY s.publisher""").fetchall():
        _cn = _lg_council(_pub)
        if _cn is None:
            _cls = _LG_EXCLUDED_CLASS.get(_pub)
            if _cls is None:
                print("WARNING league: unclassified non-council publisher ->", _pub)
                _cls = "Other national publishers"
            _lg_excl[_cls] = _lg_excl.get(_cls, 0) + _n
            continue
        _e = _lg.setdefault(_cn, {"named": 0, "completed": 0, "statusN": 0,
                                  "fyN": 0, "amtN": 0, "latest": None,
                                  "consts": {}})
        _e["named"] += _n
        _e["completed"] += _comp or 0
        _e["statusN"] += _stn or 0
        _e["fyN"] += _fyn or 0
        _e["amtN"] += _amn or 0
    for _pub, _kname, _date in c.execute(
            """SELECT DISTINCT s.publisher, k.name, s.published_date
               FROM projects pr JOIN sources s ON s.id = pr.source_id
               JOIN constituencies k ON k.id = pr.constituency_id""").fetchall():
        _cn = _lg_council(_pub)
        if _cn is None or _cn not in _lg:
            continue
        _e = _lg[_cn]
        _e["consts"][_kname] = _cslug(_kname)
        if _date and _lg_datekey(_date) > _lg_datekey(_e["latest"]):
            _e["latest"] = _date
    league_rows = []
    for _cn, _e in _lg.items():
        _n = _e["named"]
        _sp = round(100 * _e["statusN"] / _n)
        _yp = round(100 * _e["fyN"] / _n)
        _ap = round(100 * _e["amtN"] / _n)
        league_rows.append({
            "council": _cn, "named": _n, "completed": _e["completed"],
            "statusPct": _sp, "yearPct": _yp, "amountPct": _ap,
            "composite": round((_sp + _yp + _ap) / 3, 1),
            "latest": _e["latest"],
            "constituencies": [{"name": nm, "slug": _e["consts"][nm]}
                               for nm in sorted(_e["consts"])],
        })
    league_rows.sort(key=lambda r: (-r["composite"], -r["named"], r["council"]))
    for _i, _r in enumerate(league_rows, 1):
        _r["rank"] = _i
    # Constituencies with no named projects at all: their councils have
    # published nothing this record could use. Council names are printed
    # only where the tracker's council-watch records ground them.
    _LG_COUNCIL_KNOWN = {"Manyinga": "Manyinga Town Council"}
    _LG_NONE_NOTE = {
        "Manyinga": "The council has published news of CDF work — an "
                    "article on township roads rehabilitated with CDF "
                    "money — but it names no individual projects, so "
                    "nothing from it could be listed.",
    }
    league_none = []
    for _nm, in c.execute(
            """SELECT k.name FROM constituencies k
               JOIN delimitation_sets s ON s.id = k.set_id AND s.label = 'current-156'
               WHERE k.id NOT IN (SELECT DISTINCT constituency_id FROM projects)
               ORDER BY k.name""").fetchall():
        league_none.append({
            "constituency": _nm, "slug": _cslug(_nm),
            "council": _LG_COUNCIL_KNOWN.get(_nm),
            "held": _held.get(_nm.lower(), 0),
            "note": _LG_NONE_NOTE.get(_nm),
        })
    league = {
        "meta": {
            "totalProjects": record["total"],
            "attributed": sum(r["named"] for r in league_rows),
            "unattributed": sum(_lg_excl.values()),
            "councils": len(league_rows),
            "councilCompleted": sum(r["completed"] for r in league_rows),
        },
        "councils": league_rows,
        "excluded": [{"label": k, "projects": v}
                     for k, v in sorted(_lg_excl.items(), key=lambda kv: -kv[1])],
        "nothingYet": league_none,
    }
    league_body = ("// Zambia CDF Tracker — Publishing League data. GENERATED from cdf.db by generate_feed.py.\n"
                   "// Do not edit by hand: update the database, then re-run the generator.\n"
                   "window.CDF_LEAGUE = " + json.dumps(league, indent=1, ensure_ascii=False) + ";\n")
    league_out = HERE.parent / "site" / "league.js"
    league_out.write_text(league_body)
    print("wrote", league_out)

    # --- static-patch: keep the record figures printed in the hand-maintained
    # pages (index.html meta/fallback, read.html guide cards) in step with the
    # database, so a new intake can never leave a stale total behind (Caleb's
    # deep-check direction, 2026-11-01). In-browser values are also hydrated
    # from this feed by app.js; these literals serve crawlers and no-JS reads.
    # A missed pattern prints a WARNING so drift shows up in the run log.
    site_dir = HERE.parent / "site"
    total_s = f"{record['total']:,}"
    patches = [
        (site_dir / "index.html", [
            (r"[\d,]+ projects tracked across all 10 provinces",
             f"{total_s} projects tracked across all 10 provinces"),
            (r"[\d,]+ projects tracked — every figure sourced",
             f"{total_s} projects tracked — every figure sourced"),
            (r'(<b id="recordTotal">)[\d,]+(</b>)',
             rf"\g<1>{total_s}\g<2>"),
        ]),
        (site_dir / "read.html", [
            (r'(<span id="readTotal">)[\d,]+(</span>)',
             rf"\g<1>{total_s}\g<2>"),
            (r'(<span id="readConst">)\d+(</span>)',
             rf"\g<1>{record['constituencies']}\g<2>"),
            (r'(<span id="readCompPct">)\d+(</span>)',
             rf"\g<1>{round(record['completedPct'])}\g<2>"),
        ]),
    ]
    for path, subs in patches:
        if not path.exists():
            print("WARNING static-patch: missing", path)
            continue
        text = path.read_text()
        for pat, rep in subs:
            text, n = re.subn(pat, rep, text)
            if n == 0:
                print("WARNING static-patch: pattern not found in", path.name, "->", pat[:48])
        path.write_text(text)
        print("patched", path)
    con.close()

if __name__ == "__main__":
    main()
