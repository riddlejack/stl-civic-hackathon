"""R1 step 3b: kept open vs closed at hand-off, same type, judged by the same completion record.

Weeds (2026 filings; Forestry ledger) and vacant-building board-ups (2025-26; Building Division board-up
layer): outcome shares (done by promise / late / no record) for requests still open on 13 Oct, closed at a
hand-off, closed "no action", and cancelled. Reads build/R1/private/fate_requests.parquet (02_fate.py).
LRA demolition submissions (2025-26; Building Division demolition permits): completed demolition at the
parcel or address after filing, open vs closed or cancelled.

Outputs: build/R1/baseline_open.json, build/R1/baseline_open.csv
Run: .venv/bin/python -I scripts/night/R1/04_baseline_open.py
"""
import json, sys, pathlib, datetime as dt
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'N1'))
import duckdb
from normalise import norm
from common import DB, OUT, PRIV, LAYERS, NEVER_CUTOFF, q, write_csv

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
con.execute(f"""CREATE TEMP TABLE f AS
  SELECT f.*, r.status_group, r.days_to_close, coalesce(rp.is_lra, false) AS is_lra
  FROM '{PRIV / 'fate_requests.parquet'}' f JOIN s.requests r USING (request_id) LEFT JOIN s.request_parcel rp USING (request_id)""")
con.execute("""ALTER TABLE f ADD COLUMN grp VARCHAR""")
con.execute("""UPDATE f SET grp = CASE
   WHEN status_group = 'open' THEN 'still open'
   WHEN status_group = 'cancelled' THEN 'cancelled'
   WHEN closure_class IN ('handed_off', 'converted') AND kind = 'crew_work' THEN 'closed at hand-off (crew work)'
   WHEN closure_class IN ('handed_off', 'converted') THEN 'closed at hand-off (' || kind || ')'
   WHEN closure_class = 'done' THEN 'closed done'
   WHEN closure_class = 'no_action' THEN 'closed no action'
   ELSE 'closed ' || coalesce(closure_class, '?') END""")


def stats(where, label):
    r = q(con, f"""SELECT count(*) AS n_due,
        round(avg(CAST(outcome = 'done_by_promise' AS INT)), 6) AS share_done_by_promise,
        round(avg(CAST(outcome = 'done_late' AS INT)), 6) AS share_done_late,
        round(avg(CAST(outcome = 'no_record' AS INT)), 6) AS share_no_record,
        median(date_diff('day', promised, first_done)) FILTER (WHERE outcome = 'done_late') AS median_days_late,
        median(date_diff('day', init_date, first_done)) FILTER (WHERE first_done IS NOT NULL) AS median_days_to_done
      FROM f WHERE {where} AND promised <= DATE '{NEVER_CUTOFF}' AND outcome IN ('done_by_promise','done_late','no_record')""")[0]
    return {'comparison': label, **r}


rows = []
for svc, where in [('Weeds-Vacant Lot 2026', "rec='weeds' AND problem_code='Weeds-Vacant Lot' AND year(init_date)=2026"),
                   ('Weeds-Vacant Bldg 2026', "rec='weeds' AND problem_code='Weeds-Vacant Bldg' AND year(init_date)=2026"),
                   ('Weeds-Vacant Lot 2026, LRA parcels', "rec='weeds' AND problem_code='Weeds-Vacant Lot' AND year(init_date)=2026 AND is_lra"),
                   ('Weeds-Vacant Lot 2026, other parcels', "rec='weeds' AND problem_code='Weeds-Vacant Lot' AND year(init_date)=2026 AND NOT is_lra"),
                   ('Weeds-Vacant Bldg 2026, LRA parcels', "rec='weeds' AND problem_code='Weeds-Vacant Bldg' AND year(init_date)=2026 AND is_lra"),
                   ('Weeds-Vacant Bldg 2026, other parcels', "rec='weeds' AND problem_code='Weeds-Vacant Bldg' AND year(init_date)=2026 AND NOT is_lra"),
                   ('Vacant building unsecured 2025-26 (board-ups)', "rec='boardup' AND problem_code='Vacnt Bldg Unsecured'")]:
    for g in [x[0] for x in con.execute(f"SELECT DISTINCT grp FROM f WHERE {where} ORDER BY 1").fetchall()]:
        r = stats(f"{where} AND grp = '{g}'", f'{svc} | {g}')
        if r['n_due']:
            rows.append(r)
for r in rows:
    print(f"{r['comparison'][:90]:90s} n={r['n_due']:5d} byP={r['share_done_by_promise']} late={r['share_done_late']} none={r['share_no_record']} medLate={r['median_days_late']}")

# open statuses: which ones, and how old (the confound)
RES = {'by_group': rows}
RES['open_status_mix'] = q(con, f"""SELECT rec, problem_code, status, count(*) n,
     round(avg(CAST(outcome='no_record' AS INT)) FILTER (WHERE promised <= DATE '{NEVER_CUTOFF}' AND outcome IN ('done_by_promise','done_late','no_record')), 3) AS share_no_record_due
   FROM f WHERE status_group='open' AND (year(init_date)=2026 OR rec='boardup') GROUP BY ALL ORDER BY 1,2,4 DESC""")

# ------------------------------------------------------------------ LRA demolition submissions vs demolition permits
feats = json.loads((LAYERS / 'maps8_BUILDING_DIVISION_Demolitions.geojson').read_text())['features']


def utc_date(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date() if isinstance(ms, (int, float)) else None


con.execute("CREATE TEMP TABLE demo (parcel VARCHAR, addr VARCHAR, closed DATE, status VARCHAR, submitted DATE)")
con.executemany("INSERT INTO demo VALUES (?,?,?,?,?)",
                [((p.get('ParcelID') or '').strip() or None, norm(p.get('ADDRESS')) or None, utc_date(p.get('DateClosed')),
                  p.get('PermitStatus'), utc_date(p.get('DateSubmitted'))) for p in (f['properties'] for f in feats)])
con.execute("""CREATE TEMP TABLE lra_demo AS
  SELECT r.request_id, r.status_group, r.status, r.closure_class, r.init_date, CAST(r.ts_promised AS DATE) AS promised, rp.pid, r.addr_norm,
    (SELECT min(d.closed) FROM demo d WHERE ((d.parcel = rp.pid AND rp.pid IS NOT NULL) OR (d.addr = r.addr_norm AND coalesce(r.addr_norm,'') <> ''))
        AND d.status = 'Completed' AND d.closed >= r.init_date) AS demolished
  FROM s.v_requests r LEFT JOIN s.request_parcel rp USING (request_id)
  WHERE r.problem_code = 'LRA Demo Submission' AND r.init_date BETWEEN DATE '2025-01-01' AND DATE '2026-10-12'""")
RES['lra_demolition'] = q(con, f"""SELECT status_group, count(*) n,
     count(*) FILTER (WHERE demolished IS NOT NULL) AS n_demolished_after_filing,
     round(avg(CAST(demolished IS NOT NULL AS INT)), 6) AS share_demolished_after_filing,
     count(*) FILTER (WHERE demolished <= promised) AS n_demolished_by_promise,
     median(date_diff('day', init_date, demolished)) AS median_days_to_demolition,
     count(*) FILTER (WHERE promised <= DATE '{NEVER_CUTOFF}') AS n_promise_passed_30d,
     count(*) FILTER (WHERE promised <= DATE '{NEVER_CUTOFF}' AND demolished IS NULL) AS n_no_record_promise_passed_30d
   FROM lra_demo GROUP BY 1 ORDER BY 1""")
print(RES['lra_demolition'])
write_csv(OUT / 'baseline_open.csv', rows)
(OUT / 'baseline_open.json').write_text(json.dumps(RES, indent=1, default=str))
for r in RES['open_status_mix']:
    print(r)
