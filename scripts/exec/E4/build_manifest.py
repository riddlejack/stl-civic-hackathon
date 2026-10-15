#!/usr/bin/env python3
"""Build data/MANIFEST.csv for the public export, and vendor small clean city files (E4).

usage: build_manifest.py EXPORT_DIR [--repo REPO] [--vendor] [--out PATH]

A source counts as used when a file in the export (a script, report, figure registry or site
file) names its path under data/raw/, directly or through a path variable in a script. Each
used file gets one row; a folder or file pattern that a script reads as a whole (the status-page
sample, a paged Cityworks layer) gets one row for the set. Columns:

  name, url, retrieved_central, bytes, sha256, rows, used_by, tier, path, published_as, note

tier is one of
  vendored           copied to data/public/ (a city-published file under 5 MB that passes
                     scan_public.py); published_as gives the path
  fetched by script  re-downloaded by scripts/data/fetch_public.sh
  not published      named here so the claim can be traced; note says why it is not shipped

Never listed: anything under data/raw/voters/, and the audit's metadata folders for the
city's hosted services. URLs on hosts the scan forbids are withheld. With --vendor, vendored
files are copied to EXPORT_DIR/data/public/<path under data/raw>.
"""
import argparse, csv, datetime as dt, glob, hashlib, importlib.util, json, os, re, shutil, sys
from collections import defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
CENTRAL = ZoneInfo('America/Chicago')
VENDOR_MAX = 5 * 1024 * 1024
TEXT_VENDOR = {'.csv', '.json', '.geojson', '.md', '.txt', '.tsv', '.jsonl'}
NEVER = ('data/raw/voters', 'data/raw/city-services/arcgis/agol_services6', 'data/raw/city-services/arcgis/portal',
         'data/raw/city-services/arcgis/itemdata', 'data/raw/slmpd')
NOT_SHIPPED = {  # path prefix -> reason (rows are never published)
    'data/raw/cityworks-gap/authorized': 'Cityworks query-service extract read under the office-hours authorisation, which covered '
                                         'reading, not republishing; its ids resolve to addresses. Retrieval manifest: '
                                         'research/cityworks-retrieval-manifest.csv; aggregates: research/cityworks-*',
    'data/raw/stlouis-mo.gov/csb-status': "311 status-page sample (E1); each page's request id resolves to an address on the "
                                          "city's public status page. Aggregates: build/E1/service_table.csv and linkage tables",
}
NAMES = {
    'data/raw/stlouis-mo.gov/files/csb.zip': ('311 service requests, 2008 to date (csb.zip)', 'https://www.stlouis-mo.gov/data/upload/data-files/csb.zip'),
    'data/raw/stlouis-mo.gov/files/forestry-service-records.csv': ('Forestry service records (billing ledger)', 'https://www.stlouis-mo.gov/data/upload/data-files/forestry-service-records.csv'),
    'data/raw/stlouis-mo.gov/files/forestry-maintenance-properties.csv': ('Forestry maintenance properties', 'https://www.stlouis-mo.gov/data/upload/data-files/forestry-maintenance-properties.csv'),
    'data/raw/stlouis-mo.gov/files/LRA_INVENTORY.csv': ('Land Reutilization Authority inventory', 'https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_INVENTORY.csv'),
    'data/raw/msd/msd_parcels_stl_city_attrs.jsonl': ('MSD parcel attributes inside the city', 'https://services1.arcgis.com/plGX8WiX9ylnkcee/arcgis/rest/services/Development_Review/FeatureServer/9'),
    'data/raw/citystat/tableau-extract.md': ("CityStat chart tables as published (transcribed from the pages' Tableau summary data)", 'https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/'),
    'data/raw/stlouis-mo.gov/csb-status': ('311 status pages, E1 stratified sample', 'https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/check-service-request.cfm'),
}
CW_LAYER = re.compile(r'_(\d{4})\.json$')
REF_LIT = re.compile(r'data/raw/[A-Za-z0-9_.\-/]*')
ASSIGN = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$', re.M)
TOKENS = re.compile(r"'([^']*)'|\"([^\"]*)\"|([A-Za-z_][A-Za-z0-9_]*)")
JOIN = re.compile(r'os\.path\.join\(([^()]*)\)')
SLASH = re.compile(r'\b([A-Z_][A-Z0-9_]*)\s*/\s*((?:[\'"][^\'"]+[\'"]\s*/?\s*)+)')
FSTR = re.compile(r'\{([A-Z_][A-Z0-9_]*)\}/([A-Za-z0-9_.\-/]+)')
QUOTED = re.compile(r'[\'"]([A-Za-z0-9_.\-]+\.[A-Za-z0-9]{2,8})[\'"]')


def load_scan():
    spec = importlib.util.spec_from_file_location('scan_public', os.path.join(HERE, 'scan_public.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def norm(p):
    p = os.path.normpath(p).replace(os.sep, '/')
    return p[2:] if p.startswith('./') else p


def eval_path(expr, env):
    parts = []
    for s1, s2, ident in TOKENS.findall(expr):
        if ident:
            if ident in ('os', 'path', 'join', 'Path', 'str'):
                continue
            if ident not in env:
                return None
            parts.append(env[ident])
        else:
            parts.append(s1 or s2)
    if not parts:
        return None
    return norm('/'.join(p for p in parts if p))


def script_refs(text):
    """Paths under data/raw/ that a Python or shell script builds."""
    env, out = {'ROOT': '', 'REPO': ''}, set()
    for name, rhs in ASSIGN.findall(text):
        rhs = rhs.split('#')[0].strip()
        if name in ('ROOT', 'REPO'):
            continue
        m = JOIN.search(rhs)
        v = None
        if m and rhs.startswith('os.path.join'):
            v = eval_path(m.group(1), env)
        elif SLASH.match(rhs):
            sm = SLASH.match(rhs)
            if sm.group(1) in env:
                v = eval_path(sm.group(1) + ' ' + sm.group(2), env)
        elif re.fullmatch(r'[\'"][^\'"]*data/raw[^\'"]*[\'"]', rhs):
            v = norm(rhs[1:-1])
        if v is not None:
            env[name] = v
    for m in JOIN.finditer(text):
        v = eval_path(m.group(1), env)
        if v:
            out.add(v)
    for m in SLASH.finditer(text):
        if m.group(1) in env:
            v = eval_path(m.group(1) + ' ' + m.group(2), env)
            if v:
                out.add(v)
    for m in FSTR.finditer(text):
        if m.group(1) in env:
            out.add(norm(env[m.group(1)] + '/' + m.group(2)))
    out |= {v for v in env.values()}
    return {p for p in out if p.startswith('data/raw')}


def collect(export, repo):
    """{('file'|'dir'|'glob', path): set(referencing export files)}"""
    refs = defaultdict(set)
    skip = ('data/', 'scripts/exec/E4/', '.git/')
    for dp, dn, fn in os.walk(export):
        dn[:] = [d for d in dn if d != '.git']
        for f in fn:
            rel = norm(os.path.relpath(os.path.join(dp, f), export))
            if rel.startswith(skip) or os.path.splitext(f)[1].lower() in ('.png', '.jpg', '.jpeg'):
                continue
            try:
                text = open(os.path.join(dp, f), encoding='utf-8').read()
            except (UnicodeDecodeError, OSError):
                continue
            cands = {norm(m.group(0).rstrip('.,;:)')) for m in REF_LIT.finditer(text)}
            if f.endswith(('.py', '.sh')):
                built = script_refs(text)
                cands |= built
                for d in built:  # quoted file names that live in a folder the script reads
                    full = os.path.join(repo, d)
                    if os.path.isdir(full):
                        names = set(os.listdir(full))
                        cands |= {norm(d + '/' + q) for q in QUOTED.findall(text) if q in names}
            for c in cands:
                if c in ('data/raw', 'data') or any(c == n or c.startswith(n + '/') for n in NEVER):
                    continue
                full = os.path.join(repo, c)
                if '*' in c:
                    if glob.glob(full):
                        refs[('glob', c)].add(rel)
                    continue
                if os.path.isfile(full):
                    refs[('file', c)].add(rel)
                elif os.path.isdir(full):
                    refs[('dir', c)].add(rel)
                elif glob.glob(full + '*'):
                    refs[('glob', c)].add(rel)
    # a folder or pattern is its own row only when none of its files is named on its own
    files = {p for k, p in refs if k == 'file'}
    for key in [k for k in refs if k[0] != 'file']:
        if any(f.startswith(key[1].rstrip('/') + ('/' if key[0] == 'dir' else '')) for f in files):
            for f in files:
                if f.startswith(key[1]):
                    refs[('file', f)] |= refs[key]
            del refs[key]
    # drop a folder row covered by a wider folder row
    dirs = sorted(p for k, p in refs if k != 'file')
    for k, p in list(refs):
        if k != 'file' and any(p != q and p.startswith(q.rstrip('/') + '/') for q in dirs):
            refs[('dir', next(q for q in dirs if p != q and p.startswith(q.rstrip('/') + '/')))] |= refs.pop((k, p))
    return refs


def members(repo, key):
    kind, p = key
    full = os.path.join(repo, p)
    if kind == 'file':
        return [full]
    if kind == 'dir':
        return sorted(os.path.join(dp, f) for dp, dn, fn in os.walk(full) for f in fn)
    return sorted(x for x in glob.glob(full if '*' in p else full + '*') if os.path.isfile(x))


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def row_count(path, n1_rows):
    low = path.lower()
    try:
        if low.endswith('csb.zip'):
            return n1_rows
        if low.endswith('.csv'):
            csv.field_size_limit(1 << 30)
            with open(path, newline='', encoding='utf-8', errors='replace') as fh:
                return max(sum(1 for _ in csv.reader(fh)) - 1, 0)
        if low.endswith(('.jsonl', '.geojsonl')):
            return sum(1 for l in open(path, 'rb') if l.strip())
        if low.endswith(('.json', '.geojson')) and os.path.getsize(path) < 300_000_000:
            d = json.load(open(path))
            if isinstance(d, dict) and isinstance(d.get('features'), list):
                return len(d['features'])
    except Exception:
        return ''
    return ''


def embedded_source(path):
    if not path.endswith(('.json', '.geojson')) or os.path.getsize(path) > 300_000_000:
        return None, None
    with open(path, 'rb') as fh:
        fh.seek(max(0, os.path.getsize(path) - 4096))
        tail = fh.read().decode('utf-8', 'replace')
    u = re.search(r'"_source":\s*"([^"]+)"', tail)
    t = re.search(r'"_retrieved_utc":\s*"([^"]+)"', tail)
    return (u.group(1) if u else None), (t.group(1) if t else None)


TS = re.compile(r'\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:?\d{2})?')


def to_central(ts):
    """UTC timestamps (one, or a range written "A to B") as Central time."""
    out = []
    for m in TS.finditer(ts or ''):
        s = m.group(0).replace(' ', 'T').replace('Z', '+00:00')
        try:
            t = dt.datetime.fromisoformat(s)
        except ValueError:
            continue
        if t.tzinfo is None:
            t = t.replace(tzinfo=dt.timezone.utc)
        out.append(t.astimezone(CENTRAL).strftime('%Y-%m-%d %H:%M %Z'))
    return ' to '.join(dict.fromkeys(out)) if out else (ts or '')


def mtime_central(paths):
    ts = sorted(os.path.getmtime(p) for p in paths)
    f = lambda x: dt.datetime.fromtimestamp(x, CENTRAL).strftime('%Y-%m-%d %H:%M %Z')
    return f(ts[0]) if len(ts) == 1 or f(ts[0]) == f(ts[-1]) else f'{f(ts[0])} to {f(ts[-1])}'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('export_dir')
    ap.add_argument('--repo', default=os.path.abspath(os.path.join(HERE, '..', '..', '..')))
    ap.add_argument('--out', help='default EXPORT_DIR/data/MANIFEST.csv')
    ap.add_argument('--vendor', action='store_true', help='copy vendored files to EXPORT_DIR/data/public/')
    ap.add_argument('--fetch-script', default=os.path.join(HERE, 'public-data', 'fetch_public.sh'))
    a = ap.parse_args()
    export, repo = os.path.abspath(a.export_dir), os.path.abspath(a.repo)
    out = a.out or os.path.join(export, 'data', 'MANIFEST.csv')

    fetch_targets = {}
    ft = open(a.fetch_script, encoding='utf-8').read()
    for m in re.finditer(r"'url':\s*([^\n]+?),\s*(?:'fields'[^\n]*?,\s*)?(?:'where'[^\n]*?,\s*)?\n?\s*'target':\s*'([^']+)'", ft):
        fetch_targets[m.group(2)] = m.group(1)
    fetch_targets.update({t: None for t in re.findall(r"'target':\s*'([^']+)'", ft) if t not in fetch_targets})

    cw_manifest = {}
    p = os.path.join(repo, 'research', 'cityworks-retrieval-manifest.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            cw_manifest[r['layer']] = r
    audit = {}
    p = os.path.join(repo, 'research', 'data-audit-facts.csv')
    if os.path.exists(p):
        csv.field_size_limit(1 << 30)
        for r in csv.DictReader(open(p, encoding='utf-8', errors='replace')):
            u = (r.get('url') or '').strip().rstrip(',')
            if u.startswith('http'):
                audit.setdefault(u.rsplit('/', 1)[-1].split('?')[0], (u, r.get('retrieved_utc', '')))
    catalog = {}
    p = os.path.join(repo, 'data', 'raw', 'stlouis-mo.gov', 'catalog', 'data.json')
    if os.path.exists(p):
        for ds in json.load(open(p)).get('dataset', []):
            for d in ds.get('distribution', []):
                u = d.get('downloadURL') or ''
                if u:
                    catalog.setdefault(u.rsplit('/', 1)[-1], u)
    n1_rows = ''
    p = os.path.join(repo, 'build', 'N1', 'manifest.json')
    if os.path.exists(p):
        m = re.search(r'311 rows ([\d,]+)', ' '.join(json.load(open(p)).get('log', [])))
        n1_rows = int(m.group(1).replace(',', '')) if m else ''
    fig_counts = defaultdict(int)
    for fp in glob.glob(os.path.join(export, 'build', '*', 'figures.json')):
        try:
            d = json.load(open(fp))
        except Exception:
            continue
        ids = d.get('figures', d) if isinstance(d, dict) else {x.get('id'): x for x in d if isinstance(x, dict)}
        for fid in (ids.keys() if isinstance(ids, dict) else []):
            if fid and '_' in fid:
                fig_counts[fid.split('_', 1)[0]] += 1

    scan = load_scan()
    sets = scan.load_sets(repo, None)
    forbidden = scan.FORBIDDEN
    refs = collect(export, repo)
    rows, seen_sets = [], {}
    for key in sorted(refs, key=lambda k: (len(k[1]), k[1])):
        files = members(repo, key)
        if not files:
            continue
        sig = tuple(files)
        if sig in seen_sets:
            refs[seen_sets[sig]] |= refs[key]
            continue
        seen_sets[sig] = key
    for key in sorted(seen_sets.values(), key=lambda k: k[1]):
        kind, path = key
        files = members(repo, key)
        size = sum(os.path.getsize(f) for f in files)
        if kind == 'file':
            sha = sha_file(files[0])
            nrows = row_count(files[0], n1_rows)
        else:
            h = hashlib.sha256()
            for f in files:
                h.update(f'{norm(os.path.relpath(f, repo))} {sha_file(f)}\n'.encode())
            sha, nrows = h.hexdigest(), f'{len(files)} files'
        name, url, when, note = None, None, None, []
        base = os.path.basename(path.rstrip('/*'))
        for prefix, (nm, u) in NAMES.items():
            if path == prefix or path.startswith(prefix + '/') or prefix.startswith(path.rstrip('*')) and kind != 'file' and path.startswith(prefix):
                name, url = nm, u
        if path in NAMES:
            name, url = NAMES[path]
        if kind == 'file':
            u, t = embedded_source(files[0])
            if u:
                url = url or u; when = t
                name = name or 'City map layer ' + '/'.join(u.split('/services/')[-1].split('/')[:2])
            m = CW_LAYER.search(path)
            if 'cityworks-service' in path and m:
                lay = '1' if m.group(1) in ('3320', '3321') else '2'
                url = url or f'https://service.stlouis-mo.gov/cityworks/gis/1/{m.group(1)}/rest/services/cw/FeatureServer/{lay}'
                name = name or f'Cityworks public saved search {m.group(1)} ({base})'
            if not url and base in catalog:
                url = catalog[base]
            if base in audit and (not url or url == audit[base][0]):
                url, when = audit[base][0], when or audit[base][1] or None
        if 'cityworks-gap/authorized' in path:
            lay = re.search(r'layer_(\d+)', path)
            r = cw_manifest.get(lay.group(1)) if lay else None
            if r:
                url, when = r['source_url'], r['retrieved_first_utc']
            else:
                url = 'https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer'
                when = min((r['retrieved_first_utc'] for r in cw_manifest.values()), default=None)
            name = name or 'Cityworks query-service layers, authorised read (' + base + ('*' if kind == 'glob' else '') + ')'
        name = name or base
        if url and forbidden.search(url):
            url, note = '', note + ['host withheld (see scripts/exec/E4/ALLOWLIST.md)']
        retrieved = to_central(when) if when else mtime_central(files)
        if not when:
            note.append('retrieved = file time on disk')
        users = sorted(refs[key])
        sessions = sorted({m.group(1).lower() for u in users for m in [re.match(r'scripts/(?:night|exec)/([A-Z]\d+)/', u)] if m})
        figs = '; '.join(f'{s.upper()} figures ({fig_counts[s]}, ids {s}_*)' for s in sessions if fig_counts.get(s))
        used = (figs + '; ' if figs else '') + 'read or cited by ' + ', '.join(users[:6]) + (f' and {len(users) - 6} more' if len(users) > 6 else '')

        tier, published = 'not published', ''
        shipped_no = next((r for pfx, r in NOT_SHIPPED.items() if path.startswith(pfx)), None)
        if shipped_no:
            note.insert(0, shipped_no)
        elif path in fetch_targets:
            tier = 'fetched by script'
            note.insert(0, 'scripts/data/fetch_public.sh downloads it' + (' (person-name fields not requested)' if 'msd' in path or 'cityworks' in path else ''))
        else:
            city = bool(url and re.search(r'stlouis-mo\.gov|HZXbCkpCSqbGd0vK', url))
            reason = None
            if kind != 'file':
                reason = 'a set of files, listed so the claims that cite it can be traced'
            elif size >= VENDOR_MAX:
                reason = 'over 5 MB; fetch it from the URL'
            elif not url:
                reason = 'source URL not recorded in the retrieval logs; the citing report names the source'
            elif not city:
                reason = 'published by another organisation; fetch it from the URL'
            elif os.path.splitext(path)[1].lower() not in TEXT_VENDOR:
                reason = 'binary file the privacy scan cannot read; fetch it from the URL'
            else:
                text = open(files[0], encoding='utf-8', errors='replace').read()
                bad = set()
                for line in text.splitlines():
                    bad |= {c for c, _ in scan.check_line(line, sets)[0]}
                bad |= {c for _, c, _ in scan.check_structured(path, text)}
                if bad:
                    reason = 'holds ' + ', '.join(sorted(bad)) + ' (scan_public.py); fetch it from the URL'
            if reason:
                note.insert(0, reason)
            else:
                tier, published = 'vendored', 'data/public/' + path[len('data/raw/'):]
                if a.vendor:
                    dest = os.path.join(export, published)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.copy2(files[0], dest)
        rows.append({'name': name, 'url': url or '', 'retrieved_central': retrieved, 'bytes': size, 'sha256': sha,
                     'rows': nrows, 'used_by': used, 'tier': tier, 'path': path + ('*' if kind == 'glob' and '*' not in path else ''),
                     'published_as': published, 'note': '; '.join(note)})
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cols = ['name', 'url', 'retrieved_central', 'bytes', 'sha256', 'rows', 'used_by', 'tier', 'path', 'published_as', 'note']
    with open(out, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader(); w.writerows(rows)
    tiers = defaultdict(int)
    for r in rows:
        tiers[r['tier']] += 1
    print(f'build_manifest: {len(rows)} sources -> {out} (' + ', '.join(f'{k} {v}' for k, v in sorted(tiers.items())) + ')')
    return 0


if __name__ == '__main__':
    sys.exit(main())
