"""E1 option (b): a ~150-request subset of the drawn sample, for a three-minute run if Jack approves.

Takes, from build/E1/private/sample.csv (already in md5(seed || id) order within each ward cell),
the first rows per ward group for 8 strata: tree removal (H_tree), three hand-off types
(towing 'tagged', weeds vacant building 'on schedule', cave-ins 'referred'), two done types
(residential potholes, whole-block lights), two open-past-promise types (tree inspection, cave-ins).
Output: build/E1/private/sample_b.csv (ids; git-ignored), build/E1/sample_b_strata.csv (no ids).
Run: .venv/bin/python -I scripts/exec/E1/01b_sample_b.py
"""
import csv, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / 'build' / 'E1'
GROUPS = ['1-5', '6-9', '10-14']
PICK = {'H_tree': 20, 'H01': 20, 'H04': 20, 'H18': 20, 'D03': 18, 'D05': 18, 'O01': 18, 'O02': 18}

rows = list(csv.DictReader(open(OUT / 'private' / 'sample.csv', newline='')))
cells = defaultdict(list)
for r in rows:
    cells[(r['stratum'], r['ward_group'])].append(r)
out, meta = [], []
for sid, n in PICK.items():
    base, rem = divmod(n, 3)
    alloc = {g: base + (i < rem) for i, g in enumerate(GROUPS)}
    # shortfall in one ward group moves to the others
    short = sum(max(0, alloc[g] - len(cells[(sid, g)])) for g in GROUPS)
    alloc = {g: min(alloc[g], len(cells[(sid, g)])) for g in GROUPS}
    for g in GROUPS:
        extra = min(short, len(cells[(sid, g)]) - alloc[g]); alloc[g] += extra; short -= extra
    took = [r for g in GROUPS for r in cells[(sid, g)][:alloc[g]]]
    out += took
    meta.append(dict(stratum=sid, label=took[0]['stratum_label'] if took else '', n=len(took), **{f'n_{g}': alloc[g] for g in GROUPS}))
with open(OUT / 'private' / 'sample_b.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(out)
with open(OUT / 'sample_b_strata.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(meta[0])); w.writeheader(); w.writerows(meta)
print('option b sample', len(out))
for m in meta:
    print(m)
