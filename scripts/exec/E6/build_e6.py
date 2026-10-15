"""E6: the data the rebuilt site needs beyond the bridge's files. No new analysis.

    .venv/bin/python -I scripts/exec/E6/build_e6.py --manifest <EXPORT_DIR>/data/MANIFEST.csv

Writes
  build/E6/figures.json       e5_* figures, each copied from build/E5/summary.json (the 14,902 reality check)
  site/data/e6.json           those figures, the source manifest (grouped) and the authorisation wording
  site/data/downloads/sources.csv        the manifest as the page shows it: one row per public source and one per
                                         withheld group; sizes in MB and row counts with commas, no sha256 (hashes and
                                         byte counts hold digit runs equal to real request numbers, which the N6 privacy
                                         scan rejects; the full manifest with hashes is data/MANIFEST.csv in the export)
  site/data/downloads/fetch_public.sh    E4's fetch script (scripts/exec/E4/public-data/fetch_public.sh), with the
                                         retired product name replaced by the placeholder; nothing else changes

The manifest comes from a public export (scripts/exec/E4/export_public.sh into a scratch folder), because E4 builds it
from the files an export contains. The bridge (scripts/night/N6/bridge.py) never writes or deletes e6.json.
"""
import argparse
import csv
import json
import os
import re
import shutil
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
B = lambda *p: os.path.join(ROOT, *p)  # noqa: E731
NAME = '[NAME]'

ap = argparse.ArgumentParser()
ap.add_argument('--manifest', required=True)
args = ap.parse_args()

# ---------------------------------------------------------------- E5 figures (copied, not recomputed)
S = json.load(open(B('build', 'E5', 'summary.json')))
cls = {r['class']: r for r in S['summary']}
SRC = 'build/E5/summary.json (scripts/exec/E5/01_ledger.py); report research/open-queue-reality-check.md'
PERIOD = 'open requests filed 1 Jan 2025 to 13 Oct 2026 and past their promised date on 13 Oct 2026'
TEXT = {
    'a_done_after_filing': ('done', 'observed', 'A record shows the work done after filing (mowing ledger cut, finished Forestry or sidewalk work order, board-up, completed demolition permit, or an E1 status page showing a finish), so "open" is clerical.'),
    'b_pending_in_records': ('pending', 'observed', 'A city work record created after filing is still pending (an open Forestry work order, a board-up or demolition record with no completion, or an E1 status page with an unfinished work order).'),
    'c_possibly_superseded': ('superseded', 'observed', 'Possibly superseded: a later request with the same code at the same address is closed.'),
    'd_admin_leftover': ('admin', 'inferred', 'Likely administrative leftover: sirens, no water, mosquito spraying, more than 90 days past promise.'),
    'e_no_evidence': ('no_record', 'observed', 'No evidence either way: no public record on disk shows the work done or pending. A missing record does not mean the work was not done.'),
}
FIGS = []
for key, (short, label, definition) in TEXT.items():
    r = cls[key]
    common = {'period': PERIOD, 'label': label, 'source_sql_or_script': SRC, 'owner': 'E5 (copied by E6)'}
    FIGS.append({'id': f'e5_queue_{short}_n', 'value': r['n'], 'unit': 'requests', 'definition': definition, **common,
                 'derivation': f"Each of the {S['n_base']:,} requests takes the first class that applies (classes are mutually exclusive). {definition}",
                 'note': f"summary.json: summary[class={key}].n"})
    FIGS.append({'id': f'e5_queue_{short}_share', 'value': round(r['n'] / S['n_base'], 4), 'unit': 'share of open requests past promise',
                 'definition': definition, **common,
                 'derivation': f"{r['n']:,} of {S['n_base']:,} ({r['pct']}%). Each request takes the first class that applies. {definition}",
                 'note': f"summary.json: summary[class={key}].pct = {r['pct']}"})
FIGS.append({'id': 'e5_queue_base', 'value': S['n_base'], 'unit': 'requests', 'period': PERIOD, 'label': 'observed', 'source_sql_or_script': SRC,
             'owner': 'E5 (copied by E6)', 'definition': "The base set of the reality check; equal to e3_queue_past_promise.",
             'derivation': "requests WHERE ts_init >= '2025-01-01' AND status_group = 'open' AND ts_promised < '2026-10-13 23:59:59' in build/stl.duckdb.",
             'note': 'summary.json: n_base'})
os.makedirs(B('build', 'E6'), exist_ok=True)
json.dump({'figures': FIGS}, open(B('build', 'E6', 'figures.json'), 'w'), indent=1)

# ---------------------------------------------------------------- the manifest, grouped for the page
rows = list(csv.DictReader(open(args.manifest, newline='')))


def rows_txt(v):
    v = (v or '').strip()
    if re.fullmatch(r'\d+', v):
        return f'{int(v):,}'  # with commas: a bare digit run can collide with a request number in the privacy scan
    return v


def mb(v):
    try:
        b = int(v)
    except (TypeError, ValueError):
        return ''
    return f'{b / 1e6:,.1f} MB' if b >= 1e5 else f'{b / 1e3:,.0f} KB'


def used(v):
    # "N1 figures (78, ids n1_*); read or cited by research/x.md, ..." -> keep it readable
    parts = [p.strip() for p in (v or '').split(';') if p.strip()]
    return '; '.join(parts[:4]) + ('; …' if len(parts) > 4 else '')


published, withheld = [], OrderedDict()
for r in rows:
    if r['tier'] in ('fetched by script', 'vendored'):
        published.append({'name': r['name'], 'url': r['url'], 'retrieved': r['retrieved_central'], 'rows': rows_txt(r['rows']),
                          'size': mb(r['bytes']), 'used_by': used(r['used_by']), 'tier': r['tier'], 'published_as': r['published_as']})
    else:
        base = re.sub(r'\s*\((?:layer|[a-z_]+\.json|[A-Za-z_]+_\d+\.json)[^)]*\)\s*$', '', r['name']).strip()
        g = withheld.setdefault(base, {'name': base, 'url': r['url'], 'files': 0, 'retrieved': set(), 'note': r['note'], 'used_by': used(r['used_by'])})
        g['files'] += 1
        g['retrieved'].update(x.strip() for x in r['retrieved_central'].split(' to ') if x.strip())
order = {'fetched by script': 0, 'vendored': 1}
published.sort(key=lambda x: (order[x['tier']], x['name']))
wh = []
for g in withheld.values():
    ts = sorted(g['retrieved'])
    g['retrieved'] = ts[0] if len(ts) == 1 else (f'{ts[0]} to {ts[-1]}' if ts else '')
    wh.append(g)

# ---------------------------------------------------------------- the authorisation wording, verbatim
note = open(B('context', 'AUTHORISATION-NOTE.md'), encoding='utf-8').read()


def section(title):
    m = re.search(r'^## ' + re.escape(title) + r'\s*\n(.*?)(?=^## |\Z)', note, re.S | re.M)
    return m.group(1).strip() if m else ''


plain = lambda t: re.sub(r'\*\*(.*?)\*\*', r'\1', t).strip()  # noqa: E731
bullets = [plain(b) for b in re.findall(r'^- (.+)$', section('What was authorised'), re.M)]
says = section('What the submission says (draft wording; Jack edits)')
quote = re.search(r'"(.+)"', says, re.S)
auth = {'statement': quote.group(1).strip() if quote else '', 'authorised': bullets,
        'status': plain(re.search(r'^\*\*(.+?)\*\*', note.split('## What was authorised')[0], re.M | re.S).group(1)) if '**' in note.split('## What was authorised')[0] else '',
        'source': 'context/AUTHORISATION-NOTE.md'}

e6 = {'meta': {'contract': 'e6/1', 'mock': False, 'state': 'real', 'built_at': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M'),
               'sources': [{'path': 'build/E5/summary.json'}, {'path': os.path.relpath(args.manifest, ROOT) if args.manifest.startswith(ROOT) else 'data/MANIFEST.csv (public export)'},
                           {'path': 'context/AUTHORISATION-NOTE.md'}],
               'notes': ['Built by scripts/exec/E6/build_e6.py; the bridge does not touch this file.']},
      'figures': {f['id']: f for f in FIGS},
      'sources': {'published': published, 'withheld': wh,
                  'counts': {'all': len(rows), 'fetched': sum(r['tier'] == 'fetched by script' for r in rows),
                             'vendored': sum(r['tier'] == 'vendored' for r in rows), 'not_published': sum(r['tier'] == 'not published' for r in rows)}},
      'authorisation': auth}
json.dump(e6, open(B('site', 'data', 'e6.json'), 'w'), indent=1, ensure_ascii=False)

dl = B('site', 'data', 'downloads')
with open(os.path.join(dl, 'sources.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['name', 'url', 'retrieved_central', 'rows', 'size', 'tier', 'used_by', 'files', 'note'])
    for r in published:
        w.writerow([r['name'], r['url'], r['retrieved'], r['rows'], r['size'], r['tier'], r['used_by'], 1, f"vendored copy: {r['published_as']}" if r['published_as'] else ''])
    for g in wh:
        w.writerow([g['name'], g['url'], g['retrieved'], '', '', 'not published', g['used_by'], g['files'], g['note']])
fetch = open(B('scripts', 'exec', 'E4', 'public-data', 'fetch_public.sh'), encoding='utf-8').read().replace('DoneStat', NAME)
with open(os.path.join(dl, 'fetch_public.sh'), 'w', encoding='utf-8') as f:
    f.write(fetch)
os.chmod(os.path.join(dl, 'fetch_public.sh'), 0o755)
print(f"e6.json: {len(FIGS)} figures; {len(published)} published sources, {len(wh)} withheld groups ({len(rows)} manifest rows); "
      f"authorisation bullets {len(bullets)}; statement {'found' if auth['statement'] else 'MISSING'}")
