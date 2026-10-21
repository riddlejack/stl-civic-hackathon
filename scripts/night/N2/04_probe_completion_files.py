"""N2 step 4a: probe candidate completion-record files on disk for the register.

Prints, for each file: row count, field names, and min/max of date-like fields.
Prints no field values other than dates and category counts for a whitelist of
non-personal fields. Run: .venv/bin/python -I scripts/night/N2/04_probe_completion_files.py
"""
import json, pathlib, re, datetime, collections

ROOT = pathlib.Path(__file__).resolve().parents[3]
R = ROOT / "data" / "raw"
L = R / "city-services" / "arcgis" / "layers"
CW = R / "city-services" / "arcgis" / "cityworks-service" / "layers"
SAFE_CATS = {"SERVICETYPE", "Status", "STATUS", "Description", "TYPE", "Type", "WORKTYPE", "WorkType",
             "PROPERTYTYPE", "CATEGORY", "Priority", "DemoType", "DEMO_TYPE", "Phase", "PHASE"}
PERSONAL = re.compile(r"owner|name|tax|phone|email|contact|submit|inspector|staff|user|created_user|last_edited_user", re.I)

def to_dt(v):
    if v is None:
        return None
    if isinstance(v, (int, float)) and v > 1e11:
        try:
            return datetime.datetime.utcfromtimestamp(v / 1000)
        except Exception:
            return None
    if isinstance(v, str) and re.match(r"\d{4}-\d{2}-\d{2}", v):
        try:
            return datetime.datetime.fromisoformat(v[:19].replace("T", " "))
        except Exception:
            return None
    if isinstance(v, str) and re.match(r"\d{1,2}/\d{1,2}/\d{4}", v):
        try:
            return datetime.datetime.strptime(v.split()[0], "%m/%d/%Y")
        except Exception:
            return None
    return None

def probe_features(name, feats):
    print(f"\n== {name}: {len(feats)} features")
    if not feats:
        return
    keys = list(feats[0].keys())
    print("fields:", [k for k in keys])
    for k in keys:
        if PERSONAL.search(k):
            continue
        vals = [f.get(k) for f in feats]
        dts = [d for d in (to_dt(v) for v in vals) if d]
        if len(dts) > 0.3 * len(vals) and dts:
            print(f"  date {k}: {min(dts):%Y-%m-%d} .. {max(dts):%Y-%m-%d} (n={len(dts)}, null={len(vals)-len(dts)})")
        elif k in SAFE_CATS:
            c = collections.Counter(vals).most_common(12)
            print(f"  cat {k}: {c}")

def load_geojson(p):
    d = json.loads(p.read_text())
    return [f.get("properties") or f.get("attributes") or {} for f in d.get("features", [])]

def load_cw(p):
    d = json.loads(p.read_text())
    feats = d.get("features") or d.get("records") or d.get("rows") or d
    if isinstance(feats, dict):
        feats = list(feats.values())[0]
    out = []
    for f in feats:
        if isinstance(f, dict):
            out.append(f.get("attributes") or f.get("properties") or f)
    return out

for fn in ["maps8_BUILDING_DIVISION_Boardups.geojson", "maps8_BUILDING_DIVISION_Demolitions.geojson",
           "agol_Demolitions.geojson", "maps8_SLDC_Vacant_Building_Demolitions_Projects.geojson",
           "agol_Debris_Clearing.geojson", "maps8_STREETS_OneCall_StreetLights.geojson",
           "maps8_STREETS_OneCall_TrafficSignals.geojson", "maps8_Sidewalks.geojson", "maps8_CurbRamps.geojson",
           "agol_PCI2025.geojson", "maps6_Condemned.geojson", "maps8_STREETS_Street_Sweeping.geojson"]:
    p = L / fn
    if p.exists():
        try:
            probe_features(fn, load_geojson(p))
        except Exception as e:
            print(f"\n== {fn}: failed to read: {e}")
    else:
        print(f"\n== {fn}: NOT ON DISK")

for p in sorted(CW.glob("*.json")):
    try:
        probe_features("cityworks/" + p.name, load_cw(p))
    except Exception as e:
        print(f"\n== {p.name}: failed: {e}")
