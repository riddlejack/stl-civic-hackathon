# Question standard: which problem Jack takes to the mayor's office

Written Tuesday 13 October 2026, about 8:30 p.m. Central, before any research
report was opened. Follows part B of the partner standard. Sources for the
facts here: `AGENTS.md`, `context/HACKATHON_CONTEXT.md`, `context/HANDOFF.md`
section 2 (Jack's own words, which bind).

## 1. Kind and use

A **which-of-several** question: which one problem, with a tool pitched for
it, becomes Jack's hackathon entry. A design question sits underneath it (what
the tool does), but only at the level needed to choose between problems.

What Jack does differently with the answer: from Wednesday noon he builds one
thing, reports progress on it Wednesday afternoon, and records a two-minute
demo of it by Thursday 2 p.m. A wrong pick costs the whole build window; there
is no second attempt.

## 2. Decision and decider

Jack decides, by **Wednesday 14 October, noon Central**. He works alone with
agents, virtually, in the Community division. The deliverable is a two-minute
screen demo on YouTube by Thursday 15 October, 5:30 p.m. Central.

Constraints that bind: no contact with the city before submission (agents may
contact no one; Jack has emailed Mike Seper once and may do so again); the
demo may show no personal data about private people; the tool must be
something the mayor's office could run.

Not a constraint: build time. Jack removed it ("humans and agents alike always
underestimate just how much you can build with LLMs"). Not a constraint: being
one of Ben's problems ("i dont think it needs to be one of bens problems").

Missing facts, and what is done with each:

- Ben's full list of problems: only graffiti and trees are known. Asked of
  Mike Seper by email at 6:24 p.m.; no reply yet. **Assumed** the list stays
  partial through Wednesday noon; the decision must not depend on it.
- Judging rubric, judges, prizes: none found. **Assumed** none exists; the
  kickoff's stated tests (why it matters, the story, a route to use) stand in.
- Submission destination: unknown. Does not affect which problem is chosen.

## 3. Options

Candidates come from five places, and every candidate gets the same test:

1. problems Ben presented (graffiti, trees, and any later confirmed);
2. problems the city tracks and is behind on (CityStat and open data);
3. problems nobody in the city owns but someone should;
4. proposals raised at the kickoff (potholes, urban heat and planting,
   drones, overgrown lots, help for elderly neighbours, hazard trees, a crime
   detection device);
5. anything the research surfaced that nobody expected.

For each strong candidate, two more variants are tested: a **narrower** one,
and one that **improves or replaces an existing city tool** rather than adding
a new one.

The baseline option, "keep things as they are", is: take one of Ben's two
named problems as stated and build the obvious tool for it. Every other
candidate must be shown better than that, on the terms below. Not entering is
not an option.

## 4. Goal and comparison

What counts as better, in Jack's words: the entry is **implementable by the
mayor's office**, not reliant on "exorbitant government funding or constraints
that are out of our control, like labor"; it has a **wow factor** that comes
from "finding issues that people in St. Louis actually struggle with or
actually need"; and the data for it can be got. The aim is "a solution that
St. Louis adopts and the mayor's office adopts". Winning the hackathon and
being adopted are treated as the same goal, because the kickoff said
compelling work would be taken seriously and the organisers named no other
test.

**Firm requirements** (failure alone drops the candidate):

- **F1. No new city staff.** The tool runs with people the city already
  employs, inside duties they already have, or with residents and volunteers.
  No hire, no new contract labour, no new role. Jack: "having to hire ppl is a
  huge downside/barrier to implementation."
- **F2. Residents are measurably affected.** There is observed evidence
  (something people did or something that happened to them, not something
  they said) that St. Louis residents bear the problem. Jack: a solution where
  "no one cares ... or it doesn't actually help people ... is not a winner".
- **F3. The demo runs on real St. Louis data that we hold.** Rows retrieved,
  not a catalogue entry, and no personal data about private people on screen.

**Weighed with evidence**, never used alone to drop a candidate. Jack's own
examples of what must not exclude an excellent idea are the first four.

- **W1. An existing tool.** Weigh whether the existing tool is poor, unused,
  or "only boxchecking", and whether ours would "do real good" over it.
- **W2. Data not yet collected.** Weigh whether it can be found elsewhere,
  derived, or produced by the tool itself.
- **W3. No owning department.** Weigh whether the problem should be owned and
  who would plausibly take it.
- **W4. More than one person must agree.** Weigh how many, who, and whether
  they have shown they already agree.
- **W5. Money to run it.** Hosting, keys, licences; whether it stays under
  whatever the city can spend without a procurement process.
- **W6. On the agenda.** Whether the mayor's office or Ben has said this
  matters, or the city is visibly behind on it, or a deadline in the next six
  months forces it.
- **W7. Demo-ability.** Whether a two-minute screen demo can show it working
  and carry the story of who is helped.
- **W8. Legal footing.** No city dataset states a licence; weigh whether that
  matters for this data and this use.

Value choices left to Jack: how much W6 (being on Ben's list, with the
certificate tied to it) is worth against a stronger need elsewhere; and how
much a broad, modest improvement is worth against a narrow, large one.

Options are compared by judgment on these terms, without scores.

## 5. Deciding conditions

For any candidate to be the entry, these must hold, ranked by doubt, most
doubtful first:

1. **Someone in the city would use it.** A named role (not a department)
   whose existing duties include this work, and the count of people whose
   yes is needed. Most doubtful because no one can be contacted before
   submission, so it rests on public statements and job descriptions.
2. **It does something no existing tool does, or does it materially better.**
   Doubtful because existing tools are easy to miss and hard to judge from
   outside.
3. **Residents are measurably affected (F2).** Less doubtful: the city
   publishes service and outcome data, so this should be settleable.
4. **The data to demo it is on disk (F3).** Settleable by looking.
5. **It runs with no new staff (F1).** Settleable by reasoning from the
   tool's design and the roles in 1.
6. **Its effect can be measured with data the city already produces.** This
   is the success metric; see section 7.

## 6. What would count

| Condition | Counts | Does not count | Flip value, set before evidence |
|---|---|---|---|
| 1. A user in the city | A job title or named office whose published duties cover this; a public statement from that office wanting it; a CityStat measure it already reports | Our assertion that "the city would want this"; a department name alone | Needs more than three separate approvers with no sign of agreement: a heavy mark against, not a drop |
| 2. Better than what exists | The existing tool found and tried, with what it does and does not do; usage or outcome figures showing it fails | The absence of a tool because nobody looked | If the existing tool does the same job and is in use, the candidate falls unless ours is shown to be materially better |
| 3. Residents affected | Request counts, backlogs, closure times, incident or outcome counts, court or agency records, what people did in surveys | News and forum mentions (attention, not need); what people say they would do; anecdotes | Fewer than about 1,000 residents, requests or incidents a year, and no cost or harm figure to offset that: too small for the mayor's office. Jack to confirm or move this line |
| 4. Data on disk | Row counts, date ranges, retrieval URLs from the audit | A catalogue page; "Live" labels | Data older than 2024 with no newer source: a mark against, not a drop, unless the tool is about current conditions |
| 5. No new staff | The roles that would run it already exist and already do related work | "A volunteer could do it" with no volunteer base shown | Any need to hire: drop |
| 6. Measurable effect | A figure the city already publishes (CityStat) or one derivable from open data, with its current value as baseline | A metric only the tool itself would produce, with no baseline | None; absence is a finding, recorded as open |

Unknowns to bound, each end from a real case: the cost to run (lower end: a
free tier; upper end: the city's small-purchase threshold, to be found in the
research); the number of approvers (lower end: one office head; upper end:
Board of Aldermen action).

## 7. How success will be measured

Two levels, each with a measure that can be read without asking anyone.

**At the hackathon.** Success is an adoption signal from the city, in this
order of strength: a city employee uses the tool on real work; Ben's office
asks for the code or a meeting; a certificate or recognition. The demo
itself must end on the measure below, with its baseline, so a viewer can see
what would change.

**In the city.** Every candidate names one outcome figure the city already
publishes or that can be computed from retrieved data, its current value
(the baseline, labelled observed with URL), the direction the tool would move
it, and when a change would be visible. A candidate with no such figure is
recorded as open on condition 6, which counts against it but does not drop it.

## 8. Shape and stopping point

Jack receives `research/synthesis.md`: the shortlist first, each strong
candidate with the problem, one or two tool ideas in a few sentences, what it
has over the others, and which I would pick and what would switch me; then
every candidate on the tree with evidence quoted; the decomposition; the
rejects with reasons; what is open for the strongest few and how to settle
each by Wednesday afternoon; two or three questions for Ben's office; and the
self-check against part A.

Precision needed: enough to choose between candidates, not to design one.
Done when each shortlisted candidate meets F1 to F3 with quoted evidence and
every weighed item is either evidenced or marked open with what would settle
it, or when Wednesday noon arrives and the answer says what is left.

## 9. What would make it useless

- Picking on attention rather than need: a problem that is loud in news and
  forums but whose service and outcome data show little harm.
- A candidate that passes only because something was not looked for: an
  existing tool, a licence term, or a data gap found on Thursday.
- A pick whose demo cannot run on data we hold, so Thursday shows a mock-up.

## 10. Depth

Standard overall. Deep on conditions 1, 2 and 3 for every shortlisted
candidate. Quick on the rejects: one line each saying which condition fails.

## 11. What I took from the previous session's draft, and what I rejected

Read after sections 1 to 10 were on disk.

Taken:

- The "Lever" idea: the tool should change which job is done next or remove a
  step, not create work nobody is staffed to do. That is the plainest test of
  F1, and I have folded it into condition 5 and leaf 3.1 below.
- "Not having come across one" does not count as evidence that no tool
  exists. Kept as the second failure in section 9 and in leaf 2.
- Flip values on data freshness ("newest record no more than a month old" for
  a tool that guides daily work). Adopted as a weighed mark in section 6,
  row 4, not as a drop, because Jack said data gaps must not exclude an idea.
- Success measured as an adoption signal first, with the city's own published
  measure as the outcome; and that the expected change should be stated
  beforehand with its inputs labelled. Section 7 says the same.
- Its working hypothesis (a service the city tracks and is behind on, where
  public data changes which job gets done next) is kept as **one candidate
  class to test**, option class 2 in section 3, and not as a finding.

Rejected, with reasons:

- Seven knock-outs. Jack rejected these and I agree: "Easy yes", "Gap",
  "Data" and "Owner" can each exclude an excellent idea on a technicality. They
  are W1 to W4 here, weighed with evidence.
- "Owner: a named department already tracks a measure of it." Jack's own
  example is a problem nobody owns but someone should. Ownership is now
  evidence under leaf 3.3, and its absence is a finding, not a drop.
- "Data: reachable by a public link without a key." Too strict for a demo
  built from files already on disk; what matters for Thursday is the rows we
  hold (F3), and what matters for adoption is that the city holds the data
  (leaf 3.4), which it does for its own records.
- Ranking the must-haves "most doubtful first" without saying what doubt
  means. Here, **doubt means hardest to establish from desk research, not
  least important**. The firm requirements are the most important things in
  this standard; two of them are also the easiest to settle.
- Goal order "adoption, then help, then demo, then Jack's portfolio". Jack
  treats adoption and help as one goal (a tool nobody needs will not be
  adopted), and the portfolio value is not in his words, so it is out.
- The cut by stakeholder (city, residents, viewer, Jack). It mixes kinds of
  test under each party and puts "Data" under Jack, where it has no bearing on
  the city's decision. See the cuts considered in section 12.

## 12. The tree for testing any idea

Root question: **should this idea be the entry?** Built to work for any idea
proposed later, not only candidates found in the research.

### Frame

- Decider: Jack, by Wednesday noon. Action enabled: start building one thing.
- Undesired result (R1): Thursday's demo shows a tool that no one in the city
  would run, for a problem residents do not measurably bear, or on data that
  is not real; the city does not follow up.
- Desired result (R2): a two-minute demo on real St. Louis data of a tool a
  named city role could run next week with no new staff, for a problem
  residents measurably bear, that does something no existing tool does; and
  Ben's office follows up.
- Solution stance: each candidate is a proposed solution, so the tree is a
  criteria tree: conditions that can each pass, fail, gate or weigh.

### Working hypothesis

The entry that gets adopted replaces a judgment a city employee now makes by
hand with worse information, and the demo shows a finding in the city's own
data that its leadership did not know. For this to hold: (a) a named role
already makes that judgment; (b) the city's own records show residents bear
the cost of it being made badly; (c) no tool the city runs already makes it.

The rival to test: a resident-facing tool (one that helps residents do
something) rather than a staff-facing one. The discriminating evidence is
leaf 3.1: whether the user who already exists is a city role or a resident
channel the city would host. The tree works for both.

### Cuts considered

1. **By whose decision the outcome depends on** (city, residents, viewer,
   Jack): the previous session's cut. Reveals who must say yes; hides that one
   fact (the data) bears on several parties; mixes kinds of test under one
   party. Set aside.
2. **By stage on the path to adoption** (demo, noticed, tried, run routinely,
   residents see change): a funnel. Reveals the adoption bottleneck; hides the
   firm requirements, which do not sit at one stage; reads as a plan rather
   than a test. Set aside.
3. **By the distinct ways the entry would fail** (criteria): nobody is helped;
   nothing new; the city cannot run it; it cannot be shown; its effect cannot
   be seen; nobody in the city wants it; it harms someone. Each is a condition
   that can independently pass, fail, gate or weigh, and Jack's firm/weighed
   split maps onto gates and weights. A wrong answer is easiest to disconfirm
   here, because each branch has a plain fail state. **Chosen.**

Pattern check: the closest cards are "product roadmap" (an option set against
common criteria, must-haves separated from weights) and "policy portfolio"
(target population, mechanism, delivery feasibility, distributional effects,
unintended consequences). The policy card showed one missing branch, harm the
tool itself could cause, now branch 7.

### The full tree

Root, cut by: **the distinct way the entry would fail**. Siblings are
exclusive because each names a different party or resource that fails:
residents (1), the existing tool set (2), the city's resources (3), the
Thursday demo (4), the measurement (5), the city's wish (6), third parties
(7). Together they cover the goal in section 4. Deliberately not covered:
Jack's build time (removed by Jack) and his portfolio value (not in his words).

**1. Need: residents measurably bear this problem.** Gate (F2).
Cut by: the kind of observed evidence of harm. Exclusive because each is a
different record of a different act.
- 1.1 Residents act on it: service requests, complaints, filings, calls, with
  counts by year and by ward. Closes when a count with a date range and URL is
  quoted, or none is found.
- 1.2 Residents suffer outcomes from it: incidents, injuries, evictions,
  losses, costs, delays they wait through. Closes the same way.
- 1.3 Residents report it in surveys of what happened to them, by area.
  Weaker; what people say they would do does not count.
- 1.4 Who bears it: concentration by ward or group. Context for the story and
  for branch 7; does not gate.
Assignment rule: news and forum volume is attention and sits in branch 6, not
here.

**2. Gap: it does something no existing tool does, or does it materially
better.** Weighed (W1); gates only if an existing tool does the same job and
is in use.
Cut by: where the existing capability could live. Exclusive by owner of the
tool.
- 2.1 The city's own tools: 311, CityStat, department systems, maps, forms.
- 2.2 Partners' and vendors' tools: non-profits, the region, the state,
  commercial products the city buys.
- 2.3 How the existing tool performs: use, outcomes, complaints about it.
  This is the "boxchecking" test, and it is where an excellent idea that
  replaces a poor tool passes.
Assignment rule: a tool's existence goes in 2.1 or 2.2; how well it works goes
in 2.3.

**3. Runnable: the city can run it with what it already has.** Mixed.
Cut by: the resource the city would have to supply. Exclusive by resource.
- 3.1 People. Gate (F1): no new staff, no new contract labour. Then weighed:
  for a staff tool, a named role whose existing duties include this work; for
  a resident tool, the channel through which residents would reach it and the
  office that would host it. Where no role owns the problem (W3), the leaf
  records who plausibly should.
- 3.2 Money. Weighed (W5): the cost to run it a year, against what a
  department can spend without a procurement process.
- 3.3 Approvals. Weighed (W4): who must say yes, how many, and whether they
  have shown they already agree. An aldermanic vote or a new ordinance is the
  heavy end.
- 3.4 Data and legal footing. Weighed (W2, W8): whether the city holds or can
  collect the input data the tool needs; whether any licence or personal-data
  rule stops the use. If the data does not exist yet, the leaf records whether
  the tool itself could collect it.
Assignment rule: whether someone does the work goes in 3.1; whether someone
can authorise it goes in 3.3; whether the data exists for the city goes in
3.4; whether we hold it for Thursday goes in 4.1.

**4. Shown: a two-minute screen demo on real data carries the story.**
Cut by: what the demo needs. Exclusive by artefact.
- 4.1 The rows are on disk. Gate (F3): row count, date range, retrieval URL,
  the fields the demo depends on present.
- 4.2 No personal data about private people appears on screen. Gate.
- 4.3 The story fits two minutes: a viewer sees who is helped and what the
  city would do next week. Weighed (W7).

**5. Measured: the tool's output changes an action that moves a figure the
city already produces.** Weighed; this is the success measure.
Cut by: where the baseline figure comes from. Exclusive by publisher.
- 5.1 A CityStat or other published city figure, with its current value.
- 5.2 A figure derivable from open data we hold, with its current value.
Each leaf also records the direction the tool would move it and when a change
would be visible. No figure at all is recorded as open and counts against.

**6. Wanted: someone in the city has signalled this matters.** Weighed (W6).
Cut by: who signalled. Exclusive by source.
- 6.1 Ben presented it (the certificate is tied to these).
- 6.2 The mayor or senior staff have said so publicly.
- 6.3 A deadline or pressure in the next six months forces it.
- 6.4 The city is visibly behind its own target on it.
- 6.5 Residents and press are paying attention to it (attention, not need).
Assignment rule: a missed target as evidence of harm goes in 1.2; as evidence
the city cares, here in 6.4.

**7. Harmless: the tool does not shift harm onto some residents or expose
them.** Weighed; gates for surveillance of people.
Cut by: the kind of harm the tool could cause. Exclusive by mechanism.
- 7.1 Reallocation: who gets less service if the tool changes priorities.
- 7.2 Exposure: whether it watches, identifies or reports private people.
- 7.3 Wrong output: what happens if it is wrong, and who notices.

### Prioritisation and the pruned spine

Ranked by how much each could change the answer, times how uncertain it is
from desk research:

1. 3.1 (a user who already exists): highest; cannot be asked before
   submission.
2. 2.1 to 2.3 (gap): high; tools are easy to miss.
3. 1.1 and 1.2 (need): high impact, settleable from city records.
4. 4.1 (rows on disk): high impact, low uncertainty; look.
5. 6 (wanted): medium; evidence sits in the mayor's statements and pressures.
6. 5 (measured): medium; quick to check against CityStat.
7. 3.3 (approvals): medium.
8. 7 (harm): low for most candidates, decisive for a few (anything watching
   people or reallocating service).
9. 3.2 (money), 3.4 (legal), 4.2 (personal data), 4.3 (story): quick checks.

Pruned spine, what one reader holds while deciding: **1.1/1.2, 2.1–2.3, 3.1,
3.3, 4.1, 5, 6.** Seven tests. The rest are quick checks recorded in one line
per candidate. Deferred: 1.3 (surveys; reopened if 1.1 and 1.2 are empty),
1.4 (reopened for the story), 7 (reopened for any candidate that touches
enforcement, surveillance or reallocation). Risk if the deferral is wrong: a
candidate that quietly shifts service away from poorer wards passes. The
reopen rule guards it.

### What would restructure this tree

- Ben's written document or a rubric arrives with explicit judging criteria:
  branch 6 gains a sub-branch and may become a gate.
- The city offers non-public data or a key: 3.4 and 4.1 change, and candidates
  rejected on data reopen.
- Jack moves F2 from gate to weight, or sets the 1,000-a-year line elsewhere:
  branch 1 re-weights, not re-cuts.
- A candidate is a policy or a programme rather than a tool: branch 3 would
  need a delivery-capacity sub-branch and this tree would not fit.

## 13. Jack's answers, Tuesday 13 October about 9 p.m., and the edits applied

1. **The decision and goal: yes.** "Would be adopted by the mayor's office"
   is the measure of success. Jack pasted the kickoff transcript he has (the
   same excerpt summarised in `HACKATHON_CONTEXT.md`). Phrases from it now
   treated as observed, from the organisers' own mouths: Ben, "for all the
   submissions that come forward to these problems, we'll be providing each of
   you with a certificate of appreciation from Mayor Spencer"; Ben, "if it's a
   particularly compelling one ... we're going to take these seriously"; Mike,
   "ideally gets adopted by the city, or at least something that gets on the
   mayor's desk"; Mike, "even better, if it's something that's open source and
   already built, that they can deploy"; Mike, "it's really the personal story,
   why this is important"; Mike, "think as grand as possible ... it's always a
   lot easier to scale down"; Mike, "not likely to be monetized".
2. **Options: yes**, with the test "solves a real problem for citizens of
   STL" plus whatever else serves the hackathon's purpose. Two weighed items
   added from Mike's words: **W9, open source and deployable as built** (he
   named it as "even better"), and the **personal story** is now part of W7.
3. **The three firm requirements stand.** No additions.
4. **Most doubtful condition: depends on the tool.** Jack: a tool government
   officials use directly is "an easier bar to clear"; one that needs adoption
   by citizens "gets harder to prove". Applied to leaf 3.1: a resident-facing
   candidate carries a heavier burden there (it must show the channel residents
   would reach it through and the office that would host it) and on branch 5
   (how adoption would be seen). A staff-facing candidate needs the named role.
5. **The answer's shape: yes.**

No facts volunteered beyond the transcript.
