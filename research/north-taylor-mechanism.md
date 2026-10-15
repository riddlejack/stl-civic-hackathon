# North Taylor: does lot-1 show the mechanism the video claims?

Written Wednesday 14 Oct 2026, 9:35–9:55 p.m. Central. Data on disk only, no network. Files end 13 Oct 2026. Script: `scripts/exec/north-taylor/01_mechanism.py` (aggregates in `build/north-taylor/mechanism.json`; parcel rows only in git-ignored `build/north-taylor/private/`). Figures: `research/north-taylor-mechanism-facts.csv`.

## Summary

**Not as the video implies.** Closing fast cannot explain why lot-1 was missed.
- Its closest twin is the land-bank lot on the same block, reported on the same days, minutes apart. It got the same reply five times ("on schedule to be cut, call CSB for details"), closed in 4–59 minutes, and was cut three times in 2026.
- 33 of the 36 cut neighbours had no weed report at all, and 31 had no weed request of any kind (**observed**).

What sets lot-1 apart is that no cut has been billed on it since October 2024 (**observed**). In 2026 crews cut 36 parcels on its block, on 15 days. They also cut all 21 parcels that used to be billed on the same dates as lot-1. They never cut lot-1 (**observed**). So it has dropped off the crews' rounds (**inferred**). The reports and closings did not cause that. What they did was tell the resident twice that the lot was on schedule, and nothing visible checks that reply against the cutting record (**inferred**).

**The honest mechanism, in one sentence:** the lot fell off the cutting rounds; 311 still told the resident, twice and within minutes, that it was "on schedule to be cut", the same answer its cut neighbours got; and nothing checks that answer against the cutting record, so the miss stayed invisible.

**The systemic number.**
- 479 of the 1,724 vacant-lot and vacant-building weed reports closed "on schedule to be cut" in 2026 (27.8%) were on parcels with no cut billed at any time in 2026. These are reports filed by 13 Sep and matched to a parcel.
- On land-bank parcels, where the city itself is the owner, it was 70 of 550 (12.7%).
- Closing speed does not separate the two groups. The no-cut share is 25.0% for reports closed within an hour, 31.5% for 1–24 hours and 27.2% for over a day (**observed**).

**A correction to R1.** R1 described 539 parcel-dates as closed "on schedule". In fact 257 were closed "on schedule" and 282 "added to rotation" (**observed**).

**What I could not establish.**
- Why the lot dropped off. The public maintenance list dates from May 2023, and the ledger has no contractor, crew or route field.
- Whether it was cut but not billed. A 9 Sep complaint calls its cut "incomplete".
- Whether storm debris kept mowers off it. Debris work has not been in the ledger since 2021.

## 1. The block, parcel by parcel

Lot-1's assessor city block has 57 parcels: lot-1 plus 56 neighbours. Block membership uses the ledger CITYBLOCK, or else characters 2–7 of the MSD handle, as R1 did. A "cut" is one distinct date with a 'Grass Maint' or 'Weed-Grass' charge in the [Forestry billing ledger](https://www.stlouis-mo.gov/data/upload/data-files/forestry-service-records.csv), whose dates are weekly posting batches. Weed reports are 2026 "Weeds-Vacant Lot" and "Weeds-Vacant Bldg" requests in the [311 file](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip), joined to the parcel through N1's address join. Lot-1's reports matched its land-bank address exactly, with one candidate parcel. All figures are **observed**.

| | Lot-1 | Neighbours cut in 2026 | Neighbours not cut in 2026 |
|---|---|---|---|
| Parcels | 1 | 36 | 20 |
| Land-bank owned ([LRA inventory](https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_INVENTORY.csv), 13 Oct) | yes | 23 | 2 |
| On Forestry [maintenance list](https://www.stlouis-mo.gov/data/upload/data-files/forestry-maintenance-properties.csv) (dated 2023-05-26) | Vacant Lot | 32 (25 Vacant Lot, 7 Vacant Building) | 5 |
| Latest ledger property type "Vacant Lot" | yes | 28 | 2 |
| No cut billed at all 2019–26 | no | 0 | 11 |
| Cut in 2024 / in 2025 | 4 cuts / 0 | 30 / 22 parcels | 5 / 2 parcels |
| With a 2026 weed report | 2 reports | 3 parcels, 7 reports | 1 parcel, 1 report |
| Minutes to close those reports | 7.4 and 12.5 | median 12.7; 5 of 7 within an hour | about 109 days |
| Closing words | "on schedule to be cut, call csb for details" (2) | same words (6 reports on 2 parcels); "added to rotation" (1 report, after 147 days) | "added to rotation" |
| Billed cut after the report | none | 7 of 7, a median 28 days later (2 within 14 days) | none |

**Jack's questions, answered.**
- **Did the neighbours have requests too?** Mostly not. 4 of the 56 neighbours had a 2026 weed report. Of the 36 cut neighbours, 33 had none and were cut anyway. Two of those 33 drew a "missed cut" complaint (closed "supervisor notified"), so 31 had no weed request of any kind.
- **Were theirs also closed within minutes, "on schedule"?** Yes, where the comparison is closest.
  - The land-bank lot on the same block, reported alongside lot-1 (2 Jul and 28 Jul, minutes apart), had 5 reports. All closed "on schedule to be cut, call csb for details", in 3.8 to 58.7 minutes, and the lot was billed 3 cuts in 2026.
  - A land-bank vacant building got the same words after 15 hours and was cut.
  - A private vacant building was closed "added to rotation" after 147 days and was cut once.
  - Lot-1 got the same words in 7.4 and 12.5 minutes, and was not cut.
  - So neither the words nor the speed explain the difference (**inferred**).
- **Did the report bring the crew?** No sign of it. The reported neighbours were cut a median 28 days after their reports, on block cut days: on 4 of the 5 days a reported neighbour was cut, an unreported neighbour was cut too. This matches R1's citywide baseline (**reported**, `research/chapters/R1-trace.md`): reported rotation lots were cut within 14 days 17.4% of the time, against 16.9% for unreported same-block lots, so a reported lot on the rotation is cut on the rotation's timetable.
- **Were crews on the block after lot-1 was reported?** Yes, repeatedly. After the 2 Jul report, 34 block parcels were cut on 9 days. After the 28 Jul report, 28 parcels were cut on 7 days. After the 9 Sep "cut incomplete" complaint (closed in 24 hours, "supervisor notified"), 27 parcels were cut on 6 days. None of those cuts was on lot-1.
- **Who on the block is not cut?** 18 of the 20 uncut neighbours are not land-bank parcels. Eleven had no cut billed at any time in 2019–26 (they are probably occupied homes that Forestry does not mow, **inferred**). Of the 2 land-bank parcels among them, one was last billed in September 2025 as a vacant lot and has had no report: a second miss on the block that nobody reported. The other is now billed as a "Fenced & Locked or Paved Lot" and was last cut in 2024.
- **The two lots reported alongside lot-1** (N5's story) are both land-bank lots on the 2023 list. One is on lot-1's own block (3 cuts in 2026); the other is on the next block (1 cut in 2026). Both were cut.

## 2. The systemic pattern, restated

**What can and cannot be split.** No public file shows Forestry's 2026 rotation. R1 *defines* "on the 2026 rotation" as at least one cut billed in 2026, so a parcel with no 2026 cut is off the rotation by definition. That split is circular. The only list is the maintenance property file dated 2023-05-26. Its ArcGIS service, [FORESTRY_CATEGORIZATION](https://maps6.stlouis-mo.gov/arcgis/rest/services/FORESTRY/FORESTRY_CATEGORIZATION), returned "Service not started" in the data audit (**reported**, `research/data-audit.md`). The meaningful splits are therefore by the 2023 list, by ownership and by cut history.

**Base.** The base is 2026 Weeds-Vacant Lot and Weeds-Vacant Bldg requests closed "on schedule to be cut …", filed by 13 Sep 2026 (so the ledger runs at least 30 days past each report) and matched to a parcel: 1,724 requests on 1,318 parcels. **Observed** throughout.

| Split | No cut billed in 2026 |
|---|---|
| **All on-schedule closures** | **479 of 1,724 (27.8%), on 362 parcels** |
| Vacant-lot reports / vacant-building reports | 156 of 721 (21.6%) / 323 of 1,003 (32.2%) |
| Land-bank parcels / other parcels | 70 of 550 (12.7%) / 409 of 1,174 (34.8%) |
| 2023 list "Vacant Lot" / "Vacant Building" / not on the list | 118 of 571 (20.7%) / 114 of 571 (20.0%) / 220 of 468 (47.0%) |
| Vacant-lot reports on land-bank lots on the list | 49 of 378 (13.0%) |
| Cut in 2025 / cut in 2024 but not 2025 / cut only in 2019–23 / no cut 2019–25 | 14.4% / 24.9% / 48.6% / 58.8% (n = 766 / 519 / 177 / 262) |
| Parcels like lot-1: land bank, listed "Vacant Lot", cut 2019–24, none in 2025 | 34 of 205 (16.6%), on 27 parcels |
| Closed within 60 minutes / 1–24 hours / over 24 hours | 25.0% / 31.5% / 27.2% (n = 713 / 603 / 408) |
| For comparison, closed "added to rotation" (lots / buildings) | 55.7% (79) / 69.0% (548) |

- **Speed does not separate the outcomes.** On-schedule closures on parcels never cut in 2026 took a median of 175 minutes, and 37.2% closed within the hour. On parcels that were cut, the median was 110 minutes and 43.0% closed within the hour.
- **The same words regardless of history.** 262 "on schedule" replies went to parcels with no cut billed at any time in 2019–25, and 58.8% of those parcels saw no cut in 2026 either.
- **R1's figure, replicated exactly and split.** R1 counted 539 of 1,761 parcel-dates (30.6%) on parcels with no 2026 cut. Of those, 257 had an "on schedule" closure and 282 had only "added to rotation" closures. Among R1's 1,310 on-schedule parcel-dates, 257 (19.6%) are on parcels with no 2026 cut. R1's sentence "yet were closed 'on schedule to be cut'" should read "closed 'on schedule to be cut' (257) or 'added to rotation' (282)". R1's 1,761 and the 1,724 above count different things. R1 counts parcel-dates closed with either phrase, on blocks with a same-block control. The 1,724 are requests closed "on schedule" only, on any block.
- **Is lot-1 an instance?** Yes. Its two reports are 2 of R1's 539, 2 of the 479, and fall in the land-bank, listed-lot cell (49 of 378).
- **Is it effectively off the rotation?** Yes (**inferred**). The evidence: its last billed cut was 24 Oct 2024; there are none in 2025 or 2026; in 2026 crews worked both its block (15 days) and its old billing group (all 21 parcels, section 3); and by R1's own definition it is off the 2026 rotation. Whether Forestry's own current list still carries it cannot be seen.

## 3. What distinguishes lot-1 from its cut neighbours

| Field | Lot-1 | Cut neighbours | Distinguishes? |
|---|---|---|---|
| Ownership | land bank, "Available", acquired 2015 (tax suit) | 23 of 36 land bank | no |
| 2023 maintenance list | Vacant Lot | 25 of 36 Vacant Lot | no |
| MSD land use / class | 1010 / 17 | 25 / 22 of 36 | no |
| Ledger property type | Vacant Lot | 28 of 36 | no |
| Charge per cut | $62.82 (every cut 2022–24) | $33.97–$109.49 | no. The lot is 5,871 sq ft against a block land-bank median of 3,681, so the charge likely tracks size (**inferred**) |
| Contractor, crew or route | not recorded | not recorded | cannot test: the 9 ledger columns are CITYBLOCK, HANDLE, LASTDATE, LEGACY, PARCEL, PROPERTYTYPE, SERVICEAMOUNT, SERVICEDATE, SERVICETYPE |
| Billing dates (a route proxy) | shared its block's cut days on 7 of its 24 cut days in 2019–24, and on none of 4 in 2024 | most cut together on block days | yes: lot-1 was billed with a different group |
| Land-bank side files | no offer, archived offer, garden permit or PROPNS nomination; still in the available inventory | — | no innocent explanation found (the garden-permit file has only 34 rows) |

**Lot-1's old billing group kept being cut.** 21 parcels were billed on all 8 of lot-1's 2023–24 cut dates: 19 of them land-bank, all listed "Vacant Lot", on 6 other city blocks and none on lot-1's own. All 21 were cut in 2026, on 6 dates from 21 Apr to 28 Sep, and 20 of them after lot-1's second report. None of those 6 dates is a day its block was cut. In 2025, 9 of the 21 were cut, on a single date. The 2025 ledger is thin everywhere: 8,780 parcels were billed, against 17,295 in 2024 and 16,118 in 2026 (**observed**). The ledger cannot say whether a shared date means a crew, a contract or an invoice batch. Either way, the group lot-1 used to be billed with carried on in 2026 without it (**inferred**).

**Is it luck whose lot gets cut?** Not in the sense of each visit being a coin toss. Whether a lot is cut is a stable state: among land-bank lots listed "Vacant Lot" and cut in 2024, 97.0% of those also cut in 2025 were cut in 2026 (3,054 of 3,149). For those with no 2025 cut, it was 88.3% (3,413 of 3,867) (**observed**). Lot-1 is one of the minority that dropped and stayed off. Nothing in the public record explains why it, rather than a neighbour, dropped: ownership, list category, land use and type all match. From outside, the drop looks idiosyncratic. Once it happened, it persisted (**inferred**).

Citywide, 795 of 7,843 land-bank lots listed "Vacant Lot" (10.1%) look like lot-1: cuts billed in 2019–24, none in 2025 or 2026. Only 27 of them drew an "on schedule" reply in 2026 (**observed**). That makes 795 an upper bound: some will have been fenced, sold or reclassified since the 2023 list.

## 4. The honest mechanism, and what the video may say

**Observed.**
1. Lot-1 was billed for 2–6 cuts a year in 2019–24 and none since 24 Oct 2024.
2. In 2026 crews cut 36 other parcels on its block on 15 days, 34 of them after the first report, and cut all 21 parcels from its old billing group.
3. Both reports closed in 7.4 and 12.5 minutes as "on schedule to be cut, call CSB for details". The same-block land-bank lot reported alongside it got the same words five times, in 4–59 minutes, and was cut. 33 of 36 cut neighbours had no weed report.
4. The second report, 26 days after the first, got the same reply with no cut billed in between. The 9 Sep complaint closed "supervisor notified", and no cut followed in the 34 days to 13 Oct.
5. The public 311 record carries no field linking a request to a cut.

**Inferred.**
- The lot fell off the cutting rounds.
- Neither the report nor its closing decided whether it was cut.
- The closing words are a standard reply, not a check against the cutting record. Nothing in the system compares that reply with the ledger, so the miss shows up nowhere except in a resident's repeat reports.
- What I cannot tell is whether the 311 agent consulted a Forestry list that still carries the lot, in which case the list and the crews disagree, or gave the reply without looking.

**Sentences the video can say** (each true as worded):
- "This city-owned lot on the 1700 block of North Taylor was reported twice this summer. Both times, 311 closed the report within minutes: 'on schedule to be cut.'" (observed)
- "The city's own records show no cut billed on it since October 2024. This year crews cut 36 other properties on its block, on 15 different days." (observed)
- "A city-owned lot on the same block was reported on the same days, got the same answer just as fast, and was cut. Most of the properties cut on the block were never reported at all. The report didn't decide who got cut. The crews' rounds did, and this lot had fallen off them." (observed, then inferred)
- "The answer said 'on schedule' anyway. Nothing checks that answer against the cutting record, so the miss stayed invisible." (inferred)
- "Across the city this year, 479 of 1,724 'on schedule to be cut' answers, more than one in four, went to a property where the city billed no cut all year." (observed). The stricter version: "on city-owned land, one in eight" (70 of 550).

**Sentences the video cannot say:**
- "Because 311 closed it in minutes, nobody noticed", or "closing at the hand-off is why this lot was missed." The same-block lot reported alongside it was closed the same way, just as fast, and was cut.
- "Its neighbours were reported too." Only 3 of the 36 were.
- "Report a lot and it gets cut", or "the report was ignored." A report does not change when a lot is cut (R1 baseline; block reports were cut a median 28 days later, on block days).
- "Nobody cut this lot all year." The record shows only that no cut was billed, and the 9 Sep complaint says a cut was "incomplete".
- "It's on Forestry's mowing list." Say "it was on Forestry's 2023 maintenance list".
- "311 lied" or "the answer was false." We cannot see what the agent checked.
- "Both promise dates passed." The first (30 Sep) did; the second (26 Oct) falls after the files end.
- "One in three on-schedule closures had no cut" (R1's 30.6%). That figure mixes in 282 "added to rotation" closures. Use 27.8% of requests (479 of 1,724), or 19.6% of R1's parcel-dates.
- "Who gets cut is random." It is a stable roster. What cannot be seen is why one lot dropped off it.

## Method notes and negative results

- **Joins.** Parcel matches use N1's `request_parcel`, through MSD's [parcel layer](https://services1.arcgis.com/plGX8WiX9ylnkcee/arcgis/rest/services/Development_Review/FeatureServer/9). Land-bank status comes from `lra` (the LRA inventory of 13 Oct 2026). List categories come from `maint_props` (the 2023-05-26 file).
- **Cuts.** Cuts come from the `cuts` table (distinct parcel, service type and date). They run to 13 Oct 2026.
- **R1 replication.** The replication uses R1's own MSD-only block table and reproduces 1,761 and 539 exactly. Adding ledger-only parcels gives 1,762 and 540.
- **Negative results.**
  - No 2026 rotation or route file exists on disk.
  - The ledger has no contractor, crew or route column.
  - The maintenance list is 41 months old.
  - Debris work is not in the ledger after 2021, so the post-tornado debris N5 saw on the block's 2025 aerial cannot be tested as a reason for skipping the lot.
  - No 2025–26 311 request of any other type names lot-1.
- **Privacy.** No parcel id, request id or address below block level appears in this file, the facts CSV, the script or `mechanism.json`. The parcel-level rows are in `build/north-taylor/private/block_parcels.csv` and `block_requests.csv`, which are git-ignored.
