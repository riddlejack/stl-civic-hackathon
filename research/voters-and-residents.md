# F. What voters and residents want, by area — City of St. Louis

Facts only. No solutions or project ideas appear in this file.

Labels: **observed** = this thread retrieved and checked it directly; **reported** = a source says so; **inferred** = this thread's conclusion.

## Summary (at most half a page)

**Found.**

- **Elections (observed):** official results for all 24 elections the election board lists from March 2021 to August 2026 at ward and precinct level, reconciling exactly to citywide totals. Turnout was 25.8% for mayor in April 2025 and 13.8% for the earnings tax in April 2026. Since 2021, measures about streets, derelict property, dumping, bonds and existing revenue passed with 68–89%; the one measure shifting budget power to aldermen failed.
- **Turnout and vote split by area (observed):** wards 11–14 vote at 40–60% of the rate of wards 2, 4 and 5 in every election checked. Wards 2, 4 and 5 hold 22% of residents and cast 31% of April 2025 ballots. Spencer took 79–86% in the southwest and 29–32% in wards 11–13.
- **What residents were asked (observed):** no representative survey of all residents on services or priorities exists for 2021–2026. The large exercises are self-selected and lean to the same wards that vote most: wards 11–13 hold 21% of residents and supplied 7–8% of Rams-settlement survey responses.
- **Help-seeking (observed and inferred):** three north-side wards (10, 11, 12) account for about 78% of 12,733 tornado aid registrations. North-side 311 requests concentrate on vacant property, dumping, stray dogs and lighting; southwest requests on refuse and trees. Web share of 311 requests is 56–64% in the southwest and 25–26% in wards 12 and 13.
- **Aldermen (observed):** roster, stated priorities, 669 bills and 204 recorded votes. The commonest bill is a speed hump. Each ward controls about $750,000–766,000 a year.

**Could not establish.**

- Actual ward-capital spending or balances by ward (not published).
- Current 2-1-1 requests by ZIP (dashboard behind a bot check).
- More than 3–5 reviews per service listing; no neighbourhood pattern in reviews.
- What members said in hearings (video only); campaign-finance totals.
- Everything by area describes wards, precincts or ZIPs, not the individuals in them.

## Status: COMPLETE for this pass, 2026-10-14 ~00:35 UTC

Work ran 2026-10-13 23:25 UTC to 2026-10-14 00:35 UTC, with a pause at 23:38 UTC for a usage limit (nothing on disk was lost). Scripts are in `research/voters-and-residents-scripts/`. Open items are listed under "Looked for, not found" at the end.

## Part files (detail)

| Part | File | Raw downloads |
|---|---|---|
| 1. Election results (ward/precinct, turnout) | `research/parts/F1-election-results.md` | `data/raw/voters/elections/` |
| 1. What each contest was fought over | `research/parts/F1-election-coverage.md` | `data/raw/voters/election-coverage/` |
| 2. Polls, surveys, public input, help-line requests | `research/parts/F2-asked-directly.md` | `data/raw/voters/surveys/` |
| 3. Public reviews of city services | `research/parts/F3-service-reviews.md` | `data/raw/voters/reviews/` |
| 4a. Aldermen: roster, stated priorities, hearings | `research/parts/F4a-aldermen-priorities.md` | `data/raw/voters/aldermen/` |
| 4b. Aldermen: sponsored bills, ward-controlled money | `research/parts/F4b-aldermen-bills-money.md` | `data/raw/voters/aldermen-bills/` |
| 5. Differences across the city (census join) | this file, Part 5 | `data/raw/voters/census-join/` |


### Tables saved beside this file (`research/voters-and-residents--<name>.csv`)

| Name | Rows | Used in |
|---|---|---|
| `211-requests-citywide-2020-21` | 11 | Part 2.4 |
| `aldermen-rollcalls` | 204 | Part 4.1: every recorded vote, 2025–26 and 2026–27 |
| `aldermen` | 15 | Part 4.1: roster, terms, stated priorities with sources |
| `bills-by-sponsor` | 59 | Part 4.2 |
| `board-bills` | 669 | Part 4.2: one row per bill |
| `contests` | 43 | Part 1.3: contest, result, issues |
| `csb-requests-by-ward` | 560 | Part 5.2: top 40 request types × ward |
| `csb-summary-by-ward` | 14 | Part 5.2: volume, channel, closure by ward |
| `election-results-long` | 46,089 | Part 1: votes by contest, choice, ward, precinct |
| `election-turnout` | 3,468 | Part 1: registered and ballots by ward, precinct |
| `evictions-by-tract` | 111 | Part 2.4 |
| `fema-ia-dr4877-by-zip` | 483 | Part 2.4 |
| `govocal-ideas` | 1,418 | Part 2.3: open idea boards |
| `help-requests-by-ward` | 14 | Part 5.4: FEMA and eviction estimates by ward |
| `homeless-pit-counts` | 20 | Part 2.4 |
| `precinct-demographics` | 207 | Part 5.1 |
| `precinct-elections-joined` | 184 | Part 5.3 |
| `service-ratings` | 38 | Part 3 |
| `service-review-themes` | 114 | Part 3 |
| `survey-results` | 2,182 | Part 2: numeric results, long |
| `surveys` | 33 | Part 2: one row per survey |
| `ward-demographics` | 14 | Part 5.1 |
| `ward-elections-joined` | 14 | Part 5.3 |
| `ward-money` | 318 | Part 4.3: budgets, not spending |
| `ward-survey-participation` | 14 | Part 5.4 |

Every figure in this file is also listed, one per row, with unit, date, label and URL in `research/voters-and-residents-facts.csv` (built by `research/voters-and-residents-scripts/facts.py`, which checks the table figures against the CSVs above).

## Part 1. Elections

Detail: `research/parts/F1-election-results.md` (numbers) and `research/parts/F1-election-coverage.md` (what each contest was about). Tables: `research/voters-and-residents--election-results-long.csv` (46,089 rows), `--election-turnout.csv` (3,468 rows), `--contests.csv`.

### 1.1 What was retrieved (observed)

- Source: St. Louis City Board of Election Commissioners, <https://www.stlouis-mo.gov/government/departments/board-election-commissioners/elections/results/index.cfm>, retrieved 2026-10-13 23:25–23:35 UTC. 62 files (61 text-layer PDFs, 1 CSV) covering every election from 2 March 2021 to 4 August 2026; manifest with URL, time, bytes and hash at `data/raw/voters/elections/_manifest.csv`.
- Finest level published: **precinct**, with registered voters and ballots cast per precinct. 24 elections parsed to citywide, ward and precinct level. Every ward sum and precinct sum equals the published citywide figure (zero mismatches across all 24).
- Elections to 19 April 2022 use the old 28 wards; from 12 July 2022 the 14-ward map. Only the 14-ward elections are joined to demographics in Part 5.
- Cross-check (**observed**, 2026-10-14T00:05Z): OpenElections' Missouri precinct file for 5 November 2024, <https://raw.githubusercontent.com/openelections/openelections-data-mo/master/2024/20241105__mo__general__precinct.csv> (190,270 rows statewide; 12,810 rows and 183 precincts for St. Louis City), gives the same city totals as this thread's parse for the five figures compared (Harris 94,458; Kunce 93,919; Quade 91,034; Amendment 3 yes 95,704; Proposition A yes 97,262). **Inferred:** OpenElections probably transcribed the same Board report, so this confirms the parsing, not the count. It carries no city propositions.
- Negative result: the Missouri Secretary of State results pages (`www.sos.mo.gov/elections/s_default/results`, `enr.sos.mo.gov`, `enrarchives.sos.mo.gov`) each returned HTTP 403 from a Cloudflare bot check at 2026-10-14T00:04Z; not pursued.
- Not done: elections before March 2021 (the Board's archive goes back to 2004). The registered-voter base moves between elections without explanation in the files (179,412 in April 2024; 196,836 in November 2024; 176,146 in August 2026).

### 1.2 Citywide turnout, city-wide elections only (observed)

| Date | Election | Registered | Ballots | Turnout |
|---|---|---|---|---|
| 2021-03-02 | Municipal primary (approval voting) | 201,352 | 44,571 | 22.1% |
| 2021-04-06 | Municipal general (mayor) | 201,409 | 58,707 | 29.2% |
| 2022-04-05 | Special (Prop R, Prop 1) | 186,422 | 19,448 | 10.4% |
| 2022-08-02 | State primary | 190,221 | 46,000 | 24.2% |
| 2022-09-13 | Special primary, Board president | 191,587 | 11,804 | 6.2% |
| 2022-11-08 | General | 194,565 | 84,823 | 43.6% |
| 2023-03-07 | Municipal primary (first 14-ward) | 196,458 | 24,823 | 12.6% |
| 2023-04-04 | Municipal general | 196,692 | 35,604 | 18.1% |
| 2024-04-02 | Municipal general (sewer-district measures) | 179,412 | 12,466 | 6.9% |
| 2024-08-06 | State primary | 186,854 | 55,100 | 29.5% |
| 2024-11-05 | General (four city charter propositions) | 196,836 | 117,802 | 59.9% |
| 2025-03-04 | Municipal primary (mayor) | 196,340 | 34,982 | 17.8% |
| 2025-04-08 | Municipal general (mayor) | 196,472 | 50,610 | 25.8% |
| 2026-04-07 | Municipal general (Prop E only) | 196,299 | 27,013 | 13.8% |
| 2026-08-04 | State primary (Prop M) | 176,146 | 62,155 | 35.3% |

About one registered voter in four chose the mayor in April 2025; about one in seven voted on the earnings tax in April 2026.

### 1.3 Results and what each contest was fought over

Results are **observed** from the Board's files. Issue descriptions are **reported** from contemporaneous coverage (mainly St. Louis Public Radio, St. Louis Magazine, St. Louis American), with URLs and dates per claim in `F1-election-coverage.md`.

| Date | Contest | Result | What coverage said it was about |
|---|---|---|---|
| 2025-04-08 | Mayor | Spencer 32,162 (64.15%), T. Jones 17,974 (35.85%) | Basic services (January 2025 snowstorm, trash, streets, 911); incumbent ran on falling crime and north-side investment; a troubled north-side grant programme; developer and PAC money |
| 2025-03-04 | Mayor, approval primary | Approvals as % of 34,982 ballots: Spencer 68.1, T. Jones 33.2, Butler 24.9, A. Jones 13.6 | Snowstorm response and service competence |
| 2025-04-08 | Comptroller | Baringer 51.50%, D. Green 48.50% | 30-year incumbent; late payments, payroll errors, software |
| 2025-04-08 | Aldermen, odd wards | All incumbents returned; Ward 5 open seat unopposed; closest Ward 3 (52.45%) | Issue content not established |
| 2025-07-01 | Ward 8 special | Cox Antwi 54.95%; turnout 14.4% | Downtown redevelopment sites; donor money |
| 2026-04-07 | Prop E: keep the 1% earnings tax | Yes 84.70% | Tax is about a third of general revenue; police, fire and labour campaigned to keep it |
| 2026-08-04 | Prop M: charter clean-up | Yes 77.99% | Obsolete charter language; no organised opposition found |
| 2024-11-05 | Prop T: create a Department of Transportation | Yes 88.51% | Street safety; fragmented responsibility for streets; no funding attached |
| 2024-11-05 | Prop V: lift fine caps on derelict non-owner-occupied property and dumping | Yes 79.81% | Vacant buildings, dumping, absentee owners |
| 2024-11-05 | Prop S: 3% fee on short-term rentals | Yes 67.52% | Affordable Housing Trust Fund; rents; eviction legal aid |
| 2024-11-05 | Prop B: more budget power for aldermen | **Failed**, Yes 47.41% (needed 60%) | Aldermen versus the Board of Estimate and Apportionment; earmarks; credit rating |
| 2023-04-04 | Prop C: charter commission every 10 years | Yes 60.09% (needed 60%) | 1914 charter outdated |
| 2023-04-04 | 3% recreational-marijuana sales tax | Yes 62.67% | New revenue; no opposition campaign |
| 2023-04-04 | Aldermen, all 14 wards (first after cut from 28) | Closest: Ward 14, 51.5% | Public-safety reform; service delivery; how to spend ARPA, Rams and marijuana money |
| 2026-11-03 | Prop B (half-cent sales tax for early childhood education) and Prop 1 (approval voting for aldermanic vacancies) | **Not yet voted**; each needs 60% | Childcare cost versus a regressive sales tax; who runs the fund |

**Earlier measures, for the same pattern (observed results; thresholds reported):** April 2022 Prop 1, $50M capital bond for streets, bridges, recreation centres and firehouses, yes 84.41% (needed two-thirds); April 2022 Prop R, citizen redistricting commission and conflict-of-interest rules, yes 69.14%; August 2022 Prop F, higher fines for dumping, yes 85.04%; April 2021 Prop E earnings tax, yes 79.43%. Charter amendments need three-fifths (Missouri Constitution Art. VI s. 32(a)); the earnings tax needs a simple majority (state statute 92.115). Verbatim ballot text for all 25 measures on city ballots from 2021 to 2026 is in section 15 of `F1-election-coverage.md`.

**Label warning (observed):** letters repeat across bodies. "Prop S" is a school bond (August 2022), a sewer-district stormwater tax (April 2024) and the city short-term-rental fee (November 2024). Props Y and 1–5 (April 2021) and W (April 2024) are sewer-district measures, not city ones.

**2025 ward races (reported, St. Louis Public Radio candidate pieces of 21 February and 5 March 2025):** in the four contested wards, candidates named vacancy and derelict buildings and development that does not displace residents (wards 3 and 11), basic services such as bulk trash and streets (wards 1 and 7), and public safety (wards 1 and 7). Every incumbent won; three of seven seats were uncontested.

**Inferred across contests:**

- Since 2021, measures about streets, derelict property and dumping, a housing fee, capital bonds and keeping existing revenue passed with 68–89%, with no organised opposition reported.
- Measures about who holds power drew the only reported opposition and the narrowest margins: Prop B failed with 47.41% (2024); Prop C cleared its 60% threshold by 0.09 points (2023); four further charter proposals in 2024 never reached voters.
- Basic services (trash, streets, snow, 911) appear in every mayoral, Board-president and aldermanic contest read, and reporters attributed the 2025 mayoral result to them more than to any single policy dispute. Public safety led in 2021 and persisted.
- Reporters explained both the 2021 and 2025 mayoral results through north-side and south-side turnout and margins. Part 5.3 quantifies that.

**Not established:** per-ward explanations of the 2025 aldermanic results; campaign-finance totals (Ballotpedia has none; the state ethics commission search was not queried); the outcome of a November 2025 lawsuit over a citizen petition for a state audit of city government, ruled 39 signatures short; no recall since 2023 was found. The Post-Dispatch is paywalled and was not read; Riverfront Times, Missouri Independent and Fox 2 article pages returned HTTP 403.

## Part 2. What residents were asked directly

Detail: `research/parts/F2-asked-directly.md` (33 surveys, polls and input processes, 2021–2026, each with sponsor, dates, questions, sample and results). Tables: `research/voters-and-residents--surveys.csv` (33 rows), `--survey-results.csv` (2,182 rows), `--govocal-ideas.csv` (1,418 rows). Figures were read from the raw reports unless marked.

### 2.1 The main negative result

**No representative survey of all City residents about services or priorities was found for 2021–2026, and no city-commissioned resident-satisfaction survey was found** (the second rests on a web search only). What exists is of two kinds: small likely-voter polls, and large self-selected online exercises.

### 2.2 Representative samples (likely voters only)

| Poll | Field dates | n | What it asked | Result | Breakdown |
|---|---|---|---|---|---|
| Remington / Missouri Scout | 3–4 Mar 2021 | 544 | "Most important task facing the next Mayor" | Safer city 52%, schools 14%, jobs 12% | "Safer" named by 59% of white and 44% of Black respondents; area by state Senate district only |
| Remington / Missouri Scout | 25–27 Mar 2025 | 622 | Right direction or wrong track | Wrong track 52%, right direction 28% | Wrong track 70% of white, 29% of Black voters; 63% in Senate District 4, 40% in District 5 |
| Remington / Missouri Scout | Jan, Feb, Jun 2025 | 416–568 | Favourability, vote intention, job approval | No issue questions | Senate district |
| Show Me Victories | 25–28 Mar 2021 | 650 | Mayoral vote, earnings tax | No issue questions | North / central / south by ZIP |

No 2025 mayoral-race poll with an issue-priority question was found.

### 2.3 Self-selected exercises (observed; all over-represent white, higher-income, south and central residents by the sponsors' own accounts)

| Exercise | Sponsor | Dates | n | Top results | Area breakdown |
|---|---|---|---|---|---|
| Board Bill 22 (Rams settlement) survey | Board of Aldermen | 14–27 May 2026 | 1,394 | 66% supported the bill; tornado recovery ranked first by 714; water infrastructure had the highest mean score; downtown uses the lowest | Ward (support 53% in ward 2 to 84% in ward 13) |
| Rams "Vote on Ideas" (10 tokens across 20 ideas) | Board of Aldermen | 5 Jan – 4 Feb 2024 | 12,442 | Share of online voters supporting: water mains 46%, traffic calming 43%, city-worker pay 40%, subsidised child care 38% | Ward, race, age, income (see 5.4) |
| Rams Kick-Off Survey | Board of Aldermen | Aug–Oct 2023 | 3,195 | Only a summary is published (Resolution 159): city services the top challenge; car damage from streets and slow 911 most widespread; 53% of write-ins about crime or safety | None published |
| ARPA Community Needs Survey | Mayor's office | 2 Apr – 20 May 2022 | about 5,200 (city and county mixed) | Option-level counts in the CSV | City / county only |
| Direct Relief Questionnaire | Stimulus Advisory Board | 5 May – 2 Jun 2021 | 2,590 | Importance ratings by relief category in the CSV | Response rate by ZIP only |
| Transportation & Mobility Plan surveys | City | 2024–25 | 1,241 and 327 | In the part file | North / south pop-up votes |
| Strategic Land Use Plan surveys | City | Nov 2023 – Dec 2024 | 760+ | In the part file | Participant ZIP only |
| Consolidated Plan needs survey | Community Development Administration | 2024 | 379 or 397 (the document gives both) | In the part file | None |
| Open idea boards (Ideas Portal, policy proposals, data centres) | Board of Aldermen | 2023–2026 | 998 ideas, 132 proposals, 282 data-centre posts | Safety tagged on 39% of Ideas Portal posts; most-liked ideas concern traffic violence, 911 and transit; all 20 most-liked data-centre posts oppose data centres | None |

Group differences in the 2024 vote (**observed**, counts of unique supporters): Black participants' top two were the redevelopment loan fund and subsidised child care; white participants' were traffic calming and water mains; participants over 60 put water mains and water-treatment plants first; lower-income participants put child care and city-worker pay first.

**Small panels:** Washington University's iHeard St. Louis panel (n=141–198 per wave, recruitment method unpublished, city and county mixed). July 2024: 34% picked crime as the challenge whose fixing would most benefit St. Louis. May 2026: local leaders scored 3.6 out of 10 on tornado recovery.

**Recurring asks across the exercises (inferred):** public safety including 911 response and traffic; streets, trash and vacant buildings; water and sewer lines; housing; and, in 2026, tornado recovery.

### 2.4 What people ask for when they seek help

| Source | Retrieved | Rows | Period | Unit | Main figures (observed) |
|---|---|---|---|---|---|
| FEMA Individual Assistance registrations, May 2025 tornado (DR-4877), OpenFEMA API | 2026-10-13 23:28 UTC | 16,310 (12,733 in the city by census GEOID) | Applications 23 May – 26 Aug 2025 | Registration, with ZIP and block group | 55% renters; 60% with income of $30,000 or less; half of owners had no home insurance; $51.2M approved. Five ZIPs (63115, 63113, 63112, 63108, 63107) hold 86% |
| Eviction filings, Eviction Lab tracking file | 2026-10-14 00:16 UTC | 26,558 (8,320 for the city's 104 tracts) | Jan 2020 – Aug 2026 | Tract × month | City filings: 5,893 in 2023, 5,220 in 2024, 5,685 in 2025; 5,130 in the 12 months to July 2026. Top 10 of 104 tracts hold 39% |
| HUD point-in-time homeless counts, St. Louis City | 2026-10-14 | 5 reports | Jan 2021 – Jan 2025 | City-wide | 1,235 people in Jan 2024, 1,637 in Jan 2025; unsheltered 154 to 387 (before the tornado) |
| United Way 2-1-1, one published table | 2026-10-14 | 11 | Mar 2020 – Apr 2021 | City-wide | 72,610 requests; half for rent, mortgage or utility help |

FEMA registration is a request for federal aid, not a measure of all need. An eviction filing is a landlord's court filing against a tenant, not a request by a resident. Ward-level versions are in 5.4.

**Not retrieved:** current 2-1-1 requests by ZIP. The 211 Counts dashboard (`211mo.211counts.org`) returned a Cloudflare bot challenge (HTTP 403) and was left alone; by this project's rule that data does not count as available. No ZIP-level data was found for utility assistance or food-pantry visits; 988, legal-aid and findhelp data were not searched.

## Part 3. What residents say about specific services

Detail: `research/parts/F3-service-reviews.md`. Tables: `research/voters-and-residents--service-ratings.csv` (38 rows) and `--service-review-themes.csv` (114 coded reviews, own paraphrases, no reviewer names). Retrieved 2026-10-13 23:32 to 2026-10-14 00:23 UTC. All figures **observed** on rendered pages or raw JSON.

**How thin this is.** Reviewers choose themselves and lean negative. Signed out, Google Maps shows only 3–5 "most relevant" reviews per listing, which is Google's selection and not a sample; nothing beyond that was read. Dates on Google are relative ("3 months ago"). Several listings have 11 or fewer ratings. Only 7 of 114 reviews name a place, so there is no neighbourhood pattern. The ratings describe the people who left them, not residents in general.

### 3.1 Google Maps ratings (27 listings, 22 services)

| Service (listing) | Rating | Ratings | Latest review seen |
|---|---|---|---|
| Parking-ticket bureau (Traffic Violation Bureau) | 1.6 | 55 | 3 months before retrieval |
| Building Division | 1.8 | 9 | 2 months |
| Street Department | 1.9 | 37 | 2 months |
| City Justice Center (jail) | 2.3 | 95 | 5 months |
| Water Division | 2.4 | 55 | 6 years |
| Animal regulation | 2.5 | 11 | 6 months |
| Citizens' Service Bureau (311) | 2.6 | 31 | 3 months |
| Refuse Division | 2.7 | 28 | 1 month |
| Department of Health | 2.8 | 25 | 3 months |
| Collector of Revenue | 3.0 | 65 | no review text shown |
| Assessor | 3.0 | 61 | 2 months |
| Forestry Division | 3.1 | 22 | 5 months |
| Municipal Court | 3.6 | 48 | 4 months |
| Board of Election Commissioners | 3.6 | 9 | 2 months |
| City Hall | 3.7 | 331 | 2 months |
| Vital Records | 4.1 | 37 | 1 year |
| Recreation centers (Wohl, 12th & Park, Cherokee) | 4.3 each | 276, 21, 97 | 11 months to 2 years |
| Department of Human Services | 4.7 | 7 | 8 months |
| Recorder of Deeds | 4.8 | 271 | 1 month |

Listings with 1–3 ratings (Treasurer, business licences, permit section) are in the CSV. No listing for the city tow lot was found in three searches. Lambert Airport: 4.1 from 11,853 (rating only).

### 3.2 What the reviews read say, by service

- **Across departments:** unanswered or unreturned phone calls is the most widespread complaint: 9 of 67 Google reviews, in 8 services (Citizens' Service Bureau, Street, Forestry, Water, Building, animal control, the jail, Election Board).
- **Citizens' Service Bureau:** all 3 reviews shown are complaints: no reply to repeated reports, requests closed without work, phone menu and website not working.
- **Street:** snow and ice clearing (2); unanswered calls about street lights (1).
- **Parking tickets:** appeals, staff manner, towing despite a payment plan.
- **Refuse:** overflowing alley dumpsters (1); praise for supporting a volunteer clean-up (2).
- **Forestry:** a four-month wait for a hazardous tree (about 2023); praise for post-tornado help in O'Fallon Park.
- **Assessor:** confusion over personal-property tax and removal from the roll; praise for quick waivers.
- **Water:** billing and slow repair, but every review shown is 6–8 years old.
- **Praise:** quick, courteous counter service at the Recorder of Deeds, Vital Records and Municipal Court; recreation-center reviews are about programmes and instructors.

**Inferred:** in this small set, offices where a resident completes a transaction at a counter (deeds, vital records, court) rate 3.6–4.8, and services where a resident reports a problem and waits for field work (311, streets, refuse, building inspection, water) rate 1.8–2.7.

### 3.3 Other platforms

- **Yelp:** City Hall 3.4 (12 reviews), Assessor 3.2 (14), a generic "City of St. Louis" page 3.7 (35); 21 reviews coded. Water Division and Recorder listings exist with no reviews.
- **Apple App Store:** no official city app was found in two searches. ParkLouie, the parking vendor's app, has 4.70 from 1,748 star ratings; of its 26 written reviews 16 are one-star and 23 date from 2021 or earlier.
- **Employee views, not residents:** Indeed 3.2 from 177 reviews; Glassdoor 3.0 from 197.
- **Better Business Bureau:** one "City of St Louis" profile, not rated; no department profiles.

### 3.4 Access notes and what was not done

- Yelp, Indeed, Glassdoor and the BBB profile returned HTTP 403 challenge pages to a plain request but loaded normally in the built-in browser with no challenge shown; they were read there. No CAPTCHA was solved and nothing was signed in to.
- Not attempted: Google Play, Facebook, Nextdoor (login), Trustpilot-type sites, airport review sites, and listings for shelters, the land bank, emergency management, pools, Police and Fire.

## Part 4. Elected representatives by ward

Detail: `research/parts/F4a-aldermen-priorities.md` and `research/parts/F4b-aldermen-bills-money.md`. A member's priorities and bills are evidence about the member, not proof of what ward residents want.

### 4.1 Roster, stated priorities, hearings and votes

Roster **observed** on the official page <https://www.stlouis-mo.gov/government/departments/aldermen/representation/index.cfm> (2026-10-13T23:25Z; 2026–27 session, which began 2026-04-21). Priorities are each member's own words from campaign sites, interviews and 2026 coverage, with a URL and date per item in `research/voters-and-residents--aldermen.csv` and the part file. The office is nonpartisan and official pages give no party.

| Ward | Member (chair role) | Next election | Stated priorities (member's framing, shortened) |
|---|---|---|---|
| 1 | Anne Schweitzer (chairs Reducing Red Tape) | 2029 | Water system first for Rams money; city-worker and police pay; roads and sidewalks; vacancy; strict data-centre rules |
| 2 | Tom Oldenburg (not running again, reported) | 2027 | Police staffing and pay; fix 911; potholes, tree trimming, parks; dumping; opposes encampments |
| 3 | Shane Cohn (chairs Transportation and Commerce; on the Nov 2026 ballot for Recorder of Deeds) | 2029 | Public safety, basic services; neighbourhood revitalisation; reform of development incentives |
| 4 | Bret Narayan (chairs Public Safety) | 2027 | Police at authorised strength; traffic calming and lighting; neighbourhood associations; keep the Rams principal as an endowment |
| 5 | Matt Devoti (since April 2025) | 2029 | Responsive police and emergency services; fire and EMS equipment money; water meters |
| 6 | Daniela Velazquez (chairs Legislation and Rules) | 2027 | Safe, clean neighbourhoods; better city services; affordable housing; small business |
| 7 | Alisha Sonnier | 2029 | Public safety through root causes; youth and families; housing; public benefit from subsidised development |
| 8 | Jami Cox Antwi (since July 2025 special election) | 2027 | Housing; transit and street safety; downtown; most Rams money to tornado recovery |
| 9 | Michael Browning (chairs Public Infrastructure and Utilities) | 2029 | Safer streets and the new transportation department; renters' rights; reform of ward capital, which he calls inequitable |
| 10 | Shameem Clark Hubbard (chairs Housing, Urban Development and Zoning) | 2027 | Tornado money reaching residents too slowly; zoning update; civilian oversight; anti-displacement |
| 11 | Laura Keys | 2029 | Gun violence; trash, dumping, tree trimming; board up abandoned homes and cut lots; senior home repair; youth jobs |
| 12 | Sharon Tyus | 2027 | Money earmarked for north St. Louis alone; less for downtown; same-day cutting of grass and brush; Homer G. Phillips senior apartments |
| 13 | Pamela Boyd (chairs Health and Human Development) | 2029 | Gun violence; trash, dumping, alleys; senior home repair; secure abandoned homes; youth jobs |
| 14 | Rasheen Aldridge (chairs Budget and Public Employees) | 2027 | Equal investment across the ward's neighbourhoods; displacement; blight; safer streets for children |
| President | Megan Green | 2027 | Rams split across north side, infrastructure and downtown; housing affordability; more accountability for the Recovery Office; trash collection |

- **Common ground (inferred from the table):** public safety, basic services (trash, dumping, grass and trees, streets) and housing or home repair appear in almost every member's list.
- **Differences (inferred):** wards 11, 12 and 13 stress vacancy, dumping, senior home repair and money reserved for the north side; wards 2 and 4 stress police staffing; wards 7 and 9 stress root causes, renters and traffic safety. No current platform was found for six members (Oldenburg, Clark Hubbard, Cox Antwi, Devoti, Tyus, Green), whose entries rest on older campaign text and 2026 news. The campaign lists of the ward 11 and ward 13 members are nearly word-for-word identical. Vote411 guides need an address entry and were not used; social-media pages were not opened.

**Recorded votes (observed).** The city publishes every member's final-passage votes: 204 items across the 2025–26 and 2026–27 sessions, 39 of them contested, all in `research/voters-and-residents--aldermen-rollcalls.csv` (39 cross-checked against per-item pages with no mismatch).

| Item (date) | Result | No votes by ward | What was argued (reported, St. Louis Public Radio and Spectrum, dates in part file) |
|---|---|---|---|
| FY2027 budget, BB 1 (2026-06-26) | 8–6, one abstention | 3, 4, 5, 9, 11, 12; ward 13 abstained | Police raises set by the state-appointed police board; police got $220M of $250M requested; a transfer out of fire and EMS equipment money |
| Water meters, BB 28 (2026-06-26) | 9–6 | 3, 7, 11, 12, 13, 14 | No free-to-read account of the debate found |
| Rams settlement, BB 22 (2026-07-02) | 12–3 | 4, 5, 12 | Ward 12: too little reserved for the north side; ward 4: spend interest, not principal; residents and Action St. Louis asked for more tornado money from the downtown share |
| Water rates, BB 25 (2026-06-18) | 12–2 | 12, 14 | About 90% rise over six years; Water Division reserves exhausted, $700M in capital needs |
| Data-centre zoning and incentives, BB 49 and BB 55 (2026-09-11) | 13–0 | none (12, 13 absent) | Wards 1, 7, 9 opposed amendments they said weakened the rules; an attempt to ban large data centres failed at the Planning Commission |
| Reprimand of the ward 12 member, Res. 125 (2026-10-02) | 8–3 | 11, 12, 13 | Grew out of competing bills on the city-owned Homer G. Phillips senior apartments |

- **Pattern (observed counts, inferred reading):** on the 39 contested items the ward 12 member voted No 26 times and the ward 13 member 16 times, 13 of them together; ward 11 often joins them. The six votes against water meters came from wards 11–14, which cover most of north St. Louis, plus wards 3 and 7. Votes against the last two budgets came from both sides of the city: FY2026 (2025-06-13) from wards 2, 3, 4, 12 and 13; FY2027 from wards 3, 4, 5, 9, 11 and 12.
- **Hearings:** 82 committee meetings in the 2026–27 session are listed with agenda items in the part file (9 hand-checked). What individual members said in hearings exists only as video and was not transcribed. Committee-level vote tallies were not found.

### 4.2 What each member sponsors

Source: every board-bill page on <https://www.stlouis-mo.gov/government/city-laws/board-bills/> for sessions 2023–24 to 2026–27, scraped 2026-10-13 23:25–23:38 UTC: 669 bills, introduced 2023-04-28 to 2026-10-09, one primary sponsor each. Table: `research/voters-and-residents--board-bills.csv`; per-sponsor counts in `--bills-by-sponsor.csv`. Topic and ward-specific flags are keyword rules; on a fresh 40-bill hand-check the final rules had 1 topic error and 1 flag error (so the true error rate could be up to about 13%). All **observed** unless marked.

- 533 of 669 bills (80%) passed the Board. 273 (41%) concern one ward or site. The largest topic is traffic control, 137 bills, 101 of them mentioning speed humps; then site redevelopment incentives (69) and budget and pay (64). Tornado recovery and the Rams settlement account for 4 bills each.

| Ward | Member | Bills as primary sponsor | Passed Board | Ward- or site-specific | Traffic-control bills |
|---|---|---|---|---|---|
| President | Megan Green | 8 | 6 | 0 | 0 |
| 1 | Anne Schweitzer | 58 | 50 | 23 | 17 |
| 2 | Thomas Oldenburg | 18 | 9 | 7 | 5 |
| 3 | Shane Cohn | 79 (35 are airport bills) | 70 | 6 | 5 |
| 4 | Bret Narayan | 26 | 24 | 5 | 2 |
| 5 | Matt Devoti (from 2025); Joseph Vollmer (to 2025) | 13; 10 | 12; 10 | 7; 6 | 9 (both) |
| 6 | Daniela Velazquez | 23 | 14 | 5 | 4 |
| 7 | Alisha Sonnier | 46 | 30 | 19 | 11 |
| 8 | Jami Cox Antwi (from 2025); Cara Spencer (to 2025) | 12; 34 | 10; 29 | 6; 15 | 9 (both) |
| 9 | Michael Browning | 48 | 39 | 25 | 10 |
| 10 | Shameem Clark Hubbard | 73 | 61 | 24 | 15 |
| 11 | Laura Keys | 47 | 31 | 35 | 12 |
| 12 | Sharon Tyus | 24 | 15 | 18 | 4 |
| 13 | Pamela Boyd | 60 | 51 | 31 | 24 |
| 14 | Rasheen Aldridge | 90 | 72 | 41 | 10 |

- **Inferred:** the most common thing an alderperson legislates is a speed hump or stop sign on a named block. Ord. 71394 obliges the Board of Public Service to install one once a bill passes, which is why a street-level request becomes a board bill.

### 4.3 Money the ward controls

All figures are **budget, not spending**. No actual ward-capital spending or current balance by ward is published anywhere this thread looked (public expenditure ledger, open-data catalog, capital plans, Comptroller pages). Table: `research/voters-and-residents--ward-money.csv` (318 rows; the `spent` column is empty throughout).

- **Rule (observed):** half of the ½-cent capital-improvement sales tax goes to ward sub-accounts, split equally among the 14 wards since 2023-04-01 (Ord. 71656). Per ward: $752,614 in FY2025, $751,429 in FY2026, $766,304 in FY2027. Bill text: <https://www.stlouis-mo.gov/government/city-laws/board-bills/boardbill.cfm?bbDetail=true&BBId=14217>.
- **Who decides (observed):** the capital-plan manual says ward projects "shall be pre-approved by each respective alderperson"; the Board of Public Service, Streets, Parks and Forestry carry them out. <https://www.stlouis-mo.gov/government/departments/budget/capital-committee/documents/upload/Capital-Improvement-Plan-Policy-and-Procedures-manual.pdf>
- **Budgeted use, FY2025–FY2027, $32.4M across 14 wards (observed, capital budget Exhibit H):** "ward projects" 56% (mostly one unlocated sidewalk, curb, street and alley lump per ward); 50/50 sidewalk programme 14%; refuse-container replacement 13%; contingency 7%; street trees 5%; parks 3%.

| Ward | 50/50 sidewalks | Refuse containers | Street trees | Parks | Contingency (unassigned) |
|---|---|---|---|---|---|
| 1 | $460,000 | $290,000 | $127,450 | $6,250 | $0 |
| 2 | $450,000 | $405,000 | $124,404 | $138,800 | $0 |
| 3 | $0 | $265,000 | $157,000 | $143,000 | $0 |
| 4 | $855,000 | $405,000 | $127,821 | $100,625 | $0 |
| 5 | $650,000 | $405,000 | $132,836 | $75,000 | $0 |
| 6 | $450,000 | $405,000 | $121,104 | $26,250 | $0 |
| 7 | $0 | $215,000 | $87,433 | $141,250 | $0 |
| 8 | $0 | $265,000 | $92,830 | $232,500 | $751,429 |
| 9 | $181,000 | $335,000 | $108,256 | $3,750 | $0 |
| 10 | $466,000 | $405,000 | $113,476 | $48,750 | $0 |
| 11 | $729,000 | $405,000 | $60,870 | $6,250 | $0 |
| 12 | $0 | $0 | $46,355 | $0 | $1,556,201 |
| 13 | $0 | $265,000 | $74,806 | $11,250 | $0 |
| 14 | $450,000 | $120,000 | $87,716 | $135,250 | $0 |

- **Observed differences:** street-tree budgets run $121,000–157,000 in wards 1–6 and $46,000–114,000 in wards 7–14 (lowest: ward 12, $46,355; ward 11, $60,870). Ward 12 left two of three years as contingency and budgeted nothing for refuse containers, sidewalks or parks. Five wards (3, 7, 8, 12, 13) budget nothing for the 50/50 sidewalk programme, which the Street Department says is funded only from ward capital.
- **Carry-over (observed):** Ord. 71789 reallocated $17.35M of unspent balances from the old 28 ward accounts as of April 2023, from $0.59M (ward 5) to $2.71M (ward 12).
- **St. Louis Works (observed):** a second ward-linked street fund, $6.0M in 2026, appropriated by division with no per-ward schedule.
- **Two pending bills would change this (observed, 2026–27 session):** BB 87 (Aldridge, co-sponsor Green; introduced 2026-10-02) would split ward capital 60% equally and 40% by a need score, sweep balances above $800,000 and require a public portal of ward balances. BB 78 (Devoti) would move St. Louis Works into a five-year transportation plan and sweep unallocated aldermanic money.
- **Other pots (observed):** the ARPA project and expenditure files have no ward field; the Rams settlement (Board Bill 22) is divided by area, not by ward: in the floor-amended bill text, $120M North St. Louis ($89M tornado recovery, $31M neighbourhood plan), $80M citywide ($40M water, $30M public infrastructure, $10M vacancy) and $55M Downtown, $255M in all. The mayor's May 2026 release described an earlier $230M version with $25M held back (thread B, `research/parts/B-city-stated.md`).
- **Not established:** actual spending; how the reallocated $17.35M was re-appropriated; whether any ward currently runs participatory budgeting; how aldermanic courtesy over development works now.

## Part 5. Differences across the city

**Reading rule for this whole part:** every figure below describes a ward or precinct, not the people in it. A ward that is 93% Black and has low turnout does not show that Black residents vote less; a ward with many vacancy complaints does not show who filed them. With 14 wards, rank correlations are descriptive only.

### 5.1 Ward demographics (method and table)

Sources and method (all **observed**; scripts run 2026-10-13 ~23:30 UTC):

- Ward boundaries: city open-data file `wards_2020.zip` (14 wards, the 2022 map), downloaded by thread A to `data/raw/stlouis-mo.gov/files/`; catalog <https://www.stlouis-mo.gov/data/datasets/>. Precincts: `Precincts_Current.zip` (209 polygons, names like `W 2 P 6`; 207 contain at least one populated 2020 block centroid).
- 2020 Census block counts: PL 94-171 Missouri file, <https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Missouri/mo2020.pl.zip>, retrieved 2026-10-13T23:25Z, 35,967,209 bytes; 8,057 city blocks; city total 301,578 people, 247,547 adults, 173,479 housing units (28,609 vacant). Saved in `data/raw/voters/census-join/`.
- Each block was assigned to the ward and precinct containing its interior point. Check: ward totals for population, non-Hispanic White, non-Hispanic Black and 18+ match the attributes in the city's own ward file exactly for all 14 wards.
- ACS 2020–2024 five-year block-group (tract for vehicles and income) estimates from thread A's files in `data/raw/census_acs_sf/` were apportioned to wards by each block's share of its block group's 2020 population or housing units. These are **inferred** estimates with unquantified error; "approx. median income" is an occupied-unit-weighted mean of tract medians, not a true ward median.
- Full tables: `research/voters-and-residents--ward-demographics.csv` (14 rows) and `research/voters-and-residents--precinct-demographics.csv` (207 rows). Block crosswalk: `data/raw/voters/census-join/blocks2020_ward_precinct.csv` (8,057 rows).

| Ward | Main neighbourhoods (by 2020 pop.) | Pop. 2020 | % Black (NH) 2020 | % White (NH) 2020 | % below poverty (ACS 20–24) | % renter | % units vacant 2020 | % households no vehicle | Approx. median HH income |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Bevo Mill, Boulevard Heights, Carondelet, Holly Hills, Patch | 22,692 | 19.7 | 60.1 | 16.4 | 37.9 | 13.1 | 11.9 | $64,000 |
| 2 | St. Louis Hills, Princeton Heights, Bevo Mill, Boulevard Heights | 22,653 | 10.3 | 75.3 | 11.1 | 40.8 | 7.5 | 9.7 | $67,600 |
| 3 | Dutchtown, Carondelet, Mount Pleasant, Gravois Park | 21,753 | 49.6 | 27.2 | 25.3 | 64.7 | 19.2 | 24.1 | $46,400 |
| 4 | Lindenwood Park, Clifton Heights, Clayton-Tamm, Franz Park, Hi-Pointe | 21,627 | 6.1 | 80.4 | 5.2 | 38.7 | 9.5 | 5.2 | $76,000 |
| 5 | North Hampton, Southampton, Southwest Garden, The Hill | 22,521 | 11.1 | 76.5 | 10.7 | 42.1 | 9.1 | 6.5 | $74,500 |
| 6 | Tower Grove South, Shaw, Dutchtown, Compton Heights | 22,692 | 22.6 | 57.8 | 13.4 | 48.2 | 10.5 | 11.5 | $82,900 |
| 7 | Tower Grove East, Benton Park West, The Gate District, Gravois Park, Fox Park | 21,361 | 49.7 | 34.8 | 16.4 | 50.6 | 17.3 | 19.6 | $70,900 |
| 8 | Soulard, Benton Park, Downtown, Marine Villa, Peabody Darst Webbe | 21,751 | 35.8 | 51.7 | 23.4 | 65.5 | 15.9 | 16.7 | $67,700 |
| 9 | Central West End, Forest Park South East | 20,571 | 24.0 | 53.2 | 19.9 | 72.8 | 12.7 | 23.1 | $59,400 |
| 10 | West End, Skinker DeBaliviere, DeBaliviere Place, Academy, Wydown Skinker | 20,922 | 55.5 | 27.0 | 24.1 | 62.2 | 19.5 | 22.5 | $53,800 |
| 11 | Midtown, O'Fallon, Jeff Vanderlou, Covenant Blu-Grand Center, Penrose | 20,651 | 67.9 | 21.0 | 33.1 | 73.9 | 23.9 | 34.5 | $30,300 |
| 12 | Greater Ville, Penrose, Kingsway West, Kingsway East, Mark Twain | 21,153 | 92.7 | 3.0 | 33.1 | 54.9 | 29.2 | 29.3 | $38,000 |
| 13 | Baden, Wells Goodfellow, North Pointe, Walnut Park East, Walnut Park West | 20,584 | 93.0 | 2.7 | 32.9 | 49.4 | 24.4 | 26.6 | $39,000 |
| 14 | Downtown West, Downtown, St. Louis Place, Hyde Park, Carr Square | 20,647 | 71.4 | 20.7 | 32.8 | 72.9 | 21.4 | 28.3 | $44,500 |

**Observed pattern:** wards 11–14 (north side and the near-north riverfront) are 68–93% Black with about a third of residents below poverty; wards 2, 4 and 5 (southwest) are 75–80% White with 5–11% below poverty. Wards 3, 7, 8 and 10 are mixed.

### 5.2 Complaints: 311 (CSB) requests by ward, October 2025 – September 2026

Source: city CSB service-request CSVs (`csb.zip`, files `2025.csv` and `2026.csv`, latest record 2026-10-13 00:33), downloaded by thread A; catalog <https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5>. 121,276 requests in the 12 months; 120,925 fell inside a ward polygon using the file's own coordinates (EPSG:3857). Tables: `research/voters-and-residents--csb-summary-by-ward.csv` and `research/voters-and-residents--csb-requests-by-ward.csv` (top 40 request types × ward, with rate per 1,000 residents and a location quotient = ward share ÷ citywide share). All **observed** unless marked.

- **A request is not always a resident's request.** Intake channel citywide: web 54,189; phone 31,889; `NSO` (neighbourhood stabilisation staff) 17,466; `INDETERMINATE` 14,333; other 2,101. Staff-entered (`NSO`) requests are 4–8% of the total in wards 2, 4 and 5 and 18–24% in wards 10–14.
- **How people reach the city differs more than how often.** Web share of requests is 56–64% in wards 2, 4, 5, 6, 8 and 25–26% in wards 12 and 13; phone share runs the other way (16–22% vs 38–42%). Across the 14 wards, web share has a rank correlation of −0.89 with % Black, −0.91 with % below poverty and −0.92 with % of units vacant. Requests per 1,000 residents through resident channels (web, phone, e-mail, chat, letter, Twitter) show no such gradient (178 in ward 9; 239–347 in most wards; 399 in ward 13).
- **What is asked about differs by area** (requests per 1,000 residents, all channels):

| Request type | Lowest wards | Highest wards |
|---|---|---|
| High weeds/grass around vacant building | W6 3.3, W9 3.4, W5 3.6 | W13 27.7, W12 26.3, W11 17.4 |
| Debris dumped in street or alley | W9 3.3, W5 4.0, W4 4.3 | W13 23.2, W12 16.0, W3 11.2 |
| Stray dogs at large | W9 4.0, W5 4.6, W4 5.0 | W13 20.5, W12 14.8, W14 12.0 |
| Street lights out (single + whole block) | W3 6.9, W2 8.6, W5 9.1 | W8 25.2, W14 24.6, W13 23.8, W12 23.4 |
| Trash container not emptied | W9 6.3, W10 11.4, W8 14.6 | W4 45.3, W13 35.4, W2 29.7 |
| Damaged trash container | W14 7.2, W9 7.4, W11 7.4 | W4 36.7, W1 28.1, W2 26.4 |
| Inspect city tree | W14 5.1, W11 6.6, W9 8.0 | W5 27.3, W2 23.8, W6 21.5 |
| Abandoned/derelict vehicle | W9 19.0, W4 19.9, W10 21.0 | W7 45.7, W13 44.2, W3 43.5 |

- **Inferred:** in the 12 months observed, north-side wards' requests concentrate on vacant property, dumping, stray animals and lighting; southwest wards' concentrate on refuse collection and street trees; abandoned vehicles lead almost everywhere. Because north-side counts include many staff-entered requests, the vacancy figures there partly reflect city inspectors' activity, not resident demand.
- **Outcome proxies:** share of requests neither closed nor cancelled at retrieval is 6.9–9.6% in wards 1–6 and 8, and 10.6–16.0% in wards 9–14 (rank correlation with % Black 0.69). Median days to close (closed requests only) ranges 2.4–5.6 with no north–south pattern. Closure in this dataset is an administrative status; it does not establish that the problem was fixed (**inferred** caveat; the file's own description says nuisance reports "automatically close when submitted").

### 5.3 Turnout and vote by ward and precinct

Method: `--election-turnout.csv` and `--election-results-long.csv` joined to the demographic tables on ward, and on ward-plus-precinct number for precincts. All 183 precincts reporting in April 2025 match a precinct polygon; the 23 unmatched polygons hold 413 people. Tables: `research/voters-and-residents--ward-elections-joined.csv` (14 rows), `--precinct-elections-joined.csv` (184 rows: the 183 April 2025 precincts plus one that reported only in other elections). Figures are **observed** arithmetic on official results; the pattern statements are **inferred**.

| Ward | % Black 2020 | Turnout Nov 2024 | Turnout Apr 2025 | Turnout Apr 2026 | Ballots Apr 2025 per 100 adults (2020) | Spencer % Apr 2025 | Baringer % | Prop B yes | Prop T yes | Prop V yes | Prop S yes | Prop E yes 2026 | Prop M yes 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 19.7 | 62.8 | 28.6 | 15.4 | 22.2 | 79.2 | 63.1 | 44.0 | 86.5 | 79.7 | 66.1 | 84.1 | 75.0 |
| 2 | 10.3 | 71.8 | 33.6 | 19.0 | 28.0 | 85.5 | 79.6 | 42.2 | 87.3 | 82.1 | 66.4 | 86.0 | 79.4 |
| 3 | 49.6 | 51.5 | 20.2 | 9.5 | 13.8 | 56.7 | 41.3 | 48.3 | 89.0 | 78.1 | 66.1 | 79.5 | 72.3 |
| 4 | 6.1 | 73.5 | 29.5 | 18.0 | 26.0 | 81.7 | 74.5 | 44.5 | 88.9 | 83.0 | 68.9 | 85.3 | 81.2 |
| 5 | 11.1 | 74.1 | 31.7 | 17.8 | 27.0 | 80.9 | 72.0 | 45.8 | 90.0 | 84.0 | 70.1 | 86.4 | 83.4 |
| 6 | 22.6 | 69.5 | 32.6 | 19.0 | 27.9 | 63.7 | 54.2 | 57.7 | 92.6 | 86.1 | 77.0 | 90.8 | 87.6 |
| 7 | 49.7 | 62.0 | 28.8 | 14.6 | 24.2 | 52.0 | 40.4 | 52.5 | 91.4 | 81.2 | 71.0 | 86.5 | 81.5 |
| 8 | 35.8 | 64.3 | 27.4 | 13.6 | 20.3 | 75.0 | 60.5 | 53.4 | 92.6 | 84.8 | 70.5 | 87.2 | 83.6 |
| 9 | 24.0 | 64.1 | 25.0 | 14.6 | 18.6 | 67.4 | 54.2 | 51.9 | 92.7 | 83.5 | 74.2 | 87.5 | 84.9 |
| 10 | 55.5 | 55.1 | 24.4 | 12.6 | 19.6 | 48.4 | 33.5 | 45.2 | 87.6 | 75.9 | 65.5 | 85.3 | 75.6 |
| 11 | 67.9 | 44.4 | 17.8 | 7.2 | 10.7 | 31.0 | 12.6 | 43.3 | 84.7 | 71.3 | 59.8 | 76.3 | 59.6 |
| 12 | 92.7 | 42.5 | 17.9 | 8.0 | 16.0 | 28.6 | 9.5 | 40.1 | 77.6 | 64.4 | 53.8 | 73.4 | 56.6 |
| 13 | 93.0 | 43.0 | 18.0 | 8.6 | 16.7 | 32.0 | 10.3 | 41.1 | 80.4 | 67.0 | 53.7 | 74.9 | 57.8 |
| 14 | 71.4 | 45.2 | 17.1 | 8.3 | 11.7 | 43.5 | 27.5 | 49.9 | 89.9 | 77.3 | 65.2 | 77.0 | 69.7 |

Turnout is ballots ÷ registered voters. Proposition percentages are yes ÷ (yes + no).

- **Turnout gap.** In every election checked, wards 11–14 turn out at between about 40% and 60% of the rate of wards 2, 4 and 5 (November 2024: 43–45% against 72–74%; April 2025: 17–18% against 30–34%; April 2026: 7–9% against 18–19%). Ward rank correlation of turnout with % below poverty is −0.92 to −0.95 in all five elections; across 148 precincts with 200+ registered voters it is −0.68 to −0.78.
- **Whose ballots decide city contests.** Wards 2, 4 and 5 hold 22% of residents and cast 31% of April 2025 ballots and 33% of August 2026 ballots. Wards 10–14 hold 34.5% of residents and cast 25% and 22%.
- **The registered-voter denominator is uneven.** Registered voters per 100 adults counted in 2020 run from 60 (ward 11) to 93 (ward 13). Measured against 2020 adults instead of the rolls, wards 12 and 13 (16–17 ballots per 100 adults in April 2025) sit above wards 3, 11 and 14 (11–14). **Inferred:** rolls in areas that have lost population carry more stale registrations, so official turnout understates participation there somewhat; the gap with the southwest wards remains under either measure.
- **2025 mayoral vote split along the same line.** Spencer took 79–86% in wards 1, 2, 4 and 5 and 29–32% in wards 11–13; ward 10 and ward 14 were close (48.4%, 43.5%). Rank correlation of Spencer's share with % Black is −0.96 by ward and −0.91 by precinct. The comptroller race tracked it almost exactly.
- **Ballot measures passed everywhere but with less support on the north side.** Props T, V, S, E and M won a majority in all 14 wards; yes shares in wards 11–13 ran 8–31 points below the central corridor (wards 6, 8, 9), with the widest gap on Prop M (charter clean-up: 57–60% against 84–88%). The fines-on-derelict-property measure (Prop V) drew its lowest support (64–71%) in the wards with the most vacant-building complaints in 5.2.
- **The power-shift measure did not follow that line.** Prop B (aldermanic budget power) got its highest yes shares in wards 6, 7, 8 and 9 (52–58%) and failed in both the southwest (42–46%) and the far north (40–43%); its rank correlation with % Black is −0.22.
- These are area patterns. They do not show how any group of individuals voted.

### 5.4 Surveys and help requests by area

Source rows: `research/voters-and-residents--survey-results.csv` (extracted by the Part 2 agent from the Board of Aldermen's own reports; ward counts were read from chart images, so treat single counts as ±a few). Joined table: `research/voters-and-residents--ward-survey-participation.csv`.

**Who answered the city's two largest input exercises (observed arithmetic; both were self-selected online exercises):**

| Ward | Share of city population | Share of 2024 Rams "Vote on Ideas" participants (9,672 with a ward) | Share of 2026 Board Bill 22 survey (1,201 with a ward) | 2024 participants per 1,000 residents | 2024 top choice among that ward's online voters |
|---|---|---|---|---|---|
| 1 | 7.5 | 6.7 | 8.7 | 28 | Water mains |
| 2 | 7.5 | 9.6 | 10.1 | 41 | Water mains |
| 3 | 7.2 | 3.9 | 5.2 | 18 | Water mains |
| 4 | 7.2 | 10.6 | 9.4 | 48 | Water mains |
| 5 | 7.5 | 11.3 | 9.2 | 49 | Water mains |
| 6 | 7.5 | 13.4 | 12.9 | 57 | Traffic calming |
| 7 | 7.1 | 9.3 | 11.0 | 42 | Traffic calming |
| 8 | 7.2 | 9.6 | 9.3 | 43 | Traffic calming |
| 9 | 6.8 | 6.8 | 7.2 | 32 | Traffic calming |
| 10 | 6.9 | 5.7 | 5.4 | 27 | Redevelopment revolving loan fund |
| 11 | 6.8 | 2.2 | 2.2 | 11 | Redevelopment revolving loan fund |
| 12 | 7.0 | 3.8 | 2.3 | 17 | Redevelopment revolving loan fund |
| 13 | 6.8 | 2.4 | 2.1 | 11 | Redevelopment revolving loan fund |
| 14 | 6.8 | 4.6 | 4.9 | 21 | Downtown streets and sidewalks |

- Wards 11–13 hold 20.7% of residents and supplied 8.4% of 2024 participants and 6.7% of 2026 respondents. Wards 2, 4 and 5 hold 22.2% and supplied 31.6% and 28.7%. Ward 6 alone supplied more 2024 participants (1,295) than wards 11, 12, 13 and 14 together (1,259).
- **Inferred:** the citywide ranking from these exercises (water mains first in 2024) is the ranking of the wards that answered most. The same wards cast a disproportionate share of ballots (5.3) and file a larger share of their 311 requests online (5.2), so three separate channels of resident voice lean the same way.
- The ward-level top choices describe each ward's self-selected participants (216 to 1,295 per ward; each ward's top choice had 91 to 700 supporters), not the ward.

**Help requests by ward (inferred estimates):** FEMA registrations carry a census block-group code and eviction filings a tract code; both were apportioned to wards by each block's share of 2020 housing units. Table: `research/voters-and-residents--help-requests-by-ward.csv`.

| Ward | FEMA tornado registrations (est.) | Share of city | Per 100 occupied homes (2020) | FEMA aid approved (est.) | Eviction filings, Aug 2025 – Jul 2026 (est.) | Share of city | Per 100 renter households (est.) |
|---|---|---|---|---|---|---|---|
| 1 | 135 | 1.1% | 1.3 | $0.2M | 226 | 4.4% | 6.0 |
| 2 | 40 | 0.3% | 0.4 | $0.03M | 109 | 2.1% | 2.4 |
| 3 | 223 | 1.7% | 2.4 | $0.5M | 469 | 9.2% | 7.8 |
| 4 | 61 | 0.5% | 0.5 | $0.1M | 64 | 1.2% | 1.4 |
| 5 | 32 | 0.2% | 0.3 | $0.03M | 136 | 2.6% | 2.7 |
| 6 | 50 | 0.4% | 0.5 | $0.1M | 206 | 4.0% | 3.9 |
| 7 | 153 | 1.2% | 1.6 | $0.3M | 389 | 7.6% | 8.0 |
| 8 | 111 | 0.9% | 1.0 | $0.1M | 605 | 11.8% | 8.0 |
| 9 | 414 | 3.3% | 3.3 | $0.6M | 348 | 6.8% | 3.8 |
| 10 | 3,188 | 25.0% | 31.2 | $11.7M | 399 | 7.8% | 6.3 |
| 11 | 2,539 | 19.9% | 32.1 | $11.9M | 285 | 5.5% | 4.9 |
| 12 | 4,155 | 32.6% | 45.5 | $20.5M | 387 | 7.5% | 7.7 |
| 13 | 961 | 7.5% | 11.4 | $2.7M | 421 | 8.2% | 10.1 |
| 14 | 671 | 5.3% | 6.5 | $2.4M | 1,087 | 21.2% | 14.5 |

- **Tornado need is concentrated in three wards.** Wards 10, 11 and 12 account for an estimated 78% of the city's FEMA registrations and 86% of approved aid; in ward 12 there were about 45 registrations per 100 occupied homes. The same three wards hold 21% of residents, supplied 12% of 2024 Rams-vote participants and 10% of 2026 survey respondents, and cast 16% of April 2025 ballots.
- **Eviction filings follow a different map.** Ward 14 (downtown and the near north side) has an estimated 21% of filings and the highest rate; wards 2, 4 and 5 have the lowest rates (1.4–2.7 per 100 renter households).
- FEMA by ZIP (**observed**, Part 2 file): owners without home insurance are 53–73% of owner registrants in ZIPs 63115, 63113, 63107 and 63120, against about 30% in 63112 and 63108.

## Looked for, not found

Each part file has its own fuller list. The main items:

| Looked for | Result |
|---|---|
| A representative survey of all City residents on services or priorities, 2021–2026 | Not found. Only likely-voter polls (n=416–650) and self-selected exercises |
| A city-commissioned resident-satisfaction survey | Not found (web search only) |
| Current United Way 2-1-1 requests by ZIP (`211mo.211counts.org`) | HTTP 403 Cloudflare bot challenge, 2026-10-13 23:28 UTC; not pursued. One city-wide table for 2020–21 retrieved instead |
| Missouri Secretary of State results pages, to cross-check the Board's totals | HTTP 403 Cloudflare bot challenge, 2026-10-14 00:04 UTC; OpenElections file matched instead |
| Actual ward-capital spending or current balances by ward | Not published in the expenditure ledger, open-data catalog, capital plans or Comptroller pages. Budgets only; last balance sheet found is from 2015 for the old 28 wards |
| Option-level results of the 2023 Rams Kick-Off Survey; ward or ZIP results of the 2022 ARPA survey | Not published |
| A 2025 mayoral-race poll with an issue question | Not found; the KSDK poll page returned Access Denied |
| Utility-assistance or food-pantry data by ZIP | Not found; city-wide figures only |
| More than 3–5 Google reviews per listing; a Google listing for the city tow lot | Needs sign-in (not done); no tow-lot listing in three searches |
| An official city mobile app with reviews | None found in two App Store searches |
| A ward-by-ward results report for 4 March 2025 and 2 April 2024 | Not published; ward figures summed from precincts |
| Ballot wording inside the Board's results files | Absent; taken from the Board's sample ballots instead |
| Reporter explanations of each 2025 aldermanic result; reasons for several individual roll-call votes | Not found |
| Campaign-finance totals for the 2025 mayoral race and 2024–2026 measures | Ballotpedia has none; the state ethics commission search was not queried |
| Outcome of the November 2025 lawsuit over the citizen audit petition | Not found in two searches; court docket not consulted |
| Any recall since 2023; any current ward participatory budgeting | None found |
| Hearing remarks by member; committee vote tallies | Video only, not transcribed; tallies not found |
| St. Louis Post-Dispatch coverage | Paywalled; not read |
| Riverfront Times, Missouri Independent, Fox 2 and one KSDK article | HTTP 403 |

**Not attempted:** elections before March 2021; Google Play, Facebook, Nextdoor and Trustpilot-type sites; 988, legal-aid and findhelp data; resolution detail pages; the Board's CivicClerk minutes portal.

**Checks that would most change confidence (inferred):** the ward figures for ACS variables, FEMA registrations and eviction filings are apportioned estimates, not counts; chart-read survey counts are approximate; the bill topic labels are keyword rules with a measured error of about 2.5% on 40 bills (possibly up to 13%).
