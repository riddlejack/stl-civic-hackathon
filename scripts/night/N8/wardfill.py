import duckdb, json, math
from matplotlib.path import Path
con=duckdb.connect('n8.duckdb')
g=json.load(open('/Users/jackriddle/Desktop/stl-civic-hackathon/build/out/wards.geojson'))
polys=[]
for f in g['features']:
    w=int(f['properties']['Ward']); geom=f['geometry']
    rings = geom['coordinates'] if geom['type']=='Polygon' else [r for p in geom['coordinates'] for r in p]
    if geom['type']=='Polygon': rings=[geom['coordinates'][0]]
    else: rings=[p[0] for p in geom['coordinates']]
    for r in rings: polys.append((w, Path(r)))
def ward_of(x,y):
    lon=x/6378137*180/math.pi; lat=(2*math.atan(math.exp(y/6378137))-math.pi/2)*180/math.pi
    for w,p in polys:
        if p.contains_point((lon,lat)): return w
    return None
rows=con.execute("select rid, srx, sry from req where ward is null and t_init>='2024-01-01' and srx is not null").fetchall()
out=[]
for rid,x,y in rows:
    try: out.append((rid, ward_of(float(x),float(y))))
    except: out.append((rid,None))
con.execute("create or replace table wfill(rid bigint, ward int)")
con.executemany("insert into wfill values (?,?)", out)
print(len(out), sum(1 for o in out if o[1] is not None))
# sanity: polygons agree with WARD field on a sample
samp=con.execute("select rid, srx, sry, ward from req where ward is not null and t_init>='2025-01-01' using sample 2000").fetchall()
agree=sum(1 for rid,x,y,w in samp if x and ward_of(float(x),float(y))==w); print('agree', agree, len(samp))
