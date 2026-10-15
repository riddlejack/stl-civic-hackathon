# Video beats v5: the screen plan for the locked script

Written 14 Oct 2026, about 10:30 p.m. Central, for the locked `deliverable/video-script-v5.md`. Each of the 18 beats is one scene file `video/scenes/bNN_name.py` (class `BNNName`, `BEAT = "bNN"`), rendered to `video/renders/bNN.mp4`. The v2 scenes are archived in `video/scenes/v2/`. Reuse their code freely, especially `v2/b03_today.py` (the diagram), `v2/b05_lot.py`, `v2/b04_gap.py` and `v2/b08_product.py`.

## Rules every scene follows (Jack's review and `video/review/DOCTRINE-for-video.md`)

1. **Action title.** Each beat's final frame carries its action title, worded exactly as in the script's table. A viewer with the video paused and muted must get the point.
2. **Reading time.** Text fades in whole: no letter-by-letter writing, no morphing text. Once in, it stays still while it is read. After the last sentence ends, hold the final frame for at least the script's "minimum time fully visible" (call `self.until_end()`, then `self.wait(extra)`). Never under 3 s for a frame with a number.
3. **One typeface: Charter** (kit v2's `T()` and `S()`). No sans-serif anywhere.
4. **Plain words.** Every number shows its unit, population and date (small source line at the bottom, above the bottom 12% of the frame, which stays clear for YouTube's controls). No text on screen that the voice doesn't cover, except labels, legends and source lines.
5. **Joins.** Hold frame 0 still for the first 0.5 s (a composed opening, or plain background), and keep the last 0.6 s still. Assembly dissolves every join over 0.5 s.
6. **Illustrations, not placeholder cards.** Use `illus.py` (resident with phone, fallen tree, pothole, cracked sidewalk, overgrown lot, trash bags, mower, boarded window, crew truck, phone status screen, status-page tile). A PromiseCard is fine where the idea *is* "a request", but give it real content: service, block, date.
7. **Honest.** Numbers exactly as in the script's figure table. Schematics are labelled "schematic". Privacy: block level at most; no ids or addresses below the block.
8. **Check your own work.** Pull frames at each sentence start + 0.6 s and at the final hold, view them, and fix clipping, overlap, unreadable text and anything static or empty. The render duration should equal the cue duration plus your hold extension.

## The beats

Cue indices refer to the sentences of each beat in `video/audio/cues.json`.

### Builder V1: opening, headline numbers, close (b01–b05, b18)

| Beat | Scene | Screen |
|---|---|---|
| b01 | `b01_open.py` `B01Open` | One illustrated vignette per sentence, on "A fallen tree", "A cracked sidewalk", "A lot nobody mowed", "Trash nobody picked up": a resident with a phone in front of each problem, four across. On "broke the same way", a thin GOLD line draws through all four, and each vignette gets the same small stamp, "closed". End: the four vignettes dim. |
| b02 | `b02_title.py` `B02Title` | The vignettes fade out. The title, in large serif: **St. Louis can't tell which of its 311 promises it has kept** ("kept" in YELLOW). Hold 3 s. |
| b03 | `b03_headline.py` `B03Headline` | The title rises small to the top. A counter runs to **14,902** in about 1.5 s, with the label "requests past the date the city promised". Then a single horizontal bar: 84% GREY ("no record either way"), 16% split thin (2.6% done GREEN, 8.1% pending BLUE, rest MUTED). Source line: "Open 311 requests filed since 1 Jan 2025, past due on 13 Oct 2026 · city 311 file, Cityworks, city records". |
| b04 | `b04_scorecard.py` `B04Scorecard` | A clean CityStat-style bar: "Alley and street debris · Apr–Jun 2026 · share counted on time" grows to 79% (78.6). It splits into GREEN 15% "closing says it was picked up" and a RED remainder labelled "closed with other words". Hold. Source line: "CityStat (published); same requests by closing words, city 311 file". Action title as in the script. |
| b05 | `b05_fixline.py` `B05FixLine` | A request card ("Overgrown lot · N Taylor · due 30 Sep") and a crew job card (mower illustration) joined by a solid TEAL line. Title: **The fix: keep each request tied to its job until the job is done.** |
| b18 | `b18_close.py` `B18Close` | *Which promises did St. Louis keep?* ("keep" in YELLOW), held. Then the end card: "[NAME]" (muted placeholder); "Jack Riddle · Civic AI Hackathon · St. Louis · October 2026"; "repository: [link]"; "Built from the City's open data and Cityworks saved searches read with the City's permission (operational fields only; no personal data). Not a City website."; "Map data © OpenStreetMap contributors; Census TIGER". Hold 5 s, then fade to black. |

### Builder V2: how a promise works, where it breaks, the three steps (b06, b07, b08, b12)

| Beat | Scene | Screen |
|---|---|---|
| b06 | `b06_dates.py` `B06Dates` | A horizontal timeline. On each phrase a tick and label fade in: "filed", "promised", "done". A small request card rides the line. Title: **Every request has three dates.** |
| b07 | `b07_handoff.py` `B07Handoff` | The same timeline, rescaled to days. "Closed" (RED stamp) lands at about day 2, with the label "311 closes it, median 1.8 days". A bracket "the hand-off" with the closing words in italics: "on schedule to be cut". Then "work recorded, median 35 days after filing" lands far right in GREEN, with a long empty span between (label: "the request no longer tracks the job"). Title as in the script. Source: "61,845 hand-off closures, 2025–26; recorded work for traced jobs (mowing, board-ups)". |
| b08 | `b08_tiles.py` `B08Tiles` | First, Cityworks can attach a work order: a request card and a work-order card join, labelled "what Cityworks can do". Then 20 status-page tiles, 5×4, each headed with the service and its closing words from `build/E1/sample_strata.csv` (H01–H20; e.g. "Vehicle towing · 'tagged for tow'", "Refuse · 'next scheduled day'", "Debris · 'will be investigated'"). The 15 with nothing attached go grey with "no work order"; the 5 others stay lit, with their result. A large callout: "Tree removal: work order attached, 40 of 40" (the control stratum). Sub-line: "800 status pages read, 40 per type · about 22,800 requests in the 15 grey types (Jan 2025–Aug 2026)". Title as in the script. |
| b12 | `b12_steps.py` `B12Steps` | Rebuild the diagram (from `v2/b03_today.py`): resident → 311 → request card → Forestry → crew job. Three steps light in turn, each with a short label that stays:<br>1. **Attach the job**: a solid TEAL connector from request to work order; a small amber warning "no job to attach → flagged on day one"; tag "Cityworks closes a linked request when its work order closes (vendor docs)".<br>2. **Flag the misses**: a weekly list rises beside Forestry, "past its date, no finished job".<br>3. **Count the finish**: a CityStat column, "on time = job finished by the date".<br>Title: **Three steps: attach the job · flag the misses · count the finish.** |

### Builder V3: the map and the block (b09, b10, b13)

| Beat | Scene | Screen |
|---|---|---|
| b09 | `b09_map.py` `B09Map` | Kit v2 `StlBaseMap`, large (rotate if it helps), labelled St. Louis, with the river. Dots arrive in waves by service family (legend visible from the first wave). On "color each one by what the city's records show", recolour in order, each step with its legend row and number:<br>• done 2.6% (GREEN, those dots light where they are);<br>• crew order pending 8.1% (BLUE);<br>• a later request at the same address was closed 2.2%;<br>• likely never-closed leftovers 2.7%;<br>• **no record either way 84.3%** (GREY), last and largest.<br>Note at the bottom: "14,496 of 14,902 shown at block level; sensitive types and unplaceable requests withheld". Title as in the script. Hold. |
| b10 | `b10_twins.py` `B10Twins` | From the map, zoom to North Taylor (ward 12; block level), then cross-fade to `shared_block.build_block()` with **two** city-owned parcels highlighted: "this lot" and "its twin" (schematic positions). Two phones (`illus.phone_status`), each reading "Closed · on schedule to be cut", with "same day · within the hour". The twin gets three cut marks, "cut 3 times in 2026"; this lot stays grey, "no cut on record since Oct 2024". A small chip "dropped off the cutting rounds (inferred)". Closing line on screen (not spoken): "Across 2026: 28% of 'on schedule to be cut' answers went to lots with no cut on record all year (479 of 1,724)". Facts: `research/north-taylor-mechanism.md` and its facts CSV. Title as in the script. |
| b13 | `b13_replay.py` `B13Replay` | The same block. On 2 July both requests come in: the twin's request links (solid TEAL) to "next cut on the route"; this lot's request finds nothing to link, so a warning appears and the request stays open (BLUE border, no stamp). Then a small "Forestry · this week" list slides in with this lot flagged at the top. The parcel stays grey (honest). Title as in the script. |

### Builder V4: the city's words, ranking, demo, package, ask (b11, b14, b15, b16, b17)

| Beat | Scene | Screen |
|---|---|---|
| b11 | `b11_quote.py` `B11Quote` | One QuoteCard (Charter): *"Closed" does not necessarily indicate that a vehicle has been towed* — City of St. Louis, CityStat towing page, 2026. The plan line under it, smaller: *"…requests are only closed once a vehicle is actually towed."* Hold 5 s. |
| b14 | `b14_rank.py` `B14Rank` | Two columns of 25 Forestry rows (type name only, no blocks): "Oldest first" vs "Ranked: hazard + lateness + repeat reports". Hazard rows lit RED (life-safety tier). Counters at the column heads: "9 of 25" vs "25 of 25". Source: "Forestry's open requests past their date, 13 Oct 2026; ranking weights in rank-weights.json". Data: `site/data/ranked.json` and the registered figures from the site session (wait for them, or ask the orchestrator); never invent rows. Title as in the script. |
| b15 | `b15_demo.py`, or `video/tools/make_demo_beat.py` | The screen recording `video/renders/demo_zoom.mp4` (from the site session), trimmed to about 25 s and aligned to beat 15's sentences: the ranked list, a block, the resident page, then CityStat. A 0.5 s still first frame and a 0.6 s still last frame, with beat_15.wav as audio. Output `video/renders/b15.mp4`, 1920×1080, 30 fps. A thin rounded frame around the recording on the film's background is a nice touch. |
| b16 | `b16_package.py` `B16Package` | Five file glyphs ("saved search", "dashboard", "SQL", "ranking weights", "1-page practice") drop into four boxes: Cityworks, the city's map portal (ArcGIS), CityStat, Divisions. On "AI agents did the audit", the Forestry commissioner's QuoteCard: *"…we don't have somebody on staff that's just designated to kind of analyze all that data"* (Forestry Commissioner, Budget & Public Employees Committee, 6 May 2026), held 5 s. Then "plain SQL · nothing to buy" in GREEN. |
| b17 | `b17_ask.py` `B17Ask` | "One quarter" over three illustrated cards: tree removal, cave-in, vacant-lot mowing. Three verbs: "attach the job · work the list · count the finish". The baseline counter 14,902, frozen, with "citywide baseline · all request types · filed since Jan 2025 · as of 13 Oct 2026". Title as in the script. |

## Assembly

`video/tools/render_all.sh` discovers `bNN_*.py` files automatically. Then:

```bash
video/.venv/bin/python video/tools/assemble.py v3
```

Every join dissolves over 0.5 s. A beat that opens on its predecessor's exact last frame can be listed in `video/joins.json` under `cut_into` to cut instead.
