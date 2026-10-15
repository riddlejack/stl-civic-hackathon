# Restructure for v5: top-down, plain English, time to read

Written Wednesday 14 October 2026, about 9:45 p.m. Central, after Jack's beat-by-beat review of rough cut v2. It draws on four checks that ran in parallel:
- `research/north-taylor-mechanism.md`
- `research/prioritisation-option.md`
- `video/review/DOCTRINE-for-video.md` (the Keystone deck rules applied to the video)
- the basemap and demo-recording prototype (`video/review/basemap_proto.png`, `video/review/demo_proto.mp4`)

## Summary

Jack's review is right on all four counts.

1. **Order.** The cut wasn't top-down: the fix first appeared at 2:43.
2. **Time to read.** Frames carrying a number were readable for a median of 1.7 s, against the 5–7 s their main line needs.
3. **Plain language.** "1 in 4 what?", "15 of 20 what, and why care?", "800 pages of what?"
4. **The North Taylor example claimed the wrong mechanism.** The check found that closing fast is *not* why the lot was missed. Its twin on the same block was reported the same days, got the same answer within minutes, and was cut three times. The lot had dropped off the cutting rounds in October 2024. The honest version is a stronger example of the root cause: 311's answer "on schedule" is never checked against the schedule.

The proposal below keeps the evidence, reorders it so the answer comes first, adds a small built ranking tool, and plans every frame to be held long enough to read.

## Answers to Jack's questions

**Did the neighbours have requests too? (observed)**
- 33 of the 36 cut neighbours had no weed report at all.
- The closest twin, a land-bank lot reported on the same days, got "on schedule to be cut" five times, closed in 4–59 minutes, and was cut three times in 2026.
- Lot-1 has had no billed cut since 24 Oct 2024. Ownership, list category, land use and ledger type all match its cut neighbours.
- **Mechanism (inferred, and the only version we can say):** the lot fell off the cutting rounds; 311 told the resident twice, within minutes, that it was "on schedule to be cut", the same answer its cut twin got; nothing checks that answer against the cutting record, so the miss stayed invisible.
- **Systemic:** 479 of 1,724 (27.8%) "on schedule to be cut" closures in 2026 were on parcels with no cut billed all year. Closing speed makes no difference.

**"13 minutes" (observed).** That was this one lot. Across all 61,845 hand-off closures in 2025–26:
- median time to close: about 1.8 days (2,601 minutes);
- closed within the hour: 11%; within a day: 42%.

Where the work is recorded, it comes a median 35 days after filing (R1). So the honest line is: 311 closes the request in about two days; the work, when it is recorded at all, comes about five weeks after filing.

**"15 of 20 hand-offs" (observed).**
- A hand-off is a closing where 311 passes the job to a crew and closes the request, e.g. "on schedule to be cut", "collection will be made next scheduled day", "vehicle tagged for tow", "matter will be investigated".
- The 20 most common kinds cover about 29,700 requests (Jan 2025 to Aug 2026). We read 800 of their public status pages, 40 per kind.
- In 15 kinds, covering about 22,800 requests, no page showed anything attached: no work order, no inspection.
- Tree removals attached a work order 40 of 40 times.
- Why it matters: without the attachment, nothing connects the request to the job, so no one can see whether the job happened.

**Does the city already prioritise?** We don't know what divisions sort by.
- *Reported:* Cityworks has priority labels and due dates per type, and a separate scheduling product (Workload), but no ranking engine.
- *Observed:* work-order priority is empty on all 29,018 city work orders we hold.
- **Recommendation: build a small, transparent ranking**, a "Ranked" toggle on the existing list. The score adds up three things: hazard tier by request type, days past the promise, and repeat reports, with every point shown on the row.
- First, the 1,130 requests with evidence they were done, superseded, or never meant to be closed go to a separate "close-out" list.
- With this ranking, Forestry's top 25 overdue jobs go from 9 life-safety items (oldest-first) to 25.
- No AI in the score. The public file has no free text, so "AI severity" would be invented.

## The story, top-down (about 4:30 if everything stays; cut options below)

Narration is in Jack's voice, plain, and pauses after key sentences. No name in the intro. Times assume holds that meet the reading rule.

**I. The answer (0:00–0:45)**
1. *"I came into this hackathon looking for one broken city service."* Four quick vignettes, each with a resident on the phone: a fallen tree, a sidewalk, an overgrown lot, trash. *"Every one I checked broke the same way."*
2. Title card, held: **St. Louis can't tell which of its 311 promises it has kept.**
3. Two headline numbers, each held:
   - **14,902** requests are past the date the city gave; for **84%**, no record says whether the work was done.
   - CityStat counts **79%** of alley-debris requests as on time; only **15%** of those closings say the debris was picked up.
4. The answer in one line: *the fix is already in software the city owns: keep each request tied to its job until the job is done.*

**II. How a promise works today, and where it breaks (0:45–2:00)**

5. **Three dates.** Filed, promised, done, on one line. *"Every request gets a date: a promise."*
6. **The hand-off.** 311 closes the request about two days after filing, when it passes the job on ("on schedule to be cut"). When the work is recorded at all, it comes about five weeks after filing. *"From the hand-off on, the request stops tracking the job."*
7. **The missing link, with real labels.**
   - Twenty labelled tiles, each a service and its closing words.
   - Fifteen grey out: *"For 15 of the 20 most common hand-offs, about 22,800 requests, the city's status pages show no work order attached. Tree removals did, 40 of 40."*
8. **Consequence 1: the scorecard.** The 79 → 15 bar in plain English, held: *"CityStat counts the hand-off as on time."*
9. **Consequence 2: the pile.**
   - A real basemap labelled St. Louis, with river and highways.
   - 14,902 dots in waves by service, with a legend from the start.
   - Then the same dots recolour, in order: done 2.6%, crew order pending 8.1%, later request closed 2.2%, never-closed leftovers 2.7%, **no record 84.3%**.
   - *"No one can tell those residents, or the mayor, whether the work happened."*

**III. One block (2:00–2:40)**

10. **The twin lots.**
    - Two city-owned lots on North Taylor, reported on 2 July. Both get "on schedule to be cut" within the hour.
    - One is cut three times; the other hasn't been cut since October 2024.
    - *"311's answer was the same, because nothing checks it against the schedule. This year, 28% of 'on schedule to be cut' answers went to lots with no cut all year."*
11. **The city's own words**, each held 4–5 s: the towing page ("closed does not necessarily indicate…"), the 311 director ("why it's past the completion date…"), and the Forestry commissioner ("…no one designated to analyse all that data").

**IV. The fix and what it changes (2:40–3:50)**

12. **The new system, in plain steps on the same diagram.**
    - **Attach the job:** at the hand-off, the division attaches the crew's job, a work order or the lot's slot on the route. If there's no job to attach, that's visible on day one. Cityworks closes the request when the job closes (vendor documentation).
    - **Flag the misses:** every week each division sees every request past its date with no finished job, ranked so the dangerous ones come first.
    - **Count the finish:** CityStat counts on time only when the job finished by the date.
13. **The twin lots, replayed.** The twin's request attaches to its cut. Lot-1 has no job to attach, so it's flagged on 2 July instead of never.
14. **Impact.**
    - Ranked, Forestry's top 25 overdue jobs go from 9 life-safety items to 25.
    - The same weekly list works for every division in Cityworks, on 124,000 requests a year.
    - The 14,902 becomes a known list: done, waiting or lost. CityStat reports work done.
    - *"Knowing which promises were kept is the precondition for keeping more of them."* This is labelled as our expectation, with the precedents: Chicago closes a request only with its last work order; Houston and Toronto put "stay open until done" in writing.

**V. The product and the ask (3:50–4:30)**

15. **Screen-recorded demo** with cursor-follow zoom, about 35 s:
    - Forestry's list, then the Ranked toggle with "why this rank";
    - click a block on the map;
    - the resident's page, Today vs After;
    - CityStat with the new column.
16. **What we hand over:** the saved search, dashboard, SQL, scoring weights file and a one-page practice per division. AI agents did the audit; the city runs plain SQL.
17. **The ask:** one quarter, three request types; re-run against today's baseline. *"Then you'll know which promises you kept."*

**Cut options**, if 4:30 is too long:
- drop the obvious-fix beat (already folded into 12, so this costs nothing);
- drop the traced 3,640 mowing and board-up jobs (they're in the report);
- trim the quotes to two.

That gets to about 3:50.

## Visual and pacing rules for v5

- **One typeface, Charter, for everything.** The sans-serif labels go.
- **Text fades in whole and stays still while it's read.** Hold time ≥ 1 s + 1 s per 3 words + 0.5 s per number, never under 3 s for a figure. Every hero frame passes the muted-and-paused test: it has an action title, numbers with unit, population and date, and a source line.
- **Illustrations instead of generic cards:** a resident with a phone in front of the problem; a fallen tree; a mower; a boarded-up window (board-up means sealing an open vacant building); a crew truck. Simple line art in the film's palette.
- **Real basemap:** city boundary, Mississippi, highways, Forest Park, county edge, the label "St. Louis". All 14,902 dots at block-level positions, in waves by service, then recoloured by evidence.
- **Demo:** a real screen recording of the site, with zoom following the cursor (prototype status in the basemap/demo report).
- **Kept from v2:** the diagram (today vs fixed), the 79 → 15 bar, the block schematic, the quote cards and the end card. They get re-laid out and held longer.

## What has to happen, and when

- **Tonight, once Jack approves the structure:**
  - Script v5 (orchestrator). Then Jack reads it; about 10 minutes.
  - The site's Ranked view (one session), then re-shoots and the demo recording.
  - A kit upgrade: one font, hold helpers, illustration library, basemap (orchestrator).
  - Scenes rebuilt by four builders overnight, then an editor QA pass.
- **Thursday morning:** Jack records the narration (one file per beat), then cues, render, assemble (about 30 minutes), a fix pass, and upload by 3 p.m.

## Prototype status (about 9:55 p.m.)

- **Basemap works** (`video/review/basemap_proto.png`, `video/data/basemap.json`, `video/tools/build_basemap.py`). It shows the city boundary, the Mississippi, highways, streets, Forest Park, St. Louis County, and labels for "St. Louis", "Mississippi River" and "Illinois". The dots line up to within about 0.5 m of the site map, and a frame renders in 16 s. The Illinois side is blank: two small Census road files (about 3 MB in all) would fill it in, but they have not been fetched.
- **Mapping:** 14,573 of the 14,902 can be shown at block level. 329 are sensitive types, which stay at ward level, and about 77 can't be placed without going below block level. For one dot per request, spread each block's count as a small cluster inside its 60 m cell. The on-screen label would read "14,573 of 14,902 shown; sensitive types withheld".
- **Screen-recording demo works** (`video/review/demo_proto.mp4`; `video/tools/record_demo.py` and `zoom_follow.py`). It uses Playwright from an existing environment (nothing was installed) and Jack's Chrome. The cursor is drawn afterwards, and zoom eases in on each click. Weak spots: scrolling may judder, and the header shows "[NAME]".
