"""N4: write build/N4/figures.json from the outputs of 01-05 (no new analysis except two medians).
Each figure: {id, value, unit, period, definition, label, source_sql_or_script, note, derivation}.
Run after 01..05.
"""
import sys, json
sys.path.insert(0, '/Users/jackriddle/Desktop/stl-civic-hackathon/scripts/night/N4')
from common import connect, OUT
from citystat_targets import METRICS, QS

fit = json.load(open(f'{OUT}/citystat_fit.json'))
q3 = json.load(open(f'{OUT}/q3_2026.json'))
oth = json.load(open(f'{OUT}/other_metrics.json'))
rout = json.load(open(f'{OUT}/routing_search.json'))
sb = json.load(open(f'{OUT}/scoreboard.json'))
search = json.load(open(f'{OUT}/definition_search.json'))
S = 'scripts/night/N4/'
SRC311 = "311 requests (city open data, csb.zip, cleaned of invalid bytes; the file repeats a request once per caller, so counted once per request number)"
SRCCS = "CityStat's own chart tables (Tableau summary data extracted 13 Oct 2026, data/raw/citystat/tableau-extract.md)"
DEFTXT = {
    'N': 'every request filed in the quarter; on time = closed within the goal in elapsed days; cancelled and open count as late',
    'C': 'one row per request number (the file repeats a request once per caller), closed requests only, on time = close date minus filed date <= goal',
    'P': 'as C, but on time = closed by the PRJCOMPLETEDATE the city stamps on each request',
}
F = []


def add(id, value, unit, period, definition, label, script, note, derivation):
    F.append(dict(id=id, value=value, unit=unit, period=period, definition=definition, label=label,
                  source_sql_or_script=S + script, note=note, derivation=derivation))


def deftext(d):
    parts = []
    parts.append({'closed': 'closed requests only', 'notcanc': 'closed and open requests (cancelled dropped)', 'all': 'every request filed'}[d['denom']])
    dd = d['dedup']
    if isinstance(dd, str):
        parts.append('one row per request number')
        if dd != 'id':
            dd = int(dd[2:])
            parts.append('repeat requests at the same address and type ' + ('filed the same day' if dd == 0 else f'within {dd} days') + ' dropped')
    elif dd is not None:
        parts.append('rows at the same address and type ' + ('filed the same day' if dd == 0 else f'within {dd} days') + ' dropped')
    parts.append({'frac': 'on time = elapsed time <= goal', 'cd': 'on time = close date - filed date <= goal',
                  'cdlt': 'on time = close date before the goal date', 'bd': 'on time = weekdays elapsed <= goal',
                  'prom': 'on time = closed by PRJCOMPLETEDATE'}[d['rule']])
    if d['chan'] == 'res':
        parts.append('resident channels only')
    return '; '.join(parts)


# ---- reproduction summary
for name in ('C', 'B', 'N'):
    nmet = sum(1 for k in METRICS if fit[k]['fit'][name]['share_mae_pp'] <= 5)
    cells = sum(fit[k]['fit'][name]['quarters_within_5pp'] for k in METRICS)
    add(f'n4_repro_metrics_within5pp_{name}', nmet, f'of {len(METRICS)} CityStat on-time metrics', '2024 Q1-2026 Q1',
        f'metrics whose mean absolute gap to CityStat is 5 points or less under definition {name}: ' + (DEFTXT.get(name) or 'the best-fitting of 840 combinations for each metric'),
        'observed', '03_compare_and_q3.py', f'metric-quarters within 5 points: {cells} of 81',
        f"{SRC311} recomputed for the nine CityStat on-time measures that rest on 311 data and compared quarter by quarter with {SRCCS}. "
        f"Under definition {name}, {cells} of 81 metric-quarters land within five points of CityStat's published share.")

# ---- counts under definition C (added at the coordinator's request; backs the "reproduces counts" claim)
import csv as _csv
_long = list(_csv.DictReader(open(f'{OUT}/citystat_comparison.csv')))
_cnt = {}
for k in METRICS:
    d = [int(x['ours_n']) - int(x['citystat_n']) for x in _long
         if x['metric'] == k and x['definition'] == 'C' and x['quarter'] in QS[:9]]
    _cnt[k] = dict(diffs=d, exact=sum(1 for v in d if v == 0), mape=fit[k]['fit']['C']['n_mape_pct'],
                   maxabs=max(abs(v) for v in d))
_ok = [k for k in METRICS if _cnt[k]['mape'] <= 0.2]
_bad = [k for k in METRICS if k not in _ok]
_ex = sum(_cnt[k]['exact'] for k in _ok)
add('n4_repro_counts_exact_C', len(_ok), f'of {len(METRICS)} CityStat on-time metrics', '2024 Q1-2026 Q1',
    'metrics whose quarterly request counts under definition C (one row per request number, closed requests only, quarter filed) '
    'match CityStat\'s published counts within 0.2% on average', 'observed', '06_figures.py (from 03_compare_and_q3.py output)',
    f"average count error 0.0-0.2% for these {len(_ok)}; identical in {_ex} of {9*len(_ok)} metric-quarters and never off by more than "
    f"{max(_cnt[k]['maxabs'] for k in _ok)} requests; exact in all nine quarters for "
    f"{', '.join(k for k in _ok if _cnt[k]['exact'] == 9)}. Exception: "
    + '; '.join(f"{k} runs {min(_cnt[k]['diffs'])} to {max(_cnt[k]['diffs'])} requests per quarter against CityStat (average error {_cnt[k]['mape']}%)" for k in _bad)
    + '. Say "within 0.2%" or "exactly in most quarters", not "exactly" unqualified.',
    f"{SRC311}: distinct closed request numbers counted by quarter filed for each CityStat on-time measure and compared quarter by quarter "
    f"with the request counts in {SRCCS}. Counting rows instead of request numbers overcounts by 5-24%, because the file repeats a request once per caller.")

best_def = {}
for k, m in METRICS.items():
    f = fit[k]['fit']
    # decision N4-D05: the shared definition C wherever it reproduces CityStat (mean gap <= 3 points and
    # >= 7 of 9 quarters within 5 points); otherwise the best-fitting of P and B for that metric.
    if f['C']['share_mae_pp'] <= 3 and f['C']['quarters_within_5pp'] >= 7:
        bn = 'C'
    else:
        bn = min(('P', 'B'), key=lambda n: f[n]['share_mae_pp'])
    best_def[k] = bn
    d = fit[k]['definitions'][bn]
    add(f'n4_repro_mae_{k}', f[bn]['share_mae_pp'], 'percentage points (mean absolute gap)', '2024 Q1-2026 Q1',
        f"{m['label']}: our best reproduction ({bn}: {deftext(d)})", 'observed', '03_compare_and_q3.py',
        f"{f[bn]['quarters_within_5pp']}/9 quarters within 5 points; largest gap {f[bn]['share_max_abs_pp']} points; naive definition N gap {f['N']['share_mae_pp']} points",
        f"{SRC311}, problem code(s) {', '.join(m['codes'])}, recomputed per quarter filed and compared with {SRCCS}. "
        f"The definition that came closest ({deftext(d)}) misses CityStat by {f[bn]['share_mae_pp']} points on average over nine quarters.")

# Q2 2026 values per metric, from the comparison CSV
import csv
long = list(csv.DictReader(open(f'{OUT}/citystat_comparison.csv')))
for k, m in METRICS.items():
    bn = best_def[k]
    r = next(x for x in long if x['metric'] == k and x['quarter'] == '2026 Q2' and x['definition'] == bn)
    add(f'n4_q2_2026_{k}_ours', round(float(r['ours_share']) * 100, 1), '% on time', '2026 Q2 (Apr-Jun), closures to 13 Oct 2026',
        f"{m['label']}; definition {bn}: {deftext(fit[k]['definitions'][bn])}", 'observed', '03_compare_and_q3.py',
        f"CityStat published {m['share'][9]*100:.1f}% of {m['n'][9]} (preliminary, 'last updated June 30th'); ours {float(r['ours_share'])*100:.1f}% of {r['ours_n']}",
        f"{SRC311} for requests filed April-June 2026, using every closure in the file to 13 Oct 2026, with the definition that best reproduced CityStat's earlier quarters. "
        f"CityStat's figure was drawn before late closures arrived.")

# snapshot sensitivity and drift (potholes residential and alley)
for k in ('pothole_residential', 'pothole_alley', 'pothole_major'):
    snaps = fit[k]['q2_2026_by_snapshot']
    for lab, key in (('jul1', 'C as of 2026-07-01'), ('aug1', 'C as of 2026-08-01'), ('final', 'C as of file 2026-10-13')):
        v = snaps[key]
        add(f'n4_q2_2026_{k}_C_{lab}', round(v['share'] * 100, 1), '% on time (closed requests only)', '2026 Q2',
            f"{METRICS[k]['label']}; definition C counted with closures before {key.split('as of ')[1]}", 'observed', '03_compare_and_q3.py',
            f"n={v['n']}; CityStat published {METRICS[k]['share'][9]*100:.1f}% of {METRICS[k]['n'][9]}",
            f"{SRC311}, rebuilt as the file would have looked on {key.split('as of ')[1]} by ignoring later closures; requests still open then drop out of a closed-only share, which is why early figures run high.")
    drops = [x['drop_pp'] for x in fit[k]['closed_only_drift']]
    add(f'n4_drift_{k}_max', max(drops), 'percentage points', '2024 Q1-2026 Q1',
        f"largest fall in {METRICS[k]['label']} (definition C) between 12 days after a quarter ended and the full file", 'observed', '03_compare_and_q3.py',
        f"per quarter: {drops}; median {sorted(drops)[len(drops)//2]}",
        f"{SRC311}: each past quarter computed twice, once ignoring closures later than 12 days after the quarter ended and once with every closure to 13 Oct 2026. "
        f"Closed-only on-time shares fall as slow requests finally close.")

# ---- Q3 2026 (not published by CityStat)
con = connect()
for k, m in METRICS.items():
    bn = best_def[k]
    v = q3[k]
    key = {'C': 'C_closed_only', 'P': 'P_promise', 'B': 'B_best'}[bn]
    val = v[key]['share']
    rng = [v[x]['share'] for x in ('C_closed_only', 'P_promise', 'B_best')]
    add(f'n4_q3_2026_{k}', round(val * 100, 1), '% on time', '2026 Q3 (Jul-Sep), file to 13 Oct 2026',
        f"{m['label']}; definition {bn}: {deftext(fit[k]['definitions'][bn])}. Our definition, from the public file.", 'observed', '03_compare_and_q3.py',
        f"n={v[key]['n']}; range across definitions C/P/B {min(rng)*100:.1f}-{max(rng)*100:.1f}%; if every still-open request closes late: {v[('B' if bn == 'B' else 'C') + '_if_open_close_late']['share']*100:.1f}%; "
        f"CityStat Q2 2026 was {m['share'][9]*100:.1f}%",
        f"{SRC311} for requests filed July-September 2026, graded with the definition that best reproduced CityStat's published quarters (mean gap {fit[k]['fit'][bn]['share_mae_pp']} points). "
        f"CityStat has not published Q3; requests still open on 13 Oct can only lower this figure once they close.")

for qq in ('2026 Q2', '2026 Q3'):
    row = con.execute("""SELECT median(days) FILTER (status='CLOSED'), count(*) FILTER (status='CLOSED')
      FROM (SELECT DISTINCT requestid, status, days FROM c WHERE pc = 'Potholes - Residnl' AND q_init = ?)""", [qq]).fetchone()
    add(f"n4_pothole_residential_median_days_{qq.replace(' ', '').lower()}", round(row[0], 1), 'days (median, filed to closed)', qq,
        'residential pothole requests closed so far, all closing words', 'observed', '06_figures.py',
        f'closed n={row[1]}', f"{SRC311}, problem code 'Potholes - Residnl', median of DATETIMECLOSED minus DATETIMEINIT for requests filed in the quarter.")

# ---- routing
top = rout['top'][0]
add('n4_routing_best_subset_mape', round(top['mape'], 1), '% mean absolute error in quarterly request counts', '2024 Q1-2026 Q2',
    'closest subset of the 311 file to the request counts in CityStat\'s routing chart', 'observed', '02_routing_subset.py',
    f"best of {rout['combos_tested']} channel x category subsets ({'+'.join(top['callertypes'])}; {'+'.join(top['grandparent_nodes'])}; nuisance logging dropped) is still {abs(top['counts'][9]-10853)/10853*100:.0f}% off in Q2 2026; whole file is {rout['whole_file'][9]} vs CityStat 10,853. Not reproduced. The file has no routing timestamp, so the 2.5-day share cannot be recomputed at all.",
    f"{SRC311} counted by quarter for every combination of caller channel and request category and compared with {SRCCS} (CSB routing view). No subset matched convincingly.")

# ---- ward map, 2026 claim, within-type
wm = oth['ward_map']
bv = wm['variants'][wm['best_variant']]
add('n4_wardmap_avg_days_mae', bv['avg_days_mae'], 'days (mean absolute gap per ward)', '2024-01-01 to 2026-06-30',
    'average days to close by ward; one row per request number, requests filed in the period, closures before 1 July 2026', 'observed', '04_other_metrics.py',
    f"request counts within {bv['n_mape_pct']}% per ward; without the 1 July cut-off the gap is {wm['variants']['all_file']['avg_days_mae']} days",
    f"{SRC311} averaged by ward and compared with {SRCCS} (CSB ward map). Matching required ignoring closures after 30 June 2026, which indicates the map was frozen then (inferred).")
for w in ('01', '10', '13'):
    x = next(v for v in wm['within_type'] if v['ward'] == w)
    add(f'n4_ward{w}_type_mix_adjusted_avg_days', x['type_mix_adjusted_avg_days'], 'days (average, filed to closed)', '2024-01-01 to 2026-06-30',
        f'Ward {int(w)} average days to close if it had the citywide mix of request types', 'observed', '04_other_metrics.py',
        f"raw average {x['raw_avg_days']} days", f"{SRC311}: each ward's average for each request type, weighted by that type's citywide share; types with fewer than five closures in a ward use the citywide average.")
for y in oth['h1_like_for_like']:
    add(f"n4_h1_{y['year']}_avg_days_by_jul1", y['avg_days_closures_by_jul1'], 'days (average, filed to closed)', f"requests filed Jan-Jun {y['year']}",
        'average days to close, counting only closures before 1 July of the same year (the age CityStat\'s 2026 figure had)', 'observed', '04_other_metrics.py',
        f"same requests with every closure to 13 Oct 2026: {y['avg_days_all_closures_to_13oct2026']} days",
        f"{SRC311}, one row per request number. Compares years at the same age, unlike CityStat's 2026-only map, which sets young 2026 requests beside a 2024-2026 average that includes years-long closures.")

for lab, key, note in (('by_jul1', 'closed_by_0701', 'closures before 1 July 2026, as CityStat drew it'),
                       ('file', 'file', 'every closure to 13 Oct 2026')):
    w9 = next(x for x in wm['h1_2026_by_ward'][key] if x['ward'] == '09')
    add(f'n4_ward09_h1_2026_avg_days_{lab}', w9['avg_days'], 'days (average, filed to closed)', 'requests filed Jan-Jun 2026',
        f'Ward 9 average days to close, {note}', 'observed', '04_other_metrics.py',
        "CityStat's page: 'In 2026 ... the slowest average response time is 13.7 days in Ward 9' (reported)",
        f"{SRC311}, Ward 9, requests filed January-June 2026; the same requests averaged twice, with closures cut at 1 July 2026 and with every closure to 13 Oct 2026.")

# ---- snow, towing
sn = oth['snow']['ours']['distinct_id']
for wk, cs in (('2025-01-12', 17.41), ('2026-01-25', 3.07)):
    add(f"n4_snow_week_{wk}_avg_days", sn[wk]['avg_days'], 'days (average, filed to closed)', f'week of {wk}',
        'snow/ice requests (major and residential), one row per request number', 'observed', '04_other_metrics.py',
        f"CityStat {cs} days; ours n={sn[wk]['n']} (CityStat's counts are 3-18% lower in storm weeks; it appears to merge repeat reports of the same street)", f"{SRC311}, problem codes 'Snow/Ice - Major St' and 'Snow/Ice - Residnl', grouped by week filed and compared with {SRCCS}.")
tw = oth['towing']
cw = [x for x in tw['closure_words'] if x['q'] in QS]
towed = sum(x['closed_vehicle_towed'] for x in cw); closed = sum(x['closed'] for x in cw)
add('n4_tow_closed_says_towed_share', round(towed / closed * 100, 1), '% of closed towing requests', '2024 Q1-2026 Q2',
    "closed 'Vehicle Towing' requests whose closing words say the vehicle was towed", 'observed', '04_other_metrics.py',
    f"{towed} of {closed}; CityStat's own page says closed does not necessarily mean towed. Distinct requests closed in Jul 2026: 129 'tagged for tow', 6 'vehicle towed'; in Aug 2026: 32 and 67, consistent with the change CityStat promised (close only once towed) starting in August (inferred).",
    f"{SRC311}, problem code 'Vehicle Towing', closing words matched for 'towed'.")
dd = next(v for k, v in tw['variants'].items() if k == 'distinct_id')
mape = sum(abs(a['closed'] - b) / b for a, b in zip(dd, tw['citystat']['closed'])) / len(dd) * 100
add('n4_tow_closed_counts_mape', round(mape, 1), '% mean absolute error', '2024 Q1-2026 Q2',
    'closed tow requests per quarter, one row per request number, closures before 1 July 2026, vs CityStat', 'observed', '04_other_metrics.py',
    f"open at 1 July 2026 for Q2: ours {dd[9]['open']} vs CityStat 562; exact match in 2024 Q2 and Q4", f"{SRC311} compared with {SRCCS} (towing dispatch view).")

# ---- promise vs CityStat goals
for code, cs_goal, unit in (('Potholes - Alley', 17, 'days'), ('Whole Blk Lights Out', 1, 'day (24 hours)'), ('Critical Sign', 2, 'days (48 hours)')):
    row = next(x for x in sb['rows'] if x['problemcode'] == code)
    add(f"n4_promise_vs_citystat_{code.lower().replace(' - ', '_').replace(' ', '_')}", row['promise_days'], 'days (city promise date offset)', 'requests filed 2025-2026',
        f"the due date the city's system stamps on '{code}' requests", 'observed', '05_scoreboard.py',
        f"CityStat grades the same service against {cs_goal} {unit}", f"{SRC311}: PRJCOMPLETEDATE minus DATETIMEINIT, modal value; CityStat goal from its page text and chart titles.")

# ---- scoreboard headline
rows = [x for x in sb['rows'] if x['promise_applies']]
sc = sum(x['scored'] for x in rows)
kept = sum(round(x['kept_share'] * x['scored']) for x in rows if x['kept_share'] is not None)
done = sum(round(x['done_kept_share'] * x['scored']) for x in rows if x['done_kept_share'] is not None)
add('n4_sb_types', len(sb['rows']), 'request types', 'filed 2025-01-01 to 2026-10-13', 'types with at least 300 requests', 'observed', '05_scoreboard.py',
    f"{len(rows)} carry a promise date on most requests", f"{SRC311}, all types with 300 or more requests filed since 1 Jan 2025.")
add('n4_sb_kept_all', round(kept / sc * 100, 1), '% of requests closed by the promise date', 'filed 2025-01-01 to 2026-10-13, due by 13 Oct 2026',
    'requests closed on or before their own PRJCOMPLETEDATE, across the 107 request types with 300+ requests since 2025 that carry a due date; cancelled and not-yet-due excluded', 'observed', '05_scoreboard.py',
    f"{kept} of {sc} scored requests", f"{SRC311}; each request graded against the due date the city's own system set on it.")
add('n4_sb_done_kept_all', round(done / sc * 100, 1), '% of requests closed as done by the promise date', 'filed 2025-01-01 to 2026-10-13, due by 13 Oct 2026',
    "as n4_sb_kept_all, and the closing words say the work was done (N2's classes)", 'observed', '05_scoreboard.py',
    f"{done} of {sc}", f"{SRC311}; promise date from PRJCOMPLETEDATE; closing words classed by N2's rule set (research/chapters/N2-closure-classes.csv).")
for code in ('Potholes - Residnl', 'Potholes - Major St', 'Cave-Ins', 'Single Light Out', 'Whole Blk Lights Out', 'Inspect City Tree',
             'Vehicle Towing', 'Debris-alley/street', 'Refuse not collected', 'Sidewalk Repair', 'Illegal dumpg report', 'Weeds-Vacant Lot'):
    x = next(r for r in sb['rows'] if r['problemcode'] == code)
    slug = code.lower().replace(' - ', '_').replace(' ', '_').replace('/', '_').replace('-', '_')
    add(f'n4_sb_{slug}_kept', round(x['kept_share'] * 100, 1), '% closed by the promise date', 'filed 2025-01-01 to 2026-10-13',
        f"'{code}' requests closed on or before their PRJCOMPLETEDATE ({x['promise_days']} days after filing)", 'observed', '05_scoreboard.py',
        f"closed as done by the promise date: {x['done_kept_share']*100:.1f}%; median days late among late ones: {x['median_days_late']}; still open past the promise: {x['open_past_promise']}; cancelled {x['cancelled_share']*100:.1f}%; scored n={x['scored']}",
        x['derivation'])

json.dump(F, open(f'{OUT}/figures.json', 'w'), indent=1, default=str)
print(len(F), 'figures')
for f in F:
    print(f"{f['id']:55s} {f['value']} {f['unit']}")
