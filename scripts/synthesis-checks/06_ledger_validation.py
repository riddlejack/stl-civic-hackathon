"""Ledger vs CityStat first rotation (6 Apr-26 May 2026: 7,099 of 12,171), and posting-date batching."""
from common import *
win = set(); season = set(); weekday = collections.Counter(); perday = collections.Counter()
with open(os.path.join(ROOT, 'data/raw/stlouis-mo.gov/files/forestry-service-records.csv'), newline='', encoding='utf-8', errors='replace') as fh:
    for r in csv.DictReader(fh):
        d = r.get('SERVICEDATE', '')
        if d[:4] != '2026' or r.get('SERVICETYPE') != 'Grass Maint': continue
        day = dt.date.fromisoformat(d[:10]); par = (r.get('PARCEL') or '').strip()
        season.add(par); weekday[day.strftime('%a')] += 1; perday[day] += 1
        if dt.date(2026, 4, 6) <= day <= dt.date(2026, 5, 26): win.add(par)
print('parcels 6 Apr-26 May', len(win), '(CityStat 7,099 of 12,171); season', len(season))
print('rows by weekday', weekday.most_common()); print('busiest days', [(str(d), n) for d, n in perday.most_common(5)])
