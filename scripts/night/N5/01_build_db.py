"""N5 step 1: build a small DuckDB database for the hero-case search.

Tables (all from files already on disk; nothing fetched):
  csb      311 requests 2025-2026 from build/csb-clean (invalid UTF-8 stripped), with
           parsed timestamps and the project's address normaliser (common.norm).
  a2p      normalised address -> city ParcelId, from MSD parcel attributes (OWNER_NAME never used).
  lra      LRA inventory (city land bank): parcel id, status, usage, ward, neighbourhood, address.
  fmp      Forestry maintenance property list (2023-05-26): parcel id, category.
  ledger   Forestry service ledger 2025-2026 (every service type), one row per billed service.
  wo_rm    Cityworks saved search 6955 (easement tree removals, status NEW), 1,500-row sample.
  wo_trim  Cityworks saved search 6942 (easement trims, status NEW), 1,500-row sample.

Run: CSB_DIR=build/csb-clean .venv/bin/python -I scripts/night/N5/01_build_db.py
No personal data is read: the 311 file has no requester identity; owner names are never loaded
into any table; staff fields were already excluded from the Cityworks samples.
"""
import os, sys, json, csv, datetime as dt
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
os.environ.setdefault('CSB_DIR', os.path.join(ROOT, 'build', 'csb-clean'))
sys.path.insert(0, os.path.join(ROOT, 'scripts', 'synthesis-checks'))
from common import norm, addr_to_pid, CSB_DIR  # noqa: E402
import duckdb  # noqa: E402

OUT = os.path.join(ROOT, 'build', 'N5', 'private', 'n5.duckdb')
RAW = os.path.join(ROOT, 'data', 'raw')
if os.path.exists(OUT):
    os.remove(OUT)
con = duckdb.connect(OUT)
con.create_function('norm', lambda s: norm(s), ['VARCHAR'], 'VARCHAR')

files = [os.path.join(CSB_DIR, f'{y}.csv') for y in ('2025', '2026')]
con.execute(f"""
create table csb as
select REQUESTID, CALLERTYPE, PROBLEMCODE, PLAIN_ENGLISH_NAME_FOR_PROBLEMCODE as type_name,
       STATUS, PUBLICRESOLUTION as resolution, PROBADDRESS, norm(PROBADDRESS) as addr_n,
       PROBZIP, WARD, NEIGHBORHOOD, SUBMITTO, try_cast(SRX as double) as srx, try_cast(SRY as double) as sry,
       try_cast(DATETIMEINIT as timestamp) as t_init,
       try_cast(DATETIMECLOSED as timestamp) as t_closed,
       try_cast(DATECANCELLED as timestamp) as t_cancel,
       try_cast(DATEINVTDONE as timestamp) as t_invdone,
       try_cast(PRJCOMPLETEDATE as timestamp) as t_promise,
       CALLERTYPE in ('WEB','PHONE','EMAIL','CHAT','TWITTER','LETTER') as resident
from read_csv({files!r}, all_varchar=true, header=true)
""")
print('csb rows', con.execute('select count(*), min(t_init), max(t_init) from csb').fetchall())
# The yearly files repeat some REQUESTIDs (16,042 ids in 2025-26; most are exact copies, some differ
# only in CALLERTYPE, e.g. INDETERMINATE vs NSO). csbd keeps one row per request, preferring a
# resident-channel row. Hero selection uses csbd.
con.execute("""create table csbd as select * from csb
               qualify row_number() over (partition by REQUESTID order by resident desc, CALLERTYPE, t_init) = 1""")
print('csbd rows (one per REQUESTID)', con.execute('select count(*) from csbd').fetchone())

m = addr_to_pid()
con.execute('create table a2p (addr_n varchar, pid varchar)')
con.executemany('insert into a2p values (?, ?)', [(k, v) for k, v in m.items() if v])
print('a2p rows', con.execute('select count(*) from a2p').fetchone())

con.execute(f"""
create table lra as
select ParcelId as pid, Parcel_Status, Usage, ACQUISITION_DATE, PropertyType, WARD as lra_ward,
       NeighborhoodName, trim(Address) as lra_address, norm(Address) as lra_addr_n, Frontage, SQFT
from read_csv('{RAW}/stlouis-mo.gov/files/LRA_INVENTORY.csv', all_varchar=true, header=true)
""")
print('lra rows', con.execute('select count(*) from lra').fetchone())

con.execute(f"""
create table fmp as
select PARCELID as pid, HANDLE as handle, CATEGORY as fmp_category
from read_csv('{RAW}/stlouis-mo.gov/files/forestry-maintenance-properties.csv', all_varchar=true, header=true)
""")
con.execute(f"""
create table ledger as
select trim(PARCEL) as pid, HANDLE as handle, CITYBLOCK as cityblock, PROPERTYTYPE as ptype,
       SERVICETYPE as stype, try_cast(SERVICEAMOUNT as double) as amount,
       try_cast(SERVICEDATE as timestamp) as t_service
from read_csv('{RAW}/stlouis-mo.gov/files/forestry-service-records.csv', all_varchar=true, header=true)
where SERVICEDATE >= '2025-01-01'
""")
print('ledger rows 2025-26', con.execute('select count(*), max(t_service) from ledger').fetchall())

def wo_table(name, fname):
    d = json.load(open(os.path.join(RAW, 'city-services/arcgis/cityworks-service/layers', fname)))
    rows = []
    for ft in d['features']:
        pr = ft.get('properties') or ft.get('attributes') or {}
        def ts(v):
            return dt.datetime.utcfromtimestamp(v / 1000) if v else None
        rows.append((pr.get('WORKORDERID'), pr.get('Description'), pr.get('Priority'), pr.get('Status'),
                     ts(pr.get('ProjStartDate')), ts(pr.get('ProjFinishDate')), pr.get('MapPage'),
                     pr.get('WoAddress'), norm(pr.get('WoAddress')), pr.get('WOXCoordinate'), pr.get('WOYCoordinate')))
    con.execute(f'create table {name} (woid bigint, descr varchar, priority varchar, status varchar, '
                'proj_start timestamp, proj_finish timestamp, ward varchar, wo_address varchar, addr_n varchar, '
                'x double, y double)')
    con.executemany(f'insert into {name} values (?,?,?,?,?,?,?,?,?,?,?)', rows)
    print(name, len(rows))

wo_table('wo_rm', 'WO_Easement_Tree_Removals_New_6955.json')
wo_table('wo_trim', 'WO_Easement_Trims_6942.json')
con.close()
print('wrote', OUT)
