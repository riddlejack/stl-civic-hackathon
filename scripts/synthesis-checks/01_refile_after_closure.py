"""Share of closed requests re-filed at the same address and code within 30/90 days of closure, 2025-26."""
from common import *
rows = csb_rows(('2025', '2026')); byk = collections.defaultdict(list)
for r in rows: byk[(norm(r.get('PROBADDRESS')), (r.get('PROBLEMCODE') or '').strip())].append(r)
closed = re30 = re90 = blank = 0; bt = collections.Counter(); btr = collections.Counter()
for k, lst in byk.items():
    if not k[0]: continue
    inits = sorted([(p(r['DATETIMEINIT']), r) for r in lst if p(r.get('DATETIMEINIT'))], key=lambda x: x[0])
    for i, (ti, r) in enumerate(inits):
        if (r.get('STATUS') or '').upper() != 'CLOSED': continue
        tc = p(r.get('DATETIMECLOSED'))
        if not tc: continue
        closed += 1; bt[k[1]] += 1
        if not (r.get('PUBLICRESOLUTION') or '').strip(): blank += 1
        later = [tj for (tj, _) in inits[i+1:] if tj > tc]
        if later and (later[0]-tc).days <= 30: re30 += 1; btr[k[1]] += 1
        if later and (later[0]-tc).days <= 90: re90 += 1
print(f'closed {closed}; re-filed within 30d {re30} ({100*re30/closed:.1f}%); within 90d {re90} ({100*re90/closed:.1f}%); blank resolution {blank} ({100*blank/closed:.1f}%)')
for t, n in bt.most_common(40):
    if n >= 500: print(f'  {t}: {n} closed, {btr[t]} re-filed within 30d = {100*btr[t]/n:.1f}%')
