"""R1 step 2: the fate of every traceable hand-off, by the city's own completion records.

Services and records (all public files already on disk; nothing fetched):
  Weeds at vacant lots / vacant buildings, and missed / unsatisfactory-cut complaints
      -> Forestry billing ledger (forestry-service-records.csv), N1's `cuts` table: one row per
         parcel, date and service type (Grass Maint, Weed-Grass). Joined through N1's request_parcel.
  "Referred to board up crew" (any request type)
      -> Building Division board-up layer (maps8_BUILDING_DIVISION_Boardups.geojson): ParcelID,
         ADDRESS, DateCreated, DateBoardedUp. Joined on parcel id OR normalised address.
  Tree requests closed "removal work order created"
      -> Cityworks saved search 6955 (open easement tree-removal orders, 1,500-row sample).

For each hand-off: done by the promised date (the request's own PRJCOMPLETEDATE) / done after it
(days late) / no record of the work by 13 Oct 2026. "No record" is counted only where the promise
passed at least 30 days before 13 Oct 2026 (promise <= 13 Sep 2026). The headline denominator is
every matched hand-off whose promise passed by 13 Sep, so the three shares add to 100%.

Outputs: build/R1/fate_summary.json, build/R1/fate_by_service.csv,
         build/R1/private/fate_requests.parquet (request ids; never published).
Run: .venv/bin/python -I scripts/night/R1/02_fate.py
"""
import json, sys, pathlib, datetime as dt
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'N1'))
import duckdb
from normalise import norm  # N1's address normaliser, same one that built requests.addr_norm
from common import DB, OUT, PRIV, LAYERS, NEVER_CUTOFF, ASOF, kind, q, write_csv

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
con.create_function('r1_kind', kind, ['VARCHAR', 'VARCHAR'], 'VARCHAR')
SUMMARY = {'asof': str(ASOF), 'never_cutoff_promise_on_or_before': str(NEVER_CUTOFF)}


def outcome_sql(first_done, promised, matched):
    return f"""CASE WHEN NOT {matched} THEN 'unmatched'
                    WHEN {promised} IS NULL THEN 'no_promise'
                    WHEN {first_done} IS NOT NULL AND {first_done} <= {promised} THEN 'done_by_promise'
                    WHEN {first_done} IS NOT NULL THEN 'done_late'
                    WHEN {promised} <= DATE '{NEVER_CUTOFF}' THEN 'no_record'
                    ELSE 'pending' END"""


def fate_stats(table, where, label, extra=None):
    """Shares among matched hand-offs whose promise passed by NEVER_CUTOFF."""
    r = q(con, f"""
      SELECT count(*) AS n_all,
             count(*) FILTER (WHERE outcome <> 'unmatched') AS n_matched,
             count(*) FILTER (WHERE outcome IN ('done_by_promise','done_late','no_record') AND promised <= DATE '{NEVER_CUTOFF}') AS n_due,
             count(*) FILTER (WHERE outcome = 'done_by_promise' AND promised <= DATE '{NEVER_CUTOFF}') AS n_done_by_promise,
             count(*) FILTER (WHERE outcome = 'done_late' AND promised <= DATE '{NEVER_CUTOFF}') AS n_done_late,
             count(*) FILTER (WHERE outcome = 'no_record' AND promised <= DATE '{NEVER_CUTOFF}') AS n_no_record,
             median(date_diff('day', promised, first_done)) FILTER (WHERE outcome = 'done_late' AND promised <= DATE '{NEVER_CUTOFF}') AS median_days_late,
             quantile_cont(date_diff('day', promised, first_done), 0.25) FILTER (WHERE outcome = 'done_late' AND promised <= DATE '{NEVER_CUTOFF}') AS q1_days_late,
             quantile_cont(date_diff('day', promised, first_done), 0.75) FILTER (WHERE outcome = 'done_late' AND promised <= DATE '{NEVER_CUTOFF}') AS q3_days_late,
             count(*) FILTER (WHERE first_done <= promised + 7 AND promised <= DATE '{NEVER_CUTOFF}' AND outcome <> 'unmatched') AS n_done_by_promise_plus7,
             median(date_diff('day', init_date, first_done)) FILTER (WHERE outcome IN ('done_by_promise','done_late') AND promised <= DATE '{NEVER_CUTOFF}') AS median_days_filing_to_done,
             median(days_to_close) FILTER (WHERE promised <= DATE '{NEVER_CUTOFF}' AND outcome <> 'unmatched') AS median_days_to_close_311,
             median(promise_days) FILTER (WHERE promised <= DATE '{NEVER_CUTOFF}' AND outcome <> 'unmatched') AS median_promise_days,
             count(*) FILTER (WHERE outcome = 'pending') AS n_pending_promise_after_cutoff,
             count(*) FILTER (WHERE outcome = 'no_promise') AS n_no_promise,
             count(*) FILTER (WHERE closed_by_promise AND promised <= DATE '{NEVER_CUTOFF}' AND outcome <> 'unmatched') AS n_closed_by_promise
      FROM {table} WHERE {where}""")[0]
    d = r['n_due'] or 0
    out = {'service': label, **r}
    for k in ('done_by_promise', 'done_late', 'no_record', 'done_by_promise_plus7', 'closed_by_promise'):
        out[f'share_{k}'] = round(r[f'n_{k}'] / d, 6) if d else None
    out['match_rate'] = round(r['n_matched'] / r['n_all'], 6) if r['n_all'] else None
    if extra:
        out.update(extra)
    return out


# ------------------------------------------------------------------ A. weeds vs the Forestry ledger
con.execute("""
CREATE TEMP TABLE weeds AS
SELECT r.request_id, r.problem_code, coalesce(r.res_key, '') AS phrase, r.status, r.status_group, r.closure_class,
       r.class_rule, r1_kind(r.class_rule, r.res_key) AS kind,
       r.init_date, r.init_year, r.ts_init, r.ts_closed, CAST(r.ts_promised AS DATE) AS promised, r.promise_days,
       r.days_to_close, r.ward, r.ward_group, r.channel_group, rp.pid, coalesce(rp.is_lra, false) AS is_lra,
       l.first_cut_after AS first_done, l.last_cut_before,
       r.status_group = 'closed' AND r.ts_closed <= r.ts_promised AS closed_by_promise
FROM s.v_requests r
LEFT JOIN s.request_parcel rp USING (request_id)
LEFT JOIN s.request_ledger l USING (request_id)
WHERE r.problem_code IN (SELECT problem_code FROM s.weed_ledger_codes)
  AND r.init_date BETWEEN DATE '2025-01-01' AND DATE '2026-10-12'
""")
con.execute(f"ALTER TABLE weeds ADD COLUMN outcome VARCHAR")
con.execute(f"UPDATE weeds SET outcome = {outcome_sql('first_done', 'promised', 'pid IS NOT NULL')}")
con.execute("""ALTER TABLE weeds ADD COLUMN svc VARCHAR""")
con.execute("""UPDATE weeds SET svc = CASE
    WHEN problem_code = 'Weeds-Vacant Lot' THEN 'weeds_vacant_lot'
    WHEN problem_code = 'Weeds-Vacant Bldg' THEN 'weeds_vacant_bldg'
    WHEN problem_code IN ('Missed Cut - V Lot','Unsatisfy Cut - VLot') THEN 'cut_complaint_lot'
    WHEN problem_code IN ('Missed Cut - VBldg','Unsatisfy Cut -VBldg') THEN 'cut_complaint_bldg'
    ELSE 'weeds_other' END""")
HANDOFF_WEEDS = "status_group = 'closed' AND closure_class IN ('handed_off','converted') AND kind = 'crew_work'"

# ------------------------------------------------------------------ B. board-ups
feats = json.loads((LAYERS / 'maps8_BUILDING_DIVISION_Boardups.geojson').read_text())['features']


def utc_date(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date() if isinstance(ms, (int, float)) else None


def utc_ts(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).replace(tzinfo=None) if isinstance(ms, (int, float)) else None


con.execute("CREATE TEMP TABLE boardup (parcel VARCHAR, addr VARCHAR, created_utc TIMESTAMP, boarded DATE)")
con.executemany("INSERT INTO boardup VALUES (?,?,?,?)",
                [((p.get('ParcelID') or '').strip() or None, norm(p.get('ADDRESS')) or None,
                  utc_ts(p.get('DateCreated')), utc_date(p.get('DateBoardedUp'))) for p in (f['properties'] for f in feats)])
bu_meta = q(con, "SELECT count(*) n, min(boarded) min_boarded, max(boarded) max_boarded, max(created_utc) max_created, count(*) FILTER (WHERE boarded IS NULL) n_no_boarded_date FROM boardup")[0]
SUMMARY['boardup_layer'] = bu_meta
print('board-up layer', bu_meta)

con.execute("""
CREATE TEMP TABLE bu_req AS
SELECT r.request_id, r.problem_code, coalesce(r.res_key, '') AS phrase, r.status, r.status_group, r.closure_class,
       r.class_rule, r1_kind(r.class_rule, r.res_key) AS kind,
       r.init_date, r.init_year, r.ts_init, r.ts_closed, CAST(r.ts_promised AS DATE) AS promised, r.promise_days,
       r.days_to_close, r.ward, r.ward_group, r.channel_group, rp.pid, r.addr_norm,
       r.status_group = 'closed' AND r.ts_closed <= r.ts_promised AS closed_by_promise
FROM s.v_requests r LEFT JOIN s.request_parcel rp USING (request_id)
WHERE r.init_date BETWEEN DATE '2025-01-01' AND DATE '2026-10-12'
  AND (r.problem_code = 'Vacnt Bldg Unsecured' OR coalesce(r.res_key, '') = 'referred to board up crew')
""")
con.execute("""
CREATE TEMP TABLE bu_match AS
SELECT q.request_id, b.boarded, b.created_utc, (b.parcel = q.pid) AS by_parcel
FROM bu_req q JOIN boardup b
  ON (b.parcel = q.pid AND q.pid IS NOT NULL) OR (b.addr = q.addr_norm AND coalesce(q.addr_norm, '') <> '')
""")
con.execute("""
CREATE TEMP TABLE bu AS
SELECT q.*,
       (SELECT min(m.boarded) FROM bu_match m WHERE m.request_id = q.request_id AND m.boarded >= q.init_date) AS first_done,
       (SELECT min(m.created_utc) FROM bu_match m WHERE m.request_id = q.request_id AND m.created_utc >= q.ts_init - INTERVAL 1 DAY) AS first_created_after,
       (SELECT max(m.boarded) FROM bu_match m WHERE m.request_id = q.request_id AND m.boarded < q.init_date) AS last_board_before,
       EXISTS (SELECT 1 FROM bu_match m WHERE m.request_id = q.request_id) AS in_layer
FROM bu_req q
""")
# "matched" for board-ups = the request resolves to a parcel or a usable address
con.execute("ALTER TABLE bu ADD COLUMN outcome VARCHAR")
BU_MATCHED = "(pid IS NOT NULL OR coalesce(addr_norm, '') <> '')"
con.execute("UPDATE bu SET outcome = " + outcome_sql('first_done', 'promised', BU_MATCHED))
HANDOFF_BU = "status_group = 'closed' AND phrase = 'referred to board up crew'"

# ------------------------------------------------------------------ C. trees: removal work order created
con.execute("""
CREATE TEMP TABLE tr AS
SELECT r.request_id, r.problem_code, coalesce(r.res_key, '') AS phrase, r.init_date, r.init_year, r.ts_init, r.ts_closed,
       CAST(r.ts_promised AS DATE) AS promised, r.days_to_close, r.ward_group,
       (SELECT count(*) FROM s.request_wo w WHERE w.request_id = r.request_id AND w.source = 'tree_removal' AND w.addr_match
                AND w.proj_start >= r.ts_init - INTERVAL 1 DAY) AS n_open_removal_dated_after,
       (SELECT min(w.proj_finish) FROM s.request_wo w WHERE w.request_id = r.request_id AND w.source = 'tree_removal' AND w.addr_match
                AND w.proj_start >= r.ts_init - INTERVAL 1 DAY) AS wo_proj_finish,
       (SELECT count(*) FROM s.request_wo w WHERE w.request_id = r.request_id AND w.source = 'tree_removal' AND w.addr_match) AS n_open_removal_any,
       (SELECT count(*) FROM s.request_wo w WHERE w.request_id = r.request_id AND w.source = 'tree_trim' AND w.addr_match) AS n_open_trim_any
FROM s.v_requests r
WHERE r.init_date BETWEEN DATE '2025-01-01' AND DATE '2026-10-12' AND r.status_group = 'closed'
  AND coalesce(r.res_key, '') IN ('removal work order created', 'trim work order created')
  AND r.problem_code IN ('Inspect City Tree','City Tree Down','City Tree Limb Down','Stump Removal','Broken/Hanging Limb','Inspect Private Tree')
""")

# ------------------------------------------------------------------ per-service fate table (hand-offs only)
rows = []
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc='weeds_vacant_lot' AND init_year=2026", 'Weeds, vacant lot (2026 filings)'))
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc='weeds_vacant_bldg' AND init_year=2026", 'Weeds, vacant building (2026 filings)'))
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc IN ('cut_complaint_lot','cut_complaint_bldg') AND init_year=2026", 'Missed or unsatisfactory cut complaints (2026 filings)'))
rows.append(fate_stats('bu', f"{HANDOFF_BU}", 'Referred to board-up crew (2025-26 filings)'))
rows.append(fate_stats('bu', f"{HANDOFF_BU} AND problem_code='Vacnt Bldg Unsecured'", 'Referred to board-up crew, vacant building unsecured only (2025-26)'))
# sensitivity rows (not in the headline)
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc='weeds_vacant_bldg' AND init_year=2025", 'SENSITIVITY Weeds, vacant building (2025 filings; Weed-Grass ledger looks complete in 2025)'))
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc='weeds_vacant_lot' AND init_year=2025", 'EXCLUDED Weeds, vacant lot (2025 filings; Grass Maint ledger thin in 2025)'))
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc='weeds_vacant_lot' AND init_year=2026 AND phrase LIKE 'on schedule to be cut%'", 'Weeds, vacant lot, "on schedule to be cut" only (2026)'))
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc='weeds_vacant_lot' AND init_year=2026 AND phrase = 'added to rotation'", 'Weeds, vacant lot, "added to rotation" only (2026)'))
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc='weeds_vacant_bldg' AND init_year=2026 AND phrase LIKE 'on schedule to be cut%'", 'Weeds, vacant building, "on schedule to be cut" only (2026)'))
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc='weeds_vacant_bldg' AND init_year=2026 AND phrase = 'added to rotation'", 'Weeds, vacant building, "added to rotation" only (2026)'))
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc='weeds_vacant_lot' AND init_year=2026 AND is_lra", 'Weeds, vacant lot, land-bank (LRA) parcels (2026)'))
rows.append(fate_stats('weeds', f"{HANDOFF_WEEDS} AND svc='weeds_vacant_lot' AND init_year=2026 AND NOT is_lra", 'Weeds, vacant lot, other parcels (2026)'))
write_csv(OUT / 'fate_by_service.csv', rows)
SUMMARY['by_service'] = rows
for r in rows:
    print(f"{r['service'][:75]:75s} due={r['n_due']:5d} byP={r['share_done_by_promise']} late={r['share_done_late']} none={r['share_no_record']} medLate={r['median_days_late']} match={r['match_rate']}")

# ------------------------------------------------------------------ headline: pooled traceable hand-offs
con.execute(f"""
CREATE TEMP TABLE pooled AS
SELECT 'weeds' AS rec, svc, request_id, outcome, promised, first_done, init_date, days_to_close, promise_days, closed_by_promise, ward_group, channel_group
FROM weeds WHERE {HANDOFF_WEEDS} AND init_year = 2026
UNION ALL
SELECT 'boardup', 'boardup', request_id, outcome, promised, first_done, init_date, days_to_close, promise_days, closed_by_promise, ward_group, channel_group
FROM bu WHERE {HANDOFF_BU}
""")
head = fate_stats('pooled', 'TRUE', 'All traceable hand-offs (weeds 2026 + board-ups 2025-26)')
SUMMARY['headline'] = head
print('HEADLINE', json.dumps(head, default=str))
SUMMARY['headline_by_ward_group'] = [fate_stats('pooled', f"ward_group = '{wg}'", f'ward group {wg}') for wg in
                                     [r[0] for r in con.execute("SELECT DISTINCT ward_group FROM pooled WHERE ward_group IS NOT NULL ORDER BY 1").fetchall()]]
for r in SUMMARY['headline_by_ward_group']:
    print('  ', r['service'], r['n_due'], r['share_done_by_promise'], r['share_done_late'], r['share_no_record'], r['median_days_late'])
SUMMARY['headline_by_service_ward_group'] = []
for svc in ('weeds_vacant_lot', 'weeds_vacant_bldg', 'boardup'):
    for wg in ('1-5', '6-9', '10-14'):
        SUMMARY['headline_by_service_ward_group'].append(fate_stats('pooled', f"svc='{svc}' AND ward_group='{wg}'", f'{svc} wards {wg}'))
for r in SUMMARY['headline_by_service_ward_group']:
    print('  ', r['service'], r['n_due'], r['share_done_by_promise'], r['share_done_late'], r['share_no_record'], r['median_days_late'])

# ------------------------------------------------------------------ record checks (does the record see work the city says it did?)
chk = {}
chk['boardup_positive_control'] = q(con, """
  SELECT phrase, count(*) n,
         avg(CAST(first_done IS NOT NULL AND first_done <= CAST(ts_closed AS DATE) + 14 AS INT)) AS share_board_record_by_close_plus14,
         avg(CAST(first_done IS NOT NULL AS INT)) AS share_board_record_any_after_filing,
         avg(CAST(in_layer AS INT)) AS share_address_in_layer
  FROM bu WHERE status_group='closed' AND closure_class='done' GROUP BY 1 ORDER BY 2 DESC""")
chk['boardup_handoff_created_vs_closed'] = q(con, f"""
  SELECT count(*) n_with_created_after,
         median(epoch(first_created_after - ts_closed) / 86400.0) AS median_days_created_minus_311_close,
         avg(CAST(abs(epoch(first_created_after - ts_closed)) <= 2 * 86400 AS INT)) AS share_created_within_2d_of_close
  FROM bu WHERE {HANDOFF_BU} AND first_created_after IS NOT NULL""")
chk['weeds_done_closures_ledger'] = q(con, """
  SELECT svc, count(*) n, count(pid) n_matched,
         avg(CAST(first_done IS NOT NULL AND first_done <= CAST(ts_closed AS DATE) + 14 AS INT)) FILTER (WHERE pid IS NOT NULL) AS share_cut_by_close_plus14,
         avg(CAST(first_done IS NOT NULL AND first_done <= CAST(ts_closed AS DATE) + 30 AS INT)) FILTER (WHERE pid IS NOT NULL) AS share_cut_by_close_plus30,
         avg(CAST(last_cut_before >= init_date - 14 AS INT)) FILTER (WHERE pid IS NOT NULL) AS share_cut_in_14d_before_filing
  FROM weeds WHERE status_group='closed' AND closure_class='done' AND init_year = 2026 GROUP BY 1""")
SUMMARY['record_checks'] = chk
print(json.dumps(chk, indent=1, default=str))

# ------------------------------------------------------------------ trees (partial)
SUMMARY['trees_removal_order_created'] = q(con, """
  SELECT phrase, init_year, count(*) n,
         count(*) FILTER (WHERE n_open_removal_dated_after > 0) AS n_matching_order_still_open,
         count(*) FILTER (WHERE n_open_removal_any > 0) AS n_any_open_removal_at_address,
         count(*) FILTER (WHERE n_open_trim_any > 0) AS n_any_open_trim_at_address,
         median(date_diff('day', CAST(wo_proj_finish AS DATE), DATE '2026-10-13')) FILTER (WHERE n_open_removal_dated_after > 0) AS median_days_past_order_due
  FROM tr GROUP BY 1, 2 ORDER BY 1, 2""")
SUMMARY['trees_cancelled_blank_with_open_order'] = q(con, """
  WITH c AS (SELECT r.request_id, r.ts_init FROM s.v_requests r
             WHERE r.problem_code = 'Inspect City Tree' AND r.status_group = 'cancelled' AND coalesce(r.res_key, '') = ''
               AND r.init_date BETWEEN DATE '2025-01-01' AND DATE '2026-10-12'),
  o AS (SELECT c.request_id, min(w.proj_finish) AS due, max(epoch(c.ts_init - w.proj_start) / 86400.0) AS age_days
        FROM c JOIN s.request_wo w USING (request_id)
        WHERE w.source = 'tree_removal' AND w.addr_match AND w.proj_start < c.ts_init - INTERVAL 1 DAY GROUP BY 1)
  SELECT (SELECT count(*) FROM c) AS n_cancelled_blank, count(*) AS n_with_open_removal_order_before_filing,
         median(age_days) AS median_order_age_at_filing_days,
         avg(CAST(due < TIMESTAMP '2026-10-13' AS INT)) AS share_order_past_own_due_13oct,
         median(date_diff('day', CAST(due AS DATE), DATE '2026-10-13')) AS median_days_order_past_due_13oct
  FROM o""")[0]
print('trees cancelled', SUMMARY['trees_cancelled_blank_with_open_order'])
SUMMARY['trees_note'] = ('Cityworks saved search 6955 returned the 1,500 lowest work-order ids of the open (NEW) removal orders '
                         '(ids rise with ProjStartDate, r=0.997; newest start 8 Jan 2026), so an order created before 8 Jan 2026 '
                         'and still open on 13 Oct 2026 should be in the sample (inferred). Matching is by normalised address only.')
for r in SUMMARY['trees_removal_order_created']:
    print('trees', r)

# ------------------------------------------------------------------ save
con.execute(f"""COPY (SELECT 'weeds' AS rec, request_id, problem_code, phrase, status, closure_class, kind, init_date, promised, first_done, outcome, ward_group FROM weeds
                     UNION ALL SELECT 'boardup', request_id, problem_code, phrase, status, closure_class, kind, init_date, promised, first_done, outcome, ward_group FROM bu)
               TO '{PRIV / 'fate_requests.parquet'}' (FORMAT parquet)""")
(OUT / 'fate_summary.json').write_text(json.dumps(SUMMARY, indent=1, default=str))
print('wrote', OUT / 'fate_summary.json')
