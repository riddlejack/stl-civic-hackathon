# Cityworks active service-request queues: safe multi-division profile

## Summary

**Observed.** The city-authorized, field-restricted extract returned **19,291 unique rows** from Cityworks `Active SRs` for **61 exact operational problem codes** in the existing service register; 60 code strings occurred. Exact request-id matching linked **18,993 rows (98.5%)** to the city's public 311 file and exposed **22 non-null division labels**. These are routing labels, not 22 verified departments, and they do not support the requested premise that there are exactly 21 departments. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

**Observed.** The extract materially improves queue visibility: `DateSubmitTo` is populated on 99.8% of rows, `DateDispatchTo` on 66.8%, and `DateDispatchOpen` on 41.4%. It does **not** close the completion-record gap. The service-request schema has no actual-start or actual-finish field, only two rows carry `DateTimeClosed`, and 9,165 records that the public 311 file still calls open have `Completed=1`. `Completed` and `DateInvtDone` therefore cannot be treated as proof that field work finished. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

**Inferred.** This is useful evidence for showing which queue a request reached and which operational milestone flags exist. It is not an independent completion ledger. Absence from `Active SRs` also does not mean the work was done: 315 locally open 2025–26 requests in the same safe code set were absent from the saved search. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

## Scope and retrieval checks

**Observed.** The filter was an ordinary quoted SQL `IN` clause built from the exact `problemcodes` in `build/N2/register.csv`, excluding the `lead`, `homeless`, and `nuisance_log` rows. No health, police, person-specific, address, coordinate, staff, free-text, contact, account, or tax field was requested. The helper validated every response against its allowlist before persistence. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18)

**Observed.** All four extracts had equal before/after counts and unique request ids. Retrieval ran on 14 October 2026 UTC. Raw responses and fetch logs are in the ignored `data/raw/cityworks-gap/authorized/` folder. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18) [Emergency Tree](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/68) [Storm Response](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/69) [Open Debris](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/106)

| Layer | Saved-search description | Rows / unique ids | Returned problem codes | Exact 311-id matches | Non-null 311 division labels |
|---|---|---:|---:|---:|---:|
| 18 | Active SRs, safe registered codes only | 19,291 / 19,291 | 60 | 18,993 (98.5%) | 22 |
| 68 | Emergency Tree Service Requests | 514 / 514 | 2 | 511 | 3 |
| 69 | Storm Response SRs | 682 / 682 | 11 | 682 | 5 |
| 106 | Open Debris SRs | 16 / 16 | 2 | 6 | 1 |

Sources: [18](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18), [68](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/68), [69](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/69), [106](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/106), and the [public 311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5). All figures are **observed**.

**Observed data-quality qualifications.** The filter contained 61 registered codes, but `Signal Stuck` had no row. The service returned `Critical Sign` with two trailing spaces even though the register value is unpadded. Of the 298 layer-18 ids absent from the local 311 file, 296 were initiated on 13–14 October, after the local file's last observed initiation date; one was initiated in 2024 and one has a null initiation date. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

## What the division count means

**Observed.** Layer 18 matched 22 non-null `division` labels in the public 311 file, plus 29 matched requests with no division. Fourteen non-null labels account for 18,950 of 18,964 rows with a division (99.9%); the remaining eight labels account for 14 rows. The dominant labels are Forestry (9,001), Street Department 510 (5,365), Building Division (1,418), Water Division (1,151), Traffic Division 511 (454), City Emergency Management (395), Tornado Recovery (380), and LRA (338). [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

**Inferred.** Labels such as `STREET DEPT, 510` and `STREET DIVISION, 514` are operational routing values; small historical values and alternate spellings mean distinct labels should not be relabeled as distinct departments. The full aggregate, including every label and problem code, is in `research/cityworks-active-queues-aggregate.csv`. [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

## Current-cohort agreement and discrepancy

**Observed.** In the local 311 file, 11,299 safe-scope requests filed from 1 January 2025 through the file's 13 October 2026 edge are still classified open. Layer 18 contains 10,984 of them (97.2%); 315 are absent. Conversely, the layer contains one request the local file classifies closed and one it classifies cancelled. Across all 18,993 exact matches, the Cityworks queue status and public-file raw status agree on 18,821 rows (99.1%), with 172 disagreements. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

**Inferred.** The 172 status differences and two final-status contradictions may reflect the one-day source timing difference, saved-search refresh behavior, or status mapping. They are not evidence by themselves that either source is wrong. The 315 locally open requests missing from layer 18 are likewise not evidence of completion. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

## Newly visible workflow dates

| Safe field | Layer 18 populated | Layer 68 populated | Layer 106 populated | Interpretation boundary |
|---|---:|---:|---:|---|
| `DateSubmitTo` | 19,261 / 19,291 (99.8%) | 514 / 514 | 15 / 16 | Submission-routing timestamp; absent from the public 311 table |
| `DateDispatchTo` | 12,883 / 19,291 (66.8%) | 501 / 514 (97.5%) | 1 / 16 | Named workflow timestamp; not documented as first dispatch |
| `DateDispatchOpen` | 7,995 / 19,291 (41.4%) | 251 / 514 (48.8%) | 0 / 16 | Named workflow timestamp; semantics not documented here |
| `DateInvtDone` | 9,193 / 19,291 (47.7%) | 487 / 514 (94.7%) | 0 / 16 | Internal investigation/inventory milestone, not actual work finish |
| `DateTimeClosed` | 2 / 19,291 | 0 / 514 | 0 / 16 | Request closure; expected to be sparse in open queues |
| `DateSubmitToOpen` | 0 / 19,291 | 0 / 514 | 0 / 16 | Exposed but empty |
| Actual work start / finish | 0 fields | 0 fields | 0 fields | Not exposed by these service-request schemas |

Sources: [18](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18), [68](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/68), and [106](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/106). All completeness figures are **observed**.

**Observed.** `DateDispatchOpen` precedes `DateDispatchTo` in 5,306 layer-18 rows and is populated without `DateDispatchTo` in 85 more. This is direct evidence that the field names alone are insufficient to define first dispatch or elapsed routing time. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18)

**Observed.** Layer 18 has `Completed=1` on 9,202 rows (47.7%). Among exact matches that the public file still calls open, 9,165 of 18,991 (48.3%) carry that flag. `DateInvtDone` is populated on 9,193 rows, while only two carry `DateTimeClosed`. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

**Inferred.** `Completed` appears to mark an internal service-request milestone in many still-active records. Without documentation or an actual-finish date, it cannot be converted into “work completed.” [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18)

## Specialized queues

**Observed.** All 514 Emergency Tree rows are also in layer 18. The layer has 487 `Completed=1`/`DateInvtDone` rows, but no request-close or actual-finish date; 511 ids match locally open requests. This strengthens queue-state visibility for Forestry but supplies no independent tree-work completion date. [Emergency Tree](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/68) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

**Observed.** Storm Response contains 682 requests across 11 problem codes, all exactly matched to the public file. The local dates run 16 May–4 June 2025; 585 are now locally closed and 97 open. The published saved-search schema exposed only request id and problem code to the approved projection, so it adds no workflow or completion dates. [Storm Response](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/69) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

**Observed.** All 16 Open Debris rows are also in layer 18. Six match the local file; ten were initiated beyond its observed edge. Fifteen carry `DateSubmitTo`, one carries `DateDispatchTo`, and none carries `DateInvtDone`, `DateTimeClosed`, or an actual-finish field. [Open Debris](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/106) [311 catalog](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

## Use in the hackathon claim

**Inferred.** The defensible statement is: *the authorized Cityworks views expose active-queue membership and several workflow timestamps across 22 observed public-311 division labels, but they do not establish when field work finished.* The adoption ask remains an export of work orders or another completion ledger carrying an actual finish date and the request-to-work link. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18)

**Observed:** one returned projected-completion date uses year 1900, a sentinel rather than a usable service promise; any future routing or promise analysis must exclude it. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18)

**Open.** City documentation establishing the business meaning of `DateDispatchTo`, `DateDispatchOpen`, `DateSubmitTo`, `DateInvtDone`, and `Completed` was not supplied. No latency or first-dispatch claim should use them until those definitions are confirmed. [Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18)
