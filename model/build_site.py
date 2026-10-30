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
<link rel="stylesheet" href="{prefix}styles.css">
</head>
<body>
<div class="flagstripe" aria-hidden="true"><span class="g"></span><span class="r"></span><span class="k"></span><span class="o"></span></div>
<header class="sitehead">
  <a class="wordmark" href="{prefix}index.html">Zambia <em>CDF</em> Tracker</a>
  <nav class="sitenav">
    <a href="{prefix}index.html">Home</a>
    <a href="{prefix}money.html">The Money</a>
    <a href="{prefix}provinces.html">Provinces</a>
    <a href="{prefix}pilot.html">Lusaka Pilot</a>
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
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/15/Downtown_Lusaka.JPG",
        "caption": "Downtown Lusaka",
        "credit": "Photo: Matthew Grollnek — CC BY-SA 4.0, via Wikimedia Commons",
    },
    ("constituency", "Kafue"): {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/86/Kafue_River_View_From_Kafue_River_Bridge_-_July_2025.jpg",
        "caption": "The Kafue River, seen from the Kafue River Bridge",
        "credit": "Photo: Munahampondela — CC BY-SA 4.0, via Wikimedia Commons",
    },
    ("constituency", "Chongwe"): {
        "url": "https://upload.wikimedia.org/wikipedia/commons/e/ed/Nkwashi_Dam%2C_Chongwe%2C_Lusaka.jpg",
        "caption": "Nkwashi Dam, Chongwe",
        "credit": "Photo: Daka Eric — CC BY-SA 4.0, via Wikimedia Commons",
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
               pr.note, k.name, k.id, pv.name, s.publisher, s.title, s.url
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

    urls = [f"{BASE}/", f"{BASE}/provinces.html", f"{BASE}/money.html", f"{BASE}/pilot.html", f"{BASE}/scenario.html", f"{BASE}/developments.html"]

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
    body = f"""<p class="plede">CDF allocates equally per constituency — a province's share is its constituency count times the national rate ({fmt_m(rate[latest_year])} per constituency in {latest_year}).</p>
<div class="pgrid">{''.join(cards)}</div>"""
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
            f"<tr><td>{y}</td><td>{fmt_m(r)}</td><td>{fmt_m(r * seats)}</td></tr>" for y, r in years)
        chips = []
        for (cname,) in consts:
            n = len(tracked_here.get(cname, []))
            if n:
                chips.append(f'<a class="cchip" href="../constituencies/{slugify(cname)}.html">{html.escape(cname)} <span>{n} projects</span></a>')
            else:
                chips.append(f'<span class="cchip dim">{html.escape(cname)}</span>')
        total_tracked = sum(len(v) for v in tracked_here.values())
        if total_tracked:
            pilot_note = f'<p class="plede">{total_tracked} CDF projects in this province are tracked project-by-project in the pilot — tap a constituency.</p>'
        else:
            pilot_note = '<p class="plede">Project-level tracking rolls out province by province; Lusaka is the pilot. Constituencies here light up as their project lists are loaded.</p>'
        body = place_media_html("province", pname) + f"""<div class="statrow">
  <div class="stat"><b>{seats}</b><span>constituencies</span></div>
  <div class="stat"><b>{fmt_m(seats * rate[latest_year])}</b><span>{latest_year} allocation</span></div>
  <div class="stat"><b>{fmt_m(rate[latest_year])}</b><span>per constituency</span></div>
  <div class="stat"><b>{total_tracked}</b><span>projects tracked</span></div>
</div>
{pilot_note}
<h2 class="phead">Constituencies</h2>
<div class="cchips">{''.join(chips)}</div>
<h2 class="phead">Allocations by year</h2>
<div class="card"><table class="mtable"><thead><tr><th>Year</th><th>Per constituency</th><th>Province total</th></tr></thead><tbody>{rows}</tbody></table></div>"""
        (SITE / "provinces" / f"{slugify(pname)}.html").write_text(shell(
            f"{pname} Province", f"CDF in {pname}: {seats} constituencies, {fmt_m(seats * rate[latest_year])} in {latest_year}, {total_tracked} projects tracked.",
            "../", body, crumb=crumbs("../", [("Provinces", "provinces.html"), (pname, None)])))
        urls.append(f"{BASE}/provinces/{slugify(pname)}.html")

    # ---------- constituency + project pages ----------
    for pname, consts in by_province_const.items():
        for cname, items in consts.items():
            known = [i for i in items if i[6] is not None]
            total_b = sum(i[6] for i in items if i[6] is not None)
            from collections import Counter
            sc = Counter(i[7] for i in items)
            status_line = " · ".join(f"{STATUS.get(k, STATUS['unknown'])[0]}: {v}" for k, v in sorted(sc.items()))
            cards = []
            for pr in items:
                photo = f'<img loading="lazy" src="{html.escape(pr[9])}" alt="">' if pr[9] else ""
                cards.append(f"""<a class="pcard proj" href="../{project_url(pr[0], pr[1])}">
                  {photo}
                  <h3>{html.escape(pr[1])}</h3>
                  <p>{html.escape(pr[2] or '')}{' · ' if pr[2] else ''}{html.escape(pr[4] or '')}</p>
                  <p class="pcard-sub">{fmt_kwacha(pr[6])} · {STATUS.get(pr[7], STATUS['unknown'])[0]}</p>
                </a>""")
            body = place_media_html("constituency", cname) + f"""<p class="plede">{html.escape(pname)} Province · {len(items)} published CDF projects tracked · {fmt_kwacha(total_b) if known else 'per-project amounts not published'} in published budgets ({len(known)} of {len(items)} projects publish amounts)</p>
<p class="plede">{html.escape(status_line)}</p>
<div class="pgrid">{''.join(cards)}</div>"""
            (SITE / "constituencies" / f"{slugify(cname)}.html").write_text(shell(
                f"{cname} constituency", f"{len(items)} CDF projects tracked in {cname}, {pname}: budgets, status, contractors and sources.",
                "../", body, crumb=crumbs("../", [("Provinces", "provinces.html"), (pname, f"provinces/{slugify(pname)}.html"), (cname, None)])))
            urls.append(f"{BASE}/constituencies/{slugify(cname)}.html")

            for pr in items:
                (pid_, name, ward, comp, cat, contractor, budget_m, status, pct,
                 photo_url, photo_credit, note, cname2, _kid, pvname,
                 spub, stitle, surl) = pr
                facts = [
                    ("Status", STATUS.get(status, STATUS["unknown"])[0] + (f" · {pct:g}% complete" if pct else "")),
                    ("Budget", fmt_kwacha(budget_m)),
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

    # ---------- sitemap + robots ----------
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{u}</loc></url>" for u in dict.fromkeys(urls)]
    sm.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(sm))
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")

    print(f"built: 1 provinces index, {len(provinces)} province pages, "
          f"{sum(len(v) for v in by_province_const.values()) and len([1 for p in by_province_const.values() for _ in p])} constituency pages, "
          f"{len(projects)} project pages, sitemap {len(set(urls))} urls")
    con.close()


if __name__ == "__main__":
    main()
