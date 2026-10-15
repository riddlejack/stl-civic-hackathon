import duckdb
con=duckdb.connect('n8.duckdb')
def run(code, texts, label, status="upper(r.status)='CLOSED'"):
    tl=' or '.join(f"r.res ilike '{t}%'" for t in texts)
    con.execute(f"""create or replace temp table w as select r.rid, r.t_init, r.t_closed, r.res, p.pid from req r left join req_pid2 p on p.rid=r.rid
      where r.code='{code}' and r.t_init>='2026-01-01' and r.t_init<'2026-09-16' and {status} and ({tl})""")
    tot,matched=con.execute("select count(*), count(pid) from w").fetchone()
    r=con.execute("""select count(*) n,
      round(avg(case when exists(select 1 from cuts c where c.parcel=w.pid and c.sdate>=w.t_init::date and c.sdate<=w.t_init::date+30) then 1 else 0 end),4) within30,
      round(avg(case when exists(select 1 from cuts c where c.parcel=w.pid and c.sdate>=w.t_init::date) then 1 else 0 end),4) by_end,
      round(avg(case when not exists(select 1 from cuts c where c.parcel=w.pid and year(c.sdate)=2026) then 1 else 0 end),4) none2026,
      sum(case when not exists(select 1 from cuts c where c.parcel=w.pid and year(c.sdate)=2026) then 1 else 0 end) none2026_n
     from w where pid is not null""").fetchone()
    print(label, 'total',tot,'matched',matched, r)
run('Weeds-Vacant Lot', ['on schedule to be cut','added to rotation'], 'lot sched+rotation')
run('Weeds-Vacant Lot', ['on schedule to be cut'], 'lot sched only')
run('Weeds-Vacant Lot', ['added to rotation'], 'lot rotation only')
run('Weeds-Vacant Bldg', ['on schedule to be cut','added to rotation'], 'bldg sched+rotation')
