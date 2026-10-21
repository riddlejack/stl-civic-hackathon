"""N5 step 3: validate the leading lot candidates before calling any of them a hero.

For each candidate parcel (LRA-owned, so parcel level is allowed):
  - the parcel's whole ledger history, every year, matched by PARCEL and by HANDLE (in case the
    ledger bills it under a different id);
  - whether it is on Forestry's maintenance property list (2023-05-26) and with what category;
  - cuts billed on the same city block in 2026 (was a crew on the block?), and on other LRA lots
    on the block;
  - every 311 request at the address 2025-2026, any type.
Writes build/N5/private/lot_validation.json. OWNER_NAME is never read from the MSD file (only PID,
PARENT_PID, PROP_ADD are kept).
"""
import duckdb, json, os, sys, datetime as dt
ROOT = '.'
RAW = os.path.join(ROOT, 'data/raw')
# Candidate parcel ids come from the command line or from the git-ignored build/N5/private/hero_ids.json
# ('validate_pids'), so the code carries no real parcel id.
PIDS = sys.argv[1:] or json.load(open(os.path.join(ROOT, 'build/N5/private/hero_ids.json')))['validate_pids']
con = duckdb.connect(os.path.join(ROOT, 'build/N5/private/n5.duckdb'), read_only=True)

# MSD handle lookup without owner fields
handles = {}
with open(os.path.join(RAW, 'msd/msd_parcels_stl_city_attrs.jsonl')) as fh:
    for line in fh:
        if not any(p in line for p in PIDS):
            continue
        pr = json.loads(line)['properties']
        if pr.get('PID') in PIDS:
            handles[pr['PID']] = {'handle': pr.get('PARENT_PID'), 'prop_add': pr.get('PROP_ADD')}

con.execute(f"""create temp view ledger_all as
select trim(PARCEL) pid, trim(HANDLE) handle, CITYBLOCK cityblock, PROPERTYTYPE ptype, SERVICETYPE stype,
       try_cast(SERVICEDATE as timestamp) t_service, try_cast(SERVICEAMOUNT as double) amount
from read_csv('{RAW}/stlouis-mo.gov/files/forestry-service-records.csv', all_varchar=true, header=true)""")
con.execute("create temp table la as select * from ledger_all where pid in (select unnest(?)) or handle in (select unnest(?))",
            [PIDS, [h['handle'] for h in handles.values() if h.get('handle')]])

out = {}
for pid in PIDS:
    h = handles.get(pid, {})
    handle = h.get('handle')
    cityblock = handle[1:7] if handle and len(handle) == 11 else None
    lra = con.execute("select Parcel_Status, Usage, ACQUISITION_DATE, lra_ward, NeighborhoodName, lra_address, Frontage, SQFT from lra where pid=?", [pid]).fetchone()
    fmp = con.execute("select fmp_category, handle from fmp where pid=?", [pid]).fetchone()
    hist = con.execute("select year(t_service) y, stype, count(distinct t_service) n, min(t_service)::date, max(t_service)::date from la where pid=? or handle=? group by 1,2 order by 1,2",
                       [pid, handle]).fetchall()
    block = con.execute("""select count(*) n, count(distinct pid) parcels, min(t_service)::date, max(t_service)::date,
                                  count(distinct pid) filter (where pid in (select pid from lra)) lra_parcels
                           from ledger where cityblock=? and year(t_service)=2026 and stype in ('Grass Maint','Weed-Grass')""",
                        [cityblock]).fetchone() if cityblock else None
    block_dates = [str(r[0]) for r in con.execute("""select distinct t_service::date from ledger where cityblock=? and year(t_service)=2026
                    and stype in ('Grass Maint','Weed-Grass') order by 1""", [cityblock]).fetchall()] if cityblock else []
    addr_n = con.execute("select lra_addr_n from lra where pid=?", [pid]).fetchone()
    reqs = con.execute("""select REQUESTID, CALLERTYPE, PROBLEMCODE, STATUS, resolution, t_init, t_closed, t_cancel, t_promise, t_invdone, WARD, NEIGHBORHOOD
                          from csbd where addr_n in (select addr_n from a2p where pid=?) or addr_n=? order by t_init""",
                       [pid, addr_n[0] if addr_n else None]).fetchall()
    out[pid] = {
        'handle': handle, 'cityblock': cityblock, 'msd_prop_add': h.get('prop_add'),
        'lra': dict(zip(['Parcel_Status', 'Usage', 'ACQUISITION_DATE', 'ward', 'neighborhood', 'address', 'Frontage', 'SQFT'], lra)) if lra else None,
        'fmp': dict(zip(['category', 'handle'], fmp)) if fmp else None,
        'ledger_history': [dict(zip(['year', 'stype', 'n', 'first', 'last'], [str(x) for x in r])) for r in hist],
        'block_2026_cuts': dict(zip(['rows', 'parcels', 'first', 'last', 'lra_parcels'], [str(x) for x in block])) if block else None,
        'block_2026_cut_dates': block_dates,
        'requests_2025_26': [dict(zip(['id', 'caller', 'code', 'status', 'resolution', 'init', 'closed', 'cancelled', 'promise', 'invdone', 'ward', 'nbhd'],
                                      [str(x) if x is not None else None for x in r])) for r in reqs],
    }
    print('\n==', pid, out[pid]['lra'] and out[pid]['lra']['address'], '| handle', handle, '| fmp', fmp)
    print(' ledger history (all years):', hist)
    print(' block 2026 cuts:', block, block_dates[:30])
    for r in reqs:
        print('  ', r[0], r[1], r[2], r[3], (r[4] or '')[:45], str(r[5])[:16], str(r[6])[:16], str(r[8])[:10])
json.dump(out, open(os.path.join(ROOT, 'build/N5/private/lot_validation.json'), 'w'), indent=1, default=str)
