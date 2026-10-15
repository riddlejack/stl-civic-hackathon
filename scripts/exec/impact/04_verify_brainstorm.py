"""Verify the counts in research/brainstorm-v6.md Appendix A, and restate the repeat-filing
count with the earlier request closed BEFORE the repeat was filed.

Repeat filing (gross, request-anchored): a request filed in 2025 at the same addr_norm with the
same problem_code as an earlier request filed in the 90 days before it. Variants:
  v0  brainstorm's join (earlier request filed before, any status)        -> expect 20,697
  v1  earlier request CLOSED before the repeat was filed (a.ts_closed < b.ts_init)
  v2  v1, and the earlier request was closed at the hand-off (handed_off/converted)
  v3  v2, durable-fix types only (type_family.durable)
  v4  v1, earlier request closed "done"
Gross counts are NOT the effect of hand-off closing: see 01_rereports.py for the excess over "done".
Reads build/stl.duckdb READ-ONLY. Writes aggregates to build/impact/brainstorm_check.json.
Run: python3 -I scripts/exec/impact/04_verify_brainstorm.py
"""
import json
import os

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
con = duckdb.connect()
con.execute(f"ATTACH '{os.path.join(ROOT, 'build', 'stl.duckdb')}' AS s (READ_ONLY)")
q = lambda sql: con.execute(sql).fetchall()
R = {}
R['filed_2025'] = q("SELECT count(*) FROM s.requests WHERE init_year = 2025")[0][0]
R['closed_2025_by_class'] = q("""SELECT c.closure_class, count(*) FROM s.requests r JOIN s.closure_class c USING (request_id)
    WHERE r.init_year = 2025 AND r.status_group = 'closed' GROUP BY 1 ORDER BY 2 DESC""")
con.execute("""CREATE TEMP TABLE r AS SELECT r.request_id, r.addr_norm, r.problem_code, r.ts_init, r.ts_closed, r.status_group,
    r.channel_group, c.closure_class, coalesce(t.durable, false) AS durable
    FROM s.requests r LEFT JOIN s.closure_class c USING (request_id) LEFT JOIN s.type_family t USING (problem_code)
    WHERE r.addr_norm IS NOT NULL AND r.addr_norm <> ''""")
con.execute("""CREATE TEMP TABLE pr AS SELECT b.request_id AS bid, b.channel_group AS bch, a.request_id AS aid,
    a.ts_closed AS a_closed, a.status_group AS a_status, a.closure_class AS a_cls, a.durable,
    epoch(b.ts_init - a.ts_closed) / 86400.0 AS d_from_close
    FROM r b JOIN r a ON a.addr_norm = b.addr_norm AND a.problem_code = b.problem_code
     AND a.ts_init < b.ts_init AND a.ts_init >= b.ts_init - INTERVAL 90 DAY AND a.request_id <> b.request_id
    WHERE year(b.ts_init) = 2025""")
V = {
    'v0_any_earlier': 'true',
    'v1_earlier_closed_before': "a_status = 'closed' AND a_closed < (SELECT ts_init FROM r WHERE r.request_id = bid)",
}
R['v0_any_earlier'] = q("SELECT count(DISTINCT bid) FROM pr")[0][0]
con.execute("CREATE TEMP TABLE pr1 AS SELECT pr.* FROM pr JOIN r b ON b.request_id = pr.bid WHERE pr.a_status = 'closed' AND pr.a_closed < b.ts_init")
R['v1_earlier_closed_before'] = q("SELECT count(DISTINCT bid) FROM pr1")[0][0]
R['v2_after_handoff_closure'] = q("SELECT count(DISTINCT bid) FROM pr1 WHERE a_cls IN ('handed_off','converted')")[0][0]
R['v2_resident_channel'] = q("SELECT count(DISTINCT bid) FROM pr1 WHERE a_cls IN ('handed_off','converted') AND bch = 'resident'")[0][0]
R['v3_after_handoff_durable'] = q("SELECT count(DISTINCT bid) FROM pr1 WHERE a_cls IN ('handed_off','converted') AND durable")[0][0]
R['v3_resident_channel'] = q("SELECT count(DISTINCT bid) FROM pr1 WHERE a_cls IN ('handed_off','converted') AND durable AND bch = 'resident'")[0][0]
R['v4_after_done_closure'] = q("SELECT count(DISTINCT bid) FROM pr1 WHERE a_cls = 'done'")[0][0]
R['v1_median_days_from_close'] = q("SELECT median(d_from_close) FROM pr1")[0][0]
R['v2_median_days_from_close'] = q("SELECT median(d_from_close) FROM pr1 WHERE a_cls IN ('handed_off','converted')")[0][0]
R['call_csb_closings_2025'] = q("SELECT count(*) FROM s.requests WHERE init_year = 2025 AND lower(resolution) LIKE '%call csb%'")[0][0]
R['call_csb_closings_2025_26'] = q("SELECT count(*) FROM s.requests WHERE ts_init >= TIMESTAMP '2025-01-01' AND lower(resolution) LIKE '%call csb%'")[0][0]
E5 = os.path.join(ROOT, 'build', 'E5', 'private', 'ledger_rows.parquet')
SIX = "('Cave-Ins','TDebris-alley/street','City Tree Down','Broken/Hanging Limb','City Tree Limb Down','Building Collapse')"
R['six_tier1_types_by_class'] = q(f"SELECT problem_code, cls, count(*) FROM '{E5}' WHERE problem_code IN {SIX} GROUP BY 1, 2 ORDER BY 1, 2")
R['six_tier1_total'] = q(f"SELECT count(*) FROM '{E5}' WHERE problem_code IN {SIX}")[0][0]
R['six_tier1_no_done_record'] = q(f"SELECT count(*) FROM '{E5}' WHERE problem_code IN {SIX} AND cls <> 'a_done_after_filing'")[0][0]
R['class_b_pending'] = q(f"SELECT count(*) FROM '{E5}' WHERE cls = 'b_pending_in_records'")[0][0]
R['class_b_by_evidence'] = q(f"""SELECT count(*) FILTER (WHERE b_e1 OR b_bu OR b_demo OR (b_fwo AND type_name = 'Inspect city tree')),
    count(*) FILTER (WHERE problem_code = 'Inspect City Tree') FROM '{E5}' WHERE cls = 'b_pending_in_records'""")[0]
json.dump(R, open(os.path.join(ROOT, 'build', 'impact', 'brainstorm_check.json'), 'w'), indent=1, default=str)
print(json.dumps(R, indent=1, default=str))
