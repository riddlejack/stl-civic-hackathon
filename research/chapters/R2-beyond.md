# R2. Beyond the traceable: re-reports for every service, more records, a bounded extrapolation

Written Wednesday 14 October 2026, from 12:20 p.m. Central, by the R2 session. Figures with derivations: `build/R2/figures.json`. Choices: `build/R2/decisions.json`. Every source tried: `build/R2/sources-found.md`. Scripts: `scripts/night/R2/01`–`08`. Tables: `build/R2/*.csv`.

## Admission

- **Done.**
  - Re-reports after closure, for all 97 request types with at least 300 closures (filed 1 Jan 2025 to 13 Oct 2026), by closing class and by kind of hand-off, with ten checks for confounds, each compared within type.
  - A test of whether a re-report signals unfinished work at all, using R1's per-request fates.
  - Two new traces against the city's own records: tree planting (it works, late) and tornado debris (it cannot be traced).
  - A low/high estimate of untraced crew-work jobs that may never be done.
  - A helper session ran the 90-minute keyless data hunt under this brief's rules; I made the joins.
- **Plainly: re-reports differ by class, but only by a few points, and they are not a completion measure.** Most of the gap arises while the job is still waiting. Where the city's record shows whether the work was done, re-reports do not follow it.
- **Not done.** No same-family matching (e.g. a "Missed Cut" after a weeds request). The 50 m spatial check covers the 14-day window only.
- **Could not establish.** Whether street, water, towing, traffic or refuse jobs were done. No public, keyless record dates that work. So the estimate rests on rates from mowing and board-up crews.
- **Assumed.** R1's kinds, traceability and fates as written at 12:25–12:38 p.m. (`build/R1/`). Rerun `04` and `05` if R1 revises them.
- No city dataset states a licence.

## 1. Re-reports after closure, by closing class (observed)

**Headline.** After a hand-off closure, the same problem was reported again at the same address within 14 days **6.7%** of the time. After a "done" closure of the same types it was **4.1%**: 1.6 times as often (risk ratio 1.59, 95% CI 1.48–1.71; 61 types; 34,848 hand-off and 54,359 done closures). Counting residents alone, the figures are **5.5% vs 3.5%**. "No action" closures fall in between (3.2% vs 2.1%). **Absolute count:** residents filed **2,942** reports within 14 days of hand-off closures (4,441 within 30 days) over 21 months. About **700** of them (all channels, about 900) exceed what the done rate of the same types predicts, roughly **400–500 a year**. These are extra reports, not undone jobs (derived).

| control (hand-off vs done, same types; 14 days unless stated) | hand-off | done | ratio |
|---|---|---|---|
| none (briefed definition) | 6.7% | 4.1% | 1.59 |
| 7 days / 30 days | 4.6% / 9.6% | 2.6% / 7.0% | 1.80 / 1.38 |
| first report at that address in a year (chronic sites out) | 4.0% | 1.9% | 1.99 |
| ignore reports within 24 h of the original (parallel callers) | 6.2% | 3.8% | 1.49 |
| same type within 50 m instead of the same address | 12.5% | 7.3% | 1.78 |
| non-recurring services (no refuse, weeds, street cleaning, dumping) | 5.3% | 2.1% | 2.16 |
| durable fixes (potholes, cave-ins, lights, trees, signs) | 3.3% | 2.1% | 1.84 |
| recurring services, 7 days (one collection cycle) | 6.1% | 3.4% | 1.57 |
| 30 days after the later of closure and the city's promise date | 8.3% | 6.5% | 1.22 |
| **same weeks for both: reported 15–44 days after the original filing** | **6.1%** | **6.0%** | **0.94** |
| same weeks, non-recurring services only | 7.2% | 4.0% | 1.44 |

**What cuts against it.** Hand-offs close a median 1.8 days after filing; done closures take 5.1 days. A window that starts at closure therefore covers more of the wait after a hand-off. Watched over the same weeks after the first report, the pooled gap disappears. Refuse, the largest hand-off type, reverses: 9.2% vs 13.4%. The gap survives for non-recurring services (7.2% vs 4.0%): towing 10.8% vs 5.5%, cave-ins 3.9% vs 1.9%, signal bulbs 12.2% vs 1.9%. Per type, hand-offs are re-reported more in 50 of 61 comparable types. The difference is clear in **18**, reversed in **3**, unclear in **40**, and **36** types have too few closures (`rereport_type_compare.csv`). The gap holds for each kind: crew work 6.4% vs 4.0%; owner enforcement 7.0% vs 3.9%; referral elsewhere 10.9% vs 5.2%. It also holds in each ward group (wards 1–5: 7.6% vs 4.6%; 6–9: 8.2% vs 3.4%; 10–14: 5.0% vs 3.2%). North-side closures are re-reported least after either kind.

**A re-report is not a sign the work was not done, where we can check** (observed; `proxy_check_*.csv`). For board-ups, R1's per-request fates show that requests with **no board-up recorded** were re-reported *less* within 30 days (5.9%) than those boarded by the promise date (15.4%) or late (11.8%). Weeds are flat: 11.5%, 11.5%, 12.5%. My own ledger check agrees (vacant lots: 10.8% with a cut by the promise date, 11.0% with none). It repeats the earlier result: weeds were re-filed at 21.2% with or without a billed cut. **Reading (inferred):** re-reports track visible, chronic problems and resident persistence. The 1.6× gap is real resident experience, a problem still there after the status said closed. It cannot be turned into "jobs never done", and I do not use it that way.

## 2. New traces against the city's own records (observed)

**Tree planting: done, late.** The cohort is requests closed "approved for next available planting" and filed 1 Jun 2025 to 28 Feb 2026. Both of their next planting seasons fall inside the dated record: maps8 "Planted last 365 days", 27 Oct 2025 to 1 Sep 2026, plus CW_PRINT `DATE_PLANTED`. Of **806** requests, **65.0%** have a street-tree planting after filing at the same address or within 25 m (55% by address alone). Unrelated refuse, pothole and light requests from the same months match at **4.8%**. In R1's terms:
- **0.2%** were planted by the 14-day promise date.
- **65.0%** were planted late, a median of **133 days** late.
- **34.7%** have no record by 13 Oct. Every promise in the cohort passed at least 30 days before 13 Oct; the latest was 14 Mar 2026.

Forestry's own planting queue (maps9 PLANTING_PLANNING, which carries the 311 REQUESTID on 139 rows) holds **43** of the 280 with no record and only 1 of the 526 with one. So at least 43 approved requests, filed 8–16 months ago, are confirmed still waiting. Two cautions:
- The record misses some plantings: 6 of 20 requests closed "complete" have none. So 34.7% is an upper bound on "not planted".
- Cancelled requests match at 46%, so many cancelled requests were planted anyway.

This hand-off works, about five months after a promise that seasonal planting cannot meet.

**Tornado debris: cannot be traced** (negative). The city's `Debris_Clearing` layer on ArcGIS Online records 76 street segments cleared 23–28 May 2025. Only 35 of 722 debris requests filed 16 May to 15 June 2025 lie within 30 m of one, and 33 of those came after the segment was cleared.

## 3. Bounded extrapolation (ESTIMATE)

**Volume (observed).** In the 12 months to 13 Oct 2026, **13,489** crew-work hand-off closures had no public completion record. For comparison, 4,808 were traceable (weeds, board-ups), and tree planting (565) is now traced. Owner notices and referrals to other agencies are excluded, because R1's rates are crew rates.

**Rates (R1, observed; only requests whose promise passed at least 30 days before 13 Oct).** On traceable crew work, the share with no record by 13 Oct ranges from **18.4%** (board-ups) to **37.0%** (missed-cut complaints). Vacant-lot weeds are 34.9%, and vacant-building weeds 30.8% (2025 ledger). R1's 2026 vacant-building figure (52.5%) is set aside, because that ledger may not bill contractor cuts (R2-09). The share done late ranges from 44.5% to 64.6%. Two more figures fall inside the never-done range: R1's pooled 32.2% and tree planting's 34.7%.

**Estimate: about 1,700 to 3,500 crew-work jobs a year that 311 closed as handed off may never be done**, and **4,100 to 6,000** a year done only after the promise date. Applied mechanically to every category, the never-done range would be 2,400 to 4,900. Calendar 2025, a year with a tornado and a refuse staff shortage, had 20,984 untraced crew-work hand-offs; on that volume the range is 2,200 to 4,600. Separately, **209** a year are closed with words saying the work is not funded.

| category | requests a year | never done (low–high) | plausibility (`extrapolation.csv`) |
|---|---|---|---|
| water repairs | 1,944 | 360–720 | one-off, no record; urgent outages may make the high end too high |
| towing | 1,941 | 360–720 | the owner may move a tagged car; may overstate |
| street, alley, sidewalk repair | 1,889 | 350–700 | referral or inspection, no record |
| debris and street cleaning | 1,229 | 230–460 | one-off clean-up at chronic sites |
| refuse containers, other refuse jobs | 946 | 170–350 | one-off, no record |
| forestry and parks (not planting) | 771 | 140–290 | tree orders have no finish dates |
| traffic signals, signs, lights, striping | 411 | 80–150 | parts on order, timing under study |
| other | 123 | 20–50 | |
| bulky pick-up | 2,048 | 0–60 | route service; high = own 7-day excess re-report (3.1 points) |
| refuse, recycling, yard waste | 1,821 | 0–50 | weekly route; 7-day excess 2.5 points; reverses over weeks 3–6 |
| snow and ice | 157 | excluded | self-resolving |

**Weakest assumption.** The estimate assumes street, water, towing, traffic and refuse crews fail at the rates measured on vacant-property mowing and board-up crews. No public record supports or refutes this. The only other evidence, each category's re-report rate, fails as a completion signal (section 1). The traced rates themselves rest on address joins and a weekly-posted billing ledger (R1). And "no record" includes work done but not recorded.

## 4. Sources (every source tried, with URLs and times: `build/R2/sources-found.md`)

- **Joined:** the maps8 planting layers, the maps9 planting queue and the AGOL tornado debris layer (section 2).
- **Found, but no finish dates.** A full read of public city web maps (3,108), feature services (442), apps and dashboards (4,934) and 15 department pages turned up 8 Cityworks saved-search ids not on the known list. None covers streets, cave-ins, signs, lights, refuse or water:
  - 6317 and 6318 are open easement-tree removal orders. Every date field is empty, yet 105 of their trees already show as stumps or vacant sites in the inventory (inferred: removed, order left open).
  - 4900 holds 4 contractor orders from 2022.
  - Five Prop NS searches hold vacant-building cases; `DATE_COMPLETED` is empty on all of them.
  - The stlwater.com repair list gives opening dates only, over a rolling 7 days, with no id.
  - The Forest Park tree layer is dated but covers the park only.
- **Stale or empty:** street-light verification ends December 2022; SLDC Streets dates are empty; sidewalk `DateRepair` is empty (N2). **No public, keyless record dates finished street, cave-in, sign, light, refuse, bulk or water work.**
- **Not available:**
  - Open311 without a key (HTTP 400 on all four calls).
  - maps9 water and utility-work folders (token required).
  - stlwater REST (401).
  - PDFs on www.stlouis-mo.gov, which robots.txt disallows.
- **Not used, by rule:**
  - the exposed internal Cityworks host named in the private disclosure.
  - The internal "qe" service on any host. Its service.stlouis-mo.gov copy lists the same 87 layers (cached catalog only); Jack's private disclosure should mention it.
  - maps6, whose robots.txt answered 500.
  - No saved-search id was guessed.

## What surprised me

- Watched over the same weeks, hand-offs and done closures are re-reported equally when all services are pooled, and refuse reverses.
- Board-ups with no record are re-reported *less*.
- Tree planting is a hand-off that works: about five months late, against a 14-day promise, with 43 approved requests confirmed still in Forestry's queue.
