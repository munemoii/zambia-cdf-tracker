#!/usr/bin/env python3
"""Build the full Zambia CDF Tracker site from cdf.db.

The machine: every page on the site is generated from the database.
  index.html (maintained page) + data.js (via generate_feed.py) for the
  interactive home, and here: provinces index, one page per province,
  one per pilot constituency, one per tracked project, sitemap, robots.

Run after generate_feed.py. Output goes to ../site/.
"""
import sqlite3, pathlib, re, html, datetime

HERE = pathlib.Path(__file__).parent
SITE = HERE.parent / "site"
BASE = "https://sprightly-sunshine-f93b94.netlify.app"

STATUS = {
    "approved": ("Approved", "#8a6d1a"), "funded": ("Funded", "#33607e"),
    "in_progress": ("In progress", "#b35c12"), "completed": ("Completed", "#1c6b3c"),
    "stalled": ("Stalled", "#a12c2c"), "completed_unused": ("Completed, unused", "#6b4fa1"),
    "unknown": ("Status not stated", "#777"),
}


def slugify(name):
    s = name.lower().replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def project_url(pid, name):
    return f"projects/{pid}-{slugify(name)}.html"


def fmt_m(m):
    if m is None:
        return "—"
    if abs(m) >= 1000:
        v = m / 1000
        return f"K{v:.2f}".rstrip("0").rstrip(".") + "bn"
    return f"K{m:.1f}".rstrip("0").rstrip(".") + "m"


def fmt_kwacha(m):
    if m is None:
        return "Not published"
    k = m * 1_000_000
    if k >= 10_000_000:
        return fmt_m(m)
    return "K" + f"{round(k):,}"


def badge(st):
    label, color = STATUS.get(st, STATUS["unknown"])
    return f'<span class="badge" style="background:{color}">{label}</span>'


def shell(title, desc, prefix, body, og_image=None, crumb=""):
    og = og_image or f"{BASE}/og-card.png"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="color-scheme" content="light dark" />
<title>{html.escape(title)} — Zambia CDF Tracker</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Zambia CDF Tracker">
<meta property="og:title" content="{html.escape(title)} — Zambia CDF Tracker">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{prefix}styles.css?v=15">
</head>
<body>
<div class="flagstripe" aria-hidden="true"><span class="g"></span><span class="r"></span><span class="k"></span><span class="o"></span></div>
<header class="sitehead">
  <a class="wordmark" href="{prefix}index.html">Zambia <em>CDF</em> Tracker</a>
  <nav class="sitenav">
    <a href="{prefix}index.html">Home</a>
    <a href="{prefix}money.html">The Money</a>
    <a href="{prefix}provinces.html">Provinces</a>
    <a href="{prefix}projects.html">Projects</a>
    <a href="{prefix}people.html">Loans &amp; Bursaries</a>
    <a href="{prefix}photos.html">Proof of Delivery</a>
    <a href="{prefix}scenario.html">2027 Scenario</a>
    <a href="{prefix}developments.html">Developments</a>
  </nav>
</header>
<div class="pageband"><div class="pageband-in">
{crumb}
<h1>{html.escape(title)}</h1>
<p class="bandsub">{html.escape(desc)}</p>
</div></div>
<main class="pagewrap">
{body}
</main>
<footer class="sitefoot">
  <p>Generated from the Zambia CDF Tracker database — every figure traces to a published source, listed on each page. Province boundaries: geoBoundaries (CC BY 4.0).</p>
  <p><a href="{prefix}index.html">Back to the dashboard</a></p>
</footer>
</body>
</html>
"""


def crumbs(prefix, items):
    parts = [f'<a href="{prefix}index.html">Home</a>']
    for label, href in items:
        parts.append(f'<a href="{prefix}{href}">{html.escape(label)}</a>' if href else html.escape(label))
    return '<nav class="crumbs">' + " › ".join(parts) + "</nav>"


# Freely licensed place imagery (Wikimedia Commons, CC BY-SA 4.0) — atmosphere,
# clearly captioned as the place, never presented as a project photo.
PLACE_MEDIA = {
    ("province", "Lusaka"): {
        "url": "/photos/downtown-lusaka.jpg",
        "caption": "Downtown Lusaka",
        "credit": "Photo: Matthew Grollnek — CC BY-SA 4.0, via Wikimedia Commons",
    },
    ("constituency", "Kafue"): {
        "url": "/photos/kafue-river.jpg",
        "caption": "The Kafue River, seen from the Kafue River Bridge",
        "credit": "Photo: Munahampondela — CC BY-SA 4.0, via Wikimedia Commons",
    },
    ("constituency", "Chongwe"): {
        "url": "/photos/nkwashi-dam.jpg",
        "caption": "Nkwashi Dam, Chongwe",
        "credit": "Photo: Daka Eric — CC BY-SA 4.0, via Wikimedia Commons",
    },
    ("constituency", "Rufunsa"): {
        "url": "/photos/rufunsa-classrooms-opening.jpg",
        "caption": "New CDF classroom blocks opened in Rufunsa District — Mwachilele, Ebenezer and Chaola primary schools",
        "credit": "Photo: Rufunsa Town Council",
    },
    ("constituency", "Chilanga"): {
        "url": "/photos/chilanga-classrooms-handover.jpg",
        "caption": "Classroom blocks handed over in Chilanga, May 2026 — Lusaka West Day Secondary, Sekelela Community and St Michael's Secondary schools",
        "credit": "Photo: Chilanga Town Council",
    },
}


def place_media_html(kind, name):
    m = PLACE_MEDIA.get((kind, name))
    if not m:
        return ""
    return (f'<figure class="place-media"><img src="{html.escape(m["url"])}" alt="{html.escape(m["caption"])}" loading="lazy">'
            f'<figcaption>{html.escape(m["caption"])} · {html.escape(m["credit"])}</figcaption></figure>')


def main():
    con = sqlite3.connect(HERE / "cdf.db")
    c = con.cursor()
    today = datetime.date.today().strftime("%d %B %Y")

    years = c.execute("SELECT budget_year, per_constituency_m FROM budget_years ORDER BY budget_year").fetchall()
    rate = {y: r for y, r in years}
    latest_year = max(rate)

    provinces = c.execute("""
        SELECT p.id, p.name, COUNT(k.id) FROM provinces p
        JOIN constituencies k ON k.province_id = p.id
        JOIN delimitation_sets s ON s.id = k.set_id AND s.label = 'current-156'
        GROUP BY p.id ORDER BY p.name""").fetchall()

    projects = c.execute("""
        SELECT pr.id, pr.name, pr.ward, pr.component, pr.category, pr.contractor,
               pr.budget_m, pr.status, pr.completion_pct, pr.photo_url, pr.photo_credit,
               pr.note, k.name, k.id, pv.name, s.publisher, s.title, s.url, pr.funding_year
        FROM projects pr
        JOIN constituencies k ON k.id = pr.constituency_id
        JOIN provinces pv ON pv.id = k.province_id
        LEFT JOIN sources s ON s.id = pr.source_id
        ORDER BY pv.name, k.name, pr.name""").fetchall()

    by_province_const = {}
    for pr in projects:
        by_province_const.setdefault(pr[14], {}).setdefault(pr[12], []).append(pr)

    (SITE / "provinces").mkdir(exist_ok=True)
    (SITE / "constituencies").mkdir(exist_ok=True)
    (SITE / "projects").mkdir(exist_ok=True)

    urls = [f"{BASE}/", f"{BASE}/provinces.html", f"{BASE}/money.html", f"{BASE}/projects.html", f"{BASE}/people.html", f"{BASE}/photos.html", f"{BASE}/scenario.html", f"{BASE}/developments.html"]

    # ---------- provinces index ----------
    cards = []
    for pid, pname, seats in provinces:
        tracked = sum(len(v) for v in by_province_const.get(pname, {}).values())
        sub = f"{tracked} projects tracked so far" if tracked else "Project tracking in a later phase"
        cards.append(f"""<a class="pcard" href="provinces/{slugify(pname)}.html">
          <h3>{html.escape(pname)}</h3>
          <p>{seats} constituencies · {fmt_m(seats * rate[latest_year])} in {latest_year}</p>
          <p class="pcard-sub">{sub}</p>
        </a>""")
    sc_rows = []
    for pid, pname, seats in provinces:
        _items = [pr for v in by_province_const.get(pname, {}).values() for pr in v]
        _covered = sum(1 for v in by_province_const.get(pname, {}).values() if v)
        _n = len(_items)
        if not _n:
            continue
        _amt = round(100 * sum(1 for pr in _items if pr[6] is not None) / _n)
        _fy = round(100 * sum(1 for pr in _items if pr[18]) / _n)
        _comp = round(100 * sum(1 for pr in _items if pr[7] == "completed") / _n)
        sc_rows.append((_covered / seats, pname, seats, _covered, _n, _amt, _fy, _comp))
    sc_rows.sort(reverse=True)
    sc_html = "".join(
        f'<tr><td>{html.escape(pn)}</td><td>{cov} of {st}</td><td>{n}</td><td>{amt}%</td><td>{fy}%</td><td>{comp}%</td></tr>'
        for _r, pn, st, cov, n, amt, fy, comp in sc_rows)
    body = f"""<p class="plede">CDF allocates equally per constituency — a province's share is its constituency count times the national rate ({fmt_m(rate[latest_year])} per constituency in {latest_year}).</p>
<div class="pgrid">{''.join(cards)}</div>
<h2 class="phead" style="margin-top:34px">The publishing scorecard</h2>
<p class="plede">How much of each province's CDF record is actually public. This measures the <b>record</b>, not delivery: a low score means the councils publish little, not that nothing was built. It is the gap this tracker exists to close.</p>
<div class="card"><table class="mtable"><thead><tr><th>Province</th><th>Constituencies with published projects</th><th>Projects tracked</th><th>With amounts</th><th>With funding year</th><th>Shown completed</th></tr></thead><tbody>{sc_html}</tbody></table></div>"""
    (SITE / "provinces.html").write_text(
        shell("Provinces", "CDF allocations and project tracking for all ten Zambian provinces.", "", body))
    urls.append(f"{BASE}/provinces.html")

    # ---------- province pages ----------
    for pid, pname, seats in provinces:
        consts = c.execute("""
            SELECT k.name FROM constituencies k
            JOIN delimitation_sets s ON s.id = k.set_id AND s.label = 'current-156'
            WHERE k.province_id = ? ORDER BY k.name""", (pid,)).fetchall()
        tracked_here = by_province_const.get(pname, {})
        rows = "".join(
            f"<tr data-year=\"{y}\"><td>{y}</td><td>{fmt_m(r)}</td><td>{fmt_m(r * seats)}</td></tr>" for y, r in years)
        pills = '<button type="button" class="ypill pyear" data-y="all" aria-pressed="true">All years</button>' + "".join(
            f'<button type="button" class="ypill pyear" data-y="{y}" data-r="{r}" aria-pressed="false">{y}</button>' for y, r in years)
        year_counts = {}
        unknown_counts = {}
        for _cs in tracked_here.values():
            for _pr in _cs:
                _cn, _fy = _pr[12], _pr[18]
                if _fy:
                    year_counts.setdefault(_fy, {}).setdefault(_cn, 0)
                    year_counts[_fy][_cn] += 1
                else:
                    unknown_counts[_cn] = unknown_counts.get(_cn, 0) + 1
        import json as _json
        pv_data = {"totalAll": sum(len(v) for v in tracked_here.values()),
                   "years": {str(y): {"total": sum(d.values()), "byConst": d} for y, d in sorted(year_counts.items())},
                   "unknown": sum(unknown_counts.values())}
        sum_rate = sum(r for _y, r in years)
        yr_range = f"{years[0][0]}–{years[-1][0]}"
        pv_script = """<script>
(function(){
  var seats = __SEATS__, sumRate = __SUMRATE__, PV = __PVDATA__;
  function fm(m){ if(m>=1000){ return 'K'+(m/1000).toFixed(2).replace(/\\.?0+$/,'')+'bn'; } var v=Math.round(m*10)/10; return 'K'+(v%1===0 ? v.toFixed(0) : String(v))+'m'; }
  var alloc=document.getElementById('pvAlloc'), allocYr=document.getElementById('pvAllocYr'), per=document.getElementById('pvPer'),
      proj=document.getElementById('pvProj'), projLbl=document.getElementById('pvProjLbl'), note=document.getElementById('pvProjNote');
  function setChips(y, yd){
    document.querySelectorAll('.cchip[data-const]').forEach(function(ch){
      var badge = ch.querySelector('.cnt'); if(!badge) return;
      var nm = ch.getAttribute('data-const');
      var n = (y==='all') ? parseInt(badge.getAttribute('data-all')||'0',10) : ((yd && yd.byConst && yd.byConst[nm]) || 0);
      badge.textContent = n + ' projects';
      badge.style.display = n ? '' : 'none';
    });
  }
  function setYear(y, r){
    var yd = (y==='all') ? null : (PV.years[String(y)] || {total:0, byConst:{}});
    if(alloc) alloc.textContent = fm(seats * (y==='all' ? sumRate : r));
    if(allocYr) allocYr.textContent = (y==='all') ? 'allocated __YRRANGE__' : (y + ' allocation');
    if(per) per.textContent = fm(y==='all' ? sumRate : r);
    if(proj) proj.textContent = (y==='all') ? PV.totalAll : yd.total;
    if(projLbl) projLbl.textContent = (y==='all') ? 'projects tracked · all years' : ('projects · ' + y + ' funding year');
    if(note) note.textContent = (y!=='all' && PV.unknown) ? ('A further ' + PV.unknown + ' tracked projects in this province have no published funding year, so they count under All years only.') : '';
    setChips(y, yd);
    document.querySelectorAll('.pyear').forEach(function(b){ b.setAttribute('aria-pressed', b.getAttribute('data-y')==String(y) ? 'true' : 'false'); });
    document.querySelectorAll('tr[data-year]').forEach(function(tr){ tr.classList.toggle('yr-on', tr.getAttribute('data-year')==String(y)); });
  }
  document.querySelectorAll('.pyear').forEach(function(b){ b.addEventListener('click', function(){ setYear(b.getAttribute('data-y'), parseFloat(b.getAttribute('data-r')||'0')); }); });
  setYear('all', 0);
})();
</script>""".replace("__SEATS__", str(seats)).replace("__SUMRATE__", str(sum_rate)).replace("__PVDATA__", _json.dumps(pv_data)).replace("__YRRANGE__", yr_range)
        chips = []
        for (cname,) in consts:
            n = len(tracked_here.get(cname, []))
            if n:
                chips.append(f'<a class="cchip" data-const="{html.escape(cname)}" href="../constituencies/{slugify(cname)}.html">{html.escape(cname)} <span class="cnt" data-all="{n}">{n} projects</span><span class="arr" aria-hidden="true">›</span></a>')
            else:
                chips.append(f'<a class="cchip" data-const="{html.escape(cname)}" href="../constituencies/{slugify(cname)}.html">{html.escape(cname)}<span class="arr" aria-hidden="true">›</span></a>')
        total_tracked = sum(len(v) for v in tracked_here.values())
        if total_tracked:
            pilot_note = f'<p class="plede">{total_tracked} CDF projects in this province are tracked project-by-project — tap a constituency. The year switcher above splits <b>both</b> the money and the project counts: pick a year to see that funding year alone, or All years for the full record.</p>'
        else:
            pilot_note = '<p class="plede">Project-level tracking is rolling out province by province. Constituencies here light up as the published council lists for them are loaded.</p>'
        body = place_media_html("province", pname) + f"""<div class="years" role="group" aria-label="Choose budget year" style="margin-top:4px">
  <span class="label">Budget year</span>
  {pills}
</div>
<div class="statrow">
  <div class="stat"><b>{seats}</b><span>constituencies</span></div>
  <div class="stat"><b id="pvAlloc">{fmt_m(seats * sum_rate)}</b><span id="pvAllocYr">allocated {yr_range}</span></div>
  <div class="stat"><b id="pvPer">{fmt_m(sum_rate)}</b><span>per constituency</span></div>
  <div class="stat"><b id="pvProj">{total_tracked}</b><span id="pvProjLbl">projects tracked · all years</span></div>
</div>
<p class="plede" id="pvProjNote"></p>
{pilot_note}
<h2 class="phead">Constituencies</h2>
<div class="cchips">{''.join(chips)}</div>
<h2 class="phead">Allocations by year</h2>
<div class="card"><table class="mtable"><thead><tr><th>Year</th><th>Per constituency</th><th>Province total</th></tr></thead><tbody>{rows}</tbody></table></div>
{pv_script}"""
        (SITE / "provinces" / f"{slugify(pname)}.html").write_text(shell(
            f"{pname} Province", f"CDF in {pname}: {seats} constituencies, {fmt_m(seats * rate[latest_year])} in {latest_year}, {total_tracked} projects tracked.",
            "../", body, crumb=crumbs("../", [("Provinces", "provinces.html"), (pname, None)])))
        urls.append(f"{BASE}/provinces/{slugify(pname)}.html")

    # ---------- constituency + project pages ----------
    for pname, consts in by_province_const.items():
        for cname, items in consts.items():
            known = [i for i in items if i[6] is not None]
            fy_known = sum(1 for i in items if i[18])
            fy_txt = f" Funding year is published for {fy_known} of {len(items)}." if fy_known else ""
            total_b = sum(i[6] for i in items if i[6] is not None)
            from collections import Counter
            sc = Counter(i[7] for i in items)
            status_line = " · ".join(f"{STATUS.get(k, STATUS['unknown'])[0]}: {v}" for k, v in sorted(sc.items()))
            def _card(pr):
                photo = f'<img loading="lazy" src="{html.escape(pr[9])}" alt="">' if pr[9] else ""
                return f"""<a class="pcard proj" href="../{project_url(pr[0], pr[1])}">
                  {photo}
                  <h3>{html.escape(pr[1])}</h3>
                  <p>{html.escape(pr[2] or '')}{' · ' if pr[2] else ''}{html.escape(pr[4] or '')}</p>
                  <p class="pcard-sub">{fmt_kwacha(pr[6])} · {STATUS.get(pr[7], STATUS['unknown'])[0]}</p>
                </a>"""
            from collections import defaultdict as _dd
            _groups = _dd(list)
            for _pr in items:
                _groups[_pr[18]].append(_pr)
            _order = sorted((y for y in _groups if y), reverse=True) + ([None] if None in _groups else [])
            if len(_order) > 1:
                cards_html = "".join(
                    f'<h3 class="ghead">{"%d CDF" % y if y else "Funding year not published"} — {len(_groups[y])} projects</h3><div class="pgrid">{"".join(_card(pr) for pr in _groups[y])}</div>'
                    for y in _order)
            else:
                cards_html = f'<div class="pgrid">{"".join(_card(pr) for pr in items)}</div>'
            _pairs = {(pr[15], pr[16]) for pr in items}
            _tl = [(t or "") for _p, t in _pairs]
            def _has(*ws):
                return any(any(w in t.lower() for w in ws) for t in _tl)
            _kinds = []
            if _has("approved", "approval"): _kinds.append("approval lists")
            if _has("commission", "handover", "handed over"): _kinds.append("commissioning / handover reports")
            if _has("minutes"): _kinds.append("CDFC minutes")
            if _has("newsletter"): _kinds.append("council newsletters")
            if _has("catalogue", "database", "project list", "projects list", "list of"): _kinds.append("published project lists")
            if _has("tender", "zppa", "e-gp", "invitation for bids"): _kinds.append("tender notices")
            if not _kinds: _kinds.append("council and news reports")
            record_line = f"Record: based on {', '.join(_kinds)}."
            if "approval lists" not in _kinds and sc.get("completed") and not sc.get("approved"):
                record_line += " No approval list has been published for this constituency — the public record here starts at handover."
            body = place_media_html("constituency", cname) + f"""<p class="plede">{html.escape(pname)} Province · {len(items)} published CDF projects tracked across all published years · {fmt_kwacha(total_b) if known else 'per-project amounts not published'} in published budgets ({len(known)} of {len(items)} projects publish amounts).{fy_txt}</p>
<p class="plede">{html.escape(status_line)}</p>
<p class="plede">{html.escape(record_line)}</p>
{cards_html}"""
            (SITE / "constituencies" / f"{slugify(cname)}.html").write_text(shell(
                f"{cname} constituency", f"{len(items)} CDF projects tracked in {cname}, {pname}: budgets, status, contractors and sources.",
                "../", body, crumb=crumbs("../", [("Provinces", "provinces.html"), (pname, f"provinces/{slugify(pname)}.html"), (cname, None)])))
            urls.append(f"{BASE}/constituencies/{slugify(cname)}.html")

            for pr in items:
                (pid_, name, ward, comp, cat, contractor, budget_m, status, pct,
                 photo_url, photo_credit, note, cname2, _kid, pvname,
                 spub, stitle, surl, fy) = pr
                facts = [
                    ("Status", STATUS.get(status, STATUS["unknown"])[0] + (f" · {pct:g}% complete" if pct else "")),
                    ("Budget", fmt_kwacha(budget_m)),
                    ("Funding year", str(fy) if fy else "Not published"),
                    ("Ward", ward or "—"), ("Category", cat or "—"),
                    ("Component", (comp or "—").title()), ("Contractor", contractor or "—"),
                    ("Constituency", cname2), ("Province", pvname),
                ]
                fact_html = "".join(f"<div><b>{k}</b>{html.escape(str(v))}</div>" for k, v in facts)
                photo_html = (f'<figure class="pfig"><img src="{html.escape(photo_url)}" alt="Photo of {html.escape(name)}">'
                              f'<figcaption>Photo: {html.escape(photo_credit or "")}</figcaption></figure>' if photo_url else "")
                note_html = f'<p class="plede">{html.escape(note)}</p>' if note else ""
                source_html = (f'<div class="card srccard"><h2 class="phead">Source</h2><p>{html.escape(spub or "")}'
                               + (f' — {html.escape(stitle)}' if stitle else "")
                               + (f'<br><a href="{html.escape(surl)}" target="_blank" rel="noopener">View the published source</a>' if surl else "")
                               + "</p></div>") if spub else ""
                body = f"""<p class="plede">{badge(status)}&nbsp; {html.escape(cname2)}, {html.escape(pvname)} Province</p>
{photo_html}
<div class="card"><div class="factgrid">{fact_html}</div></div>
{note_html}
{source_html}"""
                (SITE / "projects" / f"{pr[0]}-{slugify(name)}.html").write_text(shell(
                    name, f"CDF project in {cname2}, {pvname}: {STATUS.get(status, STATUS['unknown'])[0]}, budget {fmt_kwacha(budget_m)}. Source: {spub or 'published list'}.",
                    "../", body, og_image=photo_url or None,
                    crumb=crumbs("../", [("Provinces", "provinces.html"), (pvname, f"provinces/{slugify(pvname)}.html"), (cname2, f"constituencies/{slugify(cname2)}.html"), (name, None)])))
                urls.append(f"{BASE}/{project_url(pr[0], pr[1])}")

    # ---------- constituency pages for constituencies with no tracked projects yet ----------
    covered = {(pn, cn) for pn, cs in by_province_const.items() for cn in cs}
    all_consts = c.execute("""
        SELECT p.name, k.name FROM constituencies k
        JOIN provinces p ON p.id = k.province_id
        JOIN delimitation_sets s ON s.id = k.set_id AND s.label = 'current-156'
        ORDER BY p.name, k.name""").fetchall()
    for pname, cname in all_consts:
        if (pname, cname) in covered:
            continue
        body = place_media_html("constituency", cname) + f"""<p class="plede">{html.escape(pname)} Province · project-level tracking has not reached this constituency yet.</p>
<div class="card"><h2 class="phead" style="margin-top:0">The publishing gap is part of the record</h2>
<p>{html.escape(cname)} receives the same CDF allocation as every constituency — {fmt_m(rate[latest_year])} in {latest_year}. What its council has not yet published, in any list we can verify, is which projects that money is funding. This page will fill in as soon as a publishable list exists; the weekly check watches for one.</p>
<p><a href="../provinces/{slugify(pname)}.html">See {html.escape(pname)} Province — allocations by year and all its constituencies</a></p></div>"""
        (SITE / "constituencies" / f"{slugify(cname)}.html").write_text(shell(
            f"{cname} constituency", f"CDF in {cname}, {pname}: {fmt_m(rate[latest_year])} allocated in {latest_year}; project-level tracking has not reached this constituency yet — the publishing gap is part of the record.",
            "../", body, crumb=crumbs("../", [("Provinces", "provinces.html"), (pname, f"provinces/{slugify(pname)}.html"), (cname, None)])))
        urls.append(f"{BASE}/constituencies/{slugify(cname)}.html")

    # ---------- development articles ----------
    import datetime as _dt
    def _fmt_date_long(iso):
        d = _dt.date.fromisoformat(iso)
        return f"{d.day} {d.strftime('%B %Y')}"
    (SITE / "developments").mkdir(exist_ok=True)
    _used_slugs = set()
    for item_date, source_label, ntitle, ntext, nid, spub, stitle, surl in c.execute(
            "SELECT ni.item_date, ni.source_label, ni.title, ni.text, ni.id, src.publisher, src.title, src.url "
            "FROM news_items ni LEFT JOIN sources src ON src.id = ni.source_id ORDER BY ni.item_date DESC, ni.id DESC"):
        slug = slugify(ntitle)
        if slug in _used_slugs:
            slug = f"{slug}-{nid}"
        _used_slugs.add(slug)
        paras = [p.strip() for p in ntext.split("\n\n") if p.strip()]
        body = f"<p class=\"plede\">{_fmt_date_long(item_date)} · {html.escape(source_label)}</p>\n"
        body += "\n".join(f"<p>{html.escape(p)}</p>" for p in paras)
        if surl:
            body += f"\n<p class=\"chart-note\">Source: <a href=\"{html.escape(surl)}\" target=\"_blank\" rel=\"noopener\">{html.escape(spub or source_label)}</a>{' — ' + html.escape(stitle) if stitle else ''}</p>"
        body += "\n<p><a href=\"../developments.html\">← All developments</a></p>"
        short = ntitle if len(ntitle) <= 60 else ntitle[:57] + "…"
        (SITE / "developments" / f"{slug}.html").write_text(shell(
            ntitle, (paras[0][:155] if paras else ntitle), "../", body,
            crumb=crumbs("../", [("Developments", "developments.html"), (short, None)])))
        urls.append(f"{BASE}/developments/{slug}.html")

    # ---------- sitemap + robots ----------
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{u}</loc></url>" for u in dict.fromkeys(urls)]
    sm.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(sm))
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")

    n_const = len(list((SITE / "constituencies").glob("*.html")))
    print(f"built: 1 provinces index, {len(provinces)} province pages, "
          f"{n_const} constituency pages, "
          f"{len(projects)} project pages, sitemap {len(set(urls))} urls")
    con.close()


if __name__ == "__main__":
    main()
