"""E5: evidence ledger over the open, past-promise 311 requests filed since 1 Jan 2025.

Base (the headline 14,902): requests WHERE ts_init >= '2025-01-01' AND status_group = 'open'
AND ts_promised < '2026-10-13 23:59:59' in build/stl.duckdb (data as of 13 Oct 2026).

Every record used is already on disk; nothing is fetched.
  weeds      Forestry billing ledger via request_ledger_flags (N1 parcel join; R1 method)
  forestry   27 Forestry Work Order saved searches, deduplicated (same loader as
             research/cityworks-gap-scripts/forestry_analysis.py); exact N1-normalised address,
             work order initiated no earlier than one day before filing
  sidewalk   Cityworks QE layer 78 (closed sidewalk work orders; all rows CLOSED), exact address
  boardup    Building Division board-up layer, parcel or normalised address (R1 method)
  demolition Building Division demolition permits, parcel or normalised address (R1 method)
  e1         E1 status-page reads (build/E1/private/linked_requests.csv), per request
  dup        a later request at the same normalised address and problem code that is now closed

Classes, mutually exclusive, first match wins:
  a done_after_filing  an independent record shows the work done on or after filing
  b pending_in_records a city work record created after filing is still open / has no finish
  c possibly_superseded a later request, same address and code, is closed
  d admin_leftover     time-bound service far past promise (inferred; rule below)
  e no_evidence

Outputs (aggregate only, no ids): build/E5/ledger_by_type.csv, build/E5/summary.json
Private row-level: build/E5/private/ledger_rows.parquet
Run: .venv/bin/python -I scripts/exec/E5/01_ledger.py
"""
import csv, json, sys, pathlib, datetime as dt
from collections import defaultdict
from zoneinfo import ZoneInfo

ROOT = pathlib.Path('.')
sys.path.insert(0, str(ROOT / 'scripts/night/N1'))
import duckdb
from normalise import norm

DB = ROOT / 'build/stl.duckdb'
OUT = ROOT / 'build/E5'
PRIV = OUT / 'private'
RAW = ROOT / 'data/raw/cityworks-gap/extracts'
LAYERS = ROOT / 'data/raw/city-services/arcgis/layers'
TZ = ZoneInfo('America/Chicago')
ASOF = dt.date(2026, 10, 13)
FORESTRY_LAYERS = [63, 64, 75, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
                   100, 101, 102, 103, 104, 105, 107, 108, 109, 124, 125, 126, 127]
TREE = ('Inspect City Tree', 'City Tree Down', 'City Tree Limb Down', 'Stump Removal', 'Broken/Hanging Limb',
        'Inspect Private Tree', 'LRA Tree', 'Tree Planting requst')
BOARDUP = ('Vacnt Bldg Unsecured', 'LRA Board up')
DEMO = ('LRA Demo Submission', 'Building Collapse')
# d: services whose condition is time-bound, so a wait of 90+ days past promise is implausible
# as a live job (inferred judgement, stated in the report).
ADMIN = {'NOWATER': 'household has no water', 'Sirens Not Heard': 'siren not heard in a monthly test',
         'Mosquito Spraying': 'seasonal spraying request'}
ADMIN_MIN_DAYS_PAST = 90


def local_dt(v):
    if not isinstance(v, (int, float)):
        return None
    try:
        return dt.datetime.fromtimestamp(v / 1000, dt.timezone.utc).astimezone(TZ).replace(tzinfo=None)
    except (OverflowError, OSError, ValueError):
        return None


def utc_date(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date() if isinstance(ms, (int, float)) else None


def utc_ts(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).replace(tzinfo=None) if isinstance(ms, (int, float)) else None


con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
con.execute("""CREATE TABLE base AS
SELECT r.request_id, r.problem_code, r.type_name, r.status, r.init_date, r.init_year, r.ts_init, r.ts_promised,
       r.addr_norm, rp.pid,
       date_diff('day', CAST(r.ts_promised AS DATE), DATE '2026-10-13') AS days_past_promise
FROM s.requests r LEFT JOIN s.request_parcel rp USING (request_id)
WHERE r.ts_init >= '2025-01-01' AND r.status_group = 'open' AND r.ts_promised < '2026-10-13 23:59:59'""")
N = con.execute("SELECT count(*) FROM base").fetchone()[0]
assert N == 14902, N
assert con.execute("SELECT count(*) - count(DISTINCT request_id) FROM base").fetchone()[0] == 0
S = {'n_base': N, 'asof': str(ASOF)}

# ------------------------------------------------------------------ weeds: Forestry ledger
con.execute("""CREATE TABLE ev_weed AS
SELECT b.request_id, f.first_cut_after, f.last_cut_before, f.ledger_max,
       date_diff('day', b.init_date, f.first_cut_after) AS days_to_cut
FROM base b JOIN s.request_ledger_flags f USING (request_id)""")
S['weed_ledger'] = con.execute("""SELECT count(*) n_joined, count(first_cut_after) n_cut_after,
   count(*) FILTER (WHERE first_cut_after < (SELECT init_date FROM base WHERE base.request_id = ev_weed.request_id)) n_cut_after_before_init,
   max(ledger_max) ledger_max FROM ev_weed""").fetchone()

# ------------------------------------------------------------------ Forestry work-order union
members = {}
for layer in FORESTRY_LAYERS:
    for row in json.loads((RAW / f'layer_{layer}_rows.json').read_text()):
        members.setdefault(int(row['WorkOrderSid']), row)
con.execute("CREATE TABLE fwo (sid BIGINT, status VARCHAR, init TIMESTAMP, finish TIMESTAMP, closed TIMESTAMP, addr VARCHAR)")
con.executemany("INSERT INTO fwo VALUES (?,?,?,?,?,?)",
                [(sid, r.get('Status'), local_dt(r.get('InitiateDate')), local_dt(r.get('ActualFinishDate')),
                  local_dt(r.get('DateWOClosed')), norm(r.get('WOAddress'))) for sid, r in members.items()])
S['forestry_union_unique_wo'] = len(members)
tree_sql = ','.join("'" + x.replace("'", "''") + "'" for x in TREE)
con.execute(f"""CREATE TABLE ev_fwo AS
SELECT b.request_id,
  min(w.finish) FILTER (WHERE w.finish >= b.ts_init AND w.finish::DATE <= DATE '2026-10-13' AND w.finish >= w.init) AS finish_after,
  count(*) FILTER (WHERE w.status <> 'CLOSED' AND w.finish IS NULL) AS n_open_after,
  count(*) FILTER (WHERE w.status = 'CLOSED' AND w.finish IS NULL) AS n_closed_nofinish,
  count(*) AS n_wo_after
FROM base b JOIN fwo w ON b.addr_norm <> '' AND w.addr = b.addr_norm AND w.init >= b.ts_init - INTERVAL 1 DAY
WHERE b.problem_code IN ({tree_sql}) GROUP BY 1""")
con.execute(f"""CREATE TABLE ev_fwo_before AS
SELECT b.request_id, count(*) n_before, count(*) FILTER (WHERE w.status <> 'CLOSED') n_open_before
FROM base b JOIN fwo w ON b.addr_norm <> '' AND w.addr = b.addr_norm AND w.init < b.ts_init - INTERVAL 1 DAY
WHERE b.problem_code IN ({tree_sql}) GROUP BY 1""")

# ------------------------------------------------------------------ sidewalk layer 78 (all CLOSED)
rows78 = json.loads((RAW / 'layer_78_rows.json').read_text())
con.execute("CREATE TABLE swo (sid BIGINT, status VARCHAR, init TIMESTAMP, finish TIMESTAMP, addr VARCHAR)")
con.executemany("INSERT INTO swo VALUES (?,?,?,?,?)",
                [(int(r['WorkOrderSid']), r.get('Status'), local_dt(r.get('InitiateDate')), local_dt(r.get('ActualFinishDate')),
                  norm(r.get('WOAddress'))) for r in rows78])
con.execute("""CREATE TABLE ev_swo AS
SELECT b.request_id, min(w.finish) AS finish_after
FROM base b JOIN swo w ON b.addr_norm <> '' AND w.addr = b.addr_norm
WHERE b.problem_code = 'Sidewalk Repair' AND w.finish::DATE >= b.init_date AND w.finish::DATE <= DATE '2026-10-13'
GROUP BY 1""")
S['sidewalk_layer78'] = {'rows': len(rows78), 'statuses': sorted({r.get('Status') for r in rows78})}

# ------------------------------------------------------------------ board-ups (R1 method)
feats = json.loads((LAYERS / 'maps8_BUILDING_DIVISION_Boardups.geojson').read_text())['features']
con.execute("CREATE TABLE boardup (parcel VARCHAR, addr VARCHAR, created_utc TIMESTAMP, boarded DATE)")
con.executemany("INSERT INTO boardup VALUES (?,?,?,?)",
                [((p.get('ParcelID') or '').strip() or None, norm(p.get('ADDRESS')) or None,
                  utc_ts(p.get('DateCreated')), utc_date(p.get('DateBoardedUp'))) for p in (f['properties'] for f in feats)])
bu_sql = ','.join(f"'{x}'" for x in BOARDUP)
con.execute(f"""CREATE TABLE ev_bu AS
SELECT b.request_id,
  min(u.boarded) FILTER (WHERE u.boarded >= b.init_date) AS boarded_after,
  count(*) FILTER (WHERE u.boarded IS NULL AND u.created_utc >= b.ts_init - INTERVAL 1 DAY) AS n_created_after_unboarded
FROM base b JOIN boardup u ON (u.parcel = b.pid AND b.pid IS NOT NULL) OR (u.addr = b.addr_norm AND coalesce(b.addr_norm,'') <> '')
WHERE b.problem_code IN ({bu_sql}) GROUP BY 1""")

# ------------------------------------------------------------------ demolition permits (R1 method)
feats = json.loads((LAYERS / 'maps8_BUILDING_DIVISION_Demolitions.geojson').read_text())['features']
con.execute("CREATE TABLE demo (parcel VARCHAR, addr VARCHAR, closed DATE, status VARCHAR, submitted DATE)")
con.executemany("INSERT INTO demo VALUES (?,?,?,?,?)",
                [((p.get('ParcelID') or '').strip() or None, norm(p.get('ADDRESS')) or None, utc_date(p.get('DateClosed')),
                  p.get('PermitStatus'), utc_date(p.get('DateSubmitted'))) for p in (f['properties'] for f in feats)])
demo_sql = ','.join(f"'{x}'" for x in DEMO)
con.execute(f"""CREATE TABLE ev_demo AS
SELECT b.request_id,
  min(d.closed) FILTER (WHERE d.status = 'Completed' AND d.closed >= b.init_date) AS demolished_after,
  min(d.closed) FILTER (WHERE d.status = 'Completed' AND d.closed < b.init_date) AS demolished_before,
  count(*) FILTER (WHERE d.status <> 'Completed' AND d.submitted >= b.init_date) AS n_permit_pending_after
FROM base b JOIN demo d ON (d.parcel = b.pid AND b.pid IS NOT NULL) OR (d.addr = b.addr_norm AND coalesce(b.addr_norm,'') <> '')
WHERE b.problem_code IN ({demo_sql}) GROUP BY 1""")

# ------------------------------------------------------------------ E1 status-page reads (per request)
e1 = list(csv.DictReader(open(ROOT / 'build/E1/private/linked_requests.csv')))
con.execute("CREATE TABLE e1 (request_id BIGINT, stratum VARCHAR, grade VARCHAR, n_wo_post INT)")
con.executemany("INSERT INTO e1 VALUES (?,?,?,?)",
                [(int(r['request_id']), r['stratum'], r['grade'], int(r['n_wo_post'] or 0)) for r in e1])
e1s = list(csv.DictReader(open(ROOT / 'build/E1/private/sample.csv')))
con.execute("CREATE TABLE e1_sample (request_id BIGINT, stratum VARCHAR)")
con.executemany("INSERT INTO e1_sample VALUES (?,?)", [(int(r['request_id']), r['stratum']) for r in e1s])
S['e1_sampled_in_base'] = con.execute("SELECT count(*) FROM e1_sample JOIN base USING (request_id)").fetchone()[0]
S['e1_linked_in_base'] = con.execute("SELECT count(*) FROM e1 JOIN base USING (request_id)").fetchone()[0]

# ------------------------------------------------------------------ duplicates: later request, same address + code
con.execute("""CREATE TABLE ev_dup AS
SELECT b.request_id,
  count(*) AS n_later,
  count(*) FILTER (WHERE r.status_group = 'closed') AS n_later_closed,
  min(r.ts_closed) FILTER (WHERE r.status_group = 'closed') AS first_later_closed
FROM base b JOIN s.requests r ON r.problem_code = b.problem_code AND r.addr_norm = b.addr_norm AND coalesce(b.addr_norm,'') <> ''
  AND r.ts_init > b.ts_init AND r.request_id <> b.request_id
GROUP BY 1""")

# ------------------------------------------------------------------ assemble
admin_sql = ','.join(f"'{x}'" for x in ADMIN)
con.execute(f"""CREATE TABLE ledger AS
SELECT b.*,
  w.first_cut_after, w.days_to_cut, f.finish_after AS fwo_finish, coalesce(f.n_open_after,0) AS fwo_open_after,
  coalesce(f.n_closed_nofinish,0) AS fwo_closed_nofinish, coalesce(fb.n_open_before,0) AS fwo_open_before,
  sw.finish_after AS swo_finish, bu.boarded_after, coalesce(bu.n_created_after_unboarded,0) AS bu_pending,
  dm.demolished_after, dm.demolished_before, coalesce(dm.n_permit_pending_after,0) AS demo_pending,
  e.grade AS e1_grade, coalesce(e.n_wo_post,0) AS e1_wo_post, (es.request_id IS NOT NULL) AS e1_sampled,
  coalesce(d.n_later,0) AS n_later, coalesce(d.n_later_closed,0) AS n_later_closed,
  -- evidence flags
  (w.first_cut_after IS NOT NULL AND w.first_cut_after >= b.init_date) AS a_weed,
  (f.finish_after IS NOT NULL) AS a_fwo,
  (sw.finish_after IS NOT NULL) AS a_swo,
  (bu.boarded_after IS NOT NULL) AS a_bu,
  (dm.demolished_after IS NOT NULL) AS a_demo,
  (e.grade IN ('done_late','done_by_promise')) AS a_e1,
  (coalesce(f.n_open_after,0) > 0) AS b_fwo,
  (coalesce(bu.n_created_after_unboarded,0) > 0) AS b_bu,
  (coalesce(dm.n_permit_pending_after,0) > 0) AS b_demo,
  (e.grade = 'no_finish' AND coalesce(e.n_wo_post,0) > 0) AS b_e1,
  (coalesce(d.n_later_closed,0) > 0) AS c_dup,
  (b.problem_code IN ({admin_sql}) AND b.days_past_promise >= {ADMIN_MIN_DAYS_PAST}) AS d_admin
FROM base b
LEFT JOIN ev_weed w USING (request_id) LEFT JOIN ev_fwo f USING (request_id) LEFT JOIN ev_fwo_before fb USING (request_id)
LEFT JOIN ev_swo sw USING (request_id) LEFT JOIN ev_bu bu USING (request_id) LEFT JOIN ev_demo dm USING (request_id)
LEFT JOIN e1 e USING (request_id) LEFT JOIN e1_sample es USING (request_id) LEFT JOIN ev_dup d USING (request_id)""")
con.execute("""ALTER TABLE ledger ADD COLUMN cls VARCHAR""")
con.execute("""UPDATE ledger SET cls = CASE
  WHEN a_weed OR a_fwo OR a_swo OR a_bu OR a_demo OR a_e1 THEN 'a_done_after_filing'
  WHEN b_fwo OR b_bu OR b_demo OR b_e1 THEN 'b_pending_in_records'
  WHEN c_dup THEN 'c_possibly_superseded'
  WHEN d_admin THEN 'd_admin_leftover'
  ELSE 'e_no_evidence' END""")
assert con.execute("SELECT count(*) FROM ledger").fetchone()[0] == N

# top 25 types, rest "other"
top = [r[0] for r in con.execute("SELECT problem_code FROM ledger GROUP BY 1 ORDER BY count(*) DESC, 1 LIMIT 25").fetchall()]
con.execute("ALTER TABLE ledger ADD COLUMN type_bucket VARCHAR")
con.execute("UPDATE ledger SET type_bucket = CASE WHEN problem_code IN (SELECT unnest(?)) THEN problem_code ELSE '(other types)' END", [top])

PRIV.mkdir(parents=True, exist_ok=True)
con.execute(f"COPY ledger TO '{PRIV / 'ledger_rows.parquet'}' (FORMAT PARQUET)")

summary = con.execute("""SELECT cls, count(*) n, round(100.0*count(*)/14902, 2) pct FROM ledger GROUP BY 1 ORDER BY 1""").fetchall()
S['summary'] = [{'class': c, 'n': n, 'pct': p} for c, n, p in summary]
S['evidence_flags'] = dict(zip(
    ['a_weed', 'a_fwo', 'a_swo', 'a_bu', 'a_demo', 'a_e1', 'b_fwo', 'b_bu', 'b_demo', 'b_e1', 'c_dup', 'd_admin',
     'a_and_b', 'fwo_closed_nofinish_rows', 'fwo_open_before_only'],
    con.execute("""SELECT count(*) FILTER (WHERE a_weed), count(*) FILTER (WHERE a_fwo), count(*) FILTER (WHERE a_swo),
      count(*) FILTER (WHERE a_bu), count(*) FILTER (WHERE a_demo), count(*) FILTER (WHERE a_e1),
      count(*) FILTER (WHERE b_fwo), count(*) FILTER (WHERE b_bu), count(*) FILTER (WHERE b_demo), count(*) FILTER (WHERE b_e1),
      count(*) FILTER (WHERE c_dup), count(*) FILTER (WHERE d_admin),
      count(*) FILTER (WHERE (a_weed OR a_fwo OR a_swo OR a_bu OR a_demo OR a_e1) AND (b_fwo OR b_bu OR b_demo OR b_e1)),
      count(*) FILTER (WHERE fwo_closed_nofinish > 0),
      count(*) FILTER (WHERE fwo_open_before > 0 AND NOT a_fwo AND NOT b_fwo)
      FROM ledger""").fetchone()))
S['dup'] = dict(zip(['n_with_later', 'n_with_later_closed', 'n_distinct_code_addr', 'n_rows_in_dup_groups', 'n_dup_groups'],
    con.execute("""SELECT count(*) FILTER (WHERE n_later > 0), count(*) FILTER (WHERE n_later_closed > 0),
      (SELECT count(DISTINCT problem_code || '|' || addr_norm) FROM ledger),
      (SELECT sum(n) FROM (SELECT count(*) n FROM ledger GROUP BY problem_code, addr_norm HAVING count(*) > 1)),
      (SELECT count(*) FROM (SELECT 1 FROM ledger GROUP BY problem_code, addr_norm HAVING count(*) > 1))
      FROM ledger""").fetchone()))
S['weed_days_to_cut'] = dict(zip(['n', 'median', 'q1', 'q3', 'n_within_30', 'n_within_60'],
    con.execute("""SELECT count(*), median(days_to_cut), quantile_cont(days_to_cut, .25), quantile_cont(days_to_cut, .75),
      count(*) FILTER (WHERE days_to_cut <= 30), count(*) FILTER (WHERE days_to_cut <= 60) FROM ledger WHERE a_weed""").fetchone()))
S['fwo_days_to_finish'] = con.execute("""SELECT count(*), median(date_diff('day', ts_init, fwo_finish)) FROM ledger WHERE a_fwo""").fetchone()

bt = con.execute("""SELECT type_bucket, count(*) n,
   median(days_past_promise) med_days_past,
   count(*) FILTER (WHERE cls='a_done_after_filing') a, count(*) FILTER (WHERE cls='b_pending_in_records') b,
   count(*) FILTER (WHERE cls='c_possibly_superseded') c, count(*) FILTER (WHERE cls='d_admin_leftover') d,
   count(*) FILTER (WHERE cls='e_no_evidence') e,
   count(*) FILTER (WHERE e1_sampled) e1_sampled,
   string_agg(DISTINCT CASE WHEN a_weed OR first_cut_after IS NOT NULL OR days_to_cut IS NOT NULL THEN 'weed ledger' END, '') AS _x
 FROM ledger GROUP BY 1 ORDER BY (type_bucket = '(other types)'), n DESC""").fetchall()
REC = {}
for pc in TREE: REC[pc] = 'Forestry work orders'
for pc in BOARDUP: REC[pc] = 'board-up layer'
for pc in DEMO: REC[pc] = 'demolition permits'
REC['Sidewalk Repair'] = 'sidewalk work orders (closed only)'
weed_codes = {r[0] for r in con.execute("SELECT DISTINCT b.problem_code FROM base b JOIN s.request_ledger_flags USING (request_id)").fetchall()}
for pc in weed_codes: REC[pc] = 'Forestry mowing ledger'
for pc in ADMIN: REC[pc] = 'none (admin-leftover rule)'
rows = []
for t, n, med, a, b, c, d, e, e1n, _ in bt:
    rows.append({'type': t, 'n': n, 'median_days_past_promise': med, 'record_used': REC.get(t, 'E1 status pages only' if e1n else 'none'),
                 'a_done_after_filing': a, 'b_pending_in_records': b, 'c_possibly_superseded': c, 'd_admin_leftover': d,
                 'e_no_evidence': e, 'pct_a': round(100 * a / n, 1), 'pct_b': round(100 * b / n, 1), 'pct_e': round(100 * e / n, 1),
                 'e1_sampled': e1n})
with open(OUT / 'ledger_by_type.csv', 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
S['by_type'] = rows
(OUT / 'summary.json').write_text(json.dumps(S, indent=1, default=str))
for k, v in S.items():
    if k != 'by_type':
        print(k, v)
for r in rows:
    print(r)
