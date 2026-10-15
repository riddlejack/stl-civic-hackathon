"""E6: one row per figure the rebuilt screens show -> build/E6/E6-site-facts.csv (no new numbers; read from the registries).

    .venv/bin/python -I scripts/exec/E6/facts.py

Columns: figure_id, figure, unit, date, label, url, computed_by, screen. The url is the public source the figure rests
on; computed_by is the registry's source_sql_or_script. Figures come from site/data/figures.json and site/data/e6.json.
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
F = json.load(open(os.path.join(ROOT, 'site', 'data', 'figures.json')))['figures']
F.update(json.load(open(os.path.join(ROOT, 'site', 'data', 'e6.json')))['figures'])
F.update(json.load(open(os.path.join(ROOT, 'site', 'data', 'ranked.json')))['figures'])  # E7 ranking
Q = json.load(open(os.path.join(ROOT, 'site', 'data', 'queue.json')))
SB = json.load(open(os.path.join(ROOT, 'site', 'data', 'scoreboard.json')))

CSB = 'https://www.stlouis-mo.gov/data/upload/data-files/csb.zip'
QE18 = 'https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18'
CITYSTAT = 'https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/'
LEDGER = 'https://www.stlouis-mo.gov/data/upload/data-files/forestry-service-records.csv'

MAIN = ['FORESTRY', 'STREET DEPT, 510', 'BUILDING DIV', 'LRA', 'WATER DIV', 'TRAFFIC DIVISION, 511',
        'VECTOR CNTRL', 'Tornado, Recovery', 'BLDG LEAD INSP', 'BLDG TRADES', 'CITY EMRGCY MNG', 'TREAS PRKG SVC']
rows = []


def add(fid, screen):
    f = F.get(fid)
    if not f:
        rows.append([fid, 'MISSING', '', '', '', '', '', screen])
        return
    v = f['value']
    if fid.startswith('e3_queue_qe_') or fid == 'e3_queue_public_same_types':
        url = f'{QE18} ; {CSB}'
    elif fid.endswith('_published'):
        url = CITYSTAT
    elif fid.startswith('n5_lot1_cuts') or fid.startswith('e5_') or fid.startswith('e7_'):
        url = f'{CSB} ; {LEDGER}'
    elif fid == 'e3_citystat_debris_published_vs_done':
        url = f'{CITYSTAT} ; {CSB}'
    else:
        url = CSB
    rows.append([fid, json.dumps(v) if isinstance(v, dict) else v, f.get('unit', ''), f.get('period', ''), f.get('label', ''), url,
                 f.get('source_sql_or_script', ''), screen])


for d in Q['divisions']:
    if d['division'] in MAIN:
        add(d['figures']['past'], 'queue (headline, per division)')
add('e3_queue_past_promise', 'queue (All divisions headline; How this list is built)')
for k in ['no_record', 'done', 'pending', 'superseded', 'admin']:
    add(f'e5_queue_{k}_share', 'queue (headline for All divisions; How this list is built)')
for b in Q['hist']:
    add(b['figure_id'], 'queue (How this list is built)')
for fid in ['e3_queue_qe_past_promise_2025', 'e3_queue_qe_codes', 'e3_queue_public_same_types', 'e3_queue_qe_promise_match',
            'e3_queue_qe_promise_both', 'e3_queue_sensitive_excluded']:
    add(fid, 'queue (How this list is built)')
for m in SB['citystat']['metrics']:
    add(f"e3_citystat_{m['metric']}_q2_published", 'citystat (table; chart for debris)')
    add(m['q2_ours_figure'], 'citystat (table)')
    add(f"e3_citystat_{m['metric']}_q2_done_on_time", 'citystat (table; chart for debris)')
add('e3_citystat_debris_published_vs_done', 'citystat (chart caption: rebuilt 78.3%)')
add('n4_repro_counts_exact_C', 'citystat (About these numbers)')
for fid in ['n5_lot1_minutes_to_close_jul02', 'n5_lot1_minutes_to_close_jul28', 'n5_lot1_promise_date', 'n5_lot1_cuts_billed_2026']:
    add(fid, 'status (the lot, Today and After)')
add('e3_status_tree_related_items', 'status (About this page)')
for fid in ['e7_closeout_n', 'e7_ranked_n', 'e7_ranked_public_n', 'e7_tier1_base_n', 'e7_tier2_base_n', 'e7_tier3_base_n',
            'e7_forestry_top25_t1_oldest', 'e7_forestry_top25_t1_ranked', 'e7_forestry_top25_overlap',
            'e7_street_dept_510_top25_t1_oldest', 'e7_street_dept_510_top25_t1_ranked', 'e7_street_dept_510_top25_overlap']:
    add(fid, 'queue (Ranked and Close-out views; How the ranking works)')

out = os.path.join(ROOT, 'build', 'E6', 'E6-site-facts.csv')
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['figure_id', 'figure', 'unit', 'date', 'label', 'url', 'computed_by', 'screen'])
    w.writerows(rows)
print(len(rows), 'rows;', sum(r[1] == 'MISSING' for r in rows), 'missing ->', os.path.relpath(out, ROOT))
