# README as the memo: outline (to replace `deliverable/README.md` on Thursday)

Drafted 14 Oct 2026, about 3:35 p.m. Central, from `context/PITCH-ARCHITECTURE.md`. The README is the long-form argument a judge or a CityStat analyst reads after the video. Every number carries its figure id and label; every section says what is proven, inferred or a bet. Target: 1,500–2,000 words plus tables; the site holds the detail.

## 0. In three sentences
The city manages requests, not jobs: a 311 request closes at the hand-off, the work order usually isn't attached, and CityStat grades the close. One division already attaches work orders and the public page already shows them. Four rules in the system the city owns, plus one saved-search dashboard, close the loop; here it is on the city's data today.

## 1. What the city asked for, and what this answers
Ben's written question 5 (CityStat), problem set 3 (dumping: the alley-debris measure and repeat blocks), problem set 1 (approved plantings; city-owned lots), Mike's implementation test. Table from the pitch architecture, section 6.

## 2. The problem, with the city's own numbers (Situation and Complication)
- CityStat restated: the nine measures, published vs done-only (R1 table). Figure ids.
- Promise grading across 103 types: 57.8% closed by promise, 19.5% done by it (N4).
- The traced fates: 3,640 hand-offs, 85 / 18 / 50 (median 28 d) / 32 (R1). Planting, sidewalks, trimming (R2, Cityworks).
- The queue: open past promise, by division and age (E3 figures), with the Cityworks corroboration.
- The city's own words: towing page, Clifford, transition committee, Price, Jonsson on asset management (R3; eight quotes with URLs).
- One block: the lot (N5), at block level.

## 3. Where the chain breaks (the diagnosis)
- The request-to-work-order link is unused for most services: `WONeeded` 8 of 19,291; E1's attach rates per service (table); no request id on work-order searches.
- What it is not: closing early (kept-open requests fare worse); resident behaviour (re-reports are not a completion signal); crew speed by ward (no gap where the words say done). Each with its negative result.
- Kepner-Tregoe one-liner: the IS/IS-NOT points at a missing link, not a change.

## 4. The fix: four rules in the system the city owns
- Rule by rule, with the Cityworks mechanism E2 names (attach; status on work-order close; promise on the job; the saved search and its publication as a feature service).
- The saved-search definition and the SQL, verbatim, with field names.
- Forestry already does rule 1; the city already wrote rule 2 for towing; Chicago keeps the request open until the last work order closes (E2, observed in the OIG audit).

## 5. What it looks like: the three surfaces
- The queue dashboard (capture; what each tile is; the map at block level).
- The public status page, before and after (capture; what changed and why).
- CityStat with the done column (capture).
- What is reconstructed and what is real, stated plainly.

## 6. Adoption: who does what, and when
- Owners: ITSA (configuration; cloud migration FY2027; three analyst posts), the CityStat analyst (the weekly run; the column), division heads (attach at hand-off; work the list), the cabinet (the weekly review).
- 30/60/90 plan.
- What it costs: no licences; analyst hours; no AI (ITSA policy 2026-001).

## 7. How we will know: the baseline
- Table as of 13 Oct 2026: done-by-promise share per service; overdue count per division; attach rate per service (E1). The same SQL re-run in 90 days.

## 8. Risks, said plainly
Crews at 60%; data quality (1,750 finishes before initiation); gaming (close without work; the field check); privacy (block level); what we did not build (surveillance for dumping; canopy) and why.

## 9. What did not hold
The seven negative results that shaped the entry, from `deliverable/negative-results.md`, in two sentences each.

## 10. Method and provenance
- Data: the open 311 file; the Forestry ledger; the board-up layer; planting layers; Cityworks saved searches and the public status pages, read with the City's permission (`context/AUTHORISATION-NOTE.md` wording).
- AI as the method, none in the product.
- Reproduce: `run_all.sh`, about 20 s; figures with derivations; choices and negative results logged.

## 11. Precedents (E2)
Cities that publish completed-versus-closed or overdue by department; what Cityworks supports; what none of them does (done against promise per request type).

## Appendix. A separate finding: first-step waits by ward (N3), unchanged, with its caveats.
