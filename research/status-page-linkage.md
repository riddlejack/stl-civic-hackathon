# Status-page linkage (E1): which services attach anything to the request?

*1,440 status pages and 223 related-items lists read on 14 Oct 2026, 3:15–3:55 p.m. Central
(see Method).*

## Admission

- **Done.**
  - Read all 1,440 sampled pages: 1,440 HTTP 200, 0 failures, and every page carried the counter.
  - Read the related-items list for every sampled page with a count above zero: 220 sampled
    requests, plus the 3 probe pages, all HTTP 200.
  - Graded the 220 linked requests against their promise dates.
  - Ran the page-versus-file agreement checks, the table by service and the figure registry.
- **Not done.**
  - Bootstrap intervals: Wilson intervals only.
  - A weighted re-estimate of the hand-off share by year. The sample spans 2025 to August 2026,
    and the linkage practice may have changed within it.
- **Could not establish.**
  - Whether a page's "Completed On or Before" date is the actual finish or the close date.
    Only 2 attached work orders had both that date and a Cityworks `ActualFinishDate`, and they
    agreed on 1. The Cityworks extracts are mostly open-queue and removal or trim
    searches; 62 of 369 attached work orders join to them.
  - Why the public page hides the closing words for four high-volume hand-offs.
  - Whether linkage differs by ward for cave-ins: 16 linked of 40 is too small for that.
- **Assumed.**
  - The hidden counter equals the number of items the panel lists. It matched for every request
    whose items were read (counter = items on all 223 calls).

## Summary

**The answer (observed, 1,440 pages):** St. Louis attaches work to the request in Forestry, partly
in the Street Department's cave-in referrals, and nowhere else in the 20 largest hand-offs.
- **Tree removal:** 40 of 40 requests closed "removal work order created" list their work
  orders on the public status page.
- **Tree planting:** 34 of 40 list a planting work order.
- **Cave-ins "referred to street maintenance":** 16 of 40 list a "Right of Way Repair" work
  order.
- **Weeds:** vacant-building weeds "added to rotation" list an inspection in 40 of 40, but no
  cut work order.
- **Everything else:** 15 of the 20 largest hand-off types show nothing attached on any of their
  600 sampled pages (0 of 40 each; 95% upper bound 9% per type). That covers towing "tagged",
  refuse and bulk "next scheduled day", code notices, board-up referrals, debris
  "investigated" and water "scheduled for repair".

Pooled over the 20 hand-off types:
- any attached item: 12.5% (100 of 800; 95% 10.4–15.0%; 10.5% weighted by volume);
- a work order: 6.3% (50 of 800).

[Status page](https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/check-service-request.cfm)

**Where the link exists, the promise is rarely kept.** Each linked request was graded by the first
work-order finish after filing:
- **Tree removals:** 1 of 40 finished within the request's 14-day promise; median 211 days
  after it.
- **Cave-ins:** 4 of 16 within the 3-day promise; the late 12 a median 9 days after it.
- **Plantings:** 2 of 34 within the promise; 24 late (median 121 days); 8 no finish.

**Inferred:** the promise belongs to the request. Nothing carries it to the job, which is the
entry's third rule.

**Done closures attach nothing:** 0 of 300 across the 10 largest "done" types (95% 0–1.3%).
**Inferred:** for potholes, lights and signs the crew closes the request itself, so there is no
second record to link. The open loop is specific to hand-offs.

**The public page hides the promise for four big hand-offs (observed):** refuse and bulk
"collection will be made next scheduled day" and both weed types "on schedule to be cut". All
160 sampled pages read "For detailed information, please contact the Citizens' Service Bureau."
in place of the closing words. These four pairs held 7,845 requests in the window.

**The join is sound (observed):** the page's due-by date equals the file's promise on 1,438 of
1,438 pages, and the close date agrees on 1,139 of 1,139.

## The table (no ids; full version `build/E1/service_table.csv`, 41 rows)

The left-hand count is pages with any item attached; the right-hand count is pages with at least
one work order.

| Service and closing words (311 file) | Division on page | Sampled | Any item | Work order |
|---|---|---|---|---|
| Tree inspection, "removal work order created" (control) | Forestry | 40 | 40 | 40 |
| Tree planting, "approved for next available planting" | Forestry | 40 | 39 | 34 |
| Weeds vacant building, "added to rotation" | Forestry | 40 | 40 | 0 (inspection only) |
| Cave-in, "referred to street maintenance for repair work to be scheduled" | Street Department | 40 | 16 | 16 |
| Weeds vacant building / vacant lot, "on schedule to be cut, call CSB" | Forestry | 80 | 5 | 0 (inspection only) |
| 15 other hand-off pairs: towing "tagged"; refuse "next scheduled day", "employee shortage", "investigated"; bulky items "next scheduled day", "employee shortage", "correct week"; debris "investigated", "correct week"; open storage and exterior code "notice of violation", "already under notice" (4); board-up "referred"; water "scheduled for repair" | Street, Refuse, Building, Water | 600 | 0 | 0 |
| 10 largest "done" types: containers, refuse, residential and major-street potholes, snow, whole-block and single lights, damaged lights, signs, debris | Refuse, Street, Traffic | 300 | 0 | 0 |
| Open past promise: tree inspection | Forestry | 30 | 27 | 27 |
| Open past promise: weeds occupied property | Forestry | 30 | 28 | 24 |
| Open past promise: sewer lateral defect | Street Department | 30 | 14 | 10 |
| Open past promise: sidewalk repair | Street Department | 30 | 10 | 6 |
| Open past promise: cave-ins | Street Department | 30 | 1 | 0 |
| Open past promise: bad condition, tornado debris, LRA tree, exterior code, city tree down | various | 150 | 0 | 0 |

Pooled shares with Wilson 95% intervals (`build/E1/figures.json`):

| Group | Any attached item | 95% interval | Weighted by volume |
|---|---|---|---|
| Hand-off (20 pairs, 800 pages) | 12.5% | 10.4–15.0% | 10.5% |
| Tree removal (40) | 100% | 91–100% | |
| Done (10 types, 300) | 0% | 0–1.3% | |
| Open past promise (10 types, 300) | 26.7% | 22.0–31.9% | 39.2% |

By division (`build/E1/linkage_by_division.csv`), hand-off pages with any item:

| Division | With items / pages | Note |
|---|---|---|
| Forestry | 124 / 200 | includes the tree control |
| Street Department | 16 / 80 | |
| Building | 0 / 200 | |
| Refuse | 0 / 240 | |
| Street Division | 0 / 80 | |
| Water | 0 / 40 | |

## Where the link exists, what it shows

Each sampled request with a work order attached was graded against its promise date, as R1 did.
The grade uses the first finish among work orders created on or after filing:
- the Cityworks `ActualFinishDate` where the order joins to the extracts;
- otherwise the page's "Completed On or Before" date, which is an upper bound.

"No finish" is counted only where the promise passed by 13 Sep 2026
(`build/E1/linked_by_service.csv`).

| Service | Linked with work order | By promise | Late (median days) | No finish | Promise |
|---|---|---|---|---|---|
| Tree removal (closed "removal work order created") | 40 | 1 | 39 (211) | 0 | 14 days |
| Tree planting (closed "approved for next available planting") | 34 | 2 | 24 (121) | 8 | 14 days |
| Cave-in (closed "referred", Right of Way Repair) | 16 | 4 | 12 (9) | 0 | 3 days |
| Open past promise: tree inspection | 27 | 0 | 2 (276) | 24 (1 not yet due) | 14 days |
| Open past promise: weeds occupied property ("Occupied" orders) | 24 | 0 | 1 (36) | 22 (1 not yet due) | 14 days |
| Open past promise: sewer lateral defect (repair-program orders) | 10 | 0 | 0 | 10 | 10 days |
| Open past promise: sidewalk repair (50-50 program orders) | 6 | 0 | 0 | 6 | 14 days |

**Observed:**
- Tree-removal requests carry, in the median, three items: typically a removal and a stump
  removal, sometimes a planting.
- The cave-in link is fast where it exists: the median from filing to first finish is 5 days.
- Planting is graded against a 14-day promise for work the city does by season.

**Inferred:** the promise date measures the wrong thing for planting, and for tree removal it
measures the inspection. That is the gap the entry's rule "carry the promise to the job" names.
**Do not** present the late medians as crew performance without that caveat.

**Observed (small n):** among the 40 sampled cave-ins
"referred", the share with a Right of Way Repair order differs by ward group:
- wards 1–5: 9 of 14;
- wards 6–9: 5 of 13;
- wards 10–14: 2 of 13.

**Inferred:** this is consistent with N3's finding that cave-in intake differs at the ward 5|6
line. It is a record-keeping difference, not evidence about wait times, and must not be used as
an equity claim.

## What the public page tells a resident

**Observed:**
- **Hidden promise.** For four large hand-offs (refuse "collection will be made next scheduled
  day", bulky items the same, and vacant building and vacant lot weeds "on schedule to be cut"),
  all 160 sampled pages show "For detailed information, please contact the Citizens' Service
  Bureau." The closing words appear nowhere on the page.
- **Investigation still open.** 35 closed weed pages (22 vacant-lot, 13 vacant-building, all
  "on schedule") also say "Investigation Still Open".
- **Other closing words.** On all other pages the page shows the file's closing words exactly
  (980 of 980).
- **Tree pages.** These list each attached work order's template, created date and status
  ("Completed On or Before <date>", "Pending", "Scheduled"). That is the "after" picture the
  demo can show.

## Agreement checks (page vs the 311 file of 13 Oct)

| Check | Agree | Of |
|---|---|---|
| "Dept Response Due By" = `PRJCOMPLETEDATE` (ts_promised) | 1,438 | 1,438 (2 pages show no due date) |
| Closed on page = closed in file | 1,436 | 1,440 |
| Close date | 1,139 | 1,139 |
| Closing words | 980 | 1,140 (all 160 misses are the generic CSB line) |

The four status mismatches are changes after the file's end: three requests open in the file
now show Closed, and one closed cave-in now shows Pending.

## Method

**Source and access.**
- **The page.** The city's public status page is
  [check-service-request.cfm](https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/check-service-request.cfm),
  one page per request.
- **Rate.** The page fetcher and the items reader share one file-locked clock
  (`scripts/exec/E1/ratelimit.py`): at most one request every 1.05 seconds to
  `www.stlouis-mo.gov`. Every request carries the user agent
  `stl-civic-hackathon research (status page linkage test; one request per second)`. Each page
  and each items list was read once. The one exception is a structure-test call for one tree
  request at about 3:24 p.m.; its response was not saved, and it is logged.
- **Allowlist.** From the related-items response, only these are kept: item type (inspection or
  work order), item id, template name, created date, status label, the status date ("Completed On
  or Before"), and an inspection result when it is a short upper-case code (e.g. APPROVED). No
  name, e-mail, phone, comment or free text is kept, and a guard aborts the save if an e-mail or
  phone pattern survives. The raw response is never written to disk; its SHA-256 and size are
  logged in `build/E1/private/itemslog.csv`. Filtered items are under
  `data/raw/stlouis-mo.gov/csb-status-items/` (git-ignored). Raw status pages, which carry
  addresses, are under `data/raw/stlouis-mo.gov/csb-status/` (git-ignored).
- **Privacy.** No request, work-order or parcel id and no address appears in `research/` or in
  `build/E1/` outside `build/E1/private/`. Nothing here is below service level, except the
  ward-group split above.

**Sample (`scripts/exec/E1/01_sample.py`; `build/E1/sample_strata.csv`).** Requests filed 1 Jan 2025
to 31 Aug 2026, so every promise has passed, drawn in these strata:
- the 20 largest hand-off pairs (problem code × closing words, classes `handed_off` and
  `converted`, from `build/R1/handoff_composition.csv`), 40 each;
- tree inspections closed "removal work order created", 40, as the positive control (390 in the
  window; not in the top 20);
- the 10 largest problem codes among closures classed `done`, 30 each;
- the 10 largest problem codes among requests still open past their promise, 30 each.

Each stratum is split evenly across ward groups 1–5, 6–9 and 10–14 where counts allow. Order
within a cell is `md5('E1-status-page-2026-10-14' || request_id)`. In total: 1,440 requests in
41 strata.

**Measures.**
- **Any attached item** (observed): the page's hidden `<span id="totalItem">N</span>`, N > 0. The
  page shows "Related Items: Inspections and work orders attached to this request" exactly when
  N > 0, on all 1,440 pages.
- **Work order attached:** at least one item in the "Work Orders" section of the related-items
  list.
- **Linked-request grade:** see the section above.

**Scripts** (`scripts/exec/E1/`; everything after the fetch reruns from saved files without
network):
- `01_sample.py`
- `02_fetch.py` (pages)
- `03_parse.py`
- `04_aggregate.py` (shares, Wilson intervals, agreement)
- `06_items.py` (related items)
- `07_linked.py` (join and grade)
- `08_tables.py` (table and figure registry)
- `09_facts.py` (facts CSV)
- `05_probe.py` (the earlier 12-page probe, kept separate because 10 of its pages were
  hand-picked)
- `01b_sample_b.py` (the unused option-(b) subset)

## Caveats

- **What a zero means.** "Nothing attached" means nothing attached, not nothing done. Potholes
  close "work completed" with nothing attached, and crews may keep records elsewhere: the Forestry
  billing ledger, for one, records weed cuts by parcel.
- **Inspections count.** "Any attached item" includes inspections. Weeds "added to rotation" are
  40 of 40 linked, but only to an inspection.
- **The finish date is a bound.** The page's "Completed On or Before" date is an upper bound on
  the finish. Late counts may be slightly overstated where the order did not join to Cityworks.
- **Sample, not census.** Each type has 30 or 40 pages: shares of 0 have a 95% upper bound of 9%
  (40 pages) or 11% (30 pages).
- **Hand-picked probe.** The 12-page probe (`build/E1/probe_pages.csv`) contained two cave-ins
  "referred" with 0 attached, both in wards 1–5. The sample finds 9 of 14 linked there. The probe
  was too small to show that; it is superseded.
