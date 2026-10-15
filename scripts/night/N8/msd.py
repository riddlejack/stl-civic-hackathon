import json, duckdb
R='/Users/jackriddle/Desktop/stl-civic-hackathon'
rows=[]
with open(f'{R}/data/raw/msd/msd_parcels_stl_city_attrs.jsonl') as f:
    for line in f:
        d=json.loads(line); p=d['properties']
        # never read OWNER_NAME
        rows.append((p.get('PID'), p.get('PARENT_PID'), p.get('PROP_ADD'), p.get('STREET_NUM'), p.get('LOW_STREET_NUM'), (p.get('STREET_PRE_DIRECTION') or '').strip(), (p.get('STREET_NAME') or '').strip(), (p.get('STREET_TYPE') or '').strip(), p.get('PROP_ZIP')))
con=duckdb.connect('n8.duckdb')
con.execute("create or replace table msd(pid varchar, parent varchar, prop_add varchar, num varchar, lownum varchar, predir varchar, sname varchar, stype varchar, zip varchar)")
con.executemany("insert into msd values (?,?,?,?,?,?,?,?,?)", rows)
print(con.execute("select count(*), count(distinct pid) from msd").fetchall())
print(con.execute("select count(distinct l.parcel), count(distinct case when m.pid is not null then l.parcel end) from (select distinct parcel from led where year(sdate)=2026) l left join msd m on m.pid=l.parcel").fetchall())
