# Status: night of Wednesday 14 October (written about 8:25 p.m. Central)

## Summary

Rough cut v2 exists: **`video/out/roughcut-v2.mp4`** (1080p, 4:31) and a 720p copy (`roughcut-v2-720p.mp4`, 12 MB). All nine beats were built in Manim from script v4, voiced by the Mac's scratch voice and timed to it sentence by sentence. An editor pass (`video/review/QA-v1.md`) was applied, and the beats join on matched frames. The site is rebuilt as five quiet screens, and its shots appear in beat 8. Your real narration drops in with three commands (`video/README.md`). Nothing is committed.

What I could not settle, because it is yours: the length, the name, the repository link, the human check of three closing phrases, the authorisation note, and the email to Mike.

## What changed tonight, and why

- **The root cause was checked before anything was built.** The 14,902 is a correct count of what the city's records say, not a misreading. Fewer than 3% of those requests have any record of the work being done, and 84% have no record either way (`research/open-queue-reality-check.md`). So the film says "the city can't tell which promises it kept", and never "residents waiting".
- **The figures were checked twice more.**
  - An independent fact-check of script v4 found 2 wrong and 8 misleading lines, all fixed (table in the script).
  - The AI-drafted closing-word classes behind "79 becomes 15" were reviewed. 15.0% holds under every reading, but only as worded: closings that *say* it was picked up (`research/closure-class-review.md`).
- **The "no AI" rule is narrower than we thought.** City IT policy #2026-001 bans AI tools the IT department hasn't approved; it doesn't ban AI. The film now says AI agents did the audit and the city runs plain SQL.
- **The North Taylor replay is corrected.** The lot's date was 30 September, not 16 July. The replay shows it reported twice (×2), and leaves out the 9 September cut complaint.
- **The site's CityStat column was relabelled.** It is now "Closing says done", because the current numbers grade closing words, not the promise date.

## Decisions for you, in order

1. **Length.** The cut runs 4:31 at the scratch voice's pace; your own pace may differ. That is over the 2:30–4:00 you set, and well over the event's "2-minute" line. The cut map at the end of `deliverable/video-script-v4.md` trims it in steps. My recommendation is items 1–4, which bring it under about 4:00 and lose nothing structural.
2. **Name.** It appears only on the end card and the site header, as "[NAME]". My pick is **Kept** ("Which promises did St. Louis keep?").
3. **Record the narration.** Record one file per beat, read the "Read-aloud" text exactly, and leave a clear half-second pause between sentences. Save the files to `video/audio/jack/`. Then run:

   ```bash
   video/.venv/bin/python video/tools/cues_from_recording.py
   ```

   ```bash
   video/tools/render_all.sh
   ```

   ```bash
   video/.venv/bin/python video/tools/assemble.py v3
   ```

   A beat that prints a warning should be re-recorded.
4. **Check three closing phrases by hand** (about 10 minutes), because the "15%" rests on them: "bulk will be picked up in correct week", "matter will be investigated", and enforcement notices (`research/closure-class-review.md`).
5. **Repository.** Choose GitHub or Dropbox. Its link replaces "[link]" on the end card and the site's "Read the full case". `scripts/exec/E4/export_public.sh` builds the clean copy (0 hits in 351 files tonight).
6. Fill in the authorisation note's blanks (`context/AUTHORISATION-NOTE.md`), and send the Dropbox email to Mike if you haven't.

## Known weak spots in the cut

- Beat 7's opening, where the two phrases turn into the "Link / List / Count" labels, is busy for about half a second.
- The screenshots in beat 8 still show "[NAME] PROTOTYPE" in the site header, until the name is chosen and the site is re-shot.
- The "×2" call chip and the list rows in beat 7 are schematic, and labelled as such.

## Where things are

- **Script:** `deliverable/video-script-v4.md`.
- **Screen plan:** `deliverable/VIDEO-BEATS.md`.
- **Scenes:** `video/scenes/` (shared kit `kit.py`).
- **Renders:** `video/renders/`.
- **Cuts:** `video/out/`.
- **Editor's notes:** `video/review/QA-v1.md`.
- **Site:** `site/`, served by `scripts/night/N6/serve.py`. Shots are in `build/E6/shots/`, the chapter in `research/chapters/E6-site.md`.

---

## Late-night update (11:27 p.m.): v5 rebuilt; rough cut v3

**What exists:**
- **Script:** v5 is locked (`deliverable/video-script-v5.md`; 18 beats, top-down).
- **Cut:** `video/out/roughcut-v3.mp4` (5:23, scratch voice). The editor's fixes are going into v3.1.
- **Ranked view:** live on the site, with the Close-out list and "why this rank" on every row. Forestry's top 25 goes from 9 life-safety items to 25.
- **Demo:** being re-recorded with the North Taylor page corrected.
- **Editor's review:** `video/review/QA-v3.md`.

**Decisions waiting for Jack (in this order):**
1. **Name.** "[NAME]" is on the end card and the site header; my pick is "Kept".
2. **Repository link** for the end card.
3. **Length.** v3.1 will run about 5:15. The editor's 40-second cut list (QA-v3.md) gets to about 4:40, but it drops things Jack asked for, so it is his call:
   - the towing-quote beat;
   - the map's 3% and 8% readouts;
   - the closing line of the ranking beat;
   - a few sentence trims.

   The editor also notes that a judge who stops at 2:00 never reaches the demo or the ask.
4. **Record the narration.** Use the read-aloud in script v5, one file per beat (18 files), and follow `video/README.md`. The scenes re-time themselves.

---

## Overnight (12:45 a.m., Thu 15 Oct): v6 and rough cut v4

**What happened.** Jack found v3.1 polished but not compelling: no wow, no credibility, no quantified impact, no case against the alternatives, too little of the real tool.
- A fresh-eyes brainstorm (`research/brainstorm-v6.md`) and an impact pass (`research/impact-quantification.md`) were approved into **script v6** (`deliverable/video-script-v6.md`; 15 beats).
- Five builders rebuilt the scenes, and the site session recorded the live CityStat page and a new demo.
- **Rough cut v4:** `video/out/roughcut-v4.mp4` (5:07, scratch voice). The pitch is complete by about 2:15, in this order: audit sweep → thesis → 14,902 on the map → the live CityStat page → the fix → the product running → "nothing to buy".

**Impact numbers on screen:**
- 2,778 life-safety requests past the city's date (median 239 days);
- 1,630 of 2,504 open tree-removal work orders past Forestry's own finish date (median 618 days);
- 52 city-owned lots told "on schedule" with no cut on record (about $7,000 to cut them for a season, estimate);
- set-up about 150 staff hours with no new licence, against Fresno's roughly $1M 311 system.

**Dropped because they didn't hold up:** repeat-request savings (only about 176 durable repeats) and labour saved by auto-closing.

**Morning, in order:**
1. **Watch v4.**
2. **Decide the name and the repository link.** They replace "[NAME]" and "[link]".
3. **Record the narration.** One file per beat (15) from the script v6 read-aloud, saved to `video/audio/jack/`. Then run:

   ```bash
   python3 video/tools/cues_from_recording.py
   ```

   ```bash
   video/tools/render_all.sh
   ```

   ```bash
   video/.venv/bin/python video/tools/make_demo6.py
   ```

   ```bash
   video/.venv/bin/python video/tools/make_b04.py
   ```

   ```bash
   video/.venv/bin/python video/tools/assemble.py v5
   ```

   b04 and b06 are footage beats built by their tools, not Manim scenes.
4. **Check three closing phrases by hand** (`research/closure-class-review.md`).
5. **Publish the repository** with `scripts/exec/E4/export_public.sh`, then upload and submit by about 3 p.m.

Nothing is committed.
