"""R1 checks behind the headline: the funnel from all traceable hand-offs to the graded set, board-up
recording lag (positive control), distinct parcels behind "no record", and the 2025 tree conversions.

Reads build/R1/private/fate_requests.parquet (02_fate.py) and build/stl.duckdb (read-only).
Output: build/R1/checks.json
Run: .venv/bin/python -I scripts/night/R1/06_checks.py
"""
import json, sys, pathlib, datetime as dt
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'N1'))
import duckdb
from normalise import norm
from common import DB, OUT, PRIV, LAYERS, NEVER_CUTOFF, q

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
con.execute(f"""CREATE TEMP TABLE f AS SELECT f.*, r.status_group, r.ts_closed, rp.pid
                FROM '{PRIV / 'fate_requests.parquet'}' f JOIN s.requests r USING (request_id)
                LEFT JOIN s.request_parcel rp USING (request_id)""")
C = {}
HAND = "status_group='closed' AND closure_class IN ('handed_off','converted') AND kind='crew_work'"
# funnel: weeds
C['funnel_weeds'] = q(con, f"""SELECT
   count(*) AS handoffs_2025_26,
   count(*) FILTER (WHERE year(init_date)=2025) AS dropped_2025_ledger,
   count(*) FILTER (WHERE year(init_date)=2026) AS filed_2026,
   count(*) FILTER (WHERE year(init_date)=2026 AND outcome='unmatched') AS dropped_no_parcel,
   count(*) FILTER (WHERE year(init_date)=2026 AND outcome='no_promise') AS dropped_no_promise,
   count(*) FILTER (WHERE year(init_date)=2026 AND outcome IN ('done_by_promise','done_late','pending') AND promised > DATE '{NEVER_CUTOFF}') AS dropped_promise_after_cutoff,
   count(*) FILTER (WHERE year(init_date)=2026 AND promised <= DATE '{NEVER_CUTOFF}' AND outcome IN ('done_by_promise','done_late','no_record')) AS graded
   FROM f WHERE rec='weeds' AND {HAND}""")[0]
C['funnel_boardups'] = q(con, f"""SELECT count(*) AS handoffs_2025_26,
   count(*) FILTER (WHERE outcome='no_promise') AS dropped_no_promise,
   count(*) FILTER (WHERE promised > DATE '{NEVER_CUTOFF}') AS dropped_promise_after_cutoff,
   count(*) FILTER (WHERE promised <= DATE '{NEVER_CUTOFF}' AND outcome IN ('done_by_promise','done_late','no_record')) AS graded
   FROM f WHERE rec='boardup' AND status_group='closed' AND phrase='referred to board up crew'""")[0]
# distinct parcels behind no-record weeds (2026)
C['weeds_no_record_parcels'] = q(con, f"""SELECT problem_code, count(*) n_requests, count(DISTINCT pid) n_parcels
   FROM f WHERE rec='weeds' AND {HAND} AND year(init_date)=2026 AND outcome='no_record' GROUP BY 1 ORDER BY 1""")

# board-up recording lag: requests the city closed as done ("secured by city") -> layer date vs 311 close
feats = json.loads((LAYERS / 'maps8_BUILDING_DIVISION_Boardups.geojson').read_text())['features']
def utc_date(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date() if isinstance(ms, (int, float)) else None
con.execute("CREATE TEMP TABLE b (parcel VARCHAR, addr VARCHAR, boarded DATE, created DATE)")
con.executemany("INSERT INTO b VALUES (?,?,?,?)", [((p.get('ParcelID') or '').strip() or None, norm(p.get('ADDRESS')) or None,
                 utc_date(p.get('DateBoardedUp')), utc_date(p.get('DateCreated'))) for p in (x['properties'] for x in feats)])
C['boardup_lag_done_closures'] = q(con, """
  WITH d AS (SELECT r.request_id, r.init_date, CAST(r.ts_closed AS DATE) AS closed, rp.pid, r.addr_norm, r.res_key
             FROM s.v_requests r LEFT JOIN s.request_parcel rp USING (request_id)
             WHERE r.problem_code='Vacnt Bldg Unsecured' AND r.closure_class='done' AND r.init_date >= DATE '2024-01-01'),
  m AS (SELECT d.request_id, min(b.boarded) AS boarded, min(b.created) AS created FROM d JOIN b
          ON ((b.parcel=d.pid AND d.pid IS NOT NULL) OR (b.addr=d.addr_norm AND coalesce(d.addr_norm,'')<>''))
         AND b.boarded >= d.init_date GROUP BY 1)
  SELECT d.res_key, count(*) n, count(m.boarded) n_with_record,
         median(date_diff('day', d.closed, m.boarded)) AS median_days_boarded_minus_311_close,
         quantile_cont(date_diff('day', d.closed, m.boarded), 0.25) AS q1, quantile_cont(date_diff('day', d.closed, m.boarded), 0.75) AS q3,
         avg(CAST(m.boarded <= d.closed AS INT)) FILTER (WHERE m.boarded IS NOT NULL) AS share_boarded_on_or_before_close,
         median(date_diff('day', d.closed, m.created)) AS median_days_created_minus_311_close
  FROM d LEFT JOIN m USING (request_id) GROUP BY 1 ORDER BY 2 DESC""")
# referred: days from board-up order creation to boarded date (the crew's own queue time)
C['boardup_referred_queue'] = q(con, """
  WITH d AS (SELECT r.request_id, r.init_date, r.ts_closed, CAST(r.ts_promised AS DATE) AS promised, rp.pid, r.addr_norm
             FROM s.v_requests r LEFT JOIN s.request_parcel rp USING (request_id)
             WHERE r.res_key='referred to board up crew' AND r.status_group='closed' AND r.init_date BETWEEN DATE '2025-01-01' AND DATE '2026-10-12'),
  m AS (SELECT d.request_id, min(b.created) AS created FROM d JOIN b
          ON ((b.parcel=d.pid AND d.pid IS NOT NULL) OR (b.addr=d.addr_norm AND coalesce(d.addr_norm,'')<>''))
         AND b.created >= d.init_date - 1 GROUP BY 1),
  m2 AS (SELECT d.request_id, m.created,
           (SELECT min(b.boarded) FROM b WHERE ((b.parcel=d.pid AND d.pid IS NOT NULL) OR (b.addr=d.addr_norm AND coalesce(d.addr_norm,'')<>''))
                 AND b.created = m.created) AS boarded_same_order
         FROM d JOIN m USING (request_id))
  SELECT count(*) n_orders, count(boarded_same_order) n_order_boarded,
         median(date_diff('day', created, boarded_same_order)) AS median_days_order_to_boarded,
         avg(CAST(boarded_same_order IS NULL AS INT)) AS share_order_without_boarded_date
  FROM m2""")
print(json.dumps(C, indent=1, default=str))
(OUT / 'checks.json').write_text(json.dumps(C, indent=1, default=str))

# is "no record" a join failure? Do the no-record parcels appear in the ledger in any year?
con.execute("""CREATE TEMP TABLE lp AS SELECT parcel, max(CAST(year(service_date)=2024 AS INT)) AS cut2024,
               max(CAST(year(service_date)=2026 AS INT)) AS cut2026 FROM s.ledger GROUP BY parcel""")
C['weeds_outcome_vs_ledger_history'] = q(con, f"""SELECT f.problem_code, f.outcome, count(*) n,
    round(avg(CAST(lp.parcel IS NOT NULL AS INT)), 3) AS share_parcel_ever_in_ledger_1995_2026,
    round(avg(coalesce(lp.cut2024, 0)), 3) AS share_parcel_cut_2024,
    round(avg(coalesce(lp.cut2026, 0)), 3) AS share_parcel_any_2026_ledger_row
  FROM f LEFT JOIN lp ON lp.parcel = f.pid
  WHERE f.rec='weeds' AND {HAND} AND year(f.init_date)=2026 AND f.promised <= DATE '{NEVER_CUTOFF}'
    AND f.outcome IN ('done_by_promise','done_late','no_record') GROUP BY ALL ORDER BY 1, 2""")
for r in C['weeds_outcome_vs_ledger_history']:
    print(r)
(OUT / 'checks.json').write_text(json.dumps(C, indent=1, default=str))

# --- robustness of the headline
# (a) does "no record" shrink when the promise is older? (if late work were merely unposted, it would)
C['no_record_by_promise_age'] = q(con, f"""SELECT rec,
    CASE WHEN promised <= DATE '2026-07-13' THEN 'promise <= 13 Jul (>=92 d before 13 Oct)'
         WHEN promised <= DATE '2026-08-13' THEN 'promise 14 Jul-13 Aug (61-91 d)'
         ELSE 'promise 14 Aug-13 Sep (30-60 d)' END AS promise_age,
    count(*) n, round(avg(CAST(outcome='no_record' AS INT)), 6) AS share_no_record,
    round(avg(CAST(outcome='done_by_promise' AS INT)), 6) AS share_done_by_promise
  FROM f WHERE outcome IN ('done_by_promise','done_late','no_record') AND promised <= DATE '{NEVER_CUTOFF}'
    AND ((rec='weeds' AND {HAND} AND year(init_date)=2026) OR (rec='boardup' AND status_group='closed' AND phrase='referred to board up crew'))
  GROUP BY 1, 2 ORDER BY 1, 2""")
# (b) one unit per parcel: first 2026 weed hand-off per parcel
C['weeds_first_request_per_parcel'] = q(con, f"""WITH x AS (SELECT *, row_number() OVER (PARTITION BY pid ORDER BY init_date, request_id) rn
     FROM f WHERE rec='weeds' AND {HAND} AND year(init_date)=2026 AND promised <= DATE '{NEVER_CUTOFF}'
       AND outcome IN ('done_by_promise','done_late','no_record'))
   SELECT count(*) n_parcels, round(avg(CAST(outcome='done_by_promise' AS INT)), 6) by_promise,
          round(avg(CAST(outcome='done_late' AS INT)), 6) late, round(avg(CAST(outcome='no_record' AS INT)), 6) no_record
   FROM x WHERE rn = 1""")
# (c) weeds filed within 14 days after a cut (a just-cut lot may not be due again)
con.execute("CREATE TEMP TABLE rl AS SELECT request_id, last_cut_before FROM s.request_ledger")
C['weeds_recent_cut_before_filing'] = q(con, f"""SELECT (rl.last_cut_before >= f.init_date - 14) AS cut_in_14d_before, count(*) n,
     round(avg(CAST(outcome='done_by_promise' AS INT)), 6) by_promise, round(avg(CAST(outcome='done_late' AS INT)), 6) late,
     round(avg(CAST(outcome='no_record' AS INT)), 6) no_record
   FROM f JOIN rl USING (request_id) WHERE rec='weeds' AND {HAND} AND year(init_date)=2026 AND promised <= DATE '{NEVER_CUTOFF}'
     AND outcome IN ('done_by_promise','done_late','no_record') GROUP BY 1 ORDER BY 1""")
# (d) board-up no-record: is the building in the layer at all (any date)?
con.execute("""CREATE TEMP TABLE bkeys AS SELECT DISTINCT parcel AS k FROM b WHERE parcel IS NOT NULL UNION SELECT DISTINCT addr FROM b WHERE addr IS NOT NULL""")
C['boardup_no_record_in_layer'] = q(con, f"""SELECT outcome, count(*) n,
     round(avg(CAST((f.pid IN (SELECT k FROM bkeys)) OR (r.addr_norm IN (SELECT k FROM bkeys)) AS INT)), 6) AS share_building_in_layer_any_date
   FROM f JOIN s.requests r USING (request_id)
   WHERE rec='boardup' AND f.status_group='closed' AND phrase='referred to board up crew' AND promised <= DATE '{NEVER_CUTOFF}'
     AND outcome IN ('done_by_promise','done_late','no_record') GROUP BY 1 ORDER BY 1""")
# (e) LRA lots only (city-owned: nobody else should cut them)
for k in ('no_record_by_promise_age', 'weeds_first_request_per_parcel', 'weeds_recent_cut_before_filing', 'boardup_no_record_in_layer'):
    print(k)
    for r in (C[k] if isinstance(C[k], list) else [C[k]]):
        print('  ', r)
(OUT / 'checks.json').write_text(json.dumps(C, indent=1, default=str))

# resident impact: distinct places behind "no record"
C['no_record_distinct_places'] = q(con, f"""SELECT rec, count(*) n_requests, count(DISTINCT coalesce(f.pid, r.addr_norm)) n_places
   FROM f JOIN s.requests r USING (request_id)
   WHERE f.outcome='no_record' AND f.promised <= DATE '{NEVER_CUTOFF}'
     AND ((rec='weeds' AND f.status_group='closed' AND f.closure_class IN ('handed_off','converted') AND kind='crew_work' AND year(f.init_date)=2026)
          OR (rec='boardup' AND f.status_group='closed' AND phrase='referred to board up crew'))
   GROUP BY 1 ORDER BY 1""")
print(C['no_record_distinct_places'])
(OUT / 'checks.json').write_text(json.dumps(C, indent=1, default=str))

# match method behind graded weed hand-offs (is "no record" a fuzzy-join artefact?)
C['weeds_match_method'] = q(con, f"""SELECT rp.method, count(*) n, round(avg(CAST(f.outcome='no_record' AS INT)), 6) AS share_no_record
   FROM f JOIN s.request_parcel rp USING (request_id)
   WHERE f.rec='weeds' AND f.status_group='closed' AND f.closure_class IN ('handed_off','converted') AND f.kind='crew_work'
     AND year(f.init_date)=2026 AND f.promised <= DATE '{NEVER_CUTOFF}' AND f.outcome IN ('done_by_promise','done_late','no_record')
     AND f.problem_code IN ('Weeds-Vacant Lot','Weeds-Vacant Bldg') GROUP BY 1 ORDER BY 2 DESC""")
# stability: board-up fate by filing year; weeds by filing quarter
C['boardup_by_year'] = q(con, f"""SELECT year(init_date) AS y, count(*) n,
     round(avg(CAST(outcome='done_by_promise' AS INT)), 6) by_promise, round(avg(CAST(outcome='done_late' AS INT)), 6) late,
     round(avg(CAST(outcome='no_record' AS INT)), 6) no_record, median(date_diff('day', promised, first_done)) FILTER (WHERE outcome='done_late') AS median_days_late
   FROM f WHERE rec='boardup' AND status_group='closed' AND phrase='referred to board up crew' AND promised <= DATE '{NEVER_CUTOFF}'
     AND outcome IN ('done_by_promise','done_late','no_record') GROUP BY 1 ORDER BY 1""")
# how long the no-record requests have waited so far (filing to 13 Oct)
C['no_record_wait_so_far'] = q(con, f"""SELECT rec, count(*) n, median(date_diff('day', init_date, DATE '2026-10-13')) AS median_days_since_filing,
     median(date_diff('day', promised, DATE '2026-10-13')) AS median_days_past_promise
   FROM f WHERE outcome='no_record' AND promised <= DATE '{NEVER_CUTOFF}'
     AND ((rec='weeds' AND status_group='closed' AND closure_class IN ('handed_off','converted') AND kind='crew_work' AND year(init_date)=2026)
          OR (rec='boardup' AND status_group='closed' AND phrase='referred to board up crew'))
   GROUP BY 1 ORDER BY 1""")
for k in ('weeds_match_method', 'boardup_by_year', 'no_record_wait_so_far'):
    print(k)
    for r in C[k]:
        print('  ', r)
(OUT / 'checks.json').write_text(json.dumps(C, indent=1, default=str))

# ledger coverage of the land bank: share of LRA parcels with at least one cut billed in 2026
C['lra_ledger_coverage_2026'] = q(con, """SELECT l.property_type, count(*) n,
     round(avg(CAST(c.parcel IS NOT NULL AS INT)), 6) AS share_with_2026_cut
   FROM s.lra l LEFT JOIN (SELECT DISTINCT parcel FROM s.cuts WHERE year(service_date) = 2026) c ON c.parcel = l.parcel_id
   GROUP BY 1 ORDER BY 2 DESC""")
print(C['lra_ledger_coverage_2026'])
(OUT / 'checks.json').write_text(json.dumps(C, indent=1, default=str))
