"""N2 step 5: the register of services, build/N2/register.json (+ register.csv for review).

One row per service delivered through 311. Data columns are computed from the
deduplicated 311 extract (requests filed 2025-01-01 .. 2026-10-12); the record
columns (independent completion record on disk, joined, what it would take) are
written by hand from the files probed in 04/05 and the project's research notes,
each with a source path or URL.

Run: .venv/bin/python -I scripts/night/N2/06_register.py
"""
import csv, json, pathlib, sys
import duckdb

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from classes import classify  # noqa: E402

ROOT = HERE.parents[2]
B = ROOT / "build" / "N2"
P = B / "private" / "csb_2024_2026.parquet"
J = json.loads((B / "joins.json").read_text())

bu_ref = next(r for r in J["boardups"]["rows"] if r["label"].startswith("closed 'referred"))
lra_open = next(r for r in J["demolitions"]["rows"] if r["PROBLEMCODE"] == "LRA Demo Submission" and r["status_group"] == "open")
coll_closed = next(r for r in J["demolitions"]["rows"] if r["PROBLEMCODE"] == "Building Collapse" and r["status_group"] == "closed or cancelled")
tp = next(r for r in J["tree_planting"]["rows"] if r["closed_approved_for_planting"])

L = "data/raw/city-services/arcgis/layers/"
CWL = "data/raw/city-services/arcgis/cityworks-service/layers/"
SERVICES = [
  dict(id="weeds_vacant_lot", service="Weeds and grass on vacant lots (city mowing)",
       codes=["Weeds-Vacant Lot", "Missed Cut - V Lot", "Unsatisfy Cut - VLot"],
       record="Forestry billing ledger: data/raw/stlouis-mo.gov/files/forestry-service-records.csv ('Grass Maint', 'Weed-Grass' by PARCEL and SERVICEDATE, posted to 13 Oct 2026; batched, precise to weeks)",
       record_status="yes",
       joined="yes (scripts/synthesis-checks/02_weeds_vs_ledger.py: vacant lots closed 'on schedule' 2026: cut on the parcel within 30 days 35%, by season end 63%, never in 2026 26%); N1 rebuilds this join tonight",
       take="Nothing new: the ledger is already published; run the join weekly and show the cut date on the request."),
  dict(id="weeds_vacant_bldg", service="Weeds and grass at vacant buildings (city mowing)",
       codes=["Weeds-Vacant Bldg", "Missed Cut - VBldg", "Unsatisfy Cut -VBldg"],
       record="Forestry billing ledger: data/raw/stlouis-mo.gov/files/forestry-service-records.csv ('Grass Maint', 'Weed-Grass' by PARCEL and SERVICEDATE, posted to 13 Oct 2026; batched, precise to weeks)",
       record_status="yes",
       joined="not for buildings in the first check (it reported vacant lots); the N1 ledger join covers weed codes",
       take="Nothing new: the ledger is already published; run the join weekly and show the cut date on the request."),
  dict(id="weeds_occupied", service="Weeds on occupied property (code enforcement)",
       codes=["Weeds-Occupied Ppty"],
       record="Partial: ledger rows of type 'Weed-Grass' and 'Occupied' (forced cuts billed to owners) in forestry-service-records.csv",
       record_status="partial", joined="no",
       take="Same ledger join by parcel as vacant lots; separate notice-then-cut timeline."),
  dict(id="trees_city", service="City trees: inspection, limbs down, trees down, stumps",
       codes=["Inspect City Tree", "City Tree Down", "City Tree Limb Down", "Broken/Hanging Limb", "Stump Removal"],
       record="Cityworks work-order samples: " + CWL + "WO_Easement_Tree_Removals_New_6955.json and WO_Easement_Trims_6942.json (1,500 each of 2,522 and 6,276; status NEW, no finish date). Tree inventory CITY_TREES.geojson has no dates.",
       record_status="partial (open work orders, sampled; no completion dates)",
       joined="yes (scripts/synthesis-checks/03: cancelled tree-inspection addresses appear in the work-order sample about five times as often as unrelated requests, 10.8% vs 1.9%; recall is poor); N1 rebuilds tonight",
       take="The full Cityworks work-order export with ActualFinishDate and the request-to-work-order link Cityworks already stores."),
  dict(id="tree_planting", service="Tree planting requests",
       codes=["Tree Planting requst"],
       record="Cityworks Forest ReLeaf completed-planting work orders, " + CWL + "Forest_ReLeaf_Completed_Planting_WOs_6862.json (1,500 sample, finished 27 Sep 2024 to 22 Aug 2025)",
       record_status="partial (partner programme sample)",
       joined=f"yes, tonight: of {tp['n']} requests filed Jan 2024 to Jun 2025 and closed 'approved for next available planting', {tp['planting_completed_after_filing']:.1%} match a completed planting in the sample. The sample does not cover city plantings from 311; negative result.",
       take="Forestry's own planting work orders with finish dates."),
  dict(id="potholes", service="Potholes (residential, major street, alley)",
       codes=["Potholes - Residnl", "Potholes - Major St", "Potholes - Alley"],
       record="None independent. The Cityworks pothole layer (" + CWL + "potholes_closed_3321.json) is the same request records: all 1,500 sampled REQUESTIDs are in the 311 file with the same close times (offset by time zone).",
       record_status="no (same system)", joined="yes, tonight (consistency check only)",
       take="Crew work orders or asphalt tickets with location and date, from Cityworks."),
  dict(id="cave_ins", service="Cave-ins (street, alley, sidewalk)",
       codes=["Cave-Ins"],
       record="None found on disk. Closures read 'referred to street maintenance for repair work to be scheduled'; the Street Maintenance work order is not published.",
       record_status="no", joined="no",
       take="Street Maintenance work orders from Cityworks with finish dates, linked to the request id."),
  dict(id="street_lights", service="Street lights out or damaged",
       codes=["Single Light Out", "Whole Blk Lights Out", "Light Damaged"],
       record="None. " + L + "maps8_STREETS_OneCall_StreetLights.geojson is an inventory (52,573 lights; Verification_Date on 2,931, all 2022; no repair dates).",
       record_status="no", joined="no",
       take="Traffic Division repair log or Cityworks work orders; networked outage detection was not found (research notes)."),
  dict(id="signals_signs", service="Traffic signals and signs",
       codes=["Signals out of sync", "Signal Damaged", "Signals Flashing", "Signal Dark", "Signal Bulb Out", "Signal Stuck", "Other Signal Damaged", "Critical Sign  ", "Sign needs attention"],
       record="None. " + L + "maps8_STREETS_OneCall_TrafficSignals.geojson is an inventory of 683 signals without repair dates.",
       record_status="no", joined="no", take="Traffic Division work orders."),
  dict(id="towing", service="Derelict or abandoned vehicles (towing)",
       codes=["Vehicle Towing"],
       record="None joinable. The Towed Vehicle Lookup (data/raw/tools-inventory/tow_lookup_48h.html) lists plate, state, make, model, VIN and date towed for 48 hours only, with no pick-up address; the CityStat towing chart does not render for the public. CityStat itself says 'Closed' does not necessarily indicate a tow.",
       record_status="no", joined="no",
       take="Tow-lot intake records carrying the pick-up address or the 311 request id."),
  dict(id="refuse", service="Missed refuse, bulky, yard-waste and recycling collection",
       codes=["Refuse not collected", "Bulky items missed", "Yrd Wste Not Collect", "Recycling not collec", "Rcy Pickup Missed"],
       record="None on disk. The city says refuse route data was not recorded until September 2025; new trucks carry route tablets (research/synthesis-notes.md).",
       record_status="no", joined="no",
       take="Route-completion or GPS logs from the truck tablets, by alley and date."),
  dict(id="debris_street", service="Debris in alley or street; illegal dumping reports",
       codes=["Debris-alley/street", "Illegal dumpg report"],
       record="Pickup: none. Illegal dumping: the 311 closing text is itself the enforcement outcome (summons issued, cleared by arrest, no evidence).",
       record_status="partial (enforcement outcome only)", joined="no",
       take="Street Division pickup work orders with date; for dumping, court disposition of summonses."),
  dict(id="debris_vacant", service="Debris on vacant lots and buildings (city clean-up)",
       codes=["Debris-Vacant Lot", "Debris-Vacant Bldg"],
       record="Stopped: the forestry ledger's 'Light Debris' rows fell from 2,038 in 2019 to 14 in 2022 and 1 or none a year since; 'Heavy Debris' 39 in 2025, 4 in 2026 (forestry-service-records.csv).",
       record_status="no (ledger stopped recording in 2022)", joined="no",
       take="Resume posting debris clean-ups to the ledger, as grass cuts still are."),
  dict(id="sidewalks", service="Sidewalk repair (50/50 programme)",
       codes=["Sidewalk Repair"],
       record="None. " + L + "maps8_Sidewalks.geojson has a DateRepair field that is empty in all 36,822 rows; maps8_CurbRamps.geojson DateRepair empty in all 7,932. Project Sidewalk labels record condition, not repair.",
       record_status="no (field exists, empty)", joined="no",
       take="Fill DateRepair from 50/50 contractor completions; the field is already there."),
  dict(id="water", service="Water leaks, no water, low pressure, hydrants",
       codes=["WTR-COMING-UP", "NOWATER", "PRESSURE", "FH-RUNNING", "FH-MAINTENANCE", "LEAKING-METER", "MISSING-COVER", "LOOSE-COVER", "HYDRANT-HIT"],
       record="Partial, live only: stlwater.com/outages lists current outages and about 26 recent repair work orders (initiate date, type, location; no finish date), refreshed every 15 minutes. Two snapshots on disk (data/raw/city-live/stlwater_outages_20261014T00*.out); no history.",
       record_status="partial (live list, no history, no finish date)", joined="no",
       take="Archive the 15-minute list (keyless) or obtain the Water Division work-order export with finish dates."),
  dict(id="lead", service="Lead-paint inspections",
       codes=["Lead Insp"],
       record="None found on disk.", record_status="no", joined="no",
       take="Building Division lead programme case outcomes (inspection date, clearance date)."),
  dict(id="vacant_unsecured", service="Vacant building unsecured (board-up)",
       codes=["Vacnt Bldg Unsecured"],
       record="Yes: " + L + "maps8_BUILDING_DIVISION_Boardups.geojson (33,141 board-ups with DateCreated and DateBoardedUp, to 8 Oct 2026).",
       record_status="yes",
       joined=(f"yes, tonight: of {bu_ref['n']:,} requests filed Jan 2024 to mid-Jul 2026 and closed 'referred to board up crew' "
               f"(median {bu_ref['median_days_to_close_311']} days to close), a board-up is recorded at the address within the 14-day promise for "
               f"{bu_ref['boarded_within_14d_promise']:.0%}, within 30 days for {bu_ref['boarded_within_30d']:.0%}, within 90 days for {bu_ref['boarded_within_90d']:.0%}; "
               f"median {bu_ref['median_days_to_boardup_if_any']} days to board-up where one exists"),
       take="Nothing new: both files are public; join weekly by parcel."),
  dict(id="tornado_debris", service="Tornado debris removal",
       codes=["TDebris-alley/street"],
       record="Street-level only: " + L + "agol_Debris_Clearing.geojson (76 street segments cleared 23 to 28 May 2025). No per-address record.",
       record_status="partial (May 2025 sweep only)", joined="no",
       take="Debris contractor load tickets or monitoring records by address."),
  dict(id="lra_demolition", service="LRA demolition submissions",
       codes=["LRA Demo Submission"],
       record="Yes: " + L + "maps8_BUILDING_DIVISION_Demolitions.geojson (3,767 demolition permits with DateSubmitted, DateIssued, DateClosed, PermitStatus).",
       record_status="yes",
       joined=(f"yes, tonight: of {lra_open['n']} LRA demolition submissions filed 2024 to 2026 and still open in 311, "
               f"{lra_open['n_completed_demolition_after_filing']} ({lra_open['completed_demolition_at_address_after_filing']:.0%}) have a completed demolition permit at the same address after filing"),
       take="Close the 311 request from the permit's DateClosed; both are city systems."),
  dict(id="building_collapse", service="Building collapse / dangerous building",
       codes=["Building Collapse"],
       record="Partial: the demolition permit layer above.",
       record_status="partial",
       joined=(f"yes, tonight: of {coll_closed['n']:,} closed or cancelled requests filed 2024 to 2026, "
               f"{coll_closed['n_completed_demolition_after_filing']} ({coll_closed['completed_demolition_at_address_after_filing']:.0%}) later have a completed demolition at the address"),
       take="Building Division case outcomes (re-inspection, emergency demolition)."),
  dict(id="code_enforcement", service="Property maintenance and open-storage complaints",
       codes=["Ppty Maint Code-Ext", "Ppty Maint Code-Int", "Illegl Use-Opn Storg"],
       record="None public. Closures are the notice step ('issued notice of violation', 'Building already under notice'); compliance on re-inspection is held in the Building Division case system.",
       record_status="no", joined="no",
       take="Case status from the Building Division system: re-inspection date and outcome."),
  dict(id="graffiti", service="Graffiti removal",
       codes=["Graffiti-Private", "Graffiti-Public", "Traffic Graffiti", "Graffiti-Prvt Dmpstr"],
       record="None besides the closing text ('Graffiti removed  painted' etc.).",
       record_status="no", joined="no", take="Crew logs (Operation Brightside)."),
  dict(id="sirens", service="Outdoor warning sirens not heard",
       codes=["Sirens Not Heard"],
       record="None. No public siren-status map; the 2026 audit lists sirens 'Not Tested' (research/synthesis-notes.md).",
       record_status="no", joined="no",
       take="CEMA siren test log by siren and date."),
  dict(id="homeless", service="Homeless outreach calls (shelter)",
       codes=["Homeless Call"],
       record="None public (HMIS is not public; no shelter-bed availability is published). Reported here at type level only; no locations.",
       record_status="no", joined="no",
       take="Aggregate outreach outcomes from Human Services (counts only)."),
  dict(id="nuisance_log", service="Public nuisance reports (logging only)",
       codes=["Public Nuisance Rpt"],
       record="Not applicable: the city describes this type as logging only; requests close automatically on submission.",
       record_status="n/a", joined="n/a",
       take="Nothing; but it should be excluded from any closure-rate measure."),
]

con = duckdb.connect()
pairs = con.execute(f"SELECT DISTINCT PROBLEMCODE, PUBLICRESOLUTION FROM '{P}' WHERE STATUS='CLOSED'").fetchall()
con.execute("CREATE TABLE cls (PROBLEMCODE VARCHAR, PUBLICRESOLUTION VARCHAR, class VARCHAR)")
con.executemany("INSERT INTO cls VALUES (?,?,?)", [(a, b, classify(a, b)[0]) for a, b in pairs])
con.execute(f"""
CREATE TABLE r AS SELECT q.*, c.class,
  (epoch(t_closed)-epoch(t_init))/86400.0 AS days, (epoch(t_promise)-epoch(t_init))/86400.0 AS promise_days
FROM '{P}' q LEFT JOIN cls c ON c.PROBLEMCODE=q.PROBLEMCODE AND c.PUBLICRESOLUTION IS NOT DISTINCT FROM q.PUBLICRESOLUTION AND q.STATUS='CLOSED'
WHERE t_init >= TIMESTAMP '2025-01-01' AND t_init < TIMESTAMP '2026-10-13'
""")

out = []
for s in SERVICES:
    codes = s["codes"]
    ph = ",".join("?" * len(codes))
    r = con.execute(f"""
      SELECT count(*),
        count(*) FILTER (WHERE STATUS='CLOSED'), count(*) FILTER (WHERE STATUS='CANCEL'),
        count(*) FILTER (WHERE STATUS NOT IN ('CLOSED','CANCEL') OR STATUS IS NULL),
        median(promise_days), avg((t_promise IS NOT NULL)::INT),
        avg((class='done')::INT) FILTER (WHERE STATUS='CLOSED'),
        avg((class IN ('handed_off','converted'))::INT) FILTER (WHERE STATUS='CLOSED'),
        avg((class='no_action')::INT) FILTER (WHERE STATUS='CLOSED'),
        avg((class IN ('blank','info_other'))::INT) FILTER (WHERE STATUS='CLOSED'),
        median(days) FILTER (WHERE STATUS='CLOSED'),
        avg((t_closed <= t_promise)::INT) FILTER (WHERE STATUS='CLOSED' AND t_promise IS NOT NULL),
        mode(coalesce(trim(PUBLICRESOLUTION),'')) FILTER (WHERE STATUS='CLOSED')
      FROM r WHERE PROBLEMCODE IN ({ph})""", codes).fetchone()
    n, nc, nx, no, pd_, pp, sd, sh, sn, sb, md, sbp, top = r
    rnd = lambda v, k=3: None if v is None else round(v, k)
    says_done = None if sd is None else ("mostly" if sd >= 0.5 else "sometimes" if sd >= 0.15 else "rarely")
    out.append({
        "id": s["id"], "service": s["service"], "problemcodes": [c.strip() for c in codes],
        "intake_recorded": "yes (311)",
        "filed_2025_26": n, "closed": nc, "cancelled": nx, "open": no,
        "promise_date": f"yes, median {pd_:g} days after filing" if pp and pp > 0.5 else (f"on {pp:.0%} of requests" if pp else "no"),
        "promise_days_median": rnd(pd_, 1), "share_with_promise": rnd(pp),
        "closure_says_done": says_done, "share_closed_done": rnd(sd), "share_closed_handoff_or_converted": rnd(sh),
        "share_closed_no_action": rnd(sn), "share_closed_blank_or_info": rnd(sb),
        "median_days_to_close": rnd(md, 1), "share_closed_by_promise": rnd(sbp),
        "top_closing_text": top,
        "independent_completion_record": s["record_status"], "completion_record_source": s["record"],
        "joined": s["joined"], "what_it_would_take": s["take"],
        "label": "observed (counts and shares from the city's 311 file, deduplicated by REQUESTID; record columns observed from files on disk)",
    })

meta = {"generated_by": "scripts/night/N2/06_register.py",
        "scope": "311 requests filed 2025-01-01 to 2026-10-12, one row per REQUESTID; closure class from scripts/night/N2/classes.py",
        "columns": {"closure_says_done": "mostly: >=50% of closures in class done; sometimes: 15-49%; rarely: <15%",
                    "independent_completion_record": "a city record of the work itself, outside the 311 request (yes / partial / no)"},
        "licence_note": "No city dataset states a licence."}
(B / "register.json").write_text(json.dumps({"meta": meta, "rows": out}, indent=2, default=str))
with open(B / "register.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=[k for k in out[0] if k != "problemcodes"] + ["problemcodes"])
    w.writeheader()
    for o in out:
        w.writerow({**o, "problemcodes": "; ".join(o["problemcodes"])})
for o in out:
    print(f"{o['id']:18s} n={o['filed_2025_26']:6d} cl={o['closed']:6d} cx={o['cancelled']:5d} op={o['open']:5d} prom={o['promise_days_median']} done={o['share_closed_done']} hand={o['share_closed_handoff_or_converted']} rec={o['independent_completion_record']}")
