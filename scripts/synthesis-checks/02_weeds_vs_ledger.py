"""Weed requests on vacant property, 2026: closed 'on schedule' vs cuts recorded on the parcel in the forestry ledger."""
from common import *
a2p = addr_to_pid(); cuts = ledger_cuts(('2026',))
rows = [r for r in csb_rows(('2026',)) if r.get('PROBLEMCODE') in ('Weeds-Vacant Lot', 'Weeds-Vacant Bldg')]
out = collections.defaultdict(collections.Counter)
for r in rows:
    if (r.get('STATUS') or '').upper() != 'CLOSED': continue
    ti = p(r.get('DATETIMEINIT'))
    if not ti or ti > dt.datetime(2026, 9, 15): continue
    pid = a2p.get(norm(r.get('PROBADDRESS')))
    if not pid: continue
    res = (r.get('PUBLICRESOLUTION') or '').lower()
    rk = 'on schedule / added to rotation' if ('schedule' in res or 'rotation' in res) else ('no violation' if 'violation' in res else 'other')
    cl = cuts.get(pid, []); later = [d for d in cl if (d-ti).days >= 0]
    k = (r['PROBLEMCODE'], rk); c = out[k]; c['n'] += 1
    c['cut within 30d'] += any((d-ti).days <= 30 for d in later); c['any cut after'] += bool(later); c['no 2026 cut'] += (not cl)
for k in sorted(out):
    c = out[k]; n = c['n']
    print(f"{k[0]} | {k[1]}: n={n}; within 30d {100*c['cut within 30d']/n:.0f}%; by season end {100*c['any cut after']/n:.0f}%; no 2026 cut {100*c['no 2026 cut']/n:.0f}%")
