# Zambia CDF Tracker

A public dashboard tracking Zambia's Constituency Development Fund (CDF):
allocations, releases, utilisation, delivered results, and developments —
every figure linked to a named, dated source.

## Layout
- `site/` — the static site Netlify publishes (`index.html` + generated `data.js`)
- `model/` — the tracking model: SQLite database (`cdf.db`), schema, seed and
  feed scripts. See `model/README.md`.

## How updates flow
1. The weekly source check updates `model/cdf.db` (sourced figures only).
2. `python3 model/generate_feed.py site/data.js` regenerates the site's data.
3. Commit + push → Netlify deploys automatically.

`site/data.js` is generated — never edit it by hand.
