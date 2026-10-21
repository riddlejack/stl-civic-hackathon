"""Same request type, median days to close by ward group, resident channels, before/after the tornado."""
from common import *
import statistics
rows = csb_rows(('2024', '2025', '2026')); tornado = dt.datetime(2025, 5, 16)
north = {'10', '11', '12', '13', '14'}; south = {'01', '02', '04', '05', '06'}
for t in ['Inspect City Tree', 'Vehicle Towing', 'Cave-Ins', 'Single Light Out', 'City Tree Down', 'Sidewalk Repair', 'Refuse not collected', 'Potholes - Residnl']:
    for per, (a, b) in {'before': (dt.datetime(2024, 1, 1), tornado), 'after': (tornado, dt.datetime(2026, 10, 14))}.items():
        g = {'north': [], 'south': []}
        for r in rows:
            if r.get('PROBLEMCODE') != t or (r.get('CALLERTYPE') or '').upper() not in RES_CH: continue
            ti = p(r.get('DATETIMEINIT')); tc = p(r.get('DATETIMECLOSED'))
            if not ti or not (a <= ti < b) or (r.get('STATUS') or '').upper() != 'CLOSED' or not tc: continue
            w = (r.get('WARD') or '').zfill(2); grp = 'north' if w in north else ('south' if w in south else None)
            if grp: g[grp].append((tc-ti).total_seconds()/86400)
        ms = lambda L: f'{statistics.median(L):6.1f}' if L else '   n/a'
        print(f"{t:20s} {per:6s} north {ms(g['north'])} d (n={len(g['north'])}) | southwest {ms(g['south'])} d (n={len(g['south'])})")
