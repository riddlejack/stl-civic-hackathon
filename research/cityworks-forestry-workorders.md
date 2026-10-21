# Forestry work-order coverage and 311 candidate links

## Summary

**Observed.** The 27 Forestry Work Order saved searches returned 34,739 memberships and 27,267 unique work orders after deduplication. All extracts passed before/after count checks; 4,573 work orders appeared in more than one search, with zero conflicts in status, finish, closure, initiation, template, address or coordinates. The searches were retrieved from 18:48:27 to 18:53:30 UTC on 14 October 2026. [QE catalog](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json)

**Observed.** Among 572 converted tree-work-order requests in the R1 cohort, 88 have a compatible work order at the same normalized address and 74 have a chronology-valid `ActualFinishDate` through 13 October. Six exact-address candidates finish by the request promise; 68 finish later, with a 268.5-day median delay after the promise. The broader address-or-coordinate sensitivity finds 89 finish candidates; all 89 are trimming. These are candidate links because the QE schemas expose no request key. [311 source](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip), [QE98](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/98), [QE99](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/99)

**Inferred.** The earlier claim that most 2025 removal hand-offs had closed does not survive as completion evidence. In the extracted current-open saved-search union, 8 of the same 294 requests have an exact-address order initiated after filing and 10 have an address-or-coordinate candidate, up from the capped sample's reported 3 and 7. More importantly, there is no general closed all-city removal search, so absence from current-open searches cannot establish completion. [311 source](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip), [QE63](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/63), [QE108](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/108)

## Retrieval and grain

**Observed.** Each layer was downloaded through the read-only QE endpoint with the shared strict field whitelist. Every extraction reports equal `count_before`, saved rows, `count_after` and unique work-order IDs. The analysis excludes the sidewalk and speed-control searches and writes no work-order IDs, request IDs, exact addresses or coordinates to its public outputs. Exact layer URLs and layer-level counts are in the [aggregate CSV](cityworks-forestry-workorders-aggregates.csv); the catalog is the source for saved-search names. [QE catalog](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json)

**Inferred.** Operation labels come from public saved-search membership and template IDs: removal, stump and trim are reliable enough for a compatibility screen, but they are not a complete template dictionary. “Open” below means `Status` is not `CLOSED` within the extracted saved-search union. It is not a claim that the physical work remains unfinished. [QE63](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/63), [QE91](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/91), [QE96](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/96)

## What the closed searches contain

**Observed.** The four searches below supply the closed records. Counts are saved-search memberships and overlap, so they must not be added. QE98 and QE99 provide closed trimming/pruning records beyond the Forest Park search; QE108 provides a small contractor-removal subset. No saved search provides general closed all-city removal coverage. [QE catalog](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json)

| QE layer | Catalog name and scope | Rows | `ActualFinishDate` present | Finish in 2025 through 13 Oct 2026 | Finish before initiation |
|---:|---|---:|---:|---:|---:|
| [89](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/89) | Closed WOs (FP), Forest Park | 5,596 | 5,031 | 2,099 | 1,601 |
| [98](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/98) | Tree Trim Within 1 Year, rolling trim | 3,555 | 3,555 | 3,553 | 127 |
| [99](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/99) | Mr. Robot Pruning | 2,297 | 2,297 | 1,268 | 0 |
| [108](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/108) | ACSTL Removal Closed | 28 | 28 | 28 | 0 |

**Observed.** Deduplication leaves 10,489 `CLOSED` work orders and 16,778 in other statuses. The closed union has 5,961 finish dates from 1 January 2025 through the 13 October 2026 comparison cutoff, while 565 closed records have no finish date. The snapshot itself includes 14 October activity; the comparison stops on the last complete 311 calendar day. [QE89](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/89), [QE98](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/98), [QE99](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/99), [QE108](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/108)

**Observed.** Search names do not reliably encode status. Layer 64, “Trees to be removed,” has the same membership as layer 63 and all its rows are `NEW`; it is not a closed-removal source. [QE63](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/63), [QE64](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/64)

## Current-open saved-search union

**Observed.** Of the 16,778 non-`CLOSED` records, 10,626 were initiated more than one year before the snapshot. Projected finish is present on 16,776, and 15,637 projected dates precede 14 October 2026. These are administrative projected dates rather than evidence that the field work remained unfinished. [QE63](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/63), [QE91](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/91), [QE96](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/96)

**Observed.** Status and finish date cannot substitute for each other: 94 non-`CLOSED` records already have an `ActualFinishDate`, including 32 dated from 2025 through 13 October 2026. Across all statuses, 1,750 finish timestamps precede work-order initiation; 565 of those finishes fall in the current comparison window. A further record has invalid year 4152. [QE catalog](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json), [QE98](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/98)

## Candidate linkage to 311

**Observed method.** The QE rows contain no direct request ID. A candidate therefore requires a compatible operation, a work-order initiation from one day before request filing through one day after request closure or cancellation, and either the same N1-normalized address or a coordinate separation of at most 30 EPSG:3857 projected metres. That last threshold is a projected-coordinate sensitivity, not a 30-ground-metre claim. A finish counts only when it is on or after both request filing and work-order initiation and no later than 13 October 2026. [311 source](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip), [QE catalog](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json)

| R1 request cohort | Requests | Candidate work order | Chronology-valid finish | By promise | Later than promise | Median days late |
|---|---:|---:|---:|---:|---:|---:|
| Converted, exact normalized address | 572 | 88 | 74 | 6 | 68 | 268.5 |
| Converted, address or projected-coordinate sensitivity | 572 | 105 | 89 | 6 | 83 | 218 |
| Cancelled, exact normalized address | 35 | 4 | 2 | 0 | 2 | 61 |

**Observed.** The converted cohort contains 420 removal, 12 stump and 140 trim requests. Candidate work orders are found for 7 removal, 2 stump and 96 trim requests, but all 89 chronology-valid finishes are trim; no removal or stump request has one. The cancelled cohort has four exact-address candidates, two with a chronology-valid trim finish and two with a non-closed work order lacking a valid finish. [311 source](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip), [QE63](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/63), [QE96](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/96), [QE98](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/98)

**Observed.** A deliberately easier contextual placebo, allowing any Forestry operation at the same address or projected-coordinate distance during the lifecycle, matches 87 of 29,797 unrelated pothole, refuse and container requests. This is context for incidental co-location, not a causal false-positive rate. [311 source](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip), [QE catalog](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json)

**Inferred.** The timing results describe the recoverable candidate set, not citywide crew performance. QE98's calendar-valid finish window begins on 14 October 2025, so early-2025 requests with prompt finishes may be absent. QE99 covers a different pruning program and does not repair that truncation. The late counts and medians are therefore selected by source availability. [QE98](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/98), [QE99](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/99)

## Recheck of the 2025 removal inference

**Reported.** The prior R1 check used a 1,500-row capped open-order sample and found 3 exact-address and 7 address-or-coordinate matches among 294 requests closed “removal work order created” in 2025. It inferred that most associated orders had closed. [311 source](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip), [QE63](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/63)

**Observed.** The extracted current-open union raises the after-filing lower bound to 8 exact-address and 10 address-or-coordinate candidates. It still finds few current-open candidates, but current-open absence is not closed-work evidence: the available closed-removal records are limited to Forest Park and a 28-row contractor subset, with no general citywide source. **Inferred:** the old sample's directional finding of limited current-open membership remains, while its “mostly closed” completion interpretation is unsupported. [QE63](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/63), [QE89](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/89), [QE108](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/108)

## Blank cancellations and private-tree inspections

**Observed.** Among 5,201 cancelled `Inspect City Tree` requests with blank public resolution, 510 have an earlier non-closed removal-order candidate: 369 match the exact normalized address and another 141 match only the projected-coordinate sensitivity. Of the candidate-linked requests, 431 have an administrative projected finish on or before 13 October 2026. This supports duplicate/already-queued work as one possible cancellation path; it does not establish completion. [311 source](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip), [QE63](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/63)

**Observed.** QE66 contains 878 closed Private Tree Removal inspection records. `ActFinishDate` falls from 2025 through the 13 October cutoff on 321 records; two more are dated 14 October, bringing the through-snapshot count to 323. These dates establish inspection completion, not physical tree removal. [QE66](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/66)

## Reproducibility and limits

The reproducible analysis is [forestry_analysis.py](cityworks-gap-scripts/forestry_analysis.py). Its aggregate outputs are [CSV](cityworks-forestry-workorders-aggregates.csv) and [JSON](cityworks-forestry-workorders-aggregates.json); the figure ledger is [facts CSV](cityworks-forestry-workorders-facts.csv). The script attaches the project DuckDB read-only and writes only aggregates.

**Open.** The candidate links cannot determine whether a specific 311 request caused a work order, whether a finish date represents the requested physical work, or whether an unmatched request was completed through a search that QE does not expose. Exact request-to-work-order attribution requires a direct foreign key or a documented operational crosswalk that these schemas do not provide. [311 source](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip), [QE catalog](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json)
