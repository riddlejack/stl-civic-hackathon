"""E3: CityStat with one added column (surface 3). Registers e3_citystat_* figures from R1's restatement.

    .venv/bin/python -I scripts/exec/E3/build_citystat.py

Reads build/R1/restated_citystat.csv (R1, scripts/night/R1/05_restate.py; read-only here) and writes e3_citystat_*
figures into build/E3/figures.json. No figure already registered elsewhere is changed.
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, 'build', 'E3')
SRC = os.path.join(ROOT, 'build', 'R1', 'restated_citystat.csv')
SCRIPT = 'scripts/exec/E3/build_citystat.py, from build/R1/restated_citystat.csv (scripts/night/R1/05_restate.py)'
CITYSTAT = 'CityStat 311 measures (Mayor\'s Office, Tableau), Q2 2026 as published; pages last updated 30 June 2026 (data/raw/citystat/tableau-extract.md)'
PERIOD = 'requests filed April to June 2026 (Q2 2026), closed requests only, file of 13 Oct 2026'

with open(SRC, newline='') as f:
    rows = [r for r in csv.DictReader(f) if r['period'].startswith('2026 Q2')]
FIGS, out = [], {}


def fl(v):
    return round(float(v), 4) if v not in (None, '') else None


for r in rows:
    m = r['metric']
    base = (f"{r['label']}: one row per REQUESTID, closed requests only, by quarter filed (N4 definition C, which matches CityStat's "
            f"published request counts within 0.2% for 8 of 9 measures); closing words classed by N2's final rules (build/N2/closure_class.sql).")
    FIGS.append({'id': f'e3_citystat_{m}_q2_done_on_time', 'value': fl(r['ontime_share_counting_only_done']), 'unit': 'share of closed requests',
                 'period': PERIOD, 'definition': f"{r['label']}, counting as on time only closings whose words say the work was done (same denominator as CityStat's on-time share).",
                 'label': 'observed', 'source_sql_or_script': SCRIPT, 'owner': 'E3',
                 'note': f"CityStat published {fl(r['citystat_published_share'])} for the same quarter; our rebuilt on-time share is {fl(r['ontime_share_ours'])}.",
                 'derivation': f"{base} Of {r['n_closed']} closed requests, the share closed within the goal AND with words recording finished work: {fl(r['ontime_share_counting_only_done'])}."})
    if m == 'parks_all':
        FIGS[-1]['note'] += (" Parks: R1 grades closed requests only against each request's own PRJCOMPLETEDATE (rebuilt on-time share "
                             f"{fl(r['ontime_share_ours'])}); the scoreboard's 'rebuilt' column shows N4's definition B (closed and open requests), so the two parks columns use different denominators.")
    out[m] = {'done_on_time_figure': f'e3_citystat_{m}_q2_done_on_time', 'n_closed': int(r['n_closed'])}
    if r['citystat_published_share']:
        FIGS.append({'id': f'e3_citystat_{m}_q2_published', 'value': fl(r['citystat_published_share']), 'unit': 'share on time (as published)',
                     'period': 'Q2 2026 (requests filed April to June 2026)', 'definition': f"{r['label']}: CityStat's published on-time share.",
                     'label': 'reported', 'source_sql_or_script': SCRIPT, 'owner': 'E3', 'note': '',
                     'derivation': f"As published by {CITYSTAT}, copied by R1 into build/R1/restated_citystat.csv."})
        out[m]['published_figure'] = f'e3_citystat_{m}_q2_published'

d = next(r for r in rows if r['metric'] == 'debris_alley_street')
pub, done, ours, ho = fl(d['citystat_published_share']), fl(d['ontime_share_counting_only_done']), fl(d['ontime_share_ours']), fl(d['share_of_ontime_closures_handoff'])
FIGS.append({'id': 'e3_citystat_debris_published_vs_done', 'value': {'published': pub, 'done_only': done, 'rebuilt': ours}, 'unit': 'share pair (published on time; done on time)',
             'period': 'Q2 2026 (requests filed April to June 2026)', 'label': 'observed', 'owner': 'E3', 'source_sql_or_script': SCRIPT,
             'definition': ("Alley and street debris cleaned within 3 days. 'published': CityStat's on-time share as published (reported). "
                            "'done_only': the same measure rebuilt from the public 311 file, counting as on time only closings whose words say the work was done (observed)."),
             'note': f"Our rebuilt on-time share for the quarter is {ours} against CityStat's {pub}; of on-time closings, {ho} record a hand-off rather than finished work.",
             'derivation': (f"CityStat published {pub:.1%} on time for Q2 2026 (reported, CityStat page last updated 30 June 2026). Rebuilt from the City's open 311 file "
                            f"(one row per REQUESTID, closed requests only, quarter filed; N4 definition C) the share is {ours:.1%}. Counting only closings whose words "
                            f"say the work was done (N2's classes), it is {done:.1%} of the same {d['n_closed']} closed requests: {ho:.0%} of the on-time closings record a hand-off "
                            "(for example 'referred to', 'scheduled'), not a clean-up.")})
FIGS.append({'id': 'e3_citystat_debris_handoff_share_of_ontime', 'value': ho, 'unit': 'share of on-time closings', 'period': 'Q2 2026 (requests filed April to June 2026)',
             'definition': 'Alley and street debris: of closings within the 3-day goal, the share whose words record a hand-off rather than finished work.',
             'label': 'observed', 'source_sql_or_script': SCRIPT, 'owner': 'E3', 'note': '',
             'derivation': f"N4 definition C on the public 311 file; closing words classed by N2's final rules. {ho:.1%} of on-time closings are hand-offs."})

with open(os.path.join(OUT, 'citystat_done.json'), 'w') as f:
    json.dump({'about': 'CityStat measure -> e3 figure ids for the added done column (Q2 2026).', 'metrics': out}, f, indent=1)
p = os.path.join(OUT, 'figures.json')
old = json.load(open(p)).get('figures', []) if os.path.exists(p) else []
ids = {x['id'] for x in FIGS}
with open(p, 'w') as f:
    json.dump({'figures': [x for x in old if x['id'] not in ids] + FIGS}, f, indent=1, default=str)
print(len(FIGS), 'figures;', {m: v['done_on_time_figure'] for m, v in out.items()})
print('debris pair', pub, done, ours, ho)
