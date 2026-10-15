# Video beats v6: the screen plan

Written 15 Oct 2026, about 12:20 a.m. Central, from `research/brainstorm-v6.md` (approved by the orchestrator under Jack's instruction to approve its ideas) and `deliverable/video-script-v6.md`. Fifteen beats, about 4:15. **The pitch is complete by 2:00:** the finding, the scale of the audit, the city's own page, the fix, the product running, and the ask. The second half is the evidence and the case.

v5 scenes and renders are archived in `video/scenes/v5/` and `video/renders/v5/`. Reuse them heavily. Every rule in `deliverable/VIDEO-BEATS-v5.md` §"Rules" still applies:
- action titles;
- reading time;
- Charter only;
- plain words with a source line;
- still first 0.5 s and last 0.6 s;
- illustrations, not placeholders;
- honest numbers.

**New in v6:**
- **Pace.** Jack found v3.1 slightly slow. Keep holds after the voice to the minimum the rule allows: about 2 s, or 3 s for dense frames.
- **Real footage.** Where it exists, show the real thing (the site, the city's CityStat page) instead of a drawing.

| # | Scene file / class | Reuses | Picture |
|---|---|---|---|
| 1 | `b01_sweep.py` B01Sweep | v5 b01 vignettes | **New.** Six tiles land one per service as named: tree removal, sidewalks, vacant-lot mowing, board-ups, towing, alley debris. Each has an illustration and one observed symptom (see the brainstorm, idea 1, for the figures; label each with its population). Under the tiles, the audit's scale counts up with `Counter`: "1,454,222 requests · 2,252,031 Forestry billing records · 29,018 work orders · 1,440 status pages · 11 cities compared" (`research/credibility-tally.md`). On "I found one", a single line draws through all six tiles. |
| 2 | `b02_thesis.py` B02Thesis | v5 b02 | The title card with the v6 thesis text. |
| 3 | `b03_pile.py` B03Pile | v5 b09 (plus the b03 counter) | The basemap: a counter to 14,902, the dots in waves by service, then recoloured (done 3%, work order pending 8%, no record 84%). The other two classes appear as small legend rows. |
| 4 | `b04_citystat.py` B04CityStat | v5 b04 | **New footage.** The live CityStat page recording (video/renders/city_citystat_raw.mp4), framed as a rounded window and held on 78.6%. Then cross-fade to the 79 → 15 bar. Title: "CityStat grades the hand-off, not the work". |
| 5 | `b05_fix.py` B05Fix | v5 b05 + b12 | The request card tied to the job card; the three verbs light up: link the job · flag the misses · count the finish. About 12 s. |
| 6 | `b06_product.py` (or tool) | v5 b15 tool | **Re-shot demo** (demo6_raw / demo6_zoom): ranked list and why-this-rank; a block; the resident page today vs with the link; the CityStat column; the data page. Cut it to the beat's sentences with `video/tools/make_demo_beat.py`, adapted. About 35–40 s. |
| 7 | `b07_landing.py` B07Landing | new | A card with three "no"s (no new software · no app for residents to adopt · no city data leaving the city) and the ask in one line ("one quarter · three request types"). Title: "Nothing to buy. One quarter to prove it." |
| 8 | `b08_breaks.py` B08Breaks | v5 b06 + b07 | One timeline: filed, promised, done (keep the promised tick visible). Closed at about day 2 with the hand-off bracket; recorded work at about 5 weeks. |
| 9 | `b09_tiles.py` B09Tiles | v5 b08 | The 20 tiles, retitled: "For 15 of the 20 most common hand-offs, no status page showed anything attached". |
| 10 | `b10_twins.py` B10Twins | v5 b10 | The twin lots, trimmed to about 22 s. The 28% line is now spoken; keep it on screen as said. |
| 11 | `b11_impact.py` B11Impact | new | **Impact: what the weekly list would surface.** Three counters land one per sentence, each with its population, date and source line. (1) **2,778** life-safety requests past the city's date, median 239 days, shown with tree-down, cave-in and water illustrations. (2) **1,630 of 2,504** open tree-removal work orders past the finish date Forestry itself set, median 618 days (authorised Cityworks extract, 14 Oct). (3) **52** city-owned lots told "on schedule" with no cut on record this year, with "about $7,000 to cut them for a season (estimate: $132 median billed rate)". Close on "the jobs a weekly list puts in front of someone": the three counters slide into a "Forestry · this week" list frame. Figures: `research/impact-quantification.md` H1–H3 and its facts CSV. Title as in script v6. |
| 12 | `b12_alternatives.py` B12Alternatives | new | **Why not the alternatives.** Five slim columns: hotspot map · chatbot · resident app · new vendor system · sending data to an AI model maker. Each has a small illustration and one line: what it needs, and that it sits on the same broken loop. A sixth, highlighted column, "this fix": "a field the city already has · a rule the city already wrote · no resident adoption · no data leaves the city". Fair, not straw men: each alternative is labelled "useful after the loop closes". |
| 13 | `b13_already.py` B13Already | v5 b11/b16 quote cards | **Already true.** Four checkmarks land one per sentence:<br>• Forestry links tree-removal work orders (40 of 40);<br>• Cityworks 23 closes a linked request when the job closes (vendor docs);<br>• the city already promised this rule for towing (quote card);<br>• the mayor's transition committee asked for this audit (quote card).<br>Footer: "Chicago, Houston and Toronto have written the same rule." |
| 14 | `b14_handover.py` B14Handover | v5 b16 + b17 | Package glyphs into the city's systems, plus the ask with three per-type baselines (open past the date, 13 Oct 2026). Owners line. |
| 15 | `b15_end.py` B15End | v5 b18 | The closing line, then the end card. |

**Builders:**

| Builder | Beats |
|---|---|
| A | 1, 2, 7, 15: opening, thesis, landing card, end |
| B | 5, 8, 9: fix, timeline, tiles |
| C | 3, 10: map, twins |
| D | 4, 6, 14: CityStat footage, demo, hand-over |
| E | 11, 12, 13: impact, alternatives, already true |
