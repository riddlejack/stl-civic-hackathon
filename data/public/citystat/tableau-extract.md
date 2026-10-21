# CityStat Tableau summary data, as extracted

Method: loaded each CityStat page in a browser on 2026-10-13 (23:14–23:40 UTC), then read each embedded
`<tableau-viz>` element's worksheets with the Tableau Embedding API v3 call `getSummaryDataAsync()`
(the same summary data the chart draws). Values are raw (unrounded to 4 dp), re-ordered chronologically
here for reading. Page narrative says "data last updated June 30th, 2026".

## Forestry — /parks/forestry-division.cfm

### Forestry-30DayRemovals/Dashboard1 — "Percent Work Orders Closed" (hazard tree removals within 30 days; goal 100%)
Year-Q | % removed in 30 days (formatted) | work orders initiated
2024 Q1 | 14% | 73
2024 Q2 | 14% | 240
2024 Q3 | 10% | 224
2024 Q4 | 28% | 120
2025 Q1 | 20% | 87
2025 Q2 | 19% | 306
2025 Q3 | 17% | 292
2025 Q4 | 23% | 77
2026 Q1 | 40% | 141
2026 Q2 | 37% | 145
(chart labels seen in screenshot: 13.7, 14.2, 10.3, 28.3, 19.5, 19.0, ~16.8, 23.4; year averages 15.4% for 2024, 18.6% for 2025)

### TreeRemovalsQuarterlyBreakdownExternal/TreeRemovalsSimplified — "Tree Removals Backlog Size"
Quarter | cancelled | closed | initiated | open work orders at quarter end
2019 Q4 | 2 | 5 | 38 | 31
2020 Q1 | 9 | 20 | 35 | 37
2020 Q2 | 3 | 23 | 87 | 98
2020 Q3 | 5 | 19 | 57 | 131
2020 Q4 | 1 | 23 | 53 | 160
2021 Q1 | 2 | 51 | 24 | 131
2021 Q2 | 1 | 40 | 157 | 247
2021 Q3 | 3 | 49 | 147 | 342
2021 Q4 | 9 | 56 | 47 | 324
2022 Q1 | 1 | 29 | 43 | 337
2022 Q2 | 5 | 56 | 144 | 420
2022 Q3 | 2 | 73 | 134 | 479
2022 Q4 | 1 | 49 | 53 | 482
2023 Q1 | 5 | 63 | 52 | 466
2023 Q2 | 4 | 29 | 103 | 536
2023 Q3 | 2 | 18 | 156 | 672
2023 Q4 | 0 | 99 | 89 | 662
2024 Q1 | 1 | 150 | 70 | 581
2024 Q2 | 0 | 95 | 243 | 729
2024 Q3 | 6 | 136 | 231 | 818
2024 Q4 | 10 | 130 | 128 | 806
2025 Q1 | 14 | 177 | 96 | 711
2025 Q2 | 2 | 138 | 316 | 887
2025 Q3 | 10 | 193 | 306 | 990
2025 Q4 | 16 | 231 | 79 | 822
2026 Q1 | 1 | 231 | 141 | 731
2026 Q2 | 27 | 260 | 147 | 591

### VacantProperyClearanceRates/ofVacantLotsandWorkOrders — vacant lots mowed, first rotation 2026 (Apr 6–May 26)
Ward | total lots | lots mowed | rate
1 | 288 | 74 | 0.26
2 | 35 | 8 | 0.23
3 | 165 | 27 | 0.16
4 | 58 | 0 | 0.00
5 | 48 | 1 | 0.02
6 | 30 | 0 | 0.00
7 | 169 | 37 | 0.22
8 | 148 | 8 | 0.05
9 | 88 | 11 | 0.13
10 | 791 | 423 | 0.53
11 | 2,052 | 1,300 | 0.63
12 | 3,057 | 2,054 | 0.67
13 | 2,705 | 1,603 | 0.59
14 | 2,537 | 1,553 | 0.61
(sum: 12,171 lots, 7,099 mowed = 58.3%)

### VacantProperyClearanceRates/ofVacantBuildingsandWorkOrders — vacant building parcels trimmed, as of 2026-06-30
Ward | total parcels | trimmed | rate
3 | 342 | 59 | 0.17
7 | 199 | 9 | 0.05
8 | 91 | 22 | 0.24
10 | 468 | 173 | 0.37
11 | 592 | 41 | 0.07
12 | 1,288 | 450 | 0.35
13 | 1,143 | 279 | 0.24
14 | 515 | 15 | 0.03
(sum: 4,638 parcels, 1,048 trimmed = 22.6%; wards 1,2,4,5,6,9 not shown)

## Parks — /parks/parks-division.cfm

### Parks-On-TimePercentage — "All Parks Requests" (goal 80% on time)
Year-Q | on-time share | requests
2024 Q1 | 0.3804 | 92
2024 Q2 | 0.2256 | 297
2024 Q3 | 0.3188 | 298
2024 Q4 | 0.3268 | 153
2025 Q1 | 0.2107 | 242
2025 Q2 | 0.2298 | 383
2025 Q3 | 0.2670 | 352
2025 Q4 | 0.5101 | 198
2026 Q1 | 0.4398 | 166
2026 Q2 | 0.6746 | 378

### Parks-On-TimePercentbyProblemCode (page says "Data as of 6/30/2026"; period of the view not stated in data)
Problem code | on-time share | requests
Dead Limbs in Park | 0.25 | 16
Graffiti-Park Equip | 0.375 | 24
Athletic Fields | 0.4545 | 44
Playground Equipment | 0.48 | 50
Trash in the Park | 0.50 | 88
High Grass in Park | 0.5143 | 35
Misc-Parks Div | 0.5161 | 31
Park Restrooms | 0.5625 | 16
Rec Bldg Maintenance | 0.6061 | 66
Park Sewer Problem | 0.7143 | 7
Cut Median-Pkwy | 0.7882 | 85
Park Lake | 0.8182 | 11
Ballfield Benches | 0.8571 | 7
Fountains | 0.9375 | 32
Rec-Athletic Lights | 0.9412 | 17
Leaves in Park | 1.0 | 1
Maintain Bike Trail | 1.0 | 4
(sum 534 requests ≈ Q1+Q2 2026 total of 544, so this view is probably 2026 year-to-date — inferred)

## CSB — /public-safety/csb.cfm

### CSBRoutingTime — share of requests routed in ≤2.5 days (goal 95%)
Year-Q | share | requests
2024 Q1 | 0.9646 | 10,664
2024 Q2 | 0.9853 | 13,110
2024 Q3 | 0.9785 | 12,469
2024 Q4 | 0.9932 | 8,262
2025 Q1 | 0.9737 | 12,967
2025 Q2 | 0.9464 | 14,884
2025 Q3 | 0.9351 | 15,678
2025 Q4 | 0.9627 | 9,304
2026 Q1 | 0.9387 | 10,643
2026 Q2 | 0.9999 | 10,853
(note: these request counts are far below the ward-map totals below; the routing view evidently counts a subset — inferred)

### CSBRequestMap — average days to close and closed share by ward, 2024-01-01 to 2026-06-30
Ward | avg days to close | requests | closed | closed share
1 | 17.18 | 23,417 | 19,603 | 0.8371
2 | 19.44 | 21,712 | 17,364 | 0.7997
3 | 22.77 | 19,074 | 16,543 | 0.8673
4 | 19.69 | 21,251 | 17,484 | 0.8227
5 | 19.91 | 19,340 | 15,363 | 0.7944
6 | 27.76 | 18,280 | 14,384 | 0.7869
7 | 27.44 | 22,822 | 18,786 | 0.8232
8 | 27.89 | 20,313 | 16,551 | 0.8148
9 | 32.59 | 12,206 | 9,966 | 0.8165
10 | 35.07 | 19,467 | 15,218 | 0.7817
11 | 30.67 | 16,361 | 13,816 | 0.8444
12 | 30.33 | 25,722 | 21,626 | 0.8408
13 | 24.32 | 28,423 | 24,319 | 0.8556
14 | 27.54 | 17,034 | 14,600 | 0.8571
Null | 13.82 | 726 | 532 | 0.7328
(sum: 286,148 requests, 236,155 closed = 82.5%; 49,993 not closed in the view)

### WinterResponseComparison — snow/ice requests by week
Week of | requests | avg completion days
2024-12-29 | 1 | 1.80
2025-01-05 | 639 | 14.19
2025-01-12 | 1,709 | 17.41
2025-01-19 | 386 | 11.24
2025-01-26 | 51 | 2.09
2026-01-11 | 8 | 0.30
2026-01-18 | 21 | 2.24
2026-01-25 | 1,334 | 3.07
2026-02-01 | 100 | 1.10
2026-02-08 | 1 | 0.01

## Street Division — /street/streets.cfm

### PotholeRepairOpetion1 — share of pothole requests repaired within goal (goal 80%) and request counts
Quarter | Major St (3-day) share / n | Residential (8-day) share / n | Alley (17-day) share / n
2024 Q1 | 0.1731 / 543 | 0.4109 / 920 | 0.4872 / 78
2024 Q2 | 0.0624 / 529 | 0.1405 / 1,025 | 0.1788 / 151
2024 Q3 | 0.1396 / 838 | 0.2637 / 2,575 | 0.0966 / 145
2024 Q4 | 0.0129 / 311 | 0.0173 / 346 | 0.0286 / 70
2025 Q1 | 0.0923 / 921 | 0.2236 / 711 | 0.3878 / 147
2025 Q2 | 0.3056 / 648 | 0.7162 / 948 | 0.8777 / 188
2025 Q3 | 0.3647 / 329 | 0.5126 / 437 | 0.5859 / 99
2025 Q4 | 0.2593 / 270 | 0.4261 / 399 | 0.6104 / 77
2026 Q1 | 0.1849 / 703 | 0.4386 / 969 | 0.7063 / 126
2026 Q2 | 0.4447 / 443 | 0.9061 / 916 | 0.9823 / 113

### DebrisRemovalv2 — share of debris requests completed within goal (goal 80%) and request counts
Quarter | Alley/Street (3-day) share / n | Vacant Bldg (14-day) share / n | Vacant Lot (14-day) share / n
2024 Q1 | 0.5297 / 825 | 0.5963 / 109 | 0.4295 / 156
2024 Q2 | 0.4134 / 687 | 0.5463 / 108 | 0.4926 / 136
2024 Q3 | 0.4875 / 1,081 | 0.7115 / 104 | 0.7109 / 128
2024 Q4 | 0.3941 / 609 | 0.3881 / 67 | 0.4045 / 89
2025 Q1 | 0.1096 / 584 | 0.3261 / 92 | 0.2288 / 118
2025 Q2 | 0.7031 / 1,216 | 0.8140 / 86 | 0.7535 / 142
2025 Q3 | 0.5622 / 1,407 | 0.9247 / 93 | 0.8261 / 161
2025 Q4 | 0.5283 / 441 | 0.8974 / 78 | 0.7474 / 95
2026 Q1 | 0.7617 / 470 | 0.8831 / 77 | 0.9211 / 114
2026 Q2 | 0.7857 / 546 | 0.9552 / 67 | 0.9735 / 113

## Refuse — /street/refuse.cfm

### QuarterlyRouteCoverage (goal 95%)
Quarter | share of routes reporting | route coverage | routes scheduled | routes reported
2024 Q1–2025 Q2 | no data (not recorded before Sept 2025)
2025 Q3 | 0.6635 | 0.7582 | 315 | 209
2025 Q4 | 0.9172 | 0.8658 | 1,365 | 1,252
2026 Q1 | 0.9861 | 0.9736 | 1,365 | 1,346
2026 Q2 | 0.9897 | 0.9423 | 1,260 | 1,247

### WeeklyCoveragePercent — monthly completion of scheduled refuse service (goal 95%)
2025-09 0.7582 | 2025-10 0.6950 | 2025-11 0.8682 | 2025-12 0.9667 | 2026-01 0.9509 | 2026-02 0.9905 | 2026-03 0.9776 | 2026-04 0.9243 | 2026-05 0.9271 | 2026-06 0.9751

### RecyclingTonnage — share of collected recycling tonnage successfully recycled, month vs same month prior year
Month | current | prior year
Sep 2025 0.9696 | Sep 2024 0.4549
Oct 2025 0.9839 | Oct 2024 0.3251
Nov 2025 0.9904 | Nov 2024 0.3837
Dec 2025 0.9799 | Dec 2024 0.3396
Jan 2026 0.9807 | Jan 2025 0.3280
Feb 2026 0.7604 | Feb 2025 0.3924
Mar 2026 0.7592 | Mar 2025 0.6327
Apr 2026 0.7607 | Apr 2025 0.4342
May 2026 0.7590 | May 2025 0.3333
(no June 2026 row in the view)

## Traffic & Lighting — /street/traffic.cfm

### WholeBlockLightsOut — share of "whole block lights out" requests completed within 24 h (goal 80%)
Quarter | share | requests
2024 Q1 | 0.7350 | 349
2024 Q2 | 0.7833 | 299
2024 Q3 | 0.7947 | 413
2024 Q4 | 0.7592 | 490
2025 Q1 | 0.5281 | 640
2025 Q2 | 0.5574 | 601
2025 Q3 | 0.6639 | 482
2025 Q4 | 0.7379 | 597
2026 Q1 | 0.7833 | 420
2026 Q2 | 0.8017 | 358

### CriticalSign — share of critical sign (Stop/Yield/One-Way/Do Not Enter) requests completed within 48 h (goal 75%)
Quarter | share | avg days open | requests (distinct) | within 48h | total sign requests
2024 Q1 | 0.3149 | 6.55 | 181 | 57 | 212
2024 Q2 | 0.3795 | 5.83 | 166 | 63 | 171
2024 Q3 | 0.1452 | 13.32 | 124 | 18 | 132
2024 Q4 | 0.1724 | 9.32 | 116 | 20 | 123
2025 Q1 | 0.4571 | 5.34 | 210 | 96 | 225
2025 Q2 | 0.4072 | 6.93 | 167 | 68 | 169
2025 Q3 | 0.4803 | 5.52 | 152 | 73 | 177
2025 Q4 | 0.5630 | 3.47 | 119 | 67 | 145
2026 Q1 | 0.6947 | 2.56 | 95 | 66 | 104
2026 Q2 | 0.5893 | 5.40 | 112 | 66 | 118

## Towing — /street/towing.cfm

### TowingData/NumberofVehiclesTowed — FAILED TO RENDER
Three attempts 23:40–23:46 UTC. The embedded view shows the message: "Tableau detected that your OAuth
refresh token is expired. Reauthenticate with new credentials. Ask your Tableau admin if you need help. /
This sheet uses data that's on a Snowflake database. You need to sign into that server." No tow counts
are visible to the public on this chart.

### TowingDispatchDates/TowingDispatch — CSB tow-related requests by quarter and status
Quarter | closed | open
2024 Q1 | 1,318 | 0
2024 Q2 | 1,358 | 0
2024 Q3 | 1,431 | 0
2024 Q4 | 1,231 | 0
2025 Q1 | 1,533 | 0
2025 Q2 | 1,782 | 0
2025 Q3 | 2,208 | 16
2025 Q4 | 1,703 | 25
2026 Q1 | 1,776 | 105
2026 Q2 | 1,075 | 562

## Water — /utilities/water-division.cfm

### WaterMainServiceRestoration — share of emergency main repairs restored in <8 h (goal 80%)
Quarter | share | incidents
2024 Q1–2025 Q3 | no data
2025 Q4 | 0.6522 | 23
2026 Q1 | 0.6102 | 236
2026 Q2 | 0.6418 | 134

## Building — /public-safety/building-division.cfm

### BuildingPermitPerformanceFinal — share of building permits issued within 30 days (goal 80%)
2024 Q1 0.7838 | Q2 0.7319 | Q3 0.7234 | Q4 0.6362
2025 Q1 0.6805 | Q2 0.7022 | Q3 0.8118 (met) | Q4 0.7295
2026 Q1 0.7052 | Q2 0.6664
(no permit counts in the view's summary data)

## Personnel — /personnel/index.cfm

### Personnel-TotalTimetoHire — share of offers accepted within 30 days of application (goal 90%)
Quarter | share | candidates | requisitions
2024 Q1 | null | 0 | 0
2024 Q2 | null | 502 | 156
2024 Q3 | null | 244 | 130
2024 Q4 | null | 210 | 120
2025 Q1 | 0.4088 | 203 | 84
2025 Q2 | 0.7480 | 143 | 78
2025 Q3 | 0.7584 | 177 | 102
2025 Q4 | 0.9214 | 160 | 90
2026 Q1 | 1.0000 | 18 | 15
(no 2026 Q2 row)

## Health — /health/index.cfm

### CityServices-FB — routine food & beverage inspections on time (goal 85%)
Quarter | on-time share | routine inspections
2024 Q1 | 0.6470 | 1,092
2024 Q2 | 0.6999 | 1,059
2024 Q3 | 0.6022 | 1,069
2024 Q4 | 0.6952 | 886
2025 Q1 | 0.5403 | 973
2025 Q2 | 0.5795 | 922
2025 Q3 | 0.6097 | 1,056
2025 Q4 | 0.6181 | 981
2026 Q1 | 0.8910 | 1,060
2026 Q2 | 0.9113 | 1,032

## Human Services — /human-services/index.cfm (HELP-STL right to counsel, run by Legal Services of Eastern Missouri)

### CasesClosedandOpened
Quarter | opened | closed | open at quarter end
2024 Q3 | 44 | 7 | 37
2024 Q4 | 71 | 52 | 59
2025 Q1 | 93 | 29 | 126
2025 Q2 | 69 | 58 | 130
2025 Q3 | 74 | 66 | 137
2025 Q4 | 66 | 102 | 101
2026 Q1 | 55 | 86 | 71
(sum opened 472, closed 400)

### TotalFinancialAid — financial impact by quarter, USD
2024 Q3 8,979.50 | 2024 Q4 60,865.71 | 2025 Q1 63,013.23 | 2025 Q2 125,977.57 | 2025 Q3 127,984.67 | 2025 Q4 186,843.29 | 2026 Q1 238,235.25
(sum 811,899.22 — equals the page's "$811,900", so that figure covers Aug 2024–Mar 2026, not "August 2025 through March 2026" as the page text says)
