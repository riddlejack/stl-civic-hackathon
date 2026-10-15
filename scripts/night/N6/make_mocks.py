"""Write schema'd mock files for every site data file (site/mock/*.json).

Mocks follow site/DATA-CONTRACT.md exactly, so a section built against a mock
renders unchanged on the real file. Every mock is visibly fake: request ids
start with "MOCK-", streets are "Example St" and friends, and meta.mock is true
(the page shows a red MOCK DATA banner for any section reading one).

Run: .venv/bin/python -I scripts/night/N6/make_mocks.py
"""
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, 'site', 'mock')
os.makedirs(OUT, exist_ok=True)
rng = random.Random(6)

STREETS = ['Example St', 'Sample Av', 'Placeholder Blvd', 'Mock Pl', 'Test Dr', 'Dummy Ct']
WARDS = [f'{w:02d}' for w in range(1, 15)]


def meta(name, notes=None):
    return {'contract': f'{name}/1', 'mock': True, 'built_at': 'mock', 'sources': [],
            'notes': notes or ['Mock data: shaped like the contract, numbers are not real.']}


def block():
    return f'{rng.randrange(1, 60) * 100} block of {rng.choice(STREETS)}'


def dump(name, obj):
    with open(os.path.join(OUT, f'{name}.json'), 'w') as f:
        json.dump(obj, f, indent=1)


dump('run', {'meta': meta('run'), 'asof': '2026-10-13 00:00', 'ledger_max_date': '2026-10-13',
             'built_at': 'mock'})

fig = lambda i, v, u, d: {'id': i, 'value': v, 'unit': u, 'period': 'mock period', 'definition': d,
                          'label': 'observed', 'source_sql_or_script': 'mock',
                          'note': 'Mock value.', 'derivation': 'Mock derivation: replaced when the real figures file lands.'}
dump('figures', {'meta': meta('figures'), 'figures': {f['id']: f for f in [
    fig('n2_share_closed_handoff', 0.30, 'share of closures', 'Share of closures recording a hand-off.'),
    fig('n2_share_closed_done', 0.40, 'share of closures', 'Share of closures recording finished work.'),
    fig('n2_share_closed_no_action', 0.20, 'share of closures', 'Share of closures recording no action.'),
    fig('n2_share_closed_blank', 0.05, 'share of closures', 'Share of closures with no text.'),
    fig('n2_handoff_closed_before_promise', 0.70, 'share of hand-off closures', 'Hand-offs closed before the promise date.'),
    fig('n2_closed_requests', 100000, 'requests', 'Closed requests in scope.'),
]}})

tl = lambda d, k, t: {'date': d, 'kind': k, 'title': t, 'source': 'csb', 'label': 'observed', 'derivation': 'Mock event.'}
mock_cases = {}
for i, (key, typ, words) in enumerate([('lot', 'Weeds-Vacant Lot', 'on schedule to be cut'), ('tree', 'Inspect City Tree', ''),
                                       ('cave', 'Cave-Ins', 'referred to street maintenance')]):
    cid = f'mock-{key}'
    mock_cases[cid] = {'id': cid, 'role': 'hero', 'type': typ, 'ward': WARDS[i * 3], 'neighborhood': 'Example Neighborhood',
                       'block': block(), 'what': 'mock example', 'story': f'Mock receipt for a {typ} request: replaced when build/N5/heroes.json lands.',
                       'facts': {}, 'images': [],
                       'timeline': [tl('2026-07-02 10:17', 'filed', 'Mock: request filed'),
                                    tl('2026-07-02 10:30', 'closed', f'Mock: closed "{words}"'),
                                    tl('2026-07-16', 'promised', "Mock: the city's promise date")]}
dump('receipts', {'meta': meta('receipts'), 'lead_case': 'mock-lot', 'cases': mock_cases,
                  'examples': [{'key': k, 'label': f'Mock {k}', 'cases': [f'mock-{k}']} for k in ('lot', 'tree', 'cave')],
                  'lookup': {'endpoint': 'api/receipt/', 'note': 'mock'}})

rows = []
for name, cat, prom in [('Potholes - Residnl', 'Right of Way', 8), ('Single Light Out', 'Street Light', 3),
                        ('Cave-Ins', 'Right of Way', 3), ('Weeds-Vacant Lot', 'Weeds/Grass', 14),
                        ('Inspect City Tree', 'Trees', 14), ('Vehicle Towing', 'Vehicles', 5),
                        ('Refuse not collected', 'Trash/Debris', 3), ('Illegal dumpg report', 'Trash/Debris', 10)]:
    kept = round(rng.uniform(0.2, 0.9), 3)
    rows.append({'problemcode': name, 'name': name, 'category': cat, 'requests': rng.randrange(2000, 15000),
                 'promise_days': prom, 'scored': 1000, 'kept_share': kept,
                 'done_kept_share': round(kept * rng.uniform(0, 0.8), 3), 'late_share': round(1 - kept, 3),
                 'median_days_late': round(rng.uniform(2, 40), 1), 'open_past_promise': rng.randrange(10, 400),
                 'median_days_to_close': round(rng.uniform(1, 30), 1), 'closed_done_share': 0.3,
                 'closed_handed_off_share': 0.3, 'closed_no_action_share': 0.3,
                 'citystat_metric': None, 'citystat_goal_days': None})
qs = ['2025 Q1', '2025 Q2', '2025 Q3', '2025 Q4', '2026 Q1', '2026 Q2', '2026 Q3']
dump('scoreboard', {'meta': meta('scoreboard'), 'window': 'mock window', 'definition': {'scored': 'mock'}, 'rows': rows,
                    'summary_figures': [],
                    'citystat': {'metrics': [{'metric': 'pothole_residential', 'label': 'Mock measure', 'goal_days': 8,
                                              'citystat_q2_share': 0.9, 'q2_ours_share': 0.85, 'q3_share': 0.5, 'q3_n': 500,
                                              'series': [{'quarter': q, 'ours_share': 0.5 + 0.05 * k, 'ours_n': 500,
                                                          'citystat_share': None if q == '2026 Q3' else 0.5 + 0.05 * k, 'citystat_n': 500}
                                                         for k, q in enumerate(qs)]}],
                                 'n_metrics': 1, 'n_counts_exact': 0, 'counts_exact_metrics': [], 'counts_derivation': 'mock',
                                 'counts_rule': 'mock', 'lead_metric': 'pothole_residential', 'lead_line': 'Mock lead line.',
                                 'lead_median_figures': []}})

comp = lambda k, g, l, d: {'key': k, 'group': g, 'label': l, 'days': d, 'share': round(d / 16, 3)}
dump('fairness', {'meta': meta('fairness'),
                  'headline': 'Mock headline for the fairness section.', 'sub': 'Mock sub-headline.',
                  'citystat': {'a_label': 'Ward 1', 'b_label': 'Ward 10', 'a_days': 17.0, 'b_days': 35.0,
                               'period': 'mock period', 'label': 'reported', 'source': 'mock'},
                  'decomposition_figure': None, 'reproduction_figures': [], 'no_gap_figure': None,
                  'decompositions': [{'key': 'mock', 'a_label': 'Ward 1', 'b_label': 'Ward 10',
                                      'a_mean': 17.0, 'b_mean': 33.0, 'gap': 16.0, 'n_a': 1000, 'n_b': 1000,
                                      'speed_share': 0.75, 'mix_share': 0.25,
                                      'components': [comp('type_mix', 'mix', 'Mix of request types', 2.0),
                                                     comp('closing_practice', 'mix', 'Closing words used', 2.0),
                                                     comp('speed_done', 'speed', 'Same type, same words: finished work', 4.0),
                                                     comp('speed_handoff', 'speed', 'Same type, same words: hand-offs', 4.0),
                                                     comp('speed_other', 'speed', 'Same type, same words: other', 4.0)]}],
                  'lead': [{'type': t, 'title': t, 'words': 'mock words', 'step': 'mock step', 'figure_id': None,
                            'period': 'mock', 'a_label': 'Wards 1–5', 'b_label': 'Wards 10–14', 'a_median': a,
                            'b_median': b, 'n_a': 300, 'n_b': 300, 'ratio': round(b / a, 2), 'ci_lo': None, 'ci_hi': None,
                            'before': None, 'promise_days': p}
                           for t, a, b, p in [('Mock type A', 10, 30, 5), ('Mock type B', 1, 40, 3)]],
                  'no_gap': [{'type': t, 'title': t, 'a_median': a, 'b_median': b, 'n_a': 300, 'n_b': 300,
                              'ratio': round(b / a, 2), 'promise_days': 3}
                             for t, a, b in [('Mock type C', 1.0, 1.0), ('Mock type D', 7.0, 8.0)]]})

cols = [{'key': 'intake', 'label': 'Request recorded', 'help': ''}, {'key': 'promise', 'label': 'Promise date', 'help': ''},
        {'key': 'says_done', 'label': 'Closing words say done', 'help': ''},
        {'key': 'record', 'label': 'Independent record of the work', 'help': ''},
        {'key': 'joined', 'label': 'Joined here', 'help': ''}]
states = ['yes', 'partial', 'no']
dump('register', {'meta': meta('register'), 'columns': cols, 'rows': [
    {'id': f'mock{i}', 'service': f'Mock service {i + 1}',
     'cells': {c['key']: {'state': rng.choice(states), 'text': 'mock'} for c in cols},
     'filed': 1000, 'share_closed_done': 0.3, 'record_source': 'mock', 'what_it_would_take': 'mock'} for i in range(8)]})

mrows = []
types = [('Single Light Out', 'Street Lighting'), ('Cave-Ins', 'Street Maintenance'), ('Inspect City Tree', 'Forestry'),
         ('Potholes - Residnl', 'Street Maintenance'), ('Vehicle Towing', 'Towing')]
for i in range(120):
    t, d = rng.choice(types)
    past = rng.randrange(1, 400)
    mrows.append({'request_id': f'MOCK-{1000 + i}', 'type_name': t, 'division': d, 'ward': rng.choice(WARDS),
                  'block': block(), 'filed': '2026-01-01', 'promised': '2026-01-10', 'days_past_promise': past,
                  'age_days': past + 9, 'status': 'NEW'})
mrows.sort(key=lambda r: -r['days_past_promise'])
bw = {}
bt = {}
for r in mrows:
    bw[r['ward']] = bw.get(r['ward'], 0) + 1
    bt[r['type_name']] = bt.get(r['type_name'], 0) + 1
dump('monday', {'meta': meta('monday'), 'asof': '2026-10-13',
                'definition': 'Open requests whose city promise date has passed (mock).',
                'by_ward': [{'ward': w, 'n': bw.get(w, 0)} for w in WARDS],
                'by_type': sorted([{'type': k, 'n': v} for k, v in bt.items()], key=lambda x: -x['n']),
                'rows': mrows, 'csv': None,
                'mowing': {'season': '2026', 'title': '2026 season, retrospective',
                           'definition': 'Lots on the mowing rotation with a gap of more than 42 days between cuts (mock).',
                           'rows': [{'ward': w, 'parcels_on_rotation': rng.randrange(100, 900),
                                     'parcels_gap_over_42d': rng.randrange(10, 300), 'median_longest_gap': rng.randrange(30, 90)}
                                    for w in WARDS]}})

blocks = []
for i in range(40):
    n = rng.randrange(3, 25)
    done = rng.randrange(0, n // 3 + 1)
    ho = rng.randrange(0, n - done + 1)
    na = rng.randrange(0, n - done - ho + 1)
    blocks.append({'block': block(), 'ward': rng.choice(WARDS), 'n_requests': n, 'n_addresses': rng.randrange(1, 6),
                   'first_report': '2025-10-20', 'last_report': '2026-10-01', 'n_closed_done': done,
                   'n_closed_handoff': ho, 'n_closed_no_action': na, 'n_open': n - done - ho - na,
                   'median_days_to_close': round(rng.uniform(1, 20), 1)})
blocks.sort(key=lambda b: -b['n_requests'])
dump('dumping', {'meta': meta('dumping'), 'window': 'mock: last 365 days',
                 'summary': {'requests': 2000, 'blocks': 900, 'repeat_blocks': 300, 'share_repeat': 0.5},
                 'blocks': blocks})

dump('brief', {'meta': meta('brief'), 'asof': '2026-10-13 00:00',
                'week': {'this_from': '2026-10-06', 'this_to': '2026-10-13', 'last_from': '2026-09-29', 'last_to': '2026-10-06'},
                'meeting_source': {'text': 'mock', 'label': 'reported', 'url': '#', 'date': 'mock'},
                'compliance': {'rows': [{'service': f'Mock service {i}', 'promise_days': 5, 'n_this': 40, 'kept_this': 0.5, 'done_this': 0.2,
                                         'n_last': 40, 'kept_last': 0.7, 'change_pts': -20.0} for i in range(3)], 'definition': 'mock', 'figure_id': None},
                'pothole_weekly': {'series': [{'week': f'2026-0{m}-01', 'n': 50, 'within_goal': 0.9 - 0.1 * k, 'median_days': 4}
                                              for k, m in enumerate(range(4, 10))], 'first_week_below_half': '2026-08-01', 'goal_days': 8,
                                   'figure_id': None, 'definition': 'mock'},
                'first_step': {'wards': [{'ward': w, 'towing_tag': {'n': 50, 'median_days': 10 + k},
                                          'cavein_referral': {'n': 20, 'median_days': 1 + k}} for k, w in enumerate(WARDS)],
                               'definition': 'mock', 'figure_id': None, 'n3_figures': []},
                'lists': [{'key': k, 'title': f'Mock list {k}', 'scope': 'mock', 'owner': 'mock',
                           'rows': [{'block': block(), 'ward': rng.choice(WARDS), 'requests': 2, 'lots': 1} for _ in range(5)],
                           'columns': ['block', 'ward', 'lots', 'requests'], 'summary': 'mock', 'figure_id': None, 'csv': '#'}
                          for k in ('a', 'b', 'c')],
                'monday_total': 1000, 'monday_csv': '#'})
dump('downloads', {'meta': meta('downloads'), 'files': []})
dump('decisions', {'meta': meta('decisions'),
                   'ten': [{'title': f'Mock choice {i + 1}', 'text': 'Replaced when deliverable/choices.md lands.'} for i in range(10)],
                   'decisions': []})
dump('negative', {'meta': meta('negative'),
                  'items': [{'title': f'Mock negative result {i + 1}', 'text': 'Replaced when deliverable/negative-results.md lands.'}
                            for i in range(5)]})
print('wrote mocks to', OUT)
