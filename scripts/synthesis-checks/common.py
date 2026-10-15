"""Shared helpers for the synthesis-session checks (13 Oct 2026). Run any check with
`python3 -I <check>.py` from the repo root after unzipping csb.zip yearly CSVs into a
scratch folder and setting CSB_DIR. No personal data is read: the 311 file has none;
parcel owner names are never loaded."""
import csv, json, re, os, collections, datetime as dt
ROOT = os.environ.get('STL_ROOT', '/Users/jackriddle/Desktop/stl-civic-hackathon')
CSB_DIR = os.environ.get('CSB_DIR', os.path.join(ROOT, 'build', 'csb-unzipped'))
RES_CH = {'WEB', 'PHONE', 'EMAIL', 'CHAT', 'TWITTER', 'LETTER'}
ABBR = {'AVENUE': 'AV', 'AVE': 'AV', 'STREET': 'ST', 'BOULEVARD': 'BLVD', 'DRIVE': 'DR', 'PLACE': 'PL',
        'ROAD': 'RD', 'COURT': 'CT', 'TERRACE': 'TER', 'LANE': 'LN', 'PARKWAY': 'PKWY'}
def p(s):
    s = (s or '').strip()
    for f in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f'):
        try: return dt.datetime.strptime(s[:19], f)
        except ValueError: pass
    return None
def norm(a):
    a = (a or '').upper().split(',')[0]
    a = re.sub(r'\bST LOUIS\b.*$', '', a)
    a = re.sub(r'[^A-Z0-9 ]', ' ', a)
    return ' '.join(ABBR.get(t, t) for t in a.split())
def csb_rows(years):
    rows = []
    for y in years:
        with open(os.path.join(CSB_DIR, f'{y}.csv'), newline='', encoding='utf-8', errors='replace') as fh:
            rows += list(csv.DictReader(fh))
    return rows
def addr_to_pid():
    """MSD parcel attrs: PROP_ADD -> PID (city ParcelId). OWNER_NAME is never read."""
    m = {}
    with open(os.path.join(ROOT, 'data/raw/msd/msd_parcels_stl_city_attrs.jsonl')) as fh:
        for line in fh:
            pr = json.loads(line)['properties']
            a = norm(pr.get('PROP_ADD'))
            if a: m.setdefault(a, pr.get('PID'))
    return m
def ledger_cuts(years=('2025', '2026'), types=('Grass Maint', 'Weed-Grass')):
    cuts = collections.defaultdict(list)
    with open(os.path.join(ROOT, 'data/raw/stlouis-mo.gov/files/forestry-service-records.csv'), newline='', encoding='utf-8', errors='replace') as fh:
        for r in csv.DictReader(fh):
            d = r.get('SERVICEDATE', '')
            if d[:4] in years and r.get('SERVICETYPE') in types:
                cuts[(r.get('PARCEL') or '').strip()].append(dt.datetime.strptime(d[:10], '%Y-%m-%d'))
    for k in cuts: cuts[k].sort()
    return cuts
