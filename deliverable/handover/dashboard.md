# The overdue dashboard: an ArcGIS Dashboard definition

**For** the city's GIS administrator. One dashboard on the city portal, shared to staff, that a division supervisor opens each week and CityStat reads each quarter. Labels as in [saved-search.md](saved-search.md).

**Already there [observed]:** the city portal has ArcGIS Dashboards installed. Seven public city maps already read Cityworks saved searches, but none is in a dashboard. None of the four public city dashboards showed data to a visitor on 14 Oct (data-source errors). This would be the city's first working operations dashboard, so keep it staff-only until it has run for a few weeks **[our design]**.

## Data sources

| Source | What | Refresh |
|---|---|---|
| **The eURL layer** from the overdue saved search ([saved-search.md](saved-search.md)): one per division, or one citywide with a division field | Every open request past its date with no finished job, with block, type, days past, status, tier, score and why | Live: the event layer reads Cityworks when it is drawn **[inferred]** |
| **Tree-removal work orders** past projected finish (the existing "Tree Removal WOs" search, through eURL) | The tree-removal test count | Live **[inferred]** |
| **Baselines**: three fixed numbers from 13 Oct 2026 | Tree removals 1,630; cave-ins 1,233; vacant-lot mowing 289 | Fixed |
| **CityStat table**: a small table, loaded from the SQL output ([sql.md](sql.md)) | Per CityStat measure: published on-time share, rebuilt share, and the share that counts only closings that say the work was done | Each quarter. Cityworks does not classify closing words, so this table comes from the SQL, not from eURL |

## Widgets

| Widget | Shows | Built from | Prototype |
|---|---|---|---|
| **Selectors** (left sidebar) | Division, request type, hazard tier, ward | eURL layer fields | `site/queue.html` filters |
| **Overdue now, against the baseline** (three indicators) | For each test type: today's count, with 13 Oct's as the reference value and the difference | eURL layer counts; baseline as a fixed reference | `site/queue.html` headline |
| **"No record either way"** (indicator per test type) | Share of overdue requests with no crew job linked and no review outcome. The target is zero | eURL layer: rows with no linked work order and no outcome recorded in the weekly review. How the outcome is recorded is **[our design]**: a status or a comment the division sets | not in the prototype |
| **Map by block** | Overdue requests drawn at block scale, coloured by days past the date | eURL layer; points clustered or aggregated to blocks, never labelled by address **[our design]** | `site/queue.html` map |
| **Ranked list** | Rows sorted by score, each with its "why" line, block, due date and status; a "work order open" tag where a link exists | eURL layer, sorted by the score field. If the score isn't stored, sort by Priority then promised date (see saved-search.md §4) | `site/queue.html`, Ranked view |
| **Close-out list** | Records already showing the work done or superseded: desk work, no crew | Same layer, routed rows | `site/queue.html`, Close-out view |
| **CityStat, with one added column** | CityStat's nine 311 measures with its published on-time share, beside a column headed **"Closing says done"**: on time only when the closing words say the work was done. Example, alley and street debris in Q2 2026: 78.6% on time as CityStat published it **[reported]**, against 15.0% when only closings that say the debris was picked up count **[observed]** | CityStat table | `site/citystat.html` |

**Layout [our design], following the city's own dashboards [observed]:** Esri light theme; a left sidebar of selectors; the three baseline indicators across the top; the map and the ranked list side by side below; the close-out list and the CityStat table at the foot. Light Gray Canvas basemap.

**Weekly use.** The supervisor filters to the division, works the top 25 of the ranked list and the close-out list, and records each outcome: done, waiting or missed ([practice pages](README.md)). The indicators then move.

## What the prototypes are

`site/queue.html` (the past-due list: Oldest first, Ranked and Close-out views, the block map and the "why this rank" line) and `site/citystat.html` (the nine measures with the "Closing says done" column) are **working prototypes of these views**. They run on the city's public 311 file of 13 Oct 2026 and on the editable weights in `site/data/rank-weights.json`. `site/status.html` is the matching spec for the resident's status page.

The prototypes are not connected to Cityworks. The dashboard replaces them with live layers, and its numbers will drift from the prototype's as the city's records change **[inferred]**.
