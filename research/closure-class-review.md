# Closure-class review: alley debris and the 40 biggest closing phrases

Independent review, 14 Oct 2026 (18:34 CDT start), of the AI-drafted closure classes behind the
"CityStat 79%, done-only 15%" figure. Files on disk only, no network. Database opened read-only.
Labels: **observed** (I ran the query), **reported** (another file or source says so), **inferred** (my
conclusion), **estimated** (a number that rests on an assumption I state).

## Summary

**The 15% holds as a statement about the closing words.** Fourteen distinct closing phrases cover the
572 closed Q2 2026 "Debris-alley/street" requests. None of them sits on the wrong side of the
done / not-done line (observed table; inferred judgement). Only two phrases say the debris was
collected, and nothing else reads that way. The one phrase whose wording is genuinely ambiguous is a blank
closing on 2 requests.

| scenario | done-only on-time share |
|---|---|
| (a) table as is | **15.0%** (86 / 572) |
| (b) my corrections (no done/not-done change) | **15.0%** |
| (c) ambiguous wording counted as done (the blank) | **15.4%** |
| (c, wide) also assume every "will be picked up / will be investigated" promise was kept within 3 days | 60.8% |
| matched to CityStat's own denominator (file as of 30 Jun-1 Jul) | 14.1-14.6% |

Counts are observed. Row (b) applies my judgement; the "wide" row is an assumption-driven upper bound.

**The word "hand-off" is weaker.** Half of the on-time "hand-offs" (151 of 300) say "bulk will be
picked up in correct week". That is most plausibly a deferral to the monthly bulk collection, not a
pass to another unit (inferred). Relabelled, hand-offs fall from 67.0% to 33.3% of on-time closures,
and the 15.0% does not move.

**Top 40 type-and-phrase pairs, 2025-26** (87,132 closures, 49.5% of all):
- no pair crosses the done / not-done line (inferred)
- relabel 4,338 out of "handed off": the bulk-week deferrals and "building already under notice"
- 3,146 enforcement notices are genuinely ambiguous
- 1,630 snow "work completed" closures were batch-closed (a fidelity flag, not a class error)

**Could not establish:** whether any debris was actually picked up, and when. No completion record for
alley debris exists on disk. The words show what the city wrote at closing, not what crews did. So "15%"
cannot be read as "15% was cleaned on time". If the "collected" closings are true, the real cleaning rate lies between
15% and about 61% (inferred).

**For the video:** the current line ("Count only the closings that say it was picked up, and it's 15")
is safe as worded. Paraphrases that drop "say" are not. A line that survives the city's best rebuttal is in section 6.

## 1. Definition used

- **Measure** (reported, `scripts/night/N4/citystat_targets.py`, transcribed from
  `data/raw/citystat/tableau-extract.md`): CityStat "Debris, alley/street, cleaned within 3 days". The
  published Q2 2026 value is 0.7857 on n = 546, from
  https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/streets.cfm (read
  13 Oct 2026, 23:14-23:40 UTC). The page says data were last updated 30 June 2026.
- **Rebuild** (observed; N4 "definition C", as coded in `scripts/night/R1/05_restate.py`):
  - problem code `Debris-alley/street`, one row per request id (`v_requests`)
  - `status_group = 'closed'`, filed 1 Apr-30 Jun 2026
  - on time = `date_diff('day', init_date, CAST(ts_closed AS DATE)) <= 3`
  - done = `closure_class = 'done'`, with the same denominator
- **Data** (observed): `build/stl.duckdb`, built from the city's 311 file
  https://www.stlouis-mo.gov/data/upload/data-files/csb.zip. The latest close time in the file is
  13 Oct 2026, 05:56.
- **Reproduction** (observed): 572 closed, 448 on time (78.3%), 86 done and on time (15.0%). This matches
  `r1_citystat_debris_alley_street_q2_2026_ontime_done_only` (15.0) and
  `..._handoff_share_of_ontime` (67.0) in `build/R1/figures.json`.
- **Classes** (observed): classes come from `closure_text_class` (252 texts) and `closure_type_override`
  (2 rows) through `build/N2/closure_class.sql`. Every Q2 debris row has `class_source = 'N2:type+text'`,
  and the classes agree with `research/chapters/N2-closure-classes.csv`.

## 2. Every Q2 2026 debris closing phrase (observed counts; my verdict is inferred)

572 closed, 448 on time. "Median h" is the median number of hours from filing to closing.

| closing phrase | closed | % of closed | on time | % of on-time | on-time rate | median h | table class | verdict |
|---|---:|---:|---:|---:|---:|---:|---|---|
| collection made | 188 | 32.9 | 84 | 18.8 | 44.7% | 94.4 | done | **agree** |
| bulk will be picked up in correct week | 154 | 26.9 | 151 | 33.7 | 98.1% | 2.8 | handed_off:scheduled | **not done: agree. Label: deferral, not hand-off** |
| matter will be investigated and appropriate action taken | 114 | 19.9 | 106 | 23.7 | 93.0% | 14.8 | handed_off:future_tense | **agree** (outcome unknown; may be stock wording) |
| citizen's responsibility to clean up trash | 45 | 7.9 | 43 | 9.6 | 95.6% | 11.1 | no_action | agree |
| referred to forestry | 38 | 6.6 | 35 | 7.8 | 92.1% | 4.1 | handed_off:internal_referral | agree |
| no service necessary | 14 | 2.4 | 13 | 2.9 | 92.9% | 16.0 | no_action | agree |
| referred to trash task force | 6 | 1.0 | 5 | 1.1 | 83.3% | 18.6 | handed_off:internal_referral | agree |
| bulk/debris items have been collected | 3 | 0.5 | 2 | 0.4 | 66.7% | 2.9 | done | agree |
| collection will be made next scheduled day | 3 | 0.5 | 3 | 0.7 | 100% | 10.8 | handed_off:future_tense | agree (same deferral logic as bulk week) |
| (blank) | 2 | 0.3 | 2 | 0.4 | 100% | 5.0 | blank | **genuinely ambiguous** |
| instructions issued to customer | 2 | 0.3 | 2 | 0.4 | 100% | 11.6 | info_other | agree |
| citizen contacted - no response, left message | 1 | 0.2 | 1 | 0.2 | 100% | 1.4 | info_other | agree |
| no such address | 1 | 0.2 | 1 | 0.2 | 100% | 1.9 | no_action | agree |
| summons issued | 1 | 0.2 | 0 | 0 | 0% | 684.3 | handed_off:enforcement | agree |

The phrases a reader could argue about:

- **"bulk will be picked up in correct week"** (154)
  - *Wording* (inferred): future tense. Nobody would read it as "the debris was picked up", so it is
    correctly not done.
  - *Meaning* (inferred, moderate confidence): St. Louis collects bulk monthly, "during the week of a
    designated Monday" (reported, City Refuse pages as summarised in `research/parts/G-seasonal.md`
    §3.3, retrieved 13 Oct 2026). "Correct week" therefore says the items were set out in the wrong
    week and will go with routine bulk collection.
  - *Label*: this is a deferral to the same service, not a hand-off to another unit. It sits between
    handed_off and no_action.
  - *Timing* (observed): it closes a median 2.8 hours after filing, 43 of 154 within the first hour,
    before any pickup could have happened. The pickup date is unknowable from the file, and with a
    monthly cycle most pickups would plausibly fall after the 3-day goal (inferred).
- **"matter will be investigated and appropriate action taken"** (114)
  - *Wording*: "will be looked at", the textbook not-done case.
  - *Stock wording?* (inferred possibility): the phrase is also the closing text on 1,092 "Refuse not
    collected" closures in 2025-26 (observed), so it may be a stock Refuse-Division reply.
  - *Timing* (observed): median 14.8 hours to close, against 94.4 for "collection made".
  - *Re-reports* (reported, `build/R2/rereport_by_type_text.csv`, 2025-26 closures, not recomputed):
    4.9% of these closures were followed within 14 days by a new debris request at the same address,
    against 1.8% after "collection made". That fits
    the debris more often remaining (inferred). But 95% never re-report, so re-reporting cannot settle
    the outcome.
- **"citizen's responsibility..." and "no service necessary"** (59)
  - *Class*: correctly not done.
  - *Fairness*: in these cases the city judged that no city pickup was owed, yet the done-only figure
    counts them against the city. This is a denominator question, not a classification error. See
    scenario (d).
- **Blank** (2): no words at all, so the closing cannot be classed. It is the only case I count as
  ambiguous in wording.

## 3. Done-only on-time share, recomputed (observed unless labelled)

| scenario | done & on time | denominator | share |
|---|---:|---:|---:|
| (a) table as is | 86 | 572 | **15.0%** |
| (b) my corrections: bulk week relabelled as deferral (still not done) | 86 | 572 | **15.0%** |
| (c) ambiguous wording counted as done (+ blank) | 88 | 572 | **15.4%** |
| (c, wide) + every promise assumed kept within 3 days (bulk week, investigated, next scheduled day) | 348 | 572 | 60.8% (assumption-driven bound) |
| (c, widest) + referrals to Forestry / Trash Task Force counted as done | 388 | 572 | 67.8% (bound) |
| (d) "no pickup owed" closures (no_action, 60) dropped from denominator | 86 | 512 | 16.8% |
| (d') also drop bulk-week deferrals (154) as "routine service" | 86 | 358 | 24.0% |
| (e) promised pickups made at the speed of recorded pickups (44.7% within 3 days) | 86 + 0.447 × 271 | 572 | 36.2% (**estimated**) |
| CityStat-style: every on-time closure counts | 448 | 572 | 78.3% (published 78.6%) |

Other results:

- **(b) moves a different figure.** The hand-off share of on-time closures falls from 67.0% to
  **33.3%** (149 / 448), because the 151 bulk-week closings move to "deferred". The done-only share is
  unchanged.
- **(e) is a guess** (estimated). It assumes promised pickups happened as fast as the pickups that
  closed as "collection made". With a monthly bulk cycle, the real rate is probably lower (inferred).
- **CityStat's denominator** (observed): CityStat counted 546 requests, against 572 in today's file. Our
  file had 545 Q2 requests closed by 30 Jun and 556 by 1 Jul. On those cut-offs the done-only on-time
  share is **14.1% and 14.6%**, and the on-time share is 80.4% and 79.7%. The freeze date does not
  move the 15.
- **Where the on-time score comes from** (observed): closings that say "collection made" met the 3-day
  goal 44.7% of the time. The promise and referral phrases met it 83-100% of the time. 80.8% of on-time
  closures (362 / 448) do not say the debris was collected.
- **On-time closures by what their words say** (observed; groups are my reading of the phrases):

  | the words say | on-time closures | share |
  |---|---:|---:|
  | collected | 86 | 19.2% |
  | will be picked up later, or will be looked into | 260 | 58.0% |
  | referred to Forestry or the Trash Task Force | 40 | 8.9% |
  | not the city's job, no service needed, or no such address | 57 | 12.7% |
  | other (information or blank) | 5 | 1.1% |

- **Trend** (observed): done-and-on-time shares for each quarter filed:

  | 2024 Q1 | 2024 Q2 | 2024 Q3 | 2024 Q4 | 2025 Q1 | 2025 Q2 | 2025 Q3 | 2025 Q4 | 2026 Q1 | 2026 Q2 | 2026 Q3 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | 3.6% | 7.0% | 2.5% | 2.1% | 0.2% | 1.7% | 8.8% | 6.7% | 15.6% | 15.0% | 18.3% |

  Q2 2026 is among the best quarters on record, so picking it does not flatter the argument (inferred).
  The six-quarter figure (2025 Q1-2026 Q2) is 7.2% (reported, `build/R1/restated_citystat.csv`).

## 4. The 40 highest-volume type-and-phrase pairs, 2025-26

- **Scope** (observed): requests filed 1 Jan 2025-12 Oct 2026 and closed. That is 175,876 requests; the
  top 40 pairs hold 87,132 (49.5%).
- **Classes in the top 40** (observed): done 40,223; handed_off 30,735; no_action 11,763; blank 4,411.
- **Timing** (observed): "median h" is the median number of hours from filing to closing.
- **Verdicts** are my judgement (inferred).

| # | type | closing phrase | n | class | median h | verdict |
|---:|---|---|---:|---|---:|---|
| 1 | Refuse not collected | collection made | 6,457 | done | 44.1 | agree |
| 2 | Vehicle Towing | vehicle gone upon inspection | 5,517 | no_action | 834.1 | agree |
| 3 | Containr damaged | container(s) replaced with new | 5,065 | done | 263.5 | agree |
| 4 | Potholes - Residnl | work completed | 4,422 | done | 209.7 | agree |
| 5 | Public Nuisance Rpt | (blank) | 4,411 | blank | 0.0 | agree (logging-only type, 97.9% closed within an hour) |
| 6 | Snow/Ice - Residnl | work completed | 3,667 | done | 364.3 | agree on words; **fidelity flag**: 1,630 closed 3-5 Feb 2025 in a batch |
| 7 | Whole Blk Lights Out | work completed | 3,294 | done | 18.8 | agree |
| 8 | Potholes - Major St | work completed | 3,166 | done | 221.4 | agree |
| 9 | Vehicle Towing | vehicle tagged for tow | 3,072 | handed_off | 405.3 | agree (note: R1 `common.py` maps it to crew work; a tag is also a notice to the owner) |
| 10 | Refuse not collected | collection will be made next scheduled day | 3,013 | handed_off | 24.9 | agree on not-done; "promised", not passed on |
| 11 | Weeds-Occupied Ppty | no forestry violations | 2,706 | no_action | 314.7 | agree |
| 12 | Single Light Out | work completed | 2,669 | done | 410.4 | agree |
| 13 | Sign needs attention | work completed | 2,261 | done | 144.5 | agree |
| 14 | Containr damaged | container maintenance completed | 2,230 | done | 161.0 | agree |
| 15 | Refuse not collected | due to employee shortage, the routes will be completed in order... | 2,197 | handed_off | 15.4 | agree on not-done; "promised" |
| 16 | Weeds-Vacant Bldg | on schedule to be cut, call csb for details | 2,095 | handed_off | 0.4 | agree |
| 17 | Vehicle Towing | no problem found | 1,948 | no_action | 216.2 | agree |
| 18 | Debris-alley/street | collection made | 1,938 | done | 180.4 | agree |
| 19 | Illegl Use-Opn Storg | issued notice of violation | 1,741 | handed_off | 98.2 | **ambiguous**: for enforcement, the notice is the service |
| 20 | Debris-alley/street | matter will be investigated and appropriate action taken | 1,663 | handed_off | 19.1 | agree (possibly stock wording) |
| 21 | Stray Dog At Large | patrolled area, no strays observed | 1,592 | no_action | 67.1 | agree |
| 22 | Vacnt Bldg Unsecured | referred to board up crew | 1,564 | handed_off | 83.7 | agree |
| 23 | Bulky items missed | collection will be made next scheduled day | 1,474 | handed_off | 18.4 | agree on not-done; "promised" |
| 24 | Tree Planting requst | approved for next available planting | 1,444 | handed_off | 210.5 | agree |
| 25 | Weeds-Vacant Lot | on schedule to be cut, call csb for details | 1,444 | handed_off | 0.1 | agree |
| 26 | Light Damaged | work completed | 1,441 | done | 87.3 | agree |
| 27 | Ppty Maint Code-Ext | issued notice of violation | 1,405 | handed_off | 121.9 | **ambiguous** (as #19) |
| 28 | Ppty Maint Code-Ext | building already under notice | 1,359 | handed_off | 124.5 | **relabel**: no new action on an existing case; closer to no_action (duplicate) |
| 29 | Illegl Use-Opn Storg | building already under notice | 1,226 | handed_off | 93.0 | **relabel** (as #28) |
| 30 | Bulky items missed | due to employee shortage, the routes will be completed in order... | 1,155 | handed_off | 17.8 | agree on not-done; "promised" |
| 31 | Weeds-Vacant Bldg | added to rotation | 1,134 | handed_off | 335.8 | agree |
| 32 | Dead Animal | animal picked up | 1,103 | done | 72.3 | agree |
| 33 | Refuse not collected | matter will be investigated and appropriate action taken | 1,092 | handed_off | 19.1 | agree |
| 34 | WTR-COMING-UP | scheduled for repair by water department | 958 | handed_off | 2.4 | agree |
| 35 | Cave-Ins | referred to street maintenance for repair work to be scheduled | 946 | handed_off | 73.1 | agree |
| 36 | Move container | container moved | 880 | done | 43.7 | agree |
| 37 | Debris-alley/street | bulk will be picked up in correct week | 878 | handed_off | 15.1 | **relabel**: deferral to the monthly bulk week (still not done) |
| 38 | Bulky items missed | bulk will be picked up in correct week | 875 | handed_off | 17.1 | **relabel**: says the pickup was not missed (wrong week); fits no_action:no_violation |
| 39 | Graffiti-Private | graffiti removed painted | 816 | done | 916.0 | agree |
| 40 | Critical Sign | work completed | 814 | done | 49.5 | agree |

### What I would change, and the volume affected

1. **Done / not-done changes: none** (0 of 87,132) (inferred). Every "done" phrase states finished work,
   and every other phrase states something else.
2. **Relabel out of "handed off", still not done: 4,338 closures** (inferred).
   - "bulk will be picked up in correct week": 1,753 (rows 37-38)
   - "building already under notice": 2,585 (rows 28-29)

   Applied to N2's headline, the "hand-off or work order" share of 2025-26 closures would fall from 35.2%
   (61,845) to **32.7%** (57,507 / 175,876) (observed arithmetic on my relabel). Done figures do not
   change.
3. **Genuinely ambiguous, keep with a sensitivity: 3,146** "issued notice of violation" closures (rows 19
   and 27) (inferred). N2 already gives headline figures with and without enforcement notices.
4. **Word choice, keep the class: 7,839** "next scheduled day" and "employee shortage" closures (rows 10,
   15, 23, 30) (inferred). These fit N2's definition of handed_off ("will be ..."), but the same crew is
   coming back later; nothing is passed to anyone. In public copy, "promised" is more accurate than
   "handed off".
5. **Fidelity, not class** (observed): 1,630 of 3,667 snow "work completed" closures were made on
   3-5 Feb 2025. That fits an administrative batch close (inferred). `research/parts/G-seasonal.md` reports 2,151
   January snow tickets bulk-closed on those dates. The
   words say done, so the class is right by the rule; whether the work happened is a separate question.

## 5. What this review cannot settle

- **Actual pickups** (observed negative): there is no completion record for alley debris on disk.
  R1's register traces nothing for this type (`scripts/night/R1/common.py`, `trace()` returns
  "none_found"). The Forestry ledger stopped recording debris clean-ups after 2021 (reported, same file),
  but that note concerns vacant-lot and vacant-building debris. A promise to pick up later may have been
  kept on day 1 or day 30. Nothing here can tell.
- **Truth of "done" closings**: not tested. "Collection made" is taken at its word.
- **Meaning of "correct week"**: inferred from the wording and the reported monthly bulk schedule. The
  Refuse Division has not confirmed it.
- **"Matter will be investigated"**: whether it reflects a real field visit or stock wording is
  unknown.
- **Second reader**: this review is also by an AI model. It replaces no human review. It narrows the
  human check to three phrases: bulk week, investigated, enforcement notices.

## 6. Is "79 percent becomes 15" safe to say?

**Yes, as the script now words it** (inferred). `deliverable/video-script-v4.md` says: "Count only the
closings that say it was picked up, and it's 15." The classification review leaves that at 15.0-15.4%,
and at 14.1-14.6% on CityStat's own freeze date.

**Not safe** (inferred):

- any paraphrase such as "only 15 percent was actually cleaned on time", or "the city only cleaned 15
  percent". The data cannot show that. If the promises were kept, the true figure could be anywhere up
  to about 61%.
- "67 percent are hand-offs" for debris. Half of those are bulk-week deferrals.

**The city's strongest rebuttal** (inferred): "bulk-week closings are routine bulk on schedule, and
'citizen's responsibility' cases were never ours." Even granting both, the figure is 24.0% (scenario
d'). The point survives the rebuttal, but the gap narrows.

**Wording that survives the rebuttal** (observed figures):

> CityStat counts 79 percent of alley-debris requests as handled on time this spring. But only about one
> in five of those on-time closings says the debris was picked up. Most say it will be picked up later,
> or that someone will look into it.

The figures behind it are 19.2% "picked up" and 58.0% "later or looked into". If the line keeps
"becomes 15", put a footnote on screen: "Share of all closed requests whose closing words say collected,
within 3 days. Words, not field checks."

## 7. Reproduction

```sql
-- python3 + duckdb, build/stl.duckdb opened read_only
WITH c AS (
  SELECT res_key, closure_class, class_rule,
         date_diff('day', init_date, CAST(ts_closed AS DATE)) <= 3 AS on_time,
         epoch(ts_closed - ts_init) / 3600.0 AS hrs
  FROM v_requests
  WHERE problem_code = 'Debris-alley/street' AND status_group = 'closed'
    AND year(init_date) = 2026 AND quarter(init_date) = 2)
SELECT res_key, closure_class, class_rule, count(*) AS n,
       count(*) FILTER (WHERE on_time) AS n_on, median(hrs) AS med_h
FROM c GROUP BY ALL ORDER BY n DESC;

-- top 40 pairs
SELECT problem_code, res_key, closure_class, count(*) AS n,
       median(epoch(ts_closed - ts_init) / 3600.0) AS med_h
FROM v_requests
WHERE init_date >= DATE '2025-01-01' AND status_group = 'closed'
GROUP BY ALL ORDER BY n DESC, problem_code LIMIT 40;
```

The freeze check counts Q2 requests by `CAST(ts_closed AS DATE) <= d` for each d from 28 Jun 2026.
No repository file other than this report and its facts CSV was written.
