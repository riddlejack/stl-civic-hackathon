# Video script v6: the audit, the product by 2:00, the impact, the case

Written 15 Oct 2026, about 12:35 a.m. Central. Jack reviewed rough cut v3.1 and said it lacked wow, credibility, quantified impact and the argument for this fix over the alternatives, and that it should show more of the real tool. He asked for a fresh-eyes brainstorm and for the orchestrator to approve the ideas and change the script. Sources: `research/brainstorm-v6.md` (fresh-eyes ideas, approved), `research/impact-quantification.md` (impact numbers, verified), `research/credibility-tally.md` (scale of the audit). Supersedes v5.

**Shape.** Fifteen beats, about 640 words, about 4:15. The pitch is complete by 2:00: the audit, the finding, the city's own page, the fix, the product running, and the ask. The second half is the evidence, the impact, and the case for this over the alternatives.

## Read-aloud (one file per beat; leave a half-second pause between sentences)

> **1.** I audited six of St. Louis's 311 services: tree removal, sidewalks, vacant-lot mowing, board-ups, towing and alley debris. One and a half million requests. Over two million forestry records. 1,440 of the city's own status pages. I expected six problems. I found one.
>
> **2.** St. Louis closes a 311 request when it hands the job to a crew, and nothing ties the request to the job after that. So the city can't tell which of its promises it has kept.
>
> **3.** Right now, 14,902 requests are past the date the city promised. Color them by what the records show. Work done: 3 percent. A work order pending: 8 percent. No record either way: 84 percent.
>
> **4.** This is CityStat, the city's own scorecard. It counts 79 percent of alley-debris requests as handled on time. But only 15 percent were closed with a note that the debris was picked up. The scorecard grades the hand-off, not the work.
>
> **5.** The fix is a practice change inside Cityworks, the system the city already runs. Link the job to the request. Flag every request past its date with no finished job. Count a promise as kept only when the job is done.
>
> **6.** Here it is, running on the city's own data. Forestry's overdue list, ranked by hazard, lateness and repeat reports, with the reason on every row. Ranked this way, its top 25 go from 9 safety hazards to 25. A resident's page, today, and under the fix. CityStat, with one more column. And every number, with its source.
>
> **7.** No new software. No app for residents to adopt. No city data leaving the city. The ask: one quarter, three request types.
>
> **8.** Here's where it breaks. Every request has three dates: filed, promised, done. 311 closes the request about two days after filing, at the hand-off. When the work is recorded at all, it comes about five weeks after filing.
>
> **9.** Cityworks can attach the crew's work order to the request. For 15 of the 20 most common hand-offs, about 22,800 requests, no status page showed anything attached. Tree removals did, every time.
>
> **10.** Here's one block. Two city-owned lots on North Taylor, reported the same July day, both closed within the hour: "on schedule to be cut." One was cut three times this year. The other has no cut on record since October 2024. Nothing checks 311's answer against the cutting schedule. This year, 28 percent of "on schedule to be cut" answers went to properties with no cut on record all year.
>
> **11.** Here's what the fix makes visible. 2,778 life-safety requests, trees down, cave-ins, water coming up, are past the city's date, by a median of eight months. In the city's own work orders, 1,630 tree removals are past the finish date Forestry itself set. 52 city-owned lots were told "on schedule" this year and have no cut on record; about $7,000 would cut them for a season. These are the jobs a weekly list puts in front of someone.
>
> **12.** Why this, and not a hotspot map, a chatbot, or a new app? Each sits on top of the same broken loop. A dumping map can tell you where. It can't tell you whether the crew came. Setting this up takes about 150 staff hours and no new license. Fresno paid about a million dollars for a new 311 system.
>
> **13.** And most of it is already true. Forestry already links work orders to tree removals. Cityworks already closes a linked request when the job closes. The city has already promised this rule for towing. The mayor's transition committee asked for exactly this audit. And Chicago, Houston and Toronto have written the same rule.
>
> **14.** I'm handing over the saved search, the dashboard, the SQL, the ranking's weights and a one-page practice for each division. AI agents did the audit; the city runs plain SQL. One quarter: tree removals, cave-ins and vacant-lot mowing, each measured against its baseline from the thirteenth of October.
>
> **15.** Then you'll know which promises you kept.

## Action titles

| # | On-screen action title |
|---|---|
| 1 | **Six services audited; one failure mode** (the scale of the audit beneath) |
| 2 | **St. Louis can't tell which of its 311 promises it has kept** |
| 3 | **14,902 requests are past the city's date; for 84%, no record either way** |
| 4 | **CityStat grades the hand-off, not the work: 79% on time, 15% closed saying it was picked up** |
| 5 | **The fix: link the job · flag the misses · count the finish** |
| 6 | (product footage) |
| 7 | **Nothing to buy. One quarter to prove it.** |
| 8 | **311 closes the request in about 2 days; recorded work comes about 5 weeks after filing** |
| 9 | **For 15 of the 20 most common hand-offs, no status page showed anything attached** |
| 10 | **Same block, same day, same answer: one lot cut three times, the other none on record since Oct 2024** |
| 11 | **What a weekly list would surface: 2,778 overdue life-safety requests; 1,630 overdue tree-removal work orders** |
| 12 | **Every alternative sits on the same broken loop; this one closes it** |
| 13 | **Already true in St. Louis, already policy elsewhere** |
| 14 | **The ask: one quarter, three request types, measured against 13 October** |
| 15 | **Which promises did St. Louis keep?** (then the end card) |

## Figures behind each spoken number

| Spoken | Value | Source | Label |
|---|---|---|---|
| one and a half million requests | 1,454,222 (2008–2026) | `research/credibility-tally.md` | observed |
| over two million forestry records | 2,252,031 ledger rows | same | observed |
| 1,440 status pages | 1,440 | same | observed |
| 14,902; 3% / 8% / 84% | 14,902; 2.6 / 8.1 / 84.3% | `research/open-queue-reality-check.md` | observed |
| 79%; 15% | 78.6% published; 15.0% done-only, same denominator | `research/closure-class-review.md` | observed |
| 9 → 25 | Forestry top 25, oldest-first vs ranked | `research/prioritisation-option.md`; site/data/ranked.json | observed |
| about two days; about five weeks | median 1.8 days to close (61,845 hand-offs); median 35 days to recorded work | `deliverable/video-script-v5.md` figure table | observed |
| the promised tick on the timeline (on screen) | median 14 days after filing, traced hand-offs | `build/R1/fate_summary.json` | observed |
| 15 of 20; about 22,800 | 22,761 requests in the 15 types | `research/status-page-linkage.md`; `build/E1/sample_strata.csv` | observed |
| twin lots; 28% | 479 of 1,724 | `research/north-taylor-mechanism.md` | observed |
| 2,778 life-safety, median eight months | 2,778 past the date (tier-1 types, after close-out), median 239 days | `research/impact-quantification.md` H1 | observed (tier map is ours, editable) |
| 1,630 tree removals past Forestry's own finish date | 1,630 of 2,504 open tree-removal work orders; median 618 days | same, H2 (authorised Cityworks extract, 14 Oct) | observed |
| 52 lots; about $7,000 | 52 lots counted; $132 median billed rate per lot-season | same, H3 | observed (count) / estimate (cost) |
| about 150 staff hours | set-up estimate | same, H5 | estimate (assumptions on screen) |
| Fresno about a million dollars | new 311 system | same, H5 (cited) | reported |
| towing rule; transition committee; Chicago, Houston, Toronto | quotes and policies | `research/chapters/R3-voices.md`; `research/precedents-closed-loop.md` | observed / reported |

## Not said, deliberately

- **Repeat-request savings.** Timed properly, the effect shrinks to about 176 durable repeats.
- **Hand-closing labour saved.** Linking may cost as much time as closing did.
- **"Never cut".** The script says "no cut on record".
- **That crews will be faster or the backlog cleared.**
- **Any equity claim.**
- **That AI is in the product.**
