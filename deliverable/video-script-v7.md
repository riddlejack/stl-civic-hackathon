# Video script v7: the problem first, then the fix, feature by feature

Written Thu 15 Oct 2026, early afternoon Central. Jack reviewed rough cut v4 (script v6) and asked for the whole diagnosis before any solution, every feature tied to the problem it fixes, the quotes early, North Taylor back in full, no early "ask", and the assumption stated openly. He chose order A in `deliverable/SCRIPT-ORDER-v7.md`, which holds the reasoning, the corrections to the dictation and the cut ladder. Supersedes v6.

**Shape.** 14 beats in six acts, 1171 words: about 7:10 at the scratch voice's pace, or about 6:40 at 170 words a minute. Jack's own voice is expected to run faster than the scratch voice.

| Act | Beats |
|---|---|
| 1. What 311 tells people | 1–5 |
| 2. What happens to the work | 6–8 |
| 3. What a fix needs | 9–10 |
| 4. What I built | 11 |
| 5. What changes | 12 |
| 6. The assumption and the test | 13–14 |

**Jack's choices (15 Oct):**
- "I" for what Jack did; "my AI agents and I" for the reading and analysis.
- In: the city's old definition of "closed" (beat 3); CityStat's "or because it was missed" (beat 7); the alternatives line (beat 9).
- In, merged into beat 4 with the towing quote on one screen: the 311 acting director's line to aldermen.
- Out: the Boston study line.
- No product name and no repository link on the end card.

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
> **10.** Most of this already exists. For tree removals, Forestry already attaches the crew's work order to the resident's request. Cityworks, the software the city already uses, can close that request on its own when the crew marks the job finished. And Chicago, Houston and Toronto have made it the rule: a request stays open until the work is done.
>
> **11.** So I built a working version on the city's own data, with one part for each problem. For residents: today, the North Taylor page says "Closed, on schedule to be cut." After the fix, it says "Open, no crew job linked, flagged to Forestry," and it stays open until the lot is actually cut. For the departments: every week, a list of each request that's past its promised date with no finished job, so misses get caught. The list puts the most dangerous jobs first, and each row says why. Sorted by age alone, only nine of Forestry's first 25 jobs are safety hazards. Sorted by danger, all 25 are. For City Hall: CityStat counts a request as on time once it's closed, even if the job was only passed on. So I added a column that counts only closings that say the work was done.
>
> **12.** What changes? I can't promise faster crews. What this does guarantee is that nothing falls through silently. Every miss like North Taylor would land on a list. This year, 311 told residents 479 times that a lot was "on schedule to be cut," and those lots still have no cut on record. Remember the 84 percent of overdue requests with no record either way: that's 12,566 requests where nobody can say whether the work was done, is still waiting, or was lost. By my estimate, the fix would settle about 5,000 of them in one quarter. About 1,500 just by linking work orders that already exist, and about 3,500 more by each department checking 25 a week, closing the ones that are done and re-sending the ones that were missed.
>
> **13.** My assumption is that a lot of missed and late work is work nobody can see. You don't have to take my word for it. Here's what it would take to test it: one quarter, on tree removals, cave-ins and vacant-lot mowing, measured against their baselines from the 13th of October. It needs no new software, no app, and no city data leaving the city. The saved searches, the dashboard, the SQL and a one-page practice for each division are ready. My AI agents did the audit. The city would run plain SQL.
>
> **14.** Then you'll know which promises you kept.

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
| 14 | **Which promises did St. Louis keep?** Then the end card: the closing line only, with no product name and no link |

## Screen notes for builders (what each beat must show)

| # | From v6 | Picture |
|---|---|---|
| 1 | b01 sweep | **Revised (Jack, 15 Oct): name each service's symptom, then look upstream.** Five service tiles land one per symptom sentence (s2–s6), each with its figure and population line: tree removals "39 of 40 late · median 211 days (sample of 40 status pages)"; sidewalks "54% of 2023 requests still open"; vacant lots "35% of 2026 reports: no cut on record (promise passed by 13 Sep)"; board-ups "17% done by the promised date (2025–26)"; towing "'Closed does not necessarily indicate … towed' (city's own page)". The alley-debris tile is dropped here (beat 5 covers it). s7: the three symptoms group under the tiles (late · stuck open · closed, no sign of the job). s8: the view moves up, to the source. s9: the audit-scale counters. s10: one line through all five tiles (the beat's title). s11: the two fates ("Closed" stamp; "Open · nothing attached" tag). |
| 2 | b13 quote card | The committee quote card: CHANGEforSTL Transition Advisory Committees, report to the mayor, 16 Jul 2025, p. 9. Hold it to be read. |
| 3 | b08 timeline | **Filed, closed (about day 2, hand-off bracket), promised (about day 14), recorded work (about day 35).** The archived definition appears as a small quote with the source line "CSB status definitions, archived June 2025". Shares: 18% done by the promise, about half late. |
| 4 | b13 quote cards plus `video/renders/city_towing_raw.mp4` | **One screen, two quotes** (Jack, 15 Oct). Left or first: the live CityStat Towing page (footage, framed as in b04) or its quote card, held on "Closed does not necessarily indicate that a vehicle has been towed" and "once a vehicle is actually towed". Second, landing on the director's sentence: a quote card, "…why it's past the completion date, but it's still not completed." Attribution by title only (privacy rule: public officials by title): "Acting Director, Neighborhood Stabilization Division (home of the Citizens' Service Bureau, 311) · Board of Aldermen budget hearing, 12 May 2026". Both cards stay up together. Then the counter: 61,845 hand-off closures since Jan 2025. |
| 5 | b04 | The CityStat footage, then the bar split into three: 15% "says picked up"; 45% "says later, or will investigate"; 18% "other: resident's job, referred elsewhere, no service needed". Use rebuilt shares; note 78.3% rebuilt against 78.6% published. |
| 6 | b10 plus the v5 two-report replay (`video/scenes/v5/`) | The lot, the two reports with their closing times (13 and 7 minutes), then the block's cuts landing around it. On screen, not spoken: cut 24 times in 2019–24; the block cut on 15 days in 2026. |
| 7 | b10 twin tail plus b09 tiles | The twin lot lights up (closed within the hour, cut 3 times). The 28% figure (479 of 1,724). The CityStat Forestry quote as a small card. Then the 20 tiles, with 15 dark. |
| 8 | b03 map, plus the b11 life-safety counter | 14,902 recoloured 3 / 8 / 84. Then the 2,778 subset with tree, cave-in and water icons; median 239 days. Footnote: "for 92% of them, no record either way"; tier map is ours, editable. |
| 9 | b05 fix card | One cause, then four requirements landing one per sentence. Then the alternatives (hotspot map · chatbot · new app) as small cards sitting on the same broken loop, with "ties the request to the job" missing from each. |
| 10 | b13 checkmarks | Forestry tree removals (40 of 40 attached) · Cityworks auto-close (vendor docs, St. Louis runs 23.10) · Chicago, Houston and Toronto. |
| 11 | b06 demo (`demo6_*.mp4`; `video/tools/make_demo6.py`) | **Revised 15 Oct (Jack): plainer narration; new sentence map** s1 intro · s2–3 resident page (Today, then After the fix) · s4 the weekly past-due list · s5–7 the ranked view and the 9 → 25 callout · s8–9 CityStat and the added column. Four segments, each opening on its audience line:<br>• `status.html`: North Taylor, Today then With the fix. The panel's own words: "Open · no crew job linked", "Flagged to Forestry", "Reported again: added to this open request".<br>• `queue.html`: the past-due list.<br>• `queue.html`: Ranked view and "why this rank", with the 9 → 25 comparison.<br>• `citystat.html`: the "Closing says done" column.<br>**Before re-shooting,** remove "[NAME]" from the site header and page titles (`site/config.json` `product_name`, five `<title>` tags), because no name is used. |
| 12 | b11 counter style | **Revised 15 Oct (Jack): 8 sentences.** s2 "I can't promise faster crews" · s3 "nothing falls through silently" · s4–s5 the 479 misses ("on schedule to be cut", no cut on record), each flagged · s6 **today**: 12,566 overdue requests with no record either way (done? waiting? lost?) · s7 **with the fix**: about 5,000 of them settled in one quarter, labelled ESTIMATE · s8 how: about 1,500 by linking work orders that already exist + about 3,500 by each department checking 25 a week (close the done ones, re-send the missed ones); range 2,600–7,100. |
| 13 | b14 plus b07 | Three baselines: 1,630 tree-removal work orders past Forestry's date; 1,233 cave-ins and 289 vacant-lot mowing requests past the city's date. "What working looks like": "no record either way" falls to zero for these types, and overdue counts are compared with the baseline. The three "no"s. The hand-over package glyphs. |
| 14 | b15 | The closing line, then the end card. **No product name and no link.** |

v6 b02 (thesis card), b07 (landing card), b11 ($7,000 and the 52 lots) and b12 (alternatives) are dropped as beats; their useful parts move into beats 1, 9, 12 and 13.

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
| baselines (on screen) | 1,630 of 2,504 open tree-removal work orders past their projected finish (authorised extract, 14 Oct); 1,233 cave-ins and 289 vacant-lot mowing requests open past the promise | observed | `build/E8/baselines.json` |

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

## As recorded (Jack, one take, 15 Oct)

Jack recorded the whole script in one take (7:16; `video/audio/jack/full-take.m4a`), reading the read-aloud above with his own wording in places. The take was transcribed offline (a local speech model) and aligned to this script word by word, so each scene still times itself from its sentences. Transcription: `video/tools/asr_take.py` (sherpa-onnx, offline); words with times in `video/audio/jack/full-take-words.json`. Alignment and beat files: `video/tools/align_take.py`. Where his wording differs, the script above is still the reference for timing, and the figures he says are the same as the figure table.

What differs, and what was done:
- **Beat 1:** he names tree removals, sidewalks and vacant lots, then "The list goes on." The board-up and towing tiles land on that line.
- **Beat 5:** he opens with "Calling a 311 request closed also means that the city isn't accurately tracking the completion rates and timing of its 311 requests." Kept: it is an inference, said as one.
- **Beat 6:** "No work was actually done, and the owner reported again" was **cut from the audio** (2.4 s). Two reasons: we know only that no cut is on record, and the lot's owner is the city's land bank, while who reported it is unknown. It now reads "…on schedule to be cut. Reported again on the twenty-eighth…".
- **Beat 11:** he adds "The city needs a way to prioritize overdue jobs, and I've created it in case there isn't already a working system." Kept.
- **Beat 13:** he adds that no data goes "to third-party vendors" and that the city could "audit and verify my work". Kept.
- **Beat 13:** "…are ready now. I built them out." This is now true: `deliverable/handover/` holds the saved-search spec, the dashboard definition, the SQL pointer and the one-page practices.
- **Beat 14:** "By implementing this, you'll know which promises the city actually kept."

## Recording sheet

One file per beat, named `beat_01` to `beat_14` (`.m4a` from Voice Memos or QuickTime is fine), saved in `video/audio/jack/`. Read the words exactly. One sentence per line below: leave about half a second between lines, and keep pauses at commas and colons short, especially just before a quote, so the tool doesn't mistake them for a sentence break. You don't need to pause for what's on screen; the edit adds reading time where a frame needs it.

**Beat 01** · file `beat_01` · 11 sentences

1. I came looking for problems to fix in St. Louis 311, and found one in every service I checked.
2. Tree removals: 39 of 40 finished late, a median of seven months past the promised date.
3. Sidewalks: more than half of 2023's repair requests are still open.
4. Vacant lots: a third reported this year have no cut on record.
5. Board-ups: done by the promised date only 17 percent of the time.
6. Towing: requests can be closed before the car is towed.
7. Different services, same symptoms: work late, requests stuck open, or closed with no sign the job was done.
8. So I looked upstream.
9. My AI agents and I read one and a half million requests, over two million Forestry records and 1,440 status pages.
10. They all break in the same place: once 311 hands a job to a crew, the request stops tracking the work.
11. It's closed anyway, or left open with nothing attached.

**Beat 02** · file `beat_02` · 3 sentences

1. The mayor's transition committee asked for exactly this: "Audit previously closed requests to ensure action was taken."
2. I ran that audit.
3. Here's what it found, and a fix that needs no new software.

**Beat 03** · file `beat_03` · 7 sentences

1. Every request has three dates: filed, promised and done.
2. The city's own definition used to say "closed" meant the work was finished.
3. Here's what actually happens.
4. 311 closes the request about two days after filing, at the hand-off.
5. The city promises the work in about two weeks.
6. Where I could trace the crews' work, in mowing and board-ups, only 18 percent was done by then.
7. Half came late.

**Beat 04** · file `beat_04` · 6 sentences

1. So "closed" tells a resident the job is done.
2. Often it isn't, and the city knows.
3. Its own towing page says: "Closed does not necessarily indicate that a vehicle has been towed."
4. It can mean the request was passed to the Towing Division, and the city plans to close them only "once a vehicle is actually towed."
5. And the acting head of the division that runs 311 told aldermen she wants to answer residents before they call to ask "why it's past the completion date, but it's still not completed."
6. Since 2025, 311 has closed about 60,000 requests at the hand-off.

**Beat 05** · file `beat_05` · 5 sentences

1. That "closed" also feeds the mayor's scorecard.
2. CityStat counts 79 percent of alley-debris requests as handled on time.
3. But read the closing notes: only 15 percent say the debris was picked up.
4. Almost half say it will be picked up later, or will be investigated.
5. The scorecard grades the hand-off, not the work.

**Beat 06** · file `beat_06` · 10 sentences

1. It's not only what people are told.
2. Once a request is closed, the job itself can drop.
3. This city-owned lot on North Taylor is on Forestry's mowing list.
4. Reported on the 2nd of July.
5. Closed in 13 minutes: "on schedule to be cut."
6. Reported again on the 28th.
7. Closed in seven, same words.
8. This year crews cut 36 parcels on its block.
9. Not this one.
10. No cut on record since October 2024.

**Beat 07** · file `beat_07` · 6 sentences

1. Closing fast wasn't the cause.
2. Another city-owned lot on the block was also closed within the hour, and was cut three times.
3. What's missing is any check of 311's answer against the work.
4. This year, 28 percent of "on schedule" answers went to properties with no cut on record all year.
5. Even CityStat says it can't yet tell whether an uncut lot was "mowed by someone else, or because it was missed."
6. And it's not only mowing: for 15 of the 20 most common hand-offs, not one sampled status page showed a crew job attached.

**Beat 08** · file `beat_08` · 7 sentences

1. Open requests aren't tracked either.
2. Right now, 14,902 are past the city's promised date.
3. I checked each one against every work record I could find.
4. 3 percent show the work done, 8 percent a crew job pending.
5. For 84 percent, no record says either way.
6. Among them are 2,778 life-safety requests, trees down, cave-ins, water coming up, a median eight months late.
7. The city can't tell which are done, waiting or lost.

**Beat 09** · file `beat_09` · 9 sentences

1. It comes down to one cause: the request isn't tied to the crew's job.
2. So a fix has to do four things.
3. Tie each request to its job.
4. Keep it open until the job is done.
5. Flag every request past its date with no finished job.
6. Put the most dangerous first.
7. And do it inside the systems the city already runs.
8. A hotspot map, a chatbot or a new app would all sit on top of the same broken loop.
9. None of them ties the request to the job.

**Beat 10** · file `beat_10` · 4 sentences

1. Most of this already exists.
2. For tree removals, Forestry already attaches the crew's work order to the resident's request.
3. Cityworks, the software the city already uses, can close that request on its own when the crew marks the job finished.
4. And Chicago, Houston and Toronto have made it the rule: a request stays open until the work is done.

**Beat 11** · file `beat_11` · 9 sentences

1. So I built a working version on the city's own data, with one part for each problem.
2. For residents: today, the North Taylor page says "Closed, on schedule to be cut."
3. After the fix, it says "Open, no crew job linked, flagged to Forestry," and it stays open until the lot is actually cut.
4. For the departments: every week, a list of each request that's past its promised date with no finished job, so misses get caught.
5. The list puts the most dangerous jobs first, and each row says why.
6. Sorted by age alone, only nine of Forestry's first 25 jobs are safety hazards.
7. Sorted by danger, all 25 are.
8. For City Hall: CityStat counts a request as on time once it's closed, even if the job was only passed on.
9. So I added a column that counts only closings that say the work was done.

**Beat 12** · file `beat_12` · 8 sentences

1. What changes?
2. I can't promise faster crews.
3. What this does guarantee is that nothing falls through silently.
4. Every miss like North Taylor would land on a list.
5. This year, 311 told residents 479 times that a lot was "on schedule to be cut," and those lots still have no cut on record.
6. Remember the 84 percent of overdue requests with no record either way: that's 12,566 requests where nobody can say whether the work was done, is still waiting, or was lost.
7. By my estimate, the fix would settle about 5,000 of them in one quarter.
8. About 1,500 just by linking work orders that already exist, and about 3,500 more by each department checking 25 a week, closing the ones that are done and re-sending the ones that were missed.

**Beat 13** · file `beat_13` · 7 sentences

1. My assumption is that a lot of missed and late work is work nobody can see.
2. You don't have to take my word for it.
3. Here's what it would take to test it: one quarter, on tree removals, cave-ins and vacant-lot mowing, measured against their baselines from the 13th of October.
4. It needs no new software, no app, and no city data leaving the city.
5. The saved searches, the dashboard, the SQL and a one-page practice for each division are ready.
6. My AI agents did the audit.
7. The city would run plain SQL.

**Beat 14** · file `beat_14` · 1 sentence

1. Then you'll know which promises you kept.
