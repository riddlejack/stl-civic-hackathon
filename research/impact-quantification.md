# Impact quantification: what LINK / LIST / COUNT would make visible, recover, avoid or save

I used data on disk only, plus external benchmarks gathered by one web-search sub-agent; no city site was crawled. Scripts are in `scripts/exec/impact/` (01 to 04). Aggregates are in `build/impact/`, with no ids or addresses. Every figure is in `research/impact-quantification-facts.csv` (152 rows).

Labels: **observed** means I counted it on disk. **Reported** means a source says so. **Inferred** means my own conclusion. **Estimated** means it rests on an assumption, which is named.

## Summary

**What I found.** The fix's impact is mostly not money. What the fix does is make a known set of overdue hazards visible, and put a few dozen city-owned lots back on the rounds at a trivial cost. All of this happens inside software the city already licenses. The savings people usually expect are small, uncertain, or both:
- **Repeat requests.** 0 to about 1,000 a year; central 200, worth about $860 of 311 time.
- **Hand-closing labour.** 0 to about 1,080 staff hours a year; central 270.

Saying so plainly is stronger than inflating it.

**Headline numbers a video could say in one breath each:**

| # | Line | Label | Assumption on screen |
|---|---|---|---|
| H1 | "2,778 life-safety requests (cave-ins, trees and limbs down, water coming up) are past the date the city promised, a median of 239 days." | observed | "Life-safety" is our tier map by request type (editable, `site/data/rank-weights.json`). Open and past the promise on 13 Oct 2026. Requests with evidence of being done, superseded or administrative are removed. |
| H2 | "1,630 trees the city has already ordered removed are past the finish date on their own work orders, a median of 618 days." | observed | Cityworks "Tree Removal WOs" saved search, read-only extract of 14 Oct 2026, operational fields only. Projected finish is the date the city's own work-order template sets. |
| H3 | "52 city-owned lots were told 'on schedule to be cut' this year and never were. Cutting them for a season would cost about $7,000 at the city's own billed rate." | count observed; cost estimated | The cost is the median $132 billed per city-owned lot cut in 2026. Wider definitions give 82 lots for about $12,000, or 171 lots for about $31,000. |
| H4 | "Linking requests to work orders that already exist would show what happened to about 1,500 of the 12,566 overdue requests no record explains. A weekly review of 25 per division would settle about 3,500 more in a quarter." | estimated | The first figure scales E1's 30-page samples per type. The second assumes 14 divisions, 25 records a week each, 13 weeks. |
| H5 | "Setting it up takes about 150 staff hours, about $7,000, in software the city already owns. Running it takes about an hour per division per week. Fresno paid about $1 million for a new 311 system." | estimated + reported | The hours are itemised in §6. The rate is the BLS St. Louis mean wage of $31.89 × 1.4 for benefits. Fresno 2023: $395,724 implementation plus $610,344 licences. |

**What I could not establish.**
- **Status chasing.** There is no status-call or web-lookup count on disk, so I did not estimate it (§2).
- **Who closes hand-offs today, and how long it takes.** Is it 311 staff or division staff? Do divisions re-key work orders or create them from the request? Section 3 therefore states its net saving only as a range from zero.
- **The split of the 12,566 between done, waiting and lost.** The fix would reveal it. Today's data cannot predict it.
- **Two earlier-draft counts.** Neither survives the closed-before-repeat rule (§7). The 20,697 repeat filings fall to 5,978 after a hand-off closure, and to 176 for durable types. I could not reproduce the 2,534 durable figure.

## 1. Repeat requests after hand-off closures

**Definition (as R2, extended to 60 and 90 days).**
- A closure counts as re-reported when another request with the same normalised address and problem code is filed **after the closure** (`next.ts_init > ts_closed`) and within k days. Any channel counts.
- Population: requests filed 1 Jan 2025 to 13 Oct 2026 00:33, closed, with an address.
- Windows count only if complete by the as-of time.
- Eligible types have at least 300 closures. Each class needs at least 30 closures with complete windows in that type.
- Rates are directly standardised to the hand-off type mix.
- Source: [311 file](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip); script `01_rereports.py`.
- At 30 days my figures reproduce R2 exactly: 9.62% vs 7.04% over 61 types and 34,220 closures (`build/R2/rereport_summary.json`).

**Observed, standardised rates (hand-off vs done):**

| Types | 30 days | 60 days | 90 days | Hand-off closures (90 d) |
|---|---|---|---|---|
| All eligible (59–61 types) | 9.62 vs 7.04 (+2.58) | 13.21 vs 9.96 (+3.26) | 15.45 vs 11.96 (+3.49) | 30,663 |
| Same, later report filed >24 h after the original | +2.41 | +3.11 | +3.36 | |
| Same, resident-channel re-reports only | +2.32 | +3.04 | +3.20 | |
| Non-recurring, non-dumping (11–12 types) | 7.76 vs 3.91 (+3.85) | 10.92 vs 7.04 (+3.89) | 13.32 vs 7.93 (+5.39) | 6,255 |
| Durable-fix types (cave-ins, lights, potholes, signs, city trees; 10 types) | 5.10 vs 3.13 (+1.96) | 7.47 vs 4.92 (+2.55) | 9.40 vs 5.89 (+3.51) | 2,852 |
| Recurring route services only (refuse, street cleaning, weeds; 18 types) | +2.42 | +2.12 | +1.52 | 12,929 |

**Two findings cut against counting these as harm (reported, R2).**
- **The gap may be mostly a timing artefact.** R2 anchored the window on the filing date instead of the closure: closures within 14 days, re-reported 15–44 days after filing. On that basis the pooled gap vanishes: 6.10% vs 6.04%, a difference of 0.06 points (CI −0.53 to 0.65). Hand-offs close sooner, so a closure-anchored window covers more of the wait. The gap holds only for non-recurring types, at 7.18% vs 4.01%.
- **Re-reports do not track unfinished work.** Where a completion record exists, they do not follow it. Board-ups with no recorded board-up were re-reported less often (5.9%) than those boarded by the promise (15.4%). Weed re-reports are flat with or without a cut.
- So re-reports are not used as proof of undone work.

**Estimate: excess re-reports a year attributable to hand-off closing.** Each case below is a standardised excess times the hand-off closures in the 12 months to 13 Oct 2026 (observed).

| | Low | Central | High |
|---|---|---|---|
| Basis | 0 (filing-anchored check) | +3.89 pts at 60 days, non-recurring types only; recurring types set to 0 | +3.49 pts at 90 days, all eligible types |
| Hand-off closures, 12 months | 29,899 | 5,138 | 29,899 |
| **Excess re-reports a year** | **0** | **200** | **1,043** |
| 311 cost at $4.28 a contact | $0 | $857 | $4,468 |
| 311 staff hours (5.4 / 6.0 / 7.0 min a contact) | 0 | 20 | 93 |
| Resident minutes per report (assumed) | 5 | 10 | 20 |
| Resident hours a year | 0 | 33 | 348 |
| Resident time at USDOT $17.00 an hour (2021 $) | $0 | $567 | $5,910 |

Durable-fix types alone give 42, 55 and 76 excess re-reports a year at 30, 60 and 90 days.

**Derivations.**
- **311 cost per contact: $4.28.** This is the CSB's FY2025 all-funds actual of $612,679 divided by its 143,008 contacts from all sources. Both figures are reported in the [FY2027 Annual Operating Plan, Public Safety, program 622-02](https://www.stlouis-mo.gov/government/departments/budget/documents/upload/11-FY2027-AOP-Public-Safety-2.pdf) (about p. 180). The same page shows 8.0 FTE and 112,916 requests entered. The figure is a direct cost only: it excludes overhead, the phone system and Cityworks. It sits between NYC's FY2025 figure of about $1.84 per contact (inferred from $68.3M over 37.1M contacts, [MMR 2025](https://www.nyc.gov/assets/operations/downloads/pdf/mmr2025/311.pdf)) and Pew's 2009 15-city median of $3.39 per call ([Pew 2010](https://www.pew.org/-/media/assets/2010/03/02/final-311-report-030210.pdf)). Toronto reports CA$11–16 per call ([Global News, 2024](https://globalnews.ca/news/10238190/toronto-311-call-cost-budget/), reported).
- **Staff minutes per contact.** 8 FTE × 1,600 / 1,800 / 2,080 productive hours a year (assumed), ÷ 143,008, gives 5.4 / 6.0 / 7.0 minutes. That is consistent with Philly311's 2009 average talk time of about 5 minutes plus 1:45 on hold (Pew 2010, reported).
- **Resident minutes.** These are an assumption. No source estimates a resident's total time per report. The low case is the talk time alone.
- **Resident value of time.** [USDOT BCA guidance, Jan 2023, Table A-3](https://www.dot.ny.gov/divisions/operating/opdm/passenger-rail/passenger-rail-repository/USDOT%20Benefit%20Cost%20Analysis%20Guidance%202023%20Update.pdf), personal travel, $17.00 per person-hour in 2021 dollars (reported).

**Inferred.** Even the high case is under $5,000 of 311 cost a year. Repeat requests are not a reason to adopt the fix, and should not be a video number.

## 2. Status chasing: skipped (no volume on disk)

- **Observed: no status-call, web-lookup or chat volume on disk.**
- **Inferred: the only bound is a ceiling.** In FY2025, 143,008 contacts minus 112,916 requests entered leaves **30,092 contacts that created no request**. Status checks are an unknown share of these; information calls, transfers and repeat calls are in the same number.
- **Reported, external, not applied:**
  - Toronto 2024: 6% of 1.29M interactions were status updates on existing requests ([Toronto CX report, Feb 2025](https://www.toronto.ca/legdocs/mmis/2025/se/bgrd/backgroundfile-253220.pdf)).
  - Chicago, 2012: "nearly 40 percent" of calls were duplicates or status checks ([ABC7](https://abc7chicago.com/archive/8817677)).
  - KMOV reported about 4,000 calls a month to St. Louis 311 ([12 Mar 2026](https://www.firstalert4.com/2026/03/12/city-highlights-citizen-service-bureau/), via `research/mayors-office-voice.md`).
- **Reported (city):** the acting director wants to answer "why it's past the completion date" before residents call ([hearing, 12 May 2026, ~3:31:10](https://www.youtube.com/watch?v=tyS2V5Ae98I)).
- **Also observed:** 2,565 closings of 2025 filings (5,576 for 2025–26) tell the resident to "call CSB" (`04_verify_brainstorm.py`).

## 3. Manual closing labour removed by auto-close

**Observed.**
- 61,845 requests filed between 1 Jan 2025 and 13 Oct 2026 were closed at the hand-off (`handed_off` + `converted`).
- **32,373** hand-off closures were made in the 12 months to 13 Oct 2026.
- Cityworks 23 closes a linked request "automatically when the work order is closed" (reported, [Cityworks help](https://help.cityworks.com/AMS/OC/Content/AMS/OC/WorkOrder/CloseAWorkOrder.htm)).

**Estimated.** The assumptions are gross minutes per manual closure (choose the closing words, close) and the share of that time *not* replaced by the new link step: someone has to create or link the crew's work order from the request.

| | Low | Central | High |
|---|---|---|---|
| Gross minutes per closure | 0.5 | 1 | 2 |
| Gross hours a year | 270 | 540 | 1,079 |
| Share not replaced by the link step | 0 | 0.5 | 1 |
| **Net hours a year** | **0** | **270 (0.15 FTE)** | **1,079 (0.6 FTE)** |
| At the CSB loaded rate ($33.2 / $38.3 / $43.1 an hour) | $0 | $10,341 | $46,533 |

The loaded rate is the FY2025 personal-services spend of $551,962 over 8 FTE, divided by productive hours.

**Inferred.**
- **The net could be zero.** If divisions already create crew work orders from the request, the link costs nothing and the whole close step goes. If they create them separately, the link step replaces the close step.
- **The net could also be larger than shown.** If divisions now re-key orders, creating them from the request would also save the re-keying. That is not estimated.
- **Labour not counted.** This also leaves out the batch clean-ups of stale records. 18.8% of the 18,580 requests from 2019–24 that closed more than a year late closed on 22 bulk days (reported, `research/open-queue-reality-check.md`).

## 4. Service restored, in physical units

### 4a. City-owned lots off the rounds but told "on schedule"

**Observed.** These are land-bank parcels ([LRA inventory](https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_INVENTORY.csv), 13 Oct) with a 2026 weed or cut-complaint request. Each request was filed by 13 Sep, closed at the hand-off and matched to its parcel (N1 join). A "cut" is a Grass Maint or Weed-Grass charge in the [Forestry billing ledger](https://www.stlouis-mo.gov/data/upload/data-files/forestry-service-records.csv), which runs to 13 Oct.

| Definition | Requests | **Parcels** |
|---|---:|---:|
| Weeds-Vacant Lot/Bldg closed "on schedule to be cut", no cut billed at any time in 2026 (matches north-taylor's 70) | 70 | **52** |
| Any hand-off wording, including cut complaints, no cut in 2026 | 136 | **82** |
| Any hand-off wording, no cut billed **after** the report | 245 | **171** |
| Context: land-bank parcels on the 2023 maintenance list as "Vacant Lot" with no 2026 cut | | 953 of 7,843 |

**Observed: the city's own billed amounts in 2026.**
- **Totals:** 8,412 land-bank parcels carry a mowing charge, **$1,387,078** in all.
  - This is more than the earlier note's $1.31M. The earlier figure came from an earlier file state or a different filter, and I did not reconcile the two.
- **Per parcel:** median $132.38 and mean $164.89, with 2.87 billed cut dates on average.
- **Per charge:** a Grass Maint charge has a median of $39.91.
- **Reported parcels:** the 599 that were cut have a median of $148.74 and a mean of $181.60.

**Estimated: season cost to cut the told-on-schedule parcels.**

| Case | Calculation | Cost |
|---|---|---:|
| Low | 52 × $132.38 | **$6,884** |
| Central | 82 × $148.74 | **$12,197** |
| High | 171 × $181.60 | **$31,054** |

Even the high case is about 2% of the 2026 land-bank mowing spend. The 953-lot context pool would be about $157,000 at the mean, but the fix surfaces only lots someone reports.

**Inferred.** The impact is not money. These lots become visible: under LINK they stay open past the date until a cut is billed, so they appear on Forestry's weekly list. Missing cuts are not "savings".

### 4b. Life-safety (tier-1) hazards past due

**Observed** (E5 ledger of 14,902 open, past-promise requests filed since 2025; tier map in `site/data/rank-weights.json`):
- **Tier 1 overall:** 2,991 requests. Of these, **2,778** remain on the ranked list after evidence of done, superseded or administrative work is removed.
  - Median **238.5 days** past the promise.
  - 2,216 are more than 90 days past, and **932** more than a year.
  - 2,562 have no record either way; 216 have a city work record pending.
- **By request type:**

  | Request type | Requests | Median days past the promise |
  |---|---:|---:|
  | Cave-ins | 1,196 | 145.5 |
  | Street or alley debris (tornado) | 364 | 316 |
  | City tree down | 316 | 373.5 |
  | Broken or hanging limb | 296 | 388 |
  | City tree limb down | 261 | 490 |
  | Water coming up | 143 | 292 |
  | Building collapse | 74 | 192 |

- **Trees and limbs down together:** 873 requests, median **455 days** past.
- **Reported:** none of the 29,018 extracted work orders carries a `PriorityCode` (`research/prioritisation-option.md`). The service-request `Priority` field was never retrieved.

So the claim to make is "past the date", not "unranked by the city".

### 4c. Trees approved for removal, waiting past their date

**Observed.** These come from the Cityworks extracts of 14 Oct 2026: read-only, operational fields only, raw data not published. A work order counts as open if it has no actual finish, no close date and no cancellation.

| Saved search | Open orders | Past projected finish | Median days past | Over a year past |
|---|---:|---:|---:|---:|
| [QE63 Tree Removal WOs](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/63) | 2,504 | **1,630** | **618** | 944 |
| [QE90 30-Day Removals, All City, New](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/90) | 314 | 229 | 264 | 77 |
| [QE102 (MTL) Removal, Open, Urgent](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/102) | 31 | 18 | 238 | 1 |

**Notes on these counts.**
- QE90 and QE102 are likely subsets of QE63, so the rows must not be added.
- The open QE63 orders were created a median of 445 days before 13 Oct. The May 2025 tornado is inside that window (inferred).
- **Reported:** the projected finish comes from the template's Days to Complete (Cityworks docs, cited in `research/prioritisation-option.md`).

## 5. What the city would learn in a quarter about the 12,566 with no record either way

**Observed.** The 12,566 sit mostly in 14 divisions with 100 or more each, 11,810 in all:

| Division | No-record requests |
|---|---:|
| Street 510 | 4,093 |
| Forestry | 3,191 |
| Building | 1,145 |
| Land bank (LRA) | 644 |
| Water | 502 |
| Traffic 511 | 485 |
| Tornado Recovery | 376 |
| Seven more divisions | 1,374 |

**Estimated, in two parts.**

**(i) Automatic, once linked.** Existing records explain these requests with no field work. E1 read 30 status pages per type in the 10 largest types (`build/E5/extrapolate.json`). Scaling each type's sampled pending share to the whole type moves about **1,411** (95% bounds 782–2,304) from "no record" to "waiting, work order open". Scaling the done share moves about **115** to "done".
- The gain is concentrated where status pages show work: weeds on occupied property (+757), Inspect City Tree (+293), sidewalks (+219) and sewer laterals (+142).
- Cave-ins, bad condition, exterior code, LRA trees, tornado debris and City Tree Down had **0 of 30** pages with anything attached. Linking reveals nothing for them.

**(ii) A weekly review.** Each division sorts the top of its ranked list into one of three outcomes: verify and close (done), link or dispatch (waiting), or re-dispatch (lost). The pace is assumed.

| | Low | Central | High |
|---|---:|---:|---:|
| Records per division per week (assumed, 3 minutes each) | 10 | 25 | 50 |
| Automatic from existing records | 782 | 1,526 | 2,419 |
| Reviewed in 13 weeks (capped at each division's remainder) | 1,775 | 3,482 | 4,680 |
| **Fate known after one quarter** | **2,557 (20%)** | **5,008 (40%)** | **7,099 (56%)** |
| Review hours in the quarter | 89 | 174 | 234 |

**Could not establish:** the done / waiting / lost split. R1 found that requests kept open have far *less* recorded work than closed ones: 93–95% of open weed requests had no cut. So "lost" may be large in the types with no attached work. The fix exists to answer that question, and this report cannot pre-empt it (inferred).

## 6. What the fix costs

**Setup, staff hours (estimated; every line is an assumption):**

| Item | Low | Central | High |
|---|---:|---:|---:|
| Cityworks admin: create crew work orders from the request, confirm auto-close, test per division | 16 | 40 | 80 |
| A saved search per division, past due and sorted by rank (14 divisions) | 14 | 28 | 56 |
| A default priority by request type (the tier map) and the rank sort or SQL | 8 | 24 | 60 |
| CityStat: restate the 311 measures as done-by-the-date | 8 | 24 | 60 |
| SOP and training for 311 staff and 14 division leads | 16 | 32 | 60 |
| **Total hours** | **62** | **148** | **316** |
| Rate (CSB loaded $38.33 / BLS St. Louis mean $31.89 × 1.4 / $60 IT or analyst, assumed) | | | |
| **Setup cost** | **$2,377** | **$6,608** | **$18,960** |
| New licence cost | $0 | $0 | $0 |

**Running cost (estimated).**
- The weekly review takes 0.5 / 1.25 / 2.5 hours per division per week.
- Across 14 divisions that is **364 / 910 / 1,820 hours a year**, or **$13,952 / $40,632 / $109,200**.
- This is the fix's largest cost, and it falls on existing supervisors' time.
- It is larger than the central labour saving in §3. That cost should be stated, not hidden.

The $0 licence cost assumes the fix needs no new module. It uses the request-to-work-order link, auto-close, saved searches and template priority, which are native to Cityworks 23. St. Louis runs 23.10, and the Workload add-on is not needed (reported, `research/prioritisation-option.md`).

**What the procurement route costs (reported, external):**
- New 311 CRM projects:
  - [Fresno 2023](https://agendas.fresno.gov/es/legislation/id-23-916-16348): $395,724 for implementation plus $610,344 for Salesforce licences.
  - [Baltimore](https://technical.ly/civic-news/baltimore-311-upgrades/): $1.6M for Salesforce 311 upgrades.
  - [Toronto](https://www.toronto.ca/legdocs/mmis/2025/gg/bgrd/backgroundfile-260459.pdf): a CA$6.75M Salesforce increase for 2026–2030.
- Smaller cities' subscriptions:
  - [Muskegon](https://muskegon-mi.gov/documents/view/63/6052/): SeeClickFix, $39,119 a year (2025).
  - [Savannah](https://agenda.savannahga.gov/publishing/december-19-2019-city-council-regular-meeting/193_4597.html): SAV311 CRM, $82,123 a year (2019).
- A Cityworks licence elsewhere: [Ann Arbor](https://a2gov.granicusideas.com/meetings/51-city-council/agenda_items/5b8854a47d7965a227027961), $83,000 a year (FY2019–21), which the city in effect already pays.
- Analytics seats, if wanted: [Power BI Pro](https://www.microsoft.com/en-us/power-platform/products/power-bi/pricing), $14 per user per month.
- These contract figures were seen by the sub-agent in search summaries; the pages were not opened (reported, lower confidence). They buy different scopes. They show what the procurement route costs; they are not a like-for-like price for this fix.

**Data-sharing and confidentiality risk.**
- **Inferred.** The fix moves no resident data out of the city's own Cityworks. There is no vendor data-sharing agreement, no external model and no new security review to run.
- **Reported, for scale only.** [IBM, 2025](https://newsroom.ibm.com/2025-07-30-ibm-report-13-of-organizations-reported-breaches-of-ai-models-or-applications,-97-of-which-reported-lacking-proper-ai-access-controls): average breach cost $4.44M globally and $10.22M in the US. I found no public-sector figure for 2025.
- **Not estimated.** There is no basis for a breach probability, so this is not an expected saving.

## 7. Verification of earlier draft figures

Script `04_verify_brainstorm.py`, output `build/impact/brainstorm_check.json`. All counts observed.

| Earlier draft claim | My check | Verdict |
|---|---|---|
| 36,705 filed in 2025 and closed at the hand-off | 36,705 `handed_off`, plus 438 `converted` (37,143) | Reproduced |
| 20,697 repeat filings in 2025 within 90 days | 20,697 with the earlier draft's join (earlier request filed before, any status). With the earlier request **closed before** the repeat: **11,475**. After a **hand-off** closure: **5,978** (4,804 resident-channel; median 27 days after the closure). After a **done** closure: 3,510 | The join reproduces. Do not use it as a headline; use the excess in §1 |
| 2,534 durable (1,700 resident) | Not reproduced. The same join with `type_family.durable` on the earlier request gives 3,742 (any status), 1,137 (closed before the repeat) and **176** (closed at the hand-off before the repeat; 138 resident). 1,776 durable repeats came while the earlier request was still open | Not reproduced; method differs |
| 2,565 closings say "call CSB" | 2,565 for 2025 filings; 5,576 for 2025–26 | Reproduced |
| 2,576 in six tier-1 types | 2,576 in the base: cave-ins 1,233, tornado debris 365, tree down 323, hanging limb 307, limb down 269, collapse 79. Of these, 2,557 have no done record (19 are class a). Across all tier-1 types, 2,778 are on the ranked list | Reproduced, but "with no finished job on record" fits 2,557, not 2,576 |
| 1,206 could be told "scheduled" today | 1,206 is E5 class b. Under the strict test it is **952** (status page, board-up, demolition, and the validated Inspect City Tree join). 254 are address-only matches that may belong to a sibling request at the same tree | Say "about 950" or "1,206, of which 952 confirmed" |

The re-report join in §1 already required `next.ts_init > ts_closed`.

## 8. Assumptions register

| Assumption | Low / central / high | Used in |
|---|---|---|
| Productive hours per FTE a year | 2,080 / 1,800 / 1,600 | §1, §3 |
| Resident minutes per report | 5 / 10 / 20 | §1 |
| Minutes per manual closure | 0.5 / 1 / 2 | §3 |
| Share of closing time not replaced by the link step | 0 / 0.5 / 1 | §3 |
| Benefits loading on the BLS wage | 1.4 | §6 |
| IT or analyst rate (high case) | $60 an hour | §6 |
| Records reviewed per division per week | 10 / 25 / 50 | §5, §6 |
| Minutes per record reviewed | 3 | §5, §6 |
| Setup hours per item | §6 table | §6 |
| Tier map (which request types are life-safety) | `site/data/rank-weights.json` | §4b, H1 |

## 9. Negative and inconclusive results

- No St. Louis status-call, web-lookup or chat volume was found on disk (§2).
- The repeat-request gap vanishes under the filing-anchored check, and re-reports do not track unfinished work (R2). The §1 low case is therefore 0.
- The earlier draft's 2,534 durable repeats could not be reproduced (§7).
- None found by the sub-agent:
  - a current US cost per 311 call;
  - a 2025 IBM public-sector breach figure;
  - any published evaluation of auto-closing requests or linking them to work orders;
  - any study of residents' total time per report.
- The sub-agent's dead links: transportation.gov 2025/26 value-of-time pages and tableau.com returned 403; the Dallas 311 audit had a certificate error.
- Land-bank mowing in 2026 totals $1,387,078 on my query, against $1.31M in the earlier note. Not reconciled.
