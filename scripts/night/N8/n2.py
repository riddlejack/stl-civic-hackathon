import duckdb
R='.'
con=duckdb.connect('n8.duckdb')
con.execute(f"create or replace table cc as select PROBLEMCODE code, coalesce(resolution_text,'') res, class, rule_or_judgement as rul from read_csv('{R}/research/chapters/N2-closure-classes.csv', all_varchar=true, header=true)")
print(con.execute("select count(*), count(distinct (code,res)) from cc").fetchall())
# closed definitions
for name,cond in [('status closed', "upper(status)='CLOSED'"), ('t_closed notnull', "t_closed is not null"), ('t_closed notnull & not cancel', "t_closed is not null and t_cancel is null and upper(status)<>'CANCEL'")]:
    print(name, con.execute(f"select count(*) from req where t_init>='2025-01-01' and t_init<'2026-10-13' and {cond}").fetchall(),
          con.execute(f"select count(*) from req where t_init>='2025-01-01' and t_init<'2026-10-12' and {cond}").fetchall())
print(con.execute("select upper(status), count(*), count(t_closed), count(t_cancel) from req where t_init>='2025-01-01' group by 1").fetchall())
print(con.execute("select max(t_init), max(t_closed) from req").fetchall())
