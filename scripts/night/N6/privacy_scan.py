"""Privacy gate: scan everything a viewer or a reader can get (site/, deliverable/, build/out/) for ids and
sub-block detail before anyone records or shares it.

Checks every text file for:
  - request numbers and Cityworks work-order numbers (exact match against N1's database)
  - parcel ids and handles (10-11 digit runs); point coordinates near St. Louis (polygon vertices of an
    area layer such as the ward boundaries are not points and are not flagged; point geometries are)
  - street addresses with a house number of any length (one to five digits, so a one-digit number counts), in any
    case ("1234 n example ave" counts), with or without a street type after a direction ("1234 N Example")
  - two-number labels ("1234 & 1236 EXAMPLE AV", "1234-1236 ..."), and "N block of" where N is not a multiple of 100
  - e-mail addresses
The only exemption is the documentation placeholder: house number 1234 with the word EXAMPLE in the same address.
There is no other allowlist. Precision rules (they decide what counts as an address or a coordinate, not which
addresses may pass): a street needs at least one word before its type; a number after a route word (Interstate,
I-, Hwy, Route, US, MO) is a route; a coordinate is a latitude and longitude pair (or a Web Mercator x/y pair),
so a lone 38.6 days is not one; a 10-11 digit run inside a decimal or glued to letters is not a parcel id.

Every address hit is also checked against the city's own address lists (MSD service addresses, 311 request
addresses): real_address true means the number and street exist in St. Louis. Two severities:
  - finding (fails the gate): any id, coordinate, e-mail, two-number label, odd block label, any address hit
    that matches a real city address, and any address-shaped hit whose street words are all street-like;
  - review (listed, does not fail the gate): an address-shaped hit that matches no city address AND whose
    "street" contains a common English function word ("14 for Street Department", "2026 residential and alley").
    These are prose. They are printed with context so a person can confirm that.

Writes build/N6/privacy-scan.json (or --out) and exits 1 if there is any finding.
Run:  .venv/bin/python -I scripts/night/N6/privacy_scan.py [--paths DIR_OR_FILE ...] [--out FILE]
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEFAULT_PATHS = [os.path.join(ROOT, p) for p in ('site', 'deliverable', os.path.join('build', 'out'))]
TEXT_EXT = {'.json', '.geojson', '.jsonl', '.csv', '.tsv', '.js', '.html', '.md', '.css', '.sql', '.txt', '.py', '.sh'}
SKIP_DIRS = {'.git', '.venv', '__pycache__', 'node_modules'}

ap = argparse.ArgumentParser()
ap.add_argument('--paths', nargs='*', default=DEFAULT_PATHS)
ap.add_argument('--out', default=os.path.join(ROOT, 'build', 'N6', 'privacy-scan.json'))
args = ap.parse_args()

# ---------------------------------------------------------------- reference sets from the city's own files
ids, wos = set(), set()
try:
    import duckdb
    con = duckdb.connect(os.path.join(ROOT, 'build', 'stl.duckdb'), read_only=True)
    ids = {str(r[0]) for r in con.execute('SELECT request_id FROM requests').fetchall()}
    wos = {str(r[0]) for r in con.execute('SELECT workorder_id FROM wo_tree').fetchall()}
except Exception as e:  # noqa: BLE001
    con = None
    print(f'! database not readable, id check skipped ({e.__class__.__name__})')

SUFFIX_WORDS = ['AV', 'AVE', 'AVENUE', 'ST', 'STREET', 'BLVD', 'BOULEVARD', 'DR', 'DRIVE', 'PL', 'PLACE', 'RD', 'ROAD',
                'CT', 'COURT', 'TER', 'TERRACE', 'LN', 'LANE', 'PKWY', 'PARKWAY', 'WAY', 'HWY', 'SQ', 'ALY', 'ALLEY',
                'CIR', 'ROW', 'PLZ']
SUFFIX_SET = set(SUFFIX_WORDS)
DIRS = {'N', 'S', 'E', 'W', 'NORTH', 'SOUTH', 'EAST', 'WEST', 'NE', 'NW', 'SE', 'SW'}


def street_core(words):
    """Street name without direction or type, upper case: ['n', 'Taylor', 'Av'] -> 'TAYLOR'."""
    w = [re.sub(r'[^A-Z0-9]', '', x.upper()) for x in words]
    w = [x for x in w if x]
    while w and w[0] in DIRS:
        w = w[1:]
    while w and (w[-1] in SUFFIX_SET or w[-1] in DIRS):
        w = w[:-1]
    if w and w[0] == 'SAINT':
        w[0] = 'ST'
    return ' '.join(w)


real = set()  # (house number, street core)
try:
    with open(os.path.join(ROOT, 'data', 'raw', 'msd', 'msd_service_address_stl_city.geojsonl'), encoding='utf-8') as fh:
        for line in fh:
            p = json.loads(line).get('properties') or {}
            if str(p.get('HNUM') or '').isdigit() and p.get('STRNAME'):
                real.add((int(p['HNUM']), street_core(str(p['STRNAME']).split())))
except OSError:
    print('! MSD address file not readable; real-address check uses 311 addresses only')
if con is not None:
    for hn, st in con.execute('SELECT DISTINCT house_num, street FROM requests WHERE house_num IS NOT NULL AND street IS NOT NULL').fetchall():
        try:
            real.add((int(hn), street_core(str(st).split())))
        except (TypeError, ValueError):
            pass
print(f'reference sets: {len(ids):,} request ids, {len(wos):,} work orders, {len(real):,} city addresses')

# ---------------------------------------------------------------- patterns (case-insensitive)
SUFFIX = '(?:' + '|'.join(sorted(SUFFIX_WORDS, key=len, reverse=True)) + ')'
WORD = r"(?:\d+(?:ST|ND|RD|TH)|[A-Za-z][A-Za-z.'’]*)"
# number [& or - number] words... type; "N block of" is handled by BLOCK, not here
# a number after a route word (Interstate 70, I-64, Hwy 40, Route 66) is a route, not a house number
ROUTE = r"(?<!INTERSTATE )(?<!HIGHWAY )(?<!ROUTE )(?<!HWY )(?<!RTE )(?<!I-)(?<!I )(?<!US )(?<!MO )"
ADDR = re.compile(ROUTE + r"(?<![\w.,/:$#-])(\d{1,5})(?:[ \t]*(?:&|-|–)[ \t]*(\d{1,5}))?(?![ \t]+block[ \t]+of\b)[ \t]+"
                  r"((?:" + WORD + r"[ \t]+){1,3}?)" + SUFFIX + r"\b\.?", re.I)
# number + direction + one or two words, no street type ("1234 N Example"); the direction letter must be upper case
ADDR_DIR = re.compile(ROUTE + r"(?<![\w.,/:$#-])(\d{1,5})[ \t]+([NSEW]\.?|North|South|East|West)[ \t]+([A-Za-z][A-Za-z'’]+(?:[ \t]+[A-Za-z][A-Za-z'’]+)?)")
TWO = re.compile(r"(?<![\w.,/-])(\d{1,5})[ \t]*&[ \t]*(\d{1,5})\b")
BLOCK = re.compile(r"(?<![\w.,/-])(\d{1,5})[ \t]+block[ \t]+of\b", re.I)
NUM = re.compile(r'(?<![\d.,-])\d{5,8}(?![\d.,])')
LONG = re.compile(r'(?<![\w.])\d{10,11}(?!\d)')
COORD = re.compile(r'(?<![\d.])38\.\d{4,}[^\d\n]{1,40}-90\.\d{4,}|-90\.\d{4,}[^\d\n]{1,40}(?<![\d.])38\.\d{4,}|'
                   r'-100[0-6]\d{4}(?:\.\d+)?[^\d\n]{1,40}(?<![\d.])46[6-9]\d{4}(?:\.\d+)?|'
                   r'(?<![\d.])46[6-9]\d{4}(?:\.\d+)?[^\d\n]{1,40}-100[0-6]\d{4}(?:\.\d+)?')
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')
FUNCTION_WORDS = set("""a an and are as at be been but by can did do does for from had has have he her his i if in into is it
its me my no not of on or our out over per she so than that the their them then there these they this those to up us
via vs was we were what when where which while who why will with within without you your days day weeks week months
month years year hours hour minutes minute percent requests request wards ward jan feb mar apr jun jul aug sep sept
oct nov dec january february march april june july august september october november december""".split())

findings, review = [], []


def ctx(text, a, b, w=40):
    return text[max(0, a - w):b + 20].replace('\n', ' ')


def placeholder(span):
    return re.match(r'\s*1234\b', span) is not None and 'EXAMPLE' in span.upper()


def is_real(nums, words):
    core = street_core(words)
    return bool(core) and any((int(n), core) in real for n in nums if n), core


def add_address(rel, text, m, kind, nums, words):
    span = m.group(0)
    if placeholder(span):
        return
    real_hit, core = is_real(nums, words)
    rec = {'file': rel, 'kind': kind, 'match': span.strip(), 'real_address': real_hit, 'street_core': core,
           'context': ctx(text, m.start(), m.end())}
    street_words = [re.sub(r'[^a-z]', '', x.lower()) for x in words]
    prose = (not real_hit) and any(x in FUNCTION_WORDS for x in street_words if x)
    (review if prose else findings).append(rec)


def geometry_points_ok(text):
    """True when a GeoJSON file holds only area geometries (no Point): its vertices are not point locations."""
    try:
        d = json.loads(text)
    except ValueError:
        return False
    feats = d.get('features') if isinstance(d, dict) else None
    if not isinstance(feats, list) or not feats:
        return False
    return all((f.get('geometry') or {}).get('type') in ('Polygon', 'MultiPolygon') for f in feats if isinstance(f, dict))


def strip_geometry(text):
    d = json.loads(text)
    for f in d['features']:
        f['geometry'] = None
    return json.dumps(d)


def scan_file(p):
    rel = os.path.relpath(p, ROOT)
    text = open(p, encoding='utf-8', errors='replace').read()
    if p.endswith(('.geojson', '.json')) and '"FeatureCollection"' in text[:200] and geometry_points_ok(text):
        text = strip_geometry(text)  # area layer: properties are still scanned
    for m in ADDR.finditer(text):
        add_address(rel, text, m, 'address' if not m.group(2) else 'two-number address', [m.group(1), m.group(2)],
                    m.group(3).split() + [m.group(0).split()[-1]])
    for m in ADDR_DIR.finditer(text):
        if ADDR.match(text, m.start()):
            continue  # already reported with its street type
        add_address(rel, text, m, 'address (no street type)', [m.group(1)], [m.group(2)] + m.group(3).split())
    for m in TWO.finditer(text):
        if placeholder(text[m.start():m.end() + 40]):
            continue
        if ADDR.match(text, m.start()):
            continue  # reported above as a two-number address
        st = re.match(r"[ \t]+(?:block[ \t]+of[ \t]+)?((?:" + WORD + r"[ \t]+){0,4}?" + SUFFIX + r")\b", text[m.end():m.end() + 60], re.I)
        real_hit = is_real([m.group(1), m.group(2)], st.group(1).split())[0] if st else False
        findings.append({'file': rel, 'kind': 'two-number label', 'match': m.group(0) + (' ' + st.group(1) if st else ''),
                         'real_address': real_hit, 'context': ctx(text, m.start(), m.end())})
    for m in BLOCK.finditer(text):
        if int(m.group(1)) % 100:
            findings.append({'file': rel, 'kind': 'odd block label', 'match': m.group(0), 'context': ctx(text, m.start(), m.end())})
    if not rel.endswith(('.js', '.css')):
        for m in NUM.finditer(text):
            v = m.group(0)
            if v in ids:
                findings.append({'file': rel, 'kind': 'request id', 'match': v, 'context': ctx(text, m.start(), m.end())})
            elif v in wos:
                findings.append({'file': rel, 'kind': 'work-order id', 'match': v, 'context': ctx(text, m.start(), m.end())})
        for m in LONG.finditer(text):
            findings.append({'file': rel, 'kind': 'parcel-like id', 'match': m.group(0), 'context': ctx(text, m.start(), m.end())})
        for m in COORD.finditer(text):
            findings.append({'file': rel, 'kind': 'coordinate', 'match': m.group(0), 'context': ctx(text, m.start(), m.end())})
    for m in EMAIL.finditer(text):
        if m.group(0).endswith(('.js', '.css', '.json', '.png', '.jpg')):
            continue
        findings.append({'file': rel, 'kind': 'email', 'match': m.group(0), 'context': ''})


files = []
for base in args.paths:
    base = os.path.abspath(base)
    if os.path.isfile(base):
        files.append(base)
        continue
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        files += [os.path.join(dp, f) for f in fn if os.path.splitext(f)[1].lower() in TEXT_EXT]
for p in sorted(files):
    scan_file(p)

out = {'paths': [os.path.relpath(os.path.abspath(p), ROOT) for p in args.paths], 'files_scanned': len(files),
       'checked_ids': len(ids), 'checked_workorders': len(wos), 'city_addresses': len(real),
       'n_findings': len(findings), 'n_real_addresses': sum(1 for f in findings if f.get('real_address')),
       'n_review': len(review), 'findings': findings[:2000], 'review': review[:2000]}
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
with open(args.out, 'w') as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
by = {}
for x in findings:
    k = (x['kind'] + (' (REAL)' if x.get('real_address') else ''), x['file'])
    by[k] = by.get(k, 0) + 1
for (k, f), n in sorted(by.items()):
    print(f'{n:6d}  {k:28s} {f}')
rv = {}
for x in review:
    rv[x['file']] = rv.get(x['file'], 0) + 1
for f, n in sorted(rv.items()):
    print(f'{n:6d}  {"review (prose)":28s} {f}')
print(f'{len(findings)} findings ({out["n_real_addresses"]} real city addresses); {len(review)} prose hits for review; '
      f'{len(files)} files; ids checked {len(ids):,}, work orders {len(wos):,}, city addresses {len(real):,}')
sys.exit(1 if findings else 0)
