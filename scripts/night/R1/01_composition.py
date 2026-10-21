"""R1 step 1: composition of every 2025-26 hand-off closure (N2 classes handed_off or converted).

One row per REQUESTID (N1's requests table), filed 1 Jan 2025 to 12 Oct 2026, STATUS CLOSED.
Output: build/R1/handoff_composition.csv (type x closing phrase x kind x traceability) and
        build/R1/composition_summary.json (kind x traceability totals).
Run: .venv/bin/python -I scripts/night/R1/01_composition.py
"""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import duckdb
from common import DB, OUT, NEVER_CUTOFF, kind, subkind, trace, q, write_csv

con = duckdb.connect(str(DB), read_only=True)
con.create_function('r1_kind', kind, ['VARCHAR', 'VARCHAR'], 'VARCHAR')
con.create_function('r1_subkind', subkind, ['VARCHAR'], 'VARCHAR')
con.create_function('r1_trace', lambda pc, rk, k: trace(pc, rk, k)[0], ['VARCHAR', 'VARCHAR', 'VARCHAR'], 'VARCHAR')
con.create_function('r1_record', lambda pc, rk, k: trace(pc, rk, k)[1], ['VARCHAR', 'VARCHAR', 'VARCHAR'], 'VARCHAR')
con.create_function('r1_note', lambda pc, rk, k: trace(pc, rk, k)[2], ['VARCHAR', 'VARCHAR', 'VARCHAR'], 'VARCHAR')

con.execute(f"""
CREATE TEMP TABLE h AS
SELECT request_id, problem_code, type_name, division, coalesce(res_key, '') AS phrase, closure_class, class_rule,
       r1_kind(class_rule, res_key) AS kind, r1_subkind(class_rule) AS subkind,
       init_year, ts_init, ts_closed, ts_promised, days_to_close, promise_days, channel_group, ward_group
FROM v_requests
WHERE init_date BETWEEN DATE '2025-01-01' AND DATE '2026-10-12'
  AND status_group = 'closed' AND closure_class IN ('handed_off', 'converted')
""")
con.execute("""
CREATE TEMP TABLE h2 AS
SELECT *, r1_trace(problem_code, phrase, kind) AS traceability, r1_record(problem_code, phrase, kind) AS record,
       r1_note(problem_code, phrase, kind) AS trace_note
FROM h
""")
n = con.execute("SELECT count(*) FROM h2").fetchone()[0]
print('hand-off closures', n)
assert n == 61845, n

# privacy: no phrase may carry an e-mail or a long number
bad = con.execute(r"SELECT count(*) FROM h2 WHERE phrase LIKE '%@%' OR regexp_matches(phrase, '\d{5,}')").fetchone()[0]
assert bad == 0, bad

comp = q(con, f"""
SELECT problem_code, any_value(type_name) AS type_name, mode(division) AS division, phrase AS closing_phrase,
       closure_class, any_value(subkind) AS subkind, kind, traceability, record, any_value(trace_note) AS trace_note,
       count(*) AS n_requests,
       count(*) FILTER (WHERE init_year = 2025) AS n_2025,
       count(*) FILTER (WHERE init_year = 2026) AS n_2026,
       count(*) FILTER (WHERE CAST(ts_promised AS DATE) <= DATE '{NEVER_CUTOFF}') AS n_promise_passed_30d,
       count(*) FILTER (WHERE ts_promised IS NULL) AS n_no_promise,
       round(median(days_to_close), 2) AS median_days_to_close,
       median(promise_days) AS median_promise_days,
       round(avg(CASE WHEN ts_promised IS NOT NULL THEN CAST(ts_closed <= ts_promised AS INT) END), 3) AS share_closed_by_promise,
       count(*) FILTER (WHERE channel_group = 'resident') AS n_resident
FROM h2 GROUP BY problem_code, phrase, closure_class, kind, traceability, record
ORDER BY n_requests DESC
""")
write_csv(OUT / 'handoff_composition.csv', comp)
print('rows', len(comp))

summ = {}
summ['n_handoff_closures'] = n
summ['by_kind'] = q(con, """SELECT kind, count(*) n, round(count(*)/sum(count(*)) over (), 6) AS share FROM h2 GROUP BY 1 ORDER BY 2 DESC""")
summ['by_traceability'] = q(con, """SELECT traceability, count(*) n, round(count(*)/sum(count(*)) over (), 6) AS share FROM h2 GROUP BY 1 ORDER BY 2 DESC""")
summ['by_kind_traceability'] = q(con, """SELECT kind, traceability, count(*) n, round(count(*)/sum(count(*)) over (), 6) AS share FROM h2 GROUP BY 1,2 ORDER BY 3 DESC""")
summ['by_record'] = q(con, """SELECT traceability, record, count(*) n FROM h2 GROUP BY 1,2 ORDER BY 3 DESC""")
summ['by_kind_subkind'] = q(con, """SELECT kind, subkind, count(*) n FROM h2 GROUP BY 1,2 ORDER BY 3 DESC""")
summ['traceable_by_type'] = q(con, """SELECT problem_code, record, phrase, count(*) n FROM h2 WHERE traceability IN ('traceable','partial') GROUP BY 1,2,3 ORDER BY 4 DESC""")
# crew work with no record: the volume R2 extrapolates over
summ['crew_untraceable_top'] = q(con, """SELECT problem_code, phrase, count(*) n FROM h2 WHERE kind='crew_work' AND traceability='none'
    GROUP BY 1,2 ORDER BY 3 DESC LIMIT 25""")
(OUT / 'composition_summary.json').write_text(json.dumps(summ, indent=1, default=str))
for k in ('by_kind', 'by_traceability', 'by_kind_traceability', 'by_record'):
    print(k)
    for r in summ[k]:
        print('  ', r)
print('top crew_work, no record:')
for r in summ['crew_untraceable_top'][:15]:
    print('  ', r)
