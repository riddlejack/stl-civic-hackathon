"""N5 step 5: aerial images for the lot cases from MSDIS (University of Missouri) keyless ImageServers.

robots.txt: https://imagery.msdis.missouri.edu/robots.txt redirects (302) to /arcgis/robots.txt, which
returns 404, so the host publishes no robots rules (checked 2026-10-13 ~23:40 CDT, re-checked here).
No key, no login. Services publish a year in the service name only; no acquisition date in the
service description or catalog attributes.

Public images (build/N5/img/): framed on the BLOCK, ~175 m across, centred on the midpoint of the
block's MSD address points (not on the lot), no marker. Private images (build/N5/private/img/): a
tight frame on the LRA parcel with its outline, for Jack only.
"""
import json, math, os, re, sys, urllib.request, urllib.parse, datetime as dt
from PIL import Image, ImageDraw
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
sys.path.insert(0, os.path.join(ROOT, 'scripts', 'synthesis-checks'))
from common import norm  # noqa: E402
RAW = os.path.join(ROOT, 'data/raw')
OUTP, OUTX = os.path.join(ROOT, 'build/N5/img'), os.path.join(ROOT, 'build/N5/private/img')
SAVE = os.path.join(RAW, 'msdis-imagery')
BASE = 'https://imagery.msdis.missouri.edu/arcgis/rest/services/'
UA = {'User-Agent': 'stl-civic-hackathon research (keyless ArcGIS exportImage; contact via project)'}
# Licence notes: what each service's own metadata says (checked 14 Oct 2026; files in data/raw/msdis-imagery/meta_* and meta/).
# For all four services, itemInfo licenseInfo and accessInformation are empty and the service metadata XML holds only a title/purpose.
LIC = {
    'NAIP/NAIP2024': dict(cleared_for_public=True, source='NAIP 2024 (USDA, public domain), via MSDIS',
        licence=("USDA National Agriculture Imagery Program 2024 (producer USDA FPAC-BC-GEO), served by MSDIS. The service states no licence; the "
                 "NAIP metadata (meta/naip2024_mo510.xml, St. Louis City mosaic, dated 2024-05-31) has one use limitation: 'Use of this data "
                 "requires a general understanding of GIS and spatial data.' No redistribution limit found. Public domain as a USDA product "
                 "(reported; not stated in the file).")),
    'StLouisImagery/StLouis_2022_SPE': dict(cleared_for_public=False, source='MSDIS StLouisImagery 2022',
        licence=("MSDIS; the service states no licence. The bundled metadata of MSDIS's 2022 St. Louis City ortho (meta/statewide2022_stlcity.xml) "
                 "says it 'should not be re-distributed' and 'cannot be used without express consent'; whether this 0.5 ft city service is the same "
                 "product is not established. Treat as not cleared for public use.")),
    'StatewideServices/Missouri_2024_South_6inch': dict(cleared_for_public=False, source='MSDIS Missouri 2024 statewide 6-inch',
        licence=("MSDIS; the service states no licence. Its product metadata (meta/2024_MO_Statewide_Ortho_Metadata.xml, owner Missouri 911 "
                 "Service Board) says it 'should not be re-distributed' and 'cannot be used without the express, written consent of the Missouri "
                 "911 Service Board'. Not cleared for public use.")),
    'EmergencyImagery/StLouisTornado_2025': dict(cleared_for_public=False, source='MSDIS EmergencyImagery St. Louis tornado 2025',
        licence=("MSDIS; the service states no licence, access or use constraint (licenseInfo and accessInformation empty; metadata holds only "
                 "the title); collector and terms unknown. Not cleared for public use until the terms are known.")),
}
SERVICES = [  # (service, year label, note); NAIP first because it is the only one cleared for public use
    ('NAIP/NAIP2024', '2024', 'USDA NAIP, 0.3 m (resampled to 0.25 m), leaf-on; metadata date 2024-05-31 (reported), no separate flight date found'),
    ('StLouisImagery/StLouis_2022_SPE', '2022', '6-inch (0.5 ft) city orthoimagery; year from the service name, no acquisition date stated by the service'),
    ('EmergencyImagery/StLouisTornado_2025', '2025 (post-tornado)', '3-inch (0.25 ft) emergency imagery; service name says St. Louis tornado 2025, no acquisition date stated; tornado debris visible on the N Taylor block'),
    ('StatewideServices/Missouri_2024_South_6inch', '2024', '6-inch statewide orthoimagery; year from the service name, no acquisition date stated'),
]
TAG = {'NAIP/NAIP2024': 'naip2024'}
log = {'checked': dt.datetime.now().isoformat(timespec='seconds'), 'robots': None, 'exports': []}

def get(url, binary=False):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
        return r.status, r.headers.get('Content-Type'), r.read()

# robots
try:
    st, ct, body = get('https://imagery.msdis.missouri.edu/arcgis/robots.txt')
    log['robots'] = f'/arcgis/robots.txt HTTP {st}'
except urllib.error.HTTPError as e:
    log['robots'] = f'/robots.txt -> 302 to /arcgis/robots.txt -> HTTP {e.code} (no robots rules published)'
print('robots:', log['robots'])

def merc(lon, lat):
    x = lon * 20037508.34 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180) * 20037508.34 / 180
    return x, y

def block_midpoint(street_n, hundred):
    pts = []
    with open(os.path.join(RAW, 'msd/msd_service_address_stl_city.geojsonl')) as fh:
        for line in fh:
            if street_n.split()[-2] not in line:  # cheap prefilter on the street name
                continue
            f = json.loads(line)
            a = norm(f['properties'].get('FULLADDRESS'))
            m = re.match(r'^(\d+) (.+)$', a)
            if m and m.group(2) == street_n and int(m.group(1)) // 100 * 100 == hundred:
                pts.append(f['geometry']['coordinates'])
    if not pts:
        return None, 0
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)), len(pts)

def export(service, lon, lat, width_m, path, px=700, outlines=()):
    cx, cy = merc(lon, lat)
    half = width_m / 2 / math.cos(math.radians(lat))  # metres on the ground -> Web Mercator units
    bbox = (cx - half, cy - half, cx + half, cy + half)
    q = urllib.parse.urlencode(dict(bbox=','.join(f'{v:.2f}' for v in bbox), bboxSR=3857, imageSR=3857, size=f'{px},{px}',
                                    format='png', bandIds='0,1,2', f='image'))
    url = BASE + service + '/ImageServer/exportImage?' + q
    err = None
    for attempt in range(3):  # the server occasionally times out; retry twice
        try:
            st, ct, body = get(url)
            err = None
            break
        except Exception as e:
            err = str(e)
    if err:
        return dict(service=service, ok=False, error=err, url=url)
    if not (ct or '').startswith('image'):
        return dict(service=service, ok=False, error=f'non-image response {ct}: {body[:200]!r}', url=url)
    open(path, 'wb').write(body)
    im = Image.open(path).convert('RGB')
    ext = im.getextrema()
    blank = all(lo == hi for lo, hi in ext)
    if outlines:
        dr = ImageDraw.Draw(im)
        for ring, colour in outlines:
            pts = []
            for lo, la in ring:
                x, y = merc(lo, la)
                pts.append(((x - bbox[0]) / (bbox[2] - bbox[0]) * px, (bbox[3] - y) / (bbox[3] - bbox[1]) * px))
            dr.line(pts + [pts[0]], fill=colour, width=3)
    im.save(path)
    return dict(service=service, ok=not blank, blank=blank, path=os.path.relpath(path, ROOT), url=url, width_m=width_m,
                px=px, metres_per_px=round(width_m / px, 3))

heroes_path = os.path.join(ROOT, 'build/N5/private/heroes_private.json')
H = json.load(open(heroes_path))
polys = {}
g = json.load(open(os.path.join(RAW, 'city-services/arcgis/layers/maps8_SLDC_LRA_and_LCRA_Properties.geojson')))
for f in g['features']:
    polys[str(f['properties'].get('Handle'))] = f['geometry']['coordinates'][0] if f['geometry']['type'] == 'Polygon' else f['geometry']['coordinates'][0][0]

for c in H['cases']:
    is_lot = c['id'].startswith('lot')
    blk = c['place']['block']
    hundred, street = re.match(r'^(\d+) block of (.+)$', blk).groups()
    street = norm(f'{hundred} {street}').split(' ', 1)[1]  # same normaliser as the MSD address points
    mid, n = block_midpoint(street, int(hundred))
    c['public_images'], c['private_images'] = [], []
    if not mid:
        print(c['id'], 'no MSD address points for', blk)
    for svc, year, note in SERVICES:
        tag = TAG.get(svc, svc.split('/')[-1])
        if not is_lot and svc != 'NAIP/NAIP2024':
            continue  # non-lot heroes get the public-domain NAIP frame only
        if mid:
            r = export(svc, mid[0], mid[1], 175, os.path.join(OUTP, f"{c['id']}_block_{tag}.png"))
            r.update(year=year, note=note, frame='block, ~175 m across, centred on the midpoint of '
                     f'{n} MSD address points on the {blk}; no marker')
            log['exports'].append(dict(case=c['id'], kind='public', **r)); print(c['id'], 'public', tag, r.get('ok'), r.get('error', ''))
            if r.get('ok'):
                c['public_images'].append(dict({k: r[k] for k in ('path', 'service', 'year', 'note', 'frame', 'metres_per_px')}, **LIC[svc]))
            elif r.get('path') and os.path.exists(os.path.join(ROOT, r['path'])):
                os.remove(os.path.join(ROOT, r['path']))  # blank (outside coverage)
        # private, tight on the parcel with outline(s)
        ring = polys.get(c['private']['handle']) if is_lot else None
        if ring:
            lons = [p[0] for p in ring]; lats = [p[1] for p in ring]
            lon0, lat0 = (min(lons) + max(lons)) / 2, (min(lats) + max(lats)) / 2
            ext_m = max((max(lons) - min(lons)) * 111320 * math.cos(math.radians(lat0)), (max(lats) - min(lats)) * 110540)
            outl = [(ring, (255, 220, 0))] + [(polys[h], (0, 200, 255)) for h in c['private'].get('related_handles', []) if h in polys]
            width = max(60, ext_m * 1.6) if not outl[1:] else max(80, ext_m * 2.4)
            r = export(svc, lon0, lat0, width, os.path.join(OUTX, f"{c['id']}_parcel_{tag}.png"), outlines=outl)
            r.update(year=year, note=note, frame='tight on the LRA parcel; yellow = this lot, blue = related LRA lots')
            log['exports'].append(dict(case=c['id'], kind='private', **r))
            if r.get('ok'):
                c['private_images'].append({k: r[k] for k in ('path', 'service', 'year', 'frame', 'metres_per_px')})
            elif r.get('path') and os.path.exists(os.path.join(ROOT, r['path'])):
                os.remove(os.path.join(ROOT, r['path']))

json.dump(H, open(heroes_path, 'w'), indent=1, default=str)
json.dump(log, open(os.path.join(SAVE, 'N5_export_log.json'), 'w'), indent=1)
print('done')
