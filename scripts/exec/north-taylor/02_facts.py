"""Write research/north-taylor-mechanism-facts.csv from build/north-taylor/mechanism.json (aggregate only).
Run after 01_mechanism.py: .venv/bin/python -I scripts/exec/north-taylor/02_facts.py
"""
import csv, json, pathlib

ROOT = pathlib.Path('.')
R = json.load(open(ROOT / 'build/north-taylor/mechanism.json'))
A, B, C, D = R['A_block'], R['B_citywide'], R['C_persistence'], R['D_route_and_checks']
CSB = 'https://www.stlouis-mo.gov/data/upload/data-files/csb.zip'
LED = 'https://www.stlouis-mo.gov/data/upload/data-files/forestry-service-records.csv'
FMP = 'https://www.stlouis-mo.gov/data/upload/data-files/forestry-maintenance-properties.csv'
LRA = 'https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_INVENTORY.csv'
LRAD = 'https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/'
MSD = 'https://services1.arcgis.com/plGX8WiX9ylnkcee/arcgis/rest/services/Development_Review/FeatureServer/9'
S = 'scripts/exec/north-taylor/01_mechanism.py -> build/north-taylor/mechanism.json'
rows = []


def add(fig, val, unit, when, label, srcs):
    rows.append({'figure': fig, 'value': val, 'unit': unit, 'date_refers_to': when, 'label': label,
                 'source': '; '.join(srcs) + f' ({S})'})


def grp(lst, name):
    return next(r for r in lst if r['grp'] == name)


L1 = A['lot1_detail']
add('Lot-1 2026 weed reports (Weeds-Vacant Lot)', L1['weed_reports_2026'], 'requests', '2026-07-02 and 2026-07-28', 'observed', [CSB, MSD])
r_l1 = grp(A['reports_by_group'], 'lot-1')
add('Lot-1 report minutes to close (shorter)', r_l1['min_minutes'], 'minutes', '2026-07-28', 'observed', [CSB])
add('Lot-1 report minutes to close (longer)', r_l1['max_minutes'], 'minutes', '2026-07-02', 'observed', [CSB])
add('Lot-1 reports closed "on schedule to be cut, call csb for details"', r_l1['on_schedule'], 'requests', '2026', 'observed', [CSB])
add('Lot-1 cuts billed 2026', L1['cuts_2026'], 'distinct cut dates', '2026-01-01 to 2026-10-13', 'observed', [LED])
add('Lot-1 cuts billed 2025', L1['cuts_2025'], 'distinct cut dates', '2025', 'observed', [LED])
add('Lot-1 cuts billed 2024', L1['cuts_2024'], 'distinct cut dates', '2024', 'observed', [LED])
add('Lot-1 cuts billed 2019-2024', L1['cuts_2019_24'], 'distinct cut dates', '2019-2024', 'observed', [LED])
add('Lot-1 last billed cut', L1['last_cut_before_2026_month'], 'month', '2024-10', 'observed', [LED])
add('Lot-1 charge per cut (all 2022-24 cuts)', L1['last_cut_charge'], 'USD', '2022-2024', 'observed', [LED])
add('Lot-1 parcel area (LRA inventory SQFT)', D['lot1_inventory']['sqft'], 'sq ft', '2026-10-13 snapshot', 'observed', [LRA])
add('Median area of the other land-bank parcels on the block', D['block_land_bank_sqft_median']['m'], 'sq ft', '2026-10-13 snapshot', 'observed', [LRA])
add('Lot-1 rows in LRA offers, offers archive, garden permits and PROPNS nominee files', sum(v for k, v in D['lot1_rows_in_land_bank_files'].items() if 'INVENTORY' not in k), 'rows', '2026-10-13 snapshot', 'observed', [LRAD])

add('Parcels on lot-1 assessor city block (MSD handle or ledger CITYBLOCK)', A['block_parcels_total'], 'parcels', '2026-10-13', 'observed', [MSD, LED])
for key, nm in (('neighbours_cut_2026', 'Cut neighbours'), ('neighbours_not_cut_2026', 'Uncut neighbours')):
    g = A[key]
    when = '2026-01-01 to 2026-10-13'
    add(f'{nm}: parcels', g['n_parcels'], 'parcels', when, 'observed', [LED, MSD])
    add(f'{nm}: land-bank owned', g['land_bank'], 'parcels', '2026-10-13 snapshot', 'observed', [LRA])
    add(f'{nm}: on Forestry maintenance list (any category)', g['on_maint_list_any'], 'parcels', '2023-05-26 list', 'observed', [FMP])
    add(f'{nm}: on maintenance list as Vacant Lot', g['maint_vacant_lot'], 'parcels', '2023-05-26 list', 'observed', [FMP])
    add(f'{nm}: on maintenance list as Vacant Building', g['maint_vacant_building'], 'parcels', '2023-05-26 list', 'observed', [FMP])
    add(f'{nm}: latest ledger property type Vacant Lot', g['ledger_type_vacant_lot'], 'parcels', 'latest cut row', 'observed', [LED])
    add(f'{nm}: no cut billed 2019-2026', g['never_in_cut_ledger_2019_26'], 'parcels', '2019-2026', 'observed', [LED])
    add(f'{nm}: MSD land use code 1010', g['msd_luc_1010'], 'parcels', 'MSD layer edited 2026-10-12', 'observed', [MSD])
    add(f'{nm}: cut in 2024', g['cut_2024'], 'parcels', '2024', 'observed', [LED])
    add(f'{nm}: cut in 2025', g['cut_2025'], 'parcels', '2025', 'observed', [LED])
    add(f'{nm}: with a 2026 weed report (Weeds-Vacant Lot or Bldg)', g['with_weed_report_2026'], 'parcels', '2026', 'observed', [CSB])
    add(f'{nm}: 2026 weed reports', g['weed_reports_2026_total'], 'requests', '2026', 'observed', [CSB])
    add(f'{nm}: with a 2026 missed or unsatisfactory cut complaint', g['with_cut_complaint_2026'], 'parcels', '2026', 'observed', [CSB])
rc = grp(A['reports_by_group'], 'neighbour cut 2026')
add('Cut neighbours: median minutes to close their weed reports', rc['median_minutes_to_close'], 'minutes', '2026', 'observed', [CSB])
add('Cut neighbours: weed reports closed within 60 minutes', rc['closed_within_60_min'], 'requests', '2026', 'observed', [CSB])
add('Cut neighbours: weed reports closed "on schedule to be cut"', rc['on_schedule'], 'requests', '2026', 'observed', [CSB])
add('Cut neighbours: weed reports closed "added to rotation"', rc['added_to_rotation'], 'requests', '2026', 'observed', [CSB])
add('Cut neighbours: reports followed by a billed cut', rc['cut_after_filing'], 'requests', '2026-10-13', 'observed', [CSB, LED])
add('Cut neighbours: median days from report to next billed cut', rc['median_days_to_next_cut'], 'days', '2026', 'observed', [CSB, LED])
add('Cut neighbours: reports cut within 14 days', rc['cut_within_14d'], 'requests', '2026', 'observed', [CSB, LED])
tw = A['twin_same_block_reports']
add('Twin (land-bank lot on the same block, reported alongside lot-1): 2026 weed reports', tw['reports'], 'requests', '2026', 'observed', [CSB])
add('Twin: reports closed "on schedule to be cut"', tw['on_schedule'], 'requests', '2026', 'observed', [CSB])
add('Twin: fastest close', tw['min_minutes'], 'minutes', '2026', 'observed', [CSB])
add('Twin: slowest close', tw['max_minutes'], 'minutes', '2026', 'observed', [CSB])
add('Twin: cuts billed 2026', tw['twin_cuts_2026'], 'distinct cut dates', '2026-01-01 to 2026-10-13', 'observed', [LED])
add('Cut neighbours with no weed, cut-complaint or debris request of any kind in 2026', A['cut_neighbours_no_weed_request_any_kind'], 'parcels', '2026', 'observed', [CSB, LED])
ru = grp(A['reports_by_group'], 'neighbour not cut 2026')
add('Uncut neighbour report: minutes to close ("added to rotation")', ru['max_minutes'], 'minutes', '2026-06-11', 'observed', [CSB])
add('Distinct 2026 cut days on the block', A['block_cut_days_2026'], 'days', '2026-04-14 to 2026-10-12', 'observed', [LED])
add('Block parcels cut on or after 2 Jul 2026 (first report)', D['block_after_2026-07-02']['parcels_cut'], 'parcels', '2026-07-02 to 2026-10-13', 'observed', [LED])
add('Block cut days on or after 2 Jul 2026', D['block_after_2026-07-02']['cut_days'], 'days', '2026-07-02 to 2026-10-13', 'observed', [LED])
add('Block parcels cut on or after 28 Jul 2026 (second report)', D['block_after_2026-07-28']['parcels_cut'], 'parcels', '2026-07-28 to 2026-10-13', 'observed', [LED])
add('Block parcels cut on or after 9 Sep 2026 (cut complaint)', D['block_after_2026-09-09']['parcels_cut'], 'parcels', '2026-09-09 to 2026-10-13', 'observed', [LED])
cd = A['cut_days_requested_vs_not']
add('Days a reported neighbour was cut', cd['days_with_requested_parcel_cut'], 'days', '2026', 'observed', [LED, CSB])
add('...of which an unreported neighbour was cut the same day', cd['requested_cut_days_also_unrequested'], 'days', '2026', 'observed', [LED, CSB])
add('Block parcels cut in 2025', A['block_parcels_cut_2025'], 'parcels', '2025', 'observed', [LED])
add('Block cut days in 2025', A['block_cut_days_2025'], 'days', '2025', 'observed', [LED])
add('Block parcels cut in 2024', A['block_parcels_cut_2024'], 'parcels', '2024', 'observed', [LED])
lnb = D['land_bank_neighbours_not_cut_2026'][0]
add('Land-bank neighbours with no 2026 cut', lnb['parcels'], 'parcels', '2026-10-13', 'observed', [LRA, LED])
add('...of which drew a 2026 weed report', lnb['with_report'], 'parcels', '2026', 'observed', [CSB])
sh = D['lot1_cut_days_shared_with_block_by_year']
add('Lot-1 cut days 2019-24 on which another block parcel was also billed', sum(r['shared_with_block'] for r in sh), 'days', '2019-2024', 'observed', [LED])
add('Lot-1 cut days 2019-24', sum(r['lot1_cut_days'] for r in sh), 'days', '2019-2024', 'observed', [LED])
add('Lot-1 2024 cut days shared with its block', next(r['shared_with_block'] for r in sh if r['y'] == 2024), 'days', '2024', 'observed', [LED])
rm, rmd = D['route_mates'], D['route_mates_2026_days']
add('Parcels billed on all 8 of lot-1 2023-24 cut dates (route-mates)', rm['parcels_billed_on_all_those_dates'], 'parcels', '2023-2024', 'observed', [LED])
add('Route-mates on lot-1 own block', rm['on_lot1_block'], 'parcels', '2023-2024', 'observed', [LED])
add('Route-mates: distinct city blocks', rm['city_blocks'], 'city blocks', '2023-2024', 'observed', [LED])
add('Route-mates land-bank owned', rm['land_bank'], 'parcels', '2026-10-13 snapshot', 'observed', [LRA])
add('Route-mates cut in 2026', rm['cut_2026'], 'parcels', '2026-01-01 to 2026-10-13', 'observed', [LED])
add('Route-mates cut on or after 28 Jul 2026', rm['cut_after_28_jul_2026'], 'parcels', '2026-07-28 to 2026-10-13', 'observed', [LED])
add('Route-mates cut in 2025', rm['cut_2025'], 'parcels', '2025', 'observed', [LED])
add('Route-mate 2026 cut days', rmd['cut_days'], 'days', '2026-04-21 to 2026-09-28', 'observed', [LED])
add('Route-mate 2026 cut days shared with lot-1 block', rmd['days_shared_with_lot1_block'], 'days', '2026', 'observed', [LED])
add('Lot-1 has dropped off the cutting rounds (no cut while its block and its former billing group were cut)', 'yes', 'judgement', '2025-2026', 'inferred', [LED])

# citywide
o = B['on_schedule_all']['rows'][0]
when = '2026-01-01 to 2026-09-13 filed; cuts to 2026-10-13'
add('2026 vacant-lot and vacant-building weed reports closed "on schedule to be cut" (parcel-matched, filed by 13 Sep)', o['requests'], 'requests', when, 'observed', [CSB, MSD])
add('...on parcels with no cut billed at any time in 2026', o['n_no_2026_cut'], 'requests', when, 'observed', [CSB, LED])
add('...share on parcels with no 2026 cut', o['pct_no_2026_cut'], '%', when, 'observed', [CSB, LED])
nc = B['no_cut_on_schedule_composition']
add('Parcels behind the no-cut on-schedule closures', nc['parcels'], 'parcels', when, 'observed', [CSB, LED])
add('No-cut on-schedule closures on parcels cut in 2019-24', nc['cut_2019_24'], 'requests', when, 'observed', [LED])
add('No-cut on-schedule closures on the 2023 maintenance list', nc['on_list'], 'requests', when, 'observed', [FMP])
for t in B['on_schedule_by_type']['rows']:
    add(f'On-schedule closures, {t["grp"]}: share with no 2026 cut', t['pct_no_2026_cut'], '%', when, 'observed', [CSB, LED])
    add(f'On-schedule closures, {t["grp"]}: n with no 2026 cut / n', f'{t["n_no_2026_cut"]} / {t["requests"]}', 'requests', when, 'observed', [CSB, LED])
for t in B['added_to_rotation_by_type']['rows']:
    add(f'"Added to rotation" closures, {t["grp"]}: share with no 2026 cut', t['pct_no_2026_cut'], '%', when, 'observed', [CSB, LED])
for t in B['on_schedule_by_lra']['rows']:
    add(f'On-schedule closures, {t["grp"]}: share with no 2026 cut ({t["n_no_2026_cut"]} of {t["requests"]})', t['pct_no_2026_cut'], '%', when, 'observed', [CSB, LED, LRA])
for t in B['on_schedule_by_maint']['rows']:
    if t['requests'] >= 25:
        add(f'On-schedule closures, maintenance list {t["grp"]}: share with no 2026 cut ({t["n_no_2026_cut"]} of {t["requests"]})', t['pct_no_2026_cut'], '%', when, 'observed', [CSB, LED, FMP])
for t in B['on_schedule_lots_by_lra_maint']['rows']:
    add(f'On-schedule vacant-lot closures, {t["grp"]}: share with no 2026 cut ({t["n_no_2026_cut"]} of {t["requests"]})', t['pct_no_2026_cut'], '%', when, 'observed', [CSB, LED, LRA, FMP])
for t in B['on_schedule_by_history']['rows']:
    add(f'On-schedule closures, {t["grp"]}: share with no 2026 cut ({t["n_no_2026_cut"]} of {t["requests"]})', t['pct_no_2026_cut'], '%', when, 'observed', [CSB, LED])
for t in B['on_schedule_by_speed']['rows']:
    add(f'On-schedule closures, closed {t["grp"][3:]}: share with no 2026 cut ({t["n_no_2026_cut"]} of {t["requests"]})', t['pct_no_2026_cut'], '%', when, 'observed', [CSB, LED])
for t in B['speed_by_outcome']:
    add(f'On-schedule closures, {t["outcome"]}: share closed within 60 minutes (n {t["n"]})', t['pct_within_60_min'], '%', when, 'observed', [CSB, LED])
    add(f'On-schedule closures, {t["outcome"]}: median minutes to close', t['median_minutes'], 'minutes', when, 'observed', [CSB, LED])
lp = B['on_schedule_lot1_profile']['rows'][0]
add(f'On-schedule closures on parcels like lot-1 (land bank, listed Vacant Lot, cut 2019-24, none 2025): share with no 2026 cut ({lp["n_no_2026_cut"]} of {lp["requests"]})', lp['pct_no_2026_cut'], '%', when, 'observed', [CSB, LED, LRA, FMP])
r1 = B['r1_replication']
add('R1 parcel-dates with same-block controls (replicated)', r1['units'], 'parcel-dates', when, 'observed', [CSB, LED])
add('R1 parcel-dates on parcels with no 2026 cut (replicated)', r1['units_no_2026_cut'], 'parcel-dates', when, 'observed', [CSB, LED])
add('...of which closed "on schedule to be cut"', r1['no_cut_on_schedule_units'], 'parcel-dates', when, 'observed', [CSB, LED])
add('...of which closed "added to rotation" only', r1['no_cut_added_to_rotation_only_units'], 'parcel-dates', when, 'observed', [CSB, LED])
add('R1 on-schedule parcel-dates', r1['on_schedule_units'], 'parcel-dates', when, 'observed', [CSB, LED])
add('R1 on-schedule parcel-dates with no 2026 cut: share', r1['pct_no_cut_among_on_schedule_units'], '%', when, 'observed', [CSB, LED])
add('Lot-1 parcel-dates among R1 539', B['lot1_in_r1_539']['lot1_units_no_cut'], 'parcel-dates', '2026', 'observed', [CSB, LED])
for t in C['lra_list_lots_cut_2024']:
    add(f'Land-bank lots listed Vacant Lot, cut 2024, {t["y2025"]}: share cut in 2026 ({t["cut_2026"]} of {t["parcels"]})', t['pct_cut_2026'], '%', '2024-2026', 'observed', [LED, LRA, FMP])
la = C['lra_list_lots_all']
add('Land-bank lots on the 2023 list as Vacant Lot', la['parcels'], 'parcels', '2026-10-13 snapshot', 'observed', [LRA, FMP])
add('...with no 2026 cut', la['no_cut_2026'], 'parcels', '2026-01-01 to 2026-10-13', 'observed', [LED])
add('...like lot-1: cut 2019-24, none in 2025 or 2026', la['like_lot1_no_cut_2025_26'], 'parcels', '2019-2026', 'observed', [LED])
add('...of which drew an "on schedule" reply in 2026', C['like_lot1_with_2026_on_schedule_report']['parcels'], 'parcels', when, 'observed', [CSB])
for t in C['parcels_cut_per_year']:
    add(f'Parcels with a billed cut, {t["y"]}', t['parcels'], 'parcels', str(t['y']), 'observed', [LED])
add('Ledger columns naming a contractor, crew or route', 0, 'columns', 'file as of 2026-10-13', 'observed', [LED])
add('Lot-1 promise date, report of 2 Jul (PRJCOMPLETEDATE)', '2026-09-30', 'date', '2026-07-02', 'observed', [CSB])
add('Lot-1 promise date, report of 28 Jul (not yet passed when the files end)', '2026-10-26', 'date', '2026-07-28', 'observed', [CSB])
add('Closing speed does not separate parcels that get cut from parcels that do not', 'yes', 'judgement', '2026', 'inferred', [CSB, LED])
add('Whether a lot is cut is set by its place on the crews\' rounds, not by a report', 'yes', 'judgement', '2026', 'inferred', [CSB, LED])

with open(ROOT / 'research/north-taylor-mechanism-facts.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['figure', 'value', 'unit', 'date_refers_to', 'label', 'source'])
    w.writeheader()
    w.writerows(rows)
print(len(rows), 'rows')
