# Muchinga Province — CDF project-list coverage

Researched 2026-10-30 following the Lusaka pilot method: only rows taken plainly
from official published lists (council/government publications) are in
`projects.csv`; single news reports, combined-figure items, ambiguous
attributions and conflicting figures are in `held.csv` for review. Empowerment
loan/grant *beneficiary* lists (names of individuals/clubs) were not
transcribed anywhere — see the notes per council; the tracker's unit is the
community project.

Constituency names follow the ECZ delimitation set (Chinsali, Isoka,
Kanchibiya, Mafinga, Mfuwe, Mpika Central, Nakonde, Shiwa Ng'andu). Councils
still use the pre-delimitation names on most documents ("Chinsali Central",
"Mpika", "Shiwang'andu"); rows were filed under the ECZ name for the same
constituency.

## Summary

| Constituency | Council(s) | Main rows | Held rows | Best source |
|---|---|---|---|---|
| Chinsali | Chinsali Municipal | 17 | 0 | 2024 approved projects PDF |
| Isoka | Isoka Town | 7 | 25 | Council approval announcement (2024) |
| Kanchibiya | Kanchibiya Town | 32 | 0 | CDFC minutes, Feb 2025 |
| Mafinga | Mafinga Town | 19 | 1 | Council minutes handover table, Jul 2025 |
| Mfuwe | Lavushimanda Town | 17 | 9 | 2025 contract awards, council site |
| Mpika Central | Mpika Town | 8 | 2 | 2026 approved projects letter (PDF) |
| Nakonde | Nakonde Town | 14 | 0 | 2024 approved projects PDF |
| Shiwa Ng'andu | Shiwang'andu Town | 0 | 5 | Nothing official found — gap |
| **Total** | | **114** | **42** | 17 sources recorded |

## Per constituency

### Chinsali (Chinsali Municipal Council)
- **Found:** the council's own PDF "2024 CDF Community Projects under Chinsali
  Central Constituency as at 30th June 2024" — 15 projects with sector and
  ward, but **no amounts published**. All 15 are in `projects.csv`
  (status: approved).
- **Also found:** the council's article of 24 Dec 2024 on two 2023 CDF projects
  at Chinsali District Hospital (mother's shelter K311,985.80, 100% complete;
  ablution block K405,953.76, 90% complete) — both in `projects.csv`.
- Council news items also mention nine education projects under the 2025 CDF,
  eleven contracts totalling K10,626,582.51, and eleven community projects
  approved under the 2026 CDF (K27,437,910) — none of these names the
  individual projects with per-project figures, so no rows were taken.
- The council publishes approved empowerment-grant beneficiary lists (e.g.
  second batch of 2025 grants) — not transcribed (beneficiary lists, not
  community projects).

### Isoka (Isoka Town Council)
- **Found (main):** the council's own announcement "Government Approves Eight
  Community Projects for Isoka under 2024 CDF" — it names seven items
  (the motorbikes for two chiefs appear to be counted as two of the eight).
  No per-project amounts (programme total over K9,773,247). 7 rows in
  `projects.csv`.
- **Held (25 rows):** Isoka is reported mainly through news, not council
  lists:
  - ZANIS (Jun 2026): seven commissioned projects named, combined value only,
    no funding year → 7 held rows.
  - ZANIS via Muchinga Provincial Administration (Jun 2024): three 2023 CDF
    ablution-block contracts with amounts, but the two named contractors
    cannot be assigned to specific projects from the text → 3 held rows.
  - Efficacy News (Jul 2023): fifteen/sixteen 2023 CDF approvals listed with
    no amounts or wards → 15 held rows. Two of them (Milongo Health Post
    ablution; Nansala Primary School staff house) may overlap the other held
    rows or the council's 2024 list — flagged in the hold reasons.
- Isoka Town Council publishes budgets and financial statements but **no CDF
  community project list** was findable on its site.

### Kanchibiya (Kanchibiya Town Council)
- **Found:** the council-published CDFC minutes of 18 Feb 2025 contain two
  full tables:
  - "Updated Status Progress Report as at 17th February 2025" — 14 ongoing/
    completed projects with contractor, contract sum, ward and % complete.
    All 14 in `projects.csv` (100% → completed; otherwise ongoing with the
    published %). The Civic Centre row notes a later price adjustment to
    K2,122,955.00; the published contract sum (K1,699,075.00) was recorded.
    One row (Kaleka 1x3 CRB) has no legible ward in the document.
  - "Budgets for Community Projects CDF 2025 Submissions to CDFC" — 18
    projects approved in principle by the CDFC, with ward, sector and budget.
    All 18 in `projects.csv` (status: approved).
- This is the strongest source in the province: contractors and completion
  percentages are published, which no other Muchinga council does.

### Mafinga (Mafinga Town Council)
- **Found:** the council's CDF webpage lists 3 community projects by ward
  (no amounts, no year) — in `projects.csv` as approved.
- **Found:** the minutes of the Second Ordinary Council Meeting (17 Jul 2025)
  contain a handover table of CDF community projects "for 2023 and 2024" with
  location, contract amount and **year of implementation per project** — 11
  unambiguous rows plus the ambulance (2024) are in `projects.csv` as
  completed. The same minutes confirm a water bowser and tipper truck were
  received under the **2025 CDF**, with a lowbed and excavator awaited — the
  four equipment items from the council CDF page are filed from this source.
- **Held (1):** handover-table row 11 ("1x3 CRB at Mafinga", Chitete) — its
  amount K790,051.13 is identical to the Vumbo Temwani row in the same table
  and the project name is incompletely printed; possible duplication/misprint
  in the source.
- The handover table's aggregate empowerment rows (2025 loans to 85
  beneficiaries, K3,736,935; grants to 127 beneficiaries, K2,451,290) were
  not transcribed — aggregates, not projects.

### Mfuwe (Lavushimanda Town Council)
- **Found:** the council's article "Over K18 Million Awarded to 17 Contracts
  under 2025 CDF Projects" lists all 17 contracts with contractor, ward
  (mostly) and exact contract sum (total K18,247,884.43). All 17 in
  `projects.csv` (status: approved — contracts awarded). Contractor names
  are transcribed as published, including the council's spellings
  ("Blecra Investiments Limited", "Grawell Genral Dealers Limited",
  "Amorgans Suppliers and Constractors Limited").
- **Held (9):** a ZANIS report of seven 2023 CDF projects commissioned in
  Lavushimanda (costs stated only approximately) → 8 held rows (incl.
  Tubondo Primary School, whose works are not named); one ZANIS item on a
  2024 CDF classroom block at Mwila Chilembwe Primary School → 1 held row.
- Note: the task brief grouped Mfuwe under Mpika; in practice Mfuwe
  constituency's CDF is administered by **Lavushimanda Town Council**
  (Lavushimanda District), not Mpika Town Council. Mpika Town Council's own
  lists cover Mpika Central only.

### Mpika Central (Mpika Town Council)
- **Found:** the council's published letter of 6 Feb 2026, "Request for
  Authority to Approve Community Projects under the 2026 CDF" (filed on the
  site as "2026 Approved Community Projects"), listing proposed projects
  with ward and engineer's estimate. The scan is poor quality: 8 project
  names are legible (2 of the 10 numbered rows are illegible), and exact
  estimates are legible for only 3 rows (Mpika Boys ablution block
  K1,300,000; Chilonga bus shelter K280,000; metallic bus shelters
  K840,000). Rows with illegible amounts are in `projects.csv` with the
  amount blank. The letter is addressed as "Mpika Constituency" — Mpika
  Town Council administers Mpika Central, and the wards named (Musakanya,
  Chilonga, Mutamba, Chishibesonde) are Mpika Central wards.
- The council downloads page also lists a "2023 CDF Community Projects" list
  and a "2023–2024 CDF Project Progress Report from WDCs"; the direct file
  links could not be retrieved through search, so those lists were not
  transcribed — worth a manual download later.
- **Held (2):** solar backup systems at Michael Chilufya Sata Hospital and
  Mpika Urban Clinic (2024 CDF) share one combined MLGRD contract of
  K699,619.20 (Grey Falcon Zambia Limited) reported in the news — no
  per-facility figure.
- Ministerial-tour coverage (Zambian Observer, May 2025) mentions the Mpika
  Urban Clinic mortuary and maternity wing, Great North Road traffic lights
  and the modern bus station as CDF projects, without years or figures —
  noted here, no rows taken.

### Nakonde (Nakonde Town Council)
- **Found:** the council's PDF "List of 2024 Approved Projects" — 14 community
  projects with approved amounts; wards are printed only for the last six.
  All 14 in `projects.csv` (status: approved). One row is explicitly a
  reservation for the **2022 CDF** inside the 2024 list, as published.
- The same PDF contains the 2024 empowerment loan (32) and grant (~100)
  beneficiary lists — not transcribed (beneficiary lists).
- The council's March 2025 announcement of 2025 approvals (9 community
  projects, K4,582,956.78 total) does not name the projects — no rows taken.

### Shiwa Ng'andu (Shiwang'andu Town Council) — the big gap
- **No official project list was findable.** The council website publishes
  budgets but no CDF community project list, approved list, progress report
  or newsletter naming projects. A 2024 CDF construction tender notice
  (ZPPA e-procurement) confirms projects exist but names none of them.
- **Held (5):** a National Assembly constituency item (Apr 2024) names three
  classroom blocks and 3,500 desks at one combined K7,024,000 → 4 held rows;
  a ZANIS report via the Provincial Administration names a 1x3 CRB at
  Kalonga Primary School (2023 CDF, K850,000) → 1 held row. A ZANIS report
  (May 2026) says the council handed over 10 CDF projects worth over
  K7.4 million but names none of them.
- Context worth recording: in 2023 the UPND publicly accused this council/
  CDFC of failing to utilise the 2022 CDF allocation (K25.7 million) at all.
  The absence of published lists is itself the accountability story here.

## Funding-year explicitness per source (for later year-tagging)

| Source key | Names a CDF funding year? |
|---|---|
| mpika-2026-approved | **Yes — 2026** (letter subject and site filename). Whole list. |
| lavushimanda-2025-contracts | **Yes — 2025** (article title/body). Whole list. |
| kanchibiya-cdfc-minutes-feb-2025 | Progress-report table: **No** — only contract start dates (2023–2024). Submissions table: **Yes — 2025** (table heading "CDF 2025"). |
| chinsali-2024-approved | **Yes — 2024** (document title). |
| chinsali-district-hospital-2023 | **Yes — 2023** (article text). |
| nakonde-2024-approved | **Yes — 2024** (document title); one row is expressly a reservation for the 2022 CDF. |
| mafinga-cdf-page | **No** — no year anywhere on the page. |
| mafinga-council-minutes-2025 | **Yes, per project** — handover table has a "Year of Implementation" column (2023 or 2024 per row); equipment prose ties the bowser/tipper to the **2025 CDF**. |
| isoka-2024-approved | **Yes — 2024** (article title/body). |
| zanis-isoka-commissioned-2026 (held) | **No** — no funding year; text only notes CDF implementation "since 2022". |
| muc-isoka-ablution-contracts-2024 (held) | **Yes — 2023** (article text). |
| efficacy-isoka-2023-approvals (held) | **Yes — 2023** (article text). |
| lsk-mfuwe-commissioned-2023 (held) | **Yes — 2023** (article text). |
| zanis-lavushimanda-education-2026 (held) | **Yes — 2024** for the classroom block (article text). |
| parliament-shiwangandu-schools-2024 (held) | **No** — commissioned April 2024, funding year not stated. |
| muc-shiwangandu-kalonga-2025 (held) | **Yes — 2023** (article text). |
| zambianeye-mpika-solar-2026 (held) | **Yes — 2024** (article text). |

## Method notes / known limitations
- Several council PDFs are low-quality scans; figures were taken only where
  the digits were legible (see Mpika Central). Where a name was legible but
  the amount was not, the row is included with the amount blank.
- Categories were mapped from each source's own sector wording onto the
  tracker vocabulary (e.g. desks → education, ablution blocks → sanitation,
  chief-retainer motorbikes/governance items → administration, plant and
  vehicles → equipment).
- Facebook was not used (login-gated), per the brief. Shiwang'andu in
  particular appears to publish mainly through Facebook/ZANIS coverage,
  which is why it is a gap.
- Mpika Town Council's 2023 CDF community projects list and 2023–2024 WDC
  progress report exist on its downloads page but the file URLs were not
  retrievable via search — a follow-up with direct site access could add a
  full Mpika Central list.
