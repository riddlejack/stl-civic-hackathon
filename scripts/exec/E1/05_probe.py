"""E1 probe: parse every status page already saved (no network) and join it to the 311 file.

Covers pages outside the drawn sample (ten earlier probe pages, fetched about 2:55 p.m. on 14 Oct 2026,
and E1's two, fetched 3:15 p.m.). This is a probe of how the page behaves, not a measurement.
Output: build/E1/private/probe_pages.csv (ids; git-ignored) and build/E1/probe_pages.csv (no ids).
Run: .venv/bin/python -I scripts/exec/E1/05_probe.py
"""
import csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import duckdb
from importlib import import_module

parse = import_module('03_parse').parse
ROOT = pathlib.Path(__file__).resolve().parents[3]
RAW = ROOT / 'data' / 'raw' / 'stlouis-mo.gov' / 'csb-status'
OUT = ROOT / 'build' / 'E1'

con = duckdb.connect(str(ROOT / 'build' / 'stl.duckdb'), read_only=True)
logp = OUT / 'private' / 'fetchlog.csv'
e1_ids = {int(r['request_id']) for r in csv.DictReader(open(logp))} if logp.exists() else set()
# the probe = ten earlier probe pages (not in the drawn sample) + E1's first two reads (before 3:16 p.m.)
in_sample = {int(r['request_id']) for r in csv.DictReader(open(OUT / 'private' / 'sample.csv'))}
first_two = {int(r['request_id']) for r in csv.DictReader(open(logp)) if r['fetched_at_local'] < '2026-10-14T15:16'}
probe_ids = {int(p.stem) for p in RAW.glob('*.html') if int(p.stem) not in in_sample} | first_two
e1_ids = first_two
rows = []
for p in sorted(RAW.glob('*.html')):
    rid = int(p.stem)
    if rid not in probe_ids:
        continue
    r = parse(p.read_text(encoding='utf-8', errors='replace'))
    d = con.execute("""SELECT problem_code, coalesce(res_key,''), closure_class, status_group,
                              CAST(ts_promised AS DATE), ward_group, CAST(ts_closed AS DATE), init_year, CAST(ts_invt_done AS DATE), lower(trim(coalesce(resolution,'')))
                       FROM v_requests WHERE request_id = ?""", [rid]).fetchone()
    pc, phrase, cls, sg, prom, wg, closed, yr, invt, res = d if d else (None,) * 10
    rows.append(dict(request_id=rid, problem_code=pc, phrase=phrase, closure_class=cls, status_group=sg,
                     ward_group=wg, init_year=yr, page_status=r['page_status'], page_resolution=r['page_resolution'],
                     page_division=r['page_division'], total_item=r['total_item'], related_heading=r['related_heading'],
                     due_by_agrees=(str(prom) == r['page_due_by']) if prom and r['page_due_by'] else None,
                     status_agrees=(r['page_status'] == 'Closed') == (sg == 'closed') if sg else None,
                     closed_date_agrees=(str(closed) == r['page_closed_on']) if closed and r['page_closed_on'] else None,
                     invt_done_page=bool(r['page_invt_done']), invt_done_file=invt is not None,
                     invt_date_agrees=(str(invt) == r['page_invt_done']) if invt and r['page_invt_done'] else None,
                     resolution_agrees=(r['page_resolution'] or '').strip().lower() == res if sg == 'closed' else None,
                     page_comments=r['page_comments'], source='E1' if rid in e1_ids else 'probe'))
rows.sort(key=lambda r: (r['problem_code'] or '', r['phrase'], -(r['total_item'] or 0)))
with open(OUT / 'private' / 'probe_pages.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
pub = [{k: v for k, v in r.items() if k != 'request_id'} for r in rows]
with open(OUT / 'probe_pages.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(pub[0])); w.writeheader(); w.writerows(pub)
for r in pub:
    print(r['problem_code'], '|', r['phrase'][:50], '|', r['closure_class'], r['status_group'], '| page:', r['page_status'],
          r['page_division'], 'items', r['total_item'], 'heading', r['related_heading'],
          'due', r['due_by_agrees'], 'st', r['status_agrees'], 'cl', r['closed_date_agrees'])

# --- probe summary: counts only, with Wilson intervals to show how little 12 pages can carry ---
import json, math


def wilson(k, n, z=1.96):
    if not n:
        return [None, None]
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0, c - h), 3), round(min(1, c + h), 3)]


def grp(r):
    if r['problem_code'] == 'Inspect City Tree' and r['phrase'] == 'removal work order created':
        return 'tree_removal'
    if r['closure_class'] in ('handed_off', 'converted'):
        return 'handoff'
    if r['closure_class'] == 'done':
        return 'done'
    return 'open'


summ = {}
for g in ['tree_removal', 'handoff', 'done', 'open']:
    sel = [r for r in rows if grp(r) == g]
    k = sum((r['total_item'] or 0) > 0 for r in sel)
    summ[g] = dict(n=len(sel), n_with_item=k, items=[r['total_item'] for r in sel], wilson95=wilson(k, len(sel)))


def agree(key):
    v = [r[key] for r in rows if r[key] is not None]
    return dict(agree=sum(v), n=len(v))


summ['agreement'] = {k: agree(k) for k in ['due_by_agrees', 'status_agrees', 'closed_date_agrees',
                                           'invt_date_agrees', 'resolution_agrees']}
summ['pages'] = len(rows)
json.dump(summ, open(OUT / 'probe_summary.json', 'w'), indent=1)
print(json.dumps(summ))
