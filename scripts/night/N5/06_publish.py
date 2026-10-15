"""N5 step 6: write the public build/N5/heroes.json from the private file, and add the hero-specific
figures to build/N5/figures.json.

Public rules (Jack, 13 Oct ~11:55 p.m., COMMON.md): block level only, including city-owned lots; no
request, work-order or parcel ids (each is a direct key to the exact property in the city's public
files); no marker images; no e-mail addresses (one 311 resolution text holds a staff address).
The script refuses to write if any of those patterns survive.
"""
import json, os, re, copy, sys
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
OUT = os.path.join(ROOT, 'build/N5')
H = json.load(open(os.path.join(OUT, 'private/heroes_private.json')))
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')

pub = copy.deepcopy(H)
pub['note'] = ('Public hero cases. Every case is at block level (house numbers rounded down to the hundred), including the '
               'city-owned land-bank lots. Request, work-order and parcel ids are withheld because each leads straight to the '
               'exact property in the city\'s own files; they are kept privately for Jack. Times are Central. Aerial images '
               'frame the block (about 175 m across, centred on the block, not the lot) with no marker. Only the NAIP 2024 frames '
               '(USDA, public domain) are cleared for public use (cleared_for_public); the MSDIS 2022, 2024 and 2025 frames carry a '
               'no-redistribution clause or unknown terms (see each licence field). All predate the 2026 requests, so they show what '
               'the block is, not the 2026 grass.')
for c in pub['cases']:
    c.pop('private', None)
    c.pop('private_images', None)
    for e in c['timeline']:
        e.pop('request_id', None); e.pop('work_order_id', None)
        if e.get('public_date'):
            e['date'] = e.pop('public_date')
        e['event'] = EMAIL.sub('[e-mail address removed]', e['event'])
    c['story'] = EMAIL.sub('[e-mail address removed]', c['story'])
    if c.get('public_images'):
        for im in c['public_images']:
            im['caption'] = (f"The {c['place']['block']} from above. Image: {im['source']}, {im['year']}. About 175 m across, "
                             f"no marker; the image predates the 2026 requests.")

text = json.dumps(pub)
problems = []
stripped = re.sub(r'\b\d+ block of\b', 'BLOCK', text)
for pat, why in [(r'\b\d{11}\b', 'parcel id or handle'), (r'\b(19|20)\d{5}\b', 'request id'), (r'\b[56]\d{5}\b', 'work-order id'),
                 (r'\b\d{1,5}\s+(?:[NSEW]\s+)?[A-Z][A-Z]+\s+(?:AV|AVE|ST|RD|BLVD|DR|PL|CT|LN|TER|PKWY)\b', 'street address'),
                 (EMAIL.pattern, 'e-mail'), (r'private/', 'private path')]:
    for m in re.finditer(pat, stripped):
        problems.append((why, stripped[max(0, m.start() - 40):m.end() + 20]))
if problems:
    for p in problems[:20]:
        print('BLOCKED:', p)
    sys.exit('public heroes.json not written: private detail would leak')
json.dump(pub, open(os.path.join(OUT, 'heroes.json'), 'w'), indent=1)
print('wrote build/N5/heroes.json:', len(pub['cases']), 'cases; leak check passed')

# hero-specific figures (numbers likely to be said on screen)
F = json.load(open(os.path.join(OUT, 'figures.json')))
F = [f for f in F if not f['id'].startswith('n5_hero_')]
cs = {c['id']: c for c in H['cases']}
LOT_DER = ("311 requests at the lot (csb.zip 2026, one row per request id) joined to the Forestry billing ledger by parcel through MSD's "
           "parcel address file, and to the LRA inventory; ledger read to 13 Oct 2026; ledger dates posted in weekly batches.")
def add(id, value, unit, period, definition, derivation, note=''):
    F.append(dict(id=id, value=value, unit=unit, period=period, definition=definition, label='observed', derivation=derivation,
                  source_sql_or_script='scripts/night/N5/04_heroes.py, 06_publish.py', note=note))
l1 = cs['lot-1']['facts']
add('n5_hero_lot1_requests_2026', l1['weeds_requests_2026'], 'requests', '2026', 'lot-1 (1700 block of N Taylor Av): weed requests in 2026, each closed "on schedule to be cut" within 15 minutes', LOT_DER)
add('n5_hero_lot1_cuts_2026', l1['cuts_billed_2026'], 'cuts', '2026 to 13 Oct', 'lot-1: grass cuts billed on the lot in 2026', LOT_DER, 'a billing ledger: no charge is not proof of no cut')
add('n5_hero_lot1_block_parcels_cut_2026', l1['other_parcels_on_city_block_cut_2026'], 'parcels', '2026 to 13 Oct',
    'lot-1: other parcels on the same city block with a cut billed in 2026', LOT_DER + ' City block from the ledger CITYBLOCK code.')
add('n5_hero_lot2_requests_2026', cs['lot-2']['facts']['weeds_requests_2026'], 'requests', '2026', 'lot-2 (8100 block of Church Rd): weed requests in 2026, each closed "on schedule to be cut"', LOT_DER)
add('n5_hero_lot3_requests_2026', cs['lot-3']['facts']['weeds_requests_2026'], 'requests', '2026', 'lot-3 (1300 block of Arlington Av): weed requests in 2026, each closed "on schedule to be cut" within a day', LOT_DER)
LR = ("311 single-light-out requests (csb.zip, one row per request id), resident channels, filed after 16 May 2025, closed \"work completed\"; "
      "chosen as the pair nearest each ward group's median and filed closest together in time; promise from PRJCOMPLETEDATE.")
add('n5_hero_light1_days', cs['light-1']['days_to_close'], 'days', 'Dec 2025 to Jan 2026', 'light-1 (wards 1-5): days from filing to "work completed"', LR)
add('n5_hero_light2_days', cs['light-2']['days_to_close'], 'days', 'Dec 2025 to Jan 2026', 'light-2 (wards 10-14): days from filing to "work completed"', LR)
CR = ("311 cave-in requests (csb.zip, one row per request id), resident channels, filed after 16 May 2025; the wards 1-5 case closed "
      "\"referred to street maintenance...\" within a day, the wards 10-14 case closed \"work completed\" near that group's median.")
add('n5_hero_cave1_days', cs['cave-1']['days_to_close'], 'days', 'Sep 2025', 'cave-1 (wards 1-5): days to a "referred ... to be scheduled" closure', CR)
add('n5_hero_cave2_days', cs['cave-2']['days_to_close'], 'days', 'Sep 2025', 'cave-2 (wards 10-14): days to a "work completed" closure', CR)
TR = ("311 'Inspect City Tree' request (csb.zip 2025) cancelled with no text, matched by identical normalised address to an open removal work order "
      "in Cityworks saved search 6955 (1,500-row public sample, read 14 Oct 00:19 UTC); work-order dates converted from UTC to Central.")
t = cs['tree-1']['facts']
add('n5_hero_tree_minutes_cancel_after_wo', t['minutes_cancel_after_wo_start'], 'minutes', '10 Apr 2025', 'tree-1: minutes between the work order\'s projected start and the 311 cancellation', TR)
add('n5_hero_tree_days_past_finish', t['days_past_projected_finish'], 'days', 'to 13 Oct 2026', 'tree-1: days the removal work order is past its projected finish date, still status NEW', TR)
# ---- figures the video script quotes (coordinator, 14 Oct): n5_lot1_* and n5_funnel_* ----
F = [f for f in F if not (f['id'].startswith('n5_lot1_') or f['id'].startswith('n5_funnel_'))]
L1 = ("311 'Weeds-Vacant Lot' requests at the land-bank lot on the 1700 block of N Taylor Av (city open data csb.zip, 2026 file, one row per "
      "request id), joined to the Forestry billing ledger by parcel through MSD's parcel address file; ledger read to 13 Oct 2026, dates "
      "posted in weekly batches.")
f1 = cs['lot-1']['facts']
mins, filed, prom = f1['weeds_requests_2026_minutes_to_close'], f1['weeds_requests_2026_filed'], f1['weeds_requests_2026_promise']
for k, (m, fd) in enumerate(zip(mins, filed)):
    day = {'2026-07-02': 'jul02', '2026-07-28': 'jul28'}.get(fd, fd.replace('-', ''))
    add(f'n5_lot1_minutes_to_close_{day}', m, 'minutes', fd,
        f'lot-1 (land-bank lot, 1700 block of N Taylor Av, Greater Ville, Ward 12): minutes from filing to closing for the weed request filed {fd}, closed "on schedule to be cut, call CSB for details"',
        "311 file (csb.zip 2026): DATETIMECLOSED minus DATETIMEINIT for that request, rounded to the minute; closing words from PUBLICRESOLUTION.")
add('n5_lot1_promise_date', prom[0], 'date', filed[0],
    "lot-1: the city's own promise date (PRJCOMPLETEDATE) on the first 2026 weed request, filed 2 Jul 2026 (90 days after filing)",
    "311 file (csb.zip 2026): PRJCOMPLETEDATE of the request, the completion date the city sets on each request.",
    note=f"the second request (filed {filed[1]}) carries {prom[1]}" if len(prom) > 1 else '')
add('n5_lot1_cuts_billed_2026', f1['cuts_billed_2026'], 'cuts', '2026-01-01 to 2026-10-13', 'lot-1: grass cuts billed on the lot in 2026', L1,
    note='a billing ledger, not an operations log: no charge is not proof of no cut; a resident called on 9 Sep 2026 to report that the cut on the lot was left incomplete (see n5_unsat_cut_calls_2026)')
add('n5_lot1_block_other_parcels_cut_2026', f1['other_parcels_on_city_block_cut_2026'], 'parcels', '2026-01-01 to 2026-10-13',
    f"lot-1: other parcels on the same city block with a grass cut billed in 2026 ({f1['other_lra_parcels_on_city_block_cut_2026']} of them land-bank lots)",
    L1 + " Same city block = same CITYBLOCK code in the ledger.")
add('n5_lot1_block_cut_days_2026', f1['distinct_cut_days_on_city_block_2026'], 'days', '2026-01-01 to 2026-10-13',
    'lot-1: distinct dates in 2026 on which a cut was billed on another parcel of the same city block', L1 + " Same city block = same CITYBLOCK code in the ledger.")
fn = json.load(open(os.path.join(OUT, 'lot_funnel.json')))
FUN = ("311 'Weeds-Vacant Lot' requests filed in 2026 (city open data csb.zip, one row per request id) on land-bank (LRA) lots, resident channels, "
       "closed within three days as \"on schedule to be cut\" or \"added to rotation\"; joined to the Forestry billing ledger by parcel through MSD's "
       "parcel address file (83% of 2026 requests matched a parcel); ledger read to 13 Oct 2026, dates posted in weekly batches.")
for id, v, u, dfn in [
    ('n5_funnel_requests', fn['requests'], 'requests', 'weed requests on land-bank lots in 2026, resident channels, closed "on schedule to be cut" or "added to rotation" within 3 days'),
    ('n5_funnel_lots', fn['parcels'], 'lots', 'distinct land-bank lots behind those requests'),
    ('n5_funnel_cut_within_7d', fn['cut_within_7d_requests'], 'requests', 'of those requests, a cut billed on the lot within 7 days of filing'),
    ('n5_funnel_cut_by_promise', fn['cut_by_promise_requests'], 'requests', "of those requests, a cut billed on the lot on or before the request's own promise date (PRJCOMPLETEDATE)"),
    ('n5_funnel_no_cut_requests', fn['no_cut_after_requests'], 'requests', 'of those requests, no cut billed on the lot at any time after filing, to 13 Oct 2026'),
    ('n5_funnel_no_cut_lots', fn['no_cut_after_parcels'], 'lots', 'distinct land-bank lots with at least one such request (no cut billed after it)'),
]:
    F.append(dict(id=id, value=v, unit=u, period='2026 season to 2026-10-13', definition=dfn, label='observed', derivation=FUN,
                  source_sql_or_script='scripts/night/N5/02_lot_candidates.py (build/N5/lot_funnel.json), 06_publish.py',
                  note='a billing ledger is not an operations log: no charge is not proof of no cut; same values as the n5_lot_* entries'))
json.dump(F, open(os.path.join(OUT, 'figures.json'), 'w'), indent=1)
print('figures:', len(F))
