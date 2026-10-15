"""N3 step 7: does the towing gap follow a crew boundary rather than wards?

Boundary: maps8 STREETS/VEHICLE_TOWING_ASSIGNMENTS layer 0 (keyless). Fetched with outFields=OBJECTID only, so the
layer's 'Inspector' (a staff name) was never downloaded. File:
data/raw/maps8-n3/towing_assignments_geom_oid_only.json (EPSG:3857, 2 polygons, fetched 13 Oct 2026 23:46 CDT).
Request points: SRX/SRY (EPSG:3857) from the 311 file. Point-in-polygon by ray casting (numpy), no shapely.

Also: cave-ins, the ward 1-5 vs 6-14 line, per ward, for the referral text and for 'work completed'.
Run: .venv/bin/python -I scripts/night/N3/07_boundaries.py
"""
import duckdb, json, os, collections
import numpy as np
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
REQ = os.path.join(ROOT, 'build/N3/req.parquet')
geo = json.load(open(os.path.join(ROOT, 'data/raw/maps8-n3/towing_assignments_geom_oid_only.json')))

def pip(x, y, ring):
    ring = np.asarray(ring); inside = np.zeros(len(x), bool)
    x1, y1 = ring[:-1, 0], ring[:-1, 1]; x2, y2 = ring[1:, 0], ring[1:, 1]
    for a, b, c, d in zip(x1, y1, x2, y2):
        cond = ((b > y) != (d > y)) & (x < (c - a) * (y - b) / ((d - b) if d != b else 1e-12) + a)
        inside ^= cond
    return inside

con = duckdb.connect()
rows = con.execute(f"""SELECT request_id, ward, wgroup, period, ptype, class, resolution, status_group, days_close, srx, sry
   FROM '{REQ}' WHERE channel='resident' AND t_init >= '2024-01-01' AND ptype = 'Vehicle Towing'
   AND srx IS NOT NULL AND ward BETWEEN '01' AND '14'""").fetchall()
x = np.array([r[9] for r in rows]); y = np.array([r[10] for r in rows])
terr = np.zeros(len(rows), int)
for f in geo['features']:
    oid = f['attributes']['OBJECTID']; m = np.zeros(len(rows), bool)
    for ring in f['geometry']['rings']: m ^= pip(x, y, ring)
    terr[m & (terr == 0)] = oid
print('towing requests with coordinates:', len(rows), 'in territory 1:', int((terr == 1).sum()), 'territory 2:', int((terr == 2).sum()), 'none:', int((terr == 0).sum()))
# territory by ward
tw = collections.Counter((r[1], int(t)) for r, t in zip(rows, terr))
wards = sorted({r[1] for r in rows})
print('ward: share in territory 1 / 2')
ward_terr = {}
for w in wards:
    a, b = tw[(w, 1)], tw[(w, 2)]; ward_terr[w] = (a, b)
    print(f'  {w}: {a:5d} {b:5d}  ({a / max(a + b, 1):.0%} in 1)')
out = {'ward_territory_counts': ward_terr}
TEXTS = ['vehicle tagged for tow', 'vehicle gone upon inspection']

def med(L): return round(float(np.median(L)), 1) if L else None
res = collections.defaultdict(list)
for r, t in zip(rows, terr):
    if r[7] == 'closed' and r[6] in TEXTS: res[(r[3], r[6], int(t), r[1])].append(r[8])
print('\nmedian days by territory (resident, same closing words)')
summ = {}
for per in ('before', 'after'):
    for tx in TEXTS:
        for t in (1, 2):
            L = [d for (p, txx, tt, w), v in res.items() if p == per and txx == tx and tt == t for d in v]
            summ[f'{per}|{tx}|territory {t}'] = (len(L), med(L)); print(f'  {per:6s} {tx:30s} territory {t}: n {len(L):5d} median {med(L)}')
# split wards: wards with >= 15% of requests in each territory -> compare the two sides within the ward
print('\nwithin split wards (same ward, either side of the territory line), after the tornado')
split = {}
for w in wards:
    a, b = ward_terr[w]
    if min(a, b) / max(a + b, 1) >= 0.15:
        for tx in TEXTS:
            L1 = res.get(('after', tx, 1, w), []); L2 = res.get(('after', tx, 2, w), [])
            L1b = res.get(('before', tx, 1, w), []); L2b = res.get(('before', tx, 2, w), [])
            split[f'{w}|{tx}'] = dict(after_t1=(len(L1), med(L1)), after_t2=(len(L2), med(L2)), before_t1=(len(L1b), med(L1b)), before_t2=(len(L2b), med(L2b)))
            print(f'  ward {w} {tx:30s} after: t1 n {len(L1)} med {med(L1)} | t2 n {len(L2)} med {med(L2)}   before: t1 n {len(L1b)} med {med(L1b)} | t2 n {len(L2b)} med {med(L2b)}')
out['territory_medians'] = summ; out['split_wards'] = split

# cave-ins per ward
print('\ncave-ins per ward, resident channels, after the tornado: referral text and work completed (median days, n), open share')
cv = con.execute(f"""SELECT ward,
   count(*) FILTER (WHERE resolution='referred to street maintenance for repair work to be scheduled') n_ref,
   round(median(days_close) FILTER (WHERE resolution='referred to street maintenance for repair work to be scheduled'),1) med_ref,
   count(*) FILTER (WHERE class='done') n_done, round(median(days_close) FILTER (WHERE class='done'),1) med_done,
   round(avg((status_group='open')::INT),2) open_share, count(*) n,
   round(median(days_close) FILTER (WHERE status_group='closed'),1) med_all
   FROM '{REQ}' WHERE channel='resident' AND ptype='Cave-Ins' AND period='after' AND ward BETWEEN '01' AND '14' GROUP BY 1 ORDER BY 1""").fetchall()
for r in cv: print('  ', r)
out['cave_ins_by_ward_after'] = [dict(ward=r[0], n_ref=r[1], med_ref=r[2], n_done=r[3], med_done=r[4], open_share=r[5], n=r[6], med_all=r[7]) for r in cv]
json.dump(out, open(os.path.join(ROOT, 'build/N3/boundaries.json'), 'w'), indent=1, default=str)
