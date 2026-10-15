import duckdb
con=duckdb.connect('n8.duckdb')
print(con.execute("select ward_raw, count(*) from req where t_init>='2025-05-16' group by 1 order by 2 desc").fetchall()[:20])
def grp(where, res=None, period=('2025-05-16','2026-10-13'), resident=True, extra=''):
    q=f"""select case when ward between 1 and 5 then 'w1_5' when ward between 10 and 14 then 'w10_14' end g,
      count(*) n, median(epoch(t_closed-t_init)/86400.0) med,
      avg(case when t_closed<=t_prj then 1.0 else 0 end) met_prj,
      avg(case when t_closed::date<=t_prj::date then 1.0 else 0 end) met_prj_date
     from req where {where} and upper(status)='CLOSED' and t_init>='{period[0]}' and t_init<'{period[1]}'
     {"and resident=1" if resident else ""} {f"and res='{res}'" if res else ""} {extra}
     and (ward between 1 and 5 or ward between 10 and 14) group by 1 order by 1"""
    return con.execute(q).fetchall()
print('tow tagged after', grp("code='Vehicle Towing'", 'vehicle tagged for tow'))
print('tow tagged after nonres', grp("code='Vehicle Towing'", 'vehicle tagged for tow', resident=False))
print('tow tagged before', grp("code='Vehicle Towing'", 'vehicle tagged for tow', period=('2024-01-01','2025-05-16')))
print('cave referral after', grp("code='Cave-Ins'", 'referred to street maintenance for repair work to be scheduled'))
print('cave referral after nonres', grp("code='Cave-Ins'", 'referred to street maintenance for repair work to be scheduled', resident=False))
print(con.execute("select res, count(*) from req where code='Vehicle Towing' and t_init>='2025-05-16' group by 1 order by 2 desc limit 10").fetchall())
print(con.execute("select res, count(*) from req where code='Cave-Ins' and t_init>='2025-05-16' group by 1 order by 2 desc limit 10").fetchall())
