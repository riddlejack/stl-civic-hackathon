"""Match-rate diagnostics for the request->parcel join (N1 knock-out test)."""
import os, sys, duckdb
ROOT = os.environ.get('STL_ROOT', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
con = duckdb.connect(os.path.join(ROOT, 'build', 'stl.duckdb'), read_only=True)
q = lambda s: con.execute(s).fetchall()
print('weed codes, request -> parcel, by code and period (all statuses):')
for r in q("""
  SELECT r.problem_code, CASE WHEN r.init_year >= 2025 THEN '2025-26' WHEN r.init_year >= 2021 THEN '2021-24' ELSE '<2021' END AS period,
         count(*) AS n, count(rp.request_id) AS n_matched, round(100.0 * count(rp.request_id) / count(*), 1) pct,
         count(*) FILTER (WHERE r.addr_norm = '' OR r.house_num IS NULL) AS no_house_number
  FROM requests r LEFT JOIN request_parcel rp USING (request_id)
  WHERE r.problem_code IN (SELECT problem_code FROM type_family WHERE family = 'weeds')
  GROUP BY 1, 2 ORDER BY 1, 2"""):
    print('  ', r)
print('method mix, weed ledger codes 2025-26:', q("""SELECT rp.method, count(*) FROM requests r JOIN request_parcel rp USING (request_id)
  WHERE r.problem_code IN (SELECT problem_code FROM weed_ledger_codes) AND r.init_year >= 2025 GROUP BY 1 ORDER BY 2 DESC"""))
print('ledger cut parcels (2025-26) found in MSD PID:', q("""SELECT count(DISTINCT parcel), count(DISTINCT parcel) FILTER (WHERE parcel IN (SELECT pid FROM parcels)),
  count(DISTINCT parcel) FILTER (WHERE parcel IN (SELECT pid FROM parcels) OR parcel IN (SELECT parcel_id FROM lra)) FROM cuts WHERE service_date >= DATE '2025-01-01'"""))
print('all request types with a house number, 2025-26, matched:', q("""SELECT count(*), count(rp.request_id), round(100.0*count(rp.request_id)/count(*),1)
  FROM requests r LEFT JOIN request_parcel rp USING (request_id) WHERE r.init_year >= 2025 AND r.house_num IS NOT NULL"""))
print('unmatched weed-ledger addresses 2025-26, sample:')
for r in q("""SELECT * FROM (SELECT r.addr_raw, r.addr_norm FROM requests r LEFT JOIN request_parcel rp USING (request_id)
  WHERE r.problem_code IN (SELECT problem_code FROM weed_ledger_codes) AND r.init_year >= 2025 AND rp.request_id IS NULL)
  USING SAMPLE 25 ROWS (reservoir, 3)"""):
    print('  ', r)
