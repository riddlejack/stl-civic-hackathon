#!/usr/bin/env bash
# Re-download the public files the DoneStat pipeline reads, into data/raw/ (and the two
# planting tables R2 reads, into build/R2/private/raw/maps8_trees/). Then:
#   bash scripts/night/N1/run_all.sh
#
#   bash scripts/data/fetch_public.sh            download everything (about 600 MB, 10 minutes)
#   bash scripts/data/fetch_public.sh --check    ask each source for its size or row count only
#   bash scripts/data/fetch_public.sh --list     print the sources and where they go
#   bash scripts/data/fetch_public.sh --only csb,wards
#   bash scripts/data/fetch_public.sh --force    replace files that already exist (default: keep them)
#
# Python 3 standard library only. One request per second. No key, no login. Every source is
# published by the City of St. Louis or MSD without restriction; none is a page the city's
# robots.txt asks crawlers to avoid. Person-name fields are never requested: the MSD parcel
# query leaves out the owner field, and the Cityworks saved searches ask only for the
# operational fields the pipeline uses. The city updates these files; a fresh download gives
# numbers as of the download day, not the ones in data/MANIFEST.csv (compare the sha256).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${STL_ROOT:-$(git -C "$HERE" rev-parse --show-toplevel 2>/dev/null || (cd "$HERE/../.." && pwd))}"
exec "${PYTHON:-python3}" - "$ROOT" "$@" <<'PY'
import csv, datetime as dt, hashlib, json, os, sys, time, urllib.parse, urllib.request

ROOT, ARGS = sys.argv[1], sys.argv[2:]
UA = 'DoneStat-public-fetch/1.0 (civic hackathon prototype; re-downloads published City of St. Louis files)'
M8 = 'https://maps8.stlouis-mo.gov/arcgis/rest/services'
CW = 'https://service.stlouis-mo.gov/cityworks/gis/1'
WO_FIELDS = 'WORKORDERID,Description,Priority,Status,MapPage,WoAddress,DomainId,WorkOrderSid,WOXCoordinate,WOYCoordinate,WOZCoordinate'
SR_FIELDS = 'REQUESTID,DateTimeInit,Description,ProbAddress,DateTimeClosed,Status,DomainId,SRX,SRY,SRZ'
TREE_FIELDS = ('OBJECTID,GUID,ADDRESS,STREET_NUM,STREET,ON_,ROW,LOCATION_T,LOCATION,COMMON,DBH,STEMS,COND,STORMDAM,'
               'HSDAMAGE,OHUTILITY,ELIGIBLE,REPLANT,SCORE,TREATED,Status,Verification_Date,DATE_PLANTED,XCOORD,YCOORD')
P0_FIELDS = 'OBJECTID,ESRI_OID,GUID,ADDRESS,ON_,CURRENT_CONDITION_OF_SITE,TREE_TYPE,LOCATION_TYPE,LOCATION,DATE_PLANTED'

# name | kind | url | target (relative to the repository) | options
SOURCES = [
    {'name': 'csb', 'kind': 'file', 'what': '311 service requests, 2008 to date (csb.zip; 128 MB)',
     'url': 'https://www.stlouis-mo.gov/data/upload/data-files/csb.zip',
     'target': 'data/raw/stlouis-mo.gov/files/csb.zip'},
    {'name': 'ledger', 'kind': 'file', 'what': "Forestry service records (the billing ledger of grass cuts)",
     'url': 'https://www.stlouis-mo.gov/data/upload/data-files/forestry-service-records.csv',
     'target': 'data/raw/stlouis-mo.gov/files/forestry-service-records.csv'},
    {'name': 'maintenance', 'kind': 'file', 'what': "Forestry maintenance properties (the mowing list)",
     'url': 'https://www.stlouis-mo.gov/data/upload/data-files/forestry-maintenance-properties.csv',
     'target': 'data/raw/stlouis-mo.gov/files/forestry-maintenance-properties.csv'},
    {'name': 'lra', 'kind': 'file', 'what': 'Land Reutilization Authority (land bank) inventory',
     'url': 'https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_INVENTORY.csv',
     'target': 'data/raw/stlouis-mo.gov/files/LRA_INVENTORY.csv'},
    {'name': 'wards', 'kind': 'geojson', 'what': 'Ward boundaries (14 wards)',
     'url': M8 + '/STLOUIS/BOUNDARIES/MapServer/4',
     'target': 'data/raw/city-services/arcgis/layers/maps8_BOUNDARIES_Wards.geojson'},
    {'name': 'boardups', 'kind': 'geojson', 'what': 'Building Division board-ups',
     'url': M8 + '/BUILDING_DIVISION/BldgDiv_Boardups/MapServer/0',
     'target': 'data/raw/city-services/arcgis/layers/maps8_BUILDING_DIVISION_Boardups.geojson'},
    {'name': 'demolitions', 'kind': 'geojson', 'what': 'Building Division demolition permits',
     'url': M8 + '/BUILDING_DIVISION/Demolitions/MapServer/0',
     'target': 'data/raw/city-services/arcgis/layers/maps8_BUILDING_DIVISION_Demolitions.geojson'},
    {'name': 'cw6955', 'kind': 'esri', 'what': 'Cityworks public saved search 6955: easement tree removals, new',
     'url': CW + '/6955/rest/services/cw/FeatureServer/2', 'fields': WO_FIELDS.replace('MapPage', 'ProjStartDate,ProjFinishDate,MapPage'),
     'target': 'data/raw/city-services/arcgis/cityworks-service/layers/WO_Easement_Tree_Removals_New_6955.json'},
    {'name': 'cw6942', 'kind': 'esri', 'what': 'Cityworks public saved search 6942: easement tree trims',
     'url': CW + '/6942/rest/services/cw/FeatureServer/2', 'fields': WO_FIELDS,
     'target': 'data/raw/city-services/arcgis/cityworks-service/layers/WO_Easement_Trims_6942.json'},
    {'name': 'cw6862', 'kind': 'esri', 'what': 'Cityworks public saved search 6862: Forest ReLeaf completed planting work orders',
     'url': CW + '/6862/rest/services/cw/FeatureServer/2', 'fields': WO_FIELDS.replace('Status,', 'Status,ActualFinishDate,'),
     'target': 'data/raw/city-services/arcgis/cityworks-service/layers/Forest_ReLeaf_Completed_Planting_WOs_6862.json'},
    {'name': 'cw6861', 'kind': 'esri', 'what': 'Cityworks public saved search 6861: Forest ReLeaf tree planting work orders',
     'url': CW + '/6861/rest/services/cw/FeatureServer/2', 'fields': WO_FIELDS,
     'target': 'data/raw/city-services/arcgis/cityworks-service/layers/WO_Forest_ReLeaf_Tree_Planting_6861.json'},
    {'name': 'cw3321', 'kind': 'esri', 'what': 'Cityworks public saved search 3321: pothole requests, closed (server caps at 1,500)',
     'url': CW + '/3321/rest/services/cw/FeatureServer/1', 'fields': SR_FIELDS,
     'target': 'data/raw/city-services/arcgis/cityworks-service/layers/potholes_closed_3321.json'},
    {'name': 'cw3320', 'kind': 'esri', 'what': 'Cityworks public saved search 3320: pothole requests, open',
     'url': CW + '/3320/rest/services/cw/FeatureServer/1', 'fields': SR_FIELDS,
     'target': 'data/raw/city-services/arcgis/cityworks-service/layers/potholes_open_3320.json'},
    {'name': 'msd', 'kind': 'msd', 'what': 'MSD parcel attributes inside the city (owner field not requested)',
     'url': 'https://services1.arcgis.com/plGX8WiX9ylnkcee/arcgis/rest/services/Development_Review/FeatureServer/9',
     'fields': 'OBJECTID,PID,PARENT_PID,PROP_ADD,PROP_ZIP,LUC,PROPERTY_CLASS,LOW_STREET_NUM,STREET_NUM',
     'target': 'data/raw/msd/msd_parcels_stl_city_attrs.jsonl'},
    {'name': 'planted', 'kind': 'csv', 'what': 'Trees planted in the last 365 days (Forestry layer)',
     'url': M8 + '/PDA/City_of_Saint_Louis_Planted_Trees/MapServer/0', 'fields': P0_FIELDS, 'where': '1=1',
     'target': 'build/R2/private/raw/maps8_trees/pda_planted_last_365_days.csv'},
    {'name': 'cwprint', 'kind': 'csv', 'what': 'Street-tree inventory rows planted or verified since 2024 (CW_PRINT)',
     'url': M8 + '/CITYWORKS/CW_PRINT/MapServer/0', 'fields': TREE_FIELDS,
     'where': "DATE_PLANTED >= DATE '2024-01-01' OR Verification_Date >= DATE '2024-01-01'",
     'target': 'build/R2/private/raw/maps8_trees/cw_print_trees_2024plus.csv'},
]

_last = [0.0]


def request(url, params=None, post=False, method=None):
    wait = 1.0 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    data = None
    if params and post:
        data = urllib.parse.urlencode(params).encode()
    elif params:
        url = url + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=data, method=method, headers={'User-Agent': UA})
    try:
        return urllib.request.urlopen(req, timeout=600)
    finally:
        _last[0] = time.time()


def query(url, params, post=False):
    with request(url + '/query', dict(params, f=params.get('f', 'json')), post=post) as r:
        d = json.loads(r.read())
    if isinstance(d, dict) and 'error' in d:
        raise RuntimeError(f'{url}: {d["error"]}')
    return d


def pages(url, params, page=1000, post=False):
    off = 0
    while True:
        d = query(url, dict(params, resultOffset=off, resultRecordCount=page), post=post)
        feats = d.get('features', [])
        yield d, feats
        if not feats or (not d.get('exceededTransferLimit') and not d.get('properties', {}).get('exceededTransferLimit') and len(feats) < page):
            return
        off += len(feats)


def now_utc():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def iso(ms):
    return None if ms is None else dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def write_atomic(target, write):
    path = os.path.join(ROOT, target)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.part'
    write(tmp)
    os.replace(tmp, path)
    h, n = hashlib.sha256(), 0
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk); n += len(chunk)
    return n, h.hexdigest()


def fetch(s):
    k, url = s['kind'], s['url']
    if k == 'file':
        def w(tmp):
            with request(url) as r, open(tmp, 'wb') as fh:
                for chunk in iter(lambda: r.read(1 << 20), b''):
                    fh.write(chunk)
        return write_atomic(s['target'], w), None
    if k == 'geojson':
        feats = []
        for d, fs in pages(url, {'where': '1=1', 'outFields': '*', 'outSR': 4326, 'returnGeometry': 'true',
                                 'orderByFields': 'OBJECTID ASC', 'f': 'geojson'}):
            feats += fs
        doc = {'type': 'FeatureCollection', 'features': feats, '_source': url, '_retrieved_utc': now_utc()}
        return write_atomic(s['target'], lambda tmp: json.dump(doc, open(tmp, 'w'))), len(feats)
    if k == 'esri':  # Cityworks saved searches: one page, capped by the server at 1,500 rows
        d = query(url, {'where': '1=1', 'outFields': s['fields'], 'outSR': 4326, 'returnGeometry': 'true'})
        return write_atomic(s['target'], lambda tmp: json.dump(d, open(tmp, 'w'))), len(d.get('features', []))
    if k == 'msd':  # parcels intersecting each ward polygon, attributes only, de-duplicated on OBJECTID
        wards = json.load(open(os.path.join(ROOT, 'data/raw/city-services/arcgis/layers/maps8_BOUNDARIES_Wards.geojson')))
        seen = {}
        for wf in wards['features'][:int(os.environ.get('FETCH_TEST_WARDS', 0)) or None]:  # test hook: first N wards
            g = wf['geometry']
            rings = g['coordinates'] if g['type'] == 'Polygon' else [r for p in g['coordinates'] for r in p]
            geom = json.dumps({'rings': rings, 'spatialReference': {'wkid': 4326}})
            for d, fs in pages(url, {'where': '1=1', 'geometry': geom, 'geometryType': 'esriGeometryPolygon', 'inSR': 4326,
                                     'spatialRel': 'esriSpatialRelIntersects', 'outFields': s['fields'],
                                     'returnGeometry': 'false', 'orderByFields': 'OBJECTID ASC'}, post=True):
                for ft in fs:
                    a = ft['attributes']
                    seen[a['OBJECTID']] = a
        def w(tmp):
            with open(tmp, 'w') as fh:
                for oid in sorted(seen):
                    fh.write(json.dumps({'type': 'Feature', 'id': oid, 'geometry': None, 'properties': seen[oid]}) + '\n')
        return write_atomic(s['target'], w), len(seen)
    if k == 'csv':  # R2's format: attributes, dates as ISO, lon/lat in EPSG:4326
        fields = s['fields'].split(',')
        rows = []
        for d, fs in pages(url, {'where': s['where'], 'outFields': s['fields'], 'outSR': 4326, 'returnGeometry': 'true',
                                 'orderByFields': 'OBJECTID ASC'}, page=2000):
            for ft in fs:
                a = dict(ft['attributes'])
                for f in ('Verification_Date', 'DATE_PLANTED'):
                    if a.get(f) is not None:
                        a[f] = iso(a[f])
                g = ft.get('geometry') or {}
                a['lon_4326'], a['lat_4326'] = g.get('x'), g.get('y')
                rows.append(a)
        def w(tmp):
            with open(tmp, 'w', newline='') as fh:
                wr = csv.DictWriter(fh, fieldnames=fields + ['lon_4326', 'lat_4326'], extrasaction='ignore')
                wr.writeheader(); wr.writerows(rows)
        return write_atomic(s['target'], w), len(rows)
    raise ValueError(k)


def check(s):
    if s['kind'] == 'file':
        with request(s['url'], method='HEAD') as r:
            return f"{int(r.headers.get('Content-Length', 0)):,} bytes, last modified {r.headers.get('Last-Modified', '?')}"
    n = query(s['url'], {'where': s.get('where', '1=1'), 'returnCountOnly': 'true'})['count']
    return f'{n:,} rows on the server'


def main():
    only = None
    if '--only' in ARGS:
        only = set(ARGS[ARGS.index('--only') + 1].split(','))
    todo = [s for s in SOURCES if not only or s['name'] in only]
    if '--list' in ARGS:
        for s in todo:
            print(f"{s['name']:12} {s['target']}\n{'':12} {s['url']}\n{'':12} {s['what']}")
        return 0
    if '--check' in ARGS:
        bad = 0
        for s in todo:
            try:
                print(f"ok   {s['name']:12} {check(s)}")
            except Exception as e:
                bad += 1; print(f"FAIL {s['name']:12} {e}")
        return 1 if bad else 0
    if 'msd' in {s['name'] for s in todo} and not os.path.exists(os.path.join(ROOT, 'data/raw/city-services/arcgis/layers/maps8_BOUNDARIES_Wards.geojson')):
        todo.sort(key=lambda s: s['name'] != 'wards')  # the MSD query needs the ward polygons
    log = []
    for s in todo:
        if os.path.exists(os.path.join(ROOT, s['target'])) and '--force' not in ARGS:
            print(f"keep {s['name']:12} {s['target']} exists; --force replaces it")
            continue
        t0 = time.time()
        print(f"get  {s['name']:12} {s['url']}", flush=True)
        (n, sha), rows = fetch(s)
        rec = {'name': s['name'], 'url': s['url'], 'target': s['target'], 'retrieved_utc': now_utc(), 'bytes': n,
               'sha256': sha, 'rows': rows, 'seconds': round(time.time() - t0, 1)}
        log.append(rec)
        print(f"     {n:,} bytes" + (f', {rows:,} rows' if rows is not None else '') + f', sha256 {sha[:12]}…', flush=True)
    os.makedirs(os.path.join(ROOT, 'data/raw'), exist_ok=True)
    with open(os.path.join(ROOT, 'data/raw/_fetch_public_log.jsonl'), 'a') as fh:
        for rec in log:
            fh.write(json.dumps(rec) + '\n')
    if any(s['name'] == 'csb' for s in todo) and os.path.isdir(os.path.join(ROOT, 'build/csb-clean')):
        print('note: delete build/csb-clean/ so build_db.py re-extracts the new csb.zip')
    print('done; now run: bash scripts/night/N1/run_all.sh')
    return 0


sys.exit(main())
PY
