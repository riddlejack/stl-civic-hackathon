# Video beats v7: the build plan

Written Thu 15 Oct 2026, about 12:25 p.m. Central, by the orchestrating thread. The script is `deliverable/video-script-v7.md` (14 beats, locked; Jack is recording it now). Its "Screen notes for builders" table says what each beat must show; this file says who builds it, from what, and how.

## State at hand-off (observed)

- **Scratch narration** for v7 is in `video/audio/beat_01.wav` … `beat_14.wav` and `video/audio/cues.json` (14 keys `b01`–`b14`, 344 s of audio). It was made by `video/tools/narrate.py`, which now reads the v7 script.
- **v6 is archived:**
  - scenes in `video/scenes/v6/`;
  - renders in `video/renders/v6/`;
  - audio, cues and `joins-v6.json` in `video/audio/v6/`.
- **v5 scenes** are in `video/scenes/v5/`, including the North Taylor replay `b13_replay.py`.
- **Shared helpers stay in `video/scenes/`:** `kit.py`, `illus.py`, `basemap.py`, `nt_common.py`, `shared_block.py` and `_v*_shared.py`. A v6 scene copied back into `video/scenes/` imports them unchanged.
- **`video/joins.json`** is reset for 14 beats. Beats 04, 05 and 11 are footage beats and 14 is the end card, so they set their own length; the others cap the hold after the voice at 2.5–3 s.
- **Jack's recordings** will arrive in `video/audio/jack/`. `video/tools/cues_from_recording.py` then rewrites the WAVs and cues. Every scene must stay cue-driven (no absolute times), so it re-times by itself.

## Naming rules for v7 (new)

- **Manim beats:**
  - each is `video/scenes/bNN_<name>.py` with `class BNN<Name>(CueScene)`, where NN is the **v7** beat number;
  - each reads cues key `bNN` and is rendered by `video/tools/render_all.sh` to `video/renders/bNN.mp4`.
- **Footage beats (04, 05, 11):**
  - a tool, `video/tools/make_bNN.py`, writes `video/renders/bNN.mp4`;
  - any Manim overlay it renders lives in a file **not** matching `b[0-9][0-9]_*.py`, for example `video/scenes/x05_bar.py`, so that `render_all.sh` doesn't render it as a beat and overwrite the footage.
  - Run the tools *after* `render_all.sh`.
- **Copying is fine; editing is not.**
  - Copy from `video/scenes/v6/`, `v5/` or `video/tools/` and adapt.
  - Never edit another builder's files, `kit.py`, the shared helpers, `make_demo_beat.py`, `render_all.sh`, `assemble.py`, `narrate.py`, `cues_from_recording.py` or `video/joins.json`.
  - If a shared helper needs a change, copy it into your own file and say so in your report.

## Beats, sources and builders

| v7 | Beat | Start from | Builder |
|---|---|---|---|
| 01 | The finding (six tiles, audit scale) | `v6/b01_sweep.py` | A |
| 02 | Committee quote card | new; the quote card style from `v6/b13_already.py` | A |
| 03 | Three dates, with the archived definition | `v6/b08_breaks.py` | A |
| 14 | Close and end card (no name, no link) | `v6/b15_end.py` | A |
| 04 | Two quotes on one screen: towing page footage plus the 311 acting director card; then 61,845 | `video/renders/city_towing_raw.mp4` (+ `city_towing_events.json`), the approach of `video/tools/make_b04.py` | B |
| 05 | CityStat footage, then the three-way bar (15 / 45 / 18) | `video/tools/make_b04.py` and `v6/b04_citystat.py` | B |
| 06 | North Taylor: two reports, closed in 13 and 7 minutes, block cut around it | `v6/b10_twins.py`, `v5/b13_replay.py`, `nt_common.py` | C |
| 07 | Twin lot, 28%, CityStat quote card, 15 of 20 tiles | `v6/b10_twins.py` (tail), `v6/b09_tiles.py` | C |
| 08 | 14,902 map recoloured 3 / 8 / 84; the 2,778 life-safety subset | `v6/b03_pile.py`, `v6/b11_impact.py` (counter 1) | C |
| 09 | One cause, four requirements; alternatives on the same broken loop | `v6/b05_fix.py`, `v6/b12_alternatives.py` | D |
| 10 | Already done: Forestry, Cityworks, Chicago/Houston/Toronto | `v6/b13_already.py` | D |
| 12 | What changes: three lines, the estimate with its assumptions | new, in the `v6/b11_impact.py` counter style | D |
| 13 | The test: three baselines, what working looks like, three "no"s, hand-over | `v6/b14_handover.py`, `v6/b07_landing.py`, `build/E8/baselines.json` | D |
| 11 | Product demo in four segments, each opened by its problem line; site name placeholder removed first | `video/tools/make_demo6.py`, `record_demo.py`, `site/` | E |

## Rules carried forward, and the v7 additions

**Carried forward:**
- everything in `video/BRIEF-COMMON.md`;
- the Rules section of `deliverable/VIDEO-BEATS-v5.md`;
- `video/KIT-v2.md`;
- `video/review/DOCTRINE-for-video.md`;
- the fixes in `video/review/QA-v3.md` where they still apply.

**New in v7:**
1. **Each beat's on-screen action title is in the script's "Action titles" table.** Every number on screen must match the script's figure table. Respect the "Not said, deliberately" list on screen too.
2. **Reading time.**
   - Use `say_and_hold()` / `hold_for()` for every frame with text.
   - Do **not** stretch or edit the narration.
   - If the hold report prints `OVERRUN`, leave it. The orchestrator adds the pause to the narration at assembly (a padding tool) and re-renders.
   - List the overruns in your report.
3. **Privacy.** Public officials by title only on screen. The beat 4 director card reads "Acting Director, Neighborhood Stabilization Division (home of the Citizens' Service Bureau, 311) · Board of Aldermen budget hearing, 12 May 2026".
4. **No product name and no repository link anywhere** (Jack, 15 Oct). Where v6 showed "[NAME]", show nothing or the tagline "Which promises did St. Louis keep?".
5. **Pace.** Jack found the v3.1 holds slightly slow, so keep holds after the voice tight.
6. **Done means rendered and looked at.**
   - Render the final at 1080p30.
   - Check at least 5 stills per beat plus the last frame with the Read tool.
   - Confirm the duration against the cue.
   - Report in under 250 words (the format in BRIEF-COMMON).

## Orchestrator's own work (this thread)

- the padding tool for reading-time overruns;
- `video/joins.json`;
- the assembly (`video/tools/assemble.py v5`);
- one QA pass;
- the swap to Jack's voice;
- the final cut.
