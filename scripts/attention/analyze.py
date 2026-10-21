"""Counts, spikes and comparisons for the attention study.

Usage: python3 -I analyze.py <tagged.jsonl> <csb.zip> <mayors-office-log.csv> <out_csv> <out_json>
"""
import collections
import csv
import io
import json
import re
import statistics
import sys
import zipfile

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import tag

tagged_path, csb_zip, mayor_csv, out_csv, out_json = sys.argv[1:6]
FULL = [f"{y}-{m:02d}" for y in (2024, 2025, 2026) for m in range(1, 13) if "2024-10" <= f"{y}-{m:02d}" <= "2026-09"]
ALLM = FULL + ["2026-10"]
rows = [json.loads(l) for l in open(tagged_path, encoding="utf-8")]

# ---- 1. monthly counts CSV (tidy; one item can appear under several issues) ----
agg = collections.Counter()
com = collections.Counter()
for r in rows:
    for iss in (r["issues"] or ["(no_issue_tag)"]):
        k = (r["month"], r["source_kind"], r["source"], iss, r["scope"], r["mention_kind"])
        agg[k] += 1
        com[k] += r.get("num_comments") or 0
with open(out_csv, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["month", "source_kind", "source", "issue", "scope", "mention_kind", "n_items", "reddit_comments"])
    for k in sorted(agg):
        w.writerow(list(k) + [agg[k], com[k] if k[1] == "community_forum" else ""])

# ---- 2. per-issue monthly series, city-named scope ----
def series(kind, scope_ok):
    s = collections.defaultdict(lambda: collections.Counter())
    for r in rows:
        if r["source_kind"] == kind and scope_ok(r["scope"]):
            for iss in r["issues"]:
                s[iss][r["month"]] += 1
    return s

news = series("news", lambda s: s == "city")
red = series("community_forum", lambda s: s == "city")
red_ne = series("community_forum", lambda s: s != "elsewhere")
boa = series("legislative", lambda s: True)
issues = sorted(set(news) | set(red) | set(boa))

# ---- 3. spikes ----
def spikes(s, min_n):
    out = []
    for iss, c in s.items():
        v = [c.get(m, 0) for m in FULL]
        med = statistics.median(v)
        mad = statistics.median([abs(x - med) for x in v]) or 1
        for m, x in zip(FULL, v):
            if x >= min_n and x >= 2 * max(med, 1) and (x - med) / (1.4826 * mad) >= 3:
                out.append({"issue": iss, "month": m, "n": x, "median": med})
    return out

sp_news, sp_red = spikes(news, 10), spikes(red, 10)

def examples(kind, iss, month, k=7):
    pool = [r for r in rows if r["source_kind"] == kind and r["scope"] == "city" and iss in r["issues"] and r["month"] == month]
    pool.sort(key=lambda r: -(r.get("num_comments") or 0))
    return [f'{r["date"]} [{r["source"][:6]}] {r["title"][:110]}' for r in pool[:k]]

# ---- 4. CSB service requests mapped to the same issues ----
CSB_RULES = [
    ("winter_storm_snow_removal", r"snow"),
    ("graffiti_vandalism", r"graffiti"),
    ("emergency_services", r"sirens"),
    ("tornado_recovery", r"^disaster (recovery|prep)"),
    ("homelessness", r"encampment|homeless"),
    ("noise_fireworks_nuisance", r"\| noise"),
    ("animal_control", r"^animals"),
    ("water_sewer", r"^water|sewer"),
    ("parking_towing", r"^vehicles|parking"),
    ("vacant_derelict_buildings", r"vacnt|vacant bldg|\blra\b|collapse|board up|demo(lition)? "),
    ("trash_dumping", r"^trash/debris|^recycling|debris|dumpg|dumpster|garbage|hazrds waste|litter"),
    ("trees_overgrowth", r"^trees|^weeds/grass|limb|stump"),
    ("parks_rec", r"^parks|^recreation center"),
    ("streets_sidewalks_lights", r"^street lights|^street sign|^traffic signal|^right of way|pothole|cave-?in|sidewalk|street repair|alley repair"),
    ("housing_tenants", r"^prpty insp interior|housing discrim"),
    ("public_health", r"^air pollution|^food control|lead insp"),
    ("(csb_only) property maintenance and nuisance", r"^prpty insp|^nuisance"),
]
CSB_RULES = [(k, re.compile(v, re.I)) for k, v in CSB_RULES]
csb = collections.defaultdict(collections.Counter)
csb_total = collections.Counter()
z = zipfile.ZipFile(csb_zip)
for y in ("2024", "2025", "2026"):
    for r in csv.DictReader(io.TextIOWrapper(z.open(f"{y}.csv"), encoding="utf-8", errors="replace")):
        m = r["DATETIMEINIT"][:7]
        if m not in ALLM:
            continue
        csb_total[m] += 1
        text = f'{r["GROUP"]} | {r["PROBLEMCODE"]}'
        for iss, rx in CSB_RULES:
            if rx.search(text):
                csb[iss][m] += 1
                break
        else:
            csb["(csb_only) other"][m] += 1

# ---- 5. mayor's-office log mapped to the same issues ----
EXTRA = [
    ("streets_sidewalks_lights", r"\bstreets\b|infrastructure|sinkhole|paving|potholes"),
    ("city_services_workforce", r"city services|basic services|city workforce|\bhiring|staffing|personnel|\bpermits?\b|csb|\b311\b|service requests|civil service|employee (pay|compensation)|vacancies|procurement|service delivery"),
    ("homelessness", r"code blue|winter shelter|shelter capacity"),
    ("violent_crime", r"public safety|violence prevention|\bcrime\b"),
    ("city_budget_taxes", r"\bbudget\b|\barpa\b|revenue"),
    ("development_incentives", r"zoning|economic development|neighborhood planning|planstl"),
    ("trash_dumping", r"refuse|recycling|trash"),
    ("policing", r"\bpolice\b"),
]
EXTRA = [(k, re.compile(v, re.I)) for k, v in EXTRA]
mayor = collections.defaultdict(collections.Counter)
mayor_rows = 0
mayor_month = collections.Counter()
for r in csv.DictReader(open(mayor_csv, encoding="utf-8")):
    m = r["date"][:7]
    if m not in ALLM:
        continue
    mayor_rows += 1
    mayor_month[m] += 1
    text = r["topics"].replace(";", " . ") + " . " + r["summary"]
    tags = set(tag.issues_for(text))
    for iss, rx in EXTRA:
        if rx.search(r["topics"]):
            tags.add(iss)
    for t in tags:
        mayor[t][m] += 1

# ---- 6. window totals, shares, ranks ----
def tot(s, iss):
    return sum(s[iss].get(m, 0) for m in FULL) if iss in s else 0

table = []
for iss in issues + [k for k in csb if k.startswith("(csb_only)")]:
    table.append({"issue": iss, "news_city": tot(news, iss), "reddit_city": tot(red, iss), "reddit_not_elsewhere": tot(red_ne, iss),
                  "boa_bills": tot(boa, iss), "csb_requests": tot(csb, iss), "mayor_rows": tot(mayor, iss),
                  "news_peak": max(FULL, key=lambda m: news[iss].get(m, 0)) if iss in news else "",
                  "reddit_peak": max(FULL, key=lambda m: red[iss].get(m, 0)) if iss in red else ""})

def corr(a, b):
    if len(set(a)) < 2 or len(set(b)) < 2:
        return None
    return round(statistics.correlation(a, b), 2)

cors = []
for iss in issues:
    if tot(csb, iss) >= 200:
        c = [csb[iss].get(m, 0) for m in FULL]
        cors.append({"issue": iss, "csb_vs_news": corr(c, [news[iss].get(m, 0) for m in FULL]),
                     "csb_vs_reddit": corr(c, [red_ne[iss].get(m, 0) for m in FULL])})

kinds = collections.Counter()
for r in rows:
    if r["issues"] and r["scope"] == "city":
        kinds[(r["source_kind"], r["mention_kind"])] += 1

out = {
    "months_full": FULL,
    "items": {"total": len(rows),
              "by_kind": collections.Counter(r["source_kind"] for r in rows),
              "by_source": collections.Counter(r["source"] for r in rows),
              "tagged_city": collections.Counter(r["source_kind"] for r in rows if r["issues"] and r["scope"] == "city"),
              "scope": collections.Counter(f'{r["source_kind"]}|{r["scope"]}' for r in rows)},
    "table": table, "spikes_news": sp_news, "spikes_reddit": sp_red, "correlations": cors,
    "kinds": {f"{a}|{b}": v for (a, b), v in kinds.items()},
    "series": {"news": {i: [news[i].get(m, 0) for m in FULL] for i in issues},
               "reddit": {i: [red[i].get(m, 0) for m in FULL] for i in issues},
               "reddit_ne": {i: [red_ne[i].get(m, 0) for m in FULL] for i in issues},
               "boa": {i: [boa[i].get(m, 0) for m in FULL] for i in issues},
               "csb": {i: [csb[i].get(m, 0) for m in FULL] for i in csb},
               "mayor": {i: [mayor[i].get(m, 0) for m in FULL] for i in mayor}},
    "csb_total_window": sum(csb_total[m] for m in FULL), "csb_by_month": [csb_total[m] for m in FULL],
    "mayor_rows_window": mayor_rows, "mayor_by_month": [mayor_month[m] for m in FULL],
}
json.dump(out, open(out_json, "w"), indent=0)

print("ISSUE TABLE (24 full months, 2024-10..2026-09)")
print("issue".ljust(46), "news  reddit(ne)  boa   csb  mayor  peaks")
for t in sorted(table, key=lambda t: -(t["news_city"] + t["reddit_city"])):
    print(t["issue"][:45].ljust(46), str(t["news_city"]).rjust(4), f'{t["reddit_city"]}({t["reddit_not_elsewhere"]})'.rjust(11),
          str(t["boa_bills"]).rjust(4), str(t["csb_requests"]).rjust(6), str(t["mayor_rows"]).rjust(5), " ", t["news_peak"], t["reddit_peak"])
print("\nCORR csb vs attention:", cors)
print("\nSPIKES news")
for s in sorted(sp_news, key=lambda s: (s["issue"], s["month"])):
    print(" ", s)
    for e in examples("news", s["issue"], s["month"], 5):
        print("      ", e)
print("\nSPIKES reddit")
for s in sorted(sp_red, key=lambda s: (s["issue"], s["month"])):
    print(" ", s)
    for e in examples("community_forum", s["issue"], s["month"], 5):
        print("      ", e)
