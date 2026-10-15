"""N2 step 4b: joins of 311 requests to independent completion records found on disk, for the register.

A. Vacant building unsecured (311 'Vacnt Bldg Unsecured') -> Building Division board-up layer
   (maps8_BUILDING_DIVISION_Boardups.geojson: ParcelID, ADDRESS, DateCreated, DateBoardedUp).
B. LRA demolition submissions (311 'LRA Demo Submission') and building collapse -> Building Division
   demolition permits (maps8_BUILDING_DIVISION_Demolitions.geojson: ADDRESS, DateSubmitted,
   DateIssued, DateClosed, PermitStatus). Owner/contractor fields are never read into the output.
C. Tree planting requests -> Cityworks Forest ReLeaf completed planting work orders (sample of 1,500).
D. Potholes: Cityworks closed-pothole sample vs the 311 file, same REQUESTID (consistency, not independence).

Address join uses the project normaliser (scripts/synthesis-checks/common.py norm()). Address-level rows
are computation only; outputs are aggregates. Run: .venv/bin/python -I scripts/night/N2/05_joins.py
"""
import json, pathlib, re, sys, datetime as dt
import duckdb

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from classes import classify  # noqa: E402

ROOT = HERE.parents[2]
B = ROOT / "build" / "N2"
P = B / "private" / "csb_2024_2026.parquet"
L = ROOT / "data/raw/city-services/arcgis/layers"
CW = ROOT / "data/raw/city-services/arcgis/cityworks-service/layers"

ABBR = {'AVENUE': 'AV', 'AVE': 'AV', 'STREET': 'ST', 'BOULEVARD': 'BLVD', 'DRIVE': 'DR', 'PLACE': 'PL',
        'ROAD': 'RD', 'COURT': 'CT', 'TERRACE': 'TER', 'LANE': 'LN', 'PARKWAY': 'PKWY'}
def norm(a):
    a = (a or '').upper().split(',')[0]
    a = re.sub(r'\bST LOUIS\b.*$', '', a)
    a = re.sub(r'[^A-Z0-9 ]', ' ', a)
    return ' '.join(ABBR.get(t, t) for t in a.split())

def ms(v):
    return dt.datetime.utcfromtimestamp(v / 1000) if isinstance(v, (int, float)) else None

con = duckdb.connect()
con.create_function("norm_addr", norm, ["VARCHAR"], "VARCHAR")
con.create_function("classify_cls", lambda pc, t: classify(pc, t)[0], ["VARCHAR", "VARCHAR"], "VARCHAR")
OUT = {}

# ---------- A. board-ups
bu = [f["properties"] for f in json.loads((L / "maps8_BUILDING_DIVISION_Boardups.geojson").read_text())["features"]]
con.execute("CREATE TABLE boardup (addr VARCHAR, created TIMESTAMP, boarded TIMESTAMP)")
con.executemany("INSERT INTO boardup VALUES (?,?,?)",
                [(norm(p.get("ADDRESS")), ms(p.get("DateCreated")), ms(p.get("DateBoardedUp"))) for p in bu])
con.execute(f"""
CREATE TABLE vb AS
SELECT REQUESTID, STATUS, t_init, t_closed, PUBLICRESOLUTION, norm_addr(PROBADDRESS) AS addr,
       coalesce(trim(PUBLICRESOLUTION),'') AS txt,
       CASE WHEN STATUS='CLOSED' THEN classify_cls(PROBLEMCODE, PUBLICRESOLUTION) WHEN STATUS='CANCEL' THEN 'cancelled' ELSE 'open' END AS cls
FROM '{P}' WHERE PROBLEMCODE = 'Vacnt Bldg Unsecured' AND t_init < TIMESTAMP '2026-10-13'
""")
con.execute("""
CREATE TABLE vbj AS
SELECT vb.*,
  (SELECT min(b.boarded) FROM boardup b WHERE b.addr = vb.addr AND b.boarded >= vb.t_init - INTERVAL 1 DAY) AS first_board_after,
  (SELECT min(b.created) FROM boardup b WHERE b.addr = vb.addr AND b.created >= vb.t_init - INTERVAL 1 DAY) AS first_created_after,
  EXISTS (SELECT 1 FROM boardup b WHERE b.addr = vb.addr) AS addr_in_layer,
  EXISTS (SELECT 1 FROM boardup b WHERE b.addr = vb.addr AND b.boarded BETWEEN vb.t_init - INTERVAL 365 DAY AND vb.t_init - INTERVAL 30 DAY) AS boarded_prior_year
FROM vb
""")
def bu_stats(where, label):
    r = con.execute(f"""
      SELECT count(*), avg(addr_in_layer::INT),
        avg(coalesce(first_board_after <= t_init + INTERVAL 30 DAY, false)::INT),
        avg(coalesce(first_board_after <= t_init + INTERVAL 14 DAY, false)::INT),
        median(epoch(t_closed) - epoch(t_init)) / 86400.0,
        avg(coalesce(first_board_after <= t_init + INTERVAL 90 DAY, false)::INT),
        avg((first_board_after IS NOT NULL)::INT),
        median(epoch(first_board_after) - epoch(t_init)) / 86400.0,
        avg(boarded_prior_year::INT)
      FROM vbj WHERE {where} AND t_init < TIMESTAMP '2026-07-15'""").fetchone()
    return {"label": label, "n": r[0], "addr_in_boardup_layer": round(r[1] or 0, 3),
            "boarded_within_30d": round(r[2] or 0, 3),
            "boarded_within_14d_promise": round(r[3] or 0, 3),
            "median_days_to_close_311": round(r[4], 1) if r[4] is not None else None,
            "boarded_within_90d": round(r[5] or 0, 3),
            "boarded_any_time_after": round(r[6] or 0, 3),
            "median_days_to_boardup_if_any": round(r[7], 1) if r[7] is not None else None,
            "boarded_in_prior_year_baseline": round(r[8] or 0, 3)}
OUT["boardups"] = {
    "source": "data/raw/city-services/arcgis/layers/maps8_BUILDING_DIVISION_Boardups.geojson (33,141 rows, DateBoardedUp 2013-04-04..2026-10-08)",
    "scope": "311 'Vacnt Bldg Unsecured' filed 2024-01-01..2026-07-14 (so every request has 90 days of follow-up), address join",
    "rows": [bu_stats("TRUE", "all requests"),
             bu_stats("txt = 'referred to board up crew'", "closed 'referred to board up crew'"),
             bu_stats("txt = 'issued notice of violation'", "closed 'issued notice of violation'"),
             bu_stats("txt = 'Building already under notice'", "closed 'Building already under notice'"),
             bu_stats("cls = 'no_action'", "closed no_action (no violation, secured at inspection, ...)"),
             bu_stats("cls = 'open'", "still open"),
             bu_stats("cls = 'cancelled'", "cancelled")],
}
print(json.dumps(OUT["boardups"], indent=1))

# ---------- B. demolitions
dm = [f["properties"] for f in json.loads((L / "maps8_BUILDING_DIVISION_Demolitions.geojson").read_text())["features"]]
con.execute("CREATE TABLE demo (addr VARCHAR, submitted TIMESTAMP, issued TIMESTAMP, closed TIMESTAMP, status VARCHAR, src VARCHAR)")
con.executemany("INSERT INTO demo VALUES (?,?,?,?,?,?)",
                [(norm(p.get("ADDRESS")), ms(p.get("DateSubmitted")), ms(p.get("DateIssued")), ms(p.get("DateClosed")),
                  p.get("PermitStatus"), p.get("BidPackage_ParcelSourcingType")) for p in dm])
rows = []
for pc in ["LRA Demo Submission", "Building Collapse"]:
    r = con.execute(f"""
      WITH q AS (SELECT REQUESTID, STATUS, t_init, norm_addr(PROBADDRESS) addr FROM '{P}'
                 WHERE PROBLEMCODE = ? AND t_init < TIMESTAMP '2026-10-13'),
      j AS (SELECT q.*,
              EXISTS (SELECT 1 FROM demo d WHERE d.addr=q.addr) AS in_layer,
              EXISTS (SELECT 1 FROM demo d WHERE d.addr=q.addr AND coalesce(d.submitted,d.issued) >= q.t_init) AS permit_after,
              EXISTS (SELECT 1 FROM demo d WHERE d.addr=q.addr AND d.closed >= q.t_init AND d.status='Completed') AS completed_after
            FROM q)
      SELECT coalesce(STATUS IN ('CLOSED','CANCEL'), false) AS done_status, count(*), avg(in_layer::INT), avg(permit_after::INT), avg(completed_after::INT),
             sum(completed_after::INT)
      FROM j GROUP BY ALL ORDER BY 1""", [pc]).fetchall()
    for x in r:
        rows.append({"PROBLEMCODE": pc, "status_group": "closed or cancelled" if x[0] else "open",
                     "n": x[1], "addr_in_demolition_layer": round(x[2], 3),
                     "demolition_permit_at_address_after_filing": round(x[3], 3),
                     "completed_demolition_at_address_after_filing": round(x[4], 3),
                     "n_completed_demolition_after_filing": x[5]})
OUT["demolitions"] = {
    "source": "data/raw/city-services/arcgis/layers/maps8_BUILDING_DIVISION_Demolitions.geojson (3,767 permits; DateClosed 2018-12-20..2026-10-09)",
    "scope": "311 requests filed 2024-01-01..2026-10-12; demolition permit submitted/issued, or completed (DateClosed, PermitStatus Completed), at the same normalised address on or after the filing date",
    "rows": rows}
print(json.dumps(OUT["demolitions"], indent=1))

# ---------- C. tree planting vs Forest ReLeaf completed planting work orders (sample)
def cw(fn):
    d = json.loads((CW / fn).read_text())
    return [f.get("attributes") or f.get("properties") or f for f in d["features"]]
pl = cw("Forest_ReLeaf_Completed_Planting_WOs_6862.json")
con.execute("CREATE TABLE plant (addr VARCHAR, finished TIMESTAMP)")
con.executemany("INSERT INTO plant VALUES (?,?)", [(norm(p.get("WoAddress")), ms(p.get("ActualFinishDate"))) for p in pl])
r = con.execute(f"""
  WITH q AS (SELECT REQUESTID, STATUS, t_init, coalesce(trim(PUBLICRESOLUTION),'') txt, norm_addr(PROBADDRESS) addr FROM '{P}'
             WHERE PROBLEMCODE = 'Tree Planting requst' AND t_init BETWEEN TIMESTAMP '2024-01-01' AND TIMESTAMP '2025-06-30')
  SELECT txt = 'approved for next available planting' AS approved, count(*),
         avg(EXISTS (SELECT 1 FROM plant p WHERE p.addr=q.addr)::INT),
         avg(EXISTS (SELECT 1 FROM plant p WHERE p.addr=q.addr AND p.finished >= q.t_init)::INT)
  FROM q WHERE STATUS='CLOSED' GROUP BY ALL ORDER BY 1""").fetchall()
OUT["tree_planting"] = {
    "source": "data/raw/city-services/arcgis/cityworks-service/layers/Forest_ReLeaf_Completed_Planting_WOs_6862.json (1,500-row sample of completed planting WOs, finished 2024-09-27..2025-08-22)",
    "scope": "311 'Tree Planting requst' closed, filed 2024-01-01..2025-06-30; completed planting WO at the same normalised address after filing",
    "rows": [{"closed_approved_for_planting": bool(x[0]), "n": x[1], "addr_in_sample": round(x[2], 3),
              "planting_completed_after_filing": round(x[3], 3)} for x in r]}
print(json.dumps(OUT["tree_planting"], indent=1))

# ---------- D. potholes: Cityworks sample vs 311 file on REQUESTID
ph = cw("potholes_closed_3321.json")
con.execute("CREATE TABLE ph (REQUESTID BIGINT, closed TIMESTAMP)")
con.executemany("INSERT INTO ph VALUES (?,?)", [(int(p["REQUESTID"]), ms(p.get("DateTimeClosed"))) for p in ph])
r = con.execute(f"""SELECT count(*), count(c.REQUESTID), avg((abs(epoch(c.t_closed)-epoch(ph.closed)) < 86400)::INT),
       avg((abs(epoch(c.t_closed)-epoch(ph.closed)) < 60)::INT)
       FROM ph LEFT JOIN '{P}' c USING (REQUESTID)""").fetchone()
OUT["potholes_cityworks_sample"] = {
    "source": "data/raw/city-services/arcgis/cityworks-service/layers/potholes_closed_3321.json (1,500 closed pothole requests)",
    "n_sample": r[0], "found_in_311_file": r[1], "closed_time_within_1_day": round(r[2] or 0, 3),
    "closed_time_within_1_minute": round(r[3] or 0, 3),
    "note": "Same request records (REQUESTID), so this is the 311 system's own copy, not an independent completion record."}
print(json.dumps(OUT["potholes_cityworks_sample"], indent=1))

(B / "joins.json").write_text(json.dumps(OUT, indent=2, default=str))
