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
