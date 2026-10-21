# Open-queue reality check: are the 14,902 open, past-promise requests real waits?

## Summary

**What we found.** The headline set is 14,902 requests in the city's public 311 file that were filed since 1 January 2025, are still open and are past the city's promised date (data as of 13 October 2026). I checked each one against every independent completion or work record already on disk. The classes are mutually exclusive, and each request takes the first one that applies:

| Class | Requests | Share | Label |
|---|---:|---:|---|
| (a) A record shows the work done after filing, so "open" is clerical | 388 | 2.6% | observed |
| (b) A city work record created after filing is still pending | 1,206 | 8.1% | observed (952, or 6.4%, under the strict test) |
| (c) Possibly superseded: a later request with the same code at the same address is closed | 333 | 2.2% | observed |
| (d) Likely administrative leftover (sirens, no water, mosquito spraying, 90+ days past promise) | 409 | 2.7% | inferred |
| (e) No evidence either way | 12,566 | 84.3% | observed |

- **Estimated.** Extending E1's 30-page samples to the whole of each of the 10 largest types raises (b) to about 2,520 (17%). Most of the rise comes from weeds on occupied property and from city tree inspections, where most sampled pages carry a pending work order. The same step raises (a) to about 500 (3.4%).
- **Observed.** At the same age, the open-past-promise share has been about the same every year since 2019. A year after filing it was 3.6–4.2% for the 2019–2024 cohorts and is 4.3% for 2025. For January–June filings seen on 13 October of the same year it was 6.7–11.0% for 2019–2025, and 8.0% for 2026.
- **Observed.** There is a long tail, but it is not a stable 2%. It shrinks with age. Requests still open today: 2.4% of 2024 filings, 2.1% of 2023, 1.5% of 2022 and 0.7% of 2019.

**What I could not establish.** For 84% of the set, no public record shows the work done or pending. Cave-ins, bad condition in the right of way, illegal use, vehicle towing, lead inspections and most code-enforcement types have no completion record on disk. E1's status pages showed nothing attached for 0 of 30 cave-ins and 0 of 30 in each of five other types. A missing record does not mean the work was not done. The ledger therefore cannot prove that residents in (e) are still waiting. It shows only that nothing on record says otherwise, and that the city's own Cityworks queue also calls 97.2% of comparable requests open (reported, `research/cityworks-active-queues.md`).

## Base and method

**Observed.** The base query is `requests WHERE ts_init >= '2025-01-01' AND status_group = 'open' AND ts_promised < '2026-10-13 23:59:59'` in `build/stl.duckdb`, opened read-only. It returns 14,902 unique requests: 5,341 filed in 2025 and 9,561 in 2026. The median wait past the promise is 438 days for 2025 filings and 83 days for 2026 filings. Raw statuses are Disptch 6,678; NEW 3,841; Pending 1,983; Inspect 1,666; and smaller groups. Source: [311 file](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip), `build/E5/summary.json`.

**Observed.** These records were joined. Nothing was fetched.

| Record | Request types | Join | Done (a) | Pending (b) |
|---|---|---|---|---|
| Forestry mowing ledger (`request_ledger_flags`; N1 parcel join, as in R1) | 10 weed and cut-complaint codes, 1,738 base rows joined | parcel | cut on or after the filing date | (none: the ledger records cuts only) |
| 27 Forestry work-order [saved searches](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json), 27,267 unique orders (loader from `research/cityworks-gap-scripts/forestry_analysis.py`) | 8 tree codes | exact normalized address; order started no earlier than one day before filing | valid finish date after filing | order still open, with no finish |
| Cityworks [QE layer 78](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/78), sidewalk work orders (all 1,738 rows are CLOSED) | Sidewalk Repair | exact address | finish on or after filing | (layer holds closed orders only) |
| Building Division [board-up layer](https://maps8.stlouis-mo.gov/arcgis/rest/services/BUILDING_DIVISION/BldgDiv_Boardups/MapServer/0) (R1 method) | Vacnt Bldg Unsecured, LRA Board up | parcel or address | boarded on or after filing | record created after filing with no board-up date |
| Building Division [demolition permits](https://maps8.stlouis-mo.gov/arcgis/rest/services/BUILDING_DIVISION/Demolitions/MapServer/0) (R1 method) | LRA Demo Submission, Building Collapse | parcel or address | permit Completed after filing | permit submitted after filing, not completed |
| E1 status-page reads (`build/E1/private/linked_requests.csv`) | 300 sampled base rows, 80 with items | request id | page shows a finish | post-filing work order with no finish |
| Later request with the same code and address (`requests`) | all | normalized address and problem code | (none) | (none; feeds class c) |

Scripts are in `scripts/exec/E5/` (`01_ledger.py` … `04_extrapolate.py`). Row-level output stays in `build/E5/private/`. Published outputs hold aggregates only.

**Observed.** Work orders the address join matched to a date *before* the request are not counted as evidence. 204 tree requests have only such older orders at their address, and they stay in (e).

## (a) Done after filing: 388 (2.6%)

**Observed.** By record:

| Record | Requests |
|---|---:|
| Mowing ledger cut after filing | 298 |
| Completed demolition after filing | 42 (37 of 175 LRA demolition submissions; 5 building collapses) |
| Forestry work order finished after filing | 24 (median 184 days from filing to finish) |
| Board-up done after filing | 17 (of 160 Vacnt Bldg Unsecured) |
| Sidewalk work order finished after filing | 5 |
| E1 status page shows a finish | 2 |

**Observed.** The mowing-ledger share is concentrated in cut complaints. Missed Cut - VBldg has 146 of 212 (68.9%) with a cut after filing. Unsatisfy Cut -VBldg has 58, Missed Cut - V Lot 34 and Unsatisfy Cut - VLot 29. Only 14 of 230 Weeds-Vacant Bldg, 7 of 194 Weeds-Vacant Lot and 10 of 1,062 Weeds-Occupied Ppty requests show a cut. Of all 298 cuts, the median comes 53 days after filing and 171 come within 60 days. [Forestry service records](https://www.stlouis-mo.gov/data/upload/data-files/forestry-service-records.csv), `build/E5/years.json`.

**Observed.** The two VBldg cut-complaint codes look like a 2025 closing lapse. None of their 2023 or 2024 filings is still open. Of 2025 filings, 62.1% of Missed Cut - VBldg (162 of 261) and 70.0% of Unsatisfy Cut -VBldg (56 of 80) are still open, against about 12% for 2026 filings. `build/E5/years.json`.

**Inferred.** A cut long after filing may be routine rotation rather than a response to the request. If weed cuts more than 60 days after filing are dropped, (a) falls to 261 (1.8%).

## (b) Pending in the city's own work records: 1,206 (8.1%)

**Observed.** Inspect City Tree accounts for 892 of the 1,206. It has an open Forestry work order at the same address, started after filing, for 60.2% of its 1,481 open requests. The rest: City Tree Down 89, Broken/Hanging Limb 74, City Tree Limb Down 53, E1 status-page pending 62 (22 weeds on occupied property, 10 sewer laterals, 6 sidewalks among them), Stump Removal 20, demolition permits not yet completed 18 and board-up records without a board-up date 7. `build/E5/ledger_by_type.csv`.

**Observed (validation).** On the 30 E1-sampled Inspect City Tree requests, all 15 address-join matches were confirmed by the status page, and the page showed 12 more that the join missed. On the 30 E1-sampled City Tree Down requests, the join found 7 matches and the pages showed none. So for City Tree Down, Broken/Hanging Limb, City Tree Limb Down, Stump Removal and other tree types, an address match may belong to a sibling request at the same tree. The strict count (b) keeps only status-page, board-up and demolition evidence plus the validated Inspect City Tree join: **952 (6.4%)**. The other 254 are address-only. `build/E5/years.json`.

**Estimated.** E1 read 30 random pages in each of the 10 largest types. Applying each type's sampled share to the whole type gives these pending counts:

| Type | Base | Sampled pages pending | Estimated pending (95% interval) |
|---|---:|---:|---:|
| Inspect City Tree | 1,481 | 24 of 30 | about 1,185 (928–1,340) |
| Weeds-Occupied Ppty | 1,062 | 22 of 30 | about 779 (590–911) |
| Sidewalk Repair | 1,124 | 6 of 30 | about 225 (107–419) |
| Sewer Lateral Defect | 455 | 10 of 30 | about 152 (87–233) |
| Cave-Ins, Bad Condition, TDebris, LRA Tree, Ppty Maint Code-Ext, City Tree Down | 3,293 | 0 of 30 each | 0 (upper bounds 37–140 per type) |

With the observed counts kept for every other type, estimated (b) is about **2,520 (17%)** and estimated (a) about 500 (3.4%). `build/E5/extrapolate.json`.

## (c) Possibly superseded duplicates: 333 (2.2%)

**Observed.** 1,467 base requests have a later request with the same problem code at the same normalized address, and 393 of those later requests are closed. Classes (a) or (b) already take 60 of the 393, which leaves 333 in (c).

**Observed (correction).** The figures given beforehand, 1,530 and 448, come out only if the join also matches requests with a *blank* normalized address. 73 base rows have a blank normalized address, so those matches are artifacts. The corrected figures are 1,467 and 393.

**Observed.** Within the set, there are 496 extra rows beyond one per distinct code at a non-blank address. These are second or later open requests for the same problem at the same place. Counted as jobs rather than requests, the set is at most about 14,400. `build/E5/summary.json`, `build/E5/years.json`.

**Inferred.** A later closed request suggests the problem was handled, or at least looked at, under the newer ticket. It does not prove it.

## (d) Likely administrative leftovers: 409 (2.7%)

**Inferred (rule).** A request falls in (d) if the service is time-bound and the request is at least 90 days past promise. The time-bound services are a household with no water, a weather siren not heard in a monthly test, and seasonal mosquito spraying. That gives Sirens Not Heard 220, NOWATER 109 and Mosquito Spraying 80.

**Observed (support).**
- NOWATER: closed requests are usually closed the same day. The median is 0.1–0.2 days, and 94–99.7% close within 7 days, for 2023–2026 filings. Yet 17.3% of 2024 and 17.5% of 2025 filings are still open.
- Sirens Not Heard: 3.5% of 2023 filings are open, then 69.4% of 2024 and 96.9% of 2025.
- Mosquito Spraying: 81.1% of 2023 filings and 98.6% of 2025 filings are open.

**Inferred.** For sirens and mosquito spraying, the 311 queue is in practice never closed, so "open" carries no information. The leftover rule could reasonably be widened. Mosquito Breeding (93.9% of 2025 filings open, 102 in the base) and tornado debris (75.9% of 2025 filings open, 365 in the base, a median 315 days past promise, and 0 of 30 sampled pages with any work attached) are candidates. I left them in (e) because a resident could still be waiting on either. `build/E5/years.json`.

## (e) No evidence either way: 12,566 (84.3%)

**Observed.** These types have no completion record on disk and zero rows in (a) or (b):

| Type | Base | In (e) |
|---|---:|---:|
| Cave-Ins | 1,233 | 1,196 |
| Bad Condition | 621 | 610 |
| Vehicle Towing | 451 | 442 |
| Ppty Maint Code-Ext | 382 | 373 |
| Illegal Use | 367 | 362 |
| TDebris-alley/street | 365 | 364 |
| Lead Insp | 266 | 254 |
| Illegl Use-Opn Storg | 255 | 242 |

Sidewalk Repair (98.5% in e) and Weeds-Occupied Ppty (96.4% in e) do have partial records. In both, the observed ledger is far below what the E1 pages suggest. `build/E5/ledger_by_type.csv`.

## Is there a stable long tail? By filing year

**Observed.** Share of each year's filings still open today:

| Filed | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Requests | 107,228 | 107,854 | 100,247 | 107,219 | 109,180 | 105,572 | 124,077 | 92,455 |
| Open now | 745 | 845 | 1,092 | 1,630 | 2,274 | 2,513 | 5,370 | 11,135 |
| Share open now | 0.69% | 0.78% | 1.09% | 1.52% | 2.08% | 2.38% | 4.33% | 12.04% |
| Open past promise on 13 Oct of the following year (rebuilt) | 3.95% | 4.17% | 4.07% | 3.71% | 3.84% | 3.58% | 4.30% | n/a |

Source: `build/E5/years.json`.

**Observed (method).** The past open state is rebuilt from this one file. A request counts as open on 13 October of year Y+1 if it is open now, or if its close or cancel timestamp falls after that date. Requests deleted from the file cannot be seen.

**Observed.** January–June filings, seen on 13 October of the same year, were open past promise at these rates: 8.45% (2019), 7.70%, 11.01%, 8.24%, 9.24%, 6.70%, 8.55% (2025) and 8.02% (2026). `build/E5/late_closures.json`.

**Inferred.** The 2025 and 2026 shares are normal for their age. The 14,902 is the usual state of the system, not a recent spike. That cuts both ways: the problem is structural, and it would be wrong to present it as a new backlog.

**Observed.** The tail decays slowly. Of the requests open a year after filing, the share still open today is 66.1% for 2024, 53.7% for 2023, 40.9% for 2022, 26.7% for 2021 and 17.6% for 2019. 18,580 requests filed in 2019–2024 closed more than a year after filing. 18.8% of those closed on 22 days that each saw 100 or more such late closures, which suggests batch clean-up. Their most common closing phrases are "work completed" (2,826), blank (1,772), "tree scheduled for removal" (1,350) and "no problem found" (994). `build/E5/late_closures.json`.

**Observed.** Types differ sharply:

- *Chronic, multi-year:* Sidewalk Repair has 42.7% of 2022, 54.4% of 2023 and 51.3% of 2024 filings still open. Lead Insp has 76.6–86.8% of 2023–2025 filings open. Inspect City Tree has 8.3–17.6% open.
- *Eventually closed:* Cave-Ins, Bad Condition, Weeds-Occupied Ppty, Vehicle Towing, Single Light Out and Illegal Use have about 0–0.7% of 2022–2024 filings open. For these, the 2025–26 open state has been temporary in past years, although nothing on record says whether the late close came with the work or with a clean-up.

**Inferred.** So the 2%-after-two-years residue is real, but it is concentrated in a few types: sidewalks, lead inspections, tree inspections, sirens and mosquito spraying. It is not spread evenly. Every time a cohort's tail has been checked, it is mostly still open after a further year.

## What the entry can and cannot say

**Inferred.** "Open" is not being over-read if the entry says what the records show. The share we can prove clerical is small: 388 (2.6%), or 1,130 (7.6%) if every superseded duplicate and every leftover is also treated as clerical. Even in that worst case, about 13,770 requests remain open past promise with no record that the work happened. What the entry cannot say is that all 14,902 are residents still waiting. For 84% there is no record either way, and the city's own late closures include batch clean-ups and "no problem found".

**Inferred.** Strongest honest wording: *"Of 14,902 requests the city's own systems still list as open past their promised date, fewer than 3% have any record of the work being done, about 8% have city work orders still pending, and for most of the rest no public record says either way. That has been the normal state of the queue every year since 2019."*

## Negative results and limits

- **Observed.** No completion record exists on disk for cave-ins, right-of-way conditions, towing, code enforcement, lead, water (beyond N2's live list of about 26 orders) or street lights. These types make up most of (e).
- **Observed.** The sidewalk layer holds closed orders only, so it cannot show pending sidewalk work. Only 5 of 1,124 open sidewalk requests match a finished order.
- **Observed.** The mowing ledger can show a cut, not an owner's own cut. For Weeds-Occupied Ppty that limits it to city abatement, and only 10 of 1,062 show one. R1 notes the Grass Maint ledger is thin for 2025 vacant-lot filings. That affects absence only, not the cuts counted in (a).
- **Reported.** Cityworks `Completed=1` is set on about 48% of open requests but does not mark finished field work, so it is not used here (`research/cityworks-active-queues.md`).
- **Observed.** Address joins can attribute a work order to the wrong request at a shared address. The Inspect City Tree join was validated (15 of 15). The City Tree Down join was not (0 of 7 confirmed).
- **Inferred.** Class (d) depends on my judgment of which services are time-bound. Its size moves by several hundred depending on whether Mosquito Breeding and tornado debris are included.
