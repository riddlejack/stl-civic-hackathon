# Fresh eyes: what the entry should be

Written Wednesday 14 October 2026, about 2:50 p.m. Central, by the fresh-eyes session that took over from HANDOFF-3. Read: HANDOFF-3 (Parts A, B, D; Part C read last and not relied on), Jack's eleven messages, the full kickoff transcript, Ben's written problem sets and the organiser Google Doc, the Cityworks gap review and gap matrix, R1, R2, R3 (voices and method), N7, the video script, progress report v2, the ask to Ben, the negative results, the site captures, this morning's explainer doc, and Mike's emails. One new count was run (section 2, last bullet). Nothing was built or sent.

Labels: **observed** (checked directly), **reported** (a source says so), **inferred** (my conclusion), **estimate**.

## Summary

The evidence supports a different problem statement from the one the entry has carried. "Closed is not done" is a measurement complaint. What the files show is a process gap: **St. Louis manages requests, not jobs.** 311 requests and crew work orders sit in the same Cityworks database, the schema has a request-to-work-order link, it is not populated, the request closes at the hand-off, the crew works a rotation that ignores the request, nothing flows back, and CityStat grades the hand-off. The kept-open requests show the same gap from the other side: the city's own active queue holds about 10,000 requests filed since January 2025 that are past the date the city promised, and nobody works that list.

The product that follows is not a scoreboard. It is a job tracker with an overdue queue: link, close on finish, rank the overdue, publish "done." That is cheap, needs no hiring, uses the city's own towing rule, scales to every Cityworks division, and answers Ben's problem set 3 (dumping) and design question 5 (CityStat) directly. What I could not establish: whether Cityworks already links work-order completion back to the request internally (the one question worth sending to Ben today), and the progress-report channel (none exists yet; see section 6).

## 1. What changed since this morning's explainer

The explainer said "not proven: that most hand-offs went undone." R1 settled it the other way. Of 3,640 traced hand-offs, 18.0% were done by the promise, 49.8% were done late (median 28 days), and 32.2% show no record (observed). The honest sentence is "most of the work gets done, late, and a third of mowing never shows up," not "jobs are lost."

Three results overturn the fix the explainer proposed ("a request stays open until the city's own records show the work done"):

- Requests the city **kept open** had far less recorded work than requests closed at the hand-off (no record 95.4% vs 34.9% for vacant lots; observed). Closing is not the mechanism. The loss sits in crew queues nobody reconciles against requests (inferred).
- A resident's report does not bring the crew. Requested rotation lots were cut on the same timetable as unreported lots on the same block (17.4% vs 16.9% within 14 days; observed).
- Re-reports are not a completion signal. Board-ups with no record were re-reported less than those done on time (observed).

New evidence that strengthens the thesis, in the city's own terms:

- **CityStat's on-time figures count hand-offs as on time.** Q2 2026 debris, alley or street: 78.6% as published; 15.0% counting only closings whose words say the work was done. Our rebuild matches CityStat within 0.2% on 8 of 9 measures (observed, N4 and R1). This is Ben's problem set 3, on Ben's own dashboard.
- **The city has already said it.** Towing page: "Closed" "does not necessarily indicate that a vehicle has been towed"; the city plans to close only "once a vehicle is actually towed." The acting director of the division that runs 311: residents ask "why it's past the completion date, but it's still not completed." Transition committee: "Audit previously closed requests to ensure action was taken." Forestry commissioner: "we have all this data but we don't have somebody on staff" to analyse it (observed, R3; ten confirmed live 14 Oct).
- **Tree planting:** 65.0% of 806 "approved for next available planting" requests were planted, 0.2% by the 14-day promise, median 133 days late; 43 confirmed still waiting 8 to 16 months in Forestry's own planting queue (observed, R2).
- **Jack's Cityworks extraction (14 Oct, 1:48 to 1:53 p.m.):** 29,018 distinct work orders. Sidewalks: 16 of 186 hand-offs have a later repair at the address, all after the promise, median 179.5 days late. Tree trimming: 89 of 572 converted requests have a chronology-valid finish; 6 by the promise, 83 later, median 218 days. No request-to-work-order key is returned although the schema advertises one. 1,750 Forestry finishes are dated before the order was opened. `Completed=1` is set on 9,165 requests the public file still shows open, so the city's internal flag is not completion either (observed).
- **The live overdue queue (new today; observed, one pass, not yet independently checked; derivation below).** The city's "Active SRs" saved search, restricted to the 61 operational codes in the register, holds 19,291 open requests; 18,100 are past their own promise date as of 13 Oct. Of those filed since 1 January 2025: 10,094 are past the promise; 4,528 by more than six months. By division: Forestry 4,327 (median 125 days past), Street Department 2,616 (162), Building Division 1,068 (153), Water 506 (324). By type: inspect city tree 1,479; cave-ins 1,204; sidewalk repair 1,115; weeds on occupied property 1,042; vehicle towing 418. The promise dates match the public file in 18,972 of 18,976 joined rows. Past promise does not mean negligence; it is the backlog the city set dates against, and no list ranks it.

Complications 3 (ward gap) and 4 (July to September potholes): Jack's "who cares" stands. The method memo agrees (Kepner-Tregoe treats the ward gap as a separate problem with an untested cause). Cut both from the story.

Derivation of the queue count: `data/raw/cityworks-gap/authorized/layer_18_page_*.json` (QE18, retrieved 14 Oct 2026 18:48 to 18:53 UTC, fields `RequestId`, `DateTimeInit`, `PrjCompleteDate`, `Completed`, `WONeeded`, `Status`), deduplicated on `RequestId`, left-joined to `requests` in `build/stl.duckdb` for `submit_to` and `problem_code`; "past promise" is `PrjCompleteDate` before 2026-10-13 23:59:59 Central. Not yet registered in `figures.json`.

## 2. What the entry should be, and why

**Problem statement.** The city manages requests, not jobs. A 311 request closes when it is handed to a crew; the crew's work order lives in the same database but is not linked back; the crew works a rotation or queue that the request does not move; CityStat grades the close, not the work. Two symptoms, one cause: hand-off closures nobody reconciles (61,845 in 2025 to 2026; where traceable, 18% done by the promise) and kept-open requests nobody ranks (about 10,000 past promise today).

**Product.** A job tracker with an overdue queue. Four rules, plain SQL, no AI in the product, nothing to buy:

1. **Link.** Every request carries its work order. The field exists in Cityworks; populate it.
2. **Close on finish.** The request closes when the work order's actual finish date is set, not at the hand-off. This is the city's own towing rule, applied to every service.
3. **Queue.** Every weekday, every job past its promise with no finish goes on its division's list, oldest first, at block level on a map. That is the geospatial ask answered with a purpose, not a map for its own sake.
4. **Publish.** CityStat gets the column "done by the promise." The resident's status reads "in Forestry's queue since 2 July, promised 30 September," not "closed."

**Why this shape.**

- It is what Ben would recognise: CityStat is his instrument, the towing change is his plan, and the first number is his dumping measure.
- It is what Mike asked for: built, open source, deployable, on the mayor's desk, with a resident's story.
- It needs no hiring, and it scales: QE18 shows 22 division labels in the active queue, so any Cityworks division joins the same queue with no new data.
- It answers problem set 3 without surveillance (259 repeat blocks produce 38% of dumping reports; hand-offs closed "will be investigated" with no clean-up record since 2021) and design question 5 directly. It touches problem set 1 (280 approved trees with no planting record; 8,412 city-owned lots mowed for $1.31M in 2026).
- It is what a forward-deployed engineer would build: not a dashboard, the join plus the queue plus the escalation rule.

**The "so what" in one line.** Monday morning, each division head opens a list of jobs the city promised and has not finished, oldest first, and residents stop being told "closed" for work nobody has scheduled.

**What it does not claim to do.** It does not add crews. It changes which jobs crews go to first and makes the misses visible. Whether visible misses get fixed is the bet; the honest ask is one quarter's trial on the services with records.

## 3. The strongest honest claim, and the claims we must not make

**Strongest honest claim (every figure observed).** "The city grades the hand-off, not the job. CityStat says 79% of alley debris is cleaned on time; counting only closings that say the work was done, it is 15%. Where the work could be traced, 311 had closed 85% of requests by the promise; 18% were done by it, half were done a median four weeks late, and a third show no record. This week the city's own system holds about 10,000 requests filed since January 2025 that are past the date it promised, and no one works that list."

**Must not say.**

- "35% of jobs aren't done." The 35% is hand-off closures; most traced ones were done, late.
- "Closing early loses the work." Kept-open requests fare worse.
- Any equity or "the north waits longer for crews" claim. No gap on the no-record measure; the first-step gap has no tested cause.
- "Re-reports prove undone work."
- "No cut billed means not cut." It is a billing record; say "no record of a cut."
- "This will clear the backlog" or "more jobs will get done." Say "visible, ranked, cheap to try for one quarter."
- "Exactly reproduces CityStat." Within 0.2%.
- The 1,700 to 3,500 never-done figure as a finding. It is an estimate on mowing and board-up rates; label it or leave it out of the video.
- Anything that hides how the Cityworks data was obtained. State it: authorised at office hours, operational fields only, no personal data, raw data not published.

## 4. Before Thursday 5:30 p.m., in priority order

1. **Decide the shape, now.** Everything below assumes the job-tracker frame.
2. **Progress report today, about 4 p.m. (Jack sends).** No channel exists: the organiser Google Doc has no submission folder, and Mike's reply last night says he is still asking the judges (he suggested a Dropbox link for the repo and YouTube for the video). Reply on the existing thread with Mike. Rewrite v2: drop "a request stays open until verified"; lead with the 79/15 debris figure, the traced fates and the queue. Separately, add a name and one-line idea to the Google Doc's team tab under "All ideas welcome"; only one team has signed up (problem set 3), and Mike said he would share ideas with Ben.
3. **Build the queue from the live Cityworks extract (tonight, about two hours).** Second-pass check of the 10,094 and 18,100 figures; by division, type, ward group and age bucket; block-level map; register each figure with its derivation. This is the product's main screen, on the city's own data.
4. **Re-centre the site (tonight).** Landing: the 79/15 number and the queue count. Receipt stays. The Monday brief becomes "The queue" (lists by division, oldest first, map). The dumping page is reframed as the problem set 3 answer. The scoreboard stays, with its done-by-promise column. Fairness moves to a methods appendix. The July to September pothole drop leaves the story.
5. **Script tonight, record Thursday morning.** One number (79 vs 15), one case (lot-1), the mechanism (same database, no link, 10,000 past promise), the queue screen, the ask. About 250 words.
6. **One question to Ben through Mike, today if Jack is willing.** Does Cityworks link work-order completion back to the request, and can that link be exported? "Yes" makes the entry "publish and manage to it"; "no" makes it "turn it on."
7. **Publish a clean repository** from an allowlist, with the disclosure line updated and a methods note on Cityworks provenance. The current repository cannot be published as it stands (N8 finding 4).
8. **Skip.** More data hunting, satellite checks, a canopy pivot, further fairness work, and merging R-figures into the registry beyond what the site uses.

## 5. What survives, what changes, what is cut

**Survives.** The pipeline (about 20 seconds, no key, no AI); the closure classes and the 25-service register; the CityStat reproduction and the done-by-promise column; the receipt; lot-1 and the counter-example; the dumping page (reframed); R1, R2 and R3; the voices table; the negative results; the choices log; the line "AI did the audit; the product has none."

**Changes.** The lead, from "closed is not done" to "the city manages requests, not jobs." The fix, from "keep open until verified" to "link, close on finish, queue the overdue." The Monday brief, from a report to the queue. Progress report v2 (its fix sentence is wrong). The ask to Ben (one question, not five). The explainer doc (superseded on the fix and on complications 3 and 4). The name: DoneStat still fits; "the job tracker" says what it does.

**Cut.** Fairness as a headline section; the Q3 pothole drop; the "one weekly job, three users" framing; storyboards A, B and C as written (A's second act is fairness; C opens on numbers). The site's three-door structure can stay as navigation.

## 6. The check-in today (observed from Jack's inbox, 14 Oct)

- Mike's email at 12:31 p.m. Central: a Teams "Day 2 check in office hours" at 2 p.m. today, and the Google Doc with the challenges. The doc's team tab lists one team (problem set 3: Ibidun Isaac, Faiz Ikramulla). It has no submission instructions.
- Mike's reply to Jack, 13 Oct 9:15 p.m.: "talking with the judges about their preferred submission method. I thought a Dropbox link for the build repo and 2-minute storytelling screen share video uploaded to YouTube."
- Kickoff (00:36:30): "around four or five o'clock … submit your progress report, what are you working on … I've had this pivot."
- The published schedule says Wednesday by 8 p.m. (HACKATHON_CONTEXT, section 6; not reconciled).

So: no folder exists. The practical route is an emailed progress report on the existing thread, with a line asking where Thursday's link should go.

## 7. Decisions for Jack

1. The shape: job tracker with an overdue queue (recommended), or keep DoneStat as a measurement product.
2. Send the progress report today on the thread with Mike, and add a line to the Google Doc.
3. Send the one question to Ben through Mike.
4. Whether to build item 3 of section 4 tonight.
