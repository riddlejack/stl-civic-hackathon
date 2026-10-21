"""Impact 3-5: physical units the fix would surface or recover.

A. Hand-off closures by hand (volume for the auto-close labour estimate).
B. City-owned (land-bank) parcels with a 2026 weed report closed at the hand-off
   ("on schedule to be cut ..." or "added to rotation") and no cut billed at any time
   in 2026 or after filing; plus the season cost to cut them at the city's own billed
   2026 amounts per land-bank parcel.
C. Tier-1 (life-safety) requests in the E5 past-due ledger: count, by code, days past
   the promise (tier map: site/data/rank-weights.json, research/prioritisation-option.md).
D. Open Forestry removal work orders (Cityworks QE layer 63 "Tree Removal WOs", extract
   of 14 Oct 2026) whose ProjectedFinishDate has passed.
E. The 12,566 "no record either way" (E5 class e): split by whether the type ever
   attaches work on the status page (E1/E5 sample), to bound what linking would reveal.

Reads build/stl.duckdb READ-ONLY, build/E5/private/ledger_rows.parquet,
data/raw/cityworks-gap/extracts/layer_63_rows.json and layer_90/102 rows.
Writes aggregates only (no ids, no addresses) to build/impact/service.json.
Run: python3 -I scripts/exec/impact/02_service.py
"""
import datetime as dt
import json
import os
import statistics as st

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB = os.path.join(ROOT, 'build', 'stl.duckdb')
E5 = os.path.join(ROOT, 'build', 'E5', 'private', 'ledger_rows.parquet')
RAW = os.path.join(ROOT, 'data', 'raw', 'cityworks-gap', 'extracts')
OUT = os.path.join(ROOT, 'build', 'impact')
W = json.load(open(os.path.join(ROOT, 'site', 'data', 'rank-weights.json')))
T1 = set(W['tiers']['1']['codes'])
T2 = set(W['tiers']['2']['codes'])

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
q = lambda sql, *a: con.execute(sql, *a).fetchall()
R = {}

# ---------------------------------------------------------------- A. hand-off closure volume
R['A_handoff_closures'] = dict(zip(
    ['filed_2025_to_asof', 'closed_in_12m_to_asof', 'filed_2025', 'first_init', 'last_init'],
    q("""SELECT count(*), count(*) FILTER (WHERE ts_closed > (SELECT asof_ts FROM s.run_dates) - INTERVAL 365 DAY),
         count(*) FILTER (WHERE init_year = 2025), min(ts_init)::VARCHAR, max(ts_init)::VARCHAR
         FROM s.v_requests WHERE closure_class IN ('handed_off','converted') AND ts_init >= TIMESTAMP '2025-01-01'""")[0]))
R['A_all_closed_12m'] = q("""SELECT count(*) FROM s.v_requests WHERE status_group='closed'
    AND ts_closed > (SELECT asof_ts FROM s.run_dates) - INTERVAL 365 DAY""")[0][0]

# ---------------------------------------------------------------- B. land-bank lots told "on schedule", no cut
WEED = "('Weeds-Vacant Lot','Weeds-Vacant Bldg','Missed Cut - V Lot','Missed Cut - VBldg','Unsatisfy Cut - VLot','Unsatisfy Cut -VBldg')"
con.execute("CREATE TEMP TABLE lra AS SELECT DISTINCT parcel_id AS parcel FROM s.lra")
con.execute("CREATE TEMP TABLE c26 AS SELECT parcel, count(DISTINCT service_date) AS n, min(service_date) AS first, max(service_date) AS last FROM s.cuts WHERE year(service_date) = 2026 GROUP BY 1")
con.execute(f"""CREATE TEMP TABLE wr AS
  SELECT r.request_id, rp.pid AS parcel, r.problem_code, r.init_date, r.res_key,
         rp.pid IN (SELECT parcel FROM lra) AS is_lra,
         coalesce(c.n, 0) AS cuts_2026,
         (SELECT min(service_date) FROM s.cuts k WHERE k.parcel = rp.pid AND k.service_date >= r.init_date) AS next_cut
  FROM s.v_requests r JOIN s.request_parcel rp USING (request_id) LEFT JOIN c26 c ON c.parcel = rp.pid
  WHERE r.problem_code IN {WEED} AND r.init_year = 2026 AND r.status_group = 'closed'
    AND r.init_date <= DATE '2026-09-13'
    AND (r.res_key LIKE 'on schedule to be cut%' OR r.res_key = 'added to rotation'
         OR r.closure_class IN ('handed_off','converted'))""")
B = {}
for label, where in [
        ('strict_on_schedule_no_2026_cut', "is_lra AND res_key LIKE 'on schedule to be cut%' AND cuts_2026 = 0 AND problem_code IN ('Weeds-Vacant Lot','Weeds-Vacant Bldg')"),
        ('handoff_any_words_no_2026_cut', "is_lra AND cuts_2026 = 0"),
        ('handoff_any_words_no_cut_after_filing', "is_lra AND next_cut IS NULL"),
        ('all_lra_handoff_weed_requests', "is_lra")]:
    B[label] = dict(zip(['requests', 'parcels'], q(f"SELECT count(*), count(DISTINCT parcel) FROM wr WHERE {where}")[0]))
B['by_words_no_2026_cut'] = q("""SELECT CASE WHEN res_key LIKE 'on schedule to be cut%' THEN 'on schedule' WHEN res_key='added to rotation' THEN 'added to rotation' ELSE 'other hand-off' END,
    count(*), count(DISTINCT parcel) FROM wr WHERE is_lra AND cuts_2026 = 0 GROUP BY 1 ORDER BY 1""")
# land-bank parcels on the 2023 maintenance list as vacant lot, with no 2026 cut (the pool the list covers)
B['lra_maint_vacant_lot_no_2026_cut'] = q("""SELECT count(DISTINCT m.parcel_id) FILTER (WHERE NOT EXISTS (SELECT 1 FROM c26 WHERE c26.parcel = m.parcel_id)),
    count(DISTINCT m.parcel_id) FROM s.maint_props m WHERE m.category = 'Vacant Lot' AND m.parcel_id IN (SELECT parcel FROM lra)""")[0]
# season cost per land-bank parcel cut in 2026, from the ledger (all 2026 mowing charges)
cost = q("""SELECT parcel, sum(service_amount) AS amt, count(DISTINCT service_date) AS dates
    FROM s.ledger WHERE year(service_date) = 2026 AND service_type IN ('Grass Maint','Weed-Grass')
      AND parcel IN (SELECT parcel FROM lra) GROUP BY 1""")
amts = sorted(x[1] for x in cost)
dates = sorted(x[2] for x in cost)
pct = lambda v, p: v[min(len(v) - 1, int(p * len(v)))]
B['lra_2026_season'] = {'parcels': len(cost), 'total_billed': round(sum(amts)), 'mean_per_parcel': round(st.mean(amts), 2),
                        'median_per_parcel': round(st.median(amts), 2), 'p25': round(pct(amts, .25), 2), 'p75': round(pct(amts, .75), 2),
                        'median_cut_dates': st.median(dates), 'mean_cut_dates': round(st.mean(dates), 2),
                        'ledger_last_date': str(q("SELECT max(service_date) FROM s.ledger")[0][0])}
B['grass_maint_2026_per_charge'] = dict(zip(['n', 'median', 'mean'], q("""SELECT count(*), median(service_amount), round(avg(service_amount), 2)
    FROM s.ledger WHERE year(service_date) = 2026 AND service_type = 'Grass Maint' AND parcel IN (SELECT parcel FROM lra)""")[0]))
# land-bank parcels with a 2026 weed report whose parcel WAS cut: their 2026 billed amount (a like-for-like season cost)
B['lra_reported_and_cut_2026_season'] = dict(zip(['parcels', 'median', 'mean'], q("""SELECT count(*), median(amt), round(avg(amt), 2) FROM (
    SELECT l.parcel, sum(service_amount) amt FROM s.ledger l WHERE year(service_date)=2026 AND service_type IN ('Grass Maint','Weed-Grass')
      AND l.parcel IN (SELECT parcel FROM wr WHERE is_lra AND cuts_2026 > 0) GROUP BY 1)""")[0]))
R['B_land_bank'] = B

# ---------------------------------------------------------------- C. tier-1 past-due requests
con.execute(f"CREATE TEMP VIEW L AS SELECT * FROM '{E5}'")
rows = q("SELECT problem_code, type_name, days_past_promise, cls, init_year FROM L")
tier = lambda pc: 1 if pc in T1 else 2 if pc in T2 else 3
t1 = [r for r in rows if tier(r[0]) == 1]
t1r = [r for r in t1 if r[3] not in ('a_done_after_filing', 'c_possibly_superseded', 'd_admin_leftover')]
C = {'base_rows': len(rows), 'tier1_all': len(t1), 'tier1_ranked_list': len(t1r),
     'tier1_median_days_past': st.median([r[2] for r in t1]), 'tier1_ranked_median_days_past': st.median([r[2] for r in t1r]),
     'tier1_ranked_over_90d': sum(1 for r in t1r if r[2] > 90), 'tier1_ranked_over_365d': sum(1 for r in t1r if r[2] > 365),
     'tier1_ranked_class_e_no_record': sum(1 for r in t1r if r[3] == 'e_no_evidence'),
     'tier1_ranked_class_b_pending': sum(1 for r in t1r if r[3] == 'b_pending_in_records'),
     'classes_seen': sorted(set(r[3] for r in rows))}
byc = {}
for r in t1r:
    byc.setdefault(r[0], []).append(r[2])
C['tier1_ranked_by_code'] = sorted([(k, len(v), st.median(v)) for k, v in byc.items()], key=lambda x: -x[1])
trees = [d for k, v in byc.items() if k in ('City Tree Down', 'City Tree Limb Down', 'Broken/Hanging Limb') for d in v]
C['tier1_trees_limbs'] = {'n': len(trees), 'median_days_past': st.median(trees) if trees else None}
R['C_tier1'] = C

# ---------------------------------------------------------------- D. open removal work orders past projected finish
ASOF = dt.datetime(2026, 10, 13, tzinfo=dt.timezone.utc)


def ts(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return dt.datetime.fromtimestamp(v / 1000, tz=dt.timezone.utc)
    try:
        return dt.datetime.fromisoformat(str(v).replace('Z', '+00:00'))
    except ValueError:
        return None


D = {}
for layer in (63, 90, 102):
    p = os.path.join(RAW, f'layer_{layer}_rows.json')
    if not os.path.exists(p):
        D[f'layer_{layer}'] = 'missing'
        continue
    rr = json.load(open(p))
    op = [x for x in rr if not x.get('ActualFinishDate') and not x.get('DateWOClosed') and not x.get('IsCancelled') in (True, 'true', 1)]
    pf = [ts(x.get('ProjectedFinishDate')) for x in op]
    past = [(ASOF - f).days for f in pf if f and f < ASOF]
    ages = [(ASOF - ts(x['InitiateDate'])).days for x in op if ts(x.get('InitiateDate'))]
    D[f'layer_{layer}'] = {'rows': len(rr), 'open_no_finish': len(op), 'with_projected_finish': sum(1 for f in pf if f),
                           'past_projected_finish': len(past), 'median_days_past_projected': st.median(past) if past else None,
                           'past_over_365d': sum(1 for d in past if d > 365),
                           'median_age_days_since_initiate': st.median(ages) if ages else None,
                           'statuses': sorted({x.get('Status') for x in rr})}
R['D_removals'] = D

# ---------------------------------------------------------------- E. the 12,566 "no record either way"
e = q("SELECT type_name, count(*) FROM L WHERE cls = 'e_no_evidence' GROUP BY 1 ORDER BY 2 DESC")
R['E_no_record'] = {'total': sum(x[1] for x in e), 'top_types': e[:15]}
json.dump(R, open(os.path.join(OUT, 'service.json'), 'w'), indent=1, default=str)
print(json.dumps(R, indent=1, default=str))
