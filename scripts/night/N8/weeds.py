import duckdb
con=duckdb.connect('n8.duckdb')
con.execute("""create or replace table cuts as select distinct parcel, sdate from led where stype in ('Grass Maint','Weed-Grass')""")
base="""select r.rid, r.t_init, r.t_closed, r.res, p.pid from req r left join req_pid2 p on p.rid=r.rid
 where r.code='{code}' and r.t_init>='2026-01-01' and r.t_init<'2026-09-16' and upper(r.status)='CLOSED' and r.res ilike 'on schedule to be cut%'"""
for code in ['Weeds-Vacant Lot','Weeds-Vacant Bldg']:
    con.execute(f"create or replace temp table w as {base.format(code=code)}")
    tot,matched=con.execute("select count(*), count(pid) from w").fetchone()
    print(code,'on-schedule closed', tot, 'matched', matched)
    q="""select count(*) n,
      avg(case when exists(select 1 from cuts c where c.parcel=w.pid and c.sdate>=w.t_init::date and c.sdate<=w.t_init::date+30) then 1 else 0 end) within30,
      avg(case when exists(select 1 from cuts c where c.parcel=w.pid and c.sdate>=w.t_init::date and c.sdate<='2026-10-13') then 1 else 0 end) by_end,
      avg(case when not exists(select 1 from cuts c where c.parcel=w.pid and year(c.sdate)=2026) then 1 else 0 end) none2026,
      avg(case when not exists(select 1 from cuts c where c.parcel=w.pid and c.sdate>=w.t_init::date) then 1 else 0 end) none_after
     from w where pid is not null"""
    print(con.execute(q).fetchall())
    # within 3 days closure variant
    print(con.execute(q.replace("from w where pid is not null","from w where pid is not null and t_closed<=t_init+interval 3 day")).fetchall())
