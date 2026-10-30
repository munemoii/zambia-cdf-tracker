# Northern Province — CDF project-list coverage

Collected 2026-10-30 following the Lusaka pilot method: only rows taken plainly
from official published lists (council/government publications, or a news
article reproducing an official list verbatim) are in `projects.csv`. Single
narrative reports, template/placeholder content, partial approvals, split
attributions and anything needing interpretation are in `held.csv` with a
reason. Nothing in `held.csv` should go live without review.

**Totals: 103 rows in projects.csv, 47 rows in held.csv, 23 sources.**

## Per constituency

### Chilubi (Chilubi Town Council) — 10 main, 0 held
- `chilubi-commissioning-2023` — council post (13–15 Nov 2023): five commissioned
  community projects, each with a contract sum (Chinikapundu 1x2 CRB K374,600;
  Kashitu staff house K296,400; Kashitu hand pump K60,000; Chinungwe 1x2 CRB
  completion K83,158; CDF Landcruiser K1,200,000). No wards published.
  **Funding year: NOT explicitly named** in the post.
- `chilubi-water-2022` — council post on the World Water Day commissioning of the
  Chief Matipa's Palace water reticulation (K216,525), stating three water
  reticulation systems were completed under CDF 2022 (Matipa Palace,
  Chiwanangala Palace, Kashitu Health Post). **Funding year: YES — 2022.**
  Post date not stated on the page (left blank in sources.csv).
- `chilubi-newsletter-2024` — council newsletter Issue 1 of 2024: Mofu 1x3 CRB
  (Mofu Ward, commissioned 5 Jan 2024) and a police vehicle.
  **Funding year: 2023 is stated explicitly for the police vehicle** ("purchased
  under the 2023 constituency development fund allocation"); the Mofu CRB is
  described only as "under CDF", year not named.

### Chimbamilonga (Nsama Town Council) — 39 main, 0 held
- `nsama-stakeholders-minutes-2024` — official minutes of the Nsama
  Stakeholders' Engagement Meeting, 16 Dec 2024, containing the Engineering
  Department's status tables:
  - Table 1, **2021 allocation: 8 projects, all Complete**, with ward, contractor
    and contract sum. Funding year: YES — 2021.
  - Table 2, **2022 allocation: rows 1–21 extracted**, with ward, contractor,
    contract sum and status (Complete / Work in progress / Substantially
    complete — the last two are mapped to `ongoing`). Funding year: YES — 2022.
    NOTE: the table continues past row 21 in the minutes; the remainder could
    not be re-fetched in this session (tool rate limit), so the 2022 set here
    is partial. The minutes also contain 2023/2024 status tables and a
    WDC-applications annexure that were not extracted for the same reason —
    re-open this PDF first in any follow-up pass.
  - Table 8, **"Proposed Prioritized Projects adopted for 2025": rows 1–10**
    (procurement of tractors/grader/TLB, Nsama guest house/theatre/maternity
    wing/mortuary completions, health equipment, Banda water scheme).
    Funding year: YES — 2025. No amounts are published in Table 8.
    Rows beyond no. 10 are cut off in the indexed copy (row 11 begins
    "Completion of…") and are not included.
  - The annexed WDC applications list for 2025 (rows ~45–57+) is applications
    only, not adoptions, and was not captured (the adopted subset is Table 8).
  - One ambiguity: in Table 1 row 2 (Kapisha Kalomo Primary School 1x2 CRB) the
    ward/contractor columns cannot be separated reliably from the PDF text
    order, so both were left blank rather than guessed.

### Kaputa (Kaputa Town Council) — 0 main, 4 held
- The council **Publications page lists exactly the right documents** —
  "LIST OF APPROVED PROJECTS 2025 VERSION 1" (26 Dec 2025), "List of Approved
  Community-Projects and justification-2025", "List of Approved Project -2025",
  "CDF Community Projects 2024" and "Community Projects with images from
  2022-2024" — but the file URLs behind those titles are not exposed in the
  page text or search index, so the lists themselves could not be retrieved in
  this pass. **This is the single biggest recoverable gap in Northern: one
  direct fetch of those PDFs would likely yield Kaputa's full approved lists.**
- The indexed "Applications for 2025 Community Projects in Kaputa District"
  PDF (`Recieved-2025-Community-Projects.pdf`) is an applications-received
  list with CDFC comments (many "Recommended", many non-approvals for
  insufficient funds); it is not an approved list and was not captured.
- Held rows are single items: Muchenja Maternity Annex and Kakomo Primary
  1x3 CRB (council PS-inspection post, no year/cost), Kalaba Mini Hospital
  solar system (**2026 CDF explicitly stated**, Mwawe Ward), and the Miyonga
  Ward piped-water approval (news report only).

### Kasama Central (Kasama Municipal Council) — 5 main, 4 held (+13 unattributed held)
- `kasama-central-2026` — council PDF "Kasama Central Constituency Proposed
  2026 Projects": 5 projects, all marked Approved, with ward and cost (truck
  park K7.9m; ablution blocks at Chikumanino, Chambeshi and Tazara markets
  K1m each; 4km solar streetlighting K4m; total K14.9m).
  **Funding year: YES — 2026.** (The PDF numbers two rows "4"; rows are
  captured as published.)
- No Kasama Central list for earlier years was found; a Lukashya-format 2024
  list exists only for Lukashya (below).
- `kasama-cdf-projects-page` — the council's "CDF Projects" webpage lists 16
  project cards with status and progress %, but the page contains placeholder
  fields ("ENTER WARD", "ENTER ACTUAL COORDINATES", "Project Image
  Placeholder") and several generic names ("Classroom Block Construction",
  "Community Hall"), and publishes no costs, contractors or funding year.
  All 16 cards are in held.csv: 4 are labelled Kasama Central on the page,
  12 cannot be attributed to either Kasama constituency.
  **Funding year: NOT stated.**
- `kasama-mortuary-moh` — Ministry of Health (19 Dec 2025): the Kasama General
  Hospital mortuary (K1,390,000, completed) was built with the **2024 CDF**
  Disaster Management component **co-financed by Kasama Central and
  Lukashya**; the split is not published, so the row is held unattributed.

### Lubansenshi (Luwingu Town Council) — 0 main, 2 held
- No approved community-project list for Luwingu district was found. The
  council publishes a 2026 CDF **grants** list (empowerment component —
  beneficiary clubs, not community projects; not captured here) and narrative
  news posts.
- Held: the modern bus terminus phase 1 (council press release; Tinna
  Investment Limited; phase-1 cost is a projection of K2.1m within an
  estimated K8m+ multi-phase project; Lubansenshi attribution rests on the
  MP/CDFC roles at the launch) and the Chifumo Primary School 1x2 CRB
  (K250,000, completed) which was funded **jointly from the 2020 and 2021
  CDF allocations** — no single funding year.

### Lukashya (Kasama Municipal Council) — 21 main, 1 held
- `kasama-lukashya-2024` — council PDF "List of Proposed, Assessed, Costed and
  Some Approved 2024 CDF Community Projects in Lukashya Constituency"
  (signed by the Ag. Director Engineering Services). 30 rows with ward,
  engineer's estimate and an Approved / Not approved status. The **21 Approved
  rows are in projects.csv** (status `approved`; budget_kwacha is the published
  engineer's estimate). The 8 "Not approved due to budget constraints" rows
  were excluded entirely. **Funding year: YES — 2024.**
- Held: the 50km Moboshi–Mukumbe road grading — the list states funding was
  approved for only 5.8km while the K12,343,520 estimate covers 50km.
- Notes for review: two different maternity wings (Ntumpa — not approved, and
  Munkonge Clinic — approved) carry the identical estimate K1,536,655.02,
  consistent with a standard design estimate; wards could be read plainly for
  only some rows (the PDF's ward column interleaves in text extraction), so
  several Lukashya rows have blank wards rather than guessed ones.
  Row 17's comment notes the Mumbi Mfumu maternity wing itself was built
  using 2022 CDF — the 2024 item is its water reticulation scheme.

### Lunte (Lunte Town Council) — 0 main, 2 held
- Lunte publishes applications, not approvals: a "List of 2023 CDF Community
  Projects Applications Received from the WDC for Consideration" and a
  10 Mar 2025 notice listing 2025 applications **NOT recommended** by the
  CDFC. No approved community-projects list was found, so nothing was taken
  from either document (the not-recommended list must never be loaded as
  projects). The council's 2026 implementation programme mixes funders
  (ZDSP etc.) and was not used.
- Held: two banana boats for Bwandela Ward handed over 13 Oct 2025
  (National Assembly Newsflash; **2025 CDF explicitly stated**, no cost) and
  the Moseni Basilio Health Post maternity annex (news report; K1,208,000
  total made up of separately priced building/solar/equipment/incinerator
  components; ward not published).

### Lupososhi (Lupososhi Town Council) — 0 main, 0 held
- **Nothing findable.** Lupososhi is a separate district/council
  (lupososhicouncil.gov.zm); its website carries CDF contact lines and an IDP
  but no published CDF project list, newsletter or project database was found
  in this pass. (The brief grouped Lupososhi under Luwingu; the council is in
  fact separate, and Luwingu's publications do not cover it.)

### Malole (Mungwi Town Council) — 0 main, 2 held
- No approved project list was found on Mungwi Town Council's site. Held:
  rehabilitation of Nsofu Primary School, Fube Ward (**2023 CDF for Malole
  explicitly stated**; completed; contractor Nchilemu General Dealers for
  phase 1 and Nikkas Enterprises for phase 2 desks — but the budget is
  published only as two K100,000 phase allocations, no single total) and the
  Chambeshi Bridge rehabilitation (2023 CDF community allocation; no cost or
  ward published).

### Mbala (Mbala Municipal Council) — 4 main, 7 held
- `mbala-newsletter-2023` — council Newsletter Issue 1 (2023):
  - "CDF Projects Handed Over to the Community": three projects handed over
    under the **2022 CDF allocation** (Musende Primary 1x2 CRB + staff house;
    Ndundundu Primary 1x3 CRB; Chila Deaf Primary 1x2 CRB), all completed.
    The three share a combined cost of K1,937,600, so per-project budgets are
    blank — the combined figure must not be split. **Funding year: YES — 2022.**
    The CDFC chair's message states 23 structures/projects were completed
    from the 2022 allocation, but the newsletter's photo-focus pages (12–15)
    carry no extractable captions, so only the three named handovers and the
    drainage below could be captured.
  - Mbulu Secondary School drainage: K673,767.19, contractor Mucart
    Investments Ltd, completed, under the **2023 CDF Disaster Management
    Component** (loaded as component `community`; the source's component
    wording is recorded here). **Funding year: YES — 2023.**
  - A CDF-purchased grader handover is reported without cost or year (held).
- Held council news posts: Mbulu Modern Market Shelter (K6.8m, ongoing,
  funded under **both 2024 and 2025 CDF**), President Avenue 2.5km CBD road
  (K8.7m, **2025 CDF**), Shacman water bowser (K2.2m, **2026 CDF**), Kawimbe
  Secondary ablution block + mechanised water reticulation (K1,058,557.10,
  **2024 CDF**, 80% complete), Kawimbe 1x3 CRB (**2022 CDF**), Kakungu Day
  Secondary 1x4 CRB, Lwandi Ward (commissioned; no year or cost).

### Mporokoso (Mporokoso Town Council) — 0 main, 4 held
- No published project list/database was found on the council site (news
  posts and CDF forms only). All four rows come from one council monitoring
  report (Provincial PS tour, 11 May 2025) and are held: Chief's Palace
  (contractor Transatlantic Ventures Limited; behind schedule — PS
  recommended termination if incomplete by 30 May 2025), Mporokoso Boarding
  Secondary 1x3 CRB (**2023 CDF**, constructed), four hostel dormitories
  renovated (**2024 CDF**), and a 1x2 cell block at Mporokoso Correctional
  Facility (**2024 CDF**). No amounts or wards are published.

### Mpulungu (Mpulungu Town Council) — 24 main, 0 held
- `mpulungu-approved-2025` — council PDF "APPROVED 2025 COMMUNITY PROJECT":
  the complete approved list, 24 projects with ward and amount (feeder roads
  K8m; 1,840 desks K3,036,000; Vyamba 1x3 CRB K1,010,000; Mengo Health Post
  K1,020,000; mortuary K970,000; etc.). All rows status `approved`.
  **Funding year: YES — 2025** (named in the document title).
  The published_date in sources.csv (2025-12-01) is the upload month from the
  file path; no exact day is published.
- A separate council news post details nine 2025 feeder roads by ward; it
  duplicates the list's single "Rehabilitation/Maintenance of Feeder Roads
  (100 km)" programme line, so it was not captured separately (splitting it
  would double-count the programme).

### Senga Hill (Senga Hill Town Council) — 0 main, 8 held
- No approved project list was found. The council's DDCC summary post
  (28 Mar 2025) names projects plainly — water reticulation at Chikwanda
  School and at Chomba and Vondoka health posts; classroom blocks and
  dormitories at Chituta, Miloso and Senka schools; the Chief Mpande Earth
  Dam — but publishes no wards, costs or per-project funding years, so all
  are held. The Mambwe Mission Hospital X-ray laboratory (council post,
  5 May 2025, nearing completion, CDF-funded) is likewise held.
  **Funding year: NOT stated for any Senga Hill source.**

## Funding-year summary (for later year-tagging)

| Source | Funding year explicitly named? |
|---|---|
| mpulungu-approved-2025 | Yes — 2025 |
| kasama-lukashya-2024 | Yes — 2024 |
| kasama-central-2026 | Yes — 2026 |
| nsama-stakeholders-minutes-2024 | Yes — per table: 2021, 2022, 2025 (adopted) |
| chilubi-water-2022 | Yes — 2022 |
| chilubi-newsletter-2024 | Partly — 2023 for the police vehicle only |
| mbala-newsletter-2023 | Yes — 2022 (handovers); 2023 (drainage, disaster component) |
| chilubi-commissioning-2023 | No |
| kasama-cdf-projects-page | No |
| All held single-item sources | Mixed — see each constituency section above |

## Biggest gaps

1. **Kaputa's approved lists exist but were not retrievable** — the council
   Publications page names approved 2025 lists and a 2024 community-projects
   document whose file URLs are not exposed to search/page text. One direct
   fetch unlocks a full constituency.
2. **Lupososhi: nothing published findable at all** — no list, newsletter or
   project post on its council site.
3. **No approved lists for Malole, Lubansenshi, Mporokoso, Senga Hill or
   Lunte** — these councils publish narrative posts, applications-received
   lists (Lunte, Kaputa) or nothing; their 33 held rows are the current
   record and none should go live unreviewed.
4. **Nsama's minutes PDF is only partly harvested** — the rest of the 2022
   table, the 2023/2024 status tables and Table 8 rows 11+ remain in the
   same document and are the cheapest follow-up win after Kaputa.
5. Kasama Central has only a 2026 list; Kasama's own CDF projects webpage is
   placeholder/template content and unusable until the council completes it.
