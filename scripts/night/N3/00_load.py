"""N3 step 0: load the cleaned 311 CSVs (2023-2026) into build/N3/csb.parquet, one row per REQUESTID.

Run from the repo root:  .venv/bin/python -I scripts/night/N3/00_load.py
Reads build/csb-clean/<year>.csv (iconv -c copies of the csb.zip yearly files).
The 311 file has no requester identity; no staff fields are read.

Finding (observed 13 Oct 2026, 11:45 p.m.): the public yearly files repeat REQUESTIDs. In 2024-2026,
349,031 rows carry 322,104 distinct REQUESTIDs; 24,020 ids appear 2 to 21 times. The repeated rows are
identical in every column except CALLERTYPE (which differs for 7,303 ids), so they look like one row
per caller attached to a request. We keep one row per REQUESTID and give it a channel by priority:
resident if any of its rows has a resident CALLERTYPE, else staff (NSO), else indeterminate, else other.
n_rows keeps the number of rows (callers) seen.
"""
import duckdb, os, sys
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
YEARS = [int(a) for a in sys.argv[1:]] or [2023, 2024, 2025, 2026]
files = [os.path.join(ROOT, 'build/csb-clean', f'{y}.csv') for y in YEARS]
out = os.path.join(ROOT, 'build/N3/csb.parquet')
con = duckdb.connect()
flist = ', '.join(f"'{f}'" for f in files)
con.execute(f"""
CREATE TABLE raw AS SELECT * FROM read_csv([{flist}], header=true, all_varchar=true, quote='"', escape='"',
    union_by_name=true, ignore_errors=false)
""")
print('raw rows', con.execute('select count(*), count(distinct REQUESTID) from raw').fetchone())
con.execute("""
CREATE TABLE typed AS SELECT
  try_cast(REQUESTID AS BIGINT) AS request_id,
  upper(trim(CALLERTYPE)) AS callertype,
  CASE WHEN upper(trim(CALLERTYPE)) IN ('WEB','PHONE','EMAIL','CHAT','TWITTER','LETTER') THEN 1
       WHEN upper(trim(CALLERTYPE)) = 'NSO' THEN 2
       WHEN upper(trim(CALLERTYPE)) = 'INDETERMINATE' THEN 3 ELSE 4 END AS ch_rank,
  try_cast(DATETIMEINIT AS TIMESTAMP) AS t_init,
  try_cast(DATETIMECLOSED AS TIMESTAMP) AS t_closed,
  try_cast(DATECANCELLED AS TIMESTAMP) AS t_cancel,
  try_cast(DATEINVTDONE AS TIMESTAMP) AS t_invt,
  try_cast(PRJCOMPLETEDATE AS TIMESTAMP) AS t_promise,
  trim(PROBLEMCODE) AS ptype,
  trim(DESCRIPTION) AS description,
  trim("GROUP") AS grp,
  trim(SUBMITTO) AS submitto,
  upper(trim(STATUS)) AS status,
  CASE WHEN upper(trim(STATUS))='CLOSED' AND try_cast(DATETIMECLOSED AS TIMESTAMP) IS NOT NULL THEN 'closed'
       WHEN upper(trim(STATUS))='CANCEL' THEN 'cancelled' ELSE 'open' END AS status_group,
  trim(PUBLICRESOLUTION) AS resolution,
  CASE WHEN trim(WARD) ~ '^[0-9]+$' THEN lpad(cast(cast(trim(WARD) AS INT) AS VARCHAR), 2, '0') ELSE NULL END AS ward,
  trim(NEIGHBORHOOD) AS neighborhood,
  trim(PROBADDRESS) AS probaddress,
  try_cast(SRX AS DOUBLE) AS srx, try_cast(SRY AS DOUBLE) AS sry
FROM raw
""")
con.execute(f"""
COPY (
  SELECT * EXCLUDE (ch_rank, rn, min_rank),
    CASE min_rank WHEN 1 THEN 'resident' WHEN 2 THEN 'staff' WHEN 3 THEN 'indeterminate' ELSE 'other' END AS channel
  FROM (
    SELECT *, row_number() OVER (PARTITION BY request_id ORDER BY ch_rank, callertype) rn,
              min(ch_rank) OVER (PARTITION BY request_id) min_rank,
              count(*) OVER (PARTITION BY request_id) n_rows
    FROM typed)
  WHERE rn = 1
) TO '{out}' (FORMAT parquet)
""")
c = duckdb.connect()
print(c.execute(f"select count(*), count(distinct request_id), min(t_init), max(t_init), count(ward), count(t_closed), count(t_promise), sum(n_rows) from '{out}'").fetchall())
print(c.execute(f"select channel, count(*) from '{out}' group by 1 order by 2 desc").fetchall())
