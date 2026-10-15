"""E7: the ranked overdue list (research/prioritisation-option.md, section 3). No AI, no model, no text mining.

    .venv/bin/python -I scripts/exec/E7/rank.py

Reads build/E5/private/ledger_rows.parquet (the 14,902 open past-promise requests, each with its E5 evidence class)
joined to build/stl.duckdb `requests` (read-only). Writes
  site/data/rank-weights.json   the editable weights and the hazard-tier map (only written if absent, so a
                                division's edits survive a rebuild; --reset-weights rewrites it)
  site/data/ranked.json         block-level rows for the Ranked view, the Close-out groups, and the e7_* figures
  build/E7/figures.json         the e7_* figures with derivations (registry entries)

Score = H + D + R (0-100), as designed:
  H  hazard tier by request type: tier 1 = 60, tier 2 = 30, tier 3 = 0 (the report's mapping, from
     research/prioritisation-scripts/simulate_rank.py, which produced the report's numbers)
  D  1 point per 12 full days past the city's promised date, capped at 30 (reached at 360 days)
  R  5 per extra open past-promise report of the same type at the same address, capped at 10. Computed here from the
     private address; only the count (repeat_n) is written.
Ties: more days past the date first. Step 0 routes E5 classes a, c, d (done after filing, possibly superseded,
administrative leftover) to Close-out; classes b and e are ranked (b is tagged "work order open").

Privacy, as E3's queue: sensitive types and SLMPD routings stay off the rows (counted in totals); routing labels
used fewer than 20 times, or shaped like a personal name, are pooled (scripts/exec/E3/build_queue.py, POOL_MIN);
no request ids, no addresses, nothing below the block. The page recomputes the score in the browser from
rank-weights.json, so editing that file re-weights the list without a rebuild.
"""
import argparse
import collections
import json
import os
import re

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
B = lambda *p: os.path.join(ROOT, *p)  # noqa: E731
RUN_DATE = '2026-10-13'
SCRIPT = 'scripts/exec/E7/rank.py'

ap = argparse.ArgumentParser()
ap.add_argument('--reset-weights', action='store_true')
args = ap.parse_args()

# ---------------------------------------------------------------- weights (the report's design, verbatim tier lists)
T1 = ['City Tree Down', 'City Tree Limb Down', 'Broken/Hanging Limb', 'Cave-Ins', 'NOWATER', 'WTR-COMING-UP', 'HYDRANT-HIT',
      'MISSING-COVER', 'LOOSE-COVER', 'Building Collapse', 'Signal Dark', 'Signals Flashing', 'Signal Stuck', 'Signal Damaged',
      'Other Signal Damaged', 'Other Signal Damage', 'Whole Blk Lights Out', 'Sprinkler Systems', 'No Smoke Detectors',
      'Fire Exit Insp', 'Dangerous Animal', 'Hazrds Waste', 'Potholes - Major St', 'TDebris-alley/street']
T2 = ['Inspect City Tree', 'LRA Tree', 'Inspect Private Tree', 'Sidewalk Repair', 'Bad Condition', 'Sewer Lateral Defect',
      'Illegal Use', 'Ppty Maint Code-Ext', 'Ppty Maint Code-Int', 'Vacnt Bldg Unsecured', 'Single Light Out', 'Light Damaged',
      'Sign needs attention', 'Potholes - Residnl', 'Potholes - Alley', 'PRESSURE', 'CHK-JOBSITE', 'FH-RUNNING', 'FH-MAINTENANCE',
      'WTR-VACANT-BLDG', 'LEAKING-METER', 'TASTE/ODOR', 'APPEARANCE', 'Rats (Exterior)', 'Lead Insp', 'Mechanical Insp',
      'Plumbing Insp', 'Electrical Insp', 'No Hot Water, Int', 'Stagnant Water', 'Sirens Not Heard', 'Injured/Sick Animal',
      'Stray Dog At Large', 'Check Welfare', 'Signals out of sync', 'Demo Blowing Dust', 'Contract Street Work',
      'Property Damage-LRA', 'Roach Infestn, Int', 'Raw Garbage, Ext', 'Comml Dumpster, Ext', 'Vehicle-Rt of Way', 'Mosquito Breeding']
WEIGHTS = {
    '_about': ('Weights for the Ranked view of the queue. Edit and reload the page: the score is recomputed in the browser. '
               'score = tier points (by request type) + 1 point per days_per_point days past the city\'s promised date (up to cap) '
               '+ points_per_extra_report for each extra open report of the same type at the same address (up to cap). '
               'Ties go to the request furthest past its date. Move a request type between tiers with tier_overrides, e.g. '
               '{"Sirens Not Heard": 1}. Design: research/prioritisation-option.md. No model, no text, no demographics.'),
    'tier_points': {'1': 60, '2': 30, '3': 0},
    'lateness': {'days_per_point': 12, 'cap': 30},
    'repeats': {'points_per_extra_report': 5, 'cap': 10},
    'bulk_check_over': 10,
    'tiers': {
        '1': {'label': 'Life-safety, blocked right of way or loss of an essential service', 'short': 'Life-safety', 'codes': T1},
        '2': {'label': 'A hazard or loss of function that is not immediate', 'short': 'Hazard, not immediate', 'codes': T2},
        '3': {'label': 'Everything else: property maintenance, nuisance, amenity, administrative', 'short': 'Maintenance', 'codes': []},
    },
    'tier_overrides': {},
    'review_first': ['Sirens Not Heard (tier 2; arguably 1 as a warning-system fault)',
                     'Lead Insp (tier 2; arguably 1 where children are present, which the file does not show)',
                     'Sign needs attention (tier 2; a missing stop sign is tier 1, but the code does not say)',
                     'Illegal Use (tier 2; blocking and obstruction are not distinguished)'],
}
wpath = B('site', 'data', 'rank-weights.json')
if args.reset_weights or not os.path.exists(wpath):
    json.dump(WEIGHTS, open(wpath, 'w'), indent=1, ensure_ascii=False)
W = json.load(open(wpath))


def tier_of(code):
    o = W.get('tier_overrides', {}).get(code)
    if o:
        return int(o)
    if code in W['tiers']['1']['codes']:
        return 1
    if code in W['tiers']['2']['codes']:
        return 2
    return 3


def score(code, days, n):
    H = W['tier_points'][str(tier_of(code))]
    D = min(days // W['lateness']['days_per_point'], W['lateness']['cap'])
    R = min(W['repeats']['points_per_extra_report'] * (n - 1), W['repeats']['cap'])
    return H + D + R, H, D, R


# ---------------------------------------------------------------- data (read-only)
con = duckdb.connect(B('build', 'stl.duckdb'), read_only=True)
SENS = "(l.problem_code IN (SELECT problem_code FROM sensitive_codes) OR upper(coalesce(r.submit_to, '')) LIKE 'SLMPD%')"
rows = con.execute(f"""
  WITH L AS (SELECT * FROM read_parquet('{B('build', 'E5', 'private', 'ledger_rows.parquet')}')),
       G AS (SELECT addr_norm, problem_code, count(*) AS n FROM L GROUP BY ALL)
  SELECT l.problem_code, coalesce(r.type_name, l.type_name) AS type_name, coalesce(r.submit_to, '(blank)') AS submit_to,
         r.ward, r.block_label, CAST(l.init_date AS VARCHAR) AS filed, CAST(CAST(l.ts_promised AS DATE) AS VARCHAR) AS promised,
         l.days_past_promise, l.status, l.cls, g.n AS repeat_n, {SENS} AS sensitive
  FROM L l JOIN requests r USING (request_id) LEFT JOIN G g ON g.addr_norm = l.addr_norm AND g.problem_code = l.problem_code
""").fetchall()
cols = ['problem_code', 'type_name', 'submit_to', 'ward', 'block', 'filed', 'promised', 'days', 'status', 'cls', 'repeat_n', 'sensitive']
rows = [dict(zip(cols, r)) for r in rows]
assert len(rows) == 14902, len(rows)
assert all(r['repeat_n'] and r['repeat_n'] >= 1 for r in rows)

# routing labels exactly as the E3 queue publishes them
POOL_MIN, POOLED = 20, 'Other (pooled)'
NAME_LIKE = re.compile(r"^[A-Za-z][A-Za-z'.-]*, [A-Za-z][A-Za-z'.-]*$")
NOT_NAMES = {'Tornado, Recovery'}
route_n = collections.Counter(r['submit_to'] for r in rows)


def label(v):
    if route_n[v] < POOL_MIN or (NAME_LIKE.match(v) and v not in NOT_NAMES):
        return POOLED
    return v


def tidy_street(t):  # as scripts/night/N6/bridge.py tidy_street
    return ' '.join(w.upper() if w.upper() in ('N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW') else w.capitalize() for w in t.replace('.', '').split())


def to_block(num, street):
    return f'{(int(num) // 100) * 100} block of {tidy_street(street)}'


def block_label(lbl):  # as scripts/night/N6/bridge.py block_label, so the labels match queue.csv and the map
    if not lbl:
        return None
    m = re.match(r'^\s*(\d+)\s*&\s*(\d+)\s+(?:block of\s+)?(.+)$', lbl, re.I)
    if m:
        return to_block(m.group(1), m.group(3))
    m = re.match(r'^\s*(\d+)\s+block of\s+(.+)$', lbl, re.I)
    if m:
        return to_block(m.group(1), m.group(2))
    m = re.match(r'^\s*(\d{1,5})\s+(.+)$', lbl)
    if m:
        return to_block(m.group(1), m.group(2))
    return tidy_street(lbl)


for r in rows:
    r['block'] = block_label(r['block'])
    r['division'] = label(r['submit_to'])
    r['tier'] = tier_of(r['problem_code'])
    r['score'], r['H'], r['D'], r['R'] = score(r['problem_code'], r['days'], r['repeat_n'])

CLOSE = {'a_done_after_filing', 'c_possibly_superseded', 'd_admin_leftover'}
closeout = [r for r in rows if r['cls'] in CLOSE]
ranked = [r for r in rows if r['cls'] not in CLOSE]
key = lambda r: (-r['score'], -r['days'])  # noqa: E731
ranked.sort(key=key)
public = [r for r in ranked if not r['sensitive']]
# block-mates among the public ranked rows only (counting sensitive rows here would hint at them on a block)
mates = collections.Counter((r['division'], r['block']) for r in public if r['block'])

# ---------------------------------------------------------------- verification against the report's simulation
tiers_base = collections.Counter(r['tier'] for r in rows)


def compare(div, pool):
    sub = [r for r in pool if r['division'] == div]
    top = sorted(sub, key=key)[:25]
    old = sorted(sub, key=lambda r: -r['days'])[:25]
    ids_top, ids_old = {id(r) for r in top}, {id(r) for r in old}
    return {'rows': len(sub), 'overlap': len(ids_top & ids_old), 't1_oldest': sum(r['tier'] == 1 for r in old),
            't1_ranked': sum(r['tier'] == 1 for r in top)}


DIVS = ['FORESTRY', 'STREET DEPT, 510', 'BUILDING DIV', 'WATER DIV', 'TRAFFIC DIVISION, 511']
sim = {d: compare(d, ranked) for d in DIVS}                       # the report's definition: within the ranked set
page = {}
for d in DIVS:                                                    # what the page shows: Oldest first = every public row
    allpub = [r for r in rows if r['division'] == d and not r['sensitive']]
    old = sorted(allpub, key=lambda r: -r['days'])[:25]
    top = [r for r in public if r['division'] == d][:25]
    page[d] = {'t1_oldest': sum(r['tier'] == 1 for r in old), 't1_ranked': sum(r['tier'] == 1 for r in top),
               'overlap': len({id(r) for r in old} & {id(r) for r in top}),
               'closeout_in_oldest25': sum(r['cls'] in CLOSE for r in old)}
print('tiers in base', dict(tiers_base), '| ranked', len(ranked), 'closeout', len(closeout), 'public ranked', len(public))
print('report definition (within ranked set):', json.dumps(sim))
print('page definition (oldest first = all public rows):', json.dumps(page))
top500 = collections.Counter(r['tier'] for r in ranked[:500])
bulk = sum(r['repeat_n'] > W['bulk_check_over'] for r in ranked)
print('top500 tiers', dict(top500), '| t1 in ranked', sum(r['tier'] == 1 for r in ranked), '| bulk-check rows', bulk)

# ---------------------------------------------------------------- figures
PERIOD = 'open requests filed 1 Jan 2025 to 13 Oct 2026, past their promised date on 13 Oct 2026'
BASE_SRC = 'build/E5/private/ledger_rows.parquet (E5 evidence classes) joined to the public 311 file (build/stl.duckdb)'
FIGS = []


def fig(fid, value, unit, definition, derivation, label='observed', note=''):
    FIGS.append({'id': fid, 'value': value, 'unit': unit, 'period': PERIOD, 'definition': definition, 'label': label,
                 'source_sql_or_script': f'{SCRIPT}, from {BASE_SRC}', 'note': note, 'owner': 'E7', 'derivation': derivation})


cc = collections.Counter(r['cls'] for r in closeout)
fig('e7_closeout_n', len(closeout), 'requests', 'Open past-promise requests routed to Close-out instead of the ranked list.',
    f"Of the 14,902, those E5 classes as done after filing ({cc['a_done_after_filing']}), possibly superseded by a later closed request "
    f"of the same type at the same address ({cc['c_possibly_superseded']}) or an administrative leftover ({cc['d_admin_leftover']}). "
    "They need a desk to verify and close the record, not a crew.", note='research/open-queue-reality-check.md classes a, c, d')
fig('e7_ranked_n', len(ranked), 'requests', 'Open past-promise requests ranked (E5 classes b and e).',
    f"14,902 minus the {len(closeout)} routed to Close-out. {len(ranked) - len(public)} of them are sensitive types or SLMPD routings, counted but never listed.")
fig('e7_ranked_public_n', len(public), 'requests', 'Ranked requests shown on the list (sensitive types excluded).',
    f"{len(ranked):,} ranked minus {len(ranked) - len(public)} sensitive or SLMPD-routed requests, as in E3's queue.")
for t in (1, 2, 3):
    fig(f'e7_tier{t}_base_n', tiers_base[t], 'requests', f'Requests among the 14,902 whose type falls in hazard tier {t}.',
        f"Problem codes mapped to tiers by research/prioritisation-option.md (tier 1: life-safety, blocked right of way or loss of an essential "
        f"service; tier 2: hazard not immediate; tier 3: everything else). Matches the report's simulation (2,991 / 7,423 / 4,488).")
for d, slug, name in [('FORESTRY', 'forestry', 'Forestry'), ('STREET DEPT, 510', 'street_dept_510', 'Street Department (510)')]:
    s, p = sim[d], page[d]
    fig(f'e7_{slug}_top25_t1_oldest', s['t1_oldest'], 'of 25 requests',
        f"{name}: life-safety (tier 1) requests among the 25 furthest past their date, within the ranked set.",
        f"{name}'s ranked set ({s['rows']:,} requests: E5 classes b and e, sensitive types included as in the report) sorted by days past the "
        f"promised date; of the first 25, {s['t1_oldest']} are tier 1. On the page's Oldest-first view (every listed request, Close-out "
        f"included) the count is {p['t1_oldest']} of 25.")
    fig(f'e7_{slug}_top25_t1_ranked', s['t1_ranked'], 'of 25 requests',
        f"{name}: life-safety (tier 1) requests among the top 25 of the Ranked view.",
        f"The same set sorted by score (hazard tier + lateness + repeats, ties to the oldest); of the first 25, {s['t1_ranked']} are tier 1. "
        f"Same on the page ({p['t1_ranked']} of 25).")
    fig(f'e7_{slug}_top25_overlap', s['overlap'], 'of 25 requests',
        f"{name}: requests in both the top 25 oldest-first and the top 25 ranked.",
        f"Within the ranked set: {s['overlap']} of 25 in common. On the page (Oldest first lists every request, Close-out included): {p['overlap']} of 25.")
json.dump({'figures': FIGS}, open(B('build', 'E7', 'figures.json'), 'w'), indent=1)

# ---------------------------------------------------------------- close-out groups (aggregates only)
WHY = {'a_done_after_filing': ('Work recorded as done', 'A city record shows the work done after the request was filed (a mowing cut, a finished work order, a board-up or a completed demolition). Verify and close.'),
       'c_possibly_superseded': ('Possibly superseded', 'A later request of the same type at the same address is closed. Check whether it covered this one, then close.'),
       'd_admin_leftover': ('Administrative leftover', 'Time-bound services long past (sirens, no water, mosquito spraying), more than 90 days past the date. Likely paperwork; close.')}
groups = []
for c, (title, why) in WHY.items():
    sub = [r for r in closeout if r['cls'] == c]
    pub = [r for r in sub if not r['sensitive']]
    by_div = collections.Counter(r['division'] for r in sub)
    by_type = collections.Counter((r['division'], r['problem_code']) for r in pub)
    groups.append({'key': c, 'title': title, 'why': why, 'n': len(sub), 'by_division': dict(by_div),
                   'by_type': [[d, t, n] for (d, t), n in by_type.most_common()]})

# ---------------------------------------------------------------- the rows (block level, no ids)
# compact: divisions and request types are listed once and referenced by index
DIV_LIST = sorted({r['division'] for r in public})
CODE_LIST = sorted({(r['problem_code'], r['type_name']) for r in public})
di = {d: i for i, d in enumerate(DIV_LIST)}
ci = {c: i for i, c in enumerate(CODE_LIST)}
OUT_COLS = ['division_i', 'code_i', 'block', 'ward', 'filed', 'promised', 'days', 'status', 'repeat_n', 'block_mates', 'wo_open']
out_rows = [[di[r['division']], ci[(r['problem_code'], r['type_name'])], r['block'], r['ward'], r['filed'], r['promised'], r['days'], r['status'],
             r['repeat_n'], max(0, mates.get((r['division'], r['block']), 0) - 1) if r['block'] else 0, 1 if r['cls'] == 'b_pending_in_records' else 0]
            for r in public]
# a row's score is recomputed in the browser; these are for checking the page against this build
check = {d: [[r['problem_code'], r['days'], r['score']] for r in [x for x in public if x['division'] == d][:5]] for d in DIVS}
json.dump({'meta': {'contract': 'ranked/1', 'mock': False, 'state': 'real', 'built_at': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'sources': [{'path': 'build/E5/private/ledger_rows.parquet'}, {'path': 'build/stl.duckdb'}, {'path': 'site/data/rank-weights.json'}],
                    'notes': [f'Built by {SCRIPT}. Block level; no request ids or addresses; sensitive types off the rows.']},
           'asof': RUN_DATE, 'divisions': DIV_LIST, 'codes': [list(c) for c in CODE_LIST], 'cols': OUT_COLS, 'rows': out_rows, 'closeout': {'n': len(closeout), 'groups': groups},
           'figures': {f['id']: f for f in FIGS}, 'check_top5': check},
          open(B('site', 'data', 'ranked.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
print('wrote site/data/ranked.json', len(out_rows), 'rows;', os.path.getsize(B('site', 'data', 'ranked.json')) // 1024, 'KB;', len(FIGS), 'figures')
