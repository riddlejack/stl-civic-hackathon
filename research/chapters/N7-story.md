# N7. The story: video script, progress report, README, questions, names, risks

Written 14 Oct 2026, 12:05–12:35 a.m. Central; revised 1:05–1:20 a.m. after N8's check. Outputs are in `deliverable/`; the decision log is `research/chapters/N7-decisions.json` (18 entries, for N9 to merge). No code was written for the product. Two throwaway checkers sit in the session scratchpad: a word counter and a script that resolves every `{{fig:...}}` tag.

## Revision after N8 (1:05–1:20 a.m.)

I applied every N8 finding that touches the files N7 owns (`research/chapters/N8-verification.md`):

- **Finding 1, the September call.** Storyboard A now names lot-1's 9 September "cut incomplete" call: "A September call says the cut was incomplete; closed in a day. … This lot: none. If a crew came, no record shows it." B and C and the README say the same. Every line keeps "no cut billed".
- **Finding 2, one in five.** "One in four" became "one in five", tagged `n1_weeds_lot_onschedule_only_no_cut_2026` (0.214, registered at 01:05). The non-existent 25% strip is gone from shot 4. In the README, vacant buildings now cite `n1_weeds_bldg_onschedule_only_no_cut_2026` (32.2%), and the 30-day vacant-lot figure was dropped.
- **Finding 3, the disclosure.** The README line reads "[JACK: update once sent] A private note about exposed data is being raised with the city through the organiser."
- **Finding 4, the repository.** A publish warning sits in the README's top comment, the end-card placeholder and risks.md. The Monday list path now points to `site/data/downloads/`.
- **Finding 6, Cityworks.** The progress report, README and Ben note now say what the register says: Cityworks would add trees, tree planting, potholes, cave-ins and street lights, taking coverage from 4 of 25 to about 9; the rest need other division records.
- **Finding 7, the tornado.** "Since the tornado" is added wherever no gap in finished work is claimed: script A and C, README, progress report, risks.
- **Finding 8, length.** Narration A is cut to 264 words (about 1:46 at 150 a minute). B is 259 and C is 267.
- **Finding 10, ledger rows.** B now speaks parcels (11,971), not ledger rows.
- **Finding 15:**
  - (a) "this city block";
  - (b) "we found no sign that residents stop using 311";
  - (c) the 0.9% is labelled January 2024 to June 2026;
  - (d) "without a billed cut (counting to 30 September)";
  - (e) "14 for most vacant-lot requests", with the 90-day answer in risks;
  - (f) the build-seconds bracket updated;
  - (†) the ten-texts review wording.
- **The towing promise share** is recorded as settled at 32% vs 4% in the script and risks. It is not spoken.
- **Lot-1 tags** now point to N5's registered `n5_lot1_*` ids.
- **N5 and N8 disagree** on how many "cut incomplete" calls hit lots with no cut all year (40 against 61). Neither is quoted aloud.
- **Tag check.** All 127 real tags resolve against the 01:05 build.

Not mine, and still open on the site: findings 3 (site wording), 5 ("reviewed"), 7 (the label on the no-gap table), 9 (garbled methods text), 10 (lot-1's 2019 history), and 11–14.

## Admission

**Did.**
- Wrote six deliverables: a recommended two-minute storyboard (A: the receipt, then fairness; 285 words at first, 264 after N8) with two full alternatives (B: mowing throughout; C: numbers first), a comparison table and a criteria table; the progress report (287 words); the README; the note of questions to Ben; names with a clash check; and risks.
- Tagged every number `{{fig:id}} [value]`. All 112 tags resolve against `build/out/figures.json` (built 00:08; values unchanged on the 00:09 re-run).
- Checked the storyboard against N6's first test captures (12:13–12:15 a.m.) and rewrote the screen lines to match what renders.
- Ran the de-slopify pass by hand on the script and README. Among other fixes, it removed "not just", "it's not one lot" and "the point is", and replaced an absolute thesis line with "often".

**Did not.**
- Did not recompute any figure; that is N8's job.
- Did not check the Monday brief's own numbers (its week-on-week table). It and the methods page rendered in N6's captures at 12:19–12:20 a.m., and the storyboard describes them from those captures.
- Sent, published and contacted nothing. The progress report, the questions to Ben and the disclosure line are Jack's to send.

**Could not establish.**
- Whether the 285-word read fits 1:56 at a natural pace. Untimed; the script names two cuts if it runs long.
- Whether the names clash as trademarks. Only web searches were run.

**Placeholders, all marked in the files:**
- the public repository URL;
- the MIT licence and LICENSE file;
- the README's private-disclosure line, to delete unless Jack sends the note;
- two screens storyboard B needs that the site lacks (a funnel graphic and a mowing-retrospective view).

## Corrections applied to the brief's default shape

- "The city's ward chart measures paperwork" is withdrawn (COMMON 2). The script says the gap is in the first step instead.
- "One in four lots" is a share of requests (n = 808), so it is worded that way.
- "No new software" became "nothing to buy", because the pipeline is software.
- The tree story uses N5's revised pattern (288 requests filed at open removal orders, median 575 days). It never says "converted".
- Q3 potholes are framed as timing, not collapse (COMMON 8). The site's own chart shows several 2024 quarters below 30%, which is a reason to keep it that way.
- Towing uses medians only (the promise share is disputed).
- Single light out appears nowhere. No request, work-order or parcel ids appear (COMMON 10).

## Figures the story rests on (all observed, `build/out/figures.json`)

| Figure | Value | Where |
|---|---|---|
| `n2_share_closed_handoff` of `n2_closed_requests` | 35.2% of 175,876 | A, B, C, README, progress |
| `n4_sb_kept_all` / `n4_sb_done_kept_all` | 57.8% / 19.5% | C, README, progress |
| `n1_weeds_lot_onschedule_only_no_cut_2026` (replaced the mixed `n1_weeds_lot_onschedule_ledger`, 0.2475) | 0.214 of 729 requests | A, README |
| `n3_towing_tagged_median_after` | 12.0 vs 36.9 median days | A, C, README, progress |
| `n3_no_gap_done_types_after` | potholes 6.9 vs 8.0; refuse 1.7 vs 1.8; whole-block lights 0.7 vs 0.7 | A, README |
| `n3_decomp_ward1_vs_10_*` | mix 0.43 + words 1.51 of 15.7 days (12%) | A on-screen, README |
| `n4_q3_2026_pothole_residential` / `n4_q2_2026_pothole_residential_ours` | 24.3% / 84.4% | A, C, README |
| `n2_register_services_with_record` | 4 of 25 | A, B, C, README, progress |
| `n5_tree_cancel_blank_wo_predates`, `n5_tree_predating_wo_median_age_days` | 288; 575 days | C, README, Ben note |
| lot-1 facts (`n5_lot1_*`) and the 9 Sep call (`heroes.json`) | 13 and 7 minutes; 0 cuts billed; 36 other parcels cut on 15 days; promise 30 Sep; a "cut incomplete" call closed in a day | A, B, C |

## Flags for the orchestrator and N8

1. **Hero numbers.** Now registered by N5 as `n5_lot1_*` (resolved 1 a.m.). The counter-example's dates and the September call remain cited from `heroes.json`.
2. **Three README counts come from `build/N2/register.json`**, not the figure registry: lead inspections open (288 of 388), sirens (224 of 232) and tornado debris (368 of 458). They are tagged `{{reg:...}}`. Register them or drop them before publishing.
3. **The site says counts are reproduced "for 8 of 9 measures"** (scoreboard card). No registered figure backs the exact-count claim: `n4_repro_metrics_within5pp_C` is about shares within five points. The scripts use only "76 of 81" from that figure's note.
4. **`deliverable/choices.md` has one remaining overstatement** (Method section, `method-like-for-like`): raw times "made the cave-in gap look sixteen times bigger than it is". The like-for-like cave-in comparison is a referral gap, and the repair gap is unproven, so "bigger than it is" has no measured "is". N9 fixed the top-ten item and the negative-results entry at 00:17.
5. **"The north doesn't wait longer for crews"** holds for the high-volume finished-work types. Cave-in "work completed" (8.3 vs 23.1 days, n = 35 in wards 1–5) is the exception a critic will find. `risks.md` carries the answer.
6. **Lot-1 drew an "Unsatisfy Cut - VLot" request on 9 Sep 2026**, closed "supervisor notified". Every script line therefore says "no cut billed".

## What surprised me

- The site matched the planned story closely: three doors (residents, city staff, CityStat team), "A weekly run would have shown this in July", and the fairness headline in N3's words. The storyboard needed only screen-line edits.
- The cleanest single picture of the thesis, closed by the promise against done by it (57.8% and 19.5%), is not on the landing page. It is the lead of storyboard C, and it could also sit beside the 35% if Jack picks A.
