"""R2 step 6: trace "approved for next available planting" to the city's own planting records.

Sources (keyless, maps8.stlouis-mo.gov, robots.txt 404 = no rules; downloaded by the R2 hunt
into build/R2/private/raw/maps8_trees/, see build/R2/sources-found.md):
  - PDA/City_of_Saint_Louis_Planted_Trees/MapServer/0 "Planted last 365 days" (DATE_PLANTED,
    ADDRESS, LOCATION_TYPE EASEMENT/PARK, point), a rolling window: 27 Oct 2025 to 1 Sep 2026 on 14 Oct.
  - CITYWORKS/CW_PRINT/MapServer/0 TREES (city tree inventory; DATE_PLANTED populated on 1,840 rows,
    almost all March-August 2026).
311 side: build/stl.duckdb (N1), 'Tree Planting requst', one row per REQUESTID.

Match: a planting at the same normalised address (N1's normalise.norm) on or after the filing date;
secondary: a planting within 25 m of the request point. Baseline: the same match for addresses of
other 311 requests filed in the same months (chance of a planting at any address).

Fair cohort: requests filed 1 Jun 2025 to 28 Feb 2026, whose "next available planting" seasons
(autumn 2025, spring 2026) both fall inside the planting record window. Earlier filings could have
been planted in spring 2025, which no public record dates, so they are reported separately.

Writes build/R2/tree_planting_fate.csv and build/R2/tree_planting_fate.json (aggregates only).
Run: .venv/bin/python -I scripts/night/R2/06_tree_planting.py
"""
import csv
import json
import math
import os
import sys

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'scripts', 'night', 'N1'))
from normalise import norm  # noqa: E402  N1's address normaliser, reused as briefed

DB = os.path.join(ROOT, 'build', 'stl.duckdb')
RAW = os.path.join(ROOT, 'build', 'R2', 'private', 'raw', 'maps8_trees')
OUT = os.path.join(ROOT, 'build', 'R2')

# ------------------------------------------------------------------ plantings (union of the two layers)
plant = {}
with open(os.path.join(RAW, 'pda_planted_last_365_days.csv'), newline='') as f:
    for r in csv.DictReader(f):
        d = (r.get('DATE_PLANTED') or '')[:10]
        if not d:
            continue
        a = norm(r.get('ADDRESS') or '')
        lon, lat = r.get('lon_4326'), r.get('lat_4326')
        key = (a, d, (r.get('LOCATION_TYPE') or '').upper())
        plant[key] = {'addr': a, 'date': d, 'loc_type': (r.get('LOCATION_TYPE') or '').upper(), 'src': 'pda',
                      'lon': float(lon) if lon else None, 'lat': float(lat) if lat else None}
with open(os.path.join(RAW, 'cw_print_trees_2024plus.csv'), newline='') as f:
    for r in csv.DictReader(f):
        d = (r.get('DATE_PLANTED') or '')[:10]
        if not d:
            continue
        a = norm(r.get('ADDRESS') or '')
        lt = (r.get('LOCATION_T') or '').upper() or 'UNKNOWN'
        key = (a, d, 'EASEMENT' if lt == 'EASEMENT' else lt)
        if key in plant:
            plant[key]['src'] = 'both'
            continue
        lon, lat = r.get('lon_4326'), r.get('lat_4326')
        plant[key] = {'addr': a, 'date': d, 'loc_type': lt, 'src': 'cw_print',
                      'lon': float(lon) if lon else None, 'lat': float(lat) if lat else None}

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
con.execute("CREATE TEMP TABLE plantings (addr VARCHAR, pdate DATE, loc_type VARCHAR, src VARCHAR, lon DOUBLE, lat DOUBLE)")
con.executemany("INSERT INTO plantings VALUES (?, ?, ?, ?, ?, ?)",
                [(p['addr'], p['date'], p['loc_type'], p['src'], p['lon'], p['lat']) for p in plant.values()])
pstats = con.execute("""SELECT count(*), count(*) FILTER (WHERE addr <> ''), min(pdate), max(pdate),
                               count(*) FILTER (WHERE loc_type = 'EASEMENT'), count(*) FILTER (WHERE src = 'both') FROM plantings""").fetchone()

# ------------------------------------------------------------------ requests and the baseline group
con.execute("""
CREATE TEMP TABLE req AS
SELECT r.request_id, r.problem_code, r.status_group, r.closure_class, lower(trim(coalesce(r.resolution_public, ''))) AS phrase,
       r.ts_init, CAST(r.ts_init AS DATE) AS init_date, CAST(r.ts_promised AS DATE) AS promise_date, r.addr_norm, r.lon, r.lat, r.ward_group
FROM s.v_requests r
WHERE r.ts_init >= TIMESTAMP '2025-01-01' AND r.addr_norm <> ''
  AND (r.problem_code = 'Tree Planting requst'
       OR (r.problem_code IN ('Refuse not collected', 'Potholes - Residnl', 'Single Light Out')
           AND r.ts_init >= TIMESTAMP '2025-06-01' AND r.ts_init < TIMESTAMP '2026-03-01'));
""")
# address match and 25 m spatial match (equirectangular distance is exact enough at 25 m)
con.execute("""
CREATE TEMP TABLE m AS
SELECT q.request_id,
       min(p.pdate) FILTER (WHERE p.addr = q.addr_norm) AS first_addr,
       min(p.pdate) FILTER (WHERE p.lon IS NOT NULL AND q.lon IS NOT NULL
             AND 6371000 * sqrt(power(radians(p.lat - q.lat), 2) + power(radians(p.lon - q.lon) * cos(radians(q.lat)), 2)) <= 25) AS first_25m
FROM req q JOIN plantings p
  ON p.pdate >= q.init_date
 AND (p.addr = q.addr_norm OR (abs(p.lat - q.lat) < 0.0005 AND abs(p.lon - q.lon) < 0.0007))
GROUP BY q.request_id;
""")


def groupstats(where):
    return con.execute(f"""
    SELECT count(*) AS n,
           count(*) FILTER (WHERE m.first_addr IS NOT NULL) AS addr_planted,
           count(*) FILTER (WHERE coalesce(m.first_addr, m.first_25m) IS NOT NULL) AS any_planted,
           count(*) FILTER (WHERE coalesce(m.first_addr, m.first_25m) <= q.promise_date) AS planted_by_promise,
           median(datediff('day', q.init_date, coalesce(m.first_addr, m.first_25m))) AS median_days_to_planting
    FROM req q LEFT JOIN m USING (request_id) WHERE {where}""").fetchone()


groups = {
    'approved, filed Jun 2025-Feb 2026 (fair cohort)': "problem_code = 'Tree Planting requst' AND phrase = 'approved for next available planting' AND ts_init >= '2025-06-01' AND ts_init < '2026-03-01'",
    'approved, filed Jan-May 2025 (spring 2025 not observable)': "problem_code = 'Tree Planting requst' AND phrase = 'approved for next available planting' AND ts_init < '2025-06-01'",
    'approved, filed Mar-Oct 2026 (next season not yet due)': "problem_code = 'Tree Planting requst' AND phrase = 'approved for next available planting' AND ts_init >= '2026-03-01'",
    'no appropriate planting site, filed Jun 2025-Feb 2026': "problem_code = 'Tree Planting requst' AND phrase LIKE 'no appropriate planting site%' AND status_group = 'closed' AND ts_init >= '2025-06-01' AND ts_init < '2026-03-01'",
    'cancelled, filed Jun 2025-Feb 2026': "problem_code = 'Tree Planting requst' AND status_group = 'cancelled' AND ts_init >= '2025-06-01' AND ts_init < '2026-03-01'",
    'still open, filed Jun 2025-Feb 2026': "problem_code = 'Tree Planting requst' AND status_group = 'open' AND ts_init >= '2025-06-01' AND ts_init < '2026-03-01'",
    'closed complete (done), all 2025-26': "problem_code = 'Tree Planting requst' AND closure_class = 'done'",
    'BASELINE other requests (refuse, potholes, single light), filed Jun 2025-Feb 2026': "problem_code <> 'Tree Planting requst'",
}
rows = []
for g, wh in groups.items():
    n, a, anyp, byp, med = groupstats(wh)
    rows.append({'group': g, 'requests': n, 'planting_same_address': a, 'planting_address_or_25m': anyp,
                 'pct_same_address': round(100.0 * a / n, 1) if n else None,
                 'pct_address_or_25m': round(100.0 * anyp / n, 1) if n else None,
                 'planted_by_promise_date': byp, 'median_days_filing_to_planting': med})
# fair cohort by ward group (block-level safe aggregate)
wg = con.execute("""
SELECT q.ward_group, count(*) AS n, count(*) FILTER (WHERE coalesce(m.first_addr, m.first_25m) IS NOT NULL) AS planted
FROM req q LEFT JOIN m USING (request_id)
WHERE q.problem_code = 'Tree Planting requst' AND q.phrase = 'approved for next available planting'
  AND q.ts_init >= '2025-06-01' AND q.ts_init < '2026-03-01' GROUP BY 1 ORDER BY 1""").fetchall()

# R1-style fate for the fair cohort (promise passed >= 30 days before 13 Oct for every request in it)
fate = con.execute("""
WITH f AS (
  SELECT q.request_id, q.promise_date, coalesce(m.first_addr, m.first_25m) AS first_done
  FROM req q LEFT JOIN m USING (request_id)
  WHERE q.problem_code = 'Tree Planting requst' AND q.phrase = 'approved for next available planting'
    AND q.ts_init >= '2025-06-01' AND q.ts_init < '2026-03-01')
SELECT count(*) AS n,
       count(*) FILTER (WHERE first_done <= promise_date) AS done_by_promise,
       count(*) FILTER (WHERE first_done > promise_date) AS done_late,
       count(*) FILTER (WHERE first_done IS NULL) AS no_record,
       median(datediff('day', promise_date, first_done)) FILTER (WHERE first_done > promise_date) AS median_days_late,
       quantile_cont(datediff('day', promise_date, first_done), 0.25) FILTER (WHERE first_done > promise_date) AS q1_days_late,
       quantile_cont(datediff('day', promise_date, first_done), 0.75) FILTER (WHERE first_done > promise_date) AS q3_days_late,
       max(promise_date) AS latest_promise
FROM f""").fetchone()
fate_d = dict(zip(['n', 'done_by_promise', 'done_late', 'no_record', 'median_days_late', 'q1_days_late', 'q3_days_late', 'latest_promise'], fate))
for k in ['done_by_promise', 'done_late', 'no_record']:
    fate_d['share_' + k] = round(fate_d[k] / fate_d['n'], 4)

# Forestry's planting queue (maps9 FORESTRY_TREES layer 5 PLANTING_PLANNING: inspected sites awaiting planting,
# REQUESTID on 139 rows). A fair-cohort request still in the queue is confirmed not yet planted.
PP = os.path.join(ROOT, 'build', 'R2', 'private', 'raw', 'maps9_forestry', 'planting_planning.csv')
queue = None
if os.path.exists(PP):
    con.execute(f"CREATE TEMP TABLE pq AS SELECT DISTINCT try_cast(REQUESTID AS BIGINT) AS request_id FROM read_csv_auto('{PP}', header=true, all_varchar=true) WHERE REQUESTID IS NOT NULL")
    queue = con.execute("""
    SELECT CASE WHEN coalesce(m.first_addr, m.first_25m) IS NULL THEN 'no planting record' ELSE 'planting matched' END AS fate,
           count(*) AS n, count(pq.request_id) AS in_planting_queue
    FROM req q LEFT JOIN m USING (request_id) LEFT JOIN pq USING (request_id)
    WHERE q.problem_code = 'Tree Planting requst' AND q.phrase = 'approved for next available planting'
      AND q.ts_init >= '2025-06-01' AND q.ts_init < '2026-03-01' GROUP BY 1 ORDER BY 1""").fetchall()

with open(os.path.join(OUT, 'tree_planting_fate.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
res = {'label': 'observed', 'plantings': {'rows': pstats[0], 'with_address': pstats[1], 'min_date': str(pstats[2]), 'max_date': str(pstats[3]),
                                          'easement': pstats[4], 'in_both_layers': pstats[5]},
       'fair_cohort_fate_r1_style': fate_d,
       'fair_cohort_in_planting_queue': [{'fate': a, 'n': b, 'in_planting_queue': c} for a, b, c in (queue or [])],
       'groups': rows, 'fair_cohort_by_ward_group': [{'ward_group': a, 'n': b, 'planted': c, 'pct': round(100.0 * c / b, 1)} for a, b, c in wg]}
json.dump(res, open(os.path.join(OUT, 'tree_planting_fate.json'), 'w'), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
