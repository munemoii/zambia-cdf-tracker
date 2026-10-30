-- Zambia CDF Tracking Model — Phase 1 schema (SQLite)
-- Design rules:
--  * Every figure links to a row in `sources`. No source, no record.
--  * Money amounts are in K millions unless a column name says otherwise.
--  * Constituency sets are versioned (delimitation_sets) so the 156 -> 226
--    change never rewrites history.
--  * Conflicting published figures coexist in reported_metrics with a status;
--    they are never silently merged.

CREATE TABLE IF NOT EXISTS sources (
  id             INTEGER PRIMARY KEY,
  publisher      TEXT NOT NULL,
  title          TEXT,
  url            TEXT,
  published_date TEXT,               -- as precise as known, e.g. 2026-10-26 or 2025-09
  note           TEXT
);

CREATE TABLE IF NOT EXISTS provinces (
  id   INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS delimitation_sets (
  id    INTEGER PRIMARY KEY,
  label TEXT UNIQUE NOT NULL,        -- e.g. current-156, delimitation-2026-226
  note  TEXT
);

CREATE TABLE IF NOT EXISTS constituencies (
  id          INTEGER PRIMARY KEY,
  name        TEXT NOT NULL,
  province_id INTEGER NOT NULL REFERENCES provinces(id),
  set_id      INTEGER NOT NULL REFERENCES delimitation_sets(id),
  council     TEXT,
  note        TEXT,
  UNIQUE (name, set_id)
);

-- National allocation rate per budget year (uniform per constituency by law).
CREATE TABLE IF NOT EXISTS budget_years (
  budget_year        INTEGER PRIMARY KEY,
  per_constituency_m REAL NOT NULL,
  seats_basis        INTEGER NOT NULL,
  total_m            REAL NOT NULL,
  source_id          INTEGER REFERENCES sources(id),
  note               TEXT
);

-- Money actually moving: releases/disbursements, national or per constituency.
CREATE TABLE IF NOT EXISTS disbursements (
  id                INTEGER PRIMARY KEY,
  budget_year       INTEGER,
  constituency_id   INTEGER REFERENCES constituencies(id),  -- NULL = national
  component         TEXT,              -- community / empowerment / bursaries / all
  amount_m          REAL NOT NULL,
  tranche_label     TEXT,
  disbursement_date TEXT,
  source_id         INTEGER REFERENCES sources(id),
  note              TEXT
);

-- Reported rates, counts and cumulative totals that are not money flows.
-- `status`: current = the set the dashboard displays; alternative = a
-- conflicting published set kept for provenance; superseded = replaced.
CREATE TABLE IF NOT EXISTS reported_metrics (
  id              INTEGER PRIMARY KEY,
  metric          TEXT NOT NULL,
  scope           TEXT NOT NULL DEFAULT 'national',
  constituency_id INTEGER REFERENCES constituencies(id),
  budget_year     INTEGER,
  value           REAL,
  unit            TEXT,                -- %, count, K millions, km ...
  as_of           TEXT,
  definition_note TEXT,
  status          TEXT NOT NULL DEFAULT 'current',
  source_id       INTEGER REFERENCES sources(id)
);

-- Project-level tracking (Phase 3 fills this; schema ready now).
CREATE TABLE IF NOT EXISTS projects (
  id              INTEGER PRIMARY KEY,
  name            TEXT NOT NULL,
  constituency_id INTEGER REFERENCES constituencies(id),
  ward            TEXT,
  component       TEXT,
  category        TEXT,                -- classrooms, boreholes, roads ...
  contractor      TEXT,
  budget_m        REAL,
  disbursed_m     REAL,
  status          TEXT,                -- approved/funded/in_progress/completed/stalled/completed_unused
  completion_pct  REAL,
  start_date      TEXT,
  target_date     TEXT,
  source_id       INTEGER REFERENCES sources(id),
  photo_url       TEXT,                -- only when a source shows THIS project
  photo_credit    TEXT,
  note            TEXT
);

CREATE TABLE IF NOT EXISTS bursaries_loans (
  id              INTEGER PRIMARY KEY,
  budget_year     INTEGER,
  constituency_id INTEGER REFERENCES constituencies(id),  -- NULL = national
  loans_due_m     REAL,
  loans_recovered_m REAL,
  recovery_pct    REAL,
  grants_m        REAL,
  source_id       INTEGER REFERENCES sources(id),
  note            TEXT
);

-- Mirror of the dashboard's news feed, so the database is the single source.
CREATE TABLE IF NOT EXISTS news_items (
  id           INTEGER PRIMARY KEY,
  item_date    TEXT,
  source_label TEXT,
  title        TEXT,
  text         TEXT,
  source_id    INTEGER REFERENCES sources(id)
);
