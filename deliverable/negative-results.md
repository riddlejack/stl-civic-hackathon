# What we tested that did not hold

Generated 2026-10-14 01:51 CDT by `scripts/night/N9/build.py`. Each entry is two sentences: what we tested or expected, and what happened, with the source. Labels: observed (we checked it), reported (a source says so), inferred (our conclusion), observed absence (we looked and did not find it).

## Summary

43 negative or bounding results, in 6 groups: tests that came back negative (12); claims we cut back (10); definitions that did not reproduce (6); things we dropped, and why (2); data that does not exist or could not be used (8); things we looked for and did not find (5). The seven that shaped the entry most come first: the exit test, the status-text test, our own inflated ward gap, the fairness twist that did not survive its own test, the tree conversions we could not prove, the CityStat definitions that did not reproduce at first, and the satellite check we dropped. None of these is hidden on the site; they are what the rest of the numbers are bounded by.

## The seven that shaped the entry

- **We found no sign that residents stop using 311 after a bad experience, within a year.** We tested whether households whose request went wrong stop filing: refuse requests that had to be re-filed within 14 days, and tree requests cancelled with no explanation. We found no sign that they do, within a year: refuse re-filers filed again later at 63.5% against 46.5% for others, and silently cancelled tree requesters at 44.6% against 41.8%, so the entry does not claim that closures drive residents away. People who never file at all are invisible in this file. (observed; source: research/synthesis.md section 9b; research/synthesis-notes.md 'Impact tests' C)

- **The status text does not change whether residents report again.** Weed requests closed 'on schedule' were re-filed within 60 days at 21.2% whether or not the ledger showed a cut within 30 days, and tree requesters re-filed at 18.7% after a silent cancel against 16.4% after 'work order created'. Residents respond to the lot and the tree, not to the words on the record, so we do not claim the status text itself harms anyone. (observed; source: research/synthesis.md section 8h; research/synthesis-notes.md 'Does the record gap itself hurt residents?')

- **Our own ward-gap headline was inflated by closure mix.** We had led with cave-ins closing in 1.7 days in the southwest against 27.6 in the north, and tree inspections in 6.7 against 98; comparing only closures with the same words, the cave-in referral itself takes 0.8 against 41.7 days, recorded repairs take 8.3 against 23.1 but number only 35 in the southwest (too few to prove a gap), and trees closed 'removal work order created' take 124 against 190 days with only 21 in the north. The raw figures compared the southwest's quick desk referrals and 'no service necessary' answers with field work in the north, so they are retired. (observed; source: prompts/night-v2/COMMON.md correction 2; context/NIGHT-PLAN.md item 1)

- **The city's ward chart gap is not mostly request mix or closing practice.** We expected most of CityStat's ward 1 versus ward 10 gap (17.2 against 35.1 days) to be the mix of request types and closing practice, the fairness line the plan proposed to lead with (now withdrawn). An exact decomposition attributes only 1.9 of 15.7 days (12%) to those; most of the gap is the same request type, closed with the same words, later, usually at a first step such as a tag or referral, so the defensible line is that the north waits longer for the city to act first. (observed; source: research/chapters/N3-fairness.md section 1; build/N3/decomposition.json; figures n3_decomp_*)

- **Cancelled tree requests are not proven to have become work orders.** Cancelled tree-request addresses appear in a one-third sample of Forestry's work orders at 10.8% against 1.9% for unrelated requests, which we first read as 'most were converted'. But requests the city closed as 'work order created' match at only 6.8% (and all closed tree requests at about 2%), so our address match misses most real pairs; the defensible statement is 'about five times as often as unrelated requests'. (observed; source: prompts/night-v2/COMMON.md correction 3; research/synthesis-notes.md 'Through-line tests' Test 2)

- **Our first recomputation of CityStat did not match; the careful one mostly does.** The synthesis's quick recomputation of Q2 2026 pothole repairs within goal gave 48.6% for major streets (CityStat 44.5%), 81.1% for residential (90.6%) and 82.9% for alleys (98.2%), because it counted rows, divided by every request filed rather than by closed ones, and read the quarter as the file stands today rather than when CityStat froze it. A search over 1,440 definitions found one shared rule that reproduces CityStat's counts within 0.2% for 8 of 9 metrics (identical in 66 of 72 metric-quarters, never off by more than 4 requests; parks 2.1%) and its shares within 5 points in 76 of 81 metric-quarters; what still does not reproduce (routing, the whole-block-lights clock, two Q2 2026 pothole shares) is listed below and sent to the city as questions. (observed; source: research/synthesis-notes.md 'Checks after Ben's document'; research/chapters/N4-citystat.md section 1)

- **Satellite verification of mowing was dropped.** The plan was to confirm cuts from Sentinel-2 imagery as a third record beside the ledger and the 311 file. A typical vacant lot is about 300 square metres, 3 to 6 pixels at 10 metres, so a cut is unlikely to show, and GeoSTL reported in August that it was already doing satellite mowing work with the city. (inferred; source: context/NIGHT-PLAN.md 'Cut scope'; build/INTEGRATION-LOG.md 23:37)

## Tests that came back negative

- **Our first land-bank join returned zero, wrongly.** The first attempt to find land-bank lots in the ledger joined on a column the land-bank file does not have and reported no matches. Joined correctly on parcel id, 7,425 of the 11,972 lots cut in 2026 are land-bank lots. (observed; source: research/synthesis-notes.md 'Files confirmed on disk' (correction))

- **The 2025 mowing season cannot be judged from the ledger.** The ledger shows cuts on 8,780 parcels in 2025 against 17,295 in 2024 and 16,118 in 2026, consistent with crews moved to tornado debris. 'No cut in 2025' is therefore weak evidence and the mowing claims rest on 2026 alone. (observed; source: build/N5/figures.json (n5_ledger_parcels_cut_*))

- **The ledger undercounts cuts at vacant buildings.** Only 516 'Vacant Building' grass-cut rows appear in the 2026 ledger, and vacant-building lots are cut by contractors who may not be billed into it. The 11% cut-within-30-days figure for vacant buildings is therefore a lower bound and is not used as a lead. (observed; source: research/synthesis.md section 8f)

- **The forestry ledger repeats rows.** Before 2021 the ledger repeats most legacy rows (2019: 112,734 cut rows but 55,624 distinct parcel-date-type entries), and 2026 has 46,346 cut rows but 39,862 distinct. Distinct-parcel counts are unaffected, but 'over 37,000 cuts' in 2026 is about 31,500 distinct parcel-days. (observed; source: research/chapters/N8-verification.md finding 10)

- **Adjusting the ward map for request mix does not shrink the gap.** Re-weighting each ward to the citywide mix of request types leaves ward 1 at 17.4 days and ward 10 at 32.2, and makes some north wards slower (ward 13 from 24.6 to 29.2). Type mix does not explain the north-south difference on the city's own chart. (observed; source: research/chapters/N4-citystat.md section 4; figures n4_ward*_type_mix_adjusted_avg_days)

- **Since the tornado, where the words say the work was done, most services show no ward gap.** Since the tornado, done-class medians are level for whole-block lights (0.7 against 0.7 days), residential potholes (6.9 against 8.0), major-street potholes (7.0 against 6.8), refuse (1.7 against 1.8), damaged containers and signs. Before the tornado, potholes did run slower in the north (residential 22.3 against 31.8 days; major streets 15.2 against 21.4), under the 1.5-times rule but visible to any analyst. The robust gaps are at first steps: towing tagged (12.0 against 36.9 days), cave-in referral (0.8 against 41.7) and building-code notices (3.3 against 8.4). (observed; source: research/chapters/N3-fairness.md section 2; figure n3_no_gap_done_types_after)

- **The towing assignment map does not explain the towing gap.** The city's keyless towing-assignment layer splits the city into two territories (wards 1-8, and 9-14 with part of 8). Wards 6-8 sit in the southern territory yet tag at 21-25 days like the north, so the boundary does not account for the gap; no keyless Streets or Forestry district layer was found. (observed; source: research/chapters/N3-fairness.md section 3; build/N3/boundaries.json)

- **The 'investigation done' stamp cannot measure time to inspection.** DATEINVTDONE is stamped within about a day in every ward 1-5 and after 7-64 days in wards 6-14 for Street Department types, which would show 25-fold gaps. But tow tags in wards 1-5 still take 6-15 days, so the stamp marks a desk step there, not a visit, and it is not used. (observed; source: build/N3/decisions.json n3-reject-invt-stamp)

- **The specified 42-day mowing threshold flagged almost every lot.** The build spec proposed listing rotation lots with no cut in 42 days; that flags 11,356 of 11,824 lots and says nothing. The city's own cycle runs about eight weeks (median longest gap 54 days), so the look-back flags gaps over 90 days instead (3,941 lots). (observed; source: build/N1/decisions.json N1-22; figure n1_mowing_gaps)

## Claims we cut back

- **'Re-filed within 30 days' measures recurrence, not false closure.** About 7% of closed requests (11,978 of 175,801 in 2025-26, counted by request) were reported again at the same address within 30 days, led by refuse and dumping (14.0% and 18.7% on the earlier row count). Refuse is collected weekly and dumping recurs at chronic sites, so this is 'came back'; only repairs that should last are used to say a fix did not hold, over 14 days, and that rate is 2.6%. (observed; source: prompts/night-v2/COMMON.md correction 4)

- **Our first reading of the harm test overreached.** We first concluded that the harm claim 'fails' because residents re-file at the same rate whether or not a cut was recorded. That test could not tell indifference from chronic lots or from residents giving up, so we withdrew the conclusion and ran the exit test instead. (observed; source: research/synthesis.md section 9a)

- **Two research-report figures used broader definitions than their wording suggested.** The research report's '14.6% blank outcomes' counted closed and cancelled requests together, and its '23.7% repeats' counted any two requests at one address within 12 months, including duplicates filed while the first was open. The post-closure figures are 3.8% closed with no text and 6.3% reported again within 30 days (7.0% counting requests rather than rows). (observed; source: research/synthesis-notes.md '311 closure integrity')

- **Counting CSV rows overstated requests by about 8%.** The city's 311 CSV repeats a request once per caller: 349,031 rows in 2024-26 hold 322,104 distinct requests. Earlier figures counted rows; tonight's count requests, which moves some medians slightly (cave-ins closed 'work completed', north: 25.1 days on rows, 23.1 on requests). (observed; source: build/N2/figures.json; build/N5/figures.json)

- **'One in four' vacant-lot requests with no cut billed was the wrong label.** The 24.8% figure counted closures reading 'on schedule to be cut' or 'added to rotation'. For 'on schedule to be cut' alone it is 21.4% (156 of 729), about one in five, and the wording follows the narrower figure. (observed; source: research/chapters/N8-verification.md finding 2)

- **One towing 'promise kept' share counted the wrong closures.** N3's 38% against 11% counted towing requests closed with any words by the promise date, including 'vehicle gone upon inspection' and blanks, the very error the entry exists to expose. Like for like (closed 'vehicle tagged for tow' within the promise) it is 32% against 4%, on only 271 requests in the north. (observed; source: research/chapters/N8-verification.md conflict 1)

- **The single-streetlight gap failed our robustness test.** Single light out was proposed as a lead like-for-like comparison: 'work completed' in 15.6 days in wards 1-5 against 41.0 in wards 10-14 since the tornado. Before the tornado it was 4.8 against 6.4, and the gap sits in requests filed October 2025 to March 2026, so it fails the rule fixed in advance and is not a lead. (observed; source: research/chapters/N3-fairness.md section 2; figure n3_single_light_done_median)

- **'Converted to a work order' is the rare tree pattern, not the usual one.** Of 345 silently cancelled tree inspections that match an open removal work order, only 9 were cancelled within a day of the order starting. 288 were filed while a removal order had already been open a median 575 days, so the usual story is 'already on the backlog, and nobody said so'. (observed; source: research/chapters/N5-heroes.md 'What failed or surprised me'; figures n5_tree_cancel_blank_*)

## Definitions that did not reproduce

- **The city's own due dates are not CityStat's goals.** Grading residential potholes against each request's own promised date gave 83.3% on time in Q2 2026, against CityStat's 90.6%, and the city's 311 due dates differ from CityStat's published goals for 3 of 9 services (alley potholes 16 days against 17; whole-block lights 2 days against 24 hours; critical signs 3 days against 48 hours). We keep the promise date because it is the city's own commitment, and list the difference as a question. (observed; source: context/NIGHT-PLAN.md item 2; research/chapters/N4-citystat.md section 5)

- **CityStat's preliminary quarters look better than they end up.** CityStat's on-time shares leave out requests still open, so a quarter read soon after it ends counts only the fast closures; in past quarters the reading 12 days after quarter end overstated the final by up to 18.5 points for residential potholes and 27.1 for alleys. Its claim that 2026 response times improved sharply is mostly the same age effect: at equal age the January-June averages are 10.6, 10.4 and 9.2 days for 2024, 2025 and 2026. (observed; source: research/chapters/N4-citystat.md sections 3-4; figures n4_drift_*, n4_h1_*)

- **The 'came back within 30 days' share did not reproduce exactly.** The registry gives 7.0% (11,978 of 175,801); the independent recompute gets 6.1% (10,790) with the same code, same address, filed after closure. The difference is not yet explained, so the figure should be quoted as 'about 6 to 7 in 100'. (observed; source: research/chapters/N8-verification.md recompute table)

- **CityStat's routing measure cannot be reproduced.** CityStat's only measure of the 311 bureau is routing within 2.5 days (99.99% of 10,853 requests in Q2 2026), but the public file has no routing timestamp. No subset of the file matches its counts convincingly (the best of 260,610 misses by 15% in Q2 2026), so no reproduced routing figure is published. (observed; source: research/chapters/N4-citystat.md section 4; build/N4/routing_search.json)

- **CityStat's Q2 2026 residential and alley pothole shares sit above anything the file supports.** Even on the day the file matches CityStat's Q2 counts, residential potholes read 86.2% against CityStat's 90.6% and alleys 92.0% against 98.2%. We could not explain the remaining 4-6 points; it is a question for CityStat. (observed; source: research/chapters/N4-citystat.md section 3; build/N4/q2_freeze.json)

## Things we dropped, and why

- **Files fetched from slmpd.org against its robots file are not used.** An early research thread downloaded some files from slmpd.org although its robots file bars automated agents; none of them are used anywhere in this entry. (observed; source: research/data-audit.md 'Read this first' item 1 (robots file observed 14 Oct 2026 00:36 UTC); no script under scripts/night/ reads data/raw/slmpd/ (checked 14 Oct 01:45))

## Data that does not exist or could not be used

- **The sidewalk inventory has no repair dates.** The city's sidewalk layer has a DateRepair field, filled on 0 of 36,822 segments (and 0 of 7,932 curb ramps). There is no public record to join a sidewalk request to a repair, so sidewalks became a register row. (observed; source: build/N2/figures.json (n2_sidewalk_daterepair_filled))

- **No shelter-bed data exists to show.** The city's unhoused challenge asks where people are and which resources they need, but no bed-availability record was found in any public source. A location tool could be built from encampment requests, but it would map where people sleep, so it was not built. (observed absence; source: research/synthesis.md sections 2n and 7b)

- **No keyless live 311 feed, and no CityStat export.** The city's Open311 and address APIs return HTTP 400 without a city-issued key, and CityStat's Tableau views ask for a sign-in to export. The pipeline therefore runs on the weekly bulk file, and CityStat's figures were read from its pages. (observed; source: research/data-audit.md 'Read this first' item 4; synthesis-notes A.5)

- **No city dataset states a licence.** None of the 72 datasets in the city's catalog has a licence value, and no export, API or map layer states terms; no open-data policy, ordinance or executive order was found. Reuse rests on the files being published, which the write-up says plainly. (observed absence; source: research/data-audit.md 'Read this first' item 5; research/what-gets-adopted.md 3.5)

- **Only a sample of the city's work orders is public.** The entry uses only the work-order lists the city publishes as public saved searches, which hold about a third of the tree work orders (1,500 of 2,522 removals; 1,500 of 6,276 trims). Every tree work-order rate is therefore a lower bound. (observed; source: research/synthesis-notes.md A.6; context/NIGHT-PLAN.md 'Cut scope')

- **The city's ARPA exports do not reconcile.** Project-level ARPA expenditures total $403,080,817 while the expenditure rows sum to $101,214,949. The ARPA-tracker idea was dropped, partly for this and partly because residents are not measurably affected by the process. (observed; source: research/synthesis.md section 2q-2u)

- **Two more completion joins were too weak to use.** The Forest ReLeaf planting sample matches only 0.3% of requests closed 'approved for next available planting', and the forestry ledger stopped recording debris clean-ups after 2021. Both stay visible in the register as weak or missing records. (observed; source: build/N2/decisions.json n2_keep_negative_results; build/N2/joins.json)

- **No aerial imagery shows the 2026 grass.** The state imagery server's newest St. Louis imagery is from 2025, so hero images show what each block is, not whether a lot was cut this year. Imagery therefore carries no claim. (observed; source: research/chapters/N5-heroes.md Admission)

## Things we looked for and did not find

- **No output from GeoSTL's satellite mowing work, and no per-lot mowing log.** GeoSTL told television in August it had been working with the city on satellite mowing priority, and CityStat's manager said a per-lot log was 'hopefully coming in the next couple of weeks'. Neither was found by mid-October; whether either exists inside the city is one of the questions for the COO's office. (observed absence; source: research/synthesis.md sections 1a and 5)

- **No representative survey of residents about city services.** No city-commissioned or representative survey of residents about services or priorities was found for 2021-2026. Resident voice rests on requests, reviews and news accounts, and several outlets and forums (Post-Dispatch, KSDK, Nextdoor, Facebook) were not reached. (observed absence; source: session transcript 3da744d3 (voters thread summary); research/synthesis.md section 0)

- **Imagery terms for a public video are unresolved.** The state's aerial imagery server is keyless and listed by the city as a resource, but its bundled metadata for the 2022 and 2024 orthophotos reports a no-redistribution clause. Imagery is used as a visual only, and whether that clause allows a public video is still open. (reported (clause), open (application); source: research/synthesis-notes.md A.3)

- **No person has yet reviewed the closure classes.** The class table was drafted by an AI model and checked for internal consistency (code and SQL agree on all 2,992 pairs; a second agent's independent rules agree on 98.4% of closures). The city's policy treats AI output as a draft, so the table is open to review but not yet reviewed; ten distinct texts carry about 60% of hand-off closures, or about 40 type-and-text pairs for a per-type review (N8). (observed; source: research/chapters/N2-what-closed-means.md Admission; figure n3_class_agreement_n2_vs_n3)

- **Whether the board-up date is the completion date is unverified.** The board-up layer's DateBoardedUp falls after its DateCreated in 86% of 2025-26 records (median 22 days later), which fits a completion date. Its meaning is not documented, so the board-up figures rest on the field name. (inferred; source: research/chapters/N2-what-closed-means.md Admission)

