# N3. Fairness, measured like for like

13 October 2026, 11:55 p.m. Central. Scripts `scripts/night/N3/00–10`; outputs `build/N3/`. Source for every 311 figure: the city's CSB file (`data/raw/stlouis-mo.gov/files/csb.zip`, cleaned copies in `build/csb-clean/`), one row per REQUESTID. CityStat figures: `data/raw/citystat/tableau-extract.md` (CSBRequestMap). No city dataset states a licence.

## Admission and summary

**What I did.** Reproduced CityStat's ward averages; split the ward 1 vs ward 10 gap (and wards 1–5 vs 10–14) exactly into type mix, closing words and speed; built like-for-like tables for the 79 types with ≥300 resident requests since the tornado, per ward and ward group, before and after; applied a robustness rule fixed in advance; tested one crew boundary. Counts are by distinct REQUESTID, and a request is resident-filed if any of its rows is (the files repeat a request once per caller; §4). Closure classes are N2's final file (`research/chapters/N2-closure-classes.csv`, 23:52). It covers 99.5% of 2023–26 closures directly; my rules cover the rest. My independent first-pass rules agree with N2 on 98.4% of closures.

**What I found.** (1) **The working hypothesis is wrong on its main point.** Mix of request types and closing practice explain little of CityStat's ward gap: 1.9 of 15.7 days for ward 1 vs ward 10 (12%). Across wards 1–5 vs 10–14 the type mix runs the *other* way: the north files a faster-closing mix. (2) Most of the gap is the same request type, closed with the same words, closed later. That time mostly ends at a *first* step (a tag, a referral, a notice, "gone upon inspection"), not at completed work. (3) Where the closing words say the work was done, most high-volume services show **little or no ward gap** since the tornado: whole-block lights out, potholes, refuse, containers, signs. (4) The comparisons that survive every test are about first steps: **towing** (tagged for tow: 12 vs 37 days; promise 5), **cave-in referral** (0.8 vs 41.7 days, a process line at ward 5|6) and **building-code notices** (3.3 vs 8.4 days). The knock-out does not fire, but the result is not "the ward chart measures paperwork" either. It measures **how long until the city first acts, and the north waits longer for that.**

**What I could not establish.** Repair dates for referred cave-ins (not in the file). What the ward 5|6 Street Department line and the ward 7|8 Forestry line are (no keyless district layer found for either). Why our ward 10–12 means run 2.6–3.4 days below CityStat's when the other eleven wards are within 0.7. *Assumed:* CityStat's chart reflects a snapshot taken about July 2026; repeated REQUESTID rows are one row per caller.

## 1. CityStat's own gap, decomposed (observed)

**Reproduction.** Take one row per REQUESTID, all channels and types, filed 1 Jan 2024–30 Jun 2026, and the mean days to close over STATUS=CLOSED requests closed by the window end. This gives ward 1 **17.3** (CityStat 17.18) and ward 10 **32.2** (35.07). Mean absolute error across 14 wards: 0.85 days. Request counts are within 1% (285,582 vs 286,148). Of seven definitions tried (`citystat_reproduction.json`), resident-only and cancelled-as-closed fit worse; locating blank wards did not close the ward 10–12 residual.

**Split** (exact two-level Kitagawa, closed by 10 July 2026, ward 1 = 17.36, ward 10 = 33.08 mean days):

| Component | Days | Share |
|---|---|---|
| Mix of request types | +0.43 | 3% |
| Closing words used (class shares within type) | +1.51 | 10% |
| Same type, same class: "done" closures slower | +1.30 | 8% |
| Same type, same class: hand-off closures slower | +6.09 | 39% |
| Same type, same class: no-action, blank, other | +6.39 | 41% |
| **Gap** | **15.72** | 100% |

Moving enforcement notices out of hand-offs into their own class (N2 puts them in `handed_off:enforcement`) changes almost nothing. Closing words rise from 1.51 to 1.72 days; enforcement takes 3.34 days of the 6.09 hand-off speed. Towing alone contributes 3.6 days: its no-action closures (mostly "vehicle gone upon inspection") take a median of 69 days in ward 10 against 9.5 in ward 1. Wards 1–5 vs 10–14: gap 7.6 = mix −3.2 + closing words +0.9 + speed (done) +1.7 + speed (other) +8.1. The two checks agree. Median reweighting puts ward 10 at **6.1** days at ward 1's type and closing mix, against an observed 5.9 (ward 1: 2.8). Capping days at 90 leaves speed at 111% of the gap. Chart: `build/N3/N3-decomposition-ward1-vs-ward10.png`.

## 2. What survives like for like (observed; rule fixed in advance)

The rule: in both periods (filed before and after 16 May 2025), n ≥ 100 each side, median ratio ≥ 1.5, bootstrap 95% lower bound > 1.2, and the promise measure also worse in wards 10–14. Like for like means same type and same closing words. Full table: `build/N3/robust_comparisons.csv`; per ward: `like_for_like_by_ward.csv`.

1. **Towing, first visit.** "Vehicle tagged for tow": 12.0 vs 36.9 days after the tornado (n 1,300/271), 16.0 vs 36.1 before. All five north wards are slower than every ward 1–5. Closed by the city's 5-day promise: 38% vs 11%. "Gone upon inspection": 10.7 vs 46.2. *Analyst check:* towing requests, resident CALLERTYPE, PUBLICRESOLUTION = "vehicle tagged for tow", median DATETIMECLOSED − DATETIMEINIT by WARD, one row per REQUESTID. Caveat: 50–61% of towing closures are entered on days with ≥15 such closures, on both sides, so the close date is a data-entry date.
2. **Cave-ins, referral.** "Referred to street maintenance…": 0.8 vs 41.7 days (n 361/115) after, 2.0 vs 66.7 before. Per ward it jumps from ≤1.1 days in every ward 1–5 to ≥15.7 in every ward 6–14. *Inferred:* a different intake process, not only slower crews. Work completed: 8.3 vs 23.1 days, but only 35 in wards 1–5, so the repair-speed gap is unproven. *Check:* the same query by ward; ask Street Department what changes at the ward 5|6 line.
3. **Building-code notices.** Exterior maintenance, "issued notice of violation": 3.3 vs 8.4 days after, 3.3 vs 8.0 before. Open storage and interior maintenance behave the same way. Closed by the 14-day promise: 74% vs 50%. The gap is about 5 days and sits in wards 9–12 (11–22 days); ward 13 (4.7) is faster than ward 4 (8.8). *Check:* same query, Building Division types, per ward.

**Fails the rule (kept visible).** *Single light out*, which COMMON proposed as a lead. Done-class 15.6 vs 41.0 days after the tornado, but 4.8 vs 6.4 before. The gap sits in requests filed Oct 2025–Mar 2026 (20 vs 49, then 5 vs 31 days); other quarters are level (`N3-single-light-by-quarter.png`). *Trees:* removal work order 124 vs 190 days, but only 21 in the north; many north tree requests are cancelled, not closed. *Stray dogs:* "no strays observed" 1.0 vs 3.8 days, but the promise measure favours the north.

**No material gap where the work is recorded as done** (after the tornado, median days, wards 1–5 vs 10–14): whole-block lights 0.7 vs 0.7, residential potholes 6.9 vs 8.0, major-street potholes 7.0 vs 6.8, refuse 1.7 vs 1.8, damaged containers 7.8 vs 8.2, signs 7.0 vs 7.5 (`N3-done-class-by-type.png`). The pothole gaps before the tornado (about 1.4×) are gone.

## 3. Boundaries (30 minutes)

`https://maps8.stlouis-mo.gov/arcgis/rest/services?f=json` (fetched 23:45) has no keyless Streets or Forestry district layer: FORESTRY_MAINTENANCE and the ROUTING, PARKS and WEB folders need a token, and FORESTRY_MAINTENANCE_NSD's districts are the 14 wards.

`STREETS/VEHICLE_TOWING_ASSIGNMENTS` exists and is keyless. I fetched geometry only, because its one attribute is a staff name. It has two territories: wards 1–8, and wards 9–14 plus part of ward 8. The towing gap does **not** follow it: wards 6–8 sit in the southern territory yet tag at 21–25 days, like the north. Inside the split ward 9 the northern side is slower (23 vs 14 days), but n is only 20 and 23.

The file's own "investigation done" stamp (DATEINVTDONE) shows division lines instead. For Street Department inspection types (towing, cave-ins, bad street condition) it reads under 3 days in every ward 1–5 and 7–64 days in every ward 6–14. For tree inspections the line falls at 7|8 (2–3 days against 13–38). Because towing tags in wards 1–5 still take 6–15 days, I treat the stamp as a process marker, not a like-for-like measure (`decisions.json`, n3-reject-invt-stamp).

## 4. Corrections for other chapters

- **The public 311 files repeat REQUESTIDs.** In 2024–2026 there are 349,031 rows for 322,104 requests; 24,020 ids appear 2–21 times, and the repeats differ only in CALLERTYPE. Dedupe before any count or median (N1). COMMON's medians move slightly: single light out 15.6 vs 41.0, not 15.8 vs 42.1.
- **COMMON correction 2 needs a nuance.** For cave-ins the same closing words take 0.8 vs 41.7 days, so "inflated by closure mix" understates the north's wait for the first step. Say that the 1.7 vs 27.6 headline compared a desk referral with a field process, and that repair speed is unknown in the south.

**Files.** Scripts `scripts/night/N3/00_load.py` … `10_blank_wards.py`, `classes.py`. Outputs in `build/N3/`: `figures.json` (20 figures, each with a derivation), `decisions.json` (13), `decomposition*.json`, `citystat_reproduction.json`, `like_for_like_by_{group,ward}.csv`, `robust_comparisons.csv`, `robust_shortlist.json`, `boundaries.json`, `closure-classes-used.csv`, four PNG charts. Download: `data/raw/maps8-n3/` (service listings; towing polygons without attributes).
