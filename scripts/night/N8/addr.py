import duckdb, re
con=duckdb.connect('n8.duckdb')
SUF={'AVE':'AV','AVENUE':'AV','STREET':'ST','BOULEVARD':'BLVD','DRIVE':'DR','PLACE':'PL','ROAD':'RD','COURT':'CT','LANE':'LN','TERRACE':'TER','PARKWAY':'PKWY','PKY':'PKWY'}
def norm(a):
    if a is None: return None
    a=a.upper().split(',')[0]
    a=re.sub(r'\s+',' ',a).strip()
    t=a.split(' ')
    if len(t)<2 or not re.match(r'^\d+$',t[0]): return None
    if t[-1] in SUF: t[-1]=SUF[t[-1]]
    return ' '.join(t)
con.create_function('norm_addr', norm, ['VARCHAR'],'VARCHAR', null_handling='special')
con.execute("create or replace table msdk as select pid, parent, norm_addr(regexp_replace(prop_add,' ST LOUIS MO.*$','')) k, try_cast(lownum as int) lo, try_cast(num as int) hi, predir, sname, stype from msd")
con.execute("create or replace table reqk as select rid, norm_addr(addr) k from req where t_init>='2024-01-01'")
# exact key match
con.execute("create or replace table req_pid as select r.rid, min(m.pid) pid, count(distinct m.pid) npid from reqk r join msdk m on m.k=r.k group by 1")
print(con.execute("select count(*), sum(case when npid>1 then 1 else 0 end) from req_pid").fetchall())
