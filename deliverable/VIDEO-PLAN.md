# Video plan: a 3Blue1Brown-style explainer of the entry

Written 14 Oct 2026, about 5:35 p.m. Central, by the orchestrating thread, after Jack asked for the video to be made in the 3Blue1Brown idiom with Manim, with the time limit treated as soft. Research is closed; this is a presentation plan. Section 6 records what was tested on this Mac today.

## 0. Decisions this plan assumes (Jack confirms or changes)

1. **Length:** 3:00 to 3:30. The two-minute limit is treated as a guideline; the submission is the idea communicated fully, trimmed only if a cut costs nothing.
2. **Narration first.** Jack records the narration (a scratch take tonight, the real take Thursday morning); scenes are timed to the audio. That is how 3Blue1Brown works and it removes the hardest sync problem.
3. **The video carries the argument; the site carries the product and the data.** Every statistic, chart, quote and example that argues moves into the video. The site keeps the three product screens, the case document and the data page.
4. **One accent colour per idea, dark background, nothing static longer than four seconds, every number arrives with motion, every line of text is written in, not pasted.**

## 1. The grammar: what makes it read as 3Blue1Brown

- **Objects transform into each other.** A bar becomes a list. Dots become a column. A diagram rebuilds itself rather than being replaced.
- **The camera moves.** Pan and zoom between ideas instead of hard cuts; the map shrinks to a corner and comes back.
- **Counters tick, clocks sweep.** Numbers are never typed on screen; they count up, and a promise date is a clock hand.
- **Real artefacts enter as cards.** A screenshot of CityStat, of the status page, of a quote with its source and date, slides in with a soft shadow, is pointed at, and leaves.
- **The narration leads and the screen answers within a beat.** No screen element appears before its sentence.
- **Text is sparse.** At most one line of text on screen besides labels; the voice carries the rest.

## 2. The beats

Times are for a 3:20 cut. Narration is script v4 (to be written on this spine, with the explicit bridge and the after-example).

| # | Time | Narration (summary) | What the screen does |
|---|---|---|---|
| 1 | 0:00–0:20 | I'm Jack. I looked at the problems residents report most: lots, cave-ins, trash, sidewalks, trees. I expected five problems. I found one. | The outline of St. Louis draws itself (ward boundaries). Dots rain in: every 311 request since January 2025, a counter ticking past 300,000. Five labels fly in and the dots recolour by type. The five labels slide together and merge into one. |
| 2 | 0:20–0:55 | How a request moves through the city today. | The map shrinks to a corner. One dot lifts out and becomes a request card. The flow builds left to right: card → "311" → a promise clock (14 days) → a division box → a CLOSED stamp slams down at the hand-off. Below, a "work order" box appears; the connector from the card draws toward it, hesitates, fades. On the right a CityStat bar ticks up at the stamp. The camera pushes into the resident's page card: "Closed · Referred · nothing attached." |
| 3 | 0:55–1:40 | The issues that gap creates, and what they mean for residents. | (a) The alley-debris bar: 78.6% stands; its hand-off segment (two thirds of it) peels off and falls away, leaving 15.0%; caption "closed as 'will be investigated', no clean-up on record". (b) 3,640 small squares (traced jobs); a clock sweeps; 18% turn green by the promise, 50% turn green late as the clock passes 28 days, 32% stay grey, "no record". (c) The map returns; 14,902 dots light up coloured by age with a counter; the dots sort themselves into a column list by division: Forestry 4,679 · Streets 4,185 · Building 1,219; "nobody holds this list." (d) A grid of 1,440 page icons groups into 20 columns by type; 15 go grey (nothing attached); 5 light up (tree removals 40 of 40, plantings 34 of 40, cave-ins 16 of 40); caption "6% of hand-offs carry a work order". |
| 4 | 1:40–2:10 | What it costs one block, and the city's own words. | Zoom to the N Taylor block: a schematic of 37 parcels; 36 turn green one by one with their cut dates; one stays brown. Two call markers appear: 2 July, "closed in 13 minutes"; 28 July, "closed in 7 minutes". Then three quote cards slide in, each line written in, with source and date: the towing page; the head of 311; the transition committee. |
| 5 | 2:10–2:45 | The fix is in the software they own; three rules. Then the same lot, under the rules. | The flow diagram rebuilds. At the hand-off the work order attaches: the connector draws solid. The CLOSED stamp hovers and fades: not stamped. The promise clock keeps running on the open card. The crew finishes; the work order closes; the request closes by itself, with the label "Cityworks 23: built in"; CityStat ticks only now. Three rules write in beside the diagram as spoken. Then the lot replays on a timeline: 2 July filed and attached; 17 July on Forestry's list, one day past; 1 August near the top; the supervisor assigns; the parcel turns green; the resident's card reads "With Forestry since 2 July, promised 16 July, cut 3 August"; the 28 July call marker is drawn and struck through: it never happens. |
| 6 | 2:45–3:20 | What we hand over, and what it produces today. | Four boxes: Cityworks, the 311 status page, CityStat, the geoportal. Four files drop into them: the closure dictionary (SQL) into CityStat; the saved search and dashboard into the geoportal; the one-page practice into the divisions; the page spec into the status page. Then the three real screens from the site enter as cards with a camera pan: the queue (map and list), the status page after, CityStat with the column. Caption: "two of these run today on your data with no change in practice." |
| 7 | 3:20–3:35 | Try it on three request types for a quarter; re-run in ninety days. | The baseline numbers freeze on screen with the date 13 October 2026. End card: the name, "built from the City's open data and Cityworks saved searches read with the City's permission; not a City website", the repository link. |

## 3. What moves from the site into the video, and what the site keeps

**Into the video:** the closure mix (35% hand-off), the alley-debris pair, the promise grading (57.8% / 19.5%), the traced fates, the queue totals and the division split, the 1,440-page table, the lot, the quotes, the four rules, the "what we hand over" stack. All of these are arguments; a viewer should not have to find them.

**The site keeps:** the queue (the working dashboard), the status page (lookup and before/after), CityStat with the column, the data page with the manifest and downloads, and the case as one readable document for the judge who wants the evidence. The site is the demonstration of the package and the proof it runs on real data; it no longer tries to persuade.

## 4. Data every animation needs (all on disk, no new analysis)

| Beat | Data | Where |
|---|---|---|
| 1, 3c | Ward outlines (14 polygons, GeoJSON) | `wards` table in `build/stl.duckdb` |
| 1 | Request counts by type since 2025 | `build/N2/register.json`, `site/data/figures.json` |
| 3c | 6,207 block dots with age, division | `site/data/queue.json` (positions snapped to a 60 m grid; block level) |
| 3a | Alley-debris published vs done-only | `e3_citystat_debris_published_vs_done` |
| 3b | Traced fates 18.0 / 49.8 / 32.2, median 28 days | R1 headline figures |
| 3d | Per-type attach counts | `build/E1/service_table.csv` |
| 4 | The lot: dates, the 36 neighbours' cut days, the two closures | `build/N5/heroes.json` (public fields); parcels drawn as a schematic, labelled as such |
| 4 | Three quotes with URLs and dates | `research/chapters/R3-voices.md` |
| 5 | The Cityworks auto-close rule | `research/precedents-closed-loop.md` §A2 |
| 6 | Screenshots of the three screens | `build/E3/shots/` (re-captured after the site reshape) |

Block positions and the parcel schematic keep every public rule: nothing below block level, no request numbers, no addresses beyond "the 1700 block of N Taylor Av".

## 5. Production plan and timeline

- **Tonight.** Script v4 locked by Jack. Jack records a scratch narration (phone or QuickTime) so scene lengths can be set. Scenes for beats 1 to 3 built at 480p and reviewed as MP4s. Each beat is its own scene file, rendered and reviewed on its own.
- **Thursday 8 a.m. to noon.** Beats 4 to 7. Final narration recorded. 1080p renders (a scene of 30 seconds renders in well under a minute on this machine).
- **Thursday noon to 2 p.m.** Assembly: concatenate the scenes, mux the narration, add captions where the spoken number should be read. Review once end to end.
- **Thursday 2 to 4 p.m.** Upload to YouTube; publish the repository; submit.
- **Risk control.** A beat that will not render in time becomes a still card with the same narration, so the video stays coherent. The worst case is animated text over screenshots, which still communicates the idea.

## 6. The substrate: what was tested on this Mac today

| Engine | Tested | Result | Notes |
|---|---|---|---|
| **Manim Community v0.22** (`video/.venv`) | A scene with written text, a counter ticking to 14,902, 300 dots fading in, a polygon drawing; rendered to MP4 at 480p | **Works.** 5.3 seconds of video in 1.6 seconds of render time; ffmpeg, cairo and pango were already installed | No LaTeX on this machine, so numbers use `Text`, not `Integer`/`Tex`; `ImageMobject`, `SVGMobject` and `MovingCameraScene` are standard, which beats 4 and 6 need |
| **franken_manim v0.5.0** (native binary, `fmn`) | The built-in `circle_shift.v1` scene to a PNG sequence | **Works.** 12 frames in 0.17 seconds; installer verified the SHA-256 | The binary cannot run Python scenes; it takes built-in scenes, `.fmtl` bundles, or the Rust API |
| **franken_manim Python front door** (`fmn-python`, manimlib dialect, macOS arm64 wheel, `video/.venv-fmn`) | The same test scene in 3b1b's manimlib dialect (`Write`, `ValueTracker`, `LaggedStart`, `ShowCreation`) | **Works for frames.** 319 PNG frames at 640x360 in about 6 seconds. The `--format mp4` run reported 319 frames but wrote no file, so MP4 would be assembled from the PNG sequence with ffmpeg ourselves | The README says 37% of the 3b1b corpus runs to completion today and the engine is pre-1.0; image mobjects (screenshots, quote cards) are not confirmed |

**Recommendation.** Build in Manim Community. The 3Blue1Brown look comes from the grammar in section 1 and from Manim's animation model, which both engines share; Manim Community is mature, has image and SVG mobjects and a moving camera, and rendered first time here. Keep franken_manim as an option for a scene if its spike passes and its native TeX look is wanted for a title; do not make the whole video depend on a pre-1.0 engine the day before the deadline.

## 7. Where the project stands

Research, analysis and synthesis are closed. What remains is selection and presentation: script v4, the scenes, the narration, the site reshape as the demonstration, the README as the case, the repository publish. No further research is needed; any gap found now is a wording gap, and the figures that the video speaks are already registered with derivations.
