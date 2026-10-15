# Brainstorm v6: what would make a judge pick this

Written Thursday 15 October 2026, 23:56 (14 Oct) to 00:03 Central (clock checked at 23:56, 00:00 and 00:03), by a fresh-eyes session. Read: `AGENTS.md`, `context/HACKATHON_CONTEXT.md`, `context/BEN-PROBLEM-SETS.md`, `deliverable/video-script-v5.md`, `deliverable/RESTRUCTURE-v5.md`, `video/review/QA-v3.md`, `video/review/DOCTRINE-for-video.md`, the eight evidence files named in the brief, `context/FRESH-EYES-ASSESSMENT.md` §3, `research/data-audit.md` (summary), `research/chapters/N4-citystat.md` (tables), `research/chapters/R2-beyond.md` (§1), and three v5 stills (`video/review/v5_b09_final.png`, `v5_b14_last.png`, `v5_b15_10.8.png`). Four read-only DuckDB queries were run tonight (Appendix A). Nothing else was edited. Figures beside this file: `research/brainstorm-v6-facts.csv`.

Labels: **observed** (I checked it in a file or ran the query), **reported** (a source says so), **inferred** (my judgement), **estimate** (rests on a stated assumption).

## Summary

**Found.** v5 is accurate and well built, and it loses for reasons that have nothing to do with accuracy. It opens on one person's hunt for one broken service, so the judge never learns that the finding is a single failure mode found across six services and 1.5 million requests. It proves the problem for 1:52 and gives impact one beat, as a ranking statistic. It never names the alternatives a judge is comparing it with, never shows the city's own pages, and reaches the real product at 4:08, after the two minutes the organisers asked for. Every number needed to fix this is already observed in `research/`; three counts were added tonight (Appendix A). The honest impact numbers are not dollars. They are counts the city can stop doing: 36,705 hand closings in 2025, about 20,700 repeat filings for the same problem at the same address, 2,576 life-safety items past the promised date with no finished job on record, and 1,206 residents who could be told "your job is scheduled" today with no new work.

**Could not establish.** A cost per 311 intake or per status call (no city figure found tonight; the impact agent should look in the FY2027 budget book for CSB's cost and call volume, or state an assumption). Whether the 20,697 repeat filings are mostly recurring services (refuse, weeds): the durable-type subset is 2,534, so the headline must be split before it is spoken. Whether the public 311 status page can be screen-recorded without showing an address (it probably shows one; crop or mask, or record a city-owned tree request).

## (a) Diagnosis in five lines (inferred)

1. **The opening undersells the work.** "I came looking for one broken service" frames a chance discovery. The truth is an audit of six services (tree removal, sidewalks, mowing, board-ups, towing, alley debris; plus planting) that found one failure mode. The scale of that audit, which is the entry's only unfair advantage, is never on screen.
2. **Problem 1:52, impact 0:24.** Beats 3–11 prove the gap three times over (84%, 15 of 20, the twins); the "so what" for residents, crews and the mayor is a single ranking statistic (9 → 25), which a judge reads as a feature, not an outcome.
3. **The alternatives are never named**, so the judge compares "SQL and a practice memo" with a hotspot map on surface appeal, instead of with the fact that a map cannot tell you whether the crew came.
4. **Drawn, not shown.** The product appears at 4:08 for 25 s; the city's own CityStat and status pages, which are the thing the fix changes, never appear. Question 5 ("look at CityStat and tell us what doesn't resonate") is answered in the abstract.
5. **Adoption is a slogan ("nothing to buy"), not an argument.** The four facts that make it a practice change rather than a procurement (the link field exists; Cityworks 23 auto-closes a linked request; the city already wrote the rule for towing; the transition committee asked for the audit) are scattered or unspoken.

## (b) Ideas, ranked by effect on a judge

Build cost is agent-hours on the existing kit (`video/scenes/kit.py`, `illus.py`, `basemap.py`) and site. "Evidence" names the file where every figure is observed.

| # | Idea | Why it persuades | Evidence / computation | Cost |
|---|---|---|---|---|
| 1 | **Open on the sweep, not the anecdote.** Six tiles, each a service with its own observed symptom landing one at a time, then one line through all six: "The request closes at the hand-off. The job lives somewhere else. Nothing joins them." Under the tiles, the audit's scale: 1.5 million requests, 2.25 million forestry records, 29,018 work orders, 1,440 status pages, 11 cities, 53 city statements. | Reframes the finding as aggregate (Jack's point), gives the credibility the film lacks, and makes the boring fix the obvious conclusion rather than a preference. | Tile figures (all observed): tree removal 1 of 40 finished by the 14-day promise, median 211 days late (`status-page-linkage.md`); sidewalks 16 of 186 hand-offs traceable, all late, median 179.5 days (`cityworks-gap-review.md`); mowing 18% done by promise, 32% no record (`chapters/R1-trace.md`); board-ups 17% by promise, 65% late (R1); towing: city's own "Closed does not necessarily indicate … towed" (`chapters/R3-voices.md` row 1); debris 79% on time, 15% closings say picked up (`closure-class-review.md`). Scale: `data-audit.md` summary; gap review; E1; `precedents-closed-loop.md` B1; R3. | New scene, 2 h (reuses the four b01 vignettes) |
| 2 | **Real product inside the first two minutes** (demo at about 1:08, 40 s): queue Oldest → Ranked with "why this rank"; the resident page Today vs With the link; CityStat with the added column; the data page showing the facts file. Fix QA-v3 #1 first (the lot page must read "no job linked"). | The brief asked for a two-minute screen share. A judge who stops at 2:00 currently sees no product. The site is more convincing than any diagram of it (`v5_b15_10.8.png` is already the best-looking frame). | `research/chapters/E6-site.md`; `video/tools/record_demo.py` | Re-shoot, 1.5 h |
| 3 | **An impact beat with three counted numbers and stated assumptions** (see "What to quantify" below): repeat filings, life-safety items past date, residents who could be told "scheduled" today. Plus one hours figure labelled *estimate*. | Answers "I don't believe in the impact". Counts the city can act on beat invented dollars, and none crosses a must-not if worded as below. | Appendix A queries; `open-queue-reality-check.md` (b = 1,206; Inspect City Tree 892); `prioritisation-option.md` (Tier 1 = 2,991 in base, 2,778 ranked; top 15 are 330–582 days past promise, each reported 2–4 times). | New scene, 1.5 h; impact agent 2 h |
| 4 | **Real city pages on screen** (5 s each): CityStat Streets showing 78.6%; the CityStat Towing note; one public status page reading "For detailed information, please contact the Citizens' Service Bureau" where the closing words should be (7,845 requests in four hand-off types hide them). | Question 5 answered on the city's own page; a wow that costs nothing; proof the gap is visible to any resident today. | R3 rows 1, 5; `status-page-linkage.md` ("hides the promise"). Robots: stlouis-mo.gov allows these paths (R3 fetched them live 14 Oct); use Jack's browser; crop to block level or below-address fields. | 1 h |
| 5 | **"Why not the alternatives" card** (12 s): five columns, each with what it needs: hotspot map (where, not whether); chatbot (a new channel, same closed loop behind it); outreach app (residents must adopt it); new vendor (a year and a contract); data to model makers (city data leaves the city). Ours: a field the city has, a rule the city wrote for towing, no resident adoption, no data leaving. | Jack's strongest argument, currently absent. It also says why problem set 3's dumping map needs this first: "matter will be investigated" closes 93% on time and no clean-up is recorded. | `closure-class-review.md` (114 of 572 debris closings "investigated", 93% on time); FRESH-EYES §2 (259 repeat blocks = 38% of dumping reports; no clean-up record since 2021). No straw men: say each alternative is useful *after* the loop closes. | New card, 1 h |
| 6 | **"Already true" adoption card** (12 s): (1) the request-to-work-order link exists and Forestry uses it, 40 of 40 tree removals; (2) Cityworks 23 closes a linked request when the work order closes, no setting needed, and St. Louis runs 23.10; (3) the city has already written this rule for towing; (4) the mayor's transition committee asked for exactly this audit. One line of precedent: Chicago closes only with the last work order; Houston and Toronto put "stay open until done" in policy. | Turns "nothing to buy" into a four-fact argument that the ask is a memo, not a procurement. | `precedents-closed-loop.md` A2 and B1; R3 rows 1 and 2; E1. | New card reusing b11/b16 quote cards, 1 h |
| 7 | **The scorecard with a second column, for nine services, not one.** Show N4's table: closed by due date vs closed *as done* by due date: towing 22% → 0.2%; cave-ins 27% → 4%; tree inspections 21% → 4%; refuse 79% → 34%; major potholes 20% → 12%. | Makes the CityStat beat a system finding, and feeds the citystat.html column. | `chapters/N4-citystat.md` table at line 123 (observed; N4's own due-date definition, not CityStat's published measures except debris; label it so). | Query check 0.5 h; scene 1 h |
| 8 | **Speak the 28% line** in the North Taylor beat (QA-v3 #3) and cut the beat to 20 s. | The one sentence that makes the lot a mechanism, not an anecdote. | `north-taylor-mechanism.md` (479 of 1,724). | 0.2 h |
| 9 | **Pacing to 4:15 with the pitch complete at 2:00.** Cut b06 into b07; drop b11 as a beat (its quote moves to idea 6); shorten b12 to 12 s (the three steps are re-explained by the demo); b09 absorbs b03's counter. | QA-v3 measured the drag; Jack's voice will run faster than TTS. | QA-v3 cut list. | 0 h (removals) |
| 10 | **Problem-set links said once, plainly:** "This answers the city's question 5 with one column, and it is what problem sets 1 and 3 need underneath them: 65% of approved plantings planted, 0.2% by the promise, median 133 days late; dumping closes 'investigated' with no clean-up on record." | Judges will score against Ben's document. | `chapters/R2-beyond.md` (806 plantings); FRESH-EYES §2. | 0.3 h (voice line on idea 5's card) |
| 11 | Optional wow: an audit counter that ticks 1,502,836 → 2,252,031 → 1,440 → stops on "one failure mode". | Cheap drama from true numbers. | data-audit.md | 0.5 h (kit `Counter`) |
| 12 | Optional: the 2024 6-inch aerial of the twin lots at block level. | Real imagery beats a schematic. | `data-audit.md` (imagery available). Privacy: city-owned land, block level only; skip if any doubt. | 1 h |

**What to quantify for the impact beat, and how (for the impact agent).** Spoken numbers must be counts of things the city does or residents do; dollars only as a labelled estimate with the assumption on screen.

- **Repeat filings (residents' time; CSB intake).** Observed tonight: 20,697 requests filed in 2025 were filed within 90 days of an earlier request with the same problem code at the same normalised address (16.7% of 124,077); 8,145 of them followed a hand-off closure. Durable (non-recurring) types only: 2,534, of which 1,700 came through resident channels. Compute: split by `refiled.durable`, by family, and report both; show median days to the repeat; exclude refuse and weeds from the headline or say "including recurring services". Must-not: never say repeats prove undone work (R2 §1). Say "a resident reporting the same thing again". Hours: 20,697 × an assumed 8 minutes per report ≈ 2,800 resident-hours a year (*estimate*; state the minutes on screen).
- **Hand closings (staff labour).** Observed: 36,705 requests filed in 2025 were closed as hand-offs (class `handed_off`), each closed by hand at the moment Cityworks could close it automatically on the work order's finish. Hours: 36,705 × an assumed 1–2 minutes ≈ 600–1,200 staff-hours (*estimate*). Also observed: 2,565 closings in 2025 told the resident to "call CSB for details".
- **Life-safety items past the promised date.** Observed: Tier-1 types in the open past-promise base: cave-ins 1,233, tornado street debris 365, city tree down 323, broken/hanging limb 307, limb down 269, building collapse 79 (2,576 in these six; 2,991 in all Tier-1 types). Hazard-days: sum of days past promise over Tier 1 (compute; label "hazard-days past the promise"). Context, reported: Parks/Forestry told aldermen of "about 3,000 hazardous trees" and 7,000 stumps (R3 row, 30 Sep 2026).
- **Residents who could be told "scheduled" today.** Observed: 1,206 (8.1%) of the 14,902 have a city work order pending; 892 are tree inspections. With the link, each of those residents' pages reads "in Forestry's queue, work order open" instead of a bare status. Zero new work.
- **Lots that fell off the rounds.** Observed: 795 city-owned lots look like lot-1 (cuts billed 2019–24, none in 2025–26), an upper bound; 479 of 1,724 "on schedule to be cut" answers in 2026 went to parcels with no cut billed all year. Money, if wanted: 8,412 city-owned lots mowed for $1.31M in 2026 (FRESH-EYES §2) ≈ $156 per lot-season (*estimate*); do not call missing cuts "savings".
- **Do not spend time on:** a 311 call cost (none found), "jobs never done" totals (must-not), or any equity split.

## (c) Proposed v6 outline (about 4:15; the pitch is complete at 2:00)

Times assume Jack's pace with the hold rule. "Reuse" means the v5 scene with the QA-v3 fixes; "new" is a scene to build.

| # | Time | Beat | Voice (gist) | Picture | Status |
|---|---|---|---|---|---|
| 1 | 0:00–0:18 | The sweep | "I audited six St. Louis services, one at a time: tree removal, sidewalks, vacant-lot mowing, board-ups, towing, alley debris. One and a half million requests, two million work records, 1,440 of the city's own status pages. I expected six problems. I found one." | Six tiles with their numbers landing; the audit scale beneath; a line through all six. | **new** (idea 1; reuses b01 vignettes) |
| 2 | 0:18–0:26 | Thesis | "St. Louis closes a request when it hands the job to a crew, and never checks whether the crew did it. So it can't tell which of its 311 promises it has kept." | Title card. | reuse b02 |
| 3 | 0:26–0:44 | The pile | "14,902 requests are past the date the city promised. Colour them by what the records show: work done 3%, a work order pending 8%, no record either way 84%." | Basemap, dots recolour (equal radius, QA #2). Absorbs b03's counter. | reuse b09 + b03 counter |
| 4 | 0:44–0:58 | The scorecard, on the city's page | "This is CityStat. It says 79% of alley debris is handled on time. Only 15% of those closings say the debris was picked up. The scorecard grades the hand-off." | 5 s screen recording of the live CityStat Streets page, then the 79/15 bar. | **new** footage + reuse b04 |
| 5 | 0:58–1:08 | The fix | "The fix is a practice, inside Cityworks, which the city already runs: link the job, flag the misses, count the finish." | Request card tied to job card; three verbs light. | reuse b05 + b12 compressed to 10 s |
| 6 | 1:08–1:50 | The product, running | "Here it is on the city's own data. Forestry's overdue list; ranked, the top 25 go from 9 safety hazards to 25, with the reason on every row. One block. A resident's page today, and with the job linked. CityStat with one more column. And every number, with its source, in one file." | Screen recording with cursor zoom; lot page fixed (QA #1). | reuse b15, re-shot (idea 2) |
| 7 | 1:50–2:00 | The two-minute landing | "Nothing to buy, no app for residents to adopt, no data leaving the city. The ask is one quarter, three request types." | Card: three "no"s and the ask in one line. | **new** card |
| 8 | 2:00–2:20 | How a promise breaks | "Every request has three dates: filed, promised, done. 311 closes it about two days in, at the hand-off. Recorded work comes about five weeks after filing." | Timeline with the promised tick kept (QA #12). | reuse b06+b07 merged |
| 9 | 2:20–2:36 | The missing link | "For 15 of the 20 most common hand-offs, about 22,800 requests, no status page showed anything attached. Tree removals, checked separately, attached a work order every time." | 20 tiles; retitled "anything attached" (QA #5). | reuse b08 |
| 10 | 2:36–2:58 | One block | Twins on North Taylor, with the 28% line spoken (QA #3). | Block schematic, two phones. | reuse b10, trimmed |
| 11 | 2:58–3:20 | What changes | "In 2025, 36,705 requests were closed by hand at the hand-off. About 20,700 were a resident reporting the same thing again within 90 days. 2,576 life-safety jobs are past their date with no finished job on record. And 1,206 residents could be told today that their job is scheduled, with no new work at all." Hours line on screen as an estimate. | Four counters with population, date and assumption lines. | **new** (idea 3) |
| 12 | 3:20–3:34 | Why not the alternatives | Five columns, each with what it needs; ours needs none of it. "A dumping map tells you where. It can't tell you whether the crew came." | Card. | **new** (idea 5, with idea 10's line) |
| 13 | 3:34–3:50 | Already true, already done elsewhere | The four facts; Chicago, Houston, Toronto in one line. | Card with the towing and transition-report quotes. | **new** (idea 6; reuses b11 and b16 quote cards) |
| 14 | 3:50–4:08 | Handover and the ask | "I'm handing over the saved search, the dashboard, the SQL, the weights and a one-page practice. AI did the audit; the city runs plain SQL. One quarter, three request types, each against its own baseline on 13 October, owned by CityStat with Forestry and Streets." | Package glyphs; three baseline counts (register them: QA #10). | reuse b16+b17, trimmed |
| 15 | 4:08–4:15 | End | "Then you'll know which promises you kept." Same words on screen (QA #13). | End card, name and link filled (QA #4). | reuse b18 |

Word budget: about 330 words to 2:00 and 620 in all at Jack's pace (inferred; v5 was 666 words for 4:13 of TTS).

## (d) If only three changes were possible

1. **Replace the opening with the sweep** (beat 1): six services, one failure mode, and the scale of the audit on screen.
2. **Put the real product and the real CityStat page inside the first two minutes** (beats 4 and 6), with the lot-page contradiction fixed.
3. **Add the impact beat** (beat 11) with the four counts above and one labelled estimate of hours.

Everything else in (b) is worth doing, but these three turn "accurate" into "picked".

---

## Appendix A. Queries run tonight (observed; `build/stl.duckdb`, read-only, 00:00 Central)

```sql
-- 2025 filings and closing classes
select count(*) from requests where init_year=2025;                       -- 124,077
select c.closure_class, count(*) from requests r join closure_class c using(request_id)
 where r.init_year=2025 and r.status_group='closed' group by 1;
 -- done 38,342 · handed_off 36,705 · no_action 21,137 · blank 3,909 · info_other 2,756 · converted 438

-- repeat filings: same addr_norm + problem_code within the prior 90 days
with r as (select request_id, addr_norm, problem_code, ts_init, channel_group from requests
           where addr_norm is not null and addr_norm<>'')
select count(distinct b.request_id) from r b join r a
  on a.addr_norm=b.addr_norm and a.problem_code=b.problem_code
 and a.ts_init < b.ts_init and a.ts_init >= b.ts_init - interval 90 day
 where year(b.ts_init)=2025;                                              -- 20,697
-- same, where the earlier request's closure_class like 'handed_off%'    -- 8,145
-- same, where the earlier request is in refiled with durable = true      -- 2,534 (1,700 resident-channel)

-- closings that invite a status call
select count(*) from requests where init_year=2025 and lower(resolution) like '%call csb%';  -- 2,565

-- Tier-1 types in the open past-promise base (filed since 2025-01-01, open, promise < 2026-10-13 23:59:59)
-- Cave-Ins 1,233 · TDebris-alley/street 365 · City Tree Down 323 · Broken/Hanging Limb 307
-- City Tree Limb Down 269 · Building Collapse 79  (sum 2,576)
```

Limits: the 90-day join counts a request once however many earlier ones exist; it does not say whether the earlier request was closed or still open at the time of the repeat (the 8,145 subset does require a hand-off closure, but not that it preceded the repeat). The impact agent should add `a.ts_closed < b.ts_init`.

## Appendix B. Footage list and rules for real pages

| Footage | URL | Rule |
|---|---|---|
| CityStat Streets page, debris measure (78.6%) | https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/streets.cfm | Public page; scroll to the measure; 5 s. |
| CityStat Towing note ("Closed does not necessarily indicate…") | https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/towing.cfm | Public; zoom on the sentence; 4 s. |
| CityStat Forestry ("…or because it was missed") | https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/parks/forestry-division.cfm | Optional. |
| Public 311 status page showing "For detailed information, please contact the Citizens' Service Bureau." | https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/check-service-request.cfm | Shows an address: crop to the status and resolution fields, or mask; prefer a city-tree request on a public right of way; nothing below block level on screen (AGENTS.md; project privacy rule). |
| The site: queue.html (Oldest/Ranked/Close-out), status.html (Today / With the link), citystat.html (the column), data.html (facts file) | local | Fix QA-v3 #1 and the `[NAME]` header first. |

All stlouis-mo.gov paths above were fetched live on 14 Oct by R3 (HTTP 200); robots.txt disallows only one custom-script folder and PDFs (memory note). Record in Jack's own browser; no accounts, no forms.

## Appendix C. Build plan (parallel agents, about 7 h wall-clock)

| Stream | Work | Hours |
|---|---|---|
| Scenes A | Beat 1 (sweep) + beat 7 (landing card) | 3 |
| Scenes B | Beat 11 (impact counters) + beat 12 (alternatives) + beat 13 (already true) | 3.5 |
| Impact agent | The six computations above, each registered with derivation and label; writes the on-screen assumption lines | 2 |
| Site + demo | QA #1 fix, header, citystat column for nine services (idea 7 if checked), re-shoot demo, record city pages | 2.5 |
| Editor | Apply QA-v3 cut list, merge b06/b07, assemble, hold check | 2 |

## Appendix D. Must-nots this outline touches, and the wording that stays inside them

- Repeat filings: "a resident reporting the same thing again", never "proof the work wasn't done" (R2 §1; FRESH-EYES §3).
- Life-safety items: "past their date with no finished job on record", never "undone" (84% has no record either way).
- Hand closings: "closed by hand at the hand-off", never "closed early loses the work" (kept-open requests fare worse).
- Lots: "no cut on record", never "never cut"; 795 is an upper bound.
- Hours and dollars: on-screen label "estimate; assumes N minutes per …".
- Scorecard flip (idea 7): N4's due-date definition, "within 0.2% of CityStat on 8 of 9", never "exactly".
- No equity claim; the map keeps equal dot sizes (QA #2).
- AI did the audit; the product is SQL.
