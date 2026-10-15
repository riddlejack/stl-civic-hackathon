# Brainstorm: what the city already has, what the ideal looks like, and what we should build

Written Wednesday 14 October 2026, about 2:50 p.m. Central, after Jack paused the build to ask: what if they already have a job-tracking system? Labels: **observed** (checked directly), **reported** (a source says so), **inferred**, **unverified** (my background knowledge, needs a check before use).

## Summary

They do have a job-tracking system. It is Cityworks, in use since 2009 at about $220k a year, and it already links work orders to requests and shows them on the public 311 status page, for some services. Ten public status pages checked today (observed): the two tree requests closed "removal work order created" and the one cave-in "added to sewer lateral repair program" show a "Related Items: inspections and work orders attached to this request" panel with 3 to 5 items; the two cave-ins "referred to street maintenance", the two potholes "work completed", the two weeds "on schedule to be cut" and the one open cave-in show no panel and a count of 0. In the city's active queue, the request-side "work order needed" flag is set on 8 of 19,291 open requests (observed). So the loop is closed where a division chose to close it (tree removals, the sewer lateral programme) and open for most of what residents report.

That changes the entry's job. It is not "build a tracker." It is: show the loop is open for most services and what that costs, specify the switch inside the system they already own, and supply the reporting layer that falls out once it is closed, running today on their exports. The thing they do not have, and that nobody else at this hackathon is building, is a cross-division, request-level "done against promise" view and an overdue queue that spans divisions.

## 1. What the city already has (observed unless marked)

| Thing | What it does | What it does not do |
|---|---|---|
| **Cityworks** (Trimble; ITSA; since 2009; about $220k/yr, `research/parts/E-stl-city-it.md`) | Holds both service requests and work orders. 87 saved searches, mostly Forestry queues ("30-Day Removals - All City - New", "Dispatch Stump WOs", "Tree Trim Within 1 Year"). Work orders carry actual finish dates. Requests carry promise dates, dispatch timestamps and a `WONeeded` flag. | The request-to-work-order link is used by Forestry for removals and by the sewer lateral programme; `WONeeded` is set on 8 of 19,291 active requests; no saved search returns a request id on a work order; `Completed=1` sits on 9,165 requests 311 still shows open; 1,750 Forestry finishes predate their order. |
| **Public 311 status page** (`check-service-request.cfm`) | Per request: status, closed date, investigation date, resolution words, "Dept Response Due By" (the promise), and a "Related Items" panel listing attached inspections and work orders when any exist. | For cave-in referrals, potholes and weeds, no items are attached, so the page ends at the hand-off. The panel loads from a `a disallowed path ` endpoint that robots.txt disallows, so we read only its count. |
| **CityStat** (Mayor's Office; Tableau; one research analyst builds the dashboards; reviewed weekly by the cabinet, reported) | Quarterly on-time shares for nine 311 measures, by quarter filed, closed requests only. Ward chart of days to close. | Counts the close, not the work; pages last updated 30 June; no per-request or weekly view; no "done" column; no overdue list. |
| **Forestry per-lot log** (reported: CityStat page and the programme manager, Jul–Aug 2026) | Planned: log each lot visit and status on rotation. | Not found published by 13 Oct. |
| **Towing closure rule** (reported: CityStat towing page) | Planned: close tow requests only once the vehicle is towed. | One service; not yet in effect in the file. |
| **STL Recovers trackers** (Recovery Office; built by Public Goodness) | Parcel-level status maps for tornado demolitions, repairs, trees. | Tornado programmes only; status without expected dates. |
| **Executive Order 96** (11 Jun 2026) | Orders an asset management programme and a central performance dashboard. | Undated; not built. |
| **Transition committee** (Jul 2025) | Recommended "audit previously closed requests to ensure action was taken." | A recommendation, not a commitment. |

Inferred: the city's problem is not missing software or missing data. It is that one division closed the loop and the others did not, and nothing above the divisions reconciles requests against work or ranks what is overdue.

## 2. The ideal system, if we had every door open

Who decides: the COO and the CityStat team, who set closure rules and CityStat definitions. Undesired result today: the request closes at the hand-off, the work order (if any) is unlinked, the promise date dies with the request, the overdue backlog is invisible above the division. Desired result: every request is tied to its job; the job carries the promise; "closed" means finished; the overdue list is ranked and owned; CityStat counts finishes.

The end state is four rules in the system they own, plus one report:

1. **Every hand-off attaches a work order** (or an existing one). Forestry removals already do this.
2. **The request's status follows the work order.** Close on actual finish, not on hand-off. The towing rule, for every service. Cityworks supports linked-request status updates natively (unverified; confirm the setting name).
3. **The promise date rides on the job.** Overdue means past promise with no finish, whether the request is open or closed.
4. **The overdue list is worked oldest-first by each division, and seen weekly by the cabinet**, at block level on a map.
5. **CityStat and the public page report "done by promise"**, and the resident's status reads "with Forestry since 2 July, promised 30 September" instead of "closed."

What that gets residents: fewer jobs that vanish at the hand-off (a third of mowing hand-offs show no cut), a status that means something, and crews pointed at the oldest promises rather than the loudest callers (Chicago moved tree trimming from complaint-driven to area-based and tripled trims, reported). What it gets the mayor's office: CityStat numbers that survive scrutiny, one list per division, and a defensible answer to "why is it past the completion date."

## 3. What other cities did (from R3, observed unless marked; to be extended by a research thread)

- **Chicago, Inspector General, Feb 2026:** the public sees only the first work order's target; residents are frustrated by "complete" with no work apparent; recommendation to show the full chain. **Chicago weeds, 2020:** complaints closed at citation with no outcome field; fix stalled; contractor later given weekly lot lists.
- **Chattanooga, 2022–23:** "completed" meant a work order existed; fix still not in place a year later.
- **Dallas, Apr 2026:** a transferred request is "closed and considered complete."
- **New Orleans, 2022:** 34% of closed pothole requests closed by referral with no tracking of the repair.
- **Boston:** residents shown a photo of the finished job filed 59.8% more requests and trusted the city 14% more.
- **Unverified, worth a check:** Houston's 311 dashboard publishes overdue counts by department; San Antonio reports an on-time closure rate; Baltimore's CitiTrack links 311 to work orders; Cityworks has a configuration that updates the request when linked work orders close.

The pattern: auditors keep finding the same gap, the fix is "record the outcome and link the work," and it stalls when nobody owns the list. Nobody in the set publishes a request-level "done against promise" measure across divisions. That is the open niche.

## 4. What they would actually use, and what they would not

**Would use (inferred from their own words):** the restated CityStat numbers (the COO launched CityStat and reviews it weekly); the overdue list per division (the Streets director asked for "a platform that will assist us in bringing together the service request information… real-time access to performance data"; the Forestry commissioner has the data and no analyst); the towing rule generalised (they already wrote it); a per-request status that answers "why is it past the completion date" (the 311 director's words).

**Would not use:** a parallel tracker that duplicates Cityworks; anything that needs new licences or hires; a public tool that exposes addresses; a dashboard with no owner; an AI component inside city systems (ITSA policy 2026-001).

## 5. Shape options

| Option | What the submission is | Adoption odds | Risk |
|---|---|---|---|
| **A. The switch** | The audit (loop open for most services, with the attached-items test per service), the four rules inside Cityworks, the cost of leaving it open (traced fates, CityStat restated, the queue). A memo with evidence. | Highest: it asks them to use what they pay for | Reads as consulting, not a build; Mike wants something "open source and already built" |
| **B. The reporting layer** | DoneStat reframed: the overdue queue by division with a map, the done-by-promise column, the receipt, all running on exports today; the SQL handed to CityStat. | High if the CityStat analyst runs it; it is the report the switch would produce | "So what" unless paired with the rules and an owner |
| **C. Resident-facing** | Honest status and a public overdue map; answers Ben's question 5 and Mike's community angle. | Medium: residents cannot adopt it; the city must publish it | Exposure concerns; no mechanism to get work done |
| **D. A + B, with C as the public face** | "You already own the tracker. One division uses it. Here is the proof, the cost, the four rules, and the report you would see once the loop is closed, running on your data today." | Highest combined: a cheap ask with a built artefact | Two minutes is tight; needs one number, one case, one screen |

My recommendation is D, with B as the thing on screen and A as the ask. The video's spine: one number (CityStat 79% vs 15% done), one case (the lot, with the public status page that stops at "on schedule"), one proof the fix exists (the tree page with work orders attached), one screen (the overdue queue by division, oldest first), one ask (attach, close on finish, run the list for a quarter).

## 6. What to test before committing (discriminating, cheap, in order)

1. **Linked rate per service, from the public status page.** Sample 30 to 50 requests per hand-off type (about 20 types), read only the attached-items count, store request id and count, no address. One request per second; the page is allowed by robots.txt, the `a disallowed path ` endpoint is not and is not touched. Result: a per-service table "work orders attached: yes/no" that proves where the loop is open. This is the test that makes the entry's claim precise. About an hour of machine time.
2. **Cityworks' own setting.** Confirm from Cityworks documentation (public) that a linked request can be set to update or close when its work orders close, and what it is called. Half an hour of reading. Turns rule 2 from a proposal into "turn on X."
3. **Other-city precedents.** Verify the four unverified items in section 3 and find any city that publishes done-against-promise. One research thread, two hours, with URLs and labels.
4. **The queue figures, second pass.** Recompute the open-past-promise counts (public file: 14,902 filed since 2025, 6,724 over six months; QE18: 10,094) by an independent route and register them.
5. **The ask to Ben, through Mike.** One question: does the city intend to attach work orders to every service's requests, as Forestry does for removals?

Tests that would change the shape: if (1) shows most hand-off types already have work orders attached (not what ten pages suggest), the problem narrows to "close on finish" alone; if (2) shows no such setting exists, rule 2 becomes a nightly SQL job rather than a configuration.

## 7. How to run it from here

Jack keeps this thread for orchestration and decisions. Execution goes to fresh Opus threads, one per piece, each with a brief that names files, method, labels and what done looks like:

- **Thread 1: linked-rate test** (section 6, item 1), writing `research/status-page-linkage.md` and its facts CSV, block-level or no-address outputs only.
- **Thread 2: precedents and Cityworks setting** (items 2 and 3), writing `research/precedents-closed-loop.md`.
- **Thread 3: the queue screen** (item 4 and the site rework), only after 1 and 2 report, so the page says "linked" where it is true.

Nothing is started until Jack says so.

## 8. The demo: inside Cityworks without cloning Cityworks (added about 3:00 p.m.)

Jack asked whether a digital clone of Cityworks with "our new tab" is feasible, whether what we saw is the employee view, and what the ideal demo looks like from Ben's seat.

**Which view is which (observed).** The status page we read is the resident view (the city's own CommonSpot page, with a Related Items panel fed from Cityworks). Employees use Cityworks AMS itself: a staff login at `service.stlouis-mo.gov`, version string 2025.01.29, in use by all operating departments since 2009, moving to the cloud in FY2027 (reported, May 2026 hearings). We do not have the city's internal screens. We do know how staff work in it: by saved searches. The 87 saved searches are their queues, and 29 of the 51 on disk are Forestry's ("Dispatch Stump WOs", "30-Day Removals - All City - New", "Tree Trim Within 1 Year"). In Cityworks, an employee's "tab" is a saved search.

**Why not a clone.** A pixel copy of the vendor's interface would be a mock-up of internal software we cannot see, which Jack ruled out on Tuesday night for good reason; it would add nothing Ben can act on; and it would irritate the people who own the system. It is also unnecessary.

**The better idea: integrate at the three surfaces we actually have, all real and all theirs.**

1. **Cityworks saved search plus a geoportal dashboard.** The overdue queue is a saved-search definition written in their field names against their request layer (`PrjCompleteDate` before today, not closed, grouped by division; a second search for requests closed at a hand-off with no attached work order). Cityworks publishes saved searches as feature services through its Query Engine, and the city already builds public maps straight from those (the ARPA sidewalk map reads QE layers 19 and 20; the Pothole Report Map reads Cityworks services). So the "new tab" is: one or two saved searches in Cityworks, and an ArcGIS dashboard on `geoportal.stlouis-mo.gov` fed by them. We demo the dashboard on the real QE data we hold, with the layer ids and field names shown, so a city GIS analyst can rebuild it in an afternoon.
2. **The public status page, before and after.** We have the real page. Before: "Status: Closed · Referred to street maintenance for repair work to be scheduled." After: "With Street Maintenance since 27 July · promised 30 July · work order open · 78 days past promise." The page already renders attached work orders for trees, so "after" is the page doing for every service what it does for trees today. A legitimate clone, because it is public and we hold its HTML.
3. **CityStat with the done column.** Already rebuilt within 0.2%; the added column is the measure the switch would move.

**The ideal two minutes from Ben's seat.** Open on his own number (alley debris, 78.6% on time; 15% done). Click into a real request at block level: the public page stops at "referred." Click a tree request: the same page shows the work orders, because Forestry attaches them. "Your system already does this. One division turned it on." Then the queue dashboard: today's overdue by division, oldest first, on the map. Then CityStat with the done column. Then the resident story (the lot, 36 neighbours cut, none here). The ask: attach a work order at every hand-off, close on finish, run the list for one quarter, as part of the cloud migration ITSA has already scheduled. The measurable improvement is defined and baselined today (done-by-promise share per service; overdue count per division, as of 13 October) and re-measured with the same SQL in ninety days.

**Do we need more on how the city uses Cityworks?** Enough for the shape. Three gaps are cheap and worth closing, in this order: (a) the attach rate per service from the public status page, so the register says "linked / not linked" with evidence; (b) Cityworks' public documentation on linking requests to work orders and updating request status on work-order close, so rule 2 is "turn on X" rather than "build X"; (c) one question to Ben: who creates work orders today, CSB or the department. What we cannot get and do not need: internal screens and workflows.

**Other considerations.** The FY2027 cloud move is the window to ask for configuration changes. ITSA's three new data-analyst posts and the CityStat analyst are the natural owners. ITSA's AI policy means the product stays SQL and saved searches. Block level everywhere in public. We cannot create an ArcGIS Online account to host a live dashboard (Jack's to do, optional); the honest substitute is our site's dashboard page built to the geoportal's layout with the real layer ids, labelled as a prototype.

## 9. Decision log

- **14 Oct, about 3:05 p.m.:** Jack chose the three-surface demo (section 8) as the direction. Briefs written: `prompts/exec/E-COMMON.md`, `E1-status-page-linkage.md`, `E2-precedents-and-cityworks.md`, `E3-three-surface-demo.md`. E1 and E2 are research and write only their own files; E3 builds the site. They do not share files, so all three can run at once; E3 reads E1's linkage table if it exists at build time and otherwise shows "not yet tested". Nothing started until Jack says so.
