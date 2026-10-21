"""N2 step 1: load 311 requests 2024-2026 from the cleaned CSVs into a parquet file, one row per request.

The city's yearly CSVs repeat a request once per caller: 2024-2026 hold 349,031 rows for 322,104
REQUESTIDs (24,020 ids repeated, up to 21 times; 19,431 rows are exact duplicates and the rest differ
only in CALLERTYPE). Counting rows over-counts requests by about 8%. This step keeps one row per
REQUESTID and records n_rows and the channel:
  channel = 'resident' if any row has CALLERTYPE in WEB/PHONE/EMAIL/CHAT/TWITTER/LETTER,
            else 'staff' if any row is NSO, else 'indeterminate'.

Input:  build/csb-clean/{2024,2025,2026}.csv (iconv -c copies of the city's csb.zip CSVs)
Output: build/N2/private/csb_2024_2026.parquet (has addresses; not for publication)
Run:    .venv/bin/python -I scripts/night/N2/01_load.py
"""
import pathlib
import duckdb

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "build" / "csb-clean"
OUT = ROOT / "build" / "N2" / "private" / "csb_2024_2026.parquet"
OUT.parent.mkdir(parents=True, exist_ok=True)

files = [str(SRC / f"{y}.csv") for y in (2024, 2025, 2026)]
con = duckdb.connect()
con.execute(f"""
CREATE TABLE raw AS SELECT * FROM read_csv({files!r}, header=true, all_varchar=true, quote='"', escape='"')
""")
con.execute(f"""
COPY (
  WITH ch AS (
    SELECT REQUESTID, count(*) AS n_rows,
      string_agg(DISTINCT CALLERTYPE, '+' ORDER BY CALLERTYPE) AS callertypes,
      CASE WHEN bool_or(CALLERTYPE IN ('WEB','PHONE','EMAIL','CHAT','TWITTER','LETTER')) THEN 'resident'
           WHEN bool_or(CALLERTYPE = 'NSO') THEN 'staff' ELSE 'indeterminate' END AS channel
    FROM raw GROUP BY REQUESTID),
  one AS (SELECT * EXCLUDE (rn) FROM (SELECT *, row_number() OVER (PARTITION BY REQUESTID ORDER BY CALLERTYPE) rn FROM raw) WHERE rn = 1)
  SELECT
    one.REQUESTID::BIGINT AS REQUESTID, ch.n_rows, ch.callertypes, ch.channel,
    STATUS, PROBLEMCODE, DESCRIPTION, PLAIN_ENGLISH_NAME_FOR_PROBLEMCODE AS PLAIN_NAME,
    "GROUP" AS GRP, PARENT_NODE, SUBMITTO, WARD, NEIGHBORHOOD, PROBADDRESS, PROBADDTYPE,
    PUBLICRESOLUTION,
    TRY_CAST(DATETIMEINIT AS TIMESTAMP)   AS t_init,
    TRY_CAST(DATETIMECLOSED AS TIMESTAMP) AS t_closed,
    TRY_CAST(DATECANCELLED AS TIMESTAMP)  AS t_cancel,
    TRY_CAST(DATEINVTDONE AS TIMESTAMP)   AS t_invdone,
    TRY_CAST(PRJCOMPLETEDATE AS TIMESTAMP) AS t_promise
  FROM one JOIN ch USING (REQUESTID)
) TO '{OUT}' (FORMAT parquet)
""")
print("raw rows, distinct ids:", con.execute("SELECT count(*), count(DISTINCT REQUESTID) FROM raw").fetchone())
print("exact-duplicate rows:", con.execute("SELECT (SELECT count(*) FROM raw) - (SELECT count(*) FROM (SELECT DISTINCT * FROM raw))").fetchone()[0])
r = con.execute(f"""SELECT count(*), min(t_init), max(t_init),
  count(*) FILTER (WHERE STATUS='CLOSED'), count(*) FILTER (WHERE STATUS='CLOSED' AND t_closed IS NULL),
  count(*) FILTER (WHERE n_rows > 1)
  FROM '{OUT}'""").fetchone()
print("requests, min init, max init, closed, closed w/o date, requests with >1 row:", r)
