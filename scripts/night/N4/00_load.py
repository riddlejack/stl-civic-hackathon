"""N4 step 0: load 311 requests 2023-2026 from the cleaned CSVs into one parquet.

Input: build/csb-clean/{2023..2026}.csv (iconv -c copies of csb.zip; invalid UTF-8 dropped).
Output: build/N4/csb_2023_2026.parquet with typed timestamps.
No personal data: the 311 file has no requester identity.
Run: .venv/bin/python -I scripts/night/N4/00_load.py
"""
import duckdb, os
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
src = [f'{ROOT}/build/csb-clean/{y}.csv' for y in (2023, 2024, 2025, 2026)]
out = f'{ROOT}/build/N4/csb_2023_2026.parquet'
con = duckdb.connect()
con.execute(f"""
COPY (
  SELECT
    CAST(REQUESTID AS BIGINT) AS requestid,
    CALLERTYPE AS callertype,
    STATUS AS status,
    PROBLEMCODE AS problemcode,
    DESCRIPTION AS description,
    PLAIN_ENGLISH_NAME_FOR_PROBLEMCODE AS plain_name,
    "GROUP" AS grp,
    PARENT_NODE AS parent_node,
    GRANDPARENT_NODE AS grandparent_node,
    SUBMITTO AS submitto,
    WARD AS ward,
    NEIGHBORHOOD AS neighborhood,
    PROBADDRESS AS probaddress,
    PROBADDTYPE AS probaddtype,
    PUBLICRESOLUTION AS publicresolution,
    TRY_CAST(NULLIF(DATETIMEINIT,'') AS TIMESTAMP) AS t_init,
    TRY_CAST(NULLIF(DATETIMECLOSED,'') AS TIMESTAMP) AS t_closed,
    TRY_CAST(NULLIF(DATECANCELLED,'') AS TIMESTAMP) AS t_cancel,
    TRY_CAST(NULLIF(DATEINVTDONE,'') AS TIMESTAMP) AS t_invtdone,
    TRY_CAST(NULLIF(PRJCOMPLETEDATE,'') AS TIMESTAMP) AS t_promise
  FROM read_csv({src!r}, header=true, all_varchar=true, quote='"', escape='"', union_by_name=true)
) TO '{out}' (FORMAT parquet)
""")
print(con.execute(f"SELECT count(*), min(t_init), max(t_init), count(t_promise), count(t_closed) FROM '{out}'").fetchall())
print(con.execute(f"SELECT year(t_init) y, count(*) FROM '{out}' GROUP BY 1 ORDER BY 1").fetchall())
