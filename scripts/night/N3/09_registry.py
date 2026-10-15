"""N3 step 9: write build/N3/figures.json and build/N3/decisions.json from the computed outputs (no typed-in numbers
except CityStat's published values, which are quoted from data/raw/citystat/tableau-extract.md).
Run after steps 0-8: .venv/bin/python -I scripts/night/N3/09_registry.py
"""
import json, os, csv, collections, sys, duckdb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classes import first_pass, load_n2, key
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
B = os.path.join(ROOT, 'build/N3')
S = 'scripts/night/N3/'
dec = json.load(open(os.path.join(B, 'decomposition.json')))
rob = json.load(open(os.path.join(B, 'decomposition_robustness.json')))
cs = json.load(open(os.path.join(B, 'citystat_reproduction.json')))
bnd = json.load(open(os.path.join(B, 'boundaries.json')))
src = json.load(open(os.path.join(B, 'class_source.json')))['class_source']
rc = list(csv.DictReader(open(os.path.join(B, 'robust_comparisons.csv'))))
def R(t, m, p): return next(r for r in rc if r['ptype'] == t and r['measure'] == m and r['period'] == p)
con = duckdb.connect(); REQ = os.path.join(B, 'req.parquet')

# duplicates (raw rows vs distinct ids, 2024-2026 files)
con.execute(f"""CREATE TABLE raw AS SELECT REQUESTID FROM read_csv(['{ROOT}/build/csb-clean/2024.csv','{ROOT}/build/csb-clean/2025.csv','{ROOT}/build/csb-clean/2026.csv'],
                header=true, all_varchar=true, union_by_name=true)""")
nrows, ndist = con.execute("SELECT count(*), count(DISTINCT REQUESTID) FROM raw").fetchone()
nrep = con.execute("SELECT count(*) FROM (SELECT REQUESTID FROM raw GROUP BY 1 HAVING count(*) > 1)").fetchone()[0]
win = con.execute(f"SELECT count(*) FROM '{REQ}' WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01'").fetchone()[0]

# class agreement N2 vs N3 first pass (by closures)
agree = tot = 0
n2 = load_n2()
if n2:
    with open(os.path.join(ROOT, 'research/chapters/N2-closure-classes.csv'), newline='', encoding='utf-8', errors='replace') as fh:
        for r in csv.DictReader(fh):
            n = int(float(r['n'] or 0)); fp = first_pass(r['resolution_text']); fp = 'handed_off' if fp == 'enforcement' else fp
            tot += n; agree += n * (fp == r['class'])

d1 = dec['citystat_window_snapshot_2026-07-10 | ward 1 vs ward 10']
d2 = dec['citystat_window_snapshot_2026-07-10 | wards 1-5 vs 10-14']
m1 = rob['citystat_window_snapshot | ward 1 vs ward 10']
tow_a, tow_b = R('Vehicle Towing', 'text: vehicle tagged for tow', 'after'), R('Vehicle Towing', 'text: vehicle tagged for tow', 'before')
gone_a = R('Vehicle Towing', 'text: vehicle gone upon inspection', 'after')
cav_ref = R('Cave-Ins', 'text: referred to street maintenance for repair work to be scheduled', 'after')
cav_done = R('Cave-Ins', 'done-class', 'after')
slo_a, slo_b = R('Single Light Out', 'done-class', 'after'), R('Single Light Out', 'done-class', 'before')
pme_a, pme_b = R('Ppty Maint Code-Ext', 'text: issued notice of violation', 'after'), R('Ppty Maint Code-Ext', 'text: issued notice of violation', 'before')
nogap = {t: R(t, 'done-class', 'after') for t in ('Whole Blk Lights Out', 'Potholes - Residnl', 'Refuse not collected', 'Containr damaged')}
cv = {r['ward']: r for r in bnd['cave_ins_by_ward_after']}
DER_RES = "311 requests (City of St. Louis open data, csb.zip yearly CSVs, invalid bytes dropped), one row per REQUESTID; resident-filed requests only (web, phone, email, chat, Twitter, letter)."
PER_A, PER_B = '16 May 2025 - 13 Oct 2026 (filed)', '1 Jan 2024 - 15 May 2025 (filed)'
F = []
def fig(id, value, unit, period, definition, label, script, derivation, note=''):
    F.append(dict(id=id, value=value, unit=unit, period=period, definition=definition, label=label,
                  source_sql_or_script=S + script, derivation=derivation, note=note))

fig('n3_duplicate_request_rows', dict(rows=nrows, distinct_request_ids=ndist, ids_repeated=nrep), 'rows / request ids', '2024-2026 yearly files',
    'Rows in the public 311 yearly files vs distinct REQUESTID; ids appearing more than once', 'observed', '00_load.py',
    'Counted rows and distinct REQUESTIDs in the city\'s 2024, 2025 and 2026 CSB files. Repeated rows are identical except CALLERTYPE, so they look like one row per caller; we keep one row per request.',
    'Medians computed on rows weight multi-caller requests; dedupe before any count or median.')
fig('n3_citystat_ward1_reproduced', round(cs['D as A, closed requests with closed date <= 2026-06-30 only']['ward01'][2], 2), 'mean days to close', '1 Jan 2024 - 30 Jun 2026',
    'Mean DATETIMECLOSED-DATETIMEINIT over STATUS=CLOSED requests closed by 30 Jun 2026, all channels, ward 1', 'observed', '01_citystat_ward.py',
    "311 requests (csb.zip), one row per REQUESTID, all channels and types, filed in CityStat's window; mean days to close for requests closed by the window end. CityStat publishes 17.18 for ward 1 (tableau-extract.md).",
    'A July 2026 snapshot (closed by 10 Jul) gives 17.36; see decomposition.')
fig('n3_citystat_reproduction_error', round(cs['D as A, closed requests with closed date <= 2026-06-30 only']['mean_abs_err_avg_days'], 2), 'days (mean absolute error across 14 wards)', '1 Jan 2024 - 30 Jun 2026',
    "How closely our definition reproduces CityStat's 14 ward averages", 'observed', '01_citystat_ward.py',
    "Compared our ward means (one row per REQUESTID, all channels, mean over closed requests) with CityStat's CSBRequestMap values extracted 13 Oct 2026. Ward request counts match within 1% once duplicate rows are removed (about 8% high without that).",
    f'Our window total {win:,} distinct requests vs CityStat 286,148. Wards 10-12 are 2-3 days lower in ours.')
fig('n3_decomp_ward1_vs_10_gap', round(d1['gap'], 1), 'mean days', '1 Jan 2024 - 30 Jun 2026, closed by 10 Jul 2026',
    "CityStat's metric: ward 10 mean days to close minus ward 1", 'observed', '03_decompose.py',
    "311 requests (csb.zip), one row per REQUESTID, all channels, as CityStat counts them; ward 1 17.4 vs ward 10 33.1 days (CityStat shows 17.2 vs 35.1).")
for k, lab, d in [('type_mix', 'mix of request types', 'Kitagawa type-mix term'),
                  ('closing_practice', 'closing words used (class shares within type)', 'Kitagawa closing-practice term'),
                  ('speed_done', 'slower handling, closures recording work done', 'speed term, done class'),
                  ('speed_other', 'slower handling, hand-off / no-action / other closures', 'speed term, all non-done classes')]:
    fig(f'n3_decomp_ward1_vs_10_{k}', round(d1[k], 2), 'mean days (share of gap in note)', '1 Jan 2024 - 30 Jun 2026, closed by 10 Jul 2026',
        f'Part of the ward 1 vs ward 10 gap due to {lab}', 'observed', '03_decompose.py',
        "311 requests (csb.zip), one row per REQUESTID, all channels; closures classed by their closing words (N2's reviewed classes). Exact two-level split of the mean gap: type mix, then share of each closing class within type, then speed within the same type and class.",
        f'{d1[k] / d1["gap"]:.0%} of the {d1["gap"]:.1f}-day gap.')
de = dec['citystat_window_snapshot_2026-07-10 | ward 1 vs ward 10 | enforcement notices as own class']
fig('n3_decomp_ward1_vs_10_enforcement_variant', dict(type_mix=round(de['type_mix'], 2), closing_practice=round(de['closing_practice'], 2),
    speed_done=round(de['speed_done'], 2), speed_enforcement=round(de['speed_by_class'].get('enforcement', 0), 2),
    speed_handoff=round(de['speed_by_class'].get('handed_off', 0), 2), speed_other=round(de['speed_other'] - de['speed_by_class'].get('enforcement', 0) - de['speed_by_class'].get('handed_off', 0), 2)),
    'mean days', '1 Jan 2024 - 30 Jun 2026, closed by 10 Jul 2026',
    'Same decomposition with enforcement notices (N2 rule handed_off:enforcement) as their own class', 'observed', '03_decompose.py',
    "As n3_decomp_ward1_vs_10_*, but notices of violation, 'already under notice' and summons are separated from other hand-offs; the split barely moves.",
    f"Mix + closing words {de['type_mix'] + de['closing_practice']:.1f} of {de['gap']:.1f} days with the split, {d1['type_mix'] + d1['closing_practice']:.1f} without.")
fig('n3_decomp_w15_vs_w1014_type_mix', round(d2['type_mix'], 2), 'mean days', '1 Jan 2024 - 30 Jun 2026, closed by 10 Jul 2026',
    'Type-mix term, wards 1-5 vs 10-14 (negative = the north files a faster-closing mix)', 'observed', '03_decompose.py',
    "Same decomposition for wards 1-5 vs 10-14: the north's mix of request types would make it faster, not slower; its gap is all within-type.",
    f"Gap {d2['gap']:.1f} d = mix {d2['type_mix']:.1f} + closing words {d2['closing_practice']:.1f} + speed (done) {d2['speed_done']:.1f} + speed (other) {d2['speed_other']:.1f}.")
fig('n3_median_ward10_at_ward1_mix', round(m1['median_B_at_A_type_class_mix'], 1), 'median days', '1 Jan 2024 - 30 Jun 2026, closed by 10 Jul 2026',
    "Ward 10's median days to close if it had ward 1's mix of request types and closing words (reweighted)", 'observed', '04_reweight.py',
    "311 requests (csb.zip), one row per REQUESTID, all channels; ward 10's closures reweighted to ward 1's type-by-closing-class shares.",
    f"Observed: ward 10 {m1['median_B']:.1f}, ward 1 {m1['median_A']:.1f}. Matching the mix does not shrink the gap.")
fig('n3_towing_tagged_median_after', dict(wards_1_5=float(tow_a['med_south']), wards_10_14=float(tow_a['med_north']), n=[int(tow_a['n_south']), int(tow_a['n_north'])],
    ci95_ratio=[float(tow_a['ci_lo']), float(tow_a['ci_hi'])]), 'median days', PER_A,
    'Median days from filing to a closure reading "vehicle tagged for tow"', 'observed', '06_robust.py', DER_RES +
    " Compared only closures with the same closing words, \"vehicle tagged for tow\", which needs a visit; the city's promise for every towing request is 5 days.",
    f"Before the tornado: {tow_b['med_south']} vs {tow_b['med_north']} (n {tow_b['n_south']}/{tow_b['n_north']}). All five north wards slower than every ward 1-5 after the tornado.")
fig('n3_towing_closed_by_promise_after', dict(wards_1_5=float(tow_a['closed_by_promise_south']), wards_10_14=float(tow_a['closed_by_promise_north'])), 'share of requests', PER_A,
    'Share of towing requests closed (any words) by the city\'s own promise date; open and cancelled count as not', 'observed', '06_robust.py',
    DER_RES + " Promise = PRJCOMPLETEDATE, set by the city on each request (5 days for towing); only requests whose promise date had passed by 13 Oct 2026.")
# Retired for public use (N8 conflict 1, re-check R6, 14 Oct 2026): the share above counts any closing words, so
# "vehicle gone upon inspection", "no problem found" and blank closings count as kept promises. Kept in the registry
# for the record; N1's merge and N6's bridge keep retired figures off everything the site reads.
F[-1]['retired'] = True
F[-1]['note'] = ("Retired for public use 14 Oct 2026 (N8 conflict 1): counts closures with any words, so 'vehicle gone upon inspection', "
                 "'no problem found' and blank closings count as kept promises. Use n3_towing_tagged_by_promise_after, the same population "
                 "and closing words as the 12.0 vs 36.9-day medians.")

# Like-for-like promise share for towing (N8 conflict 1): re-derived from the cleaned 311 CSVs, one row per REQUESTID (the
# row with the best channel, as in 00_load.py), resident if any row is a resident channel, filed on or after 16 May 2025,
# STATUS CLOSED with PUBLICRESOLUTION 'vehicle tagged for tow'; kept = DATETIMECLOSED <= PRJCOMPLETEDATE (timestamps).
_tow_files = ', '.join(f"'{ROOT}/build/csb-clean/{y}.csv'" for y in (2025, 2026))
_tow = {g: (n, k, kc) for g, n, k, kc in con.execute(f"""
    WITH raw AS (SELECT * FROM read_csv([{_tow_files}], header=true, all_varchar=true, quote='"', escape='"', union_by_name=true)),
    typed AS (SELECT REQUESTID, upper(trim(CALLERTYPE)) AS ct,
                     CASE WHEN upper(trim(CALLERTYPE)) IN ('WEB','PHONE','EMAIL','CHAT','TWITTER','LETTER') THEN 1
                          WHEN upper(trim(CALLERTYPE)) = 'NSO' THEN 2 WHEN upper(trim(CALLERTYPE)) = 'INDETERMINATE' THEN 3 ELSE 4 END AS ch_rank,
                     trim(PROBLEMCODE) AS ptype, upper(trim(STATUS)) AS status, lower(trim(PUBLICRESOLUTION)) AS res,
                     try_cast(DATETIMEINIT AS TIMESTAMP) AS t_init, try_cast(DATETIMECLOSED AS TIMESTAMP) AS t_closed,
                     try_cast(PRJCOMPLETEDATE AS TIMESTAMP) AS t_promise,
                     CASE WHEN regexp_full_match(trim(WARD), '[0-9]+') THEN cast(trim(WARD) AS INT) END AS ward FROM raw),
    req AS (SELECT * FROM (SELECT *, row_number() OVER (PARTITION BY REQUESTID ORDER BY ch_rank, ct) AS rn,
                                  min(ch_rank) OVER (PARTITION BY REQUESTID) AS min_rank FROM typed) WHERE rn = 1)
    SELECT CASE WHEN ward BETWEEN 1 AND 5 THEN 'w1_5' ELSE 'w10_14' END AS g, count(*),
           count(*) FILTER (WHERE t_closed <= t_promise), count(*) FILTER (WHERE CAST(t_closed AS DATE) <= CAST(t_promise AS DATE))
    FROM req
    WHERE min_rank = 1 AND ptype = 'Vehicle Towing' AND t_init >= TIMESTAMP '2025-05-16' AND status = 'CLOSED'
      AND t_closed IS NOT NULL AND res = 'vehicle tagged for tow' AND (ward BETWEEN 1 AND 5 OR ward BETWEEN 10 AND 14)
    GROUP BY 1""").fetchall()}
fig('n3_towing_tagged_by_promise_after', dict(wards_1_5=round(_tow['w1_5'][1] / _tow['w1_5'][0], 3), wards_10_14=round(_tow['w10_14'][1] / _tow['w10_14'][0], 3),
                                               n=[_tow['w1_5'][0], _tow['w10_14'][0]]), 'share of requests', PER_A,
    'Share of towing requests closed "vehicle tagged for tow" whose closing time is at or before the city\'s own promise date (PRJCOMPLETEDATE, 5 days)', 'observed', '09_registry.py',
    "311 requests (City of St. Louis open data, csb.zip 2025 and 2026 yearly CSVs, invalid bytes dropped: build/csb-clean), one row per REQUESTID, "
    "resident-filed if any of its rows has a resident CALLERTYPE (web, phone, email, chat, Twitter, letter); towing requests filed on or after "
    "16 May 2025, STATUS CLOSED with PUBLICRESOLUTION 'vehicle tagged for tow' (the inspector's first visit, the same population as the 12.0 vs "
    "36.9-day medians); share whose DATETIMECLOSED is at or before PRJCOMPLETEDATE; wards from the WARD column, 1-5 against 10-14.",
    f"{_tow['w1_5'][1]:,} of {_tow['w1_5'][0]:,} and {_tow['w10_14'][1]:,} of {_tow['w10_14'][0]:,} requests (the north figure rests on about "
    f"{_tow['w10_14'][1]} requests). By calendar date instead of timestamp: {_tow['w1_5'][2] / _tow['w1_5'][0]:.1%} vs {_tow['w10_14'][2] / _tow['w10_14'][0]:.1%}. "
    "Replaces N3's earlier share counting any closing words (38% vs 11%, now retired). N8 conflict 1 reproduced 31.8% vs 3.7%.")
fig('n3_towing_gone_median_after', dict(wards_1_5=float(gone_a['med_south']), wards_10_14=float(gone_a['med_north'])), 'median days', PER_A,
    'Median days to a closure reading "vehicle gone upon inspection"', 'observed', '06_robust.py',
    DER_RES + ' Same closing words both sides; a long wait here means the inspection came after the car left.')
fig('n3_cavein_referral_median_after', dict(wards_1_5=float(cav_ref['med_south']), wards_10_14=float(cav_ref['med_north']), n=[int(cav_ref['n_south']), int(cav_ref['n_north'])]), 'median days', PER_A,
    'Median days to "referred to street maintenance for repair work to be scheduled", cave-ins', 'observed', '06_robust.py',
    DER_RES + ' Same closing words both sides. Per ward the line falls between ward 5 (under 1.2 days in every ward 1-5) and ward 6 (over 15 days in every ward 6-14), which points to a different intake process, not only slower crews.',
    'Inferred: in wards 1-5 the referral is made at intake; in 6-14 after an inspection wait. Repair dates for referred cave-ins are not in the file.')
fig('n3_cavein_done_median_after', dict(wards_1_5=float(cav_done['med_south']), wards_10_14=float(cav_done['med_north']), n=[int(cav_done['n_south']), int(cav_done['n_north'])]), 'median days', PER_A,
    'Median days to a closure recording the work as done ("work completed"), cave-ins', 'observed', '06_robust.py',
    DER_RES + ' Only closures whose words record the repair; referrals excluded because in wards 1-5 they happen within a day whatever the repair date.',
    'South n is 35: too few for the robustness rule (n >= 100).')
fig('n3_single_light_done_median', dict(after=[float(slo_a['med_south']), float(slo_a['med_north'])], before=[float(slo_b['med_south']), float(slo_b['med_north'])]), 'median days [wards 1-5, wards 10-14]', f'{PER_B}; {PER_A}',
    'Single light out, median days to "work completed"', 'observed', '06_robust.py',
    DER_RES + ' Only closures recording the repair. City promise 3 days.',
    'Not robust: the gap sits in two quarters (filed Oct 2025-Mar 2026: 20 vs 49 and 5 vs 31 days); other quarters are level.')
fig('n3_code_enforcement_nov_median', dict(after=[float(pme_a['med_south']), float(pme_a['med_north'])], before=[float(pme_b['med_south']), float(pme_b['med_north'])]), 'median days [wards 1-5, wards 10-14]', f'{PER_B}; {PER_A}',
    'Exterior property-maintenance complaints: median days to "issued notice of violation"', 'observed', '06_robust.py',
    DER_RES + ' Same closing words both sides; promise 14 days.', 'Absolute gap about 5 days, inside the promise; slowness concentrated in wards 9-12 (11-22 days); ward 13 (4.7) is faster than ward 4 (8.8).')
fig('n3_no_gap_done_types_after', {t: [float(r['med_south']), float(r['med_north'])] for t, r in nogap.items()}, 'median days [wards 1-5, wards 10-14]', PER_A,
    'Done-class median days for high-volume types with no material ward gap', 'observed', '06_robust.py',
    DER_RES + ' Only closures whose words record the work as done.')
fig('n3_class_agreement_n2_vs_n3', round(agree / tot, 3) if tot else None, 'share of closures', '2024-2026 closures in N2 file',
    "Share of closures where N3's independent first-pass rules give the same class as N2's reviewed classes", 'observed', '09_registry.py',
    "Two independent classifications of the city's closing words (N2's reviewed list; N3's rules), compared closure-weighted; enforcement notices counted as hand-offs as N2 does.")

decisions = [
 dict(id='n3-dedupe', decision='Count one row per REQUESTID; give a request the resident channel if any of its rows has a resident CALLERTYPE.',
      why=f'The public yearly files repeat REQUESTIDs ({nrows:,} rows, {ndist:,} ids in 2024-2026); repeats differ only in CALLERTYPE. After dedupe our ward request counts match CityStat within 1%; before, they ran about 8% high.',
      alternative_rejected='Counting rows (inflates counts and weights multi-caller requests in medians).', shows_up_in='every N3 figure; flagged to N1'),
 dict(id='n3-citystat-definition', decision="Reproduce CityStat's ward chart as the mean (not median) days to close over STATUS=CLOSED requests, all channels and types, filed 1 Jan 2024-30 Jun 2026, ward as recorded in the file.",
      why='Of seven definitions tried this one fits best (mean absolute error 0.85 days across 14 wards; closed counts within 1.1%); a closed-by-10-July snapshot fits the closed counts best.',
      alternative_rejected='Resident-only (counts 29% low); counting cancellations as closures (closed counts 15% high); geocoding blank wards (not done; 2,561 blank-ward requests vs CityStat 726).', shows_up_in='n3_citystat_*, decomposition chart'),
 dict(id='n3-decomposition', decision='Split the ward gap with an exact two-level Kitagawa decomposition of the mean: type mix, then closing-class shares within type, then speed within the same type and class. Check with median reweighting and with days capped at 90.',
      why="CityStat's metric is a mean, which splits exactly with no residual and can be shown as arithmetic. The median and capped versions give the same answer (speed within type and class is 99-148% of the gap).",
      alternative_rejected='Regression with ward dummies (harder to explain to an analyst; same conclusion expected).', shows_up_in='N3-decomposition-ward1-vs-ward10.png, n3_decomp_*'),
 dict(id='n3-closure-classes', decision="Use N2's reviewed closure classes; N3's own rules only for texts N2 has not classed.",
      why=f'Single source of truth for all chapters. N3 classified the same texts independently first; the two agree on {agree / tot:.1%} of closures.' if tot else 'Single source of truth.',
      alternative_rejected="A separate N3 class list (would let chapters disagree).", shows_up_in='all done-class and hand-off figures'),
 dict(id='n3-enforcement-variant', decision="Show the decomposition both with enforcement notices inside hand-offs (N2's class) and as their own class.",
      why="N2 classes notices of violation as handed_off:enforcement (25,639 closures); a notice is an action, not a referral, so the reader should see it makes no difference: closing words 1.5 vs 1.7 days of 15.7.",
      alternative_rejected='Silently merging (hides a contestable choice) or silently splitting (diverges from N2).', shows_up_in='n3_decomp_ward1_vs_10_enforcement_variant; report section 1'),
 dict(id='n3-like-for-like', decision="Like for like = same request type AND same closing words: the done class, plus each type's three most common closing texts, compared separately.",
      why="Some types almost never close as 'done' (towing after the tornado: 153 of 3,722 requests in wards 1-5, 43 of 2,284 in wards 10-14), so done-only comparisons would drop them; same-words comparisons keep the step constant.",
      alternative_rejected='Done-class only (drops towing and enforcement); all closures (mixes a one-day referral with a weeks-long repair, the error in the original headline).', shows_up_in='robust_comparisons.csv, towing and cave-in figures'),
 dict(id='n3-promise-measure', decision="Grade against the city's own promise date (PRJCOMPLETEDATE): done-class closure on or before it, denominator every request whose promise had passed by 13 Oct 2026; open, cancelled, handed-off and no-action count as not done.",
      why="The promise is the city's own per-request commitment; counting open and cancelled requests avoids the closed-only bias that flatters slow areas.",
      alternative_rejected='Closed-only medians as the sole measure; CityStat goal days (not per request).', shows_up_in='done_by_promise and closed_by_promise columns'),
 dict(id='n3-robust-rule', decision='Call a ward comparison robust only if, in both periods (before and after 16 May 2025): n >= 100 each side, median ratio >= 1.5, bootstrap 95% lower bound > 1.2, and the promise measure also lower in wards 10-14.',
      why='The brief asked for comparisons that survive the done-class and promise tests before and after the tornado; the thresholds are stated in advance in 06_robust.py.',
      alternative_rejected='Significance alone (tiny differences pass with large n); after-tornado only.', shows_up_in='robust_shortlist.json, report'),
 dict(id='n3-reject-invt-stamp', decision="Do not use DATEINVTDONE ('investigation done') as a like-for-like measure.",
      why=f"For Street Department types it is stamped within about a day in every ward 1-5 and after 7-64 days in wards 6-14, while towing tags in wards 1-5 still take 6-15 days, so in wards 1-5 it marks a desk step, not the visit. Forestry's stamp has its own line between wards 7 and 8.",
      alternative_rejected='Using the stamp as time to inspection (would show 25x gaps that are partly process).', shows_up_in='right panel of N3-towing-by-ward.png; report'),
 dict(id='n3-cavein-process-flag', decision='Report the cave-in referral gap (0.8 vs 41.7 days) as a process difference, not as like-for-like speed of work.',
      why='Per ward, referral time jumps from under 1.2 days (every ward 1-5) to over 15 days (every ward 6-14); the same 5|6 line appears in the towing and bad-condition investigation stamps, all Street Department types.',
      alternative_rejected="Calling the south 'fast' (its repair dates are not recorded) or the gap 'mix only' (the same words take 50 times longer).", shows_up_in='n3_cavein_* figures'),
 dict(id='n3-single-light-not-robust', decision='Do not lead with single light out.',
      why='Its done-class gap (15.6 vs 41.0 days after the tornado) comes from two quarters filed Oct 2025-Mar 2026; before the tornado the gap is 4.8 vs 6.4 and other quarters are level.',
      alternative_rejected='Using it as a headline candidate (as COMMON correction 2 suggested).', shows_up_in='N3-single-light-by-quarter.png'),
 dict(id='n3-towing-boundary-no-names', decision="Fetch the maps8 VEHICLE_TOWING_ASSIGNMENTS polygons with outFields=OBJECTID only.",
      why="The layer's only attribute is 'Inspector', a staff name; the rules bar staff fields.",
      alternative_rejected='Downloading all fields and dropping later.', shows_up_in='boundaries.json'),
 dict(id='n3-periods-groups', decision="Before = filed 1 Jan 2024-15 May 2025; after = filed 16 May 2025-13 Oct 2026; ward groups 1-5 vs 10-14, always with per-ward tables beside them.",
      why='Tornado date and ward groups from T-COMMON; the 14-ward map applies from 2024 (2023 data mixes old wards 15-28).',
      alternative_rejected='Including 2023 (old ward numbers).', shows_up_in='all N3 tables'),
]
json.dump(F, open(os.path.join(B, 'figures.json'), 'w'), indent=1, default=str)
json.dump(decisions, open(os.path.join(B, 'decisions.json'), 'w'), indent=1)
print(len(F), 'figures;', len(decisions), 'decisions; class agreement', round(agree / tot, 4) if tot else None, '| class source:', src)
