#!/usr/bin/env python3
"""DoneStat pipeline, step 1 (N1): public files on disk -> build/stl.duckdb.

Loads the 311 yearly CSVs (all years), the forestry service ledger, MSD
parcel attributes (PID, PARENT_PID, PROP_ADD, PROP_ZIP, LUC, PROPERTY_CLASS
and the street-number range; OWNER_NAME is never read), the LRA inventory,
forestry-maintenance-properties, ward polygons, and the Cityworks tree
work-order and pothole samples (whitelisted columns; no staff fields).
Then builds the derived tables and the measure views from measures.sql.

Builds into build/N1/stl.building.duckdb and swaps it into build/stl.duckdb
at the end, so readers never see a half-built file.

Run: .venv/bin/python -I scripts/night/N1/build_db.py
"""
import csv
import glob
import io
import json
import math
import os
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import duckdb  # noqa: E402
import numpy as np  # noqa: E402
import pyarrow as pa  # noqa: E402
from normalise import norm, parts, block  # noqa: E402

ROOT = os.environ.get('STL_ROOT', os.path.abspath(os.path.join(HERE, '..', '..', '..')))
RAW = os.path.join(ROOT, 'data', 'raw')
FILES = os.path.join(RAW, 'stlouis-mo.gov', 'files')
CSB_ZIP = os.path.join(FILES, 'csb.zip')
CSB_DIR = os.environ.get('CSB_DIR', os.path.join(ROOT, 'build', 'csb-clean'))
OUT_DB = os.path.join(ROOT, 'build', 'stl.duckdb')
TMP_DB = os.path.join(ROOT, 'build', 'N1', 'stl.building.duckdb')
N2_CODE = os.path.join(ROOT, 'research', 'chapters', 'N2-closure-classes.csv')
N2_SQL = os.path.join(ROOT, 'build', 'N2', 'closure_class.sql')
CW = os.path.join(RAW, 'city-services', 'arcgis', 'cityworks-service', 'layers')
WARDS = os.path.join(RAW, 'city-services', 'arcgis', 'layers', 'maps8_BOUNDARIES_Wards.geojson')
LOG = []
T0 = time.time()


def log(msg):
    line = f"[{time.time() - T0:6.1f}s] {msg}"
    print(line, flush=True)
    LOG.append(line)


def insert_rows(con, table, columns, rows):
    """Create `table` from Python tuples via Arrow (executemany is slow in DuckDB)."""
    names = [c.split()[0] for c in columns]
    data = {n: [r[i] for r in rows] for i, n in enumerate(names)}
    con.register('_rows', pa.table(data) if rows else pa.table({n: pa.array([], pa.string()) for n in names}))
    casts = ', '.join(f'CAST({c.split()[0]} AS {c.split()[1]}) AS {c.split()[0]}' for c in columns)
    con.execute(f'CREATE TABLE {table} AS SELECT {casts} FROM _rows')
    con.unregister('_rows')


def q1(con, sql):
    return con.execute(sql).fetchone()


# ---------------------------------------------------------------- 311 input
def ensure_clean_csb():
    """The city's CSVs contain invalid UTF-8. Recreate build/csb-clean/ from
    csb.zip if it is missing, dropping invalid bytes (same as `iconv -c`)."""
    if glob.glob(os.path.join(CSB_DIR, '20*.csv')):
        return
    os.makedirs(CSB_DIR, exist_ok=True)
    with zipfile.ZipFile(CSB_ZIP) as z:
        for name in z.namelist():
            if not name.endswith('.csv'):
                continue
            data = z.read(name).decode('utf-8', errors='ignore')
            with open(os.path.join(CSB_DIR, os.path.basename(name)), 'w', encoding='utf-8') as fh:
                fh.write(data)
    log(f'recreated {CSB_DIR} from csb.zip')


def load_311(con):
    con.execute(f"""
        CREATE TABLE csb_rows AS
        SELECT * FROM read_csv('{CSB_DIR}/*.csv', all_varchar=true, header=true, filename=true)""")
    n_rows, n_ids = q1(con, "SELECT count(*), count(DISTINCT REQUESTID) FROM csb_rows")
    log(f'311 rows {n_rows:,}; distinct REQUESTID {n_ids:,}')
    # One row per REQUESTID. Duplicate rows differ only in CALLERTYPE (13.7k ids)
    # and PUBLICRESOLUTION (148 ids); keep every caller type, the longest text.
    con.execute(r"""
        CREATE TABLE requests_base AS
        WITH r AS (
          SELECT TRY_CAST(REQUESTID AS BIGINT) AS request_id,
                 trim(PROBLEMCODE) AS problem_code,
                 trim(PLAIN_ENGLISH_NAME_FOR_PROBLEMCODE) AS type_name,
                 trim(DESCRIPTION) AS description,
                 trim("GROUP") AS grp,
                 trim(PARENT_NODE) AS parent_node,
                 trim(GRANDPARENT_NODE) AS grandparent_node,
                 nullif(trim(regexp_replace(coalesce(SUBMITTO, ''), '[,\s]+$', '')), '') AS submit_to,
                 upper(trim(CALLERTYPE)) AS callertype,
                 trim(STATUS) AS status,
                 TRY_CAST(DATETIMEINIT AS TIMESTAMP) AS ts_init,
                 TRY_CAST(DATETIMECLOSED AS TIMESTAMP) AS ts_closed,
                 TRY_CAST(DATECANCELLED AS TIMESTAMP) AS ts_cancelled,
                 TRY_CAST(DATEINVTDONE AS TIMESTAMP) AS ts_invt_done,
                 TRY_CAST(PRJCOMPLETEDATE AS TIMESTAMP) AS ts_promised,
                 nullif(trim(PUBLICRESOLUTION), '') AS resolution,
                 trim(WARD) AS ward_raw,
                 trim(NEIGHBORHOOD) AS neighborhood,
                 trim(PROBZIP) AS probzip,
                 nullif(trim(PROBADDRESS), '') AS addr_raw,
                 trim(PROBADDTYPE) AS addr_type,
                 TRY_CAST(SRX AS DOUBLE) AS srx,
                 TRY_CAST(SRY AS DOUBLE) AS sry,
                 regexp_extract(filename, '(\d{4})\.csv$', 1) AS src_year
          FROM csb_rows)
        SELECT request_id,
               first(problem_code) AS problem_code, first(type_name) AS type_name,
               first(description) AS description, first(grp) AS grp,
               first(parent_node) AS parent_node, first(grandparent_node) AS grandparent_node,
               first(submit_to) AS submit_to,
               list_sort(list_distinct(list(coalesce(callertype, 'NULL')))) AS callertypes,
               count(*) AS source_rows,
               first(status) AS status,
               first(ts_init) AS ts_init, first(ts_closed) AS ts_closed,
               first(ts_cancelled) AS ts_cancelled, first(ts_invt_done) AS ts_invt_done,
               first(ts_promised) AS ts_promised,
               arg_max(resolution, length(coalesce(resolution, ''))) AS resolution,
               first(ward_raw) AS ward_raw, first(neighborhood) AS neighborhood,
               first(probzip) AS probzip, first(addr_raw) AS addr_raw, first(addr_type) AS addr_type,
               first(srx) AS srx, first(sry) AS sry, first(src_year) AS src_year
        FROM r WHERE request_id IS NOT NULL
        GROUP BY request_id""")
    con.execute("DROP TABLE csb_rows")
    log(f"requests_base {q1(con, 'SELECT count(*) FROM requests_base')[0]:,} rows")


# ---------------------------------------------------------------- reference files
def load_reference(con):
    led = os.path.join(FILES, 'forestry-service-records.csv')
    con.execute(f"""
        CREATE TABLE ledger AS
        SELECT trim(PARCEL) AS parcel, trim(HANDLE) AS handle, trim(CITYBLOCK) AS cityblock,
               trim(PROPERTYTYPE) AS property_type, trim(SERVICETYPE) AS service_type,
               TRY_CAST(SERVICEAMOUNT AS DOUBLE) AS service_amount,
               TRY_CAST(SERVICEDATE AS TIMESTAMP) AS ts_service,
               CAST(TRY_CAST(SERVICEDATE AS TIMESTAMP) AS DATE) AS service_date,
               CAST(TRY_CAST(LASTDATE AS TIMESTAMP) AS DATE) AS last_date,
               trim(LEGACY) AS legacy
        FROM read_csv('{led}', all_varchar=true, header=true)""")
    log(f"ledger {q1(con, 'SELECT count(*) FROM ledger')[0]:,} rows")
    # One cut = one distinct (parcel, service date, service type). The ledger repeats many
    # rows (most pre-2021 LEGACY rows twice), so rows overcount cuts.
    con.execute("""
        CREATE TABLE cuts AS
        SELECT parcel, any_value(handle) AS handle, any_value(property_type) AS property_type, service_type, service_date,
               count(*) AS ledger_rows
        FROM ledger
        WHERE service_type IN ('Grass Maint', 'Weed-Grass') AND service_date >= DATE '1995-01-01'
        GROUP BY parcel, service_type, service_date""")

    msd = os.path.join(RAW, 'msd', 'msd_parcels_stl_city_attrs.jsonl')
    # Explicit column whitelist: OWNER_NAME is never parsed into the database.
    con.execute(f"""
        CREATE TABLE parcels AS
        SELECT properties.* FROM read_json('{msd}', format='newline_delimited',
          columns={{'properties': 'STRUCT(PID VARCHAR, PARENT_PID VARCHAR, PROP_ADD VARCHAR, PROP_ZIP VARCHAR, LUC VARCHAR, PROPERTY_CLASS VARCHAR, LOW_STREET_NUM VARCHAR, STREET_NUM VARCHAR)'}})""")
    con.execute("ALTER TABLE parcels RENAME COLUMN PID TO pid")
    con.execute("ALTER TABLE parcels RENAME COLUMN PARENT_PID TO handle")
    log(f"parcels (MSD) {q1(con, 'SELECT count(*) FROM parcels')[0]:,} rows")

    lra = os.path.join(FILES, 'LRA_INVENTORY.csv')
    con.execute(f"""
        CREATE TABLE lra AS
        SELECT trim(ParcelId) AS parcel_id, trim(Parcel_Status) AS parcel_status, trim(Usage) AS usage,
               trim(Address) AS address, TRY_CAST(WARD AS INT) AS ward,
               trim(NeighborhoodName) AS neighborhood, trim(PropertyType) AS property_type,
               trim(Property_Source) AS property_source
        FROM read_csv('{lra}', all_varchar=true, header=true)""")
    log(f"lra {q1(con, 'SELECT count(*) FROM lra')[0]:,} rows")

    fmp = os.path.join(FILES, 'forestry-maintenance-properties.csv')
    con.execute(f"""
        CREATE TABLE maint_props AS
        SELECT trim(CATEGORY) AS category, trim(HANDLE) AS handle, trim(PARCELID) AS parcel_id,
               trim(PROPERTYADDRESS) AS address
        FROM read_csv('{fmp}', all_varchar=true, header=true)""")
    log(f"maint_props {q1(con, 'SELECT count(*) FROM maint_props')[0]:,} rows")

    # Cityworks samples: whitelisted fields only.
    rows = []
    for fname, src in [('WO_Easement_Tree_Removals_New_6955.json', 'tree_removal'),
                       ('WO_Easement_Trims_6942.json', 'tree_trim'),
                       ('Forest_ReLeaf_Completed_Planting_WOs_6862.json', 'planting_completed'),
                       ('WO_Forest_ReLeaf_Tree_Planting_6861.json', 'planting_open')]:
        d = json.load(open(os.path.join(CW, fname)))
        for ft in d.get('features', []):
            a = ft.get('attributes') or ft.get('properties') or {}
            rows.append((src, a.get('WORKORDERID'), a.get('Description'), a.get('Priority'),
                         a.get('Status'), a.get('ProjStartDate'), a.get('ProjFinishDate'),
                         a.get('ActualFinishDate'), a.get('WoAddress'),
                         a.get('WOXCoordinate'), a.get('WOYCoordinate'), d.get('count')))
    insert_rows(con, 'wo_tree', ['source VARCHAR', 'workorder_id BIGINT', 'description VARCHAR',
                'priority VARCHAR', 'status VARCHAR', 'proj_start_ms BIGINT', 'proj_finish_ms BIGINT',
                'actual_finish_ms BIGINT', 'address VARCHAR', 'x DOUBLE', 'y DOUBLE', 'layer_count BIGINT'], rows)
    # Cityworks dates are epoch milliseconds in UTC; 311 times are Central. Convert to Central.
    con.execute("""CREATE OR REPLACE TABLE wo_tree AS SELECT * EXCLUDE (proj_start_ms, proj_finish_ms, actual_finish_ms),
        timezone('America/Chicago', to_timestamp(proj_start_ms / 1000.0)) AS proj_start,
        timezone('America/Chicago', to_timestamp(proj_finish_ms / 1000.0)) AS proj_finish,
        timezone('America/Chicago', to_timestamp(actual_finish_ms / 1000.0)) AS actual_finish FROM wo_tree""")
    rows = []
    for fname, src in [('potholes_closed_3321.json', 'closed_sample'), ('potholes_open_3320.json', 'open')]:
        d = json.load(open(os.path.join(CW, fname)))
        for ft in d.get('features', []):
            a = ft.get('attributes') or ft.get('properties') or {}
            rows.append((src, a.get('REQUESTID'), a.get('Description'), a.get('Status'),
                         a.get('DateTimeInit'), a.get('DateTimeClosed'), a.get('ProbAddress'),
                         a.get('SRX'), a.get('SRY')))
    insert_rows(con, 'cw_potholes', ['source VARCHAR', 'request_id BIGINT', 'description VARCHAR', 'status VARCHAR',
                'init_ms BIGINT', 'closed_ms BIGINT', 'address VARCHAR', 'x DOUBLE', 'y DOUBLE'], rows)
    con.execute("""CREATE OR REPLACE TABLE cw_potholes AS SELECT * EXCLUDE (init_ms, closed_ms),
        timezone('America/Chicago', to_timestamp(init_ms / 1000.0)) AS ts_init,
        timezone('America/Chicago', to_timestamp(closed_ms / 1000.0)) AS ts_closed FROM cw_potholes""")
    log(f"wo_tree {q1(con, 'SELECT count(*) FROM wo_tree')[0]:,}; cw_potholes {q1(con, 'SELECT count(*) FROM cw_potholes')[0]:,}")

    # Ward polygons, kept as GeoJSON text (no spatial extension needed).
    gj = json.load(open(WARDS))
    insert_rows(con, 'wards', ['ward VARCHAR', 'geojson VARCHAR'],
                [(f"{int(f['properties']['Ward']):02d}", json.dumps(f['geometry'])) for f in gj['features']])
    return gj


# ---------------------------------------------------------------- addresses
def build_addresses(con):
    raws = set()
    for sql in ["SELECT DISTINCT addr_raw FROM requests_base",
                "SELECT DISTINCT PROP_ADD FROM parcels", "SELECT DISTINCT address FROM lra",
                "SELECT DISTINCT address FROM maint_props", "SELECT DISTINCT address FROM wo_tree",
                "SELECT DISTINCT address FROM cw_potholes"]:
        raws.update(r[0] for r in con.execute(sql).fetchall() if r[0])
    rows = []
    for a in raws:
        n = norm(a)
        num, street = parts(n)
        if num is not None and num > 99999:  # parcel ids typed into the address field
            num, street = None, n
        label = block(n) if num is not None or '&' in n.split() else street
        # never publish a long number (parcel ids typed as addresses)
        label = ' '.join(t for t in label.split() if not (t.isdigit() and len(t) > 5))
        rows.append((a, n, num, street, label))
    insert_rows(con, 'addr_lookup', ['addr_raw VARCHAR', 'addr_norm VARCHAR', 'house_num INTEGER',
                                     'street VARCHAR', 'block_label VARCHAR'], rows)
    log(f"addr_lookup {len(rows):,} distinct raw addresses normalised")


def assign_wards(con, gj):
    """File WARD is already the current 14-ward plan for all years (observed).
    Polygons fill the ~1% of rows with a missing or malformed WARD, and a
    sample measures agreement between the file and the polygons."""
    from matplotlib.path import Path
    polys = []
    for f in gj['features']:
        w = f"{int(f['properties']['Ward']):02d}"
        g = f['geometry']
        rings = [g['coordinates'][0]] if g['type'] == 'Polygon' else [p[0] for p in g['coordinates']]
        for ring in rings:
            polys.append((w, Path(np.array(ring))))

    def locate(lon, lat):
        pts = np.column_stack([lon, lat])
        out = np.array([None] * len(pts), dtype=object)
        for w, p in polys:
            m = p.contains_points(pts)
            out[m & (out == None)] = w  # noqa: E711
        return out

    need = con.execute("""SELECT request_id, lon, lat FROM requests_tmp
                          WHERE ward_file IS NULL AND lon IS NOT NULL""").fetchall()
    if need:
        ids = [r[0] for r in need]
        w = locate(np.array([r[1] for r in need]), np.array([r[2] for r in need]))
        insert_rows(con, 'wfill', ['request_id BIGINT', 'ward_geo VARCHAR'], list(zip(ids, w.tolist())))
    else:
        insert_rows(con, 'wfill', ['request_id BIGINT', 'ward_geo VARCHAR'], [])
    samp = con.execute("""SELECT * FROM (SELECT ward_file, lon, lat FROM requests_tmp
                          WHERE ward_file IS NOT NULL AND lon IS NOT NULL AND ts_init >= TIMESTAMP '2025-01-01')
                          USING SAMPLE 20000 ROWS (reservoir, 7)""").fetchall()
    w = locate(np.array([r[1] for r in samp]), np.array([r[2] for r in samp]))
    agree = sum(1 for r, g in zip(samp, w) if g == r[0])
    inside = sum(1 for g in w if g is not None)
    log(f"ward polygons: filled {len(need):,} rows lacking WARD; sample agreement {agree}/{inside} "
        f"({100 * agree / max(inside, 1):.1f}%) of {len(samp)} sampled 2025-26 points inside a ward")
    return {'ward_fill_rows': len(need), 'ward_agree': agree, 'ward_sample_inside': inside, 'ward_sample': len(samp)}


def build_requests(con, gj):
    con.execute(r"""
        CREATE TABLE requests_tmp AS
        SELECT b.*,
               CASE WHEN regexp_full_match(b.ward_raw, '\d{1,3}') AND TRY_CAST(b.ward_raw AS INT) BETWEEN 1 AND 14
                    THEN lpad(CAST(TRY_CAST(b.ward_raw AS INT) AS VARCHAR), 2, '0') END AS ward_file,
               CASE WHEN b.srx BETWEEN -10070000 AND -10020000 THEN b.srx / 6378137.0 * 180 / pi() END AS lon,
               CASE WHEN b.sry BETWEEN 4640000 AND 4700000
                    THEN (2 * atan(exp(b.sry / 6378137.0)) - pi() / 2) * 180 / pi() END AS lat
        FROM requests_base b""")
    stats = assign_wards(con, gj)
    con.execute(r"""
        CREATE TABLE requests AS
        SELECT t.request_id, t.problem_code, t.type_name, t.description, t.grp, t.parent_node,
               t.grandparent_node, t.submit_to,
               t.callertypes, t.source_rows,
               CASE WHEN list_has_any(t.callertypes, ['WEB','PHONE','EMAIL','CHAT','TWITTER','LETTER']) THEN 'resident'
                    WHEN list_contains(t.callertypes, 'NSO') THEN 'staff'
                    WHEN list_contains(t.callertypes, 'INDETERMINATE') THEN 'indeterminate'
                    ELSE 'other' END AS channel_group,
               t.status,
               CASE WHEN upper(t.status) = 'CLOSED' AND t.ts_closed IS NOT NULL THEN 'closed'
                    WHEN upper(t.status) = 'CLOSED' THEN 'closed_no_date'
                    WHEN upper(t.status) = 'CANCEL' THEN 'cancelled'
                    ELSE 'open' END AS status_group,
               t.ts_init, t.ts_closed, t.ts_cancelled, t.ts_invt_done, t.ts_promised,
               CAST(t.ts_init AS DATE) AS init_date,
               year(t.ts_init) AS init_year,
               CAST(year(t.ts_init) AS VARCHAR) || 'Q' || CAST(quarter(t.ts_init) AS VARCHAR) AS init_quarter,
               CASE WHEN t.ts_init >= TIMESTAMP '2025-05-16' THEN 'after' ELSE 'before' END AS tornado_period,
               CASE WHEN upper(t.status) = 'CLOSED' AND t.ts_closed IS NOT NULL
                    THEN epoch(t.ts_closed - t.ts_init) / 86400.0 END AS days_to_close,
               epoch(t.ts_promised - t.ts_init) / 86400.0 AS promise_days,
               t.resolution,
               lower(trim(regexp_replace(coalesce(t.resolution, ''), '\s+', ' ', 'g'))) AS res_key,
               coalesce(t.ward_file, f.ward_geo) AS ward,
               CASE WHEN t.ward_file IS NOT NULL THEN 'file' WHEN f.ward_geo IS NOT NULL THEN 'polygon' END AS ward_source,
               CASE WHEN coalesce(t.ward_file, f.ward_geo) IN ('01','02','03','04','05') THEN '1-5'
                    WHEN coalesce(t.ward_file, f.ward_geo) IN ('06','07','08','09') THEN '6-9'
                    WHEN coalesce(t.ward_file, f.ward_geo) IN ('10','11','12','13','14') THEN '10-14' END AS ward_group,
               t.ward_raw, t.neighborhood, t.probzip,
               t.addr_raw, t.addr_type,
               coalesce(a.addr_norm, '') AS addr_norm, a.house_num, a.street, a.block_label,
               t.srx, t.sry, t.lon, t.lat, t.src_year
        FROM requests_tmp t
        LEFT JOIN wfill f USING (request_id)
        LEFT JOIN addr_lookup a ON a.addr_raw = t.addr_raw""")
    con.execute("DROP TABLE requests_tmp")
    con.execute("DROP TABLE requests_base")
    # Public-safe columns. SUBMITTO holds a few personal names (values used 1-3 times);
    # any routing value used fewer than 20 times is pooled. Resolution text used fewer
    # than 5 times is withheld (free text may name people); e-mail addresses are removed.
    con.execute(r"""
        CREATE OR REPLACE TABLE requests AS
        SELECT r.*,
               CASE WHEN r.submit_to IS NULL THEN NULL
                    WHEN count(*) OVER (PARTITION BY r.submit_to) >= 20 THEN r.submit_to
                    ELSE 'Other (pooled)' END AS division,
               CASE WHEN r.resolution IS NULL THEN NULL
                    WHEN count(*) OVER (PARTITION BY r.res_key) < 5 THEN '[uncommon free text withheld]'
                    ELSE regexp_replace(r.resolution, '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}', '[e-mail removed]', 'g')
               END AS resolution_public
        FROM requests r""")
    log(f"requests {q1(con, 'SELECT count(*) FROM requests')[0]:,} rows")
    return stats


# ---------------------------------------------------------------- closure classes
PROVISIONAL_SQL = r"""
CASE
  WHEN @K = '' THEN 'blank'
  WHEN @K LIKE '%work order%' THEN 'converted'
  WHEN regexp_matches(@K, 'no violation|no evidence|no service|unable to (locate|confirm|find|gain)|not located|could not (be )?locat|gone upon|gone on|no problem found|nothing found|not city|private property|no vehicle found|no strays|duplicate|meets minimum|abated (before|at time)|not enough evidence|no response required|no forestry violation|already under notice|does not meet|no action') THEN 'no_action'
  WHEN regexp_matches(@K, 'schedul|rotation|referred|refer to|will be|forwarded|sent to|tagged|assigned|added to|placed on|pending|to be |in progress|report to|notified|notice of violation|investigat|issued|summons|approved for') THEN 'handed_off'
  WHEN regexp_matches(@K, 'complete|collected|collection made|repair|removed|replaced|fixed|\bcut\b|picked up|cleaned|restored|filled|towed|abated|done|resolved|installed|trimmed|placed|moved|uprighted|patched|painted') THEN 'done'
  ELSE 'info_other'
END"""


def build_closure_classes(con):
    """Closure class per request. Order: N2's reviewed per-type table
    (research/chapters/N2-closure-classes.csv: PROBLEMCODE + exact text); then
    N2's SQL classifier for other years (build/N2/closure_class.sql: per-type
    overrides, then the text table, unlisted text -> info_other); N1's
    provisional regex only if N2's files are absent. Text is compared as
    lower(trim(collapse spaces)), the same normalisation N2 uses."""
    src = 'N1-provisional'
    con.execute("CREATE TABLE n2_code_classes (problem_code VARCHAR, res_key VARCHAR, class VARCHAR, n BIGINT, rule VARCHAR)")
    if os.path.exists(N2_CODE):
        con.execute(rf"""
            INSERT INTO n2_code_classes
            SELECT problem_code, res_key, arg_max(class, n), max(n), arg_max(rule, n) FROM (
              SELECT trim(PROBLEMCODE) AS problem_code,
                     lower(trim(regexp_replace(coalesce(resolution_text, ''), '\s+', ' ', 'g'))) AS res_key,
                     lower(trim(class)) AS class, TRY_CAST(n AS BIGINT) AS n, rule_or_judgement AS rule
              FROM read_csv('{N2_CODE}', all_varchar=true, header=true))
            GROUP BY 1, 2""")
        src = 'N2'
    have_sql = os.path.exists(N2_SQL)
    if have_sql:
        with open(N2_SQL) as fh:
            for stmt in sql_statements(fh.read()):
                con.execute(stmt)
    else:
        con.execute("CREATE TABLE closure_text_class (text_norm VARCHAR, class VARCHAR, rule VARCHAR)")
        con.execute("CREATE TABLE closure_type_override (problemcode VARCHAR, text_norm VARCHAR, class VARCHAR, rule VARCHAR)")
    fallback = ("CASE WHEN r.res_key = '' THEN 'blank' ELSE 'info_other' END" if have_sql
                else PROVISIONAL_SQL.replace('@K', 'r.res_key'))
    fallback_src = "'N2:sql-unlisted-text'" if have_sql else "'N1:provisional-rule'"
    con.execute(f"""
        CREATE TABLE closure_class AS
        SELECT r.request_id,
               CASE WHEN r.status_group = 'cancelled' THEN 'cancelled'
                    WHEN r.status_group IN ('closed', 'closed_no_date')
                    THEN coalesce(c.class, o.class, t.class, ({fallback}))
               END AS closure_class,
               CASE WHEN r.status_group = 'cancelled' THEN 'status'
                    WHEN r.status_group IN ('closed', 'closed_no_date')
                    THEN CASE WHEN c.class IS NOT NULL THEN 'N2:type+text'
                              WHEN o.class IS NOT NULL THEN 'N2:sql-override'
                              WHEN t.class IS NOT NULL THEN 'N2:sql-text'
                              WHEN r.res_key = '' THEN 'blank'
                              ELSE {fallback_src} END
               END AS class_source,
               coalesce(c.rule, o.rule, t.rule) AS class_rule
        FROM requests r
        LEFT JOIN n2_code_classes c ON c.problem_code = r.problem_code AND c.res_key = r.res_key
        LEFT JOIN closure_type_override o ON trim(o.problemcode) = r.problem_code AND o.text_norm = r.res_key
        LEFT JOIN closure_text_class t ON t.text_norm = r.res_key""")
    cov = con.execute("""SELECT class_source, count(*) FROM closure_class c JOIN requests r USING (request_id)
                         WHERE r.status_group = 'closed' AND r.init_year >= 2024 GROUP BY 1 ORDER BY 2 DESC""").fetchall()
    cov_all = con.execute("""SELECT class_source, count(*) FROM closure_class c JOIN requests r USING (request_id)
                         WHERE r.status_group = 'closed' GROUP BY 1 ORDER BY 2 DESC""").fetchall()
    log(f"closure_class source={src}; closed 2024+ by source: {cov}; all years: {cov_all}")
    return src, cov


# ---------------------------------------------------------------- parcels
def build_request_parcel(con):
    con.execute("""
        CREATE TABLE parcel_addr AS
        SELECT a.addr_norm, p.pid, p.handle, 'msd' AS src
        FROM parcels p JOIN addr_lookup a ON a.addr_raw = p.PROP_ADD WHERE a.addr_norm <> ''
        UNION ALL
        SELECT a.addr_norm, l.parcel_id, NULL, 'lra' FROM lra l JOIN addr_lookup a ON a.addr_raw = l.address WHERE a.addr_norm <> ''
        UNION ALL
        SELECT a.addr_norm, m.parcel_id, m.handle, 'maint' FROM maint_props m JOIN addr_lookup a ON a.addr_raw = m.address WHERE a.addr_norm <> ''""")
    # Range parcels (e.g. 1234-1238 EXAMPLE AV) for numbers inside a recorded range, same parity.
    con.execute("""
        CREATE TABLE parcel_ranges AS
        SELECT p.pid, p.handle, a.street, TRY_CAST(p.LOW_STREET_NUM AS INT) AS lo, TRY_CAST(p.STREET_NUM AS INT) AS hi
        FROM parcels p JOIN addr_lookup a ON a.addr_raw = p.PROP_ADD
        WHERE TRY_CAST(p.LOW_STREET_NUM AS INT) < TRY_CAST(p.STREET_NUM AS INT) AND a.street <> ''""")
    con.execute("CREATE TABLE cut_parcels AS SELECT DISTINCT parcel FROM cuts")
    # one parcel per normalised address: prefer a parcel that appears in the cut ledger, then LRA, then MSD
    con.execute("""
        CREATE TABLE addr_parcel AS
        SELECT addr_norm,
               arg_min(pid, (CASE WHEN pid IN (SELECT parcel FROM cut_parcels) THEN 0 ELSE 1 END,
                             CASE src WHEN 'lra' THEN 0 WHEN 'msd' THEN 1 ELSE 2 END, pid)) AS pid,
               arg_min(src, (CASE WHEN pid IN (SELECT parcel FROM cut_parcels) THEN 0 ELSE 1 END,
                             CASE src WHEN 'lra' THEN 0 WHEN 'msd' THEN 1 ELSE 2 END, pid)) AS src,
               count(DISTINCT pid) AS n_candidates
        FROM parcel_addr GROUP BY addr_norm""")
    con.execute("""
        CREATE TABLE request_parcel AS
        WITH ra AS (SELECT DISTINCT addr_norm, house_num, street FROM requests
                    WHERE addr_norm <> '' AND house_num IS NOT NULL),
        exact AS (SELECT ra.addr_norm, ap.pid, 'exact:' || ap.src AS method, ap.n_candidates
                  FROM ra JOIN addr_parcel ap USING (addr_norm)),
        rng AS (SELECT ra.addr_norm, min(pr.pid) AS pid, 'range:msd' AS method, count(*) AS n_candidates
                FROM ra JOIN parcel_ranges pr ON pr.street = ra.street
                     AND ra.house_num BETWEEN pr.lo AND pr.hi AND (ra.house_num % 2) = (pr.lo % 2)
                WHERE ra.addr_norm NOT IN (SELECT addr_norm FROM exact)
                GROUP BY ra.addr_norm),
        -- same number and street name, street type ignored ("1234 EXAMPLE" = "1234 EXAMPLE AV"); unique only
        pnt AS (SELECT a.house_num, regexp_replace(a.street, ' (AV|ST|BLVD|DR|PL|RD|CT|TER|LN|PKWY|WAY|CIR|ALY|SQ|PLZ|HWY)$', '') AS core,
                       min(pa.pid) AS pid, count(DISTINCT pa.pid) AS n
                FROM parcel_addr pa JOIN (SELECT DISTINCT addr_norm, house_num, street FROM addr_lookup WHERE house_num IS NOT NULL) a
                     USING (addr_norm)
                GROUP BY 1, 2),
        nt AS (SELECT ra.addr_norm, pnt.pid, 'street-type-free' AS method, pnt.n AS n_candidates
               FROM ra JOIN pnt ON pnt.house_num = ra.house_num
                    AND pnt.core = regexp_replace(ra.street, ' (AV|ST|BLVD|DR|PL|RD|CT|TER|LN|PKWY|WAY|CIR|ALY|SQ|PLZ|HWY)$', '')
               WHERE pnt.n = 1 AND ra.addr_norm NOT IN (SELECT addr_norm FROM exact)
                     AND ra.addr_norm NOT IN (SELECT addr_norm FROM rng)),
        m AS (SELECT * FROM exact UNION ALL SELECT * FROM rng UNION ALL SELECT * FROM nt)
        SELECT r.request_id, m.pid, m.method, m.n_candidates,
               p.handle, p.LUC AS luc, p.PROPERTY_CLASS AS property_class,
               (m.pid IN (SELECT parcel_id FROM lra)) AS is_lra
        FROM requests r JOIN m USING (addr_norm)
        LEFT JOIN parcels p ON p.pid = m.pid""")
    log(f"request_parcel {q1(con, 'SELECT count(*) FROM request_parcel')[0]:,} rows")


def sql_statements(sql):
    """Split a .sql file on ';' at line end; drop comment-only chunks."""
    out = []
    for chunk in sql.split(';\n'):
        body = '\n'.join(l for l in chunk.splitlines() if not l.strip().startswith('--')).strip()
        if body:
            out.append(body)
    return out


def main():
    os.makedirs(os.path.dirname(TMP_DB), exist_ok=True)
    if os.path.exists(TMP_DB):
        os.remove(TMP_DB)
    ensure_clean_csb()
    con = duckdb.connect(TMP_DB)
    con.execute("SET preserve_insertion_order = false")
    load_311(con)
    gj = load_reference(con)
    build_addresses(con)
    wstats = build_requests(con, gj)
    cls_src, cls_cov = build_closure_classes(con)
    build_request_parcel(con)
    asof_ts = q1(con, "SELECT max(ts_init) FROM requests")[0]
    asof = asof_ts.date()
    ledger_max = q1(con, "SELECT max(service_date) FROM cuts")[0]
    con.execute("CREATE TABLE meta (key VARCHAR, value VARCHAR)")
    meta = {'asof': str(asof), 'asof_ts': str(asof_ts), 'ledger_max_date': str(ledger_max), 'built_at': time.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'closure_class_source': cls_src, 'n2_code_file': N2_CODE if os.path.exists(N2_CODE) else '',
            'n2_code_file_mtime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(N2_CODE))) if os.path.exists(N2_CODE) else '',
            **{k: str(v) for k, v in wstats.items()}}
    con.executemany("INSERT INTO meta VALUES (?, ?)", list(meta.items()))
    with open(os.path.join(HERE, 'measures.sql')) as fh:
        sql = fh.read()
    for stmt in sql_statements(sql):
        try:
            con.execute(stmt)
        except Exception as e:
            raise RuntimeError(f'measures.sql failed at: {stmt[:200]}') from e
    log('measures.sql applied')
    counts = {t: q1(con, f'SELECT count(*) FROM "{t}"')[0] for (t,) in con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' ORDER BY 1").fetchall()}
    con.execute("CHECKPOINT")
    con.close()
    os.replace(TMP_DB, OUT_DB)
    if os.path.exists(TMP_DB + '.wal'):
        os.remove(TMP_DB + '.wal')
    manifest = {'meta': meta, 'table_rows': counts, 'log': LOG, 'seconds': round(time.time() - T0, 1)}
    with open(os.path.join(ROOT, 'build', 'N1', 'manifest.json'), 'w') as fh:
        json.dump(manifest, fh, indent=1, default=str)
    log(f'wrote {OUT_DB}')


if __name__ == '__main__':
    main()
