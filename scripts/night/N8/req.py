import duckdb
R='/Users/jackriddle/Desktop/stl-civic-hackathon'
con=duckdb.connect('n8.duckdb')
con.execute("""
create or replace table req as
select REQUESTID::bigint as rid,
 any_value(PROBLEMCODE) code,
 any_value(STATUS) status,
 try_strptime(any_value(DATETIMEINIT), ['%Y-%m-%d %H:%M:%S.%g','%Y-%m-%d %H:%M:%S']) t_init,
 try_strptime(any_value(DATETIMECLOSED), ['%Y-%m-%d %H:%M:%S.%g','%Y-%m-%d %H:%M:%S']) t_closed,
 try_strptime(any_value(DATECANCELLED), ['%Y-%m-%d %H:%M:%S.%g','%Y-%m-%d %H:%M:%S']) t_cancel,
 try_strptime(any_value(DATEINVTDONE), ['%Y-%m-%d %H:%M:%S.%g','%Y-%m-%d %H:%M:%S']) t_invt,
 try_strptime(any_value(PRJCOMPLETEDATE), ['%Y-%m-%d %H:%M:%S.%g','%Y-%m-%d %H:%M:%S']) t_prj,
 any_value(PRJCOMPLETEDATE) prj_raw,
 any_value(PROBADDRESS) addr,
 any_value(WARD) ward_raw,
 try_cast(any_value(WARD) as int) ward,
 any_value(NEIGHBORHOOD) nbhd,
 min(trim(coalesce(PUBLICRESOLUTION,''))) res,
 count(distinct trim(coalesce(PUBLICRESOLUTION,''))) n_res,
 max(case when CALLERTYPE in ('WEB','PHONE','EMAIL','CHAT','TWITTER') then 1 else 0 end) resident,
 string_agg(distinct CALLERTYPE, ',') callers,
 any_value(SRX) srx, any_value(SRY) sry,
 count(*) nrows
from raw group by REQUESTID
""")
print(con.execute("select count(*), count(t_init), count(t_closed), count(t_prj), count(t_cancel), count(t_invt) from req").fetchall())
print(con.execute("select count(*) from req where t_prj is null and prj_raw is not null and prj_raw<>''").fetchall())
print(con.execute("select prj_raw from req where t_prj is null and prj_raw is not null and prj_raw<>'' limit 5").fetchall())
