# Video script v4: which promises did St. Louis keep?

Written Wednesday 14 October 2026, about 6:20 to 6:45 p.m. Central, from scratch, after the 14,902 reality check (`research/open-queue-reality-check.md`). Supersedes v3. Narration first; the screen plan that follows from it is `deliverable/VIDEO-BEATS.md`. The read-aloud is about 730 words (4:17 in the scratch voice); the cut map at the end gives shorter versions.

## What changed from HANDOFF-4 Part C, and why (the half-page note)

1. **The root cause is now one sentence the evidence fully supports: the city can't tell which of its promises it has kept.** The check of the 14,902 found that fewer than 3% have any record of the work being done and 84% have no record either way. The old line, "closed is not done", only described the closed half. The new line covers both halves: hand-off closures counted as service, and open requests nobody can confirm.
2. **The fix is three parts, and the list carries most of the weight.** The parts are link, list and count. Requests the city already keeps open fare worse (95% of open vacant-lot weed requests have no cut on record), so "stop closing at the hand-off" on its own fails. The script now says so out loud, in beat 6, before it gives the fix. The point you were worried about becomes the bridge from problem to fix, and the fix no longer reads as tacked on. The "three layers" framing (C1) is gone, and so is rule 3.
3. **The after-example is corrected and kept honest.** The lot's first promise was **30 September**, not 16 July as C1 had it. The replay now ends on what is certain: on 1 October the lot is on Forestry's list and the resident's page tells the truth. Whether the crew comes sooner is said to be the bet.
4. **The video opens on the City's own question** (Ben's question 5: how the city could better communicate how it's doing). The whole argument also arrives within the first 45 seconds, so a judge who stops at 2:00 has still heard it. Then the depth.
5. **AI is framed as the method, not left out.** City IT policy #2026-001 bars AI tools the IT department hasn't approved; it does not ban AI (`data/raw/mayors-office/datatech/`, lines 112, 55–57). So: AI agents did the audit; what the city runs is plain SQL. There is no "no AI inside" boast on a Civic AI stage.
6. **The site's role is said plainly.** Two of the three screens run today on public data with no change in practice. The third needs the work order attached. What we hand over is the package that runs them. This settles the "tool or demonstration?" question: it is both.
7. **Dropped:**
   - the 9 September "cut left incomplete" call. It is ambiguous: it could imply a partial cut the record does not show.
   - the mayor's "report card" quote. We have no saved copy (R3, line 161).
   - "residents still waiting" as a claim about all 14,902.
   - the 1,700–3,500 never-done estimate.
   - the 2025 lot claim. The 2025 mowing record is thin, so the lot story speaks only of 2019–24 and 2026.

Name: the script uses **[NAME]** and needs one only on the end card. With the root cause as it now reads, my pick is **Kept**, with the tag "Which promises did St. Louis keep?" Closed Loop still works.

## The argument in one breath

St. Louis gives every 311 request a completion date. It closes most requests when it hands them to a crew. The crew's work order is almost never attached to the request, so the city can't tell which promises it kept. Its scorecard counts the hand-offs as service. The requests it doesn't close pile up with no record either way. Keeping them open isn't the fix; that pile proves it. The fix is to link the request to the job (the city's own software already closes a linked request when the job closes), put every unkept promise on a weekly list, and count done. Two of those run on the city's data today.

## Why this order (the three lenses)

- **As a hackathon video.** A cold judge hears whose question this answers, who I am, and the whole case by 0:45. The ask comes at the end, with a baseline the city can test against.
- **As 3Blue1Brown would do it.** One object carries the whole video: a promise card with a clock. Start with a concrete puzzle (five problems that turn out to be one), then build the mechanism visibly. Show the obvious fix and why it fails. Then the real fix, replayed on the same lot.
- **As a McKinsey or Palantir team would lay it out.**
  - Situation: a date on every request.
  - Complication: closed at the hand-off and never linked.
  - Question: how can the city know, and show, which promises it kept, without buying anything?
  - Answer: link, list, count.
  - Every symptom maps to one part of the fix (the bridge table below). Every claim has a figure. The plan has owners and a measurable trial.
  - Other entries are never mentioned. The contrast is carried by "software you already own", "runs Monday", "nothing to buy" and "re-run it against today's baseline".

## Read-aloud (tightened to about 730 words; the scratch voice runs 4:17)

Revised about 6:35 p.m. after an independent fact-check (2 wrong, 8 misleading lines fixed; table below), then tightened from 901 words at about 6:40 p.m. Every element Jack required is still here; the cut map at the end goes further.

> **1.** The City asked this hackathon a question: how can St. Louis better communicate how it's doing on city services? I'm Jack Riddle. To answer it, I had to find out what "done" means.
>
> **2.** Every 311 request gets a completion date: a promise. So I checked some. A city tree marked for removal: of forty, one was removed by the request's date; typically, seven months after. A city-owned lot: one report in four, no cut on the city's own mowing record. I expected separate problems. It's one: the city can't tell which of its promises it has kept. And the fix is already in software it owns.
>
> **3.** Here's how a promise works today. A resident reports an overgrown lot. 311 gives it a date and routes it to Forestry. Often within minutes, someone closes it: "on schedule to be cut." That's the hand-off. The crew's record of the job is almost never attached. In fifteen of the twenty most common hand-offs, the city's status pages show nothing attached at all. So after the hand-off, nothing is waiting for the work. The resident sees "closed." On CityStat, a closed hand-off counts as on time. If the crew never comes, nothing notices.
>
> **4.** That gap shows up twice. First, in the scorecard. CityStat says 79 percent of alley debris was cleared on time this spring. Count only closings that say it was picked up: 15. Where I could trace mowing and board-ups, 18 percent were done by the promise and half came weeks late; for mowing, a third have no cut on record.
>
> Second, in the requests nobody closes. 14,902 requests filed since January 2025 are past the date the city gave. Three in four came from residents. Fewer than 3 percent have any record of the work being done. For 84 percent, no record says either way. No one can tell those residents, or the mayor, whether the work happened.
>
> **5.** Here's one: a city-owned lot on North Taylor, on Forestry's mowing list, cut every year from 2019 to 2024. Reported on 2 July: closed in thirteen minutes, "on schedule to be cut," due 30 September. Reported again: closed in seven. Thirty-six other parcels on its city block were cut this year. This one has no cut on record.
>
> **6.** The obvious fix: stop closing requests early. The city already plans that for towing; its own page admits "closed" does not mean towed. But look at the ones it already leaves open: 95 percent of open vacant-lot weed requests have no cut on record, worse than the closed ones. Keeping a request open with no job attached doesn't cut the lot either. The request has to know about the job, and someone has to see the list.
>
> **7.** So, three changes, in systems the city already runs. Link: at the hand-off, attach the crew's work order instead of closing the request. Cityworks' documentation says the version St. Louis runs closes a linked request when its work order closes. List: every week, each division sees every request past its date with no finished work order, oldest first, on a map. Count: CityStat adds one column, done by the promise. The column fixes the scorecard; the link tells done from waiting; the list puts each broken promise in front of someone.
>
> Replay North Taylor. 2 July: a cut order is attached, and the request stays open. The second call lands on that open job. 1 October, the day after its date, the lot is on Forestry's list. The resident's page says: "With Forestry since 2 July. Due 30 September." Whether the crew comes sooner is up to the crew. But the lot can't disappear.
>
> **8.** I built this on the city's own data: Forestry's list, CityStat with the column, a resident's page before and after. Simple versions of the list and the column run today on public data; the link makes them exact. I'm handing over the package: a saved search and dashboard for the city's geoportal, the SQL, and one page of practice per division. AI agents did the audit, the analysis Forestry's commissioner said no one on staff is designated to do. What the city runs is plain SQL. Nothing to buy.
>
> **9.** The ask: one quarter, three request types: tree removals, cave-ins and vacant-lot mowing. Attach the work order, work the list, publish the column. Then re-run it against today's baseline. You'll know which promises you kept.

### Fact-check changes (about 6:35 p.m.)

| Line (v4 first draft) | Problem | Now |
|---|---|---|
| "CityStat counts it on time" (the lot); "CityStat counts it late" (replay) | **Wrong.** No CityStat 311 measure covers weeds | "On CityStat's measures, a closed hand-off counts as on time"; the replay drops CityStat |
| "Those are residents who were given a date" | **Wrong.** 11,297 of the 14,902 were resident-filed; 2,595 staff; 986 unclear | "Three in four came from residents" |
| tree "came down by its date" | The 14-day date is the inspection request's | "within the request's two-week date" |
| "just a slower way to lose it"; "nobody looks at" | Implies closing loses work (a must-not); open ones sit in dispatch or inspection | "Keeping a request open, with no job attached, doesn't get the lot cut either" |
| "Forestry already does this" | Forestry attaches, then closes by hand | "attaches work orders to tree removals, then closes the request by hand anyway" |
| Auto-close stated as fact | It is the vendor's documentation, untested on the city's system | "Cityworks' own documentation says…" |
| "The list and the column run today" | The built list is open past-promise requests; the column grades closing words | "Simple versions… run today… The link makes both exact" |
| "The crew keeps its own work order in Cityworks"; "the mowing order is attached" | Vacant-lot mowing is recorded in a billing ledger, not a Cityworks layer we hold | "a route, a ledger, a work order"; the replay says "a cut order is attached" (a counterfactual; Forestry already uses weed work orders, "Occupied" and "HandCrew", on occupied-property requests, observed on 24 of 30 status pages) |
| the trace sentence after debris | It covers mowing and board-ups; board-up "no record" doesn't hold up | "in mowing and board-ups… For mowing, about a third has no cut on record" |
| "On 1,440 status pages, 15 of 20" | The 15 of 20 comes from the 800 hand-off pages | 1,440 moves to beat 8 |
| "36 other parcels on that block" | It is the assessor's city block | "on the same city block" |
| "within minutes" (in general) | Only 49% of 2026 lot closings came within the hour | "Often within minutes"; 13 and 7 stay for the lot |
| "what residents report most" | Weeds rank 21st, sidewalks 25th of 280 types | "everyday services" |
| "two calls" / "later calls" | A third call (an "unsatisfactory cut" complaint) came on 9 September | Settled at 7:30 p.m.: the lot is shown reported twice, and the replay says "The second call lands on that open job" (×2). The 9 September call stays out because its wording could imply a partial cut |
| the commissioner | The quote says no one "designated" | "no one on staff is designated to do" |

Closing-word classes behind "79 becomes 15" (reviewed 6:45 p.m., `research/closure-class-review.md`): 15.0% holds under every reading (15.0–15.4%; 14.1–14.6% on CityStat's own count). Safe only as worded: "closings that **say** it was picked up". Do not say "only 15 percent was cleaned" or "67 percent are hand-offs". The city's best rebuttal still leaves 24.0%. Q2 2026 is one of the better quarters (2024–25 ran 0.2–8.8%), so don't imply it is getting worse. A human still needs to check three phrases: "bulk will be picked up in correct week", "matter will be investigated" and enforcement notices. Jack's to do.

## The bridge: each problem, the part that fixes it, what changes for a resident

Spoken once in beat 7, built on screen as a three-row table:

| What the city sees today | Why | The part that fixes it | What changes, with certainty | What it makes possible (the bet) |
|---|---|---|---|---|
| A scorecard that counts hand-offs as on time (79% vs 15%) | The close happens at the hand-off | **Count:** done by the promise | CityStat reports work done, on the city's own data, from Monday | Divisions are managed to finishing |
| 14,902 requests past their date, 84% with no record either way | The request is never linked to the job | **Link:** attach the work order; Cityworks closes the request with the job | Each request shows "done" or "waiting" | The pile shrinks to real waits |
| No one sees a broken promise until a resident calls again | No list exists above the crew | **List:** weekly, by division, oldest first, on a map | Every unkept promise is on someone's screen within a week of its date | The oldest promises get worked first |
| The resident is told "closed" | The page reflects the hand-off | **Link** (it feeds the page) | "With Forestry since 2 July. Due 30 September." | Fewer repeat calls |

## Figures behind each spoken number

| Spoken | Value | Source | Label |
|---|---|---|---|
| "a completion date, a promise" | `PRJCOMPLETEDATE`; the page shows it as "Dept Response Due By", equal on 1,438 of 1,438 pages. The acting director of the division that runs 311 calls it "the completion date" | `e1_promise_date_agreement`; R3 row 3 | observed |
| tree: of forty, one by its date; typical seven months late | 1 of 40 by the 14-day promise; 39 late, median 211 days. Requests closed "removal work order created" | `e1_linked_svc_h_tree` | observed (sample of 40) |
| sidewalk: where on record, every one late, about six months | 16 of 186 hand-offs have a later repair at the address, all after the promise, median 179.5 days late | `research/cityworks-gap-review.md` (Jack's Cityworks extraction, 14 Oct) | observed |
| city-owned lot: one in four, no cut by October | 24.3% of hand-off closures on land-bank lots have no cut billed by 13 Oct (n = 313) | `research/chapters/R1-trace.md`, "Weed no record holds up" | observed |
| 1,440 status pages; 15 of the 20 most common hand-offs nothing attached | 15 of 20 pairs, 600 pages, 0 items | `e1_handoff_pairs_with_nothing_attached` | observed |
| CityStat 79%; 15 counting only closings that say it was picked up | Q2 2026 debris, alley or street: 78.6% published; 15.0% done-only on the same denominator | `e3_citystat_debris_published_vs_done`; `r1_citystat_debris_alley_street_q2_2026_ontime_done_only` | observed |
| 18% done by the promise; half weeks late; a third no record | 3,640 traced hand-offs: 18.0% / 49.8% (median 28 days) / 32.2% | R1 headline | observed |
| 14,902 past the date, filed since January 2025 | 14,902 of 16,505 open | `e3_queue_past_promise` | observed |
| fewer than 3% done; 84% no record either way | 388 (2.6%); 12,566 (84.3%) | `research/open-queue-reality-check.md` | observed |
| the lot: on Forestry's list; cut every year 2019–24; closed in 13 and 7 minutes; due 30 Sept; 36 other parcels cut; no cut on record | `on_forestry_maintenance_list`; cuts 6, 5, 3, 2, 4, 4; minutes 13 and 7; promise 2026-09-30; 36 other parcels on the city block cut in 2026; 0 cuts billed in 2026 | `build/N5/heroes.json` (lot-1) | observed |
| towing page quote | "Currently, "Closed" does not necessarily indicate that a vehicle has been towed…"; plan: "only closed once a vehicle is actually towed" | R3 row 1 (live 14 Oct) | observed |
| 95% of open vacant-lot weed requests have no cut on record | 95.4% (n = 131), against 34.9% for those closed at the hand-off | R1, "Kept open vs closed" | observed |
| Forestry already links tree removals | 40 of 40 pages list the work orders | `e1_tree_removal_share_with_attached` | observed |
| Cityworks closes a linked request by itself | Cityworks 23 help; St. Louis runs CW 23.10 | `research/precedents-closed-loop.md` §A2 | observed (vendor documentation) |
| the commissioner: no one on staff to analyse the data | Forestry Commissioner, 6 May 2026: "we have all this data but we don't have somebody on staff…" | R3 row 7 | observed (captions) |
| "the list and the column run today" | The queue and the done column are built from the public file and saved searches | `site/queue.html`, `build/E3/citystat_done.json` | observed |

## Claims this script deliberately does not make

- **That all 14,902 are residents still waiting.** It says "past the date" and "no record either way".
- **That closing early loses the work.** Beat 6 says the opposite, with the data.
- **That the fix clears the backlog or speeds up crews.** "Whether the crew comes sooner is still up to the crew."
- **Any equity or ward claim.**
- **That re-reports prove undone work.**
- **"Never cut".** It says "no cut on record".
- **That we reproduce CityStat exactly.** It is within 0.2% on 8 of 9 measures, and the script doesn't claim more.
- **How the Cityworks data was obtained** is on the end card: read with the City's permission, operational fields only, no personal data.

## Cut map

**To about 3:00 (about 450 words), in this order:**
1. Beat 4: drop the trace sentence ("Where I could trace… no record at all"); 25 words.
2. Beat 2: drop the sidewalk line; 15 words.
3. Beat 5: drop "on Forestry's own mowing list, cut every year from 2019 to 2024" and the towing quote; the towing quote moves to an on-screen card in beat 6, where "the city already plans that for towing" stays; 35 words.
4. Beat 7: drop "Forestry already attaches work orders to tree removals, then closes the request by hand anyway"; 16 words.
5. Beat 8: drop "Forestry's list. CityStat with the column. A resident's page, before and after." The screens show them; 13 words.
6. Beat 3: drop the 1,440-page sentence; it stays on screen as a caption; 20 words.
7. Beat 4: drop "Tree inspections, cave-ins, sidewalks, weeds." It stays on screen; 6 words.

**To about 2:15 (about 330 words):** additionally merge beats 5 and 7. The lot appears once, in the replay ("A city-owned lot on North Taylor, reported twice, closed in minutes both times, no cut on record. Under the new system…"). Drop beat 6 down to its last sentence.
