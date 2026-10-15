# Video script v5 (LOCKED 14 Oct, 10:20 p.m., with the cut list applied): top-down, plain English, one idea per beat

Written Wednesday 14 October 2026, about 9:55 p.m. Central, on the v5 structure Jack approved (`deliverable/RESTRUCTURE-v5.md`). It supersedes v4. There are 18 beats, each one hero frame. After the voice ends, every scene holds its frame long enough to read (the hold rule), so pauses come from the picture and the narration doesn't need padding.

**Length (measured after the cuts).** 666 words; the scratch voice takes 4:13, including 1.4 s of silence at each beat's ends. With short holds after key frames and the demo running about 10 s past its narration, **the film is about 4:55**. Jack's own pace will move this in either direction.

**What changed from v4:**
- The answer comes first; there is no name in the intro.
- Every term is defined the first time it appears.
- North Taylor is now the twin-lots example, with the honest mechanism (`research/north-taylor-mechanism.md`).
- "Link, list, count" became three plain steps.
- There is an impact beat with the ranking, and a screen-recorded demo.

## Read-aloud (record one file per beat; leave a clear half-second pause between sentences)

> **1.** I came into this hackathon looking for one broken city service to fix. A fallen tree. A cracked sidewalk. A lot nobody mowed. Trash nobody picked up. Every one I looked at broke the same way.
>
> **2.** St. Louis can't tell which of its 311 promises it has kept.
>
> **3.** Right now, 14,902 requests are past the date the city promised. For 84 percent of them, no record shows whether the work was ever done.
>
> **4.** And CityStat, the city's scorecard, counts 79 percent of alley-debris requests as handled on time. Only 15 percent were closed with a note that the debris was picked up.
>
> **5.** The fix doesn't need new software. Each request has to stay tied to its job until the job is done.
>
> **6.** Every request has three dates: the day it's filed, the date the city promises, and the day the work is done.
>
> **7.** Here's what happens instead. About two days after filing, 311 closes the request as it passes the job to a crew, with words like "on schedule to be cut." That's the hand-off. The work, when it's recorded at all, comes about five weeks after filing.
>
> **8.** Cityworks, the system the city already runs, can attach the crew's work order to the request. I read 800 of the city's status pages, for the 20 most common hand-offs. In 15 of them, about 22,800 requests, not one page showed a work order. Tree removals did, every time.
>
> **9.** Here are those 14,902 open requests on a map of St. Louis. Now color each one by what the city's records show. Work done: 3 percent. A work order still pending: 8 percent. No record either way: 84 percent. No one can tell those residents, or the mayor, whether the work happened.
>
> **10.** Here's one block. Two city-owned lots on North Taylor, reported the same July day. Both got the same answer within the hour: "on schedule to be cut." One was cut three times this year. The other has no cut on record since October 2024. It had dropped off the cutting rounds, and nothing checks 311's answer against the schedule.
>
> **11.** The city has said this itself. Its own towing page: "Closed does not necessarily indicate that a vehicle has been towed."
>
> **12.** So, the fix, in three steps, inside the systems the city already runs. First, attach the job. At the hand-off, staff link the crew's work order to the request. If there's no job to link, that's a warning on day one. Cityworks' documentation says a linked request closes when its work order does. Second, flag the misses. Every week, each division sees every request past its date with no finished job. Third, count the finish. CityStat counts a request as on time only when the job was finished by the date.
>
> **13.** Back to North Taylor. The twin's request links to its next cut. The other lot has nothing to link, so its request stays open, and Forestry sees it that week. Whether the crew comes sooner is still up to the crew. But the lot can't disappear.
>
> **14.** The list can also rank. Sorted by hazard, lateness and repeat reports, Forestry's top 25 overdue jobs go from 9 safety hazards to 25. The same list works for every division, across 124,000 requests a year. Knowing which promises were kept is how a city starts keeping more of them.
>
> **15.** Here it is, running on the city's own data. Forestry's list, ranked, with the reason for every rank. One block's open requests. A resident's page, today, and under the fix. And CityStat, with one more column.
>
> **16.** I'm handing over the package: the saved search, the dashboard, the SQL, the ranking's weights, and a one-page practice for each division. AI agents did the audit. What the city runs is plain SQL. Nothing to buy.
>
> **17.** The ask: one quarter, three request types: tree removals, cave-ins and vacant-lot mowing. Attach the job, flag the misses, count the finish. Then re-run this against today's baseline.
>
> **18.** And you'll know which promises you kept.

## What each beat shows (action titles: each frame states its takeaway and passes the muted, paused test)

| # | On-screen action title (or the frame) | Picture | Minimum time the final frame stays fully visible |
|---|---|---|---|
| 1 | (no title) | Four line-art vignettes, each a resident on the phone in front of the problem: a fallen tree, a cracked sidewalk, an overgrown lot, trash bags. A thin line then draws through all four. | 1.5 s |
| 2 | **St. Louis can't tell which of its 311 promises it has kept** | The title alone | 3 s |
| 3 | **14,902 requests are past the date the city promised; for 84%, no record shows whether the work was done** | The counter to 14,902, then the 84% bar. Source line: "Open requests filed since 1 Jan 2025, past due as of 13 Oct 2026. City 311 file; city records." | 4 s |
| 4 | **CityStat counts 79% of alley-debris requests on time; 15% were closed saying it was picked up** | One bar: 79% splits into 15% "closing says picked up" and 64% "says it will be picked up later, or investigated". Source: CityStat Q2 2026; 311 closing words. | 5 s |
| 5 | **The fix: keep each request tied to its job until the job is done** | The title; a request card and a job card joined by a solid line | 3 s |
| 6 | **Every request has three dates** | A timeline with three ticks: filed, promised, done | 3 s |
| 7 | **311 closes the request in about 2 days; the work comes about 5 weeks after filing** | The same timeline: "closed" stamped at day 2, "done" at week 5, "the hand-off" bracket | 4 s |
| 8 | **For 15 of the 20 most common hand-offs, no status page showed a work order** | 20 tiles, each named (service and closing words). 15 go grey with "no work order", 5 lit; "Tree removal: 40 of 40". Sub-line: "800 status pages read · about 22,800 requests in the 15 grey types". | 5 s |
| 9 | **For 84% of the 14,902, no record says whether the work was done** | Real basemap labelled St. Louis. Dots arrive in waves by service with a legend, then recolour in order: done 3%, pending 8%, later request closed 2%, never-closed leftovers 3%, no record 84%. Note: "14,496 of 14,902 shown at block level; sensitive types withheld". | 4 s |
| 10 | **Same block, same day, same answer: one lot cut three times, the other none on record since Oct 2024** | Block schematic with the twin lots highlighted; two phones each reading "on schedule to be cut"; cut marks on one. Closing line on screen (not spoken): "Across 2026: 28% of 'on schedule to be cut' answers went to lots with no cut on record all year" | 5 s |
| 11 | **The city has said it** | The towing-page quote card, held 4–5 s | 2 s |
| 12 | **Three steps: attach the job · flag the misses · count the finish** | The beat-7 diagram rebuilt; each step lights one part of it | 4 s |
| 13 | **With the link, the lot that fell off the rounds is seen that week** | The twin lots replayed: one linked, one flagged on Forestry's list | 3 s |
| 14 | **Ranked by hazard, Forestry's top 25 overdue jobs go from 9 safety hazards to 25** | Two columns of 25 rows, oldest-first against ranked, with hazards lit | 5 s |
| 15 | (screen recording) | The demo with cursor-follow zoom | about 25 s in all |
| 16 | **What the city gets: a saved search, a dashboard, SQL, weights, a one-page practice** | Five file glyphs dropping into Cityworks, the map portal, CityStat and the divisions; then the Forestry commissioner's quote card ("…we don't have somebody on staff that's just designated to kind of analyze all that data"), held 5 s while "AI agents did the audit" is spoken | 5 s |
| 17 | **The ask: one quarter, three request types, then re-run against today's baseline** | Three cards, three verbs, and the baseline 14,902 frozen with its date | 3 s |
| 18 | **Which promises did St. Louis keep?** | The question, then the end card | end card 5 s |

## Figures behind each spoken number

| Spoken | Value | Source | Label |
|---|---|---|---|
| 14,902 past the date | 14,902 open, filed since 1 Jan 2025, promise before 13 Oct 2026 | `e3_queue_past_promise` | observed |
| 84% no record; 3% done; 8% pending | 84.3% / 2.6% / 8.1% | `research/open-queue-reality-check.md` | observed |
| CityStat 79%; 15% "picked up"; most "later or investigated" | 78.6% published; 15.0% done-only on the same denominator; 58.0% of on-time closings say later or investigated | `e3_citystat_debris_published_vs_done`; `research/closure-class-review.md` | observed |
| about two days to close | median 2,601 minutes (1.8 days) over 61,845 hand-off closures, 2025–26 | DuckDB query (14 Oct, 10:05 p.m.); to register | observed |
| about five weeks after filing | median 35 days, filing to recorded work (traced hand-offs) | `research/chapters/R1-trace.md` headline | observed |
| 800 pages; 20 most common hand-offs; 15 with no work order; about 22,800 requests; tree removals every time | 40 pages × 20 kinds; 15 kinds with 0 items; 22,761 requests in those 15 kinds (Jan 2025 to Aug 2026); 40 of 40 | `research/status-page-linkage.md`; `build/E1/sample_strata.csv` | observed |
| twin lots: same July day, within the hour, three cuts; no cut on record since Oct 2024; dropped off the rounds | lot-1: 2 Jul, closed in 13 min; twin: closed in 4–59 min, cut 3 times in 2026; lot-1: last billed cut 24 Oct 2024. "Dropped off the rounds" is inferred: 97% of land-bank lots cut in 2025 were cut again in 2026 | `research/north-taylor-mechanism.md` | observed / inferred |
| 28% of "on schedule" answers | 479 of 1,724 (27.8%), 2026 | same | observed |
| towing quote; commissioner quote | CityStat towing page (live 14 Oct); Forestry Commissioner, 6 May 2026 | `research/chapters/R3-voices.md` rows 1 and 7 | observed |
| Cityworks closes a linked request | Cityworks 23 help; St. Louis runs 23.10 | `research/precedents-closed-loop.md` §A2 | observed (vendor documentation) |
| 9 safety hazards → 25 | Forestry top 25, oldest-first vs ranked, tier-1 hazard types | `research/prioritisation-option.md`; the site session is verifying it | observed (pending recheck) |
| 124,000 requests a year | 124,077 filed in 2025 | `requests` table | observed |

## Claims v5 does not make

- **That the 14,902 are all residents waiting.** It says "past the date" and "no record either way".
- **That closing fast caused the North Taylor miss.** Its twin was closed just as fast and was cut.
- **"Never cut".** It says "no cut on record".
- **That the 15% is what crews cleaned.** It says closings that *say* it was picked up.
- **That ranking makes crews faster.** "Whether the crew comes sooner is up to the crew."
- **Any equity claim.**
- **That AI is in the product.** AI did the audit; the product is SQL.

## Cut list, applied at lock (beat 6 kept as its own short beat, because Jack asked for the three-dates framing)

1. Beat 6 merges into beat 7: "311 gives every request a promised date. About two days after filing…" Saves about 6 s.
2. Beat 11 keeps only the towing quote; the commissioner quote moves to beat 16 as an on-screen card. Saves about 8 s.
3. Beat 4 drops its last sentence. Saves about 4 s.
4. Beat 10 drops its last sentence; the 28% stays as an on-screen line. Saves about 7 s.
5. Beat 15's demo is trimmed to 25 s. Saves about 15 s.
