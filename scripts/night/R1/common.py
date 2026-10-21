"""R1 shared definitions: kind of hand-off, traceability, dates. Imported by every R1 script.

Kind (R-COMMON): crew work (the city will do it), owner enforcement (a notice; the owner must act),
referral elsewhere (MSD, Ameren, MoDOT, another agency or an unnamed department).
Derived from N2's final rule column (closure_class.class_rule) plus four phrase overrides listed below.

Traceability: is there a public completion record we can join?
  traceable  record exists and is joined here (Forestry billing ledger; Building Division board-ups;
             Building Division demolition permits)
  partial    a record exists but covers only part of the outcome (open-order samples, or the city's own
             action after an owner notice)
  none       no public completion record found (reason given)
"""
import datetime as dt
import pathlib

ROOT = pathlib.Path('.')
DB = ROOT / 'build' / 'stl.duckdb'
OUT = ROOT / 'build' / 'R1'
PRIV = OUT / 'private'
LAYERS = ROOT / 'data/raw/city-services/arcgis/layers'
CW = ROOT / 'data/raw/city-services/arcgis/cityworks-service/layers'

ASOF = dt.date(2026, 10, 13)               # the 311 file and the ledger both end 13 Oct 2026
NEVER_CUTOFF = dt.date(2026, 9, 13)        # "never done" only where the promise passed >= 30 days before ASOF

OWNER_EXTRA = {'vehicle not derelict, refer to treasurer for ticketing', 'sent to parking enforcement'}
REFERRAL_EXTRA = {'referred to proper department', 'building was occupied, will need police'}


def kind(class_rule, res_key):
    base = (class_rule or '').split(';')[0].strip()
    rk = (res_key or '').strip()
    if base == 'handed_off:enforcement' or rk in OWNER_EXTRA:
        return 'owner_enforcement'
    if base == 'handed_off:external_agency' or rk in REFERRAL_EXTRA:
        return 'referral_elsewhere'
    return 'crew_work'


def subkind(class_rule):
    return (class_rule or '').split(';')[0].strip().split(':')[-1]


WEED_LEDGER = {'Weeds-Vacant Lot', 'Weeds-Vacant Bldg', 'Vcnt weed check-web', 'Missed Cut - V Lot',
               'Missed Cut - VBldg', 'Unsatisfy Cut - VLot', 'Unsatisfy Cut -VBldg'}
TREE_CITY = {'Inspect City Tree', 'City Tree Down', 'City Tree Limb Down', 'Stump Removal',
             'Broken/Hanging Limb', 'Inspect Private Tree', 'LRA Tree'}
POTHOLE = {'Potholes - Residnl', 'Potholes - Major St', 'Potholes - Alley'}
WATER_PREFIX = ('WTR-', 'FH-', 'NOWATER', 'PRESSURE', 'LEAKING', 'LOOSE-COVER', 'MISSING-COVER', 'CHK-JOBSITE',
                'HYDRANT', 'Misc-Water', 'TASTE', 'WATER-', 'HOLE-DEPRESSION', 'APPEARANCE', 'STREET-CAVEIN',
                'WALK-CAVEIN', 'LAWN-CAVEIN')
REFUSE_WORDS = ('collection will be made', 'routes will be completed', 'bulk will be picked up')


def trace(pc, res_key, k):
    """(traceability, record, note) for one type x closing phrase."""
    rk = (res_key or '').strip()
    if pc in WEED_LEDGER:
        if k == 'crew_work':
            return ('traceable', 'forestry_ledger', 'cut billed on the matched parcel (Grass Maint / Weed-Grass)')
        return ('partial', 'forestry_ledger', 'owner must act; the ledger shows only a city cut')
    if rk == 'referred to board up crew':
        return ('traceable', 'boardup_layer', 'Building Division board-up at the parcel or address')
    if pc == 'Vacnt Bldg Unsecured' and k == 'owner_enforcement':
        return ('partial', 'boardup_layer', 'owner must secure; the layer shows only a city board-up')
    if pc == 'LRA Board up' and rk == 'work ticket issued to crew':
        return ('partial', 'boardup_layer', 'LRA contractor board-ups may not be in the Building Division layer')
    if pc == 'LRA Demo Submission':
        return ('traceable', 'demolition_permits', 'completed demolition permit at the parcel or address')
    if pc == 'Building Collapse' and k == 'owner_enforcement':
        return ('partial', 'demolition_permits', 'owner must act; demolition is one possible outcome')
    if pc in TREE_CITY and rk in ('removal work order created', 'trim work order created'):
        return ('partial', 'cityworks_open_order_sample',
                '1,500-row samples of OPEN removal/trim orders: can show still open, cannot show done')
    if pc == 'Tree Planting requst':
        return ('none', 'tested_negative', 'Forest ReLeaf completed-planting sample is another programme (N2: 0.3% match)')
    if pc in POTHOLE:
        return ('none', 'tested_negative', 'Cityworks pothole layer is the same 311 record, not independent (N2)')
    if pc in ('Debris-Vacant Lot', 'Debris-Vacant Bldg'):
        return ('none', 'tested_negative', 'ledger stopped recording debris clean-ups after 2021 (N2)')
    if pc == 'Sidewalk Repair':
        return ('none', 'tested_negative', 'sidewalk inventory DateRepair empty in all 36,822 rows (N2)')
    if pc.startswith(WATER_PREFIX):
        return ('none', 'none_found', 'water work orders: live list of ~26 recent orders, no history (N2 register)')
    return ('none', 'none_found', '')


def q(con, sql, params=None):
    """Run SQL and return a list of dicts (no pandas in .venv)."""
    cur = con.execute(sql, params) if params else con.execute(sql)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def write_csv(path, rows):
    import csv
    with open(path, 'w', newline='') as f:
        if not rows:
            f.write('')
            return
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
