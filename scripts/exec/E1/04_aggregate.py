"""E1 step 4: agreement checks and linkage shares by service (no network).

Input:  build/E1/private/linkage_sample.parquet, build/E1/sample_strata.csv, build/stl.duckdb (read-only).
Output: build/E1/linkage_by_service.csv, build/E1/linkage_by_division.csv, build/E1/agreement.json,
        build/E1/figures.json (no ids anywhere outside private/).
"any attached item" = the page's hidden totalItem counter > 0 (inspections and work orders together).
Run: .venv/bin/python -I scripts/exec/E1/04_aggregate.py
"""
import csv, json, math, pathlib, statistics
from collections import defaultdict
import duckdb, pyarrow.parquet as pq

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / 'build' / 'E1'
PAGE = ('https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/'
        'citizens-service-bureau/check-service-request.cfm')
SCRIPT = 'scripts/exec/E1/04_aggregate.py'


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0, c - h), 3), round(min(1, c + h), 3))


rows = pq.read_table(OUT / 'private' / 'linkage_sample.parquet').to_pylist()
strata = {r['stratum']: r for r in csv.DictReader(open(OUT / 'sample_strata.csv'))}
con = duckdb.connect(str(ROOT / 'build' / 'stl.duckdb'), read_only=True)
ids = [r['request_id'] for r in rows]
db = {r[0]: r[1:] for r in con.execute(
    """SELECT request_id, CAST(ts_promised AS DATE), status_group, lower(trim(coalesce(resolution,''))),
              CAST(ts_closed AS DATE), CAST(ts_invt_done AS DATE)
       FROM requests WHERE request_id IN (SELECT unnest(?))""", [ids]).fetchall()}

valid = [r for r in rows if r['total_item'] is not None and not r['not_found']]

# --- agreement between page and file ---
agree = defaultdict(lambda: [0, 0])
for r in valid:
    prom, sg, res, closed, invt = db[r['request_id']]
    if prom and r['page_due_by']:
        agree['due_by_vs_ts_promised'][1] += 1
        agree['due_by_vs_ts_promised'][0] += str(prom) == r['page_due_by']
    agree['closed_status'][1] += 1
    agree['closed_status'][0] += (r['page_status'] == 'Closed') == (sg == 'closed')
    if sg == 'closed' and r['page_resolution']:
        agree['resolution_text'][1] += 1
        agree['resolution_text'][0] += r['page_resolution'].strip().lower() == res
    if sg == 'closed' and r['page_closed_on'] and closed:
        agree['closed_date'][1] += 1
        agree['closed_date'][0] += str(closed) == r['page_closed_on']
agreement = {k: dict(agree=a, n=n, share=round(a / n, 3) if n else None) for k, (a, n) in agree.items()}
json.dump(agreement, open(OUT / 'agreement.json', 'w'), indent=1)


def summarise(group):
    n = len(group)
    k = sum(r['total_item'] > 0 for r in group)
    pos = [r['total_item'] for r in group if r['total_item'] > 0]
    lo, hi = wilson(k, n)
    return dict(n=n, n_with_item=k, share_with_item=round(k / n, 3) if n else None, ci_low=lo, ci_high=hi,
                median_items_if_any=statistics.median(pos) if pos else None,
                share_related_heading=round(sum(r['related_heading'] for r in group) / n, 3) if n else None,
                share_page_generic_words=round(sum((r['page_resolution'] or '').startswith('For detailed information')
                                                   for r in group) / n, 3) if n else None,
                share_closed_but_investigation_open=round(sum(r['page_status'] == 'Closed' and
                                                              (r['page_invt_text'] or '').startswith('Investigation Still Open')
                                                              for r in group) / n, 3) if n else None)


by = defaultdict(list)
for r in valid:
    by[r['stratum']].append(r)
svc = []
for sid, m in strata.items():
    g = by.get(sid, [])
    if not g:
        continue
    divs = [r['page_division'] for r in g if r['page_division']]
    svc.append(dict(stratum=sid, family=m['family'], service=m['stratum_label'],
                    division_on_page=max(set(divs), key=divs.count) if divs else None,
                    population=int(m['population']), **summarise(g)))
with open(OUT / 'linkage_by_service.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(svc[0].keys())); w.writeheader(); w.writerows(svc)

dv = defaultdict(list)
for r in valid:
    dv[(r['page_division'] or '(none)', 'handoff' if r['stratum'].startswith('H') else
        'done' if r['stratum'].startswith('D') else 'open_past_promise')].append(r)
with open(OUT / 'linkage_by_division.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['division_on_page', 'family', 'n', 'n_with_item', 'share_with_item', 'ci_low', 'ci_high'])
    for (d, fam), g in sorted(dv.items()):
        s = summarise(g); w.writerow([d, fam, s['n'], s['n_with_item'], s['share_with_item'], s['ci_low'], s['ci_high']])


def pooled(pred):
    g = [r for r in valid if pred(r['stratum'])]
    s = summarise(g)
    # population-weighted share across strata (each stratum weighted by its 2025-Aug 2026 population)
    num = den = 0
    for x in svc:
        if pred(x['stratum']):
            num += x['population'] * x['share_with_item']; den += x['population']
    s['share_weighted'] = round(num / den, 3) if den else None
    return s


fams = {
    'handoff': lambda s: s.startswith('H') and s != 'H_tree',
    'tree': lambda s: s == 'H_tree',
    'done': lambda s: s.startswith('D'),
    'open': lambda s: s.startswith('O'),
}
P = {k: pooled(f) for k, f in fams.items()}
period = 'requests filed 1 Jan 2025 to 31 Aug 2026; pages read 14 Oct 2026'


def fig(id_, value, unit, definition, derivation, note=''):
    return dict(id=id_, value=value, unit=unit, period=period, definition=definition, label='observed',
                source_sql_or_script=SCRIPT, note=note, derivation=derivation)


figs = []
if P['handoff']['n']:
    figs.append(fig('e1_handoff_share_with_attached',
                    dict(pooled=P['handoff'], by_service=[x for x in svc if x['family'] == 'handoff']), 'share of requests',
                    'Share of sampled hand-off closures (20 largest hand-off type x closing-phrase pairs) whose public status page shows one or more attached inspections or work orders',
                    f"{P['handoff']['n_with_item']} of {P['handoff']['n']} sampled hand-off pages had a totalItem counter above zero; Wilson 95% interval; weighted share uses each pair's population",
                    'any attached item, not necessarily a work order'))
for key, fid, d in [('done', 'e1_done_share_with_attached', 'closures whose words say the work was done (10 largest types)'),
                    ('open', 'e1_open_past_promise_share_with_attached', 'requests still open past their promise date (10 largest types)'),
                    ('tree', 'e1_tree_removal_share_with_attached', "tree inspections closed 'removal work order created'")]:
    if P[key]['n']:
        figs.append(fig(fid, P[key], 'share of requests', f'Share of sampled {d} whose status page shows any attached item',
                        f"{P[key]['n_with_item']} of {P[key]['n']} sampled pages had totalItem > 0; Wilson 95% interval"))
if 'due_by_vs_ts_promised' in agreement:
    a = agreement['due_by_vs_ts_promised']
    figs.append(fig('e1_promise_date_agreement', a['share'], 'share of pages',
                    "Share of sampled pages whose 'Dept Response Due By' date equals the 311 file's PRJCOMPLETEDATE (ts_promised) date",
                    f"{a['agree']} of {a['n']} pages with both dates agree to the day"))
for x in svc:
    figs.append(fig(f"e1_svc_{x['stratum'].lower()}", x['share_with_item'], 'share of requests',
                    f"{x['service']}: share of sampled requests whose status page shows any attached item",
                    f"{x['n_with_item']} of {x['n']} sampled pages had totalItem > 0 (95% {x['ci_low']}-{x['ci_high']})"))
json.dump(figs, open(OUT / 'figures_attach.json', 'w'), indent=1, default=str)
print(json.dumps(dict(pooled=P, agreement=agreement), indent=1, default=str))
