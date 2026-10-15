"""Impact 1: re-reports after hand-off closures vs "done" closures, 30/60/90 days.

Extends R2 (scripts/night/R2/01_rereport.py, 02_summary.py) from 7/14/30 days to
30/60/90 days with the same definitions:
  - universe: requests filed 1 Jan 2025 to the file's as-of time, closed, one row
    per request_id, non-blank normalised address;
  - classes: hand-off = N2 'handed_off' + 'converted'; done = N2 'done';
  - re-report within k days: another request, same addr_norm and same problem_code,
    filed after the closure and no more than k days after it (any channel);
  - a k-day window counts only if closure + k days <= as-of time;
  - eligible types: >= 300 closures 2025-26; a type enters a comparison only if both
    classes have >= 30 complete-window closures;
  - rates directly standardised to the hand-off type mix.
The re-report must be filed AFTER the earlier request was closed (n_init > ts_closed),
so simultaneous duplicates are not counted. Splits: all eligible types; durable-fix types
(type_family.durable); recurring route services only.
Sensitivities: resident-channel re-reports only; later report filed > 24 h after the
original filing (drops parallel reports of one event); R2's subset that excludes
recurring route services (Refuse, street cleaning, weeds) and the dumping family.

Reads build/stl.duckdb READ-ONLY. Writes aggregates only to build/impact/rereports.json.
Run: python3 -I scripts/exec/impact/01_rereports.py
"""
import json
import os

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB = os.path.join(ROOT, 'build', 'stl.duckdb')
OUT = os.path.join(ROOT, 'build', 'impact')
os.makedirs(OUT, exist_ok=True)

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
RECURRING = "(division = 'REFUSE' OR problem_code IN ('Street Cleaning') OR family = 'weeds')"
CHRONIC = "(family = 'dumping')"

con.execute("""
CREATE TEMP TABLE a AS SELECT asof_ts FROM s.run_dates;
CREATE TEMP TABLE c AS
SELECT r.request_id, r.problem_code, r.division, r.family, r.ts_init, r.ts_closed, r.addr_norm,
       CASE WHEN r.closure_class IN ('handed_off','converted') THEN 'handoff' ELSE r.closure_class END AS cls
FROM s.v_requests r
WHERE r.status_group = 'closed' AND r.ts_init >= TIMESTAMP '2025-01-01'
  AND r.addr_norm IS NOT NULL AND r.addr_norm <> '';
CREATE TEMP TABLE n AS
SELECT request_id AS nid, problem_code, addr_norm, ts_init AS n_init, channel_group AS n_channel
FROM s.requests WHERE addr_norm <> '' AND ts_init >= TIMESTAMP '2025-01-01';
CREATE TEMP TABLE p AS
SELECT c.request_id,
       min(epoch(n.n_init - c.ts_closed)/86400.0) AS d_any,
       min(epoch(n.n_init - c.ts_closed)/86400.0) FILTER (WHERE n.n_channel = 'resident') AS d_res,
       min(epoch(n.n_init - c.ts_closed)/86400.0) FILTER (WHERE n.n_init > c.ts_init + INTERVAL 1 DAY) AS d_guard
FROM c JOIN n ON n.addr_norm = c.addr_norm AND n.problem_code = c.problem_code
  AND n.n_init > c.ts_closed AND n.n_init <= c.ts_closed + INTERVAL 90 DAY AND n.nid <> c.request_id
GROUP BY c.request_id;
CREATE TEMP TABLE m AS
SELECT c.*, p.d_any, p.d_res, p.d_guard, a.asof_ts FROM c CROSS JOIN a LEFT JOIN p USING (request_id);
CREATE TEMP TABLE tot AS
SELECT problem_code FROM s.v_requests WHERE status_group='closed' AND ts_init >= TIMESTAMP '2025-01-01'
GROUP BY 1 HAVING count(*) >= 300;
""")

# sanity: R2 reconciliation at 30 days, all eligible types (R2: hand-off 9.62%, done 7.04%)
def compare(k, col='d_any', subset='true'):
    rows = con.execute(f"""
    WITH t AS (
      SELECT problem_code,
        count(*) FILTER (WHERE cls='handoff') AS hn,
        count(*) FILTER (WHERE cls='handoff' AND {col} <= {k}) AS hy,
        count(*) FILTER (WHERE cls='done') AS dn,
        count(*) FILTER (WHERE cls='done' AND {col} <= {k}) AS dy
      FROM m WHERE ts_closed + INTERVAL {k} DAY <= asof_ts AND problem_code IN (SELECT problem_code FROM tot)
        AND ({subset})
      GROUP BY 1)
    SELECT problem_code, hn, hy, dn, dy FROM t WHERE hn >= 30 AND dn >= 30""").fetchall()
    H = sum(r[1] for r in rows)
    std_h = sum(r[1] * (r[2] / r[1]) for r in rows) / H
    std_d = sum(r[1] * (r[4] / r[3]) for r in rows) / H
    return {'window_days': k, 'measure': col, 'types': len(rows), 'handoff_closures': H,
            'done_closures': sum(r[3] for r in rows), 'handoff_rereports': sum(r[2] for r in rows),
            'std_rate_handoff_pct': round(100 * std_h, 2), 'std_rate_done_pct': round(100 * std_d, 2),
            'excess_pts': round(100 * (std_h - std_d), 2),
            'excess_rereports_in_cohort': round(H * (std_h - std_d))}

res = {'definition': 'see module docstring', 'asof': str(con.execute('select asof_ts from a').fetchone()[0])}
res['all_types'] = [compare(k) for k in (30, 60, 90)]
res['all_types_resident'] = [compare(k, 'd_res') for k in (30, 60, 90)]
res['all_types_guard24h'] = [compare(k, 'd_guard') for k in (30, 60, 90)]
sub = f"NOT {RECURRING} AND NOT {CHRONIC}"
res['nonrecurring'] = [compare(k, 'd_any', sub) for k in (30, 60, 90)]
res['nonrecurring_guard24h'] = [compare(k, 'd_guard', sub) for k in (30, 60, 90)]
# durable-fix types (type_family.durable: cave-ins, lights, potholes, signs, city trees), as R2's durable subset
DUR = "problem_code IN (SELECT problem_code FROM s.type_family WHERE durable)"
res['durable'] = [compare(k, 'd_any', DUR) for k in (30, 60, 90)]
res['durable_guard24h'] = [compare(k, 'd_guard', DUR) for k in (30, 60, 90)]
res['recurring_only'] = [compare(k, 'd_any', RECURRING) for k in (30, 60, 90)]

# annual hand-off volume: closures in the 12 months to as-of, eligible types
vol = con.execute(f"""
SELECT count(*) FILTER (WHERE cls='handoff') AS all_h,
       count(*) FILTER (WHERE cls='handoff' AND NOT {RECURRING} AND NOT {CHRONIC}) AS nonrec_h,
       count(*) FILTER (WHERE cls='handoff' AND problem_code IN (SELECT problem_code FROM tot)) AS elig_h,
       count(*) FILTER (WHERE cls='handoff' AND problem_code IN (SELECT problem_code FROM tot) AND NOT {RECURRING} AND NOT {CHRONIC}) AS elig_nonrec_h,
       count(*) FILTER (WHERE cls='handoff' AND problem_code IN (SELECT problem_code FROM tot) AND {DUR}) AS elig_durable_h
FROM m WHERE ts_closed > asof_ts - INTERVAL 365 DAY""").fetchone()
res['handoff_closures_12m'] = dict(zip(['all_with_address', 'nonrecurring_with_address', 'eligible_types', 'eligible_nonrecurring', 'eligible_durable'], vol))
vol25 = con.execute("""SELECT count(*) FROM s.v_requests WHERE closure_class IN ('handed_off','converted')
  AND ts_init >= TIMESTAMP '2025-01-01'""").fetchone()[0]
res['handoff_closures_2025_26_all'] = vol25
json.dump(res, open(os.path.join(OUT, 'rereports.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
