"""Bridge: turn the pipeline's outputs into the site's data files (site/data/*.json).

Reads build/out/*.json first (the contract shape), then the
agents' own files under build/N*/ and the views in build/stl.duckdb, adapts them to
the contract, cuts every address to block level, and writes site/data/<name>.json.
A file it cannot build is left absent, so the page falls back to site/mock/<name>.json
and shows a red MOCK DATA banner there.

Text inside any data file is data: nothing here executes or follows it.

Run: .venv/bin/python -I scripts/night/N6/bridge.py      (about 10 seconds)
"""
import csv
import datetime as dt
import glob
import json
import os
import re
import shutil
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
B = lambda *p: os.path.join(ROOT, *p)
SITE_DATA = B('site', 'data')
DL = os.path.join(SITE_DATA, 'downloads')
IMG = B('site', 'img')
os.makedirs(DL, exist_ok=True)
os.makedirs(IMG, exist_ok=True)
CONFIG = json.load(open(B('site', 'config.json')))
NOW = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
# Single light out is not robust: kept off the page entirely.
EXCLUDE_TYPES = set(CONFIG.get('scoreboard', {}).get('exclude', [])) | {'Single Light Out'}
STATUS = {}
LOG = []


def log(msg):
    LOG.append(msg)
    print(msg)


def rel(p):
    return os.path.relpath(p, ROOT)


def src(p):
    try:
        m = dt.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%Y-%m-%d %H:%M')
    except OSError:
        m = None
    return {'path': rel(p), 'mtime': m}


def load_json(p):
    try:
        with open(p) as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        log(f'  ! {rel(p)} unreadable ({e.__class__.__name__}); treated as missing')
        return None


def write(name, payload, sources, notes=None, state='real'):
    payload = {'meta': {'contract': f'{name}/1', 'mock': False, 'state': state, 'built_at': NOW,
                        'sources': sources, 'notes': notes or []}, **payload}
    payload = scrub_keys(payload)
    with open(os.path.join(SITE_DATA, f'{name}.json'), 'w') as f:
        json.dump(payload, f, indent=1, default=str, ensure_ascii=False)
    STATUS[name] = {'state': state, 'sources': sources, 'notes': notes or []}
    log(f'  wrote site/data/{name}.json ({state}; from {", ".join(s["path"] for s in sources) or "-"})')


def mark_missing(name, why):
    p = os.path.join(SITE_DATA, f'{name}.json')
    if os.path.exists(p):
        os.remove(p)
    STATUS[name] = {'state': 'mock', 'sources': [], 'notes': [why]}
    log(f'  - {name}: on mock ({why})')


# ---------------------------------------------------------------- block level
SUFFIX = (r'(?:AV|AVE|AVENUE|ST|STREET|BLVD|BOULEVARD|DR|DRIVE|PL|PLACE|RD|ROAD|CT|COURT|TER|TERRACE|'
          r'LN|LANE|PKWY|PARKWAY|WAY|HWY|SQ|ALY|ALLEY|CIR|ROW|PLZ)')
# Case-sensitive on purpose: street words start with a capital and the suffix is 'AV' or 'Av'.
# A case-insensitive pattern turned prose such as "Q2 2026 residential and alley ..." into a fake block.
SUFFIX_ANY = '(?:' + '|'.join(sorted({w for t in SUFFIX[3:-1].split('|') for w in (t, t.capitalize())}, key=len, reverse=True)) + ')'
ADDR_SUFFIX = re.compile(r'\b(\d{1,5})(?:-\d{1,5})?[ \t]+((?:[NSEW]\.?[ \t]+)?(?:[A-Z0-9][A-Za-z0-9\.\']*[ \t]+){0,4}?' + SUFFIX_ANY + r')\b\.?')
ADDR_DIR = re.compile(r'\b(\d{1,5})\s+([NSEW]\.?\s+[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)')
ALREADY = re.compile(r'\b\d{1,5}00 block of\b', re.I)
PARCELISH = re.compile(r'\b\d{10,11}\b')


def tidy_street(s):
    words = s.replace('.', '').split()
    out = []
    for w in words:
        u = w.upper()
        out.append(u if u in ('N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW') else w.capitalize())
    return ' '.join(out)


def to_block(num, street):
    n = int(num)
    return f'{(n // 100) * 100} block of {tidy_street(street)}'


def scrub_text(s):
    if not isinstance(s, str) or not s:
        return s
    if ALREADY.search(s) and not ADDR_SUFFIX.search(ALREADY.sub('', s)):
        return PARCELISH.sub('[parcel]', s)

    def rep(m):
        # leave "block of" phrases and years/durations alone
        pre = s[max(0, m.start() - 9):m.start()].lower()
        if 'block of' in pre:
            return m.group(0)
        return to_block(m.group(1), m.group(2))
    out = ADDR_SUFFIX.sub(rep, s)
    out = ADDR_DIR.sub(rep, out)
    return PARCELISH.sub('[parcel]', out)


def scrub_obj(o):
    if isinstance(o, dict):
        return {k: scrub_obj(v) for k, v in o.items()}
    if isinstance(o, list):
        return [scrub_obj(v) for v in o]
    if isinstance(o, str):
        return scrub_text(o)
    return o


# Only fields that can carry an address are scrubbed; prose (negative results, derivations) is left as written.
ADDRESS_KEYS = {'block', 'public_address', 'block_label', 'closed_with_words', 'story', 'caption', 'title', 'detail', 'line'}


def scrub_keys(o, key=None):
    if isinstance(o, dict):
        return {k: scrub_keys(v, k) for k, v in o.items()}
    if isinstance(o, list):
        return [scrub_keys(v, key) for v in o]
    if isinstance(o, str) and key in ADDRESS_KEYS:
        return scrub_text(o)
    return o


def block_label(lbl):
    """N1 block labels look like '4100 block of N NEWSTEAD AV'; tidy the case."""
    if not lbl:
        return None
    m = re.match(r'^\s*(\d+)\s*&\s*(\d+)\s+(?:block of\s+)?(.+)$', lbl, re.I)  # "1234 & 1236 EXAMPLE AV"
    if m:
        return to_block(m.group(1), m.group(3))
    m = re.match(r'^\s*(\d+)\s+block of\s+(.+)$', lbl, re.I)
    if m:
        return to_block(m.group(1), m.group(2))
    m = re.match(r'^\s*(\d{1,5})\s+(.+)$', lbl)
    if m:
        return to_block(m.group(1), m.group(2))
    return tidy_street(lbl)


# ---------------------------------------------------------------- helpers
def iso(v, minutes=True):
    if v is None or v == '':
        return None
    if isinstance(v, dt.datetime):
        return v.strftime('%Y-%m-%d %H:%M') if minutes else v.strftime('%Y-%m-%d')
    if isinstance(v, dt.date):
        return v.strftime('%Y-%m-%d')
    if isinstance(v, (int, float)) and v > 1e11:  # epoch ms
        return dt.datetime.fromtimestamp(v / 1000).strftime('%Y-%m-%d %H:%M')
    return str(v).replace('T', ' ')[:16 if minutes else 10]


DATE_FIELDS = ('filed', 'promised', 'investigation_done', 'closed', 'cancelled', 'ledger_last_cut_before',
               'ledger_first_cut_after', 'ledger_max', 'next_same_request_filed')


def num(v):
    try:
        if v is None or v == '':
            return None
        f = float(v)
        return None if f != f else f
    except (TypeError, ValueError):
        return None


def first(*paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def rows_of(obj, *keys):
    if obj is None:
        return None
    if isinstance(obj, list):
        return obj
    for k in keys:
        if isinstance(obj.get(k), list):
            return obj[k]
    return None


NEIGHBORHOODS = {}
try:
    _nb = json.load(open(B('data', 'raw', 'city-services', 'arcgis', 'layers', 'maps8_BOUNDARIES_Neighborhoods.geojson')))
    NEIGHBORHOODS = {str(f['properties']['NHD_NUM']): f['properties']['NHD_NAME'] for f in _nb['features']}
except Exception as e:  # noqa: BLE001
    log(f'  ! neighbourhood names unavailable ({e.__class__.__name__})')


def nbhd(v):
    if v is None:
        return None
    s = str(v).strip().lstrip('0') or '0'
    return NEIGHBORHOODS.get(s, None if s.isdigit() else str(v))


# The city's own plain-English name for each request type (PLAIN_ENGLISH_NAME_FOR_PROBLEMCODE,
# most common value per PROBLEMCODE, as loaded by N1 into requests.type_name). Pages show these,
# never the abbreviated codes. Fallback: the code with its abbreviations spelled out.
PLAIN = None
ABBREV = {'containr': 'container', 'cntnr': 'container', 'cntainr': 'container', 'cntnrs': 'containers', 'ppty': 'property',
          'illegl': 'illegal', 'opn': 'open', 'storg': 'storage', 'vacnt': 'vacant', 'bldg': 'building', 'requst': 'request',
          'residnl': 'residential', 'rt': 'right', 'dumpg': 'dumping', 'blk': 'block', 'yrd': 'yard', 'wste': 'waste',
          'collect': 'collected', 'misg': 'missing', 'postion': 'position', 'int': 'interior', 'ext': 'exterior',
          'st': 'street', 'v': 'vacant', 'vlot': 'vacant lot', 'vbldg': 'vacant building', 'unsatisfy': 'unsatisfactory',
          'equip': 'equipment', 'rpt': 'report', 'wtr': 'water', 'misc': 'miscellaneous', 'div': 'division'}


def _clean_code(code):
    words = re.split(r'[\s\-/]+', str(code or '').strip())
    out = [ABBREV.get(w.lower(), w.lower()) for w in words if w]
    t = ' '.join(out)
    return t[:1].upper() + t[1:] if t else code


def _tidy_plain(t):
    t = re.sub(r'\s+', ' ', str(t or '')).strip().rstrip('.')
    return t[:1].upper() + t[1:] if t else t


def plain_name(code):
    global PLAIN
    if code is None:
        return None
    if PLAIN is None:
        PLAIN = {}
        rows = q("""SELECT problem_code, mode(type_name) AS t FROM requests
                    WHERE type_name IS NOT NULL AND trim(type_name) <> '' GROUP BY 1""") or []
        PLAIN = {r['problem_code']: _tidy_plain(r['t']) for r in rows if r['t']}
        for r in rows_of(load_json(B('build', 'N4', 'scoreboard.json')), 'rows') or []:
            if r.get('problemcode') and r.get('name') and r['problemcode'] not in PLAIN:
                PLAIN[r['problemcode']] = _tidy_plain(r['name'])
    return PLAIN.get(code) or _clean_code(code)


def plain_in_text(text):
    """Replace a quoted request-type code inside free text with the city's plain name."""
    if not isinstance(text, str) or '"' not in text:
        return text
    plain_name('_load_')
    for code in sorted(PLAIN or {}, key=len, reverse=True):
        if f'"{code}"' in text:
            text = text.replace(f'"{code}"', f'"{PLAIN[code]}"')
    return text


DB = None


def db():
    global DB
    if DB is None:
        p = B('build', 'stl.duckdb')
        if not os.path.exists(p):
            return None
        try:
            import duckdb
            DB = duckdb.connect(p, read_only=True)
        except Exception as e:  # noqa: BLE001
            log(f'  ! build/stl.duckdb not readable ({e.__class__.__name__}: {str(e)[:80]})')
            DB = False
    return DB or None


def q(sql, params=None):
    con = db()
    if con is None:
        return None
    try:
        cur = con.execute(sql, params or [])
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    except Exception as e:  # noqa: BLE001
        log(f'  ! query failed ({e.__class__.__name__}: {str(e)[:120]})')
        return None


# ---------------------------------------------------------------- run
def build_run():
    p = first(B('build', 'out', 'run.json'), B('build', 'out', 'meta.json')) or B('build', 'out', 'run.json')
    d = load_json(p)
    if d:
        write('run', {'asof': d.get('asof'), 'ledger_max_date': d.get('ledger_max_date'), 'built_at': d.get('built_at')}, [src(p)])
        return
    p = B('build', 'N1', 'manifest.json')
    d = load_json(p)
    if d and d.get('meta'):
        m = d['meta']
        write('run', {'asof': iso(m.get('asof_ts')) or m.get('asof'), 'ledger_max_date': m.get('ledger_max_date'),
                      'built_at': m.get('built_at')}, [src(p)])
        return
    mark_missing('run', 'no build/out/run.json or build/N1/manifest.json')


# ---------------------------------------------------------------- figures
def norm_derivations(d):
    out = {}
    if d is None:
        return out
    if isinstance(d, dict) and isinstance(d.get('chains'), list):
        chains = {c.get('id'): c for c in d['chains'] if isinstance(c, dict)}
        for fid, cid in (d.get('figure_index') or {}).items():
            c = chains.get(cid)
            if not c:
                continue
            out[fid] = {'text': None, 'chain': None, 'curated': {
                'title': c.get('title'), 'plain': c.get('plain'), 'label': c.get('label'),
                'sources': [{'name': x.get('name'), 'where': x.get('where')} for x in (c.get('sources') or []) if isinstance(x, dict)],
                'joins': c.get('joins'), 'corrections': c.get('corrections'), 'bounds': c.get('bounds'), 'script': c.get('script')}}
        return out
    items = d if isinstance(d, list) else rows_of(d, 'derivations', 'figures')
    if items is None and isinstance(d, dict):
        items = [{'id': k, **(v if isinstance(v, dict) else {'text': v})} for k, v in d.items() if k != 'meta']
    for it in items or []:
        if not isinstance(it, dict) or not it.get('id'):
            continue
        text = it.get('derivation') or it.get('text') or it.get('plain')
        chain = it.get('chain') or it.get('steps') or it.get('sources')
        if isinstance(text, list):
            text = ' '.join(str(t) for t in text)
        out[it['id']] = {'text': text, 'chain': chain if isinstance(chain, list) else None,
                         'negative': it.get('negative_results') or it.get('bounds')}
    return out


def build_figures():
    figs, sources = {}, []
    p = B('build', 'out', 'figures.json')
    d = load_json(p)
    items = rows_of(d, 'figures')
    if items is None and isinstance(d, dict) and isinstance(d.get('figures'), dict):
        items = [{'id': k, **v} for k, v in d['figures'].items() if isinstance(v, dict)]
    if items is None and isinstance(d, dict) and d:
        items = [v for k, v in d.items() if isinstance(v, dict) and 'value' in v]
    if items:
        sources.append(src(p))
    else:
        items = []
    # union with every agent's own registry: build/out wins, newer agent figures fill the gaps
    have = {str(it.get('id')) for it in items if isinstance(it, dict)}
    # E3 (14 Oct): the three-surface demo registers e3_* figures in build/E3/figures.json
    for fp in sorted(glob.glob(B('build', 'N*', 'figures.json'))) + [B('build', 'E3', 'figures.json')]:
        fd = load_json(fp)
        its = [it for it in (rows_of(fd, 'figures') or []) if isinstance(it, dict) and str(it.get('id')) not in have
               and not it.get('retired')]  # retired figures stay in build/out/retired_figures.json
        if its:
            items.extend(its)
            have |= {str(it.get('id')) for it in its}
            sources.append(src(fp))
    n_retired = 0
    for it in items:
        if isinstance(it, dict) and it.get('retired'):  # retired figures never reach the site
            n_retired += 1
            continue
        if isinstance(it, dict) and it.get('id') is not None:
            figs[str(it['id'])] = {k: (public_text(it.get(k)) if isinstance(it.get(k), str) else it.get(k))
                                   for k in ('id', 'value', 'unit', 'period', 'definition', 'label', 'source_sql_or_script', 'note', 'derivation')}
    dp = B('build', 'out', 'derivations.json')
    der = norm_derivations(load_json(dp))
    if der:
        sources.append(src(dp))
    n_der = 0
    for fid, f in figs.items():
        dd = der.get(fid)
        if dd:
            if dd.get('text') and not f.get('derivation'):
                f['derivation'] = dd['text']
            if dd.get('chain'):
                f['derivation_chain'] = dd['chain']
            if dd.get('curated') and not unsafe(dd['curated']):
                f['chain'] = json.loads(json.dumps(dd['curated']), object_hook=lambda o: {k: public_text(v) if isinstance(v, str) else
                                        ([public_text(x) if isinstance(x, str) else x for x in v] if isinstance(v, list) else v) for k, v in o.items()})
                if not f.get('derivation'):
                    f['derivation'] = dd['curated'].get('plain')
        if f.get('derivation'):
            n_der += 1
    if not figs:
        mark_missing('figures', 'no figures files yet')
        return {}
    notes = [f'{len(figs)} figures; {n_der} carry a derivation sentence'] + ([f'{n_retired} retired figures left out'] if n_retired else [])
    wanted = [CONFIG['lead']['figure_id']] + [s['figure_id'] for s in CONFIG['lead'].get('support', [])]
    missing = [w for w in wanted if w not in figs]
    if missing:
        notes.append('lead figures missing: ' + ', '.join(missing))
    write('figures', {'figures': figs}, sources, notes, 'real' if not missing else 'partial')
    return figs


# ---------------------------------------------------------------- receipts
RECEIPT_COLS = ['request_id', 'problem_code', 'type_name', 'family', 'division', 'ward', 'neighborhood', 'channel_group',
                'public_address', 'is_lra', 'filed', 'promised', 'promise_days', 'investigation_done', 'closed',
                'cancelled', 'status', 'status_group', 'closed_with_words', 'closure_class', 'days_to_close',
                'closed_by_promise', 'done_by_promise', 'days_vs_promise', 'ledger_last_cut_before',
                'ledger_first_cut_after', 'ledger_days_to_first_cut', 'ledger_no_cut_in_season', 'ledger_cut_within_30',
                'ledger_cut_within_60', 'ledger_max', 'work_orders_nearby', 'next_same_request_filed',
                'days_to_next_same_request', 'sensitive']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']


def nice_date(s, year=False):
    if not s:
        return None
    try:
        d = dt.datetime.strptime(str(s)[:10], '%Y-%m-%d')
    except ValueError:
        return str(s)
    return f'{d.day} {MONTHS[d.month - 1]}' + (f' {d.year}' if year else '')


def clean_receipt(r):
    out = {}
    for k in RECEIPT_COLS:
        if k in r:
            v = r[k]
            if isinstance(v, (dt.datetime, dt.date)) or (k in DATE_FIELDS and v):
                v = iso(v)
            out[k] = v
    out['request_id'] = str(r.get('request_id'))
    out['public_address'] = block_label(r.get('public_address') or r.get('block_label') or r.get('block'))
    out['neighborhood'] = nbhd(r.get('neighborhood'))
    out['ward'] = (f"{int(r['ward']):02d}" if str(r.get('ward') or '').strip().isdigit() else r.get('ward'))
    return out


def when_closed(days):
    if days is None:
        return None
    if days < 1 / 24:
        return 'within the hour'
    if days < 1:
        return 'the same day' if days < 0.5 else 'within a day'
    d = int(days)
    return f'on day {d}'


def receipt_line(r):
    parts = []
    words = (r.get('closed_with_words') or '').strip()
    sg = r.get('status_group')
    dtc = num(r.get('days_to_close'))
    if sg == 'closed':
        w = when_closed(dtc) or ''
        parts.append(f'Closed {w} as “{words}”.' if words else f'Closed {w} with no words recorded.')
    elif sg == 'cancelled':
        c, f = r.get('cancelled'), r.get('filed')
        days = None
        try:
            days = (dt.datetime.fromisoformat(c) - dt.datetime.fromisoformat(f)).total_seconds() / 86400
        except (TypeError, ValueError):
            pass
        w = when_closed(days) or ''
        parts.append(f'Cancelled {w} as “{words}”.' if words else f'Cancelled {w} with no explanation.')
    else:
        parts.append(f'Still open (status {r.get("status")}).')
    if r.get('promised'):
        parts.append(f"The city's own promised date was {nice_date(r['promised'])}.")
    fam = r.get('family') or ''
    pc = (r.get('problem_code') or '')
    lot = 'this city-owned lot' if r.get('is_lra') else ('this lot' if 'Lot' in pc else 'this property')
    if fam == 'weeds' or pc.startswith('Weeds-Vacant'):
        lm = r.get('ledger_max')
        yr = (r.get('filed') or '')[:4]
        if r.get('ledger_no_cut_in_season'):
            parts.append(f'Its forestry ledger shows no cut on {lot} in {yr}.')
        elif r.get('ledger_first_cut_after'):
            n = num(r.get('ledger_days_to_first_cut'))
            parts.append(f'Its forestry ledger shows the next cut billed on {nice_date(r["ledger_first_cut_after"])}'
                         + (f', {int(n)} days after the request.' if n is not None else '.'))
        elif lm:
            parts.append(f'Its forestry ledger, posted to {nice_date(lm)}, shows no cut on {lot} after the request.')
    elif pc in ('Inspect City Tree', 'Tree Planting requst') or fam == 'trees':
        n = r.get('work_orders_nearby')
        if n:
            parts.append(f"The city's published sample of Forestry work orders shows {int(n)} at this address.")
        else:
            parts.append("No Forestry work order at this address in the city's published sample.")
    else:
        parts.append("The city publishes no separate record of this work, so the closing words are the only record.")
    if r.get('next_same_request_filed'):
        n = num(r.get('days_to_next_same_request'))
        parts.append(f'The same problem was reported at this address again {int(n)} days later.' if n is not None
                     else 'The same problem was reported at this address again.')
    return ' '.join(parts)


def receipt_timeline(r):
    ev = []
    add = lambda d, k, t, det='', s='311', lab='observed': ev.append(
        {'date': d, 'kind': k, 'title': t, 'detail': det, 'source': s, 'label': lab}) if d else None
    add(r.get('filed'), 'filed', 'Filed', f"{r.get('type_name') or r.get('problem_code')}"
        + (f" · {r['channel_group']} channel" if r.get('channel_group') else ''))
    words = (r.get('closed_with_words') or '').strip()
    inv, end = r.get('investigation_done'), r.get('closed') or r.get('cancelled')
    if inv and (not end or abs((dt.datetime.fromisoformat(str(end)[:16]) - dt.datetime.fromisoformat(str(inv)[:16])).total_seconds()) > 3600):
        add(inv, 'inspect', 'Investigation recorded done', 'the request\'s own investigation stamp (DATEINVTDONE)')
    if r.get('status_group') == 'closed':
        add(r.get('closed'), 'closed', 'Closed', f'“{words}”' if words else 'no words recorded')
    elif r.get('status_group') == 'cancelled':
        add(r.get('cancelled'), 'cancelled', 'Cancelled', f'“{words}”' if words else 'no explanation recorded')
    add(r.get('promised'), 'promised', "The city's promised date",
        f"{int(num(r['promise_days']))} days after filing, set by the city on the request" if num(r.get('promise_days')) else '')
    pc = r.get('problem_code') or ''
    if r.get('family') == 'weeds' or pc.startswith('Weeds-Vacant'):
        if r.get('ledger_first_cut_after'):
            add(r['ledger_first_cut_after'], 'record', 'Forestry ledger: cut billed', 'grass cut billed on the parcel; ledger dates are posted in weekly batches', 'ledger')
        elif r.get('ledger_max'):
            add(r['ledger_max'], 'record', 'Forestry ledger: no cut', f"no cut billed on the parcel after the request, ledger posted to {nice_date(r['ledger_max'], True)}", 'ledger')
    elif pc == 'Inspect City Tree':
        if r.get('work_orders_nearby'):
            add(r.get('closed') or r.get('cancelled') or r.get('filed'), 'record', 'Forestry work orders', f"{int(r['work_orders_nearby'])} in the published sample at this address", 'cityworks')
    if r.get('next_same_request_filed'):
        add(r['next_same_request_filed'], 'refiled', 'Reported again', 'same problem, same address')
    ev.sort(key=lambda e: e['date'])
    return ev


EXAMPLES = [
    {'key': 'lot', 'label': 'The lot', 'cases': ['lot-1']},
    {'key': 'tree', 'label': 'The tree', 'cases': ['tree-2']},
    {'key': 'cave', 'label': 'The cave-in pair', 'cases': ['cave-1', 'cave-2']},
    {'key': 'works', 'label': 'When it works', 'cases': ['lot-counterexample']},
    {'key': 'lot2', 'label': 'Another lot', 'cases': ['lot-2']},
    {'key': 'tree1', 'label': 'Another tree', 'cases': ['tree-1']},
]
ID_KEYS = {'request_id', 'request_ids', 'workorder_id', 'parcel_id', 'handle', 'next_same_request_id', 'related_parcels',
           'centroid_lat', 'centroid_lon', 'lat', 'lon', 'srx', 'sry', 'x', 'y', 'cityblock', 'work_orders'}


def strip_ids(o):
    """Drop id-bearing keys anywhere in a structure (no request, work-order or parcel ids)."""
    if isinstance(o, dict):
        return {k: strip_ids(v) for k, v in o.items() if k not in ID_KEYS}
    if isinstance(o, list):
        return [strip_ids(v) for v in o]
    return o


def event_kind(e):
    d = str(e.get('date') or '')
    text = str(e.get('event') or '').lower()
    s = str(e.get('source') or '')
    if e.get('related') or text.startswith('neighbouring') or text.startswith('neighboring'):
        return 'related'
    if re.fullmatch(r'\d{4}', d):
        return 'history'
    if 'promise date' in text:
        return 'promised'
    if re.search(r'\bfiled\b', text):
        return 'filed'
    if text.startswith('closed') or ' closed after' in text:
        return 'closed'
    if 'cancel' in text:
        return 'cancelled'
    if 'latest date in the ledger' in text or s in ('ledger', 'wo_rm', 'wo_trim', 'cityworks') or 'work order' in text:
        return 'record'
    return 'history'


def copy_images(case):
    """Public-domain NAIP images are the default. MSDIS images appear only when site/config.json sets
    "show_msdis_imagery": true (their terms for public use are unsettled)."""
    out = []
    show_msdis = bool(CONFIG.get('show_msdis_imagery', False))
    try:
        from PIL import Image
    except Exception:  # noqa: BLE001
        Image = None
    for im in case.get('public_images') or case.get('images') or []:
        if isinstance(im, str):
            im = {'path': im}
        path = im.get('path') or im.get('src')
        if not path or '/private/' in path:
            continue
        tag = f"{im.get('service') or ''} {path} {im.get('source') or ''}".lower()
        kind = 'naip' if 'naip' in tag else 'msdis'
        if kind == 'msdis' and not show_msdis:
            continue
        sp = path if os.path.isabs(path) else B(path)
        if not os.path.exists(sp):
            continue
        base = os.path.splitext(os.path.basename(sp))[0]
        dst = os.path.join(IMG, base + '.jpg')
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(sp):
            if Image:
                img = Image.open(sp).convert('RGB')
                if img.width > 1400:
                    img = img.resize((1400, round(img.height * 1400 / img.width)))
                img.save(dst, 'JPEG', quality=86, optimize=True)
            else:
                dst = os.path.join(IMG, os.path.basename(sp))
                shutil.copyfile(sp, dst)
        lic = im.get('licence') or im.get('license')
        label = im.get('source') or ('NAIP 2024 (USDA, public domain)' if kind == 'naip' else 'MSDIS')
        out.append({'src': 'img/' + os.path.basename(dst), 'year': im.get('year'), 'service': im.get('service'), 'kind': kind,
                    'source_label': label, 'licence': lic,
                    'caption': scrub_text(im.get('caption') or ''), 'note': im.get('note')})
    out.sort(key=lambda x: (x['kind'] != 'naip', str(x.get('year') or '')), reverse=False)
    naip = [x for x in out if x['kind'] == 'naip']
    rest = sorted([x for x in out if x['kind'] != 'naip'], key=lambda x: str(x.get('year') or ''), reverse=True)
    return naip + rest


def build_receipts():
    """Named examples from N5 (block level, no ids). Typed ids are answered by serve.py's local lookup, not by data here."""
    hp = B('build', 'N5', 'heroes.json')
    hd = load_json(hp)
    cases = {c.get('id'): c for c in (rows_of(hd, 'cases', 'heroes') or []) if isinstance(c, dict)}
    if not cases:
        mark_missing('receipts', 'no build/N5/heroes.json')
        return
    out_cases = {}
    for cid, c in cases.items():
        if str(c.get('type') or '') in EXCLUDE_TYPES:
            continue
        place = c.get('place') or {}
        events = []
        for e in c.get('timeline') or []:
            events.append({'date': str(e.get('date') or '')[:16], 'kind': event_kind(e), 'title': plain_in_text(scrub_text(str(e.get('event') or ''))),
                           'source': e.get('source'), 'label': e.get('label') or 'observed',
                           'derivation': scrub_text(e.get('derivation') or '')})
        out_cases[cid] = {'id': cid, 'role': c.get('role'), 'type': c.get('type'), 'type_label': plain_name(c.get('type')), 'ward': c.get('ward'),
                          'neighborhood': c.get('neighborhood'), 'block': block_label(place.get('block')),
                          'what': place.get('what'), 'story': plain_in_text(scrub_text(c.get('story') or '')),
                          'days_to_close': c.get('days_to_close'), 'promise_days': c.get('promise_days'),
                          'facts': strip_ids(c.get('facts') or {}), 'timeline': events, 'images': copy_images(c)}
    examples = []
    for ex in EXAMPLES:
        cs = [x for x in ex['cases'] if x in out_cases]
        if cs:
            examples.append({'key': ex['key'], 'label': ex['label'], 'cases': cs})
    notes = []
    skipped = [cid for cid, c in cases.items() if str(c.get('type') or '') in EXCLUDE_TYPES]
    if skipped:
        notes.append('not shown (single light out is not robust): ' + ', '.join(skipped))
    fp = B('build', 'N5', 'lot_funnel.json')
    funnel = load_json(fp)
    srcs = [src(hp)] + ([src(fp)] if funnel else [])
    write('receipts', {'examples': examples, 'cases': out_cases, 'lead_case': CONFIG['lead'].get('hero_id'),
                       'lot_funnel': strip_ids(funnel) if isinstance(funnel, dict) else None,
                       'lookup': {'endpoint': 'api/receipt/', 'note': 'Typed request numbers are looked up live by the local weekly-job server (scripts/night/N6/serve.py); the page ships no ids.'}},
          srcs, notes)


# ---------------------------------------------------------------- scoreboard
CITYSTAT_ORDER = ['pothole_residential', 'pothole_major', 'pothole_alley', 'debris_alley_street', 'debris_vacant_bldg',
                  'debris_vacant_lot', 'whole_block_lights', 'critical_sign', 'parks_all']
SETTLED = ['2024 Q1', '2024 Q2', '2024 Q3', '2024 Q4', '2025 Q1', '2025 Q2', '2025 Q3', '2025 Q4', '2026 Q1']


def build_scoreboard():
    p = B('build', 'out', 'scoreboard.json')
    d = load_json(p)
    if d and rows_of(d, 'rows') and 'q3' in d and 'citystat' in d:
        write('scoreboard', {k: v for k, v in d.items() if k != 'meta'}, [src(p)])
        return
    p = B('build', 'N4', 'scoreboard.json')
    d = load_json(p)
    rows = rows_of(d, 'rows')
    if not rows:
        mark_missing('scoreboard', 'no build/N4/scoreboard.json')
        return
    sources, notes = [src(p)], []
    figs = (load_json(os.path.join(SITE_DATA, 'figures.json')) or {}).get('figures', {})
    out = []
    for r in rows:
        if r.get('problemcode') in EXCLUDE_TYPES:
            continue
        out.append({'problemcode': r.get('problemcode'), 'name': r.get('name'), 'category': r.get('category'),
                    'requests': r.get('requests') or r.get('requests_2025_26'), 'promise_days': r.get('promise_days'),
                    'promise_applies': r.get('promise_applies', True),
                    'scored': r.get('scored'), 'kept_share': r.get('kept_share'), 'done_kept_share': r.get('done_kept_share'),
                    'late_share': r.get('late_share'), 'median_days_late': r.get('median_days_late'),
                    'open_past_promise': r.get('open_past_promise'), 'median_days_to_close': r.get('median_days_to_close'),
                    'cancelled_share': r.get('cancelled_share'),
                    'closed_done_share': r.get('closed_done_share'), 'closed_handed_off_share': r.get('closed_handed_off_share'),
                    'closed_no_action_share': r.get('closed_no_action_share'), 'citystat_metric': r.get('citystat_metric'),
                    'citystat_goal_days': r.get('citystat_goal_days'), 'derivation': r.get('derivation')})
    # CityStat rebuilt: per metric, Q2 published vs Q2 in today's file vs Q3 (ours), and the quarterly series
    qp, cp = B('build', 'N4', 'q3_2026.json'), B('build', 'N4', 'citystat_comparison.csv')
    qd = load_json(qp) or {}
    comp = []
    if os.path.exists(cp):
        with open(cp, newline='') as f:
            comp = list(csv.DictReader(f))
        sources.append(src(cp))
    if qd:
        sources.append(src(qp))
    metrics, n_exact, exact_list = [], 0, []
    for key in CITYSTAT_ORDER + [k for k in qd if k not in CITYSTAT_ORDER and isinstance(qd.get(k), dict)]:
        m = qd.get(key) if isinstance(qd.get(key), dict) else {}
        series = [{'quarter': r['quarter'], 'ours_share': num(r['ours_share']), 'ours_n': num(r['ours_n']),
                   'citystat_share': num(r['citystat_share']), 'citystat_n': num(r['citystat_n'])}
                  for r in comp if r['metric'] == key and r['definition'] == 'B']
        series.sort(key=lambda x: x['quarter'])
        crow = [r for r in comp if r['metric'] == key and r['definition'] == 'C' and r['quarter'] in SETTLED and num(r['citystat_n'])]
        rel = [abs(num(r['ours_n']) - num(r['citystat_n'])) / num(r['citystat_n']) for r in crow]
        mean_rel = sum(rel) / len(rel) if rel else None
        if mean_rel is not None and round(mean_rel * 100, 1) <= 0.2:
            n_exact += 1
            exact_list.append(key)
        fq2, fq3, fmae = figs.get(f'n4_q2_2026_{key}_ours'), figs.get(f'n4_q3_2026_{key}'), figs.get(f'n4_repro_mae_{key}')
        cs = m.get('citystat_q2_2026') or {}
        best = m.get('B_best') or {}
        metrics.append({'metric': key, 'label': m.get('label') or key, 'goal_days': m.get('goal_days'),
                        'citystat_q2_share': cs.get('share'), 'citystat_q2_n': cs.get('n'),
                        'q2_ours_share': (fq2['value'] / 100) if fq2 and num(fq2.get('value')) is not None else None,
                        'q2_ours_figure': fq2 and fq2['id'],
                        'q3_share': (fq3['value'] / 100) if fq3 and num(fq3.get('value')) is not None else best.get('share'),
                        'q3_n': best.get('n'), 'q3_figure': fq3 and fq3['id'],
                        'q3_floor_share': (m.get('B_if_open_close_late') or m.get('C_if_open_close_late') or {}).get('share'),
                        'mean_gap_pp': fmae.get('value') if fmae else None, 'mae_figure': fmae and fmae['id'],
                        'count_mean_rel_err': round(mean_rel, 4) if mean_rel is not None else None,
                        'series': series, 'note': m.get('label_note') or 'our definition, from the public file'})
    citystat = {'metrics': metrics, 'n_metrics': len([m for m in metrics if m['series']]),
                'n_counts_exact': n_exact, 'counts_exact_metrics': exact_list,
                'counts_rule': 'mean absolute difference between our request count and CityStat\'s, 2024 Q1 to 2026 Q1, within 0.2% (rounded to a tenth of a percent)',
                'counts_derivation': ("Computed by N6 from N4's quarter-by-quarter table (build/N4/citystat_comparison.csv): for each of CityStat's nine "
                                      "311-based on-time measures, our request count under definition C (one row per request number, closed requests, "
                                      "by quarter filed) against the count in CityStat's own chart tables (Tableau summary data extracted 13 Oct 2026), "
                                      "averaged over the nine settled quarters 2024 Q1 to 2026 Q1."),
                'within5_figure': 'n4_repro_metrics_within5pp_C',
                'lead_metric': 'pothole_residential',
                'lead_line': 'A weekly run would have shown this in July.',
                'lead_median_figures': ['n4_pothole_residential_median_days_2026q2', 'n4_pothole_residential_median_days_2026q3']}
    meta = (d or {}).get('meta') or {}
    write('scoreboard', {'window': meta.get('window'), 'definition': {'scored': meta.get('scored_definition'),
                         'kept': meta.get('kept'), 'done_kept': meta.get('done_kept')},
                         'summary_figures': ['n4_sb_kept_all', 'n4_sb_done_kept_all'],
                         'rows': out, 'citystat': citystat},
          sources, notes, 'real' if metrics else 'partial')


# ---------------------------------------------------------------- fairness
def build_fairness():
    """N3's settled reading: the gap is the same type, same closing words, later,
    and it sits in the first step. Single light out is not robust and is never shown."""
    fc = CONFIG['fairness']
    p = B('build', 'out', 'fairness.json')
    d = load_json(p)
    if d and d.get('lead') is not None and d.get('decompositions') is not None:
        write('fairness', {k: v for k, v in d.items() if k != 'meta'}, [src(p)])
        return
    sources, notes = [], []
    decs = []
    dp = B('build', 'N3', 'decomposition.json')
    dd = load_json(dp)
    if isinstance(dd, dict):
        sources.append(src(dp))
        for key, v in dd.items():
            if not isinstance(v, dict) or 'gap' not in v:
                continue
            a_lbl, b_lbl = ('Ward 1', 'Ward 10') if 'ward 1 vs ward 10' in key else ('Wards 1–5', 'Wards 10–14')
            sbc = v.get('speed_by_class') or {}
            other = sum(float(x) for k, x in sbc.items() if k not in ('done', 'handed_off'))
            comps = [
                {'key': 'type_mix', 'group': 'mix', 'label': 'Mix of request types', 'days': round(float(v['type_mix']), 2)},
                {'key': 'closing_practice', 'group': 'mix', 'label': 'Closing words used', 'days': round(float(v['closing_practice']), 2)},
                {'key': 'speed_done', 'group': 'speed', 'label': 'Same type, same words: closings that record finished work', 'days': round(float(sbc.get('done', v.get('speed_done', 0))), 2)},
                {'key': 'speed_handoff', 'group': 'speed', 'label': 'Same type, same words: hand-offs (referral, tag, notice)', 'days': round(float(sbc.get('handed_off', 0)), 2)},
                {'key': 'speed_other', 'group': 'speed', 'label': 'Same type, same words: no action, blank, other', 'days': round(other, 2)},
            ]
            gap = float(v['B_mean']) - float(v['A_mean'])
            for c in comps:
                c['share'] = round(c['days'] / gap, 3) if gap else None
            if abs(sum(c['days'] for c in comps) - gap) > 0.1:
                notes.append(f'{key}: components do not sum to the gap')
            decs.append({'key': key, 'a_label': a_lbl, 'b_label': b_lbl,
                         'a_mean': round(float(v['A_mean']), 2), 'b_mean': round(float(v['B_mean']), 2),
                         'gap': round(gap, 2), 'n_a': v.get('n_A'), 'n_b': v.get('n_B'), 'components': comps,
                         'speed_share': round(sum(c['days'] for c in comps if c['group'] == 'speed') / gap, 3) if gap else None,
                         'mix_share': round(sum(c['days'] for c in comps if c['group'] == 'mix') / gap, 3) if gap else None})
    cp = B('build', 'N3', 'robust_comparisons.csv')
    rows = []
    if os.path.exists(cp):
        sources.append(src(cp))
        with open(cp, newline='') as f:
            rows = list(csv.DictReader(f))
    promise = {}
    sb = load_json(B('build', 'N4', 'scoreboard.json'))
    for r in rows_of(sb, 'rows') or []:
        promise[r.get('problemcode')] = r.get('promise_days')

    def pick(t, measure, period='after'):
        return next((r for r in rows if r['ptype'] == t and r['measure'] == measure and r['period'] == period), None)

    lead = []
    for want in fc.get('lead', []):
        if want['type'] == 'Single Light Out':
            continue
        hit, before = pick(want['type'], want['measure']), pick(want['type'], want['measure'], 'before')
        if not hit:
            notes.append(f"lead comparison not found: {want['type']} / {want['measure']}")
            continue
        lead.append({'type': want['type'], 'title': want.get('title'), 'words': want.get('words'), 'step': want.get('step'),
                     'figure_id': want.get('figure_id'), 'period': 'resident requests filed since 16 May 2025',
                     'a_label': 'Wards 1–5', 'b_label': 'Wards 10–14',
                     'a_median': num(hit['med_south']), 'b_median': num(hit['med_north']),
                     'n_a': int(float(hit['n_south'])), 'n_b': int(float(hit['n_north'])),
                     'ratio': num(hit.get('ratio')), 'ci_lo': num(hit.get('ci_lo')), 'ci_hi': num(hit.get('ci_hi')),
                     'before': {'a_median': num(before['med_south']), 'b_median': num(before['med_north'])} if before else None,
                     'promise_days': promise.get(want['type'])})
    no_gap = []
    for want in fc.get('no_gap', []):
        hit = pick(want['type'], 'done-class')
        if not hit:
            notes.append(f"no-gap row not found: {want['type']}")
            continue
        bef = pick(want['type'], 'done-class', 'before')
        no_gap.append({'before': {'a_median': num(bef['med_south']), 'b_median': num(bef['med_north']), 'n_a': int(float(bef['n_south'])),
                                  'n_b': int(float(bef['n_north'])), 'ratio': num(bef.get('ratio'))} if bef else None,
                       'type': want['type'], 'title': want.get('title'), 'a_median': num(hit['med_south']),
                       'b_median': num(hit['med_north']), 'n_a': int(float(hit['n_south'])), 'n_b': int(float(hit['n_north'])),
                       'ratio': num(hit.get('ratio')), 'promise_days': promise.get(want['type'])})
    if not decs and not lead:
        mark_missing('fairness', 'no N3 outputs')
        return
    key = fc.get('decomposition_key')
    decs.sort(key=lambda x: x['key'] != key)
    write('fairness', {'headline': fc.get('headline'), 'sub': fc.get('sub'), 'citystat': fc['citystat'],
                       'decomposition_key': key, 'decomposition_figure': fc.get('decomposition_figure'),
                       'reproduction_figures': fc.get('reproduction_figures'), 'no_gap_figure': fc.get('no_gap_figure'),
                       'decompositions': decs, 'lead': lead, 'no_gap': no_gap},
          sources + [{'path': 'site/config.json (CityStat ward figures, reported)', 'mtime': None}],
          notes, 'real' if decs and lead else 'partial')


# ---------------------------------------------------------------- register
def tri(text, yes=('yes',), partial=('partial', 'sometimes'), no=('no', 'rarely')):
    t = (text or '').strip().lower()
    if not t or t.startswith('n/a'):
        return 'na'
    if 'consistency check only' in t or t.startswith('not '):
        return 'partial'
    for w in yes:
        if t.startswith(w):
            return 'yes'
    for w in partial:
        if t.startswith(w):
            return 'partial'
    for w in no:
        if t.startswith(w):
            return 'no'
    if t.startswith('mostly'):
        return 'yes'
    if t.startswith('on '):
        return 'partial'
    return 'partial'


def paren(text):
    m = re.search(r'\((.*)\)', text or '')
    return m.group(1) if m else ''


ATTACH_COL = {'key': 'attached', 'label': 'Work orders attached (public status page)',
              'help': "Whether the City's public status page lists inspections or work orders attached to the request (E1's sample of status pages)."}


def attach_cells(rows):
    """E3: the register's sixth column, read from E1's linkage table when it exists; otherwise 'not yet tested'."""
    # E1's service table counts work orders separately from inspections; the older linkage table counts any item.
    path = first(B('build', 'E1', 'service_table.csv'), B('build', 'E1', 'linkage_by_service.csv'))
    strata = []
    if path:
        with open(path, newline='', encoding='utf-8') as f:
            strata = list(csv.DictReader(f))
    wo_counts = path and path.endswith('service_table.csv')
    by_code = {}
    for st in strata:
        if wo_counts:
            code, phrase = (st.get('service') or '').strip(), (st.get('closing_words') or '').strip()
        else:
            code = (st.get('service') or '').split(' | ')[0].strip()
            phrase = (st.get('service') or '').split(' | ', 1)[1].strip() if ' | ' in (st.get('service') or '') else ''
        try:
            n = int(float(st.get('n') or 0))
            k = int(float((st.get('work_order') if wo_counts else st.get('n_with_item')) or 0))
        except ValueError:
            continue
        by_code.setdefault(code, []).append((f'{code}: {phrase}' if phrase else code, n, k))
    for r in rows:
        hits = [x for c in (r.get('problemcodes') or []) for x in by_code.get(c, [])]
        if not hits:
            r.setdefault('cells', {})['attached'] = {'state': 'untested', 'text': 'Not yet tested: no status pages of this service in the sample' if strata else 'Not yet tested'}
            continue
        n = sum(x[1] for x in hits)
        k = sum(x[2] for x in hits)
        state_ = 'yes' if k / n >= 0.8 else ('partial' if k / n >= 0.2 else 'no')  # 'no' covers 'rarely' (count in the text)
        parts = '; '.join(f'"{ph}": {kk} of {nn}' for ph, nn, kk in hits)
        what = 'an attached work order' if wo_counts else 'attached items (inspections or work orders)'
        r.setdefault('cells', {})['attached'] = {'state': state_, 'text': f'{k} of {n} sampled status pages list {what} ({parts}). Source: E1, {rel(path)}.'}
    return rel(path) if path else None


def build_register():
    p = first(B('build', 'out', 'register.json'), B('build', 'N2', 'register.json'))
    d = load_json(p) if p else None
    rows = rows_of(d, 'rows')
    if not rows:
        mark_missing('register', 'no register file')
        return
    if rows and isinstance(rows[0].get('cells'), dict):
        e1 = attach_cells(rows)
        payload = {k: v for k, v in d.items() if k != 'meta'}
        payload['columns'] = list(payload.get('columns') or []) + [ATTACH_COL]
        write('register', payload, [src(p)] + ([src(B(e1))] if e1 else []), [] if e1 else ['E1 linkage table not found: attached column reads "not yet tested"'])
        return
    cols = [{'key': 'intake', 'label': 'Request recorded', 'help': 'The 311 file records the request.'},
            {'key': 'promise', 'label': 'Promise date', 'help': 'The city sets a promised completion date (PRJCOMPLETEDATE) on the request.'},
            {'key': 'says_done', 'label': 'Closing words say done', 'help': 'Share of closures whose words record finished work: mostly (50% or more), sometimes (15–49%), rarely (under 15%).'},
            {'key': 'record', 'label': 'Independent record of the work', 'help': 'A city record of the work itself, outside the 311 request.'},
            {'key': 'joined', 'label': 'Joined here', 'help': 'This prototype joins the request to that record.'}]
    out = []
    for r in rows:
        sd = num(r.get('share_closed_done'))
        says = r.get('closure_says_done') or ''
        rec = r.get('independent_completion_record') or ''
        joined = r.get('joined') or ''
        out.append({'id': r.get('id'), 'service': r.get('service'), 'problemcodes': r.get('problemcodes'),
                    'cells': {
                        'intake': {'state': tri(r.get('intake_recorded')), 'text': r.get('intake_recorded')},
                        'promise': {'state': tri(r.get('promise_date')), 'text': r.get('promise_date')},
                        'says_done': {'state': {'mostly': 'yes', 'sometimes': 'partial', 'rarely': 'no'}.get(says.lower(), tri(says)),
                                      'text': (f'{says}: {sd * 100:.0f}% of closures' if sd is not None else says)},
                        'record': {'state': tri(rec), 'text': rec},
                        'joined': {'state': tri(joined), 'text': joined},
                    },
                    'filed': r.get('filed_2025_26'), 'share_closed_done': sd,
                    'share_closed_handoff': num(r.get('share_closed_handoff_or_converted')),
                    'top_closing_text': r.get('top_closing_text'),
                    'record_source': r.get('completion_record_source'), 'what_it_would_take': r.get('what_it_would_take')})
    meta = (d or {}).get('meta') or {}
    e1 = attach_cells(out)
    write('register', {'scope': meta.get('scope'), 'columns': cols + [ATTACH_COL], 'rows': out}, [src(p)] + ([src(B(e1))] if e1 else []),
          [] if e1 else ['E1 linkage table not found: attached column reads "not yet tested"'])


# ---------------------------------------------------------------- monday list + mowing
def write_csv(path, rows, cols):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([scrub_text(r.get(c)) if isinstance(r.get(c), str) else r.get(c) for c in cols])


def build_monday():
    sources, notes = [], []
    p = B('build', 'out', 'monday_list.json')
    d = load_json(p)
    rows = rows_of(d, 'rows', 'rows_filed_last_365_days', 'requests')
    summary = rows_of(d, 'summary') if d else None
    total = (d or {}).get('n_total')
    from_db = False
    if rows:
        sources.append(src(p))
        if 'rows_filed_last_365_days' in (d or {}):
            notes.append('page rows: requests filed in the last 365 days (N1 export); counts by ward and type: all years')
    else:
        rows = q("""SELECT request_id, problem_code, type_name, division, ward, block_label, filed, promised,
                           days_past_promise, age_days, status, channel_group FROM monday_list""")
        from_db = bool(rows)
        if rows:
            sources.append({'path': 'build/stl.duckdb (view monday_list)', 'mtime': src(B('build', 'stl.duckdb'))['mtime']})
            notes.append('build/out/monday_list.json not yet exported; read from N1 view monday_list')
    if not rows:
        mark_missing('monday', 'no monday list export or view')
        return
    clean = []
    for r in rows:
        if r.get('problem_code') in EXCLUDE_TYPES and False:
            continue
        clean.append({'type_name': plain_name(r.get('problem_code')) if r.get('problem_code') else _tidy_plain(r.get('type_name')), 'problem_code': r.get('problem_code'),
                      'type_long': r.get('type_name'), 'division': r.get('division'),
                      'ward': (f"{int(r['ward']):02d}" if str(r.get('ward') or '').isdigit() else r.get('ward')),
                      'block': block_label(r.get('block_label') or r.get('block')),
                      'filed': iso(r.get('filed'), False), 'promised': iso(r.get('promised'), False),
                      'days_past_promise': r.get('days_past_promise'), 'age_days': r.get('age_days'), 'status': r.get('status')})
    clean.sort(key=lambda r: -(r['days_past_promise'] or 0))
    by_ward, by_type, by_div = {}, {}, {}
    if summary:
        for srow in summary:
            n = srow.get('n_open_past_promise') or 0
            w = f"{int(srow['ward']):02d}" if str(srow.get('ward') or '').isdigit() else srow.get('ward')
            by_ward[w] = by_ward.get(w, 0) + n
            tn = plain_name(srow.get('problem_code'))
            by_type[tn] = by_type.get(tn, 0) + n
            by_div[srow.get('division')] = by_div.get(srow.get('division'), 0) + n
        total = total or sum(by_ward.values())
    else:
        for r in clean:
            by_ward[r['ward']] = by_ward.get(r['ward'], 0) + 1
            by_type[r['type_name']] = by_type.get(r['type_name'], 0) + 1
            by_div[r['division']] = by_div.get(r['division'], 0) + 1
        total = len(clean)
    # The full CSV: N1's export when present (every row, all years), else ours from the rows we have.
    n1_csv = B('build', 'out', 'monday_list.csv')
    if os.path.exists(n1_csv):
        with open(n1_csv, newline='', encoding='utf-8', errors='replace') as f:
            rd = list(csv.reader(f))
        hdr = rd[0] if rd else []
        banned = {'addr_norm', 'addr_raw', 'probaddress', 'parcel', 'parcel_id', 'pid', 'lat', 'lon', 'srx', 'sry', 'handle',
                  'request_id', 'next_same_request_id', 'workorder_id', 'requestid'}
        keep_idx = [i for i, h in enumerate(hdr) if h.lower() not in banned]
        with open(os.path.join(DL, 'monday_list.csv'), 'w', newline='') as f:
            w = csv.writer(f)
            for r in rd:
                w.writerow([scrub_text(r[i]) if i < len(r) else '' for i in keep_idx])
        sources.append(src(n1_csv))
    else:
        write_csv(os.path.join(DL, 'monday_list.csv'), clean,
                  ['type_name', 'division', 'ward', 'block', 'filed', 'promised', 'days_past_promise', 'age_days', 'status'])
    asof = (d or {}).get('run', {}).get('asof') if isinstance((d or {}).get('run'), dict) else None
    if not asof:
        run = load_json(os.path.join(SITE_DATA, 'run.json'))
        asof = run.get('asof') if run else None
    mowing = build_mowing(d)
    recent = [r for r in clean if (r['days_past_promise'] or 0) <= 90]
    keep = clean[:300] + [r for r in recent if r not in clean[:300]][:2700]
    write('monday', {'asof': asof,
                     'definition': (d or {}).get('definition') or "Open requests whose promised date, set by the city on the request, has passed. Block level; sensitive request types excluded.",
                     'total': total, 'rows_scope': 'filed in the last 365 days' if d and 'rows_filed_last_365_days' in d else 'all',
                     'rows_total': len(clean), 'past_90_or_less': len(recent),
                     'by_ward': sorted([{'ward': k, 'n': v} for k, v in by_ward.items() if k], key=lambda x: x['ward']),
                     'by_type': sorted([{'type': k, 'n': v} for k, v in by_type.items() if k], key=lambda x: -x['n']),
                     'by_division': sorted([{'division': k, 'n': v} for k, v in by_div.items() if k], key=lambda x: -x['n']),
                     'rows': keep, 'csv': 'data/downloads/monday_list.csv', 'mowing': mowing},
          sources, notes, 'partial' if from_db else 'real')


def build_mowing(monday_doc=None):
    mp = load_json(B('build', 'out', 'mowing_2026.json'))
    if isinstance(mp, dict) and rows_of(mp, 'rows'):
        return {'season': '2026', 'title': '2026 season, retrospective', 'definition': mp.get('definition'), 'threshold_days': 90,
                'rows': [{'ward': r.get('ward'), 'parcels_on_rotation': r.get('parcels_on_rotation'),
                          'parcels_gap_over_threshold': r.get('parcels_gap_over_90d'), 'lra_gap_over_threshold': r.get('lra_parcels_gap_over_90d'),
                          'lots_cut_once': r.get('parcels_cut_once'), 'median_longest_gap': r.get('median_longest_gap')}
                         for r in mp['rows'] if r.get('ward')],
                'blocks': [{k: v for k, v in b.items()} for b in (mp.get('blocks_top_300') or [])[:300]]}
    m = (monday_doc or {}).get('mowing_2026_retrospective') if isinstance(monday_doc, dict) else None
    if isinstance(m, dict) and rows_of(m, 'by_ward', 'rows'):
        rows = rows_of(m, 'by_ward', 'rows')
        return {'season': '2026', 'title': '2026 season, retrospective', 'definition': m.get('definition'),
                'threshold_days': 90,
                'rows': [{'ward': r.get('ward'), 'parcels_on_rotation': r.get('rotation_lots_2026'),
                          'parcels_gap_over_threshold': r.get('lots_with_gap_over_90_days'),
                          'lra_gap_over_threshold': r.get('lra_lots_with_gap_over_90_days'),
                          'lots_cut_once': r.get('lots_cut_once'),
                          'median_longest_gap': r.get('median_longest_gap_days')} for r in rows if r.get('ward')],
                'totals': {k: v for k, v in m.items() if k not in ('by_ward', 'rows', 'definition', 'top_lots', 'lots')
                           and not isinstance(v, (list, dict))}}
    return None


# ---------------------------------------------------------------- dumping
def build_dumping():
    sources, notes = [], []
    p = first(B('build', 'out', 'dumping_blocks.json'), B('build', 'out', 'dumping_sites.json')) or B('build', 'out', 'dumping_blocks.json')
    d = load_json(p)
    rows = rows_of(d, 'blocks', 'rows')
    from_db = False
    if rows:
        sources.append(src(p))
    else:
        rows = q('SELECT * FROM dumping_blocks')
        from_db = bool(rows)
        if rows:
            sources.append({'path': 'build/stl.duckdb (view dumping_blocks)', 'mtime': src(B('build', 'stl.duckdb'))['mtime']})
            notes.append('build/out dumping export not found; read from N1 view dumping_blocks')
    if not rows:
        mark_missing('dumping', 'no dumping export or view')
        return
    blocks = []
    for r in rows:
        blocks.append({'block': block_label(r.get('block_label') or r.get('block')),
                       'ward': (f"{int(r['ward']):02d}" if str(r.get('ward') or '').isdigit() else r.get('ward')),
                       **{k: r.get(k) for k in ('n_requests', 'n_addresses', 'n_illegal_dumping_reports', 'n_debris_reports',
                                                'n_closed', 'n_open', 'n_closed_done', 'n_closed_handoff', 'n_closed_no_action')},
                       'first_report': iso(r.get('first_report'), False), 'last_report': iso(r.get('last_report'), False),
                       'median_days_to_close': round(float(r['median_days_to_close']), 1) if num(r.get('median_days_to_close')) is not None else None})
    blocks.sort(key=lambda b: -(b['n_requests'] or 0))
    d = d or {}
    sm = d.get('summary') if isinstance(d.get('summary'), dict) else {}
    total = sm.get('requests') or d.get('requests_total') or sum(b['n_requests'] or 0 for b in blocks)
    n_blocks = sm.get('blocks') or d.get('blocks_total') or len(blocks)
    rep = sm.get('repeat_blocks') or d.get('blocks_3plus') or len([b for b in blocks if (b['n_requests'] or 0) >= 3])
    rep_req = sm.get('requests_on_repeat_blocks') or d.get('requests_on_3plus_blocks') or sum(b['n_requests'] for b in blocks if (b['n_requests'] or 0) >= 3)
    d.setdefault('blocks_10plus', sm.get('blocks_10plus'))
    # outcomes: N1 gives (problem_code x class) counts; fold to classes
    outcome = {}
    for o in rows_of(d, 'outcomes') or []:
        outcome[o.get('closure_class')] = outcome.get(o.get('closure_class'), 0) + (o.get('n') or 0)
    by_code = {}
    for o in rows_of(d, 'outcomes') or []:
        by_code.setdefault(o.get('problem_code'), {})[o.get('closure_class')] = {'n': o.get('n'), 'median_days': o.get('median_days')}
    if not outcome:
        outcome = {'done': sum(b.get('n_closed_done') or 0 for b in blocks), 'handed_off': sum(b.get('n_closed_handoff') or 0 for b in blocks),
                   'no_action': sum(b.get('n_closed_no_action') or 0 for b in blocks)}
    by_ward = {}
    for b in blocks:
        by_ward[b['ward']] = by_ward.get(b['ward'], 0) + (b['n_requests'] or 0)
    write_csv(os.path.join(DL, 'dumping_blocks.csv'), blocks,
              ['block', 'ward', 'n_requests', 'n_addresses', 'n_illegal_dumping_reports', 'n_debris_reports', 'first_report',
               'last_report', 'n_closed', 'n_open', 'n_closed_done', 'n_closed_handoff', 'n_closed_no_action', 'median_days_to_close'])
    write('dumping', {'window': d.get('window'), 'definition': d.get('definition') or 'Illegal dumping reports and alley/street debris filed in the 365 days to the run date, by block.',
                      'summary': {'requests': total, 'blocks': n_blocks, 'repeat_blocks': rep, 'repeat_threshold': 3,
                                  'requests_on_repeat_blocks': rep_req, 'share_repeat': (rep_req / total) if total else None,
                                  'blocks_10plus': d.get('blocks_10plus')},
                      'outcomes': outcome, 'outcomes_by_code': by_code,
                      'repeat_blocks_by_ward': sorted([{'ward': k, 'n': v} for k, v in by_ward.items() if k], key=lambda x: x['ward']),
                      'blocks': blocks[:200], 'csv': 'data/downloads/dumping_blocks.csv'},
          sources, notes, 'partial' if from_db else 'real')


# ---------------------------------------------------------------- the Monday brief (for city staff)
N6_FIGS = {}


def fmt_int(v):
    try:
        return f'{int(round(float(v))):,}'
    except (TypeError, ValueError):
        return str(v)


def n6fig(fid, value, unit, period, definition, derivation, note='', retired=False):
    N6_FIGS[fid] = {'id': fid, 'value': value, 'unit': unit, 'period': period, 'definition': definition,
                    'label': 'observed', 'source_sql_or_script': 'scripts/night/N6/bridge.py (build_brief), over build/stl.duckdb (N1)',
                    'note': note, 'derivation': derivation, 'owner': 'N6'}
    if retired:  # kept in build/N6/figures.json and build/out/retired_figures.json for the record; never on the site
        N6_FIGS[fid]['retired'] = True
    return fid


def save_retired(figs):
    """Upsert retired figures into build/out/retired_figures.json (N1's export writes the rest)."""
    p = B('build', 'out', 'retired_figures.json')
    d = load_json(p) or {'about': 'Figures retired from public use: kept for the record, never read by the site.', 'figures': {}}
    d.setdefault('figures', {}).update({f['id']: f for f in figs})
    with open(p, 'w') as fh:
        json.dump(d, fh, indent=1, default=str, ensure_ascii=False)


SRC_311 = "311 requests (City of St. Louis open data, csb.zip yearly CSVs, invalid bytes dropped, one row per request number), as loaded by N1 into build/stl.duckdb"


def build_brief():
    if db() is None:
        mark_missing('brief', 'build/stl.duckdb not readable')
        return
    run = q('SELECT max(ts_init) AS asof FROM requests')
    asof = run[0]['asof'] if run else None
    if not asof:
        mark_missing('brief', 'no requests table')
        return
    asof_d = asof.date()
    wk_end = asof_d
    wk_a = wk_end - dt.timedelta(days=7)
    wk_b = wk_a - dt.timedelta(days=7)
    out = {'asof': iso(asof), 'week': {'this_from': iso(wk_a), 'this_to': iso(wk_end), 'last_from': iso(wk_b), 'last_to': iso(wk_a)},
           'meeting_source': {'text': "weekly cabinet data reviews since mid-November 2025, described by the mayor and the COO at CityStat's public launch",
                              'label': 'reported', 'url': 'https://www.youtube.com/watch?v=a1H60btjS2E', 'date': '2 Apr 2026'}}
    # 1. promise-date compliance by service: due this week vs due last week
    rows = q(f"""
        SELECT problem_code,
               count(*) FILTER (WHERE ts_promised >= TIMESTAMP '{wk_a}' AND ts_promised < TIMESTAMP '{wk_end}') AS n_a,
               avg(CAST(closed_by_promise AS INT)) FILTER (WHERE ts_promised >= TIMESTAMP '{wk_a}' AND ts_promised < TIMESTAMP '{wk_end}') AS kept_a,
               avg(CAST(done_by_promise AS INT)) FILTER (WHERE ts_promised >= TIMESTAMP '{wk_a}' AND ts_promised < TIMESTAMP '{wk_end}') AS done_a,
               count(*) FILTER (WHERE ts_promised >= TIMESTAMP '{wk_b}' AND ts_promised < TIMESTAMP '{wk_a}') AS n_b,
               avg(CAST(closed_by_promise AS INT)) FILTER (WHERE ts_promised >= TIMESTAMP '{wk_b}' AND ts_promised < TIMESTAMP '{wk_a}') AS kept_b,
               median(promise_days) AS promise_days
        FROM promise
        WHERE status_group <> 'cancelled' AND has_promise
          AND problem_code NOT IN (SELECT problem_code FROM sensitive_codes)
        GROUP BY problem_code
        HAVING count(*) FILTER (WHERE ts_promised >= TIMESTAMP '{wk_a}' AND ts_promised < TIMESTAMP '{wk_end}') >= 20
           AND count(*) FILTER (WHERE ts_promised >= TIMESTAMP '{wk_b}' AND ts_promised < TIMESTAMP '{wk_a}') >= 20
    """) or []
    comp = []
    sbp = {x.get('problemcode'): x.get('promise_days') for x in (rows_of(load_json(B('build', 'N4', 'scoreboard.json')), 'rows') or [])}
    for r in rows:
        if r['problem_code'] in EXCLUDE_TYPES:
            continue
        comp.append({'service': plain_name(r['problem_code']), 'problem_code': r['problem_code'], 'promise_days': sbp.get(r['problem_code']) or r['promise_days'], 'n_this': r['n_a'], 'kept_this': r['kept_a'],
                     'done_this': r['done_a'], 'n_last': r['n_b'], 'kept_last': r['kept_b'],
                     'change_pts': round((r['kept_a'] - r['kept_b']) * 100, 1) if r['kept_a'] is not None and r['kept_b'] is not None else None})
    comp.sort(key=lambda x: (x['change_pts'] if x['change_pts'] is not None else 0))
    out['compliance'] = {'rows': comp, 'definition': ("Requests whose promised date (PRJCOMPLETEDATE, set by the city on each request) fell in the week; "
                                                       "share closed on or before that date. Cancelled requests excluded; services with at least 20 requests due in each week."),
                         'figure_id': n6fig('n6_brief_compliance_window', len(comp), 'services compared',
                                            f'promised dates {wk_b} to {wk_end}', 'Services with at least 20 requests due in each of the two weeks.',
                                            SRC_311 + "; each request graded against its own promised date (N1 view promise), this week's due requests against last week's; cancelled requests left out.")}
    # 1b. what it would have flagged in July: residential potholes by week filed, 2026
    wk = q("""
        SELECT date_trunc('week', ts_init) AS week, count(*) AS n_closed,
               avg(CAST(days_to_close <= 8 AS INT)) AS within_goal,
               median(days_to_close) AS median_days
        FROM promise
        WHERE problem_code = 'Potholes - Residnl' AND status_group = 'closed'
          AND ts_init >= TIMESTAMP '2026-04-06' AND ts_init < TIMESTAMP '2026-10-05'
        GROUP BY 1 ORDER BY 1""") or []
    series = [{'week': iso(r['week'], False), 'n': r['n_closed'], 'within_goal': r['within_goal'],
               'median_days': round(float(r['median_days']), 1) if r['median_days'] is not None else None} for r in wk]
    first_bad = next((s_ for s_ in series if s_['n'] >= 15 and s_['within_goal'] is not None and s_['within_goal'] < 0.5), None)
    out['pothole_weekly'] = {'series': series, 'goal_days': 8, 'first_week_below_half': first_bad and first_bad['week'],
                             'figure_id': n6fig('n6_brief_pothole_first_week_below_half', first_bad and first_bad['week'], 'week (Monday)',
                                                'residential pothole requests filed 6 Apr to 4 Oct 2026, closed by 13 Oct 2026',
                                                'First week of 2026 in which fewer than half of closed residential pothole requests (at least 15) were closed within CityStat\'s 8-day goal.',
                                                SRC_311 + "; residential pothole requests grouped by the week filed; share of closed requests closed within 8 days of filing (CityStat's goal and definition C, which N4 found reproduces CityStat's counts); weeks with fewer than 15 closed requests not used. Recent weeks still have open requests, so their shares can only fall."),
                             'definition': "Residential pothole requests by week filed: share of those closed that closed within 8 days (CityStat's goal; N4's definition C). Open requests are not counted, as CityStat does not count them."}
    # 2. first-step waits by ward
    fw = q("""
        SELECT lpad(trim(ward_raw), 2, '0') AS ward, problem_code, count(*) AS n, median(days_to_close) AS med
        FROM requests
        WHERE channel_group = 'resident' AND ts_init >= TIMESTAMP '2025-05-16' AND status_group = 'closed'
          AND ward_raw IS NOT NULL AND trim(ward_raw) <> '' AND regexp_full_match(trim(ward_raw), '[0-9]{1,2}')
          AND ((problem_code = 'Vehicle Towing' AND resolution = 'vehicle tagged for tow')
            OR (problem_code = 'Cave-Ins' AND resolution ILIKE 'referred to street maintenance%'))
        GROUP BY 1, 2 ORDER BY 1, 2""") or []
    wards = {}
    for r in fw:
        w = f"{int(str(r['ward']).strip()):02d}" if str(r['ward']).strip().isdigit() else r['ward']
        k = 'towing_tag' if r['problem_code'] == 'Vehicle Towing' else 'cavein_referral'
        wards.setdefault(w, {'ward': w})[k] = {'n': r['n'], 'median_days': round(float(r['med']), 1)}
    out['first_step'] = {'wards': [wards[k] for k in sorted(wards)],
                         'definition': "Resident-filed requests since 16 May 2025, one row per request number, closed with the same words: towing 'vehicle tagged for tow' (the inspector's first visit) and cave-ins 'referred to street maintenance for repair work to be scheduled' (the referral). Median days from filing to that closing, by ward as published in the file's WARD column (requests with a blank ward are left out, as in N3).",
                         'figure_id': n6fig('n6_brief_first_step_by_ward', len(wards), 'wards',
                                            'resident requests filed 16 May 2025 to 13 Oct 2026',
                                            'Median days to the first-step closing, by ward, for towing tags and cave-in referrals.',
                                            SRC_311 + "; resident channels only; ward from the published WARD column, blank wards left out, so a city analyst can reproduce it from the CSV without GIS; only closures with the same closing words, so the comparison is like for like (N3's method, recomputed by ward)."),
                         'n3_figures': ['n3_towing_tagged_median_after', 'n3_cavein_referral_median_after']}
    # 3a. LRA lots closed "on schedule" / "added to rotation" with no cut billed after the request (2026), resident-filed.
    # Headline count is N5's (94 requests on 75 lots, registered funnel); the block rows come from N1's join.
    la = q("""
        SELECT r.public_address AS block, r.ward, count(*) AS requests, count(DISTINCT q.addr_norm) AS lots,
               min(r.filed) AS first_filed, max(r.filed) AS last_filed, max(r.promised) AS last_promised
        FROM receipt_base r JOIN requests q USING (request_id)
        WHERE r.problem_code = 'Weeds-Vacant Lot' AND r.is_lra AND r.channel_group = 'resident'
          AND (r.closed_with_words ILIKE 'on schedule%' OR r.closed_with_words ILIKE '%added to rotation%')
          AND r.filed >= TIMESTAMP '2026-01-01' AND r.days_to_close <= 3 AND r.ledger_first_cut_after IS NULL
          AND r.public_address IS NOT NULL
        GROUP BY 1, 2 ORDER BY lots DESC, requests DESC, first_filed""") or []
    lots = [{'block': block_label(r['block']), 'ward': r['ward'], 'requests': r['requests'], 'lots': r['lots'],
             'first_filed': iso(r['first_filed'], False), 'last_filed': iso(r['last_filed'], False),
             'last_promised': iso(r['last_promised'], False)} for r in la]
    figs_all = (load_json(os.path.join(SITE_DATA, 'figures.json')) or {}).get('figures', {})
    f94, f75 = figs_all.get('n5_funnel_no_cut_requests'), figs_all.get('n5_funnel_no_cut_lots')
    lra_head = (f"{fmt_int(f94['value'])} requests on {fmt_int(f75['value'])} lots" if f94 and f75
                else f"{sum(x['requests'] for x in lots)} requests on {sum(x['lots'] for x in lots)} lots")
    # 3b. cave-ins referred, no completion record (the file never records the repair of a referred cave-in)
    cv = q(f"""
        SELECT public_address AS block, ward, count(*) AS referrals, min(closed) AS first_referred, max(closed) AS last_referred,
               max(date_diff('day', CAST(closed AS DATE), DATE '{asof_d}')) AS oldest_days
        FROM receipt_base
        WHERE problem_code = 'Cave-Ins' AND closed_with_words ILIKE 'referred to street maintenance%'
          AND closed >= TIMESTAMP '{asof_d - dt.timedelta(days=90)}' AND public_address IS NOT NULL
        GROUP BY 1, 2 ORDER BY oldest_days DESC, referrals DESC""") or []
    caves = [{'block': block_label(r['block']), 'ward': r['ward'], 'referrals': r['referrals'],
              'first_referred': iso(r['first_referred'], False), 'last_referred': iso(r['last_referred'], False),
              'days_since_first': r['oldest_days']} for r in cv]
    # 3c. tree requests cancelled with no words at the SAME ADDRESS as a removal order started more than a day before
    # (within-30 m reaches neighbours; the headline uses N5's 288, median 575 days)
    tr = q("""
        WITH m AS (
          SELECT r.request_id, r.public_address, r.ward, r.filed,
                 max(date_diff('day', w.proj_start, r.filed)) AS order_open_days
          FROM receipt_base r JOIN request_wo w USING (request_id)
          WHERE r.problem_code = 'Inspect City Tree' AND r.status_group = 'cancelled'
            AND coalesce(trim(r.closed_with_words), '') = '' AND w.addr_match AND w.source = 'tree_removal'
            AND w.proj_start < r.filed - INTERVAL 1 DAY AND r.filed >= TIMESTAMP '2025-01-01'
          GROUP BY 1, 2, 3, 4)
        SELECT public_address AS block, ward, count(*) AS cancelled_requests, max(order_open_days) AS order_open_days,
               max(filed) AS last_filed
        FROM m WHERE public_address IS NOT NULL GROUP BY 1, 2 ORDER BY order_open_days DESC""") or []
    trees = [{'block': block_label(r['block']), 'ward': r['ward'], 'cancelled_requests': r['cancelled_requests'],
              'order_open_days': r['order_open_days'], 'last_filed': iso(r['last_filed'], False)} for r in tr]
    f288, f575 = figs_all.get('n5_tree_cancel_blank_wo_predates'), figs_all.get('n5_tree_predating_wo_median_age_days')
    tree_head = (f"{fmt_int(f288['value'])} cancelled requests; the removal order had been open a median {fmt_int(f575['value'])} days"
                 if f288 and f575 else f"{sum(t['cancelled_requests'] for t in trees)} cancelled requests")
    lists = [
        {'key': 'lra_lots', 'title': 'City-owned lots closed "on schedule" with no cut billed since',
         'scope': 'Resident weed requests on land-bank (LRA) lots filed in 2026, closed within three days as "on schedule to be cut" or "added to rotation", with no grass cut billed on the parcel in the Forestry ledger after the request (ledger posted to the run date). Requests filed after mid-September have had little time.',
         'owner': 'Forestry', 'rows': lots, 'columns': ['block', 'ward', 'lots', 'requests', 'first_filed', 'last_filed'],
         'summary': lra_head, 'summary_note': f'{len(lots)} blocks in the list below (the pipeline\'s parcel join; it finds {sum(x["requests"] for x in lots)} requests on {sum(x["lots"] for x in lots)} lots)',
         'figure_id': ['n5_funnel_no_cut_requests', 'n5_funnel_no_cut_lots'] if f94 else None,
         'csv': 'data/downloads/brief_lra_lots.csv'},
        {'key': 'cavein_referred', 'title': 'Cave-ins referred to Street Maintenance in the last 90 days: no completion record',
         'scope': 'Cave-in requests closed "referred to street maintenance for repair work to be scheduled" in the 90 days to the run date. No public file records when a referred cave-in is repaired, so every row is open as far as the record goes.',
         'owner': 'Street Department', 'rows': caves, 'columns': ['block', 'ward', 'referrals', 'first_referred', 'days_since_first'],
         'summary': f"{sum(c['referrals'] for c in caves)} referrals on {len(caves)} blocks",
         'figure_id': n6fig('n6_brief_cavein_referrals_90d', sum(c['referrals'] for c in caves), 'requests', f'closed {asof_d - dt.timedelta(days=90)} to {asof_d}',
                            'Cave-in requests closed as referred to Street Maintenance in the last 90 days.',
                            SRC_311 + "; closing words matched exactly; the city publishes no repair date for these, so none can be joined."),
         'csv': 'data/downloads/brief_cavein_referred.csv'},
        {'key': 'tree_cancelled', 'title': 'Tree requests cancelled with no words at an address where a removal order was already open',
         'scope': "'Inspect City Tree' requests filed since 1 January 2025, cancelled with no public words, at the same address as a Forestry tree-removal work order that had started more than a day before (the city's published Cityworks sample: 1,500 of 2,522 open removal orders, so this undercounts).",
         'owner': 'Forestry', 'rows': trees, 'columns': ['block', 'ward', 'cancelled_requests', 'order_open_days', 'last_filed'],
         'summary': tree_head, 'summary_note': f'{len(trees)} blocks in the list below (exact-address match; {sum(t["cancelled_requests"] for t in trees)} requests)',
         'figure_id': ['n5_tree_cancel_blank_wo_predates', 'n5_tree_predating_wo_median_age_days'] if f288 else None,
         'csv': 'data/downloads/brief_tree_cancelled.csv'},
    ]
    # Retired 14 Oct 2026: the pipeline's own counts, kept for the record only.
    n6fig('n6_brief_lra_no_cut_requests', sum(x['requests'] for x in lots), 'requests', '2026 season to 13 Oct 2026',
          'Resident LRA-lot weed requests closed "on schedule" or "added to rotation" within 3 days with no cut billed after (N1\'s parcel join).',
          SRC_311 + ", joined by N1 to parcels and to the Forestry billing ledger; land-bank ownership from the LRA inventory.",
          note=("Retired for public use 14 Oct 2026: N1's wider parcel join; earlier runs counted all channels (103 on 82 lots). "
                "The brief and every public text use N5's registered resident-filed count, n5_funnel_no_cut_requests and n5_funnel_no_cut_lots (94 on 75)."),
          retired=True)
    n6fig('n6_brief_tree_cancelled_open_order', sum(t['cancelled_requests'] for t in trees), 'requests', '1 Jan 2025 to 13 Oct 2026',
          'Inspect City Tree requests cancelled with no words at the same address as a removal order started more than a day before (N1\'s join).',
          SRC_311 + ", joined by N1 to the city's published Cityworks tree work-order saved searches by normalised address.",
          note=("Retired for public use 14 Oct 2026: an earlier version counted removal orders within 30 m (499) under an "
                "'at the address' definition. The brief and every public text use N5's exact-address count, n5_tree_cancel_blank_wo_predates "
                "(288, median 575 days)."),
          retired=True)
    for L in lists:
        write_csv(os.path.join(DL, os.path.basename(L['csv'])), L['rows'], L['columns'])
    out['lists'] = lists
    # all-years open-past-promise count from the Monday list, for the brief's last line
    md = load_json(os.path.join(SITE_DATA, 'monday.json'))
    if md:
        out['monday_total'] = md.get('total')
        out['monday_csv'] = md.get('csv')
    write('brief', out, [{'path': 'build/stl.duckdb (N1 views: promise, requests, receipt_base, request_wo_summary)',
                          'mtime': src(B('build', 'stl.duckdb'))['mtime']}],
          ['every figure here is registered in build/N6/figures.json with its derivation'])
    with open(B('build', 'N6', 'figures.json'), 'w') as f:
        json.dump(list(N6_FIGS.values()), f, indent=1, default=str)
    save_retired([v for v in N6_FIGS.values() if v.get('retired')])
    # fold N6 figures into the page's registry so "How we know" finds them (retired ones stay out)
    fpth = os.path.join(SITE_DATA, 'figures.json')
    fd = load_json(fpth)
    if fd:
        fd['figures'].update(scrub_obj({k: v for k, v in N6_FIGS.items() if not v.get('retired')}))
        with open(fpth, 'w') as f:
            json.dump(fd, f, indent=1, default=str, ensure_ascii=False)


# ---------------------------------------------------------------- negative results
def md_sections(text):
    """Split markdown into (heading, body) by ##/### headings."""
    out, cur, body = [], None, []
    for line in text.splitlines():
        m = re.match(r'^(#{2,4})\s+(.*)$', line)
        if m:
            if cur is not None:
                out.append((cur, '\n'.join(body).strip()))
            cur, body = m.group(2).strip(), []
        else:
            body.append(line)
    if cur is not None:
        out.append((cur, '\n'.join(body).strip()))
    return out


def md_items(body):
    """Numbered or bulleted items; continuation lines folded in."""
    items, cur = [], None
    for line in body.splitlines():
        m = re.match(r'^\s{0,3}(?:\d+[\.\)]|[-*])\s+(.*)$', line)
        if m:
            if cur:
                items.append(cur)
            cur = m.group(1).strip()
        elif cur is not None and line.strip():
            cur += ' ' + line.strip()
        elif cur is not None and not line.strip():
            items.append(cur)
            cur = None
    if cur:
        items.append(cur)
    return items


def strip_md(s):
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    s = re.sub(r'`([^`]+)`', r'\1', s)
    return s.replace('**', '').replace('__', '').strip()


def split_title(item):
    m = re.match(r'^\*\*(.+?)\*\*[\s:.—–-]*(.*)$', item)
    if m:
        return strip_md(m.group(1)).rstrip('.:'), strip_md(m.group(2))
    s = strip_md(item)
    m = re.match(r'^(.{12,140}?[.:])\s+(.*)$', s)
    return (m.group(1).rstrip('.:'), m.group(2)) if m else (s, '')


# Sentences that match a private word list stay off the site. The word list lives in a
# git-ignored file, build/N6/private/exposure_words.json (a JSON list of regular expressions), so that this builder can
# be published (E4 export scan, 14 Oct). Without the file the guard matches nothing.
def _exposure_words():
    try:
        with open(B('build', 'N6', 'private', 'exposure_words.json'), encoding='utf-8') as f:
            words = [w for w in json.load(f) if isinstance(w, str) and w]
    except (OSError, ValueError):
        words = []
    return re.compile('|'.join(words), re.I) if words else re.compile(r'(?!)')


EXPOSURE_WORDS = _exposure_words()
REVIEWED = [(re.compile(r"\b(N2's |the )reviewed (class table|classes|table|list|closing-word table|closing-word rules)", re.I),
             lambda m: f"{m.group(1)}published {m.group(2)} (AI-drafted, open to review)")]


def public_text(t):
    if not isinstance(t, str):
        return t
    for rx, rep in REVIEWED:
        t = rx.sub(rep, t)
    return t


def flat(o):
    if isinstance(o, dict):
        return ' '.join(flat(v) for v in o.values())
    if isinstance(o, list):
        return ' '.join(flat(v) for v in o)
    return str(o) if o is not None else ''


def unsafe(o):
    t = flat(o)
    return bool(EXPOSURE_WORDS.search(t))


def strip_sources(t):
    """Drop the trailing '(observed; source: ...)' parenthetical: provenance stays in the deliverable, not on the page."""
    return re.sub(r'\s*\((?:observed|reported|inferred|estimated)[^()]*(?:\([^()]*\)[^()]*)*\)\s*$', '', t or '').strip()


def build_negative():
    p = B('deliverable', 'negative-results.md')
    if not os.path.exists(p):
        mark_missing('negative', 'no deliverable/negative-results.md yet')
        return
    text = open(p, encoding='utf-8', errors='replace').read()
    items, seen, held = [], set(), 0
    secs = md_sections(text)
    for head, body in secs:
        if re.search(r'summary|admission|about this|^contents', head, re.I):
            continue
        group = strip_md(head)
        featured = bool(re.search(r'shaped|headline|most important|top', head, re.I))
        bullets = md_items(body)
        cands = [split_title(b) for b in bullets] if bullets else [(group, strip_md(' '.join(l.strip() for l in body.splitlines() if l.strip())))]
        for t, x in cands:
            x = strip_sources(x)
            key = t.lower().strip()
            if key in seen:
                continue
            if unsafe({'t': t, 'x': x}):
                held += 1
                continue
            seen.add(key)
            items.append({'title': public_text(t), 'text': public_text(x), 'group': group, 'featured': featured})
    notes = [f'{held} items held back from the public file (privacy rule)'] if held else []
    write('negative', {'items': items}, [src(p)], notes)


# ---------------------------------------------------------------- queue (E3, surface 1)
QUEUE_BUCKETS = ['0-30', '31-90', '91-180', '181-365', '366+']


def build_queue():
    """site/data/queue.json from build/E3/queue.json (scripts/exec/E3/build_queue.py). Block level; no ids."""
    p = B('build', 'E3', 'queue.json')
    d = load_json(p)
    if not d or not d.get('divisions'):
        mark_missing('queue', 'build/E3/queue.json not built yet (scripts/exec/E3/build_queue.py)')
        return

    def row(r):
        return {'division': r.get('division'), 'type_name': plain_name(r.get('problem_code')) if r.get('problem_code') else _tidy_plain(r.get('type_name')),
                'ward': r.get('ward'), 'block': block_label(r.get('block_label')), 'filed': r.get('filed'), 'promised': r.get('promised'),
                'days_past_promise': r.get('days_past_promise')}
    top = [row(r) for r in d.get('top') or []]
    m = d.get('map') or {}
    # compact dots: [x, y, n, bucket index, oldest days past, ward, block]
    def dot(x):
        return [x['x'], x['y'], x['n'], QUEUE_BUCKETS.index(x['bucket']), x['max_days_past'], x.get('ward'), block_label(x['block'])]
    dots = [dot(x) for x in m.get('dots') or []]
    dots_by_div = {k: [dot(x) for x in v] for k, v in (m.get('dots_by_div') or {}).items()}
    top_by_div = {k: [row(r) for r in v] for k, v in (d.get('top_by_div') or {}).items()}
    rp = B('build', 'E3', 'queue_rows.json')
    allrows = rows_of(load_json(rp), 'rows') or []
    write_csv(os.path.join(DL, 'queue.csv'), [dict(row(r), problem_code=r.get('problem_code'), age_days=r.get('age_days'), status=r.get('status')) for r in allrows],
              ['division', 'problem_code', 'type_name', 'ward', 'block', 'filed', 'promised', 'days_past_promise', 'age_days', 'status'])
    write('queue', {'asof': d.get('asof'), 'run_cutoff': d.get('run_cutoff'), 'since': d.get('since'), 'definition': d.get('definition'),
                    'tiles': d.get('tiles'), 'divisions': d.get('divisions'), 'hist': d.get('hist'),
                    'map': {'width': m.get('width'), 'height': m.get('height'), 'grid_m': m.get('grid_m'), 'figure_id': m.get('figure_id'),
                            'wards': m.get('wards'), 'dot_fields': ['x', 'y', 'n', 'bucket', 'oldest_days_past', 'ward', 'block'], 'dots': dots,
                            'dots_by_div': dots_by_div},
                    'rows_total': d.get('rows_total'), 'top': top, 'top_by_div': top_by_div, 'csv': 'data/downloads/queue.csv',
                    'saved_search': d.get('saved_search'), 'corroboration': d.get('corroboration'), 'oldest_filed': d.get('oldest_filed')},
          [src(p), src(rp)], [f'{len(allrows)} rows in queue.csv; {len(dots)} block dots'])


# ---------------------------------------------------------------- status page before/after (E3, surface 2)
def build_statuspage():
    """site/data/statuspage.json from build/E3/statuspage.json (scripts/exec/E3/build_statuspage.py)."""
    p = B('build', 'E3', 'statuspage.json')
    d = load_json(p)
    if not d or not d.get('panels'):
        mark_missing('statuspage', 'build/E3/statuspage.json not built yet (scripts/exec/E3/build_statuspage.py)')
        return
    d = strip_ids({k: v for k, v in d.items() if k != 'meta'})
    write('statuspage', scrub_obj(d), [src(p)])


# ---------------------------------------------------------------- downloads
def build_downloads():
    files = []
    for sp, name, desc in [
        (B('scripts', 'night', 'N1', 'measures.sql'), 'measures.sql', 'The measures as plain DuckDB SQL: promise, re-filed, ledger and work-order joins, Monday list, receipt.'),
        (B('build', 'N2', 'closure_class.sql'), 'closure_class.sql', "The closure classes as SQL: the city's closing words to done / handed off / no action."),
        (B('research', 'chapters', 'N2-closure-classes.csv'), 'closure-classes.csv', 'Every closing text, its class and the rule or judgement behind it: the table a person reviews.'),
        (B('build', 'N4', 'scoreboard.csv'), 'scoreboard.csv', 'The scoreboard, every request type.'),
    ]:
        if os.path.exists(sp):
            if name.endswith('.csv'):
                with open(sp, newline='', encoding='utf-8', errors='replace') as f:
                    rows = list(csv.reader(f))
                with open(os.path.join(DL, name), 'w', newline='') as f:
                    w = csv.writer(f)
                    for r in rows:
                        w.writerow([scrub_text(c) for c in r])
            else:
                shutil.copyfile(sp, os.path.join(DL, name))
            files.append({'name': name, 'href': f'data/downloads/{name}', 'desc': desc, 'from': rel(sp),
                          'kb': max(1, round(os.path.getsize(os.path.join(DL, name)) / 1024))})
    for name, desc in [('queue.csv', 'The overdue queue: every open request filed since 1 Jan 2025 past its promised date, oldest first, block level, no request numbers.'),
                       ('monday_list.csv', 'The Monday list: every open request past its promised date, block level, no request numbers.'),
                       ('brief_lra_lots.csv', 'Brief list 1: city-owned lots closed "on schedule" with no cut billed since.'),
                       ('brief_cavein_referred.csv', 'Brief list 2: cave-ins referred in the last 90 days.'),
                       ('brief_tree_cancelled.csv', 'Brief list 3: tree requests cancelled where a removal order is open.'),
                       ('dumping_blocks.csv', 'Illegal dumping and debris reports by block, last 365 days.')]:
        if os.path.exists(os.path.join(DL, name)):
            files.append({'name': name, 'href': f'data/downloads/{name}', 'desc': desc, 'from': 'scripts/night/N6/bridge.py',
                          'kb': max(1, round(os.path.getsize(os.path.join(DL, name)) / 1024))})
    write('downloads', {'files': files}, [{'path': f['from'], 'mtime': None} for f in files])


def main():
    log(f'bridge {NOW}')
    build_run()
    build_figures()
    build_receipts()
    build_scoreboard()
    build_fairness()
    build_register()
    build_monday()
    build_dumping()
    build_brief()
    build_queue()
    build_statuspage()
    build_negative()
    build_downloads()
    status = {'built_at': NOW, 'files': STATUS, 'log': LOG}
    with open(os.path.join(SITE_DATA, 'status.json'), 'w') as f:
        json.dump(status, f, indent=1, default=str)
    with open(B('build', 'N6', 'bridge-status.json'), 'w') as f:
        json.dump(status, f, indent=1, default=str)
    real = [k for k, v in STATUS.items() if v['state'] != 'mock']
    mock = [k for k, v in STATUS.items() if v['state'] == 'mock']
    log(f'real or partial: {", ".join(real)}')
    log(f'mock: {", ".join(mock) or "none"}')


if __name__ == '__main__':
    sys.exit(main())
