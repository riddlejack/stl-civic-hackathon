# Video script v2: the three-surface demo (spine, with figure slots)

Drafted 14 Oct 2026, about 3:30 p.m. Central, by the orchestrating thread from `context/PITCH-ARCHITECTURE.md`, while E1–E3 run. Supersedes storyboards A, B and C in `video-script.md`. Screens are named by surface; E3's captures fill them in. Every spoken number carries a slot `{{fig:…}}`; the integration pass resolves each against `site/data/figures.json` and no number is spoken without a registered figure behind it. Target: about 250 words, under 1:52 spoken, two minutes with the end card.

**Spine:** his number → one block → the page that stops and the page that doesn't → the size of it → the queue → the column and the status → four rules and one ask.

## Shots

**1 · 0:00–0:12 · His number.** *Screen:* CityStat's alley-debris measure as published, then our scoreboard row with the added column. *Narration:* "St. Louis grades its services on CityStat. Alley debris: 79 percent cleaned on time. Count only the closings that say the work was done: 15. The measure counts the hand-off, not the job." *Slots:* `{{fig:citystat_debris_published_q2_2026}}` [78.6%], `{{fig:citystat_debris_done_only_q2_2026}}` [15.0%] (R1 restated table; E3 registers as `e3_citystat_debris_*` if no id exists).

**2 · 0:12–0:30 · One block.** *Screen:* the receipt for the lot, timeline scrolling. *Narration:* "July 2nd: weeds on a city-owned lot, 1700 block of North Taylor. Closed in thirteen minutes: 'on schedule to be cut.' July 28th, again. Forestry's ledger bills cuts on 36 other parcels on this block this year. This lot: none." *Slots:* `{{fig:n5_lot1_minutes_to_close_jul02}}` [13], `{{fig:n5_lot1_block_other_parcels_cut_2026}}` [36], `{{fig:n5_lot1_cuts_billed_2026}}` [0].

**3 · 0:30–0:50 · The page that stops, and the page that doesn't.** *Screen:* the reconstructed public status page, cave-in: "Closed · Referred to street maintenance · nothing attached." Then the tree page: "Related items: 3 work orders attached," with dates. *Narration:* "Here is what a resident sees for a cave-in: closed, referred, nothing attached. Same page, a tree request: work orders attached, with dates. Where a division attaches the job, the page can show it. But the request was closed by hand the day it was filed, so even here, closed came first." *Slots (E1 final, 3:58 p.m., `build/E1/figures.json`):* tree removal `{{fig:e1_linked_svc_h_tree}}` [40 of 40 with a work order; 1 of 40 done by the 14-day promise; 39 late, median 211 days]; referred cave-ins `{{fig:e1_linked_svc_h18}}` [16 of 40; 4 of 16 by the 3-day promise; late median 9 days]; pooled hand-offs `{{fig:e1_handoff_share_with_work_order}}` [50 of 800, 6.2%]; `{{fig:e1_handoff_pairs_with_nothing_attached}}` [15 of the 20 largest hand-off types: 0 of 40 each]. *Optional line if time allows:* `{{fig:e1_page_hides_words_h02}}` and siblings h04, h08, h09: for refuse and bulk "next scheduled day" and both weed types "on schedule to be cut" (7,845 requests in the window), the public page replaces the closing words with "contact the Citizens' Service Bureau." *Note (E2, observed):* Cityworks 23 closes a linked request automatically when its work order closes, and St. Louis runs 23.10. The loop exists in the software; closing by hand at the hand-off is what defeats it. *Revised after E1's interim:* "one division turned it on" is withdrawn; Streets attaches on 16 of 40 referred cave-ins too.

**4 · 0:50–1:05 · The size of it.** *Screen:* the fates bar (done by promise / late / no record) and the queue count. *Narration:* "Where the work could be traced, 311 had closed 85 percent of requests by the promised date. 18 percent were done by it. Half were done a month late. A third show no record. And today about 15,000 open requests sit past their promised date. No list ranks them." *Slots:* R1 headline `{{fig:r1_traced_closed_by_promise}}` [84.9%], `{{fig:r1_traced_done_by_promise}}` [18.0%], `{{fig:r1_traced_done_late}}` [49.8%, median 28 d], `{{fig:r1_traced_no_record}}` [32.2%]; queue `{{fig:e3_queue_open_past_promise_2025_26}}` [14,902].

**5 · 1:05–1:28 · The queue.** *Screen:* the queue page: tiles, division table, map, the saved-search definition. *Narration:* "This is that list, built from one saved search in the system the city already runs: by division, oldest first, on the map. Forestry, 4,700. Streets, 4,200. Here is the definition, in their field names, so their analyst can build it this week." *Slots:* `{{fig:e3_queue_by_division}}` [Forestry 4,679; Street Dept 4,185].

**6 · 1:28–1:42 · The column and the status.** *Screen:* the scoreboard with "done by the promise" lit; then the status page "after." *Narration:* "CityStat gets one more column: done by the promise. And the resident's page says 'with Street Maintenance since July 27, promised July 30, 75 days past,' instead of 'closed.'" *Slots:* `{{fig:n4_sb_kept_all}}` [57.8%], `{{fig:n4_sb_done_kept_all}}` [19.5%] on screen, not spoken.

**7 · 1:42–1:55 · Four rules, one ask.** *Screen:* plain text, one line at a time. *Narration:* "Four rules in the system you already own. Attach the work order at every hand-off. Stop closing the request by hand: Cityworks already closes it when the crew closes the job. Carry the promise to the job. Work the list oldest first. No new staff, nothing to buy, no AI inside. The ask: do it for three request types this quarter, and re-run this list in ninety days. The baseline is on the site today." *Note (E2):* rule 2 is native in Cityworks 23 ("the service request closes automatically when the work order is closed"); the city's own archived status definition said Closed means the work "has been finished by the department". "Your towing rule" moves to the README; "stop closing by hand" is the sharper line.

**8 · 1:55–2:00 · End card.** Name, "Independent prototype built from the City of St. Louis's open data and Cityworks saved searches read with the City's permission. Not a City website." Repository link (only once a clean repository exists).

## Read-aloud, v2 final draft (268 words; about 1:47 at 150 a minute; time it)

> St. Louis grades its services on CityStat. Alley debris: 79 percent cleaned on time. Count only the closings that say the work was done: 15. The measure counts the hand-off, not the job.
>
> July 2nd: weeds on a city-owned lot, 1700 block of North Taylor. Closed in thirteen minutes: "on schedule to be cut." July 28th, again. Forestry's ledger bills cuts on 36 other parcels on this block. This lot: none.
>
> For a cave-in, the resident's page says: closed, referred, nothing attached. Same page, a tree request: work orders attached. Across the twenty biggest hand-offs, six percent carry a work order. Fifteen types carry none.
>
> Where the work could be traced, 311 closed 85 percent on time. 18 percent were done on time. Half were done a month late. A third show no record. And 15,000 open requests are past their promised date today, with no list that ranks them.
>
> This is that list: one saved search in Cityworks, by division, oldest first, on the map. Forestry, 4,700. Streets, 4,200. Their analyst can build it this week.
>
> CityStat gets one more column: done by the promise. The resident's page says "with Street Maintenance since July 27, promised July 30, 75 days past," instead of "closed."
>
> Four rules in the system you already own. Attach the work order at every hand-off. Stop closing the request by hand: Cityworks already closes it when the crew closes the job. Carry the promise to the job. Work the list oldest first. Nothing to buy, no AI inside. Try it on three request types for one quarter, and re-run this list in ninety days.

Every figure above is registered: 78.6/15.0 (`e3_citystat_debris_published_vs_done`), lot-1 (`n5_lot1_*`), 6% and 15 of 20 (`e1_handoff_share_with_work_order`, `e1_handoff_pairs_with_nothing_attached`), 85/18/half/third (R1 headline), 14,902 (`e3_queue_past_promise`), divisions (`e3_queue_div_*`), 75 days (`e3_status_cavein_days_past_promise`, inferred and labelled so on the page), the Cityworks auto-close (E2, section A2, observed in the vendor's help).

## Lines that depend on threads

- Shot 3's spoken attach rates: E1 final (1,440 pages, 0 failures): 50 of 800 hand-off pages carry a work order (6.2%); 15 of 20 types 0 of 40. Resolved.
- Tree removals as the "linked but late" proof: 1 of 40 by the promise, median 211 days (E1). Use in the README; in the video only if a line is cut elsewhere.
- "Your towing rule": the CityStat towing page (R3, confirmed live 14 Oct). Stands.
- "In the cloud move you've scheduled": reported (May 2026 hearings). If E2 cannot confirm, say "as part of your next Cityworks upgrade."
- "One saved search": E2 confirms the mechanism name; E3 shows the definition.
- Shot 6's "75 days past": computed from the cave-in example E3 reconstructs; must match its page.

## Cuts if it runs long (in order)

1. "this year" in shot 2. 2. "with dates" in shot 3. 3. "Here is the definition, in their field names, so their analyst can build it this week" → "Their analyst can build it this week." 4. "The baseline is on the site today."
