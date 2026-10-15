# N8 independent recompute. Run from an EMPTY scratch directory (writes n8.duckdb to the cwd), in this order:
# load, req, n2, n2b, ledger, msd, addr, addr2, weeds, weeds2, lfl, tow, wardfill, misc, misc2, trees, lra, scan.

import duckdb, sys
R='/Users/jackriddle/Desktop/stl-civic-hackathon'
con=duckdb.connect('n8.duckdb')
files=[f"{R}/build/csb-clean/{y}.csv" for y in range(2008,2027)]
con.execute(f"""
create or replace table raw as
select *, filename as src from read_csv({files}, all_varchar=true, header=true, filename=true, quote='"', escape='"', strict_mode=false, null_padding=true)
""")
print(con.execute("select count(*), count(distinct REQUESTID) from raw").fetchall())
print(con.execute("select regexp_extract(src,'(\\d{4})\\.csv',1) y, count(*), count(distinct REQUESTID) from raw group by 1 order by 1").fetchall())
