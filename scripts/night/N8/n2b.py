import duckdb
con=duckdb.connect('n8.duckdb')
print(con.execute("select count(*) from req where t_init>='2025-01-01' and upper(status)='CLOSED'").fetchall())
con.execute("""create or replace view closed25 as select r.*, c.class, c.rul from req r left join cc c on c.code=r.code and c.res=r.res
 where t_init>='2025-01-01' and t_init<'2026-10-13' and upper(status)='CLOSED'""")
tot=con.execute("select count(*) from closed25").fetchone()[0]
for row in con.execute("select coalesce(class,'UNMATCHED'), count(*) from closed25 group by 1 order by 2 desc").fetchall():
    print(row, round(row[1]/tot,4))
ho=con.execute("select count(*) from closed25 where class in ('handed_off','converted')").fetchone()[0]
hon=con.execute("select count(*) from closed25 where class in ('handed_off','converted') and rul not like 'handed_off:enforcement%'").fetchone()[0]
print('handoff+converted', ho, ho/tot, 'excl enforcement', hon, hon/tot)
# resident share
r=con.execute("select count(*), sum(case when class in ('handed_off','converted') then 1 else 0 end) from closed25 where resident=1").fetchone(); print('resident', r, r[1]/r[0])
# hand-offs before promise
r=con.execute("select count(*), sum(case when t_closed<=t_prj then 1 else 0 end), count(t_prj) from closed25 where class in ('handed_off','converted')").fetchone(); print('handoff before promise', r, r[1]/r[0], r[1]/r[2])
# texts with multiple resolution among dups
print(con.execute("select count(*) from closed25 where n_res>1").fetchall())
# top hand-off texts concentration
rows=con.execute("select code,res,count(*) n from closed25 where class in ('handed_off','converted') group by 1,2 order by 3 desc limit 10").fetchall()
print(sum(x[2] for x in rows)/ho)
for x in rows: print(x)
