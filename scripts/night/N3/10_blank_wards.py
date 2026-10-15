"""N3 step 10: assign blank-ward requests to wards by location (SRX/SRY, EPSG:3857 -> lon/lat) using
data/raw/city-services/arcgis/layers/maps8_BOUNDARIES_Wards.geojson, and test whether that closes the residual gap
between our ward means and CityStat's (wards 10-12 run 2.6-3.4 days low in ours).
Run: .venv/bin/python -I scripts/night/N3/10_blank_wards.py
"""
import json, os, math, duckdb
import numpy as np
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
REQ = os.path.join(ROOT, 'build/N3/req.parquet')
CS = {'01': 17.18, '02': 19.44, '03': 22.77, '04': 19.69, '05': 19.91, '06': 27.76, '07': 27.44, '08': 27.89, '09': 32.59,
      '10': 35.07, '11': 30.67, '12': 30.33, '13': 24.32, '14': 27.54}
g = json.load(open(os.path.join(ROOT, 'data/raw/city-services/arcgis/layers/maps8_BOUNDARIES_Wards.geojson')))
def pip(x, y, ring):
    ring = np.asarray(ring); inside = np.zeros(len(x), bool)
    for (a, b), (c, d) in zip(ring[:-1], ring[1:]):
        inside ^= ((b > y) != (d > y)) & (x < (c - a) * (y - b) / ((d - b) if d != b else 1e-12) + a)
    return inside
con = duckdb.connect()
rows = con.execute(f"""SELECT request_id, srx, sry, status_group, t_closed, days_close FROM '{REQ}'
   WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01' AND (ward IS NULL OR ward NOT BETWEEN '01' AND '14')""").fetchall()
x = np.array([(r[1] or 0) for r in rows]) / 6378137.0 * 180 / math.pi
y = np.array([(math.atan(math.exp((r[2] or 0) / 6378137.0)) * 360 / math.pi - 90) for r in rows])
assigned = np.array([None] * len(rows), dtype=object)
for f in g['features']:
    w = f'{int(f["properties"]["Ward"]):02d}'; geom = f['geometry']
    polys = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
    m = np.zeros(len(rows), bool)
    for poly in polys:
        for ring in poly: m ^= pip(x, y, ring)
    assigned[m & (assigned == None)] = w
print('blank/odd-ward requests in window:', len(rows), 'assigned by location:', int((assigned != None).sum()))
con.execute("CREATE TABLE asg (request_id BIGINT, ward2 VARCHAR)")
con.executemany("INSERT INTO asg VALUES (?, ?)", [(r[0], a) for r, a in zip(rows, assigned) if a is not None])
res = con.execute(f"""SELECT coalesce(a.ward2, q.ward) w, count(*), avg(days_close) FILTER (WHERE status_group='closed' AND t_closed < '2026-07-01')
   FROM '{REQ}' q LEFT JOIN asg a USING (request_id) WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01' GROUP BY 1 ORDER BY 1""").fetchall()
err = []
for w, n, a in res:
    if w in CS: err.append(abs(a - CS[w])); print(w, n, round(a, 2), CS[w], round(a - CS[w], 2))
print('mean abs err', round(sum(err) / len(err), 2))
