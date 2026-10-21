"""Three plain charts for research/attention-over-time.md. Usage: python -I charts.py <analysis.json> <out_dir>"""
import json, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = json.load(open(sys.argv[1])); OUT = sys.argv[2]
M = A["months_full"]; S = A["series"]
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})
NAMES = {"violent_crime": "Violent crime", "tornado_recovery": "Tornado and recovery", "downtown": "Downtown",
         "traffic_safety": "Traffic safety", "airport": "Airport", "winter_storm_snow_removal": "Winter storms, snow removal",
         "vacant_derelict_buildings": "Vacant and derelict buildings", "jail_sheriff": "Jail and sheriff",
         "schools_slps": "Public schools (SLPS)", "policing": "Policing and police control", "data_centers": "Data centers",
         "water_sewer": "Water and sewer", "trash_dumping": "Trash, recycling, dumping", "streets_sidewalks_lights": "Streets, sidewalks, lights",
         "trees_overgrowth": "Trees, weeds, overgrowth", "animal_control": "Animals", "parking_towing": "Vehicles, parking, towing",
         "housing_tenants": "Housing and tenants", "graffiti_vandalism": "Graffiti", "homelessness": "Homelessness",
         "city_budget_taxes": "City budget and taxes", "city_services_workforce": "City services and workforce",
         "development_incentives": "Development and incentives", "emergency_services": "911, sirens, fire/EMS",
         "public_health": "Public health", "parks_rec": "Parks and recreation", "property_crime": "Property crime",
         "transit": "Transit", "fires": "Fires", "immigration_enforcement": "Immigration enforcement"}

def clean(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True); ax.tick_params(length=0)

# Chart 1: monthly attention, twelve issues, news vs r/StLouis
pick = ["tornado_recovery", "violent_crime", "winter_storm_snow_removal", "policing", "jail_sheriff", "schools_slps",
        "data_centers", "water_sewer", "traffic_safety", "vacant_derelict_buildings", "streets_sidewalks_lights", "trash_dumping"]
fig, axes = plt.subplots(4, 3, figsize=(11, 9.6), sharex=True)
ticks = [i for i, m in enumerate(M) if m.endswith(("-01", "-04", "-07", "-10"))]
for ax, iss in zip(axes.flat, pick):
    ax.plot(range(len(M)), S["news"][iss], color=BLUE, lw=2, label="Local news (3 outlets + NextSTL)")
    ax.plot(range(len(M)), S["reddit"][iss], color=ORANGE, lw=2, label="r/StLouis posts")
    ax.set_title(NAMES[iss], loc="left", fontsize=10, color=INK, pad=4)
    ax.set_ylim(bottom=0); clean(ax)
    ax.set_xticks(ticks); ax.set_xticklabels([M[i][2:] for i in ticks], fontsize=7.5)
h, l = axes.flat[0].get_legend_handles_labels()
fig.legend(h, l, loc="upper left", bbox_to_anchor=(0.01, 0.955), ncol=2, frameon=False, fontsize=9.5)
fig.suptitle("Items per month naming the City of St. Louis, by issue (Oct 2024 to Sep 2026)", x=0.012, ha="left", fontsize=12.5, y=0.985)
fig.text(0.012, 0.012, "Each panel has its own vertical scale. Counts are tagged headlines and post titles, not need. Post-Dispatch, KSDK and KMOV are not included.", fontsize=8, color=INK2)
fig.tight_layout(rect=(0, 0.025, 1, 0.925))
fig.savefig(f"{OUT}/attention-chart-1-monthly-by-issue.png", dpi=160); plt.close(fig)

def share(stream, issues, denom_keys=None):
    tot = sum(sum(v) for k, v in S[stream].items() if (denom_keys is None or k in denom_keys))
    return {i: 100 * sum(S[stream].get(i, [0])) / tot for i in issues}

def dots(issues, streams, title, note, fname, order_by):
    fig, ax = plt.subplots(figsize=(9.5, 0.42 * len(issues) + 1.9))
    vals = {name: share(st, issues) for name, st, _, _ in streams}
    issues = sorted(issues, key=lambda i: vals[order_by][i])
    for y, iss in enumerate(issues):
        xs = [vals[name][iss] for name, *_ in streams]
        ax.plot([min(xs), max(xs)], [y, y], color=GRID, lw=1.5, zorder=1)
    for name, st, col, mk in streams:
        ax.scatter([vals[name][i] for i in issues], range(len(issues)), s=58, color=col, marker=mk, label=name, zorder=3, edgecolor=SURF, linewidth=1.2)
    ax.set_yticks(range(len(issues))); ax.set_yticklabels([NAMES.get(i, i) for i in issues], color=INK)
    ax.set_xlabel("Share of that source's issue-tagged total, 24 months (%)")
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True); ax.tick_params(length=0)
    ax.set_xlim(left=-0.8)
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.set_title(title, loc="left", fontsize=12, pad=10)
    fig.text(0.012, 0.012, note, fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    fig.savefig(f"{OUT}/{fname}", dpi=160); plt.close(fig)
    return {i: {n: round(vals[n][i], 1) for n in vals} for i in issues}

svc = ["trash_dumping", "streets_sidewalks_lights", "trees_overgrowth", "parking_towing", "animal_control", "vacant_derelict_buildings",
       "water_sewer", "winter_storm_snow_removal", "graffiti_vandalism", "housing_tenants", "parks_rec", "tornado_recovery", "homelessness"]
t2 = dots(svc, [("Residents' 311 requests (CSB)", "csb", BLUE, "o"), ("Local news", "news", ORANGE, "s"), ("r/StLouis posts", "reddit", AQUA, "^")],
          "What residents request from the city vs what gets public attention",
          "Only issues that exist as 311 request types. Shares are of each source's own total, so the three sources are comparable in mix, not in volume.",
          "attention-chart-2-requests-vs-attention.png", "Residents' 311 requests (CSB)")
may = ["tornado_recovery", "city_services_workforce", "city_budget_taxes", "streets_sidewalks_lights", "development_incentives", "emergency_services",
       "vacant_derelict_buildings", "winter_storm_snow_removal", "homelessness", "trash_dumping", "policing", "water_sewer", "data_centers",
       "violent_crime", "jail_sheriff", "schools_slps", "traffic_safety", "property_crime", "airport", "transit"]
t3 = dots(may, [("Mayor's office statements", "mayor", BLUE, "o"), ("Local news", "news", ORANGE, "s"), ("r/StLouis posts", "reddit", AQUA, "^")],
          "What the mayor's office talks about vs what gets public attention",
          "Mayor's office = rows in research/mayors-office-log.csv (mostly official releases). Shares are of each source's own issue-tagged total.",
          "attention-chart-3-mayor-vs-attention.png", "Mayor's office statements")
json.dump({"chart2": t2, "chart3": t3}, open(f"{OUT}/../data/raw/attention/_derived/chart_tables.json", "w"), indent=0)
for name, t in (("chart2", t2), ("chart3", t3)):
    print(name)
    for i, v in reversed(list(t.items())): print("  ", i.ljust(30), v)
