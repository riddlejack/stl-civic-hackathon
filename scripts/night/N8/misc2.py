import duckdb
con=duckdb.connect('n8.duckdb')
X=lambda q: con.execute(q).fetchall()
# came back within 30 days: closed 2025-26 with address; later request same code same address within 30 days after close
con.execute("""create or replace temp table c as select rid, code, upper(trim(addr)) a, t_init, t_closed from req where upper(status)='CLOSED' and t_init>='2025-01-01' and t_init<'2026-10-13' and addr is not null and trim(addr)<>''""")
con.execute("""create or replace temp table allr as select rid, code, upper(trim(addr)) a, t_init from req where t_init>='2025-01-01' and addr is not null""")
print('came back', X("""select count(*), sum(case when exists(select 1 from allr r where r.code=c.code and r.a=c.a and r.rid<>c.rid and r.t_init>c.t_closed and r.t_init<=c.t_closed+interval 30 day) then 1 else 0 end) from c"""))
# mowing gaps: parcels with >=2 distinct grass maint dates in 2026
print('mowing', X("""with d as (select distinct parcel, sdate from led where stype in ('Grass Maint','Weed-Grass') and year(sdate)=2026),
 g as (select parcel, sdate - lag(sdate) over (partition by parcel order by sdate) gap from d),
 p as (select parcel, count(*) n, max(gap) mx from g group by 1)
 select count(*) filter (where n>=2), count(*) filter (where n>=2 and mx>90), median(mx) filter (where n>=2), count(*) filter (where n=1) from p"""))
print('mowing GM only', X("""with d as (select distinct parcel, sdate from led where stype='Grass Maint' and year(sdate)=2026),
 g as (select parcel, sdate - lag(sdate) over (partition by parcel order by sdate) gap from d),
 p as (select parcel, count(*) n, max(gap) mx from g group by 1)
 select count(*) filter (where n>=2), count(*) filter (where n>=2 and mx>90), median(mx) filter (where n>=2), count(*) filter (where n=1), count(*) from p"""))
