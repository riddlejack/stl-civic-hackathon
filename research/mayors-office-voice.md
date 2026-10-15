# C. What the mayor's office says — City of St. Louis

**Status: complete, 14 October 2026 (UTC).** Facts only; no solutions or project ideas. Labels: **observed** = read
directly on the page by this thread; **reported** = a source says so; **inferred** = this thread's conclusion.

## Summary

**Found**

- **Log** (`research/mayors-office-log.csv`): 2,099 statements from 546 pages; 1,892 since the inauguration
  (15 Apr 2025 – 13 Oct 2026) and 207 from the campaign and transition. It covers all 151 Mayor's Office releases,
  both major speeches, executive orders 81–98, budget summaries, CityStat pages, hearing and press-conference
  captions, and news coverage. 771 rows record a commitment; 2,044 quotes were machine-matched to saved text.
- **Priorities.** The May 2025 tornado is in over half of all documents in mid-2025 and a fifth by Q3 2026.
  Workforce, CityStat and data, water, and trees and vacant lots rise through 2026. The five Strategic Priorities
  and 25 initiatives of 7 Jul 2026 carry no public owner, date or target.
- **Promises.** Dated promises on laws, budgets, pay and appointments were mostly kept, some late. Promises on
  the pace of tornado recovery were mostly missed.
- **Admissions.** The office says much is not working: emergency management, home repair, hiring speed, the 311
  phone system, paving money, tree and mowing backlogs, water finances, old IT and a structural budget gap.
- **Data and AI.** CityStat (public since 31 Mar 2026) is the main accountability tool. No statement by the mayor
  or staff about AI in city operations was found; the one city text is an ITSA policy of 23 Jul 2026.
- **"Ben"** is Col. Ben Jonsson, Chief Operating Officer (inferred, high confidence; section 6.1).

**Not established**

- Unread: Post-Dispatch and Business Journal (paywalled); KSDK, Missouri Independent and Riverfront Times (HTTP
  403 or empty); most social timelines (login walls); 51 saved City videos; the campaign's two plan posts (4 log rows rest on a
  search-engine summary and are marked unverified).
  No mayoral newsletter or op-ed was found.
- Whether many commitments were met (section 2 marks each); who spoke for the City at the kickoff; an
  organisation chart.
- **For Jack to decide:** 30 rows quote Fox 2 articles whose pages returned 403 to curl; a collector read the
  text from the site's public WordPress API instead. They are flagged in `quote_check`; filter `url` on
  `fox2now.com` to drop them.

## Files

Detail and could-not-reach lists: `research/parts/C-*.md` (one per collector). Raw downloads:
`data/raw/mayors-office/`. Rebuild the log: `research/parts/C-scripts/merge_rows.py --write`, then
`theme_counts.py --write`. Every figure in this report, with unit, date, label and URL:
`research/mayors-office-voice-facts.csv` (617 rows; built by `research/parts/C-scripts/facts.py --write`).

## 1. Recurring topics: counts and movement

**How counted.** Collectors wrote topic labels from the material (1,106 distinct labels; kept in the `topics`
column). This thread then grouped them into 25 themes by keyword (`themes` column; rules in
`research/parts/C-scripts/theme_counts.py`; full tables in `research/parts/C-theme-counts.csv`). A row can sit in
several themes. Counts measure what was said in the sources read, so they follow the collection: one outlet
(St. Louis Public Radio) supplies about half the news rows, and the Post-Dispatch is absent. The theme grouping
is **inferred**; the counts are **observed** in the log.

### 1.1 Documents touching each theme, by quarter

Distinct pages (a release, article, hearing or speech counts once), all sources.

| Theme | Campaign (to 14 Apr 2025) | 2025 Q2 | 2025 Q3 | 2025 Q4 | 2026 Q1 | 2026 Q2 | 2026 Q3 | 2026 Q4 (to 13 Oct) | In office |
|---|---|---|---|---|---|---|---|---|---|
| **All documents** | 38 | 71 | 97 | 92 | 70 | 87 | 70 | 22 | 509 |
| Tornado recovery | 0 | 38 | 51 | 30 | 18 | 25 | 14 | 1 | 177 |
| Budget, revenue, ARPA, Rams settlement | 14 | 17 | 20 | 15 | 19 | 42 | 9 | 2 | 124 |
| Streets, potholes, paving, traffic, infrastructure | 13 | 12 | 11 | 13 | 12 | 20 | 12 | 5 | 85 |
| Public safety, police, jail, curfew | 16 | 14 | 12 | 4 | 17 | 22 | 8 | 3 | 80 |
| City workforce: hiring, pay, civil service | 10 | 8 | 7 | 10 | 6 | 23 | 11 | 8 | 73 |
| Permits, building, zoning, planning | 5 | 6 | 10 | 9 | 8 | 14 | 14 | 2 | 63 |
| Economic development, downtown, SLDC | 13 | 3 | 16 | 4 | 8 | 17 | 13 | 1 | 62 |
| Transparency, accountability, trust | 15 | 8 | 15 | 10 | 7 | 7 | 11 | 2 | 60 |
| CityStat, data and performance measures | 4 | 3 | 3 | 6 | 9 | 14 | 18 | 5 | 58 |
| Winter shelter and homelessness | 5 | 1 | 1 | 29 | 14 | 7 | 4 | 1 | 57 |
| Technology and modernisation | 4 | 0 | 8 | 14 | 4 | 18 | 8 | 3 | 55 |
| Housing and neighbourhoods | 11 | 6 | 10 | 10 | 5 | 14 | 7 | 2 | 54 |
| Emergency preparedness and sirens | 2 | 13 | 14 | 13 | 2 | 10 | 1 | 0 | 53 |
| Snow and winter operations | 6 | 0 | 1 | 18 | 13 | 7 | 2 | 0 | 41 |
| City services (general framing) | 17 | 7 | 8 | 7 | 6 | 6 | 4 | 1 | 39 |
| Resident reporting: CSB and 311 | 3 | 3 | 8 | 3 | 7 | 9 | 6 | 2 | 38 |
| Water | 0 | 0 | 6 | 3 | 2 | 17 | 6 | 1 | 35 |
| Refuse, recycling, dumping | 10 | 2 | 6 | 6 | 3 | 9 | 5 | 0 | 31 |
| Trees, mowing, vacant lots | 0 | 0 | 0 | 3 | 2 | 5 | 11 | 3 | 24 |
| Data centers | 0 | 0 | 2 | 1 | 2 | 7 | 9 | 0 | 21 |
| Vacant property and land | 2 | 1 | 1 | 1 | 4 | 4 | 6 | 1 | 18 |
| Transit | 8 | 4 | 7 | 0 | 0 | 1 | 0 | 0 | 12 |

### 1.2 The office's own releases: how many of the 151 mention each term

Counted in the full text of every release on the Mayor's Office news index
(<https://www.stlouis-mo.gov/government/departments/mayor/news/index.cfm>, retrieved 2026-10-13 23:21–23:23 UTC).
Full table: `research/parts/C-term-counts-by-quarter.tsv`. **Observed.**

| Term | 2025 Q2 | Q3 | Q4 | 2026 Q1 | Q2 | Q3 | Q4 | Total |
|---|---|---|---|---|---|---|---|---|
| Releases issued | 12 | 27 | 39 | 26 | 22 | 19 | 6 | 151 |
| tornado | 7 | 18 | 19 | 7 | 5 | 6 | 1 | 63 |
| housing | 2 | 8 | 18 | 7 | 7 | 6 | 1 | 49 |
| shelter / Code Blue | 1 | 1 | 16 | 9 | 4 | 3 | 0 | 34 |
| tree / forestry | 0 | 3 | 5 | 5 | 5 | 3 | 2 | 23 |
| vacant / LRA / land bank | 1 | 4 | 3 | 3 | 8 | 4 | 0 | 23 |
| hiring / pay / employees | 0 | 4 | 4 | 3 | 6 | 3 | 3 | 23 |
| public safety | 1 | 3 | 3 | 4 | 4 | 5 | 3 | 23 |
| water | 1 | 2 | 1 | 1 | 5 | 6 | 2 | 18 |
| downtown | 0 | 1 | 1 | 6 | 5 | 4 | 1 | 18 |
| snow | 1 | 0 | 9 | 5 | 2 | 0 | 0 | 17 |
| refuse / trash / recycling | 1 | 3 | 2 | 3 | 5 | 0 | 0 | 14 |
| street / paving | 1 | 3 | 3 | 1 | 2 | 4 | 0 | 14 |
| permit | 0 | 2 | 2 | 1 | 4 | 3 | 1 | 13 |
| data (not "data center") | 0 | 0 | 1 | 4 | 2 | 4 | 1 | 12 |
| Citizens' Service Bureau / 311 | 0 | 3 | 1 | 1 | 3 | 1 | 0 | 9 |
| towing | 1 | 1 | 1 | 1 | 1 | 3 | 0 | 8 |
| pothole | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 5 |
| CityStat | 0 | 0 | 0 | 1 | 1 | 2 | 0 | 4 |
| AI / artificial intelligence | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 3 |
| mowing / vacant lot | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 2 |
| graffiti | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| illegal dumping | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### 1.3 Movement over time (inferred from the two tables)

- **Tornado recovery crowds out the rest, then recedes.** It is in 54% of documents in 2025 Q2 (38 of 71), 53% in
  Q3, 33% in Q4 and 20% in 2026 Q3 (14 of 70). It was no part of the campaign.
- **Seasonal pulses.** Winter shelter (29 documents) and snow (18) in 2025 Q4; sirens and emergency management in
  every 2025 quarter and again at the anniversary and storm season in 2026 Q2 (10).
- **Rising through 2026.** CityStat and data: 3 documents a quarter in 2025, 18 in 2026 Q3 (26% of that quarter).
  City workforce: 6–10 a quarter, then 23 in 2026 Q2 and 8 in the first two weeks of Q4 (the civil-service
  package). Water: 17 in 2026 Q2 (rate rise, sinkhole). Trees, mowing and vacant lots: none before 2025 Q4, 11 in
  2026 Q3. Data centers: 7 and 9 in 2026 Q2–Q3.
- **Budget and Rams settlement peak in 2026 Q2** (42 documents): the police-budget dispute, FY2027 budget and the
  Rams bill.
- **Falling.** Transit: 8 campaign documents, 4 and 7 in the first two quarters in office (the bus rapid transit
  decision), then one. General
  "city services" framing: 17 campaign documents, 4–8 a quarter in office, as the talk moves to named services.
- **The campaign's mix was different.** Before inauguration the leading themes were city services (17 of 38
  documents), public safety (16), transparency (15), Rams and budget (14), economic development (13), streets (13),
  housing (11), refuse (10) and workforce (10).
- **What the office's own releases rarely name.** Graffiti and illegal dumping appear in none of the 151 releases;
  potholes in 5; mowing or vacant lots in 2; CityStat in 4; AI in 3, all about job training (**observed**). These
  subjects do come up when officials are questioned: illegal dumping "has plagued our city for years" (Spencer,
  13 Aug 2025, [KMOV](https://www.firstalert4.com/2025/08/13/residents-businesses-city-officials-frustrated-by-illegal-dumping-st-louis/));
  graffiti crews, stumps, hazardous trees and mowing at the May and September 2026 hearings (section 3).

### 1.4 The named priority lists, in order of appearance (observed)

| Date | Where | The list |
|---|---|---|
| Jan–Mar 2025 | Campaign platform, eight then nine planks ([Wayback, 22 Mar 2025](https://web.archive.org/web/20250322051034/https://caraspencer.com/platform)) | Trust and Transparency; A Safer City; Quality Education; A Thriving Business Environment; Basic City Services (fifth); City Justice Center; Unhoused Population; Downtown; Transit |
| 11 Apr 2025 | Transition "Change agenda" ([Wayback](https://web.archive.org/web/20250411080000/https://www.changeforstl.com/)) | High-Quality City Services (first); Economic Transformation; Inclusive Growth; Public Safety & Justice |
| 15 Apr 2025 | [Inaugural address](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/inaugural-address.cfm) | "Openness and accountability."; "Service Delivery."; "Public Safety"; "Inclusive economy" |
| 15 Aug 2025 | [Office restructure release](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-office-restructure.cfm) | High-quality services; economic transformation; inclusive growth; public safety and justice; tornado recovery |
| Apr 2026 (undated page) | ["50 Key Accomplishments"](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/spencer-accomplishments.cfm) | Tornado Recovery (10 items); High-Quality City Services (13); Transparency & Good Governance (9); Inclusive Growth & Economic Transformation (10); Public Safety & Justice (8) |
| 17 Apr 2026 | [State of the City](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/2026-sotc-address.cfm) | Strengthen neighbourhoods; rebuild trust in City services; customer-first and collaboration; accelerate economic development; modernise City government |
| 7 Jul 2026 | [Strategic Priorities](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-strategic-priorities.cfm), 25 initiatives | "Rebuild Trust in City Services"; "Recover & Revitalize Neighborhoods"; "Accelerate Economic Development"; "Cultivate a Culture of Excellence"; "Modernize City Government" |

Public safety is a named priority in every list to April 2026 and is not a heading in July 2026, where it appears
only inside the downtown initiative (**observed**). The July release says the 25 initiatives are tracked "weekly
in cabinet meetings" in an "internal task management system" and gives no deadline, owner or numeric target for
any of them (**observed absence**). The 25 are listed in `research/parts/C-notes-releases-4.md`.

## 2. Commitments and deadlines, and what is publicly known about each

The log marks 771 rows as commitments; `commitment_detail` holds the wording. This section covers those with a
date, a number or a named deliverable. "Status" is what this thread found in the sources read; "no follow-up
found" is not evidence that nothing happened. Fuller lists: `C-notes-releases-1..4.md`, `C-news-2025.md`,
`C-news-2026.md`, `C-other-channels.md` (section g), `C-campaign.md` (section b).

### 2.1 Kept, on the evidence found

| Commitment | Made | Status |
|---|---|---|
| Report on the siren failure by 20 May 2025 | Spencer, 18 May 2025 ([STLPR](https://www.stlpr.org/health-science-environment/2025-05-18/latest-numbers-friday-tornado-st-louis)) | **Observed:** documents and audio released 20 May ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/mayor-cara-spencer-places-cema-commissioner-on-leave-releases-documents-and-audio-regarding-siren-failure.cfm)) |
| Publish the external investigation of the tornado response | Spencer and Hawes, 10 Jul 2025 ([St. Louis Magazine](https://www.stlmag.com/news/tornado-sirens-probe-spencer/)) | **Observed:** published 18 Aug 2025 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/tornado-report.cfm)) |
| Siren activation automated "within a year" | Spencer, 20 May 2025 ([STLPR](https://www.stlpr.org/health-science-environment/2025-05-20/spencer-says-20m-in-arpa-funds-may-be-used-for-st-louis-tornado-recovery)) | **Reported:** automated on National Weather Service alerts by Nov 2025 ([St. Louis Magazine](https://www.stlmag.com/news/tornado-sirens-dont-work/)) |
| Recycling drop-off sites up 50% in 90 days (25 sites) | City, 15 Aug 2025 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/alley-recycling-ended.cfm)) | **Reported:** 44 sites by 29 Oct 2025 ([St. Louis Magazine](https://www.stlmag.com/news/stlouis-recycling-drop-sites-results/)) |
| Permanent emergency management commissioner | City, 20 May 2025 (release above) | **Observed:** Gregg Favre named 17 Nov 2025 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/favre-cema-commissioner.cfm)) |
| Data-center zoning framework within five months | Executive Order 92, 19 Sep 2025 ([order](https://www.stlouis-mo.gov/government/departments/mayor/documents/executive-orders/mayor-executive-order-no-92.cfm)) | **Observed:** report 5 Feb 2026, "that deadline has been met" ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/data-center-regulations-report.cfm)); ordinance signed 17 Sep 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/mayor-signs-board-bill-49.cfm)). The water-rate framework in the same order was not checked |
| Building permit applications online | Spencer, 13 Oct 2025 ([St. Louis Magazine](https://www.stlmag.com/news/spencer-st-louis-yes-to-development/)) | **Observed:** portal announced 5 Mar 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/new-online-building-permit.cfm)). CityStat later calls permit timeliness "lagging" (section 5.2) |
| CityStat to add mowing and towing data "next quarter" | City, 31 Mar 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-launch.cfm)) | **Observed:** added 1 Jul 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-q2.cfm)) |
| FY2027 budget on the normal schedule despite the police-board lawsuit | Spencer, 9 Apr 2026 ([KMOV](https://www.firstalert4.com/2026/04/09/st-louis-city-files-lawsuit-against-board-police-commissioners/)) | **Reported:** $1.4B budget passed 26 Jun 2026 ([STLPR](https://www.stlpr.org/government-politics-issues/2026-06-26/st-louis-police-get-less-than-they-asked-for-in-citys-1-4b-budget)) |
| Rams settlement bill introduced in May 2026 | Spencer, 17 Apr 2026 ([speech](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/2026-sotc-address.cfm)) | **Observed:** $230M bill announced 14 May ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/rams-bill-friday.cfm)); signed 13 Jul ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/rams-bill-signed.cfm)). **Reported:** passed at $255M ([STLPR](https://www.stlpr.org/government-politics-issues/2026-07-02/after-nearly-4-years-and-a-tornado-st-louis-passes-plan-to-spend-255m-rams-settlement)) |
| At least a 3% raise and a $1,000 payment | Spencer, 17 Apr 2026 (speech above) | **Reported:** pay bill signed 11 Jun 2026 ([STLPR](https://www.stlpr.org/government-politics-issues/2026-06-11/spencer-signs-pay-boost-for-city-workers-and-new-direction-for-st-louis-transportation)). Payment date not checked |
| Water plan with rate increases "very soon" | Spencer, 17 Apr 2026 (speech above) | **Reported:** about 90% over six years passed 18 Jun 2026; first 18% step 1 Jul ([STLPR](https://www.stlpr.org/news-briefs/2026-06-18/st-louis-aldermen-ok-90-water-rate-increase)) |
| Fund Code Blue winter shelter for 2026–27 | Spencer, 20 Apr 2026 ([St. Louis Magazine](https://www.stlmag.com/news/code-blue-success-funding/)) | **Observed:** $2M in the FY2027 budget; request for proposals 14 Jul 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/funding-opportunity-to-support-unhoused-in-winter-2026-2027.cfm)) |
| Keep the earnings tax | Campaign debate, 14 Mar 2025 ([Spectrum](https://spectrumlocalnews.com/mo/st-louis/news/2025/03/14/mayor-tishaura-jones-cara-spencer-mayoral-debate)) | **Observed (city's account):** renewal "passed with a massive 85% support" (speech above) |

### 2.2 Kept late, changed, or partly kept

| Commitment | Made | Status |
|---|---|---|
| New pay plan in force 1 Feb 2026 | City, 4 Nov 2025 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/personnel-cc-study-released.cfm)) | **Observed:** moved to "by March" on 29 Jan 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/employee-compensation-plan-timeline.cfm)); implemented 1 Jul 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-strategic-priorities.cfm)). Five months late (**inferred**) |
| Rams relief money flowing in about two weeks | Spencer, 17 Jun 2025 ([STLPR](https://www.stlpr.org/news-briefs/2025-06-17/st-louis-aldermen-waste-no-time-in-approving-30m-in-rams-money-for-tornado-relief)) | **Reported:** $23M allocated, $4M spent by 30 Oct 2025 ([STLPR](https://www.stlpr.org/government-politics-issues/2025-10-30/st-louis-14m-winter-sheltering-tornado)) |
| Safe housing for tornado-affected residents "by winter" | Spencer and Nicks, 4 Sep 2025 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/rams-funds-housing-debris.cfm)) | **Observed:** $13.7M winter package signed 14 Nov ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-signs-board-bills-housing-winter-shelter.cfm)). **Reported:** tenant aid had accepted no applications by 20 Nov ([St. Louis American](https://www.stlamerican.com/news/local-news/as-winter-approaches-questions-mount-over-citys-tornado-response/)); Spencer on 11 Dec: "we are not doing nearly enough" ([STLPR](https://www.stlpr.org/government-politics-issues/2025-12-11/st-louis-help-tornado-affected-residents-shelter-winter)) |
| Every siren working | 90% restored, 24 Jul 2025 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/100-days.cfm)); full modernisation "next month", 17 Apr 2026 (speech above) | **Reported:** 10 of 60 silent in the 3 Nov 2025 test ([St. Louis Magazine](https://www.stlmag.com/news/tornado-sirens-dont-work/)); three out on 2 Apr 2026 ([KMOV](https://www.firstalert4.com/2026/04/03/st-louis-city-outlines-updates-severe-weather-preparedness/)); an unplanned sounding on 4 May 2026 traced to vendor software ([hearing, auto-caption](https://www.youtube.com/watch?v=9lsGp9Wy4yw)). Completion of the modernisation: no confirmation found |
| GPS on snowploughs, location shared with the public | Spencer, 11 Dec 2025 ([St. Louis Magazine](https://www.stlmag.com/news/cara-spencer-winter-weather-snow/)) | **Observed (city's account):** GPS tracking used "for real-time monitoring and quality control" (speech above). Public sharing: not found |
| Rams money: "a large chunk" for downtown ($98M in her own earlier bill, reported) | Campaign, 17 Feb 2025 ([transcript](https://www.stlmag.com/news/transcript-citizens-agenda-cara-spencer/)) | **Observed:** $55M for downtown in the signed law; the largest share went to tornado recovery and north St. Louis (releases above) |
| A CityStat-type programme and "a true accountability of citizen service requests" | Campaign, 17 Feb 2025 (transcript above) | **Observed:** CityStat public 31 Mar 2026; it reports routing time and on-time rates by service, and average response by ward (section 5). Per-request completion times for residents: see 5.4 |
| Chief Economic Development Officer | "has yet to be appointed", 15 Aug 2025 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-office-restructure.cfm)) | **Observed:** Stephen Davis started 1 Jun 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/stephen-davis-economic-development.cfm)) |

### 2.3 Missed or slipping

| Commitment | Made | Status |
|---|---|---|
| Private-property debris removal starts the week of 14 Jul 2025 | Spencer, 10 Jul 2025 ([STLPR](https://www.stlpr.org/government-politics-issues/2025-07-10/st-louis-rams-money-tornado-repairs-meals-rent)) | **Reported:** moved to late August, then November, then 2026 ([KMOV, 6 Nov 2025](https://www.firstalert4.com/2025/11/06/private-property-debris-clean-up-st-louis-tornado-stricken-areas-pushed-2026)). **Observed:** FEMA/SEMA demolition began 14 May 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/city-state-begin-fema-sema-demolition.cfm)) |
| Home repairs at 40 a month, then 100 | Spencer and Nicks, Jan 2026 (**reported** by [STLPR, 17 Feb 2026](https://www.stlpr.org/government-politics-issues/2026-02-17/st-louis-program-tornado-damaged-homes-broke)) | **Reported:** 34 of 200 prioritised homes by 10 Aug ([STLPR](https://www.stlpr.org/government-politics-issues/2026-08-10/st-louis-disaster-recovery-team-bottlenecks-home-repair-program)); about 2% of an estimated 2,674 by 1 Oct 2026 ([STLPR](https://www.stlpr.org/government-politics-issues/2026-10-01/tornado-recovery-chief-warns-housing-crisis-north-st-louis-recovery)) |
| City-run demolitions finished within five months (about Aug 2026) | Nicks, 17 Mar 2026 ([STLPR](https://www.stlpr.org/health-science-environment/2026-03-20/st-louis-demolished-2-tornado-damaged-homes)) | **Reported:** 1,000–1,200 demolitions still needed overall on 1 Oct 2026 (STLPR above). The city-run subset alone: not established |
| Third-party air monitoring at demolition sites "within weeks" | Nicks, 17 Mar 2026 (STLPR above) | **Observed:** still "actively developing partnerships" on 11 May 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/tornado-demolition-work.cfm)). Nothing later found |
| Hiring in 45 days, application to start | Light, 27 Mar 2026 ([St. Louis Magazine](https://www.stlmag.com/news/bright-light-st-louis-personnel-director/)) | Series as stated: 111 days (Feb 2025), 70 (Aug 2025), 51 (Mar 2026) (same article, **reported**); 46 (May 2026, [hearing](https://www.youtube.com/watch?v=MgQu7EC0oow)); 54 on 13 Oct 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/legislation-to-modernize-stl-civil-service-system.cfm)). The figures do not form one consistent series (**inferred**) |
| Rail quiet zones restored in "a couple of months" | Jonsson, 17 Sep 2026 ([STLPR](https://www.stlpr.org/government-politics-issues/2026-09-17/st-louis-train-horn-federal-upgrades)) | **Reported:** now December 2026 ([KMOV, 8 Oct](https://www.firstalert4.com/2026/10/08/st-louis-city-rushes-restore-railroad-crossing-quiet-zones/)) |
| The "pothole transformation I promised" | Campaign | **Observed:** the mayor says it is "not yet" delivered (speech above); major-street potholes still below the 80% target in Q2 2026 ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-q2.cfm)) |
| Per-lot mowing records "in the next couple of weeks" | Alex Price, 14 Aug 2026 ([KMOV](https://www.firstalert4.com/2026/08/14/cut-down-unmowed-vacant-lots-st-louis-city-looks-data-north-city-resident-discusses-wait/)) | No follow-up found by 13 Oct 2026 |
| CityStat updated every quarter | City, 31 Mar 2026 (release above) | **Observed:** Q2 update on 1 Jul 2026; on 13 Oct 2026 the pages still say data "was last updated June 30th, 2026" ([CityStat](https://www.stlouis-mo.gov/citystat/)). No Q3 update seen two weeks after quarter end |

### 2.4 Open, with a date still ahead (all observed on the source linked)

| Due | Commitment | Source |
|---|---|---|
| 19 Oct 2026 | New Building Commissioner starts. **Reported:** she plans to review permitting data first ([KMOV](https://www.firstalert4.com/2026/10/01/st-louis-city-announces-appointment-next-building-commissioner/)) | [release](https://www.stlouis-mo.gov/government/departments/public-safety/news/mangapora-building-appointment.cfm) |
| 1 Nov and 31 Dec 2026 | Final ARPA invoices; all ARPA spent ($35,593,802 left to process on 6 Oct) | [release](https://www.stlouis-mo.gov/government/departments/mayor/news/arpa-performance-deadline-final-invoices.cfm) |
| "planned for 2026" | CSB improvement work (training, documentation); Bloomberg Harvard recommendations "in the coming months" | [release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-launch.cfm); [press conference](https://www.youtube.com/watch?v=a1H60btjS2E) |
| Late fall 2026 | Registered neighbourhood organisations programme | [hearing, 12 May 2026](https://www.youtube.com/watch?v=tyS2V5Ae98I) |
| End of 2026 | Arterial resurfacing complete; about $25M general obligation bond | [FY2027 budget summary](https://www.stlouis-mo.gov/government/departments/budget/documents/upload/2-FY2027-AOP-Executive-Summary-and-Overview.pdf) |
| Sep–Dec 2026 (inferred from "12-15 months") | New bus rapid transit alignment for the Green Line corridor | [release, 26 Sep 2025](https://www.stlouis-mo.gov/government/departments/mayor/news/bi-state-begins-exploration-of-bus-rapid-transit-in-green-line-transit-corridor.cfm). No later release on it |
| January 2027 | Six infrastructure metrics and the first Rams spending report (hazardous trees and stumps removed "citywide and by ward", miles repaved, sidewalk sections) | [hearing, 30 Sep 2026](https://www.youtube.com/watch?v=ltJWr1X9UTc) |
| "this next year" (to Apr 2027) | "clear key performance indicators for every department" | [State of the City](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/2026-sotc-address.cfm) |
| 6 Apr 2027 | Proposition HR charter amendment on the ballot; hiring target 45 days | [release](https://www.stlouis-mo.gov/government/departments/mayor/news/legislation-to-modernize-stl-civil-service-system.cfm) |
| FY2027 (to 30 Jun 2027) | Cityworks moved to the cloud; mainframe switched off; Building Division off its 1989 system; three data-analyst posts in ITSA | hearings of [11 May](https://www.youtube.com/watch?v=2MX-2honIkI) and [7 May 2026](https://www.youtube.com/watch?v=34oJcMY-UtM) |
| 2027 | New zoning code adopted (18 months from Aug 2025 at first) | [Aug 2025](https://www.stlouis-mo.gov/government/departments/mayor/news/zoning-public-participation.cfm); [Jun 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/zoning-upgrade-workshops.cfm) |
| 2028 | Fixes funded at the ten highest crash-risk locations; digital sidewalk map and asset dashboard (no date) | [Executive Order 96](https://www.stlouis-mo.gov/government/departments/mayor/documents/executive-orders/mayor-executive-order-no-96.cfm) |

### 2.5 Made, with no follow-up found

- Emergency Operations Plan (dated 2003) updated in 2026; emergency planners hired
  ([release, 2 Apr 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/severe-weather-prep-following-may-2025.cfm)).
  The July 2026 priorities still list it as to do.
- Winter plans made public by 15 Dec 2025 and a post-action review by 31 Mar 2026
  ([Executive Order 93](https://www.stlouis-mo.gov/government/departments/mayor/documents/executive-orders/mayor-executive-order-no-93.cfm)).
  A Code Blue review was published 30 Jul 2026
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/code-blue-after-action-2025-6.cfm));
  the 15 Dec publication was not checked.
- Refuse billing audit within three months; full alley-collection replacement plan within a year (Jonsson,
  14 Aug 2025, [STLPR](https://www.stlpr.org/government-politics-issues/2025-08-14/st-louis-ends-alley-recycling-refuse)).
- Community salt bank pilot ([release, 23 Oct 2025](https://www.stlouis-mo.gov/government/departments/mayor/news/snow-plan-update.cfm)).
- Winter Shelter Fund of $250,000 ([release, 18 Dec 2025](https://www.stlouis-mo.gov/government/departments/mayor/news/winter-shelter-fund.cfm)).
- $2.5M spent "immediately" on trees, stumps and sidewalks in north St. Louis
  ([release, 13 Jul 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/rams-bill-signed.cfm)).
  At the 30 Sep 2026 hearing Jonsson said a $500,000 tree inventory contract was approved in August
  ([hearing](https://www.youtube.com/watch?v=ltJWr1X9UTc)); the $2.5M itself was not followed up.
- Regular public reporting on service requests and turnaround; "a lot of work to do on that" (Spencer, 24 Jul 2025,
  [Spectrum](https://spectrumlocalnews.com/mo/st-louis/news/2025/07/24/st--louis-mayor-cara-spencer-s-first-100-days)).
- Mutual-aid agreements for public works: "continued strengthening" on 2 Apr 2026 (release above); none announced.
- Campaign promises with nothing found in the city releases (**reported** in `C-campaign.md`): an appointee
  working only on education; 911 overflow contracts; monitors on refuse trucks with published tracking data;
  trash-fee audits; collection of building-code fines; an SLDC bylaw change; how the Open Door Policy operates;
  a resident-satisfaction measure ("We will use data to better understand citizens' satisfaction", inaugural).
  **Reported:** new refuse trucks carry route tablets ([KMOV, 8 May 2026](https://www.firstalert4.com/2026/05/08/city-rolls-out-new-trash-trucks-keep-routes-track/)).

## 3. Problems the office itself says are unsolved

Each line is the office's own statement. Quotes are verbatim and under 15 words. Hearing and press-conference
quotes come from YouTube auto-captions, checked against the caption file, not the audio. Longer lists:
`C-news-2025.md` (a), `C-news-2026.md` (a), `C-other-channels.md` (f), `C-notes-releases-1..4.md` (a).

**Resident reporting (311 and the Citizens' Service Bureau)**

- 12 May 2026, Acting Director of Neighborhood Stabilization (captioned "Erin Clifford"; the City's 10 Mar 2026
  release names Karen Clifford): callers say of the 311 line "it hangs up on me or it doesn't understand what I'm
  saying"; the bureau took "over 120,000 service requests last year"; Cityworks "may not always get the service
  requests done"; the aim is to "go from a reactive um department to a proactive" one that tells residents a
  request's status before they call ([hearing](https://www.youtube.com/watch?v=tyS2V5Ae98I)).
- 31 Mar and 2 Apr 2026, Spencer: the City was missing its goal of routing 95% of requests to the right
  department in 2.5 days (93.5% in Q1 2026, [release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-launch.cfm)).
  CityStat shows 99.9% for Q2 2026 (section 5.2). Routing is not completion.
- CityStat: average response differs by ward, 35.1 days in Ward 10 against 17.2 in Ward 1
  ([CityStat CSB](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/public-safety/csb.cfm)).

**Trees, stumps, mowing and vacant lots**

- 30 Sep 2026, Parks Director Hayes: "7,000 stumps in the hopper so to speak and about 3,000 hazardous trees"
  ([hearing](https://www.youtube.com/watch?v=ltJWr1X9UTc)).
- 6 May 2026, Forestry Commissioner: "we have all this data but we don't have somebody on staff"
  ([hearing](https://www.youtube.com/watch?v=9lsGp9Wy4yw)).
- 31 Mar 2026: 39.2% of validated hazardous trees removed within 30 days against a target of all
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-launch.cfm)).
- 21 Jul 2026, Spencer (**reported**): the City does a poor job maintaining and mowing vacant parcels
  ([STLPR](https://www.stlpr.org/government-politics-issues/2026-07-22/can-st-louis-mimic-detroit-renaissance)).
- 14 Aug 2026, Alex Price (**reported**): wards 10–14 show about 60% vacant-lot clearance and the City does not
  yet know what the figure means; Forestry has about 60% of its seasonal mowing staff
  ([KMOV](https://www.firstalert4.com/2026/08/14/cut-down-unmowed-vacant-lots-st-louis-city-looks-data-north-city-resident-discusses-wait/)).
- 25 Aug 2026, land bank spokesperson (**reported**): clearing overgrowth from a land-bank building falls in no
  department's scope ([KMOV](https://www.firstalert4.com/2026/08/25/i-want-our-street-back-overgrown-lots-frustrating-south-city-residents/)).
- 30 Sep 2026, Nicks: demolished lots are "right now they're just more grass that's not being cut"
  ([hearing](https://www.youtube.com/watch?v=ltJWr1X9UTc)).
- Graffiti: the Brightside crew is four workers and a foreman and works only above 35°F (6 May 2026,
  [hearing](https://www.youtube.com/watch?v=9lsGp9Wy4yw)). No statement that graffiti is a problem was found.

**Streets, potholes and assets**

- 17 Apr 2026, Spencer: "not yet the pothole transformation I promised you when I ran"; "I made the decision to
  deprioritize potholes" ([speech](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/2026-sotc-address.cfm)).
- 13 May 2026, Streets Commissioner Flake: "the last 10 years, we've been averaging probably $2 million a year in
  paving" against a stated need of $12–15M; Director Jackson: "Right now we're behind the curve"; 129 vacancies
  ([hearing](https://www.youtube.com/watch?v=2erY12agBgU)).
- 30 Sep 2026, Jonsson: "right now we don't have a comprehensive asset management program"
  ([hearing](https://www.youtube.com/watch?v=ltJWr1X9UTc)).
- 3 Mar 2026, Streets (**reported**): five inspectors cover a 12-person abandoned-vehicle workload
  ([KSDK via syndication](https://www.azfamily.com/2026/03/03/car-parked-same-spot-since-april-has-gathered-8660-tickets/)).
- 12 Oct 2026, Street Department: summer paving "left fewer resources for potholes"
  ([Facebook, truncated post](https://www.facebook.com/CityofStLouis/)).

**Refuse and dumping**

- 15 Aug 2025: "the City has struggled to run some of its recycling and trash routes"; refuse costs $28M against
  $16.5M in fees ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/alley-recycling-ended.cfm)).
- 13 Aug 2025, Spencer: illegal dumping "has plagued our city for years"
  ([KMOV](https://www.firstalert4.com/2025/08/13/residents-businesses-city-officials-frustrated-by-illegal-dumping-st-louis/)).
- 13 May 2026, Jackson: refuse routes have been "created and maintained manually"
  ([hearing](https://www.youtube.com/watch?v=2erY12agBgU)). FY2027 budget: $200,000 added for illegal tire dumping
  ([budget summary](https://www.stlouis-mo.gov/government/departments/budget/documents/upload/2-FY2027-AOP-Executive-Summary-and-Overview.pdf)).

**Tornado recovery**

- 1 Oct 2026, Nicks and Brinkmann (**reported**): about 2% of 2,674 estimated repairs done; 1,000–1,200
  demolitions still needed; rental payments end in November
  ([STLPR](https://www.stlpr.org/government-politics-issues/2026-10-01/tornado-recovery-chief-warns-housing-crisis-north-st-louis-recovery)).
- 17 Apr 2026, Spencer: "this will take years, maybe decades. Not months."; "the City cannot fix or rebuild every
  home" ([speech](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/2026-sotc-address.cfm)).
- 20 Jan 2026, Nicks: "The delivery of services has not started in scale"
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/private-property-assistance-deadline.cfm)).
- 15 Aug 2025, Spencer: "we don't have the local expertise or the manpower within city government to lead"
  debris removal ([STLPR](https://www.stlpr.org/news-briefs/2025-08-15/st-louis-plan-b-debris-removal-army-corps)).
- 29 Jan 2026, Nicks: owner contact details in FEMA and City databases are often wrong
  ([press update](https://www.youtube.com/watch?v=81uUs9xO1LA)).
- 30 Sep 2026, Nicks: 75–80% of buildings being demolished were already vacant or condemned; "a city failure to
  address vacancy at scale in the past" ([hearing](https://www.youtube.com/watch?v=ltJWr1X9UTc)).

**Emergency management**

- 18 Aug 2025, Spencer: "our City was ill-equipped to handle the immediate aftermath of the May 16 tornado"
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/tornado-report.cfm)).
- 2 Apr 2026: the Emergency Operations Plan dates from 2003; key posts unfilled
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/severe-weather-prep-following-may-2025.cfm)).
  **Reported:** Favre says there is no active emergency operations plan
  ([KMOV](https://www.firstalert4.com/2026/04/03/st-louis-city-outlines-updates-severe-weather-preparedness/)).

**Workforce and hiring**

- 4 Nov 2025: vacancy of 42% among utility workers, 50% among tree trimmers, 20% among heavy equipment operators
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/personnel-cc-study-released.cfm)).
- 17 Apr 2026, Spencer: "We are operating with limited funds and an overworked, underpaid workforce." (speech above).
- 14 May 2026, Light: "The last few years have been rough and we have lost some trust"; 65% of 150 summer
  utility-worker applicants failed the drug test ([hearing](https://www.youtube.com/watch?v=MgQu7EC0oow)).
- 7 May 2026, Building Division: 62 vacancies, "being down 30 plus inspectors doesn't feel good"
  ([hearing](https://www.youtube.com/watch?v=34oJcMY-UtM)). 11 May 2026, Water: trades posts 46% vacant
  ([hearing](https://www.youtube.com/watch?v=2MX-2honIkI)).
- 13 Oct 2026: "From application to start date takes an average of 54 days."
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/legislation-to-modernize-stl-civil-service-system.cfm)).
  Jonsson (**reported**): staff submissions describe Corrections officers without working radios
  ([St. Louis Magazine](https://www.stlmag.com/news/voice-of-the-workforce-city-hall/)).

**Technology, data and internal coordination**

- 17 Apr 2026, Spencer: "abysmal turnover, antiquated technology, and a crippling lack of trust"; "we should have
  had building permits online already" (speech above).
- 7 May 2026, Building Division: until February 2026 permits ran on "a 1989 black screen with green text"
  ([hearing](https://www.youtube.com/watch?v=34oJcMY-UtM)).
- 22 Dec 2025, Jonsson (**reported**): no coordination system existed before the City adopted a project tool;
  "It was astonishing to us" ([St. Louis Magazine](https://www.stlmag.com/news/colonels-stlouis-city-hall-spencer/)).
- 30 Jul 2026: "the system needs better infrastructure for data keeping and tracking of shelter residents"
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/code-blue-after-action-2025-6.cfm)).
- 7 Oct 2026, Jonsson (**reported**): 18 years of unfiled quiet-zone paperwork; other inherited gaps may exist
  ([KMOV](https://www.firstalert4.com/2026/10/08/st-louis-city-rushes-restore-railroad-crossing-quiet-zones/)).

**Water**

- 17 Apr 2026, Spencer: "The City and our Water Division are in crisis mode." (speech above).
- 1 Jul 2026: 64.2% of main breaks restored in eight hours against an 80% target
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-q2.cfm)).
- 3 Jun 2026, Water Division (**reported**): reserves last only to the end of July
  ([KMOV](https://www.firstalert4.com/2026/06/03/limited-road-left-st-louis-water-division-budget-department-seeks-water-rate-increase/)).

**Money**

- FY2027 budget: "a persistent structural imbalance remains", with gaps of $9.5M (FY2028) to $17.4M (FY2032)
  ([budget summary](https://www.stlouis-mo.gov/government/departments/budget/documents/upload/2-FY2027-AOP-Executive-Summary-and-Overview.pdf)).
- 9 Apr 2026, Spencer on the police board's budget: "a cost that the City cannot cover without resorting to
  layoffs and severe cuts" ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/lawsuit-filed-to-challenge-state-takeover-law.cfm)).
- 8 Oct 2026, Spencer: "55% of the ARPA funds were not spent and we had 18 months left"
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/arpa-performance-deadline-final-invoices.cfm)).

**Homelessness, vacancy and population**

- 22 May 2026, Pearson (**reported**): homelessness is a crisis the City lacks resources for
  ([STLPR](https://www.stlpr.org/news-briefs/2026-05-22/homelessness-continues-to-grow-st-louis-local-leaders-calling-it-crisis)).
  8 Oct 2026, Spencer (**reported**): not enough resources to clear every encampment
  ([STLPR](https://www.stlpr.org/government-politics-issues/2026-10-09/st-louis-looks-to-disband-high-risk-tent-encampments-by-providing-holistic-resources)).
- 1 Oct 2026, incoming Building Commissioner Mangapora (**reported**): vacancy is a systemic, citywide problem
  ([KMOV](https://www.firstalert4.com/2026/10/01/st-louis-city-announces-appointment-next-building-commissioner/)).
- 5 Mar 2026, Spencer: "To end 70 years of population decline"
  ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/new-online-building-permit.cfm)).

The log flags 211 rows as admissions in news, hearings and data pages (`themes` and `topics` columns; release rows
were not flagged, so their admissions are listed in the notes files).

## 4. What a success looks like to them

Drawn from what the releases, speeches and the "50 Key Accomplishments" page announce and how they word it. The
grouping is **inferred**; each example is **observed** on the page linked.

| Kind of win | How it is worded | Example |
|---|---|---|
| A before-and-after number on a basic service | percent on time, days to respond, "without additional cost" | Refuse route completion 50–65% to over 90%; pothole requests on time 17% to 46%; snow and ice response 17.4 days to 3.1 ([CityStat launch](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-launch.cfm)) |
| Speed | "In Just Four Weeks"; "back in three days, whereas before it would take weeks" | [one-month review](https://www.stlouis-mo.gov/government/departments/mayor/news/stl-recovers-one-month-in-review.cfm); [permit portal](https://www.stlouis-mo.gov/government/departments/mayor/news/new-online-building-permit.cfm) |
| Volume of physical work | tons, miles, potholes, beds | "we removed more than 167,000 tons of debris, mobilized $155 million"; 21,290 miles ploughed ([State of the City](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/2026-sotc-address.cfm)) |
| Dollars secured or committed | grants, state and federal aid, settlement money | "Historic Investment of Rams Settlement Funds" ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/rams-bill-signed.cfm)); "a monumental win" for a $1,285,628 grant ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/slate-youthbuild-grant.cfm)) |
| A first, or a first in decades | "first Transportation & Mobility Plan since 1948"; "since the 1950s"; "for the first time ever" | Transportation plan ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/city-adopts-tmp.cfm)); winter shelter funded from general revenue ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/code-blue-after-action-2025-6.cfm)) |
| National standing | "nation-leading", "landmark", "best-in-class" | Data-center ordinance ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/mayor-signs-board-bill-49.cfm)) |
| Owning a failure, then fixing it | first person, short sentences | "The system was broken, we owned it, and our City fixed it." (State of the City, on sirens) |
| A new system or capability | "Those capabilities did not exist a year ago." | Unified command, weather briefings, automated sirens ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/severe-weather-prep-following-may-2025.cfm)) |
| A deadline met or a promise kept | "Living up to the promise" | Winter housing bills passed in two weeks ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-signs-board-bills-housing-winter-shelter.cfm)) |
| A target beaten, published | "This is the first time the division has exceeded that goal." | Street lighting ([CityStat Q2](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-q2.cfm)) |
| An appointment | credentials, rank, years of service | "a huge win for the City" ([Building Commissioner](https://www.stlouis-mo.gov/government/departments/public-safety/news/mangapora-building-appointment.cfm)) |
| Agreement with the Board of Aldermen | joint announcements | Rams bill "ambitious, realizable and catalytic" ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/rams-bill-friday.cfm)) |
| Nobody turned away; no harm | absence of a bad outcome | "capacity has not been exceeded" ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/city-extends-code-blue-jan-30-2026.cfm)) |

**The "50 Key Accomplishments" page** ([page](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/spencer-accomplishments.cfm)),
classified by this thread (**inferred**; an item can be of more than one kind): speed or timeliness 10; dollars 8;
things built, removed or repaired 8; rules and process changes 8; systems, data or technology launched 7; plans
adopted 5; people served 4; service rates raised 4; workforce 4; firsts 3; oversight actions 3; awards 0. 24 of
the 50 state a measured result and 8 give a before-and-after.

**What is not celebrated (observed absence).** The word "satisfaction" appears in none of the 151 releases, and
no release announces a graffiti, mowing or illegal-dumping result. Awards to the City are rare: a
digital-inclusion award ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/digital-trailblazer-26.cfm)),
a "Certified Welcoming" designation ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/stl-certified-welcoming-designation.cfm))
and, in the State of the City, Forest Park and two departmental awards.

## 5. Data, technology, AI, CityStat and how residents report problems

Full chronology, 137 logged statements and the search log: `research/parts/C-datatech.md`. All items **observed** on
the city page linked unless marked.

### 5.1 CityStat

| Date | Statement | Source |
|---|---|---|
| 15 Apr 2025 | Inaugural address: the mayor, "a mathematician by training", will "harness the power of data to make decisions" and use data to gauge residents' satisfaction. | [inaugural address](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/inaugural-address.cfm) |
| 31 Mar 2026 | Public launch of CityStat as a quarterly performance site. Mayor: "CityStat measures what matters"; publishing is to "help provide accountability for me, my office and our departments". The release lists misses against targets (below). | [release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-launch.cfm) |
| 31 Mar 2026 | **Reported:** at the launch COO Jonsson said "You'll continue to see those functions grow in our CityStat program." | [STLPR](https://www.stlpr.org/government-politics-issues/2026-04-01/st-louis-website-city-services-fixes) |
| 17 Apr 2026 | State of the City: CityStat and "our strengthened 311 service line" are the two examples given of welcoming accountability; "we are defining clear key performance indicators for every department". | [speech](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/2026-sotc-address.cfm) |
| 1 Jul 2026 | Health, Human Services and Towing added to the "nine departments and divisions already included"; new CSB and Forestry datasets. Four services named as still short of target. | [release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-q2.cfm) |
| 7 Jul 2026 | Strategic Priorities, initiative 17: "Define operational KPIs and targets for all departments and incorporate them in CityStat." Initiative 25: an IT roadmap. No owner or date for either. | [release](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-strategic-priorities.cfm) |
| 8 Jul 2026 | **Reported:** Martin O'Malley visit. Mayor: "that's the report card that residents are going to rely on"; "We're really focused right now on delivering data to the public." Jonsson on pairing data staff with neighbourhood staff: "That's where we're heading". | [St. Louis Magazine](https://www.stlmag.com/news/martin-omalley-visits-citystat/); [KMOV](https://www.firstalert4.com/2026/07/09/first-alert-forward-what-can-st-louis-learn-baltimore-about-improving-services/) |
| 9 Jul and 14 Aug 2026 | **Reported:** CityStat Program Manager Alex Price on vacant-lot mowing records: "we don't have that tracked in a system, so now we're starting"; per-lot logging by crews "hopefully coming in the next couple of weeks"; "CityStat can also help make the case potentially that we need more resources". | [KMOV 9 Jul](https://www.firstalert4.com/2026/07/09/cant-walk-down-street-tall-grass-overruns-sidewalks-north-st-louis-neighborhood/); [KMOV 14 Aug](https://www.firstalert4.com/2026/08/14/cut-down-unmowed-vacant-lots-st-louis-city-looks-data-north-city-resident-discusses-wait/) |
| 13 Oct 2026 | CityStat pages still say data "was last updated June 30th, 2026". No Q3 2026 update or release found. | [CityStat](https://www.stlouis-mo.gov/citystat/) |

Internal rhythm: see 5.6 (weekly cabinet data reviews since mid-November 2025, per the launch press conference).
Not established: who presents, and whether departments other than Streets hold their own sessions.

### 5.2 Targets the city has published, and where it says it is missing them

| Measure | Target | Latest stated | Source |
|---|---|---|---|
| CSB requests routed to the right department | 95% within 2.5 days | 93.5% Q1 2026; 99.9% Q2 2026 | [launch release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-launch.cfm); [CityStat CSB](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/public-safety/csb.cfm) |
| Potholes | 80% on time (major street 3 days, residential 8, alley 17) | Q2 2026: alley 98%, residential 91%, major streets below 80% | [Q2 release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-q2.cfm); [CityStat Streets](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/streets.cfm) |
| Validated hazardous trees removed | all within 30 days | 39.2% Q1 2026; under 20% in 2024 and 2025 | [launch release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-launch.cfm) |
| Emergency water main breaks restored | 80% within 8 hours | 61.9% Q1; 64.2% Q2 2026 | [Q2 release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-q2.cfm) |
| Building permits issued | 80% within 30 days | missed three quarters running; "lagging" since the online portal | [CityStat Building](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/public-safety/building-division.cfm) |
| Parks Division requests | 80% on time | 67.5% Q2 2026 (under 30% in 2024 and 2025) | [Q2 release](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-q2.cfm) |
| Refuse route coverage | 95% | met Q1 2026, slightly short Q2 | [CityStat Refuse](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/refuse.cfm) |
| Vacant-building lot maintenance | four rotations per cut season | first rotation not complete by 30 Jun 2026 | [CityStat Forestry](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/parks/forestry-division.cfm) |
| Hiring, application to start | 45 days (tied to Proposition HR, 6 Apr 2027 ballot) | 54 days | [release](https://www.stlouis-mo.gov/government/departments/mayor/news/legislation-to-modernize-stl-civil-service-system.cfm) |

No published target was found for graffiti removal, vacant-lot mowing or illegal-dumping response beyond the general
debris target (observed absence).

### 5.3 Gaps in its own data that the city states

- Refuse: "route completion and coverage data was not recorded until September 2025" ([CityStat Refuse](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/refuse.cfm)).
- Vacant lots: about 14,000 on rotation, about 7,000 mowed in the first 2026 rotation; "More root cause analysis needs to be done" ([CityStat Forestry](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/parks/forestry-division.cfm)). Mowing was tracked on paper (**reported**, KMOV 9 Jul 2026, link above).
- Service-request response differs by ward: Ward 10 slowest at 35.1 days average, Ward 1 fastest at 17.2 (Jan 2024–Mar 2026) ([CityStat CSB](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/public-safety/csb.cfm)).
- Winter shelter: "the system needs better infrastructure for data keeping and tracking of shelter residents" ([Code Blue review, 30 Jul 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/code-blue-after-action-2025-6.cfm)).
- Technology generally: the mayor said she inherited "abysmal turnover, antiquated technology, and a crippling lack of trust" and that "we should have had building permits online already" ([State of the City](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/2026-sotc-address.cfm)).

### 5.4 Resident reporting: 311 and the Citizens' Service Bureau (CSB)

- 311 was launched as the single phone number for CSB in June 2025; the web form and X (@stlcsb) remain channels, and the CSB page offers "Check The Status of a Service Request" ([100 days](https://www.stlouis-mo.gov/government/departments/mayor/news/100-days.cfm); [CSB page](https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/index.cfm)).
- The CityStat CSB page says "How well CSB works is directly tied to trust in city government." ([CityStat CSB](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/public-safety/csb.cfm)).
- The first-year list claims "Enabled real-time case tracking for residents interacting with city services." The system is not named ([accomplishments](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/spencer-accomplishments.cfm)).
- Strategic Priorities: "improve response times, resolutions, and accessibility" and bring the Neighborhood Stabilization Division, which houses CSB, "into the Mayor's cabinet" ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-strategic-priorities.cfm)). The executive post that leads the division and CSB was advertised on 14 Sep 2026, promising "a new era of data-driven decision-making" ([posting](https://careers.stlouis-mo.gov/careersection/cstl_career_portal_ext/jobdetail.ftl?job=2500004O)).
- Graffiti is reported through CSB and removed by Brightside St. Louis's graffiti eradication team ([report graffiti](https://www.stlouis-mo.gov/government/departments/parks/operation-brightside/report-graffiti.cfm)).
- The Mayor's Office runs a separate constituent casework system ([profile](https://www.stlouis-mo.gov/government/departments/mayor/profiles/garrett-allen.cfm)).
- Not found: any announcement of a new 311 mobile app, chatbot or vendor. The planned move of Cityworks to the cloud and the unfunded request to fix the 311 phone system are in 5.6.

### 5.5 IT, modernisation and AI

- IT Project Governance Committee (page created 17 Dec 2025): COO, ITSA Director, CTO, Budget Director, Board of Public Service President, Supply Commissioner. Goals include "Reducing redundant systems and encouraging enterprise solutions." ([governance page](https://www.stlouis-mo.gov/government/departments/information-technology/governance/index.cfm)).
- Online building permit portal launched 5 Mar 2026, replacing "manual routing and paper-based processes" ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/new-online-building-permit.cfm)).
- Operations technology named by the city: GPS on ploughs, camera monitoring of road conditions in a snow operations centre, "refuse route digitization", GIS-triggered sirens ([accomplishments](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/spencer-accomplishments.cfm); [CityStat Streets](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/streets.cfm); [severe weather release](https://www.stlouis-mo.gov/government/departments/mayor/news/severe-weather-prep-following-may-2025.cfm)). A Refuse GIS job posting names "Cityworks asset management, permitting (PLL), and CAD systems" ([posting](https://careers.stlouis-mo.gov/careersection/cstl_career_portal_ext/jobdetail.ftl?job=260000DL)).
- **AI.** The only city statement on AI found is ITSA's IT Policy #2026-001 of 23 Jul 2026. It prohibits "Use of any AI tool that has not been approved by ITSA.", says output "should be treated as a draft or support tool", says "Do not input sensitive or regulated data", and requires public-facing use to be disclosed. The approved-tool list is internal ([policy PDF](https://www.stlouis-mo.gov/government/departments/information-technology/documents/upload/Artificial-Intelligence-Policy-2.pdf)).
- **AI in the mayor's own output: absent.** Across 151 releases, the two major speeches and the accomplishments page, "AI" or "artificial intelligence" appears only in three SLATE job-training items. The data-centre releases never use the word. No statement by the mayor, COO, CTO or CIO about an AI pilot, chatbot or vendor was found (observed absence; searches listed in `C-datatech.md`).
- **Reported, non-city speaker:** at the 26 Aug 2026 launch of an AI innovation centre, GeoSTL's Mark Munsell (one of the hackathon's two podcast voices, section 8) said of vacant-lot mowing priorities "we've been working with the city for a few weeks on that problem". No city official is quoted ([KMOV](https://www.firstalert4.com/2026/08/26/st-louis-launches-ai-innovation-center-backed-by-tech-giants/)).
- Open data portal: page metadata last updated 11 Apr 2025, before the mayor took office; no Spencer-era statement about it found ([data portal](https://www.stlouis-mo.gov/data/)).

### 5.6 Added from hearings, press conferences, interviews and the campaign

Hearing, press-conference and interview items are **observed in YouTube auto-captions** (checked against the
caption file, not the audio; names are caption spellings). Detail: `research/parts/C-other-channels.md`.

- **How CityStat runs inside City Hall.** At the public launch the mayor and COO described weekly cabinet data
  reviews since mid-November 2025 ([press conference, 2 Apr 2026](https://www.youtube.com/watch?v=a1H60btjS2E)).
  **Reported:** operations are coordinated in the Asana project tool, with dashboards for time to hire, water-main
  repair time and hazardous-tree response; before that, by text, email and phone
  ([St. Louis Magazine, 22 Dec 2025](https://www.stlmag.com/news/colonels-stlouis-city-hall-spencer/)). The mayor
  said the first "StreetStat" had been held that week
  ([Fast Forward STL, published 27 Aug 2026](https://www.youtube.com/watch?v=Jzl1_gaOZKo)).
- **The system behind service requests.** Cityworks holds CSB requests and department work orders; ITSA plans to
  move it "from an on-prem system to a cloud" (Trimble Unity) in FY2027. A "My City" sign-in that gathers a
  resident's transactions in one dashboard was "soft launched". ITSA is adding three data-analytics posts that
  now support CityStat: "that's a big need and a big gap to be filled"
  (CIO Riordan, [hearing, 11 May 2026](https://www.youtube.com/watch?v=2MX-2honIkI)).
- **311 as its manager describes it.** Over 120,000 requests a year; a phone system residents say hangs up on
  them; a wish for language recognition and a post-call survey ("We want to find out the missing voices in the
  city"); ITSA's developer put the minimum fix at about $45,000; in the January 2026 storm staff mapped 300–400
  snow requests a day to redirect ploughs ([hearing, 12 May 2026](https://www.youtube.com/watch?v=tyS2V5Ae98I)).
  **Reported:** about 4,000 calls a month to 311
  ([KMOV, 12 Mar 2026](https://www.firstalert4.com/2026/03/12/city-highlights-citizen-service-bureau/)).
- **Streets and Refuse.** The Streets director is investigating a platform to join service requests,
  performance data and vehicle telematics; refuse routes are being digitised from manual records
  ([hearing, 13 May 2026](https://www.youtube.com/watch?v=2erY12agBgU)). **Reported:** new refuse trucks carry
  route tablets ([KMOV, 8 May 2026](https://www.firstalert4.com/2026/05/08/city-rolls-out-new-trash-trucks-keep-routes-track/)).
- **Forestry.** Data sits in Cityworks with no analyst; an analyst post was funded from 1 Jul 2026 and a $500,000
  tree inventory contracted (hearings of [6 May](https://www.youtube.com/watch?v=9lsGp9Wy4yw) and
  [30 Sep 2026](https://www.youtube.com/watch?v=ltJWr1X9UTc)).
- **Assets.** No comprehensive asset management programme (COO, 30 Sep 2026, hearing above).
  [Executive Order 96](https://www.stlouis-mo.gov/government/departments/mayor/documents/executive-orders/mayor-executive-order-no-96.cfm)
  (11 Jun 2026) orders a digital sidewalk map and a central asset inventory and performance dashboard, undated.
  The FY2027 budget funds a $500,000 inventory of signs and striping into GIS
  ([budget summary](https://www.stlouis-mo.gov/government/departments/budget/documents/upload/2-FY2027-AOP-Executive-Summary-and-Overview.pdf)).
- **Building.** Permits ran on a 1989 system (Dataflex) until February 2026; 99% of the work has moved to the
  online system ([hearing, 7 May 2026](https://www.youtube.com/watch?v=34oJcMY-UtM)).
- **Staff ideas.** **Reported:** a "Voice of the Workforce" app took over 100 employee submissions in its first
  days ([St. Louis Magazine, 13 Oct 2026](https://www.stlmag.com/news/voice-of-the-workforce-city-hall/)).
- **Before taking office.** As a candidate the mayor said "a program like CitySTAT is something that I think can
  be very, very helpful" and "we need to look at these things geographically"
  ([transcript, 17 Feb 2025](https://www.stlmag.com/news/transcript-citizens-agenda-cara-spencer/)). Her
  transition committee recommended, among other things, "Audit previously closed requests to ensure action was
  taken." and "Establish a data warehouse and integrate city data sets"
  ([report page, Wayback](https://web.archive.org/web/20250729223020/https://www.changeforstl.com/updates/transition-advisory-report)).
  These are recommendations to her, not her commitments.
- **AI in hearings and coverage: still absent.** A keyword search of the 69 saved City video captions ("artificial
  intelligence", "AI", "chatbot", "ChatGPT", "copilot", "machine learning") found AI raised by public commenters,
  in a business-award video, in a SLATE job-training class and in one aside about translation. No official
  describes using AI in a city service. No official mentions AI in the 2025 or 2026 news coverage read.

## 6. Who is who, and who would own a new tool in each area

Full roster with start dates, predecessors, conflicts between city pages and dead links: `research/parts/C-who-is-who.md`.
Titles **observed** on the [Staff and Cabinet page](https://www.stlouis-mo.gov/government/departments/mayor/cabinet.cfm)
or the appointment release unless marked.

### 6.1 "Ben"

**Inferred, high confidence, not confirmed:** the city speaker called Ben at the kickoff is Col. Benjamin "Ben" Jonsson,
Chief Operating Officer.

- **Observed:** announced 15 May 2025, to start 7 Jul 2025, after 25+ years in the U.S. Air Force (chief of staff, Air Mobility Command; vice superintendent and COO, Air Force Academy) ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/colonel-ben-jonsson-appointed-chief-operating-officer.cfm)). He "will oversee City departments and operations" and answers directly to the mayor ([15 Aug 2025 release](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-office-restructure.cfm)). He is the only Ben on the Staff and Cabinet page and sits on the IT Project Governance Committee. At a Board of Aldermen hearing on 30 Sep 2026 he said "I lead 14 departments and agencies" ([auto-caption](https://www.youtube.com/watch?v=ltJWr1X9UTc)).
- **Reported:** he speaks for CityStat in the press (links in 5.1) and for an employee-ideas programme: "They're not going to come from Room 200" ([St. Louis Magazine, 13 Oct 2026](https://www.stlmag.com/news/voice-of-the-workforce-city-hall/)).
- **Missing:** no organiser, UMSL or city page names the kickoff presenter, and no city release mentions the hackathon, Innovate USA or Missouri Innovation Week. Which departments formally report to him is not published; no organisation chart was found.

### 6.2 Senior team

| Role | Name | Since | Responsible for |
|---|---|---|---|
| Mayor | Cara Spencer | 15 Apr 2025 | Alderman 2015–2025; B.S. in mathematics |
| Chief of Staff | Casey Millburg | 15 Aug 2025 | "will lead policy and strategy and manage office staff"; was policy director |
| Chief Operating Officer | Col. Ben Jonsson | 7 Jul 2025 | City departments and operations |
| Deputy COO | Col. Bryan Barroqueiro | 3 Nov 2025 | Reports to Jonsson |
| Chief Recovery and Neighborhood Transformation Officer | Julian Nicks | 10 Jul 2025 | Tornado recovery; Recovery Office |
| Chief Economic Development Officer | Stephen Davis | 1 Jun 2026 | Economic development; chairs SLDC board (post empty Aug 2025–May 2026) |
| Director of Communications | Holly Roberts | 19 Jan 2026 | Media; predecessor Beverly Isom named on 2025 releases |
| Press Secretary | Kia Murray | 5 Oct 2026 | Predecessor Rasmus Jorgensen (contact on releases to 1 Jul 2026; leaving date not established) |
| CityStat Program Manager | Alex Price | not established | Runs CityStat; defines metrics with each department. Research analyst Jasper Wilson builds the dashboards |
| Chief Technology Officer (City and SLDC) | Simon Huang | pre-dates Spencer | Long-range technology planning; sits in the Mayor's Office |
| CIO and Director of ITSA | Cindy Riordan | CIO since Dec 2017 | City IT; previously managed CSB for eight years |
| Constituent Services Lead | Garrett Allen | not established | Mayor's Office casework system |
| Recovery Office | Jennifer Brinkmann (Innovation Team Director); Harsha Dara (Senior Data Analyst) | 2025–26 | Recovery "i-team"; reporting and dashboards |

No chief data, performance or innovation officer title exists on the staff page; no policy director is listed (observed).

### 6.3 Department heads most relevant to service delivery

| Area | Head | Notes |
|---|---|---|
| Street Department (Streets, Refuse, Traffic and Lighting, Towing) | James Jackson, Director (announced 12 Nov 2025) | Kent Flake, Commissioner of Streets; Dale Lee, Commissioner of Towing (named 24 Sep 2026); Refuse commissioner **not published** |
| Parks, Recreation and Forestry | Greg Hayes, Director since 2015 (certified arborist) | Alan Jankowski, Commissioner of Forestry (trees; vacant-lot mowing) |
| Brightside St. Louis (graffiti removal) | Joe Cunningham, Executive Director (announced 1 Sep 2026) | Not-for-profit listed under Parks ([release](https://www.stlouis-mo.gov/government/departments/parks/news/joe-cunningham-brightside-st-louis.cfm)) |
| Public Safety (Building, CEMA, Corrections, Neighborhood Stabilization, Violence Prevention) | Shawn Dace, Director | Building Commissioner Sarah Mangapora starts 19 Oct 2026; CEMA Commissioner Gregg Favre |
| Neighborhood Stabilization Division and CSB | **Interim** (Levaughn Smart, per the staff page); head post advertised 14 Sep 2026 | City pages conflict: a 10 Mar 2026 release names Karen Clifford "Acting Director", and an acting director (captioned "Erin Clifford", **inferred** the same person) presented the division's budget on 12 May 2026 ([hearing](https://www.youtube.com/watch?v=tyS2V5Ae98I)). CSB has two team leads; no CSB manager is published |
| Health; Human Services | Dr. Faisal Khan (from 3 Aug 2026); Dr. Adam Pearson | |
| Personnel | Brian Light (from 12 Jan 2026) | |
| Public Utilities / Water | Niraj Patel | |
| Planning and Urban Design | Don Roe | GIS Manager Ibrahim Gumel |
| SLDC; CDA | Stephen Westbrooks (**reported** from 30 Mar 2026); Matt Moak | |

### 6.4 Area → who would own a new tool

Every owner here is **inferred** from the reporting lines above; the city publishes no owner list.

| Area | Operational owner | Senior owner |
|---|---|---|
| Streets, potholes, debris, snow | Kent Flake (Streets) | James Jackson → COO |
| Refuse | Refuse commissioner (name not published) | James Jackson → COO |
| Trees and forestry | Alan Jankowski | Greg Hayes → COO |
| Vacant-lot mowing | Forestry Division (Jankowski) | Greg Hayes → COO |
| Graffiti | Removal: Brightside (Joe Cunningham). Intake: CSB | Greg Hayes; Shawn Dace |
| Resident reporting (CSB / 311) | CSB team leads; interim division head | Shawn Dace → COO; the July 2026 priorities move the division into the cabinet |
| Building, permits, code enforcement | Sarah Mangapora (from 19 Oct 2026) | Shawn Dace → COO |
| Performance data and CityStat | Alex Price | COO (public voice); Mayor |
| IT systems and any AI tool | Cindy Riordan, ITSA (the AI policy makes ITSA the approver) | Simon Huang (CTO); IT Project Governance Committee, which includes the COO |
| Tornado recovery | Julian Nicks | Mayor |
| Homelessness / winter shelter | Amy Bickford (Homeless Services) | Dr. Adam Pearson |
| Economic development | Stephen Westbrooks (SLDC) | Stephen Davis → Mayor |
| Hiring | Brian Light | Mayor; depends on Proposition HR (Apr 2027) |

## 7. The words and phrases they use for their priorities

Counts are **observed**: the number of the 151 Mayor's Office releases containing each term (full table
`research/parts/C-phrase-counts.tsv`; script `research/parts/C-scripts/phrase_counts.py`). Phrases in news and
hearings come from the short quotes in the log, so those counts undercount.

### 7.1 The standing vocabulary of the releases

| Term | Releases (of 151) | Note |
|---|---|---|
| residents | 108 | The default word for the public. "customer" is in 8, "taxpayer" in 8 |
| partner / partnership | 77 | 2 of 12 releases in 2025 Q2; 23 of 39 in 2025 Q4 |
| neighborhood(s) | 64 | |
| safe / safety | 61 | |
| priority / priorities | 54 | "top priority" in 12, all between Jul 2025 and Jun 2026: tornado housing and debris, then winter safety; four are snow-route boilerplate |
| collaborat- | 36 | |
| deliver / delivering | 32 | |
| long-term / long haul | 29 | |
| committed | 22 | |
| trust | 19 | "Rebuild Trust" only from 2026 Q2 |
| deserve(s) | 19 | |
| resilien- | 18 | |
| transparen- | 16 | |
| moderniz- | 13 | |
| accountab- | 12 | 5 of the 12 in 2026 Q3 |
| urgent / urgency | 10 | 8 of the 10 in Jul–Dec 2025 |
| high-quality | 9 | 6 of the 9 in 2025 Q3; the phrase fades after the transition |
| basic(s) | 8 | |
| first-ever / first time / first since | 7 | 5 of the 7 from 2026 Q2 on |
| catalytic | 5 | 4 of the 5 from 2026 Q2 on |
| data-driven / data-informed | 4 | none before 2026 |
| landmark | 3 | all in 2026 Q3 |
| satisfaction | 0 | Used once, in the inaugural address |

### 7.2 Signature phrases (observed, verbatim)

**The mayor**

- Purpose of city government: "a municipal government is a service delivery operation" (candidate, 17 Feb 2025,
  [transcript](https://www.stlmag.com/news/transcript-citizens-agenda-cara-spencer/)); "make our city grow, make
  our city safe, and make our city work" ([campaign site, Wayback](https://web.archive.org/web/20250218170315/https://caraspencer.com/about)).
- The standard: "basic city services should be delivered at the highest levels"
  ([12 Nov 2025](https://www.stlouis-mo.gov/government/departments/mayor/news/key-staff-cda.cfm)); services "at the
  levels St. Louisans count on and deserve"
  ([7 Jul 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-strategic-priorities.cfm)).
- Data: "We're also going to harness the power of data to make decisions"; "As a mathematician by training, I'm
  excited to dig into the numbers" ([inaugural](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/inaugural-address.cfm));
  "CityStat measures what matters" ([31 Mar 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/citystat-launch.cfm)).
- Openness: "The Mayor's Office has an 'Open Door Policy.'"; "We can no longer afford to operate in silos"
  (inaugural).
- What she inherited: "abysmal turnover, antiquated technology, and a crippling lack of trust"; "We are finally
  dragging City Hall into the 21st century"
  ([State of the City](https://www.stlouis-mo.gov/government/departments/mayor/news/speeches-remarks/2026-sotc-address.cfm)).
- Owning failure: "As mayor, that is my responsibility"; "The system was broken, we owned it, and our City fixed
  it." (State of the City).
- The stakes: "To end 70 years of population decline"
  ([5 Mar 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/new-online-building-permit.cfm));
  initiatives "to turn St. Louis around" (7 Jul 2026 release above).
- Partnership: "with the City" appears 11 times in the State of the City (**observed** count).
- Not enough, not fast enough: "We know that it's not enough"
  ([17 Jun 2025](https://www.stlpr.org/news-briefs/2025-06-17/st-louis-aldermen-waste-no-time-in-approving-30m-in-rams-money-for-tornado-relief));
  "I wish we could move faster. That's been frustrating."
  ([11 Dec 2025](https://www.stlmag.com/news/cara-spencer-winter-weather-snow/)); "I will move heaven and earth to
  get this done" ([30 Oct 2025](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-boa-tornado-housing-shelter.cfm)).
  In 2025 quotes "not enough" or a variant appears 7 times and "we know" opens 8 admissions
  (`C-news-2025.md`, section d).
- **Reported** in 2026 coverage: "one foot in front of the other" (8 May, 16 May, 21 Jul); "decades of
  disinvestment" (17 Apr, 8 May, 14 May); "catastrophic" for the police board's budget; "impasse" (9 Apr)
  (`C-news-2026.md`, section d).
- Wins: "ambitious, realizable and catalytic"
  ([14 May 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/rams-bill-friday.cfm));
  "nation-leading", "landmark"
  ([17 Sep 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/mayor-signs-board-bill-49.cfm)).
- Police: "state-controlled" ([26 Feb 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/mass-cuts-layoffs-police-budget.cfm)).

**The July 2026 priority titles** ([release](https://www.stlouis-mo.gov/government/departments/mayor/news/spencer-strategic-priorities.cfm)):
"Rebuild Trust in City Services"; "Recover & Revitalize Neighborhoods"; "Accelerate Economic Development";
"Cultivate a Culture of Excellence"; "Modernize City Government". Initiative names inside them: "Customer-First
Culture", "Data-Driven Performance", "Ease of Business", "Catalytic Investments", "Governance Reform".

**The Chief Operating Officer (Jonsson)**

- "we don't have a final solution. We're on a journey."
  ([14 Aug 2025](https://www.stlmag.com/news/st-louis-ends-alley-recycling/)); "we definitely have not arrived"
  ([29 Oct 2025](https://www.stlmag.com/news/stlouis-recycling-drop-sites-results/)).
- "It was astonishing to us" ([22 Dec 2025](https://www.stlmag.com/news/colonels-stlouis-city-hall-spencer/)).
- "You'll continue to see those functions grow in our CityStat program."
  ([31 Mar 2026](https://www.stlpr.org/government-politics-issues/2026-04-01/st-louis-website-city-services-fixes)).
- "I lead 14 departments and agencies"; "right now we don't have a comprehensive asset management program"
  ([30 Sep 2026](https://www.youtube.com/watch?v=ltJWr1X9UTc)).
- "They're not going to come from Room 200"
  ([13 Oct 2026](https://www.stlmag.com/news/voice-of-the-workforce-city-hall/)), on where ideas come from.

**The Chief Recovery Officer (Nicks)**

- "we also know that it's not fast enough"
  ([24 Sep 2025](https://www.stlpr.org/economy-business/2025-09-24/st-louis-residents-tornado-debris-removal-plan));
  "The delivery of services has not started in scale"
  ([20 Jan 2026](https://www.stlouis-mo.gov/government/departments/mayor/news/private-property-assistance-deadline.cfm)).
  "Scale" recurs in his 2026 statements (`C-news-2026.md`, section d).
- "Recovery can't be successfully led by City Hall alone"
  ([27 Aug 2025](https://www.stlouis-mo.gov/government/departments/mayor/news/recovery-committees-announced.cfm)).

**Department heads at the 2026 budget hearings** (auto-caption)

- Reactive to proactive: "we are going to go from a reactive um department to a proactive" (311,
  [12 May 2026](https://www.youtube.com/watch?v=tyS2V5Ae98I)).
- "So there's a heavy emphasis on metrics" (Parks, [6 May 2026](https://www.youtube.com/watch?v=9lsGp9Wy4yw)).
- "Right now we're behind the curve" (Streets, [13 May 2026](https://www.youtube.com/watch?v=2erY12agBgU)).
- "we'll continue to drive toward our 30-day target" (Personnel,
  [14 May 2026](https://www.youtube.com/watch?v=MgQu7EC0oow)).

### 7.3 How the wording has moved (inferred from 7.1 and section 1.4)

- From "basics" and "high-quality city services" (campaign, transition, 2025) to "Rebuild Trust in City
  Services" and "customer-first" (April and July 2026).
- From "openness and accountability" as the first priority (April 2025) to accountability shown through CityStat
  ("measures what matters", March 2026).
- "Urgent" and "top priority" belong to the tornado and winter months of 2025; "catalytic", "landmark" and
  "first" belong to mid-2026.
- "Public safety" stays in the vocabulary (23 releases) but leaves the list of headings in July 2026.

## 8. The hackathon's organisers: what they say they want from the event

Source: saved transcript of *The STL Bucket List Show*, episode "Mike Seper & Mark Munsell - Missouri Innovation
Week", dated 30 September 2026, 38:50 long
(<https://www.stlbucketlistshow.com/1932300/episodes/19885025-mike-seper-mark-munsell-missouri-innovation-week>;
local copy `.../innovate-usa-2026-10-13/sources/www.stlbucketlistshow.com_..._missouri-innovation-week.txt`, saved
2026-10-13 15:26 CDT). **observed** = read in the saved transcript. The transcript is machine-generated and labels
speakers only as SPEAKER_01/02/03. **Inferred:** SPEAKER_01 is Mike Seper (he refers to "my current role as director
of innovation and IP at UMSL", 6:01) and SPEAKER_03 is Mark Munsell (retired from NGA, speaks for GeoSTL, 3:17–4:34);
SPEAKER_02 is the host. Timestamps are the transcript's.

**What Seper says he wants (observed):**

| Time | What he says | Short quote |
|---|---|---|
| 2:32 | The week exists to give students more chances to learn about innovation and to give the community one place to gather and network, tied to workforce development and careers. | "the first Missouri Innovation Week" |
| 6:01 | Leaders should think about where AI is and "applications for good"; community bodies, including the City of St. Louis, propose challenges they are encountering. | "How do we use it to advance our community?" |
| 10:05 | The hackathon is 33.5 hours (the Spirit of St. Louis flight time); students work on problems presented by the City of St. Louis. | "building solutions that might be adopted by the city" |
| 10:05 | He contrasts it with hackathons about cybersecurity or building a startup. | "We're trying to empower our community." |
| 17:45 | Aim is to show young people why St. Louis is a place to stay and to position the city as a leader in AI. | "open the aperture for the kids" |
| 20:24 | His stated measure of success is one young person whose direction changes. | "that 14-year-old that this changes their life" |
| 31:38 | Framing of AI is growth, not cuts; the expo is free to students. | "looking at ways to be able to grow for tomorrow" |
| 32:46 | Judges look at what was built and how it can be applied; selected builders are invited to the T-REX finish-line event to meet leaders. | "how these can be applied" |
| 34:52 | He wants a "connected network" of universities and community partners; says over three dozen leaders back it. | "Everyone's aligned on the mission" |

**What Munsell says he wants (observed):**

| Time | What he says | Short quote |
|---|---|---|
| 7:40 | The Spirit of St. Louis AI Innovation Center is about non-commercial uses of AI: humanitarian, environmental, food security from satellite imagery. | "so many good things that we can do" |
| 12:06–13:05 | GeoSTL's own yardstick is economic: companies, jobs, investment in St. Louis. | "That's my metric, that's our metric at GeoSTL." |
| 15:32 | He expects hackathon participants to produce large amounts of code with AI coding tools; names Claude and Google. | "thousands of lines of code because of Claude" |
| 19:20 | Young people need to be shown, given the environment and equipped to invent. | "you have to show them" |
| 21:50 | AI lets people without training build software. | "it does democratize your ability to invent something" |
| 24:21 | AI-built prototypes still need a software engineer to implement them. | "you should bring in a software engineer" |
| 28:01 | Replacing workers with AI is a mistake. | "that's a race to the bottom" |

**What the podcast does not say (observed absence):** it names no prizes, no scoring rubric, no judges, no specific
city challenge, no city official, and no process by which the city would adopt a build. "Adopted by the city" is
stated as a possibility ("might be"), not a commitment. It speaks of high-school and university students throughout;
the Community division is not mentioned.

**Consistency with other saved sources (observed):** the event's hackathon page says "City of St. Louis leaders will
present real challenges" and states the goal as "to empower and excite our future leaders to solve community
challenges" (<https://innovateusa.org/hackathon.html>, saved copy). UMSL's 28 September 2026 article says participants
may also identify problems in their own communities
(<https://blogs.umsl.edu/news/2026/09/28/missouri-innovation-week/>, saved copy). The kickoff excerpt summarised in
`context/HACKATHON_CONTEXT.md` (**reported**, Jack's partial transcript) has Seper stressing why a problem matters,
the community story, and a route to actual use.

**One further sighting (observed, auto-caption; identification inferred):** at the Board of Aldermen's Public
Infrastructure and Utilities Committee on 1 Oct 2025, a public commenter captioned "Mark Manzel" said he had
"recently retired from the National Geospatial Intelligence Agency", where he had been chief technology officer and
chief artificial intelligence officer, and spoke in favour of data centers
(<https://www.youtube.com/watch?v=rj60D5r7TAo>, about 0:53:53). This matches Munsell's description of himself in
the podcast.
