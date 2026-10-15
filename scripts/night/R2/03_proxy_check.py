"""R2 step 3: is a re-report a valid signal that the job was not done?

Where the city's own completion record exists (the Forestry billing ledger
for weeds on vacant lots and vacant buildings), compare re-report rates for
hand-off closures whose cut WAS billed by the promise date with those whose
cut was billed late or not at all. If the rates are the same, re-reports do
not track completion for that service, and the re-report table cannot be
read as a completion measure (the earlier negative result: synthesis-notes,
"Does the record gap itself hurt residents?").

Reads build/stl.duckdb read-only; writes build/R2/proxy_check_weeds.csv.
Run: .venv/bin/python -I scripts/night/R2/03_proxy_check.py
"""
import csv
import os

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB = os.path.join(ROOT, 'build', 'stl.duckdb')
OUT = os.path.join(ROOT, 'build', 'R2')

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
rows = con.execute("""
WITH a AS (SELECT asof_ts FROM s.run_dates),
w AS (
  SELECT r.request_id, r.problem_code, r.addr_norm, r.ts_init, r.ts_closed, r.ts_promised, rl.first_cut_after,
         CASE WHEN rl.first_cut_after IS NULL THEN 'no cut billed by 13 Oct'
              WHEN rl.first_cut_after <= CAST(r.ts_promised AS DATE) THEN 'cut billed by promise'
              ELSE 'cut billed after promise' END AS fate
  FROM s.v_requests r JOIN s.request_ledger rl USING (request_id) CROSS JOIN a
  WHERE r.problem_code IN ('Weeds-Vacant Lot', 'Weeds-Vacant Bldg')
    AND r.status_group = 'closed' AND r.closure_class = 'handed_off'
    AND year(r.ts_init) = 2026 AND r.addr_norm <> ''
    AND r.ts_promised + INTERVAL 30 DAY <= a.asof_ts),
nx AS (SELECT request_id AS nid, problem_code, addr_norm, ts_init AS n_init, channel_group FROM s.requests WHERE addr_norm <> '' AND ts_init >= TIMESTAMP '2026-01-01'),
f AS (
  SELECT w.request_id, w.problem_code, w.fate,
         bool_or(nx.n_init > w.ts_closed AND nx.n_init <= w.ts_closed + INTERVAL 14 DAY) AS rr14,
         bool_or(nx.n_init > w.ts_closed AND nx.n_init <= w.ts_closed + INTERVAL 30 DAY) AS rr30,
         bool_or(nx.n_init > w.ts_promised AND nx.n_init <= w.ts_promised + INTERVAL 30 DAY) AS rr_after_promise30,
         bool_or(nx.n_init > w.ts_closed AND nx.n_init <= w.ts_closed + INTERVAL 30 DAY AND nx.channel_group = 'resident') AS rr30_res
  FROM w LEFT JOIN nx ON nx.addr_norm = w.addr_norm AND nx.problem_code = w.problem_code AND nx.nid <> w.request_id
  GROUP BY ALL)
SELECT problem_code, fate, count(*) AS n,
       round(100.0 * avg(coalesce(rr14, false)::INT), 1) AS pct_rr14,
       round(100.0 * avg(coalesce(rr30, false)::INT), 1) AS pct_rr30,
       round(100.0 * avg(coalesce(rr30_res, false)::INT), 1) AS pct_rr30_resident,
       round(100.0 * avg(coalesce(rr_after_promise30, false)::INT), 1) AS pct_rr30_after_promise
FROM f GROUP BY ROLLUP (problem_code, fate) ORDER BY 1, 2
""").fetchall()
cols = [d[0] for d in con.description]
with open(os.path.join(OUT, 'proxy_check_weeds.csv'), 'w', newline='') as fh:
    wr = csv.writer(fh)
    wr.writerow(cols)
    wr.writerows(rows)
for r in rows:
    print(r)

# ------------------------------------------------------------------ same test on R1's per-request fates (board-ups and weeds), when R1 has written them
R1F = os.path.join(ROOT, 'build', 'R1', 'private', 'fate_requests.parquet')
if os.path.exists(R1F):
    rows = con.execute(f"""
    WITH a AS (SELECT asof_ts FROM s.run_dates),
    f AS (SELECT request_id, rec, outcome FROM '{R1F}' WHERE outcome IN ('done_by_promise', 'done_late', 'no_record')),
    w AS (
      SELECT f.rec, f.outcome, r.request_id, r.problem_code, r.addr_norm, r.ts_closed, r.ts_promised
      FROM f JOIN s.v_requests r USING (request_id) CROSS JOIN a
      WHERE r.status_group = 'closed' AND r.closure_class IN ('handed_off', 'converted') AND r.addr_norm <> ''
        AND r.ts_closed + INTERVAL 30 DAY <= a.asof_ts AND r.ts_promised + INTERVAL 30 DAY <= a.asof_ts),
    nx AS (SELECT request_id AS nid, problem_code, addr_norm, ts_init AS n_init FROM s.requests WHERE addr_norm <> '' AND ts_init >= TIMESTAMP '2024-01-01'),
    g AS (
      SELECT w.rec, w.outcome, w.request_id,
             bool_or(nx.n_init > w.ts_closed AND nx.n_init <= w.ts_closed + INTERVAL 14 DAY) AS rr14,
             bool_or(nx.n_init > w.ts_closed AND nx.n_init <= w.ts_closed + INTERVAL 30 DAY) AS rr30,
             bool_or(nx.n_init > w.ts_promised AND nx.n_init <= w.ts_promised + INTERVAL 30 DAY) AS rrp30
      FROM w LEFT JOIN nx ON nx.addr_norm = w.addr_norm AND nx.problem_code = w.problem_code AND nx.nid <> w.request_id
      GROUP BY ALL)
    SELECT rec, outcome, count(*) AS n,
           round(100.0 * avg(coalesce(rr14, false)::INT), 1) AS pct_rr14,
           round(100.0 * avg(coalesce(rr30, false)::INT), 1) AS pct_rr30,
           round(100.0 * avg(coalesce(rrp30, false)::INT), 1) AS pct_rr30_after_promise
    FROM g GROUP BY ALL ORDER BY 1, 2
    """).fetchall()
    cols = [d[0] for d in con.description]
    with open(os.path.join(OUT, 'proxy_check_r1_fates.csv'), 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(cols)
        wr.writerows(rows)
    print('R1 fates:')
    for r in rows:
        print(r)
