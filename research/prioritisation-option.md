# Prioritisation option: should the entry ship a ranked overdue list?

The simulation is [prioritisation-scripts/simulate_rank.py](prioritisation-scripts/simulate_rank.py). It reads the private E5 ledger and prints only aggregates: no request ids, no addresses. Run it with `python3 -I research/prioritisation-scripts/simulate_rank.py` from the repo root. No new queries were sent to the city's Cityworks service; every Cityworks figure comes from the extracts already on disk.

## Summary

**Recommendation (inferred): build it, small.** A "Ranked" toggle on the existing queue page, with a one-line "why this rank" per row and a plain-text weights file a division can edit. It is worth building because it changes what a supervisor sees first. On the simulated list, **none** of Forestry's or the Street Department's top-25 ranked rows are in their top-25 oldest-first rows. Forestry's oldest-first top 25 holds 9 life-safety items; ranked, it holds 25. It also gives LINK/LIST/COUNT a working first use: the rank sorts each overdue record into "dispatch" or "verify and close", which is the same split the entry argues the city cannot make today.

**What Cityworks likely already has (observed and reported):** every retrieved St. Louis Cityworks layer except one advertises `Priority`, `PriorityCode`, `PriorityDescription` and `Effort`. Service requests carry a city-set due date (`PrjCompleteDate`, filled on 19,804 of 19,821 extracted rows) and an `Emergency` flag. The one priority field we retrieved, work-order `PriorityCode`, is **empty on all 29,018 distinct work orders**. Several saved searches are named "Urgent", "Hazard" or "Emergency", so urgency seems to live in templates and saved searches rather than in a priority value. **Reported (vendor docs, 1b):** Cityworks 23 has these things natively:
- a per-template priority label;
- a per-template duration that produces the due date we call "promised";
- inboxes built from saved searches;
- a separate, possibly unlicensed, map-and-calendar crew scheduler ("Workload");
- automatic closure of a linked request when its work order closes.

No native escalation or ranking engine was found.

**What we could not establish:** whether service-request `Priority` or `Emergency` is populated (we never retrieved those fields, and did not re-query the city); what each division actually sorts by; and whether St. Louis licenses Cityworks's scheduling or crew-planning modules. Only staff access can answer these. The public 311 file has no resident free text: its `DESCRIPTION` column is a category label, with 223 distinct values across 14,902 rows. So an "AI severity score" from text is not possible on public data. The score therefore keys on the request type, which is what the resident picked, and that choice is sometimes wrong.

**Score in one line:** hazard tier by request type (60 / 30 / 0 points), plus 1 point per 12 days past the city's own promised date (capped at 30, so a year late is worth one tier), plus 5 per extra open report of the same type at the same address (capped at 10). Records with evidence the work is done, superseded or administrative go to a separate close-out list and are not ranked. Block clustering is shown beside each row, not scored.

## 1. What St. Louis's Cityworks already offers

### 1a. Fields in the city's query layers (observed)

**Observed:** 50 of the 51 retrieved layer metadata files advertise `Priority`, `PriorityCode`, `PriorityDescription` and `Effort`. The exception is layer 69 (Storm Response SRs, 4 fields). Service-request layers, e.g. [QE18 Active SRs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18), also advertise `Emergency`, `PrjCompleteDate` ("Projected Completion Date"), `DateDispatchTo` and `WONeeded`. Work-order layers, e.g. [QE100 MTL Open WOs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/100), advertise `ProjectedStartDate`, `ProjectedFinishDate`, `SupervisorName` and `Stage`. Inspection layers, e.g. [QE23 "Priority 1, PCA"](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/23), add `CondScore` and `CondRating`. No field named Severity, SLA, Escalation, Risk or Score appears in any of the 51. Source: `data/raw/cityworks-gap/extracts/layer_*_metadata.json`.

**Observed (populated values in our extracts):** the extraction kept only an operational allowlist ([downloader](cityworks-gap-scripts/qe_client.py); [gap review](cityworks-gap-review.md)), so most of these fields were never retrieved.
- Work-order `PriorityCode` was retrieved, and it is null on all 36,490 search memberships, i.e. all **29,018 distinct work orders**. That includes [QE102 "(MTL) REMOVAL – Open – Urgent"](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/102) (31 rows) and [QE103 "(MTL) Trim – Open – Urgent"](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/103) (7 rows).
- **Inferred:** "Urgent" is encoded in the saved search, probably by template or category, not in `PriorityCode`. The separate work-order `Priority` field was not retrieved, so a null `PriorityCode` does not prove the city has no priority values.
- Service-request `PrjCompleteDate` is filled on 19,804 of 19,821 values across SR search memberships (QE18 and the other SR layers). This is the city's own due date per request, the same date E3 uses as "promised".
- SR `DateDispatchTo` is filled on 13,385 of 19,821 values.
- SR `Priority`, `Effort` and `Emergency` were **not retrieved**.

**Observed (saved-search names that imply a triage practice):** [QE68 "Emergency Tree Service Requests"](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/68) (514 rows), [QE126 "(FP) Tree Trimming – Hazard"](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/126) (78), [QE90 "30-Day Removals – All City – New"](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/90) (316), and ten repeated sets of "Priority 1–4, PCA" inspection searches ([catalog](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json)). **Inferred:** Forestry already triages by hazard and by deadline in its own saved views. Any ranking we propose should be framed as something to compare with that practice, not as a replacement for it.

### 1b. Vendor documentation (reported)

St. Louis runs **Cityworks 23.10**, per the city's own query service root, recorded in [precedents-closed-loop.md](precedents-closed-loop.md) ([service root](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json)). Help pages below were read on 2026-10-14 through a page-summarising fetch. The two most load-bearing pages, marked †, were re-fetched and their quotes checked.

- **Priority is native and set per template.** On the SR panel the Priority field is "Select the order of importance for the work to be completed." † [Respond 4.3 SR fields](https://help.cityworks.com/Respond/4-3/Content/Online/AMS/15-8/ServiceRequest/ServiceRequestPanelFields.htm). SR and WO templates each carry a default priority ([SR template](https://help.cityworks.com/Admin/3-8/Content/ServiceRequests/ServiceRequestTemplateFields.htm), [WO template](https://help.cityworks.com/Admin/3-8/Content/WorkOrders/WorkOrderTemplateFields.htm)). Priority values are a plain code list (code, description, active), with no weights ([priority values](https://help.cityworks.com/Designer/OC/Content/Preferences/AddorEditPriorityValues.htm)). No Severity field was found.
- **The "promised date" is a native due date.** The projected completion date "calculates using the Duration and Duration Units" set on the SR template, and stays blank if none is set. † (same Respond 4.3 page). The WO template's Days to Complete sets Projected Finish and is used to find past-due work orders (WO template page above). **Inferred:** St. Louis has configured durations for nearly every SR type, since `PrjCompleteDate` is filled on 19,804 of 19,821 extracted values.
- **No native escalation or SLA engine was found.** Email events fire on field values, not elapsed time ([email events](https://help.cityworks.com/Admin/3-2/Content/Email/AddorEditanEmailEvent.htm)), and Action Manager offers activity updates and webhooks ([Action Manager](https://help.cityworks.com/Designer/15-7/Content/ActionManager/ActionManager.htm)). This is a negative search result, not proof of absence.
- **No ranking engine; inbox order comes from saved searches.** The inbox is built from saved-search widgets ([inbox widgets](https://help.cityworks.com/Designer/OC/Content/ActionManager/AddaMessageQueueSavedSearchtotheInbox.htm)), ordered by each search's sort field ([inbox](https://help.cityworks.com/iOS/11-3/Content/RestOfTheTopics/Inbox.htm)). Mobile can sort SRs by priority ([mobile sort](https://help.cityworks.com/TrimbleUnityMobileCityworks/15-7/Content/ServiceRequests/SortServiceRequests.htm)). Trimble reports that Cityworks Analytics runs on ArcGIS Insights ([Trimble blog, 2023](https://www.trimble.com/en/blog/construction/article/get-to-know-your-cityworks-apps)).
- **Crew planning exists as a separate product, "Workload".** It shows a list beside a map, filters by dates and crew, and you drag a WO to an employee ([Workload 2.1](https://help.cityworks.com/Workload/2-1_15-6/Content/15-6/AssignWorkOrders.htm)). Version 3.0 adds a calendar to "drag unscheduled work" onto ([Workload 3.0 calendar](https://help.cityworks.com/Workload/3-0/Content/CalendarView.htm)). Allocation Manager totals Effort hours per employee ([Allocation Manager](https://help.cityworks.com/AMS/OC/Content/AllocationManager/AllocationManager.htm)). Nothing called "Crew Planner" was found. The [Workload product page](https://assetlifecycle.trimble.com/en/products/software/cityworks-workload) now redirects to a Trimble Unity page that does not mention Workload (dead link, observed by the sub-check).
- **LINK's mechanism is native.** In Cityworks 23, a linked SR "closes automatically when the work order is closed." † [Close a work order (Office Companion, Cityworks 23+)](https://help.cityworks.com/AMS/OC/Content/AMS/OC/WorkOrder/CloseAWorkOrder.htm); same in [Respond 5.1](https://help.cityworks.com/Respond/5-1/Content/WorkOrder/CloseAWorkOrder.htm).

**Inferred, plain statement:** Cityworks 23 natively offers a per-type priority label, a per-type due date, saved-search inboxes, and (if licensed) a map-and-calendar crew scheduler. It does not appear to compute a ranked list that combines hazard, lateness and repeats. Whether St. Louis sets priorities, uses Workload, or sorts saved searches by anything other than date is unknown from outside.

**Inferred (consequence for the pitch):** do not demo "crew day-plans"; Workload is the vendor's answer and may already be licensed. The ranking is a candidate **sort order and default priority map** that a division could load into its saved searches or template priorities. It is not a parallel system.

### 1c. What we cannot know without staff access

- Whether SR `Priority` / `Emergency` are set at intake or by the division, and how often.
- What each division's supervisor actually sorts by: Cityworks inbox, saved search, paper list, or the crew lead's judgment.
- Whether the city licenses Cityworks crew-scheduling or analytics add-ons.
- How `PrjCompleteDate` is computed per problem code.

**Inferred:** these are the first four questions to ask city staff. The pitch should say "if you already do this, the useful part is the close-out split and the weekly count".

## 2. What data we have to score honestly

Base: the E5 ledger of **14,902** open requests filed since 1 Jan 2025 and past their promised date on 13 Oct 2026 (`build/E5/summary.json`, from the public 311 file in `build/stl.duckdb`). The site's queue (`build/E3/queue_rows.json`) shows **14,573** of them. The gap is 329 rows: 320 of sensitive types plus 9 routed to SLMPD, which E3 counts in totals but never lists ([scripts/exec/E3/build_queue.py](../scripts/exec/E3/build_queue.py) lines 69, 96). All observed 2026-10-14 against local builds.

| Signal | Available? | What we observed | Usable for score? |
|---|---|---|---|
| Request type (problem code) | Yes, every row | 369 division × type combinations | **Yes**, the hazard tier |
| Division | 14,866 of 14,902 | 46 values; Forestry 4,679, Street 510 4,185, Building 1,219 | Yes, as a filter (rank within division) |
| Days past promise | Every row | Median 152; 2,206 are ≤30 days, 5,972 are 31–180, 6,724 are >180, 4,052 are >365; max 645 | **Yes**. Already normalised by type, because the promise window is the city's own per type |
| Filing date | Every row | 2025-01-01 to 2026-10-11 | Redundant with days past promise |
| Block | 14,829 rows (73 missing) | 10,384 division-blocks; 2,560 blocks hold ≥2 overdue items (7,005 rows); 959 hold ≥3 (3,803 rows); max 26 | Display only (crew grouping), not scored |
| Repeat reports (same address + type, open) | Address on every row (private) | 402 address-type groups with ≥2 open past-promise filings (956 rows); 53 with ≥3; the largest is 51 "Inspect City Tree" at one address | Yes, **capped**. Groups >10 look like bulk entry |
| Later filings, any status (E5 `n_later`) | Every row | 1,467 rows have ≥1 later filing at same address + type; 350 have ≥2; max 42 | Used through E5 class c, not scored again |
| Request text | **No** | `DESCRIPTION` holds 223 distinct category labels, mean 20.6 characters; a keyword scan found almost nothing request-specific | No. Kills text-based severity |
| Status | Every row | Disptch 6,678; NEW 3,841; Pending 1,983; Inspect 1,666; SCHEDULED 254; ON HOLD 89 | Display only. "Disptch" means sent to a crew, not done |
| E5 evidence class | Every row | a done-after-filing 388; b pending in records 1,206; c possibly superseded 333; d admin leftover 409; e no evidence 12,566 | **Yes, as a router**, not as points |

**Observed:** the evidence class matters most. 1,130 records (a + c + d) already carry evidence that the job was done, superseded, or is paperwork. Ranking them for a crew would put a supervisor's attention on records that need a desk to close them, not a truck. The other 13,772 (b + e) are the ranked list. Class b (1,206) keeps its rank but is tagged "work order open".

**Reported:** 311 call volume is not neutral. In Kansas City, Missouri, lower-income and minority neighbourhoods filed fewer street and nuisance complaints despite greater measured need ([Kontokosta & Hong 2021, NYU Marron summary](https://marroninstitute.nyu.edu/papers/bias-in-smart-city-governance-how-socio-spatial-disparities-in-311-complaint-behavior-impact-the-fairness-of-data-driven-decisions); Sustainable Cities and Society 64, 102503, doi:10.1016/j.scs.2020.102503). **Inferred:** a repeat-report term rewards neighbourhoods that call more. That is why it is capped at +10 of 100 and shown separately. It is a bias control, not an equity weighting, so it stays within the entry's no-equity-claims rule.

## 3. The proposed score

**Design rule (inferred):** every point traces to one field the city already records, and the "why" line shows each term. No model, no text mining, no demographics.

**Step 0: route before ranking.** E5 class a, c or d → **Close-out list** ("evidence the job is done / superseded / administrative; verify and close"). Class b or e → **Ranked list**.

**Step 1: score = H + D + R (0–100).**
- **H, hazard tier by request type:** Tier 1 = 60, Tier 2 = 30, Tier 3 = 0. Mapping below.
- **D, lateness:** 1 point per 12 full days past the promised date, capped at 30 (reached at 360 days). Consequence: **a year late counts as one hazard tier**, so nuisance work rises over time instead of waiting forever. This is "ageing", the standard scheduler fix for starvation.
- **R, repeats:** +5 per additional open report of the same type at the same address, capped at +10.
- **Ties:** more days past promise first.

**Not scored, shown beside the row:** "N other overdue [division] jobs on this block". This gives crew grouping without letting dense blocks outrank sparse ones. Status ("Disptch", "NEW") is shown as recorded.

**Hazard tier mapping (by problem code; edit per division).** Tier 1 means life-safety, a blocked right of way, or loss of an essential service. Tier 2 means a hazard or loss of function that is not immediate. Tier 3 means property maintenance, nuisance, amenity or administrative.

| Tier | Problem codes (open past-promise count in base where ≥20) |
|---|---|
| 1 | City Tree Down (312+9), City Tree Limb Down (268), Broken/Hanging Limb (305), Cave-Ins (1,233), NOWATER (118), WTR-COMING-UP (174), HYDRANT-HIT (23), MISSING-COVER (26), LOOSE-COVER, Building Collapse (78), Signal Dark / Signals Flashing / Signal Stuck / Signal Damaged / Other Signal Damaged, Whole Blk Lights Out, Sprinkler Systems, No Smoke Detectors, Fire Exit Insp, Dangerous Animal, Hazrds Waste, Potholes – Major St, TDebris-alley/street (363) |
| 2 | Inspect City Tree (1,481), LRA Tree (368), Inspect Private Tree "possibly hazardous" (230), Sidewalk Repair (1,124), Bad Condition (621), Sewer Lateral Defect (455), Illegal Use of right of way (362), Ppty Maint Code-Ext (379) / -Int (215), Vacnt Bldg Unsecured (160), Single Light Out (183), Light Damaged (110), Sign needs attention (98), Potholes – Residnl / Alley, PRESSURE (64), CHK-JOBSITE (51), FH-RUNNING (39), FH-MAINTENANCE (29), Rats (Exterior) (125), Lead Insp (266), Mechanical (111) / Plumbing (87) / Electrical Insp, No Hot Water, Sirens Not Heard (220), Vehicle-Rt of Way (205), Mosquito Breeding (101), Stagnant Water, Check Welfare, Injured/Sick Animal, Stray Dog At Large |
| 3 | Everything else, e.g. Weeds-Occupied Ppty (1,062), Weeds-Vacant Bldg/Lot, Missed / Unsatisfy Cut, Tree Planting (204), Stump Removal (62), Illegl Use-Opn Storg (248), Vehicle Towing (451), Mosquito Spraying (106), NOSPRAY, graffiti, refuse containers, new-sign and street-painting requests, Misc-* |

Tier counts in the base: **Tier 1 = 2,991, Tier 2 = 7,423, Tier 3 = 4,488** (observed in simulation). Judgment calls a division should review first: Sirens Not Heard (T2; arguably T1 as a warning-system fault), Lead Insp (T2; arguably T1 where children are present, which we cannot see), Sign needs attention (T2; a missing stop sign is T1, but the code does not say), and Illegal Use (T2; blocking vs. obstruction is not distinguished).

**How a division re-weights it (inferred design).** One plain file, e.g. `site/data/rank-weights.json`, holds three tier points, a days-per-point value, a lateness cap, a repeat step and a repeat cap, plus a `tier_overrides` map of problem code → tier, set per division. The page recomputes in the browser, so a supervisor can move "Sirens Not Heard" to Tier 1 or set lateness to 1 point per 6 days and see the list reorder. Nothing is learned from data, so nothing drifts.

**Simulation on the 14,902 (observed, 2026-10-14):**
- 13,772 ranked; 1,130 routed to close-out.
- 2,778 Tier-1 rows in the ranked list. The citywide top 500 are all Tier 1.
- Overlap of ranked top 25 with oldest-first top 25, by division:
  - Forestry: 0 overlap (Tier-1 rows in top 25: 9 oldest-first vs 25 ranked).
  - Street 510: 0 overlap (1 vs 25).
  - Building: 2 overlap (2 vs 25).
  - Water: 18 overlap (18 vs 25; Water's oldest items are already mostly Tier 1).
  - Traffic 511: 13 overlap (1 vs 6).
- The citywide top 15 are tree limbs down, cave-ins and tornado street debris, 330–582 days past promise. All but one are status "Disptch", and each has 2–4 open reports of the same type at the same address. **Inferred:** in a real build, collapse same-address, same-type reports into one row ("4 reports").

**Inferred, and the main garbage-in risk:** the top of the ranked list is exactly where "done but never closed" is most likely. The 84% no-evidence share applies there too. So the honest label for the ranked list is **"call these first"**: either confirm the work and close the record (COUNT gets a true number), or find a tree limb that has been down for 18 months. Either result is worth the call. The ranking does not claim these jobs are undone.

Other risks:
- Type is what the resident chose, and some are miscoded: an "Inspect City Tree" can be a hanging limb.
- `PrjCompleteDate` reflects each type's configured window, not risk.
- 77 ranked rows sit in address-type groups of more than 10. Those look like bulk or placeholder entries and should be flagged "check".
- Block grouping is block-level only on the public site. Exact crew routing would need addresses the site deliberately omits.

## 4. Recommendation and minimum credible build (inferred)

**Build: yes, as a toggle on the existing list, not a new product.** About 2–3 hours of agent work:

1. `scripts/exec/E7/build_rank.py`: reads `build/E5/private/ledger_rows.parquet` and `build/stl.duckdb`. Computes the tier, the repeat count (private address join, output as a count only), the block-mates count and the route. Applies the same sensitive-type exclusion as E3. Writes `build/E7/rank_rows.json` (block level, no request ids, no addresses), shaped like `queue_rows.json` plus `tier`, `repeat_n`, `block_mates`, `route` and `evidence_class`. It writes figures to the same figures/facts pattern E3 uses.
2. `site/data/rank-weights.json`: the weights and the tier map above, with a comment line per tier.
3. `site/js/queue.js` + `site/queue.html`: an "Oldest first | Ranked | Close-out" toggle. The ranked view shows a "why this rank" line per row, e.g. *Tier 1 · tree limb down (+60) · 538 days past promise (+30) · 3 open reports here (+10) = 100 · 4 other overdue Forestry jobs on this block*. A "Weights" drawer shows the file's values and lets a viewer edit them in the session, with reset.
4. A short methods note on the page. It names the four fields used, says what is not used (text, demographics, AI), and states the reporting-bias cap.
5. Check: re-run the simulation numbers above from `rank_rows.json`, and confirm no ids or addresses ship (reuse the E3 privacy scan).

**Not included:** crew day-plans (they need crew counts, shift capacity and exact locations, which we do not have), heat maps beyond the existing map, and any "AI" label.

**Video, two sentences:**
> "We don't know how each division orders its work today; if it isn't already in your system, here is a ranking anyone can check: hazard of the request type, how far past the city's own promised date it is, and repeat reports, with every point shown on the row. Records that already show the job was done go to a separate close-out list, so crews see fieldwork and the desk sees paperwork."

What not to say: that the ranking finds undone work, that it is AI, or that it is better than what supervisors do now.
