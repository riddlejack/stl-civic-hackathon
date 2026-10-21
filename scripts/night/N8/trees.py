import duckdb, json, re, datetime, collections
R='.'
con=duckdb.connect('n8.duckdb')
d=json.load(open(f'{R}/data/raw/city-services/arcgis/cityworks-service/layers/WO_Easement_Tree_Removals_New_6955.json'))
SUF={'AVE':'AV','AVENUE':'AV','STREET':'ST','BOULEVARD':'BLVD','DRIVE':'DR','PLACE':'PL','ROAD':'RD','COURT':'CT','LANE':'LN','TERRACE':'TER','PARKWAY':'PKWY'}
def norm(a):
    if a is None: return None
    a=a.upper().split(',')[0]; a=re.sub(r'\s+',' ',a).strip(); t=a.split(' ')
    if len(t)<2 or not re.match(r'^\d+$',t[0]): return None
    if t[-1] in SUF: t[-1]=SUF[t[-1]]
    return ' '.join(t)
rows=[]
st=collections.Counter()
for f in d['features']:
    a=f['attributes']; st[(a['Status'],a['Description'])]+=1
    sd=a['ProjStartDate']
    rows.append((a['WORKORDERID'], norm(a['WoAddress']), datetime.datetime.utcfromtimestamp(sd/1000) if sd else None, a['WOXCoordinate'], a['WOYCoordinate'], a['Status']))
print(st.most_common(10))
con.execute("create or replace table wo(woid bigint, k varchar, start_utc timestamp, x double, y double, status varchar)")
con.executemany("insert into wo values (?,?,?,?,?,?)", rows)
# convert UTC to Central
con.execute("create or replace table wo2 as select *, timezone('America/Chicago', start_utc::timestamptz) as start_ct from wo")
print(con.execute("select min(start_utc), max(start_utc), count(*), count(k) from wo").fetchall())
con.execute("""create or replace temp table tc as select r.rid, r.t_init, k.k, try_cast(r.srx as double) x, try_cast(r.sry as double) y from req r join reqk k using(rid)
  where r.code='Inspect City Tree' and upper(r.status)='CANCEL' and r.res='' and r.t_init>='2025-01-01' and r.t_init<'2026-10-14'""")
print('blank cancelled', con.execute("select count(*) from tc").fetchall())
# check tz of start: does wo2 start_ct look like naive local?
print(con.execute("select start_utc, start_ct from wo2 limit 2").fetchall())
for label, cond in [('exact', 'w.k=t.k'), ('exact or 30m', "(w.k=t.k or (t.x is not null and sqrt((w.x-t.x)^2+(w.y-t.y)^2)*cos(radians(38.63))<=30))")]:
    for lagdesc, lag in [('>1 day before', "w.start_ct < t.t_init - interval 1 day"), ('before', "w.start_ct < t.t_init")]:
        r=con.execute(f"""select count(*), median(age_days) from (select t.rid, max(epoch(t.t_init - w.start_ct)/86400.0) age_days from tc t join wo2 w on {cond} where {lag} group by 1)""").fetchone()
        print(label, lagdesc, r)
    print(label, 'any match', con.execute(f"select count(distinct t.rid) from tc t join wo2 w on {cond}").fetchone())
