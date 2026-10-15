"""N9 seed: deliberate choices recovered from the project files and session transcripts.

One entry per choice. Fields follow prompts/night-v2/N9-decisions-and-derivations.md:
  id, category, decision, why, evidence, alternative_rejected, shows_up_in, strength
plus provenance fields: decided_by, when, status, top10 (rank in the "ten choices" list).

Labels inside `why`: (observed) checked directly by this project; (reported) a source
says so; (inferred) our conclusion. Times are Central (CDT) on 13 Oct 2026 unless noted.
build.py merges this list with build/N*/decisions.json and writes build/out/decisions.json.
"""

DECISIONS = []


def D(id, category, strength, decision, why, evidence, alternative_rejected, shows_up_in,
      decided_by, when, status="in force", top10=None):
    DECISIONS.append(dict(
        id=id, category=category, decision=decision, why=why, evidence=evidence,
        alternative_rejected=alternative_rejected, shows_up_in=shows_up_in,
        strength=strength, decided_by=decided_by, when=when, status=status, top10=top10,
        sources_merged=["N9 seed (project files and transcripts)"],
    ))


# ---------------------------------------------------------------- privacy
D("privacy-block-level", "privacy", "strong",
  "Every public output shows locations at block level (house number rounded down to the hundred block), never a house or lot address, including the hero lot in the video.",
  "Jack's ruling, about 11:50 p.m. on 13 Oct, after the orchestrator proposed an exception for city-owned (land bank) lots: he preferred blocks to a specific house everywhere. The rule predates the ruling (T-COMMON: 'Report nothing below block level on any public-facing output'). Nobody private can be pinpointed, and the claim does not need more precision than a block.",
  ["prompts/night-v2/COMMON.md (Rules: 'Public outputs: block level or coarser, including the hero examples')",
   "prompts/overnight/T-COMMON.md (Rules)",
   "context/NIGHT-PLAN.md decision 4 (default was parcel level for LRA lots)",
   "session transcript 1bc71fad, 13 Oct about 11:43-11:50 p.m. (proposal, Jack's reply, ruling recorded)"],
  "Parcel-level display for land-bank (LRA) lots only, proposed as the default in NIGHT-PLAN decision 4 because no private owner is exposed; and address-level display everywhere.",
  ["site: receipt, Monday list, dumping page", "video: opening lot", "README: privacy line"],
  "Jack", "13 Oct about 11:50 p.m.", top10=5)

D("privacy-aerial-no-marker", "privacy", "moderate",
  "Aerial images frame the whole block with no marker on the lot; any parcel-level image or address is kept in build/N5/private/ for Jack only.",
  "Follows from the block-level ruling: an image centred on a lot with a pin is an address by other means.",
  ["prompts/night-v2/N5-hero-cases.md (Display rule)", "prompts/night-v2/COMMON.md (Rules)"],
  "Centre the image on the hero lot with a marker, as a receipt would naturally do.",
  ["site: receipt card image", "video: opening shot"],
  "Jack (ruling) / night-v2 orchestrator", "13 Oct about 11:55 p.m.")

D("privacy-no-personal-fields", "privacy", "strong",
  "No personal fields enter the pipeline: fields about people (owners, staff, contacts) are dropped from every file when it is loaded, not when pages are drawn. The 311 file itself has no requester identity.",
  "The entry's argument is about trust, and the demo must show no personal data (firm requirement F3; tree leaf 4.2). The data audit observed that the 311 file carries no requester identity, while some other files the pipeline reads carry fields about people (observed).",
  ["research/data-audit.md section 2 (CSB: 'No requester identity in the file')",
   "prompts/overnight/T-COMMON.md (Rules: No personal data)"],
  "Load the raw files whole and filter at display time.",
  ["pipeline: N1 load scripts", "site: Methods", "README"],
  "synthesis session (T-COMMON)", "13 Oct about 10:50 p.m.", top10=5)

D("privacy-exposed-tables-unused", "ethics", "strong",
  "Personal data we came across in city-hosted data while auditing it is not used in any form, not even aggregated or anonymised.",
  "Jack asked whether such data could be used the way a responsible company uses anonymised data, to show that unmet requests change how households engage. The synthesis rejected it: the city's AI policy says 'Do not input sensitive or regulated data', any such use falls under the surveillance ordinance, the entry's argument is trust, and every finding is already aggregate and address-free, so the data is also unnecessary.",
  ["research/synthesis.md section 9d", "context/JACK-INPUTS-synthesis-thread.md section 6 (the question)",
   "ITSA IT Policy #2026-001, https://www.stlouis-mo.gov/government/departments/information-technology/documents/upload/Artificial-Intelligence-Policy-2.pdf (observed by research thread C)",
   "Ordinance 71842 (surveillance technology), https://www.stlouis-mo.gov/government/city-laws/ordinances/ordinance.cfm?ord=71842"],
  "Anonymised, aggregate use of that data to link service failures to residents.",
  ["README: privacy line", "site: Methods", "write-up"],
  "synthesis session, after Jack's question", "13 Oct about 10:40 p.m.", top10=5)

D("ethics-private-disclosure", "ethics", "strong",
  "Raise exposed data with the city privately, through the hackathon organiser, and describe it nowhere in public. The only public line: 'A private note about exposed data is being raised with the city through the hackathon organiser.'",
  "Describing what is exposed, even in general terms, would point others at it before the city can act; staying silent would leave it exposed. A private note is a good-faith act the office can act on. Only metadata and counts were ever read. The note is drafted and is Jack's to send; it had not been sent as of 14 Oct about 01:00, so no public text may say it was sent.",
  ["context/disclosure-draft.md (private; not for publication)", "research/chapters/N8-verification.md finding 3"],
  "Describe the exposure in the public write-up, site or video; or say nothing to the city.",
  ["site: Methods (the one line)", "README (the one line)"],
  "synthesis session; Jack sends", "13 Oct about 10:55 p.m.; public wording fixed 14 Oct about 01:05", status="drafted, NOT sent; Jack's to send, then update the one public line")

D("ethics-no-encampment-points", "ethics", "strong",
  "No map, list or count by location of 'Tent Encampment' or 'Homeless Call' requests, ever; Ben's unhoused problem set is not built.",
  "Both codes exist in the 311 file (262 and 219 rows in 2025-26, observed), so a location tool could be made, but it would map where people sleep (tree branch 7.2, exposure). The other half of the ask, shelter-bed availability, has no data to show (fails F3).",
  ["research/synthesis-notes.md 'Checks after Ben's document' (codes and counts)",
   "research/synthesis.md sections 2n and 7b", "prompts/night-v2/COMMON.md (Rules: 'No encampment or homeless-call points, ever')"],
  "A location and outreach-targeting tool for Ben's problem set 2 built from those 311 codes.",
  ["site: register (shelter row says no record exists)", "README: what it does not fix"],
  "synthesis session", "13 Oct about 10:10 p.m.", top10=6)

D("ethics-decline-perpetrators", "ethics", "strong",
  "Decline the 'identify and track down perpetrators' half of Ben's illegal-dumping problem set, and say so on the page; deliver repeat sites at block level and what happened after each report instead.",
  "Identifying people is surveillance under tree branch 7.2 and any city use of surveillance technology needs the Board of Aldermen after a public hearing (Ordinance 71842, effective 6 May 2024, observed). Cameras catch few offenders where tried: Oakland cited 13% of 457 recorded incidents (reported, KGO-TV, 5 Aug 2024). The 311 file already codes enforcement outcomes ('summons issued' 458, 'not enough evidence' 298, 'cleared by arrest' 267, observed), so the useful half needs no new watching.",
  ["context/BEN-PROBLEM-SETS.md problem set 3", "research/synthesis.md sections 7d and 9g",
   "research/demand-and-existing-tools.md (Oakland row, https://abc7news.com/ via KGO-TV)",
   "https://www.stlouis-mo.gov/government/city-laws/ordinances/ordinance.cfm?ord=71842",
   "research/synthesis-notes.md 'Checks after Ben's document' (dumping outcomes)"],
  "A perpetrator-identification or camera-placement tool, which is what the problem set asks for first.",
  ["site: illegal dumping page (the declining paragraph)", "README", "video: possibly one line"],
  "synthesis session", "13 Oct about 9:45 p.m.", top10=6)

D("ethics-electorate-framing-only", "ethics", "moderate",
  "Election, survey and demographic material is used only as framing, never as evidence that service failures cause anything about residents or votes; no request is linked to a person or household attribute.",
  "Nothing in the data can support causation about votes or demographic harm, and individual-level linkage would need personal data the entry refuses to use. The 2025 race being reported as decided on basic services, and the city's own line that how well CSB works 'is directly tied to trust', are context only.",
  ["research/synthesis.md section 9c ('What it cannot claim')", "context/HANDOFF-2.md section 1 ('The electorate material is framing only')"],
  "A heat map tying unmet requests to older residents or to turnout, which Jack floated as a way to show impact.",
  ["video narration", "README", "progress report"],
  "synthesis session", "13 Oct about 10:40 p.m.")

D("privacy-layers-not-downloaded", "privacy", "minor",
  "During the data audit, layers whose only extra content was personal were deliberately not downloaded, and no POST forms, keys or sign-ins were used.",
  "Personal fields with no analytic need; the audit's rule was metadata only where personal data appeared.",
  ["research/data-audit.md (regional section)", "session transcript 81405052, 13 Oct about 7:30-7:35 p.m. (worker reports)"],
  "Download everything keyless and sort it out later.",
  ["write-up: data note"],
  "data-audit thread", "13 Oct about 7:30 p.m.")

D("privacy-aggregate-exports", "privacy", "moderate",
  "Request-level rows stay in the local database; public exports are aggregated to type x ward x quarter, plus block-level receipts for a curated sample.",
  "Address-level joins are needed to compute (request to parcel to ledger cut), but nothing below block level may leave the build.",
  ["context/BUILD-SPEC.md (Data layer: 'request level stays in the database')", "prompts/night-v2/N1-pipeline.md steps 4-5"],
  "Publish the joined request-level table so others can re-run the analysis.",
  ["pipeline: build/out exports", "site: downloads"],
  "synthesis session (spec)", "13 Oct about 11 p.m.")

# ---------------------------------------------------------------- adoption
D("adoption-no-ai-in-product", "adoption", "strong",
  "AI is the method, not the product: AI helped one person audit the files and draft the closure-text classes, but the product itself runs no AI. It is plain SQL, Python and DuckDB with template text.",
  "ITSA IT Policy #2026-001 (23 Jul 2026, observed) prohibits 'Use of any AI tool that has not been approved by ITSA'; approval needs a business case, costs, a procurement method, a data-retention plan and staff AI training, and AI output may not be published without human verification. A product with no model in it can be run by the city without that approval, and a person can check every output.",
  ["https://www.stlouis-mo.gov/government/departments/information-technology/documents/upload/Artificial-Intelligence-Policy-2.pdf",
   "research/mayors-office-voice.md section 5 (AI)", "research/what-gets-adopted.md section 3.3",
   "context/NIGHT-PLAN.md 'What changes' item 4", "session transcript 1bc71fad, about 11:50 p.m. (Jack: a built-out system that does not rely on AI to be maintained)"],
  "An AI chatbot, summariser or classifier running inside the product (the obvious move at a 'Civic AI' hackathon), which would need ITSA approval before any staff use.",
  ["video: one line", "site: Methods", "README: how AI was used"],
  "night-v2 orchestrator; Jack (default accepted)", "13 Oct about 11:37 p.m.", top10=1)

D("adoption-reviewable-classes", "method", "strong",
  "The one AI-assisted step, classing the city's closing text, is delivered as a reviewable rule table (problem code, exact closing text, class, count, rule or judgement) that SQL applies; a person can read and overrule every line.",
  "Keeps the product AI-free at runtime and is how the policy's 'treat AI output as a draft' clause is met. It also lets the CityStat team disagree with a class without touching code. N2's Python and SQL versions agree on all 2,992 type-and-text pairs, and N3's independently written rules agree with N2 on 98.4% of closures (observed); no person has reviewed the table yet.",
  ["research/chapters/N2-closure-classes.csv", "prompts/night-v2/N2-what-closed-means.md step 1",
   "build/N2/figures.json notes ('drafted by an AI model and open for review')", "research/chapters/N2-what-closed-means.md Admission",
   "build/out/figures.json n3_class_agreement_n2_vs_n3"],
  "Classify closures with a model at run time, or by opaque keyword rules nobody reviews.",
  ["site: Methods (download the class table)", "README"],
  "night-v2 orchestrator (N2 brief)", "13 Oct about 11:35 p.m.",
  status="in force; open to review, not yet reviewed by a person (ten distinct texts carry about 60% of hand-off closures; about 40 type-and-text pairs for a per-type review, N8)", top10=3)

D("adoption-sql-and-definitions", "adoption", "strong",
  "What the city adopts is the SQL and the definitions, not our hosting: deliver files the CityStat team could run without our code or our servers.",
  "Precedents show adoption follows output that drops into a routine the city already runs, using data it already holds (research E). The project's lesson: 'One owner, one ask: the city adopts links into its own routine, not apps.'",
  ["context/HANDOFF-2.md section 7 (last lesson)", "research/what-gets-adopted.md section 3.6 and E.1 patterns",
   "prompts/night-v2/COMMON.md (entry paragraph)"],
  "A hosted app the city would have to procure, host or depend on us to run.",
  ["README: how the city would run it", "site: Methods (SQL downloads)", "video: closing ask"],
  "synthesis session", "13 Oct about 11 p.m.", top10=9)

D("adoption-enhancement-route", "adoption", "strong",
  "Build only on files the city already publishes and on free tools (Python, DuckDB), so that running it needs no new licence, no purchase and no new hire.",
  "The city's IT governance page routes a request that 'uses only existing software licenses and hardware' and can be done by existing staff to an ITSA team as an enhancement, not to the IT Project Governance Committee; requiring procurement triggers committee review whatever the price (observed). The research thread's judgement: the shortest documented route is a department sponsor plus the CityStat team on data and licences the city already holds (inferred).",
  ["https://www.stlouis-mo.gov/government/departments/information-technology/governance/index.cfm",
   "research/parts/E-stl-city-it.md (Project Request Form, 'No, uses only existing software licenses and hardware')",
   "research/what-gets-adopted.md sections 3.2 and 3.6"],
  "A tool on a commercial platform or paid API, which would make it a procured 'strategic project'.",
  ["README: how the city would run it", "write-up: adoption section"],
  "synthesis session", "13 Oct about 9:45 p.m.", top10=9)

D("adoption-no-new-staff", "adoption", "strong",
  "No new staff is a firm requirement: the users are people the city already employs (the CityStat programme manager and research analyst, ITSA's analysts), and the pipeline replaces hand assembly rather than adding work.",
  "Jack: 'having to hire ppl is a huge downside/barrier to implementation.' The city's capacity is thin: 20.7% of 6,420 budgeted positions vacant; Forestry at about 60% of seasonal mowing staff (reported).",
  ["context/HANDOFF.md section 2", "context/question-standard.md F1",
   "research/pressures-next-six-months.md (capacity)", "research/what-gets-adopted.md section 3.3"],
  "A programme or tool that needs a new post, volunteers with no base, or contract labour.",
  ["README", "write-up", "video: 'no new staff'"],
  "Jack", "13 Oct about 8:15 p.m.")

D("adoption-free-under-threshold", "adoption", "moderate",
  "Running cost is effectively zero (free tools, public files, a weekly job), comfortably under the $2,500 per-transaction line below which no bids are needed.",
  "Purchases up to $2,500 need no bids or advertising since March 2026 (observed); cost questions in the city's templates are about staff hours and recurring cost (observed).",
  ["research/what-gets-adopted.md section 3.2", "research/synthesis-notes.md E.3"],
  "Paid imagery, a hosted database or a SaaS dashboard.",
  ["README", "write-up"],
  "synthesis session", "13 Oct about 9:45 p.m.")

D("adoption-answer-question-5", "scope", "strong",
  "One entry with one owner and one ask: answer Ben's written design question 5 ('how can the city better communicate how we're doing on delivering key city services?') with data instead of a mock-up, and make the other findings its pages rather than separate apps.",
  "Ben's written document (received about 9:35 p.m.) put CityStat on his list as written, invites the critique, and dropped hazard trees. Three apps would be three adoption asks and three stories in two minutes. Most entrants were expected to answer question 5 with a design mock-up (inferred).",
  ["context/BEN-PROBLEM-SETS.md (question 5)", "research/synthesis.md sections 7b-7d"],
  "Several separate tools (mowing, 311, trees, sidewalks), which Jack first proposed given abundant compute.",
  ["site structure", "video: framing", "README"],
  "synthesis session, accepted by Jack ('This sounds good as a first read')", "13 Oct about 9:45-10 p.m.")

D("adoption-weekly-bulk-file", "data source", "moderate",
  "The pipeline reads the city's weekly bulk files (csb.zip and the forestry ledger under /data/upload/data-files/) rather than the 311 API.",
  "The CSB Open311 API needs a city-issued key and returns HTTP 400 without one (observed); the bulk path is allowed by the city's robots file and the 311 file was refreshed the same day (observed).",
  ["research/data-audit.md 'Read this first' items 2 and 4; section 2 (CSB ds 5)",
   "https://www.stlouis-mo.gov/data/upload/data-files/csb.zip"],
  "A live API integration (needs a key the city issues on request; Jack's to request, not ours).",
  ["pipeline: N1 run_all.sh", "README: how the city would run it"],
  "synthesis session (spec)", "13 Oct about 11 p.m.")

D("adoption-open-source-mit", "adoption", "moderate",
  "Release the code openly under the MIT licence, deployable as built.",
  "Mike at the kickoff named 'open source and already built, that they can deploy' as 'even better' (observed in the transcript excerpt); this became weighed item W9.",
  ["context/question-standard.md section 13 (W9)", "context/BUILD-SPEC.md acceptance test 5"],
  "Keep the code private and show only the demo.",
  ["README", "site: Methods"],
  "synthesis session", "13 Oct about 9 p.m.", status="provisional: public hosting is Jack's call")

D("adoption-tone-with-coo", "presentation", "moderate",
  "Pitch the layer as the thing the COO says the city is heading toward, and label every recomputed number 'our definition, from the public file' rather than saying CityStat is wrong.",
  "The COO already says 'right now we don't have a comprehensive asset management program' (30 Sep 2026) and 'That's where we're heading' (reported). CityStat's denominators are unpublished, so differences are definitional until shown otherwise.",
  ["context/HANDOFF-2.md section 4 item 5", "research/mayors-office-voice.md section 5",
   "prompts/overnight/T-COMMON.md (CityStat goals: 'our definition, from the public file')"],
  "An audit framing ('the city's numbers are wrong'), which invites defensiveness from the office that would adopt it.",
  ["site: scoreboard labels", "video narration", "README"],
  "synthesis session", "13 Oct about 11 p.m.")

D("adoption-questions-for-ben", "adoption", "moderate",
  "Send four questions through the organiser before claiming more: does Cityworks update the request when its work order closes; is GeoSTL's satellite mowing work in use; what denominator CityStat's on-time charts use; is the tree backlog limited by crews or by the order of work.",
  "Each answer could change the pitch: if Cityworks already propagates completion, the entry becomes 'publish it' (cheaper, not wrong); if GeoSTL delivers, mowing becomes 'the ledger they are not using'.",
  ["context/HANDOFF-2.md section 3", "research/synthesis.md sections 7e and 8f"],
  "Assume the answers and build on the assumption.",
  ["deliverable/ask-to-ben.md", "write-up"],
  "synthesis session; Jack sends", "13 Oct about 10-11 p.m.", status="drafted; Jack's to send")

D("adoption-no-public-hosting-yet", "adoption", "minor",
  "Nothing is published or pushed overnight: the baseline commit is local only, and public hosting (for example GitHub Pages) waits for Jack.",
  "Hosting is outward-facing, and outward-facing actions are Jack's (AGENTS.md boundaries). N8 also found the repository cannot be published as it stands (private folders not ignored; the baseline commit holds request and parcel ids), so publication needs a fresh repository with one clean commit.",
  ["context/NIGHT-PLAN.md decision 5 and 'Morning'", "AGENTS.md (Boundaries)", "research/chapters/N8-verification.md finding 4"],
  "Publish the prototype overnight so it is ready when he wakes.",
  ["process"],
  "night-v2 orchestrator", "13 Oct about 11:40 p.m.")

D("adoption-monday-list-one", "scope", "moderate",
  "Ship one Monday list that is useful this week (requests past the city's own promised date, open, by ward and type, block level, downloadable CSV), not a list per division.",
  "One owner, one ask; the mowing list cannot be live until April because the season is over, so it is shown as a retrospective.",
  ["prompts/night-v2/N6-site.md section 6", "context/NIGHT-PLAN.md 'What changes' item 2"],
  "Five Monday lists (mowing, trees, cave-ins, dumping, sidewalks) from the original spec.",
  ["site: Monday list"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

# ---------------------------------------------------------------- method
D("method-promise-date", "method", "strong",
  "Grade every request against the promise date the city itself sets on it (PRJCOMPLETEDATE), not against CityStat's goals or our own targets.",
  "The field is a fixed offset per request type (single light out 3 days, cave-ins 3, towing 5, residential potholes 8, alley potholes 16, illegal dumping 10, debris 3, tree inspection 14, weeds on a vacant lot 14, weeds at a vacant building mostly 90) and is filled on about 98% of rows (observed, 13 Oct about 11:30 p.m.; N1: 97.9% of 2024-26 requests, offsets identical). It is the city's own promise, so nobody can say we picked the bar; CityStat's goals rest on unpublished denominators and differ from the city's own due dates for 3 of 9 services (alley potholes 16 vs 17 days; whole-block lights 2 days vs 24 hours; critical signs 3 days vs 48 hours; observed, N4). Caveat: for vacant-lot weeds the offset is 14 days on some 2026 requests and 90 on others, so the date is shown as given (N5).",
  ["prompts/night-v2/COMMON.md correction 1", "context/NIGHT-PLAN.md 'What I checked' item 2",
   "session transcript 1bc71fad, about 11:28-11:37 p.m. (field noticed while spot-checking)"],
  "Grade against CityStat's published goals (whose denominators are unpublished) or our own guess at a reasonable time.",
  ["site: receipt ('the city's own promised date was ...')", "site: scoreboard", "video", "README"],
  "night-v2 orchestrator", "13 Oct about 11:30 p.m.", top10=2)

D("method-closure-classes", "method", "strong",
  "Read 'closed' through the city's own closing words: every closing text is classed as done, handed off (scheduled, referred, added to rotation, tagged, 'will be', sent elsewhere), converted (work order created), no action, other, or blank.",
  "Closed requests include referrals and hand-offs, not only finished work: a cave-in shows Closed with 'Referred to street maintenance for repair work to be scheduled'; the towing page itself says 'Closed' does not necessarily mean towed (observed). So a closed status, and the time it took to reach it, does not by itself say the work was done.",
  ["prompts/night-v2/N2-what-closed-means.md", "research/synthesis.md sections 1b and 8b",
   "research/chapters/N2-closure-classes.csv"],
  "Treat STATUS = CLOSED as done, which is what time-to-close (and CityStat) implicitly does.",
  ["site: landing headline", "site: scoreboard 'done by promise' column", "site: receipt", "README"],
  "synthesis session; formalised by N2", "13 Oct about 10:20 p.m.-11:35 p.m.", top10=3)

D("method-conservative-handoff", "method", "moderate",
  "Publish a conservative version of the hand-off headline that counts enforcement notices to owners (notice of violation, already under notice, warning, ticket, summons) as neither hand-off nor done.",
  "A notice is a real action but not the fix; showing both versions (35.2% and 25.2% of 2025-26 closures, observed by N2) stops the headline resting on a contestable class.",
  ["build/N2/figures.json (n2_share_closed_handoff, n2_share_closed_handoff_excl_notices)"],
  "One headline figure that counts notices as hand-offs without saying so.",
  ["site: landing ('How we know')", "README"],
  "N2", "13 Oct about 11:50 p.m.")

D("method-dedup-requestid", "correction", "strong",
  "Count requests by distinct REQUESTID, not by CSV rows.",
  "The city's CSV repeats a request once per caller: 349,031 rows in 2024-26 hold 322,104 distinct request ids, about 8% more rows than requests (observed, N2). Medians shift slightly when deduplicated (cave-ins closed 'work completed', wards 10-14: 25.1 days on rows, 23.1 on requests; observed, N5).",
  ["build/N2/figures.json (n2_csv_rows_per_request)", "build/N5/figures.json (n5_dup_requestid_rows and median notes)"],
  "Count rows, as the earlier synthesis and COMMON corrections did.",
  ["pipeline", "every 311 figure", "site: Methods"],
  "N2 found it (N5 and N3 independently); orchestrator verified; adopted for all as COMMON correction 6", "13 Oct about 11:50-11:54 p.m.")

D("method-clean-utf8", "correction", "minor",
  "Read the 311 CSVs with invalid UTF-8 bytes dropped (iconv -c into build/csb-clean/), or with encoding_errors='replace'.",
  "The city's CSVs contain invalid UTF-8 and break strict readers (observed). Dropping the bad bytes loses a few characters in free text and changes no dates, codes or ids (inferred).",
  ["prompts/night-v2/COMMON.md correction 5", "build/INTEGRATION-LOG.md (23:37 entry)"],
  "Decode as Latin-1 (silently changes characters) or fail on the bad rows.",
  ["pipeline", "site: Methods (data note)"],
  "night-v2 orchestrator", "13 Oct about 11:30 p.m.")

D("method-resident-channels", "method", "strong",
  "Fairness comparisons use resident-filed requests only (web, phone, email, chat, Twitter, letter); staff-entered requests (NSO) are excluded and 'indeterminate' is reported separately.",
  "Staff-entered requests are 18-24% of the total in wards 10-14, so part of the north-side count is inspectors' own work, which follows a different clock (observed by the synthesis session).",
  ["prompts/overnight/T-COMMON.md (Definitions)", "research/synthesis.md section 6 item 5"],
  "All channels together, which mixes inspectors' self-generated work into residents' waits.",
  ["site: fairness section", "README: definitions"],
  "synthesis session", "13 Oct about 10:35 p.m.")

D("method-like-for-like", "method", "strong",
  "Compare wards like for like: same request type, same closing class (done-class closures), resident channels, and also share done by the city's promised date counting open and cancelled requests as not done.",
  "Raw time-to-close mixes types and closing practice. Cave-ins in wards 1-5 close in a median 1.1 days mostly because their closures read 'referred ... to be scheduled' (median 0.8 days); 'work completed' takes 8.3 days there against 23.1 in wards 10-14 (observed, distinct requests, N3/N5; 9.6 vs 25.1 on rows), but only 35 such repairs are recorded in wards 1-5, so the repair gap is unproven and repair dates for referred cave-ins are in no public file; the referral step itself takes 0.8 against 41.7 days. Across all services, type mix and closing words explain only 12% of CityStat's ward 1 vs ward 10 gap (N3). N3 applied the rule to 79 types; the comparisons that survive are about first steps (towing tagged, cave-in referral, building-code notices).",
  ["prompts/night-v2/COMMON.md correction 2", "prompts/night-v2/N3-fairness-like-for-like.md", "context/NIGHT-PLAN.md item 1"],
  "Raw median days to close by ward, the measure behind the earlier headline and CityStat's own ward chart.",
  ["site: fairness section", "video", "README"],
  "night-v2 orchestrator; N3 re-derives", "13 Oct about 11:30 p.m.", top10=4)

D("method-tornado-split", "method", "moderate",
  "Split every ward comparison at the tornado (16 May 2025) and require a gap to hold on both sides before calling it robust.",
  "The tornado moved crews and requests; a gap that exists only afterwards could be recovery work. The earlier check found the gaps predate it (for example towing, resident channels: 53.2 vs 31.2 days before, 36.9 vs 9.7 after; observed, rows).",
  ["prompts/overnight/T-COMMON.md (Tornado date)", "research/synthesis-notes.md 'Impact tests' B2", "prompts/night-v2/N3-fairness-like-for-like.md step 4"],
  "Pool 2024-26, or use only the post-tornado period.",
  ["site: fairness section", "README"],
  "synthesis session", "13 Oct about 10:40 p.m.")

D("method-robust-thresholds", "method", "moderate",
  "A ward comparison is called robust only if it survives both done-class medians and share done by promise, has at least 100 requests on each side, and holds before and after the tornado; types need 300 or more resident requests since 16 May 2025 to be tested.",
  "Small groups and single measures produced headlines that fell over (the cave-in and tree gaps). Fixed thresholds set before looking keep the shortlist from being cherry-picked.",
  ["prompts/night-v2/N3-fairness-like-for-like.md steps 3-4"],
  "Report whichever comparison shows the largest gap.",
  ["site: fairness section"],
  "night-v2 orchestrator (N3 brief)", "13 Oct about 11:35 p.m.")

D("method-ward-groups", "method", "minor",
  "Summaries use ward groups 1-5 (southwest and south), 6-9 (central) and 10-14 (north), always alongside per-ward figures.",
  "Groups make small types readable; per-ward figures stop a group hiding a boundary. For cave-ins and towing the line ran between wards 1-5 and 6-14, not north against south (observed), which per-ward figures exposed.",
  ["prompts/overnight/T-COMMON.md (Ward groups)", "research/synthesis-notes.md 'Impact tests' B2"],
  "North versus south only.",
  ["site: fairness section"],
  "synthesis session", "13 Oct about 10:50 p.m.")

D("method-medians-and-survival", "method", "moderate",
  "Report medians, and alongside them a survival-style share done by the promised date that counts open requests as not done.",
  "Closed-only medians understate a gap where more requests stay open: cave-ins open 40.6% in wards 10-14 against 17.6% in the southwest (observed). Medians resist the multi-year outliers in the file. Unresolved overnight: N1 and N3 count cancelled requests as not done in the promise measure, while N4's scoreboard drops them from the denominator (many are duplicates), so the citywide figures differ (N1 50.8% closed and 16.7% done by promise; N4 57.8% and 19.5%).",
  ["prompts/overnight/T-COMMON.md (Days to close)", "research/synthesis-notes.md 'Impact tests' B"],
  "Mean days over closed requests only (CityStat's ward chart).",
  ["site: scoreboard and fairness sections"],
  "synthesis session", "13 Oct about 10:50 p.m.")

D("method-refile-durable-14d", "correction", "strong",
  "'The closure did not hold' is measured only for durable-fix types (potholes, cave-ins, lights, trees, signs) over 14 days; the broad 30-day figure is called 'came back', not false closure.",
  "Refuse is collected weekly and dumping recurs at chronic sites, so a second report within 30 days often means a new event, not a failed fix.",
  ["prompts/night-v2/COMMON.md correction 4", "context/NIGHT-PLAN.md item 3"],
  "Present 11,992 re-filed requests (6.3%) as closures that were false.",
  ["site: scoreboard", "video", "README laundry list"],
  "night-v2 orchestrator", "13 Oct about 11:30 p.m.", top10=10)

D("method-ledger-to-the-week", "method", "strong",
  "Treat forestry-ledger dates as precise to the week, not the day, and say so beside every figure that uses them.",
  "Postings are batched: 8,507 of the 2026 rows carry a Sunday date and 2,608 carry 23 April (observed). SERVICEDATE is a posting date. Any figure counted in days (the 35% cut within 30 days) carries that caveat; if challenged, lead with 'no cut billed all season' (about one in five vacant-lot requests closed 'on schedule to be cut': 21.4% of 729; a quarter if 'added to rotation' closures are included, N8).",
  ["research/synthesis-notes.md 'Impact tests' A", "context/HANDOFF-2.md section 4 item 4", "prompts/night-v2/COMMON.md (derivation example)"],
  "Read the ledger as a day-level operations log.",
  ["site: receipt ('How we know')", "site: mowing retrospective", "README"],
  "synthesis session", "13 Oct about 10:40 p.m.", top10=7)

D("method-validate-ledger", "method", "strong",
  "Before using the billing ledger as the city's cut record, check it against an independent count: parcels with a cut posted 6 April-26 May 2026 against CityStat's first mowing rotation.",
  "7,545 parcels in the ledger against CityStat's '7,099 of 12,171' for the same rotation (observed): the ledger matches at rotation level and is probably CityStat's source. A billing charge is not an operations log, so the check had to be made before the claim.",
  ["research/synthesis-notes.md 'Impact tests' A", "research/synthesis.md section 9b"],
  "Assume the ledger is a cut record because its rows look like one.",
  ["site: receipt ('How we know')", "README"],
  "synthesis session", "13 Oct about 10:40 p.m.", top10=7)

D("method-independent-record-and-falsify", "method", "strong",
  "Test every claim against an independent record before making it, and run the test that could falsify it; record the result either way.",
  "The project's working rule since the synthesis: ledger against CityStat; cancellations against work orders; re-filing after a cut against no cut; the exit test. Two tests came back negative and are kept (no exit; status text does not drive re-filing).",
  ["context/HANDOFF-2.md section 7 (lessons)", "research/synthesis.md sections 8h, 9a, 9b"],
  "Report findings from one file at a time.",
  ["site: 'What we tested that did not hold'", "deliverable/negative-results.md"],
  "synthesis session", "13 Oct about 10:20-10:45 p.m.")

D("method-knockout-admission", "method", "minor",
  "Every overnight brief carries a working hypothesis, a knock-out condition that would kill it, and asks for an admission first.",
  "A thread that can say 'my premise failed' early is worth more than one that reports around it (the one habit kept from the Stemma project).",
  ["context/HANDOFF-2.md section 7", "prompts/night-v2/N1-N5 briefs ('Knock-out')"],
  "Open-ended briefs that report whatever they find.",
  ["process"],
  "synthesis session", "13 Oct about 10:50 p.m.")

D("method-address-parcel-join", "method", "moderate",
  "Join requests to parcels by normalised address text against the MSD parcel attribute file (PID equals the city's ParcelId), with owner names dropped, and always report the match rate; below 80% for weed requests is a knock-out.",
  "The 311 file has addresses and coordinates but no parcel id; the ledger has parcel ids but no addresses. MSD's file bridges them for 134,919 city parcels (observed). Matches ran 85% for 2026 weed requests in the synthesis check (3,962 of 4,658); N1's tested normaliser and number-range step reach 90.1% (vacant lots, 2,387 of 2,649) and 93.3% (vacant buildings) for 2025-26, above the 80% knock-out (observed).",
  ["prompts/overnight/T-COMMON.md (Address normalisation)", "prompts/night-v2/N1-pipeline.md (Knock-out)",
   "research/synthesis-notes.md 'Through-line tests'", "build/N5/figures.json notes"],
  "Spatial join on SRX/SRY to parcel polygons (needs the parcel shapefile with owner fields), or no join.",
  ["pipeline", "site: Methods", "README: what is fragile"],
  "synthesis session", "13 Oct about 10:20 p.m.")

D("method-tree-match-relative", "correction", "strong",
  "Read the tree address match as a relative rate against a baseline, never as a share converted: say cancelled tree requests appear in Forestry's work orders 'about five times as often as unrelated requests'.",
  "Cancelled addresses match a one-third work-order sample at 10.8% against 1.9% for unrelated requests (observed; N1 on distinct requests: 10.9% against 1.8%), but requests closed 'work order created' match at only 6.8% (N1; COMMON's 2.4% was for all closed tree requests), so the address match misses most true pairs and cannot measure the share converted. N5 then found most matches sit on removal orders already open long before the request (288 of 345), so even 'converted' is the wrong story.",
  ["prompts/night-v2/COMMON.md correction 3", "context/NIGHT-PLAN.md item 3",
   "research/synthesis-notes.md 'Through-line tests' Test 2"],
  "'Most cancelled tree requests were in fact converted to work orders' (the synthesis wording).",
  ["site: register and trees text", "README", "video if trees appear"],
  "night-v2 orchestrator", "13 Oct about 11:30 p.m.", top10=10)

D("method-ignore-explanation", "correction", "minor",
  "Ignore the EXPLANATION field.",
  "It holds only the request type's help text, not anything about the request (observed).",
  ["prompts/night-v2/COMMON.md correction 1"],
  "Treat it as a per-request explanation of the outcome.",
  ["pipeline"],
  "night-v2 orchestrator", "13 Oct about 11:30 p.m.")

D("method-vacant-building-lower-bound", "method", "moderate",
  "Lead with vacant lots, not vacant buildings, for the uncut-lot claim, and treat vacant-building figures as a lower bound.",
  "Vacant-building lots are cut by contractors who may not be billed into the ledger: only 516 'Vacant Building' Grass Maint rows in 2026 (observed). So 11% cut within 30 days at vacant buildings is partly artefact; 35% at vacant lots (city crews) is the defensible figure.",
  ["research/synthesis.md section 8f", "research/synthesis-notes.md 'Through-line tests' and correction note"],
  "Lead with the more dramatic vacant-building figure.",
  ["site: mowing retrospective", "video"],
  "synthesis session", "13 Oct about 10:20 p.m.")

D("method-exclude-no-violation", "method", "minor",
  "Exclude closures that read 'no forestry violations' from the uncut-lot measure.",
  "Those lots are not expected to be cut; 85-86% of them have no 2026 cut, as expected (observed).",
  ["research/synthesis-notes.md 'Through-line tests' (split by closure text)"],
  "Count every closed weed request.",
  ["site: mowing retrospective"],
  "synthesis session", "13 Oct about 10:20 p.m.")

D("method-2026-not-2025", "method", "moderate",
  "Rest the mowing and hero-lot claims on the 2026 season, not 2025.",
  "The 2025 ledger is thin (8,780 parcels cut against 17,295 in 2024 and 16,118 in 2026; observed, N5), consistent with crews moved to tornado debris, so 'no cut in 2025' is weak evidence.",
  ["build/N5/figures.json (n5_ledger_parcels_cut_2024/2025/2026)", "research/synthesis-notes.md (2025 Grass Maint rows)"],
  "Use two seasons to show persistence.",
  ["site: receipt", "video"],
  "N5", "14 Oct about 00:00")

D("method-refile-definition", "method", "minor",
  "'Re-filed after closure' means another request with the same normalised address and problem code started after the closure time, within 14, 30, 60 or 90 days.",
  "Address plus code is the only stable key in a file with no requester identity; starting the clock at closure separates 'came back' from duplicates filed while open.",
  ["prompts/overnight/T-COMMON.md (Definitions)", "research/synthesis-notes.md '311 closure integrity'"],
  "Report B's measure (any two requests sharing address and code in 12 months, 23.7%), which counts duplicates filed while open.",
  ["site: scoreboard", "README: definitions"],
  "synthesis session", "13 Oct about 10:10 p.m.")

D("method-reproduce-before-critique", "method", "moderate",
  "Reproduce CityStat's own figures from the public file before critiquing them, and report any gap as a finding about unpublished definitions with the question to ask.",
  "The first quick recomputation (Q2 2026 potholes: major 48.6% of 494 against CityStat's 44.5% of 443; residential 81.1% against 90.6%; alley 82.9% against 98.2%) did not match, because it counted rows and used a different quarter state (observed). N4 then searched 1,440 definitions per metric: one shared rule (one row per request, closed requests only, quarter filed, close minus filed within goal) reproduces CityStat's published counts within 0.2% for 8 of 9 metrics (identical in 66 of 72 metric-quarters, never off by more than 4 requests; parks 2.1%) and its shares within 5 points in 76 of 81 metric-quarters (observed; figures n4_repro_counts_exact_C, n4_repro_metrics_within5pp_C). What does not reproduce is reported as questions: routing, the lights clock, and Q2 2026 pothole shares 4-6 points above the file.",
  ["research/synthesis-notes.md 'Checks after Ben's document'", "prompts/night-v2/N4-citystat-and-promises.md"],
  "Build a new scoreboard without showing whether the city's existing one can be recovered.",
  ["site: scoreboard", "deliverable/ask-to-ben.md"],
  "synthesis session; N4 extends", "13 Oct about 10:10 p.m.")

D("method-q3-our-definition", "presentation", "moderate",
  "Show Q3 2026 values (July-September), which CityStat has not published, under the best-matching definition and marked 'our definition, from the public file'.",
  "CityStat's pages say last updated 30 June (observed); the public file runs to 13 October. Showing the next quarter is the demonstration that the quarterly site could be weekly. Each Q3 value carries a floor because closed-only shares fall as slow requests close (N4). The first Q3 result is striking: residential potholes met the 8-day goal 24.3% of the time, against 90.6% published for Q2, with closing words mostly 'work completed' (observed, N4; cause unknown). If CityStat publishes Q3 before Thursday, the line goes stale (check Thursday morning).",
  ["prompts/night-v2/N4-citystat-and-promises.md step 2", "context/NIGHT-PLAN.md 'Doubts'"],
  "Wait for the city's own Q3 figures, or present ours as the official numbers.",
  ["site: scoreboard", "video: site tour"],
  "night-v2 orchestrator", "13 Oct about 11:35 p.m.")

D("method-need-is-acts", "method", "moderate",
  "Measure residents' need by what they did (requests filed, waits, outcomes), not by news or forum attention or by what people say they would do.",
  "Attention and need diverge: graffiti and heat are loud in the news and thin in the request file (observed, reports D and B). Requests are acts, 112,859 a year.",
  ["context/question-standard.md sections 6 and 12 (branch 1 assignment rule)", "research/synthesis.md section 3"],
  "Rank problems by news and social-media volume.",
  ["write-up: why these problems"],
  "synthesis session (question standard)", "13 Oct about 8:30 p.m.")

D("method-gates-vs-weights", "method", "moderate",
  "Three firm gates only (no new staff; residents measurably affected; demo on real data we hold); everything else (an existing tool, data not yet collected, no owning department, several approvers, cost, being on Ben's list) is weighed with evidence and never used alone to drop an idea.",
  "Jack rejected the earlier draft's seven knock-outs as rigid: an excellent idea should not die because a poor tool exists or the data is elsewhere.",
  ["context/question-standard.md sections 4 and 11", "context/HANDOFF.md section 2"],
  "Seven knock-out criteria from the previous session's draft.",
  ["write-up: how we chose"],
  "Jack, with the synthesis session", "13 Oct about 8:30-9 p.m.")

D("method-one-figure-registry", "presentation", "strong",
  "One figure registry (figures.json), written by the code and read by the site and the script, with a plain-English derivation for every number and a 'How we know' link beside it on the site.",
  "Jack does not want the chain behind any number to stay implicit. A single registry also means a number changes in one place, and the research phase's hand-written facts CSVs had already lost figures (fifteen dropped in the earlier synthesis run).",
  ["prompts/night-v2/COMMON.md ('Every figure carries its derivation')", "context/NIGHT-PLAN.md 'What changes' item 6",
   "session transcript 1bc71fad, about 11:48 p.m. (Jack's request)"],
  "A hand-written facts CSV per chapter, as in the research phase.",
  ["site: every number", "video script ({{fig:id}})", "README"],
  "Jack; night-v2 orchestrator", "13 Oct about 11:50 p.m.", top10=8)

D("method-labels", "presentation", "moderate",
  "Every figure is labelled observed (we computed or read it), reported (a source says so) or inferred (our conclusion).",
  "Project rule from the first hour; keeps the city's statements, our counts and our readings apart.",
  ["AGENTS.md (Evidence rules)", "prompts/overnight/T-COMMON.md"],
  "Unlabelled figures.",
  ["site: 'How we know'", "README"],
  "Jack (AGENTS.md)", "13 Oct, start of project")

D("presentation-negative-results", "presentation", "strong",
  "Show what we tested that did not hold, on the site and in the write-up.",
  "Two of the project's own tests failed (no exit; status text does not drive re-filing) and three of its claims were cut back (ward gap, tree conversions, re-filing). Showing them is what lets a city analyst trust the rest.",
  ["AGENTS.md ('Keep negative results')", "prompts/night-v2/N6-site.md section 8", "deliverable/negative-results.md"],
  "Report only what held.",
  ["site: Methods", "README", "deliverable/negative-results.md"],
  "Jack (AGENTS.md); night-v2 orchestrator", "13 Oct", top10=8)

D("method-run-date-first", "method", "minor",
  "Run `date` before writing any timestamp.",
  "The synthesis thread overestimated the time by about five hours and had to correct every stamp; a research thread also wrote a status time ahead of the clock.",
  ["context/HANDOFF-2.md section 7", "memory: check-clock-before-timestamps"],
  "Estimate times from context.",
  ["process"],
  "synthesis session", "13 Oct about 10:47 p.m.")

D("method-write-as-you-go", "method", "minor",
  "Write figures to disk as they are read, and keep them exactly.",
  "The Stemma project's synthesis step dropped about fifteen figures it had been given by relying on memory.",
  ["context/HANDOFF.md section 5", "context/HANDOFF-2.md section 7"],
  "Hold figures in context and write at the end.",
  ["process"],
  "Jack (from the Stemma lesson)", "13 Oct about 8:15 p.m.")

D("method-three-threads", "method", "minor",
  "Split the night into separate agents (pipeline, closure classes, fairness, CityStat, heroes, then site, story, verification, record of choices) under one integrator, rather than one long thread.",
  "One context cannot hold pipeline code, evidence reconciliation and the story without losing figures. Jack asked whether fewer, larger threads would be better; the answer was one integrator with fresh context plus parallel agents.",
  ["context/JACK-INPUTS-synthesis-thread.md section 8", "context/NIGHT-PLAN.md 'The night'", "session transcript 8c95679f, about 10:57 p.m."],
  "One thread with everything in context, or many threads with no integrator.",
  ["process"],
  "synthesis session; night-v2 orchestrator", "13 Oct about 10:50-11:37 p.m.")

D("method-independent-check", "method", "moderate",
  "An independent agent (N8) recomputes every on-screen figure from the raw files before reading the producing script, and scans for personal data, mock data and overclaims.",
  "The people who built a number are the worst placed to see what is wrong with it; the check runs before the COO sees anything.",
  ["prompts/night-v2/N8-verify.md"],
  "Trust each agent's own validation.",
  ["process", "research/chapters/N8-verification.md"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

# ---------------------------------------------------------------- data source
D("data-ledger-as-cut-record", "data source", "strong",
  "Use the city's forestry billing ledger (forestry-service-records.csv, 2,252,031 rows) as its per-lot record of grass cuts: 'Grass Maint' and 'Weed-Grass' rows count as cuts.",
  "In 2026 it holds 37,543 Grass Maint postings (about 31,500 distinct parcel-days: the ledger repeats some rows, N8) on 11,972 parcels, 7,425 of them land-bank lots (observed), while CityStat's manager said in August that per-lot mowing status 'we don't have that tracked in a system' (reported, First Alert 4, 14 Aug 2026). The data the city says it lacks is on its own open-data portal.",
  ["https://www.stlouis-mo.gov/data/upload/data-files/forestry-service-records.csv",
   "research/synthesis-notes.md 'Forestry service records' and correction note",
   "https://www.firstalert4.com/2026/08/14/cut-down-unmowed-vacant-lots-st-louis-city-looks-data-north-city-resident-discusses-wait/"],
  "Satellite imagery as the cut record, or no cut record (take the 311 'closed' at face value).",
  ["site: receipt", "site: mowing retrospective", "video: opening lot", "README"],
  "synthesis session", "13 Oct about 9:40 p.m.")

D("data-lra-join-fixed", "correction", "moderate",
  "Identify land-bank (city-owned) lots by joining the ledger's PARCEL to the LRA inventory's ParcelId.",
  "The first land-bank join used a column the LRA file does not have and returned '0 in LRA', which was wrong; the corrected join finds 7,425 of 11,972 parcels cut in 2026 are LRA (observed). It also showed city-owned lots are in the ledger, not only billed private lots.",
  ["research/synthesis-notes.md 'Files confirmed on disk' (Correction and addition, about 9:40 p.m.)",
   "https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_INVENTORY.csv"],
  "The first join's result.",
  ["site: receipt (LRA flag)", "README"],
  "synthesis session", "13 Oct about 9:40 p.m.")

D("data-cityworks-samples-only", "data source", "moderate",
  "Use Cityworks work orders only from the city's public saved-search samples (1,500 rows each, truncated), with staff fields dropped; no wider pull of the city's work-order system.",
  "The city publishes these saved searches as public links; wider work-order data looks internal rather than published (inferred), and the entry should run only on what the city chose to publish. The cost is coverage: the samples hold about a third of the tree work orders, so tree matches are lower bounds.",
  ["research/synthesis-notes.md A.6", "context/NIGHT-PLAN.md 'Cut scope'",
   "https://service.stlouis-mo.gov/cityworks/gis/1/6955/rest/services/cw/FeatureServer/2"],
  "Pull the full work-order history from the city's wider work-order system.",
  ["site: trees text", "README: what is fragile"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

D("data-no-slmpd", "data source", "strong",
  "Use nothing from slmpd.org.",
  "slmpd.org's robots.txt names ClaudeBot, anthropic-ai and Claude-Web with 'Disallow: /' (observed 14 Oct 00:36 UTC), and policing is out of scope in any case (a state-appointed board).",
  ["research/data-audit.md 'Read this first' item 1", "memory: stl-robots-txt-limits"],
  "Use police data in the analysis.",
  ["README: data note", "process"],
  "data-audit thread; synthesis session", "13 Oct about 7:43 p.m.")

D("data-robots-city-site", "data source", "strong",
  "Respect the city site's robots file: nothing under an address the City's robots.txt disallows, and nothing ending .pdf/.xls/.xlsx/.txt, is fetched by the pipeline; the weekly job uses the bulk files under /data/upload/data-files/, which robots allows.",
  "www.stlouis-mo.gov's robots.txt disallows those paths (observed); research fetched some once, but repeated or scheduled pulls would go against stated policy. A pipeline the city's own robots file forbids could not be the thing the city adopts.",
  ["research/data-audit.md 'Read this first' item 2", "memory: stl-robots-txt-limits", "prompts/overnight/T-COMMON.md (Rules)"],
  "Scrape the catalog's CSV/JSON exports weekly from an address the City's robots.txt disallows.",
  ["pipeline", "README: how the city would run it"],
  "data-audit thread", "13 Oct about 7:43 p.m.")

D("data-no-keys", "data source", "moderate",
  "Use no keys, tokens, sign-ins or POST forms anywhere; the pipeline runs keyless.",
  "Keys and accounts are Jack's to request (AGENTS.md); acceptance test 1 requires a rebuild from public zips with no key. The CSB Open311 API, the address API and CityStat's Tableau export all need credentials (observed).",
  ["AGENTS.md (Boundaries)", "context/BUILD-SPEC.md acceptance test 1", "research/data-audit.md 'Read this first' item 4"],
  "Request a city API key or sign in to CityStat's Tableau for its underlying data.",
  ["pipeline", "README"],
  "Jack (AGENTS.md); synthesis session (spec)", "13 Oct")

D("data-no-licence-said", "data source", "strong",
  "Say plainly, once, that no city dataset states a licence, rather than implying one.",
  "None of the city's 72 catalogued datasets carries a licence value in data.json, and no export, API or ArcGIS layer states one (observed); no open-data policy, ordinance or executive order was found (observed absence). Two Missouri imagery services carry a reported no-redistribution clause.",
  ["research/data-audit.md 'Read this first' item 5", "research/synthesis-notes.md A.1 and E.3 'Not found'"],
  "Assume public-domain reuse without comment.",
  ["site: Methods", "README", "video: closing line"],
  "data-audit thread; synthesis session", "13 Oct")

D("data-imagery-visual-only", "data source", "moderate",
  "Use MSDIS aerial imagery only as a visual frame, with no analytic claim attached; check its robots file first; never Google or any keyed service.",
  "Ben's document lists the MSDIS server as a resource (observed). Its robots.txt redirects to a 404, so it publishes no crawl rules, and it needs no key (observed, N5). Its newest St. Louis imagery is 2025, so it cannot show 2026 grass (observed, N5). The 2022 and 2024 orthos carry a reported no-redistribution clause in their bundled metadata, and Google Street View terms bar scraping (observed), so imagery is decoration, not evidence.",
  ["context/BEN-PROBLEM-SETS.md (Resources)", "prompts/night-v2/N5-hero-cases.md (Imagery)", "research/synthesis-notes.md A.3"],
  "Use imagery as evidence of a missed cut, or use Google imagery.",
  ["site: receipt image", "video"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.", status="open: redistribution clause not resolved")

D("data-board-up-and-demolition", "data source", "moderate",
  "Use the city's board-up layer and demolition permits as independent completion records for 'vacant building unsecured' and land-bank demolition requests.",
  "They are dated, address-level records of the work itself (Boardups 33,141 rows to 8 Oct 2026; Demolitions 3,767 to 9 Oct 2026; observed), the same kind of second record the ledger is for mowing.",
  ["build/N2/joins.json", "https://maps8.stlouis-mo.gov/arcgis/rest/services/BUILDING_DIVISION/BldgDiv_Boardups/MapServer",
   "https://maps8.stlouis-mo.gov/arcgis/rest/services/BUILDING_DIVISION/Demolitions/MapServer"],
  "Limit the completion layer to mowing and trees.",
  ["site: register", "README laundry list"],
  "N2", "13 Oct about 11:50 p.m.")

D("data-research-sources-flagged", "data source", "minor",
  "Two research-phase news sources were kept but flagged as droppable: r/StLouis posts from Arctic Shift (a third-party archive with no published terms) and Fox 2 article text read through its public WordPress API after the pages returned 403. Neither feeds the product.",
  "Reddit blocks direct collection; the archive was the only route. Both were surfaced to Jack as his call rather than silently used or silently dropped.",
  ["session transcripts 12bea175 (about 6:35 p.m.) and ea016740 (about 7:40 p.m.)", "research/attention-over-time.md"],
  "Use them without flagging, or discard them without telling Jack.",
  ["research only"],
  "attention and mayor's-voice threads", "13 Oct about 6:35-7:40 p.m.", status="open: Jack's call")

# ---------------------------------------------------------------- scope
D("scope-through-line", "scope", "strong",
  "Build the through line (St. Louis records when a job starts and is handed off, not when it is done) as one completion layer, rather than a single-service tool.",
  "Jack asked for the upstream cause behind the separate findings. Two tests on the city's own records supported it: weed requests closed the day they are filed with no cut in the ledger on most lots that month, and tree requests cancelled with no text whose addresses turn up in Forestry's work orders (observed). The same shape appears in towing, water leaks, refuse, sidewalks, the tornado tracker and sirens.",
  ["context/JACK-INPUTS-synthesis-thread.md section 4", "research/synthesis.md sections 8a-8g"],
  "Mowing alone (the synthesis's first pick; it passes every gate and remains the fallback).",
  ["video: thesis line", "site: landing", "README: thesis"],
  "synthesis session after Jack's request; Jack 'sounds good as a first read'", "13 Oct about 10 p.m.")

D("scope-trees-one-page", "scope", "moderate",
  "Hazard trees become one page (the silent cancellations), not a tool.",
  "Ben's written tree challenge is canopy investment, not hazard removal, so the certificate argument fell away (observed in the document); resident evidence for hazard trees is thin and the constraint looks like crews (tree trimmers 50% vacant, reported).",
  ["research/synthesis.md sections 7b and 8g", "context/BEN-PROBLEM-SETS.md"],
  "A removal-backlog ordering tool and 'where is my tree' page.",
  ["site: register and trees text"],
  "synthesis session", "13 Oct about 9:45 p.m.")

D("scope-sidewalks-register-row", "scope", "moderate",
  "Sidewalks become one row in the register, not a chapter.",
  "It is a separate data world (inventory, crowd labels, ward funds); the city's sidewalk inventory has DateRepair filled on 0 of 36,822 segments (observed, N2), so there is no completion record to join; and sidewalk money is ward money needing up to fourteen yeses (observed).",
  ["context/NIGHT-PLAN.md 'Cut scope'", "build/N2/figures.json (n2_sidewalk_daterepair_filled)", "research/synthesis.md section 1d"],
  "The EO 96 sidewalk map and repair queue as a chapter.",
  ["site: register"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

D("scope-satellite-dropped", "scope", "strong",
  "Satellite verification of mowing is dropped.",
  "A vacant lot is about 300 square metres, which is 3 to 6 Sentinel-2 pixels at 10 m, so a cut is unlikely to be detectable (inferred); GeoSTL reported in August it was already working with the city on satellite mowing priority (reported), so we would be racing them.",
  ["context/NIGHT-PLAN.md 'Cut scope'", "build/INTEGRATION-LOG.md (23:37 entry)", "research/synthesis.md section 1a"],
  "Sentinel-2 vegetation-index change on twenty known-cut parcels as a third record (the synthesis's stretch goal).",
  ["write-up: what we did not do"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

D("scope-mowing-retrospective", "scope", "moderate",
  "Show mowing as a 2026 retrospective, not a live list.",
  "The mowing season is over or ending, so a live next-cut list is not useful until April 2027. The city's own Forestry page says mowing runs 'Between April and October each year' (observed, research G) and the research dates the season's end to 31 October; NIGHT-PLAN's '1 March to 30 September' window has no source in the project files (untraced). The 2026 first rotation started 6 April.",
  ["context/NIGHT-PLAN.md 'Cut scope'", "research/synthesis.md section 1a", "research/parts/G-capacity.md (31 Oct row)", "research/parts/G-seasonal.md (April 2027 row)"],
  "A live mowing Monday list.",
  ["site: mowing retrospective", "video"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

D("scope-dumping-light-page", "scope", "moderate",
  "Illegal dumping stays as one light page: repeat sites at block level and outcomes by site.",
  "It is Ben's problem set 3 and the 311 file is named as its data, so many entrants will build a hotspot map (inferred); the depth only this entry has is the repeat-address count (959 addresses, 50 with five or more, one with 32) and the enforcement outcomes already coded in the file (observed).",
  ["research/synthesis.md sections 7b, 7c", "context/NIGHT-PLAN.md 'Cut scope'"],
  "A full dumping chapter with hotspot prediction by time and place.",
  ["site: dumping page"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

D("scope-rejected-candidates", "scope", "moderate",
  "Candidates dropped with a stated reason: graffiti (lowest need; not in Ben's written document), heat and planting (tools exist and the field is crowded), potholes (need halved; detection years away), water mains (no mains layer; token-gated), tornado dashboard (duplicates contracted UMSL work), ARPA tracker, ward capital portal, building permits, drones, the crime device and help for elderly neighbours.",
  "Each failed a firm gate or did not beat the baseline on evidence; for example the ARPA exports do not reconcile ($403,080,817 against $101,214,949; observed) and no ward capital spending is published (observed absence).",
  ["research/synthesis.md sections 2q-2u and 4"],
  "Keep a long list of candidates open into the build.",
  ["write-up: how we chose"],
  "synthesis session", "13 Oct about 9:45 p.m.")

D("scope-tornado-prioritisation-dropped", "ethics", "moderate",
  "Drop the tornado-repair prioritisation variant.",
  "Ranking households for aid from outside on partial data fails the personal-data gate and the harm branch: a wrong ranking lands on a household.",
  ["research/synthesis.md sections 2e and 4"],
  "A ranked list of tornado-repair applicants.",
  ["write-up: how we chose"],
  "synthesis session", "13 Oct about 9:45 p.m.")

D("scope-out-of-scope-said", "presentation", "strong",
  "Say plainly what the layer does not fix: crews and money, police and 911, shelter beds, permits, identifying dumping perpetrators, and any use of exposed personal data. 'Data does not cut grass.'",
  "The city's own words put its backlogs on crews and money: tree trimmers 50% vacant, Forestry at about 60% of mowing staff, 129 Street Department vacancies, $150M of unfunded water mains (reported). A completion layer makes a shortfall visible and orderable; claiming more would be overclaiming.",
  ["research/synthesis.md section 8c", "context/BUILD-SPEC.md 'Out of scope'", "context/HANDOFF-2.md section 4 item 3"],
  "Imply that better data will clear the backlogs.",
  ["video: closing", "README: what it does not fix", "site: Methods"],
  "synthesis session", "13 Oct about 10 p.m.", top10=10)

D("scope-calibrated-claims", "correction", "strong",
  "Claim about residents only what the evidence carries: the wait, the miss, and the city's inability to see what it finished. Do not claim that residents give up, that the status text itself harms them, or anything about votes.",
  "Two tests came back negative: no exit within a year (refuse re-filers filed more later, 63.5% against 46.5%) and re-filing does not depend on whether a cut was recorded (21.2% both ways) (observed). The evidence that seeing completion changes output comes from other cities' audits, not St. Louis.",
  ["research/synthesis.md sections 8h, 9a-9c", "context/HANDOFF-2.md section 1 ('Cannot claim')"],
  "The strong form: wrong statuses harm residents and drive them away.",
  ["video narration", "README", "progress report"],
  "synthesis session", "13 Oct about 10:30-10:45 p.m.", top10=10)

D("scope-no-teaming", "scope", "minor",
  "Stay solo; do not team with another entrant.",
  "Coordination would cost more than it gains with about 40 hours left, and the entry's edge is depth only this pipeline has (inferred).",
  ["context/NIGHT-PLAN.md 'Doubts'", "context/HANDOFF-2.md section 4 item 7"],
  "Join the kickoff team that said it was open to collaborators.",
  ["process"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

D("scope-build-time-not-criterion", "scope", "minor",
  "Build time is not a selection criterion, and the entry need not be one of Ben's problems.",
  "Jack removed both: people and agents underestimate what can be built with LLMs in a short time, and he did not think it needed to be one of Ben's problems.",
  ["context/HANDOFF.md section 2", "context/question-standard.md section 2"],
  "Prefer ideas that are quick to build, or only Ben's listed problems.",
  ["process"],
  "Jack", "13 Oct about 8:15 p.m.")

# ---------------------------------------------------------------- presentation
D("presentation-not-a-clone", "presentation", "strong",
  "No city look-alike: no seal, no city colours or logo, a footer saying 'Independent prototype built from the City of St. Louis's open data. Not a City website.', hosted under our own name. CityStat's structure appears only in the scoreboard section.",
  "A clone invites the 'derivative of a two-person team's quarterly site' comparison and drifts toward impersonating the city. Jack liked a clone because it shows where each fix would go; the scoreboard keeps that benefit.",
  ["context/NIGHT-PLAN.md 'What changes' item 3", "prompts/night-v2/N6-site.md", "context/JACK-INPUTS-synthesis-thread.md section 3",
   "session transcript 93c7fcd6, about 9:44 p.m. ('Do not publish a lookalike of a city site')"],
  "A digital clone of the CityStat site with the improvements dropped in (Jack's first idea).",
  ["site: whole design", "video"],
  "night-v2 orchestrator, from Jack's clone idea", "13 Oct about 9:50-11:37 p.m.")

D("presentation-receipt-face", "presentation", "strong",
  "The product's face is a per-request receipt: filed, promised, closed with the city's exact words, and what the city's other records show (ledger cut, work order, or nothing).",
  "Mike's test at the kickoff was 'the personal story, why this is important' (observed); the biggest doubt about the through line was abstraction in two minutes. One request on one screen carries the thesis.",
  ["context/NIGHT-PLAN.md 'What changes' item 2", "context/question-standard.md section 13", "context/HANDOFF-2.md section 4 item 1"],
  "Lead with the ward table or a dashboard of rates.",
  ["site: landing and receipt", "video: opening"],
  "night-v2 orchestrator; Jack provisional yes", "13 Oct about 11:37-11:50 p.m.", status="provisional: Jack decides the lead after sleep")

D("presentation-fairness-twist", "presentation", "moderate",
  "Lead the numbers with promise dates and a fairness finding that survives scrutiny: the north waits longer for the city's first step (a tag, a referral, a notice), not for crews. The fairness line planned at 11:37 p.m. (that the city's ward chart mostly reflects closing practice) was withdrawn at 11:57 p.m. after N3 tested it.",
  "The inflated raw gap would not survive a city analyst. The planned twist was then tested: an exact decomposition puts only 12% of CityStat's ward 1 vs ward 10 gap on request mix and closing words (1.9 of 15.7 days), and adjusting for mix does not shrink the gap (N4). What survives like for like is the wait for a first step (towing tagged 12.0 against 36.9 days, promise 5; cave-in referral 0.8 against 41.7; building-code notices 3.3 against 8.4), while, since the May 2025 tornado, most closures that say the work was done show no gap (observed, N3; before the tornado potholes ran 22.3 vs 31.8 days, under the 1.5 rule, N8).",
  ["context/NIGHT-PLAN.md 'What I checked' item 1 and 'What changes' item 1", "prompts/night-v2/COMMON.md correction 2",
   "research/chapters/N3-fairness.md (summary and section 2)", "research/chapters/N4-citystat.md section 4"],
  "Lead with the raw ward gap (retired: it compared a referral with a repair); or keep the planned line that the ward chart mostly reflects closing practice, after N3 found mix and closing words explain 12% of the gap.",
  ["video", "site: fairness section", "progress report"],
  "night-v2 orchestrator; Jack provisional yes; reworded by N3's result", "13 Oct about 11:37 p.m.; revised 14 Oct about 00:00",
  status="provisional: the twist's wording changed after N3; Jack decides the lead")

D("presentation-lead-swappable", "presentation", "minor",
  "Make the landing's lead block driven by one config file (which hero, which headline figure), and build the site tonight on a default thesis-first layout instead of waiting for Jack's pick.",
  "Jack wanted to decide the lead after sleep; waiting would have pushed the front end into Wednesday and squeezed the video.",
  ["prompts/night-v2/N6-site.md ('The lead must be swappable')", "context/NIGHT-PLAN.md 'What changes' item 3"],
  "Wait for the morning decision before building the front end.",
  ["site: config.json"],
  "night-v2 orchestrator", "13 Oct about 11:50 p.m.")

D("presentation-video-shape", "presentation", "moderate",
  "The two-minute video holds one story, one proof that it generalises, and one ask; everything else lives on the site.",
  "Two minutes cannot carry five chapters; trees and sidewalks are for Ben to click, not for the video.",
  ["context/NIGHT-PLAN.md 'Doubts'", "context/BUILD-SPEC.md acceptance test 4", "session transcript 93c7fcd6, about 9:44 p.m."],
  "A tour of every chapter.",
  ["video"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

D("presentation-say-where-ai-is", "presentation", "moderate",
  "Say where the AI is, in about ten seconds of narration: AI was the method (one person audited 1.5M requests, 2.2M ledger rows and the work orders in two days, and drafted the closure classes in a form a person can review); the product deliberately runs none.",
  "This is a Civic AI hackathon and the earlier plan never said where the AI was; leaving it out invites the question, and the policy turns a constraint into a design choice.",
  ["context/NIGHT-PLAN.md 'What changes' item 4", "prompts/night-v2/N7-story.md"],
  "Say nothing about AI, or pretend the product is AI-driven.",
  ["video", "README", "site: Methods"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

D("presentation-figure-ids-in-text", "presentation", "minor",
  "Narration and write-up refer to numbers by figure id ({{fig:id}}) with the current value beside it, so text updates when a figure changes.",
  "Figures are still moving overnight (deduplication shifted several medians); hard-coded numbers in a script go stale silently.",
  ["prompts/night-v2/N7-story.md"],
  "Type the numbers into the script.",
  ["video script", "README"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

D("presentation-mock-banner", "presentation", "minor",
  "Any site section built against a placeholder file shows a red 'MOCK DATA' banner until real data replaces it.",
  "The site is built in parallel with the data; a mock number must never be mistaken for a finding.",
  ["prompts/night-v2/N6-site.md", "prompts/night-v2/N8-verify.md step 3"],
  "Wait for every export before building any page.",
  ["site"],
  "night-v2 orchestrator", "13 Oct about 11:37 p.m.")

D("presentation-progress-report-correction", "presentation", "minor",
  "The progress report names the correction we made to our own headline.",
  "Saying what we got wrong and fixed is evidence of method, and the city will check the ward numbers.",
  ["prompts/night-v2/N7-story.md (Make the choices visible)"],
  "Report only progress.",
  ["progress report"],
  "night-v2 orchestrator", "13 Oct about 11:55 p.m.")

# ---------------------------------------------------------------- corrections to our own claims
D("correction-ward-gap-inflated", "correction", "strong",
  "Retire the raw ward-gap headlines: never use '1.7 vs 27.6 days' (cave-ins) or '98 vs 6.7 days' (tree inspection) anywhere.",
  "Both compared different kinds of closure. Cave-ins, like for like ('work completed'): 9.6 against 25.1 days on rows, 8.3 against 23.1 on distinct requests, but only 35 such closures in wards 1-5, so the repair gap is unproven; share closed 75% against 45%. Tree inspection, 'removal work order created': 125 against 204 days on rows (124 against 190 on requests, only 21 in the north), 1.6x; the headline was fast 'no service necessary' closures in the southwest (observed, 13 Oct about 11:30 p.m.; N1, N3, N5 re-derived). Nuance from N3: the 1.7 vs 27.6 headline compared a desk referral in the southwest with a field process in the north, and the referral itself takes 0.8 against 41.7 days, so 'inflated by mix' understates the north's wait for the first step. The planned replacement lead, single light out, then failed N3's robustness rule; towing holds.",
  ["prompts/night-v2/COMMON.md correction 2", "context/NIGHT-PLAN.md 'What I checked' item 1", "build/INTEGRATION-LOG.md (23:37 entry)"],
  "Keep the larger numbers from the synthesis and HANDOFF-2, which the entry had been planned around.",
  ["video", "site: fairness section", "README laundry list", "progress report"],
  "night-v2 orchestrator", "13 Oct about 11:30 p.m.", top10=4)

D("correction-report-b-definitions", "correction", "moderate",
  "Use 3.8% (closed with blank text) and 6.3% (re-filed within 30 days of closure) rather than the research report's 14.6% blank and 23.7% repeat.",
  "Report B's 14.6% is over closed and cancelled requests together, and its 23.7% counts any two requests sharing address and code within 12 months, including duplicates filed while the first was open (observed on re-reading the method).",
  ["research/synthesis-notes.md '311 closure integrity' (parenthesis)", "research/demand-and-existing-tools.md"],
  "Quote the report's larger figures.",
  ["site: scoreboard", "README"],
  "synthesis session", "13 Oct about 10:10 p.m.")

D("correction-strong-form-overreach", "correction", "moderate",
  "Withdraw the synthesis's own first reading that the harm claim 'fails' because residents re-file at the same rate whether or not a cut was recorded.",
  "Equal re-filing could mean residents ignore the record, that one cut does not settle a chronic lot, or that discouraged residents leave; that test could not tell them apart. Jack challenged it, and a sharper test (exit) was run instead (it found no exit within a year).",
  ["research/synthesis.md section 9a", "context/JACK-INPUTS-synthesis-thread.md section 6"],
  "Keep 'the strong form fails' as stated in section 8h.",
  ["write-up", "deliverable/negative-results.md"],
  "synthesis session after Jack's push-back", "13 Oct about 10:40 p.m.")

D("correction-unhoused-count", "correction", "minor",
  "Use Ben's figure for the unhoused population (1,790 in 2026, 323 unsheltered), not Board Bill 91's 'more than 1,700' unsheltered.",
  "The organiser document gives the 2026 count directly and settles the research's open point (observed).",
  ["context/BEN-PROBLEM-SETS.md (problem set 2 and 'What this changes')"],
  "The bill's figure.",
  ["write-up (context only)"],
  "synthesis session", "13 Oct about 9:40 p.m.")

D("correction-trees-not-bens", "correction", "moderate",
  "Stop treating hazard trees as Ben's 'trees' problem.",
  "The written document's tree challenge is canopy and green-space investment; graffiti is absent from it. The spoken 'graffiti and trees' at the kickoff was shorthand (observed in the document).",
  ["context/BEN-PROBLEM-SETS.md", "research/synthesis.md section 7b"],
  "Keep the earlier reading from the kickoff transcript.",
  ["write-up: how we chose"],
  "synthesis session", "13 Oct about 9:40 p.m.")

# ---------------------------------------------------------------- orchestrator decisions during the night (INTEGRATION-LOG, COMMON 6-10)
D("scope-three-doors", "scope", "strong",
  "Name three end users and give each a door: residents (a public CityStat redesign and the receipt, answering Ben's question 5); city staff (a one-page Monday brief and block-level lists for the weekly data review, as a plain document, not a mock of internal software); the CityStat team (SQL, definitions, and the register as a roadmap).",
  "Jack asked who the end user is. Each audience already has a routine the output can drop into (CityStat's internal operations meetings; the resident-facing CityStat page), and a mock of internal city software would claim knowledge of systems we have not seen. Decision recorded as reversible.",
  ["build/INTEGRATION-LOG.md 00:04 entry", "research/what-gets-adopted.md section 3.2 (CityStat's internal operations meetings, reported)"],
  "One audience (the public page only), or a mock-up of the city's internal work-order screens.",
  ["site: three entry points", "README", "video: site tour"],
  "night-v2 orchestrator, after Jack's question", "14 Oct about 00:04", status="in force; reversible")

D("presentation-q3-framing", "presentation", "strong",
  "Frame the Q3 2026 pothole figure as 'a weekly run would have shown this in July', not 'your potholes collapsed'.",
  "Residential potholes met the 8-day goal 24.3% of the time in Q3 against 84.4% for Q2 in today's file (CityStat published 90.6%), but the four quarters before Q2 ran 42-50%, so Q2 was the outlier and Q3 the low; the cause is unknown. The orchestrator checked it is not a batch-closure artefact (the largest single close day is 12% of Q3 closures). The point the city can use is timeliness, not blame.",
  ["prompts/night-v2/COMMON.md correction 8", "build/INTEGRATION-LOG.md 00:01 entry", "research/chapters/N4-citystat.md section 2"],
  "Lead with the collapse ('from 90.6% to 24.3%').",
  ["site: scoreboard", "video", "README", "progress report"],
  "night-v2 orchestrator", "14 Oct about 00:01")

D("presentation-towing-medians-first", "presentation", "moderate",
  "Lead the towing comparison with medians (12.0 against 36.9 days), not the share of promises met, until the independent check settles which share is right.",
  "Two derivations of the share closed by the 5-day promise disagree: N3 38% against 11%; the orchestrator's raw recomputation 32% against 4% (different timestamp rule). The medians match exactly in both (orchestrator 12.0 vs 36.9 on 1,299/271 requests).",
  ["prompts/night-v2/COMMON.md correction 2", "build/INTEGRATION-LOG.md 23:57 entry"],
  "Quote either share now.",
  ["site: fairness section", "video"],
  "night-v2 orchestrator", "13 Oct about 11:57 p.m.", status="resolved by N8: if a share is used, 32% vs 4% (tagged within the promise, like for like); N3's 38% vs 11% counts any closing words and is retired")

D("method-orchestrator-spot-checks", "method", "moderate",
  "Before relaying any agent's headline to the others, the orchestrator recomputes it from the raw file.",
  "N2's 35.2% hand-off share and N3's towing and cave-in medians matched exactly on recomputation; the towing promise share did not, and was held back. The full pipeline was also re-run to show figures reproduce (191 then 197 figures; only the build time changed).",
  ["build/INTEGRATION-LOG.md 23:54, 23:57, 00:09 entries"],
  "Relay agents' figures as reported.",
  ["process", "site: 'How we know' (orchestrator check noted)"],
  "night-v2 orchestrator", "13-14 Oct night")

D("adoption-register-as-roadmap", "adoption", "moderate",
  "Present the register as the city's roadmap: 4 of 25 services can be joined to a completion record on public files today; of the other 21, the register names Cityworks work orders for 5 (trees, tree planting, potholes, cave-ins, street lights), and the rest need other division records (tow lot, truck GPS, Building Division, CEMA, Human Services, the 50/50 programme).",
  "That turns the register from a list of gaps into a list of specific records to connect, without new software (N2's register; N8 corrected an earlier 'most' to 5 of 21).",
  ["build/INTEGRATION-LOG.md 00:04 entry", "build/N2/register.json", "build/out/figures.json n2_register_services_with_record", "research/chapters/N8-verification.md finding 6"],
  "Present the register as a list of failings.",
  ["site: register", "README", "deliverable/ask-to-ben.md"],
  "night-v2 orchestrator", "14 Oct about 00:04")

D("privacy-lead-receipt-narrowing", "privacy", "moderate",
  "Flag, not decide: the lead receipt names the land-bank lot's block together with details (its acquisition year, a neighbouring lot's block) that together narrow it to one parcel.",
  "Block-level rounding is the rule for every public output (Jack's ruling). The lot is city-owned, so no private owner is exposed and the orchestrator judged it acceptable under the rule, but the combination undoes the rounding in practice; Jack asked for blocks rather than a specific property, so it is his call.",
  ["build/INTEGRATION-LOG.md 00:37 entry (note for morning)", "prompts/night-v2/COMMON.md (Rules: block level, including the hero examples)"],
  "Silently keep the extra details; or strip them without asking.",
  ["site: lead receipt", "video: opening shot"],
  "night-v2 orchestrator (flag for Jack)", "14 Oct about 00:37", status="open: Jack to judge in the morning")
