# E6. The site rebuilt as five quiet product screens

Written Wednesday 14 October 2026, 6:58 to 7:10 p.m. Central, by the E6 session (work ran from 6:29 p.m.). Clock checked with `date`. Revised the same evening at the orchestrating thread's request: the CityStat column is relabelled "Closing says done" (see the CityStat row below and `research/closure-class-review.md`).

## Summary

**What changed (observed: built, served on `http://127.0.0.1:8806/`, checked in a browser at 1920×1080 and 390 px).** The site is now five screens with one job each, and every number on them is a registered figure:

1. `/` (landing): the name placeholder **[NAME]**, the tag "Which promises did St. Louis keep?", one sentence and three doors (List: Forestry's list · Count: CityStat, with one column ("closings that say done") · Link: A resident's page). Under them sit "Get the data" and "Read the full case". There are no statistics on it.
2. `/queue.html`: opens on Forestry. Six divisions are buttons; six more and "All divisions" sit under "Other". The page has one headline ("Forestry: 4,679 requests past the date the city gave"), one definition line, the block map and the list, oldest first. Clicking a block on the map filters the list to that block. Everything explanatory is behind "How this list is built", and the CSV download is per division.
3. `/status.html`: the lookup box, then one request with a toggle between **Today** and **With the work order attached**. The North Taylor lot comes first. Today reads "Closed · “on schedule to be cut”". With the work order it reads "With Forestry since 2 July · Due 30 September · Not yet done". Chips switch to the tree and the cave-in.
4. `/citystat.html`: one chart (alley and street debris, 78.6% as published against 15.0% where the closing says it was cleaned within 3 days) and the nine measures in three columns (published, rebuilt, and "Closing says done", within CityStat's goal). The subtitle says that with work orders linked the column becomes done by the promise. The SQL is a download.
5. `/data.html`: seven downloads, the 15 public sources (URL, retrieval time, rows, size, how used) and the 105 withheld files in a collapsed list. Then the authorisation statement, word for word from `context/AUTHORISATION-NOTE.md` with its bracketed fields left as they are, and the fetch script.

The old narrative pages are gone: the landing narrative (`residents.js`), the methods page, the fairness appendix, and the dumping and receipt sections. The Monday brief (`brief.html`) is out of the nav but kept, because `deliverable/README.md` links to it. The word DoneStat no longer appears on any page.

**Privacy (observed).** The N6 privacy scan (`build/E6/privacy-scan.json`) reports **0 findings** over site/, deliverable/ and build/out/ (94 files). The public-export check (`export_public.sh` into a scratch folder, then `scan_public.py`) reports **0 hits in 351 files**, with the eight new screenshots OCR-scanned. All screens show block level only, with no request, work-order or parcel numbers.

**What could not be done, or was done differently.**
- The "Read the full case" link points to `../README.md`. That is right inside the repository but gives a 404 on the local server, which serves only `site/`. Set `links.case` in `site/config.json` to the GitHub URL once the repository exists.
- The status lookup works only under `scripts/night/N6/serve.py`. A static copy says so and points to the examples.
- The two video crops (07, 08) use a card mode of the page (`?card=map`, `?card=chart`) that draws the element alone, not a pixel crop of the full screenshot.
- "For most, no record says whether the work was done" (84%) appears only under **All divisions**. It is a city-wide figure, and Forestry's share is lower: 60% of its tree inspections have a pending work order (`build/E5/ledger_by_type.csv`).

## The screens and the choices behind them

| Choice | Why | Label |
|---|---|---|
| The six divisions in the picker are Forestry, Streets (STREET DEPT, 510), Building Division, Land bank (LRA), Water Division and Traffic (511) | The six largest routing labels that are operating crews. The non-crew labels E3 named (Tornado recovery, Emergency management, Treasurer parking) go under "Other" with Vector Control, Lead inspection and Building trades. The 16 pooled labels are reachable only through "All divisions", because they have no map dots or figures of their own. | inferred (my reading of "operating divisions") |
| Headline count from the registry, list rows from `queue.csv` | The headline is `e3_queue_div_<label>_past` (Forestry 4,679). The list has 4,676 Forestry rows because three of a sensitive type stay off the list, as before. The page shows no count it cannot cite. | observed |
| The list columns are Days past · Type · what the request says · Block · Due by · City status | The type (PROBLEMCODE) and the description often repeat ("Inspect City Tree" and "Inspect city tree"), so the description shows only where it adds words. City statuses are spelled out (Disptch becomes Dispatched). | observed |
| Map colour is one hue of late gold, in three steps (up to 90 days, 91 to 365, more than a year) | One accent per meaning, in the video's palette. Age is ordinal, so it gets one hue going from light to dark. The validator confirms the video hues fall below 3:1 contrast on white, so values sit in ink beside the marks and never in the mark colour. | observed (validator run) |
| Colours on the resident's page: Today is red ("closed at the hand-off"); After is blue for the division and gold for "Not yet done" | These follow the video's colours for closed-at-hand-off, promise and late. | n/a |
| Every "After" view is tagged "Illustration" | For the lot, the request's own dates and "no cut on record" (`n5_lot1_cuts_billed_2026` = 0) are observed; the attached order is illustrative. For the tree, the removal order is real and was still open on 13 October 2026; only the attachment is illustrative. For the cave-in, nothing is attached, so whether the repair was done is unknown, and the page says so. | observed / illustrative |
| The CityStat page has one chart, for the lead measure, and a table for all nine | The two bars (78.6% against 15.0%) read in five seconds. Rebuilt (78.3%) sits in the caption and the table. | observed |
| The added column is labelled "Closing says done" ("within CityStat's goal"), not "done by the promise" | Its values count a request as on time when it closed within CityStat's goal and its closing words say the work was done. They are not graded against each request's promise date and are not a record of work done; the closure-class review clears them only as closings that say done. Same numbers and figure ids (`e3_citystat_<m>_q2_done_on_time`). | observed (relabelled at the orchestrator's request) |
| `site/data/downloads/sources.csv` is the formatted manifest, not E4's raw `MANIFEST.csv` | The raw file's sha256 hashes and byte counts contain digit runs that equal real request numbers. The N6 scan flagged 37 of them plus one parcel-like run, which were false positives, and the gate has no allowlist. The full manifest with hashes ships in the export as `data/MANIFEST.csv`. | observed |
| The queue draws its headline and map before the list | The CSV is 1.9 MB, and the screen was blank until it loaded. | observed |

## Figures on the screens

Every figure is a registered id: 63 rows in `build/E6/E6-site-facts.csv`, none missing. They break down as:
- **Queue:** the 12 per-division headlines; `e3_queue_past_promise` 14,902; the reality-check split copied from `build/E5/summary.json` as `e5_queue_*` (done 2.6%, pending 8.1%, superseded 2.2%, leftover 2.7%, no record 84.3%); the five age bins; and the Cityworks corroboration (10,094; 60 types; 10,298; 18,972 of 18,976).
- **Privacy note:** `e3_queue_sensitive_excluded` 329.
- **CityStat:** 27 table cells and the rebuilt debris share, 78.3%.
- **Status:** the lot's minutes to close (13 and 7), its promise date and its cuts in 2026 (0), plus the tree page's 5 attached items.

The facts file sits in `build/E6/` because this thread may write only its own chapter under `research/`.

## Checks run

| Check | Result | Label |
|---|---|---|
| `privacy_scan.py --out build/E6/privacy-scan.json` | **0 findings**. 48 prose hits for review, all in files E6 did not write (`site/data/figures.json`, `decisions.json`, `negative.json`, `build/out/*`, `deliverable/*`). | observed |
| `export_public.sh <scratch> --no-commit`, then `scan_public.py <scratch> --repo .` | **0 hits in 351 files** (rerun after this chapter was written), with 6 reviewed accepts. The 86 placeholder and 44 address-shaped warnings are unchanged from the baseline run before E6's edits (328 files, 0 hits). No image warning was raised, so the screenshots were OCR-scanned (tesseract is installed). | observed |
| Browser at 1920×1080 | All five screens render with no console errors (the only error logged was the deliberate 400 from testing a too-short lookup number). Checked by hand: the division menu, "All divisions", a block filter (28 rows on the block, matching the dot's count), the Today/After toggle on all three examples, a live lookup through `serve.py` (block-level result) and the Monday brief with the new nav. | observed |
| Browser at 390 px | No page scrolls sideways (scroll width equals viewport width on all five). The CityStat table hides the Rebuilt column on phones so the Done column is not clipped. The Today/After toggle stays on one line. The queue list becomes one card per request. | observed |

## Files

- **New:** `site/{citystat,data}.html`, `site/css/app.css`, `site/js/{app,landing,citystat,data}.js`, `site/data/e6.json`, `site/data/downloads/{sources.csv,fetch_public.sh}`, `scripts/exec/E6/{build_e6.py,facts.py,shots.sh}`, `build/E6/{figures.json,E6-site-facts.csv,privacy-scan.json,shots/}`.
- **Rewritten:** `site/index.html`, `site/queue.html`, `site/status.html`, `site/js/queue.js` and `site/js/status.js`.
- **Edited:**
  - `site/js/common.js`: new nav doors, and a figure-as-text option for "How we know".
  - `site/config.json`: `product_name` is "[NAME]", plus the tagline and `links.case`.
  - `site/brief.html` (title) and the `site/css/site.css` comment.
  - `scripts/exec/E4/ALLOWLIST.md`: adds `build/E6/shots/**` and `build/E6/E6-site-facts.csv`.
- **Deleted:** `site/methods.html` and `site/js/{methods,residents,fairness}.js`. The deletions are not staged. Copies of every edited or deleted file are in `build/E6/before/`.
- **Shots:** `build/E6/shots/` at 1920×1080, device scale 2. `01-landing`, `02-queue-forestry`, `03-citystat`, `04-status-today`, `05-status-after` and `06-data` are 3840×2160. The crops are `07-queue-map` (1800×2160) and `08-citystat-chart` (2800×1520).

## For the orchestrator

1. **"DoneStat" survives outside the screens**, in files this thread does not own:
   - `scripts/night/N1/measures.sql` line 1. The bridge copies it to `site/data/downloads/measures.sql`, so it reaches the CityStat page's "Download the SQL".
   - `scripts/exec/E4/export_public.sh`: the public repository's commit message.
   - `scripts/exec/E4/public-data/fetch_public.sh`: the user agent. E6's copy in `site/data/downloads/` replaces it with [NAME].
   - `scripts/night/N6/serve.py`: a docstring.
   - `site/data/decisions.json`, which the bridge writes and no page reads any more.

   Replace them all at once when Jack picks the name.
2. **Set `links.case`** in `site/config.json` to the repository URL.
3. **The 14,902 wording is applied as the reality check advises.** The page says "past the date the city gave" and never "residents waiting". The 84% appears only for all divisions.

## How to run

```
.venv/bin/python -I scripts/exec/E6/build_e6.py --manifest <EXPORT_DIR>/data/MANIFEST.csv   # e6.json, sources.csv, fetch copy
.venv/bin/python -I scripts/exec/E6/facts.py                                               # build/E6/E6-site-facts.csv
.venv/bin/python -I scripts/night/N6/serve.py --no-bridge                                  # http://127.0.0.1:8806/
scripts/exec/E6/shots.sh                                                                   # build/E6/shots/
.venv/bin/python -I scripts/night/N6/privacy_scan.py --out build/E6/privacy-scan.json
bash scripts/exec/E4/export_public.sh <scratch> --no-commit                                 # runs scan_public.py
```

The bridge never writes or deletes `site/data/e6.json` or the two new downloads, so a bridge re-run keeps them.

## E7 addendum: the Ranked view and the screen-recorded demo

Written Wednesday 14 October 2026, 10:20 p.m. Central (work from 9:57 p.m.), at the orchestrating thread's request, on Jack's approval. Design: `research/prioritisation-option.md`, built as specified except where noted.

**Summary.**
- **What was built (observed).** `scripts/exec/E7/rank.py` writes `site/data/ranked.json` (13,464 block-level rows, with no ids and no addresses) and an editable `site/data/rank-weights.json`. The queue page now has three views: Oldest first, **Ranked** (the default) and Close-out.
  - Each ranked row carries a "why this rank" line, for example "Life-safety +60 · 582 days past the date +30 · reported 4 times +10 · work order open · 3 more on this block".
  - "How the ranking works" opens a short panel with the weights and the requested note.
  - The page recomputes every score from `rank-weights.json`, so editing that file re-weights the list.
- **The figures (observed, each recomputed here and matching the report).**
  - Hazard tiers among the 14,902: 2,991 tier 1, 7,423 tier 2, 4,488 tier 3.
  - 1,130 requests go to Close-out (388 done after filing, 333 possibly superseded, 409 administrative), leaving 13,772 ranked; 13,464 are listed once sensitive types are left out.
  - Forestry's top 25: **9** life-safety items oldest-first against **25** ranked, with **0** in common.
  - Street Department's top 25: 1 against 25, with 0 in common.
  - The citywide top 500 are all tier 1, 2,778 tier-1 rows are ranked, and 77 rows are flagged for a bulk-entry check.
  - These are registered as `e7_*` in `build/E7/figures.json` (12 figures with derivations) and listed in `build/E6/E6-site-facts.csv`, which now has 75 rows.
- **The demo (observed).** `video/renders/demo_raw.mp4` is the cursor with no zoom; `video/renders/demo_zoom.mp4` adds the cursor-follow zoom (1.6x). Both are 44.4 s at 1080p30. The cursor and click log is `video/renders/demo_events.json`.
  - The flow is: Forestry Oldest first, then Ranked, hover the top row's "why", click that row's block on the map, the resident's page from Today to With the work order attached, then CityStat's "Closing says done" column.
  - There are no blank frames. There is no judder: the only large frame-to-frame changes are smooth camera ramps and the two page changes.
- **Scans.** The privacy scan reports 0 findings and the export check 0 hits (figures in the table below).

**Deviations from the design, and why.**
1. **Block neighbours** ("N more on this block") are counted over the listed ranked rows only, not over all overdue rows. Counting sensitive requests would reveal them on a block.
2. **Same-address repeats are not merged** into one row, so the top of Forestry's list shows the same block two to four times, each row saying "reported 4 times". The report suggested merging only "in a real build", and merging by block would join different addresses.
3. **Close-out is a third view of counts**, by evidence group and request type, with a one-line reason each. It lists no rows, because the evidence comes from address joins.
4. **The weights file is not editable in the page.** The report's "Weights drawer" with in-session edits was not built. The panel shows the weights, and a division edits `rank-weights.json`.
5. **Oldest first still lists every request**, Close-out included, as before. Measured that way, Forestry is still 9 against 25. For the Street Department it is 3 against 25, because three of its 25 oldest are close-out records.
6. **Block labels in `ranked.json` use the bridge's formatting**, copied into `rank.py`. Four interstate intersections read correctly here, but the bridge's scrub had mangled them in `queue.csv` (for example "Interstate 0 block of …"). Clicking one of those blocks on the map can therefore return an empty list in Oldest first.

**Weaknesses.**
- The repeated top rows (point 2).
- The demo's zoomed frames crop the left edge of the headline while the camera follows the cursor.
- The header still shows "[NAME]".
- The ranking cannot tell undone work from work done but never closed (the report's "call these first" caveat). The page says nothing beyond the score.

**Checks.**

| Check | Result |
|---|---|
| `privacy_scan.py` | 0 findings (99 files). The one new prose hit for review is in `deliverable/video-script-v5.md`, which another session wrote. |
| `export_public.sh` + `scan_public.py` | 0 hits in 368 files (final run, after this addendum). The ranking files are included. |
| Browser parity | The page's Forestry top 5 (scores and days) equal `rank.py`'s `check_top5`. |
| Demo frames | 1,331 frames scanned in each render. Two blank navigation frames were dropped from the frame list by `scripts/exec/E7/drop_blank_frames.py`. |

**Shots.** `build/E6/shots/` was re-shot. `02-queue-forestry` is now Oldest first, `09-queue-ranked` is new, and `10-ranked-why.png` (2590×786) is a tight crop of the ranked header and its first four rows.

**How to run.** Run `rank.py`, then `scripts/exec/E6/facts.py`. For the demo, start `serve.py --no-bridge` on a free port, run `scripts/exec/E7/demo_flow.py` (Playwright from `~/lsat-coach/.venv`), then `drop_blank_frames.py`, then `video/tools/zoom_follow.py` twice. Its full usage is in the script's docstring.

## Later change (14 Oct, 11:30 p.m. Central): the North Taylor "after" state

At the orchestrating thread's request, following `research/north-taylor-mechanism.md`, the lot's after-state was rewritten. The lot had dropped off the cutting rounds, so at the hand-off there was no crew job to link.

- **What changed:**
  - The after-state no longer shows an open mowing work order. It now reads: "Open · no crew job linked · Due 30 September"; "Flagged to Forestry: No cut scheduled for this lot"; "On Forestry's past-due list since 1 October" (the day after the promise date `n5_lot1_promise_date`); "Reported again: 28 July 2026: added to this open request"; "Closes: When a cut is recorded".
  - The Today state is unchanged.
  - The toggle now reads **"After the fix"**, not "With the work order attached", because the lot has no work order to attach. The subtitle and "About this page" now cover both outcomes.
  - The tree and cave-in after-states are as before.
- **Checks:** the privacy scan reports 0 findings, and the export check 0 hits in 369 files.
- **Redone:** shots 04 and 05 were re-shot; nothing else changed. The demo was re-recorded with the same flow, the toggle click now labelled "After the fix": `video/renders/demo_raw.mp4` and `demo_zoom.mp4` (44.8 s each), cursor log `video/renders/demo_events.json`.
- **The raw render:** `zoom_follow.py --zoom 1.0 --inset 1.0` failed on a floating-point edge case ("box offset can't be negative"). The raw version therefore comes from `scripts/exec/E7/render_raw.py`, which uses the same cursor sprite and ripple. The video tool was not edited.

## E8 addendum (15 Oct, 12:05 to 12:35 a.m. Central): live city pages and demo take 6

- **City pages (observed; Playwright, headless Chrome at 1920×1080, DPR 2).** Script: `scripts/exec/E8/record_city.py`.
  - **Streets.** `video/renders/city_citystat_raw.mp4` (15.9 s, `city_citystat_events.json`) records the CityStat Streets page ([streets.cfm](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/streets.cfm), HTTP 200 at 00:08 Central). The clip holds on the top of the page, scrolls smoothly to the Q2 2026 debris paragraph and the embedded Tableau dashboard, then hovers the 2026 Q2 alley/street bar.
    - **What the city shows is "79%", not 78.6%.** The paragraph reads "increased to 79% from 76%", and the bar's tooltip reads "Percentage Meeting Goal: 79%". 78.6% comes from the dashboard's underlying summary data (`data/raw/citystat/tableau-extract.md`).
  - **Towing.** `video/renders/city_towing_raw.mp4` (12.0 s, `city_towing_events.json`) holds on the paragraph with "“Closed” does not necessarily indicate that a vehicle has been towed" and the planned process change ([towing.cfm](https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/towing.cfm), HTTP 200).
  - **Page loads.** Both paths are allowed by the city's robots.txt. Streets was loaded four times: once timed out waiting for idle network, once to test, and twice to take. Towing was loaded twice. No other site page was requested, and no 311 status page was opened.
  - **Scroll.** The first takes' wheel scroll stuttered, because uneven screencast frames repeated every third output frame. The final takes scroll inside the page on every animation frame: 1 repeated frame in 123, and 0 in 92.
- **Demo take 6.** `video/renders/demo6_raw.mp4` and `demo6_zoom.mp4` are 46.5 s each; the event log is `demo6_events.json`. Script: `scripts/exec/E7/demo_flow.py --with-data --pace 0.7`, with holds never under 2 s.
  - The flow is the take-5 flow with the corrected North Taylor state (toggle "After the fix"), ending on the Data page: the downloads, then a scroll to the sources list.
  - There are no blank frames. The only abrupt change is the page switch to Data.
  - Block level only, checked on the stills.
