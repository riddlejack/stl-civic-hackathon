"""E1 step 1: draw the stratified sample of requests whose public status page we read.

Window: requests filed 1 Jan 2025 to 31 Aug 2026 (every promise date has passed).
Strata (see prompts/exec/E1-status-page-linkage.md):
  H  the 20 largest hand-off (problem_code, closing phrase) pairs in build/R1/handoff_composition.csv
     (classes handed_off and converted), 40 each; plus the tree-removal pair as a named positive
     control if it is not already in the top 20;
  D  the 10 largest problem codes among closures classed 'done', 30 each (control);
  O  the 10 largest problem codes among requests still open past their promise
     (status_group = 'open', ts_promised < 2026-10-13), 30 each.
Each stratum is split as evenly as counts allow across ward groups 1-5, 6-9, 10-14.
Order within a cell is md5(SEED || request_id): fixed, reproducible, independent of DuckDB threads.

Output: build/E1/private/sample.csv (ids; git-ignored) and build/E1/sample_strata.csv (no ids).
Run: .venv/bin/python -I scripts/exec/E1/01_sample.py
"""
import csv, json, pathlib
import duckdb

ROOT = pathlib.Path(__file__).resolve().parents[3]
DB = ROOT / 'build' / 'stl.duckdb'
OUT = ROOT / 'build' / 'E1'
PRIV = OUT / 'private'
SEED = 'E1-status-page-2026-10-14'
W0, W1 = '2025-01-01', '2026-08-31'
GROUPS = ['1-5', '6-9', '10-14']
TREE_PAIR = ('Inspect City Tree', 'removal work order created')

con = duckdb.connect(str(DB), read_only=True)


def top_handoff_pairs(k=20):
    with open(ROOT / 'build' / 'R1' / 'handoff_composition.csv', newline='') as f:
        rows = [r for r in csv.DictReader(f) if r['closure_class'] in ('handed_off', 'converted')]
    rows.sort(key=lambda r: -int(r['n_requests']))
    pairs = [(r['problem_code'], r['closing_phrase'], r['closure_class'], int(r['n_requests'])) for r in rows]
    top = pairs[:k]
    extra = []
    if not any((p[0], p[1]) == TREE_PAIR for p in top):
        extra = [p for p in pairs if (p[0], p[1]) == TREE_PAIR]
    return top, extra, pairs


def allocate(target, avail):
    """Split target across ward groups as evenly as availability allows."""
    alloc = {g: 0 for g in GROUPS}
    left = target
    while left > 0:
        open_g = [g for g in GROUPS if alloc[g] < avail.get(g, 0)]
        if not open_g:
            break
        for g in open_g:
            if left == 0:
                break
            alloc[g] += 1
            left -= 1
    return alloc


def draw(stratum_id, family, label, where, target):
    base = f"""FROM v_requests WHERE init_date BETWEEN DATE '{W0}' AND DATE '{W1}'
               AND ward_group IS NOT NULL AND {where}"""
    avail = dict(con.execute(f"SELECT ward_group, count(*) {base} GROUP BY 1").fetchall())
    alloc = allocate(target, avail)
    out = []
    for g in GROUPS:
        if alloc[g] == 0:
            continue
        rows = con.execute(f"""SELECT request_id, problem_code, coalesce(res_key,'') AS phrase, closure_class,
                                      status_group, ward_group, division, submit_to
                               {base} AND ward_group = ?
                               ORDER BY md5('{SEED}' || CAST(request_id AS VARCHAR)) LIMIT {alloc[g]}""",
                           [g]).fetchall()
        for r in rows:
            out.append(dict(stratum=stratum_id, family=family, stratum_label=label, request_id=r[0],
                            problem_code=r[1], phrase=r[2], closure_class=r[3], status_group=r[4],
                            ward_group=r[5], division=r[6], submit_to=r[7]))
    meta = dict(stratum=stratum_id, family=family, stratum_label=label, target=target,
                population=sum(avail.values()), drawn=len(out),
                **{f'pop_{g}': avail.get(g, 0) for g in GROUPS},
                **{f'drawn_{g}': alloc[g] for g in GROUPS})
    return out, meta


def sq(s):
    return s.replace("'", "''")


sample, strata = [], []
top, extra, _ = top_handoff_pairs()
for i, (pc, ph, cls, n) in enumerate(top + extra, 1):
    sid = f'H{i:02d}' if (pc, ph) != TREE_PAIR or i <= len(top) else 'H_tree'
    where = f"status_group = 'closed' AND problem_code = '{sq(pc)}' AND coalesce(res_key,'') = '{sq(ph)}' AND closure_class = '{cls}'"
    s, m = draw(sid, 'handoff', f'{pc} | {ph}', where, 40)
    sample += s; strata.append(m)

done_codes = [r[0] for r in con.execute(f"""SELECT problem_code, count(*) n FROM v_requests
    WHERE init_date BETWEEN DATE '{W0}' AND DATE '{W1}' AND status_group = 'closed' AND closure_class = 'done'
      AND ward_group IS NOT NULL GROUP BY 1 ORDER BY n DESC, 1 LIMIT 10""").fetchall()]
for i, pc in enumerate(done_codes, 1):
    s, m = draw(f'D{i:02d}', 'done', f'{pc} | (any done phrase)',
                f"status_group = 'closed' AND closure_class = 'done' AND problem_code = '{sq(pc)}'", 30)
    sample += s; strata.append(m)

open_codes = [r[0] for r in con.execute(f"""SELECT problem_code, count(*) n FROM v_requests
    WHERE init_date BETWEEN DATE '{W0}' AND DATE '{W1}' AND status_group = 'open'
      AND ts_promised < TIMESTAMP '2026-10-13' AND ward_group IS NOT NULL
    GROUP BY 1 ORDER BY n DESC, 1 LIMIT 10""").fetchall()]
for i, pc in enumerate(open_codes, 1):
    s, m = draw(f'O{i:02d}', 'open_past_promise', f'{pc} | (open past promise)',
                f"status_group = 'open' AND ts_promised < TIMESTAMP '2026-10-13' AND problem_code = '{sq(pc)}'", 30)
    sample += s; strata.append(m)

ids = [r['request_id'] for r in sample]
assert len(ids) == len(set(ids)), 'duplicate request across strata'

PRIV.mkdir(parents=True, exist_ok=True)
with open(PRIV / 'sample.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(sample[0].keys()))
    w.writeheader(); w.writerows(sample)
with open(OUT / 'sample_strata.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(strata[0].keys()))
    w.writeheader(); w.writerows(strata)
json.dump(dict(seed=SEED, window=[W0, W1], n=len(sample), n_strata=len(strata),
               tree_pair_in_top20=not extra), open(OUT / 'sample_meta.json', 'w'), indent=1)
print('sample', len(sample), 'strata', len(strata), 'tree extra' if extra else 'tree in top 20')
for m in strata:
    print(m['stratum'], m['drawn'], m['population'], m['stratum_label'])
