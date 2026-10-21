"""R1 figure registry: every number the report uses, read from the R1 outputs (never hand-typed).

Output: build/R1/figures.json  ({id, value, unit, period, definition, label, source_sql_or_script, derivation, note})
Run after 01-06: .venv/bin/python -I scripts/night/R1/07_figures.py
"""
import json, csv, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import OUT, ROOT

comp = json.loads((OUT / 'composition_summary.json').read_text())
fate = json.loads((OUT / 'fate_summary.json').read_text())
base = json.loads((OUT / 'baseline_weeds.json').read_text())
bopen = json.loads((OUT / 'baseline_open.json').read_text())
rest = json.loads((OUT / 'restated.json').read_text())
chk = json.loads((OUT / 'checks.json').read_text())
r2 = {}
r2p = ROOT / 'build/R2/rereport_type_compare.csv'
if r2p.exists():
    for r in csv.DictReader(open(r2p)):
        r2[r['problem_code']] = r

F = []
LEDGER = ("311 requests (city open data, csb.zip; one row per REQUESTID) joined to the Forestry billing ledger "
          "(forestry-service-records.csv) by parcel through MSD's parcel address file; ledger dates are weekly posting batches, "
          "so a cut is dated to the week")
BOARD = ("311 requests joined to the Building Division board-up layer (maps8 BUILDING_DIVISION/Boardups, ParcelID and "
         "DateBoardedUp) on parcel id or normalised address")
CLS = "closing words classed by N2's final rules (build/N2/closure_class.sql)"


def add(id, value, unit, period, definition, label, script, derivation, note=''):
    F.append(dict(id=id, value=value, unit=unit, period=period, definition=definition, label=label,
                  source_sql_or_script=script, derivation=derivation, note=note))


def pct(x):
    return round(100 * x, 1) if x is not None else None


S01, S02, S03, S04, S05, S06 = (f'scripts/night/R1/0{i}_{n}.py' for i, n in
                                [(1, 'composition'), (2, 'fate'), (3, 'baseline_weeds'), (4, 'baseline_open'), (5, 'restate'), (6, 'checks')])
# composition
add('r1_handoff_closures', comp['n_handoff_closures'], 'requests', 'filed 1 Jan 2025-12 Oct 2026, closed',
    'closed requests whose closing words record a hand-off or a work order (N2 classes handed_off, converted)', 'observed', S01,
    f'311 requests, one row per REQUESTID; {CLS}.')
for k in comp['by_kind']:
    add(f"r1_handoff_kind_{k['kind']}_share", pct(k['share']), '%', 'filed 2025-26, closed',
        f"share of hand-off closures that are {k['kind'].replace('_', ' ')}", 'observed', S01,
        f'311 hand-off closures ({CLS}); kind from N2 rule column plus four phrase overrides in scripts/night/R1/common.py.',
        f"n = {k['n']}")
for k in comp['by_traceability']:
    add(f"r1_handoff_{k['traceability']}_share", pct(k['share']), '%', 'filed 2025-26, closed',
        f"share of hand-off closures with traceability '{k['traceability']}' (a public completion record we join / partial / none)",
        'observed', S01, '311 hand-off closures matched to the register of public completion records (N2 register, R1 common.py).',
        f"n = {k['n']}")
# headline
h = fate['headline']
add('r1_traceable_graded_n', h['n_due'], 'requests', 'weeds filed 2026; board-ups filed 2025-26; promise on or before 13 Sep 2026',
    'traceable crew-work hand-offs with a parcel match whose promised date passed at least 30 days before 13 Oct 2026', 'observed', S02,
    f'{LEDGER}; and {BOARD}. 2025 weed requests dropped (2025 ledger thin).')
for k, lab in [('done_by_promise', 'done by the promised date'), ('done_late', 'done after the promised date'),
               ('no_record', 'no record of the work by 13 Oct 2026')]:
    add(f'r1_traceable_{k}_share', pct(h[f'share_{k}']), '%', 'as r1_traceable_graded_n',
        f'share of graded traceable hand-offs {lab}', 'observed', S02,
        f'{LEDGER}; and {BOARD}. Promise = the request\'s own PRJCOMPLETEDATE.', f"n = {h[f'n_{k}']} of {h['n_due']}")
add('r1_traceable_median_days_late', h['median_days_late'], 'days', 'as r1_traceable_graded_n',
    'median days from the promised date to the recorded work, among hand-offs done late', 'observed', S02,
    f'{LEDGER}; and {BOARD}.', f"quartiles {h['q1_days_late']}-{h['q3_days_late']}")
add('r1_traceable_closed_by_promise_share', pct(h['share_closed_by_promise']), '%', 'as r1_traceable_graded_n',
    'share of the same hand-offs that 311 closed on or before the promised date', 'observed', S02,
    '311 close time vs PRJCOMPLETEDATE, same requests as r1_traceable_graded_n.')
add('r1_traceable_done_by_promise_plus7_share', pct(h['share_done_by_promise_plus7']), '%', 'as r1_traceable_graded_n',
    'share done within 7 days after the promised date (allows for weekly ledger posting)', 'observed', S02,
    f'{LEDGER}; and {BOARD}.')
# per service
names = {'Weeds, vacant lot (2026 filings)': 'weeds_lot', 'Weeds, vacant building (2026 filings)': 'weeds_bldg',
         'Missed or unsatisfactory cut complaints (2026 filings)': 'cut_complaints',
         'Referred to board-up crew (2025-26 filings)': 'boardup'}
for r in fate['by_service']:
    if r['service'] not in names:
        continue
    sid = names[r['service']]
    src = BOARD if sid == 'boardup' else LEDGER
    for k in ('done_by_promise', 'done_late', 'no_record', 'closed_by_promise'):
        add(f'r1_{sid}_{k}_share', pct(r[f'share_{k}']), '%', r['service'], f"{r['service']}: share {k.replace('_', ' ')}",
            'observed', S02, src + '.', f"n = {r['n_due']}")
    add(f'r1_{sid}_median_days_late', r['median_days_late'], 'days', r['service'], 'median days late among those done late',
        'observed', S02, src + '.')
for r in fate['headline_by_ward_group']:
    wg = r['service'].replace('ward group ', '')
    add(f"r1_traceable_no_record_share_wards_{wg.replace('-', '_')}", pct(r['share_no_record']), '%', 'as r1_traceable_graded_n',
        f'no record of the work, wards {wg}', 'observed', S02, f'{LEDGER}; and {BOARD}.', f"n = {r['n_due']}")
# baseline: request vs same-block
sb = {r['group']: r for r in base['same_block']}
a, b = sb['all (lots and buildings)'], sb['requested parcel itself cut in 2026 (like controls)']
for tag, r in [('all', a), ('rotation', b)]:
    for k in ('14d', '30d'):
        add(f'r1_weeds_req_cut_{k}_{tag}', pct(r[f'req_cut_{k}']), '%', '2026 requests closed "on schedule"/"added to rotation", filed by 13 Sep',
            f'requested parcels cut within {k} of the request ({tag})', 'observed', S03, LEDGER + '; same-block controls from ledger CITYBLOCK.',
            f"n = {r['n_units']} parcel-dates")
        add(f'r1_weeds_ctl_cut_{k}_{tag}', pct(r[f'ctl_cut_{k}']), '%', 'same dates',
            f'same-block rotation parcels with no request in the prior 60 days, cut within {k} of the same date ({tag})', 'observed', S03,
            LEDGER + '; controls = other parcels on the same ledger CITYBLOCK cut at least once in 2026, no weed request in the 60 days to the date.')
add('r1_weeds_req_no_cut_all', pct(a['req_no_cut_by_13oct']), '%', 'as above', 'requested parcels with no cut billed by 13 Oct', 'observed', S03, LEDGER + '.')
add('r1_weeds_ctl_no_cut_all', pct(a['ctl_no_cut_by_13oct']), '%', 'as above', 'same-block rotation controls with no cut billed by 13 Oct', 'observed', S03, LEDGER + '.')
nrot = a['n_units'] - b['n_units']
add('r1_weeds_req_not_on_rotation_share', pct(nrot / a['n_units']), '%', 'as above',
    'requested parcel-dates on parcels with no cut billed at any time in 2026', 'observed', S03, LEDGER + '.', f'{nrot} of {a["n_units"]}')
# kept open
for r in bopen['by_group']:
    key = None
    if r['comparison'] == 'Weeds-Vacant Lot 2026 | still open':
        key = 'r1_open_weeds_lot_no_record_share'
    elif r['comparison'] == 'Vacant building unsecured 2025-26 (board-ups) | still open':
        key = 'r1_open_vbu_no_record_share'
    elif r['comparison'] == 'Weeds-Vacant Bldg 2026 | still open':
        key = 'r1_open_weeds_bldg_no_record_share'
    if key:
        add(key, pct(r['share_no_record']), '%', r['comparison'], 'share with no record of the work, requests still open on 13 Oct',
            'observed', S04, (BOARD if 'board' in r['comparison'] else LEDGER) + '.', f"n = {r['n_due']}")
for r in bopen['lra_demolition']:
    if r['status_group'] == 'open':
        add('r1_lra_demo_open_already_demolished_share', pct(r['share_demolished_after_filing']), '%', 'LRA demolition submissions filed 2025-26, still open',
            'share with a completed demolition permit at the parcel or address after filing', 'observed', S04,
            '311 LRA Demo Submission requests joined to the Building Division demolition-permit layer (ParcelID / address, PermitStatus Completed, DateClosed).',
            f"{r['n_demolished_after_filing']} of {r['n']}; median {r['median_days_to_demolition']} days after filing")
# checks
q0 = chk['boardup_referred_queue'][0]
add('r1_boardup_order_to_boarded_median_days', q0['median_days_order_to_boarded'], 'days', 'referred to board-up crew, filed 2025-26',
    'median days from the board-up order (DateCreated) to DateBoardedUp', 'observed', S06, BOARD + '.', f"{q0['n_order_boarded']} of {q0['n_orders']} orders boarded")
bc = fate['record_checks']['boardup_handoff_created_vs_closed'][0]
add('r1_boardup_order_created_within_2d_of_close_share', pct(bc['share_created_within_2d_of_close']), '%', 'referred to board-up crew, filed 2025-26',
    'share of referred requests whose board-up order was created within 2 days of the 311 closure', 'observed', S02, BOARD + '.',
    f"median {round(bc['median_days_created_minus_311_close'] * 24, 1)} hours after the 311 closure")
# restated CityStat
for r in rest['citystat']:
    if r['period'].startswith('2026 Q2'):
        m = r['metric']
        add(f'r1_citystat_{m}_q2_2026_ontime_ours', pct(r['ontime_share_ours']), '%', '2026 Q2 (filed)', f"{r['label']}: on-time share, N4 definition C",
            'observed', S05, '311 requests, one row per REQUESTID, closed only, by quarter filed (N4 definition C).',
            f"CityStat published {pct(r['citystat_published_share'])}%")
        add(f'r1_citystat_{m}_q2_2026_handoff_share_of_ontime', pct(r['share_of_ontime_closures_handoff']), '%', '2026 Q2 (filed)',
            'share of on-time closures whose words record a hand-off', 'observed', S05, f'N4 definition C; {CLS}.')
        add(f'r1_citystat_{m}_q2_2026_ontime_done_only', pct(r['ontime_share_counting_only_done']), '%', '2026 Q2 (filed)',
            'on-time share counting only closures whose words say the work was done (same denominator)', 'observed', S05, f'N4 definition C; {CLS}.')
# R2 cross-reference for the 'is not'
for pc, tag in [('Potholes - Residnl', 'pothole_res'), ('Whole Blk Lights Out', 'whole_block'), ('Weeds-Vacant Lot', 'weeds_lot'),
                ('Weeds-Vacant Bldg', 'weeds_bldg'), ('Vacnt Bldg Unsecured', 'vbu')]:
    if pc in r2:
        add(f'r1_r2_rereport14_{tag}_done', float(r2[pc]['done_pct14']), '%', 'closures 2025-26, complete 14-day window',
            f'{pc}: re-reported within 14 days after a "done" closure (R2)', 'observed', 'build/R2/rereport_type_compare.csv (R2)',
            'R2: another request at the same normalised address and type within 14 days of closure.')
        add(f'r1_r2_rereport14_{tag}_handoff', float(r2[pc]['handoff_pct14']), '%', 'closures 2025-26, complete 14-day window',
            f'{pc}: re-reported within 14 days after a hand-off closure (R2)', 'observed', 'build/R2/rereport_type_compare.csv (R2)',
            'R2: another request at the same normalised address and type within 14 days of closure.')

# robustness and resident impact
add('r1_traceable_median_days_to_close_311', round(h['median_days_to_close_311'], 1), 'days', 'as r1_traceable_graded_n',
    'median days from filing to the 311 closure', 'observed', S02, '311 file, same requests as r1_traceable_graded_n.')
add('r1_traceable_median_days_filing_to_work', h['median_days_filing_to_done'], 'days', 'as r1_traceable_graded_n',
    'median days from filing to the recorded work, where work is recorded', 'observed', S02, f'{LEDGER}; and {BOARD}.')
old = [r for r in chk['no_record_by_promise_age'] if r['promise_age'].startswith('promise <=')]
n_old = sum(r['n'] for r in old)
add('r1_traceable_no_record_share_promise_3m', pct(sum(r['n'] * r['share_no_record'] for r in old) / n_old), '%',
    'promise on or before 13 Jul 2026 (at least 92 days before 13 Oct)', 'no record of the work, hand-offs whose promise passed at least three months earlier',
    'observed', S06, f'{LEDGER}; and {BOARD}.', f'n = {n_old}; weeds and board-ups pooled')
add('r1_traceable_done_by_promise_share_promise_3m', pct(sum(r['n'] * r['share_done_by_promise'] for r in old) / n_old), '%',
    'as r1_traceable_no_record_share_promise_3m', 'done by the promise, same set', 'observed', S06, f'{LEDGER}; and {BOARD}.', f'n = {n_old}')
for r in chk['no_record_by_promise_age']:
    tag = {'promise <= 13 Jul (>=92 d before 13 Oct)': '92d', 'promise 14 Jul-13 Aug (61-91 d)': '61_91d', 'promise 14 Aug-13 Sep (30-60 d)': '30_60d'}[r['promise_age']]
    add(f"r1_{r['rec']}_no_record_share_promise_age_{tag}", pct(r['share_no_record']), '%', r['promise_age'],
        f"no record of the work ({r['rec']}), by time since the promise", 'observed', S06,
        (BOARD if r['rec'] == 'boardup' else LEDGER) + '.', f"n = {r['n']}")
lag = [r for r in chk['boardup_lag_done_closures'] if 'secured' in r['res_key']]
n_l, w_l = sum(r['n'] for r in lag), sum(r['n_with_record'] for r in lag)
add('r1_boardup_record_recall_city_secured', pct(w_l / n_l), '%', "311 'Vacnt Bldg Unsecured' closed 'building was (re-)secured by city', filed 2024-26",
    'share of buildings the city says it secured that have a board-up record dated on or after filing (the record\'s recall)', 'observed', S06,
    BOARD + '.', f'{w_l} of {n_l}; the layer date is a median 14 (re-secured) to 29 (secured) days after the 311 closure')
lra = next(r for r in fate['by_service'] if r['service'].startswith('Weeds, vacant lot, land-bank'))
add('r1_weeds_lot_lra_no_record_share', pct(lra['share_no_record']), '%', 'Weeds-Vacant Lot hand-offs filed 2026 on land-bank (LRA) parcels',
    'no cut billed on a city-owned lot by 13 Oct, promise passed by 13 Sep', 'observed', S02, LEDGER + '; LRA inventory parcel ids.', f"n = {lra['n_due']}")
own = next((r for r in bopen['by_group'] if r['comparison'] == 'Vacant building unsecured 2025-26 (board-ups) | closed at hand-off (owner_enforcement)'), None)
if own:
    for k in ('done_by_promise', 'done_late', 'no_record'):
        add(f'r1_vbu_owner_notice_city_boardup_{k}_share', pct(own[f'share_{k}']), '%', 'Vacnt Bldg Unsecured closed with an owner notice, filed 2025-26',
            f'city board-up recorded after an owner-notice closure: {k.replace("_", " ")}', 'observed', S04, BOARD + '.', f"n = {own['n_due']}")
ppp = chk['weeds_first_request_per_parcel']
ppp = ppp[0] if isinstance(ppp, list) else ppp
add('r1_weeds_no_record_share_per_parcel', pct(ppp['no_record']), '%', 'first 2026 weed hand-off per parcel, promise by 13 Sep',
    'no cut recorded, counting each parcel once', 'observed', S06, LEDGER + '.', f"n = {ppp['n_parcels']} parcels")

# ranges for R2's extrapolation (inferred from the measured rates above; R2 chooses how to use them)
import math
def wilson(k, n, z=1.96):
    ph = k / n; d = 1 + z * z / n; c = ph + z * z / (2 * n); r = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return round(100 * (c - r) / d, 1), round(100 * (c + r) / d, 1)
lo, hi = wilson(w_l, n_l)
add('r1_boardup_record_recall_ci95', f'{lo}-{hi}', '%', 'as r1_boardup_record_recall_city_secured', 'Wilson 95% interval for the board-up record\'s recall',
    'observed', S06, BOARD + '.', 'so the record misses roughly 12-30% of board-ups the city says it did')
byage = {(r['rec'], r['promise_age'][:9]): r for r in chk['no_record_by_promise_age']}
bu3 = byage[('boardup', 'promise <')]['share_no_record']; wd3 = byage[('weeds', 'promise <')]['share_no_record']
add('r1_range_never_done_low', pct(bu3), '%', 'promise at least three months before 13 Oct 2026',
    'low end of the measured "no record of the work" rate for crew-work hand-offs: board-up referrals three months past the promise',
    'inferred', S06, f'{BOARD}. Raw rate, before allowing for the layer missing about one board-up in five.',
    'after allowing for the board-up layer\'s own miss rate (recall 80.6%, 95% CI ' + f'{lo}-{hi}' + '%), board-up no-record is indistinguishable from zero')
add('r1_range_never_done_high', pct(wd3), '%', 'promise at least three months before 13 Oct 2026',
    'high end of the measured "no record of the work" rate: weed hand-offs (lots, buildings, cut complaints) three months past the promise',
    'inferred', S06, LEDGER + '.', 'land-bank lots alone (city-owned): ' + str(pct(lra['share_no_record'])) + '% at 30+ days')
add('r1_range_late_low', pct(next(r for r in fate['by_service'] if r['service'].startswith('Weeds, vacant lot (2026'))['share_done_late']), '%',
    'promise passed by 13 Sep 2026', 'low end of the measured done-late rate (weeds, vacant lots)', 'inferred', S02, LEDGER + '.')
add('r1_range_late_high', pct(next(r for r in fate['by_service'] if r['service'].startswith('Referred to board-up crew (2025'))['share_done_late']), '%',
    'promise passed by 13 Sep 2026', 'high end of the measured done-late rate (board-up referrals; may include recording lag)', 'inferred', S02, BOARD + '.')

for k, lab in [('all', 'all requested parcel-dates'), ('on_rotation', 'requested parcels on the 2026 rotation'),
               ('on_rotation_lots', 'vacant lots on the rotation'), ('on_rotation_buildings', 'vacant buildings on the rotation')]:
    b = base['paired_diff_bootstrap'][k]
    for w in ('14d', '30d'):
        add(f'r1_weeds_request_effect_{w}_{k}', round(100 * b[f'diff_{w}'], 1), 'percentage points', '2026 requests closed "on schedule"/"added to rotation", filed by 13 Sep',
            f'requested minus same-block control: share cut within {w} ({lab})', 'observed', S03,
            LEDGER + '; same-block rotation controls; 95% interval from 1,000 bootstrap resamples of city blocks.',
            f"95% CI {round(100 * b[f'diff_{w}_ci95'][0], 1)} to {round(100 * b[f'diff_{w}_ci95'][1], 1)}; {b['n_units']} parcel-dates on {b['n_blocks']} blocks")

for r in chk['boardup_by_year']:
    for k in ('by_promise', 'late', 'no_record'):
        add(f"r1_boardup_{r['y']}_{k}_share", pct(r[k]), '%', f"referred to board-up crew, filed {r['y']}, promise by 13 Sep 2026",
            f'board-up referrals {k.replace("_", " ")}, by filing year', 'observed', S06, BOARD + '.', f"n = {r['n']}; median days late {r['median_days_late']}")
for r in chk['no_record_wait_so_far']:
    add(f"r1_{r['rec']}_no_record_median_days_past_promise", r['median_days_past_promise'], 'days', 'as r1_traceable_graded_n',
        'median days from the promise to 13 Oct 2026 for hand-offs with no record of the work', 'observed', S06,
        (BOARD if r['rec'] == 'boardup' else LEDGER) + '.', f"n = {r['n']}; median {r['median_days_since_filing']} days since filing")
mm = chk['weeds_match_method']
ex = sum(r['n'] for r in mm if r['method'].startswith('exact')); tot = sum(r['n'] for r in mm)
add('r1_weeds_exact_parcel_match_share', pct(ex / tot), '%', 'graded 2026 Weeds-Vacant Lot/Bldg hand-offs',
    'share matched to their parcel by exact normalised address (MSD, LRA or Forestry list)', 'observed', S06, LEDGER + '.', f'{ex} of {tot}')
pl = next(x for x in chk['no_record_distinct_places'] if x['rec'] == 'weeds')
add('r1_weeds_no_record_requests', pl['n_requests'], 'requests', 'weed hand-offs filed 2026, promise by 13 Sep',
    'weed requests closed at a hand-off with no cut billed by 13 Oct 2026', 'observed', S06, LEDGER + '.', f"on {pl['n_places']} parcels")
pb = next(x for x in chk['no_record_distinct_places'] if x['rec'] == 'boardup')
add('r1_boardup_no_record_requests', pb['n_requests'], 'requests', 'board-up referrals filed 2025-26, promise by 13 Sep',
    'board-up referrals with no board-up recorded by 13 Oct 2026 (within the layer miss rate; not evidence of lost work)', 'observed', S06, BOARD + '.', f"on {pb['n_places']} buildings")

lc = next(r for r in chk['lra_ledger_coverage_2026'] if r['property_type'] == 'Lot')
add('r1_lra_lots_with_2026_cut_share', pct(lc['share_with_2026_cut']), '%', '2026 to 13 Oct', 'land-bank (LRA) lots with at least one cut billed in 2026',
    'observed', S06, 'LRA inventory parcel ids joined to the Forestry billing ledger (distinct parcel-days).', f"n = {lc['n']} lots")
sens = next(r for r in fate['by_service'] if r['service'].startswith('SENSITIVITY Weeds, vacant building (2025'))
for k in ('done_by_promise', 'done_late', 'no_record'):
    add(f'r1_weeds_bldg_2025_{k}_share', pct(sens[f'share_{k}']), '%', 'Weeds-Vacant Bldg hand-offs filed 2025 (sensitivity)',
        f'2025 vacant-building weed hand-offs: {k.replace("_", " ")} by 13 Oct 2026', 'observed', S02,
        LEDGER + '; the 2025 Weed-Grass ledger (the vacant-building cut) is about as full as 2026 (8,182 vs 8,369 distinct cuts).', f"n = {sens['n_due']}")

for svc_label, tag in [('Weeds, vacant lot, "on schedule to be cut" only (2026)', 'weeds_lot_onschedule'),
                       ('Weeds, vacant lot, "added to rotation" only (2026)', 'weeds_lot_rotation'),
                       ('Weeds, vacant building, "on schedule to be cut" only (2026)', 'weeds_bldg_onschedule'),
                       ('Weeds, vacant building, "added to rotation" only (2026)', 'weeds_bldg_rotation')]:
    r = next(x for x in fate['by_service'] if x['service'] == svc_label)
    for k in ('done_by_promise', 'done_late', 'no_record'):
        add(f'r1_{tag}_{k}_share', pct(r[f'share_{k}']), '%', svc_label, f"{svc_label}: share {k.replace('_', ' ')}", 'observed', S02, LEDGER + '.',
            f"n = {r['n_due']}")

tc = fate['trees_cancelled_blank_with_open_order']
add('r1_trees_cancelled_with_open_order', tc['n_with_open_removal_order_before_filing'], 'requests', 'Inspect City Tree filed 2025-26, cancelled with no words',
    'blank-cancelled tree inspections filed where a removal order at the same address was already open (started more than a day before)',
    'observed', S02, '311 requests matched by normalised address to Cityworks saved search 6955 (open easement tree-removal orders, 1,500-row sample; UTC dates); a lower bound.',
    f"of {tc['n_cancelled_blank']}; median order age at filing {round(tc['median_order_age_at_filing_days'])} days")
add('r1_trees_open_order_past_due_share', pct(tc['share_order_past_own_due_13oct']), '%', 'as r1_trees_cancelled_with_open_order',
    'share of those removal orders past their own projected finish date on 13 Oct 2026', 'observed', S02,
    'Cityworks saved search 6955 ProjFinishDate (UTC) vs 13 Oct 2026.', f"median {tc['median_days_order_past_due_13oct']} days past due")
tr25 = next(r for r in fate['trees_removal_order_created'] if r['phrase'] == 'removal work order created' and r['init_year'] == 2025)
add('r1_trees_converted_2025_still_open', tr25['n_matching_order_still_open'], 'requests', 'tree requests closed "removal work order created", filed 2025',
    'with an open removal order at the same address dated after the request, on 13 Oct 2026', 'observed', S02,
    '311 requests matched by normalised address to Cityworks saved search 6955 (open orders only).',
    f"of {tr25['n']}; the open-order list appears complete for orders started before 8 Jan 2026 (inferred), so most of these orders were closed")

(OUT / 'figures.json').write_text(json.dumps(F, indent=1, default=str))
print(len(F), 'figures')
