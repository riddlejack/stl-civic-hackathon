# Building Division: keep the request open until the building is secured

**For** Building Division supervisors and whoever takes 311 hand-offs. **Covers** unsecured vacant buildings (board-ups), building collapse and property-maintenance complaints. Building is not one of the three test types, but the same practice applies.

## 1. At the hand-off: attach the crew's job

Today Building closes at the hand-off: "referred to board up crew", "issued notice of violation", "already under notice". None of 200 sampled Building hand-off pages has anything attached (*observed*). The job does exist: 80% of board-up referrals got an order in the division's board-up layer within 2 days (*observed*). Whether that order, or a code case, is a Cityworks work order is *not established*.

- **Board-up order in Cityworks:** attach it (Related Work Activities > Add) or create it from the request (> Create) (*documented*).
- **Board-up order kept outside Cityworks:** keep the request open; close it by hand at the boarded date, with "building was secured by city".
- **Notice of violation:** the job is the reinspection. Attach the inspection if it is in Cityworks; otherwise keep the request open to the reinspection date (*our design*).

## 2. Set the status; don't close it

| Situation | Today | Instead |
|---|---|---|
| Board-up order attached | Closed, "referred to board up crew" | **Dispatch.** If the order is in Cityworks, the request closes with it (*documented*) |
| Notice issued | Closed, "issued notice of violation" | **Pending** until the reinspection |
| Secured on the spot | Closed, "building was secured by city" | No change: these words say the work was done |

Board-ups get done, but late. Of 1,528 referrals in 2025–26, 17.0% were boarded by the promised date and 64.6% late (median 26 days) (*observed*; the layer misses about one board-up in five and dates some late, so part of "late" may be the record's delay). After an owner notice, the city's board-up record later shows a board-up for 72.8% of the buildings, mostly late (*observed*). Notices usually end in city work, so keep them tracked.

## 3. Each week: work the past-due list

Take about **25 rows from the top of the ranked list**: roughly 75 minutes (*assumed*). Also clear the Close-out list.

| You find | Do this |
|---|---|
| **Done**: a boarded date, or a passed reinspection | Verify; close with words that say so |
| **Waiting**: an order or notice exists but isn't linked | Link it, or record the reinspection date |
| **Missed**: no order, and the building is still open | Re-dispatch to the board-up crew; leave the request open |

On 13 October your ranked list held 1,149 requests, led by exterior maintenance (370), open storage (235), interior maintenance (195), unsecured vacant buildings (142) and building collapse (73). Oldest first, 2 of the top 25 were life-safety; ranked, all 25 were (*observed*).

## 4. What the resident's status page shows

- **Today:** "Closed", "referred to board up crew". Nothing attached.
- **After:** "With the board-up crew since" the referral date, the due date, "Not yet done". It closes when the building is secured. A notice reads "Notice issued; reinspection due" with the date.

This is our spec for the city's page. The prototype (`site/status.html`) shows a lot, a tree and a cave-in, not a building. Figures and sources: [figures.csv](figures.csv).
