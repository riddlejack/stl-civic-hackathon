"""E1 step 8: one judge-readable table per service, and the merged figure registry (no network, no ids).

Input:  build/E1/linkage_by_service.csv (04), build/E1/linked_by_service.csv (07),
        build/E1/figures_attach.json (04), build/E1/linked_summary.json (07), build/E1/agreement.json.
Output: build/E1/service_table.csv, build/E1/service_table.md, build/E1/figures.json.
Run: .venv/bin/python -I scripts/exec/E1/08_tables.py
"""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / 'build' / 'E1'
PERIOD = 'requests filed 1 Jan 2025 to 31 Aug 2026; pages and items read 14 Oct 2026'

att = list(csv.DictReader(open(OUT / 'linkage_by_service.csv')))
lnk = {r['stratum']: r for r in csv.DictReader(open(OUT / 'linked_by_service.csv'))} if (OUT / 'linked_by_service.csv').exists() else {}
FAM = {'handoff': 'Hand-off', 'done': 'Done', 'open_past_promise': 'Open past promise'}


def pct(x):
    return '' if x in (None, '') else f'{100 * float(x):.0f}%'


rows = []
for a in att:
    l = lnk.get(a['stratum'], {})
    n = int(a['n'])
    fam = 'Tree removal (control)' if a['stratum'] == 'H_tree' else FAM[a['family']]
    svc, _, words = a['service'].partition(' | ')
    rows.append(dict(
        stratum=a['stratum'], group=fam, service=svc, closing_words=words, division=a['division_on_page'],
        n=n, any_item=int(a['n_with_item']), any_item_pct=pct(a['share_with_item']),
        any_item_ci=f"{pct(a['ci_low'])}–{pct(a['ci_high'])}",
        work_order=int(l.get('n_with_work_order') or 0),
        work_order_pct=pct(int(l.get('n_with_work_order') or 0) / n if n else None),
        post_filing_wo=int(l.get('n_with_post_filing_work_order') or 0),
        done_by_promise=l.get('n_done_by_promise', ''), done_late=l.get('n_done_late', ''),
        median_days_late=l.get('median_days_late', ''), no_finish=l.get('n_no_finish', ''),
        not_yet_due=l.get('n_not_yet_due', ''), inspection_only=l.get('n_inspection_only', ''),
        page_hides_words_pct=pct(a['share_page_generic_words']),
        population=int(a['population'])))
order = {'Tree removal (control)': 0, 'Hand-off': 1, 'Done': 2, 'Open past promise': 3}
rows.sort(key=lambda r: (order[r['group']], -r['any_item'] / max(r['n'], 1), -r['population']))
with open(OUT / 'service_table.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

md = ['| Group | Service, closing words | Sampled | Any item attached | 95% interval | Work order attached | Page shows the closing words? |',
      '|---|---|---|---|---|---|---|']
for r in rows:
    words = f", \"{r['closing_words']}\"" if not r['closing_words'].startswith('(') else ''
    md.append(f"| {r['group']} | {r['service']}{words} | {r['n']} | {r['any_item']} ({r['any_item_pct']}) | "
              f"{r['any_item_ci']} | {r['work_order']} ({r['work_order_pct']}) | "
              f"{'no (generic CSB line)' if r['page_hides_words_pct'] == '100%' else ('yes' if r['page_hides_words_pct'] == '0%' else r['page_hides_words_pct'] + ' generic')} |")
(OUT / 'service_table.md').write_text('\n'.join(md) + '\n')

# ---------------- merged figure registry
figs = json.load(open(OUT / 'figures_attach.json'))
ls = json.load(open(OUT / 'linked_summary.json')) if (OUT / 'linked_summary.json').exists() else None
if ls:
    def lf(id_, value, definition, derivation, note=''):
        return dict(id=id_, value=value, unit='requests', period=PERIOD, definition=definition, label='observed',
                    source_sql_or_script='scripts/exec/E1/07_linked.py', note=note, derivation=derivation)
    a = ls['all']
    figs.append(lf('e1_linked_requests', a,
                   'Sampled requests whose status page lists related items, graded against the promise by their first work-order finish',
                   f"{a['n_linked']} sampled requests had items read; grades from the first finish among work orders created on/after filing "
                   "(Cityworks ActualFinishDate where joined, else the page's 'Completed On or Before' date)",
                   "'no finish' only where the promise passed by 13 Sep 2026"))
    for k, v in ls['by_family'].items():
        figs.append(lf(f'e1_linked_{k}', v, f'Linked requests in the {k} group, graded against the promise',
                       f"{v['n_graded_due']} graded with promise passed: {v['n_done_by_promise']} by promise, {v['n_done_late']} late "
                       f"(median {v['median_days_late']} days), {v['n_no_finish']} no finish; {v['n_inspection_only']} inspection only"))
    figs.append(lf('e1_linked_page_vs_cityworks_finish', ls['page_vs_cityworks_finish'],
                   "Work orders where the page's completion date equals the Cityworks extract's ActualFinishDate",
                   'Count of work orders with both dates, and how many agree to the day'))
for r in rows:
    if r['group'] == 'Hand-off' and r['page_hides_words_pct'] == '100%':
        figs.append(dict(id=f"e1_page_hides_words_{r['stratum'].lower()}", value=r['n'], unit='pages', period=PERIOD,
                         definition=f"{r['service']} closed '{r['closing_words']}': pages showing the generic CSB line instead of the closing words",
                         label='observed', source_sql_or_script='scripts/exec/E1/04_aggregate.py', note='',
                         derivation=f"All {r['n']} sampled pages read 'For detailed information, please contact the Citizens' Service Bureau.'"))
for st, l in lnk.items():
    if int(l.get('n_with_work_order') or 0) == 0:
        continue
    figs.append(dict(id=f'e1_linked_svc_{st.lower()}', unit='requests', period=PERIOD, label='observed',
                     source_sql_or_script='scripts/exec/E1/07_linked.py',
                     value={k: l[k] for k in ('n_sampled', 'n_with_work_order', 'n_done_by_promise', 'n_done_late',
                                              'median_days_late', 'n_no_finish', 'n_not_yet_due', 'n_inspection_only')},
                     definition=f"{l['service']}: sampled requests with a work order attached, graded against the promise by first work-order finish",
                     note="Finish = Cityworks ActualFinishDate where joined, else the page's 'Completed On or Before' date (an upper bound)",
                     derivation=f"{l['n_with_work_order']} of {l['n_sampled']} sampled pages list a work order; {l['n_done_by_promise']} finished by the promise, "
                                f"{l['n_done_late']} after it (median {l['median_days_late']} days), {l['n_no_finish']} no finish with the promise passed by 13 Sep 2026"))
ho = [r for r in rows if r['group'] == 'Hand-off']
n_ho = sum(r['n'] for r in ho); wo_ho = sum(r['work_order'] for r in ho)
none = [r for r in ho if r['any_item'] == 0]
base = dict(unit='share of requests', period=PERIOD, label='observed', source_sql_or_script='scripts/exec/E1/08_tables.py')
figs.append(dict(id='e1_handoff_share_with_work_order', value=dict(n=n_ho, with_work_order=wo_ho, share=round(wo_ho / n_ho, 3)),
                 definition='Share of sampled hand-off closures (20 largest pairs) with at least one work order in the related-items list',
                 note='Planting (34) and cave-ins referred (16) are the only hand-off pairs with work orders', **base,
                 derivation=f'{wo_ho} of {n_ho} sampled hand-off pages list a work order; unweighted across 20 pairs of 40'))
figs.append(dict(id='e1_handoff_pairs_with_nothing_attached', value=dict(pairs=len(none), of_pairs=len(ho), pages=sum(r['n'] for r in none)),
                 definition='Hand-off pairs (type x closing words) in which no sampled page shows any attached item',
                 note='Each such pair: 0 of 40, 95% upper bound 9%', **{**base, 'unit': 'pairs'},
                 derivation=f"{len(none)} of {len(ho)} pairs had 0 attached items on all {sum(r['n'] for r in none)} of their sampled pages"))
json.dump(figs, open(OUT / 'figures.json', 'w'), indent=1, default=str)
print('\n'.join(md))
print(len(figs), 'figures')
