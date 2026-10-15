# Pitch architecture: how the entry argues, and what must be true for it to land

Written Wednesday 14 October 2026, about 3:15 p.m. Central, by the orchestrating thread while E1, E2 and E3 run. Labels as in `AGENTS.md`. Figures cited here are observed unless marked; sources are in `context/FRESH-EYES-ASSESSMENT.md`, `research/chapters/R1-trace.md`, `research/chapters/R3-voices.md` and `research/mayors-office-voice.md`.

## 0. The package and who judges it

- **What is submitted:** a two-minute screen demo on YouTube (the hook), a repository link (the memo lives in its README), the site (the evidence, every number with its derivation), and a one-page note to Ben's office (the ask). Mike's words at the kickoff: "telling the story about what we're building, why it's important" (00:37:00); "something that's open source and already built, that they can deploy" (00:24:52).
- **Who judges:** Ben Jonsson (COO; "I lead 14 departments and agencies"; launched CityStat; "are we making things better for our residents"), Mike Seper (implementation, community, the personal story), and whoever Mike calls the judges. Only one other team is listed on the sign-up doc (problem set 3). The audience that matters is the mayor's office.
- **Their tests, in their words:** Ben: "leverage geospatial data and other open source data sources"; "take a look at our current CityStat webpage and let us know what resonates"; "these are real problems we're trying to solve." Mike: "our goal is implementation"; "think as grand as possible"; "ways you can rally your community."

## 1. The governing question, from Ben's seat

How can my departments know which requested jobs are done, and get the overdue ones done, with the staff and systems we already have?

## 2. SCQA, in two lengths

**Situation.** The city measures service with CityStat and reviews it weekly. Every 311 request carries a date the city itself promises. Residents report, and get "closed."

**Complication.** "Closed" means handed off, not done. CityStat's alley-debris measure reads 78.6% on time; counting only closings whose words say the work was done, 15%. Where the work can be traced, 18% was done by the promise, half was done late by a median four weeks, a third shows no record. About 15,000 open requests filed since 2025 are past their promise and no list ranks them. The city knows: its towing page says "closed" does not mean towed; the head of 311 hears "why it's past the completion date, but it's still not completed"; the transition committee asked for an audit of closed requests.

**Question.** How does the city close the loop without new staff or software?

**Answer.** It already owns the loop. Cityworks attaches work orders to requests, Forestry uses it for tree removals, and the public status page already shows them. Four rules: attach a work order at every hand-off; close on actual finish; carry the promise to the job; work the overdue list oldest-first and see it weekly. Here is what that looks like on the city's own data today: the queue by division, the status page after, CityStat with the done column. The ask: turn it on for every service, as part of the Cityworks cloud move already scheduled, and run the list for one quarter.

Video version: the same four beats in about 250 words, with the lot as the resident story inside the complication. Memo version (README): the same spine, each claim with its figure id and label, the tree in section 3, the chain in section 4.

## 3. The issue tree (the memo's spine; cut by: the stage of the decision)

| Branch | Question | Evidence | Status | Owner |
|---|---|---|---|---|
| 1. Is there a problem worth the COO's time? | How big, who pays, does the city see it? | N2 35% hand-offs; N4/R1 restated CityStat (78.6 vs 15.0); R1 fates (18/50/32); R2 planting and extrapolation (estimate); the queue (14,902); R3 voices; Philadelphia and Boston analogues | Proven, with the extrapolation labelled | Done |
| 2. Where does the chain break? | Intake, hand-off, work order, finish, status, measure: which link is missing? | `WONeeded` on 8 of 19,291 active requests; public page attach counts (ten pages; E1 at scale); no request id returned on work orders; kept-open requests fare worse; a report does not move the crew; CityStat counts the close | Proven on the request side; E1 makes it per-service | E1 |
| 3. What closes it, given what the city owns? | Configuration, practice or new work? | Forestry already attaches; the towing plan; Cityworks documentation (E2); Chicago's weekly lot lists | Pending E2 for the setting's name | E2 |
| 4. Will it be adopted and survive? | Who flips it, who runs it, what breaks it? | ITSA cloud move FY2027 and three analyst posts; CityStat's analyst and the weekly cabinet review; the division heads who already asked (Streets, Forestry, 311); risks: crews at 60%, 1,750 bad finish dates, gaming, privacy, AI policy | Partly written; needs a 30/60/90 plan and named owners | Orchestrator |
| 5. How will we know it worked? | What is the measure and the baseline? | Done-by-promise share per service and overdue count per division as of 13 Oct 2026; the same SQL in 90 days | Defined; baseline table from E3's figures | E3 then orchestrator |
| 6. What does it cost, and what is next? | Licences, hours, the services still without a completion record | $0 new licences; analyst hours; the register's "what it would take" (refuse, towing, water); EO 96's asset dashboard | Written in the register; needs one paragraph | Orchestrator |

Division principle at the top: each branch is one stage of the decision a COO makes (is it real, why, what fixes it, will it stick, how will I know, what next). They do not overlap; together they are the decision.

## 4. The logic chain, link by link (the "nothing missing" check)

| # | Claim | Evidence | Status | Where it appears |
|---|---|---|---|---|
| 1 | The city measures the close, not the work | CityStat definition reproduces from the public file within 0.2% | Proven | Video, memo |
| 2 | For most services the close is a hand-off | 35.2% of 175,876 closures; 67% of alley-debris on-time closures are hand-offs | Proven | Video, memo |
| 3 | After the hand-off, nothing links the request to the work, except where one division chose to | `WONeeded` 8 of 19,291; attach counts on the public page (E1); no request id on work-order searches | Proven on ten pages; E1 at scale | Video (tree page vs cave-in page), memo |
| 4 | So nobody can rank or audit overdue work above the division, and the resident's status is wrong | 14,902 open past promise with no published list; the status page ends at "referred"; Clifford's words | Inferred from 3; the count is observed | Video (queue), memo |
| 5 | Where the work can be traced, it is late or missing at material rates | R1: 18.0% by promise, 49.8% late (median 28 d), 32.2% no record; planting 133 d late; sidewalks 180 d; trimming 218 d | Proven | Memo; one line in video |
| 6 | The cost lands on residents and on the city's credibility | The lot (36 neighbours cut, none here); Resolution 142; Philadelphia trials on uncut lots and open buildings; the mayor: "the report card residents are going to rely on" | Partly proven; analogues labelled | Video (lot), memo |
| 7 | The link already exists in Cityworks and one division uses it | Tree pages with 3–5 attached items; the sewer lateral programme; E2 names the setting | Proven; E2 pending for the mechanism | Video (the turn), memo |
| 8 | Attach, close on finish, carry the promise, rank the overdue: the misses become visible and ordered | Built on the city's data (E3) | By construction | Video (queue, status after, CityStat column) |
| 9 | Visible and ranked leads to more done on time | The city's own towing plan; Chicago weekly lists (trims tripled, reported); Boston: proof of work raised trust 14% | A bet, said as one | Video (one sentence), memo (strongest case against) |
| 10 | It costs nothing new and fits the migration | Configuration plus SQL; AI-free; ITSA's posts and cloud move | Proven on cost; migration window reported | Video (ask), memo |

Weakest links: 4 (inferred), 6 (partly), 9 (bet). The pitch says so in one line each; the negative-results page carries the rest. Honesty is also persuasion here: Boston residents shown failures alongside finished work did not trust the city less.

## 5. Branches that were missing or thin (Jack's list), now placed

- **Implementation.** Who flips what: ITSA (Cityworks administrator) enables the request-to-work-order link and status update per template (E2 names it); division heads instruct crews to attach at hand-off; the CityStat analyst runs the queue SQL weekly and adds the column. Window: the FY2027 cloud migration. A 30/60/90 plan: 30 days, Forestry and Streets attach and close on finish for three request types; 60 days, the queue in the cabinet review and on the geoportal; 90 days, the done column on CityStat and the same SQL re-run against the 13 October baseline.
- **Adoption.** It fits routines that already exist: saved searches staff already work; the weekly cabinet data review; the public page the city already runs. No new login, no new vendor. The first users are the people who already asked for it in hearings.
- **Maintenance.** SQL and saved searches; owners are the CityStat analyst and ITSA's new analysts; runs on the weekly 311 export the city already publishes; our hosting is not part of the ask.
- **Cross-department data.** Cityworks already holds every operating department's requests; the queue spans divisions on day one. For services with no completion record at all (refuse, towing, water, cave-ins, lights), the register says what it would take, and the work-order link supplies most of it.
- **Next steps for the mayor's office.** The ask, the plan, the baseline, and one question back: who creates work orders today, CSB or the department.
- **Risks, said plainly.** Crews are the limit (ranking helps; no new crews claimed). Data quality (1,750 finishes before initiation; the queue is a ranking, not an accusation). Gaming (a work order closed without work scores; keep a small field check; Rumelt's warning). Privacy (block level). AI (none in the product). What we did not build and why (surveillance for dumping; canopy).

## 6. What the mayor's office asked for, mapped

| They asked | Where the entry answers |
|---|---|
| Geospatial and open data (Ben) | The queue map by block from the public file; the saved search on their own layer |
| CityStat: what resonates, how to structure it (written question 5) | The done-by-promise column; the status page that explains "past the completion date" |
| Illegal dumping (problem set 3) | The alley-debris measure (78.6 vs 15.0); 259 repeat blocks; hand-offs closed "will be investigated" with no clean-up record |
| Tree canopy (problem set 1) | 806 approved plantings, 65% planted a median 133 days late, 280 with no record; 8,412 city-owned lots mowed for $1.31M |
| "Are we making things better for our residents" (Ben) | The receipt and the status after; the lot |
| Implementation, built, open source (Mike) | Running on the city's own data; SQL and saved-search definitions in the repo |
| The personal story (Mike) | One block in the Greater Ville, reported twice, closed in minutes, no cut billed all season, 36 neighbours cut |
| "As grand as possible" (Mike) | Every department, every request, one rule |

## 7. How to say it (craft)

- Open on his artifact and his words: the CityStat page, "are we making things better for our residents."
- One resident, one block, inside the first forty seconds.
- Show real pages, real data, their field names. No mock of internal software.
- The turn of the video is "you already do this for trees": it changes an audit into an invitation.
- The ask is small and specific, with an owner and a window.
- Pre-empt three objections in one line each: crews, data quality, "we might be wrong."
- Tone: the city authored the idea (the towing page, the transition committee); we built the instrument. Never "gaming"; say "the measure counts the hand-off; this column counts the job."
- At most four numbers spoken; each on the site with its derivation.
- End on what Monday morning looks like for one division head.

## 8. Research still needed for the pitch (selection, not collection)

- E1 and E2 outputs, in flight.
- A pitch pack of eight quotes with URLs and dates: Ben (asset management, "refining those measures", "that's where we're heading"), the mayor ("the report card residents are going to rely on"), Clifford, Price, the towing page, the transition committee, one resident account (First Alert 4, 24 Jul 2026, saved copy). All already in `research/chapters/R3-voices.md` and `research/mayors-office-voice.md`.
- The baseline table (done-by-promise per service; overdue per division) from E3's registered figures.
- Not needed: more sentiment research. The 53 statements exist; the job is choosing eight.

## 9. Timeline to Thursday 5:30 p.m.

- Tonight: E1 and E2 report by 6:30; E3's first screen by 8, finish by midnight. Orchestrator drafts script v2 and the README memo from this architecture, filling figure ids as E1–E3 land.
- Thursday morning: Jack reviews the screens and the script; record; README final; publish a clean repository from an allowlist; one-page note to Ben; submit by about 4 p.m. to leave margin.
