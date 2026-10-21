"""R2 step 5: figure registry with derivations (build/R2/figures.json).

Reads only R2's own aggregated outputs; run after steps 1-4 and 6.
Run: .venv/bin/python -I scripts/night/R2/05_figures.py
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
B = os.path.join(ROOT, 'build', 'R2')
S = json.load(open(os.path.join(B, 'rereport_summary.json')))
C = S['comparisons']
X = json.load(open(os.path.join(B, 'extrapolation.json')))
T = json.load(open(os.path.join(B, 'tree_planting_fate.json'))) if os.path.exists(os.path.join(B, 'tree_planting_fate.json')) else None
absr = list(csv.DictReader(open(os.path.join(B, 'rereport_absolute_counts.csv'))))
prox = list(csv.DictReader(open(os.path.join(B, 'proxy_check_r1_fates.csv')))) if os.path.exists(os.path.join(B, 'proxy_check_r1_fates.csv')) else []

PERIOD = 'requests filed 1 Jan 2025 to 13 Oct 2026, closed; windows complete before the file as-of time (13 Oct 2026 00:33)'
RR_DEF = ('another request at the same normalised address (N1 addr_norm) with the same PROBLEMCODE, any channel, filed after the '
          'closure and within the window; one row per REQUESTID')
BASE_DER = ('311 requests (city open data, csb.zip, cleaned copies, one row per REQUESTID) in N1\'s database, closing class from N2\'s '
            'final table; each closure checked for a later request at the same normalised address and problem code. ')
STD = ('Compared within each request type, then averaged with the same weights for both classes (the hand-off count per type: '
       'direct standardisation), over types with >= 300 closures and >= 30 complete-window closures in each class; '
       'Mantel-Haenszel risk ratio beside it. ')
figs = []


def add(id_, value, unit, definition, label, derivation, note='', period=PERIOD, src='scripts/night/R2/01_rereport.py; scripts/night/R2/02_summary.py'):
    figs.append({'id': id_, 'value': value, 'unit': unit, 'period': period, 'definition': definition, 'label': label,
                 'source_sql_or_script': src, 'derivation': derivation, 'note': note})


def cmp(key):
    c = C[key]
    return {'handoff_pct': c['std_rate_a_pct'], 'done_same_types_pct': c['std_rate_b_pct'], 'diff_pts': c['std_diff_pts'],
            'diff_ci95_pts': c['std_diff_ci95_pts'], 'mh_risk_ratio': c['mh_rr'], 'mh_rr_ci95': c['mh_rr_ci95'],
            'types': c['types'], 'handoff_closures': c['n_a'], 'done_closures': c['n_b'],
            'types_first_class_higher': c['types_a_higher']}


h14 = cmp('handoff_vs_done|all_eligible_types|rr14')
add('r2_rereport14_handoff_vs_done', h14, 'percent of closures',
    'Re-reported within 14 days of closure (' + RR_DEF + '): after a hand-off closure (handed_off or converted) vs after a "done" closure of the same types.',
    'observed', BASE_DER + STD + f"Hand-off {h14['handoff_pct']}% vs done {h14['done_same_types_pct']}% across {h14['types']} types.",
    'Headline as briefed. Most of the gap falls while the job is still waiting: see r2_rereport_filing_window.')
for k, wnd in [('rr7', 7), ('rr30', 30)]:
    v = cmp(f'handoff_vs_done|all_eligible_types|{k}')
    add(f'r2_rereport{wnd}_handoff_vs_done', v, 'percent of closures',
        f'As r2_rereport14_handoff_vs_done, within {wnd} days of closure.', 'observed', BASE_DER + STD)
add('r2_rereport14_crude_by_class', S['crude_all_types'], 'percent of closures',
    'Re-reported within 14 and 30 days of closure, all types pooled, by closing class (no standardisation; confounded by type mix).',
    'observed', BASE_DER + 'Pooled over every type, no weighting.', 'Do not compare these classes directly; use the standardised figures.')
v = cmp('handoff_vs_done|all_eligible_types|rr14_first_report')
add('r2_rereport14_first_report', v, 'percent of closures',
    'As r2_rereport14_handoff_vs_done, only closures at addresses with no request of the same type in the 365 days before filing (chronic-site control).',
    'observed', BASE_DER + STD + 'Chronic addresses removed.')
v = cmp('handoff_vs_done|all_eligible_types|rr14_resident')
add('r2_rereport14_resident', v, 'percent of closures',
    'As r2_rereport14_handoff_vs_done, counting only later requests from resident channels (web, phone, e-mail, chat, Twitter, letter).',
    'observed', BASE_DER + STD)
v = cmp('handoff_vs_done|all_eligible_types|rr14_guard24h')
add('r2_rereport14_guard24h', v, 'percent of closures',
    'As r2_rereport14_handoff_vs_done, ignoring later requests filed within 24 hours of the original filing (parallel reports of the same event).',
    'observed', BASE_DER + STD)
v = cmp('handoff_vs_done|all_eligible_types|rr30_after_promise')
add('r2_rereport30_after_promise', v, 'percent of closures',
    'Re-reported within 30 days after the later of closure and the city\'s promise date (PRJCOMPLETEDATE): "still reported after the city\'s own deadline".',
    'observed', BASE_DER + STD)
vf = cmp('handoff_vs_done|all_eligible_types|rr_filing_day15_44')
vfn = cmp('handoff_vs_done|excluding_recurring_and_chronic|rr_filing_day15_44')
add('r2_rereport_filing_window', {'all_types': vf, 'excluding_recurring_and_chronic': vfn}, 'percent of closures',
    'Same calendar window for every class: closures made within 14 days of filing, re-reported 15 to 44 days after the ORIGINAL filing.',
    'observed', BASE_DER + STD + 'Hand-offs close earlier than done closures, so a window anchored at closure covers more of the wait; this anchors at filing instead.',
    'Cuts against the headline: pooled over all types the gap vanishes (refuse, the largest hand-off type, reverses); for non-recurring services it remains.')
fwt = S.get('filing_window_by_type', {})
add('r2_rereport_filing_window_selected_types', {k: fwt[k] for k in ['Refuse not collected', 'Vehicle Towing', 'Cave-Ins', 'Signal Bulb Out'] if k in fwt},
    'percent of closures', 'As r2_rereport_filing_window, per type (hand-off vs done, same type): closed within 14 days of filing, re-reported 15-44 days after filing.',
    'observed', BASE_DER + 'Per type, no weighting (build/R2/rereport_filing_window_by_type.csv).')
for sub, nm in [('excluding_recurring_and_chronic', 'r2_rereport14_nonrecurring'), ('durable_fix_types', 'r2_rereport14_durable')]:
    v = cmp(f'handoff_vs_done|{sub}|rr14')
    add(nm, v, 'percent of closures',
        'As r2_rereport14_handoff_vs_done, ' + ('excluding recurring services (Refuse Division codes, street cleaning, weeds) and chronic sites (dumping, debris).'
                                                 if 'nonrec' in nm else 'durable-fix types only (potholes, cave-ins, lights, city trees, signs).'),
        'observed', BASE_DER + STD)
SP = os.path.join(B, 'rereport_spatial_summary.json')
if os.path.exists(SP):
    sp = json.load(open(SP))
    add('r2_rereport14_spatial50m', {k: sp[k] for k in ['handoff_pct', 'done_same_types_pct', 'mh_rr', 'types', 'handoff_closures']},
        'percent of closures', 'As r2_rereport14_handoff_vs_done, counting a later request of the same PROBLEMCODE within 50 m of the closed request\'s point instead of the same address.',
        'observed', BASE_DER.replace('same normalised address', 'point within 50 m') + STD,
        'Catches reports a neighbour files for the same spot (and some independent neighbouring problems); both rates roughly double, the ratio holds.',
        src='scripts/night/R2/07_rereport_spatial.py')
v = cmp('handoff_vs_done|recurring_only|rr7')
add('r2_rereport7_recurring', v, 'percent of closures',
    'Recurring services only (Refuse Division codes, street cleaning, weeds), within 7 days of closure (inside one collection cycle).',
    'observed', BASE_DER + STD)
v = cmp('no_action_vs_done|all_eligible_types|rr14')
add('r2_rereport14_noaction_vs_done', v, 'percent of closures',
    'Re-reported within 14 days: after a "no action" closure (gone on arrival, no violation, not city\'s, declined) vs a "done" closure of the same types.',
    'observed', BASE_DER + STD.replace('hand-off count', 'no-action count'))
kinds = {}
for kd in ['crew_work', 'owner_enforcement', 'referral_elsewhere']:
    kinds[kd] = cmp(f'handoff[{kd}]_vs_done|all_eligible_types|rr14')
add('r2_rereport14_by_kind', kinds, 'percent of closures',
    'As r2_rereport14_handoff_vs_done, by kind of hand-off (R1\'s phrase-level composition: crew work, owner enforcement, referral elsewhere).',
    'observed', BASE_DER + STD + 'Kinds from build/R1/handoff_composition.csv (61,845 of 61,845 hand-offs matched).')
add('r2_rereport14_by_ward_group', {wg: {k: v[k] for k in ['std_rate_a_pct', 'std_rate_b_pct', 'mh_rr', 'types', 'n_a']} for wg, v in S['by_ward_group_rr14'].items()},
    'percent of closures', 'As r2_rereport14_handoff_vs_done, within each ward group (std_rate_a = hand-off, std_rate_b = done, same types and ward group).',
    'observed', BASE_DER + STD + 'Ward from N1 (file ward, polygon fill).')
add('r2_median_days_to_close_by_class', S['median_days_to_close_by_class'], 'days',
    'Median days from filing to closure, by closing class, all closures filed 1 Jan 2025 to 13 Oct 2026.',
    'observed', '311 requests (one row per REQUESTID), DATETIMECLOSED minus DATETIMEINIT, by N2 closing class.',
    'Why a window anchored at closure favours finding re-reports after hand-offs.', src='scripts/night/R2/02_summary.py')
add('r2_rereport14_type_verdicts', S['per_type_verdicts_14d'], 'request types',
    'Per type, hand-off vs done 14-day re-report rate: higher / lower if the 95% interval of the difference excludes 0; too few if either class has < 30 complete-window closures.',
    'observed', BASE_DER + 'Normal-approximation interval per type (build/R2/rereport_type_compare.csv).')
hand = [r for r in absr if r['class'] == 'handoff']
tot = {k: sum(int(r[k]) for r in hand) for k in ['later_reports_within14', 'later_reports_within30', 'resident_later_reports_within14', 'resident_later_reports_within30']}
add('r2_later_reports_after_handoff', tot, 'requests',
    'Later requests (same address and type) filed within 14 / 30 days after a hand-off closure; each later request counted once, attributed to the most recent earlier closure.',
    'observed', BASE_DER + 'Counts of distinct later requests, closures filed 1 Jan 2025 to 13 Oct 2026 (windows of the latest closures still open, so slightly low).')
exc14 = round(h14['handoff_closures'] * h14['diff_pts'] / 100.0)
v30 = cmp('handoff_vs_done|all_eligible_types|rr30')
exc30 = round(v30['handoff_closures'] * v30['diff_pts'] / 100.0)
months = 21.4
vr = cmp('handoff_vs_done|all_eligible_types|rr14_resident')
exc14r = round(vr['handoff_closures'] * vr['diff_pts'] / 100.0)
add('r2_excess_reports_after_handoff', {'within14': exc14, 'within30': exc30, 'per_year_within14': round(exc14 * 12 / months, -1),
                                        'resident_within14': exc14r, 'resident_per_year_within14': round(exc14r * 12 / months, -1)},
    'requests', 'Later reports after hand-off closures beyond what the "done" rate of the same types predicts (hand-off closures x standardised difference), compared types only.',
    'derived', BASE_DER + STD + f'{h14["handoff_closures"]} complete-window hand-off closures x {h14["diff_pts"]} points; per year = x 12/{months} months.',
    'Count of extra reports, not of undone jobs.')
if prox:
    add('r2_proxy_check_r1_fates', prox, 'percent of hand-off closures',
        'Re-report rate (14 / 30 days after closure; 30 days after the promise date) by the fate R1 measured in the city\'s completion record (done by promise / done late / no record).',
        'observed', '311 hand-off closures joined to R1\'s per-request fates (Forestry ledger for weeds; Building Division board-up layer for board-ups), then checked for later requests at the same address and type.',
        'Cuts against using re-reports as a completion measure: board-ups with no record are re-reported LESS (5.9% vs 15.4% within 30 days); weeds are flat (11.5%, 11.5%, 12.5%).',
        src='scripts/night/R2/03_proxy_check.py')
PW = os.path.join(B, 'proxy_check_weeds.csv')
if os.path.exists(PW):
    pw = [r for r in csv.DictReader(open(PW)) if r['problem_code'] == 'Weeds-Vacant Lot' and r['fate']]
    add('r2_proxy_check_weeds_ledger', {r['fate']: {'n': int(r['n']), 'pct_rr30': float(r['pct_rr30'])} for r in pw}, 'percent of hand-off closures',
        'Weeds-Vacant Lot hand-off closures filed in 2026 (promise passed >= 30 days before 13 Oct), re-reported within 30 days of closure, by the first cut billed on the parcel in the Forestry ledger.',
        'observed', '311 requests joined to the Forestry billing ledger by parcel (N1 request_ledger), then checked for later requests at the same address and type.',
        'Flat: re-reports do not track whether the cut happened.', src='scripts/night/R2/03_proxy_check.py')
add('r2_traced_crew_work_12m', X['traced_crew_work_requests_12m'], 'requests a year',
    'Crew-work hand-off closures with a public completion record that R1 joins (weeds via the Forestry ledger, board-ups via the Building Division layer), filed in the 12 months to 13 Oct 2026.',
    'observed', '311 hand-off closures joined to R1\'s composition (traceability = traceable).', src='scripts/night/R2/04_extrapolate.py', period='12 months to 13 Oct 2026')
add('r2_untraced_crew_work_12m', X['untraced_crew_work_requests_12m'], 'requests a year',
    'Crew-work hand-off closures with no public completion record (R1: traceability none or partial), filed in the 12 months to 13 Oct 2026.',
    'observed', '311 hand-off closures joined to R1\'s phrase-level composition (kind and traceability); tree planting excluded once traced by R2.',
    src='scripts/night/R2/04_extrapolate.py', period='12 months to 13 Oct 2026')
add('r2_est_never_done_per_year', X['estimate_never_done_jobs_per_year'], 'jobs a year (low, high)',
    'ESTIMATE of crew-work hand-off jobs a year that may never be done: untraced crew-work volume by category x the range of "no record" shares R1 measured on traceable crew work, with routine route services bounded by their own excess re-report rate, snow excluded and unfunded jobs counted separately.',
    'estimate', 'R1\'s measured "no record by 13 Oct" shares (board-ups 18.4% to missed-cut complaints 37.0%; vacant-lot weeds 34.9%; vacant-building weeds 2025 30.8%) applied to the untraced volume by category (build/R2/extrapolation.csv).',
    'Weakest assumption: that vacant-property crews (mowing, board-ups) fail at the same rate as street, water, towing and traffic crews. Nothing observed supports or refutes it.',
    src='scripts/night/R2/04_extrapolate.py', period='12 months to 13 Oct 2026')
add('r2_est_never_done_2025_volume', X['sensitivity_calendar_2025_volume'], 'jobs (low, high)',
    'As r2_est_never_done_per_year, applied to calendar-2025 volume instead of the last 12 months (2025 had the May tornado and the refuse staff shortage).',
    'estimate', 'Same rates and tiers; volume = crew-work hand-off closures filed in calendar 2025 with no public completion record.',
    src='scripts/night/R2/04_extrapolate.py', period='calendar 2025')
add('r2_est_never_done_mechanical', X['mechanical_never_done_jobs_per_year'], 'jobs a year (low, high)',
    'As r2_est_never_done_per_year but applying the measured range to every untraced crew-work category without plausibility adjustment (snow and unfunded excluded).',
    'estimate', 'Same inputs, no category adjustment.', src='scripts/night/R2/04_extrapolate.py', period='12 months to 13 Oct 2026')
add('r2_est_done_late_per_year', X['estimate_done_late_jobs_per_year'], 'jobs a year (low, high)',
    'ESTIMATE of untraced crew-work jobs a year done only after the promise date: full-range categories x R1\'s measured "done late" shares (44.5% to 64.6%).',
    'estimate', 'R1\'s measured late shares applied to the full-range categories only.', src='scripts/night/R2/04_extrapolate.py', period='12 months to 13 Oct 2026')
unf = [c for c in X['categories'] if c['tier'] == 'separate']
if unf:
    add('r2_unfunded_per_year', unf[0]['requests_12m'], 'requests a year',
        'Crew-work hand-off closures whose words say the work is not funded ("not funded by traffic division", "aldermanic funding support/approval needed").',
        'observed', '311 closing texts, 12 months to 13 Oct 2026.', src='scripts/night/R2/04_extrapolate.py', period='12 months to 13 Oct 2026')
if T:
    g = {x['group']: x for x in T['groups']}
    fc = g['approved, filed Jun 2025-Feb 2026 (fair cohort)']
    bl = g['BASELINE other requests (refuse, potholes, single light), filed Jun 2025-Feb 2026']
    dn = g['closed complete (done), all 2025-26']
    add('r2_tree_planting_fate', {'requests': fc['requests'], 'planted_address_or_25m_pct': fc['pct_address_or_25m'],
                                  'planted_same_address_pct': fc['pct_same_address'], 'planted_by_promise': fc['planted_by_promise_date'],
                                  'median_days_to_planting': fc['median_days_filing_to_planting'],
                                  'no_record_pct': round(100 - fc['pct_address_or_25m'], 1),
                                  'baseline_pct_address_or_25m': bl['pct_address_or_25m'], 'baseline_pct_same_address': bl['pct_same_address'],
                                  'done_closures_matched_pct': dn['pct_address_or_25m'], 'done_closures_n': dn['requests'],
                                  'fate_r1_style': T.get('fair_cohort_fate_r1_style'),
                                  'in_forestry_planting_queue': T.get('fair_cohort_in_planting_queue'),
                                  'cancelled_pct_address_or_25m': g['cancelled, filed Jun 2025-Feb 2026']['pct_address_or_25m'],
                                  'no_site_pct_address_or_25m': g['no appropriate planting site, filed Jun 2025-Feb 2026']['pct_address_or_25m'],
                                  'tree_planting_handoffs_12m': [c['requests_12m'] for c in X['categories'] if c['tier'] == 'traced'][0]},
        'requests / percent',
        'Tree Planting requests closed "approved for next available planting", filed 1 Jun 2025 to 28 Feb 2026: a street-tree planting dated after filing at the same normalised address or within 25 m.',
        'observed',
        '311 requests joined to the city\'s planting records on maps8 (PDA "Planted last 365 days", 27 Oct 2025 to 1 Sep 2026, and the CW_PRINT tree inventory\'s DATE_PLANTED) by N1\'s address normaliser and a 25 m radius; baseline = the same match for refuse, pothole and light requests filed in the same months.',
        'Planted by the 14-day promise: almost none (planting is seasonal). The record\'s recall is below 100%: only 70% of the 20 requests closed "complete" match, so "no record" overstates not-planted.',
        src='scripts/night/R2/06_tree_planting.py', period='filed 1 Jun 2025 to 28 Feb 2026; plantings to 25 Sep 2026')
TD = os.path.join(B, 'tornado_debris_fate.json')
if os.path.exists(TD):
    td = json.load(open(TD))
    add('r2_tornado_debris_trace', {k: td[k] for k in ['segments', 'requests_16may_15jun_2025', 'requests_near_cleared_segment', 'fate_of_matched']},
        'requests', 'Debris requests filed 16 May to 15 Jun 2025 within 30 m of a street segment the city\'s contractor recorded as cleared (23-28 May 2025).',
        'observed', '311 debris requests (one row per REQUESTID, with coordinates) against the city\'s Debris_Clearing layer on ArcGIS Online (76 segments), point-to-line distance.',
        'Negative: the record covers arterial segments only; 35 of 722 requests lie near one and 33 of those were filed after the segment was cleared, so it cannot trace the hand-offs.',
        src='scripts/night/R2/08_tornado_debris.py', period='16 May to 15 Jun 2025')
json.dump({'meta': {'agent': 'R2', 'written': 'see file time', 'labels': 'observed / derived / estimate'}, 'figures': figs},
          open(os.path.join(B, 'figures.json'), 'w'), indent=1)
print(len(figs), 'figures')
