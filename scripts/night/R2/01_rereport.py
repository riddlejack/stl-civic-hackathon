"""R2 step 1: re-reports after closure, by closing class, every service.

Reads build/stl.duckdb (N1's database) READ-ONLY and writes aggregated tables
to build/R2/. No addresses or ids leave this script.

Definition (R2 brief, item 1): a closure is "re-reported within k days" if
another request with the same normalised address (N1's addr_norm, made by
scripts/night/N1/normalise.py) and the same PROBLEMCODE was filed after the
closure time and no more than k days after it. Universe: requests filed
1 Jan 2025 to the file's as-of time, closed (STATUS CLOSED), one row per
REQUESTID (COMMON correction 6), with a non-blank address. A k-day window
counts only if it ended before the file's as-of time.

Sensitivities (each a separate column):
  res   - the later request came from a resident channel
  guard - the later request was filed more than 24 h after the ORIGINAL was
          filed (drops parallel reports of the same event, which fall after
          a closure only because hand-offs close in minutes)
  first - only closures at addresses with no request of the same type in
          the 365 days before filing (chronic-site control)
  prom  - window starts at the later of closure and the city's promise date
          (PRJCOMPLETEDATE): "still reported after the city's own deadline"

Run: .venv/bin/python -I scripts/night/R2/01_rereport.py
"""
import csv
import json
import os
import sys
import time

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB = os.path.join(ROOT, 'build', 'stl.duckdb')
OUT = os.path.join(ROOT, 'build', 'R2')
os.makedirs(OUT, exist_ok=True)
t0 = time.time()

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")

# ---------------------------------------------------------------- hand-off kind (R-COMMON: crew work / owner enforcement / referral elsewhere)
# Provisional R2 mapping from N2's rule and the closing text; R1 publishes the official composition.
KIND_SQL = """
CASE
  WHEN closure_class = 'converted' THEN 'crew_work'
  WHEN closure_class <> 'handed_off' THEN NULL
  WHEN class_rule LIKE 'handed_off:enforcement%' THEN 'owner_enforcement'
  WHEN lower(resolution_public) LIKE '%refer to treasurer for ticketing%' THEN 'owner_enforcement'
  WHEN class_rule LIKE 'handed_off:external_agency%' THEN 'referral_elsewhere'
  WHEN lower(trim(resolution_public)) IN ('referred to proper department', 'referred to building division',
                                          'referred to community sanitation') THEN 'referral_elsewhere'
  ELSE 'crew_work'
END
"""

R1_COMP = os.path.join(ROOT, 'build', 'R1', 'handoff_composition.csv')
if os.path.exists(R1_COMP):
    # R1's phrase-level composition (kind and traceability per type x closing phrase) is the official one;
    # it covers every 2025-26 hand-off closure (61,845 of 61,845 matched on 14 Oct).
    con.execute(f"CREATE TEMP TABLE r1map AS SELECT problem_code, closing_phrase, kind AS r1_kind, traceability, record FROM read_csv_auto('{R1_COMP}', header=true)")
else:
    con.execute("CREATE TEMP TABLE r1map (problem_code VARCHAR, closing_phrase VARCHAR, r1_kind VARCHAR, traceability VARCHAR, record VARCHAR)")

con.execute(f"""
CREATE TEMP TABLE run_asof AS SELECT asof_ts FROM s.run_dates;

CREATE TEMP TABLE c AS
SELECT r.request_id, r.problem_code, r.type_name, r.division, r.family, r.durable,
       r.closure_class, r.class_rule, trim(r.resolution_public) AS res_text,
       CASE WHEN r.closure_class IN ('handed_off', 'converted') THEN 'handoff' ELSE r.closure_class END AS cls,
       coalesce(m.r1_kind, {KIND_SQL}) AS kind, m.r1_kind IS NOT NULL AS kind_from_r1, m.traceability, m.record,
       r.ts_init, r.ts_closed, r.ts_promised, r.promise_days, r.addr_norm, r.ward_group, r.channel_group,
       greatest(r.ts_closed, coalesce(r.ts_promised, r.ts_closed)) AS ts_anchor,
       r.addr_norm IS NOT NULL AND r.addr_norm <> '' AS has_addr
FROM s.v_requests r
LEFT JOIN r1map m ON r.closure_class IN ('handed_off', 'converted') AND m.problem_code = r.problem_code
                 AND m.closing_phrase = lower(trim(r.resolution_public))
WHERE r.status_group = 'closed' AND r.ts_init >= TIMESTAMP '2025-01-01';

-- every later request at the same address and type (any status, any channel)
CREATE TEMP TABLE n AS
SELECT request_id AS nid, problem_code, addr_norm, ts_init AS n_init, channel_group AS n_channel
FROM s.requests
WHERE addr_norm <> '' AND ts_init >= TIMESTAMP '2024-01-01';

-- prior history: same address and type in the 365 days before filing
CREATE TEMP TABLE prior AS
SELECT c.request_id, count(n.nid) AS prior365
FROM c LEFT JOIN n ON n.addr_norm = c.addr_norm AND n.problem_code = c.problem_code
   AND n.n_init < c.ts_init AND n.n_init >= c.ts_init - INTERVAL 365 DAY AND n.nid <> c.request_id
WHERE c.has_addr
GROUP BY c.request_id;

-- later reports within 30 days of closure
CREATE TEMP TABLE pairs AS
SELECT c.request_id, n.nid, n.n_init, n.n_channel,
       epoch(n.n_init - c.ts_closed) / 86400.0 AS d,
       n.n_init > c.ts_init + INTERVAL 1 DAY AS guard_ok
FROM c JOIN n ON n.addr_norm = c.addr_norm AND n.problem_code = c.problem_code
   AND n.n_init > c.ts_closed AND n.n_init <= c.ts_closed + INTERVAL 30 DAY AND n.nid <> c.request_id
WHERE c.has_addr;

-- later reports within 30 days of the later of closure and promise
CREATE TEMP TABLE pairs_p AS
SELECT c.request_id, min(epoch(n.n_init - c.ts_anchor) / 86400.0) AS dp
FROM c JOIN n ON n.addr_norm = c.addr_norm AND n.problem_code = c.problem_code
   AND n.n_init > c.ts_anchor AND n.n_init <= c.ts_anchor + INTERVAL 30 DAY AND n.nid <> c.request_id
WHERE c.has_addr
GROUP BY c.request_id;

-- filing-anchored: closed within 14 days of filing, and reported again 15-44 days after the ORIGINAL filing
-- (same calendar window for every class, so early hand-off closures get no longer exposure)
CREATE TEMP TABLE pairs_f AS
SELECT c.request_id, min(epoch(n.n_init - c.ts_init) / 86400.0) AS df
FROM c JOIN n ON n.addr_norm = c.addr_norm AND n.problem_code = c.problem_code
   AND n.n_init > c.ts_init + INTERVAL 14 DAY AND n.n_init <= c.ts_init + INTERVAL 44 DAY AND n.nid <> c.request_id
WHERE c.has_addr AND c.ts_closed <= c.ts_init + INTERVAL 14 DAY
GROUP BY c.request_id;

CREATE TEMP TABLE cm AS
WITH p AS (
  SELECT request_id,
         min(d) AS d_any,
         min(d) FILTER (WHERE n_channel = 'resident') AS d_res,
         min(d) FILTER (WHERE guard_ok) AS d_guard
  FROM pairs GROUP BY request_id)
SELECT c.*, coalesce(pr.prior365, 0) AS prior365,
       p.d_any, p.d_res, p.d_guard, pp.dp, pf.df,
       c.ts_closed <= c.ts_init + INTERVAL 14 DAY AND c.ts_init + INTERVAL 44 DAY <= a.asof_ts AS wf,
       c.ts_closed + INTERVAL 7 DAY <= a.asof_ts AS w7,
       c.ts_closed + INTERVAL 14 DAY <= a.asof_ts AS w14,
       c.ts_closed + INTERVAL 30 DAY <= a.asof_ts AS w30,
       c.ts_anchor + INTERVAL 30 DAY <= a.asof_ts AS wp30
FROM c CROSS JOIN run_asof a
LEFT JOIN prior pr USING (request_id)
LEFT JOIN p USING (request_id)
LEFT JOIN pairs_p pp USING (request_id)
LEFT JOIN pairs_f pf USING (request_id);
""")

print('base tables', round(time.time() - t0, 1), 's', file=sys.stderr)

# ---------------------------------------------------------------- per type x class
AGG = """
  count(*) AS closed_all,
  count(*) FILTER (WHERE has_addr) AS closed_addr,
  count(*) FILTER (WHERE has_addr AND w7) AS n7,
  count(*) FILTER (WHERE has_addr AND w7 AND d_any <= 7) AS rr7,
  count(*) FILTER (WHERE has_addr AND w14) AS n14,
  count(*) FILTER (WHERE has_addr AND w14 AND d_any <= 14) AS rr14,
  count(*) FILTER (WHERE has_addr AND w30) AS n30,
  count(*) FILTER (WHERE has_addr AND w30 AND d_any <= 30) AS rr30,
  count(*) FILTER (WHERE has_addr AND w14 AND d_res <= 14) AS rr14_res,
  count(*) FILTER (WHERE has_addr AND w14 AND d_guard <= 14) AS rr14_guard,
  count(*) FILTER (WHERE has_addr AND w14 AND prior365 = 0) AS n14_first,
  count(*) FILTER (WHERE has_addr AND w14 AND prior365 = 0 AND d_any <= 14) AS rr14_first,
  count(*) FILTER (WHERE has_addr AND wp30) AS np30,
  count(*) FILTER (WHERE has_addr AND wp30 AND dp <= 30) AS rrp30,
  median(epoch(ts_closed - ts_init) / 86400.0) AS med_days_to_close
"""
con.execute(f"""
CREATE TEMP TABLE type_class AS
SELECT problem_code, any_value(type_name) AS type_name, any_value(division) AS division, cls, {AGG}
FROM cm GROUP BY problem_code, cls;
CREATE TEMP TABLE type_tot AS
SELECT problem_code, count(*) AS closures_2025_26 FROM cm GROUP BY problem_code;
CREATE TEMP TABLE type_kind AS
SELECT problem_code, kind, {AGG} FROM cm WHERE cls = 'handoff' GROUP BY problem_code, kind;
""")

ELIG = 300
rows = con.execute(f"""
SELECT t.problem_code, t.type_name, t.division, tt.closures_2025_26, t.cls,
       t.closed_all, t.closed_addr, t.n7, t.rr7, t.n14, t.rr14, t.n30, t.rr30, t.rr14_res, t.rr14_guard,
       t.n14_first, t.rr14_first, t.np30, t.rrp30, round(t.med_days_to_close, 2)
FROM type_class t JOIN type_tot tt USING (problem_code)
WHERE tt.closures_2025_26 >= {ELIG}
ORDER BY tt.closures_2025_26 DESC, t.problem_code, t.cls
""").fetchall()
hdr = ['problem_code', 'type_name', 'division', 'closures_2025_26', 'class', 'closed', 'closed_with_address',
       'n_window7', 'rereported7', 'n_window14', 'rereported14', 'n_window30', 'rereported30',
       'rereported14_resident', 'rereported14_guard24h', 'n_window14_first_report', 'rereported14_first_report',
       'n_window30_after_promise', 'rereported30_after_promise', 'median_days_to_close']


def pct(a, b):
    return round(100.0 * a / b, 1) if b else None


with open(os.path.join(OUT, 'rereport_by_type_class.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(hdr + ['pct7', 'pct14', 'pct30', 'pct14_resident', 'pct14_guard24h', 'pct14_first_report', 'pct30_after_promise'])
    for r in rows:
        (n7, rr7, n14, rr14, n30, rr30, r14r, r14g, n14f, r14f, np30, rp30) = r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18]
        w.writerow(list(r) + [pct(rr7, n7), pct(rr14, n14), pct(rr30, n30), pct(r14r, n14), pct(r14g, n14),
                              pct(r14f, n14f), pct(rp30, np30)])

krows = con.execute(f"""
SELECT k.problem_code, k.kind, k.closed_all, k.closed_addr, k.n7, k.rr7, k.n14, k.rr14, k.n30, k.rr30,
       k.rr14_res, k.rr14_guard, k.n14_first, k.rr14_first, k.np30, k.rrp30, round(k.med_days_to_close, 2)
FROM type_kind k JOIN type_tot tt USING (problem_code)
WHERE tt.closures_2025_26 >= {ELIG}
ORDER BY k.problem_code, k.kind
""").fetchall()
with open(os.path.join(OUT, 'rereport_by_type_handoff_kind.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['problem_code', 'kind', 'closed', 'closed_with_address', 'n_window7', 'rereported7', 'n_window14',
                'rereported14', 'n_window30', 'rereported30', 'rereported14_resident', 'rereported14_guard24h',
                'n_window14_first_report', 'rereported14_first_report', 'n_window30_after_promise',
                'rereported30_after_promise', 'median_days_to_close', 'pct14', 'pct30'])
    for r in krows:
        w.writerow(list(r) + [pct(r[7], r[6]), pct(r[9], r[8])])

# ---------------------------------------------------------------- per closing text (hand-offs), for the extrapolation's plausibility checks
trows = con.execute(f"""
SELECT problem_code, cls, kind, res_text, count(*) AS closed,
       count(*) FILTER (WHERE has_addr AND w7) AS n7, count(*) FILTER (WHERE has_addr AND w7 AND d_any <= 7) AS rr7,
       count(*) FILTER (WHERE has_addr AND w14) AS n14, count(*) FILTER (WHERE has_addr AND w14 AND d_any <= 14) AS rr14,
       count(*) FILTER (WHERE has_addr AND w30) AS n30, count(*) FILTER (WHERE has_addr AND w30 AND d_any <= 30) AS rr30,
       count(*) FILTER (WHERE has_addr AND wp30) AS np30, count(*) FILTER (WHERE has_addr AND wp30 AND dp <= 30) AS rrp30
FROM cm GROUP BY ALL HAVING count(*) >= 50
ORDER BY problem_code, closed DESC
""").fetchall()
with open(os.path.join(OUT, 'rereport_by_type_text.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['problem_code', 'class', 'kind', 'closing_text', 'closed', 'n_window7', 'rereported7', 'n_window14',
                'rereported14', 'n_window30', 'rereported30', 'n_window30_after_promise', 'rereported30_after_promise',
                'pct7', 'pct14', 'pct30', 'pct30_after_promise'])
    for r in trows:
        w.writerow(list(r) + [pct(r[6], r[5]), pct(r[8], r[7]), pct(r[10], r[9]), pct(r[12], r[11])])

# ---------------------------------------------------------------- persist the per-closure measure table (no ids, no addresses) for the summary step
os.makedirs(os.path.join(OUT, 'private'), exist_ok=True)
con.execute(f"""
COPY (SELECT problem_code, division, family, durable, closure_class, cls, kind, kind_from_r1, traceability, record,
             lower(res_text) AS closing_phrase, ward_group, channel_group,
             prior365, d_any, d_res, d_guard, dp, df, w7, w14, w30, wp30, wf, has_addr,
             promise_days,
             epoch(ts_closed - ts_init) / 86400.0 AS days_to_close,
             CASE WHEN ts_promised IS NOT NULL THEN ts_closed <= ts_promised END AS closed_by_promise,
             year(ts_init) AS init_year
      FROM cm) TO '{os.path.join(OUT, 'private', 'closure_measures.parquet')}' (FORMAT PARQUET)
""")

# ---------------------------------------------------------------- absolute count of later reports after hand-off closures
# Each later request is attributed once, to the most recent earlier closure at the same address and type
# (so a report that follows two closures is not counted twice).
abs_rows = con.execute("""
WITH att0 AS (
  -- arg_max over a struct: plain arg_max skips NULL arguments (kind is NULL for non-hand-offs)
  SELECT p.nid, arg_max({'cls': c.cls, 'kind': c.kind, 'd': p.d}, c.ts_closed) AS m, any_value(p.n_channel) AS n_channel
  FROM pairs p JOIN c USING (request_id)
  GROUP BY p.nid),
att AS (SELECT nid, m.cls AS cls, m.kind AS kind, m.d AS d, n_channel FROM att0)
SELECT cls, kind,
       count(*) FILTER (WHERE d <= 14) AS reports14,
       count(*) FILTER (WHERE d <= 30) AS reports30,
       count(*) FILTER (WHERE d <= 14 AND n_channel = 'resident') AS resident_reports14,
       count(*) FILTER (WHERE d <= 30 AND n_channel = 'resident') AS resident_reports30
FROM att GROUP BY ALL ORDER BY 1, 2
""").fetchall()
with open(os.path.join(OUT, 'rereport_absolute_counts.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['class', 'kind', 'later_reports_within14', 'later_reports_within30', 'resident_later_reports_within14',
                'resident_later_reports_within30'])
    for r in abs_rows:
        w.writerow(r)

meta = con.execute("SELECT asof_ts FROM run_asof").fetchone()[0]
json.dump({'asof_ts': str(meta), 'eligible_min_closures': ELIG, 'seconds': round(time.time() - t0, 1)},
          open(os.path.join(OUT, 'rereport_run.json'), 'w'), indent=1)
print('done', round(time.time() - t0, 1), 's', file=sys.stderr)
