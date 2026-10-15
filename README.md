# Follow-Through STL

*Which promises did St. Louis keep?*

**When St. Louis 311 hands a job to a crew, the request stops tracking the work.** Usually it is closed at the hand-off; sometimes it is left open with nothing attached. Either way, residents, departments and CityStat lose sight of whether the job was done. This repository is Jack Riddle's entry to the Innovate USA Civic AI Hackathon (City of St. Louis, 13–15 October 2026). **The product is the analysis:** a request-by-request audit of the city's own records, packaged as plain SQL and saved searches that plug into the systems the city already runs (Cityworks, CityStat and the 311 status page). It does not replace the city's 311 system. The website is a demo of what that output looks like on real city data, and the hand-over package says how to set it up.

> Independent prototype built from the City of St. Louis's open data, plus Cityworks saved searches and public 311 status pages read with the City's permission (operational fields only; no personal data). Not a City website. Every public figure is at block level or coarser.

## The finding, in numbers

Every figure is **observed** (counted from the city's own files) unless marked. Sources and derivations: [the video script's figure table](deliverable/video-script-v7.md#figures-behind-each-spoken-number) and the reports in `research/`.

- **The symptoms, service by service.**
  - Tree removals: 39 of 40 sampled requests finished late, a median of 211 days past the promise.
  - Sidewalks: 54% of 2023's repair requests are still open.
  - Vacant lots: 35% of 2026 reports have no cut on record.
  - Board-ups: 17% were done by the promised date.
  - Towing: the city's own CityStat page says "Closed" does not necessarily mean towed.
- **How it breaks.** 311 closes the request a median of 1.8 days after filing, at the hand-off. The promise is about 14 days out. Where the crews' work can be traced (3,640 mowing and board-up hand-offs), 18% was done by the promised date, and about half came late. ([R1](research/chapters/R1-trace.md))
- **The scorecard grades the hand-off.**
  - CityStat counts 79% of alley-debris requests as handled on time.
  - Only 15% of those closings *say* the debris was picked up.
  - About 45% say it will be picked up later or will be investigated.

  ([closure-class review](research/closure-class-review.md))
- **Jobs drop, and nothing notices.**
  - A city-owned lot on North Taylor was reported twice in July 2026. Both requests were closed within 15 minutes, "on schedule to be cut". It has no cut on record since October 2024, while crews cut 36 parcels on its block this year.
  - Another city-owned lot on the same block got the same answer just as fast, and was cut three times.
  - In 2026, 479 of 1,724 "on schedule to be cut" answers (28%) went to properties with no cut on record all year.

  ([North Taylor](research/north-taylor-mechanism.md))
- **Open requests aren't tracked either.**
  - 14,902 open requests filed since 2025 are past the city's promised date. 3% show the work done, 8% have a crew job pending, and for 84% (12,566) no record says either way.
  - 2,778 of them are life-safety requests (trees down, cave-ins, water coming up), a median of 239 days past the date.

  ([open-queue check](research/open-queue-reality-check.md), [impact](research/impact-quantification.md))
- **The missing link.** Cityworks can attach the crew's work order to the request. For 15 of the 20 most common hand-offs, none of the sampled status pages showed anything attached; tree removals did, 40 of 40. ([status-page linkage](research/status-page-linkage.md))

The mayor's transition committee recommended in July 2025: "Audit previously closed requests to ensure action was taken." This is that audit.

## The fix: one cause, four requirements

The cause is that the request isn't tied to the crew's job. A fix has to:
1. tie each request to its job;
2. keep the request open until the job is done;
3. flag every request past its date with no finished job;
4. put the most dangerous first.

All of this happens inside the systems the city already runs: no new software, no app for residents, and no city data leaving the city.

Much of it already exists:
- Forestry attaches work orders to tree removals.
- Cityworks 23 closes a linked request when its work order closes.
- Chicago, Houston and Toronto have made "open until the work is done" the rule. ([precedents](research/precedents-closed-loop.md))

## What is in this repository

| Path | What it is |
|---|---|
| [`deliverable/handover/`](deliverable/handover/README.md) | **The hand-over package:**<br>• a one-page practice each for Forestry, Streets and the Building Division;<br>• the overdue saved-search specification;<br>• the ArcGIS dashboard definition;<br>• the SQL;<br>• the one-quarter test. |
| `site/` | **The working prototype**, on the city's own data:<br>• the resident's status page, today and after the fix;<br>• each division's weekly past-due list, ranked by danger with the reason on every row;<br>• CityStat with one added column (closings that say the work was done);<br>• every source, with a download. |
| [`deliverable/video-script-v7.md`](deliverable/video-script-v7.md) | The video's script, figure table, the claims it deliberately does not make, and what was said in the recording. |
| `research/` | The audit: one report per question, each opening with what was and was not established, with a `-facts.csv` beside it (one row per figure, labelled observed, reported, inferred or estimated, with its URL). |
| `scripts/` | The pipeline that builds every figure from the public files. |
| `data/`, `scripts/data/` | `data/MANIFEST.csv` lists every public source; `scripts/data/fetch_public.sh` re-downloads them. Raw data is not committed. |

### Run the prototype

```bash
python3 scripts/night/N6/serve.py --no-bridge
```

Then open http://127.0.0.1:8806/. The pages read `site/data/`, which is already built. The status lookup works only under this server.

## What it would take to test

One quarter, on three request types, measured against the baselines of 13 October 2026:
- tree removals: 1,630 work orders past Forestry's own projected finish;
- cave-ins: 1,233 requests open past the city's date;
- vacant-lot mowing: 289 requests open past the city's date.

Working looks like this: the "no record either way" share falls to zero for these types, and overdue counts are compared with the baselines.

The impact claim is an **estimate**: in one quarter, the city would learn what happened to about 5,000 of the 12,566 unexplained overdue requests (range 2,600–7,100). About 1,500 come from linking work orders that already exist, and about 3,500 from each division reviewing 25 a week. See [impact-quantification](research/impact-quantification.md).

## What this entry does not claim

- that crews will be faster, or that the backlog clears;
- that the 14,902 open requests were closed early (they are open);
- that a lot was "never cut" (only that no cut is on record);
- repeat-request savings, or labour saved by auto-closing;
- any equity claim;
- that AI is in the product. AI agents did the audit; the city would run plain SQL.

Negative and inconclusive results are kept in the research reports and in [`deliverable/negative-results.md`](deliverable/negative-results.md).

## Data, permission and privacy

The analysis uses:
- the city's public 311 file;
- Forestry's billing ledger;
- the land bank's inventory and the Building Division's map layers;
- Cityworks saved searches and public status pages, read on 14 October 2026 with the permission described in [`context/AUTHORISATION-NOTE.md`](context/AUTHORISATION-NOTE.md).

Reads were limited to one per second and to operational fields. No personal data was collected, and raw extracts are not published. Every page and file here is at block level or coarser, with no request, parcel or work-order numbers.

Built by Jack Riddle with AI research and coding agents (Anthropic's Claude), October 2026. MIT licence.
