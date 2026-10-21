"""E5 step 2: does a stable long tail of never-closed requests exist? Open share by filing year,
overall and for the largest types; closure profile of the admin-leftover candidate types; class
splits that the report needs (strict vs address-only pending; weed cut timing).

Outputs: build/E5/years.json (aggregate only)
Run: .venv/bin/python -I scripts/exec/E5/02_years.py
"""
import json, pathlib
import duckdb

ROOT = pathlib.Path('.')
con = duckdb.connect()
con.execute(f"ATTACH '{ROOT / 'build/stl.duckdb'}' AS s (READ_ONLY)")
con.execute(f"CREATE VIEW l AS SELECT * FROM '{ROOT / 'build/E5/private/ledger_rows.parquet'}'")
R = {}


def q(sql):
    cur = con.execute(sql)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


R['by_year'] = q("""SELECT init_year, count(*) filed,
    count(*) FILTER (WHERE status_group='open') open,
    round(100.0*count(*) FILTER (WHERE status_group='open')/count(*), 2) pct_open,
    count(*) FILTER (WHERE status_group='open' AND ts_promised < '2026-10-13 23:59:59') open_past_promise,
    round(100.0*count(*) FILTER (WHERE status_group='open' AND ts_promised < '2026-10-13 23:59:59')/count(*), 2) pct_open_past_promise,
    count(*) FILTER (WHERE status_group='open' AND ts_promised IS NULL) open_no_promise
  FROM s.requests WHERE init_year BETWEEN 2019 AND 2026 GROUP BY 1 ORDER BY 1""")
# 2026 to date split: filed through June (promise mostly passed) vs later
R['2026_by_half'] = q("""SELECT CASE WHEN init_date < DATE '2026-07-01' THEN '2026 Jan-Jun' ELSE '2026 Jul-Oct 13' END AS period,
    count(*) filed, count(*) FILTER (WHERE status_group='open') open,
    round(100.0*count(*) FILTER (WHERE status_group='open')/count(*), 2) pct_open,
    round(100.0*count(*) FILTER (WHERE status_group='open' AND ts_promised < '2026-10-13 23:59:59')/count(*), 2) pct_open_past_promise
  FROM s.requests WHERE init_year = 2026 GROUP BY 1 ORDER BY 1""")
top = [r[0] for r in con.execute("SELECT problem_code FROM l GROUP BY 1 ORDER BY count(*) DESC LIMIT 25").fetchall()]
R['by_type_year'] = q(f"""SELECT problem_code, init_year, count(*) filed, count(*) FILTER (WHERE status_group='open') open,
    round(100.0*count(*) FILTER (WHERE status_group='open')/count(*), 1) pct_open
  FROM s.requests WHERE init_year BETWEEN 2022 AND 2026 AND problem_code IN (SELECT unnest({top!r}::VARCHAR[]))
  GROUP BY 1, 2 ORDER BY 1, 2""")
R['admin_candidates_closure'] = q("""SELECT problem_code, init_year, count(*) filed,
    count(*) FILTER (WHERE status_group='open') open,
    round(100.0*count(*) FILTER (WHERE status_group='open')/count(*), 1) pct_open,
    median(days_to_close) FILTER (WHERE status_group='closed') median_days_to_close,
    round(100.0*count(*) FILTER (WHERE status_group='closed' AND days_to_close <= 7)/nullif(count(*) FILTER (WHERE status_group='closed'),0), 1) pct_closed_within_7d
  FROM s.requests WHERE init_year BETWEEN 2023 AND 2026
    AND problem_code IN ('NOWATER','Sirens Not Heard','Mosquito Spraying','PRESSURE','WTR-COMING-UP','TDebris-alley/street','Missed Cut - VBldg','Missed Cut - V Lot','Unsatisfy Cut -VBldg','Unsatisfy Cut - VLot')
  GROUP BY 1, 2 ORDER BY 1, 2""")
# pending split: strict = validated against E1 status pages or a non-address record
R['b_split'] = q("""SELECT
    count(*) FILTER (WHERE cls='b_pending_in_records') b_all,
    count(*) FILTER (WHERE cls='b_pending_in_records' AND (b_e1 OR b_bu OR b_demo OR (b_fwo AND problem_code IN ('Inspect City Tree')))) b_strict,
    count(*) FILTER (WHERE cls='b_pending_in_records' AND NOT (b_e1 OR b_bu OR b_demo OR (b_fwo AND problem_code IN ('Inspect City Tree')))) b_address_only
  FROM l""")
R['b_address_only_types'] = q("""SELECT problem_code, count(*) n FROM l WHERE cls='b_pending_in_records'
   AND NOT (b_e1 OR b_bu OR b_demo OR (b_fwo AND problem_code IN ('Inspect City Tree'))) GROUP BY 1 ORDER BY 2 DESC""")
R['a_by_record'] = q("""SELECT CASE WHEN a_weed THEN 'mowing ledger cut' WHEN a_demo THEN 'demolition completed' WHEN a_bu THEN 'board-up done'
      WHEN a_fwo THEN 'Forestry WO finished' WHEN a_swo THEN 'sidewalk WO finished' WHEN a_e1 THEN 'E1 status page finish' END rec,
    count(*) n FROM l WHERE cls='a_done_after_filing' GROUP BY 1 ORDER BY 2 DESC""")
R['a_weed_by_type_timing'] = q("""SELECT problem_code, count(*) n, median(days_to_cut) med_days_to_cut,
    count(*) FILTER (WHERE days_to_cut <= 60) within_60d, count(*) FILTER (WHERE init_year=2025) filed_2025
  FROM l WHERE a_weed GROUP BY 1 ORDER BY 2 DESC""")
R['a_strict_60d'] = q("""SELECT count(*) FILTER (WHERE cls='a_done_after_filing') a_all,
    count(*) FILTER (WHERE cls='a_done_after_filing' AND NOT (a_weed AND days_to_cut > 60 AND NOT (a_fwo OR a_swo OR a_bu OR a_demo OR a_e1))) a_excl_weed_cut_after_60d
  FROM l""")
R['base_by_year'] = q("SELECT init_year, count(*) n, median(days_past_promise) med_days_past FROM l GROUP BY 1 ORDER BY 1")
R['class_by_year'] = q("SELECT init_year, cls, count(*) n FROM l GROUP BY 1, 2 ORDER BY 1, 2")
R['dup_extra_rows'] = q("""SELECT count(*) - count(DISTINCT problem_code || '|' || addr_norm) AS extra_rows_same_code_addr
   FROM l WHERE coalesce(addr_norm,'') <> ''""")
R['blank_addr_norm'] = q("SELECT count(*) n FROM l WHERE coalesce(addr_norm,'') = ''")
R['status_by_class'] = q("SELECT cls, status, count(*) n FROM l GROUP BY 1, 2 ORDER BY 1, 3 DESC")
(ROOT / 'build/E5/years.json').write_text(json.dumps(R, indent=1, default=str))
for k, v in R.items():
    if k in ('by_type_year', 'status_by_class'):
        continue
    print(k)
    for r in v:
        print('  ', r)

# ------------------------------------------------------------------ age-matched comparison
# A cohort filed in year Y, seen on 13 Oct of year Y+1: open then = open now, or closed/cancelled after that date.
# Requests closed later carry ts_closed / ts_cancelled, so the past open state can be rebuilt from this one file.
R['age_matched'] = q("""WITH c AS (
  SELECT init_year, ts_init, ts_promised, status_group, ts_closed, ts_cancelled,
         make_timestamp(init_year + 1, 10, 13, 23, 59, 59) AS asof_then
  FROM s.requests WHERE init_year BETWEEN 2019 AND 2025)
SELECT init_year, count(*) filed,
  count(*) FILTER (WHERE status_group = 'open' OR ts_closed > asof_then OR ts_cancelled > asof_then) open_then,
  round(100.0*count(*) FILTER (WHERE status_group = 'open' OR ts_closed > asof_then OR ts_cancelled > asof_then)/count(*), 2) pct_open_then,
  count(*) FILTER (WHERE (status_group = 'open' OR ts_closed > asof_then OR ts_cancelled > asof_then) AND ts_promised < asof_then) open_past_promise_then,
  round(100.0*count(*) FILTER (WHERE (status_group = 'open' OR ts_closed > asof_then OR ts_cancelled > asof_then) AND ts_promised < asof_then)/count(*), 2) pct_open_past_promise_then,
  count(*) FILTER (WHERE status_group = 'open') open_now,
  round(100.0*count(*) FILTER (WHERE status_group = 'open')/nullif(count(*) FILTER (WHERE status_group = 'open' OR ts_closed > asof_then OR ts_cancelled > asof_then),0), 1) pct_of_then_open_still_open_now,
  count(*) FILTER (WHERE status_group NOT IN ('open','closed','cancelled')) other_status
FROM c GROUP BY 1 ORDER BY 1""")
# types where the city almost never closes requests (2025 filings >= 80% open now)
R['types_rarely_closed'] = q("""SELECT problem_code, count(*) filed_2025, count(*) FILTER (WHERE status_group='open') open_2025,
    round(100.0*count(*) FILTER (WHERE status_group='open')/count(*),1) pct_open_2025,
    (SELECT count(*) FROM l WHERE l.problem_code = r.problem_code) n_in_base
  FROM s.requests r WHERE init_year = 2025 GROUP BY 1
  HAVING count(*) >= 20 AND count(*) FILTER (WHERE status_group='open') >= 0.8*count(*) ORDER BY n_in_base DESC""")
(ROOT / 'build/E5/years.json').write_text(json.dumps(R, indent=1, default=str))
for k in ('age_matched', 'types_rarely_closed'):
    print(k)
    for r in R[k]:
        print('  ', r)
print('by_type_year')
from collections import defaultdict
d = defaultdict(dict)
for r in R['by_type_year']:
    d[r['problem_code']][r['init_year']] = f"{r['open']}/{r['filed']}={r['pct_open']}%"
for k, v in d.items():
    print('  ', k, v)
