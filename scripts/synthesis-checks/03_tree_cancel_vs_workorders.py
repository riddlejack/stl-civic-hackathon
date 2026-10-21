"""Do cancelled 'Inspect City Tree' requests reappear as Forestry work orders at the same address? Uses the saved 1,500-row samples."""
from common import *
import random
base = os.path.join(ROOT, 'data/raw/city-services/arcgis/cityworks-service/layers/')
wo = set()
for f in ('WO_Easement_Tree_Removals_New_6955.json', 'WO_Easement_Trims_6942.json'):
    for ft in json.load(open(base+f))['features']:
        pr = ft.get('properties') or ft.get('attributes') or {}; wo.add(norm(pr.get('WoAddress')))
wo.discard('')
rows = csb_rows(('2025', '2026'))
def share(sub): n = len(sub); m = sum(1 for r in sub if norm(r.get('PROBADDRESS')) in wo); return n, m, 100*m/max(n, 1)
tree = [r for r in rows if r.get('PROBLEMCODE') == 'Inspect City Tree']
groups = {'cancelled': [r for r in tree if (r.get('STATUS') or '').upper() == 'CANCEL'],
          'closed': [r for r in tree if (r.get('STATUS') or '').upper() == 'CLOSED']}
random.seed(1)
groups['baseline (potholes/refuse/container)'] = random.sample([r for r in rows if r.get('PROBLEMCODE') in ('Potholes - Residnl', 'Refuse not collected', 'Containr damaged')], 5000)
for g, sub in groups.items(): n, m, s = share(sub); print(f'{g}: n={n}, address in WO sample {m} ({s:.1f}%)')
