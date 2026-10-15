# N1. The pipeline: public files to `build/stl.duckdb` and `build/out/`

Written 13–14 October 2026, about 11:40 p.m. to 12:30 a.m. Central, by the N1 session.

## Admission

**Done.** `bash scripts/night/N1/run_all.sh` rebuilds the database and every export from the files on disk in **21 seconds** (observed), with no key, no network and no model call. It loads all 19 years of 311 (1,502,836 rows, **1,454,222 requests** after one row per REQUESTID), the forestry ledger (2,252,031 rows), MSD parcel attributes (owner names never parsed), the LRA inventory, Forestry's maintenance list, ward polygons and the Cityworks tree and pothole samples (no staff fields). It applies N2's final closure classes, builds the measures as plain SQL views, writes block-level JSON and CSV in the shapes of `site/DATA-CONTRACT.md`, merges every `build/N*/figures.json` (191 figures; each N1 figure has a `derivation`), checks 26 established figures, and runs a privacy scan that fails the build on any id, e-mail, exact address or parcel number in an N1 export (0 issues).

**Knock-out passed.** Weed requests 2025–26 match a parcel at **90.1%** (Weeds-Vacant Lot, 2,387 of 2,649) and **93.3%** (Weeds-Vacant Bldg, 4,840 of 5,187), observed.

**Not done.** Sidewalks, tree inventory, crowd labels and satellite (out of scope tonight). No spatial baseline for the 30 m work-order match. The mowing retrospective has no ward for most non-LRA parcels (ward comes only from LRA or a matched 311 request). The site's scoreboard stays N4's; mine is `scoreboard_n1.json`.

**Could not establish.** Why the 2025 forestry ledger is thin: **13,168 cut rows on 8,780 parcels, against 46,346 on 16,118 in 2026** (observed). "No cut recorded" in 2025 is therefore not evidence of no cut; ledger measures are totalled for 2026 only.

**Assumed.** A request with several caller types counts as resident if any caller is a resident channel (N2's rule). A weed request matches its parcel by address only, without nearest-number or spatial guesses. The 90-day mowing flag is my threshold (decision N1-22). Every choice is logged in `build/N1/decisions.json` (28 entries).

**No ids in public files (COMMON correction 10, decision N1-19).** Sample receipts are numbered R001–R200, and the Monday list is published without request ids. The keys and the copy with ids are in `build/N1/private/`. That is what a division would actually use, so Jack still has to decide how the city version handles ids.

## How to run

```
bash scripts/night/N1/run_all.sh            # normalise tests, build, export, validate, match rates, privacy check
duckdb build/stl.duckdb "SELECT * FROM receipt(<request_id>)"   # one request's receipt (database only)
```

The scripts are `normalise.py` (address normaliser and its 21 tests), `build_db.py` (load and derive), `measures.sql` (every measure, in plain DuckDB SQL), `export.py`, `validate.py`, `match_rates.py` and `privacy_check.py`, all in `scripts/night/N1/`. The build writes to a temporary file and swaps it in, so readers never open a half-built database.

## Schema (main objects)

- **Tables.** `requests` (one row per id). It holds typed `ts_init/closed/cancelled/invt_done/promised`, `channel_group`, `status_group`, `ward` with `ward_source`, `ward_group`, `addr_norm`, `block_label`, and the public-safe `division` and `resolution_public`. Alongside it: `closure_class` (class and source per request), `ledger`, `cuts`, `parcels`, `lra`, `maint_props`, `wo_tree`, `cw_potholes`, `wards`, `addr_lookup`, `request_parcel` (pid and match method), `request_ledger`, `request_wo`, `refiled_next`, `by_ward` (type × ward × quarter × channel × class) and `by_ward_type`.
- **Views.** `v_requests`, `promise`, `refiled`, `request_ledger_flags`, `weed_promise_ledger`, `request_wo_summary`, `monday_list`, `dumping_blocks`, `mowing_gaps`, `receipt_base`, the macro `receipt(id)`, and `receipt_private` (exact address and parcel; database only).
- **Exports in `build/out/`, contract-shaped with the meta envelope:**
  - `run.json` and `meta.json`.
  - `figures.json`: 191 figures keyed by id, N1's 36 plus N2–N5.
  - `receipts.json`: 200 receipts, 20 per main type, each with a contract timeline and a template `line`.
  - `monday_list.json` and `.csv`, with the mowing retrospective, and `mowing_2026.json`.
  - `dumping_blocks.json`.
  - `scoreboard_n1.json`: promise days; closed by promise among requests now due and among closed ones; done by promise; hand-off share; the CityStat goal; and a weeds `ledger_check` against the city's own cut records.
  - `register_counts.json`, `ward_like_for_like.json`, `by_ward.json` and `wards.geojson`.

## Match rates (observed, filed 2025–26)

| Join | Rate |
|---|---|
| Weeds-Vacant Lot / Bldg → parcel | 90.1% / 93.3% |
| Missed-cut and incomplete-cut codes → parcel | 87.8–94.5% |
| All requests with a house number → parcel | 86.3% |
| Ledger parcels cut in 2025–26 found among MSD parcel ids | 99.7% (17,831 of 17,890) |
| File ward vs ward polygon, 20,000 requests sampled | 99.9% agree |
| Cancelled Inspect City Tree → tree work order sample (address) | 10.9% vs 1.8% for unrelated requests |
| Same, address or within 30 m | 19.2% (no spatial baseline computed) |

## Validation (ours, one row per request, vs established)

| Figure | Established | Ours | Why different |
|---|---|---|---|
| Requests, 12 months | 112,859 | 112,858 | as-of boundary |
| Open since 2023; over a year | 21,292; 9,069 | 21,292; 9,072 | as-of boundary |
| Blank outcomes | 14.6% | 14.6% | — |
| Repeat address+code, 12 months | 23.7% | 23.7% raw text (28.0% normalised) | normaliser merges spellings |
| Closed 2025–26; re-filed ≤30 d | 190,856; 11,992 (6.3%) | 175,801; 11,978 (6.8%) | old figure counted rows |
| Vacant-lot weeds "on schedule": cut ≤30 d; by season end; none in 2026 | 35%; 63%; 26% | 36%; 63%; 25% (n=808) | — |
| Tree cancellations 2025–26; with no words | 5,537; 5,415 | 5,316; 5,201 | rows vs requests (rows match exactly) |
| Ledger 2026: rows; parcels; LRA | 37,543; 11,972; 7,425 | 37,543; 11,971; 7,425 | — |
| Q2 2026 potholes within goal, major / residential / alley | 48.6 / 81.1 / 82.9% | 49.8 / 81.5 / 83.9% | rows vs requests |
| Promise offsets for 10 types | 3, 3, 5, 8, 16, 10, 3, 14, 14, 90 | identical | — |
| Light out "work completed", wards 1–5 vs 10–14 | 15.8 vs 42.1 | 16.1 vs 41.0 | dedup, channel rule |
| Towing "tagged for tow" | 12.3 vs 41.0 | 11.9 vs 36.9 | dedup |
| Cave-in "work completed" | 9.6 (n=44) vs 25.1 (n=137) | 8.2 (36) vs 23.0 (115) | dedup |
| Whole-block lights | 0.7 vs 0.7 | 0.7 vs 0.7 | — |

Correction to COMMON note 3: the 2.4% figure is for **all closed** tree requests (ours 2.2%). Closed requests reading "work order created" match at **6.8%** (observed). On timing, using address or a 30 m radius: of 5,201 tree requests cancelled with no words (2025–26), **499 sit near a removal order that was already open when the resident filed** (median 596 days old). Only 84 sit near an order dated after the request. This supports N5's reading (COMMON 9).

New measures from the ledger (observed; 2026 filings, parcel matched, promise date passed):
- Weeds-Vacant Lot: a cut was recorded by the city's own 14-day promise for **18.4% of 1,193 requests**, while 65% were closed as a hand-off.
- Weeds-Vacant Bldg: **18.9% of 1,671** had a cut by the 90-day promise.
- Rotation lots: the median longest gap between cuts is **54 days**. 3,941 of 11,824 rotation lots went more than 90 days.

## What a city analyst needs

Python 3 with four free packages: duckdb, pyarrow, numpy and matplotlib. They also need the city's own public files: `csb.zip`, `forestry-service-records.csv`, `LRA_INVENTORY.csv`, `forestry-maintenance-properties.csv` and the ward boundaries. Two more files are needed: MSD's parcel attributes, or the city's own parcel file with the same three fields, and the Cityworks saved searches. With full Cityworks access the samples become complete layers. Analysts can query `measures.sql` from the DuckDB command line with no Python at all. No licence is stated on any city dataset.

## What is fragile

- **Address matching.** About 10% of weed requests have addresses that match no parcel: unnumbered lots, numbers next to a parcel's recorded range, and spelling. A parcel-id field on the 311 request would remove the whole join.
- **The ledger.** Posting dates are batched by week. 2025 is unexplained and thin. Cuts are keyed by parcel id, so a re-platted parcel drops out.
- **Closure classes.** They are a lookup table. New resolution wording falls to "info_other" until someone reviews it. `class_source` counts how many requests that affects: 6 in 2024–26 today.
- **Work orders.** The Cityworks data are 1,500-row samples, so every tree-work-order rate is a lower bound.
- **Undocumented file quirks.** The CSVs repeat a request once per caller and contain invalid bytes. If the city fixes or changes either, `source_rows` and the build log will show it.

## Addendum, 14 Oct about 1:05 a.m.: N8's findings applied (one re-run, 21 s, privacy check 0 issues)

- **"On schedule" alone (N8 finding 2).** Two new figures count closures reading only "on schedule to be cut" in 2026, parcel matched, filed by 15 September:
  - **`n1_weeds_lot_onschedule_only_no_cut_2026` = 0.214.** 156 of 729 requests had no cut billed all season; 37.2% were cut within 30 days.
  - **`n1_weeds_bldg_onschedule_only_no_cut_2026` = 0.322** (325 of 1,008).
  - The pooled `n1_weeds_*_onschedule_ledger` figures stay registered, now defined as "on schedule OR added to rotation".
- **The ledger repeats rows (finding 10).** `cuts` now holds one row per parcel, date and service type, so per-parcel counts are distinct. In 2026, Grass Maint has **37,543 ledger rows but 31,527 distinct cuts** on 11,971 parcels (`n1_ledger_2026`). `n1_ledger_coverage_by_year` gives both counts for every year.
- **Monday list (finding 14).** Intersections of two house numbers are now rounded to the block. Any longer number run is dropped from the label, and the privacy check fails the run if a three-digit number follows "block of". Police-routed rows (SLMPD Referral, and any request routed to SLMPD) are excluded. The list now holds 24,871 rows.
- **Trees (conflict 3).** The "already open" columns of `request_wo_summary` now use N5's rule: the same address, and an order started more than a day before the request. Cityworks dates are converted from UTC to Central. This gives **289 requests, median 575 days**; N5 has 288. Matches within 30 m (496) sit in separate columns and are worded "possibly a neighbouring tree". N6's brief list c reads these columns, so a bridge re-run will pick up the change.
- **LRA lots (conflict 2).** A new view, `lra_onschedule_no_cut`, applies N5's rule (resident-filed only). It gives 96 requests on 76 lots, against N5's 94 on 75; the gap comes from N1's wider parcel join. Public text should use N5's ids. N6's brief list a does not read this view yet. It still drops the resident filter, which produces the 103 on 82, and a bridge.py change is needed there.
- **Not resolved.** The "came back within 30 days" share is 7.0% here against 6.1% in N8's recompute (10,790 vs 11,978 requests). The likeliest cause is address normalisation, the same effect behind 28.0% vs 23.7% for repeats, but I have not tested it.
