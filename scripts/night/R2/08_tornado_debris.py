"""R2 step 8: tornado debris requests against the city's own street-clearance record.

Source (keyless; city ArcGIS Online org; downloaded by the R2 hunt):
  Debris_Clearing FeatureServer/0 (AGOL item d6dd7b5e43de4da7a13333a31e8afada,
  "ClayCo Engineering debris cleanup"): 76 street segments, Debris_Cleared = Yes,
  Clearance_Date 23-28 May 2025. It covers street segments cleared after the 16 May 2025 tornado,
  not alleys or private lots.
311 side: debris requests (Debris-alley/street, Debris-Vacant Lot, Debris-Vacant Bldg, TDebris-*)
filed 16 May to 15 Jun 2025, one row per REQUESTID, with coordinates.

Match: request point within 30 m of a cleared segment (equirectangular projection, exact enough at
this scale). Fate for matched requests in R1's terms: cleared by the promise date / cleared after it /
cleared before the request was filed (the record cannot speak to it). Unmatched requests are outside
the record's coverage, NOT evidence of no clearance.

Writes build/R2/tornado_debris_fate.json (aggregates only).
Run: .venv/bin/python -I scripts/night/R2/08_tornado_debris.py
"""
import datetime as dt
import json
import math
import os

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB = os.path.join(ROOT, 'build', 'stl.duckdb')
GJ = os.path.join(ROOT, 'build', 'R2', 'private', 'raw', 'agol_debris', 'debris_clearing_all.geojson')
OUT = os.path.join(ROOT, 'build', 'R2')
R_M = 30.0

segs = []
for f in json.load(open(GJ))['features']:
    p = f['properties']
    when = dt.datetime.fromtimestamp(p['Clearance_Date'] / 1000, tz=dt.timezone.utc).astimezone(
        dt.timezone(dt.timedelta(hours=-5))).replace(tzinfo=None)  # CDT in May
    g = f['geometry']
    lines = [g['coordinates']] if g['type'] == 'LineString' else g['coordinates']
    for line in lines:
        segs.append((line, when, p.get('Debris_Cleared')))

LAT0 = 38.63
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110540.0


def dist_point_line(lon, lat, line):
    px, py = lon * KX, lat * KY
    best = 1e18
    for (x1, y1), (x2, y2) in zip(line[:-1], line[1:]):
        ax, ay, bx, by = x1 * KX, y1 * KY, x2 * KX, y2 * KY
        dx, dy = bx - ax, by - ay
        t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        cx, cy = ax + t * dx, ay + t * dy
        best = min(best, math.hypot(px - cx, py - cy))
    return best


con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
reqs = con.execute("""
SELECT request_id, problem_code, status_group, closure_class, ts_init, ts_promised, ts_closed, lon, lat, ward_group
FROM s.v_requests
WHERE (problem_code LIKE 'Debris-%' OR problem_code LIKE 'TDebris%')
  AND ts_init >= TIMESTAMP '2025-05-16' AND ts_init < TIMESTAMP '2025-06-16' AND lon IS NOT NULL""").fetchall()

out = {'cleared_by_promise': 0, 'cleared_after_promise': 0, 'cleared_before_filing': 0}
by_class = {}
matched = 0
for rid, code, st, cls, ti, tp, tc, lon, lat, wg in reqs:
    near = [w for line, w, ok in segs if ok == 'Yes' and dist_point_line(lon, lat, line) <= R_M]
    key = cls or st
    b = by_class.setdefault(key, {'requests': 0, 'near_cleared_segment': 0})
    b['requests'] += 1
    if not near:
        continue
    matched += 1
    b['near_cleared_segment'] += 1
    after = [w for w in near if w >= ti]
    if not after:
        out['cleared_before_filing'] += 1
    elif tp is not None and min(after) <= tp:
        out['cleared_by_promise'] += 1
    else:
        out['cleared_after_promise'] += 1
res = {'label': 'observed', 'segments': len(segs), 'radius_m': R_M, 'requests_16may_15jun_2025': len(reqs),
       'requests_near_cleared_segment': matched, 'fate_of_matched': out, 'by_closing_class': by_class,
       'note': 'The clearance record covers 76 street segments cleared 23-28 May 2025; requests away from them are outside its coverage.'}
json.dump(res, open(os.path.join(OUT, 'tornado_debris_fate.json'), 'w'), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
