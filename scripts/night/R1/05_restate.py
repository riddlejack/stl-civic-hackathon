"""R1 step 4: restate the city's own on-time numbers if hand-offs were not counted as service.

A. CityStat's published 311 measures, rebuilt with N4's definition C (one row per REQUESTID; closed requests
   only; grouped by quarter filed; on time = close date - filed date <= CityStat goal, calendar days;
   whole-block lights: elapsed <= 24 h; parks: the request's own PRJCOMPLETEDATE). For each metric and
   period: CityStat's on-time share (ours, reproduced), the share of on-time closures whose words record a
   hand-off (N2 classes handed_off / converted), and the on-time share counting only closures whose words
   say the work was done (same denominator).
B. Traceable services (from 02_fate.py): share closed by the promised date vs share verifiably done by it.
C. Overall: N4's 57.8% closed by the due date, 19.5% closed by it as done, against R1's verified rate.

Outputs: build/R1/restated_citystat.csv, build/R1/restated.json
Run: .venv/bin/python -I scripts/night/R1/05_restate.py
"""
import json, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import duckdb
from common import DB, OUT, q, write_csv  # R1's common (N4 also has a common.py, so N4 goes last on the path)
sys.path.append(str(HERE.parent / 'N4'))
from citystat_targets import METRICS, QS

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
rows = []
PERIODS = {'2026 Q2 (latest published)': ['2026 Q2'],
           '2025 Q1-2026 Q2 (six published quarters)': ['2025 Q1', '2025 Q2', '2025 Q3', '2025 Q4', '2026 Q1', '2026 Q2'],
           '2026 Q3 (unpublished; our definition)': ['2026 Q3']}
for key, m in METRICS.items():
    codes = m['codes']
    if key == 'whole_block_lights':
        ontime = "epoch(r.ts_closed - r.ts_init) <= 86400"
    elif m['goal_days'] is None:
        ontime = "date_diff('day', r.init_date, CAST(r.ts_closed AS DATE)) <= date_diff('day', r.init_date, CAST(r.ts_promised AS DATE))"
    else:
        ontime = f"date_diff('day', r.init_date, CAST(r.ts_closed AS DATE)) <= {m['goal_days']}"
    for plabel, qs in PERIODS.items():
        qlist = ','.join(f"'{x}'" for x in qs)
        r = q(con, f"""
          WITH c AS (
            SELECT r.request_id, r.closure_class, ({ontime}) AS on_time,
                   (year(r.init_date) || ' Q' || quarter(r.init_date)) AS qf
            FROM s.v_requests r
            WHERE r.problem_code IN ({','.join("'" + c + "'" for c in codes)}) AND r.status_group = 'closed')
          SELECT count(*) AS n_closed,
                 avg(CAST(on_time AS INT)) AS ontime_share,
                 count(*) FILTER (WHERE on_time) AS n_ontime,
                 avg(CAST(closure_class IN ('handed_off','converted') AS INT)) FILTER (WHERE on_time) AS share_of_ontime_handoff,
                 avg(CAST(closure_class = 'done' AS INT)) FILTER (WHERE on_time) AS share_of_ontime_done,
                 avg(CAST(closure_class = 'no_action' AS INT)) FILTER (WHERE on_time) AS share_of_ontime_no_action,
                 avg(CAST(on_time AND closure_class = 'done' AS INT)) AS ontime_done_only_share,
                 avg(CAST(closure_class IN ('handed_off','converted') AS INT)) AS handoff_share_all_closed
          FROM c WHERE qf IN ({qlist})""")[0]
        pub = None
        if len(qs) == 1 and qs[0] in QS:
            pub = m['share'][QS.index(qs[0])]
        elif all(x in QS for x in qs):
            idx = [QS.index(x) for x in qs]
            pub = sum(m['share'][i] * m['n'][i] for i in idx) / sum(m['n'][i] for i in idx)
        rows.append({'metric': key, 'label': m['label'], 'period': plabel, 'citystat_published_share': round(pub, 6) if pub is not None else None,
                     'n_closed': r['n_closed'], 'ontime_share_ours': round(r['ontime_share'] or 0, 6),
                     'share_of_ontime_closures_handoff': round(r['share_of_ontime_handoff'] or 0, 6),
                     'share_of_ontime_closures_done': round(r['share_of_ontime_done'] or 0, 6),
                     'share_of_ontime_closures_no_action': round(r['share_of_ontime_no_action'] or 0, 6),
                     'ontime_share_handoffs_not_counted': round((r['ontime_share'] or 0) * (1 - (r['share_of_ontime_handoff'] or 0)), 6),
                     'ontime_share_counting_only_done': round(r['ontime_done_only_share'] or 0, 6),
                     'handoff_share_of_all_closures': round(r['handoff_share_all_closed'] or 0, 6)})
write_csv(OUT / 'restated_citystat.csv', rows)
for r in rows:
    print(f"{r['metric']:20s} {r['period'][:22]:22s} pub={r['citystat_published_share']} ours={r['ontime_share_ours']} n={r['n_closed']} handoff_of_ontime={r['share_of_ontime_closures_handoff']} done_only={r['ontime_share_counting_only_done']}")

# B. traceable services from 02_fate.py
fate = json.loads((OUT / 'fate_summary.json').read_text())
trace_rows = []
for r in fate['by_service'][:5] + [fate['headline']]:
    trace_rows.append({'service': r['service'], 'n': r['n_due'], 'closed_by_promise_311': r['share_closed_by_promise'],
                       'verified_done_by_promise': r['share_done_by_promise'],
                       'verified_done_by_promise_plus7d': r['share_done_by_promise_plus7'],
                       'verified_done_late': r['share_done_late'], 'no_record': r['share_no_record']})
out = {'citystat': rows, 'traceable': trace_rows,
       'overall': {'n4_closed_by_due_date': 0.578, 'n4_closed_by_due_date_n': 170719, 'n4_closed_by_due_date_as_done': 0.195,
                   'r1_traceable_closed_by_promise': fate['headline']['share_closed_by_promise'],
                   'r1_traceable_verified_done_by_promise': fate['headline']['share_done_by_promise'],
                   'r1_traceable_verified_done_by_promise_plus7d': fate['headline']['share_done_by_promise_plus7'],
                   'r1_traceable_n': fate['headline']['n_due']}}
(OUT / 'restated.json').write_text(json.dumps(out, indent=1, default=str))
for r in trace_rows:
    print(r)
