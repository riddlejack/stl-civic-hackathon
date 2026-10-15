# R1. What happened after the hand-off

Written Wednesday 14 Oct 2026, 12:20 to 1:10 p.m. Central, by the R1 session. Figures (150, each with its derivation) are in `build/R1/figures.json`, and choices (18) are in `build/R1/decisions.json`. `scripts/night/R1/run_all.sh` rebuilds everything in about 45 seconds. Everything is **observed** from public files on disk unless marked *inferred*. No city dataset states a licence.

## Admission

- **Done.**
  - Classed all 61,845 hand-off closures of 2025–26 (N2 classes `handed_off`/`converted`) by kind and by whether a public completion record exists.
  - Traced every traceable one to the city's own record: the Forestry billing ledger for weed cuts, and the Building Division board-up layer for "referred to board up crew".
  - Ran three baselines, restated CityStat's nine 311 measures, and tested the records themselves (recall, lag, join failure).
- **Not done.**
  - Demolition is not in the headline: one LRA demolition was closed at a hand-off in 2025–26, because the city keeps these open.
  - Trees are partial (open-order sample only).
  - Re-reports are R2's table, cited here.
- **Could not establish.**
  - A missing ledger charge or board-up date shows only that the city's own record does not show the work.
  - The board-up layer misses about one board-up in five (see below), so board-up "no record" is not evidence of lost work.
- **Assumed.**
  - The promise is each request's own `PRJCOMPLETEDATE`.
  - Work counts if it is recorded on or after the filing date.
  - Board-up dates are UTC calendar dates.
  - "No record" is counted only where the promise passed by 13 Sep 2026, at least 30 days before the files end on 13 Oct (R-COMMON).
  - 2025 weed requests are dropped because the 2025 ledger is thin (4,052 Grass Maint cuts against 31,527 in 2026).

## Headline

**Of 3,640 hand-offs we could trace to the city's own completion records (weed cuts promised on 2026 requests, and board-ups referred in 2025–26) whose promised date had passed by 13 September, 18.0% were done by that date, 49.8% were done late (median 28 days after the promise), and 32.2% had no record of the work by 13 October. 311 had closed 84.9% of them by the promised date, a median 1.8 days after filing. Where the work is recorded, it came a median 35 days after filing.**

| Service (filed) | Graded | 311 closed by promise | Done by promise | Done late (median days late) | No record by 13 Oct |
|---|---|---|---|---|---|
| Weeds, vacant lot (2026) | 631 | 91.1% | 20.4% | 44.7% (25) | 34.9% |
| Weeds, vacant building (2026; mostly 90-day promise, filed by mid-June) | 797 | 76.9% | 19.3% | 28.2% (40) | 52.4% |
| Missed / unsatisfactory cut complaints (2026) | 684 | 98.5% | 16.4% | 46.6% (30) | 37.0% |
| Referred to board-up crew (2025–26) | 1,528 | 80.5% | 17.0% | 64.6% (26) | 18.4% |
| **All traceable** | **3,640** | **84.9%** | **18.0%** | **49.8% (28)** | **32.2%** |

**Weed "no record" holds up.**
- **It persists.** It is still 36.5% where the promise passed three months or more before 13 Oct (n = 800), and 41.9% counting each parcel once.
- **It is not a fuzzy join.** 95% of graded lot and building requests matched their parcel exactly. 91% of no-record lots appear in the ledger in other years, 55% of them cut in 2024.
- **It is cleanest on city-owned land.** On land-bank lots, where no owner could have cut instead, it is 24.3% (n = 313); land-bank buildings 11.6% (n = 69). The ledger is the land bank's mowing record: 82.4% of its 8,585 lots have a 2026 cut. Private parcels are higher, at 45.3% for lots and 56.3% for buildings, but there an owner may have cut, unrecorded.
- **It lasts.** 30.8% of 2025 vacant-building requests still have no cut billed a median 15 months after filing (n = 1,589). The vacant-building cut is about as fully recorded in 2025 as in 2026.
- **The words matter.** "Added to rotation" closures have the most missing cuts: 64.0% of buildings (n = 367) and 57.8% of lots (n = 64), against 42.4% and 31.8% for "on schedule to be cut".
- **In all,** 891 weed requests on 707 parcels were closed at a hand-off with no cut billed by 13 Oct.
- **"Done" means only that the parcel was cut after the request,** not that the request caused it (baseline 1).

**Board-up "no record" does not hold up.**
- **The layer misses about one board-up in five.** It holds a board-up for only 80.6% of buildings 311 says the city secured (54 of 67; 95% CI 69.6–88.3%), and it dates them a median 14–29 days after that closure.
- **No record shrinks as promises age:** from 62% (promise 30–60 days old) to 14.8% (three months or more).
- **So board-ups are done, but late,** and the layer's lag may inflate "late". 2026 is worse than 2025: 11.7% vs 19.9% by the promise, a median 32 vs 23 days late.
- **The layer is the crew's queue.** 80% of "referred" requests got a board-up order within 2 days of the 311 closure (median 1.3 hours after it), and the order took a median 26 days to show a boarded date.

**Stricter cuts and the funnel.**
- **Pooled, promises at least three months old:** 16.2% done by the promise, 61.0% late, 22.8% no record (n = 2,168). With seven days' grace for weekly ledger posting, done by promise is 25.2%.
- **Funnel.** Of 8,362 traceable crew-work hand-offs, 2,900 are 2025 weed requests (dropped), 286 have no parcel, 19 no promise, and 1,517 a promise after 13 Sep.
- **By ward group,** no record is 27.8% in wards 10–14, against 42.2% in wards 1–5 and 42.8% in wards 6–9. The north does *better*, because land-bank rotation lots sit there.

## Is it the hand-off? Three baselines

**1. Does a report change anything?** (Weeds, 2026, filed by 13 Sep.) Each requested parcel is compared, from the same date, with the parcels on its city block (ledger CITYBLOCK) that were on the 2026 rotation and had no request in the prior 60 days: 1,761 parcel-dates, a median of 8 controls each.

| | Cut within 14 d | Within 30 d | No cut by 13 Oct | Median days |
|---|---|---|---|---|
| Requested parcels (all) | 12.1% | 22.6% | 41.3% | 93 |
| Same-block rotation controls | 16.0% | 31.0% | 23.8% | 49 |
| Requested parcels on the rotation (1,222) | 17.4% | 32.6% | 15.4% | 48 |
| their controls | 16.9% | 32.5% | 21.7% | 46 |

- **A report does not bring the crew.** A requested rotation lot is cut on the rotation's timetable, like its unreported neighbours. The difference is +0.6 points within 14 days (95% CI −1.6 to +2.9; bootstrap over 591 city blocks).
  - Lots are cut slightly sooner: +5.3 points (CI +2.0 to +8.5).
  - Buildings are cut later: −3.1 points (CI −5.6 to −0.5).
- **Nor does it pull the crew to the block.** Rotation parcels on other blocks in the same ward, with no request, were cut within 14 days *more* often (17.7%).
- **Where the work goes missing.** 30.6% of requested parcel-dates (539) are on parcels with no cut billed at any time in 2026, yet the requests were closed "on schedule to be cut".

**2. Kept open vs closed at the hand-off.** *This cuts against the simple story:* requests left open have far less recorded work.

| No record of the work | Still open | Closed at hand-off |
|---|---|---|
| Weeds, vacant lot, 2026 | 95.4% (131) | 34.9% (631) |
| Weeds, vacant building, 2026 | 93.4% (137) | 52.4% (797) |
| Vacant building unsecured, 2025–26 | 88.6% (132) | 18.1% (1,443) |

- **The confound.** Open requests are the stalled ones: dispatch, inspection, re-inspection, or a letter to the owner. But ownership does not explain it away: on land-bank lots, 20 of 22 open requests have no cut.
- **The reading.** Closing at the hand-off is when a job enters a crew queue. The closure does not lose the work; the loss is in the queue afterwards, which nobody reconciles against the request.
- **Open does not mean undone either.** 37 of 190 LRA demolition requests still open (19.5%) already have a completed demolition, a median 282 days after filing.
- **Owner notices end in city work.** After an owner notice on an unsecured building, the city's own board-up record shows a board-up for 72.8%, mostly late (n = 1,405).

**3. "Done" closures as the "is not"** (R2, `build/R2/rereport_type_compare.csv`).
- **Re-reported within 14 days, done vs hand-off:** residential potholes 1.1% vs 4.4%; whole-block lights 4.9% vs 7.6%; across 61 types, standardised for type mix, 4.1% vs 6.7%.
- **Not for board-ups:** unsecured buildings come back 5.9% after a hand-off, against 6.8% after "secured by city".

## What the city reports vs counting only work recorded as done

CityStat's 311 measures, rebuilt with N4's definition C, which reproduces CityStat (one row per request, closed only, by quarter filed).

| Measure (goal) | CityStat Q2 2026 | Ours Q2 2026 | Hand-offs among on-time closures | Hand-offs not counted | Only "done" counted | 2025 Q1–2026 Q2: ours → only done |
|---|---|---|---|---|---|---|
| Debris, alley/street (3 d) | 78.6% | 78.3% | **67.0%** | 25.9% | **15.0%** | 55.9% → 7.2% |
| Debris, vacant lot (14 d) | 97.4% | 93.1% | 36.1% | 59.5% | 41.4% | 73.1% → 31.0% |
| Debris, vacant building (14 d) | 95.5% | 94.1% | 20.3% | 75.0% | 36.8% | 77.5% → 28.9% |
| Parks, all (own due date) | 67.5% | 74.2% | 58.9% | 30.5% | 18.6% | 41.4% → 11.6% |
| Potholes, major (3 d) | 44.5% | 46.8% | 24.7% | 35.3% | 34.6% | 23.5% → 16.5% |
| Potholes, residential (8 d) | 90.6% | 84.4% | 8.0% | 77.7% | 76.3% | 55.5% → 48.4% |
| Potholes, alley (17 d) | 98.2% | 87.3% | 3.9% | 83.9% | 83.1% | 69.0% → 62.7% |
| Whole-block lights (24 h) | 80.2% | 78.1% | 9.3% | 70.8% | 65.9% | 61.9% → 56.1% |
| Critical signs (48 h) | 58.9% | 58.8% | 1.5% | 57.9% | 49.1% | 52.0% → 43.3% |

- **How the columns are built.** "Hand-offs not counted" drops hand-off closures from the on-time count. "Only done" also drops "no action" and other closures. The denominator stays CityStat's.
- **Overall.** N4: 57.8% of 170,719 requests were closed by their own due date, but 19.5% were closed by it as done. Traceable hand-offs: 84.9% were closed by the promise, but 18.0% were verifiably done by it.
- **Q3 2026** (unpublished; our definition): for residential potholes, 61.9% of the few on-time closures are hand-offs.

## Composition (`build/R1/handoff_composition.csv`, 953 type × phrase rows)

| Kind of hand-off | Traceable | Partial | No public record | All |
|---|---|---|---|---|
| Crew work (the city will do it) | 8,363 | 578 | 32,776 | 41,717 (67.5%) |
| Owner enforcement (a notice) | 0 | 2,331 | 15,259 | 17,590 (28.4%) |
| Referral elsewhere (MSD, MoDOT, Ameren…) | 0 | 0 | 2,538 | 2,538 (4.1%) |
| **All 2025–26 hand-off closures** | **8,363 (13.5%)** | **2,909 (4.7%)** | **50,573 (81.8%)** | **61,845** |

- **Traceable:** ledger 6,709, board-ups 1,653, demolition 1.
- **Partial:**
  - owner notices on unsecured buildings (1,510), collapses (760) and weeds (61), where city work is one possible outcome;
  - 572 tree work orders;
  - 6 LRA board-up tickets.
- **Largest crew work with no record:**
  - towing "tagged for tow" (3,072);
  - refuse "next scheduled day" (3,013) and "employee shortage…" (2,197);
  - debris "will be investigated" (1,663);
  - tree planting "approved for next available planting" (1,444).
- **Tested and unusable (2,930):**
  - the pothole layer is the 311 record itself;
  - the ReLeaf sample is another programme;
  - debris has not been in the ledger since 2021;
  - the sidewalk repair date is empty.
- **Trees, partial.**
  - Of 294 requests closed "removal work order created" in 2025, 3 still have an open order at the address (7 within 30 m). The open-order list holds the 1,500 lowest ids, which rise with start date (r = 0.997) to 8 Jan 2026, so it should be complete for 2025 orders (*inferred*). These orders mostly closed, which does *not* support "converted means lost"; closed is not proven removed.
  - N5's story stands: 289 of 5,201 blank-cancelled inspections were filed where a removal order was already open (median 577 days old). On 13 Oct, 99.3% of those orders were past their own finish date, a median 763 days overdue.

## What cuts against us, and what survives

**Against:**
1. Requests kept open have far less recorded work than hand-off closures, so the hand-off closure is not what loses the work.
2. A report does not change when a rotation lot is cut. The missing cuts are on lots on no rotation that were closed "on schedule".
3. Board-ups are done, late. Their no-record share is within the record's miss rate.
4. The north has the lowest no-record share: no equity gap on this measure.
5. Tree work orders created in 2025 mostly closed (*inferred*).
6. Only 13.5% of hand-offs are traceable, and those are the services with the best records. Refuse, towing, water and street repair cannot be checked.

**Survives:**
- The city's on-time numbers measure the hand-off, not the work: 85% closed by the promise, 18% done by it.
- Recorded work comes a median four weeks after the promise.
- For weed cuts, about a third of hand-offs (36.5% three months on) have no cut at all, and on city-owned lots a quarter.

## Files

- **Scripts:** `scripts/night/R1/` (`common.py`, `01`–`07`, `run_all.sh`).
- **Outputs (`build/R1/`):**
  - `handoff_composition.csv` and `composition_summary.json`
  - `fate_summary.json` and `fate_by_service.csv`
  - `baseline_weeds.*` and `baseline_open.*`
  - `restated_citystat.csv` and `restated.json`
  - `checks.json`, `figures.json` and `decisions.json`
  - `log_*.txt`
- **Private:** request ids are in `build/R1/private/fate_requests.parquet` only.
