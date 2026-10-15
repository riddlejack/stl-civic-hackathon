import duckdb
con=duckdb.connect('n8.duckdb')
X=lambda q: con.execute(q).fetchall()
con.execute("create or replace table lrap as select distinct ParcelId pid from lra")
def run(texts, resident=True, within3=True, start='2026-01-01', end='2026-10-14', label=''):
    tl=' or '.join(f"r.res ilike '{t}%'" for t in texts)
    con.execute(f"""create or replace temp table L as select r.rid, r.t_init, r.t_closed, r.t_prj, p.pid from req r join req_pid2 p using(rid) join lrap using(pid)
      where r.code='Weeds-Vacant Lot' and r.t_init>='{start}' and r.t_init<'{end}' and upper(r.status)='CLOSED' and ({tl})
      {"and r.resident=1" if resident else ""} {"and r.t_closed<=r.t_init+interval 3 day" if within3 else ""}""")
    r=con.execute("""select count(*), count(distinct pid),
      sum(case when exists(select 1 from cuts c where c.parcel=L.pid and c.sdate>=L.t_init::date and c.sdate<=L.t_init::date+7) then 1 else 0 end) w7,
      sum(case when exists(select 1 from cuts c where c.parcel=L.pid and c.sdate>=L.t_init::date and c.sdate<=L.t_prj::date) then 1 else 0 end) by_prj,
      sum(case when not exists(select 1 from cuts c where c.parcel=L.pid and c.sdate>=L.t_init::date) then 1 else 0 end) none_after,
      count(distinct case when not exists(select 1 from cuts c where c.parcel=L.pid and c.sdate>=L.t_init::date) then pid end) none_after_lots
      from L""").fetchone()
    print(label, r)
run(['on schedule to be cut','added to rotation'], label='res, 3d, sched+rot')
run(['on schedule to be cut'], label='res, 3d, sched only')
run(['on schedule to be cut','added to rotation'], resident=False, label='all callers, 3d, sched+rot')
run(['on schedule to be cut','added to rotation'], within3=False, label='res, any time, sched+rot')
run(['on schedule to be cut','added to rotation'], end='2026-09-16', label='res, 3d, filed to 15 Sep')
