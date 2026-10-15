import duckdb
con=duckdb.connect('n8.duckdb')
print(con.execute("select stype, count(*) from msdk group by 1 order by 2 desc limit 30").fetchall())
# parse request key into num + rest
con.execute("""create or replace table reqk2 as select rid, k, try_cast(split_part(k,' ',1) as int) num, substr(k, length(split_part(k,' ',1))+2) street from reqk where k is not null""")
con.execute("""create or replace table msdk2 as select pid, lo, hi, substr(k, length(split_part(k,' ',1))+2) street from msdk where k is not null""")
# range match where exact failed
con.execute("""create or replace table req_pid2 as
 select rid, pid, 'exact' how from req_pid
 union all
 select r.rid, min(m.pid), 'range' from reqk2 r join msdk2 m on m.street=r.street and r.num between m.lo and greatest(m.hi,m.lo)
 where r.rid not in (select rid from req_pid) group by r.rid""")
print(con.execute("select how, count(*) from req_pid2 group by 1").fetchall())
