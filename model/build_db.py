#!/usr/bin/env python3
"""Build cdf.db from schema.sql and seed it with everything the dashboard
currently shows (migrated 2026-10-30 from data.js + verified research).

Constituencies are loaded separately by load_constituencies.py.
Re-running this script rebuilds cdf.db from scratch (deterministic)."""
import sqlite3, pathlib

HERE = pathlib.Path(__file__).parent
DB = HERE / "cdf.db"
if DB.exists():
    DB.unlink()
con = sqlite3.connect(DB)
con.executescript((HERE / "schema.sql").read_text())
cur = con.cursor()

def src(publisher, title, url, date, note=None):
    cur.execute("INSERT INTO sources(publisher,title,url,published_date,note) VALUES(?,?,?,?,?)",
                (publisher, title, url, date, note))
    return cur.lastrowid

# ---------------------------------------------------------------- sources
S_MLGRD = src("Ministry of Local Government and Rural Development",
              "CDF increase to K40 million: what it means for Zambia's communities",
              "https://www.mlgrd.gov.zm/?p=34032", "2025-09",
              "Allocation history 2021-2026 and the delivered-results set the dashboard tiles display (Caleb's choice, 2026-10-30).")
S_GUIDE = src("Ministry of Local Government and Rural Development",
              "CDF Guidelines", "http://www.lumezicouncil.gov.zm/wp-content/uploads/2026/09/CDF-Guidelines.pdf",
              None, "Component split: 5% admin first, remaining 95% split 60/20/20.")
S_ECZ = src("Electoral Commission of Zambia",
            "2026 Delimitation of Constituencies — Province Summary",
            "https://www.elections.org.zm/wp-content/uploads/20260416-Provincial-Summaries.pdf",
            "2026-04-16", "Province constituency counts (156 current); 226 under the 2026 delimitation.")
S_2025 = src("National reporting of 2025 CDF (compiled for the dashboard)",
             "2025 CDF release and utilisation figures", None, "2025",
             "As reported nationally for the 2025 CDF; reported figures, not audited project-level records.")
S_OZ_JUN = src("Open Zambia",
               "Government releases fresh CDF funds for local projects",
               "https://www.openzambia.com/politics/2026/6/5/government-releases-fresh-cdf-funds-for-local-projects",
               "2026-06-05", "MLGRD briefing by PS Dr Gabriel Pollen: extra K500m release, 2026 disbursements K2.2bn, plus a cumulative delivered set that conflicts with the Sept 2025 MLGRD set.")
S_OZ_FEB = src("Open Zambia",
               "Government disburses K100 million in CDF bursaries",
               "https://www.openzambia.com/lifestyle/2026/2/3/government-disburses-k100-million-in-cdf-bursaries",
               "2026-02-03", "First 2026 bursary tranche; cumulative beneficiary counts use broader definitions than the tiles.")
S_OBS_SEP = src("Zambian Observer",
                "Govt suspends 2026 CDF loans as repayment rate falls to 35 percent",
                "https://zambianobserver.com/govt-suspends-2026-cdf-loans-as-repayment-rate-falls-to-35-percent/",
                "2026-09-29", "Quotes MLGRD Director of Planning and Information Martin Sodala.")
S_OBS_OCT = src("Zambian Observer",
                "State House makes clarifications on FRA and CDF / CDF: Beyond the Budget Cuts",
                "https://zambianobserver.com/state-house-makes-clarifications-on-fra-and-cdf/",
                "2026-10-13", "State House: K40m unchanged, disbursement realigned. Explainer: Finance Minister's 9 Oct 2026 cut warning for 2027.")
S_ECON = src("Zambian Economist",
             "Budget 2027: The Run-Up — what the numbers say",
             "https://zambianeconomist.com/budget-2027-run-up-what-the-numbers-say/",
             "2026-10-26", "Draws on the Auditor General's CDF report for 2024.")
S_JCTR = src("Jesuit Centre for Theological Reflection (JCTR)",
             "From Expansion to Accountability: Is CDF Delivering in Zambia?",
             "https://jctr.org.zm/en/from-expansion-to-accountability-is-cdf-delivering-in-zambia/",
             "2026-04-16", "Analysis of Auditor General reports 2022-2024.")

# ---------------------------------------------------------------- provinces & sets
PROVINCES = ["Central", "Copperbelt", "Eastern", "Luapula", "Lusaka",
             "Muchinga", "Northern", "North-Western", "Southern", "Western"]
for p in PROVINCES:
    cur.execute("INSERT INTO provinces(name) VALUES(?)", (p,))
cur.execute("INSERT INTO delimitation_sets(label,note) VALUES('current-156','156 constituencies in use through the 2026 budget year.')")
cur.execute("INSERT INTO delimitation_sets(label,note) VALUES('delimitation-2026-226','ECZ 2026 delimitation: 226 constituencies. Full official list seeding pending.')")

# ---------------------------------------------------------------- budget years (K m per constituency)
for year, per in [(2021, 1.6), (2022, 25.7), (2023, 28.3), (2024, 30.6), (2025, 36.1), (2026, 40.0)]:
    cur.execute("INSERT INTO budget_years VALUES(?,?,?,?,?,?)",
                (year, per, 156, round(per * 156, 1), S_MLGRD, "Uniform national rate."))

# ---------------------------------------------------------------- disbursements (K millions)
DISB = [
    (2024, None, "all", 2630.0, "Treasury releases in 2024", None, S_ECON,
     "Treasury released K2.63bn of the K4.78bn provided (~55%), per the Auditor General's 2024 CDF report."),
    (2025, None, "all", 5260.0, "Reported cumulative releases", None, S_2025,
     "Reported disbursed to constituencies for the 2025 CDF year (~94% of allocation)."),
    (2026, None, "bursaries", 100.0, "First 2026 bursary tranche", "2026-02-03", S_OZ_FEB,
     "K641,025 deposited per constituency."),
    (2026, None, "community", 215.7, "Community Projects Component spend, Q1 2026", "2026-03-31", S_OZ_JUN,
     "Already spent under the Community Projects Component by end of Q1 2026, per MLGRD PS."),
    (2026, None, "all", 2200.0, "Reported cumulative disbursements", "2026-06-05", S_OZ_JUN,
     "Reported 2026 disbursements reaching K2.2bn, incl. an extra K500m release."),
]
cur.executemany("INSERT INTO disbursements(budget_year,constituency_id,component,amount_m,tranche_label,disbursement_date,source_id,note) VALUES(?,?,?,?,?,?,?,?)", DISB)

# ---------------------------------------------------------------- reported metrics
M = []
def metric(metric, value, unit, source, year=None, as_of=None, defn=None, status="current", scope="national"):
    M.append((metric, scope, None, year, value, unit, as_of, defn, status, source))

# 2025 movement rates
metric("released_pct_of_allocation", 94, "%", S_2025, 2025, defn="Share of the 2025 allocation reported released.")
metric("utilisation_pct", 86, "%", S_2025, 2025, defn="Reported share of funds put to use, 2025.")
metric("community_projects_approved_count", 2985, "count", S_2025, 2025)
metric("community_projects_approved_amount", 2900, "K millions", S_2025, 2025)
metric("community_projects_share_of_allocation_pct", 52, "%", S_2025, 2025)

# Delivered set A — displayed on the dashboard (MLGRD, Sept 2025)
for mname, val in [("classroom_blocks_built", 2800), ("school_desks_procured", 670000),
                   ("health_facilities_built", 164), ("maternity_annexes_built", 206),
                   ("secondary_boarding_bursaries", 82652), ("skills_bursaries", 151518)]:
    metric(mname, val, "count", S_MLGRD, as_of="2025-09",
           defn="Cumulative since the fund's 2022 expansion, as reported by MLGRD (Sept 2025 article). Classroom/desk figures published as '2,800+' / '670,000+'.")
# Delivered set B — conflicting June 2026 briefing set, kept for provenance
for mname, val, defn in [("classroom_blocks_built", 5088, "MLGRD PS briefing, June 2026."),
                         ("school_desks_procured", 732000, "Published as 'over 732,000'."),
                         ("health_posts_built", 599, "'Health posts' — not directly comparable to set A's 'health facilities'."),
                         ("maternity_annexes_built", 272, "MLGRD PS briefing, June 2026."),
                         ("boreholes_drilled", 6317, "MLGRD PS briefing, June 2026.")]:
    metric(mname, val, "count", S_OZ_JUN, as_of="2026-06-05", defn=defn, status="alternative")

# Broader cumulative bursary counts (Feb 2026)
metric("secondary_bursary_beneficiaries_cumulative", 131640, "count", S_OZ_FEB, as_of="2026-02-03",
       defn="All secondary bursaries since 2022 — broader than set A's boarding-only figure.")
metric("skills_beneficiaries_cumulative", 198559, "count", S_OZ_FEB, as_of="2026-02-03",
       defn="All skills development beneficiaries since 2022.")

# Auditor General 2024 findings (via Zambian Economist)
metric("projects_total_audited", 4879, "count", S_ECON, 2024, defn="Projects covered by the AG's 2024 CDF report, all 156 constituencies.")
metric("projects_completed", 3060, "count", S_ECON, 2024)
metric("projects_not_started", 526, "count", S_ECON, 2024)
metric("unspent_amount", 771.4, "K millions", S_ECON, 2024, defn="Unspent out of K5.12bn available (figure highlighted in the Zambian Observer explainer of the same report).")
metric("desks_paid_amount", 514.2, "K millions", S_ECON, 2024, defn="Paid for 356,460 school desks.")
metric("desks_undelivered_count", 71301, "count", S_ECON, 2024, defn="Desks not arrived by September 2025.")
metric("desks_undelivered_value", 130.7, "K millions", S_ECON, 2024)
metric("completed_but_unused_value", 22.0, "K millions", S_ECON, 2024, defn="Clinics, police posts and classrooms in 18 constituencies, finished but unused for up to 23 months.")
metric("roads_worked_km", 567, "km", S_OZ_JUN, as_of="2026-03", defn="Roads worked on as of March 2026; K3.7m per constituency set aside for road maintenance.", status="current")

# Loan recovery / irregularities (JCTR + AG + MLGRD)
metric("loan_recovery_pct", 10.6, "%", S_JCTR, 2023)
metric("loan_recovery_pct", 17.0, "%", S_JCTR, 2024)
metric("loan_recovery_pct_since_2021", 35, "%", S_OBS_SEP, as_of="2026-09-29",
       defn="Recovery on all CDF loans disbursed since 2021, per MLGRD Director of Planning; basis for suspending 2026 loans.")
metric("financial_irregularities", 18.7, "K millions", S_JCTR, 2022, defn="CDF financial irregularities per AG reports, via JCTR.")
metric("financial_irregularities", 25.7, "K millions", S_JCTR, 2024, defn="CDF financial irregularities per AG reports, via JCTR.")

cur.executemany("INSERT INTO reported_metrics(metric,scope,constituency_id,budget_year,value,unit,as_of,definition_note,status,source_id) VALUES(?,?,?,?,?,?,?,?,?,?)", M)

# ---------------------------------------------------------------- bursaries & loans
cur.execute("INSERT INTO bursaries_loans(budget_year,constituency_id,loans_due_m,loans_recovered_m,recovery_pct,source_id,note) VALUES(2024,NULL,375.3,63.8,17.0,?,?)",
            (S_ECON, "CDF loans due by October 2025 per the AG's 2024 report; ~17% collected."))

# ---------------------------------------------------------------- news items (mirror of data.js)
NEWS = [
    ("2026-10-26", "Auditor General's 2024 CDF report, via Zambian Economist", "Auditor General: most 2024 projects finished, but funds left idle",
     "The Auditor General's report on the 2024 CDF found 3,060 of 4,879 projects completed and 526 not started, about K771 million unspent out of K5.12 billion available, and only about 17% of CDF loans due collected (K63.8 million of K375.3 million).", S_ECON),
    ("2026-10-13", "Zambian Observer", "2027 CDF rate in question ahead of the budget",
     "On 9 October the Finance Minister warned the 2027 CDF allocation will be lower than budgeted; State House clarified on 13 October that the current K40 million per constituency is unchanged and only disbursement is being realigned by need and absorption. The 2027 budget, presented 30 October 2026, sets the new rate — and the Electoral Commission has confirmed 70 additional constituencies (226 in total) under the 2026 delimitation.", S_OBS_OCT),
    ("2026-09-29", "Zambian Observer", "2026 CDF loan component suspended",
     "The Ministry of Local Government has suspended new CDF empowerment loans for 2026 after recovering only about 35% of loans disbursed since 2021, its Director of Planning said. Funds earmarked for 2026 loans were redirected within CDF, and new loans will be issued only from recovered funds.", S_OBS_SEP),
    ("2026-06-05", "Open Zambia", "Extra K500 million CDF release reported",
     "Reported 2026 disbursements reaching K2.2 billion, with 2,293 projects worth about K2.79 billion approved.", S_OZ_JUN),
    ("2026-02-03", "Open Zambia", "First 2026 bursary tranche released",
     "Government released K100 million as the first 2026 CDF bursary allocation — K641,025 per constituency. Cumulative beneficiaries since 2022 were reported at 131,640 secondary school learners and 198,559 skills development trainees.", S_OZ_FEB),
]
cur.executemany("INSERT INTO news_items(item_date,source_label,title,text,source_id) VALUES(?,?,?,?,?)", NEWS)

con.commit()
for t in ["sources", "provinces", "delimitation_sets", "budget_years", "disbursements",
          "reported_metrics", "bursaries_loans", "news_items", "projects", "constituencies"]:
    print(t, cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
con.close()
print("cdf.db built")
