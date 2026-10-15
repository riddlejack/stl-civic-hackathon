"""Impact: turn the observed counts into low / central / high estimates, every assumption named.

Inputs (aggregates only): build/impact/rereports.json (01), build/impact/service.json (02),
build/E5/extrapolate.json, build/E5/private/ledger_rows.parquet (division counts only).
Every assumption is a named constant below; change one and rerun.
Writes build/impact/estimates.json and research/impact-quantification-facts.csv.
Run order: 01, 02, 04, then 03 (03 reads 04's brainstorm_check.json).
Run: python3 -I scripts/exec/impact/03_estimates.py
"""
import csv
import json
import os

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
B = os.path.join(ROOT, 'build')
RR = json.load(open(os.path.join(B, 'impact', 'rereports.json')))
SV = json.load(open(os.path.join(B, 'impact', 'service.json')))
E5X = json.load(open(os.path.join(B, 'E5', 'extrapolate.json')))

# ------------------------------------------------------------------ sources
U_CSB = 'https://www.stlouis-mo.gov/data/upload/data-files/csb.zip'
U_BUDGET = 'https://www.stlouis-mo.gov/government/departments/budget/documents/upload/11-FY2027-AOP-Public-Safety-2.pdf'
U_LEDGER = 'https://www.stlouis-mo.gov/data/upload/data-files/forestry-service-records.csv'
U_LRA = 'https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_INVENTORY.csv'
U_QE63 = 'https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/63'
U_QE90 = 'https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/90'
U_QE102 = 'https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/102'
U_PEW = 'https://www.pew.org/-/media/assets/2010/03/02/final-311-report-030210.pdf'
U_NYC = 'https://www.nyc.gov/assets/operations/downloads/pdf/mmr2025/311.pdf'
U_TOR = 'https://www.toronto.ca/legdocs/mmis/2025/se/bgrd/backgroundfile-253220.pdf'
U_DOT = 'https://www.dot.ny.gov/divisions/operating/opdm/passenger-rail/passenger-rail-repository/USDOT%20Benefit%20Cost%20Analysis%20Guidance%202023%20Update.pdf'
U_BLS = 'https://www.bls.gov/regions/mountain-plains/news-release/2026/occupationalemploymentandwages_stlouis_20260811.htm'
U_FRESNO = 'https://agendas.fresno.gov/es/legislation/id-23-916-16348'
U_BALT = 'https://technical.ly/civic-news/baltimore-311-upgrades/'
U_TORSF = 'https://www.toronto.ca/legdocs/mmis/2025/gg/bgrd/backgroundfile-260459.pdf'
U_MUSK = 'https://muskegon-mi.gov/documents/view/63/6052/'
U_SAV = 'https://agenda.savannahga.gov/publishing/december-19-2019-city-council-regular-meeting/193_4597.html'
U_A2 = 'https://a2gov.granicusideas.com/meetings/51-city-council/agenda_items/5b8854a47d7965a227027961'
U_PBI = 'https://www.microsoft.com/en-us/power-platform/products/power-bi/pricing'
U_IBM = 'https://newsroom.ibm.com/2025-07-30-ibm-report-13-of-organizations-reported-breaches-of-ai-models-or-applications,-97-of-which-reported-lacking-proper-ai-access-controls'
U_CWHELP = 'https://help.cityworks.com/AMS/OC/Content/AMS/OC/WorkOrder/CloseAWorkOrder.htm'

# ------------------------------------------------------------------ St. Louis CSB, FY2025 actual (budget book p. ~180, program 622-02)
CSB_FY25_ALL_FUNDS = 612_679
CSB_FY25_PERSONAL = 551_962
CSB_FY25_FTE = 8.0
CSB_FY25_CONTACTS = 143_008
CSB_FY25_REQUESTS = 112_916
COST_PER_CONTACT = CSB_FY25_ALL_FUNDS / CSB_FY25_CONTACTS          # direct budget only
PROD_HOURS = {'low': 2080, 'central': 1800, 'high': 1600}          # ASSUMPTION: productive hours per FTE-year
MIN_PER_CONTACT = {k: CSB_FY25_FTE * h * 60 / CSB_FY25_CONTACTS for k, h in PROD_HOURS.items()}
CSB_RATE = {k: CSB_FY25_PERSONAL / CSB_FY25_FTE / h for k, h in PROD_HOURS.items()}   # $/productive hour, loaded
BLS_STL_MEAN_WAGE = 31.89      # May 2025, all occupations, St. Louis MSA
FRINGE = 1.40                  # ASSUMPTION: benefits loading on wages
STAFF_RATE = {'low': CSB_RATE['central'], 'central': round(BLS_STL_MEAN_WAGE * FRINGE, 2), 'high': 60.0}  # high = ASSUMPTION (IT/analyst)
DOT_VTTS_PERSONAL = 17.00      # 2021 $ per person-hour, USDOT BCA guidance Jan 2023, Table A-3

E = {'assumptions': {}, 'estimates': {}}
A = E['assumptions']
A['cost_per_contact_stl_fy25'] = round(COST_PER_CONTACT, 2)
A['minutes_per_contact_stl_fy25'] = {k: round(v, 1) for k, v in MIN_PER_CONTACT.items()}
A['csb_loaded_rate_per_hour'] = {k: round(v, 2) for k, v in CSB_RATE.items()}
A['staff_rate_per_hour'] = STAFF_RATE
A['productive_hours_per_fte'] = PROD_HOURS

# ------------------------------------------------------------------ 1. re-reports
by = lambda key, k: next(r for r in RR[key] if r['window_days'] == k)
vol = RR['handoff_closures_12m']
rr = {
    'low': {'excess_pts': 0.0, 'volume': vol['eligible_types'],
            'basis': "R2 filing-anchored check: pooled hand-off 6.10% vs done 6.04% re-reported 15-44 days after filing (diff 0.06 pts, CI -0.53 to 0.65); and R2-08: re-reports do not track unfinished work where a completion record exists"},
    'central': {'excess_pts': by('nonrecurring', 60)['excess_pts'], 'volume': vol['eligible_nonrecurring'],
                'basis': '60-day standardised excess in non-recurring, non-dumping types (the only subset where the filing-anchored check also holds: 7.18% vs 4.01%), times 12-month hand-off closures in those types; recurring route services set to zero'},
    'high': {'excess_pts': by('all_types', 90)['excess_pts'], 'volume': vol['eligible_types'],
             'basis': '90-day standardised excess over all eligible types, closure-anchored, times 12-month hand-off closures in eligible types'},
}
for k, v in rr.items():
    v['excess_rereports_per_year'] = round(v['volume'] * v['excess_pts'] / 100)
# durable-fix types only (coordinator note): reported beside the range, not inside it
rr_durable = {k: {'excess_pts': by('durable', k)['excess_pts'], 'volume': vol['eligible_durable'],
                  'excess_rereports_per_year': round(vol['eligible_durable'] * by('durable', k)['excess_pts'] / 100)} for k in (30, 60, 90)}
RES_MIN = {'low': 5, 'central': 10, 'high': 20}   # ASSUMPTION: resident minutes per report (Philly311 2009 talk ~5 min + hold 1:45, Pew)
for k, v in rr.items():
    n = v['excess_rereports_per_year']
    v['csb_cost_per_year'] = round(n * COST_PER_CONTACT)
    v['csb_staff_hours_per_year'] = round(n * MIN_PER_CONTACT[k] / 60)
    v['resident_minutes_per_report'] = RES_MIN[k]
    v['resident_hours_per_year'] = round(n * RES_MIN[k] / 60)
    v['resident_time_value_usd_2021'] = round(n * RES_MIN[k] / 60 * DOT_VTTS_PERSONAL)
E['estimates']['1_rereports'] = rr
E['estimates']['1_rereports_durable_only_by_window'] = rr_durable
BC = json.load(open(os.path.join(B, 'impact', 'brainstorm_check.json')))
E['estimates']['1_gross_repeat_filings_2025'] = {k: BC[k] for k in ('v0_any_earlier', 'v1_earlier_closed_before', 'v2_after_handoff_closure',
    'v2_resident_channel', 'v3_after_handoff_durable', 'v4_after_done_closure', 'v2_median_days_from_close')}

# ------------------------------------------------------------------ 2. status chasing: no volume on disk
E['estimates']['2_status_chasing'] = {
    'estimated': False,
    'contacts_not_entering_a_request_fy25': CSB_FY25_CONTACTS - CSB_FY25_REQUESTS,
    'note': 'Ceiling only: FY25 contacts minus requests entered. Status checks are an unknown share of it (information calls, transfers and repeat calls are in it too). No status-call or web-lookup count found on disk; not estimated.'}

# ------------------------------------------------------------------ 3. manual closing labour
H12 = SV['A_handoff_closures']['closed_in_12m_to_asof']
CLOSE_MIN_GROSS = {'low': 0.5, 'central': 1.0, 'high': 2.0}   # ASSUMPTION: minutes to pick closing words and close
NET_SHARE = {'low': 0.0, 'central': 0.5, 'high': 1.0}          # ASSUMPTION: share of that time not replaced by the link step
cl = {}
for k in ('low', 'central', 'high'):
    gross_h = H12 * CLOSE_MIN_GROSS[k] / 60
    net_h = gross_h * NET_SHARE[k]
    cl[k] = {'handoff_closures_12m': H12, 'gross_min_per_closure': CLOSE_MIN_GROSS[k], 'gross_hours': round(gross_h),
             'net_share': NET_SHARE[k], 'net_hours': round(net_h), 'net_fte': round(net_h / PROD_HOURS['central'], 2),
             'net_cost': round(net_h * CSB_RATE[k])}
E['estimates']['3_manual_closing'] = cl

# ------------------------------------------------------------------ 4. service restored, physical units
LB = SV['B_land_bank']
lots = {
    'low': {'parcels': LB['strict_on_schedule_no_2026_cut']['parcels'], 'season_cost_each': LB['lra_2026_season']['median_per_parcel'],
            'basis': 'land-bank parcels, 2026 Weeds-Vacant Lot/Bldg report closed "on schedule to be cut", filed by 13 Sep, no cut billed in 2026; median 2026 billed per land-bank parcel cut'},
    'central': {'parcels': LB['handoff_any_words_no_2026_cut']['parcels'], 'season_cost_each': LB['lra_reported_and_cut_2026_season']['median'],
                'basis': 'adds cut complaints and every hand-off wording; median 2026 billed per reported land-bank parcel that was cut'},
    'high': {'parcels': LB['handoff_any_words_no_cut_after_filing']['parcels'], 'season_cost_each': LB['lra_reported_and_cut_2026_season']['mean'],
             'basis': 'parcels with no cut billed after the report (some were cut earlier in 2026); mean 2026 billed per reported land-bank parcel that was cut'},
}
for v in lots.values():
    v['season_cost_total'] = round(v['parcels'] * v['season_cost_each'])
lots['context_lra_listed_vacant_lots_no_2026_cut'] = LB['lra_maint_vacant_lot_no_2026_cut']
lots['context_lra_2026_total_billed'] = LB['lra_2026_season']['total_billed']
E['estimates']['4a_land_bank_lots'] = lots
E['estimates']['4b_tier1'] = {k: SV['C_tier1'][k] for k in ('tier1_ranked_list', 'tier1_ranked_median_days_past', 'tier1_ranked_over_90d',
                                                             'tier1_ranked_over_365d', 'tier1_ranked_class_e_no_record', 'tier1_ranked_class_b_pending', 'tier1_trees_limbs')}
E['estimates']['4c_removals'] = SV['D_removals']

# ------------------------------------------------------------------ 5. what a quarter would show
inc = {'low': 0, 'central': 0, 'high': 0}
done_inc = 0
for t in E5X['by_type']:
    inc['low'] += max(t['est_pending_lo'], t['obs_b']) - t['obs_b']
    inc['central'] += max(t['est_pending'], t['obs_b']) - t['obs_b']
    inc['high'] += max(t['est_pending_hi'], t['obs_b']) - t['obs_b']
    done_inc += max(t['est_done'], t['obs_a']) - t['obs_a']
con = duckdb.connect()
con.execute(f"ATTACH '{os.path.join(B, 'stl.duckdb')}' AS s (READ_ONLY)")
divs = con.execute(f"""SELECT coalesce(r.division, '(none)'), count(*) FROM '{os.path.join(B, 'E5', 'private', 'ledger_rows.parquet')}' l
    LEFT JOIN s.requests r USING (request_id) WHERE l.cls = 'e_no_evidence' GROUP BY 1 ORDER BY 2 DESC""").fetchall()
big = [d for d in divs if d[1] >= 100]
REVIEW_PER_WEEK = {'low': 10, 'central': 25, 'high': 50}   # ASSUMPTION: records each division dispositions a week
WEEKS = 13
MIN_PER_REVIEW = 3                                           # ASSUMPTION: minutes to verify-and-close or dispatch one record
q5 = {}
for k in ('low', 'central', 'high'):
    auto = inc[k] + (done_inc if k != 'low' else 0)
    # reviewed records: capped at what remains in each division after automatic resolution (pro rata)
    remaining_share = 1 - auto / 12566
    reviewed = sum(min(REVIEW_PER_WEEK[k] * WEEKS, round(n * remaining_share)) for _, n in big)
    q5[k] = {'auto_from_existing_records': auto, 'reviewed_in_quarter': reviewed, 'total_known_after_quarter': auto + reviewed,
             'share_of_12566': round(100 * (auto + reviewed) / 12566, 1), 'divisions_reviewing': len(big),
             'review_per_week_per_division': REVIEW_PER_WEEK[k],
             'review_staff_hours_quarter': round(reviewed * MIN_PER_REVIEW / 60)}
q5['divisions_with_100plus_no_record'] = big
E['estimates']['5_quarter'] = q5

# ------------------------------------------------------------------ 6. what the fix costs
SETUP = {  # ASSUMPTION: staff hours, low / central / high
    'Cityworks admin: create crew work orders from the request, confirm auto-close, test per division': (16, 40, 80),
    'Saved search per division: past due, sorted by rank (14 divisions)': (14, 28, 56),
    'Default priority by request type (tier map) and the rank sort / SQL': (8, 24, 60),
    'CityStat: restate the 311 measures as done-by-the-date': (8, 24, 60),
    'SOP and training: 311 staff and 14 division leads': (16, 32, 60),
}
setup = {k: sum(v[i] for v in SETUP.values()) for i, k in enumerate(('low', 'central', 'high'))}
WEEKLY_REVIEW_H = {'low': 0.5, 'central': 1.25, 'high': 2.5}   # ASSUMPTION: hours per division per week (= REVIEW_PER_WEEK x 3 min)
fix = {'setup_items_hours': SETUP}
for k in ('low', 'central', 'high'):
    fix[k] = {'setup_hours': setup[k], 'rate': STAFF_RATE[k], 'setup_cost': round(setup[k] * STAFF_RATE[k]),
              'weekly_review_hours_per_division': WEEKLY_REVIEW_H[k],
              'review_hours_per_year': round(WEEKLY_REVIEW_H[k] * len(big) * 52),
              'review_cost_per_year': round(WEEKLY_REVIEW_H[k] * len(big) * 52 * STAFF_RATE[k]),
              'new_licence_cost': 0}
E['estimates']['6_fix_cost'] = fix
json.dump(E, open(os.path.join(B, 'impact', 'estimates.json'), 'w'), indent=1)

# ------------------------------------------------------------------ facts CSV
F = []
def f(fig, val, unit, date, label, url):
    F.append([fig, val, unit, date, label, url])

S1 = 'scripts/exec/impact/01_rereports.py -> build/impact/rereports.json'
S2 = 'scripts/exec/impact/02_service.py -> build/impact/service.json'
S3 = 'scripts/exec/impact/03_estimates.py -> build/impact/estimates.json'
for key, lab in (('all_types', 'all eligible types'), ('nonrecurring', 'non-recurring, non-dumping types')):
    for r in RR[key]:
        f(f"Re-reported within {r['window_days']} days after a hand-off closure, standardised ({lab})", r['std_rate_handoff_pct'], '% of closures', 'closures of requests filed 2025-01-01 to 2026-10-13', 'observed', f'{U_CSB} ({S1})')
        f(f"Re-reported within {r['window_days']} days after a done closure, standardised to hand-off mix ({lab})", r['std_rate_done_pct'], '% of closures', 'same', 'observed', f'{U_CSB} ({S1})')
        f(f"Hand-off closures with a complete {r['window_days']}-day window ({lab})", r['handoff_closures'], 'closures', 'same', 'observed', f'{U_CSB} ({S1})')
f('Hand-off closures, 12 months to as-of, eligible types', vol['eligible_types'], 'closures', '2025-10-13 to 2026-10-13', 'observed', f'{U_CSB} ({S1})')
f('Hand-off closures, 12 months to as-of, eligible non-recurring types', vol['eligible_nonrecurring'], 'closures', '2025-10-13 to 2026-10-13', 'observed', f'{U_CSB} ({S1})')
for k in (30, 60, 90):
    d_ = by('durable', k)
    f(f'Re-reported within {k} days, durable-fix types: hand-off vs done, standardised', f"{d_['std_rate_handoff_pct']} vs {d_['std_rate_done_pct']}", '% of closures', 'closures of requests filed 2025-01-01 to 2026-10-13', 'observed', f'{U_CSB} ({S1})')
    f(f'Excess re-reports per year, durable-fix types only ({k}-day window)', rr_durable[k]['excess_rereports_per_year'], 'requests per year', '12 months to 2026-10-13', 'estimated', S3)
S4 = 'scripts/exec/impact/04_verify_brainstorm.py -> build/impact/brainstorm_check.json'
f('2025 filings with a same-type, same-address request filed in the prior 90 days (brainstorm join)', BC['v0_any_earlier'], 'requests', '2025 filings', 'observed', f'{U_CSB} ({S4})')
f('Same, earlier request closed before the repeat was filed', BC['v1_earlier_closed_before'], 'requests', '2025 filings', 'observed', f'{U_CSB} ({S4})')
f('Same, earlier request closed at the hand-off before the repeat', BC['v2_after_handoff_closure'], 'requests', '2025 filings', 'observed', f'{U_CSB} ({S4})')
f('Same, earlier request closed at the hand-off, durable-fix types', BC['v3_after_handoff_durable'], 'requests', '2025 filings', 'observed', f'{U_CSB} ({S4})')
f('Same, earlier request closed done before the repeat', BC['v4_after_done_closure'], 'requests', '2025 filings', 'observed', f'{U_CSB} ({S4})')
f('2025 filings closed as handed_off (excl. converted)', 36705, 'requests', '2025 filings', 'observed', f'{U_CSB} ({S4})')
f('2025 closings whose words say "call CSB"', BC['call_csb_closings_2025'], 'requests', '2025 filings', 'observed', f'{U_CSB} ({S4})')
f('Past-due requests in six tier-1 types (cave-ins, tornado debris, trees and limbs down, building collapse)', BC['six_tier1_total'], 'requests', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S4})')
f('Past-due requests with a city work record pending (E5 class b) / strict', f"{BC['class_b_pending']} / {BC['class_b_by_evidence'][0]}", 'requests', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S4})')
f('Filing-anchored re-report check, hand-off vs done, pooled (R2)', '6.10 vs 6.04', '% re-reported 15-44 days after filing', '2025-26 closures', 'reported', 'build/R2/rereport_summary.json')
for k in ('low', 'central', 'high'):
    v = rr[k]
    f(f'Excess re-reports per year attributable to hand-off closing ({k})', v['excess_rereports_per_year'], 'requests per year', '12 months to 2026-10-13', 'estimated', S3)
    f(f'311 cost of those re-reports ({k})', v['csb_cost_per_year'], 'USD per year', 'FY2025 cost basis', 'estimated', S3)
    f(f'Resident time spent on those re-reports ({k}, {v["resident_minutes_per_report"]} min each)', v['resident_hours_per_year'], 'hours per year', '12 months to 2026-10-13', 'estimated', S3)
f('CSB (311) all-funds actual spend', CSB_FY25_ALL_FUNDS, 'USD', 'FY2025', 'reported', f'{U_BUDGET} (program 622-02)')
f('CSB personal services actual', CSB_FY25_PERSONAL, 'USD', 'FY2025', 'reported', U_BUDGET)
f('CSB full-time positions', CSB_FY25_FTE, 'FTE', 'FY2025', 'reported', U_BUDGET)
f('CSB number of contacts (all sources)', CSB_FY25_CONTACTS, 'contacts', 'FY2025', 'reported', U_BUDGET)
f('CSB city service requests entered', CSB_FY25_REQUESTS, 'requests', 'FY2025', 'reported', U_BUDGET)
f('CSB direct cost per contact', round(COST_PER_CONTACT, 2), 'USD per contact', 'FY2025', 'inferred', U_BUDGET)
f('CSB staff minutes per contact (1,800 productive h/FTE)', round(MIN_PER_CONTACT['central'], 1), 'minutes', 'FY2025', 'inferred', U_BUDGET)
f('Contacts that did not enter a request (ceiling for status calls)', CSB_FY25_CONTACTS - CSB_FY25_REQUESTS, 'contacts', 'FY2025', 'inferred', U_BUDGET)
f('Median cost per 311 call, 15 cities', 3.39, 'USD per call', '2009', 'reported', U_PEW)
f('Philly311 average talk time', 5, 'minutes', '2009', 'reported', U_PEW)
f('NYC 311 spending / contacts, all channels', '68.3M / 37.1M', 'USD / contacts', 'FY2025', 'reported', U_NYC)
f('Toronto 311 interactions that were status updates on existing requests', 6, '% of 1.29M interactions', '2024', 'reported', U_TOR)
f('USDOT value of travel time, personal', DOT_VTTS_PERSONAL, 'USD (2021) per person-hour', 'guidance Jan 2023', 'reported', U_DOT)
f('St. Louis MSA mean hourly wage, all occupations', BLS_STL_MEAN_WAGE, 'USD per hour', 'May 2025', 'reported', U_BLS)
f('Hand-off closures, requests filed 2025-01-01 to as-of', SV['A_handoff_closures']['filed_2025_to_asof'], 'closures', '2025-01-01 to 2026-10-13', 'observed', f'{U_CSB} ({S2})')
f('Hand-off closures made in the 12 months to as-of', H12, 'closures', '2025-10-13 to 2026-10-13', 'observed', f'{U_CSB} ({S2})')
for k in ('low', 'central', 'high'):
    f(f'Net closing labour removed by auto-close ({k})', cl[k]['net_hours'], 'staff hours per year', '12 months to 2026-10-13', 'estimated', S3)
    f(f'Net closing labour removed, cost ({k})', cl[k]['net_cost'], 'USD per year', 'FY2025 cost basis', 'estimated', S3)
for lab, key in (('"on schedule", no 2026 cut', 'strict_on_schedule_no_2026_cut'), ('any hand-off words, no 2026 cut', 'handoff_any_words_no_2026_cut'),
                 ('any hand-off words, no cut after filing', 'handoff_any_words_no_cut_after_filing')):
    f(f'Land-bank parcels with a 2026 weed report closed at hand-off, {lab}', LB[key]['parcels'], 'parcels', '2026 filings to 13 Sep; ledger to 13 Oct', 'observed', f'{U_CSB}; {U_LEDGER}; {U_LRA} ({S2})')
    f(f'Requests behind those parcels, {lab}', LB[key]['requests'], 'requests', 'same', 'observed', f'{U_CSB}; {U_LEDGER}; {U_LRA} ({S2})')
f('Land-bank parcels with a 2026 mowing charge', LB['lra_2026_season']['parcels'], 'parcels', '2026 to 13 Oct', 'observed', f'{U_LEDGER}; {U_LRA} ({S2})')
f('2026 mowing billed on land-bank parcels', LB['lra_2026_season']['total_billed'], 'USD', '2026 to 13 Oct', 'observed', f'{U_LEDGER}; {U_LRA} ({S2})')
f('Median 2026 billed per land-bank parcel cut', LB['lra_2026_season']['median_per_parcel'], 'USD per parcel', '2026 to 13 Oct', 'observed', f'{U_LEDGER} ({S2})')
f('Mean 2026 billed per land-bank parcel cut', LB['lra_2026_season']['mean_per_parcel'], 'USD per parcel', '2026 to 13 Oct', 'observed', f'{U_LEDGER} ({S2})')
f('Median 2026 billed per reported land-bank parcel that was cut', LB['lra_reported_and_cut_2026_season']['median'], 'USD per parcel', '2026 to 13 Oct', 'observed', f'{U_LEDGER} ({S2})')
f('Land-bank parcels listed as Vacant Lot (2023 list) with no 2026 cut', LB['lra_maint_vacant_lot_no_2026_cut'][0], 'parcels', '2026 to 13 Oct', 'observed', f'{U_LEDGER}; {U_LRA} ({S2})')
for k in ('low', 'central', 'high'):
    f(f'Season cost to cut the told-on-schedule land-bank parcels ({k})', lots[k]['season_cost_total'], 'USD', '2026 billed rates', 'estimated', S3)
T = SV['C_tier1']
f('Tier-1 (life-safety) requests past the promise on the ranked list', T['tier1_ranked_list'], 'requests', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S2})')
f('Median days past the promise, tier-1 ranked', T['tier1_ranked_median_days_past'], 'days', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S2})')
f('Tier-1 ranked more than a year past the promise', T['tier1_ranked_over_365d'], 'requests', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S2})')
f('Tier-1 ranked with no record either way', T['tier1_ranked_class_e_no_record'], 'requests', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S2})')
f('Trees or limbs down (3 codes), past promise, ranked', T['tier1_trees_limbs']['n'], 'requests', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S2})')
f('Median days past promise, trees or limbs down', T['tier1_trees_limbs']['median_days_past'], 'days', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S2})')
for code, n, med in T['tier1_ranked_by_code'][:6]:
    f(f'Tier-1 ranked past due: {code}', n, 'requests', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S2})')
    f(f'Median days past promise: {code}', med, 'days', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S2})')
for layer, url, name in ((63, U_QE63, 'Tree Removal WOs'), (90, U_QE90, '30-Day Removals - All City - New'), (102, U_QE102, '(MTL) REMOVAL - Open - Urgent')):
    d = SV['D_removals'][f'layer_{layer}']
    f(f'Open removal work orders, {name}', d['open_no_finish'], 'work orders', 'extract 2026-10-14', 'observed', f'{url} ({S2})')
    f(f'Of those, past their projected finish date, {name}', d['past_projected_finish'], 'work orders', 'as of 2026-10-13', 'observed', f'{url} ({S2})')
    f(f'Median days past projected finish, {name}', d['median_days_past_projected'], 'days', 'as of 2026-10-13', 'observed', f'{url} ({S2})')
f('Removal WOs more than a year past projected finish (layer 63)', SV['D_removals']['layer_63']['past_over_365d'], 'work orders', 'as of 2026-10-13', 'observed', f'{U_QE63} ({S2})')
f('No record either way (E5 class e)', 12566, 'requests', 'as of 2026-10-13', 'reported', 'research/open-queue-reality-check.md')
for k in ('low', 'central', 'high'):
    f(f'No-record requests that existing work records would explain once linked ({k})', q5[k]['auto_from_existing_records'], 'requests', 'one quarter', 'estimated', f'build/E5/extrapolate.json ({S3})')
    f(f'No-record requests dispositioned by a weekly review in a quarter ({k}, {REVIEW_PER_WEEK[k]}/division/week)', q5[k]['reviewed_in_quarter'], 'requests', 'one quarter', 'estimated', S3)
    f(f'No-record requests whose fate is known after a quarter ({k})', q5[k]['total_known_after_quarter'], 'requests', 'one quarter', 'estimated', S3)
for k in ('low', 'central', 'high'):
    f(f'Setup staff hours ({k})', fix[k]['setup_hours'], 'hours', 'one-off', 'estimated', S3)
    f(f'Setup cost ({k})', fix[k]['setup_cost'], 'USD', 'one-off', 'estimated', S3)
    f(f'Weekly review, staff hours per year ({k})', fix[k]['review_hours_per_year'], 'hours per year', 'ongoing', 'estimated', S3)
    f(f'Weekly review, cost per year ({k})', fix[k]['review_cost_per_year'], 'USD per year', 'ongoing', 'estimated', S3)
f('Fresno 311 CRM: implementation + Salesforce licences', '395,724 + 610,344', 'USD', '2023', 'reported', U_FRESNO)
f('Baltimore Salesforce 311 upgrades', 1_600_000, 'USD', 'date not seen', 'reported', U_BALT)
f('Toronto Salesforce increase 2026-2030', 6_751_001, 'CAD', '2025 staff report', 'reported', U_TORSF)
f('Muskegon SeeClickFix (CivicPlus) subscription', 39_119, 'USD per year', '2025', 'reported', U_MUSK)
f('Savannah SAV311 CRM', 82_123, 'USD per year', '2019', 'reported', U_SAV)
f('Ann Arbor Cityworks enterprise licence and maintenance', 83_000, 'USD per year', 'FY2019-21', 'reported', U_A2)
f('Power BI Pro list price', 14, 'USD per user per month', '2026', 'reported', U_PBI)
f('IBM average cost of a data breach, global / US', '4.44M / 10.22M', 'USD', '2025', 'reported', U_IBM)
f('Toronto 311 cost per call', '11-16', 'CAD per call', '2024', 'reported', 'https://globalnews.ca/news/10238190/toronto-311-call-cost-budget/')
f('Chicago 311 calls that were duplicates or status checks', 'nearly 40', '% of calls', '2012', 'reported', 'https://abc7chicago.com/archive/8817677')
f('Calls a month to St. Louis 311', 4000, 'calls per month', '2026-03', 'reported', 'https://www.firstalert4.com/2026/03/12/city-highlights-citizen-service-bureau/')
f('Philly311 average hold time', 1.75, 'minutes', '2009', 'reported', U_PEW)
f('2025-26 closings whose words say "call CSB"', BC['call_csb_closings_2025_26'], 'requests', '2025-01-01 to 2026-10-13 filings', 'observed', f'{U_CSB} ({S4})')
f('No-record requests moving to "waiting" once linked, E1 sample scaled (central; 95% bounds)', f"{inc['central']} ({inc['low']}-{inc['high']})", 'requests', 'as of 2026-10-13', 'estimated', 'build/E5/extrapolate.json')
f('No-record requests moving to "done" once linked, E1 sample scaled', done_inc, 'requests', 'as of 2026-10-13', 'estimated', 'build/E5/extrapolate.json')
f('Divisions with 100+ no-record past-due requests / requests in them', f"{len(big)} / {sum(n for _, n in big)}", 'divisions / requests', 'as of 2026-10-13', 'observed', f'{U_CSB} ({S3})')
f('Reported land-bank parcels cut in 2026 / mean billed each', f"{LB['lra_reported_and_cut_2026_season']['parcels']} / {LB['lra_reported_and_cut_2026_season']['mean']}", 'parcels / USD', '2026 to 13 Oct', 'observed', f'{U_LEDGER} ({S2})')
f('Median age of open removal work orders since initiation (layer 63)', SV['D_removals']['layer_63']['median_age_days_since_initiate'], 'days', 'as of 2026-10-13', 'observed', f'{U_QE63} ({S2})')
f('Blended staff rate, central (BLS mean x 1.4)', STAFF_RATE['central'], 'USD per hour', 'May 2025 wage basis', 'estimated', U_BLS)
f('CSB loaded rate per productive hour (1,800 h)', round(CSB_RATE['central'], 2), 'USD per hour', 'FY2025', 'inferred', U_BUDGET)
with open(os.path.join(ROOT, 'research', 'impact-quantification-facts.csv'), 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['figure', 'value', 'unit', 'date_refers_to', 'label', 'source'])
    w.writerows(F)
print(json.dumps(E['estimates'], indent=1, default=str))
print('facts rows', len(F))
