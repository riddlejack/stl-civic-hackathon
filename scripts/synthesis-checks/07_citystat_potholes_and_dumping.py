"""Recompute CityStat Q2 2026 pothole on-time rates from the file; profile illegal-dumping reports."""
from common import *
rows = csb_rows(('2025', '2026'))
for code, g in {'Potholes - Major St': 3, 'Potholes - Residnl': 8, 'Potholes - Alley': 17}.items():
    n = ok = 0
    for r in rows:
        if r.get('PROBLEMCODE') != code: continue
        ti = p(r.get('DATETIMEINIT'))
        if not ti or not (dt.datetime(2026,4,1) <= ti < dt.datetime(2026,7,1)): continue
        n += 1; tc = p(r.get('DATETIMECLOSED'))
        if tc and (tc-ti).days <= g: ok += 1
    print(f'Q2 2026 {code}: initiated {n}, within {g} days {ok} = {100*ok/max(n,1):.1f}%')
dump = [r for r in rows if (r.get('PROBLEMCODE') or '').lower().startswith('illegal dump')]
addr = collections.Counter(norm(r.get('PROBADDRESS')) for r in dump)
print('dumping reports', len(dump), 'by ward', collections.Counter(r.get('WARD') for r in dump).most_common(6))
print('addresses', len(addr), 'with 2+', sum(1 for c in addr.values() if c >= 2), 'with 5+', sum(1 for c in addr.values() if c >= 5), 'max', max(addr.values()))
print('resolutions', collections.Counter((r.get('PUBLICRESOLUTION') or '').strip()[:45] for r in dump if (r.get('STATUS') or '').upper() == 'CLOSED').most_common(6))
