"""North Taylor mechanism test: does lot-1 show what the video says it shows?

Question: did lot-1's 36 cut neighbours have weed requests too, closed just as fast
and with the same words? If so, fast closing cannot explain why lot-1 was missed. Is it luck whose lot
gets cut?

Part A, the block. Every parcel on lot-1's assessor city block (ledger CITYBLOCK, else characters 2-7 of
the MSD handle, as R1 step 3): 2026 weed requests matched to the parcel (count, filing dates, minutes to
close, closing words), land-bank ownership, Forestry maintenance list category (file dated 2023-05-26),
MSD land use, ledger property type and charge, and billed cut dates by year.
Part B, citywide. 2026 Weeds-Vacant Lot / Weeds-Vacant Bldg requests closed "on schedule to be cut ..."
(and, separately, "added to rotation"), filed by 13 Sep 2026, matched to a parcel: share on parcels with
no cut billed at any time in 2026, split by maintenance list, ownership, 2024/2025 cut history and closing
speed. Also replicates R1's 539 of 1,761.
Part C, persistence. Of maintenance-list land-bank vacant lots cut in 2024, how many are cut in 2026,
by whether they were cut in 2025.

A "cut" is one distinct (parcel, service date) of 'Grass Maint' or 'Weed-Grass' in the Forestry billing
ledger (table cuts). Ledger dates are weekly posting batches. The ledger and the 311 file end 13 Oct 2026.

Lot-1's parcel id is read from the git-ignored build/N5/private/hero_ids.json; the code carries no id.
Public output (build/north-taylor/mechanism.json) is aggregate only: no ids, no addresses.
Parcel-level rows go to build/north-taylor/private/ (git-ignored).
Run: .venv/bin/python -I scripts/exec/north-taylor/01_mechanism.py
"""
import csv, json, pathlib, datetime as dt
import duckdb

ROOT = pathlib.Path('.')
DB = ROOT / 'build' / 'stl.duckdb'
OUT = ROOT / 'build' / 'north-taylor'
PRIV = OUT / 'private'
OUT.mkdir(parents=True, exist_ok=True)
PRIV.mkdir(parents=True, exist_ok=True)
IDS = json.load(open(ROOT / 'build/N5/private/hero_ids.json'))['lots']['lot-1']
LOT = IDS['pid']
RELATED = [r['pid'] if isinstance(r, dict) else r for r in IDS['related']]
CUTOFF = dt.date(2026, 9, 13)
ASOF = dt.date(2026, 10, 13)
REPORT = ('Weeds-Vacant Lot', 'Weeds-Vacant Bldg')
COMPLAINT = ('Missed Cut - V Lot', 'Missed Cut - VBldg', 'Unsatisfy Cut - VLot', 'Unsatisfy Cut -VBldg')

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")


def q(sql, params=None):
    cur = con.execute(sql, params or [])
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def one(sql, params=None):
    return q(sql, params)[0]


RES = {'definition': __doc__, 'asof': str(ASOF), 'generated': dt.datetime.now().strftime('%Y-%m-%d %H:%M %Z')}

# ------------------------------------------------------------------ shared tables
con.execute("CREATE TEMP TABLE lblock AS SELECT parcel, mode(cityblock) AS cityblock FROM s.ledger WHERE cityblock IS NOT NULL GROUP BY parcel")
con.execute("""CREATE TEMP TABLE pblock AS
  SELECT p.pid AS parcel, coalesce(l.cityblock, substr(p.handle, 2, 6)) AS cityblock FROM s.parcels p LEFT JOIN lblock l ON l.parcel = p.pid
  UNION SELECT l.parcel, l.cityblock FROM lblock l WHERE l.parcel NOT IN (SELECT pid FROM s.parcels)""")
con.execute("""CREATE TEMP TABLE cy AS
  SELECT parcel, year(service_date) AS y, count(DISTINCT service_date) AS n
  FROM s.cuts WHERE service_date BETWEEN DATE '2019-01-01' AND DATE '2026-10-13' GROUP BY 1, 2""")
con.execute("""CREATE TEMP TABLE hist AS
  SELECT parcel,
         sum(n) FILTER (WHERE y = 2026) AS c2026, sum(n) FILTER (WHERE y = 2025) AS c2025, sum(n) FILTER (WHERE y = 2024) AS c2024,
         sum(n) FILTER (WHERE y BETWEEN 2019 AND 2024) AS c2019_24
  FROM cy GROUP BY parcel""")
con.execute("CREATE TEMP TABLE c26 AS SELECT DISTINCT parcel, service_date AS d FROM s.cuts WHERE service_date BETWEEN DATE '2026-01-01' AND DATE '2026-10-13'")
con.execute("CREATE TEMP TABLE maint AS SELECT parcel_id AS parcel, any_value(category) AS category FROM s.maint_props GROUP BY 1")
con.execute("CREATE TEMP TABLE lra AS SELECT parcel_id AS parcel, any_value(parcel_status) AS lra_status, any_value(property_type) AS lra_type FROM s.lra GROUP BY 1")

# ------------------------------------------------------------------ Part A: the block
CB = one("SELECT cityblock FROM pblock WHERE parcel = ?", [LOT])['cityblock']
con.execute("CREATE TEMP TABLE blk AS SELECT DISTINCT parcel FROM pblock WHERE cityblock = ?", [CB])
con.execute(f"""CREATE TEMP TABLE blk_req AS
  SELECT rp.pid AS parcel, r.request_id, r.problem_code, r.ts_init, r.ts_closed, r.init_date, r.status_group, r.res_key,
         r.resolution_public, r.ts_promised, r.channel_group, rp.method,
         round(extract(epoch FROM (r.ts_closed - r.ts_init)) / 60.0, 1) AS minutes_to_close
  FROM s.v_requests r JOIN s.request_parcel rp USING (request_id)
  WHERE rp.pid IN (SELECT parcel FROM blk) AND r.init_year = 2026
    AND r.problem_code IN {REPORT + COMPLAINT + ('Weeds-Occupied Ppty', 'Debris-Vacant Lot', 'Debris-Vacant Bldg')}""")

rows = q(f"""
SELECT b.parcel, b.parcel = ? AS is_lot1, b.parcel IN (SELECT unnest(?)) AS is_related,
       l.parcel IS NOT NULL AS is_lra, l.lra_status, l.lra_type,
       m.category AS maint_category,
       p.LUC AS luc, p.PROPERTY_CLASS AS property_class,
       (SELECT arg_max(property_type, service_date) FROM s.ledger g WHERE g.parcel = b.parcel AND g.service_type IN ('Grass Maint', 'Weed-Grass')) AS ledger_property_type,
       (SELECT arg_max(service_amount, service_date) FROM s.ledger g WHERE g.parcel = b.parcel AND g.service_type IN ('Grass Maint', 'Weed-Grass')) AS last_cut_charge,
       (SELECT max(service_date) FROM s.cuts c WHERE c.parcel = b.parcel AND c.service_date < DATE '2026-01-01') AS last_cut_before_2026,
       coalesce(h.c2026, 0) AS cuts_2026, coalesce(h.c2025, 0) AS cuts_2025, coalesce(h.c2024, 0) AS cuts_2024,
       coalesce(h.c2019_24, 0) AS cuts_2019_24,
       (SELECT list(d ORDER BY d) FROM c26 WHERE c26.parcel = b.parcel) AS cut_dates_2026,
       (SELECT count(*) FROM blk_req r WHERE r.parcel = b.parcel AND r.problem_code IN {REPORT}) AS weed_reports_2026,
       (SELECT count(*) FROM blk_req r WHERE r.parcel = b.parcel AND r.problem_code IN {COMPLAINT}) AS cut_complaints_2026,
       (SELECT count(*) FROM blk_req r WHERE r.parcel = b.parcel AND r.problem_code NOT IN {REPORT + COMPLAINT}) AS other_weed_debris_2026
FROM blk b LEFT JOIN lra l USING (parcel) LEFT JOIN maint m USING (parcel) LEFT JOIN s.parcels p ON p.pid = b.parcel
LEFT JOIN hist h USING (parcel)
ORDER BY is_lot1 DESC, cuts_2026 DESC""", [LOT, RELATED])

# private parcel-level table
with open(PRIV / 'block_parcels.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
req_rows = q("SELECT * FROM blk_req ORDER BY ts_init")
with open(PRIV / 'block_requests.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(req_rows[0].keys()))
    w.writeheader()
    w.writerows(req_rows)

lot = rows[0]
assert lot['is_lot1']
nb = [r for r in rows if not r['is_lot1']]
cut = [r for r in nb if r['cuts_2026'] > 0]
uncut = [r for r in nb if r['cuts_2026'] == 0]


def profile(group):
    n = len(group)
    def cnt(f):
        return sum(1 for r in group if f(r))
    return {
        'n_parcels': n,
        'land_bank': cnt(lambda r: r['is_lra']),
        'on_maint_list_any': cnt(lambda r: r['maint_category'] is not None),
        'maint_vacant_lot': cnt(lambda r: r['maint_category'] == 'Vacant Lot'),
        'maint_vacant_building': cnt(lambda r: r['maint_category'] == 'Vacant Building'),
        'maint_other': cnt(lambda r: r['maint_category'] not in (None, 'Vacant Lot', 'Vacant Building')),
        'ledger_type_vacant_lot': cnt(lambda r: r['ledger_property_type'] == 'Vacant Lot'),
        'ledger_type_vacant_building': cnt(lambda r: r['ledger_property_type'] == 'Vacant Building'),
        'ledger_type_other_or_none': cnt(lambda r: r['ledger_property_type'] not in ('Vacant Lot', 'Vacant Building')),
        'never_in_cut_ledger_2019_26': cnt(lambda r: r['cuts_2019_24'] + r['cuts_2025'] + r['cuts_2026'] == 0),
        'msd_luc_1010': cnt(lambda r: r['luc'] == '1010'),
        'msd_class_17': cnt(lambda r: r['property_class'] == '17'),
        'cut_2024': cnt(lambda r: r['cuts_2024'] > 0),
        'cut_2025': cnt(lambda r: r['cuts_2025'] > 0),
        'cut_2026': cnt(lambda r: r['cuts_2026'] > 0),
        'cut_2024_not_2025': cnt(lambda r: r['cuts_2024'] > 0 and r['cuts_2025'] == 0),
        'with_weed_report_2026': cnt(lambda r: r['weed_reports_2026'] > 0),
        'weed_reports_2026_total': sum(r['weed_reports_2026'] for r in group),
        'with_cut_complaint_2026': cnt(lambda r: r['cut_complaints_2026'] > 0),
        'median_cuts_2026': sorted(r['cuts_2026'] for r in group)[n // 2] if n else None,
        'last_cut_charge_values': sorted({r['last_cut_charge'] for r in group if r['last_cut_charge'] is not None}),
    }


A = {'block_parcels_total': len(rows), 'lot1': profile([lot]), 'neighbours_cut_2026': profile(cut),
     'neighbours_not_cut_2026': profile(uncut), 'neighbours_all': profile(nb)}
A['lot1_detail'] = {k: lot[k] for k in ('is_lra', 'lra_status', 'lra_type', 'maint_category', 'luc', 'property_class',
                                         'ledger_property_type', 'last_cut_charge', 'cuts_2026', 'cuts_2025', 'cuts_2024',
                                         'cuts_2019_24', 'weed_reports_2026', 'cut_complaints_2026')}
A['lot1_detail']['last_cut_before_2026_month'] = str(lot['last_cut_before_2026'])[:7]
A['block_cut_days_2026'] = one("SELECT count(DISTINCT d) n FROM c26 WHERE parcel IN (SELECT parcel FROM blk)")['n']
A['block_cut_days_2026_list'] = [str(r['d']) for r in q("SELECT DISTINCT d FROM c26 WHERE parcel IN (SELECT parcel FROM blk) ORDER BY d")]
A['block_cut_days_2025'] = one("SELECT count(DISTINCT service_date) n FROM s.cuts WHERE year(service_date) = 2025 AND parcel IN (SELECT parcel FROM blk)")['n']
A['block_parcels_cut_2025'] = one("SELECT count(DISTINCT parcel) n FROM s.cuts WHERE year(service_date) = 2025 AND parcel IN (SELECT parcel FROM blk)")['n']
A['block_parcels_cut_2024'] = one("SELECT count(DISTINCT parcel) n FROM s.cuts WHERE year(service_date) = 2024 AND parcel IN (SELECT parcel FROM blk)")['n']
A['block_cut_days_2024'] = one("SELECT count(DISTINCT service_date) n FROM s.cuts WHERE year(service_date) = 2024 AND parcel IN (SELECT parcel FROM blk)")['n']
# parcels cut on each 2026 block cut day
A['parcels_per_block_cut_day_2026'] = [r['n'] for r in q("SELECT d, count(DISTINCT parcel) n FROM c26 WHERE parcel IN (SELECT parcel FROM blk) GROUP BY d ORDER BY d")]
# the lot's 2024 cut days: was it cut on the same days as its block?
A['lot1_2024_cut_days_shared_with_block'] = one("""SELECT count(*) n_days, count(*) FILTER (WHERE EXISTS (
    SELECT 1 FROM s.cuts c2 WHERE c2.service_date = c.service_date AND c2.parcel IN (SELECT parcel FROM blk) AND c2.parcel <> ?)) shared
    FROM (SELECT DISTINCT service_date FROM s.cuts WHERE parcel = ? AND year(service_date) = 2024) c""", [LOT, LOT])

# requests on the block, request level (Weeds-Vacant Lot / Bldg only)
con.execute(f"""CREATE TEMP TABLE blk_rep AS
  SELECT r.*, r.parcel = ? AS is_lot1, coalesce(h.c2026, 0) > 0 AS parcel_cut_2026,
         (SELECT min(d) FROM c26 WHERE c26.parcel = r.parcel AND c26.d >= r.init_date) AS next_cut,
         (SELECT max(d) FROM c26 WHERE c26.parcel = r.parcel AND c26.d < r.init_date) AS prev_cut
  FROM blk_req r LEFT JOIN hist h USING (parcel) WHERE r.problem_code IN {REPORT}""", [LOT])
A['reports_by_group'] = q("""SELECT CASE WHEN is_lot1 THEN 'lot-1' WHEN parcel_cut_2026 THEN 'neighbour cut 2026' ELSE 'neighbour not cut 2026' END AS grp,
    count(*) AS reports, count(DISTINCT parcel) AS parcels, min(init_date) AS first_filed, max(init_date) AS last_filed,
    median(minutes_to_close) AS median_minutes_to_close, min(minutes_to_close) AS min_minutes, max(minutes_to_close) AS max_minutes,
    count(*) FILTER (WHERE minutes_to_close <= 60) AS closed_within_60_min,
    count(*) FILTER (WHERE res_key LIKE 'on schedule to be cut%') AS on_schedule,
    count(*) FILTER (WHERE res_key = 'added to rotation') AS added_to_rotation,
    count(*) FILTER (WHERE status_group <> 'closed') AS not_closed,
    count(*) FILTER (WHERE next_cut IS NOT NULL) AS cut_after_filing,
    median(date_diff('day', init_date, next_cut)) AS median_days_to_next_cut,
    count(*) FILTER (WHERE date_diff('day', init_date, next_cut) <= 14) AS cut_within_14d,
    count(*) FILTER (WHERE date_diff('day', init_date, next_cut) <= 30) AS cut_within_30d
    FROM blk_rep GROUP BY 1 ORDER BY 1""")
A['report_words_block'] = q("SELECT res_key, count(*) n FROM blk_rep GROUP BY 1 ORDER BY 2 DESC")
A['report_filing_dates_block'] = q("""SELECT init_date, count(*) reports, count(DISTINCT parcel) parcels,
    count(*) FILTER (WHERE is_lot1) lot1, count(*) FILTER (WHERE NOT is_lot1 AND parcel_cut_2026) cut_neighbours,
    count(*) FILTER (WHERE NOT is_lot1 AND NOT parcel_cut_2026) uncut_neighbours FROM blk_rep GROUP BY 1 ORDER BY 1""")
A['complaints_block'] = q("""SELECT problem_code, res_key, count(*) n, count(*) FILTER (WHERE parcel = ?) lot1
    FROM blk_req WHERE problem_code IN ('Missed Cut - V Lot', 'Missed Cut - VBldg', 'Unsatisfy Cut - VLot', 'Unsatisfy Cut -VBldg') GROUP BY 1, 2""", [LOT])
A['other_weed_debris_block'] = q(f"SELECT problem_code, res_key, count(*) n FROM blk_req WHERE problem_code NOT IN {REPORT + COMPLAINT} GROUP BY 1, 2")
# were requested neighbours cut on the same batch days as unrequested ones?
A['cut_days_requested_vs_not'] = one("""WITH rq AS (SELECT DISTINCT parcel FROM blk_rep)
    SELECT count(DISTINCT d) FILTER (WHERE parcel IN (SELECT parcel FROM rq)) AS days_with_requested_parcel_cut,
           count(DISTINCT d) FILTER (WHERE parcel NOT IN (SELECT parcel FROM rq)) AS days_with_unrequested_parcel_cut,
           count(DISTINCT d) FILTER (WHERE parcel IN (SELECT parcel FROM rq) AND d IN (SELECT d FROM c26 WHERE parcel IN (SELECT parcel FROM blk) AND parcel NOT IN (SELECT parcel FROM rq))) AS requested_cut_days_also_unrequested
    FROM c26 WHERE parcel IN (SELECT parcel FROM blk)""")
# the two lots reported with lot-1: same block or not, cut or not
A['related_lots'] = q("""SELECT (pb.cityblock = ?) AS same_city_block, coalesce(h.c2026, 0) AS cuts_2026, coalesce(h.c2025, 0) AS cuts_2025,
    coalesce(h.c2024, 0) AS cuts_2024, l.parcel IS NOT NULL AS is_lra, m.category AS maint_category
    FROM (SELECT unnest(?) AS parcel) x LEFT JOIN pblock pb USING (parcel) LEFT JOIN hist h USING (parcel)
    LEFT JOIN lra l USING (parcel) LEFT JOIN maint m USING (parcel)""", [CB, RELATED])
# the twin: the related lot on lot-1's own block, reported alongside it
A['twin_same_block_reports'] = one(f"""SELECT count(*) AS reports, count(*) FILTER (WHERE res_key LIKE 'on schedule to be cut%') AS on_schedule,
    min(minutes_to_close) AS min_minutes, max(minutes_to_close) AS max_minutes, median(minutes_to_close) AS median_minutes,
    (SELECT coalesce(max(c2026), 0) FROM hist WHERE hist.parcel IN (SELECT parcel FROM blk WHERE parcel IN (SELECT unnest(?)))) AS twin_cuts_2026
    FROM blk_rep WHERE parcel IN (SELECT unnest(?)) AND parcel IN (SELECT parcel FROM blk)""", [RELATED, RELATED])
A['cut_neighbours_no_weed_request_any_kind'] = one(f"""SELECT count(*) AS n FROM hist h
    WHERE h.parcel IN (SELECT parcel FROM blk) AND h.parcel <> ? AND coalesce(h.c2026, 0) > 0
      AND NOT EXISTS (SELECT 1 FROM blk_req r WHERE r.parcel = h.parcel)""", [LOT])['n']
A['ledger_fields'] =[r['column_name'] for r in q("SELECT column_name FROM information_schema.columns WHERE table_name = 'ledger' AND table_catalog = 's'")]
RES['A_block'] = A

# ------------------------------------------------------------------ Part B: citywide on-schedule closures
con.execute(f"""CREATE TEMP TABLE req AS
  SELECT r.request_id, rp.pid AS parcel, r.problem_code, r.init_date, r.res_key, r.ts_init, r.ts_closed,
         extract(epoch FROM (r.ts_closed - r.ts_init)) / 60.0 AS mins, coalesce(rp.is_lra, false) AS is_lra,
         m.category AS maint_category, coalesce(h.c2026, 0) AS c2026, coalesce(h.c2025, 0) AS c2025,
         coalesce(h.c2024, 0) AS c2024, coalesce(h.c2019_24, 0) AS c2019_24,
         (SELECT min(d) FROM c26 WHERE c26.parcel = rp.pid AND c26.d >= r.init_date) AS next_cut
  FROM s.v_requests r JOIN s.request_parcel rp USING (request_id)
  LEFT JOIN maint m ON m.parcel = rp.pid LEFT JOIN hist h ON h.parcel = rp.pid
  WHERE r.problem_code IN {REPORT} AND r.init_year = 2026 AND r.status_group = 'closed'
    AND (r.res_key LIKE 'on schedule to be cut%' OR r.res_key = 'added to rotation')
    AND r.init_date <= DATE '{CUTOFF}'""")


def split(where, label, by):
    out = q(f"""SELECT {by} AS grp, count(*) AS requests, count(DISTINCT parcel) AS parcels,
        round(100.0 * avg(CAST(c2026 = 0 AS INT)), 1) AS pct_no_2026_cut,
        count(*) FILTER (WHERE c2026 = 0) AS n_no_2026_cut,
        round(100.0 * avg(CAST(next_cut IS NULL AS INT)), 1) AS pct_no_cut_after_filing,
        round(100.0 * avg(CAST(mins <= 60 AS INT)), 1) AS pct_closed_within_60_min,
        round(median(mins), 1) AS median_minutes_to_close
        FROM req WHERE {where} GROUP BY 1 ORDER BY 1""")
    return {'label': label, 'rows': out}


ONS = "res_key LIKE 'on schedule to be cut%'"
LOTW = "problem_code = 'Weeds-Vacant Lot'"
B = {}
B['on_schedule_all'] = split(ONS, 'on schedule, lots and buildings', "'all'")
B['on_schedule_by_type'] = split(ONS, 'on schedule, by request type', 'problem_code')
B['added_to_rotation_by_type'] = split("res_key = 'added to rotation'", 'added to rotation, by type', 'problem_code')
B['on_schedule_by_maint'] = split(ONS, 'on schedule, by maintenance list category (2023 file)', "coalesce(maint_category, '(not on list)')")
B['on_schedule_lots_by_maint'] = split(f"{ONS} AND {LOTW}", 'on schedule, vacant-lot requests, by maintenance list', "coalesce(maint_category, '(not on list)')")
B['on_schedule_by_lra'] = split(ONS, 'on schedule, by land-bank ownership', "CASE WHEN is_lra THEN 'land bank' ELSE 'other' END")
B['on_schedule_lots_by_lra_maint'] = split(f"{ONS} AND {LOTW}", 'on schedule, vacant-lot requests, land bank x on any maintenance list',
                                           "CASE WHEN is_lra THEN 'land bank' ELSE 'other' END || ' | ' || CASE WHEN maint_category IS NULL THEN 'not on list' ELSE 'on list' END")
B['on_schedule_by_history'] = split(ONS, 'on schedule, by cut history',
    "CASE WHEN c2025 > 0 THEN 'cut in 2025' WHEN c2024 > 0 THEN 'cut in 2024, not 2025' WHEN c2019_24 > 0 THEN 'cut 2019-23 only' ELSE 'no cut 2019-25' END")
B['on_schedule_lots_by_history'] = split(f"{ONS} AND {LOTW}", 'on schedule, vacant-lot requests, by cut history',
    "CASE WHEN c2025 > 0 THEN 'cut in 2025' WHEN c2024 > 0 THEN 'cut in 2024, not 2025' WHEN c2019_24 > 0 THEN 'cut 2019-23 only' ELSE 'no cut 2019-25' END")
B['on_schedule_by_speed'] = split(ONS, 'on schedule, by closing speed',
    "CASE WHEN mins <= 60 THEN 'a) within 60 min' WHEN mins <= 1440 THEN 'b) 1-24 h' ELSE 'c) over 24 h' END")
B['on_schedule_lots_by_speed'] = split(f"{ONS} AND {LOTW}", 'on schedule, vacant-lot requests, by closing speed',
    "CASE WHEN mins <= 60 THEN 'a) within 60 min' WHEN mins <= 1440 THEN 'b) 1-24 h' ELSE 'c) over 24 h' END")
# lot-1's own profile: land bank, on maintenance list as Vacant Lot, cut 2019-24, no cut 2025
LIKE_LOT1 = "is_lra AND maint_category = 'Vacant Lot' AND c2025 = 0 AND c2019_24 > 0"
B['on_schedule_lot1_profile'] = split(f"{ONS} AND {LIKE_LOT1}", 'on schedule, parcels like lot-1 (land bank, list Vacant Lot, cut 2019-24, no cut 2025)', "'like lot-1'")
B['on_schedule_lra_listed_lots_cut2025_vs_not'] = split(f"{ONS} AND is_lra AND maint_category = 'Vacant Lot'",
    'on schedule, land-bank lots on the list as Vacant Lot, by 2025 cut', "CASE WHEN c2025 > 0 THEN 'cut in 2025' ELSE 'no cut 2025' END")
# share of all no-2026-cut on-schedule closures that are on the maintenance list
B['no_cut_on_schedule_composition'] = q(f"""SELECT count(*) AS requests, count(DISTINCT parcel) AS parcels,
    count(*) FILTER (WHERE maint_category IS NOT NULL) AS on_list, count(*) FILTER (WHERE is_lra) AS land_bank,
    count(*) FILTER (WHERE c2025 = 0) AS no_cut_2025, count(*) FILTER (WHERE c2019_24 > 0) AS cut_2019_24,
    count(*) FILTER (WHERE c2019_24 > 0 AND c2025 = 0) AS cut_2019_24_not_2025,
    count(*) FILTER (WHERE mins <= 60) AS closed_within_60_min
    FROM req WHERE {ONS} AND c2026 = 0""")[0]
# speed, cut vs not cut (the same question at city scale)
B['speed_by_outcome'] = q(f"""SELECT CASE WHEN c2026 > 0 THEN 'parcel cut in 2026' ELSE 'no 2026 cut' END AS outcome, count(*) n,
    round(median(mins), 1) AS median_minutes, round(100.0 * avg(CAST(mins <= 60 AS INT)), 1) AS pct_within_60_min,
    round(100.0 * avg(CAST(mins <= 1440 AS INT)), 1) AS pct_within_24h
    FROM req WHERE {ONS} GROUP BY 1 ORDER BY 1""")

# R1 replication: units (parcel, filing date) with at least one same-block 2026-cut control parcel lacking a weed request in the 60 days up to D
con.execute("""CREATE TEMP TABLE wreq AS
  SELECT DISTINCT rp.pid AS parcel, r.init_date AS d FROM s.requests r JOIN s.request_parcel rp USING (request_id)
  WHERE r.problem_code IN (SELECT problem_code FROM s.weed_ledger_codes) OR r.problem_code IN ('Weeds-Occupied Ppty', 'Debris-Vacant Lot', 'Debris-Vacant Bldg')""")
con.execute("CREATE TEMP TABLE rot AS SELECT DISTINCT parcel FROM c26")
con.execute("""CREATE TEMP TABLE unit AS
  SELECT parcel, init_date AS d, bool_or(res_key LIKE 'on schedule to be cut%') AS any_on_schedule, bool_and(res_key = 'added to rotation') AS only_added,
         any_value(c2026) AS c2026, any_value(maint_category) AS maint_category, bool_or(is_lra) AS is_lra, any_value(c2025) AS c2025,
         any_value(c2019_24) AS c2019_24, any_value(problem_code) AS problem_code
  FROM req GROUP BY parcel, init_date""")
# R1's own block table: MSD parcels only (our pblock also adds ledger-only parcels, which gives 1,762 / 540)
con.execute("""CREATE TEMP TABLE pblock_r1 AS SELECT p.pid AS parcel, coalesce(l.cityblock, substr(p.handle, 2, 6)) AS cityblock
  FROM s.parcels p LEFT JOIN lblock l ON l.parcel = p.pid""")
con.execute("""CREATE TEMP TABLE unit_ctl AS
  SELECT u.* FROM unit u JOIN pblock_r1 b ON b.parcel = u.parcel
  WHERE EXISTS (SELECT 1 FROM pblock_r1 pb WHERE pb.cityblock = b.cityblock AND pb.parcel <> u.parcel
                AND EXISTS (SELECT 1 FROM rot WHERE rot.parcel = pb.parcel)
                AND NOT EXISTS (SELECT 1 FROM wreq w WHERE w.parcel = pb.parcel AND w.d BETWEEN u.d - 60 AND u.d))""")
B['r1_replication'] = one("""SELECT count(*) AS units, count(*) FILTER (WHERE c2026 = 0) AS units_no_2026_cut,
    round(100.0 * avg(CAST(c2026 = 0 AS INT)), 1) AS pct,
    count(*) FILTER (WHERE c2026 = 0 AND any_on_schedule) AS no_cut_on_schedule_units,
    count(*) FILTER (WHERE c2026 = 0 AND only_added) AS no_cut_added_to_rotation_only_units,
    count(*) FILTER (WHERE any_on_schedule) AS on_schedule_units,
    round(100.0 * avg(CAST(c2026 = 0 AS INT)) FILTER (WHERE any_on_schedule), 1) AS pct_no_cut_among_on_schedule_units,
    count(*) FILTER (WHERE c2026 = 0 AND maint_category IS NOT NULL) AS no_cut_on_list,
    count(*) FILTER (WHERE c2026 = 0 AND is_lra) AS no_cut_land_bank,
    count(*) FILTER (WHERE c2026 = 0 AND c2019_24 > 0) AS no_cut_but_cut_2019_24
    FROM unit_ctl""")
B['lot1_in_r1_539'] = one("SELECT count(*) AS lot1_units, count(*) FILTER (WHERE c2026 = 0) AS lot1_units_no_cut FROM unit_ctl WHERE parcel = ?", [LOT])
RES['B_citywide'] = B

# ------------------------------------------------------------------ Part C: does falling off persist?
C = {}
C['lra_list_lots_cut_2024'] = q("""SELECT CASE WHEN coalesce(h.c2025, 0) > 0 THEN 'cut in 2025' ELSE 'no cut 2025' END AS y2025,
    count(*) AS parcels, count(*) FILTER (WHERE coalesce(h.c2026, 0) > 0) AS cut_2026,
    round(100.0 * avg(CAST(coalesce(h.c2026, 0) > 0 AS INT)), 1) AS pct_cut_2026
    FROM lra l JOIN maint m USING (parcel) JOIN hist h USING (parcel)
    WHERE m.category = 'Vacant Lot' AND h.c2024 > 0 GROUP BY 1 ORDER BY 1""")
C['lra_list_lots_all'] = one("""SELECT count(*) AS parcels, count(*) FILTER (WHERE coalesce(h.c2026, 0) > 0) AS cut_2026,
    count(*) FILTER (WHERE coalesce(h.c2026, 0) = 0 AND coalesce(h.c2025, 0) = 0 AND coalesce(h.c2019_24, 0) > 0) AS like_lot1_no_cut_2025_26,
    count(*) FILTER (WHERE coalesce(h.c2026, 0) = 0) AS no_cut_2026
    FROM lra l JOIN maint m USING (parcel) LEFT JOIN hist h USING (parcel) WHERE m.category = 'Vacant Lot'""")
C['like_lot1_with_2026_on_schedule_report'] = one(f"""SELECT count(DISTINCT parcel) AS parcels, count(*) AS requests FROM req
    WHERE {ONS} AND {LIKE_LOT1} AND c2026 = 0""")
# 2025 thinness check on the block's ward-level neighbours is in A; citywide parcels cut per year
C['parcels_cut_per_year'] = q("SELECT y, count(DISTINCT parcel) AS parcels FROM cy WHERE y BETWEEN 2022 AND 2026 GROUP BY y ORDER BY y")
RES['C_persistence'] = C

# ------------------------------------------------------------------ Part D: route, crews on the block, innocent explanations
D = {}
D['lot1_cut_days_shared_with_block_by_year'] = q("""SELECT year(c.service_date) AS y, count(*) AS lot1_cut_days,
    count(*) FILTER (WHERE EXISTS (SELECT 1 FROM s.cuts c2 WHERE c2.service_date = c.service_date AND c2.parcel IN (SELECT parcel FROM blk) AND c2.parcel <> ?)) AS shared_with_block
    FROM (SELECT DISTINCT service_date FROM s.cuts WHERE parcel = ? AND year(service_date) BETWEEN 2019 AND 2024) c GROUP BY 1 ORDER BY 1""", [LOT, LOT])
for d in ('2026-07-02', '2026-07-28', '2026-09-09'):
    D[f'block_after_{d}'] = one(f"""SELECT count(DISTINCT d) AS cut_days, count(DISTINCT parcel) AS parcels_cut
        FROM c26 WHERE parcel IN (SELECT parcel FROM blk) AND parcel <> ? AND d >= DATE '{d}'""", [LOT])
# route-mates: parcels billed on every one of lot-1's 2023-24 cut dates (same weekly posting batches)
con.execute("CREATE TEMP TABLE ld AS SELECT DISTINCT service_date AS d FROM s.cuts WHERE parcel = ? AND year(service_date) IN (2023, 2024)", [LOT])
NLD = one("SELECT count(*) n FROM ld")['n']
con.execute("""CREATE TEMP TABLE mates AS SELECT c.parcel FROM s.cuts c JOIN ld ON c.service_date = ld.d
    WHERE c.parcel <> ? GROUP BY 1 HAVING count(DISTINCT c.service_date) = ?""", [LOT, NLD])
D['route_mates'] = one("""SELECT ? AS lot1_cut_dates_2023_24, count(*) AS parcels_billed_on_all_those_dates,
    count(*) FILTER (WHERE parcel IN (SELECT parcel FROM lra)) AS land_bank,
    count(*) FILTER (WHERE parcel IN (SELECT parcel FROM maint WHERE category = 'Vacant Lot')) AS list_vacant_lot,
    count(*) FILTER (WHERE parcel IN (SELECT parcel FROM blk)) AS on_lot1_block,
    count(DISTINCT (SELECT cityblock FROM pblock pb WHERE pb.parcel = m.parcel)) AS city_blocks,
    count(*) FILTER (WHERE coalesce((SELECT c2025 FROM hist h WHERE h.parcel = m.parcel), 0) > 0) AS cut_2025,
    count(*) FILTER (WHERE coalesce((SELECT c2026 FROM hist h WHERE h.parcel = m.parcel), 0) > 0) AS cut_2026,
    count(*) FILTER (WHERE EXISTS (SELECT 1 FROM c26 WHERE c26.parcel = m.parcel AND c26.d >= DATE '2026-07-28')) AS cut_after_28_jul_2026
    FROM mates m""", [NLD])
D['route_mates_2026_days'] = one("""SELECT count(DISTINCT d) AS cut_days, min(d) AS first, max(d) AS last,
    count(DISTINCT d) FILTER (WHERE d IN (SELECT d FROM c26 WHERE parcel IN (SELECT parcel FROM blk))) AS days_shared_with_lot1_block
    FROM c26 WHERE parcel IN (SELECT parcel FROM mates)""")
# land-bank neighbours not cut in 2026
D['land_bank_neighbours_not_cut_2026'] = q("""SELECT b.parcel IS NOT NULL AS x,
    count(*) AS parcels, count(*) FILTER (WHERE r.weed_reports > 0) AS with_report,
    list(DISTINCT (SELECT arg_max(property_type, service_date) FROM s.ledger g WHERE g.parcel = l.parcel AND g.service_type IN ('Grass Maint', 'Weed-Grass'))) AS ledger_types,
    list(DISTINCT (SELECT year(max(service_date)) FROM s.cuts c WHERE c.parcel = l.parcel)) AS last_cut_years
    FROM lra l JOIN blk b USING (parcel)
    LEFT JOIN (SELECT parcel, count(*) FILTER (WHERE problem_code IN ('Weeds-Vacant Lot', 'Weeds-Vacant Bldg')) AS weed_reports FROM blk_req GROUP BY 1) r USING (parcel)
    WHERE l.parcel <> ? AND coalesce((SELECT c2026 FROM hist h WHERE h.parcel = l.parcel), 0) = 0 GROUP BY 1""", [LOT])
# innocent explanations in the land-bank side files (counts of rows naming the lot's parcel id)
RAWF = ROOT / 'data/raw/stlouis-mo.gov/files'
side = {}
for fn in ('LRA_OFFERS.csv', 'LRA_OFFERS_ARCHIVE_GEOSTL.csv', 'LRA_GARDEN_PERMITS.csv', 'SLDC_LRA_PROPNS_NOMINEES.csv',
           'LRA_INVENTORY.csv', 'LRA_INVENTORY_AVAILABLE.csv'):
    with open(RAWF / fn, errors='replace') as fh:
        side[fn] = sum(1 for line in fh if LOT in line)
D['lot1_rows_in_land_bank_files'] = side
con.execute(f"CREATE TEMP TABLE inv AS SELECT * FROM read_csv('{RAWF / 'LRA_INVENTORY.csv'}', all_varchar=true, header=true)")
D['lot1_inventory'] = one("""SELECT Parcel_Status, Property_Source, regexp_extract(ACQUISITION_DATE, '(\\d{4})', 1) AS acquisition_year,
    try_cast(SQFT AS DOUBLE) AS sqft FROM inv WHERE ParcelId = ?""", [LOT])
D['block_land_bank_sqft_median'] = one("SELECT median(try_cast(SQFT AS DOUBLE)) AS m, count(*) AS n FROM inv WHERE ParcelId IN (SELECT parcel FROM blk) AND ParcelId <> ?", [LOT])
D['ledger_columns_raw'] = open(RAWF / 'forestry-service-records.csv').readline().strip().replace('"', '').split(',')
RES['D_route_and_checks'] = D

(OUT / 'mechanism.json').write_text(json.dumps(RES, indent=1, default=str))
print(json.dumps({k: v for k, v in RES.items() if k != 'definition'}, indent=1, default=str))
