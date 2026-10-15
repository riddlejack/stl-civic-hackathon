# Video script v3: the plain-language spine (Jack's structure)

Drafted 14 Oct 2026, about 4:45 p.m. Central, after Jack's review of the day-two doc. Supersedes v2. The viewer knows nothing. Every beat says its takeaway out loud; the examples serve the one root cause. Full version runs about 345 words (2:15 at 150 a minute); the cuts at the end bring it to about 300 (2:00). Jack shapes the visuals; the screen notes are suggestions.

## Spine

Who and what → how the system works today → the issues that gap creates → what it costs, and the city already knows → the new system → the product → the ask.

## Beats

**1 · 0:00–0:10 · Who and what.** *Screen:* title card, then five issue cards appearing in a row (uncut city lots, cave-ins, missed trash, broken sidewalks, hazardous trees). *Narration:* "I'm Jack Riddle. I went into this hackathon looking at the problems St. Louis residents report most: uncut city lots, cave-ins, missed trash pickups, broken sidewalks, hazardous trees. I expected five separate problems. I found one."

**2 · 0:10–0:35 · How the system works today.** *Screen:* the flow diagram from the day-two doc, drawn box by box as each is named; the dashed line appears last. *Narration:* "Here's how a request moves through the city. A resident calls 311. The request gets a promised date. It's routed to a division. And at the hand-off, staff close the request by hand, with words like 'on schedule to be cut.' The crew's work order lives in the same system, Cityworks, but for most services it's never attached to the request. CityStat, the city's scorecard, counts that close as service delivered."

**3 · 0:35–1:00 · The issues that gap creates.** *Screen:* three numbers land one at a time (79% → 15%; 18% done by promise; 15,000 past promise), then the status page pair (cave-in: nothing attached; tree: work orders attached). *Narration:* "That one gap shows up everywhere. On the city's own alley-debris measure, 79 percent on time becomes 15 percent when you count only closings that say the work was done. Where I could trace the work, 18 percent was done by the promise, half came a month late, a third has no record. 15,000 open requests sit past their promised date, and no list ranks them. I checked 1,440 public status pages: 15 of the 20 biggest hand-off types never attach a work order. The resident sees 'closed.'"

**4 · 1:00–1:15 · What it costs, and the city knows.** *Screen:* the lot's receipt (two filings, two closures in minutes, 36 neighbours cut), then three quotes on screen with attribution. *Narration:* "A city-owned lot on North Taylor: reported twice, closed in minutes, never cut while 36 neighbours were. The city has said it. Its towing page: 'closed does not necessarily indicate that a vehicle has been towed.' The head of 311: residents ask 'why it's past the completion date but still not completed.' The mayor's transition committee: 'audit previously closed requests.'"

**5 · 1:15–1:40 · The new system.** *Screen:* the same diagram, now closed: the work order attaches at the hand-off, the request stays open, the dashed line becomes solid, the promise rides on the job, the overdue list appears. *Narration:* "The fix is already in the software they own. Cityworks closes a request automatically when its work order closes. Forestry already attaches work orders, and the public page already shows them. So, four rules, for every service: attach the work order at every hand-off. Stop closing the request by hand. Carry the promise to the job. Work the overdue list oldest first."

**6 · 1:40–2:00 · The product.** *Screen:* the queue (one division, oldest first, the map), the resident's page after, CityStat with the added column. *Narration:* "What that produces, built on the city's own data today: the queue, every promised job not finished, by division, oldest first, on a map. The resident's page with the real status: which division holds it, since when, how far past the promise. And CityStat with one more column: done by the promise. One saved search and plain SQL. Nothing to buy, no AI inside."

**7 · 2:00–2:12 · The ask.** *Screen:* three lines, then the end card. *Narration:* "Try it on three request types for one quarter, and re-run this list in ninety days. The baseline is on the site. Every division gets the same list."

## Read-aloud (full, about 345 words)

> I'm Jack Riddle. I went into this hackathon looking at the problems St. Louis residents report most: uncut city lots, cave-ins, missed trash pickups, broken sidewalks, hazardous trees. I expected five separate problems. I found one.
>
> Here's how a request moves through the city. A resident calls 311. The request gets a promised date. It's routed to a division. And at the hand-off, staff close the request by hand, with words like "on schedule to be cut." The crew's work order lives in the same system, Cityworks, but for most services it's never attached to the request. CityStat, the city's scorecard, counts that close as service delivered.
>
> That one gap shows up everywhere. On the city's own alley-debris measure, 79 percent on time becomes 15 percent when you count only closings that say the work was done. Where I could trace the work, 18 percent was done by the promise, half came a month late, a third has no record. 15,000 open requests sit past their promised date, and no list ranks them. I checked 1,440 public status pages: 15 of the 20 biggest hand-off types never attach a work order. The resident sees "closed."
>
> A city-owned lot on North Taylor: reported twice, closed in minutes, never cut while 36 neighbours were. The city has said it. Its towing page: "closed does not necessarily indicate that a vehicle has been towed." The head of 311: residents ask "why it's past the completion date but still not completed." The mayor's transition committee: "audit previously closed requests."
>
> The fix is already in the software they own. Cityworks closes a request automatically when its work order closes. Forestry already attaches work orders, and the public page already shows them. So, four rules, for every service: attach the work order at every hand-off. Stop closing the request by hand. Carry the promise to the job. Work the overdue list oldest first.
>
> What that produces, built on the city's own data today: the queue, every promised job not finished, by division, oldest first, on a map. The resident's page with the real status: which division holds it, since when, how far past the promise. And CityStat with one more column: done by the promise. One saved search and plain SQL. Nothing to buy, no AI inside.
>
> Try it on three request types for one quarter, and re-run this list in ninety days. The baseline is on the site. Every division gets the same list.

## Cuts to reach 2:00 (about 300 words), in order

1. Beat 3: drop "I checked 1,440 public status pages: 15 of the 20 biggest hand-off types never attach a work order." (keep it on screen as a caption; 17 words).
2. Beat 4: keep one quote, the towing page (drops about 25 words).
3. Beat 6: drop "which division holds it, since when, how far past the promise" (11 words).
4. Beat 7: drop "Every division gets the same list." (6 words).

## Figures behind each spoken number

79/15 `e3_citystat_debris_published_vs_done` · 18% / half / a third: R1 headline · 15,000 `e3_queue_past_promise` (14,902) · 1,440 and 15 of 20 `e1_handoff_pairs_with_nothing_attached` · the lot `n5_lot1_*` · the three quotes: `research/chapters/R3-voices.md` rows 1, 3 and the transition committee (all confirmed live 14 Oct) · Cityworks auto-close: E2 section A2 (vendor help, observed) · the four rules: `context/BRAINSTORM-shape.md` §2.

## Names (Jack is not in love with DoneStat)

Candidates that say what it does: **Closed Loop** (the fix, literally: close the loop between 311 and the work order); **Kept** (a promise kept; the column is "done by the promise"); **WorkDone**; **The Last Mile**; **Promise Date**. My pick: Closed Loop, with the tag "311 to work order to done." Avoid anything that sounds like a product the city must buy.
