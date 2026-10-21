# B. Demand and existing tools — City of St. Louis

**Status: COMPLETE 2026-10-14 00:27 UTC (7:27 p.m. CDT 13 Oct).** Started 2026-10-13 23:10 UTC; paused 23:36–00:03 UTC. All four detail files are complete and their corrections are folded in (see the last section).

## Summary

**What was found**

- **CityStat** has 24 metrics on 12 pages. Of 18 with a target, 9 were missed in the latest quarter; hazard trees (37% against 100%), major-street potholes, critical signs and parks requests have never met target. Nothing has been updated since 30 June 2026.
- **The 311 file** (1.45 million requests, retrieved rows) shows 112,859 requests in the last year, 21,292 open, 9,069 open for more than a year, and closure that often records a referral rather than a fix.
- **Four problems are supported by the city's own figures, data retrieved here and resident accounts together:** tornado home repair (46 of 2,674 homes, 2%), tornado demolition and debris, vacant and overgrown property, and water-main breaks.
- **Residents also raise** 911 answering, loose dogs, dangerous driving, evictions, homelessness and the jail, none of which CityStat measures.
- **About 150 existing tools and programmes** were inventoried. Most service problems enter one request form and one status page; trackers show status without dates.
- **Elsewhere:** 25 deployments in other cities are recorded; three have an independent evaluation showing an effect.

**What could not be established**

- Any city-published 911 answer time, resident satisfaction survey, or CityStat figure after 30 June 2026.
- Why 49% of tree requests are cancelled; whether the promised per-lot mowing log exists; whether the police dispatch replacement is live.
- Contract terms for any major system; only payment totals were found.
- Resident counts for trees, sidewalks and missed refuse. Graffiti, urban heat and residential potholes were not found as current resident complaints.
- Sources not reached: KSDK, Fox 2, most Post-Dispatch pages, X, Facebook, Nextdoor, Reddit comments, hearing video.

Facts only. No solutions or project ideas appear in this file.

Labels: **observed** = checked directly by this thread; **reported** = a source says so; **inferred** = this thread's conclusion.

Supporting detail files (written by parallel research agents):

- `research/parts/B-city-stated.md` — mayor's priorities, budget, audits, Board of Aldermen
- `research/parts/B-resident-voice.md` — news, forums, neighborhood groups, surveys
- `research/parts/B-existing-tools.md` and `research/parts/B-existing-tools.d/` — inventory of existing city/partner tools
- `research/parts/B-other-cities.md` — what other cities deployed
- `research/parts/B-csb-request-analysis.md` — 311/CSB file analysis output; scripts in `research/parts/B-csb-scripts/`
- `data/raw/citystat/tableau-extract.md` — every CityStat chart's underlying table
- `research/demand-and-existing-tools-facts.csv` — one row per figure in this report (881 rows): figure, unit, date it refers to, label and URL

---

## Part 1A. CityStat, every department and metric

Source: <https://www.stlouis-mo.gov/citystat/> and its 15 sub-pages, HTML retrieved 2026-10-13 23:10–23:12 UTC and saved under `data/raw/citystat/`.

**Observed, structural facts**

- CityStat covers 7 departments/divisions groups and 12 leaf pages: Health; Human Services; Parks (Forestry, Parks); Personnel; Public Safety (Building, CSB); Street (Refuse, Street, Traffic & Lighting, Towing); Water.
- Every leaf page carries the same note: "This data was last updated June 30th, 2026" and says validated Q2 data would be available August 1st, 2026. As of 13 October 2026 the pages still show the preliminary Q2 text, so **the published figures are 3.5 months old** and no Q3 2026 data is published. (observed)
- The Personnel page still says Q2 data "is currently being validated and will be updated in August 2026". (observed)
- Charts are embedded Tableau views (22 of them) with per-load tokens; there is no download link, CSV or table on any CityStat page. Figures below marked *(text)* come from the page narrative; figures marked *(chart)* were read from the rendered Tableau view. (observed)
- CityStat has **no page for**: police, fire/EMS, 911 dispatch, the jail, the Land Reutilization Authority, demolition, code enforcement/building inspections other than permits, homeless services, the tornado recovery office, or the Community Development Administration. (observed: absent from the CityStat navigation)

**How the figures were read.** Each chart's underlying summary table was read from the embedded Tableau view in a browser (Tableau Embedding API `getSummaryDataAsync`), 2026-10-13 23:14–23:46 UTC. Full extracted tables: `data/raw/citystat/tableau-extract.md`. All rows below are **observed** unless marked. "Latest" is Q2 2026 (April–June 2026, preliminary) unless stated. Counts in brackets are the number of requests/items behind the percentage.

| # | Dept / division | Metric | City's target | Latest value | Trend (from the chart data) | Figure dated | Page |
|---|---|---|---|---|---|---|---|
| 1 | Health | Routine food & beverage inspections done on schedule | 85% | **91.1%** (1,032) — met | 2024: 60–70%; 2025: 54–62%; Q1 2026 89.1%. Missed every quarter of 2024–25, met both quarters of 2026 | 30 Jun 2026 | [health](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/health/index.cfm) |
| 2 | Human Services | HELP-STL (tenant right to counsel) cases opened / closed / open at quarter end | none stated | Q1 2026: 55 opened, 86 closed, 71 open. Cumulative since Aug 2024: 472 opened, 400 closed | Intake fell from 93 (Q1 2025) to 55 (Q1 2026); open caseload peaked at 137 (Q3 2025) | **31 Mar 2026** (one quarter older than the rest) | [human-services](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/human-services/index.cfm) |
| 3 | Human Services | HELP-STL financial impact for clients | none stated | Q1 2026: $238,235; cumulative $811,899 | Rising every quarter from $8,980 (Q3 2024) | 31 Mar 2026 | same |
| 4 | Parks / Forestry | Hazard-tree removals completed within 30 days | 100% ("all validated hazard tree requests") | **37%** (145) — missed | 2024 average 15.4%; 2025 average 18.6%; Q1 2026 40%. Never above 40% in 10 quarters | 30 Jun 2026 | [forestry](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/parks/forestry-division.cfm) |
| 5 | Parks / Forestry | Hazard-tree removal backlog (open work orders at quarter end) | none stated | **591** | 31 (Q4 2019) → 482 (Q4 2022) → 806 (Q4 2024) → peak **990** (Q3 2025, post-tornado) → 822 → 731 → 591. Three straight quarterly falls; still 19× the 2019 level | 30 Jun 2026 | same |
| 6 | Parks / Forestry | Vacant lots mowed in first rotation (6 Apr–26 May 2026) | No % stated; aim is to work the rotation "as many times as possible" April–October | **7,099 of 12,171 lots (58.3%)** in the chart; page text says "approximately 7,000" of "approximately 14,000" | Single rotation, no trend. By ward: 0% (Wards 4, 6) to 67% (Ward 12). The four wards with 2,000+ lots (11–14) were 59–67% | 26 May 2026 | same |
| 7 | Parks / Forestry | Vacant-building parcels trimmed (contract crews) | 4 rotations per cutting season | First rotation **not complete** at 30 Jun: 1,048 of 4,638 parcels (22.6%) in the 8 wards shown — missed pace | No trend published. Ward 14: 15 of 515 (3%); Ward 11: 41 of 592 (7%) | 30 Jun 2026 | same |
| 8 | Parks / Parks Division | Parks service requests completed on time (5–30 day goals by type) | 80% | **67.5%** (378) — missed | 21.1% (Q1 2025) → 51.0% (Q4 2025) → 44.0% (Q1 2026) → 67.5%. Never met in 10 quarters | 30 Jun 2026 | [parks](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/parks/parks-division.cfm) |
| 9 | Parks / Parks Division | On-time rate by problem type (period not labelled; 534 requests ≈ 2026 year to date, **inferred**) | 80% overall | Lowest: dead limbs in park 25% (16); graffiti on park equipment 37.5% (24); athletic fields 45% (44); playground equipment 48% (50); trash in park 50% (88); high grass 51% (35). Highest: fountains 94% (32), athletic lights 94% (17) | n/a | 30 Jun 2026 | same |
| 10 | Personnel | Job offers accepted within 30 days of application | 90% | Latest full quarter **Q4 2025: 92.1%** (160 candidates) — met. Q1 2026 shows 100% on only 18 candidates; **no Q2 2026 figure** | 40.9% (Q1 2025) → 74.8% → 75.8% → 92.1% | 31 Mar 2026 at best; page says Q2 "will be updated in August 2026" and was not | [personnel](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/personnel/index.cfm) |
| 11 | Public Safety / Building | Building permits issued within 30 days | 80% | **66.6%** — missed | Met once in 10 quarters (Q3 2025, 81.2%). Since then 73.0% → 70.5% → 66.6%, falling for three quarters despite online permitting from Feb 2026. City cites a 25% surge in applications in March–April | 30 Jun 2026 | [building](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/public-safety/building-division.cfm) |
| 12 | Public Safety / CSB | Service requests routed to the right department within 2.5 days | 95% | **99.99%** (10,853) — met | Missed Q2 2025 (94.6%), Q3 2025 (93.5%), Q1 2026 (93.9%); otherwise met | 30 Jun 2026 | [csb](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/public-safety/csb.cfm) |
| 13 | Public Safety / CSB | Average days for departments to complete a request, by ward | none stated | 1 Jan 2024–30 Jun 2026: fastest Ward 1 **17.2 days**, slowest Ward 10 **35.1 days**; 286,148 requests, 82.5% closed. Page text for 2026 only: 6.5 days (Ward 4) to 13.7 days (Ward 9) (text, not re-derived) | City says 2026 is much faster than the 2024–26 average | 30 Jun 2026 | same |
| 14 | Public Safety / CSB | Snow/ice request completion time ("previous highlight") | none stated | Jan 2026 storm, peak week: 1,334 requests, 3.1 days average | Jan 2025 storm, peak week: 1,709 requests, 17.4 days average | Feb 2026 | same |
| 15 | Street / Refuse | Quarterly alley and roll-cart route coverage | 95% | **94.2%** (1,260 routes) — missed narrowly | 75.8% (Q3 2025, first data) → 86.6% → 97.4% (met) → 94.2%. No data before Sept 2025 | 30 Jun 2026 | [refuse](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/refuse.cfm) |
| 16 | Street / Refuse | Monthly completion of scheduled refuse service | 95% | June 2026 **97.5%** — met; April 92.4%, May 92.7% — missed | Low of 69.5% (Oct 2025); met Dec 2025–Mar 2026 | 30 Jun 2026 | same |
| 17 | Street / Refuse | Share of collected recycling tonnage actually recycled | none stated | May 2026 **75.9%** | 33–45% under alley collection (2024–early 2025) → 97–99% after move to drop-off sites (Sep 2025–Jan 2026) → fell to ~76% from Feb 2026 and stayed there. City says the cause is under investigation | 31 May 2026 (no June row) | same |
| 18 | Street / Street Division | Pothole requests repaired within goal (major street 3 days; residential 8; alley 17) | 80% each | Major **44.5%** (443) — missed; residential **90.6%** (916) — met; alley **98.2%** (113) — met | Q4 2024 was 1.3% / 1.7% / 2.9%. Major-street has never met goal in 10 quarters (best 44.5%) | 30 Jun 2026 | [streets](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/streets.cfm) |
| 19 | Street / Street Division | Debris cleanup requests completed within goal (alley/street 3 days; vacant building and vacant lot 14) | 80% each | Alley/street **78.6%** (546) — missed narrowly; vacant building **95.5%** (67); vacant lot **97.4%** (113) | Q1 2025 was 11.0% / 32.6% / 22.9%. Alley/street has never met goal in 10 quarters | 30 Jun 2026 | same |
| 20 | Street / Traffic & Lighting | "Whole block lights out" requests completed within 24 hours | 80% | **80.2%** (358) — met for the first time in 10 quarters | Low 52.8% (Q1 2025); rising five quarters running | 30 Jun 2026 | [traffic](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/traffic.cfm) |
| 21 | Street / Traffic & Lighting | Critical sign (Stop, Yield, One-Way, Do Not Enter) repairs within 48 hours | 75% | **58.9%** (112), average 5.4 days open — missed | 14.5% (Q3 2024) → 69.5% (Q1 2026, best) → 58.9%. Never met in 10 quarters. City cites staffing | 30 Jun 2026 | same |
| 22 | Street / Towing | Completed tows per quarter by type (abandoned, booted, other) | none stated | **Chart does not render for the public**: it shows "Tableau detected that your OAuth refresh token is expired" and a Snowflake sign-in prompt (three attempts, 23:40–23:46 UTC) | Text only: abandoned-vehicle tows "nearly doubled" in Q4 2025 and Q1 2026; booted-vehicle towing restarted March 2026 | n/a | [towing](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/towing.cfm) |
| 23 | Street / Towing | Resident tow requests received, open vs closed | none stated | Q2 2026: 1,075 closed, **562 open**; Q1 2026: 1,776 closed, 105 open | 1,231–1,431 a quarter in 2024; 1,533–2,224 in 2025. The page states "Closed" does not mean the vehicle was towed and that time-to-tow is not yet measurable | 30 Jun 2026 | same |
| 24 | Water | Emergency water-main repairs back in service within 8 hours | 80% | **64.2%** (134) — missed | 65.2% (Q4 2025, 23 incidents) → 61.0% (Q1 2026, 236) → 64.2%. No data before Q4 2025; never met | 30 Jun 2026 | [water](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/utilities/water-division.cfm) |

**Scorecard against the city's own targets, latest quarter (inferred from the table).** Counting each pothole and debris category separately, 18 measures carry a target. 9 were met (food inspections; hiring time, on its latest full quarter; CSB routing; refuse service in June; residential potholes; alley potholes; vacant-building debris; vacant-lot debris; whole-block lights) and 9 were missed: hazard-tree removal (37% vs 100%), vacant-building mowing pace, parks requests (67.5% vs 80%), building permits (66.6% vs 80%), quarterly refuse coverage (94.2% vs 95%), major-street potholes (44.5% vs 80%), alley/street debris (78.6% vs 80%), critical signs (58.9% vs 75%), water-main restoration (64.2% vs 80%). Four have never been met in any published quarter: hazard trees, parks requests, major-street potholes, critical signs (and water mains, with only three quarters of data).

**Where CityStat itself falls short (observed)**

- **Stale.** Latest data 30 June 2026; today is 13 October. The promised 1 August validation note is still on every page. No Q3 2026 figures.
- **One chart is broken** for anonymous visitors (towing, row 22).
- **No downloads.** No CSV, no table view, toolbar hidden. The data-audit thread separately observed that anonymous `.csv` export redirects to a Tableau sign-in (`research/data-audit-parts/city-services-docs.md`).
- **"Closed" is not "done."** The towing page says so explicitly for tow requests. The CSB routing measure (row 12) times the hand-off to a department, not the fix.
- **Text and chart disagree in places.** HELP-STL text says the $811,900 covers "August 2025 through March 2026"; the chart's quarters from Q3 2024 sum to $811,899, so it covers August 2024 onward. Vacant-lot text says ~14,000 lots on rotation; the chart totals 12,171. CSB text says the ward averages run "January 2024 to March 2026" in one sentence and "1/1/2024 to 6/30/2026" in another.
- **Request counts differ between views.** The routing chart counts 10,853 requests in Q2 2026; the open-data file has about 31,000 requests initiated in the same quarter (`research/parts/B-csb-request-analysis.md`). The routing metric therefore covers a subset; the page does not say which. (inferred)
- **Coverage gaps.** No CityStat page for police, fire/EMS, 911, the jail, LRA, demolition, code enforcement, lead inspection, homeless services, tornado recovery or CDA.

## Part 1A-bis. What the raw 311/CSB request file shows (observed, this thread's own calculation)

Source: the city's open-data CSB archive (<https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5>), file `csb.zip` downloaded by the data-audit thread 2026-10-13 23:16 UTC; yearly CSVs inside are stamped 2026-10-13 06:01–06:04. 1,502,836 rows, 1,454,222 distinct request IDs, initiated 2008-09-02 to 2026-10-13 00:33. Duplicated request IDs were dropped. Scripts and full output: `research/parts/B-csb-scripts/`, `research/parts/B-csb-request-analysis.md`.

Caveats: "closed" is the city's status field and does not prove the work was done (see above). "On time" below means closed no later than one day after the request's own `PRJCOMPLETEDATE`; that is this thread's calculation, not a city metric.

**Volume**

- 2024: 105,572 requests. 2025: 124,077 (+17.5%). 2026 through 12 Oct: 92,455 (same period 2025: 103,673; 2024: 88,207).
- Last 12 months (13 Oct 2025–12 Oct 2026): **112,859** requests. 79% closed, 10% cancelled, **10.8% (12,220) still open**.
- Channel, 2026: web 44%, phone 28%, neighborhood stabilization officers 13%, indeterminate 12%, X/Twitter 1%, email 1%, chat 0.3%.

**Largest request types, last 12 months**

| Request type | Requests | Median days to close | 90th pct days | Still open | Cancelled | Closed on time |
|---|---|---|---|---|---|---|
| Vehicle towing (derelict/abandoned vehicle) | 8,376 | 15.0 | 68 | 533 | 1,161 | 28% |
| Refuse not collected | 6,239 | 1.7 | 4 | 27 | 490 | 87% |
| Container damaged | 4,951 | 7.9 | 45 | 160 | 315 | 63% |
| Inspect city tree | 4,091 | 4.9 | 123 | 972 | **2,561 (63%)** | 65% |
| Weeds – vacant building | 3,174 | 2.2 | 51 | 497 | 427 | 87% |
| Potholes – residential | 3,083 | 6.9 | 28 | 38 | 234 | 56% |
| Public nuisance report | 2,728 | 0.0 | 0 | 8 | 13 | 98% |
| Weeds – occupied property | 2,681 | 13.1 | 66 | **1,171** | 369 | 61% |
| Stray dog at large | 2,676 | 1.2 | 9 | 33 | 267 | 96% |
| Illegal use / open storage | 2,611 | 4.7 | 42 | 237 | 52 | 77% |
| Debris – alley/street | 2,436 | 1.0 | 9 | 7 | 211 | 77% |
| Property maintenance code – exterior | 2,327 | 5.1 | 46 | 267 | 49 | 76% |
| Cave-ins (street, alley, sidewalk) | 2,252 | 3.3 | 90 | **1,020** | 185 | 54% |
| Single street light out | 2,154 | 11.8 | 143 | 190 | 220 | 38% |
| Vacant building unsecured | 2,024 | 3.7 | 27 | 172 | 27 | 84% |
| Potholes – major street | 1,781 | 7.2 | 27 | 23 | 109 | 29% |
| Tree planting request | 1,070 | 32.2 | 148 | 228 | 178 | 31% |
| Sidewalk repair (filed under "Disability Issues") | 1,009 | 88.4 | 286 | **625** | 215 | 27% |
| Graffiti – private property | 976 | 31.0 | 64 | 68 | 24 | 44% |
| Graffiti – public property | 736 | 19.9 | 49 | 40 | 18 | 32% |

**Open backlog today** (requests initiated 2023 or later, status neither closed nor cancelled): **21,292**. Age: 9,069 over a year; 2,729 six to twelve months; 3,441 three to six months; 3,223 one to three months; 2,830 under 30 days.

- By type: sidewalk repair 2,612; inspect city tree 2,398; cave-ins 1,260; weeds on occupied property 1,177; **lead-paint inspection 655** (of 838 filed since 2023, 139 closed); bad right-of-way condition 646; vehicle towing 533; sewer lateral defect 531; weeds at vacant building 499; rats (exterior) 406; tree on LRA property 402; **weather sirens not heard 380**; **tornado debris removal 368** (of 458 filed; median open age 300 days); LRA demolition submission 281 (of 397).
- By department: Forestry 6,172; Street Department 5,901; Building Division 1,534; Water 1,214; LRA 1,025; Vector Control 898; lead inspection 656.
- By ward: Ward 12 2,198; Ward 13 2,117; Ward 10 2,038; lowest Ward 9 931.

**Other patterns**

- **Tree requests are mostly cancelled, not closed.** Trees group, last 12 months: 8,967 requests, 4,433 cancelled (49%), 2,642 closed, 1,890 open. "Inspect city tree": 2,561 of 4,091 cancelled, 2,501 of those with no public resolution text. "Stump removal": 516 of 591 cancelled. Why they are cancelled is not stated in the data (possibly converted to work orders in Forestry's own system — **inferred, unverified**).
- **Towing closures rarely say a tow happened.** Of 7,843 tow requests closed or cancelled: "vehicle gone upon inspection" 3,006; "vehicle tagged for tow" 1,598; blank 1,130; "no problem found" 694; "work completed" 501.
- **Repeat requests.** 23.7% of requests in the last 12 months share an address and problem code with another request in the same period. Highest: public nuisance 52%, illegal dumping report 49%, leash law 46%, refuse not collected 40%, water coming up 35%, vacant building unsecured 34%, major-street potholes 33%, vehicle towing 32%.
- **Blank outcomes.** 14.6% of closed or cancelled requests carry no public resolution text.
- **Vacancy and dumping requests concentrate in five wards.** Weeds/debris/unsecured/collapse/dumping types, last 12 months: 12,253 requests; Wards 13, 12, 11, 14 and 10 account for 63%.
- **Growing types** (Jan 1–Oct 12, 2024 → 2025 → 2026): cave-ins 1,326 → 1,958 → 1,878; weeds at vacant buildings 2,460 → 2,013 → 3,032; weeds on vacant lots 945 → 1,085 → 1,500; bad right-of-way condition 565 → 803 → 923 (full-year 2024, 2025; 2026 to date); water coming up 621 → 746 → 932; interior property-maintenance code 690 → 829 → 1,028; city tree down 385 → 965 → 948. **Shrinking:** residential potholes 5,131 → 2,502 → 2,654; private-property graffiti 1,182 → 760 → 731.
- **Graffiti** is routed to Operation Brightside: 1,853 requests in 12 months, median 27 days to close, 40% on time; 36 closed as "unable to remove, too high, no access or too dangerous".

---

## Part 1B. Other statements by the city of its own performance and priorities

Full detail, page references and retrieval log: `research/parts/B-city-stated.md` (primary pages and PDFs read 2026-10-13 23:13–23:40 UTC; PDFs in `data/raw/city-docs/`). Everything in this section is **observed** in the cited city document unless marked.

### Mayor's stated priorities

- **Strategic Priorities, 7 July 2026** — five priorities, 25 initiatives. Service-delivery items in the city's wording: Streets ("paving and sidewalk pilot program"), Towing ("Eliminate backlog and develop a tow lot expansion plan"), Water ("Complete water infrastructure plan and update rates"), Vacant lots ("Optimize the mowing and trimming operations model"), CEMA (update the 2003 plan and the agency's structure), Tornado Recovery ("Rapidly scale demolitions and repairs"), Vacant Properties (blight plan "led by the land bank"), Homelessness, Ease of Business ("Simplify permitting and licensing"), Customer-First Culture ("improve response times, resolutions, and accessibility"), Data-Driven Performance ("Define operational KPIs and targets for all departments and incorporate them in CityStat"), Hiring, Procurement, IT ("Create a roadmap to leverage modern technologies"). Tracked in an internal system; no public tracker is linked. <https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-strategic-priorities.cfm>
- **State of the City, 17 April 2026** — the mayor's own admissions: the tornado response was one "our City, simply put, was not prepared for"; "the sirens didn't go off on May 16"; demolition and home repair "slower than anyone wants"; on potholes, "not yet the pothole transformation I promised" because crews were moved to debris; overflowing trash containers "a problem for years"; "The City and our Water Division are in crisis mode"; "an overworked, underpaid workforce"; "antiquated technology". <https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/2026-sotc-address.cfm>

### Figures the city has published about its own shortfalls

| Area | City's own figure | Date | Source |
|---|---|---|---|
| Tornado scale | "almost $2 billion in damage", "almost 50,000 residents, more than 23,000 homes", five deaths | 17 Apr 2026 | State of the City (URL above) |
| Tornado housing | 2,900+ owner-occupied homes and 2,200+ rental units damaged; **184 homes** stabilized or repaired by the city; 69 buildings demolished (10 by the city); 140,000+ of an estimated 900,000 tons of debris removed | 22 Dec 2025 (no later report of this form found) | [Recovery Office progress report](https://www.stlouis-mo.gov/government/departments/mayor/recovery-office/news/update-december-2025.cfm) |
| Tornado demolition | "as many as 1,600 potential demolitions are required"; combined funding supports "more than 470"; 36 under way or done by 11 May 2026; 80%+ were vacant or condemned before the tornado | 11–14 May 2026 | [demolition release](https://www.stlouis-mo.gov/government/departments/mayor/news/tornado-demolition-work.cfm), [FEMA/SEMA release](https://www.stlouis-mo.gov/government/departments/mayor/news/city-state-begin-fema-sema-demolition.cfm) |
| Tornado private-property assistance | 3,617 completed applications, 653 started and not finished | 7 Mar 2026 | [release](https://www.stlouis-mo.gov/government/departments/mayor/news/private-property-assistance-transitions-to-review-prioritization.cfm) |
| Workforce | Vacancy: utility workers 42%, **tree trimmers 50%**, heavy equipment operators 20%; ~600 employees more than 5% below market minimum; application-to-start averages 54 days (goal 45) | 4 Nov 2025; 13 Oct 2026 | [pay study release](https://www.stlouis-mo.gov/government/departments/mayor/news/personnel-cc-study-released.cfm), [civil-service release](https://www.stlouis-mo.gov/government/departments/mayor/news/legislation-to-modernize-stl-civil-service-system.cfm) |
| Police / EMS staffing | "around 300 vacancies" of ~1,100 authorized officers; EMS overtime driven by "persistent vacancies among EMT and paramedic positions" | 26 Jun 2026 | FY2027 budget book pp. S-5, S-6 |
| Water finances | 16,000+ accounts past due, $14M+ owed; shut-offs resumed Sept 2025 after a five-year moratorium; 4,164 delinquent accounts ($4.34M) in tornado neighborhoods, disconnections there resume 30 Sep 2026 | 18 Dec 2025; 25 Aug 2026 | [Dec release](https://www.stlouis-mo.gov/government/departments/mayor/news/water-utility-assistance-program-expands.cfm), [Aug release](https://www.stlouis-mo.gov/government/departments/mayor/news/water-moratorium-lifted.cfm) |
| Refuse | Service costs $28M a year against $16.5M fee revenue; 4,252 of 8,918 tons of recycling rejected in FY2025; "+$200,000 allocated to manage ongoing illegal tire dumping" | 15 Aug 2025; FY27 budget | [alley recycling release](https://www.stlouis-mo.gov/government/departments/mayor/news/alley-recycling-ended.cfm); budget p. S-16 |
| Vacant lots | $2M "to address a backlog of vacant buildings and lots where excessive undergrowth has exceeded current mowing capacity". Budget book counts vacant-lot grass cuts falling from 26,448 (FY25 actual) to 7,000 (FY26 estimate) | 26 Jun 2026 | FY27 budget pp. S-8, 67 |
| Trees | ~5,450 ash trees still to remove; $2.5M of Rams money for hazardous trees, stumps and sidewalks in North St. Louis | Jun–Jul 2026 | budget p. S-8; [Rams signing](https://www.stlouis-mo.gov/government/departments/mayor/news/rams-bill-signed.cfm) |
| Streets | $500,000 one-time "to create a comprehensive inventory of all traffic signage and roadway striping" (so no complete inventory exists — **inferred**); 70,000+ street lights, 650+ signalized intersections | 26 Jun 2026 | budget p. S-15 |
| Towing | Vehicles towed: 14,174 (FY25), 6,990 (FY26 estimate), goal 14,500 | 26 Jun 2026 | budget p. 134 |
| 911 | 668,304 calls received by the 911 center in 2025; 210,727 police calls dispatched; new consolidated 911 facility "expected to be completed within the next year" | 26 Jun 2026 | budget pp. 190, S-7 |
| Homelessness | Code Blue after-action: "the system needs better infrastructure for data keeping and tracking of shelter residents"; federal homelessness grants down $2.8M | 30 Jul 2026 | [after-action release](https://www.stlouis-mo.gov/government/departments/mayor/news/code-blue-after-action-2025-6.cfm); budget p. S-18 |
| Capital | $460M+ inventoried capital need against a $50.4M FY27 capital budget | 26 Jun 2026 | budget pp. C-4, C-6 |
| Budget | Balanced for FY27; projected General Fund gaps of $7.6M–$17.4M a year FY28–FY32; "a persistent structural imbalance remains" | 26 Jun 2026 | budget pp. S-24, S-25 |
| ARPA | $35.6M of $498M still to process before the 31 Dec 2026 clawback deadline | 6 Oct 2026 | [ARPA release](https://www.stlouis-mo.gov/government/departments/mayor/news/arpa-performance-deadline-final-invoices.cfm) |

### Audits

City Comptroller, Internal Audit Section (<https://www.stlouis-mo.gov/government/departments/comptroller/services/online-audit-database.cfm>). Most were read by OCR from scanned PDFs.

- **Towing (26 Mar 2025):** "Four audits over the past five years have repeated the same findings. As of this date, none of the findings have been resolved." Tow tickets missing or in error; vehicle inventory records not maintained.
- **Emergency management (14 Mar 2024 and 28 Apr 2026):** the 2024 review, 14 months before the tornado, recorded "Inadequate Outdoor Warning Sirens" (60 sirens installed 1999). The 2026 follow-up lists sirens as "Not Tested" and says CEMA "lacks sufficient employees"; the commissioner's reply says CEMA needs at least 11 staff.
- **50/50 Sidewalk Program (17 Jul 2026):** all four findings from 2022 "have not been resolved", including "a Significant Decline in Program Participation"; management "was not able to provide documentation".
- **Refuse fees (27 Mar 2026):** all three 2024 findings unresolved.
- **Citizens' Service Bureau "Response Time & Operation Review" (26 Aug 2024):** "no findings", and it contains no response-time data.
- **Pattern (inferred by the research agent):** audits with findings mostly repeat earlier unresolved findings; audits with service-sounding titles test fiscal controls only.

**Federal Single Audit (observed by the research agent in rows retrieved from the Federal Audit Clearinghouse bulk files, <https://www.fac.gov/data/download/current/>, 2026-10-14 00:08–00:11 UTC; city rows cover fiscal years ended 30 Jun 2016 to 30 Jun 2022; extract in `data/raw/city-docs/federal/`).** The latest Single Audit on file for the City of St. Louis is for the year ended 30 June 2022 (KPMG; accepted 24 May 2023; $115,992,772 of federal spending). It discloses a material weakness and material noncompliance, and the city is not a low-risk auditee. Every year on file from FY2016 shows a material weakness. Six FY2022 findings on federal awards include late payment of homeless-services subrecipients (a repeat finding; cause given: "employee turnover"), no risk assessment or audit review for three of nine ARPA subrecipients sampled, and block-grant cash reports not reconciled to the ledger (cause given: "staffing shortages and turnover"). **No Single Audit for fiscal years 2023, 2024 or 2025 was found in the file** (caveat: rows were filtered on the string "LOUIS"). The lead thread re-read the saved extract (6,359 rows) at 00:23 UTC: the Missouri city's rows run FY2016–FY2022 with the flags stated; the 2023 and 2024 rows named "CITY OF ST. LOUIS" are St. Louis, Michigan. No city document explaining the gap was found.

Missouri State Auditor: no 2023–2026 report on Refuse, Streets, Personnel, Building, Water, CDA, LRA or Corrections was found. Board of Aldermen Resolution 59 (introduced 2 Jul 2026) asks the State Auditor to begin a performance audit of the city following a citizen petition. <https://www.stlouis-mo.gov/government/city-laws/resolutions/resolution.cfm?RSDetail=true&RSId=18009>

### Budget-book performance measures that disagree with CityStat (inferred from comparing the two)

- Water: budget book reports "% of times water restored within **24 h** of a main break" at 85% (FY25) with a 99% goal; CityStat measures restoration within **8 h** at 64% against 80%. Different yardsticks for the same service.
- Personnel: budget book says a "30-day hiring goal"; the 13 Oct 2026 release says application-to-start averages 54 days against a 45-day goal; CityStat reports 92% of offers accepted within 30 days.
- Several budget-book rows repeat identical numbers under different programmes (e.g. 7,226 / 10,077 / 10,000 appears under both Streets and Traffic), which the research agent reads as copy errors.

### Board of Aldermen

Detail and every bill URL: `research/parts/B-city-stated.md` section 4. Sources: board-bill and resolution indexes on stlouis-mo.gov, bill PDFs, and the Board's meeting portal (<https://stlouismo.portal.civicclerk.com/>), retrieved 2026-10-13 23:23 to 2026-10-14 00:06 UTC by the research agent. The 2026-27 session lists 91 board bills and 152 resolutions; 2025-26 listed 175 and 297 (observed). Recitals in a bill are the sponsor's statements; status is given for each.

**The one hearing record with current numbers.** Budget & Public Employees Committee, 30 Sep 2026: Mayor's Office deck on the Rams settlement, dated 29 Sep 2026, with Recovery Office tables "Last Updated on September 28, 2026" (packet PDF, 57 pp.: <https://stlouismo.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=3850,plainText=false)>). Observed by the research agent and checked against the page images. "Complete" change is since March 2026.

| Tornado recovery item | Total need | Complete | % as printed | Not complete |
|---|---|---|---|---|
| Home repairs | 2,674 | 46 (+19) | 2% | 2,628 |
| — Phase 2 of home repair | 2,438 | 0 | 0% | 2,438 |
| Home stabilization | 609 | 525 | 86% | 84 |
| Demolitions, all phases | 1,400–1,600 | 395 (+344) | 25–28% | 1,005–1,205 |
| — Phase 2 "Priority" and Phase 3 | 660–860 | 0 | 0% | 660–860 |
| Debris projects | 443 | 256 (+119) | 58% | 187 |
| Private-property trees | 400 | 192 (+132) | 48% | 208 |
| Emergency trees and limbs | 5,583 | 5,511 | 99% | 72 |
| City hazardous trees | 570 | 512 | 90% | 58 |
| City stumps | 2,768 | 148 | 5% | 2,620 |
| Tornado-damaged sidewalks | 176 | 61 | 35% | 115 |

Same deck (observed): recovery funding allocated $401M, of which City $253M with $164M contracted and $114M spent; $63M of housing money "Unallocated"; disaster case management 1,679 cases, 778 closed, "Wait list: 179"; the city's behavioral-health contractor "cancelled their contract in June". For the non-tornado Rams money: public infrastructure ($30M) and Downtown ($55M) "Funding plan is being finalized"; vacancy ($10M) "Mayor's Office is defining staff and teams" and "We will have metrics to present at the next meeting". The infrastructure page lists "Finish backlog of 50/50 sidewalk program", "Purchase asset management software" and "Update tree inventory map and complete backlog of hazardous tree removal and stump removal" as intended uses.

**Bills and resolutions that state a problem (2026-27 session; all observed in the bill text):**

| Item and status | What the text states | URL |
|---|---|---|
| BB 25 Water Rate (Ordinance 72155) | Increases "absolutely necessary"; schedule 18%, 18%, 6%, 6%, 6%, 5%, 5%, then CPI; a cost-of-service study to be procured by 30 Jun 2027 | [bill](https://www.stlouis-mo.gov/government/city-laws/board-bills/boardbill.cfm?bbDetail=true&BBId=16864) |
| BB 22 Rams Settlement (Ordinance 72165) | Appropriates $230,000,000 | [bill](https://www.stlouis-mo.gov/government/city-laws/board-bills/boardbill.cfm?bbDetail=true&BBId=16861) |
| BB 75 Traffic Calming (delivered to mayor) | "90 pedestrian and bicyclist fatalities" 2017–2021; "non-white areas are 3.9 times more likely" to see fatal and severe pedestrian crashes; ward-by-ward discretion "has resulted in disparate outcomes citywide" | [bill](https://www.stlouis-mo.gov/government/city-laws/board-bills/boardbill.cfm?bbDetail=true&BBId=17913) |
| BB 87 Equitable Ward Capital (introduced 2 Oct 2026) | Would allocate ward capital by need rather than equally | [bill](https://www.stlouis-mo.gov/government/city-laws/board-bills/boardbill.cfm?bbDetail=true&BBId=17925) |
| BB 90 Municipal Receivership (introduced 9 Oct 2026) | "approximately 24,000 vacant parcels … roughly 9,000 vacant buildings"; 84% north of Delmar (sponsor cites the STL Vacancy Collaborative: reported) | [bill](https://www.stlouis-mo.gov/government/city-laws/board-bills/boardbill.cfm?bbDetail=true&BBId=17928) |
| BB 91 Code Blue (introduced 9 Oct 2026) | Unsheltered count "more than 500" (2025) to "more than 1,700" (2026); tornado left "approximately 5,000 households … homeless or housing insecure" (sponsor's figures, not verified against the Continuum of Care count; the 1,700 here is described as unsheltered, whereas STLPR reports "nearly 1,800" as the total count — unresolved) | [bill](https://www.stlouis-mo.gov/government/city-laws/board-bills/boardbill.cfm?bbDetail=true&BBId=17929) |
| BB 30 Sunshine Portal (in committee) | An earlier ordinance "left out the requirement to post to the Sunshine Portal" | [bill](https://www.stlouis-mo.gov/government/city-laws/board-bills/boardbill.cfm?bbDetail=true&BBId=16869) |
| Resolution 126, grass cutting (introduced 18 Sep 2026; committee hearing 1 Oct 2026) | Weed crew is seasonal, 1 May–30 Sep; lots cut "every 4-6 weeks", vacant property "every 6-8 weeks"; residents "are being told by Citizen Service Bureau not to cut the front yard because the private contractors … will not get out of the vehicle and look at the back yard". Sponsor's statements; no departmental reply found | [resolution](https://www.stlouis-mo.gov/government/city-laws/resolutions/resolution.cfm?RSDetail=true&RSId=19077) |
| Resolution 142, LRA properties (introduced 25 Sep 2026) | "the purpose of LRA has gone astray"; neighbors report "falling bricks", fires, rats, "low to no level of grass cutting" | [resolution](https://www.stlouis-mo.gov/government/city-laws/resolutions/resolution.cfm?RSDetail=true&RSId=19094) |
| Resolution 59, state audit (introduced 2 Jul 2026) | "the City has acknowledged deficiencies and concerns relating to certain grant administration programs" | [resolution](https://www.stlouis-mo.gov/government/city-laws/resolutions/resolution.cfm?RSDetail=true&RSId=18009) |

**Board Bill 134, Vegetation Ordinance (2025-26; law as Ordinance 72098, effective 23 Feb 2026; observed in the bill text):** vegetation of "seven (7) inches or more" is a violation; owners get "up to ten (10) calendar days to abate"; "A non-occupied parcel shall only have to have one notice at the beginning of" the season, after which Forestry may abate; Forestry must report a "Vegetation Memo" to committee each January. No Vegetation Memo was found; the first would fall due in January 2027 (inferred). Resolution 126, seven months later, still describes 4–8 week cutting cycles. [bill](https://www.stlouis-mo.gov/government/city-laws/board-bills/boardbill.cfm?bbDetail=true&BBId=16796)

2025-26 session, by title and status only (observed on the index): Nuisance Review Board (Ord. 72140); Prop NS / LRA agreement (Ord. 72087); $30M Rams to tornado relief (Ord. 72009); minor-purchase threshold raised from $500, set in 1955, to $2,500 (Ord. 72127); Special Committee on Reducing Red Tape re-established for "permitting, licensing, and inspection requirements" (Resolution 6); Resolution 197 asks for sidewalk repairs and a 25 mph limit on Gravois Avenue.

**Negative results (observed by the research agent):**

- No hearing transcripts or written departmental testimony exist online; hearings are video only and minutes record votes. Of seven committee packets opened, two contain a presentation with figures, both from the Mayor's Office or Budget Division, none from an operating department. The Water Division, Streets, Refuse, Forestry, Fire and Public Safety budget presentations of 5–13 May 2026 are not in the packets.
- No Public Safety Committee agenda from 29 May 2025 to 11 Jun 2026 (16 agendas read) lists 911, dispatch or the 911 centre.
- The $40M Rams water allocation was "to be reported out" in the Public Infrastructure and Utilities Committee; its 30 Sep and 7 Oct 2026 agendas do not list it.
- A 12 May 2026 budget hearing covered "Neighborhood Improvement Specialist Office (NIS) and the Citizen Service Bureau (CSB)"; the packet was not opened.

## Part 2. What residents say

Full detail, every URL and the list of sources not reached: `research/parts/B-resident-voice.md`. Sources: local news (mainly St. Louis Public Radio and First Alert 4/KMOV; also St. Louis American, St. Louis Magazine, Type Investigations), six months of r/StLouis post metadata (13 Apr–13 Oct 2026), two Board of Aldermen surveys, American Community Survey 2020–2024, advocacy-group reports, and the 311/CSB file analysed in Part 1A-bis.

Labelling in this part: **reported** = the cited source says so. News figures were matched in the page text by the research agent; the lead thread re-checked seven of them on 2026-10-14 00:02 UTC (tornado repairs, 911 answer rate, 43,200 slow answers, 399 main breaks, nuisance complaints, eviction filings, the Rams survey scores) and all matched the cited page. One of them, the eviction figure, was later found to describe city plus county; see R11. **observed** = counted directly from data (311 file, Census API, survey PDF, Reddit metadata). Reddit figures are "score / comments" and are a rough attention signal from a self-selected, mostly south-city and central-corridor audience.

**Not reached:** KSDK, Fox 2, Missouri Independent, Riverfront Times and most of the Post-Dispatch (blocked or paywalled); X, Facebook, Nextdoor; Reddit comment threads (titles and post text only); 211 data for the city alone. The problems below are ordered by theme, not ranked.

### R1. Tornado recovery: home repair, demolition, debris, displacement

- **Who:** owners and renters in the 16 May 2025 tornado path across north St. Louis; mostly Black neighborhoods; about 73% of homeowners in some of the hardest-hit areas were uninsured (reported, [St. Louis American, 6 Jun 2026](https://www.stlamerican.com/?p=337544)).
- **How many:** city figures: "almost 50,000 residents, more than 23,000 homes" affected; 2,900+ owner-occupied homes and 2,200+ rental units damaged (Part 1B). An estimated **2,674 homes need repair and 2% are complete**; 19 repair jobs finished between March and October 2026; "over 2,200" repair applications waiting; the city pays leases for about 391 displaced people (reported, [STLPR, 1 Oct 2026](https://www.stlpr.org/government-politics-issues/2026-10-01/tornado-recovery-chief-warns-housing-crisis-north-st-louis-recovery); [STLPR, 10 Aug 2026](https://www.stlpr.org/government-politics-issues/2026-08-10/st-louis-disaster-recovery-team-bottlenecks-home-repair-program)).
- **Evidence of dissatisfaction:** WashU "iHeard STL" survey, 16–18 May 2026, n=176 city and county adults: satisfaction with local leaders 3.6/10 (3.04 among Black respondents); more than 8 in 10 said recovery was slower than expected (reported, St. Louis American, above; small non-representative panel). Board of Aldermen Rams survey, 14–27 May 2026, n=1,394, self-selected: tornado recovery ranked first most often; home repair for tornado-hit residents 57% "strongly agree" (observed in the [survey PDF](https://www.stlouis-mo.gov/government/departments/aldermen/president/documents/upload/Board-Bill-22-Survey-Report-with-Appendices-6_5_26-High-Res.pdf)). The city's own recovery report records residents asking for "a timeline they can plan around" (observed, [STL Recovers 2025 Report p. 26](https://tornadorecovery.stl.gov/wp-content/uploads/2026/05/STLRecovers_2025Report-1.pdf)).
- **311 data (observed):** 458 "tornado debris removal" requests since 2025; 368 still open, median age 300 days.
- **Recency / direction:** 1 Oct 2026. Demolitions sped up from March 2026; home repair has stalled; the chief recovery officer warned of a housing crisis as lease support winds down (reported, STLPR 1 Oct 2026).

### R2. Emergency response: 911 answering, police response, warning sirens

- **Who:** anyone calling 911; residents reporting non-violent crime.
- **How many:** St. Louis answered **78% of 2025 calls within 15 seconds** against a 90% national standard; **more than 43,200 callers waited 40 seconds or longer** in 2025 (reported, [STLPR, 15 Sep 2026](https://www.stlpr.org/show/st-louis-on-the-air/2026-09-15/consolidated-911-dispatch-center-st-louis-delayed-2027-police-slmpd); [Type Investigations, 8 Sep 2026](https://typeinvestigations.org/investigation/2026/09/08/americas-911-system-is-facing-its-own-emergency/)). The consolidated 911 centre planned for 2026 is now due to finish construction in late fall 2027 (reported, STLPR, same). Average police response to lower-priority calls rose from about 18 to more than 40 minutes over a decade (reported, Post-Dispatch analysis via [Officer.com reprint, 28 Jul 2026](https://www.officer.com/command-hq/news/55394008/st-louis-police-response-times-for-lower-priority-911-calls-more-than-double-over-decade); original paywalled). The same analysis, seen in three reprints, gives "priority 3" calls rising from 20 to 51 minutes and sworn officers falling to 843 (reported; one underlying source). City budget: about 300 of ~1,100 officer posts vacant (Part 1B).
- **Sirens:** the mayor said "the sirens didn't go off on May 16" (Part 1B). 311 data (observed): 619 "weather sirens not heard during testing" reports since 2023, 380 still open.
- **Resident voice:** r/StLouis "Unresponsive STLPD", 24 Jul 2026, 473 / 221 (observed; one anecdote with many replies).
- **Recency / direction:** 15 Sep 2026. 911 answering better than its 2023 low but below standard; lower-priority police response worsening; the consolidation fix slipped a year (all reported).
- **Note:** police are under a state-appointed board, not the mayor (Part 1B).

### R3. Water: main breaks, multi-day outages, rising rates, overdue bills

- **Who:** all Water Division customers; specific neighborhoods during outages.
- **How many:** **399 main breaks in 2025**, "the most in seven years" (reported, [First Alert 4, 4 Feb 2026](https://www.firstalert4.com/2026/02/04/st-louis-water-main-breaks-strain-already-stressed-fund/)); 155 breaks in January–February 2026 alone (reported, [First Alert 4, 5 Mar 2026](https://www.firstalert4.com/2026/03/05/st-louis-water-division-increases-deficit-projection-10-million-with-busy-start-year/)); about 400 Tower Grove South homes without water during a multi-day break (reported, [First Alert 4, 28 Jan 2026](https://www.firstalert4.com/2026/01/28/we-cant-flush-toilets-city-residents-complain-days-long-water-main-break-city-leaders-aiming-repair-infrastructure-long-term/)); Lindenwood Park and St. Louis Hills "without running water for days" in a heat wave (reported, [First Alert 4, 28 Jul 2026](https://www.firstalert4.com/2026/07/28/water-main-breaks-leave-st-louis-neighborhoods-taps-dry-amid-heat/)). City figures: 16,000+ accounts past due; shut-offs resumed (Part 1B).
- **Demand signal:** water infrastructure had the highest support of 37 proposed Rams uses, 4.32/5 (observed, survey PDF above); it also topped the February 2024 Rams vote, 5,510 of 12,442 respondents (reported, [city release, 8 Feb 2024](https://www.stlouis-mo.gov/government/departments/aldermen/president/news/voting-period-results.cfm)). r/StLouis "City water bills to increase 64% over 6 years", 21 May 2026, 252 / 207 (observed; the 64% is the simple sum of the seven steps in Board Bill 25; compounded they come to about 83%, and STLPR reports "about 90%" over six years, [STLPR, 18 Jun 2026](https://www.stlpr.org/news-briefs/2026-06-18/st-louis-aldermen-ok-90-water-rate-increase)).
- **311 data (observed):** 3,868 water requests in 12 months. "Water coming up" rose 621 → 746 → 932 (Jan–12 Oct, 2024–2026). Requests close in a median 0.1 days, usually as "scheduled for repair by water department", so closure does not mark the repair; 368 are open with a median age of 221 days.
- **Recency / direction:** 28 Jul 2026 (news). Worsening: breaks at a seven-year high, Water Division deficit near $10M, rate rises sought (reported).

### R4. Vacant, overgrown and nuisance properties

- **Who:** neighbors of vacant parcels; 84% of vacant parcels are north of Delmar; pockets in Dutchtown, Gravois Park, Marine Villa.
- **How many:** about **24,000 vacant parcels and 9,000 vacant buildings**; nearly 90% of vacant buildings privately owned; ten neighborhoods hold nearly half (reported, [STLPR, 25 Jun 2026](https://www.stlpr.org/government-politics-issues/2026-06-25/rams-money-st-louis-vacancy-issues); [Community Builders Network summary of the STL Vacancy Collaborative report, 2026](https://www.communitybuildersstl.org/stories-and-news/2026/8/5/vc-report-examines-the-scale-and-impact-of-24000-vacancies-across-st-louis)). 29,220 of 174,111 housing units vacant, 16.8% (observed, ACS 2020–2024 table B25002). 2,300+ public-nuisance property complaints in 2025 and about 1,900 by early September 2026 (reported, [STLPR, 9 Sep 2026](https://www.stlpr.org/government-politics-issues/2026-09-09/new-st-louis-board-community-members-nuisance-properties)).
- **Resident accounts (all reported, First Alert 4):** a 78-year-old amputee in the Greater Ville said overgrown city-owned lots made leaving home unsafe ([24 Jul 2026](https://www.firstalert4.com/2026/07/24/st-louis-woman-says-overgrown-city-owned-lots-make-it-unsafe-leave-her-home/)); a resident beside an LRA lot said no crew had come all year ([14 Aug 2026](https://www.firstalert4.com/2026/08/14/cut-down-unmowed-vacant-lots-st-louis-city-looks-data-north-city-resident-discusses-wait/)); weeds "over six, even seven feet tall" on Iowa Avenue ([25 Aug 2026](https://www.firstalert4.com/2026/08/25/i-want-our-street-back-overgrown-lots-frustrating-south-city-residents/)); tall grass covering a north-side sidewalk (9 Jul 2026). r/StLouis "What to do about squatters?", 15 Sep 2026: the poster says repeated CSB reports got the reply "already under notice" (observed; one anecdote).
- **311 data (observed):** 12,253 vacancy- and dumping-type requests in 12 months, 63% from Wards 10–14. Weeds at vacant buildings up 2,013 → 3,032 and on vacant lots 1,085 → 1,500 (Jan–12 Oct, 2025 → 2026). 34% of "vacant building unsecured" requests repeat an address. "Building already under notice" closed 2,266 requests.
- **City's own measure:** 58% of lots reached in the first 2026 mowing pass; first vacant-building pass 23% done by 30 June (Part 1A rows 6–7).
- **Recency / direction:** 15 Sep 2026. Vacant-parcel count fell about 4% from 2018 before the tornado (reported, [STLPR, 8 May 2025](https://www.stlpr.org/economy-business/2025-05-08/vacant-buildings-st-louis-decreasing-slowly)); the tornado added demolition-grade vacancy; weed requests are up sharply in 2026 (observed).

### R5. Refuse: missed collection, overflowing dumpsters, illegal dumping

- **Who:** households on alley-dumpster routes; blocks beside vacant lots for dumping. No household count found.
- **Evidence:** the city wrote that "many St. Louisans have experienced overflowing dumpsters" (observed, [city release, 15 Aug 2025](https://www.stlouis-mo.gov/government/departments/mayor/news/alley-recycling-ended.cfm)); drop-off recycling bins overflowing a month after the switch (reported, [First Alert 4, 15 Sep 2025](https://www.firstalert4.com/2025/09/15/1-month-st-louis-residents-frustrated-with-new-recycling-system)); r/StLouis "Dump truck load of trash behind my house", 24 Aug 2026, 498 / 112 (observed; one incident). A city trash-and-recycling survey closed 31 Aug 2026; results not found.
- **311 data (observed):** the largest request group: 25,889 in 12 months. "Refuse not collected" 9,077 → 5,079 (Jan–12 Oct, 2025 → 2026), median 1.7 days to close, 40% repeat an address. "Container damaged" 4,951, median 7.9 days. "Illegal dumping report" 880, 49% repeat an address.
- **Recency / direction:** 24 Aug 2026. Missed-collection complaints are down by 44% year on year (observed) and CityStat coverage is near target; dumping remains live. News coverage of missed pickups is thinner in 2026 than 2025 (inferred by the research agent).

### R6. Trees: hazard trees, inspection requests, stumps

- **Who:** residents beside city street trees; tornado-zone blocks. No count of affected residents found.
- **311 data (observed):** 8,967 tree requests in 12 months; 49% cancelled, 21% open. 2,398 "inspect city tree" requests open, 2,012 of them older than 90 days. "City tree down" 385 → 965 → 948 (Jan–12 Oct, 2024–2026).
- **City's own measure:** 591 hazard-tree removals outstanding; 37% removed within 30 days against a 100% goal; half of tree-trimmer posts vacant (Parts 1A, 1B).
- **Resident-side evidence is thin:** two older TV stories (limbs falling on Milentz Avenue with CSB requests unanswered; a homeowner who waited seven years for a dead city tree) could not be opened or dated (reported, search summaries only). Low Reddit volume. Hazardous tree and stump removal scored 3.85/5 in the Rams survey, below most options (observed). A dedicated search found no 2026 news story of a city resident waiting on a hazard tree. Older accounts: St. Louis Hills residents said limbs fell daily and three homes had been damaged, with the Forestry commissioner citing a six-month waiting list (reported, Fox 2 via [NewsNation, 20 Nov 2024](https://digital-release.newsnationnow.com/?p=3138135)); in 2019 the city awarded a $1M contract to remove about 2,000 backlogged trees (observed, [city release, 23 Oct 2019](https://www.stlouis-mo.gov/government/departments/mayor/news/city-awards-contract-to-remove-thousands-of-potentially-dangerous-backlogged-trees.cfm)), so the backlog is long-standing (inferred by the research agent). Reddit: 11 title matches, 129 comments in six months (observed).
- **Recency:** 311 data to 12 Oct 2026.

### R7. Streets and right-of-way: sinkholes and cave-ins, sidewalks, potholes, signs, lights, snow

- **Who:** drivers, cyclists, pedestrians; sidewalk requests are filed under "Disability Issues".
- **Evidence:** sinkholes downtown, north and south; one "had been causing concern for months" and was filled hours after a TV station called (reported, [First Alert 4, 18 Aug 2026](https://www.firstalert4.com/2026/08/18/sinkholes-causing-concern-across-st-louis-residents-say-streets-disrepair/)); a hole near I-44 and North Broadway closed the interstate for nearly two weeks in June 2026 (reported, [STLPR, 26 Jun 2026](https://www.stlpr.org/news-briefs/2026-06-26/i-44-reopen-st-louis-hole)). After the January 2026 storm, north and west-side residents said they waited days for ploughs (reported, [First Alert 4, 28 Jan 2026](https://www.firstalert4.com/2026/01/28/please-help-us-city-residents-concerned-about-unequal-city-services-snow-removal)). Rams survey: streets, sidewalks and lighting in North St. Louis 4.22/5; sidewalk maintenance citywide 4.06/5 (observed).
- **311 data (observed):** cave-ins 1,326 → 1,958 → 1,878 (Jan–12 Oct, 2024–2026), 1,020 of the last year's 2,252 still open. Sidewalk repair: 2,612 open, median 88 days to close. Residential potholes halved, 5,131 → 2,654 (2024 → 2026). Single street light out: median 11.8 days, 90th percentile 143.
- **City's own measure:** major-street potholes 44.5% on time against 80%; critical signs 58.9% against 75% (Part 1A).
- **Recency / direction:** 18 Aug 2026. Sinkholes tied to water and sewer failures are newly salient in 2026; pothole complaints are down.

### R8. Derelict vehicles and towing

- **311 data (observed):** the largest single request type: 8,376 in 12 months, median 15 days to close, 28% closed by the target date; most common outcomes "vehicle gone upon inspection" and "vehicle tagged for tow".
- **City's own statements:** mayoral priority to "eliminate backlog"; four audits in five years with unresolved findings (Part 1B). The public tow-count chart is broken (Part 1A row 22).
- **Resident-side evidence is thin:** one 2025 TV story on an abandoned half-car; booting and towing for unpaid fines resumed about March 2026 (reported, [First Alert 4, 5 Jun 2026](https://www.firstalert4.com/2026/06/05/first-alert-4-sees-car-booted-city-with-1700-owed-fines/)). No 2026 coverage of abandoned vehicles found.

### R9. Dangerous driving, expired tags, street takeovers, traffic deaths

- **Who:** pedestrians, cyclists and drivers citywide; arterials such as Gravois.
- **How many:** Gravois Avenue: 23 crashes and four deaths involving people walking or cycling in 2025 (reported, [STLPR, 23 Jun 2026](https://www.stlpr.org/news-briefs/2026-06-23/safer-streets-st-louis-walking-biking-deaths)); more than 8 in 10 pedestrian deaths in the city happen on arterials (reported, [Trailnet, 23 Jun 2026](https://trailnet.org/2026/06/22/trailnets-2025-state-of-the-streets/)).
- **Resident voice (observed, Reddit):** 90 posts and about 4,400 comments in six months, e.g. "How can people drive around for years with temp tags…", 31 Jul 2026, 678 / 369; "Wild downtown takeover", 24 Sep 2026, 675 / 279.
- **Recency / direction:** 24 Sep 2026. Pedestrian deaths fell in 2025 from a 2024 record; cyclist deaths rose (reported). Enforcement sits with the state-controlled police.

### R10. Loose and dangerous dogs

- **Who:** pedestrians and pet owners; a majority of 2026 dangerous-animal cases came from Wards 11, 12 and 13 (reported, [STLPR, 4 Jun 2026](https://www.stlpr.org/news-briefs/2026-06-04/family-pet-killed-tower-grove-park-dog-attack)).
- **How many:** animal-bite calls 488 (2023), 559 (2024), 657 (2025) and 389 by early June 2026; 420 dangerous-animal complaints in 2025 (reported, [STLPR, 12 Jun 2026](https://www.stlpr.org/show/st-louis-on-the-air/2026-06-12/dog-bite-attack-st-louis-public-safety-animal-control)). Budget book: "a 43% increase in bite-related service requests" (Part 1B detail file).
- **Evidence:** a victim was passed from police to Animal Control to CSB and back (reported, STLPR 12 Jun 2026). The largest civic thread in six months of r/StLouis: a fatal dog attack on a pet in Tower Grove Park, 4 Jun 2026, 1,689 / 852; 56 posts and about 3,800 comments on the topic (observed).
- **311 data (observed):** 8,568 animal requests in 12 months; stray dog at large 2,676, median 1.2 days to close; leash-law complaints repeat an address 46% of the time.
- **Recency / direction:** 25 Jul 2026. Bite calls rising year on year; part of the June spike in attention is one viral event (inferred by the research agent).

### R11. Housing: evictions, rent burden, unsafe rentals, lead

- **Who:** 79,279 renter households, 54.7% of occupied units (observed, ACS 2020–2024).
- **How many:** 34,188 renter households pay 30% or more of income in rent; 18,680 pay 50% or more (observed, ACS B25070). **Eviction filings in City of St. Louis census tracts: 5,893 (2023), 5,220 (2024), 5,685 (2025); 2,932 in January–July 2026 against 3,487 a year earlier, down 15.9%** (observed: Princeton Eviction Lab monthly file, <https://eviction-lab-data-downloads.s3.amazonaws.com/ets/all_sites_monthly_2020_2021.csv>, retrieved by the research agent 2026-10-14 00:16 UTC, 26,558 St. Louis rows of which 8,320 are city tracts, January 2020 to early August 2026, last updated 8 Aug 2026; recomputed by the lead thread). **Correction to a widely quoted figure:** STLPR reported about 10,400 filings "in the city" in 2026 and 17,452 in the past full year ([STLPR, 27 Aug 2026](https://www.stlpr.org/government-politics-issues/2026-08-27/st-louis-right-counsel-expansion-efforts)). In the file all three of STLPR's figures match the combined city-plus-county site: 10,388 for January–July 2026, 1,732 for July, and exactly 17,452 for August 2025–July 2026 (observed). The city alone had 5,130 filings in those 12 months, about 29% of the combined total. The right-to-counsel programme closed 400 cases in its first 20 months (Part 1A row 2). More than 60 people were told to leave the condemned Concord Apartments with little notice (reported, [STLPR, 7 Apr 2026](https://www.stlpr.org/law-order/2026-04-07/st-louis-kicks-dozens-of-people-out-of-their-apartment-complex-with-little-notice)).
- **311 data (observed):** lead-paint inspection requests: 838 filed since 2023, 139 closed, 655 open. Interior property-maintenance complaints 690 → 829 → 1,028 (Jan–12 Oct, 2024–2026).
- **Recency / direction:** data to early August 2026. City filings are below 2025 so far in 2026 but well above the 2020–21 lows (2,612 and 2,933) (observed). Rent burden: one survey period only, no trend.

### R12. Homelessness and shelter

- **How many:** January 2026 point-in-time count "nearly 1,800 city residents", presented as the total including people in shelters, up about 9% on 2025 (reported, [STLPR, 9 Oct 2026](https://www.stlpr.org/government-politics-issues/2026-10-09/st-louis-looks-to-disband-high-risk-tent-encampments-by-providing-holistic-resources)).
- **Evidence:** year-round shelter space fills quickly; homeowners sued the city over a three-year sidewalk encampment (reported, [First Alert 4, 22 Jul 2026](https://www.firstalert4.com/2026/07/22/st-louis-homeowners-sue-city-over-years-long-sidewalk-encampment-tower-grove-south/)). City's own after-action review says shelter-resident tracking needs "better infrastructure" (Part 1B).
- **Recency / direction:** 9 Oct 2026. Rising.

### R13. City Justice Center (jail)

- **How many:** at least 22 deaths in custody since 2020 by STLPR's count; an NAACP report describes gaps in death and medical investigations (reported, [STLPR, 2 Sep 2026](https://www.stlpr.org/law-order/2026-09-02/st-louis-naacp-details-gaps-in-death-medical-investigations-at-city-jail)). Average daily population 774 in FY2025 and 733 over three quarters of FY2026 per the budget book; the city's inmate dashboard shows 787 for calendar 2026 (observed; Part 1B detail file, Part 3.2).
- **Recency:** 2 Sep 2026. Narrow affected population; direction not established.

### R14. The complaint system itself: CSB/311

- **Evidence:** the mayor named CSB routing time as needing improvement (reported, [First Alert 4, 31 Mar 2026](https://www.firstalert4.com/2026/03/31/heres-how-you-can-see-st-louis-city-service-performance-data/)). Problems were fixed within hours or days of a TV station calling: the Miami Street sinkhole (18 Aug 2026) and overgrown lots (July 2026) (reported, First Alert 4; the reading that media attention works faster than a request is the research agent's inference). Reddit is mixed and sparse: 12 posts in six months, including "Reporting to CSB works!" (2 Sep 2026) and a poster who found CSB reviews "are not good" (13 Sep 2026) (observed; anecdotes).
- **311 data (observed):** 21,292 requests open, 9,069 older than a year; 23.7% of requests repeat an address and problem; 14.6% of closures carry no outcome text; "closed" does not mean done (Part 1A-bis).
- **Recency:** 8 Oct 2026. Resident-side evidence is moderate; the data evidence is strong.

### R15. Raised by residents, but outside city service delivery

Kept so they are not lost; each is controlled by another body or is a policy dispute.

- **Data-centre siting** — the largest civic topic on r/StLouis by volume: 81 posts, about 4,920 comments in six months; a Board of Adjustment hearing drew nearly 11 hours of public comment and opponents sued (reported, [STLPR, 29 Aug 2026](https://www.stlpr.org/government-politics-issues/2026-08-29/opponents-st-louis-data-center-take-fight-court)). A land-use dispute.
- **St. Louis Public Schools closures** — 14 schools proposed for closure; board vote 10 Nov 2026 (reported, [STLPR, 9 Sep 2026](https://www.stlpr.org/education/2026-09-09/st-louis-public-schools-delays-school-closures-timeline-again-for-more-community-input)). Separate government.
- **Electricity bills** — Ameren filed for a third increase in five years (reported, [STLPR, 30 Jun 2026](https://www.stlpr.org/economy-business/2026-06-30/ameren-missouri-customers-bills-could-go-up-by-13-a-month-2027)); 80 Reddit posts, about 2,290 comments. State-regulated utility.
- **Licence-plate-reader surveillance** — 1,000+ readers in the region; "Someone tore down a Flock camera in The Grove", 11 Oct 2026, 936 / 71 (reported/observed).
- **Gun violence and property crime** — police counts show homicides falling: 151 (2024), 141 (2025), and 80 through August 2026 against 96 a year earlier (reported, one underlying source, SLMPD; [First Alert 4, 1 Sep 2026](https://www.firstalert4.com/2026/09/01/st-louis-police-report-lowest-number-homicides-through-august-over-decade/), [STLPR, 13 Jan 2026](https://www.stlpr.org/law-order/2026-01-13/crime-rates-st-louis-drop-2025-police)). Felony thefts were higher in 2026, driven by car break-ins (reported, [STLPR, 1 Jul 2026](https://www.stlpr.org/law-order/2026-07-01/st-louis-homicides-reach-12-year-low-through-first-half-of-2026)). Reddit: 85 posts on shootings, about 4,020 comments, and 67 on break-ins (observed; metro-wide). No shooting-incident count and no survey of whether residents feel safer was found. Policing is under the state-appointed board.
- **Transit, immigration-enforcement fear, food access in the tornado zone, pests, fireworks** — single sources or anecdotes; see the detail file section 2.16.

### Searched for and not supported as current resident complaints

- **Graffiti** (kickoff topic): 18 Reddit matches in six months, the largest about corporate advertising stencils; a dedicated search found no 2025–2026 story of residents complaining about tagging or slow removal. 311 volume is modest and falling: private-property graffiti 1,182 → 731 (Jan–12 Oct, 2024 → 2026) (observed).
- **Potholes** (kickoff topic): moderate and seasonal. Named resident accounts cluster in February–March 2025 and 2026 (reported; e.g. south-side streets "not repaved in more than 20 years", [First Alert 4, 19 Mar 2026](https://www.firstalert4.com/2026/03/19/theyre-awful-shape-some-south-st-louis-roads-havent-been-paved-20-years/)); the mayor said the pothole request backlog had been cut by 70% (reported, [STLPR, 1 Apr 2026](https://www.stlpr.org/government-politics-issues/2026-04-01/st-louis-website-city-services-fixes)). Reddit April–October: 9 posts. 311 volume halved since 2024 (observed).
- **Urban heat** (kickoff topic): thin as a complaint about a city service. It appears tied to electricity cost, tornado-damaged housing and water outages: an 84-year-old tornado survivor without air conditioning since May 2025 (reported, [First Alert 4, 10 Jun 2026](https://www.firstalert4.com/2026/06/10/heat-can-beat-you-st-louis-organizations-help-those-need-during-heat-wave/)); a 2024 listening session where residents described too few accessible cooling centres and shade trees (reported, [STLPR, 22 Nov 2024](https://www.stlpr.org/health-science-environment/2024-11-22/st-louis-extreme-heat-plan)). No city heat-illness or heat-death count for 2026 and no resulting heat plan was found.
- **Building-permit delays, streetlight outages, property-tax bills:** no 2025–2026 complaint coverage found. Permits do appear in the city's own figures (Part 1A row 11).

### Surveys found

| Instrument | Dates | n | Finding | Label |
|---|---|---|---|---|
| Board of Aldermen Rams-settlement survey (Board Bill 22) | 14–27 May 2026 | 1,394, self-selected | Six uses drew over 50% "strongly agree": water infrastructure 57%, tornado home repair 57%, tornado rental assistance 53%, North St. Louis streets/sidewalks/lighting 53%, demolition in tornado areas 52%, case management 50%. Downtown items ranked lowest. Open comments asked for transparency and measurable outcomes | observed (PDF above) |
| Rams-settlement public vote | to Feb 2024 | 12,442 | Water-main replacement 5,510 supporters; traffic calming 5,155 | reported (city release above) |
| WashU iHeard STL tornado survey | 16–18 May 2026 | 176, city and county | Local leaders 3.6/10; 8 in 10 say recovery slower than expected | reported (St. Louis American) |
| St. Louis Magazine / Nine PBS "Citizens' Agenda" | Feb 2025 | not stated | Five themes: transparency and accountability; city services; public safety; downtown; vision | reported, [stlmag.com](https://www.stlmag.com/news/citizens-agenda-2025-st-louis-mayoral-race) |
| United Way 211 | 2025 | 254,000+ contacts, 16 counties | Top needs: housing and shelter, utilities, food, disaster relief, transportation. 3,207 residents sought tornado help through 211 in the year after the storm | reported, [First Alert 4, 10 Feb 2026](https://www.firstalert4.com/2026/02/10/united-way-celebrates-211-day/); no city-only split |
| **No city-run resident satisfaction survey was found.** | | | | negative result |

Census context (observed, ACS 2020–2024 via Census Reporter API, retrieved 2026-10-13 23:27 UTC): population 288,512; 20.6% below poverty; 18.5% of households with no vehicle; 9.8% with no internet access; 2.1% limited-English households.

## Part 3. What already exists

Full inventory (about 150 tools, systems, programmes and vendors, each with operator, what was loaded and when, and URLs): `research/parts/B-existing-tools.md` and the two files under `research/parts/B-existing-tools.d/`. Pages were loaded by research agents on 2026-10-13 23:14–23:38 UTC without signing in, submitting any form or creating an account, so anything behind a login or a submit button was not seen.

Labels: **observed** = the page or file was loaded and the stated text or count was in it; **reported** = a news or third-party source says so; **not found** = searched for and not located, which does not prove absence. **✔** marks items the lead thread re-checked on 2026-10-14 00:07–00:08 UTC (13 items; 11 matched, 1 did not reproduce, 1 could not be re-queried — see "Looked for, not found").

**Data retrieved by the lead thread for this part.** STL Recovers tracker files, retrieved 2026-10-14 00:08:22 UTC, `Last-Modified` 13 Oct 2026 23:05 GMT, saved in `data/raw/stl-recovers-tracker/`: `https://publicgoodness.org/stlrecovers/city/code/bld_dashboard_home_repair.geojson` (2,743 records), `…/bld_dashboard_demolitions.geojson` (1,761) and `…/bld_dashboard_trees_debris.geojson` (808). The files carry a status per parcel and no date range field was read; the newest completion date seen by the research agent was 12 Oct 2026.

### 3.1 Systems that sit under most services

| System | Operator / vendor | What it does | Visible shortfall | Label and source |
|---|---|---|---|---|
| CSB / 311 intake | Citizens' Service Bureau, Neighborhood Stabilization Division; "staff of seven (7) CSRs serve the entire City" ✔ | Phone 311 (since June 2025), web form with 27 categories, live chat, email, X; issues a request number | Staffed Mon–Fri 8–5 only; location step is a typed address with no map pin seen; web session expires after about 20 minutes; chat requires name, email and phone; no mobile app found in the App Store | observed, [CSB](https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/index.cfm), [NSD](https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/index.cfm) |
| CSB status lookup | In-house (ITSA web team) | Public lookup by request number or address: status, resolution text, department, due date | "Closed" can mean referred: a 2021 cave-in request shows Closed with "Referred to street maintenance for repair work to be scheduled". The page that should define status codes returns "Inactive Content" ✔ | observed, [lookup](https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/check-service-request.cfm), [status definitions](https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/status-definitions.cfm) |
| Cityworks | Azteca Systems (Trimble); city paid Azteca $220,273 in FY2026 | Staff-side work management behind CSB, in use since 2009; live on 13 Oct 2026 (it feeds the public pothole map) | Staff login only. No city statement or contract found describing a replacement or upgrade | observed, [login page](https://service.stlouis-mo.gov/cityworks/Login.aspx), [expenditure database](https://www.stlouis-mo.gov/government/departments/budget/transparency/expenditure/suppliers/index.cfm) |
| Open311 API and weekly CSV | ITSA | Read/write API (key required); bulk CSV of all requests | API returns HTTP 400 without a key; catalog shows "Data updated: Unknown" although the CSV was modified 13 Oct 2026 | observed, [API](https://www.stlouis-mo.gov/government/departments/information-technology/web-development/city-api/csb-api.cfm), [dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5) |
| "My City" account | ITSA, in-house (launched March 2025 as OneStopGov) | One login for CSB requests and some applications | Its own help page lists as unsupported: "Permits issued by the Building Division", "Licenses issued by the License Collector", "City job applications" ✔ | observed, [applications help](https://www.stlouis-mo.gov/my/city/applications.cfm) |
| CityStat | Mayor's Office; Tableau | Public performance pages since 31 Mar 2026 | See Part 1A: stale since 30 June, no downloads, one broken chart, coverage gaps | observed |
| Website, open data, GIS | ITSA; CommonSpot CMS; Esri (paid $456,000 in FY2026) | 72 open datasets; public map services for trees, LRA property, recycling sites | Most operational layers (building, water, police, Cityworks) need a token; several catalog entries are stale or dead (Forestry parcel classification CSV last modified 26 May 2023 but labelled weekly) | observed, [open data](https://www.stlouis-mo.gov/data/), [services](https://maps9.stlouis-mo.gov/arcgis/rest/services) |
| Translation | Google website-translate widget | Machine translation of city web pages in six featured languages and more | Does not extend to linked tools: no translate control on the permit portal, the tornado hub or the tracker | observed, [translate page](https://www.stlouis-mo.gov/government/departments/information-technology/web-development/web-accessibility/translate.cfm) |
| Payments | PayIt (taxes, water, forestry, street charges); WBlue (permits); Click2Gov (water account) | Online payment | Three payment systems; the city's "Pay a Water-Refuse Bill" button led to an HTTP 404; PayIt iOS app rated 2.54 from 26 ratings; the Click2Gov page says it is designed for "Internet Explorer 7+" | observed, [PayIt](https://payitstlouis.com/), [Click2Gov](https://stlo-egov.aspgov.com/Click2GovCX/index.html) |
| Chatbot or AI assistant; 311/CRM procurement | — | — | Not found on any city page loaded. No open solicitation for a 311 replacement, resident app, AI tool, pavement assessment or fleet tracking in the procurement list on 13 Oct 2026 | not found, [procurement](https://www.stlouis-mo.gov/government/procurement/index.cfm) |

### 3.2 Crosswalk: problem → what exists → where it visibly falls short

| Problem (Part 2 ref.) | What the city or partners operate | Where it visibly falls short | Label and source |
|---|---|---|---|
| **Tornado home repair, demolition, debris (R1)** | STL Recovers hub (Recovery Office); application portal app.stlrecovers.com (vendor not identified); public parcel trackers for demolition, repair, trees and debris (built and hosted by Public Goodness, a one-person civic-tech shop); construction manager SLSCO Ltd (contract "could go up to $26 million", repairs capped at $50,000 a house); outreach centre and phone lines; disaster case management; Impacted Tenants Fund; rental assistance; legal aid (LSEM) | Tracker data, modified 13 Oct 2026 23:05 GMT ✔: **2,743 home-repair records, 2,256 (82%) "Awaiting Prioritization", 52 complete**; demolition 1,761 parcels, 542 complete, 524 "Needed"; 89% of repair records are in Wards 10–12. The tracker has status but no expected date, and no lookup by application number. The hub lists four programmes as "no longer accepting applications" and two as "COMING SOON" ✔. Hub and tracker are English only. About 5,000 of roughly 7,300 damaged properties had not applied for city aid by February 2026 (reported). No public dashboard of recovery spending was found; a petition asks for one. No progress report after June 2026 on the city's documents page | observed (tracker files saved in `data/raw/stl-recovers-tracker/`), [hub](https://tornadorecovery.stl.gov/help/), [tracker](https://tornadorecovery.stl.gov/dashboard/?repair); reported, [STLPR 6 Feb 2026](https://www.stlpr.org/government-politics-issues/2026-02-06/tornado-victims-lose-hope-st-louis-programs-deny-relief-hundreds), [First Alert 4, 14 May 2026](https://www.firstalert4.com/2026/05/14/st-louis-hires-texas-company-manage-tornado-recovery-programs/), [petition](https://www.change.org/p/demand-mayor-spencer-show-where-every-north-st-louis-recovery-dollar-went) |
| **911 answering and police response (R2)** | SLMPD Communications Division answers 911 and transfers fire/EMS calls to a separate Fire dispatch site; police CAD is Hexagon/Intergraph, with a CentralSquare replacement paid for from ARPA ($1.09M spent; go-live not determined); a $45M consolidated 911 centre under construction; SLMPD "Calls for Service" rolling list; CrimeMapping.com (180 days); P3 anonymous tips | No public call-answer-time figures on any SLMPD or city page; centre slipped from 2026 to late fall 2027; no online form for reporting minor crime found (residents are told to phone); no text-to-911 announcement found for the city; police and the 911 answering point are governed by the state-appointed board, not the mayor | observed, [SLMPD communications](https://slmpd.org/communications/), [ARPA CAD project](https://www.stlouis-mo.gov/government/recovery/covid-19/arpa/projects/project.cfm?id=341); reported, [STLPR 15 Sep 2026](https://www.stlpr.org/show/st-louis-on-the-air/2026-09-15/consolidated-911-dispatch-center-st-louis-delayed-2027-police-slmpd) |
| **Warning sirens and emergency alerts (R2)** | 60 outdoor sirens, moved from CEMA to the Fire Department in May 2025, activation automated in 2026; NotifySTL opt-in alerts (Everbridge, $89,527 a year); siren faults reported through CSB | Sirens did not sound on 16 May 2025; in March 2026, 17 of 60 had been replaced and 4 were still broken (reported); no public siren-status map; NotifySTL needs an account and publishes no enrolment figure; the emergency operations plan dates from 2003 (city release) | observed, [sirens](https://www.stlouis-mo.gov/government/departments/public-safety/fire/ows.cfm), [NotifySTL](https://www.stlouis-mo.gov/notifystl/); reported, [First Alert 4, 13 Mar 2026](https://www.firstalert4.com/2026/03/13/first-alert-4-sits-down-with-cema-commissioner-fire-chief-latest-tornado-sirens/) |
| **Water: main breaks, outages, bills (R3)** | Outage and repair list at stlwater.com/outages (refreshed every 15 minutes); leak reports through CSB; billing by the separately elected Collector of Revenue through PayIt, plus a second Click2Gov account site; meter upgrade programme (about 11,100 of 16,500 meters); lead-service-line viewer; tornado water affordability programme (enrolment closes 31 Oct 2026); HDR master plan in progress ($1.275M) | Outage page is a list: no map, address lookup or per-address notice. Most homes are billed a flat rate by rooms and fixtures and have no usage data. The master plan page lists $150M of unfunded small-main replacement across about 1,300 miles. Two city sites disagree on whether the $500 assistance credit is open or "Discontinued". Lead viewer depends on residents submitting photos; no replacement schedule shown | observed, [outages](https://www.stlwater.com/outages/), [projects](https://www.stlwater.com/about-us/projects/), [rates](https://www.stlwater.com/customers/water-rates/), [assistance](https://www.stlwater.com/resources/assistance-programs/) |
| **Vacant lots and buildings: mowing, securing, LRA (R4)** | Forestry mowing rotation (city crews for lots, contractors for vacant-building lots); CSB weed categories (vacant types "Seasonal Only", 1 Mar–30 Sep); LRA land bank (about 8,000 lots and 2,000 buildings) with city-owned property search; Prop NS stabilisation ($6M a year); Vacancy Collaborative's Vacant Property Explorer and Demolition Dashboard (Public Goodness); LSEM neighborhood advocacy litigation; new Nuisance Property Review Board; GeoSTL reported in August 2026 to be working with the city on satellite-based mowing priorities | CityStat itself: "More root cause analysis needs to be done to determine why some lots were not mowed". A per-lot status log was "hopefully coming" in mid-August 2026 (reported); not found. Lot counts conflict: 12,171 (chart), about 14,000 (CityStat text), "in excess of 20,000" (Forestry to KMOV). LRA: "all offers must be submitted in-person" ✔, by appointment, on PDF forms, with no offer-status lookup; the city page says it can no longer guarantee offers reach the next agenda. Prop NS: 190+ buildings stabilised, 113 sold, 12 fully rehabbed after five years (reported). Vacancy Collaborative has no paid staff in 2026; its explorer updates monthly and hands reports off to the CSB form. Vacant-building registry lookup: not found. The city's own Demolition Permit Data dashboard counts permits issued (865 so far in 2026 against 415 in 2025 ✔), not demolitions pending, done or funded. No output from the GeoSTL work found | observed, [CityStat Forestry](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/parks/forestry-division.cfm), [LRA](https://www.lrastl.org/offer-to-purchase), [explorer](https://www.stlvacancytools.com/); reported, [First Alert 4, 14 Aug 2026](https://www.firstalert4.com/2026/08/14/cut-down-unmowed-vacant-lots-st-louis-city-looks-data-north-city-resident-discusses-wait/), [STLPR 14 Jan 2026](https://www.stlpr.org/government-politics-issues/2026-01-14/struggling-st-louis-program-fixes-sells-vacant-homes-north-city-boost), [First Alert 4, 26 Aug 2026](https://www.firstalert4.com/2026/08/26/st-louis-launches-ai-innovation-center-backed-by-tech-giants/) |
| **Refuse and illegal dumping (R5)** | Collection-day lookup by address; route completion recorded since September 2025 (vendor not identified); 46 recycling drop-off sites with Brightside and the Recycle Coach app; SLMPD dumping cameras (255 in 2023, reported); missed pickups and dumping reported through CSB | No resident-facing "was my alley collected" status found; route completion was unrecorded before September 2025; share of recycling actually recycled fell to about 76% from February 2026, cause "currently being investigated"; dumping-camera and enforcement figures are from 2023 | observed, [CityStat Refuse](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/refuse.cfm); reported, [STLPR 30 Mar 2023](https://www.stlpr.org/health-science-environment/2023-03-30/st-louis-police-issue-record-number-of-summonses-for-illegal-dumping-but-problem-remains) |
| **Trees (R6)** | Tree reports through CSB (7 types); public tree inventory map (134,920 sites); federal canopy grant with Forest ReLeaf and contractors (targets: plant 3,200, prune 20,000+, remove 1,600+); stump-removal RFP closed 14 Sep 2026; removal "blitz" with contractors from July 2026 | No Forestry-specific tracker: same CSB status page. Canopy-grant page gives targets and no progress figures. New-tree planting waits on each ward's funds. Bulk inventory export dated March 2026. Rams deck lists "Update tree inventory map" as an intended purchase. Half of tree-trimmer posts vacant (Part 1B) | observed, [report a tree](https://www.stlouis-mo.gov/government/departments/parks/forestry/trees/report-tree-problems.cfm), [inventory](https://www.stlouis-mo.gov/government/departments/parks/forestry/trees/tree-inventory.cfm), [canopy programme](https://www.stlouis-mo.gov/government/departments/parks/forestry/trees/tree-canopy-program.cfm) |
| **Streets: potholes, cave-ins, sidewalks, signs, lights, snow (R7)** | Pothole reports through CSB, with a public pothole map fed live from Cityworks; 50/50 sidewalk programme; streetlight reports through CSB (alley lights belong to Ameren, a different channel); snow operations centre with internal camera monitoring and plough GPS since 2025; $500,000 budgeted for a sign and striping inventory | Published pothole targets disagree (service page 2/7/16 business days; CityStat 3/8/17). Potholes are known only from resident reports. Pothole map configuration untouched since March 2020; an open request dated 4 Aug 2026 was 70 days old against a 3–17 day target (agent query; not re-queried by the lead thread). No public plough tracker. Not found: any automated road-condition detection, pavement-condition index, or networked streetlight outage detection (the city page says "sometimes your call is what's needed to learn about a lighting issue"). Sidewalk audit findings unresolved since 2022 (Part 1B); the 50/50 page says "The waiting list can be long, because it depends on the amount of funds available in your ward" ✔, with no queue position or date; the newest item on the city's disability-access transition plan page is from May 2021 | observed, [pothole map](https://stlcity.maps.arcgis.com/apps/mapviewer/index.html?webmap=f634bd1e65bd4d7e9f92650f47219db4), [potholes](https://www.stlouis-mo.gov/government/departments/street/street-division/potholes/report-a-pothole.cfm), [lighting](https://www.stlouis-mo.gov/government/departments/street/street-division/report-street-lighting-problem.cfm), [snow](https://www.stlouis-mo.gov/government/departments/street/street-division/snow-ice/index.cfm) |
| **Derelict vehicles and towing (R8)** | CSB "Vehicles" category → Street Division inspection → Towing Division; Towed Car Lookup by plate or VIN (45 vehicles listed for the previous two days); new Towing Commissioner announced 24 Sep 2026; seven telecom posts added in the FY27 budget | CityStat states that "'Closed' does not necessarily indicate that a vehicle has been towed" ✔ and that the city "plans to implement process changes"; retrieval is in person with fees quoted by phone; the public tow-count chart is broken; four audits with unresolved findings | observed, [CityStat Towing](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/towing.cfm), [lookup](https://www.stlouis-mo.gov/government/departments/street/towing/lookup/index.cfm) |
| **Dangerous driving and traffic deaths (R9)** | Traffic calming by ward-by-ward ordinance; Board Bill 75 (centralised request path and monthly public map) delivered to the mayor; red-light and speed cameras authorised by ordinance in April 2024; Trailnet's annual crash report | No resident request form or tracker for traffic calming yet; cameras reported not installed and no vendor contracted (July 2025; "headwinds" January 2026); enforcement sits with the state-controlled police; no city crash or traffic-death dashboard found, and the pedestrian-safety documents posted are dated 2013 and 2014 | reported, [First Alert 4, 10 Sep 2026](https://www.firstalert4.com/2026/09/10/st-louis-proposes-legislation-streamline-traffic-calming-measures/), [St. Louis Magazine, 12 Jan 2026](https://www.stlmag.com/news/red-light-cameras-stlouis-city/); observed, [Trailnet](https://trailnet.org/blog/2025-state-of-our-streets/) |
| **Loose and dangerous dogs (R10)** | Animal Care and Control reports through CSB (11 complaint types); shelter run by nonprofit CARE STL; contract extended July 2026, the operator saying "the total contract provides about $1 million" (reported) | Complaints share the general CSB queue with pest control; no city list of impounded animals (lost-pet advice includes "Check Craigslist frequently") | observed, [report](https://www.stlouis-mo.gov/government/departments/health/animal-care-control/report-animal-problem.cfm), [shelter](https://www.stlouis-mo.gov/government/departments/health/animal-care-control/shelter.cfm); reported, [STLPR 21 Jul 2026](https://www.stlpr.org/government-politics-issues/2026-07-21/care-stl-extends-contract-st-louis-money) |
| **Evictions, unsafe rentals, lead (R11)** | HELP-STL right to counsel (Legal Services of Eastern Missouri); Impacted Tenants Fund (Jotform); citywide rental occupancy inspections since October 2024 through the WBlue permit portal; code complaints through CSB; child lead screening by referral | HELP-STL: request is by phone only; two attorneys, hotline switched off hours after opening on Mondays (reported, November 2025); monthly reports stop at April 2026; contract status after September 2026 not found. City's own eviction indicator is from 2018. No public lookup of whether a rental holds a current occupancy certificate, or of open violations by address. Code complaints close at notice, not at compliance. Newest city lead report is 2018; 655 lead-inspection requests open (Part 1A-bis) | observed, [HELP-STL](https://www.stlouis-mo.gov/government/departments/human-services/help-stl/request-help-stl.cfm), [occupancy](https://www.stlouis-mo.gov/government/departments/public-safety/building/permits/occupancy-permits/residential-occupancy.cfm), [lead reports](https://www.stlouis-mo.gov/government/departments/health/documents/lead/index.cfm); reported, [STLPR 20 Nov 2025](https://www.stlpr.org/government-politics-issues/2025-11-20/st-louis-program-evictions-free-legal-aid-crisis) |
| **Homelessness and shelter (R12)** | Intake through United Way 211, the Housing Helpline and St. Patrick Center; provider-side HMIS (WellSky, run by the Institute for Community Alliances); Code Blue winter plan with 22 warming centres; two Airtable inquiry forms | No public view of shelter-bed availability; every city page says to call. The Continuum of Care domain cocstl.org, linked from the city's pages for data and board information, redirects to a gambling-spam URL ✔. Newest point-in-time count on the city page is 2019. The Code Blue page gives the same trigger for three different activation levels | observed, [resources](https://www.stlouis-mo.gov/government/departments/human-services/homeless-services/resources.cfm), [CoC page](https://www.stlouis-mo.gov/government/departments/human-services/homeless-services/continuum-of-care/index.cfm), [Code Blue](https://www.stlouis-mo.gov/government/departments/human-services/homeless-services/winter-housing-outreach-and-emergency-shelters.cfm) |
| **Jail (R13)** | Inmate locator (exact-name match only); Inmate Population Data dashboard (average daily population 774 in 2025, 787 in 2026); Detention Facilities Oversight Board | Oversight board: 30 complaints in FY2025, one investigated, 29 pending (Part 1B detail file); six of nine board seats filled; no online complaint form or status lookup seen. Dashboard gives counts only: nothing on deaths, incidents, staffing or complaints. Locator returns no charges, bond or court date | observed, [locator](https://www.stlouis-mo.gov/government/departments/public-safety/corrections/stl-city-find-an-inmate.cfm), [dashboard](https://www.stlouis-mo.gov/data/dashboards/inmates/index.cfm), [oversight board](https://www.stlouis-mo.gov/government/departments/public-safety/civilian-oversight/detention-facilities-oversight/index.cfm) |
| **City hiring and vacancies (problem 20)** | Careers portal on Oracle Taleo; CityStat Personnel page (one measure: offers accepted within 30 days) | Separate login from "My City"; no public vacancy-rate figure by division; CityStat Personnel page still awaiting its Q2 2026 update | observed, [jobs](https://www.stlouis-mo.gov/jobs/), [CityStat Personnel](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/personnel/index.cfm) |
| **Parks maintenance (problem 21)** | Park problems reported through CSB | No park-specific status tool; CityStat lists two upgrades as not yet done: "Moving to an online payment system (PayIt)" and "Upgrading the Park Reservation system (coming in 2027)" | observed, [CityStat Parks](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/parks/parks-division.cfm) |
| **Building permits (Part 1A row 11)** | STL City Permits portal (WBlue, LLC ✔; about $1.48M paid to Wireless Blue Yonder LLC over three fiscal years, vendor link inferred); online since February 2026 | 66.6% of permits within 30 days against 80%, falling for three quarters since the portal launched; third-party plan review funded only from FY27; separate login from "My City"; FAQ page empty | observed, [portal](https://www.stlcitypermits.com/), [CityStat Building](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/public-safety/building-division.cfm) |
| **Graffiti (kickoff topic)** | Brightside St. Louis crew, funded mainly by federal block-grant money through CDA; 2,530 sites in 2024; CSB graffiti category with five types | Complaint-driven only; no stated turnaround; private property needs a paper consent form, with two different waiting periods published (14 days and 5 days); crew does not work above ground level; no tracking map | observed, [Brightside](https://www.brightsidestl.org/what-we-do/cleaning/graffiti-removal/), [annual report](https://www.brightsidestl.org/wp-content/uploads/2025/12/Annual-Report-2024.pdf) |
| **Third-party reporting channels** | SeeClickFix lists a St. Louis place | "There are no organizations in this area that are participating with SeeClickFix" ✔; 216 issues listed, the ten newest all "Open" and unacknowledged. OpenSTL (the Code for America brigade): website dead, one repository pushed in two years | observed, [SeeClickFix](https://seeclickfix.com/st-louis), [OpenSTL](https://github.com/OpenSTL) |

### 3.3 Patterns across the inventory (inferred by this thread from the rows above)

- **One intake, many back ends.** Water leaks, sirens, dogs, pests, food complaints, code violations, graffiti, trees and discrimination complaints all enter through the same CSB form and get the same status page. Forestry, Water, Recovery and Building then hold the actual work in other systems.
- **Status stops at hand-off.** Towing, cave-ins, code complaints and water leaks close when referred, tagged or noticed. The city says so itself for towing.
- **Trackers show state, not time.** The tornado tracker, CSB lookup and pothole map carry no expected date.
- **Several public tools rest on one outside developer.** The tornado trackers, Vacancy Explorer and Demolition Dashboard are all built and hosted by Public Goodness.
- **The city learns about many faults only when a resident reports them:** potholes, streetlights, missed collections, siren failures.
- **Unresolved link rot on city pages** (observed): Continuum of Care, behavioral-health crisis line, crime-mapping link, water bill payment button, status definitions.

### 3.4 What other cities have deployed (most serious problems only)

Full tables (25 deployments, each with operator, years, cost where found, status and the data the city needed): `research/parts/B-other-cities.md`. Pages and PDFs were retrieved 2026-10-13 23:33 to 2026-10-14 00:12 UTC and saved under `data/raw/other-cities/`. This is a record of what was deployed elsewhere and what was measured. It is not a recommendation.

Labels: **observed** = the research agent read the audit, paper or agency report itself; **reported** = a news relay or the deploying agency's own unevaluated claim. The lead thread re-checked eight headline figures in the saved source text (New York, Houston, Philadelphia greening, Chicago 311, San Diego, Boston, Los Angeles, Washington DC); all matched.

Covered: the five problems ranked highest in the evidence section, plus trees, sidewalks and derelict vehicles, where the city's own figures show the largest shortfalls.

| St. Louis problem | City | What was deployed | What the city had to hold already | Measured outcome, and who measured it | Label and source |
|---|---|---|---|---|---|
| Disaster home repair (1) | New York City, after Hurricane Sandy | Build It Back: repair, rebuild or buyout, run through a purpose-built case management system fed by 311 registrations; $2.3 billion | 311 registrations plus buildings, FEMA and finance records | City Comptroller: 22,436 applied, 8,131 served (36%); 11,140 withdrew, 9,011 with no reason recorded; three years on average from application to finished construction | observed, [Comptroller audit, 20 Oct 2025](https://comptroller.nyc.gov/wp-content/uploads/2025/11/FK23-075A.pdf) |
| | Houston, after Hurricane Harvey | City-run homeowner programmes with pipeline reports by stage | Not stated | HUD Inspector General: three years on, 297 of 8,784 participants assisted (3.4%); 1.8% of funds spent | observed, [HUD OIG, 4 Jan 2022](https://www.hudoig.gov/sites/default/files/2024-02/2022-FW-1001.pdf) |
| | Joplin, Missouri, after the 2011 tornado | Master-developer contract for redevelopment | None | Missouri State Auditor: "no redevelopment had occurred"; rating "Poor" | observed, [State Auditor, Aug 2015](https://auditor.mo.gov/AuditReport/CitzSummaryDirect?id=393) |
| Vacant lots (7) | Philadelphia | Cleaning and greening of vacant lots with ongoing maintenance, about $5 per square metre | A citywide vacant-lot list; geocoded crime reports | Randomised trial of 541 lots: gun violence down 29.1% around treated lots in neighborhoods below the poverty line | observed, [PNAS, 26 Feb 2018, doi 10.1073/pnas.1718503115, read via Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5866574/fullTextXML) |
| | Flint | Neighborhood groups paid small sums to mow land-bank lots every three weeks | Land-bank ownership records | Academic comparison (not randomised): nearly 40% fewer assaults and violent crimes on maintained segments | observed, [Heinze et al., 2018, read via the PMC text service](https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC6373470/unicode) |
| | Chicago | Mowing contractors dispatched by ward superintendents | A complete list of city-owned lots, which it did not have | Inspector General: the department could not show lots were cut the required four times a season, nor whether complaints met the 42-day goal | observed, [OIG audit, 23 Jul 2020](https://igchicago.org/wp-content/uploads/2023/08/DSS-Weed-Cutting-Program-Audit.pdf) |
| | Oakland | Cameras to catch illegal dumping | Readable licence plates in footage | City's own report via KGO-TV: 457 incidents recorded in a year, 13% cited; officers on foot issued 500+ citations | reported, [KGO-TV, 5 Aug 2024](https://abc7news.com/post/new-report-shows-oakland-cameras-do-not-work-foot-patrols-catch-illegal-dumping-city/15144333/) |
| Water mains (5) | Syracuse | Machine-learning break-risk score per block, built in-house with university fellows | About 10,000 work orders (2004–2015); a GIS layer of mains digitised from hand-drawn notebooks | Builders' own evaluation: 33 breaks occurred on the 52 riskiest blocks within two years. Not independently evaluated | observed (paper), [Kumar et al., KDD 2018](https://arxiv.org/pdf/1805.03597) |
| Water bills (6) | Philadelphia | Bills capped at a share of income; from 2024 customers were pre-qualified from other city records | Linked city records identifying low-income customers | City's own reports: participants 21,694 (Dec 2023) → 60,378 (Dec 2024); 37,538 of 42,212 enrolments in 2024 came through pre-qualification | observed (agency report), [2024 report](https://www.phila.gov/media/20250814092458/Tiered-Assistance-Program-TAP-2024-annual-report.pdf) |
| | Detroit | Income-based fixed bills from $18 a month | Not stated | Enrolled about 29,000–30,000 households, then scaled back when state and federal money ran out | reported, [BridgeDetroit, 17 Oct 2025](https://www.bridgedetroit.com/detroit-water-affordability-program-to-raise-bills-serve-fewer-households-as-funding-dries/) |
| 311 closure and status (12) | Boston | App sent the requester a photo of the completed work | A completion photo on each closed request | Harvard study: users who received photos filed 60% more requests over the next 13 months. Measures engagement and trust, not whether work was done | observed (abstract), [Buell et al., 2020, doi 10.1287/msom.2020.0877, abstract read via OpenAlex](https://api.openalex.org/works?search=Surfacing%20the%20Submerged%20State%20Operational%20Transparency%20Increases%20Trust) |
| | Chicago | CHI311 site and app showing status and a timeliness target | Consistent work-order outcome codes across 40+ departments | Inspector General: status information "contributes to public confusion and distrust"; the public sees a 20-day target where the full chain of work orders totals 110 days; requests reported closed as complete with no work apparent; no percentage given | observed, [OIG audit, 26 Feb 2026](https://igchicago.org/wp-content/uploads/2026/02/OIG-Audit-of-311-Service-Request-Process.pdf) |
| | San Diego | Get It Done app and portal | Accurate closure codes; a way to hold a case open while another body handles it | City Auditor: closure details inaccurate or misleading in 19% of cases reviewed; referred requests shown as "Closed" while unresolved | observed, [City Auditor, 6 Oct 2022](https://www.sandiego.gov/sites/default/files/23-004_get_it_done_application_and_service_requests_management.pdf) |
| 911 answering (3) | Baltimore | 311 as a police non-emergency number | Dispatch records for both numbers | Federally funded evaluation: 25% fewer 911 calls; total calls unchanged; 57% of 311 calls still dispatched to patrol | observed, [NIJ report, 2003](https://www.ojp.gov/pdffiles1/nij/grants/199060.pdf) |
| | Washington, DC | 911 agency audited against national standards | Time-stamped call and dispatch records | DC Auditor: of about 99,000 top-priority incidents, time-to-answer missed about half the time; the 60-second dispatch standard never met | observed (auditor's release), [23 Mar 2023](https://dcauditor.org/wp-content/uploads/2023/08/OUC.911.Reform.Status.Report.Press_.Release.3.23.23.pdf) |
| | Grand Traverse County, Michigan | AI voice system on the non-emergency line only | Not stated | Dispatch director's own account: 3–5% of calls deflected at launch, 30% after two months of fixes; "still gets confused about 10 percent of the time" | reported, [9&10 News, 18 Mar 2026](https://www.9and10news.com/2026/03/18/grand-traverse-county-911s-ai-system-hits-stride-after-rocky-start/) |
| Tree backlog (8) | Chicago | Switch from trimming by 311 request to trimming every tree area by area | A tree inventory (not confirmed in the audit text) | Inspector General, 2019: 75% of crew time went on 311 requests; about 206,000 trees untrimmed for ten years. City's own count after the switch: 34,262 trees trimmed by July 2023 against 9,342 a year earlier | observed (advisory), [OIG, 30 Oct 2019](https://igchicago.org/wp-content/uploads/2023/08/OIG-Advisory-Concerning-DSS-Inefficient-Tree-Trimming-Operations.pdf); reported (2023 count), [Daily Line, 4 Aug 2023](https://www.thedailyline.com/city-forestry-crews-trim-triple-grid-based-system-trees) |
| | Toronto | Crew daily logs checked against vehicle GPS | GPS on crew vehicles | Auditor General: crews logged work at trees where the vehicle never stopped; 41% of sampled logs had gaps | observed, [Auditor General, 3 May 2019](https://www.toronto.ca/legdocs/mmis/2019/au/bgrd/backgroundfile-132624.pdf) |
| Sidewalks (9) | Los Angeles | Repair programme under a disability-rights settlement, $1.37 billion over 30 years | A citywide condition assessment, which it did not have | City Controller: under 1% of 640,000 parcels certified; $35M+ paid in injury claims over five years | observed, [Controller, 17 Nov 2021](https://controller.lacity.gov/audits/sidewalks) |
| | Seattle | Full condition survey by 14 interns with tablets, $400,000 | An existing sidewalk inventory | Department's own report: 2,300+ miles inspected, 99% of the inventory rated; no figure for repairs that followed | observed (agency report), [SDOT, 2018](https://seattle.gov/Documents/Departments/SDOT/About/SidewalkAssessExecSummary_4_6_2018R5.pdf) |
| Derelict vehicles (11) | Philadelphia | Police unit investigating each 311 report; district sweeps from 2024 | 311 complaints by district | News analysis: 34,000+ active reports in April 2022; wait from report to tow rose from two to about six months. No figure after the sweeps | reported, [Inquirer, 24 Apr 2022](https://www.inquirer.com/news/abandoned-cars-philadelphia-police-towing-20220424.html) |
| | San Jose | Reports ranked by vehicle condition; photo required with each report | A photo with every report | City officials via news: before the change 7–8% of 55,000–60,000 yearly requests ended in a tow; 25,000 visits a year found the vehicle gone. No result after the change | reported, [San Jose Spotlight, 24 Jun 2022](https://sanjosespotlight.com/san-jose-refreshes-its-approach-to-abandoned-vehicles-cars-rvs-blight-towing/) |

**What this record shows (observed across the rows):**

- Independent evaluations with a measured effect exist for three deployments only: Philadelphia lot greening, Boston completion photos, Baltimore 311.
- Most of the rest are auditors' findings, and most are negative. Every disaster-housing case found is negative or mixed.
- Several audits turn on a missing base record: a complete lot list (Chicago), a sidewalk condition assessment (Los Angeles), accurate tree-pruning lists (New York). For St. Louis, Parts 1 and 3 record conflicting vacant-lot counts and a sign inventory that is budgeted but not yet built; whether the city holds a sidewalk condition assessment was not found. (inferred comparison)

**Not found elsewhere:** a tornado-hit city giving residents an application-status tracker; an audit stating what share of 311 requests were closed with no work done; an abandoned-vehicle backlog shown to have been eliminated. Not searched: imagery or LiDAR for tree condition, plate-reader detection of abandoned cars, 911 consolidation outcomes.

## Problem list with evidence

One row per problem found in Parts 1–3. URLs, dates and labels for every figure are in the section named in the last column. "City's own evidence" is always **observed** in a city document or CityStat chart unless marked; "311 file" figures are **observed** (this thread's calculation, last 12 months to 12 Oct 2026 unless stated); resident-side figures are **reported** unless marked.

| # | Problem | Who, and roughly how many | City's own evidence | Independent data | Resident-side evidence | Latest evidence | Detail |
|---|---|---|---|---|---|---|---|
| 1 | Tornado home repair has barely started; displaced households | Owners of an estimated 2,674 homes; about 391 people on city-paid leases; "almost 50,000 residents" in the path | 46 of 2,674 repairs complete (2%); 2,438 homes in a phase with 0 complete; mayor: repair "slower than anyone wants" | Tracker file: 2,256 of 2,743 records "Awaiting Prioritization" | Survey: satisfaction 3.6/10; 8 in 10 say slower than expected; Rams survey ranks tornado recovery first | 13 Oct 2026 | 1B, R1, 3.2 |
| 2 | Tornado demolition, debris and stumps unfinished | Neighbors of 1,005–1,205 structures still to demolish; 2,620 stumps | 395 of 1,400–1,600 demolitions; stumps 5%; debris projects 58% | Tracker: 542 of 1,761 complete; 311 file: 368 of 458 tornado-debris requests open, median age 300 days | Demolition dust concerns (reported) | 13 Oct 2026 | 1B, R1, 3.2 |
| 3 | 911 calls answered slowly; police slow on lower-priority calls | All callers; 668,304 calls to the centre in 2025 | Budget: about 300 of 1,100 officer posts vacant; no city-published answer-time measure | None retrieved | 78% answered within 15 s against 90%; 43,200+ waited 40 s or more; lower-priority response 18 → 40+ minutes | 15 Sep 2026 | 1B, R2, 3.2 |
| 4 | Warning sirens and emergency management | All residents | Mayor: "the sirens didn't go off"; audits 2024 and 2026; 22 of 60 sirens non-functional on the day; plan dated 2003 | 311 file: 380 "sirens not heard" reports open | — | 28 Apr 2026 | 1B, R2, 3.2 |
| 5 | Water-main breaks and multi-day outages | All customers; about 400 homes in one January 2026 break | 64.2% of emergency repairs restored within 8 hours against 80%, never met; "crisis mode"; $150M unfunded main replacement | 311 file: "water coming up" 621 → 746 → 932; 368 open, median age 221 days | 399 breaks in 2025, most in seven years; top-ranked use in two surveys | 28 Jul 2026 | 1A, 1B, R3, 3.2 |
| 6 | Water bills: arrears and rising rates | 16,000+ past-due accounts; 4,164 in tornado neighborhoods | $14M+ owed; shut-offs resumed; rates +18%, +18%, then 5–6% a year | — | Reddit thread on the increases (252 / 207) | 25 Aug 2026 | 1B, R3 |
| 7 | Vacant lots and buildings overgrown, unsecured, dumped on | Neighbors of about 24,000 vacant parcels and 9,000 buildings (reported), 84% north of Delmar | First mowing pass reached 58% of lots; vacant-building pass 23% done at 30 June; $2M for a backlog that "exceeded current mowing capacity"; Resolutions 126 and 142 | 311 file: 12,253 requests, 63% from five wards; weeds at vacant buildings +51% year on year | Four TV accounts July–August 2026; 2,300+ nuisance complaints in 2025 | 15 Sep 2026 | 1A, 1B, R4, 3.2 |
| 8 | Hazard trees, tree inspections and stumps | Not quantified per resident; 591 hazard-tree removals outstanding | 37% removed within 30 days against 100%, never above 40%; half of trimmer posts vacant | 311 file: 49% of tree requests cancelled; 2,398 inspections open, 2,012 older than 90 days | Thin: two undated TV stories; low survey priority (3.85/5) | 12 Oct 2026 | 1A, R6, 3.2 |
| 9 | Cave-ins, sinkholes and sidewalks | Not quantified; sidewalk requests are filed as disability issues | All four 2022 sidewalk audit findings unresolved; Rams deck: "Finish backlog" | 311 file: 1,260 cave-ins and 2,612 sidewalk requests open; sidewalk median 88 days | Sinkhole coverage August 2026; I-44 closure June 2026; sidewalks 4.06/5 in survey | 18 Aug 2026 | 1A-bis, 1B, R7 |
| 10 | Major-street potholes and critical signs | Road users | Major-street potholes 44.5% on time against 80%; critical signs 58.9% against 75%; neither ever met | 311 file: pothole volume halved since 2024 | Thin in 2026 | 30 Jun 2026 | 1A, R7 |
| 11 | Derelict vehicles and towing | 8,376 requests a year | "Closed" does not mean towed; four audits unresolved; mayoral priority to "eliminate backlog" | 311 file: median 15 days, 28% on time; 3,006 closed as "vehicle gone upon inspection" | Thin | 24 Sep 2026 | 1A, 1B, R8, 3.2 |
| 12 | The request system: open backlog, closure without work, no status meaning | Everyone who files; 112,859 requests a year | CityStat's own statement on towing; routing is the only CSB target; audit held no response-time data | 311 file: 21,292 open, 9,069 over a year; 23.7% repeats; 14.6% blank outcomes; status-definition page inactive | Mixed and sparse; media contact produced faster fixes (inferred by research agent) | 13 Oct 2026 | 1A, 1A-bis, R14, 3.1 |
| 13 | Refuse collection and illegal dumping | Alley-dumpster households; no count | Coverage 94.2% against 95%; overflowing containers "a problem for years"; recycling contamination | 311 file: missed collections down 44%; dumping reports repeat 49% | Dumping thread; 2025 recycling complaints | 24 Aug 2026 | 1A, R5 |
| 14 | Dangerous driving, expired tags, traffic deaths | Citywide; 90 pedestrian and cyclist deaths 2017–2021 (bill recital) | BB 75: ward discretion "has resulted in disparate outcomes" | — | Gravois: 23 crashes, four deaths in 2025; 90 Reddit posts, about 4,400 comments | 24 Sep 2026 | 1B, R9 |
| 15 | Loose and dangerous dogs | 657 bite calls in 2025 | Budget book: 43% rise in bite-related requests | 311 file: 8,568 animal requests; leash complaints repeat 46% | Largest civic Reddit thread of six months (1,689 / 852) | 25 Jul 2026 | R10 |
| 16 | Evictions, rent burden, unsafe rentals, lead | 34,188 rent-burdened renter households (observed, ACS); 5,685 eviction filings in city tracts in 2025 and 2,932 in January–July 2026, down 15.9% (observed, Eviction Lab file) | HELP-STL: 472 cases opened in 20 months | 311 file: 655 of 838 lead-inspection requests open; interior code complaints +49% since 2024 | Concord Apartments condemnation, 60+ people | 27 Aug 2026 | 1A, R11, 3.2 |
| 17 | Homelessness and shelter capacity | "Nearly 1,800" in the January 2026 count, up 9% | After-action review: tracking "needs better infrastructure"; baseline shelter "Max capacity reached" | — | Lawsuit over an encampment | 9 Oct 2026 | 1B, R12, 3.2 |
| 18 | Jail deaths and oversight | About 790 people held (2026 average daily population) | Oversight board: 29 of 30 complaints pending | — | 22+ deaths since 2020 | 2 Sep 2026 | R13 |
| 19 | Building permits slow | Applicants | 66.6% within 30 days against 80%; falling three quarters | — | None found | 30 Jun 2026 | 1A, 3.2 |
| 20 | City workforce vacancies | All services | Tree trimmers 50%, utility workers 42% vacant; "overworked, underpaid workforce" | — | — | 13 Oct 2026 | 1B |
| 21 | Parks maintenance requests | Park users | 67.5% on time against 80%, never met | — | None found | 30 Jun 2026 | 1A |
| 22 | Public performance data is stale and partial | Public, press, aldermen | CityStat unchanged since 30 June; no downloads; one broken chart; no police, fire, 911, LRA, recovery pages | This thread's own extraction | Survey comments ask for transparency; petition for a recovery spending dashboard | 13 Oct 2026 | 1A, 3.2 |
| 23 | Graffiti | 1,853 requests a year | No city target | 311 file: median 27 days, 40% on time; volume falling | Not found as a current complaint | 12 Oct 2026 | 1A-bis, 3.2 |
| 24 | Outside city service delivery: data-centre siting, school closures, electricity bills, licence-plate cameras | Varies | — | — | Data centres are the largest Reddit civic topic (81 posts, about 4,920 comments) | 11 Oct 2026 | R15 |

## Which problems have the strongest evidence

This section sorts the problems by what evidence exists, using four tests applied the same way to each. It does not weigh which problem matters most; that is in the next section.

Tests: **(a)** a count of affected people or households from a dated source; **(b)** documented harm to safety, housing, health or household money, not only inconvenience; **(c)** a shortfall in the city's own published figure or admission; **(d)** corroboration from data this thread retrieved itself (311 file, tracker files, Census).

| Problem | (a) Count | (b) Harm | (c) City's own shortfall | (d) Own data | Latest dated source other than the 311 file |
|---|---|---|---|---|---|
| 1. Tornado home repair | yes | yes: housing loss | yes: 2% | yes | 13 Oct 2026 |
| 2. Tornado demolition and debris | yes | yes: unsafe structures | yes | yes | 13 Oct 2026 |
| 7. Vacant and overgrown property | yes (parcels, not people) | yes: safety, access | yes | yes | 15 Sep 2026 |
| 5. Water mains and outages | yes | yes: no water for days | yes | yes | 28 Jul 2026 |
| 12. Request backlog and closure | yes (requests) | partly: depends on type | yes | yes | 13 Oct 2026 |
| 8. Hazard trees | no | partly: by definition hazardous; no injury data found | yes: 37% vs 100% | yes | 28 Sep 2026 |
| 9. Cave-ins and sidewalks | no | partly: access, sinkholes | yes: audit | yes | 18 Aug 2026 |
| 3. 911 and police response | yes | yes: emergency delay | no city figure published; reported only | no | 15 Sep 2026 |
| 4. Sirens | yes (all residents) | yes: five tornado deaths; link to siren failure not established here | yes | yes | 28 Apr 2026 |
| 16. Evictions, rentals, lead | yes | yes: housing loss, lead | weak: caseload only | yes (lead requests, ACS, eviction file) | 27 Aug 2026 |
| 17. Homelessness | yes | yes | yes: own review | no | 9 Oct 2026 |
| 11. Derelict vehicles | yes (requests) | no evidence found | yes | yes | 24 Sep 2026 |
| 15. Dogs | yes | yes: bites | weak | yes | 25 Jul 2026 |
| 14. Dangerous driving | yes | yes: deaths | partly: bill recital | no | 24 Sep 2026 |
| 6. Water bills | yes | yes: shut-offs | yes | no | 25 Aug 2026 |
| 10. Potholes and signs | no | no evidence found | yes | yes (falling) | 30 Jun 2026 |
| 13. Refuse and dumping | no | weak | narrowly missed; improving | yes (falling) | 24 Aug 2026 |
| 18. Jail | yes | yes: deaths | yes: oversight backlog | no | 2 Sep 2026 |
| 19. Permits; 21. Parks | no | no evidence found | yes | no | 30 Jun 2026 |
| 23. Graffiti | no | no evidence found | no target | yes (falling) | none found |

**All four tests met:** tornado home repair (1), tornado demolition and debris (2), vacant and overgrown property (7), water mains and outages (5). For each, the city's own figure, this thread's own data and resident accounts point the same way.

**Strongest evidence of harm to residents:** tornado home repair (thousands of households without a repaired home 17 months on; lease support for 391 people ending); 911 answering (43,200+ slow answers in a year); water outages; evictions and rent burden; homelessness; jail deaths. Of these, 911, homelessness and the jail rest mainly on reported figures that this thread did not derive from primary data. Eviction filings were derived from primary data and are falling in 2026.

**Strongest evidence of the city falling short of its own standard:** hazard trees (37% against 100%, never above 40% in ten quarters); tornado repair (2% of need); major-street potholes (44.5% against 80%, never met); critical signs (58.9% against 75%, never met); water-main restoration (64.2% against 80%, never met); vacant-building mowing (first of four rotations 23% done by 30 June); towing (four audits unresolved; closure does not mean a tow); sidewalks (all 2022 audit findings unresolved); sirens.

**Where city figures and resident evidence diverge (observed):**

- Trees, towing, potholes, permits and parks requests show large shortfalls in the city's own numbers but little resident-voiced complaint in the sources reached.
- 911, dogs, dangerous driving and data centres draw heavy resident attention but have no CityStat measure at all.
- Refuse was the mayor's "problem for years"; both the city's figures and the 311 file show it improving in 2026.
- Kickoff topics graffiti, potholes and urban heat have thin resident evidence in the window searched.

## Judgment (kept separate from the evidence)

Everything in this section is this thread's opinion (**inferred**). It ranks and qualifies the evidence above; it proposes nothing.

**How I would rank seriousness, and why**

1. **Tornado home repair.** The largest gap between need and delivery in the file: 2% of 2,674 homes after 17 months, 2,256 households in a waitlist status with no date, and lease support for displaced families winding down. The city's deck, its tracker file and independent reporting agree to within a few units. It is also the most concentrated harm: 89% of repair records are in three wards.
2. **Vacant and overgrown property.** Chronic rather than acute, but it touches the most blocks, and the city's own pages admit it cannot yet say which lots were mowed or why others were missed. The 311 increase in 2026 and the four TV accounts are consistent with the CityStat shortfall.
3. **Water.** Breaks at a seven-year high, a restoration target never met, and steep rate rises arriving while 16,000 accounts are in arrears. Residents ranked it first in both surveys. The constraint the Water Division itself names is capital: $150M of main replacement is listed as unfunded.
4. **The request system itself.** Less visible as a resident complaint, but it is the mechanism through which problems 2, 7, 8, 9, 11 and 13 are reported, and the data show closure is a weak signal of work done. I rate the data evidence strong and the resident-voice evidence only moderate.
5. **911 answering.** Potentially the most severe harm per incident, but the weakest evidence base of the top group: every figure is from journalists' records requests, the city publishes nothing, and the answering point belongs to the state-controlled police.

**Where I think the evidence is weaker than it looks**

- **Trees.** The city's shortfall is the worst of any CityStat measure, yet I found almost no dated resident complaint, and half of tree requests are cancelled for reasons the data do not give. The backlog may partly be an artefact of how Forestry moves requests into its own work-order system. I would not treat the 311 tree numbers as a measure of unmet need without that being explained.
- **Towing.** Large volume and poor on-time figures, but 3,006 of 7,843 closures say the vehicle was already gone, and I found no evidence of harm. This may be a problem the city cares about more than residents do.
- **Reddit.** The forum skews to south-city and central-corridor users. Dogs, data centres and reckless driving dominate there; tornado recovery and vacancy, which fall mainly on north St. Louis, are under-represented. I gave the forum little weight for ranking.
- **311 counts measure willingness to report**, not incidence. Wards 10–14 file the most vacancy requests; it does not follow that other wards have fewer problems of other kinds. The tornado wards may under-report where residents have given up, which the Greater Ville accounts hint at.
- **The surveys are self-selected.** The Rams survey (n=1,394) asked about uses of one pot of money, so it measures spending preference among options offered, not satisfaction with services.

**Things I could not settle**

- Whether CityStat's Q3 2026 update is late or abandoned. The pages have not changed since 30 June.
- Why tree requests are cancelled at 49%.
- The sheltered/unsheltered split of the 2026 point-in-time homelessness count. STLPR presents "nearly 1,800" as the total including people in shelters; Board Bill 91 says "more than 1,700" were unsheltered. The research agent found no source for a 1,700 unsheltered figure; the primary count report was not retrieved (the Continuum of Care site is down).
- Whether the per-lot mowing log promised in August 2026 and the GeoSTL satellite work exist in usable form inside the city.
- Whether the police CAD replacement has gone live.

**On the kickoff topics.** Of the topics named at the kickoff, vacant lots and trees are well supported by the city's own figures; potholes are supported only for major streets; graffiti and urban heat are not supported as resident-voiced problems in anything I reached. That is a statement about the sources reached, not proof that residents do not care.

## Looked for, not found

Negative results are kept in full in each detail file. The main ones:

**City performance data**

- No CityStat figures later than 30 June 2026; no CityStat page for police, fire/EMS, 911, the jail, LRA, demolition, code enforcement, lead, homeless services, tornado recovery or CDA. (observed)
- CityStat towing chart does not render for the public: expired Snowflake token. (observed, three attempts)
- No CSV or table export from CityStat. (observed)
- No city-run resident satisfaction survey. (not found)
- No public 911 answer-time or police response-time figures from the city or SLMPD. (not found)
- The Comptroller's 2024 CSB "Response Time & Operation Review" contains no response-time data. (observed)
- No Missouri State Auditor report on a mayoral service department for 2023–2026. (not found)
- No federal Single Audit for the city for fiscal years 2023–2025 in the Federal Audit Clearinghouse file (see Part 1B, Audits); no HUD, EPA or DOJ monitoring document on the city pages fetched; no link to a CAPER on the Community Development pages. hudoig.gov returned HTTP 403; epa.gov, hud.gov and justice.gov were not queried. (observed by the research agent)
- No hearing transcripts or departmental written testimony; operating-department budget presentations are not in the committee packets. (observed)
- No public tracker for the mayor's 25 strategic initiatives. (not found)
- No Recovery Office progress report dated after June 2026 on the documents page; the only later figures are in the 29 Sep 2026 committee deck and the tracker files. (observed)

**Existing tools**

- No city 311 mobile app, chatbot or AI assistant; no open procurement for a 311 or CRM replacement. (not found)
- No public snow-plough tracker, pavement-condition index, automated pothole detection or networked streetlight outage detection. (not found)
- No per-lot mowing status tool; no vacant-building registry lookup. (not found) A city list of demolitions pending or completed was not found outside the tornado tracker; the city does publish demolition permits issued (see corrections below).
- No public shelter-bed availability view; no city list of impounded animals; no online form for minor crime reports; no public siren-status map. (not found)
- No public dashboard of tornado recovery spending. (not found)
- Vendor behind the tornado application portal; contract documents and values for Cityworks, the permit portal, the trackers and the refuse route system. (not determined)
- Whether the CSB web form accepts photos. (not determined: later steps need a submission)

**Residents**

- KSDK, Fox 2, Missouri Independent, Riverfront Times and most Post-Dispatch pages were blocked or paywalled; X, Facebook and Nextdoor need a login; Reddit comment threads were not readable. (observed)
- 211 request counts for the city alone; a year-on-year eviction filing trend. (not retrieved)
- Any count of residents affected by hazard trees, missed refuse collection or sidewalk defects. (not found)
- Dated 2026 complaint coverage of graffiti, potholes, urban heat, permit delays or streetlight outages. (not found)

**Spot-checks by the lead thread that did not confirm an agent's finding**

- A research agent recorded at 23:27 UTC that the restaurant-inspection lookup's TLS certificate had expired on 5 Aug 2026. At 00:07 UTC the host the city links to (`www.healthspace.com`) presented a certificate valid from 18 Jul 2026 to 1 Feb 2027; only the bare host `healthspace.com` failed. The claim is therefore left out of Part 3. (observed)
- The pothole-map feed (95 open requests, oldest 4 Aug 2026) could not be re-queried by the lead thread: the service path guessed returned 404. The figure stands as observed by the agent only.

**Dead or broken links on city pages (observed 13 Oct 2026)**

- `…/citizens-service-bureau/status-definitions.cfm` → "Inactive Content".
- `cocstl.org` (Continuum of Care) → redirect to a gambling-spam URL.
- "Pay a Water-Refuse Bill" → `payitstlouis.com/auth`, HTTP 404.
- "Mental Health Help" → `bhrstl.com`, certificate error (live site is bhrstl.org).
- Police page "Crime Mapping Data" → `crimereports.com`, expired certificate.
- Open-data catalog → `maps6.stlouis-mo.gov/.../FORESTRY_CATEGORIZATION`, HTTP 500.
- `rdx.stldata.org` (Regional Data Exchange) → no response on four attempts.

## Corrections after agent verification

Changes made to this file after the research agents re-checked their own detail files (2026-10-14 00:03–00:19 UTC):

- **Animal shelter contract.** An earlier draft gave "$112,500 a month for 180 animals", "intake about 350 a month" and "city payment covers about half of intake". The agent's re-fetch found none of these in the cited article; only "the total contract provides about $1 million" is there. The three figures were removed from Part 3.2. (observed by the agent; [STLPR, 21 Jul 2026](https://www.stlpr.org/government-politics-issues/2026-07-21/care-stl-extends-contract-st-louis-money))
- **City demolition data.** An earlier "not found" was wrong: the city publishes a Demolition Permit Data dashboard with a download link. It counts permits issued: 461 (2021), 491, 377, 398, 415 (2025) and 865 so far in 2026. Re-checked by the lead thread at 00:19 UTC. (observed; <https://www.stlouis-mo.gov/data/dashboards/demolition-permits/years.cfm>)
- **Jail population.** Updated from "about 750" to the dashboard's 2026 average of 787. (observed by the agent; <https://www.stlouis-mo.gov/data/dashboards/inmates/index.cfm>)
- **Jail population (second correction).** Part 2 gave "733–774" as a range. The agent clarified that 774 is FY2025 and 733 a three-quarter FY2026 average; Part 2 now says so.
- **Federal audits.** "Not found on the city's site" was replaced by the agent's Federal Audit Clearinghouse result: latest Single Audit on file is FY2022, with a material weakness and material noncompliance; none found for FY2023–2025 (Part 1B, Audits).
- **Board Bill 134 (Vegetation Ordinance)** was read in full by the agent and added to the Board of Aldermen subsection.
- **Checked and already correct here:** "Wait list: 179" belongs to disaster case management; 16 Public Safety Committee agendas were read; two committee packets contain figures.
- **Eviction filings (the largest correction).** Earlier drafts, and the lead thread's first spot-check, carried STLPR's "about 10,400 eviction filings in the city" in 2026. The Eviction Lab file shows that total is city plus county. City tracts alone: 5,685 in 2025; 2,932 in January–July 2026, 15.9% below 2025; 5,130 in the 12 months to July 2026 against the 17,452 quoted. Recomputed by the lead thread at 00:25–00:29 UTC. Part 2 R11, the problem list and the evidence section were changed; the direction changes from unknown to falling.
- **Homicides** added to R15: 151 (2024), 141 (2025), 80 through August 2026 against 96. Reported police counts.
- **Water:** 155 main breaks in January–February 2026 added; the "64%" rate figure explained (simple sum; about 83% compounded; STLPR says about 90%).
- **Kickoff topics** re-tested by dedicated searches: trees thin, graffiti not supported, potholes moderate and seasonal, heat thin. Part 2 text updated.
- **Homelessness:** "nearly 1,800" is the total including sheltered people; no source was found for the 1,700 unsheltered figure in Board Bill 91.
- **Kept as reported and not confirmed** by the resident-voice agent (pages blocked): KSDK's 10-second 911 percentages; Newsweek's winter main-break counts; 23 pedestrian deaths in 2024; the Milentz Avenue and seven-year tree stories. None of these is relied on above except where marked.
- **Two source notes updated (2026-10-14, while building the facts file).** Part 2 R4 (vacant-parcel count down about 4% since 2018) and R7 (I-44 closure) said "search summary"; the resident-voice detail file records both STLPR pages as confirmed at 00:05 UTC, so the links were added. No figure changed.
- **Rows added to Part 3.2** from the agent's final pass: city hiring portal, parks maintenance, the 50/50 sidewalk waiting list, the absence of a city crash dashboard.
