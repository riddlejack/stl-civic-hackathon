"""Exit test: do addresses with a bad first experience file less in the following 3-12 months? (aggregate only)"""
from common import *
rows = csb_rows(('2023', '2024', '2025', '2026')); byaddr = collections.defaultdict(list)
for r in rows:
    if (r.get('CALLERTYPE') or '').upper() not in RES_CH: continue
    ti = p(r.get('DATETIMEINIT'))
    if ti: byaddr[norm(r.get('PROBADDRESS'))].append((ti, r))
for k in byaddr: byaddr[k].sort(key=lambda x: x[0])
def test(label, sel, bad, start, end):
    out = collections.defaultdict(lambda: [0, 0])
    for a, lst in byaddr.items():
        if not a: continue
        for i, (ti, r) in enumerate(lst):
            if not sel(r) or not (start <= ti < end) or any(sel(rr) and start <= tj < ti for (tj, rr) in lst[:i]): continue
            later = any(90 < (tj-ti).days <= 365 for (tj, rr) in lst[i+1:])
            g = 'bad' if bad(ti, r, lst[i+1:]) else 'good'; out[g][0] += 1; out[g][1] += later
    print(label); [print(f'  {g}: n={n}, filed again 3-12 months later {m} ({100*m/max(n,1):.1f}%)') for g, (n, m) in out.items()]
refuse = lambda r: r.get('PROBLEMCODE') == 'Refuse not collected'
test('Refuse not collected, Jan-Jun 2025; bad = re-filed within 14 days', refuse, lambda ti, r, rest: any(refuse(rr) and 0 < (tj-ti).days <= 14 for (tj, rr) in rest), dt.datetime(2025,1,1), dt.datetime(2025,7,1))
tree = lambda r: r.get('PROBLEMCODE') == 'Inspect City Tree'
test('Inspect City Tree, Jan-Jun 2025; bad = cancelled with no text', tree, lambda ti, r, rest: (r.get('STATUS') or '').upper() == 'CANCEL' and not (r.get('PUBLICRESOLUTION') or '').strip(), dt.datetime(2025,1,1), dt.datetime(2025,7,1))
