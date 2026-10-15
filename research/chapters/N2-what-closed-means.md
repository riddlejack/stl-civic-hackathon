# N2. What "closed" means

Written 13–14 Oct 2026 overnight. Every figure here is **observed** from the city's 311 file (csb.zip, cleaned copies in `build/csb-clean/`) unless labelled otherwise. The registry is `build/N2/figures.json`, with a derivation for each figure. Choices are logged in `build/N2/decisions.json`.

## Admission

- **Done:** I classed every closing text (PUBLICRESOLUTION) on closures of requests filed 2024–2026: 262 distinct strings and 2,992 type-and-text pairs, every type included. I measured class mix, median days, closure by the city's own promise date (PRJCOMPLETEDATE) and closure within one day, by type and by division. I built the register of 25 services and checked three completion records on disk that nobody had joined before: board-ups, demolition permits and a planting sample.
- **The classes are an AI judgement.** I (Claude) drafted the rule table. It is fixed code (`scripts/night/N2/classes.py`) and plain SQL (`build/N2/closure_class.sql`), and the two agree on all 2,992 pairs. **No person has reviewed it yet.** Ten texts carry 60% of the hand-off closures, so a review can be short. The hardest call is enforcement notices. I classed them as hand-offs and give every headline both with and without them.
- **Not done:** I did not join weeds to the ledger or trees to work orders. Earlier sessions did those, and N1 rebuilds them tonight. Re-filing by class was in the old T2 brief, not in N2, and I did not compute it.
- **Could not establish:** whether a "done" text is true. Only the ledger, board-up and demolition joins test that. I also could not establish whether DateBoardedUp is the completion date. Its field name says so, and in 86% of 2025–26 records it falls after DateCreated (median 22 days later).
- **Correction for everyone:** the city's CSV repeats a request once per caller. 2024–26 holds 349,031 rows for 322,104 REQUESTIDs. 24,020 ids repeat, up to 21 times; 19,431 rows are exact duplicates, and the rest differ only in CALLERTYPE. **Count distinct REQUESTIDs.** Row counts run about 8% high. The earlier "190,856 closed 2025–26" looks like a row count. By request it is 175,876, filed 1 Jan 2025 to 12 Oct 2026 and closed. I set channel to "resident" if any caller row was a resident channel.
- No city dataset states a licence.

## The knock-out did not fire

Only 4.0% of 2025–26 closures are blank, and half of those are "Public Nuisance Rpt", which the city calls logging-only and auto-closes. Every remaining text is classed. The mix for 175,876 closed requests:

| class | share | what the words say |
|---|---|---|
| done | **37.3%** | work completed, collection made, repairs made, graffiti removed |
| handed_off | 34.8% | will be, scheduled, referred, queued, in progress, tagged, sent to another agency, notice to owner |
| converted | 0.4% | work order created (mostly tree inspections) |
| no_action | 20.5% | gone on arrival, no violation, not city's, declined |
| info_other | 3.0% | call CSB for details, need more info |
| blank | 4.0% | nothing |

**Headline candidates:**
- **35.2%** of closures record a hand-off or a work order rather than finished work. Counting enforcement notices to owners as neither, the figure is **25.2%**. For resident channels it is 36.1%.
- Among closures that say anything about the work (done, hand-off or work order), **48.5% say it was passed on**: about half.
- Of the 107,279 closures made **on or before the city's own promised date, 42.7% are hand-offs** and only 32.5% say done. A closed-by-promise rate scores these as on time.
- 74% of hand-off closures came before the promised date, at a median of 1.8 days after filing with 2.9 days of the promise left. The rate was stable at 31–39% every quarter.

## Where it bites (2025–26 closures)

| type | closed | done | hand-off | promise | closed by promise | done by promise |
|---|---|---|---|---|---|---|
| Weeds, vacant building | 4,136 | 0.3% | 83% | 90 d | 90% | 0.2% |
| Weeds, vacant lot | 2,249 | 0.9% | 85% | 14 d | 88% | 0.5% |
| Bulky items missed | 4,322 | 7% | 82% | 3 d | 91% | 5% |
| Vacant building unsecured | 3,434 | 1% | 90% | 14 d | 83% | 0.6% |
| Debris, alley/street | 5,492 | 36% | 56% | 3 d | 59% | 8% |
| Cave-ins | 2,534 | 22% | 56% | 3 d | 40% | 5% |
| Water coming up | 1,642 | 2% | 62% | 9 d | 90% | 0.8% |
| Refuse not collected | 14,010 | 48% | 45% | 3 d | 79% | 34% |
| Vehicle towing | 12,456 | 6% | 29% | 5 d | 23% | 0.2% |
| Potholes, residential | 4,947 | 90% | 9% | 8 d | 51% | 43% |
| Single light out | 3,453 | 78% | 5% | 3 d | 26% | 18% |

The cleanest example is weeds at vacant buildings. 2,092 requests were closed "on schedule to be cut" a **median 23 minutes after filing**, with the city's own promise 90 days away. For vacant lots the median is **5 minutes** against a 14-day promise. The speed suggests an automatic rule (inferred). Water "scheduled for repair by water department" closes in 94–143 minutes. Towing is mostly no_action: 63% "vehicle gone upon inspection" or similar. Potholes and lights mostly say done but miss the promise. Per-type and per-division tables are in `build/N2/by_type_class.csv`, `by_division_class.csv` and `handoff_before_promise.csv`. Building Division closures are 62% enforcement notices. Water Division hand-offs close in a median 0.1 days.

## Three new joins to the city's own completion records

- **Board-ups.** Requests closed "referred to board up crew" took a median 3.7 days to close in 311 (n = 2,437, filed Jan 2024 to mid-Jul 2026). The Building Division board-up layer shows a board-up at the address within the 14-day promise for **19%**, within 30 days for 36% and within 90 days for **71%**. Where a board-up exists, the median is 34.5 days. For comparison, closures saying "no violation" or similar reached 19% within 90 days. Board-ups recur: 33% of these addresses had one in the prior year. So the referral is usually followed by a board-up, but weeks after the request closed.
- **LRA demolitions.** Of 246 LRA demolition submissions still open in 311, **70 (28%)** have a completed demolition permit at the same address after filing. Open is not undone either. For "Building Collapse", 17% of closed requests later show a completed demolition.
- **Tree planting (negative).** The Forest ReLeaf completed-planting sample matches 0.3% of "approved for next available planting" requests. It is a different programme and cannot confirm city plantings.
- **Potholes.** The Cityworks pothole layer is not independent. All 1,500 sampled ids are the same 311 requests with the same close times, offset by the time zone.

## The register (`build/N2/register.json`, 25 services)

Independent completion record on disk:
- **yes (4):** weeds on vacant lots and at vacant buildings (forestry ledger), vacant building unsecured (board-ups), LRA demolition (permits).
- **partial (7):** city trees (open work-order samples, no finish dates), tree planting, weeds on occupied property, water (live list of about 26 recent work orders, no finish date, no history), tornado debris (76 street segments, May 2025), building collapse, illegal dumping (the enforcement outcome is the closing text).
- **none (13):** potholes, cave-ins, street lights, signals and signs, towing, missed refuse, debris on vacant property, sidewalks, lead inspections, code enforcement, graffiti, sirens, homeless calls.
- **not applicable (1):** nuisance logging.

Two of the "none" rows are fixable records:
- The sidewalk inventory has a `DateRepair` field that is **empty in all 36,822 rows**, and 0 of 7,932 curb ramps have one.
- The forestry ledger recorded vacant-lot debris clean-ups (2,038 "Light Debris" rows in 2019) and stopped after 2021. "Debris-Vacant Lot/Bldg" requests still close "Services completed".

Other notable rows:
- Sirens: 232 requests filed 2025–26, 224 still open.
- Lead inspections: 388 filed, 288 open.
- Tornado debris: 458 filed, 368 open.
- City trees: 8,214 of 14,007 requests cancelled rather than closed.

## For N1 and N3

- Join on `(PROBLEMCODE, trim(PUBLICRESOLUTION))`. The class column in the CSV is final for 2024–26. Blank appears as `""`. Keep PROBLEMCODE raw: "Critical Sign  " has trailing spaces.
- For other years, load `build/N2/closure_class.sql` and call `closure_class(PROBLEMCODE, PUBLICRESOLUTION)`. Unknown texts return info_other with rule "unlisted", so they stay visible.
- `rule_or_judgement` beginning `handed_off:enforcement` marks the notices, so the conservative version can be computed.
- Deduplicate by REQUESTID first.
- Rerun everything in order with `.venv/bin/python -I scripts/night/N2/0{1..8}_*.py`; it takes under a minute.
- The address-bearing extract sits in `build/N2/private/`. Every other N2 output is aggregated.

## What surprised me

- The duplicate rows.
- Closure in 5 and 23 minutes against promises of 14 and 90 days.
- 28% of open LRA demolition requests are already demolished.
- A sidewalk repair-date field that exists and is empty.
- "Due to employee shortage, the routes will be completed in order, as soon possible" closes 3,840 refuse requests.
