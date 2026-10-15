# Video beats: the screen plan for script v4

Written 14 Oct 2026, about 6:50 p.m. Central. It follows from `deliverable/video-script-v4.md` (narration first, screen second). Each beat becomes one Manim scene file in `video/scenes/`. The scene is timed to the narration of that beat (`video/audio/beat_NN.wav`, sentence cues in `video/audio/cues.json`, scratch voice for now), and the rough cut is the nine renders concatenated.

**Summary.** Nine beats, 4:17 with the scratch voice. One object runs through the film: **the promise card**, a 311 request with a clock that fills toward its due date. The first half takes the city's system apart around that card (beats 2–5). Beat 6 shows the obvious fix failing. Beat 7 rebuilds the same diagram with the link, the list and the count, then replays the real lot. Beat 8 shows the real screens; beat 9 is the ask. The shared kit is `video/scenes/kit.py`. Most likely to survive Jack's feedback: the kit, the system diagram (beats 3 and 7), the map and waffle (beat 4), the lot's block (beats 5 and 7), the quote cards and the end card. Most likely to change: beat 2's examples, beat 8's screens (they wait on the site reshape), and the beat lengths (they follow his real voice).

## 0. How a scene is built

- `from kit import *`. Subclass `CueScene` and set `BEAT = "b03"`. Call `self.until(i)` to wait until sentence *i* of the beat starts. Size each animation's `run_time` to the gap (`self.fit(desired, i)`). End with `self.until_end()`. The beat's WAV is attached automatically.
- **Never hard-code a time.** When Jack records his own narration, the cues get regenerated and every scene re-times itself.
- Render a draft: `cd video/scenes && ../.venv/bin/manim -ql --media_dir ../media bNN_name.py SceneName`.
- Render for the rough cut: `../.venv/bin/manim -r 1920,1080 --frame_rate 30 --media_dir ../media bNN_name.py SceneName`. Copy the MP4 to `video/renders/bNN.mp4`.
- Review your own work. Take stills with `-s`, or pull frames with ffmpeg (`ffmpeg -ss T -i file.mp4 -frames:v 1 out.png`), and look at them. Check at least five moments per scene.
- Scene-only helpers stay in the scene file. Never edit `kit.py`; report anything the kit needs.
- **Privacy, in every frame:** block level at most. No request, work-order or parcel ids, no addresses, no personal names except public officials' titles.

## 1. The quality bar (3Blue1Brown)

- **Nothing pops.** Every element is written in (`Write`), drawn (`Create`), grown, or *becomes* something that was already on screen (`Transform`, `ReplacementTransform`). Cuts happen only between beats.
- **Continuity.** When the narration moves from one idea to the next, the old objects transform into the new ones, or the camera moves (`self.camera.frame.animate`), or they leave cleanly (fade with a small shift). Never a hard swap.
- **The screen answers the voice within half a second.** Nothing appears before its sentence starts (`self.until(i)`), and nothing a sentence names is missing when it ends.
- **One idea on screen at a time.** At most one line of text besides labels. Numbers count up (`Counter`). Dates are clocks or a timeline. Colours carry meaning (kit palette; never decorate with them).
- **Smooth.** Use `smooth` / `rate_functions.ease_in_out_cubic` by default and `rush_into` only for the stamp. Use LaggedStart for groups. Nothing static for more than about 4 s: if the voice is still talking about the same thing, drift the camera slowly, pulse the element in question with `Indicate`, or draw a highlight.
- **Breathing room.** Keep margins of at least 0.5 units. Text sizes: headline 56–64, body 34–40, labels 18–24.
- **Honest.** Every number on screen matches the script's figure table, and schematics are labelled "schematic".

## 2. The beats

Sentence numbers are the cue indices in `video/audio/cues.json` (scratch voice). Times are approximate.

### Beat 1 · The question (0:00–0:12) · `b01_question.py` · scene `B01Question`
- s0 "The City asked this hackathon a question…": a small label "City of St. Louis · Civic AI Hackathon challenge" writes in at the top. The question writes in at the centre as one serif sentence in two lines: *How can St. Louis better communicate how it's doing on city services?*
- s1 "I'm Jack Riddle.": the question shrinks and rises. "Jack Riddle" writes in below in muted serif.
- s2 "…what "done" means.": the word **"done"**, in quotes, splits out of the question (TransformFromCopy), grows to the centre in YELLOW, and the rest fades. Hold.
- End state: the word "done" alone at the centre, so beat 2 can open from it.

### Beat 2 · The promise, and five problems that are one (0:12–0:40) · `b02_issues.py` · `B02Issues`
- s0 "Every 311 request gets a completion date: a promise.": "done" shrinks into a PromiseCard at the centre ("311 request", kind "A REQUEST", due "due by its date"). Its ClockRing starts filling slowly (BLUE). The word "promise" writes under it.
- s1 "So I checked some.": the card slides left and shrinks. Two more card outlines draw beside it.
- s2 (tree): card 1 becomes "City tree · marked for removal". A timeline at the bottom marks "2 weeks" and "7 months". The ring overruns into GOLD. A row of 40 small squares: 1 GREEN, 39 GOLD. Label "1 of 40 by the request's date · typically 7 months after".
- s3 (city-owned lot): card 2 becomes "City-owned lot · overgrown". Four small parcel squares; one goes GREY-hollow with a "?". Label "1 report in 4: no cut on the city's mowing record".
- s4 "I expected separate problems.": the two cards and a third ghost card (cave-in) sit in a row with a gap between them.
- s5 "It's one: the city can't tell which of its promises it has kept.": the cards slide together and merge (Transform) into **one** PromiseCard at the centre. Its ring turns GREY with a "?" in the middle. The sentence writes in above, "kept" in YELLOW.
- s6 "And the fix is already in software it owns.": a small TEAL tag "Cityworks · already owned" fades in under the card.
- End state: one PromiseCard at the centre ("Overgrown lot", "WEEDS · VACANT LOT"), ring empty again, ready for beat 3.

### Beat 3 · How a promise works today (0:40–1:15) · `b03_today.py` · `B03Today` · HERO
The diagram here is rebuilt in beat 7, so build it in a way beat 7 can reconstruct (same positions, same objects; consider a module-level `build_diagram()` in `b03_today.py` that `b07_fix.py` imports).
- s1 "A resident reports an overgrown lot.": a small resident glyph (a simple circle head over a rounded body, drawn with Create) at the far left. A phone-call arc travels to a "311" box.
- s2 "311 gives it a date and routes it to Forestry.": the PromiseCard (from the centre) slides into place after "311". Its due date writes in ("due 30 Sep") and the ring starts (BLUE). An arrow draws to a "Forestry" box on the right.
- s3 "Often within minutes, someone closes it: 'on schedule to be cut.'": a small clock icon reads "13 min". The Stamp (CLOSED) slams onto the card with `stamp_in()`, the border turns RED, and the closing words write in under the card in italics: "on schedule to be cut".
- s4 "That's the hand-off.": a bracket labelled "the hand-off" draws under the step from the card to Forestry.
- s5 "The crew's record of the job is almost never attached.": a WorkOrderCard ("the crew's record", sub "route · ledger · work order") rises below Forestry. A dashed TEAL Connector grows from the request toward it, stops at 55%, and fades (`grow_to(0.55)` then FadeOut).
- s6 "In fifteen of the twenty most common hand-offs…": the camera eases right. A 4×5 grid of 20 small "status page" icons (rounded rectangles with three text lines) draws. 15 turn GREY with a small "nothing attached" mark; 5 stay lit (TEAL outline: tree removals, plantings, weeds rotation, cave-ins partly). Counter "15 of 20". Caption: "status pages of the 20 most common hand-offs, 800 pages read". The camera returns.
- s7 "So after the hand-off, nothing is waiting for the work.": the space between the request and the work order dims. A thin empty bracket labelled "nothing waiting" sits between them.
- s8 "The resident sees 'closed.'": a phone-sized status card ("Status: Closed") flies from the request back to the resident.
- s9 "On CityStat, a closed hand-off counts as on time.": a small CityStat bar at the top right ticks up by one segment, coloured RED (a hand-off counted as on time), labelled "CityStat: on time".
- s10 "If the crew never comes, nothing notices.": the work-order card fades to 30%. Hold the whole diagram.
- End state: the full "today" diagram. Beat 4 starts by pulling the CityStat bar to the centre.

### Beat 4 · The gap shows up twice (1:15–2:00) · `b04_gap.py` · `B04Gap` · HERO
- s1–s3 the scorecard: a large horizontal bar "Debris, alley or street · Apr–Jun 2026". Counter to **79%** (78.6). On s3 ("Count only closings that say it was picked up"), the bar splits into two segments: GREEN 15.0 ("closing says it was picked up") and RED 63.6 ("says it will be picked up later, or investigated"). The RED segment peels off and falls away, leaving **15**. Small caption: "CityStat's published share vs. the same requests counted by their closing words".
- s4 the trace: the bar becomes a field of 3,640 tiny squares (or 364 squares of 10, labelled). A sweep line (the promise date) passes. 18% turn GREEN before the line, 50% turn GOLD after it, and the mowing third stays GREY-hollow. Labels "done by the promise 18%", "late 50%", "mowing: a third no cut on record". Keep the labels short.
- s5 "Second, in the requests nobody closes.": the squares dissolve. The St. Louis map (`StlMap`) draws its ward outlines.
- s6 "14,902…": block dots fade in across the map with a LaggedStart, coloured by age (BLUE recent → GOLD → RED oldest), while a Counter ticks to **14,902**. Label "open, past the date the city gave · filed since Jan 2025".
- s7 "Three in four came from residents.": a small 4-square row, 3 lit. Label "3 in 4 filed by residents".
- s8–s9: the dots gather (Transform) into a Waffle of 100 squares at the right. 3 GREEN ("record shows it done, 3%"), 8 BLUE ("crew order still pending, 8%"), 2 MUTED ("later request closed, 2%"), 3 FAINT ("likely never-closed leftovers, 3%"), 84 GREY-hollow ("no record either way, 84%"). Write the 84% label last and largest.
- s10 "No one can tell those residents, or the mayor…": the 84 grey squares pulse once (Indicate). Hold.
- Data: `video/data/map.json`; figures in the script's table (78.6, 15.0, 3,640 / 18.0 / 49.8 / 32.2, 14,902, 75.8% resident-filed, 2.6 / 8.1 / 2.2 / 2.7 / 84.3).

### Beat 5 · One lot (2:00–2:23) · `b05_lot.py` · `B05Lot`
- s0: the map returns at full size. The camera zooms toward north-central St. Louis (Greater Ville, ward 12; use the ward-12 polygon's centroid; no address-level point). The ward outlines fade to a **block schematic**: a 6×7 grid of 37 parcel squares, labelled "schematic · one city block". One parcel is outlined in YELLOW ("city-owned lot, on Forestry's mowing list"). A small row of six tick marks reads "cut every year 2019–2024".
- s1 "Reported on 2 July: closed in thirteen minutes…": a timeline from July to October draws under the block. On 2 July a PromiseCard pops from the parcel, its ring starts, a "13 min" chip appears, the CLOSED stamp lands, and a due marker is set at 30 Sep.
- s2 "Reported again: closed in seven.": on 28 July a second card, a "7 min" chip, and the stamp again.
- s3 "Thirty-six other parcels on its city block were cut this year.": the timeline playhead sweeps July→October. The other 36 parcels turn GREEN in 15 waves (15 distinct cut days; the schematic's dates are illustrative, so label it "15 cut days, 2026"). A Counter reaches 36.
- s4 "This one has no cut on record.": the one parcel stays GREY-hollow. The playhead crosses 30 Sep and the due marker turns GOLD. Hold.
- End state: the block with one grey parcel and the two stamped cards.

### Beat 6 · The obvious fix (2:23–2:48) · `b06_obvious.py` · `B06Obvious`
- s0 "The obvious fix: stop closing requests early.": one PromiseCard at the centre with its CLOSED stamp. The stamp lifts off (reverse of `stamp_in`, up and out) and the border returns to BLUE.
- s1 "The city already plans that for towing…": a QuoteCard slides in from the right: *"Closed" does not necessarily indicate that a vehicle has been towed* (City of St. Louis, CityStat towing page, 2026). Below it, in smaller type: *"…only closed once a vehicle is actually towed."* Then it slides out.
- s2 "But look at the ones it already leaves open: 95 percent…": two bars (vacant-lot weed requests, 2026). "closed at the hand-off": 34.9% no cut on record. "left open": 95.4% no cut on record. Both grow, Counters attached; the open bar is the taller grey one.
- s3 "Keeping a request open with no job attached doesn't cut the lot either.": the open card's ring overruns, goes GOLD, then the card greys out. A small empty slot beside it shows where a work order would be.
- s4 "The request has to know about the job, and someone has to see the list.": two phrases write in, each with an icon. "know about the job" with a TEAL connector stub; "see the list" with three short list lines. These two become the first two parts of beat 7.

### Beat 7 · The fix, and the lot replayed (2:48–3:47) · `b07_fix.py` · `B07Fix` · HERO
- s0 "So, three changes…": the beat-3 diagram rebuilds quickly (import `build_diagram` from b03), in the same positions, without the stamp.
- s1 "Link…": the WorkOrderCard sits below Forestry. The Connector grows **solid** TEAL all the way (`make_solid()`, `grow_to(1.0)`). The CLOSED stamp hovers over the request, then fades without landing. A label "1 · Link" writes in at the top left.
- s2 "Cityworks' documentation says…": the work order gets a GREEN check (the crew finishes). A GREEN pulse travels back along the connector, and the request closes by itself: border GREEN, ring complete. A small TEAL tag "Cityworks 23: built in (vendor docs)".
- s3 "List: every week, each division sees every request past its date…": the camera pulls back. The request card multiplies into a column of overdue cards, sorted oldest first, under a header "Forestry · this week". A tiny map thumbnail at its side shows a few dots. Label "2 · List".
- s4 "Count: CityStat adds one column, done by the promise.": the CityStat bar from beat 3 returns with a second column beside it ("done by the promise"), GREEN. Label "3 · Count".
- s5 "The column fixes the scorecard; the link tells done from waiting; the list puts…": a three-row table writes in, one row per clause: *scorecard → Count*, *done or waiting? → Link*, *broken promises seen → List*. This is the bridge; keep it big and slow.
- s6–s13 the replay: the table moves aside. The beat-5 block returns with its July–October timeline.
  - s7 "2 July": the card is filed, a work-order card attaches with a solid connector, no stamp, ring BLUE.
  - s8 "The second call lands on that open job.": the 28 July call merges into the same card (a "×2" chip). The 9 September call is left out, as in the script.
  - s9 "1 October…": the playhead passes 30 Sep, the ring goes GOLD, and the card flies into a "Forestry · past its date" list, which highlights it.
  - s10–s11: a phone-sized resident page writes in: "With Forestry since 2 July · Due 30 September".
  - s12 "Whether the crew comes sooner is up to the crew.": the parcel stays grey, honestly.
  - s13 "But the lot can't disappear.": the card's highlight holds; the frame pulls back to the whole list.

### Beat 8 · What I built (3:47–4:18) · `b08_product.py` · `B08Product`
- s0 "I built this on the city's own data: Forestry's list, CityStat with the column, a resident's page…": three ScreenCards enter one at a time from the right in a gentle arc, with the camera panning across them. Use the reshaped site's shots in `build/E6/shots/` (02-queue-forestry, 03-citystat, 04/05-status); until they exist, use `build/E3/shots/01-queue.png`, `04-scoreboard.png`, `02-status.png`. Keep the image paths in one dict at the top of the file.
- s1 "Simple versions… run today on public data; the link makes them exact.": two of the three cards get a small GREEN badge "runs today"; the status card gets a TEAL badge "needs the link".
- s2 "I'm handing over the package…": the cards shrink to a row. Four boxes appear below: "Cityworks", "Geoportal (ArcGIS)", "CityStat", "Divisions". Four file glyphs drop into them: "saved search" → Cityworks, "dashboard" → Geoportal, "SQL" → CityStat, "1-page practice" → Divisions.
- s3 "AI agents did the audit…": a small Counter "1,440 status pages read" and the Forestry commissioner's words as a small QuoteCard: *"…we don't have somebody on staff that's just designated to kind of analyze all that data"* (Forestry Commissioner, Budget & Public Employees Committee, 6 May 2026).
- s4–s5 "What the city runs is plain SQL. Nothing to buy.": a three-line SQL snippet writes in in monospace, then "$0 new software" in GREEN.

### Beat 9 · The ask (4:18–4:31) · `b09_ask.py` · `B09Ask`
- s0: three PromiseCards in a row: "Tree removals", "Cave-ins", "Vacant-lot mowing". Above them, "one quarter".
- s1: three verbs write in under them: "attach · work the list · publish the column".
- s2 "Then re-run it against today's baseline.": the 14,902 Counter returns, freezes, and gets a date stamp: "baseline · 13 Oct 2026".
- s3 "You'll know which promises you kept.": everything fades except the question. It writes in big: *Which promises did St. Louis keep?*, "kept" in YELLOW.
- End card (after the audio, about 4 s): the name placeholder "[NAME]". Then "Jack Riddle · Civic AI Hackathon · St. Louis, October 2026", "repository: [link]", and the line "Built from the City's open data and Cityworks saved searches read with the City's permission (operational fields only; no personal data). Not a City website." Then fade to black.

## 3. Assembly

`video/tools/assemble.py vN` normalises each render, joins neighbours with a 0.5 s dissolve and audio crossfade, and writes a 1080p cut plus a 720p phone copy. Each beat WAV starts with 0.8 s of silence (the lead-in that makes the joins possible). The older `video/tools/assemble.sh` concatenates `video/renders/b01.mp4 … b09.mp4` into `video/out/roughcut-vN.mp4`. Each scene carries its own narration, so assembly is a plain concat with an audio check. The scratch voice is macOS Samantha (`video/tools/narrate.py`). Jack's take replaces it: split by beat, rebuild `cues.json`, re-render.

## 4. What is built first, and by whom (14 Oct evening)

| Scene | Owner | Why first |
|---|---|---|
| kit, narration, cues, map data, assembly | orchestrator | everything depends on them |
| b03 + b07 (the diagram, today and fixed, and the replay) | subagent V-A | the heart of the argument; survives any script edit |
| b04 + b05 (scorecard, trace, map, waffle, the block) | subagent V-B | the most data-driven visuals; survive edits |
| b01 + b02 + b06 (question, issues, obvious fix) | subagent V-C | short; the most likely to change with feedback |
| b08 + b09 (product cards, package, ask, end card) | subagent V-D | waits on the site's new shots; built with placeholders now |
