#!/usr/bin/env python3
"""Privacy scan over a public export of this repository (E4).

usage: scan_public.py EXPORT_DIR [--repo REPO] [--no-ocr] [--failing-files OUT] [--names-file F]

Exits 1 if any file in EXPORT_DIR holds one of:
  request-id     a 7-digit number equal to a real 311 or Cityworks request id, or a
                 6-7 digit number written next to "request id/number", "REQUESTID", "SR #"
  parcel-id      an 11-digit number (parcel id and handle format), or a 9-11 digit
                 number equal to a real parcel id or handle
  workorder-id   a 6-digit number equal to a real Cityworks work-order id on a line that
                 mentions work orders
  id-field       a JSON key or CSV column that carries request, work-order or parcel ids,
                 exact addresses, coordinates or owner names
  address        a house-number street address ("1234 Example St"; "1700 block of" is
                 fine), a two-number label ("1234 & 1236 ..."), "N block of" with N not a
                 multiple of 100, or any number + street that equals a real 311 or parcel
                 address
  latlon         a latitude/longitude pair in the St. Louis area with 4+ decimals
  srx-sry        SRX/SRY or work-order X/Y values (Web Mercator metres around St. Louis)
  staff-name     a person-name routing value from the 311 file's SUBMITTO, or a staff
                 name from Cityworks person fields in data/raw, in any word order
  email          any e-mail address
  forbidden      the Cityworks query host on the city's "work" subdomain, or the city
                 site's robots-disallowed "custom-cf" path prefix (spelled here without
                 the hyphen in the real check)
  disclosure     wording that describes the unsent security disclosure (map layers that
                 anyone can edit, the tax-id field names)
  unscannable    a binary file that is neither text nor an image

Images (.png, .jpg) are OCR'd with tesseract when it is installed, and the OCR text gets
the same checks; "(OCR)" marks those hits. Unfinished placeholders ("{{fig:", "[JACK",
"PLACEHOLDER") are printed as warnings and do not fail the scan.

The real id, address and name sets are read at run time from REPO/build/stl.duckdb and
REPO/data/raw/, which never leave the machine. This file embeds none of them. Without the
database the request-id check falls back to every 7-digit number from 1,000,000 to
2,999,999 and the address check to the format rule alone.
"""
import argparse, csv, io, json, os, re, shutil, subprocess, sys
from collections import Counter, defaultdict

TEXT_EXT = {'.md', '.txt', '.csv', '.json', '.geojson', '.py', '.sh', '.sql', '.js', '.mjs', '.css',
            '.html', '.htm', '.yml', '.yaml', '.toml', '.cfg', '.ini', '.log', '.tsv', '.svg', ''}
IMAGE_EXT = {'.png', '.jpg', '.jpeg'}

# Numbers that equal a real request id but are counts in our prose (checked by hand, E4).
KNOWN_COUNTS = {
    1454222: 'distinct 311 request ids, 2008 to Oct 2026 (n1_duplicate_rows.request_ids)',
    1502836: 'rows in the 311 CSVs, 2008 to Oct 2026',
}

SEVEN = re.compile(r'(?<![A-Za-z0-9.])(?<!\d,)(\d{7})(?![A-Za-z0-9]|\.\d|,\d{3})')
# a 7-digit number inside a URL is skipped unless the URL is about 311 or city services
CITY_URL = re.compile(r'(?i)request|311|csb|stlouis-mo|cityworks|service')
# an amount or a count, not an id: "1536656,USD", "2000000 USD", "of 1519813 rows", "$1932300"
UNIT_AFTER = re.compile(r'\s*,\s*(?:USD|dollars)\b|\s+(?:USD|dollars|rows|records|features|people|residents|parcels|households|voters|calls)\b', re.I)
UNIT_BEFORE = re.compile(r'(?:\$|USD\s?)\s*$')
HIGHWAY_BEFORE = re.compile(r'(?i)(?:interstate|highway|hwy|route|rte|exit|\bI|\bUS)[\s-]*$')
MAP_PLACE_BEFORE = re.compile(r'google\.[a-z.]+/maps/place/[^\s/]+/@$')
SIX = re.compile(r'(?<![\w.])(?<!\d,)(\d{6})(?!\w|\.\d|,\d{3})')
LONGNUM = re.compile(r'(?<![\w.])(\d{9,11})(?!\w|\.\d)')
REQ_CONTEXT = re.compile(r'(?i)(?:request\s*(?:id|number|no\.?|#)|requestid|\bSR\s*#|\bSR\s+(?=\d))\s*[:#=]?\s*["\']?(\d{6,7})\b')
WO_CONTEXT = re.compile(r'(?i)work\s*-?\s*orders?|workorder|\bWO\b|wo_id|woid')

SUFFIX = (r'(?:AVE?|AV|ST|STREET|AVENUE|BLVD|BOULEVARD|DR|DRIVE|RD|ROAD|PL|PLACE|CT|COURT|LN|LANE|'
          r'TER|TERR|TERRACE|PKWY|PARKWAY|WAY|HWY|SQ|CIR|PLZ|PLAZA|ALY|ALLEY|ROW)')
# Format rule: house number, optional direction, 1-3 capitalised words, a street suffix.
ADDR_FORMAT = re.compile(
    r'(?<![\w.,$#/:-])(\d{1,5})[A-Z]?(?:\s*(?:&|-)\s*\d{1,5}[A-Z]?)?\s+(?!block\b|Block\b|BLOCK\b)'
    r'((?:[NSEW]\.?\s+)?(?:(?:[A-Z][A-Za-z\'.]*|\d+(?:ST|ND|RD|TH|st|nd|rd|th))\s+){1,3}?'
    r'(?:Ave?|Av|St|Street|Avenue|Blvd|Boulevard|Dr|Drive|Rd|Road|Pl|Place|Ct|Court|Ln|Lane|Ter|Terr|'
    r'Terrace|Pkwy|Parkway|Way|Hwy|Sq|Cir|Plz|Plaza|Aly|Alley|Row|'
    r'AVE?|AV|ST|STREET|AVENUE|BLVD|BOULEVARD|DR|DRIVE|RD|ROAD|PL|PLACE|CT|COURT|LN|LANE|TER|TERR|'
    r'TERRACE|PKWY|PARKWAY|WAY|HWY|SQ|CIR|PLZ|PLAZA|ALY|ALLEY|ROW))(?![\w])')
# Candidate rule for the set check: any number + up to five words, any case.
ADDR_CAND = re.compile(r'(?<![\w.,$#/:-])(\d{1,5})\s+(?!block\b)((?:[NSEW]\s+)?(?:[A-Za-z0-9\'.]+\s+){0,4}?' + SUFFIX + r')(?![\w])', re.I)
TWO_NUM = re.compile(r'(?<![\w.])(\d{2,5})[A-Z]?\s*&\s*(\d{2,5})[A-Z]?\s+(?:block of\s+)?((?:[NSEW]\.?\s+)?(?:[A-Za-z0-9\'.]+\s+){0,3}?' + SUFFIX + r')(?![\w])', re.I)
ODD_BLOCK = re.compile(r'(?<![\w.,])(\d{1,5})\s+block\s+of\b', re.I)
PLACEHOLDER_STREET = re.compile(r'EXAMPLE', re.I)
PLACEHOLDER_NUMS = {'123', '1234', '12345', '4321'}   # skipped only when the address is not a real one

LATLON = re.compile(r'(?<![\d.])(?:3[89]\.\d{4,}\s*[,;/ ]\s*-\s?9[01]\.\d{4,}|-\s?9[01]\.\d{4,}\s*[,;/ ]\s*3[89]\.\d{4,})(?![\d])')
MERC = re.compile(r'(?<![\d.])-100[0-9]{5}(?:\.\d+)?(?![\d])|(?<![\d.])-100,[0-9]{3},[0-9]{3}(?![\d])')
MERC_PAIR_Y = re.compile(r'(?<![\d.])46[0-9]{5}\.\d+(?![\d])')
SRXY_KV = re.compile(r'(?i)["\']?\b(srx|sry|wox\w*|woy\w*|xcoord\w*|ycoord\w*)\b["\']?\s*[:=,]\s*["\']?-?\d{5,}')

EMAIL = re.compile(r'(?<![\w.%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.([A-Za-z]{2,})(?![\w-])')
NOT_TLD = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'css', 'js', 'mjs', 'json', 'py'}
FORBIDDEN = re.compile(r'(?i)wor[k]\.stlouis-mo\.gov|custo[m]cf')
DISCLOSURE = re.compile(r'(?i)anonymous(?:ly)?[\s-]+(?:editable|edit(?:ing|s)?\b)|editable\s+(?:map\s+|feature\s+)?layers?|\bFe[d]TaxId\b|\bStat[e]TaxId\b'
                        r'|vote[r]\s+(?:list|table|file|roll)s?\b|dates?\s+of\s+birt[h]|chron[o]_table|registratio[n]_chart'
                        r'|wate[r][- ]?accounts?\s+(?:table|layer)s?|editabl[e],\s*voter|vote[r]\|water|(?<![\d,-])12[7]\s+(?:\w+\s+){0,2}layers\b')
WARN = re.compile(r'\{\{fig:|\[JACK|PLACEHOLDER')
COUNT_COLS = {'bytes', 'rows', 'row_count', 'file_count', 'size_bytes'}

ID_KEYS = {'request_id', 'requestid', 'request_ids', 'requestids', 'next_same_request_id', 'next_id',
           'workorder_id', 'workorderid', 'workorder_ids', 'wo_id', 'parcel_id', 'parcelid', 'pid', 'handle',
           'lra_parcel_id', 'parent_pid', 'srx', 'sry', 'woxcoordinate', 'woycoordinate', 'lat', 'lon', 'lng',
           'latitude', 'longitude', 'exact_address', 'probaddress', 'woaddress', 'prop_add', 'lra_address',
           'owner', 'owner_name', 'ownername'}

STAFF_FIELDS = {'initiatedby', 'initiatedbyname', 'closedby', 'closedbyname', 'submitto', 'submittoname',
                'dispatchto', 'dispatchtoname', 'supervisor', 'supervisorname', 'workcompletedby',
                'woclosedby', 'requestedby', 'cancelledby', 'submittoopenby', 'inspectedby', 'assignedto'}
DEPT_WORDS = re.compile(r'(?i)DEPT|DIV|OFFICE|OFC|SVC|SERV|CNTRL|CONTROL|INSP|BUREAU|FORESTRY|REFUSE|WATER|STREET|'
                        r'PARKS|COURT|HEALTH|LRA|TRAFFIC|FIRE|POLICE|SLMPD|CITY|BOARD|ANIMAL|CSB|TREAS|RECOV|'
                        r'EXCISE|ZONING|LEAD|VECTOR|BLDG|BUILDING|UNIT|CENTER|SECTION|PROGRAM|HUMAN|ADMIN|'
                        r'MGMT|CREW|SHOP|TEAM|GROUP|QUEUE|CONTRACT')


def load_sets(repo, names_file):
    s = {'req': set(), 'parcel': set(), 'wo': set(), 'addr': set(), 'names': [], 'source': []}
    db = os.path.join(repo, 'build', 'stl.duckdb')
    if os.path.exists(db):
        try:
            import duckdb
            con = duckdb.connect(db, read_only=True)
            q = lambda sql: [r[0] for r in con.execute(sql).fetchall() if r[0] is not None]
            s['req'] = set(q("SELECT request_id FROM requests"))
            s['req'] |= set(q("SELECT DISTINCT request_id FROM cw_potholes"))
            for sql in ("SELECT DISTINCT pid FROM parcels", "SELECT DISTINCT handle FROM parcels",
                        "SELECT DISTINCT parcel FROM ledger", "SELECT DISTINCT handle FROM ledger",
                        "SELECT DISTINCT parcel_id FROM lra", "SELECT DISTINCT parcel_id FROM maint_props",
                        "SELECT DISTINCT handle FROM maint_props"):
                for v in q(sql):
                    v = str(v).strip()
                    if v.isdigit():
                        s['parcel'].add(v.lstrip('0'))
            s['wo'] = {int(v) for v in q("SELECT DISTINCT workorder_id FROM wo_tree") if str(v).isdigit()}
            s['wo'] |= {int(v) for v in q("SELECT DISTINCT workorder_id FROM request_wo") if str(v).isdigit()}
            for v in q("SELECT DISTINCT addr_norm FROM requests WHERE house_num IS NOT NULL"):
                s['addr'].add(norm_addr(v))
            for v in q("SELECT DISTINCT PROP_ADD FROM parcels"):
                s['addr'].add(norm_addr(re.sub(r'\s+ST LOUIS MO\s*\d*\s*$', '', v)))
            s['addr'].discard('')
            for v in q("SELECT DISTINCT submit_to FROM requests"):
                if re.fullmatch(r"[A-Za-z'.-]{2,}\s*,\s*[A-Za-z'. -]{2,}", v.strip()) and not DEPT_WORDS.search(v):
                    s['names'].append(v.strip())
            s['source'].append(f'build/stl.duckdb ({len(s["req"]):,} request ids, {len(s["parcel"]):,} parcel ids/handles, '
                               f'{len(s["wo"]):,} work orders, {len(s["addr"]):,} addresses)')
        except Exception as e:  # keep scanning with the format rules
            s['source'].append(f'build/stl.duckdb unreadable ({e.__class__.__name__}); format rules only')
    else:
        s['source'].append('build/stl.duckdb not found; format rules only')
    raw = os.path.join(repo, 'data', 'raw')
    n_raw = 0
    for sub in ('cityworks-gap', os.path.join('city-services', 'arcgis', 'cityworks-service'), 'stlouis-mo.gov'):
        top = os.path.join(raw, sub)
        for dp, dn, fn in os.walk(top):
            for f in fn:
                if not f.endswith(('.json', '.jsonl')) or 'metadata' in f:
                    continue
                try:
                    p = os.path.join(dp, f)
                    if os.path.getsize(p) > 50_000_000:
                        continue
                    txt = open(p, encoding='utf-8', errors='replace').read()
                    recs = [json.loads(l) for l in txt.splitlines() if l.strip()] if f.endswith('.jsonl') else [json.loads(txt)]
                except Exception:
                    continue
                stack = recs
                while stack:
                    o = stack.pop()
                    if isinstance(o, dict):
                        for k, v in o.items():
                            if isinstance(v, (dict, list)):
                                stack.append(v)
                            elif isinstance(v, str) and k.lower() in STAFF_FIELDS and looks_like_person(v):
                                s['names'].append(v.strip()); n_raw += 1
                    elif isinstance(o, list):
                        stack.extend(o)
    s['source'].append(f'data/raw Cityworks person fields: {n_raw} values')
    if names_file and os.path.exists(names_file):
        s['names'] += [l.strip() for l in open(names_file, encoding='utf-8') if l.strip()]
    s['name_res'] = name_patterns(s['names'])
    s['source'].append(f'{len(set(s["names"]))} staff-name values')
    return s


def looks_like_person(v):
    v = v.strip()
    if DEPT_WORDS.search(v) or any(ch.isdigit() for ch in v):
        return False
    return bool(re.fullmatch(r"[A-Za-z'.-]{2,}\s*,\s*[A-Za-z'. -]{2,}", v) or
                re.fullmatch(r"[A-Z][a-z'.-]+(?:\s+[A-Z]\.?)?\s+[A-Z][A-Za-z'.-]+", v))


def name_patterns(names):
    out = []
    for n in sorted(set(names)):
        if ',' in n:
            last, first = [x.strip() for x in n.split(',', 1)]
        else:
            parts = n.split()
            first, last = ' '.join(parts[:-1]), parts[-1]
        first1 = first.split()[0] if first else ''
        if len(last) < 2 or len(first1) < 2:
            continue
        L, F = re.escape(last), re.escape(first1)
        out.append(re.compile(rf'(?i)(?<![A-Za-z]){L}\s*,\s*{F}(?![a-z])|(?<![A-Za-z]){F}\s+(?:[A-Z]\.?\s+)?{L}(?![A-Za-z])|(?<![A-Za-z]){L}\s+{F}(?![A-Za-z])'))
    return out


ABBR = {'AVENUE': 'AV', 'AVE': 'AV', 'STREET': 'ST', 'BOULEVARD': 'BLVD', 'DRIVE': 'DR', 'ROAD': 'RD',
        'PLACE': 'PL', 'COURT': 'CT', 'LANE': 'LN', 'TERRACE': 'TER', 'TERR': 'TER', 'PARKWAY': 'PKWY',
        'PLAZA': 'PLZ', 'ALLEY': 'ALY', 'NORTH': 'N', 'SOUTH': 'S', 'EAST': 'E', 'WEST': 'W'}


def norm_addr(a):
    a = re.sub(r'[^A-Z0-9 ]', ' ', str(a).upper())
    return ' '.join(ABBR.get(w, w) for w in a.split())


def check_line(line, sets, ocr=False):
    """Returns (hits, warnings); each item is (category, text)."""
    hits, warns = [], []
    add = lambda cat, txt: hits.append((cat, txt))
    for m in FORBIDDEN.finditer(line):
        add('forbidden', m.group(0))
    for m in DISCLOSURE.finditer(line):
        add('disclosure', m.group(0))
    for m in EMAIL.finditer(line):
        if m.group(1).lower() not in NOT_TLD:
            add('email', m.group(0))
    for m in REQ_CONTEXT.finditer(line):
        if int(m.group(1)) not in KNOWN_COUNTS:
            add('request-id', m.group(0).strip())
    for m in SEVEN.finditer(line):
        n = int(m.group(1))
        if n in KNOWN_COUNTS or UNIT_AFTER.match(line, m.end()) or UNIT_BEFORE.search(line[max(0, m.start() - 5):m.start()]):
            continue
        tok = re.search(r'\S*$', line[:m.start()]).group(0) + re.match(r'\S*', line[m.end():]).group(0)
        if ('://' in tok or tok.startswith('www.') or '/' in tok) and not CITY_URL.search(tok):
            continue
        if sets['req']:
            if n in sets['req']:
                add('request-id', m.group(1))
        elif 1_000_000 <= n <= 2_999_999:
            add('request-id', m.group(1) + ' (unverified: no id set)')
    for m in LONGNUM.finditer(line):
        v = m.group(1)
        if len(v) == 11 or v.lstrip('0') in sets['parcel']:
            add('parcel-id', v)
    if sets['wo'] and WO_CONTEXT.search(line):
        for m in SIX.finditer(line):
            if int(m.group(1)) in sets['wo']:
                add('workorder-id', m.group(1))

    def real(num, street):
        words = norm_addr(street).split()
        forms = {' '.join(words)} | ({' '.join(words[1:])} if len(words) > 2 and words[0] in 'NSEW' else set())
        return any(f'{num} {f}' in sets['addr'] for f in forms)

    def highway(start):
        return bool(HIGHWAY_BEFORE.search(line[max(0, start - 12):start]))

    # Format rule. With the address set loaded, an address-shaped string that is not a real
    # 311 or parcel address (a docstring example) is a warning; a real one is a hit.
    seen = set()
    for m in ADDR_FORMAT.finditer(line):
        if PLACEHOLDER_STREET.search(m.group(2)) or highway(m.start()):
            continue
        seen.add(m.start())
        if not sets['addr'] or real(m.group(1), m.group(2)):
            add('address', m.group(0).strip())
        else:
            warns.append(('address-shaped', m.group(0).strip()))
    if sets['addr']:
        for m in ADDR_CAND.finditer(line):
            if m.start() in seen or PLACEHOLDER_STREET.search(m.group(2)) or highway(m.start()):
                continue
            if real(m.group(1), m.group(2)):
                add('address', m.group(0).strip() + ' (real address)')
    for m in TWO_NUM.finditer(line):
        if PLACEHOLDER_STREET.search(m.group(0)):
            continue
        a, b, street = m.group(1), m.group(2), m.group(3)
        if not sets['addr'] or real(a, street) or real(b, street):
            add('address', m.group(0).strip() + ' (two-number label)')
        else:
            warns.append(('address-shaped', m.group(0).strip() + ' (two-number label)'))
    for m in ODD_BLOCK.finditer(line):
        if int(m.group(1)) % 100 != 0:
            add('address', m.group(0) + ' (block label with a house number)')
    if not ocr:
        for m in LATLON.finditer(line):
            if not MAP_PLACE_BEFORE.search(line[max(0, m.start() - 200):m.start()]):
                add('latlon', m.group(0))
        for m in MERC.finditer(line):
            v = m.group(0).replace(',', '')
            if '.' not in v and int(v) % 10000 == 0:
                continue  # a round bounding-box constant in code, not a point
            add('srx-sry', m.group(0))
        if MERC_PAIR_Y.search(line) and re.search(r'-100\d{5}\.\d', line):
            add('srx-sry', MERC_PAIR_Y.search(line).group(0))
        for m in SRXY_KV.finditer(line):
            add('srx-sry', m.group(0))
    for rx in sets['name_res']:
        for m in rx.finditer(line):
            add('staff-name', '[name withheld]')
    return hits, warns


def plausible(key, v):
    """A number under an id or coordinate key that could be a real id or a St. Louis location."""
    if key in ('lat', 'latitude'):
        return 38 <= v <= 39
    if key in ('lon', 'lng', 'longitude'):
        return -91 <= v <= -89
    if key in ('srx', 'woxcoordinate'):
        return -10_100_000 <= v <= -10_000_000 or 800_000 <= v <= 950_000
    if key in ('sry', 'woycoordinate'):
        return 4_600_000 <= v <= 4_720_000 or 950_000 <= v <= 1_100_000
    return abs(v) >= 100_000


def check_structured(rel, text):
    """JSON keys and CSV columns that carry ids, exact addresses or coordinates."""
    hits = []
    low = rel.lower()
    if low.endswith('.csv') or low.endswith('.tsv'):
        try:
            rdr = csv.reader(io.StringIO(text), delimiter='\t' if low.endswith('.tsv') else ',')
            header = next(rdr, [])
            bad = [i for i, h in enumerate(header) if h.strip().lower() in ID_KEYS]
            if bad:
                filled = Counter()
                for row in rdr:
                    for i in bad:
                        if i < len(row) and row[i].strip() not in ('', 'null', 'None', 'NaN'):
                            filled[i] += 1
                for i in bad:
                    if filled[i]:
                        hits.append((1, 'id-field', f'column "{header[i]}" ({filled[i]} values)'))
        except Exception:
            pass
    elif low.endswith('.json') or low.endswith('.geojson'):
        try:
            obj = json.loads(text)
        except Exception:
            return hits
        found = Counter()
        stack = [obj]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                for k, v in o.items():
                    if isinstance(k, str) and k.lower() in ID_KEYS and v not in (None, '', [], {}):
                        if isinstance(v, int) and v in KNOWN_COUNTS:
                            continue  # e.g. "request_ids": 1454222 is the count of ids
                        if k.lower() == 'owner' and not (isinstance(v, str) and looks_like_person(v)):
                            continue  # figure owner = the session that registered it ("N1")
                        if isinstance(v, (int, float)) and not isinstance(v, bool) and not plausible(k.lower(), v):
                            continue  # a count keyed by the field name ("WOAddress": 0)
                        found[k] += 1
                    if isinstance(v, (dict, list)):
                        stack.append(v)
            elif isinstance(o, list):
                stack.extend(o)
        for k, n in found.items():
            line = next((i for i, l in enumerate(text.splitlines(), 1) if f'"{k}"' in l), 1)
            hits.append((line, 'id-field', f'key "{k}" ({n} non-empty values)'))
    return hits


def ocr_text(path):
    try:
        r = subprocess.run(['tesseract', path, 'stdout', '--psm', '3'], capture_output=True, text=True, timeout=180)
        return r.stdout
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('export_dir')
    ap.add_argument('--repo', default=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')),
                    help='working repository that holds build/stl.duckdb and data/raw (default: this script\'s repo)')
    ap.add_argument('--no-ocr', action='store_true', help='skip OCR of images')
    ap.add_argument('--failing-files', help='write the relative paths of failing files here, one per line')
    ap.add_argument('--names-file', help='extra staff names, one per line (kept outside the export)')
    ap.add_argument('--accept', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ALLOWLIST.md'),
                    help='file whose ```accept block lists reviewed hits: path | category | exact text | reason')
    a = ap.parse_args()
    accepted = set()
    if a.accept and os.path.exists(a.accept):
        m = re.search(r'```accept\n(.*?)```', open(a.accept, encoding='utf-8').read(), re.S)
        for l in (m.group(1).splitlines() if m else []):
            parts = [x.strip() for x in l.split('|')]
            if len(parts) >= 3 and not l.lstrip().startswith('#'):
                accepted.add(tuple(parts[:3]))
                # the reviewed text also appears in the accept block itself
                accepted.add(('scripts/exec/E4/' + os.path.basename(a.accept), parts[1], parts[2]))
    root = os.path.abspath(a.export_dir)
    if not os.path.isdir(root):
        print(f'scan_public: {root} is not a directory', file=sys.stderr); return 2
    sets = load_sets(os.path.abspath(a.repo), a.names_file)
    for s in sets['source']:
        print('scan_public: using', s)
    have_ocr = shutil.which('tesseract') and not a.no_ocr
    hits, warns, awarns, files, ocr_skipped = [], [], [], 0, []
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if d != '.git')
        for f in sorted(fn):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root)
            files += 1
            for cat, txt in check_line(rel, sets)[0]:
                hits.append((rel, 0, cat, 'in the file name: ' + txt))
            ext = os.path.splitext(f)[1].lower()
            if ext in IMAGE_EXT:
                if not have_ocr:
                    ocr_skipped.append(rel); continue
                t = ocr_text(p)
                if t is None:
                    ocr_skipped.append(rel); continue
                for i, line in enumerate(t.splitlines(), 1):
                    h, w = check_line(line, sets, ocr=True)
                    hits += [(rel, i, cat + ' (OCR)', txt) for cat, txt in h]
                    awarns += [(rel, i, cat + ' (OCR)', txt) for cat, txt in w]
                continue
            raw = open(p, 'rb').read()
            if ext not in TEXT_EXT or b'\x00' in raw[:8192]:
                hits.append((rel, 0, 'unscannable', f'binary file ({ext or "no extension"}), not scanned'))
                continue
            text = raw.decode('utf-8', errors='replace')
            count_cols = []
            if ext in ('.csv', '.tsv'):
                head = next(csv.reader([text.split('\n', 1)[0]]), [])
                count_cols = [i for i, c in enumerate(head) if c.strip().lower() in COUNT_COLS]
            for i, line in enumerate(text.splitlines(), 1):
                if count_cols and i > 1:  # sizes and row counts are not ids
                    cells = next(csv.reader([line]), [])
                    for c in count_cols:
                        if c < len(cells) and re.fullmatch(r'\d+', cells[c].strip()):
                            cells[c] = ''
                    buf = io.StringIO(); csv.writer(buf).writerow(cells); line = buf.getvalue().rstrip('\r\n')
                h, w = check_line(line, sets)
                hits += [(rel, i, cat, txt) for cat, txt in h]
                awarns += [(rel, i, cat, txt) for cat, txt in w]
                if WARN.search(line):
                    warns.append((rel, i, WARN.search(line).group(0)))
            for i, cat, txt in check_structured(rel, text):
                hits.append((rel, i, cat, txt))
    kept = [h for h in hits if (h[0], h[2].replace(' (OCR)', ''), h[3]) not in accepted]
    if len(kept) < len(hits):
        print(f'scan_public: {len(hits) - len(kept)} hits accepted by the reviewed list in {a.accept}')
    hits = kept
    for rel, i, cat, txt in hits:
        print(f'HIT  {rel}:{i}: [{cat}] {txt[:160]}')
    byfile = defaultdict(int)
    for rel, i, tag in warns:
        byfile[rel] += 1
    for rel, n in sorted(byfile.items()):
        print(f'WARN {rel}: {n} unfinished placeholder(s) ({{{{fig:, [JACK or PLACEHOLDER)')
    for rel, i, cat, txt in awarns:
        print(f'WARN {rel}:{i}: [{cat}, matches no real address] {txt[:120]}')
    if ocr_skipped:
        print(f'WARN {len(ocr_skipped)} image(s) not OCR-scanned (tesseract missing or failed); check them by eye')
    failing = sorted({h[0] for h in hits})
    if a.failing_files:
        with open(a.failing_files, 'w') as fh:
            fh.write(''.join(r + '\n' for r in failing))
    cats = Counter(h[2] for h in hits)
    print(f'scan_public: {files} files scanned; {len(hits)} hits in {len(failing)} files'
          + (' (' + ', '.join(f'{c} {n}' for c, n in cats.most_common()) + ')' if hits else '')
          + f'; {len(warns)} placeholder warnings; {len(awarns)} address-shaped warnings')
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main())
