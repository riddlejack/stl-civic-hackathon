"""E5 step 3: (1) half-year age-matched comparison for the 2026 part of the base;
(2) do requests that close more than a year after filing close in batches (a clerical signature)?
Outputs: build/E5/late_closures.json (aggregate only)
Run: .venv/bin/python -I scripts/exec/E5/03_late_closures.py
"""
import json, pathlib
import duckdb
ROOT = pathlib.Path('/Users/jackriddle/Desktop/stl-civic-hackathon')
con = duckdb.connect()
con.execute(f"ATTACH '{ROOT / 'build/stl.duckdb'}' AS s (READ_ONLY)")
def q(sql):
    cur = con.execute(sql); cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]
R = {}
# Jan-Jun filings of year Y, seen on 13 Oct of the same year Y
R['h1_age_matched'] = q("""WITH c AS (SELECT init_year, ts_promised, status_group, ts_closed, ts_cancelled,
      make_timestamp(init_year, 10, 13, 23, 59, 59) AS asof_then FROM s.requests
      WHERE init_year BETWEEN 2019 AND 2026 AND month(init_date) <= 6)
  SELECT init_year, count(*) filed,
   round(100.0*count(*) FILTER (WHERE (status_group='open' OR ts_closed > asof_then OR ts_cancelled > asof_then) AND ts_promised < asof_then)/count(*), 2) pct_open_past_promise_then
  FROM c GROUP BY 1 ORDER BY 1""")
# late closures: closed > 365 days after filing, filed 2019-2024
con.execute("""CREATE TEMP TABLE late AS SELECT request_id, problem_code, CAST(ts_closed AS DATE) d, res_key, init_year
  FROM s.requests WHERE status_group='closed' AND init_year BETWEEN 2019 AND 2024 AND days_to_close > 365""")
R['late_n'] = q("SELECT count(*) n, count(DISTINCT d) n_days FROM late")
R['late_top_days'] = q("""SELECT d, count(*) n, count(DISTINCT problem_code) n_types, mode(res_key) top_phrase
  FROM late GROUP BY 1 ORDER BY 2 DESC LIMIT 12""")
R['late_share_on_top10_days'] = q("""WITH t AS (SELECT d, count(*) n FROM late GROUP BY 1 ORDER BY 2 DESC LIMIT 10)
  SELECT (SELECT sum(n) FROM t) top10, (SELECT count(*) FROM late) total,
         round(100.0*(SELECT sum(n) FROM t)/(SELECT count(*) FROM late),1) pct""")
R['late_share_on_days_with_100plus'] = q("""WITH t AS (SELECT d, count(*) n FROM late GROUP BY 1 HAVING count(*) >= 100)
  SELECT count(*) n_days, sum(n) n_req, round(100.0*sum(n)/(SELECT count(*) FROM late),1) pct FROM t""")
R['late_top_phrases'] = q("SELECT res_key, count(*) n FROM late GROUP BY 1 ORDER BY 2 DESC LIMIT 10")
(ROOT / 'build/E5/late_closures.json').write_text(json.dumps(R, indent=1, default=str))
for k, v in R.items():
    print(k)
    for r in v: print('  ', r)
