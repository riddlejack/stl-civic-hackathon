# The SQL: two files, and how to run them on the 311 file

Both files are plain DuckDB SQL over the city's public 311 file (`csb.zip`, one CSV per year: [download](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip)). DuckDB is free and needs no server. They are in `site/data/downloads/`.

## closure_class.sql: what the closing words say

**What it computes.** It sorts each closed request into one of six classes from its closing words (the `PUBLICRESOLUTION` column):
- `done`: the work was done ("grass cut", "street maintenance work completed");
- `handed_off`: passed on or promised for later ("referred to street maintenance for repair work to be scheduled", "on schedule to be cut");
- `converted`: turned into a work order ("removal work order created");
- `no_action`: nothing to do, or not the city's job;
- `info_other`: words that don't fit, or that haven't been reviewed yet;
- `blank`: no closing words.

It holds two lookup tables, one for closing texts and one for per-type overrides, and two functions, `closure_class(problem_code, text)` and `closure_rule(problem_code, text)`. The rule table was drafted by an AI model and checked against samples (`research/closure-class-review.md`). A division should review its own rows. The full list, with the reason for each class, is `site/data/downloads/closure-classes.csv`.

**Where it is used.** CityStat's "Closing says done" column counts a request as on time only when it closed within CityStat's goal *and* its class is `done`. The weekly review's "verify and close" uses `done` words.

**Run it** (standalone; tested on 15 Oct on the 2026 rows of the 13 Oct file):

```sql
-- duckdb, in the folder with the unzipped yearly CSVs
.read closure_class.sql
SELECT closure_class(trim(PROBLEMCODE), PUBLICRESOLUTION) AS class, count(*) AS n
FROM read_csv('2026.csv', all_varchar = true, header = true)
WHERE DATETIMECLOSED IS NOT NULL
GROUP BY 1 ORDER BY 2 DESC;
```

Some yearly CSVs contain invalid characters. The prototype's loader drops them first, as `iconv -c` does.

## measures.sql: the measures and the past-due list

**What it computes**, as views over the loaded 311 table:
- `promise`: per request, whether it was closed by its promised date (`PRJCOMPLETEDATE`), whether it was **done** by it (closed by the date *and* class `done`), and whether it was within CityStat's goal;
- `monday_list`: the past-due list. Open requests past their promised date, block level, with sensitive types left out. It is the SQL twin of the saved search in [saved-search.md](saved-search.md);
- `weed_promise_ledger` and `request_ledger_flags`: weed requests graded against the Forestry cut ledger (was the lot cut by the promised date?);
- `request_wo_summary`: tree requests matched to Forestry work orders;
- `by_ward`, `by_ward_type`: on-time and done-by-promise shares by type, ward and quarter;
- `receipt(request_id)`: one request's full record (block level). Plus `receipt_private`, with the exact address, for use inside the city only.

**It is not standalone.** It expects the tables the prototype's loader builds: the normalised 311 table, the Forestry cut ledger, parcels, the land-bank list and the Cityworks tree work-order samples. To build them from public files (about 600 MB, no key, no login):

```bash
bash scripts/data/fetch_public.sh
bash scripts/night/N1/run_all.sh
duckdb build/stl.duckdb "SELECT division, count(*) FROM monday_list WHERE filed >= DATE '2025-01-01' GROUP BY 1 ORDER BY 2 DESC"
```

`monday_list` covers every filing year, so add the 2025 filter to match the baselines. Its cut-off is the file's own timestamp (13 Oct, 00:33), while the baselines count promises due by the end of 13 Oct. Counts therefore differ slightly. On the 13 Oct file it returns 1,231 cave-ins, against the baseline's 1,233 (*observed*, read-only, 15 Oct).

In the public repository the fetch script is `scripts/data/fetch_public.sh`; in the working folder a copy is at `site/data/downloads/fetch_public.sh`. A fresh download gives numbers as of that day, not 13 Oct.

## What is not in the two files

- **The ranking** is in `site/data/rank-weights.json` (weights and tier map) and `scripts/exec/E7/rank.py`.
- **The "no record either way" classes** (done, pending, superseded, administrative, no evidence) are in `scripts/exec/E5/`.
- **The 13 Oct baselines** are in `video/tools/b14_baselines.py`, written to `build/E8/baselines.json`.

**Inside the city.** The same logic can run against Cityworks' own database. Its engine, and the translation that needs, are *not established* from outside.
