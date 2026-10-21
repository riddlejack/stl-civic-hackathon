# Video script v7: the problem first, then the fix, feature by feature

**Shape.** 14 beats in six acts, 1171 words: about 7:10 at the scratch voice's pace, or about 6:40 at 170 words a minute.

| Act | Beats |
|---|---|
| 1. What 311 tells people | 1–5 |
| 2. What happens to the work | 6–8 |
| 3. What a fix needs | 9–10 |
| 4. What I built | 11 |
| 5. What changes | 12 |
| 6. The assumption and the test | 13–14 |

## Read-aloud (one file per beat; leave a half-second pause between sentences)

> **1.** I came looking for problems to fix in St. Louis 311, and found one in every service I checked. Tree removals: 39 of 40 finished late, a median of seven months past the promised date. Sidewalks: more than half of 2023's repair requests are still open. Vacant lots: a third reported this year have no cut on record. Board-ups: done by the promised date only 17 percent of the time. Towing: requests can be closed before the car is towed. Different services, same symptoms: work late, requests stuck open, or closed with no sign the job was done. So I looked upstream. My AI agents and I read one and a half million requests, over two million Forestry records and 1,440 status pages. They all break in the same place: once 311 hands a job to a crew, the request stops tracking the work. It's closed anyway, or left open with nothing attached.
>
> **2.** The mayor's transition committee asked for exactly this: "Audit previously closed requests to ensure action was taken." I ran that audit. Here's what it found, and a fix that needs no new software.
>
> **3.** Every request has three dates: filed, promised and done. The city's own definition used to say "closed" meant the work was finished. Here's what actually happens. 311 closes the request about two days after filing, at the hand-off. The city promises the work in about two weeks. Where I could trace the crews' work, in mowing and board-ups, only 18 percent was done by then. Half came late.
>
> **4.** So "closed" tells a resident the job is done. Often it isn't, and the city knows. Its own towing page says: "Closed does not necessarily indicate that a vehicle has been towed." It can mean the request was passed to the Towing Division, and the city plans to close them only "once a vehicle is actually towed." And the acting head of the division that runs 311 told aldermen she wants to answer residents before they call to ask "why it's past the completion date, but it's still not completed." Since 2025, 311 has closed about 60,000 requests at the hand-off.
>
> **5.** That "closed" also feeds the mayor's scorecard. CityStat counts 79 percent of alley-debris requests as handled on time. But read the closing notes: only 15 percent say the debris was picked up. Almost half say it will be picked up later, or will be investigated. The scorecard grades the hand-off, not the work.
>
> **6.** It's not only what people are told. Once a request is closed, the job itself can drop. This city-owned lot on North Taylor is on Forestry's mowing list. Reported on the 2nd of July. Closed in 13 minutes: "on schedule to be cut." Reported again on the 28th. Closed in seven, same words. This year crews cut 36 parcels on its block. Not this one. No cut on record since October 2024.
>
> **7.** Closing fast wasn't the cause. Another city-owned lot on the block was also closed within the hour, and was cut three times. What's missing is any check of 311's answer against the work. This year, 28 percent of "on schedule" answers went to properties with no cut on record all year. Even CityStat says it can't yet tell whether an uncut lot was "mowed by someone else, or because it was missed." And it's not only mowing: for 15 of the 20 most common hand-offs, not one sampled status page showed a crew job attached.
>
> **8.** Open requests aren't tracked either. Right now, 14,902 are past the city's promised date. I checked each one against every work record I could find. 3 percent show the work done, 8 percent a crew job pending. For 84 percent, no record says either way. Among them are 2,778 life-safety requests, trees down, cave-ins, water coming up, a median eight months late. The city can't tell which are done, waiting or lost.
>
> **9.** It comes down to one cause: the request isn't tied to the crew's job. So a fix has to do four things. Tie each request to its job. Keep it open until the job is done. Flag every request past its date with no finished job. Put the most dangerous first. And do it inside the systems the city already runs. A hotspot map, a chatbot or a new app would all sit on top of the same broken loop. None of them ties the request to the job.
>
> **10.** Most of this already exists. For tree removals, Forestry already attaches the crew's work order to the resident's request. Cityworks, the software the city already uses, can close that request on its own when the crew marks the job finished. And Chicago, Houston and Toronto have made it the rule: a request stays open until the work is done. I didn't try to rebuild the city's 311 system; it already has one. The value is the audit underneath: the city's 311 file, Forestry's billing records, its Cityworks work orders and 1,440 status pages, joined request by request. That analysis is written as plain SQL and saved searches that plug into the systems the city already runs: Cityworks, CityStat and the 311 status page. The website is a demo of what that looks like, running on real city data.
>
> **11.** So I built a working version on the city's own data, with one part for each problem. For residents: this is what the city's 311 status page shows today: "Closed, on schedule to be cut." With the fix, the same request stays open, linked to the crew's job and its due date, until the lot is actually cut. For the departments: every week, a list of each request that's past its promised date with no finished job, across every division. It filters by type, by life-safety versus less urgent work, and by how late it is, and the map follows the filters. The list puts the most dangerous jobs first, and each row says why. Sorted by age alone, only nine of Forestry's first 25 jobs are safety hazards. Sorted by danger, all 25 are. And each department can set its own weights for what counts as urgent. For City Hall: every CityStat 311 measure, rebuilt from the city's own file, with one more line for the closings that say the work was done. So the scorecard shows where the closings and the work part ways, measure by measure.
>
> **12.** What changes? I can't promise faster crews. What this does guarantee is that nothing falls through silently. Every miss like North Taylor would land on a list. This year, 311 told residents 479 times that a lot was "on schedule to be cut," and those lots still have no cut on record. Remember the 84 percent of overdue requests with no record either way: that's 12,566 requests where nobody can say whether the work was done, is still waiting, or was lost. By my estimate, the fix would settle about 5,000 of them in one quarter. About 1,500 just by linking work orders that already exist, and about 3,500 more by each department checking 25 a week, closing the ones that are done and re-sending the ones that were missed.
>
> **13.** My assumption is that a lot of missed and late work is work nobody can see. You don't have to take my word for it. Here's what it would take to test it: one quarter, on tree removals, cave-ins and vacant-lot mowing, measured against their baselines from the 13th of October. It needs no new software, no app, and no city data leaving the city. The saved searches, the dashboard, the SQL and a one-page practice for each division are ready. My AI agents did the audit. The city would run plain SQL.
>
> **14.** By implementing this, residents would see the truth about their requests: open until the work is done, not "closed" the day it's handed off, so they don't have to call to find out why. Missed jobs would stop falling through the cracks, because every miss lands on someone's list. And the most urgent work, trees down, cave-ins, water coming up, would rise to the top of that list every week. The city wouldn't just know which promises it kept. It would see every promise it hasn't kept yet, and could keep the most urgent ones first.

## Action titles

| # | On-screen action title |
|---|---|
| 1 | **Five services, one problem: once the job goes to a crew, the 311 request stops tracking the work** (the audit's scale beneath) |
| 2 | **The mayor's transition committee asked for this audit (July 2025)** |
| 3 | **311 closes in about 2 days; only 18% of traced work was done by the promised date** |
| 4 | **The city already knows "closed" isn't "done"** (two quotes on one screen: the towing page and the 311 acting director) |
| 5 | **CityStat: 79% on time. Closings that say the debris was picked up: 15%** |
| 6 | **Reported twice, closed in minutes, "on schedule to be cut": no cut on record since October 2024** |
| 7 | **Nothing checks 311's answer against the work: 15 of the 20 most common hand-offs attach nothing** |
| 8 | **14,902 open requests past the city's date: for 84%, no record says whether the work was done** |
| 9 | **One cause, four requirements: tie the job · keep it open · flag the misses · danger first** |
| 10 | **Already done in St. Louis for tree removals, and the rule in Chicago, Houston and Toronto** |
| 11 | Four segments: **For residents: "open" until the job is done** · **For departments: a weekly list of the misses** · **Danger first, with the reason on every row** · **For City Hall: count only work that says it's done** |
| 12 | **Nothing falls through silently: about 5,000 unexplained requests accounted for in one quarter (estimate)** |
| 13 | **What it would take to test it: one quarter, three request types, measured against 13 October** |
| 14 | **What changes: residents see the truth · misses land on a list · urgent work first** Then the end card: "Which promises did St. Louis keep?", with no product name and no link |

## Figures behind each spoken number

| Spoken | Value | Label | Source |
|---|---|---|---|
| one and a half million requests; over two million Forestry records; 1,440 status pages | 1,454,222 (2008–2026); 2,252,031 ledger rows; 1,440 | observed | `research/credibility-tally.md` |
| 39 of 40 tree removals late; seven months | 1 of 40 sampled tree-removal requests done by the 14-day promise; 39 late, median 211 days | observed | `research/status-page-linkage.md` (E1 table) |
| more than half of 2023's sidewalk requests still open | 54.4% of 2023 Sidewalk Repair filings open on 13 Oct 2026 | observed | `research/open-queue-reality-check.md` |
| a third of this year's vacant-lot reports, no cut on record | 34.9% of 631 2026 Weeds-Vacant Lot requests whose promise passed by 13 Sep | observed | `research/chapters/R1-trace.md` |
| board-ups 17 percent by the promised date | 17.0% of 1,528 "referred to board-up crew" hand-offs, 2025–26 (the board-up layer lags; see R1) | observed | `research/chapters/R1-trace.md` |
| towing closed before the car is towed | CityStat Towing page | observed live 14 Oct | `research/chapters/R3-voices.md` row 1 |
| "Audit previously closed requests to ensure action was taken" | CHANGEforSTL Transition Advisory Committees, report to the mayor, 16 Jul 2025, p. 9 (volunteer advisers) | observed (saved PDF; Wayback page opened 14 Oct) | `research/chapters/R3-voices.md` row 2 |
| "closed" meant the work was finished | "the work indicated by the problem code has been finished by the department" (archived 22 Jun 2025; live page "Inactive Content" since about Sep 2025) | observed (archive and live page) | `research/precedents-closed-loop.md` A2 |
| about two days; about two weeks; 18 percent; half late | median 1.8 days to close; median promise 14 days; 18.0% done by the promise; 49.8% late (n = 3,640 traceable weed-cut and board-up hand-offs) | observed | `research/chapters/R1-trace.md`; `build/R1/fate_summary.json` |
| towing quote; "once a vehicle is actually towed" | CityStat Towing page (data to 30 Jun 2026) | observed live 14 Oct | `research/chapters/R3-voices.md` row 1 |
| "why it's past the completion date, but it's still not completed" | Karen Clifford, Acting Director, Neighborhood Stabilization Division (houses the CSB, 311), Budget & Public Employees Committee, 12 May 2026, about 3:31:10 ([hearing video](https://www.youtube.com/watch?v=tyS2V5Ae98I)) | observed (hearing page opened 14 Oct; words from the saved auto-captions) | `research/chapters/R3-voices.md` row 3 |
| about 60,000 at the hand-off since 2025 | 61,845 hand-off closures, Jan 2025–Oct 2026 (includes about 4,300 "bulk week"-type deferrals, also closed before the work) | observed | `research/chapters/R1-trace.md`; `research/closure-class-review.md` |
| 79 percent; 15 percent; almost half | 78.6% published (78.3% rebuilt, n = 572 closed Q2 2026); 86 of 572 say done; 260 of 572 (45.5%) say "bulk will be picked up in correct week" (151), "collection will be made next scheduled day" (3) or "matter will be investigated" (106), all on time | observed | `research/closure-class-review.md` §2 |
| 13 minutes; seven; 36 parcels; no cut since October 2024 | 12.5 and 7.4 minutes; 36 parcels cut in 2026, on 15 days; last cut billed 2024-10 | observed | `research/north-taylor-mechanism.md`; `build/north-taylor/mechanism.json` |
| another lot closed within the hour, cut three times | same-block land-bank lot: 5 reports closed in 3.8–58.7 minutes; 3 cuts in 2026 | observed | same |
| 28 percent | 479 of 1,724 2026 "on schedule to be cut" weed reports, on parcels with no cut billed in 2026 | observed | same |
| "mowed by someone else, or because it was missed" | CityStat Forestry page (data to 30 Jun 2026) | observed live 14 Oct | `research/chapters/R3-voices.md` row 4 |
| 15 of the 20 most common hand-offs | 0 of 40 sampled pages each; about 22,800 requests in those 15 | observed | `research/status-page-linkage.md` |
| 14,902; 3 percent; 8 percent; 84 percent | 14,902 open past the promise (filed since 1 Jan 2025, file of 13 Oct 2026); 2.6%; 8.1%; 84.3% | observed | `research/open-queue-reality-check.md` |
| 2,778 life-safety; eight months | 2,778; median 238.5 days past the promise; 2,562 (92%) with no record either way | observed (tier map ours, editable: `site/data/rank-weights.json`) | `research/impact-quantification.md` §4b |
| Forestry attaches work orders to tree removals | 40 of 40 sampled tree-removal requests list their work orders | observed | `research/status-page-linkage.md` |
| Cityworks closes a linked request when the job closes | Cityworks 23 documentation; St. Louis runs 23.10 | observed (vendor docs) | `research/precedents-closed-loop.md` A2 |
| Chicago, Houston, Toronto | Chicago: by design, per its inspector general (Feb 2026); Houston: A.P. 2-23 (2022); Toronto: 2023 budget note | observed (primary documents) / reported (practice) | same, B1 |
| nine; all 25 | Forestry top 25: 9 life-safety rows age-sorted against 25 ranked | observed | `research/prioritisation-option.md`; `site/data/ranked.json` |
| 311 told residents 479 times "on schedule to be cut"; no cut on record | 479 of 1,724 2026 "on schedule to be cut" reports, on parcels with no cut billed in 2026 (as the 28% row) | observed | `research/north-taylor-mechanism.md` |
| about 5,000 of the 12,566 | 5,008 central (2,557–7,099): about 1,526 from linking existing work orders, plus about 3,482 from reviewing 25 a week per division in 14 divisions over 13 weeks | estimated | `research/impact-quantification.md` §5 |
| baselines (on screen) | 1,630 of 2,504 open tree-removal work orders past their projected finish (extract, 14 Oct); 1,233 cave-ins and 289 vacant-lot mowing requests open past the promise | observed | `build/E8/baselines.json` |

## Not said, deliberately

- **That the 14,902, the 2,778 or the 1,630 were closed early.** They are open.
- **That crews will be faster, or that the backlog clears.** Beat 12 says so out loud.
- **"Never cut".** The script says "no cut on record".
- **That closing fast caused the North Taylor miss.** The twin shows it didn't.
- **That Forestry's tracking is accurate.** Its linked tree removals are still late.
- **That the city works its queue oldest-first, or ranks nothing.** The 9 → 25 compares two sorting rules; it is not a claim about current practice.
- **Repeat-request savings, labour saved by auto-close, the $7,000 lot-cutting cost.**
- **Outcomes in other cities.** Only their rules are cited.
- **Any equity claim.**
- **That AI is in the product.**
