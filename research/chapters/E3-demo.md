# E3. The three-surface demo on the existing site

Written Wednesday 14 October 2026, 3:40 to 4:00 p.m. Central, by the E3 session. The work ran from 3:14 p.m.; the first real screen (the queue on the public file) rendered at about 3:25 p.m.

## Summary

**Found and built (observed unless marked).** The site now opens on the thesis and has two new pages:

- **The queue** (`site/queue.html`) is the dashboard one Cityworks saved search would feed. It is built on the public 311 file. 14,902 of 16,505 open requests filed since 1 January 2025 are past the city's own promised date; 6,724 are more than 180 days past; the median is 152 days. The page breaks this down by division, shows an age histogram and a block-level map, lists the 100 oldest, and offers a CSV of all 14,573 non-sensitive rows.
- **The city's active queue corroborates this.** Cityworks layer 18 holds 10,094 requests filed since 2025 that are past promise, across the 60 request types it covers. The public file gives 10,298 for the same types a day earlier. Promise dates match on 18,972 of 18,976 requests. "Work order needed" is set on 8 of 19,291.
- **The status page, before and after** (`site/status.html`) rebuilds the City's page at block level in three panels: a referred cave-in (no related items), a tree removal (5 items attached), and the cave-in under the four rules.
- **The landing** leads with CityStat's alley debris measure: 78.6% on time as published, 15.0% counting only closings that say the work was done. The scoreboard carries that added column for all nine CityStat measures.

**Not established.**
- Fresh status pages. The City's robots.txt disallows `check-service-request.cfm` for every user agent, so E3 fetched none and used two copies the orchestrator's probe had already saved.
- Whether the sample cave-in's repair is still open. Its "after" figure (75 days past promise) is **inferred**, and the assumption is stated on the page.
- A final register column. E1's sample was still growing during the build.

**Late finding, from E1's final sample (1,440 pages; observed by E1, shown on the status page; rebuilt 4:00 p.m.).** Attaching is not finishing:
- **Tree removals** (the control) carry a work order on 40 of 40 sampled pages, but only 1 of the 40 finished by the promise (39 late, median 211 days late).
- **Referred cave-ins** carry one on 16 of 40, so Forestry is not the only division that attaches work orders. 4 of those 16 finished by the promise and 12 late (median 9 days late).
- **Tree planting** carries one on 34 of 40; 2 of 34 finished by the promise.
- **The other 18 hand-off closing phrases** sampled show no work order on any of their 40 pages; 15 of them show no attached item at all.

## Admission

**Done:**
1. The queue page.
2. The status page before and after.
3. The landing and navigation re-centred.
4. The fairness section moved to a methods appendix, unchanged.
5. The dumping section retitled.
6. A register column for attached work orders, read from E1.
7. The brief removed from the nav and linked from methods.
8. The July pothole callout removed.
9. 241 `e3_*` figures, each with a derivation.
10. 20 decisions.
11. The privacy scan: 0 findings.
12. Every page checked in a browser: no MOCK banner or tag, and every "How we know" link resolves (34 on the landing, 11 on the queue, 24 on the status page, 8 on methods, 6 on the brief).
13. Captures in `build/E3/shots/`.

**Not done, or done differently from the brief:**
- **Pages not fetched (deliberate).** The brief asked me to fetch the two status pages "allowed by robots.txt". They are not allowed. I read `https://www.stlouis-mo.gov/robots.txt` once at 3:27 p.m. and saved a copy to `data/raw/stlouis-mo.gov/E3/robots-2026-10-14.txt`. Under `User-agent: *` it has the comment "Do not crawl service request, board bills, etc." followed by `Disallow: check-service-request.cfm`. There is no leading slash, so parsers report the page as allowed, but the owner's intent is plain. E1 reached the same reading at 3:24 p.m. I used the orchestrator's saved copies (`data/raw/stlouis-mo.gov/csb-status/`, file time 3:16 p.m.). The `a disallowed path ` endpoint was never called.
- **Existing typed numbers not removed.** Some older numbers in the receipt, fairness and brief sections are still typed into JavaScript or come straight from section data files. I did not refactor them; the rule binds new content. The scoreboard credibility line, which I rewrote, now takes its numbers from the registry.

**Could not establish:** whether the work behind any queued request is done. The queue ranks by the city's date; it does not claim the work is undone.

**Assumed:**
- The run date is 13 October 2026, 23:59 Central, as the brief set it.
- The public file's SUBMITTO carries the same routing as Cityworks' `SubmitToName` (**inferred**). The field was not extracted because it can name staff.

## What each page shows

### 1. The queue (`site/queue.html`, data `site/data/queue.json`, CSV `site/data/downloads/queue.csv`)

**Header.** The header carries the page label "Prototype of the dashboard the city would build from one saved search. Independent, not a City page." Directly under the title: "“Past promise” is the city’s own date ... The list includes work that is legitimately queued: it is a ranking, not an accusation."

**Tiles.** Four stat tiles:
- `e3_queue_past_promise` 14,902
- `e3_queue_past_180` 6,724
- `e3_queue_median_days_past` 152 days
- `e3_queue_blocks` 6,211

Their sub-lines use `e3_queue_open_since_2025` 16,505, `e3_queue_past_promise_share` 90%, `e3_queue_past_365` 4,052 and `e3_queue_sensitive_excluded` 329.

**Corroboration.** One line under the tiles:
- `e3_queue_qe_past_promise_2025` 10,094 past promise in Cityworks
- `e3_queue_qe_codes` 60 request types
- `e3_queue_public_same_types` 10,298 in the public file for the same types
- `e3_queue_qe_promise_match` 18,972 of `e3_queue_qe_promise_both` 18,976 promise dates agree
- `e3_queue_qe_woneeded` 8 of `e3_queue_qe_active` 19,291 flagged "work order needed"

All of these are observed, from [QE layer 18](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18) and the [public file](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip).

**Division table.** The 12 largest SUBMITTO labels plus a row for the rest, as published, with figures `e3_queue_div_<label>_{past,past180,median_days,open}`. Examples: Forestry 4,679; Street Dept 510 4,185; Building Div 1,219; LRA 755; Water Div 654; Traffic Division 511 496. Clicking a row filters the map and the list (`?div=` in the URL).

**Age histogram.** `e3_queue_age_*`: 2,206 at 0–30 days; 2,906 at 31–90; 3,066 at 91–180; 2,672 at 181–365; 4,052 at more than a year.

**Map.** Plain SVG with ward outlines from the `wards` table and 6,207 block dots:
- **Position:** each dot sits at the mean SRX/SRY of every request ever filed on that block, snapped to a 60 m grid, so a single queued request is not drawn on its house.
- **Size and colour:** sized by count; coloured by the oldest request on the block, on a one-hue ramp that passed the dataviz validator (ordinal, light).
- **Labels:** on hover only.
- **Exclusions:** sensitive types are not mapped.
- **Caption:** says the map makes no ward comparison.

**List.** The 100 oldest (or the 100 oldest for the chosen division), at block level: days past, type, block, ward, routed to, filed, promised.

**The saved search behind it.**
- Layer 18 "Active SRs".
- Expression `PrjCompleteDate < CURRENT_DATE AND DateTimeInit >= DATE '2025-01-01'`.
- Grouped by `SubmitToName` and ordered by `PrjCompleteDate`, with the field names.
- The equivalent DuckDB SQL on the public file.
- A sentence on how the Cityworks rows were obtained: authorised at office hours, operational fields only, raw rows not published.

### 2. The status page, before and after (`site/status.html`, data `site/data/statuspage.json`)

The page is labelled "Reconstruction of the City's public status page, block level; sample request". It uses the City's field names and wording, cuts the address to the block and withholds the request number. It carries no City branding.

| Panel | What it shows | Status |
|---|---|---|
| Today: a cave-in, referred | 5200 block of Robert Av, Ward 2. Submitted, closed and investigated on 07/27/2026. "Referred to street maintenance for repair work to be scheduled." Dept Response Due By 07/30/2026. No Related Items section (`e3_status_cavein_related_items` 0). | **real** (saved copy) |
| Today: a tree removal, same page | 3600 block of Gasconade St, Ward 3. "Removal work order created." Comment "Tree(s) scheduled for a thirty (30) day removal". Related Items, "Inspections and work orders attached to this request." (`e3_status_tree_related_items` 5). | **real** (saved copy; count only) |
| Proposed: the cave-in under the four rules | Status "With Street Maintenance" since 07/27/2026, promised 07/30/2026. Days past the promise `e3_status_cavein_days_past_promise` 75 (**inferred**). "Done by the promised date: Not yet: work order open". Related items: inspection completed, street-repair work order open. | **reconstructed / illustrative** |

The footer table reads E1's final stratified sample (`build/E1/service_table.csv`, 4:00 p.m. build) through `e3_status_e1_<stratum>_*` figures. It shows the tree-removal control and E1's 20 hand-off strata, 40 pages each (observed by E1). E1's "done" and "open past promise" strata are counted in the register but not shown in this footer:
- **Tree removals:** 40 of 40 carry a work order, but only 1 of those 40 finished by the promise (39 late; E1's median is 211 days late).
- **Tree planting:** 34 of 40 carry a work order; 2 of 34 finished by the promise.
- **Referred cave-ins:** 16 of 40 carry a work order; 4 of 16 finished by the promise.
- **The other 18 hand-off phrases:** 0 work orders on 40 pages each; 15 of them have no attached item at all.

E1's script records that Jack authorised its reads of the related-items endpoint at office hours (**reported**, `scripts/exec/E1/06_items.py`). E3 received no such ruling and called neither address. The footer replaced the earlier 12-page probe line once E1's sample landed. It also lists the four rules.

### 3. Landing, navigation, scoreboard, methods

- **Navigation (all pages):** For residents · The queue · For the CityStat team.
- **Landing (`index.html`).**
  - Headline: "The city grades the hand-off, not the job."
  - Lead pair `e3_citystat_debris_published_vs_done`: 78.6% as published (**reported**, CityStat Q2 2026) against 15.0% counting only closings that say done (**observed**, from R1's restatement; rebuilt on-time 78.3%; 67% of on-time closings are hand-offs).
  - Supports: `n2_share_closed_handoff` 35% (existing) and `e3_queue_past_promise` 14,902, linking to the queue.
  - The receipt search box and the lot-1 hero card are unchanged.
  - Doors: For residents (receipt, and the status page before/after), The queue, For the CityStat team.
- **Scoreboard (surface 3): "CityStat, with one added column: done on time".**
  - The nine measures with columns: published Q2, rebuilt Q2, **done on time Q2** (`e3_citystat_<metric>_q2_done_on_time`), and Q3 (ours, unpublished; Q3 appears here only).
  - The credibility line now reads its numbers from `n4_repro_counts_exact_C`.
  - The quarterly chart stops at the last published quarter.
  - The per-service "missing column" table is unchanged.
- **Dumping:** retitled "Problem set 3: where dumping keeps coming back, and what the city did each time", with content unchanged.
- **Methods.**
  - Table of contents, and a link to "The printable Monday brief".
  - Three new definitions: done on time, past promise, work order attached.
  - Register column "Work orders attached (public status page)", read from `build/E1/linkage_by_service.csv` at build time. Services without a sample read "not yet tested".
  - At the end, the appendix "A separate finding: first-step waits by ward", which is the fairness section unchanged (`site/js/fairness.js`).
- **Brief (`brief.html`):** out of the nav; the July pothole callout is removed.

## Real versus reconstructed

| Element | Status |
|---|---|
| Every queue count, division row, histogram bar and list row | **real**, from the public 311 file (observed) |
| Cityworks corroboration | **real**, from the authorised extract (observed) |
| The queue page's layout as an "ArcGIS dashboard" | a **prototype**, labelled as such; no geoportal page exists |
| Status panels 1 and 2 | **real** saved pages, re-drawn at block level |
| Status panel 3 | **proposed**: the field values come from the real request, and the status, attached work order and day count illustrate the rule |
| CityStat published shares | **reported** |
| Rebuilt shares and the done column | **observed** |

## Files

**Code:**
- `scripts/exec/E3/`:
  - `build_queue.py`: the queue and its figures.
  - `build_statuspage.py`: the status page; no fetch.
  - `build_citystat.py`: the done column.
  - `finish.py`: decisions and the facts table.
  - `shots.sh`: the captures.
- `scripts/night/N6/bridge.py`, with these changes:
  - E3 figures are merged in.
  - `build_queue` and `build_statuspage` were added.
  - The register gains the `attached` column.
  - E3 decisions are appended.
  - `queue.csv` is listed in downloads, and sizes are stored in KB.

**Site:**
- New: `site/queue.html`, `site/status.html`, `site/js/{queue,status,fairness}.js`.
- Edited: `site/js/{common,residents,methods,brief}.js`, `site/css/site.css`, `site/config.json`, `site/index.html` (title).
- Pre-E3 copies of the edited files are in `build/E3/*.before-E3.*`.

**Outputs:**
- `build/E3/figures.json` (241), `decisions.json` (20), `queue.json`, `queue_rows.json`, `statuspage.json`, `citystat_done.json`, `privacy-scan.json`.
- `build/E3/E3-demo-facts.csv`: one row per figure. It sits in `build/E3/` because this thread may write only this one file under `research/`.
- Request ids for the two sample pages: `build/E3/private/` only.

**Captures:** `build/E3/shots/` at 1920 wide, made by `scripts/exec/E3/shots.sh` (headless Chrome), retaken 4:01–4:03 p.m. after the final rebuild.
- `01` queue at 1080; `01b` queue filtered to Street Dept 510; `01c` queue full page.
- `02` and `02b` status page (`02b` at 2300 px tall, to include the full E1 footer table).
- `03` landing; `03b` receipt.
- `04` and `04b` scoreboard; `05` dumping.
- `06`, `06b`, `06c` (register) and `06d` (appendix) methods.
- `07` brief.

The residents page is captured section by section (`?only=`), because each section is at least one screen tall.

## For the orchestrator to decide

1. **Which overdue number the video says.** The site says **14,902**: the public file, all request types, filed since 2025. The assessment's strongest claim says "about 10,000": the Cityworks count, which is 10,094 for 60 types. Both are observed. They count different scopes, so pick one per sentence.
2. **The live status page in the recording.** Should Jack open it by hand in a browser during the recording? That is not a crawl, but it shows the address and the request number, so it would need cropping. Or use `status.html` only. Jack's call (E1 asked the same).
3. **Non-crew routings in the queue.** The queue includes routing labels that are not field crews, such as "Tornado, Recovery" (379), TREAS PRKG SVC (206) and CITY EMRGCY MNG (230). Should they stay, or be filtered to operating divisions? Today they stay, as published.
4. **Register column: final (rebuilt at 4:00 p.m. on E1's final table).** It counts **work orders** (E1's `service_table.csv`), not any attached item, pooled across every E1 stratum for the service, including E1's "done" and "open past promise" strata:
- **yes (2):** weeds on occupied property (24 of 30 open past promise), tree planting (34 of 40).
- **partly (3):** city trees (67 of 100: removals 40 of 40, open past promise 27 of 30, tree down 0 of 30), cave-ins (16 of 70), sidewalks (6 of 30).
- **no (12):** both weed services on vacant property, potholes, street lights, signals and signs, towing, refuse, street debris, water, board-up, tornado debris, code enforcement.
- **not yet tested (8).**

The pooling is why city trees reads "partly". Hover text gives each stratum's count.
5. **"No published list ranks them"** on the landing is **inferred**: we found none among the city's published pages and saved searches. Keep it or soften it.
6. **Parks in the done column** uses R1's closed-only grading, so its rebuilt and done columns have different denominators. This is footnoted on the page.
7. **"One division turned it on" needs revising.** E1's sample shows Street Department attaches a work order to 16 of 40 referred cave-ins (40%), not only Forestry. It also shows that attaching is not finishing: 1 of 40 attached tree removals finished by the promise. The page now says "where a division attaches its work order, residents can see the job". The script line should match; the done-by-promise column is what moves the argument.
8. **Rebuild order (done at 4:00 p.m. on E1's final table):** `scripts/exec/E3/build_statuspage.py`, then `finish.py`, then the bridge. The privacy scan has 0 findings; no page shows a MOCK banner or tag; every "How we know" link resolves.

## How to run

```
.venv/bin/python -I scripts/exec/E3/build_queue.py
.venv/bin/python -I scripts/exec/E3/build_statuspage.py
.venv/bin/python -I scripts/exec/E3/build_citystat.py
.venv/bin/python -I scripts/exec/E3/finish.py
.venv/bin/python -I scripts/night/N6/serve.py        # runs the bridge, serves http://127.0.0.1:8806/
scripts/exec/E3/shots.sh                              # captures into build/E3/shots/
.venv/bin/python -I scripts/night/N6/privacy_scan.py --out build/E3/privacy-scan.json
```
