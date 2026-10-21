"""Facts table for research/attention-over-time.md: one row per figure the report gives.

Usage: python3 -I facts.py <repo_root>
Recomputes figures from the derived files where it can; hand-check results and
negative-result figures are entered as reported in the report.
"""
import collections
import csv
import json
import os
import statistics
import sys

root = sys.argv[1]
D = os.path.join(root, "data/raw/attention")
a = json.load(open(f"{D}/_derived/analysis.json"))
ct = json.load(open(f"{D}/_derived/chart_tables.json"))
rep = json.load(open(f"{D}/_derived/items_report.json"))
rows = [json.loads(l) for l in open(f"{D}/_derived/tagged.jsonl", encoding="utf-8")]
M, S = a["months_full"], a["series"]
T = {t["issue"]: t for t in a["table"]}

U = {
    "fox2": "https://fox2now.com/wp-json/wp/v2/posts",
    "stlamerican": "https://www.stlamerican.com/wp-json/wp/v2/posts",
    "stlpr": "https://www.stlpr.org/sitemap.xml",
    "nextstl": "https://nextstl.com/wp-json/wp/v2/posts",
    "reddit_stlouis": "https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=StLouis",
    "boa_bills": "https://www.stlouis-mo.gov/government/city-laws/board-bills/index.cfm",
}
NEWS = " ; ".join(U[k] for k in ("fox2", "stlamerican", "stlpr", "nextstl"))
RED, BOA = U["reddit_stlouis"], U["boa_bills"]
ALL = f"{NEWS} ; {RED} ; {BOA}"
CSB = "https://www.stlouis-mo.gov/data/upload/data-files/csb.zip"
MAYOR = "research/mayors-office-log.csv (local file; each row there carries its own source URL)"
W24, WALL = "2024-10-01/2026-09-30", "2024-10-01/2026-10-13"
AN, TG, HC = "data/raw/attention/_derived/analysis.json", "data/raw/attention/_derived/tagged.jsonl", "data/raw/attention/_derived/handcheck_*"
NAME = {"fox2": "Fox 2", "stlamerican": "St. Louis American", "stlpr": "St. Louis Public Radio", "nextstl": "NextSTL",
        "reddit_stlouis": "r/StLouis", "boa_bills": "Board of Aldermen bills"}

out = []


def add(section, what, figure, unit, date, label="observed", url="", src=""):
    out.append([section, what, figure, unit, date, label, url, src])


def mon(m):
    return m  # YYYY-MM


# ---- 1. sources ----
for s in U:
    mf = json.load(open(f"{D}/{s}/manifest.json"))
    src = f"data/raw/attention/{s}/manifest.json"
    add("1 sources", f"{NAME[s]}: rows pulled", mf["rows"], "rows", f'{mf["date_min"]}/{mf["date_max"]}', "observed", U[s], src)
    add("1 sources", f"{NAME[s]}: rows kept after merge", rep[s]["kept"], "rows", WALL, "observed", U[s], "data/raw/attention/_derived/items_report.json")
    add("1 sources", f"{NAME[s]}: requests made", mf["requests"], "requests", "2026-10-13", "observed", U[s], src)
    add("1 sources", f"{NAME[s]}: earliest item date pulled", mf["date_min"], "date", mf["date_min"], "observed", U[s], src)
    add("1 sources", f"{NAME[s]}: latest item date pulled", mf["date_max"], "date", mf["date_max"], "observed", U[s], src)
    add("1 sources", f"{NAME[s]}: pull started", mf["started"], "UTC time", "2026-10-13", "observed", U[s], src)
    add("1 sources", f"{NAME[s]}: pull finished", mf["finished"], "UTC time", "2026-10-13", "observed", U[s], src)
mf = json.load(open(f"{D}/boa_bills/manifest.json"))
for k in ("2024-2025", "2025-2026", "2026-2027"):
    add("1 sources", f"Board bills listed, session {k}", mf[f"listed_{k}"], "bills", k, "observed", BOA, "data/raw/attention/boa_bills/manifest.json")
add("1 sources", "Board bills: request errors", len(mf["errors"]), "errors", "2026-10-13", "observed", BOA, "data/raw/attention/boa_bills/manifest.json")

per = collections.defaultdict(collections.Counter)
for r in rows:
    per[r["source"]][r["month"]] += 1
for s in ("fox2", "stlamerican", "stlpr", "reddit_stlouis"):
    v = [per[s].get(m, 0) for m in M]
    add("1 sources", f"{NAME[s]}: fewest kept items in a month", min(v), "items per month", W24, "observed", U[s], TG)
    add("1 sources", f"{NAME[s]}: most kept items in a month", max(v), "items per month", W24, "observed", U[s], TG)
add("1 sources", "NextSTL: months with no items", sum(1 for m in M if per["nextstl"].get(m, 0) == 0), "months of 24", W24, "observed", U["nextstl"], TG)

fox_scope = collections.Counter(r["scope"] for r in rows if r["source"] == "fox2")
add("1 sources", "Fox 2 items with a city reference", fox_scope["city"], "items", WALL, "observed", U["fox2"], TG)
add("1 sources", "Fox 2 items with a city reference, share of its kept items", round(100 * fox_scope["city"] / sum(fox_scope.values())), "percent", WALL, "observed", U["fox2"], TG)

red_rows = [r for r in rows if r["source"] == "reddit_stlouis"]
fl = collections.Counter(r.get("section", "") for r in red_rows)
add("1 sources", "r/StLouis posts with no flair", fl[""], "posts", WALL, "observed", RED, TG)
for f in ("Ask STL", "Things to Do", "News"):
    add("1 sources", f"r/StLouis posts with flair '{f}'", fl[f], "posts", WALL, "observed", RED, TG)
add("1 sources", "r/StLouis kept posts with removed or deleted body", sum(1 for r in red_rows if r.get("removed")), "posts", WALL, "observed", RED, TG)
add("1 sources", "r/StLouis median comments per post", statistics.median(r.get("num_comments") or 0 for r in red_rows), "comments", WALL, "observed", RED, TG)

# negative results (entered as reported in the report)
STL = "https://www.stltoday.com/search/?f=rss&t=article&c[]=news/local*"
GD = "https://api.gdeltproject.org/api/v2/doc/doc"
add("1 negative results", "Post-Dispatch search feed: HTTP status once throttled", 429, "HTTP status", "2026-10-13", "observed", STL, "data/raw/attention/_logs/stltoday_local.log")
add("1 negative results", "GDELT DOC API: HTTP status on almost every request", 429, "HTTP status", "2026-10-13", "observed", GD, "data/raw/attention/_logs/gdelt_ksdk.log")
add("1 negative results", "Post-Dispatch search feed: requests before HTTP 429", 20, "requests (about)", "2026-10-13", "estimated", STL, "data/raw/attention/_logs/stltoday_local.log")
add("1 negative results", "Post-Dispatch search feed: block length after 429", 20, "minutes (more than)", "2026-10-13", "estimated", STL, "data/raw/attention/_logs/stltoday_local.log")
add("1 negative results", "Post-Dispatch search feed: collection runs attempted", 3, "runs", "2026-10-13/2026-10-14", "observed", STL, "data/raw/attention/_logs/stltoday_local.log")
add("1 negative results", "Post-Dispatch search feed: last 429 block", "2026-10-14T00:13Z", "UTC time", "2026-10-14", "observed", STL, "data/raw/attention/_logs/stltoday_local.log")
add("1 negative results", "Post-Dispatch rows kept", 0, "rows", WALL, "observed", STL, "data/raw/attention/stltoday_local/items.jsonl")
add("1 negative results", "GDELT (ksdk.com): weekly windows that returned", 3, "windows of 7 tried", "2024-10-01/2024-11-19", "observed", GD, "data/raw/attention/_logs/gdelt_ksdk.log")
for n in (30, 30, 32):
    add("1 negative results", "GDELT (ksdk.com): articles in one returned weekly window", n, "articles", "2024-10/2024-11", "observed", GD, "data/raw/attention/_logs/gdelt_ksdk.log")
add("1 negative results", "GDELT: time spent before stopping", 30, "minutes (about)", "2026-10-13", "estimated", GD, "data/raw/attention/_logs/gdelt_ksdk.log")
add("1 negative results", "GDELT: stopped at", "2026-10-13T23:59Z", "UTC time", "2026-10-13", "observed", GD, "data/raw/attention/_logs/gdelt_ksdk.log")
add("1 negative results", "GDELT rows kept (KSDK and KMOV)", 0, "rows", WALL, "observed", GD, "data/raw/attention/gdelt_ksdk/")
add("1 negative results", "KSDK news sitemap: URLs listed", 156, "URLs", "2026-10-13", "observed", "https://www.ksdk.com/sitemap.xml", "data/raw/attention/_probes/ksdk_gnews.xml")
add("1 negative results", "KMOV sitemap: URLs listed", 470, "URLs (about)", "2026-10-13", "estimated", "https://www.firstalert4.com/arc/outboundfeeds/sitemap-index/?outputType=xml", "data/raw/attention/_probes/kmov_sm400.xml")
add("1 negative results", "KMOV sitemap: span covered", 1, "weeks (roughly)", "2026-10-13", "estimated", "https://www.firstalert4.com/arc/outboundfeeds/sitemap-index/?outputType=xml", "data/raw/attention/_probes/kmov_sm400.xml")
add("1 negative results", "reddit.com /r/StLouis/new.json: HTTP status", 403, "HTTP status", "2026-10-13", "observed", "https://www.reddit.com/r/StLouis/new.json", "data/raw/attention/_probes/reddit_new.json")
add("1 negative results", "Missouri Independent WordPress API: HTTP status", 403, "HTTP status", "2026-10-13", "observed", "https://missouriindependent.com/wp-json/wp/v2/posts", "data/raw/attention/_probes/moindep_wp.json")
add("1 negative results", "Bluesky public search: HTTP status", 403, "HTTP status", "2026-10-13", "observed", "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts", "data/raw/attention/_probes/bsky.json")

# ---- 2. merge ----
IR = "data/raw/attention/_derived/items_report.json"
add("2 merge", "Board bills dropped as outside the window", rep["boa_bills"]["out_of_window"], "rows", "2024-04-26/2024-09-30", "observed", BOA, IR)
add("2 merge", "STLPR rows dropped as non-local sections (almost all npr)", rep["stlpr"]["dropped_section"], "rows", WALL, "observed", U["stlpr"], IR)
for s in ("fox2", "stlamerican", "reddit_stlouis"):
    add("2 merge", f"{NAME[s]}: same-title same-month duplicates dropped", rep[s]["dup_title_same_month"], "rows", WALL, "observed", U[s], IR)
add("2 merge", "Items kept, all sources", a["items"]["total"], "items", WALL, "observed", ALL, AN)
add("2 merge", "News items kept", a["items"]["by_kind"]["news"], "items", WALL, "observed", NEWS, AN)
add("2 merge", "Forum posts kept", a["items"]["by_kind"]["community_forum"], "posts", WALL, "observed", RED, AN)
add("2 merge", "Board bills kept", a["items"]["by_kind"]["legislative"], "bills", WALL, "observed", BOA, AN)
add("2 merge", "Snippet length stored per item, maximum", 240, "characters", "2026-10-13", "observed", ALL, "scripts/attention/collect.py")

# ---- 3. categories, scope ----
add("3 categories", "Topic-model topics, news titles", 45, "topics", WALL, "observed", NEWS, "scripts/attention/topics.py")
add("3 categories", "Topic-model topics, r/StLouis titles", 50, "topics", WALL, "observed", RED, "scripts/attention/topics.py")
add("3 categories", "Topic-model topics, city-named civic subset", 60, "topics", WALL, "observed", ALL, "scripts/attention/topics_city.py")
add("3 categories", "Items in the city-named civic subset used for the third topic pass", 23172, "items", WALL, "observed", ALL, "scripts/attention/topics_city.py")
add("3 categories", "Issue categories derived", 34, "categories", WALL, "observed", ALL, "scripts/attention/tag.py")
tc = [r for r in rows if r["issues"] and r["scope"] == "city"]
add("3 categories", "Tagged city-named items carrying more than one tag", round(100 * sum(1 for r in tc if len(r["issues"]) > 1) / len(tc)), "percent", WALL, "observed", ALL, TG)
for k, v in a["items"]["scope"].items():
    kind, sc = k.split("|")
    if kind == "legislative":
        continue
    add("3 categories", f"Scope '{sc}': {'news items' if kind == 'news' else 'r/StLouis posts'}", v, "items", WALL, "observed", NEWS if kind == "news" else RED, AN)
tcn = a["items"]["tagged_city"]
add("3 categories", "News items with an issue tag and a city reference", tcn["news"], "items", WALL, "observed", NEWS, AN)
add("3 categories", "r/StLouis posts with an issue tag and a city reference", tcn["community_forum"], "posts", WALL, "observed", RED, AN)
add("3 categories", "Board bills with an issue tag", tcn["legislative"], "bills", WALL, "observed", BOA, AN)
add("3 categories", "All items with an issue tag and a city reference", sum(tcn.values()), "items", WALL, "observed", ALL, AN)

CHECK = {4: "airport city_services_workforce data_centers flood_heat_storms property_crime schools_slps streets_sidewalks_lights tornado_recovery violent_crime",
         1: "graffiti_vandalism",
         2: "city_budget_taxes city_government_general emergency_services fires homelessness immigration_enforcement noise_fireworks_nuisance parking_towing utilities_power winter_storm_snow_removal"}
check = {i: n for n, names in CHECK.items() for i in names.split()}
for t in a["table"]:
    i = t["issue"]
    if i.startswith("(csb_only)"):
        add("3 categories", f"311 requests with no attention category: {i[11:]}", t["csb_requests"], "requests", W24, "observed", CSB, AN)
        continue
    add("3 categories", f"{i}: city-named news items", t["news_city"], "items", W24, "observed", NEWS, AN)
    add("3 categories", f"{i}: city-named r/StLouis posts", t["reddit_city"], "posts", W24, "observed", RED, AN)
    add("3 categories", f"{i}: board bills", t["boa_bills"], "bills", W24, "observed", BOA, AN)
    if t["csb_requests"]:
        add("3 categories", f"{i}: 311 (CSB) requests mapped to this category", t["csb_requests"], "requests", W24, "observed", CSB, AN)
    if i != "city_government_general":
        add("3 categories", f"{i}: mayor's-office log rows mapped to this category", t["mayor_rows"], "rows", W24, "observed", MAYOR, AN)
    add("3 categories", f"{i}: sampled items with a correct tag (sample B)", check.get(i, 3), "items of 4", WALL, "observed", ALL, HC)

# ---- 4. hand-check (as reported in the report; labels assigned by the agent) ----
H = [("Sample A: random items read", 150, "items"), ("Sample A: tag precision", 0.77, "proportion"), ("Sample A: tag recall", 0.79, "proportion"),
     ("Sample A: items tagged that should not be", 6, "items"), ("Sample A: tagged items missed", 8, "items"),
     ("Sample A: kind of mention correct", 31, "items of 47"), ("Sample A: kind of mention correct, share", 66, "percent"),
     ("Sample A2: fresh random items read", 100, "items"), ("Sample A2: tag precision", 0.80, "proportion"), ("Sample A2: tag recall", 0.67, "proportion"),
     ("Sample A2: items wrongly tagged", 4, "items"), ("Sample A2: tagged items missed", 10, "items"),
     ("Sample A2: kind of mention correct", 20, "items of 38"), ("Sample A2: kind of mention correct, share", 53, "percent"),
     ("Sample A2 re-scored after rules were extended (not unbiased): precision", 0.84, "proportion"),
     ("Sample A2 re-scored after rules were extended (not unbiased): recall", 0.90, "proportion"),
     ("Scope check (A + A2): tagged items judged", 69, "items"), ("Scope check: tagger said city", 42, "items"),
     ("Scope check: tagger said city and hand label agreed", 36, "items of 42"), ("Scope check: tagger city correct, share", 86, "percent"),
     ("Scope check: tagger said unstated", 27, "items"), ("Scope check: unstated items that were city", 6, "items of 27"),
     ("Scope check: unstated items that were elsewhere", 9, "items of 27"), ("Scope check: unstated items that could not be told", 12, "items of 27"),
     ("Sample B: tagged city-named items read (4 per category)", 136, "items"), ("Sample B: tag correct", 99, "items of 136"),
     ("Sample B: tag correct, share", 73, "percent"), ("Sample B: city scope correct", 123, "items of 136"), ("Sample B: city scope correct, share", 90, "percent"),
     ("Sample B: tag and scope both correct", 92, "items of 136"), ("Sample B: both correct, share", 68, "percent"),
     ("Sample B, Fox 2: tag correct", 40, "items of 47"), ("Sample B, r/StLouis: tag correct", 43, "items of 65"),
     ("Sample B, St. Louis American: tag correct", 7, "items of 12"), ("Sample B, STLPR: tag correct", 6, "items of 9"),
     ("Sample B, board bills: tag correct", 3, "items of 3"), ("Scope fixes made after sample B", 3, "rule fixes")]
for what, fig, unit in H:
    add("4 hand-check", what, fig, unit, WALL, "observed", ALL, HC)
add("4 hand-check", "Issue-month counts below this should not be read closely", 20, "items (about)", W24, "inferred", ALL, HC)
for k, v in a["kinds"].items():
    kind, mk = k.split("|")
    if kind == "legislative":
        continue
    add("4 hand-check", f"Kind of mention '{mk}': city-named tagged {'news items' if kind == 'news' else 'r/StLouis posts'}", v, "items", WALL, "observed", NEWS if kind == "news" else RED, AN)

# ---- 5. shares, persistence, comments, spikes ----
SRC = {"Residents' 311 requests (CSB)": ("311 requests", CSB), "Local news": ("news issue tags", NEWS),
       "r/StLouis posts": ("r/StLouis issue tags", RED), "Mayor's office statements": ("mayor's-office log issue tags", MAYOR)}
seen = set()
for chart in ("chart2", "chart3"):
    for iss, d in ct[chart].items():
        for k, v in d.items():
            if (iss, k) in seen:
                continue
            seen.add((iss, k))
            add("5-7 shares", f"{iss}: share of {SRC[k][0]}", v, "percent", W24, "observed", SRC[k][1], "data/raw/attention/_derived/chart_tables.json")
rt = sum(t["reddit_city"] for t in a["table"])
add("5-7 shares", "downtown: share of r/StLouis issue tags", round(100 * T["downtown"]["reddit_city"] / rt, 1), "percent", W24, "observed", RED, AN)
top4 = sum(T[i]["csb_requests"] for i in ("trash_dumping", "streets_sidewalks_lights", "trees_overgrowth", "parking_towing"))
add("5-7 shares", "Trash, streets, trees and vehicles together: share of 311 requests", round(100 * top4 / a["csb_total_window"]), "percent", W24, "observed", CSB, AN)
add("5-7 shares", "r/StLouis share relative to news share on the four largest request categories, low end", 2, "times (about)", W24, "inferred", f"{NEWS} ; {RED}", AN)
add("5-7 shares", "r/StLouis share relative to news share on the four largest request categories, high end", 5, "times (about)", W24, "inferred", f"{NEWS} ; {RED}", AN)

O = {s: collections.Counter() for s in ("fox2", "stlpr", "stlamerican")}
for r in rows:
    if r["source"] in O and r["scope"] == "city" and r["month"] in M:
        for i in r["issues"]:
            O[r["source"]][i] += 1
ot = {s: sum(c.values()) for s, c in O.items()}
nt = sum(t["news_city"] for t in a["table"])
add("5-7 shares", "Fox 2 share of all news issue tags", round(100 * ot["fox2"] / nt), "percent", W24, "observed", NEWS, TG)
for i in ("violent_crime", "property_crime", "traffic_safety"):
    add("5-7 shares", f"{i}: city-named news items that are Fox 2's", O["fox2"][i], f'items of {T[i]["news_city"]}', W24, "observed", U["fox2"], TG)
OUT = {"fox2": "violent_crime traffic_safety property_crime trash_dumping streets_sidewalks_lights trees_overgrowth parking_towing",
       "stlpr": "tornado_recovery jail_sheriff schools_slps violent_crime trash_dumping streets_sidewalks_lights trees_overgrowth parking_towing",
       "stlamerican": "tornado_recovery downtown schools_slps development_incentives violent_crime trash_dumping streets_sidewalks_lights trees_overgrowth parking_towing"}
for s, names in OUT.items():
    for i in names.split():
        add("5-7 shares", f"{i}: share of {NAME[s]}'s city issue tags", round(100 * O[s][i] / ot[s], 1), "percent", W24, "observed", U[s], TG)

PERS = "violent_crime traffic_safety vacant_derelict_buildings property_crime downtown jail_sheriff schools_slps policing housing_tenants streets_sidewalks_lights trash_dumping trees_overgrowth parking_towing tornado_recovery data_centers winter_storm_snow_removal animal_control graffiti_vandalism parks_rec"
for i in PERS.split():
    add("5 persistence", f"{i}: months with at least 3 city-named news items", sum(1 for x in S["news"][i] if x >= 3), "months of 24", W24, "observed", NEWS, AN)
    add("5 persistence", f"{i}: months with at least 3 city-named r/StLouis posts", sum(1 for x in S["reddit"][i] if x >= 3), "months of 24", W24, "observed", RED, AN)

COM = "downtown violent_crime traffic_safety winter_storm_snow_removal airport immigration_enforcement tornado_recovery transit policing data_centers trash_dumping"
for i in COM.split():
    p = [r for r in red_rows if r["scope"] == "city" and i in r["issues"] and r["month"] in M]
    c = sum(r.get("num_comments") or 0 for r in p)
    add("5 reddit comments", f"{i}: comments on city-named r/StLouis posts", c, "comments", W24, "observed", RED, TG)
    add("5 reddit comments", f"{i}: mean comments per city-named r/StLouis post", round(c / len(p)), "comments per post", W24, "observed", RED, TG)

for key, lab, url in (("spikes_news", "news items", NEWS), ("spikes_reddit", "r/StLouis posts", RED)):
    for s in sorted(a[key], key=lambda s: (s["issue"], s["month"])):
        add("5 spikes", f'{s["issue"]}: city-named {lab} in a spike month', s["n"], "items in month", s["month"], "observed", url, AN)
for st, lab, url in (("news", "news items", NEWS), ("reddit", "r/StLouis posts", RED)):
    add("5 spikes", f"tornado_recovery: median monthly city-named {lab}", statistics.median(S[st]["tornado_recovery"]), "items per month", W24, "observed", url, AN)
add("5 spikes", "trash_dumping: city-named r/StLouis posts, just under the spike rule", S["reddit"]["trash_dumping"][M.index("2025-01")], "items in month", "2025-01", "observed", RED, AN)
add("5 spikes", "graffiti_vandalism: most city-named news items in any month", max(S["news"]["graffiti_vandalism"]), "items in month", W24, "observed", NEWS, AN)
add("5 spikes", "Date of the tornado", "2025-05-16", "date", "2025-05-16", "reported",
    "https://fox2now.com/news/missouri/tornado-devastates-stl-leaving-residents-displaced/", "headline dated 2025-05-17; city inspection type 'ES - 5-16-25 Tornado' per research/data-audit-parts/city-catalog.md")
add("5 spikes", "Proposed water-rate rise over ten years", 86, "percent", "2026-06-04", "reported",
    "https://fox2now.com/news/missouri/st-louis-proposes-86-water-rate-hike-over-next-decade/", "headline only")
add("7 mayor", "Date of the 2025 mayoral primary", "2025-03-04", "date", "2025-03-04", "reported",
    "https://fox2now.com/news/missouri/mayoral-race-highlights-st-louis-city-primary-election-day/", "headline only")

# ---- 6. 311 ----
add("6 311", "311 (CSB) requests in the 24 full months", a["csb_total_window"], "requests", W24, "observed", CSB, AN)
add("6 311", "311 requests, fewest in a month", min(a["csb_by_month"]), "requests per month", W24, "observed", CSB, AN)
add("6 311", "311 requests, most in a month", max(a["csb_by_month"]), "requests per month", W24, "observed", CSB, AN)
add("6 311", "CSB file timestamp when downloaded for the data audit", "2026-10-13T11:04Z", "GMT time", "2026-10-13", "reported", CSB, "research/data-audit-parts/city-catalog.md")
cs = S["csb"]


def at(i, m):
    return cs[i][M.index(m)]


for i, m, what in (("winter_storm_snow_removal", "2025-01", "Snow and ice requests"), ("winter_storm_snow_removal", "2026-01", "Snow and ice requests"),
                   ("streets_sidewalks_lights", "2025-03", "Street and light requests"), ("streets_sidewalks_lights", "2026-03", "Street and light requests"),
                   ("trash_dumping", "2025-01", "Trash requests"), ("trash_dumping", "2025-07", "Trash requests"),
                   ("trees_overgrowth", "2025-05", "Tree and weed requests"),
                   ("vacant_derelict_buildings", "2025-05", "Vacant-building requests"), ("vacant_derelict_buildings", "2026-07", "Vacant-building requests")):
    add("6 311", f"{what} in the month", at(i, m), "requests", m, "observed", CSB, AN)
add("6 311", "Graffiti requests, fewest in a month", min(cs["graffiti_vandalism"]), "requests per month", W24, "observed", CSB, AN)
add("6 311", "Graffiti requests, most in a month", max(cs["graffiti_vandalism"]), "requests per month", W24, "observed", CSB, AN)
add("6 311", "First month with 'Disaster Recovery/Prep' requests in volume", "2025-06", "month", "2025-06", "observed", CSB, AN)
CORR = "winter_storm_snow_removal emergency_services trees_overgrowth trash_dumping animal_control water_sewer streets_sidewalks_lights parking_towing vacant_derelict_buildings housing_tenants".split()
cd = {c["issue"]: c for c in a["correlations"]}
for i in CORR:
    add("6 311", f"{i}: monthly correlation, 311 requests vs city-named news items", cd[i]["csb_vs_news"], "Pearson r, 24 months", W24, "observed", f"{CSB} ; {NEWS}", AN)
    add("6 311", f"{i}: monthly correlation, 311 requests vs r/StLouis posts not marked elsewhere", cd[i]["csb_vs_reddit"], "Pearson r, 24 months", W24, "observed", f"{CSB} ; {RED}", AN)

# ---- 7. mayor's-office log ----
# The log keeps growing. The report's figures are from the state read at
# 2026-10-14 00:14 UTC, so those are entered as read; the later row count is recorded beside them.
ml = list(csv.DictReader(open(os.path.join(root, "research/mayors-office-log.csv"), encoding="utf-8")))
SNAP = "research/mayors-office-log.csv as read 2026-10-14T00:14Z"
add("7 mayor", "Mayor's-office log: rows when read for the analysis", 1945, "rows", "2026-10-14T00:14Z", "observed", MAYOR, SNAP)
add("7 mayor", "Mayor's-office log: rows when this facts file was first written (later state, not analysed)", 2081, "rows", "2026-10-14T00:31Z", "observed", MAYOR, "research/mayors-office-log.csv")
add("7 mayor", "Mayor's-office log: earliest row date", "2019-03-01", "date", "2019-03-01", "observed", MAYOR, SNAP)
add("7 mayor", "Mayor's-office log: latest row date", "2026-10-13", "date", "2026-10-13", "observed", MAYOR, SNAP)
add("7 mayor", "Mayor's-office log: rows in the 24 full months", sum(a["mayor_by_month"]), "rows", W24, "observed", MAYOR, AN)
add("7 mayor", "Mayor's-office log: rows that are official news releases", 911, "rows", "2026-10-14T00:14Z", "observed", MAYOR, SNAP)
add("7 mayor", "Mayor's-office log: rows before February 2025 in the window", sum(a["mayor_by_month"][:4]), "rows", "2024-10-01/2025-01-31", "observed", MAYOR, AN)
ms = S["mayor"]


def mat(i, m):
    return ms[i][M.index(m)]


t1 = [mat("tornado_recovery", m) for m in ("2025-05", "2025-06", "2025-07", "2025-08", "2025-09")]
t2 = [mat("tornado_recovery", m) for m in ("2026-04", "2026-05")]
add("7 mayor", "Log rows on tornado recovery, lowest month May-Sep 2025", min(t1), "rows per month", "2025-05/2025-09", "observed", MAYOR, AN)
add("7 mayor", "Log rows on tornado recovery, highest month May-Sep 2025", max(t1), "rows per month", "2025-05/2025-09", "observed", MAYOR, AN)
add("7 mayor", "Log rows on tornado recovery, lower of Apr-May 2026", min(t2), "rows per month", "2026-04/2026-05", "observed", MAYOR, AN)
add("7 mayor", "Log rows on tornado recovery, higher of Apr-May 2026", max(t2), "rows per month", "2026-04/2026-05", "observed", MAYOR, AN)
for i, m, what in (("data_centers", "2026-04", "data centers"), ("data_centers", "2026-09", "data centers"), ("trash_dumping", "2025-08", "trash and recycling"),
                   ("winter_storm_snow_removal", "2025-10", "snow"), ("winter_storm_snow_removal", "2026-01", "snow")):
    add("7 mayor", f"Log rows on {what} in the month", mat(i, m), "rows", m, "observed", MAYOR, AN)

# ---- 10. files ----
n_csv = sum(1 for _ in open(os.path.join(root, "research/attention-monthly.csv"))) - 1
add("10 files", "Rows in research/attention-monthly.csv", n_csv, "rows", "2024-10/2026-10", "observed", ALL, "research/attention-monthly.csv")
add("10 files", "Charts saved beside the report", 3, "charts", W24, "observed", "research/attention-chart-*.png (local files)", "scripts/attention/charts.py")

dst = os.path.join(root, "research/attention-over-time-facts.csv")
with open(dst, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["report_section", "what", "figure", "unit", "date_refers_to", "label", "url", "computed_from"])
    w.writerows(out)
print(len(out), "rows ->", dst)
print(collections.Counter(r[5] for r in out))
