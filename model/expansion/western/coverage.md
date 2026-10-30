# Western Province CDF expansion — coverage report

Collected: 30 October 2026 (research pass, published sources only).
Output: `projects.csv` — **135 project rows** across 12 of Western Province's 19 constituencies, traced to 21 project-level sources in `sources.csv` (29 sources captured in total; 8 are held-only sources for `held.csv`). `held.csv` holds **46 rows** that must not go live without review. Validated clean against `expansion_ingest.py` (dry run, 135/135 rows OK).

## Method note

Same rule as the Lusaka pilot: a row goes in `projects.csv` only when it is taken plainly from an official published list or official council/government publication (council websites, CDFC minutes, council procurement documents, MLGRD, National Assembly), or from a news article that reproduces an official statement/list verbatim (the Nalolo MP press statement; the ZANIS report republished by Africa Press — the same precedent as the pilot's Matero and Chilanga rows). Single news reports of ceremonies, round/planned figures, and anything needing interpretation went to `held.csv`.

## Funding-year explicitness — per source (for later year-tagging)

| Source | Names a CDF funding year? |
|---|---|
| mongu-approved-nalikwanda | **Not on the page itself.** The table sits on Mongu's "Approved Projects" page; the council's separate CDF page links it alongside "2025 Mongu Central / 2025 Nalikwanda Approved Projects" PDFs, so it is very likely the 2025 Nalikwanda list — but the year is not stated in the table, so it is NOT tagged here. |
| mongu-older-news | No year stated for any of the three items (Mabumbu, Kaande, Lukweta). |
| mongu-water-schemes | **Yes — collectively:** "more than 15 water schemes have been constructed from the 2022 and 2023 CDF allocation"; the three rowed schemes are not individually year-tagged in the source. |
| parliament-nalikwanda-simulima | **Yes — 2024 CDF** (stated). |
| parliament-nalikwanda-equipment | No year stated (equipment for facilities "built using CDF"). |
| luampa-2024-approved | **Yes — 2024** (document title: "CDF 2024 Approved Projects"). |
| nalolo-press-statement-2025 | Mostly no; three items carry years inline: Nalolo Primary solar water reticulation **(2024 CDF)**, Lwambi Primary flushable toilet **(2024 CDF — amount truncated in the source, left blank)**, Lunga Combined School 1×3 block **(2023 CDF)**. All other items are undated; the commissioning was July 2025. |
| kalabo-commissioned-14 | No year stated anywhere in the article. |
| sesheke-tracker-2022 | **Yes — 2022** (the tracker page is organised by year; the only populated row sits under 2022, Quarter 1). |
| sesheke-contracts-2025 | **Yes — 2025 CDF allocation** (stated). |
| sesheke-commissioned-2025 | Only the water bowser is year-tagged (**2025 CDF**, per the District Commissioner); the five other projects are undated in the article. |
| senanga-earth-moving-eval | **Yes — CDF 2023** (tender no. STC/CDF23/Q1/EMESUPPLY; evaluation report of 29 Dec 2023). Amounts are the CDFC-approved budgets per lot. |
| senanga-medical-equipment | **Yes — 2022 CDF** for the maternity annexes the equipment serves; the equipment procurement itself is reported without a separate year. |
| nkeyema-maternity-contracts | **Yes — 2024 CDF** for the Mimpongo and Nkeyema Mini Hospital maternity annexes and the Chikamba Bridge (stated). The Kapa Clinic and Munkuye Police Post are described in the same article as under construction under the Presidential directives; their year is not separately stated. |
| nkeyema-kandende-handover | The handover article itself names no year; the sister article (nkeyema-maternity-contracts) states the Kandende annex was built "using the 2023 CDF" at the same K480,000 — cross-source year: **2023**. |
| nkeyema-classrooms-handover | **Collectively only:** the two blocks "were constructed through the 2023 and 2022 CDF" — not assigned per school. |
| nkeyema-ntuba-namamono | **Collectively only, and oddly:** "the 2021 and 2023 CDF allocations funded the projects" — not assigned per school. |
| mwandi-news | No years stated for any of the three items. |
| mlgrd-lukulu-kashongo | No year stated (handover 27 Feb 2023). |
| africa-press-kaoma | **Yes — 2020/2021 CDF** (stated). Pre-dates the CDF increase; amounts are correspondingly small. |
| sikongo-cdfc-minutes-2023 | **Yes — 2024 implementation year** (all 21 approved projects). Document title dates the meeting 28 Dec 2023; the signing note inside says the meeting sat on 23 Nov 2023 — an internal inconsistency in the source, noted here. |
| zambian-observer-mulobezi (held) | No year stated. |
| zambian-observer-liuwa (held) | No year stated. |
| agency-ilute (held) | **Yes — 2023 CDF** (stated). |
| zppa-luena-furniture (held) | No CDF year stated (tender dispatched 25 Nov 2024). |
| mitete-monitoring-2025 (held) | **Yes — 2025 CDF** projects (stated), but only as an aggregate of 20. |
| openzambia-mongu-police (held) | **Yes — 2025 CDF** (stated); 95% complete. |
| melomedia-mangango-2025 (held) | Mixed: maternity wings dated 2022/2023 collectively; 2025 items presented as the 2025 plan within a K17.7m 2025 budget; earlier classroom blocks dated only "2021–2024". |
| melomedia-mangango-equipment (held) | No year stated. |

## Per-constituency coverage

### Mongu Municipal Council (Mongu Central + Nalikwanda)

**Nalikwanda — 18 main rows + 1 held.** The backbone is the council's Approved Projects table (13 projects with wards and estimated budgets totalling K16,585,205). Attribution: the table's own page does not name a constituency, but every ward in it (Nanjeko, Imalyo, Nalwei, Looma, Mutondo, Siyowe) is an ECZ Nalikwanda ward — verified against the ECZ delimitation schedule for Mongu District, which lists Nalikwanda's wards as Looma, Nalwei, Siyowe, Lukalanya, Imalyo, Mutondo, Namengo — and none is a Mongu Central ward. Also rowed: three completed water schemes and the Lukweta maternity annex (council news), and Parliament's report of the completed Simulima health facility built with the 2024 CDF. Held: Parliament's K875,000 medical-equipment delivery to five Nalikwanda facilities, which may be the delivered version of the approved list's K752,205 "health facility equipment" line — amounts differ, so the pair cannot be reconciled yet. Note: Mongu's CDF page also links separate "2025 Mongu Central Constituency Approved Projects" and "2025 Nalikwanda Constituency Approved Projects" PDFs, but the PDF URLs could not be extracted through the text-fetch tool used in this pass — a browser pass could likely recover both lists in full.

**Mongu Central — 2 main rows + 2 held.** Only two council news items could be rowed plainly: the Mabumbu Rural Health Post staff house (100% complete, completion_pct recorded) and the Kaande Health Post staff house (completed). This is an undercount of the same kind as Lusaka Central in the pilot — Mongu publishes updates as one-off news items, not lists. Held: the Ilute maternity annex (K681,106.35, 2023 CDF, The Agency Media) because the report never says which constituency Ilute Ward falls in, and the Kasima Mini Police Station (Open Zambia) because that report attributes it to a "Mongu East Constituency" — a name from the 2026 delimitation, not the current ECZ set.

### Nalolo — 37 main rows + 1 held

The strongest single source in the province: the area MP's signed press statement (reproduced verbatim by the Zambian Observer, 11 July 2025) commissioning 38 CDF projects — 17 East Bank, 21 West Bank — each with an amount, some with wards (Muoyo, Kataba) and three with explicit funding years (2024, 2024, 2023). All 38 were rowed as `completed` (commissioned = handed over) except one: **the Lunga Combined School 1×3 block appears in both bank lists** (East: K794,150.49 tagged 2023 CDF; West: K793,055 untagged). The East Bank entry is in `projects.csv`; the West Bank entry is in `held.csv` as a possible duplicate within the source itself. One East Bank amount (Lwambi Primary flushable toilet) is truncated in the published statement ("(2024 CDF" with no figure) — the row is live with a blank budget. The statement's aggregate claims (7,471 desks delivered; K13 million total) are not rowed.

### Sikongo — 21 main rows

Sikongo Town Council publishes its CDFC minutes, and the Q4 2023 extract ends with a "RESOLVED and APPROVED" table of **21 community projects for the 2024 implementation year**, each with ward/location and an estimate (total K16,589,200.12 — the same total, to the ngwee, as several other districts' 2024 community allocations). All 21 are rowed as `approved`. Judgement calls: (a) the ward column merges ward and site (e.g. "Lumbamba – Shamalumba Community School") — ward is the first element, the site is carried in the project name; (b) item 19, the Chief's Retainer motor bike, is priced "K25,000.00 each" with no quantity — the row carries K25,000 because the document's own total reconciles only if exactly one bike is counted (sum of the other 20 rows is K16,564,200); flagged here for review; (c) the minutes also list 62 WDC applications "considered" — applications, not approvals; not rowed. The council site itself (sikongocouncil.gov.zm) was reachable via its uploads; a ZPPA tender for a Sikongo play park in Maala Ward (2026) was noted but not rowed (tender notice only).

### Kalabo Town Council (Kalabo Central + Liuwa)

**Kalabo Central — 11 main rows.** The council's own handover article lists 14 completed Kalabo Central projects totalling K4,919,858.23 with per-project amounts (the rowed amounts sum exactly to the stated total). Two published groupings were kept as single rows because the source publishes only a combined cost: the five Namulilo Ward boreholes (K638,426.25 combined) and the four water reticulation installations at Ituya, Ng'uma and Lyapepa primary schools and Liumba RHC (K697,300 combined) — splitting them would invent per-project figures. That is why 14 published projects yield 11 rows. Spelling note: the article body names "Nalionwa Primary School"; its own photo caption spells it "Naliyonwa" and places it in Muchatanga Ward — the caption's ward is used. No funding year is stated for any Kalabo Central project.

**Liuwa — 0 main rows, 12 held.** Kalabo Town Council publishes no Liuwa project list that could be found. The only enumeration is a Zambian Observer (Wagon Media) report of the MP's handover tour (16 May 2025) claiming 21 commissioned projects but listing only 17 items (three 1×3 blocks, one 1×2 block, two water schemes, six staff houses at Salunda, four health posts, one Hino truck) with no amounts — all 12 rowable items are in `held.csv` (the six Salunda staff houses kept as one row, as published).

### Sesheke — 14 main rows

Sesheke Town Council is the only Western council running a public "CDF Tracker" page — but it is almost empty: one populated row (Nakatindi Market, K700,000, completed, under 2022 Q1) and blank "Click here to add content" placeholders for the remaining 2022 quarters and all of 2023. The substance came from two council news releases: seven contracts signed under the **2025 CDF** (7 rows, wards stated, no amounts — rowed as `ongoing`, contracts signed 10 Sep 2025) and six commissioned projects (18 Jun 2025) with amounts (rowed as `completed`; the article names the three wards collectively — Maondo, Mulimambango, Silumbu — but does not tie each project to a ward, so wards are blank). Sesheke District has a single constituency, so attribution is plain throughout. (The commissioned-projects article calls the MP "Sesheke Central" — a colloquialism; the ECZ name Sesheke is used.)

### Luampa — 10 main rows

Luampa Town Council's official "CDF 2024 Approved Projects" PDF is a clean, complete list: 10 community projects with wards and costs totalling exactly the document's K16,589,200. All rowed as `approved`. Four items are district-wide procurements whose ward is published as "District Project" (motorbike, 3,845 desks, ambulance, tipper truck, grader — five in fact) and are carried with that ward text as published.

### Nkeyema — 10 main rows + 3 held

Nkeyema Town Council's website carries detailed project news, and Nkeyema District has a single constituency. Rowed: two maternity annexes and Chikamba Bridge under signed **2024 CDF** contracts (K1.2m / K1.1m / K1.2m), Kapa Clinic (K650,000) and Munkuye Police Post (K750,000) described as under construction in the same article (all five `ongoing`); the Kandende RHC maternity annex (K480,000, completed, contractor **Integrity Construction** — one of only two contractor names found in the province); two handed-over 1×3 classroom blocks (Kanatebe K645,300, Shishamba K560,000); and the Ntuba (K425,000) and Namamono (K662,000) blocks. Held: three further classroom blocks (Kalale-Kamazambo, Kanyata, Kankwanda) named in the handover article only as due for handover later that week, with no amounts and no confirmation of completion. Year caveat: the Kanatebe/Shishamba pair is dated only collectively ("2023 and 2022 CDF") and the Ntuba/Namamono pair only collectively ("2021 and 2023 CDF") — see the source table above.

### Senanga — 5 main rows

No community-project list is published by Senanga Town Council. What is official and rowable: the council's own tender evaluation report for earth-moving equipment under **CDF 2023**, which gives the CDFC-approved budget per lot (grader K3,300,000; water bowser, tractor loader backhoe and roller K1,900,000 each — total K9,000,000), rowed as four `approved` equipment projects; and a council news item recording the completed procurement of basic medical equipment (K896,293.59) for the three maternity annexes built under the **2022 CDF** at Mata, Sibukali and Mwanamwalye — rowed as one combined procurement row because no per-annex figure is published (the annexes' own construction costs are not published anywhere found). Senanga's 2022 CDF loans (K2,926,000 to 44 applicants) and 2024 loans/grants (K5,820,740.38 to 147 beneficiaries) are empowerment aggregates — not rowed, per the pilot's convention.

### Kaoma Town Council (Kaoma Central + Mangango; Luampa is now its own council)

**Kaoma Central — 3 main rows.** Kaoma Town Council publishes no CDF project list that could be found (its website returned nothing extractable in this pass). The three rowed projects come from a ZANIS report republished by Africa Press: two health posts and a market shelter completed under the **2020/2021 CDF** and handed over, with per-project costs given by the Council Secretary (Namimbwe K203,000 in Namaloba Ward; Chilombo health post K208,000 and market shelter K187,000 in Chilombo Ward). A Kaoma Central CDF community-projects tender (Mar 2025) exists on tender aggregators but names no projects — not rowed.

**Mangango — 0 main rows, 18 held.** The only Mangango enumeration anywhere is a Melo Media feature (1 Apr 2025) summarising CDF delivery 2021–2025, plus its report of K9 million of earth-moving equipment unveiled by the MP. The feature's 2025 figures are round, planned amounts within a stated K17.7m 2025 budget; its earlier classroom blocks carry only a K600,000–K1,000,000 cost range; none of it reproduces a council list. All 17 feature items and the combined equipment item are in `held.csv` for review — Mangango is the province's largest single held pile and the first place to look if Kaoma Town Council ever publishes its lists.

### Lukulu Town Council (Lukulu East + Mitete district covers Mitete)

**Lukulu East — 1 main row.** One well-documented project: the 1×3 classroom block at Kashongo Primary School, Kangoti Ward, K371,059.25, contractor **MC Kangunge**, handed over 27 Feb 2023 (MLGRD). Lukulu Town Council publishes budgets, annual financial statements and a 2025 CDF loans beneficiary list (32+ individual empowerment loans — not rowed, per the pilot's convention of not rowing individual loan beneficiaries), but no community-project list. A ZANIS-mirror report of three commissioned Lukulu East projects (two 1×3 blocks, one health post, "over K2 million") names none of them — too vague to row; noted here as a lead.

**Mitete — 0 main rows, 2 held.** Mitete Town Council reports strong 2025 delivery — 20 approved CDF projects, six completed and the rest ~80% complete by Nov 2025 (Western Province PLGO monitoring, reported in the National Assembly's Nov 2025 newsletter) — but no project is individually named anywhere found. The only named items are zone-level mentions in council statements: maternity annexes and rural health posts "at Lutumo and Kashizhi zones" — held as two rows with that weakness stated. Mitete's website has a CDF Tracker heading but no extractable project data in this pass.

### Mwandi — 3 main rows

Mwandi Town Council publishes project news but no list. Three items are stated plainly enough to row (single-constituency district): a new clinic in Mushukula Ward (Nov 2025), the Aibelilwe 1×3 classroom block ("100% complete", Mar 2025, completion_pct recorded), and a staff house at Lwazamba Primary School ("100% Complete", Dec 2024). No amounts or funding years are published for any Mwandi project found. The council's news index also references a Sikuzu–Matoya feeder road project launch (Oct 2025) — a launch announcement without CDF attribution detail or figures; not rowed.

### Mulobezi — 0 main rows, 6 held

Mulobezi Town Council publishes no project list that could be found. A Zambian Observer report (9 May 2025) of the council's handover of six completed CDF projects (five 1×3 classroom blocks — Sejamba, Kasamba, Kabula, Salumbwe, Sanembo — and the rehabilitated Machile Police Post, each with an amount, total "over K4.1 million") is detailed but is a single news report, not a reproduced council list — all six are in `held.csv`. (A separate Africa Press/ZANIS item records a teacher's house and classroom block at Chibwe Primary School, Salumbwe Ward, at K410,000/K600,000 — a possible overlap with the held Salumbwe block at a different figure; noted here rather than rowed twice.)

### Luena (Limulunga Town Council) — 0 main rows, 1 held

Limulunga Town Council's CDF page is generic (presidential-directive themes, no projects). Council stakeholder minutes mention CDF delivery in general terms and a *proposed* maternity annex at Sitoya Health Post — a proposal, not a project. The only concrete Luena item found is an official ZPPA tender notice for 1,382 items of school furniture for Luena Constituency (Nov 2024, no amount) — held as a tender-only record.

### Shang'ombo — 0 rows

Shangombo Town Council's website exists (shangombocouncil.gov.zm) but publishes no CDF project list, tracker or project news that could be found in this pass; council social posts report contractor-engagement meetings about CDF community projects without naming any. A genuine publishing gap: no rows, main or held, could be sourced.

### Sioma — 0 rows

Sioma Town Council's website (siomacouncil.gov.zm) exists but no CDF project list or project-level publication could be extracted in this pass. A ZPPA tender for desks for various schools under Sioma Constituency (Apr 2026) confirms procurement activity but names no schools or amounts. Recorded as a publishing gap.

## Biggest gaps

1. **Five of 19 constituencies have no rowable official record at all** (Shang'ombo, Sioma — nothing found; Luena, Mitete, Mulobezi, Mangango, Liuwa — held-only). In every case the cause is the same: the council publishes no project list, tracker or detailed project news online. The gaps are publishing gaps, not evidence that CDF delivered nothing — Mitete alone reports 20 projects delivered in 2025 without naming one.
2. **Mongu Central is the thinnest covered constituency with any rows (2)** despite Mongu Municipal Council being one of the province's better publishers — its output is news items, not lists, and its two 2025 approved-projects PDFs (Mongu Central and Nalikwanda) could not be text-extracted in this pass. Recovering those two PDFs is the single highest-value follow-up for this province.
3. **Per-project amounts are missing for all Sesheke contract rows, all Mwandi rows, and the Mongu news rows** — councils announce projects without figures; amounts exist mainly where a list, minutes or evaluation document was published (Nalolo, Sikongo, Luampa, Nalikwanda-approved, Kalabo, Nkeyema, Senanga lots).
4. **Contractors are almost never published**: only 2 of 135 main rows carry a contractor (Kandende RHC — Integrity Construction; Kashongo Primary — MC Kangunge).
5. **Funding years are explicit for only about half the main rows** (Luampa 2024; Sikongo 2024; Nalolo 3 items; Sesheke 2025 contracts + tracker 2022; Senanga 2023 lots; Nkeyema 2024 contracts; Kaoma Central 2020/2021; Simulima 2024). The Mongu approved table — 13 rows — carries no year on its face (see the source table), and Kalabo, Mwandi, Lukulu East and most Nalolo items are undated.
6. **Empowerment components are published as beneficiary lists, not projects** (e.g. Lukulu East's approved 2025 CDF loans list, Senanga's loan/grant handovers). Following the pilot's convention, individual loan/grant beneficiaries were not rowed anywhere in this province; if the tracker later wants empowerment coverage, Lukulu's official loans PDF is the cleanest starting point.
