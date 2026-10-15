# R3c. Method memo: three lenses on "closed is not done"

14 Oct 2026, about 12:45 p.m. Central. I read only the three named book texts in `/Users/jackriddle/.keystone/practice-library/book-text/`; line numbers refer to those files, and the extracts and checks are in `build/R3/work/E-books.md`. Entry figures come from N1–N5.

**Summary.** All three methods say the same thing: judge the job, not the 311 step.
- **Kepner-Tregoe.** Mapping where the problem is and is not shows a missing condition, not a change: nothing joins the request to the work record.
- **Rumelt.** On-time rates are results, not a diagnosis. DoneStat supplies the diagnosis and one coherent action, but it is not a strategy on its own.
- **Value stream mapping.** Lead time runs until the job is done as the resident sees it, so a 311 closure ends only the intake segment.

## 1. Kepner-Tregoe: specify, then test causes (*The New Rational Manager*, ch. 2)

**Deviation.** A request should close when the work is done. The mayor's transition committee defined closed as "action taken". Instead, 35.2% of 175,876 closures since January 2025 record a hand-off, and only 19.5% of requests with a due date closed by it with words saying the work was done.

| | IS | IS NOT |
|---|---|---|
| What | Weeds at lots and buildings (83–85% hand-off); unsecured buildings (90%); tows; cave-ins; tree inspections | Potholes, single lights (5–9%) |
| Where | First step in wards 10–14: tow tag 36.9 vs 12.0 days; cave-in referral 41.7 vs 0.8 | Work recorded as done: lights 0.7 vs 0.7 days; potholes 6.9 vs 8.0 |
| When | Minutes after filing (weed medians 5 and 23 minutes) | Any change: 31–39% hand-off in every quarter |

**What the specification says.**
- **Distinction (inferred).** In the IS types, a unit other than the closer does the work and keeps the record: Forestry's ledger, Building's board-up layer, the Towing Division.
- **No change.** The share is stable, so this is KT's case of performance that was never acceptable: look for a missing condition, not a change (L2958–2963).
- **Testing.** A cause "must explain both the IS and IS NOT data in each dimension" (L2135–2136).
  - "Staff close early for CityStat" fails, because potholes close "done" under the same goals.
  - "No link to the other unit's record" passes. It still needs verifying with the city: does Cityworks link work-order completion to the request?

**Warnings.** KT says to separate bundled problems: the ward gap is a second, first-step problem, and its cause is untested. KT also says to verify in the field: "no cut billed" is not "not cut", and CityStat says some lots are mowed by others.

## 2. Rumelt: diagnosis, guiding policy, coherent action (*Good Strategy / Bad Strategy*, ch. 3, 5, 7)

**Diagnosis.** "Underperformance is a result. The true challenges are the reasons for the underperformance." (L1140–1141). The reason here: the city's record of a request ends at the hand-off, and the record of the work sits in files nobody joins back. The mayor's office already holds the cheap levers, 311 closure rules and CityStat definitions; crews are the expensive half.

**Guiding policy.** Count a request as done only when a completion record or a done-word closure exists, graded against the city's own promise date. The city has already set this rule for towing.

**Coherent actions.**
- The weekly join.
- The receipt for residents.
- A register of the 13 services with no completion record, which gives EO 96's asset programme a starting list.
- A "done by promise" column in CityStat.

**Proximate objective** (L2072–2075). Publish weekly, for the four services that have records, the share done by the promise date.

**Warning.** A measure can be met by the wrong action (Rumelt's Los Angeles test-score case, L1137–1139). If "done" means "billed", billing without cutting scores. Keep a small field check.

## 3. Martin and Osterling: lead time and hand-offs (*Value Stream Mapping*, ch. 1 and 3)

**Lead time.** The resident's stream runs from report to cut, tow or board-up. A 311 closure ends only the pre-service segment, the top line of the book's two-timeline map (L2285–2324). On service agreements the book says: "document the actual lead time, not the lead time stated in the agreement" (L1896–1897). The promise date is that agreement.

**%C&A (percent complete and accurate).** From the resident's side, an "on schedule to be cut" closure is complete and accurate only if a cut follows. For lots in 2026 it is at most about 79% (21.4% had no cut billed all season). For "referred to board up crew" it is 19% within the promise. Both figures are inferred proxies taken from records.

**Hand-offs.** The book's steepest lead-time cuts come from removing hand-offs (L2512–2513). The north's extra wait sits in the first one.

**Warning.** Records cannot show process time. VSM also faults maps that lead to no action and asks for one owner of the whole stream. Here the natural owner is the Mayor's Office CityStat team and its weekly cabinet data reviews with the mayor (described by the COO, 2 Apr 2026).

## What this changes for the entry

1. Lead with the city's own words, "action taken" and the towing rule, then the 35%.
2. Treat the ward gap as a separate first-step problem whose cause is not yet tested.
3. Pair the measure with an owner (CityStat), a routine (the Monday list) and a small field check.
