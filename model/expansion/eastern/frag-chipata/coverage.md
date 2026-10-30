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
