import duckdb
con=duckdb.connect('n8.duckdb')
def q(where, label):
    r=con.execute(f"""select case when ward between 1 and 5 then 'w1_5' else 'w10_14' end g, count(*) n,
      avg(case when t_closed is not null and t_closed<=t_prj then 1.0 else 0 end) met_ts,
      avg(case when t_closed is not null and t_closed::date<=t_prj::date then 1.0 else 0 end) met_date,
      avg(case when t_closed is not null and t_closed<=t_init+interval 5 day then 1.0 else 0 end) met_5d,
      avg(case when t_closed is not null and t_closed::date<=t_init::date+5 then 1.0 else 0 end) met_5d_date
      from req where code='Vehicle Towing' and t_init>='2025-05-16' and t_init<'2026-10-13' and (ward between 1 and 5 or ward between 10 and 14) and {where} group by 1 order by 1""").fetchall()
    print(label, [(g,n,round(a,3),round(b,3),round(c,3),round(d,3)) for g,n,a,b,c,d in r])
q("resident=1 and upper(status)='CLOSED' and res='vehicle tagged for tow'", 'tagged res closed')
q("resident=1 and upper(status)='CLOSED'", 'all words res closed')
q("upper(status)='CLOSED'", 'all words all callers closed')
q("resident=1", 'all res incl open/cancel')
q("resident=1 and upper(status)<>'CANCEL'", 'res not cancelled')
q("resident=1 and upper(status)='CLOSED' and res in ('vehicle tagged for tow','vehicle towed','vehicle gone upon inspection')", 'res closed tagged/towed/gone')
print(con.execute("select epoch(t_prj-t_init)/86400.0 d, count(*) from req where code='Vehicle Towing' and t_init>='2025-05-16' group by 1 order by 2 desc limit 5").fetchall())
