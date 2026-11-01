# Central Province CDF expansion — coverage report

Collected: 30 October 2026 (research pass, published sources only).
Output: `projects.csv` — **91 project rows** across 9 of Central Province's 15 constituencies, traced to 10 project-level sources in `sources.csv` (28 sources captured in total; the rest support `held.csv` or document gaps). `held.csv` holds **37 rows** that must not go live without review. The ingest validator (`expansion_ingest.py central`, dry run) accepts all 91 main rows with zero problems.

**Two independent totals reconcile exactly**, which cross-validates the transcription:
- Muchinga 2023 list: the 22 rowed allocations (including the itemised sub-costs of the four health-post completions) sum to the document's own stated community-projects total of **K15,324,450.00**.
- Mumbwa 2025 contracts: the 13 rowed contracts plus the held K5,900,000 roller-compactor contract sum to the council's stated **K23,617,793.70**.

## Naming notes (read before ingest review)

- **"Mumbwa Central" → Mumbwa.** Mumbwa Town Council's post calls the constituency "Mumbwa Central"; rows are filed under the ECZ name **Mumbwa**, as instructed.
- **"Serenje Central" → Serenje.** Serenje Town Council uses "Serenje Central" throughout; rows are filed under the ECZ name **Serenje**.
- **"Mwembezhi" → Mwembeshi.** Shibuyunji Town Council spells the constituency "Mwembezhi"; rows use the ECZ spelling **Mwembeshi**.
- **"Katuba" in Mkushi is a place, not the constituency.** The Mkushi maternity wing is at a locality called Katuba inside Mkushi District. It is filed under Mkushi North and must never be merged with Katuba Constituency (Chibombo).
- **"Kabwe Kupela" is in Serenje District**, not Kabwe. The Muchinga 2023 health post of that name is filed under Muchinga, ward Kabwe Kupela, as the source states.
- **Mkushi attribution.** Mkushi Town Council's CDF work is filed under **Mkushi North**: since Luano District was separated from Mkushi District in August 2013, Mkushi South's CDF is administered by Luano Town Council (whose own posts run the "Mkushi South CDFC"), leaving Mkushi Town Council with Mkushi North. The council posts themselves say only "Mkushi District" — the attribution rests on this jurisdictional split and is flagged here for the record.

## Per-constituency coverage

**Chisamba — 18 rows (main) + 1 held.** The strongest single source in the province: Chisamba Town Council publishes a formal **2025 CDF approved community projects list** (PDF) with project name, ward, zone and sector for all 18 projects. No amounts or contractors are published in it. A separate council contract-signing post names contractors for three projects that match the 2025 list (staff house at Mulungushi Agro — Lemon Civils and General Dealers; staff house at Lombwa — spelled "Nankolo" in the approved list's orbit, contractor Nankolo Investments; 1x2 CRB at Makeni — Njonjo General Dealers) but states no CDF year, so those contractor names were **not** merged into the approved rows; the post's fourth project (ablution block at Chisamba Market, Samweba Construction) is in held.csv.

**Chitambo — 7 rows (main) + 2 held.** Chitambo Town Council publishes a **CDF 2024 list of approved community projects** (PDF) — only 4 numbered projects, two of them bundled packages: "Mpempa Health Post" (Nakatambo Ward) covers a maternity annex, ablution block, incinerator, solar-powered water reticulation system and medical equipment; "Katonga Health Post" covers a maternity annex plus its medical equipment. Names are rowed as published; the bundling is recorded here. No amounts are published. A council commissioning post adds 3 completed projects (combined K2,235,850.16 for four projects — the post says four but names only three; the unnamed fourth could not be rowed). Two 2022-CDF school packages known only from an invitation for bids are held.

**Muchinga — 25 rows (main).** Serenje Town Council publishes a **Muchinga Constituency 2023 CDF projects** document (PDF) with ward, sector and allocated funds for 22 community projects. Four health-post completions (S/N 11–14) publish itemised sub-costs rather than one figure; their rowed budgets are the sums of the published sub-costs, proven by the exact reconciliation with the document total (see above). Ward extraction for S/N 13 (Koffi Kunda) and S/N 21 (Kampabwa) was not legible in the document's table layout, so wards are blank rather than guessed; S/N 19 (Ipila) the same. The document's separate K806,550 disaster-management line (all fields "TBA") was not rowed. Three further Muchinga contracts come from the council's CDF contract-signing post (solar systems at six health posts; ablution block and water reticulation at Nchimishi Primary School, Masaninga Ward).

**Serenje — 2 rows (main).** Only the two Serenje ("Serenje Central") contracts from the council's contract-signing post: 25 solar streetlights on Ng'answa Road and the main bus station waiting shelter, both Ibolelo Ward, with contractors and amounts. Serenje Town Council's Publications page lists full approved-project documents for Serenje (2022 community projects; 2025 approved projects by ward; 2025 conveyance notifications for both constituencies) but the document files themselves could not be retrieved in this pass — the page exposes titles only through the available tools. This is the province's most recoverable gap: the lists demonstrably exist.

**Nangoma — 7 rows (main) + 6 held.** Mumbwa Town Council's 29 Aug 2025 post lists the **2025 CDF contract signings** with constituency, ward (mostly), contractor and exact amount for every project — 7 Nangoma rows rowed, all reconciling into the council total. The two-constituency roller-compactor contract is held (×2). Separately, the MLGRD **2026 CDF approval for Nangoma** (10 applications, K23,788,461.45, letter dated 12 Feb 2026) is published as a scanned PDF whose table extraction is garbled; five identifiable items are in held.csv with amounts blank or flagged, pending a visual read of the PDF.

**Mumbwa — 6 rows (main) + 1 held.** The other half of the Mumbwa Town Council 2025 contract-signing post (filed under ECZ name Mumbwa; see naming notes). The same ceremony's ultra-modern bus station in Itezhi Tezhi Compound (K2,541,681.86, Winners Business Solutions) is **excluded entirely** — the council states it is funded under the Zambia Devolution Support Program (ZDSP) 2024, not CDF.

**Mwembeshi — 17 rows (main) + 1 held.** Shibuyunji Town Council's commissioning post names 8 × 1×3 classroom blocks (school + ward for each), 7 water reticulation systems (site + ward for most), 8,000 procured desks and the rehabilitated Nampundwe Police Post (K362,431.28 — the only per-project amount). Classroom blocks share a combined K6,652,538.70 and the water systems a combined K812,000, so per-project budgets are blank per the no-splitting rule. The nine staff houses (combined K3,720,608.78, sites not enumerated) are held as one aggregate row. Wards: the water system at Shimatete Primary School takes its ward (Chikonka) from the same post's classroom list; Sala Rural Health Centre's ward is not stated for the water item and is left blank.

**Katuba — 6 rows (main) + 6 held.** The Katuba Constituency Information & Publicity Desk (the constituency office's page, read via a govserv.org mirror — the same source class as the Lusaka pilot's Munali rows) published a clean list of **six commissioned community projects** with wards (1 Aug 2026, combined K2,882,979.04; no per-project amounts, no CDF year stated). A second desk post (the MP's March 2026 Youth Day address) lists six Chunga Ward "milestone" items; those are held as publicity-framed, not a formal list. The same post's three "pipeline" items (Naluyanda Police Post, Kapini Bridge, Kingstone clinic) were not rowed anywhere.

**Mkushi North — 3 rows (main) + 3 held.** Mkushi Town Council's post on the **2022 CDF** projects commissioned on 7 June 2024 gives three projects each with its own cost (Nkumbi water reticulation K419,570; Ilume School ablution block K287,000; Katuba maternity wing K436,000). A ZANIS handover report (Feb 2025: Chibefwe and Kasokota classroom blocks at a combined K1,215,000; 12 vulnerable-person houses in Milombwe at K10 million) is held as news, not a council list. The council's August 2026 news item on **ten commissioned CDF projects worth over K6 million** could not be opened to its project list in this pass (the article body was not retrievable) — a recoverable gap.

**Bwacha — 0 rows (main) + 3 held. Kabwe Central — 0 rows (main) + 2 held.** The province's most frustrating gap: Kabwe Municipal Council's CDF page links formal **2025 approved project lists for both constituencies** (plus bursary, grant and loan lists), but the council site refuses direct connections from this environment and the document URLs are not indexed, so the lists themselves could not be read. What could be captured is held: Yotam Muleya Stadium and the Ngungu Mini Hospital maternity annex (Bwacha, tender notices only), the Prospect Police Station tender (constituency not stated), the 2023 CDF Bwacha road-grading programme (ZANIS report of a council statement, K5,183,631, ZNS, eight wards), and the Kabwe Central Hospital mourner's shelter (MakanDay investigation, ~K890,000, conflicting completion accounts).

**Kapiri Mposhi — 0 rows (main) + 5 held.** Kapiri Mposhi Town Council publishes no CDF project list that could be found — only individual news items (Soweto Clinic handover; Twalumba classroom block seen on a ministerial tour; Mulungushi police post groundbreaking) and ZPPA tenders (Chankomo maternity wing, Lunchu Ward; Chipepo police post, Lukanga Ward). All five captures are held. (The council's K2.2 million TLB purchase names no funding source and was not captured at all.)

**Keembe — 0 rows (main) + 5 held.** Chibombo Town Council publishes no CDF project list that could be found. Captures are two ZPPA tenders expressly "under 2026 CDF" (Chibombo Ward police post package; Malambanyama Ward maternity wing package — no amounts) and the constituency's CDF earth-moving equipment purchase (grader K5.5m, TLB K2.1m, tipper truck K1,998,000) from a single news report.

**Mkushi South — 0 rows (main) + 2 held.** Luano Town Council publishes bursary/grant approvals (aggregates only — 84 secondary bursaries K252,000; 270 skills bursaries K5,672,647; 64 grant beneficiaries K1,910,000 under the 2025 CDF) but **no community project list**. Held: the 2022-CDF Mulungushi River foot bridge tender at Liteta Community (Chimika Ward) and the 2023-CDF fuel bowsers delivery (single news-style council item, no amount).

**Lufubu — 0 rows.** Ngabwe Town Council publishes budgets and a ZDSP (non-CDF) project sheet, plus a general January 2025 explainer on how CDF has helped the district, but **no CDF project list of any kind** could be found. Nothing rowed, nothing held — the gap itself is the finding.

## Funding year, source by source (for later year-tagging)

| Source | Explicit CDF funding year? |
|---|---|
| chisamba-2025-approved | **Yes — 2025** (document title) |
| chitambo-2024-approved | **Yes — 2024** (document title) |
| chitambo-commissioned | No — projects' year unstated (2024 CDF loans were disbursed at the same ceremony) |
| mumbwa-2025-contracts | **Yes — 2025** ("under the 2025 Constituency Development Fund") |
| nangoma-2026-approved | **Yes — 2026** (approval letter, 12 Feb 2026) |
| muchinga-2023-approved | **Yes — 2023** (document title) |
| serenje-contracts | No — post states no CDF year |
| mkushi-2022-commissioned | **Yes — 2022** ("funded by the 2022 Constituency Development Fund") |
| shibuyunji-commissioned | No — community projects' year unstated (the post separately notes 2024 CDF grants disbursed) |
| katuba-commissioned-2026 | No — no CDF year stated (commissioned 1 Aug 2026) |
| chisamba-contracts (held) | No |
| chitambo-2022-ifb (held) | **Yes — 2022** |
| zanis-mkushi-handover (held) | No |
| makanday-kabwe-shelter (held) | Mixed — shelter completed Nov 2023; report discusses 2022 allocations and a further K1.8m from the **2023** CDF |
| zppa-bwacha-stadium (held) | No (tender Oct 2025; CDF itself not expressly stated in the notice) |
| zppa-bwacha-ngungu (held) | No (tender Mar 2026) |
| zppa-kabwe-prospect (held) | No (tender May 2025; CDF not expressly stated) |
| zanis-bwacha-roads (held) | **Yes — 2023** |
| kapiri-council-news (held) | No |
| zppa-kapiri-chankomo / zppa-kapiri-chipepo (held) | CDF in the tender references, but no funding year (tenders Apr 2025) |
| zppa-keembe-chibombo / zppa-keembe-malambanyama (held) | **Yes — 2026** ("under 2026 CDF") |
| keembe-equipment-news (held) | No (reported Mar 2025) |
| luano-2022-tender (held) | **Yes — 2022** |
| luano-council-news (held) | **Yes — 2023** (fuel bowsers) |
| katuba-desk-chunga (held) | No |

## Biggest gaps, in order

1. **Kabwe (Bwacha + Kabwe Central):** formal 2025 approved lists exist on the council's CDF page but were unreachable — the council site blocks direct connections here and the files are unindexed. Needs a browser session that can open kabwecouncil.gov.zm and follow the CDF page links.
2. **Serenje constituency:** the council's Publications page lists the actual 2025 approved-by-ward documents (and 2022 lists) for both Serenje and Muchinga; only Muchinga's 2023 list had a retrievable URL. Same retrieval problem as Kabwe, smaller scale.
3. **Lufubu, Mkushi South, Keembe, Kapiri Mposhi:** no council-published community project list exists in findable form at all — coverage rests on tenders and news singles, all held.
4. **Nangoma 2026:** the official approval exists but only as a garbled scan; a visual read of the PDF would convert 5 held rows (and up to 5 more applications) into main rows with amounts.
5. **Mkushi North:** the council's August 2026 "ten CDF projects commissioned" article body was not retrievable; its list would roughly triple Mkushi North's main rows.

## Addendum — 2026-11-01 council watch: Kabwe + Serenje lists retrieved and ingested

The two biggest retrieval gaps in this province are closed. A live-browser pass extracted the actual document URLs from the Kabwe Municipal CDF page and the Serenje Town Council Publications page (the page-fetch tool strips hrefs; the council sites also refuse direct connections from this network).

**Kabwe Central — 15 main rows (was 0).** The official "Approved Community Projects for 2025 CDF" (CDFC minute KCCDF/29/02/25) is a clean table with wards, sectors and Approved Amounts; the 15 rows sum exactly to the document's printed subtotal K15,326,232.85. Funding year 2025 from the document title. Notes: (a) the medical-equipment row's ward cell prints two ward names unclearly ("david ramushu and luansase"), so the ward is left blank rather than guessed; (b) "procurement of tipper ruck" is rowed as "Procurement of Tipper Truck" (obvious typo); (c) the ablution/water rows keep the document's wards; categories follow the project, not the document's sector label (the C-Gate ablution block is labelled Education in the document).
**Kabwe Central held — 7 rows.** The same document's second table, "Ongoing projects that need additional funds", prints ESTIMATE columns for top-ups to ongoing projects. Those amounts are additional-funds estimates, not approved project budgets, so all 7 rows are held (incl. the Kabwe General Hospital relatives' waiting shelter — related to, but a different document from, the MakanDay mourner's-shelter row already held).
**Bwacha — 0 main, 7 new held rows (9-row list).** The Bwacha document is titled "List of 2025 Community Projects **Recommended by** the Bwacha CDFC" — a recommendation, not an approval, so under the Chipangali policy all rows are held. Seven are new held rows; the other two (Yotam Muleya Stadium; Prospect Police Station) were already held from tender sources. Two things for Caleb: (1) the recommended list places the Prospect Police Station in **Bwacha** (Munga Ward, K3,000,000), while the older held tender row is filed under Kabwe Central because the tender stated no constituency — the list is the stronger attribution, but the held row was not moved without his say; (2) the list's Mukobeko maternity annex (K2,407,693.58) is a different facility from the held Ngungu Mini Hospital annex.
**Serenje — 19 main rows (was 2). Muchinga — 18 new main rows (43 total).** Serenje Town Council's Publications page links both constituencies' 2025 approved lists, but the page's link titles are **swapped**: the "Serenje" link downloads the Muchinga document and vice versa. The documents' own printed titles match their filenames, and rows were filed by the documents' contents. Muchinga notes: the four "Completion of Storage Shelters" rows each bundle three printed sub-lines (water reticulation K250,000 + ablution block K600,000 + shelter balance); each row's budget is the sum of its printed sub-lines, proven by the document's own sector table (Agriculture total K3,665,862.00 reproduces exactly), the same reconciliation class as the Muchinga 2023 sub-costs. The Mupepetwe dormitory row likewise sums its two printed sub-lines (K300,000 + K500,000), proven by the Education sector total. Serenje Central notes: classroom rows sum their printed block + desks sub-amounts, proven by the document's printed main total (K17,750,443.38, reproduced exactly); the document's sector table is internally inconsistent (its Education line excludes one desks sub-line and its sector grand total is digit-transposed) — the main table governs and is what is rowed. Shared district lines: both Serenje-district lists print the same Veterinary Offices (K1,000,000, Ibolelo) and CDF Vehicle Servicing (K1,290,000) rows; each is rowed under its own constituency exactly as published. Funding year 2025 from both documents' titles.
