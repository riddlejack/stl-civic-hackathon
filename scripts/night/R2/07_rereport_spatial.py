"""R2 step 7: spatial sensitivity for re-reports (50 m instead of the exact normalised address).

Exact address matching undercounts re-reports at street locations (potholes, signals, cave-ins,
towing), where two callers give different house numbers for the same spot. This repeats the
14-day hand-off vs done comparison counting any later request of the same PROBLEMCODE within 50 m
of the closed request's point (N1's lon/lat from SRX/SRY), filed after the closure and within 14 days.

Reads build/stl.duckdb read-only; writes build/R2/rereport_spatial_summary.json (aggregates only).
Run: .venv/bin/python -I scripts/night/R2/07_rereport_spatial.py
"""
import json
import math
import os

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB = os.path.join(ROOT, 'build', 'stl.duckdb')
OUT = os.path.join(ROOT, 'build', 'R2')
R = 50.0

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
con.execute("""
CREATE TEMP TABLE c AS
SELECT r.request_id, r.problem_code, r.ts_init, r.ts_closed, r.lat, r.lon,
       CASE WHEN r.closure_class IN ('handed_off', 'converted') THEN 'handoff' ELSE r.closure_class END AS cls
FROM s.v_requests r CROSS JOIN s.run_dates a
WHERE r.status_group = 'closed' AND r.ts_init >= TIMESTAMP '2025-01-01' AND r.lat IS NOT NULL AND r.lon IS NOT NULL
  AND r.ts_closed + INTERVAL 14 DAY <= a.asof_ts;
CREATE TEMP TABLE n AS
SELECT request_id AS nid, problem_code, ts_init AS n_init, lat, lon FROM s.requests
WHERE ts_init >= TIMESTAMP '2025-01-01' AND lat IS NOT NULL AND lon IS NOT NULL;
""")
con.execute(f"""
CREATE TEMP TABLE hit AS
SELECT c.request_id
FROM c JOIN n ON n.problem_code = c.problem_code AND n.n_init > c.ts_closed AND n.n_init <= c.ts_closed + INTERVAL 14 DAY
   AND n.nid <> c.request_id AND abs(n.lat - c.lat) < 0.0005 AND abs(n.lon - c.lon) < 0.0007
WHERE 6371000 * sqrt(power(radians(n.lat - c.lat), 2) + power(radians(n.lon - c.lon) * cos(radians(c.lat)), 2)) <= {R}
GROUP BY c.request_id;
""")
rows = con.execute("""
WITH t AS (SELECT problem_code, count(*) AS n FROM c GROUP BY 1 HAVING count(*) >= 300)
SELECT c.problem_code,
       count(*) FILTER (WHERE cls = 'handoff') AS na, count(h.request_id) FILTER (WHERE cls = 'handoff') AS ya,
       count(*) FILTER (WHERE cls = 'done') AS nb, count(h.request_id) FILTER (WHERE cls = 'done') AS yb
FROM c JOIN t USING (problem_code) LEFT JOIN hit h USING (request_id)
GROUP BY 1 HAVING count(*) FILTER (WHERE cls = 'handoff') >= 30 AND count(*) FILTER (WHERE cls = 'done') >= 30
""").fetchall()
W = sum(r[1] for r in rows)
pa = sum(r[2] for r in rows) / W
pb = sum(r[1] * r[4] / r[3] for r in rows) / W
Rm = sum(r[2] * r[3] / (r[1] + r[3]) for r in rows)
Sm = sum(r[4] * r[1] / (r[1] + r[3]) for r in rows)
res = {'label': 'observed', 'radius_m': R, 'window_days': 14, 'types': len(rows), 'handoff_closures': W,
       'handoff_pct': round(100 * pa, 2), 'done_same_types_pct': round(100 * pb, 2), 'mh_rr': round(Rm / Sm, 2),
       'note': 'Same comparison as r2_rereport14_handoff_vs_done (exact address: 6.66% vs 4.07%, RR 1.59), with a 50 m radius instead of the address. '
               'Types are re-selected on closures with coordinates, so the type set differs slightly.'}
json.dump(res, open(os.path.join(OUT, 'rereport_spatial_summary.json'), 'w'), indent=1)
print(res)
