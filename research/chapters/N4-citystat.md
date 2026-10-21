# N4. CityStat reproduced, its unpublished Q3, and promises kept

Every figure, with its derivation, is in `build/N4/figures.json`. No city dataset states a licence.

## Admission

**What I did.** I recomputed every CityStat on-time measure that rests on 311 data from the public file (`build/csb-clean/`, filed to 13 Oct 2026 00:33):

- potholes (3 types)
- debris (3 types)
- whole-block lights
- critical signs
- all parks requests

For each, I searched 1,440 candidate definitions and scored them against CityStat's nine settled quarters (2024 Q1–2026 Q1). I then produced Q3 2026 values. I also tried to reproduce the CSB routing counts, the ward map, the snow chart and the towing chart. Finally, I built the "done scoreboard": 104 request types, each graded against the due date the city's own system stamps on every request (`PRJCOMPLETEDATE`).

**What I did not do.**
- **No holiday calendar.** Business days are weekdays only.
- **Out of scope.** I did not reproduce hazard-tree removals, vacant-lot mowing, refuse route coverage, water mains, permits, hiring, health or human services, because none of them rest on 311.

**What I could not establish.**
- **Routing.** I could not find which requests make up the routing chart, and the file has no routing time.
- **Lights rule.** I could not find the exact clock behind "24 hours" for whole-block lights (best fit: a 4.7-point mean gap).
- **Q2 2026 pothole shares.** I could not explain why CityStat's residential and alley pothole shares for Q2 2026 sit above anything the public file supports.

**What I assumed.** The Tableau tables in `data/raw/citystat/tableau-extract.md` are complete and current.

**Corrections tonight.**
- **Double counting.** The 311 file repeats a request once per caller. The rows are identical except for `CALLERTYPE`: 349,031 rows hold 322,104 request numbers in 2024–26 (an independent check, which I re-verified). Every figure here counts each request number once.
- **A bug in my first pass.** My first same-address de-duplication also dropped multi-caller requests entirely. That is fixed.

**Privacy.** On at least one 2026 parks row, `SUBMITTO` holds a person's name. That field is never output (N4-D11).

## What we found

**1. CityStat can be rebuilt from the public file.** *Observed.*

The working hypothesis survives for on-time shares. Definition C is:
- one row per request number
- closed requests only
- grouped by the quarter the request was filed
- on time means the close date minus the filed date is within the goal

Under C:
- **Counts:** CityStat's published counts are reproduced within 0.2% for 8 of 9 metrics: identical in 66 of 72 settled metric-quarters, and never off by more than 4 requests. Parks counts are 2–9 requests per quarter below CityStat's, a 2.1% error (figure n4_repro_counts_exact_C).
- **Shares:** within 5 points in 76 of 81 metric-quarters. The mean gap is 0.5–2.7 points on 7 metrics.
- **Naive reading:** reading the file naively (every row, cancelled and open requests counted as late) gets only 38 of 81 within 5 points.

| Metric (CityStat goal; city due date) | Definition | Mean gap, 9 qtrs | Q2 2026 CityStat → file today | Q3 2026, ours [floor] |
|---|---|---|---|---|
| Potholes, major (3 d; 3 d) | C | 1.4 pts | 44.5% → 46.8% | **13.4%** [13.0] |
| Potholes, residential (8 d; 8 d) | C | 0.5 | 90.6% → 84.4% | **24.3%** [23.5] |
| Potholes, alley (17 d; **16 d**) | C | 0.6 | 98.2% → 87.3% | **51.0%** [45.3] |
| Debris, alley/street (3 d; 3 d) | C | 2.7 | 78.6% → 78.3% | 75.9% [75.8] |
| Debris, vacant building (14 d; 14 d) | C | 1.4 | 95.5% → 94.1% | 97.5% |
| Debris, vacant lot (14 d; 14 d) | C | 0.8 | 97.4% → 93.1% | 98.7% |
| Whole-block lights (24 h; **2 d**) | elapsed ≤24 h | 4.7 | 80.2% → 78.1% | 78.2% |
| Critical signs (48 h; **3 d**) | C | 1.4 | 58.9% → 58.8% | 64.4% [63.7] |
| Parks, all (5–30 d by type; own due date) | see note | 2.3 | 67.5% → 70.4% | 84.5% |

How to read the table:
- **Q3 values** are our definition, from the public file. CityStat has not published Q3; its pages say "last updated June 30th".
- **The floor** is the value if every still-open request closes late. Closed-only shares can only fall.
- **Parks definition:** closed and open requests count, cancelled ones are dropped, and on time means closed before the request's own due date.
- **Full tables:** quarter by quarter, every definition: `build/N4/citystat_comparison.csv`; scoring: `citystat_fit.json`.

**2. Potholes collapsed in Q3 2026.** *Observed; cause unknown.*
- Residential pothole requests filed July–September took a median 17.8 days to close, against 4.0 days in Q2.
- 24.3% met the 8-day goal, down from the 90.6% CityStat published for Q2.
- The closing words are mostly "work completed", so this is slower repair, not different paperwork.

**3. Preliminary quarters look better than they turn out.** *Observed; mechanism inferred.*
- CityStat's on-time shares leave out requests that are still open. A share measured soon after a quarter ends therefore counts only the fast ones.
- **History:** in past quarters, the share 12 days after quarter end overstated the final by up to 18.5 points for residential potholes and 27.1 for alleys.
- **Q2 2026 on 1 July** read 95.5% for residential and 97.1% for alleys. Today it reads 84.4% and 87.3%.
- **Freeze dates differ by page.** Matching CityStat's Q2 counts against the file as it stood day by day dates the freezes:
  - debris, vacant building: 2–9 July
  - critical signs: 8 July
  - residential potholes: 4 August
- **Unexplained remainder.** Even on the matching day, residential potholes read 86.2% against CityStat's 90.6%, and alleys 92.0% against 98.2%. Major potholes read 3.8 points *lower* than CityStat. Details: `q2_freeze.json`.

**4. The other CSB views.**

- **Ward map: reproduced.** *Observed.*
  - The fit is within 0.86 days per ward, with 285,582 requests against CityStat's 286,148.
  - It matches only if closures after 30 June 2026 are ignored, so the map was frozen then (*inferred*).
  - The within-type version does not shrink the north–south gap. Ward 1 averages 17.4 days and Ward 10 32.2 days at the citywide request mix. North wards get slower, not faster: Ward 13 rises from 24.6 to 29.2 days.
- **CityStat's "2026 is much faster" is mostly an age effect.** *Observed.*
  - CityStat compares 2026 requests (at most six months old) with a 2024–26 average that includes closures made years later.
  - Measured at the same age (closures by 1 July of each year), January–June averages are 10.6 days in 2024, 10.4 in 2025 and 9.2 in 2026. That is a real improvement, but a modest one.
  - With every closure to date, 2024 becomes 34.6 days.
  - Ward 9's 2026 figure was 14.0 days on 1 July (CityStat: 13.7) and is 19.8 days now.
- **Snow: reproduced.** Weekly averages fit within 0.4 days: 17.8 days in the January 2025 storm against 3.3 in January 2026 (CityStat: 17.4 and 3.1). CityStat's storm-week counts run 3–18% below ours, so it appears to merge repeat reports.
- **Towing: reproduced.**
  - Closed counts fit within 1.2%, with exact matches in 2024 Q2 and Q4.
  - Only 0.9% of closed tow requests (143 of 16,221) say "vehicle towed".
  - In August 2026, "tagged for tow" closures fell from 129 to 32 and "vehicle towed" rose from 6 to 67. That is consistent with the close-only-when-towed change CityStat promised (*inferred*).
- **Routing: not reproduced.**
  - The file has no routing timestamp, so the 2.5-day share cannot be recomputed.
  - No subset matches the counts. The best of 260,610 channel-by-category subsets still misses by 4.5% on average and by 15% in Q2 2026.

**5. The city's own due dates differ from CityStat's goals for 3 of 9 services.** *Observed.* Alley potholes: 16 days vs 17. Whole-block lights: 2 days vs 24 hours. Critical signs: 3 days vs 48 hours.

## Inferred definitions

CityStat's on-time share works like this:
- one row per request number
- only requests closed by the day the data were pulled
- grouped by the quarter filed, not the quarter closed (the best quarter-of-closure fits miss by 2.0–21.7 points, against 0.5–3.8 for quarter filed)
- on time means close date minus filed date is within the goal (calendar days, not business days or elapsed hours), except for lights
- parks goals are the per-type due dates the 311 system already stamps on each request; resident and staff requests are both counted

## Promises kept: the done scoreboard (`build/N4/scoreboard.json`)

The scoreboard covers 104 types with 300+ requests filed since 1 Jan 2025. Each request is graded against its own due date. Cancelled requests are excluded and shown separately, and only requests already due are graded. The "done" class comes from N2's closing-word rules.

Across the 103 types that carry a due date:
- 57.8% of 170,719 graded requests were closed by it.
- Only 19.5% were closed by it with words saying the work was done.

Selected types:

| Type | Due (days) | Closed by due date | Closed as done by due date | Note |
|---|---|---|---|---|
| Residential potholes | 8 | 50.6% | 42.7% | |
| Major potholes | 3 | 19.9% | 12.4% | |
| Cave-ins | 3 | 26.6% | 3.6% | 1,231 still open past due |
| Single light out | 3 | 25.1% | 17.4% | |
| Vehicle towing | 5 | 22.0% | 0.2% | |
| Inspect City Tree | 14 | 21.0% | 4.2% | 66% cancelled |
| Sidewalk repair | 14 | 5.8% | — | median 260 days late |
| Whole-block lights | 2 | 85.5% | 78.2% | |
| Refuse not collected | 3 | 79.4% | 34.2% | |

## Questions for CityStat

1. Is the on-time share "distinct closed requests filed in the quarter, close date minus filed date ≤ goal", with open and cancelled requests left out? If so, why leave open requests out? That choice makes every new quarter look better than it will end up.
2. When was each Q2 2026 view frozen? Why are residential and alley potholes 4–6 points above what the file shows at the matching count?
3. Which requests make up the routing chart (10,853 in Q2 2026), and where is routing time recorded?
4. For whole-block lights, the "24 hours" runs from what to what?
5. Why do three CityStat goals differ from the due dates the 311 system stamps on the same requests?

## Files written

**Scripts:** `scripts/night/N4/`
- `00_load.py`
- `common.py`
- `citystat_targets.py`
- `01_definition_search.py`
- `02_routing_subset.py`
- `03_compare_and_q3.py`
- `04_other_metrics.py`
- `05_scoreboard.py`
- `06_figures.py`
- `07_q2_freeze_date.py`

**Outputs:** `build/N4/`
- `figures.json` (76 figures)
- `scoreboard.json` and `.csv`
- `citystat_comparison.csv`
- `citystat_fit.json`
- `q3_2026.json`
- `q2_freeze.json`
- `definition_search.json`
- `routing_search.json`
- `other_metrics.json`
- logs
- `csb_2023_2026.parquet` (working copy)
