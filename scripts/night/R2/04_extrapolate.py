"""R2 step 4: bounded extrapolation of crew-work hand-offs that may never be done.

LABEL: ESTIMATE. Nothing here is observed completion; it applies completion
rates MEASURED by R1 on the traceable services (weeds on vacant property via the
Forestry ledger; board-ups via the Building Division layer) to crew-work
hand-offs that have no public completion record, by category, with a stated
plausibility judgement per category.

Inputs (read-only): build/stl.duckdb (N1), build/R1/handoff_composition.csv and
build/R1/fate_summary.json (R1), build/R2/private/closure_measures.parquet (R2 step 1).
Outputs: build/R2/extrapolation.csv, build/R2/extrapolation.json.
Run: .venv/bin/python -I scripts/night/R2/04_extrapolate.py
"""
import csv
import json
import math
import os

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB = os.path.join(ROOT, 'build', 'stl.duckdb')
R1C = os.path.join(ROOT, 'build', 'R1', 'handoff_composition.csv')
R1F = os.path.join(ROOT, 'build', 'R1', 'fate_summary.json')
PQ = os.path.join(ROOT, 'build', 'R2', 'private', 'closure_measures.parquet')
OUT = os.path.join(ROOT, 'build', 'R2')

# ------------------------------------------------------------------ 1. measured rates (R1)
fate = json.load(open(R1F))
svc = {s['service']: s for s in fate['by_service']}
MAIN = ['Weeds, vacant lot (2026 filings)',
        'Missed or unsatisfactory cut complaints (2026 filings)',
        'Referred to board-up crew (2025-26 filings)']
# Vacant-building weeds: the 2026 Grass Maint ledger may not bill contractor cuts on vacant-building lots
# (N1/N5 caveat), so R1's 2025 sensitivity row (Weed-Grass ledger complete) stands in for it.
VB_2026 = 'Weeds, vacant building (2026 filings)'
VB_2025 = [k for k in svc if k.startswith('SENSITIVITY Weeds, vacant building')]
used = MAIN + VB_2025
rates = {k: {'no_record': svc[k]['share_no_record'], 'late': svc[k]['share_done_late'],
             'by_promise': svc[k]['share_done_by_promise'], 'n_due': svc[k]['n_due']} for k in used if k in svc}
never_low = min(v['no_record'] for v in rates.values())
never_high = max(v['no_record'] for v in rates.values())
late_low = min(v['late'] for v in rates.values())
late_high = max(v['late'] for v in rates.values())
never_high_sens = svc[VB_2026]['share_no_record'] if VB_2026 in svc else None

# ------------------------------------------------------------------ 2. untraced crew-work volume by category, 12 months to the file's as-of time
CATEGORY_SQL = """
CASE
  WHEN lower(phrase) LIKE '%not funded%' OR lower(phrase) LIKE '%aldermanic funding%' OR lower(phrase) LIKE '%aldermanic approval%'
       THEN 'unfunded (closing words say no funding)'
  WHEN problem_code LIKE 'Snow/Ice%' THEN 'snow and ice (self-resolving)'
  WHEN problem_code = 'Tree Planting requst' AND lower(phrase) = 'approved for next available planting' THEN 'tree planting (traced by R2, step 6)'
  WHEN problem_code = 'Bulky items missed' OR lower(phrase) LIKE 'bulk will be picked up%' THEN 'bulky pick-up'
  WHEN division = 'REFUSE' AND (lower(phrase) LIKE 'collection will be made%' OR lower(phrase) LIKE 'due to employee shortage%')
       THEN 'refuse, recycling, yard-waste collection'
  WHEN division = 'REFUSE' THEN 'refuse containers and other refuse jobs'
  WHEN problem_code IN ('Vehicle Towing', 'Illegal Use') AND lower(phrase) IN ('vehicle tagged for tow', 'work in progress') AND division <> 'TREASURER'
       THEN 'towing'
  WHEN division = 'WATER DIV' THEN 'water repairs'
  WHEN problem_code IN ('Cave-Ins', 'STREET-CAVEIN', 'WALK-CAVEIN', 'LAWN-CAVEIN', 'Potholes - Residnl', 'Potholes - Major St', 'Potholes - Alley',
                        'Other Street Repair', 'Other Alley Repair', 'Bad Condition', 'Sewer Lateral Defect', 'Sidewalk Repair', 'Misc-Street Div')
       THEN 'street, alley and sidewalk repair'
  WHEN problem_code IN ('Debris-alley/street', 'Street Cleaning', 'Debris-Vacant Lot', 'Debris-Vacant Bldg', 'Illegal dumpg report',
                        'Bagged Leaf Pickup', 'Leaf pick up') THEN 'debris and street cleaning'
  WHEN division LIKE 'TRAFFIC%' THEN 'traffic signals, signs, lights, striping'
  WHEN division IN ('FORESTRY', 'PARKS DIV') THEN 'forestry and parks'
  ELSE 'other crew work'
END
"""
TIER = {
    'unfunded (closing words say no funding)': 'separate',
    'snow and ice (self-resolving)': 'excluded',
    'bulky pick-up': 'routine',
    'refuse, recycling, yard-waste collection': 'routine',
    'tree planting (traced by R2, step 6)': 'traced',
}
REASON = {
    'refuse, recycling, yard-waste collection': 'The truck passes every address on a fixed weekly route, so the job is redone by routine; the closing words promise the next scheduled day. Low bound 0; high bound = this category\'s own excess re-report rate within 7 days of closure over "done" closures of the same types.',
    'bulky pick-up': 'Bulk is collected in scheduled weeks on a route, so a missed item is collected by routine; high bound = own excess re-report rate within 7 days over "done" closures.',
    'snow and ice (self-resolving)': 'Snow and ice melt; "never done" has no meaning here. Excluded.',
    'tree planting (traced by R2, step 6)': 'Now traced: the maps8 planting layers date street-tree plantings (Nov 2025 to Sep 2026); see tree_planting_fate.json. Observed, so not extrapolated.',
    'unfunded (closing words say no funding)': 'The closing words themselves say the work is not funded; counted separately, not given a rate.',
    'towing': 'One-off crew job with a backlog (311 median close 15 days against a 5-day promise). A tagged vehicle may also be moved by its owner, which ends the problem without the crew; full measured range applied, which may overstate.',
    'water repairs': 'One-off Water Division repair; closed in hours as "scheduled for repair", no public repair record (the live outage list has no history). Full range applied.',
    'street, alley and sidewalk repair': 'One-off Street Department repair after a referral or inspection; no public repair record (the pothole saved search is not independent of 311; the sidewalk DateRepair field is empty). Full range applied.',
    'debris and street cleaning': 'One-off clean-up dispatched to a crew, often at chronic sites; Forestry stopped recording lot debris clean-ups after 2021. Full range applied.',
    'traffic signals, signs, lights, striping': 'One-off Traffic Division job (parts on order, timing under study, seasonal striping); no public record. Full range applied.',
    'forestry and parks': 'Tree planting queue ("next available planting"), tree work orders (open-order sample has no finish dates), parks repairs and mowing; no public finish record. Full range applied.',
    'refuse containers and other refuse jobs': 'Container repairs, deliveries and complaints routed to Refuse ("matter will be investigated"); one-off jobs with no record. Full range applied.',
    'other crew work': 'Small remaining crew-work closures. Full range applied.',
}

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
con.execute(f"CREATE TEMP TABLE r1 AS SELECT * FROM read_csv_auto('{R1C}', header=true)")
con.execute(f"""
CREATE TEMP TABLE ho AS
SELECT r.request_id, r.problem_code, r.division, lower(trim(r.resolution_public)) AS phrase, r.ts_init, r.addr_norm,
       m.kind, m.traceability, m.record
FROM s.v_requests r JOIN r1 m ON m.problem_code = r.problem_code AND m.closing_phrase = lower(trim(r.resolution_public))
WHERE r.status_group = 'closed' AND r.closure_class IN ('handed_off', 'converted') AND r.ts_init >= TIMESTAMP '2025-01-01';
CREATE TEMP TABLE hoc AS SELECT *, {CATEGORY_SQL} AS category FROM ho;
""")
asof = con.execute("SELECT asof_ts FROM s.run_dates").fetchone()[0]
vol = con.execute("""
SELECT category,
       count(*) FILTER (WHERE ts_init > (SELECT asof_ts FROM s.run_dates) - INTERVAL 365 DAY) AS v12,
       count(DISTINCT (addr_norm, problem_code)) FILTER (WHERE ts_init > (SELECT asof_ts FROM s.run_dates) - INTERVAL 365 DAY AND addr_norm <> '') AS v12_distinct_addr_type,
       count(*) FILTER (WHERE year(ts_init) = 2025) AS v2025,
       count(*) AS v_2025_26
FROM hoc WHERE kind = 'crew_work' AND traceability IN ('none', 'partial')
GROUP BY 1 ORDER BY 2 DESC""").fetchall()
traced_vol = con.execute("""
SELECT count(*) FILTER (WHERE ts_init > (SELECT asof_ts FROM s.run_dates) - INTERVAL 365 DAY) FROM hoc
WHERE kind = 'crew_work' AND traceability = 'traceable'""").fetchone()[0]
kinds_vol = con.execute("""
SELECT kind, traceability, count(*) FILTER (WHERE ts_init > (SELECT asof_ts FROM s.run_dates) - INTERVAL 365 DAY) FROM hoc GROUP BY ALL ORDER BY 1, 2""").fetchall()

# ------------------------------------------------------------------ 3. each category's own re-report evidence (hand-off vs done, same types)
con.execute(f"CREATE TEMP VIEW m AS SELECT * FROM '{PQ}' WHERE has_addr")
con.execute(f"""
CREATE TEMP TABLE mc AS
SELECT m.*, CASE WHEN m.cls = 'handoff' THEN {CATEGORY_SQL.replace('phrase', 'm.closing_phrase').replace('problem_code', 'm.problem_code').replace('division', 'm.division')} END AS category
FROM m""")


def own_evidence(cat, wflag, outcome):
    rows = con.execute(f"""
    WITH h AS (SELECT problem_code, count(*) AS na, count(*) FILTER (WHERE {outcome}) AS ya FROM mc
               WHERE cls = 'handoff' AND kind = 'crew_work' AND traceability IN ('none', 'partial') AND category = ? AND {wflag} GROUP BY 1),
         d AS (SELECT problem_code, count(*) AS nb, count(*) FILTER (WHERE {outcome}) AS yb FROM mc WHERE cls = 'done' AND {wflag} GROUP BY 1)
    SELECT h.problem_code, na, ya, nb, yb FROM h JOIN d USING (problem_code) WHERE na >= 30 AND nb >= 30""", [cat]).fetchall()
    if not rows:
        return None
    W = sum(r[1] for r in rows)
    pa = sum(r[2] for r in rows) / W
    pb = sum(r[1] * r[4] / r[3] for r in rows) / W
    return {'types': len(rows), 'n_handoff': W, 'handoff_pct': round(100 * pa, 1), 'done_same_types_pct': round(100 * pb, 1),
            'excess_pts': round(100 * (pa - pb), 1)}


out_rows = []
tot = {'low': 0.0, 'high': 0.0, 'mech_low': 0.0, 'mech_high': 0.0, 'late_low': 0.0, 'late_high': 0.0, 'v12': 0,
       'low_2025': 0.0, 'high_2025': 0.0, 'v2025': 0}
for cat, v12, v12d, v2025, vall in vol:
    tier = TIER.get(cat, 'full')
    ev7 = own_evidence(cat, 'w7', 'coalesce(d_any <= 7, false)')
    ev14 = own_evidence(cat, 'w14', 'coalesce(d_any <= 14, false)')
    evf = own_evidence(cat, 'wf', 'df IS NOT NULL')
    if tier == 'full':
        lo, hi = never_low * v12, never_high * v12
        llo, lhi = late_low * v12, late_high * v12
    elif tier == 'routine':
        exc = max(0.0, (ev7 or {}).get('excess_pts', 0.0)) / 100.0
        lo, hi = 0.0, exc * v12
        llo, lhi = 0.0, 0.0
    else:
        lo = hi = llo = lhi = 0.0
    mech_lo, mech_hi = (never_low * v12, never_high * v12) if tier not in ('excluded', 'traced') else (0.0, 0.0)
    # sensitivity: calendar-2025 volume (a tornado year, and a refuse staff-shortage year) instead of the last 12 months
    if tier == 'full':
        tot['low_2025'] += never_low * v2025; tot['high_2025'] += never_high * v2025
    elif tier == 'routine':
        tot['high_2025'] += max(0.0, (ev7 or {}).get('excess_pts', 0.0)) / 100.0 * v2025
    if tier not in ('traced',):
        tot['v2025'] += v2025
    if tier not in ('separate', 'traced'):
        tot['low'] += lo; tot['high'] += hi
        tot['mech_low'] += mech_lo; tot['mech_high'] += mech_hi
        tot['late_low'] += llo; tot['late_high'] += lhi
    if tier != 'traced':
        tot['v12'] += v12
    out_rows.append({'category': cat, 'tier': tier, 'requests_12m': v12, 'distinct_address_type_12m': v12d,
                     'requests_2025': v2025, 'requests_2025_26': vall,
                     'never_low': round(lo), 'never_high': round(hi), 'mechanical_low': round(mech_lo), 'mechanical_high': round(mech_hi),
                     'late_low': round(llo), 'late_high': round(lhi),
                     'own_rereport_7d': ev7, 'own_rereport_14d': ev14, 'own_rereport_filing_day15_44': evf,
                     'reason': REASON.get(cat, '')})

with open(os.path.join(OUT, 'extrapolation.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['category', 'tier', 'requests_12m', 'distinct_address_type_12m', 'requests_2025', 'requests_2025_26',
                'never_low', 'never_high', 'mechanical_low', 'mechanical_high', 'late_low', 'late_high',
                'handoff_rr7_pct', 'done_same_types_rr7_pct', 'handoff_rr14_pct', 'done_same_types_rr14_pct',
                'handoff_filing_day15_44_pct', 'done_same_types_filing_day15_44_pct', 'reason'])
    for r in out_rows:
        e7, e14, ef = r['own_rereport_7d'] or {}, r['own_rereport_14d'] or {}, r['own_rereport_filing_day15_44'] or {}
        w.writerow([r['category'], r['tier'], r['requests_12m'], r['distinct_address_type_12m'], r['requests_2025'], r['requests_2025_26'],
                    r['never_low'], r['never_high'], r['mechanical_low'], r['mechanical_high'], r['late_low'], r['late_high'],
                    e7.get('handoff_pct'), e7.get('done_same_types_pct'), e14.get('handoff_pct'), e14.get('done_same_types_pct'),
                    ef.get('handoff_pct'), ef.get('done_same_types_pct'), r['reason']])

res = {
    'label': 'estimate',
    'asof_ts': str(asof),
    'window': '12 months of filings to the file as-of time',
    'measured_rates_used': rates,
    'never_done_range_applied': [never_low, never_high],
    'late_range_applied': [late_low, late_high],
    'vacant_building_2026_no_record_not_used': never_high_sens,
    'traced_crew_work_requests_12m': traced_vol,
    'kinds_traceability_12m': kinds_vol,
    'untraced_crew_work_requests_12m': tot['v12'],
    'estimate_never_done_jobs_per_year': [round(tot['low'], -1), round(tot['high'], -1)],
    'mechanical_never_done_jobs_per_year': [round(tot['mech_low'], -1), round(tot['mech_high'], -1)],
    'estimate_done_late_jobs_per_year': [round(tot['late_low'], -1), round(tot['late_high'], -1)],
    'sensitivity_calendar_2025_volume': {'untraced_crew_work_requests_2025': tot['v2025'],
                                         'estimate_never_done_jobs': [round(tot['low_2025'], -1), round(tot['high_2025'], -1)]},
    'categories': out_rows,
}
json.dump(res, open(os.path.join(OUT, 'extrapolation.json'), 'w'), indent=1, default=str)
print(json.dumps({k: res[k] for k in ['never_done_range_applied', 'late_range_applied', 'vacant_building_2026_no_record_not_used',
                                      'traced_crew_work_requests_12m', 'untraced_crew_work_requests_12m',
                                      'estimate_never_done_jobs_per_year', 'mechanical_never_done_jobs_per_year',
                                      'estimate_done_late_jobs_per_year']}, indent=1, default=str))
for r in out_rows:
    print(r['category'], r['tier'], r['requests_12m'], r['never_low'], r['never_high'], r['own_rereport_7d'], r['own_rereport_filing_day15_44'])
