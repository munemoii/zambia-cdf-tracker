# Eastern Province CDF — coverage report (merged)

Collected: 30 October 2026 (research pass, published sources only), following the Lusaka pilot method.
Output: `projects.csv` — **224 project rows**; `held.csv` — **136 held rows**; `sources.csv` — **77 sources**.
The merged `projects.csv` passes the tracker ingest validator (dry-run): 224/224 rows OK, 0 problems.
Working inputs: `frag-chipata/`, `frag-north/`, `frag-petauke/`, `frag-south/` hold the per-cluster
CSVs this file was merged from; the per-cluster coverage detail follows in Parts 1–4 below.
(`sinda-publications` was captured by two clusters with the same URL and merged to one source row.)

## Rows per constituency (projects.csv + held.csv)

| Constituency | projects.csv | held.csv |
|---|---|---|
| Chadiza | 16 | 5 |
| Chama North | 1 | 9 |
| Chama South | 1 | 3 |
| Chasefu | 12 | 21 |
| Chipangali | 12 | 8 |
| Chipata Central | 15 | 7 |
| Kapoche | 6 | 1 |
| Kasenengwa | 18 | 1 |
| Kaumbwe | 14 | 1 |
| Luangeni | 0 | 6 |
| Lumezi | 16 | 13 |
| Lundazi | 15 | 21 |
| Malambo | 11 | 3 |
| Milanzi | 18 | 1 |
| Mkaika | 8 | 1 |
| Msanzala | 13 | 2 |
| Nyimba | 1 | 4 |
| Petauke Central | 2 | 0 |
| Sinda | 0 | 13 |
| Vubwi | 45 | 3 |
| (unattributed — constituency not stated in source) | — | 13 |
| **Total** | **224** | **136** |

## Administrative corrections found during research

- **Kapoche is in Sinda District (Sinda Town Council)**, not Petauke — Sinda's own publications state the district's two constituencies are Sinda and Kapoche. Petauke Town Council covers only Petauke Central and Kaumbwe.
- **Msanzala is administered mainly by Lusangazi Town Council** (4 of its wards sit on the Petauke side; all rows found came from Lusangazi-side sources).
- Chama North/South are filed under Eastern for CDF tracking per the brief, though Chama District was realigned to Muchinga administratively.

## Biggest gaps

1. **Sinda (0 main rows, 13 held) and Luangeni (0 main, 6 held): publication exists, retrieval failed.** Sinda Town Council's Publications page lists the actual approved-project documents for both Sinda and Kapoche (2022 Sinda/Kapoche projects; 2024 Kapoche split projects; 2022 Kapoche approved-incomplete; 2024 and 2025 Sinda approved lists), and Chipata City Council's Publications page lists Luangeni approved lists for 2022, 2023 and 2025 (plus un-rowed Chipata Central 2022/2023/2024 lists) — but the text-fetch tool could not extract the PDF download URLs (and hit a fetch-service 429 on the Chipata index page). **Highest-value follow-up: one live-browser pass over sindacouncil.gov.zm and chipatacouncil.gov.zm Publications pages to open those PDFs.** This is an access gap, not a publication gap.
2. **Chama (2 main rows, 19 held incl. 7 unattributed):** Chama Town Council publishes no findable constituency-split community project list; its only approval announcement covers bursaries/grants/loans. Most Chama material cannot be split North/South plainly.
3. **Chasefu (12 main, 21 held):** the council's official 2022 approved-projects PDF exists but a tool-side 429 limited capture to search-snippet fragments (16 rows held as an incomplete list).
4. **Nyimba (1 main, 4 held):** no project-level CDF list findable at all — only the District Hospital genset (2023 CDF, K548,183) could be rowed.
5. **Petauke Central (2 main):** the council's commissioning article covers 21 completed projects (K9,499,043.32 total) but names only 2 of them.
6. **Thin years:** Lundazi has an approved list only for 2025; Vubwi only for 2022 and 2024; Kaumbwe only for 2022; Katete (Milanzi/Mkaika) only for 2025; no Kasenengwa or Chipangali lists for other years were found.

## Strongest sources (full official lists in projects.csv)

- Vubwi Town Council 2022 approved list (30 projects, wards + costs, K13,935,384.66 printed total) and 2024 approved list (15, K16,589,200.12) — both explicitly name their CDF funding year.
- Chipata Central 2025 approved list (MLGRD approval notification, 16 Apr 2025; 15 projects; programme total K20,916,106.93; no per-project amounts published).
- Kasenengwa 2025 CDF Project Status PDF (18 projects with ward, contractor, contract sum, progress %).
- Lundazi Town Council Approved 2025 PDF (15 projects, ward + sector, no budget column).
- Lumezi 2022 signed-contract breakdown via MLGRD (15 projects with contractors and exact sums, plus a K2,030,000 grader).
- Kaumbwe 2022 approved list (Petauke Town Council PDF; 9 projects with allocations + 5 varied-from-bursaries projects).
- Katete 2025 approved lists for Milanzi (17 items) and Mkaika (8) — no wards for Milanzi, no amounts for either.
- Mambwe Town Council Appendix I, Approved 2024 CDF Community Projects (11 projects, wards + estimated costs).
- Chipangali 2024 CDF Community Projects Recommended for Approval PDF (12 projects).

## Funding years

Per-source funding-year explicitness (whether the source names a CDF year, and which) is recorded in the per-cluster tables in Parts 1–4. Headline: the Vubwi 2022/2024, Chipata Central 2025, Kaumbwe 2022, Katete 2025, Mambwe 2024, Lundazi 2025, Lumezi 2022, Kasenengwa 2025 and Chipangali 2024 lists all explicitly name their funding year; most council-article and ZANIS-derived rows do not, and those rows carry no year anywhere in the CSVs.

## Merge note (one editorial touch)

Petauke's Kaumbwe 2022 PDF lists two items both named plainly "Water Project" (main list: K2,085,956; varied-from-bursaries list: K395,299), which the ingest validator rejects as a within-file duplicate. They were disambiguated using the PDF's own published scope text — "Water Project (drilling and equipping of at least 22 boreholes)" and "Water Project (drilling and equipping of 6 boreholes)" — verified against the PDF on 30 Oct 2026. No other names were altered beyond tidy capitalization. Two Vubwi rows share the name "Rehabilitation of 2 Staff Houses" but sit in different wards (Chisiya, Sindemisale) and passed validation as published.

## Access notes

No council website refused a connection in any cluster. All retrieval failures were tool-side: the page-fetch service returned 429 rate limits on the Chipata Publications index, the Chasefu 2022 PDF, and one Katete/Sinda fetch batch; affected material was read from search-index extracts where possible and otherwise held or recorded as a gap above. Facebook was not used anywhere.

---


# Part 1 — Chipata cluster (Chipata Central, Luangeni, Kasenengwa, Chipangali)

# Coverage — Chipata cluster, Eastern Province

Research date: 2026-10-30. Method: only rows taken plainly from official published
lists are in `projects.csv`; single news items, success stories, aggregate
figures and uncertain attributions are in `held.csv`.

Real council domains found (via search, not guessed):
- Chipata City Council — chipatacouncil.gov.zm (the chipatacitycouncil.gov.zm
  variant does not exist)
- Kasenengwa Town Council — kasenengwacouncil.gov.zm (the site itself spells
  the town "Kasenegwa" in places; the official district name Kasenengwa is used
  in the CSVs)
- Chipangali Town Council — chipangalicouncil.gov.zm

Connection note: no council site refused a connection in this pass. The
Chipata Publications index page and the Chipata council news listing could not
be opened in full because the page-fetch service returned a rate-limit (429)
error; their content was read from search-index snippets instead. That is a
tool limit, not a council refusal, and it is the direct cause of the Luangeni
gap below.

## Chipata Central (Chipata City Council)

- FOUND — official approved list: MLGRD Eastern Province "Notification of
  Approval of Community Project (CDF 2025) under Chipata Central Constituency",
  dated 16 April 2025, hosted on the Chipata City Council website
  (`chipata-central-2025-approved`). It names 15 community projects and a
  programme total of K20,916,106.93; no per-project amounts are published, so
  all 15 rows in projects.csv have a blank budget. All 15 are in projects.csv
  with status "approved".
- Corroboration (not separately rowed, to avoid double-counting): the
  council's news item "Grading of Township Roads under the 2025 CDF Allocation
  Commence" (chipatacouncil.gov.zm/?p=4669) describes the same roads project as
  the approved list's "Maintenance of Selected Roads", with a ward split of
  90.97 km (Kapata 19.82, Kanjala 11.3, Msanga 20.8, Dilika 20.35, Masupe 18.7).
- The council Publications page (see Luangeni below) also lists Chipata
  Central approved lists for 2022, 2023 and 2024 and a "2024 CDF Approved
  Projects" document dated 18 September 2024. Their direct PDF URLs could not
  be retrieved in this pass, so no 2022–2024 Chipata Central list rows are
  included; individual 2022–2023 projects reported by ZANIS / Parliament are
  in held.csv instead.
- One spelling caution: the 2025 approval PDF is a poor-quality scan. The
  health-post location read as "Nkhombolakabaye" (council news elsewhere
  writes a similar place as "Mkombola Kabaye"); the PDF spelling is kept and
  should be verified against the original scan before publication.

## Luangeni (Chipata City Council)

- BIGGEST GAP IN THIS CLUSTER. Chipata City Council's Publications page
  (`chipata-publications-index`, read via search-index text) lists, with
  publication dates, all of the following official documents:
  - "2025 Luangeni Approved Community Projects" — 8 April 2025
  - "2023 Luangeni Approved projects" — 11 October 2024
  - "2022 Luangeni Approved projects" — 11 October 2024
  - "2025 Luangeni WDC Proposed Community Projects With Justifications" —
    12 December 2025
  So the council DOES publish Luangeni lists — but the direct PDF URLs behind
  the Publications index were not discoverable through search and the index
  page itself could not be opened (fetch rate-limit). No Luangeni rows are
  therefore in projects.csv; a follow-up pass that opens the Publications
  page and follows its links should recover full Luangeni lists for 2022,
  2023 and 2025 in one step.
- In the meantime, six individually reported Luangeni projects are in
  held.csv (Mainga Primary 1x2 CRB, K934,927.17, 2024 CDF; Chief Nzamane's
  Palace, K4,000,000, 2024 CDF; Kaphinde/Kazimule electrification, K8.5m
  combined; Thantwe Primary / Agriculture Camp House electricity connection,
  K788,725.97, Chikando Ward, 2025 CDF; Nsanjika Health Post completion,
  ~K217,000; Feni water scheme with 5 kiosks, K924,131.25).
- A January 2023 ZANIS briefing (eas.gov.zm) states Luangeni implemented 34
  projects at K17,724,059.00 in the previous year, but it does not list them
  or split its named examples by constituency; the unattributable "Sairi
  Health Post" (~K753,000) from that briefing is held under Chipata Central
  as a placeholder only — its constituency is UNRESOLVED and it must not be
  published without verification.

## Kasenengwa (Kasenengwa District Council)

- FOUND — official status list: "Kasenengwa Town Council 2025 CDF Project
  Status" PDF on the council website (`kasenengwa-2025-cdf-status`). It lists
  18 community projects with ward, contractor, contract sum and progress %.
  Kasenengwa district is a single constituency, so all 18 rows are attributed
  to Kasenengwa plainly. All 18 are in projects.csv; status is mapped from
  the published progress figure (100% = completed, below 100% = ongoing) and
  the figure itself is kept in completion_pct. The PDF carries no date on its
  face (uploaded December 2025 per its URL path).
- No Kasenengwa CDF list for 2022, 2023 or 2024 was found on the council site
  or elsewhere in this pass. One 2022 project (Champhundu Primary 1x3 CRB,
  K412,000) is in held.csv from a ZANIS commissioning report.
- Parsing caution: the PDF text layer interleaves columns. Contractor/school
  splits were read plainly where the name order made them unambiguous (e.g.
  row 4, Stelamilla Business Ventures at Chinkholowodyo Primary). Two
  different projects share an identical contract sum of K645,701.70 in the
  PDF as published (Chinkholowodyo Primary CRB and Mkowe Day Secondary CRB);
  both figures are reproduced exactly as published.

## Chipangali (Chipangali District Council)

- FOUND — official approved list: "2024 CDF Community Projects Recommended
  for Approval" PDF on the council website (`chipangali-2024-approved`,
  file name ends APPROVED_FINAL; uploaded September 2024 per its URL path).
  Chipangali district is a single constituency. Rows 1–12 were readable from
  the PDF's search-indexed text and are in projects.csv with status
  "approved".
- Budget column choice: the PDF publishes both an Engineer's Estimate and a
  CDFC Approval amount per project. projects.csv uses the CDFC Approval
  amount. Where the two differ: Nyaviombo maternity annex equipment —
  estimate K165,000, approval K150,000 (CSV: 150000); road grading — estimate
  K1,000,000, approval K942,200.12 (CSV: 942200.12); borehole drilling —
  estimate K1,000,000, approval K700,000 (CSV: 700000).
- The incinerators row (row 11) has no plainly readable total in the indexed
  text, so its budget is blank. Rows beyond row 12, if any exist in the PDF,
  could not be confirmed from the indexed text — the list may be incomplete
  at the tail and should be re-checked against the PDF directly.
- No Chipangali CDF list for 2022, 2023 or 2025 was found. The council did
  launch a "CDF News Bulletin for 2022 Projects" (reported by ZANIS, August
  2023), but the bulletin itself was not findable online in this pass.
  Individually reported Chipangali items (fleet purchases, Mushawa maternity
  annex, three empowerment-grant stories) are in held.csv.

## Does each source explicitly name a CDF funding year?

| source_key | Explicit CDF year? |
|---|---|
| chipata-central-2025-approved | YES — CDF 2025, in the document title and body |
| chipata-publications-index | YES — each listed document title carries its year (2022, 2023, 2024, 2025) |
| kasenengwa-2025-cdf-status | YES — 2025, in the document title |
| chipangali-2024-approved | YES — 2024, in the document title |
| chipata-zanis-2023-spend | NO single year in the title — January 2023 article reporting the previous year's (2022) spend; years are stated in the body for bursaries/grants context only |
| chipata-central-zanis-2022-inspection | YES in body — projects stated to use the 2022 CDF |
| chipata-council-news | MIXED — the Kauzu item states 2024 CDF and the Luangeni commissioning item states 2025 CDF in their bodies; the Magwero Maternity Annex item as retrieved states no funding year |
| chipata-madzimoyo-parliament-2025 | YES in body — 2023 CDF |
| luangeni-mainga-parliament | YES in body — 2024 CDF |
| luangeni-nzamane-palace | YES in body — 2024 CDF |
| luangeni-power-zanis | NO — no CDF funding year is stated in the retrieved text |
| kasenengwa-champhundu-zanis | YES in body — 2022 CDF |
| chipangali-fleet-2025 | YES in body — tractor 2023 CDF, water bowser 2024 CDF, grader and roller compactor 2022 CDF |
| chipangali-success-stories | YES in body — Chimwemwe grant 2022, Mpaka Mpaka grant 2023 |
| chipangali-mushawa-maternity | NO — no CDF funding year is stated in the retrieved text |
| chipangali-chipilimunzi-zanis | NO — no CDF funding year is stated in the retrieved text (article dated 30 June 2025) |
| chipata-tour-openzambia | NO — tour report (June 2026) naming Magwero Police Post, Magwero Maternity Annex, Kauzu Primary School and water systems in Magwero and Feni; no funding year and no amounts; used for coverage only, no rows |
| luangeni-health-posts-zanis | NO — April 2024 report that K1.6 million CDF was spent on health facilities in Luangeni, naming no individual facilities; used for coverage only, no rows |

## Other gaps

- MLGRD (mlgrd.gov.zm) and the National Assembly constituency pages yielded
  no Chipata-cluster project lists in this pass (the Assembly site yielded
  one Luangeni news item, held).
- No source in this cluster published per-project photos, so photo_url and
  photo_credit are blank throughout, as instructed.
- Category note: two held Chipangali empowerment rows (goat-rearing
  cooperatives) have no fitting category in the allowed category list; they
  are filed under "infrastructure" as the least-wrong option and should be
  re-categorised if an agriculture/livestock category is ever added.

---

# Part 2 — North cluster (Lundazi, Chasefu, Lumezi, Chama North, Chama South)

# Eastern Province — northern-eastern cluster (frag-north) CDF coverage report

Collected: 30 October 2026 (research pass, published sources only).
Constituencies: **Lundazi, Chasefu, Lumezi, Chama North, Chama South** (Chama District is filed under Eastern for CDF tracking in this dashboard, per the task brief; the Chama Town Council newsletter itself describes Chama as "the largest district in Zambia's Eastern Province", while other sources place it in Muchinga — no project attribution turns on the province question).
Output: `projects.csv` — **45 project rows**; `held.csv` — **74 held rows**; `sources.csv` — **24 sources**.

Method, following the Lusaka pilot: rows taken plainly from official published lists/documents (council approved-projects PDFs, an MLGRD contract breakdown, official council newsletters/articles) go in `projects.csv`. Single news reports that do not reproduce an official list, snippet-only fragments, rows needing interpretation, rows with uncertain Chama North/South attribution, and rows with conflicting figures go in `held.csv` with a `hold_reason`. Per-project budgets are recorded only where published per project; programme totals are never split across projects (they are recorded as aggregates below). No photos were captured for any row in this pass (`photo_url`/`photo_credit` left blank throughout — no source page checked returned a verifiable per-project direct image URL).

## Per-constituency coverage

### Lundazi (Lundazi Town Council) — 15 projects.csv rows, 21 held rows

**Strongest source in the cluster:** the council's own **Approved 2025 CDF Community Projects** PDF (`lundazi-2025-approved`) — a clean 15-row table with project name, description, sector and ward for every row. All 15 are rowed as `approved`. **No per-project amounts are published in the PDF** (no budget column at all), so every Lundazi budget in this pass is blank. The PDF's ward for three Lundazi-town items is given simply as "Lundazi" and is recorded as published. Judgement calls: the crossing points/bridge (sectors published as "Transport") are categorised `infrastructure`; the Parliamentary Office completion is categorised `administration` (sector published as "Governance"); the health-post equipment purchase is categorised `equipment` (sector published as "Health").

Held: the Zambian Observer handover report of 6 Aug 2023 (`lundazi-handover-2023`) lists 2021 CDF projects (4) and 2022 CDF projects — it is a news report, not an official list, so all 17 enumerated projects are held. **Discrepancy in the source: the headline says 18 projects totalling K9,591,000, but only 17 projects can be enumerated from the text** (4 under 2021 CDF; 10 listed under 2022 CDF plus 3 further "other projects" — Gumbilwe Police Post, Lundazi District Hospital mortuary, Kaphodo Bridge — whose funding year is not separately stated). No wards or per-project amounts are published for any of them. A further 4 commissioned projects (Lukwizizi, Kambale and Kachete 1×3 classroom blocks, Mchereka Maternity Annex) are held from a **search snippet of the Lundazi Town Council news index only** (`lundazi-council-news-index`) — the full article was not captured, so CDF year, wards and amounts are unverified.

Gap: no Lundazi approved-projects list for 2022, 2023, 2024 or 2026 was found — only the 2025 PDF. The council site also hosts an Auditor General's report on its 2024 financial statements (found in search), which was not mined for project rows in this pass.

### Chasefu (Chasefu Town Council) — 12 projects.csv rows, 21 held rows

No complete official approved-projects list could be fully captured. The council **does** publish one — **"Chasefu District Community Projects CDF 2022"** PDF (`chasefu-2022-approved-pdf`) — but **its full text could not be fetched in this pass: the fetch failed with an upstream tool rate-limit error (429), not a refusal by the council site**. Only search-snippet fragments of its table were verified (rows 1–6, 8–14, 18, 20, 21; rows 7, 15–17, 19 and any later rows are missing from the fragments). The 16 fragment rows are therefore all in `held.csv`, flagged as an incomplete list. Several fragment rows are the earlier-stage versions of projects rowed as completed from the council articles below (Champheta, Mswazi, Khulamayembe, Kapekesa) — they are not duplicates within `projects.csv`, but the overlap is real and is flagged here.

`projects.csv` rows come from two articles on the council's own website: the MP's CDF project tour (`chasefu-council-tour`, 5 rows — statuses as stated: Champheta Magodi 1×3 and Mswazi 1×3 and the Susa staff house "completed"; the Champheta staff house "at roof level" and the Khulamayembe staff house "in its final stage" — the Khulamayembe row is not repeated here because the commissioning article below rows it as completed; Chidolo 1×2 is given no explicit stage in the tour text and is rowed `ongoing` as a toured work-in-progress) and a handover/commissioning article (`chasefu-council-commissioned`, 7 rows, all `completed`, including a Tipper truck). Parsing notes for the commissioning article: its sentence "a 1 x 3 Classroom block at Phikamalaza and Chiginya Primary Schools in Membe ward" is read as one block at each school (two rows, both Membe Ward); "a 3 Bedroomed Staff House at Khulamayembe and a 1×2 Classroom Block at Munthyengu Primary Schools in Mandahill and Kapilisanga wards" is read in order — Khulamayembe → Mandahill (consistent with the tour article's "Mandaholl" ward for Khulamayembe, standardised to the 2022 list's "Manda Hill"/article's "Mandahill"), Munthyengu → Kapilisanga. Neither council article states a CDF funding year or any amounts.

Held news rows: five staff houses at Kapekesa Primary School (ZANIS, 2025 CDF, K2.1m for the five as one project, `ongoing`; the same report's passing mention of a "recently constructed Kapekesa Health Facility" is held separately with no year/amount); Nkhanga Police Post (K1.2m allocated) and Kapekesa Clinic (K1.8m allocated, Membe Ward) from a Feb 2025 launch report — the clinic may be the same facility as the 2022 list's Kapekesa health post; and a CDF motor-grader hire contract (K1,450,000, Rutch Contractors and General Dealers, Oct 2026, Zambia Monitor reporting a council statement). **In that Monitor report, only the grader hire is explicitly stated to be CDF-funded** — the radiology department (K1,479,208.50, Alideate Sky Investment Limited) and the Civic Centre office block Phase One (K1,902,685.51, Kiprique Construction Supplier and General Dealers) in the same report are **not** stated to be CDF-funded and were not rowed anywhere.

Aggregates (not rowed): the MP stated in July 2025 that since 2022 Chasefu had issued 406 empowerment grants, 540 cooperative loans, 585 secondary bursaries, 209 driving licences and 946 skills trainees, and that the council had procured 9,445 desks, drilled 20 boreholes, rehabilitated 120 km of feeder roads and constructed 14 health facilities and 34 classroom blocks (no project-level list published); at a 2025 launch the MP said 79 projects had been completed since 2021 with over 25 more due in 2025. A council handover article records empowerment totals of K2,348,898.36 in grants to 76 groups, K3,492,963.18 in loans to 40 beneficiaries and K715,069 as a revolving fund to 10 beneficiaries (its "72 wards of Chasefu District" wording is as published and is not used anywhere as a ward count).

### Lumezi (Lumezi Town Council) — 16 projects.csv rows, 13 held rows

**Backbone source:** the MLGRD article `lumezi-mlgrd-contracts-2022`, which reproduces Lumezi Town Council's signed-contract breakdown for the **2022 CDF**: 15 named projects, each with ward (12 of 15), contractor and exact contract sum — all rowed as `approved` (contracts signed, works "earmarked to commence", 12-week delivery period), plus the grader the council had procured the previous month at K2,030,000 "as part of the community projects", rowed as `completed` (procured). The article says 16 community projects were shortlisted at a projected K13,935,384.84; only 15 contracts were signed (K7,547,070.72) plus the grader — the 16th shortlisted project is not named. **Ward conflict in the sources, recorded as published in each row:** the MLGRD list places the Yakhobe mother's shelter/incinerator in **Chibande Ward** and the Yakhobe staff house in **Lukusuzi Ward**, while the council's own commissioning article (`lumezi-council-commissioned-2022`) describes all three commissioned Yakhobe works as "at Yakhobe Rural Health Post under Lukusuzi ward". That council article confirms three of the MLGRD rows (the two Yakhobe items and the Milulu Primary completion) were later commissioned/completed at a combined K1,149,928.44 — they are **not** rowed a second time; the `projects.csv` rows keep the MLGRD contract-stage status. Spellings are as published in the MLGRD list ("Chamkoma", "Kamnkongono", "Kabobola"); other sources spell the health post "Chamkhoma".

Held: the four **2025 CDF health posts** (Chiweza, Mbuzi, Kavinaka, Chasera) from a Zambian Observer reproduction of a council statement (`lumezi-observer-health-2025`) — the published K2,736,342.85 is the **combined** cost of all four, so no per-project budget is recorded; four further named **2025 contract awards** from RCV (`lumezi-rcv-2025-contracts`: Kateme Police Post and staff house, 800 desks, Lukusuzi Primary and Kamo Primary classroom blocks) — RCV names only *selected* projects of the 19 approved for 2025 (over K21m total, no per-project amounts), and its Kavinaka/Chasera items are the same projects as the Observer rows, so they are held once only; two **2022 CDF disaster-component** projects in Chamtowa Ward from a single ZANIS report (Kapongolo Primary 1×3, K400,000, 80% complete; Katete crossing point, K570,000, 70% complete — the report spells it both "Katete" and "Ketete"); the Chamkhoma Health Post at 99% / K500,000 from a single ZANIS report, whose combined figure **conflicts/overlaps** the MLGRD list's separate Chamkoma contracts (K318,000 + K378,944.50); Katope Rural Health Post as the one named project in Parliament's July 2025 aggregate commissioning report (13 completed 2023–2024 CDF projects, K8,105,146.48 total, the other 12 unnamed — aggregate recorded here only); and the Kapangala Primary 1×2 rehabilitation (2024 CDF Disaster Component, "more than K276,000" — row carries 276000) from a low-tier outlet, with no ward stated.

Gap: **no full Lumezi approved-projects list was found for any year** — not for 2022 (only the contract breakdown), and not for 2025, where the council states 19 community projects were approved at over K21 million but only 8 distinct projects are named across the two 2025 sources captured. The council website was reachable and its news/documents were searchable; no CDF project database PDF was found on it.

### Chama North & Chama South (Chama Town Council) — 1 + 1 projects.csv rows, 19 held rows (9 attributed to Chama North, 3 to Chama South, 7 unattributed between the two)

The thinnest coverage in the cluster. **Chama Town Council publishes no consolidated community-project list for either constituency that could be found.** The only council approval announcement captured (`chama-council-2024-approvals`, 2024 CDF) covers **bursaries, empowerment grants and loans only** — no community projects — and is recorded here as a source with no rows.

The backbone is the council's official **September 2023 newsletter** (hosted on the MLGRD website, `chama-newsletter-2023`), a narrative publication, not a project list. Only two of its project stories state a constituency plainly enough to row: the **Champanda Community School staff house** (text: "Chama South constituency's Bazimu ward", completed → Chama South, `projects.csv`) and the **Kaozi Primary School 1×3 CRB** (Kaozi Ward; the newsletter does not name the constituency, but Kaozi Ward is unambiguously in Chama North in the Electoral Commission of Zambia's ward listing, `ecz-chama-wards` — attributed by ward per the task rule, roof level → `ongoing`).

Everything else Chama is in `held.csv`, mostly for **uncertain North/South attribution**, exactly as the task prescribes:
- The council's 2022 CDF commissioning article (`chama-council-commissioned-2022`) names five projects (Kajimomo 1×2, Kaozi 1×2, Makeni Community School 1×2, Champhanda staff house, Mundalanga Health Post staff house) with **no North/South split and no wards** — all held. Two carry extra conflicts: the Kaozi item is a **1×2** block "commissioned" here but a **1×3** CRB "at roof level" in the Sept 2023 newsletter; and "Champhanda" is very likely the same Champanda (Bazimu Ward, Chama South) staff house rowed from the newsletter — held here to avoid double-counting.
- Newsletter stories with no constituency/ward: Kalovya Day Secondary girls' dormitory (at roof installation, nearing completion); the Chilubunta Primary 1×3 CRB story, whose **body repeatedly names a different school (Katangalika Primary School)** — name conflict within one article (Kaozi Ward → North, held).
- District-wide newsletter aggregates held as single programme rows: 30 boreholes (15 drilled, 15 underway, **no locations published**) and the 108 mattresses handed over by the Chama North MP to the district health department (which constituency's CDF paid is not stated). **Not rowed anywhere:** the newsletter's desk figures — 5,547 desks in total across both constituencies, with the two MP messages giving 2,987 desks for Chama North and 2,560 for Chama South while the desks article describes 2,560 as "awaiting delivery" and 2,987 as pending procurement clearance; and the 2022 empowerment grant totals (Chama North: 101 clubs/cooperatives, K1,471,200; Chama South: 58 clubs/cooperatives, K1,449,000).
- ZANIS road-works report, 12 June 2025 (`chama-zanis-roads-2025`) — a single news report, but the only source that **does** split projects by constituency: Chama North — Kambombo-Sitwe road (works commenced → `ongoing`), Mwimba, Katangalinga-Kapembe, Chibale-Kabobe and Mulilo roads and CBD/Makeni-area roads (all named as next/slated → `approved`); Chama South — Chikwa-Chasato road (`ongoing`, "significant progress"), Muyukwa-Kasela road (`approved`), plus unnamed crossing points in Chama South that were **not rowed** (no project named). No wards, amounts, contractors or CDF year are published for any of these.
- Kasangani Primary School water reticulation (Open Zambia, 2026; 2024 CDF, K297,095, contractor DIMVI General and Agro Suppliers, commissioned → `completed`) — held because the article states **no constituency and no ward** for Kasangani.
- 200 mattresses for Chama South Boarding School (ZANIS via Eastern Province administration, 2024 CDF, handed over) — held as an aggregate procurement from a single report; no amount or ward.

Aggregates (not rowed): Chama Town Council's audited 2023 financial statements (found on the council site) record total CDF funding of K71,272,568 across both constituencies (Chama North K33,696,448; Chama South K37,576,119, including 2022 underfunding received in 2023) — financial totals only, no project list, not mined for rows. The council's 2024 approvals article records empowerment/bursary approvals only (Chama North: grants K2,280,000/100 people, loans K3,490,000/48 applicants, 123 skills bursaries; Chama South: 104 secondary bursaries, 156 skills bursaries).

## Funding-year statement, per source

For **every** source: whether it explicitly names a CDF funding year, and which.

| source_key | Explicit CDF funding year? |
|---|---|
| lundazi-2025-approved | **Yes — 2025** (in the document title; applies to all 15 rows) |
| lundazi-handover-2023 | **Yes — 2021 and 2022** (projects are grouped under each year in the text; the final three "other projects" are not separately year-tagged) |
| lundazi-council-news-index | **No** — no year in the captured snippet |
| chasefu-2022-approved-pdf | **Yes — 2022** (in the document title) |
| chasefu-council-tour | **No** — no funding year stated for any toured project |
| chasefu-council-commissioned | **No** — no funding year stated for the commissioned projects |
| chasefu-zanis-kapekesa-2025 | **Yes — 2025** (staff houses; the Kapekesa Health Facility mention is not year-tagged) |
| chasefu-observer-launch-2025 | **No** — no per-project funding year (article is Feb 2025 and mentions completions "since 2021" only in aggregate) |
| chasefu-monitor-contracts-2026 | **No** — CDF mentioned with no funding year |
| lumezi-mlgrd-contracts-2022 | **Yes — 2022** (all 15 contracts and the grader) |
| lumezi-council-commissioned-2022 | **Yes — 2022** (the three commissioned projects; 2023 CDF progress mentioned only in aggregate) |
| lumezi-rcv-2025-contracts | **Yes — 2025** |
| lumezi-observer-health-2025 | **Yes — 2025** ("this year's CDF") |
| lumezi-eas-chamtowa-2023 | **Yes — 2022** (disaster component) |
| lumezi-eas-chamkhoma-2023 | **Yes — 2022** |
| lumezi-parliament-newsletter-2025 | **Yes — 2023 and 2024** (the 13 commissioned projects collectively) |
| lumezi-zedgossip-kapangala | **Yes — 2024** (disaster component) |
| chama-newsletter-2023 | **Partial** — the empowerment-grant sections explicitly say **2022 CDF**, but the individual community-project stories (Champanda, Kaozi, Kalovya, Kajimomo, boreholes, desks, mattresses) state **no funding year** |
| chama-council-commissioned-2022 | **Yes — 2022** |
| chama-council-2024-approvals | **Yes — 2024** (but it lists no community projects) |
| chama-zanis-roads-2025 | **No** — no funding year stated for the road works |
| chama-openzambia-kasangani-2026 | **Yes — 2024** |
| chama-eas-mattresses-2024 | **Yes — 2024** |
| ecz-chama-wards | Not a CDF source — ward/constituency reference only |

## Council website access notes

- **lundazicouncil.gov.zm** — reachable; the 2025 approved-projects PDF opened and read in full.
- **chasefucouncil.gov.zm** — reachable; both council articles opened and read in full. The one failure was the 2022 approved-projects PDF, whose fetch failed with an **upstream tool rate-limit (429) error — a tool-side failure, not a council-site refusal**; only search-snippet fragments of that PDF were verified, which is why its rows are held as an incomplete list.
- **lumezicouncil.gov.zm** — reachable; the commissioning article and council documents (budget estimates, council minutes) were found in search, but no CDF project list/document was found on the site.
- **chamacouncil.gov.zm** — reachable; articles and the audited financial statements PDF were found, but no community-project list is published there that could be found. The council newsletter used here is hosted on **mlgrd.gov.zm**, which was reachable.
- One web search in this pass failed transiently (connection reset); it was not repeated and no finding rests on it. Facebook was not used (login-gated, per brief).

## Biggest gaps

1. **Chama is the biggest gap by far:** 2 rowed projects against a district that received over K71m of CDF in 2023 alone. No constituency-split community project list exists in any source found; most named Chama projects sit in `held.csv` awaiting a council list that splits North/South.
2. **Chasefu's official 2022 list is captured only in fragments** (fetch failure, above) and no Chasefu list for any other year was found; the 12 rowed Chasefu projects have no amounts and no funding years because the two council articles publish neither.
3. **Lumezi 2025 is mostly unnamed:** 19 approved projects, only 8 distinct ones named in published sources; and Lumezi has no published per-project amounts for any 2025 project (only combined totals).
4. **Lundazi has amounts for nothing:** its exemplary 2025 list has no budget column, and no other-year Lundazi list was found.
5. **Per-project amounts exist in this cluster only where contracts were published** — the Lumezi 2022 MLGRD breakdown is the sole source in the whole fragment with project-level contractor + amount data.

---

# Part 3 — Petauke–Katete cluster (Petauke Central, Kaumbwe, Kapoche, Msanzala, Milanzi, Mkaika, Nyimba)

# Eastern Province CDF — Petauke–Katete cluster coverage report

Collected: 30 October 2026 (research pass, published sources only).
Output: `projects.csv` — **62 project rows** across the 7 assigned constituencies, plus **16 held rows** in `held.csv` and **21 sources** in `sources.csv`.

## Important council-attribution correction

The assignment brief grouped Kapoche and Msanzala under Petauke District Council. The published record says otherwise, and the rows follow the published record:

- **Kapoche is in Sinda District (Sinda Town Council)** — Sinda's own financial statements and About page state the district's two constituencies are Sinda and Kapoche. Kapoche sources below are therefore Sinda Town Council / ZANIS-Sinda items.
- **Msanzala is administered mainly by Lusangazi Town Council** (Lusangazi District was split from Petauke; the Petauke/Lusangazi Joint IDP notes Msanzala is shared, with 4 wards — Nyakawise, Mateyo Mzeka, Lutwazi, Singozi — on the Petauke side). All Msanzala rows found came from Lusangazi-side sources (Eastern Provincial Administration/ZANIS and Lusangazi Town Council). No Petauke-side Msanzala project list was found.
- Petauke Town Council itself covers **Petauke Central and Kaumbwe only** (its website says so in terms).

## Per-constituency coverage

### Petauke Central (Petauke Town Council) — 2 projects.csv rows

Only one council article names individual projects: the commissioning of 21 community projects completed under the 2022, 2023 and 2024 CDF (total **K9,499,043.32** for all 21 — aggregate, not split per project). Only two projects are actually named in the article text — the Kang'ambwa Primary School rehabilitation (Nsimbo Ward) and the Petauke Boarding School ablution block/storeroom rehabilitation (Nyika Ward) — and only those two are rowed, as `completed`. The other 19 commissioned projects are not named anywhere in the published text: **this is the cluster's biggest single gap**. No approved-projects list for Petauke Central was found on the council site (unlike Kaumbwe's 2022 PDF). Aggregates only: ZANIS (4 Feb 2026) reported K22.8m disbursed in Petauke district in Q4 2025 — K17m Petauke Central, K5.8m Kaumbwe — plus loan/grant counts; no project names. A Petauke news-index headline on six CDF-funded skip bins (2026 CDF) does not state a constituency and is held.

### Kaumbwe (Petauke Town Council) — 14 projects.csv rows, 1 held

The strongest Petauke source: the council's official **List of Approved 2022 Community Projects under Kaumbwe Constituency** (PDF) — 9 projects with per-project approved allocations (annual community-projects total K13,916,550.00) plus a second list of 5 projects with funds varied from the 2022 bursaries component (total K4,367,473.62). All 14 are rowed as `approved`. Notes: (a) the PDF's "LOCATION" column values (Kaumbwe, Lusinde, Manjazi, Manyane, Kanyanga) are exactly Kaumbwe's five wards per the Petauke/Lusangazi Joint IDP, so they are recorded as wards; the two constituency-wide items (Water Project — at least 22 boreholes; Procurement of desks — various schools) and the varied-list Water Project (6 boreholes) have no ward. (b) The two "Water Project" rows are distinct items from the PDF's two separate lists and are kept separate. (c) The "CDF Vehicle" (monitoring vehicle, K1,200,000) is recorded with component `admin`. No Kaumbwe list for 2023–2026 was found. Held: the Mpamanzi–Mando bridge, raised only in an MP's December 2025 parliamentary speech (contractor on site but unfunded; K30,743,762.24 CDF said to be owed to Kaumbwe — aggregate).

### Kapoche (Sinda Town Council — see correction above) — 6 projects.csv rows, 1 held

No Kapoche project list could be opened in this pass (see gap note below). Rows come from the ZANIS commissioning report published by the Eastern Province Provincial Administration (21 May 2025): five named Kapoche projects with exact costs, all commissioned = `completed` (Kapungwe Rural Health Center rehabilitation K314,000; Chipungu 1×3 classroom block rehabilitation K196,384.88; Mshawa Health Post K1,660,323; Mwangaila Primary School 1×3 block K1,478,496; Nyanje Day Secondary School boys' dormitory K680,663). No wards or per-project funding years are stated for the Kapoche items (the Sinda-constituency items in the same article do carry years; the Kapoche ones do not). Sixth row: Sinda Town Council's own report of the district mortuary under the **2025 CDF, Kapoche Constituency, at 45% completion** (completion_pct = 45, status `ongoing`; article text captured via the council's author archive — the individual article URL was not captured). Held: Lemmy Bridge (Luandazi Ward) — parliamentary debate and council news index conflict on its status. **Known-but-unopened lists:** Sinda's Publications page lists spreadsheet/PDF documents titled "2022 CDF Sinda and Kapoche Project", "2024 Kapoche CDF Community split projects", "2022 Kapoche Approved Incomplete CDF Community Projects" and "2025 Kapoche Constituency List of Approved CDF Projects". Their download links could not be captured with the text-fetch tool in this pass — retrieving them is the single highest-value follow-up for this cluster. Sinda council minutes (Oct 2025) also reference a detailed 2024/2025 CDF status table (Appendices A and B) that is not reproduced in the published minutes PDF. Aggregates: Sinda financial report FY2025 — Kapoche community projects K19,582,558 (2025) / K11,453,232 (2024).

### Msanzala (Lusangazi Town Council — see correction above) — 13 projects.csv rows, 2 held

Two official sources. (1) ZANIS via Eastern Provincial Administration (25 Jan 2023): three items handed over under the **2021 and 2022 CDF** — 33 rehabilitated boreholes ("over K1.2 million" — the row carries 1200000; the "over" qualifier is noted here), Chikuse Primary School staff-house repairs K95,172, Kalumbi Primary School 1×3 block rehabilitation K495,000. The borehole figure is a programme total for that single published item, not a split. (2) Lusangazi Town Council, 6 Nov 2025: contracts signed for the last phase of 2025 projects, headed "Key Projects Awarded (2024 & 2025 CDF)" — rowed as `ongoing`: completion of Mudonsa Health Post; maternity annexes in Nyakawise and Mateyo Mzeka Wards (rowed separately per ward); classroom blocks at six named primary schools (Kasangazi, Kasuma, Mudonsa, Nsenya, Mzenje, Ukwimi — the source groups them as "construction and rehabilitation of CRBs", rowed per school); and the Makale Primary School staff house, the one row with a published contractor (Chalex Investments Limited). No amounts published for any of these. Held: Msanzala Bridge (commissioned 3 Sep 2025; the council article does not explicitly state the bridge itself was CDF-funded) and Masomphenya Primary School, Chingolo Ward (council news-index excerpt only, full article not opened). Aggregate: over K3m invested in Msanzala empowerment in 2025 alone (Lusangazi council).

### Milanzi (Katete Town Council) — 18 projects.csv rows, 1 held (+2 unattributed held)

Backbone: Katete Town Council's official **Milanzi Constituency CDF Approved Community Projects in 2025** PDF — 17 items, no wards, no amounts, all rowed as `approved`. Item 1 as published bundles four works (1×2 CRB at Zakonka Primary School; wiring of Kalimeta Primary School, Kamphambe Rural Health Post and Chilingondi School) and is kept as one row, as published. Plus one row from the council's 24 Nov 2025 stakeholder minutes: the clinic in **Kazala Ward**, unfinished and unused — status `ongoing` (the minutes say that since 2021 no Milanzi project has been fully completed; the minutes' detailed Appendix A progress report is not reproduced in the published PDF, a noted gap). Held: the Mzime Health Post maternity annex (Dole Ward) — official ZPPA contract award with contractor (Kwasu General Dealers Limited) and price (K1,201,889.41), but the award notice text captured does not state CDF funding. The Kamphambe Zakonka ablution block (incomplete, per the same minutes) is held unattributed — the minutes do not state its constituency. ZPPA tender notices corroborate several 2025-list items at implementation stage (ablution blocks and water schemes at Kawaza/Kapepe/Chakhompwa, staff houses at Kagoro Police Post and Bombwe Health Post) but were not rowed separately — they are the same projects as the approved list.

### Mkaika (Katete Town Council) — 8 projects.csv rows, 1 held

Katete Town Council's official **Mkaika Constituency CDF Approved Community Projects in 2025** PDF — 8 items with wards for six of them (Chimtende, Chavuka, Mphangwe, Matunga, Chilongamawe, Kamiza, as sequenced in the document), no amounts published, all `approved`. The two road items (Kapako School road/Undi culvert; the multi-road rehabilitation package) carry no ward in the document. Held: Omelo Mumba Primary School 1×3 block (ZANIS, 2023, 2022 CDF, K470,000) — the article contradicts itself on status ("have been completed" vs "is nearing completion") and mentions Front Line Construction Company without plainly naming it as this project's contractor. Aggregates: Katete Town Council via Open Zambia (16 Jun 2026) — over K45m invested in community projects across Mkaika and Milanzi 2022–present, over K10.7m in bursaries to 1,000+ students; MLGRD's July 2025 commissioning covered 40 Katete projects (CDF 2022–2024) of which only three are named (Kanjeza Secondary School, Soweto Market, Kagolo Admission Ward) and none is attributed to a constituency — all three are held unattributed. The district water bowser (2023 CDF) is likewise held unattributed.

### Nyimba (Nyimba Town Council) — 1 projects.csv row, 4 held

The thinnest constituency in the cluster. **No project-level CDF list for Nyimba was found anywhere** — no approved-projects PDF, no project database, despite the council homepage advertising a "CDF Projects" section ("View ongoing and completed CDF projects across Nyimba District") whose underlying project list could not be retrieved as text in this pass. The single rowed project is the Nyimba District Hospital standby generator (2023 CDF, K548,183, received/procured — `completed`, from the council's own article). Nyimba district is treated as a single-constituency district for CDF purposes (the council's 2026 CDF allocation figure of K40,032,550 is one constituency's allocation), but the council's September 2026 stakeholder minutes describe the district as having "two constituencies" — that internal inconsistency is one reason district-level items from those minutes are held rather than rowed. Held: Chimphanje Mothers Shelter (homepage photo caption only); and three items named only in the Sept 2026 stakeholder minutes' summary paragraph (motorbike for Chinambi Rural Health Centre; solar system at the DEBS office; banana boats), where the minutes group items as "completed or substantially advanced" without saying which. Aggregates (not rowed): 31 projects under the 2024 CDF handed over for a total of K9,832,898.16 (council; the 31 projects are not named in the captured text); the council's 2025 Output-Based Budget plans 1,000 desks, 12 boreholes, 2 maternity annexes, 1 skills centre, 3 classroom blocks, a chief's palace and an ablution block (programme lines, not named projects); CDF disbursed by 30 June 2026 K13,671,085.12 of K40,032,550 (34%).

## Funding-year explicitness, per source

| source_key | Explicitly names a CDF funding year? |
|---|---|
| petauke-kaumbwe-2022-approved | **Yes — 2022** (title; second list is funds varied from the 2022 bursaries component) |
| petauke-central-commissioning | Partially — projects completed under **2022, 2023 and 2024** CDF combined; no per-project year |
| katete-mkaika-2025-approved | **Yes — 2025** |
| katete-milanzi-2025-approved | **Yes — 2025** |
| katete-stakeholder-minutes-2025 | No per-project year — meeting is a feedback assessment for the **2025** CDF; the Kazala clinic's funding year is not stated |
| katete-loans-grants-2024 | **Yes — 2023** for the water bowser; 2024 for the loans/grants programme |
| eas-sinda-commissioning-2025 | **No** for the Kapoche items (years are given only for the Sinda-constituency items in the same article) |
| sinda-mortuary-2025 | **Yes — 2025** CDF |
| sinda-publications | Years in document titles only (**2022, 2024, 2025** Kapoche lists) — documents not opened |
| eas-msanzala-handover-2023 | **Yes — 2021 and 2022** CDF combined |
| lusangazi-contracts-2025 | **Yes — 2024 & 2025** CDF combined; no per-project split |
| lusangazi-msanzala-bridge-2025 | No funding year stated |
| lusangazi-news-index | No funding year stated |
| nyimba-genset-2023 | **Yes — 2023** CDF |
| nyimba-stakeholder-minutes-2026 | No single year — minutes review **2025** budget performance; items not tied to a funding year |
| nyimba-homepage | No funding year stated |
| eas-katete-omelo-2023 | **Yes — 2022** CDF |
| mlgrd-katete-40-projects-2025 | Range only — CDF **2022 to 2024** |
| parliament-debates-2025-12-10 | No per-project year (Kaumbwe CDF arrears figure and Lemmy Bridge funds discussed without a project year) |
| zppa-mzime-award-2025 | No — the award notice does not mention CDF at all in the captured text |
| petauke-news-index | **Yes — 2026** CDF (skip-bins headline) |

## Council sites and access notes

- All five relevant council sites were reachable through search and text fetch at least once: petaukecouncil.gov.zm, katetecouncil.gov.zm, sindacouncil.gov.zm, lusangazicouncil.gov.zm, nyimbacouncil.gov.zm. No council site outright refused a connection in this pass.
- One batch of page fetches (Katete approved-2025 PDF and the Sinda Publications page) failed with an upstream **429 rate-limit from the fetch service** (not a council refusal). The Katete Mkaika list was recovered in full from two independent search-result extracts of the PDF; the Milanzi PDF (approved-2025-1.pdf) was subsequently opened in full. The Sinda Publications page itself was read via search extracts, but the individual Kapoche spreadsheet/PDF download links on it could not be captured — see the Kapoche gap above.
- Sinda Town Council's homepage carries a "CDF Tracker" snapshot (17 projects, budgets, contractors, completion percentages). The items visible in the snapshot are in **Sinda constituency, not Kapoche**, and several entries look like template/demo data (generic contractor names); it was **not used** as a source.
- Facebook was not used (login-gated), per instructions.

## Biggest gaps

1. **Sinda's published Kapoche lists (2022, 2024, 2025) exist but could not be opened** — Kapoche coverage (6 rows) is a fraction of what those documents hold.
2. **Petauke Central: 19 of 21 commissioned projects are unnamed** in the only council article; no approved list found (2 rows only).
3. **Nyimba: no project-level list found at all** (1 row); the council's advertised CDF Projects section could not be retrieved as a list.
4. **Per-project amounts are missing for all Katete 2025 rows and all Lusangazi rows** — both councils publish names (and Katete, wards) without budgets. Contractors are almost never published (one exception: Chalex Investments Limited, Makale Primary School staff house, Msanzala).
5. **Katete's detailed CDF progress appendix (Appendix A to the Nov 2025 stakeholder minutes) is not in the published PDF**, and Sinda's 2024/2025 status appendices are likewise missing from its published minutes — the two documents that would resolve most held rows.
6. Msanzala's Petauke-side wards (Nyakawise, Mateyo Mzeka, Lutwazi, Singozi) are covered by the Lusangazi sources used here for two of them (Nyakawise, Mateyo Mzeka maternity annexes); no Petauke Town Council Msanzala list was found.

---

# Part 4 — South cluster (Chadiza, Sinda, Malambo, Vubwi)

# Coverage — Eastern Province, Southern-Eastern Cluster (frag-south)

Research date: 2026-10-30. Method follows the Lusaka pilot: only rows taken plainly
from officially published lists go in `projects.csv`; weaker, incomplete,
conflicting or single-report rows go in `held.csv`. Figures are quoted exactly
as published (converted to plain numbers, no commas, in the CSVs). No names,
amounts, wards or contractors were invented.

Summary counts:
- projects.csv: 72 rows (Vubwi 45, Chadiza 16, Malambo 11, Sinda 0)
- held.csv: 24 rows (Sinda 13, Chadiza 5, Malambo 3, Vubwi 3)
- sources.csv: 15 sources

## Chadiza (Chadiza Town Council — chadizacouncil.gov.zm)

Found:
- "Chadiza Town Council Commissions 11 CDF Projects" — Chadiza Town Council's own
  website (source_key `chadiza-commissioned-11`). 10 discrete commissioned projects
  taken into projects.csv as completed (Chamandala Staff House, Chamandala Maternity
  Annex with Water Scheme, Ngala Maternity Annex with Water Scheme, Ngala Staff
  House, Motor Grader, Tractor Loader Backhoe (TLB), Compactor, Tipper Truck, Water
  Bowser, Maternity Wing at Chadiza Urban Clinic). No per-project amounts are
  published in that post — only a combined "over K13 million" for the equipment fleet,
  which was NOT split across projects. The 11th item, the Official Flag-Off of the
  2025 Road Works Programme, is in held.csv (programme flag-off, not a discrete project).
- "CDF Community Projects Update" — Chadiza Town Council category page
  (source_key `chadiza-2025-update`). 6 projects taken into projects.csv as ongoing:
  maternity annexes at Mwala, Chamaseche, Kapachi and Chafulu, and classroom blocks
  at Madzaela and Kabvumo, all stated to be above ring-beam level. No amounts or
  ward names published (the names given are places, not confirmed wards, so the
  ward column is blank).

Held (5 rows): Zemba Health Centre Rehabilitation (single council post; contractor
Chikondi General Suppliers and Contractors named, but the contract sum is printed
in a garbled form in the post, so no figure recorded); Ngala Health Post Expansion
(update post conflicts with / duplicates the commissioned Ngala rows); Chamandala
Health Post Borehole Upgrade (single post, no amount); Girls Dormitory at Kalembe
Day School (single post seen only in the council author feed); the 2025 Road Works
Programme flag-off.

Gap: **No Chadiza approved-projects list / CDF project database PDF was findable.**
The council publishes news-style posts about individual projects and commissioning
ceremonies, but no tabular approved list for any year was found on
chadizacouncil.gov.zm, MLGRD, or the National Assembly site. A January 2024 ZANIS
report (via Eastern Province Provincial Administration) states the council planned
15 community projects for 2024 and had procured 5,120 desks from 2022/2023 CDF and
planned 3,198 more desks, but it does not name the 15 projects, so no rows were
taken from it.

Funding-year naming, per source:
- `chadiza-commissioned-11`: does NOT explicitly name a CDF funding year for the
  commissioned projects as a whole (the post only names the "2025 Road Works
  Programme" for the road item).
- `chadiza-2025-update`: YES — explicitly "2025 CDF projects" (2025).
- `chadiza-zemba-rehab`: names the CDF Disaster Component as the funding source;
  work started 14 February 2024; no CDF funding year explicitly named.
- `chadiza-chamandala-borehole`: no CDF funding year explicitly named.
- `chadiza-council-news-feed`: no CDF funding year explicitly named for the
  Kalembe dormitory item.

## Sinda (Sinda Town Council — sindacouncil.gov.zm)

Found — but nothing that qualifies for projects.csv:
- The council **Publications page** (`sinda-publications`) lists exactly the right
  documents: "2022 CDF SINDA AND KAPOCHE PROJECT", "2024 SINDA APPROVED_INCOMPLETE
  CDF COMMUNITY PROJECTS", "2024 SINDA CONSTITUENCY APPROVED_CDF_COMMUNITY PROJECTS",
  "2025 SINDA CONSTITUENCY LIST OF APPROVED PROJECTS" (and Kapoche equivalents,
  which are out of scope for this fragment). However, the text fetch of that page
  returned the document titles without their download URLs, and web searches did
  not surface the PDFs directly, so the contents of those approved lists could
  not be read or transcribed. **This is the biggest recoverable gap in this
  fragment: the lists exist on the council site but their file URLs need a live
  browser session to extract.**
- ZANIS commissioning report, 21 May 2025, via Eastern Province Provincial
  Administration (`sinda-commissioned-20-zanis`): 20 CDF projects commissioned
  across Sinda and Kapoche constituencies. The 7 rows the report plainly attributes
  to **Sinda Constituency** are in held.csv (Gumbi 1x3 classroom block
  K1,600,181.71; Tikondane 1x3 classroom block K1,433,791; Kasambandola 1x3
  classroom and ablution blocks K1,030,303.69; Kaingo Health Post ablution block
  K465,804; Seya ablution block K416,936.52; Sambani water reticulation K270,040;
  Tilewe water reticulation K270,040). Held because it is a single news report,
  not a council published list, and it says the projects were "among others"
  (incomplete). Kapoche rows in the same report were not collected (out of scope).
- Council website **CDF Tracker** (`sinda-cdf-tracker`, redesigned site, page
  states "Updated 15 September 2026"): page states 17 projects / 17 contracts, but
  only 6 project cards were readable in the text fetch (Kaphika Community School
  Staff House; Sewa Chikankeni Rural Health Post; Chassa Nyanje Road Grading;
  Staff House at Masulwe Primary School; Sinda District Library Construction;
  Nyanje Borehole & Water Scheme — with budgets, contractors and completion %
  as published). All 6 are in held.csv: the tracker does not name a CDF funding
  year and does not state constituency, and Sinda District covers both Sinda and
  Kapoche constituencies, so attribution to Sinda constituency is uncertain.

Gap: **Sinda has 0 rows in projects.csv** despite the council apparently publishing
approved lists for 2022, 2024 and 2025 — the gap is access to the PDF contents,
not absence of publication. A live-browser pass over sindacouncil.gov.zm
Publications to capture the PDF URLs is the recommended follow-up.

Funding-year naming, per source:
- `sinda-publications`: the listed document titles explicitly name CDF years —
  2022, 2024 and 2025 (contents not read — see gap above).
- `sinda-commissioned-20-zanis`: partially — it explicitly states the Gumbi row
  was under the **2022** CDF allocation and the Tikondane row under the **2023**
  CDF allocation; no funding year is stated for the other Sinda rows.
- `sinda-cdf-tracker`: NO CDF funding year named (page is headed as a live/2026
  tracker and mentions a separate "33 approved projects for 2026" district total,
  but no per-project funding year).

## Malambo (Mambwe Town Council — mambwecouncil.gov.zm)

Found:
- "Appendix I. List of Approved 2024 CDF Community Projects" — Mambwe Town Council
  PDF (`mambwe-2024-approved`). All **11 projects** taken into projects.csv as
  approved, with wards and estimated costs exactly as published (total as printed,
  K16,589,200.12, matches the sum of the 11 rows and the "K16.5 million / 11
  community projects under 2024 funding" statement in the council newsletter).
  Note row 2 (Motor Bikes for Chief Retainers) lists chiefdoms (Jumbe, Malama,
  Kakumbi, Mknhanya, Nsefu, Msoro), not a single ward, so its ward column is blank;
  row 3's estimated cost is the 2024 additional amount (K3,038,239.48) as published
  in the estimated-cost column, not the K4,038,239.48 contract sum mentioned in
  the comments column.

Held (3 rows): Mtetezi Acrow Bridge (ZANIS report; CDF/RDA jointly funded —
K3.5m CDF contribution vs K7m total, ward given as Msoro Central / Msoro in
different reports); the 2023 CDF roads grading/gravelling programme from the
council newsletter (K1.5m programme total, not per-project); rehabilitation of a
1x3 classroom block at Ncheka Primary School (named only on the newsletter cover).

Not used: the council's "2025 CDF Community Projects Applications" PDF
(`mambwe-2025-applications`) is an **applications / CDFC-recommendations** document
(Appendix II), not an approved list, so no rows were taken from it. It also
contains applicants' personal phone/NRC data. The council newsletter otherwise
covers bursaries, desk distribution (1,900 desks in 2022, 1,000 in 2023 — programme
figures, not per-project rows) and cash-for-work, which are out of scope here.

Funding-year naming, per source:
- `mambwe-2024-approved`: YES — explicitly "Approved 2024 CDF Community Projects"
  (2024). Row 1's comment also references initial allocation under 2023 funding.
- `mambwe-newsletter-2024`: YES for the items it covers — "11 CDF Community
  Projects Approved under 2024 Funding" (2024), and the roads item is explicitly
  "2023 Constituency Development Fund" (2023).
- `mambwe-2025-applications`: YES in its title (2025) — but it is an applications
  document, not an approved list (no rows taken).
- `mambwe-acrow-bridge-eas`: no CDF funding year explicitly named (report dated
  9 July 2025; a related October 2024 report also names no funding year).

## Vubwi (Vubwi Town Council — vubwicouncil.gov.zm)

Found — the strongest coverage in this fragment:
- "List of Approved Community Projects for funding under the 2022 Constituency
  Development Fund" — Vubwi Town Council PDF (`vubwi-2022-approved`). All **30
  projects** taken into projects.csv as approved, with sector, ward and cost as
  published (grand total as printed: K13,935,384.66). Two costs are printed with
  misplaced decimal points in the PDF ("115.375.00" and "52.756.52") and were
  recorded as 115375 and 52756.52 respectively, consistent with the printed
  subtotals.
- "List of Approved Community Projects for funding under the 2024 Constituency
  Development Fund" — Vubwi Town Council PDF (`vubwi-2024-approved`). All **15
  projects** taken into projects.csv as approved, with location, ward and amount
  as published (grand total as printed: K16,589,200.12).

Held (3 rows): earth moving equipment and community radio station commissioned
in November 2023 (single ZNBC/Zambia 24 report; combined K4.7m total also covered
a conference hall built with Local Government Equalisation Fund money, so no
per-project CDF figure can be split out); a water scheme in Mlawe ward (K250,000,
stated as 2021 CDF) seen only via a mirror of a council post.

Gap: No Vubwi approved list for 2023 or 2025 was findable — only the 2022 and
2024 lists are published on the council site as far as could be found. The
council's 2026 Output Based Budget narrative mentions planned 2026 community
projects (e.g. a bull dozer, classroom blocks at Chigwe and Zozwe secondary
schools, a mortuary/theatre at Chikoma Health Centre) but that is a budget
narrative, not an approved-projects list, so no rows were taken from it.

Funding-year naming, per source:
- `vubwi-2022-approved`: YES — explicitly 2022 CDF.
- `vubwi-2024-approved`: YES — explicitly 2024 CDF.
- `vubwi-commissioning-zambia24`: NO CDF funding year explicitly named (report
  dated 26 November 2023).

## Council site access notes

- chadizacouncil.gov.zm, sindacouncil.gov.zm, mambwecouncil.gov.zm and
  vubwicouncil.gov.zm were all reachable via the search/text-fetch crawler; no
  council site outright refused a connection during this pass. One Chadiza
  article fetch hit a crawler rate limit (429 from the fetch service, not the
  council site) and was completed from the search-result text instead.
- The Sinda Publications page limitation is a link-extraction problem (titles
  readable, download URLs not returned), not a connection refusal.
- Facebook was not used (login-gated, per brief). MLGRD and National Assembly
  searches returned no constituency-level project lists for these four
  constituencies (a National Assembly committee report on the Auditor General's
  2022 CDF report mentions Chadiza only in aggregate/audit-finding terms, with
  no project list usable as rows).

---
