# Street Department: keep the request open until the repair is done

**For** Street Department supervisors and whoever takes 311 hand-offs to street maintenance. **Covers** cave-ins (the test type) first. Sidewalk repair, sewer lateral defects and bad condition follow the same pattern.

## 1. At the hand-off: attach the crew's job

Today a referred cave-in is closed "referred to street maintenance for repair work to be scheduled", or "sent to street maintenance for repair". Only 16 of 40 sampled referrals list a "Right of Way Repair" work order (*observed*).

- **Create the repair work order from the request:** Related Work Activities > Create. It inherits the request's comments and priority (*documented*). If the order already exists, attach it with > Add.
- The admin first associates the repair work-order template with the Cave-Ins request template (*documented*).
- Sidewalks ("already on sidewalk program") and sewer laterals ("added to sewer lateral repair program") attach the programme's work order the same way.

## 2. Set the status; don't close it

| Situation | Today | Instead |
|---|---|---|
| Repair order attached | Closed, "referred to street maintenance…" | **Dispatch.** Cityworks closes the request when the order closes (*documented*) |
| Sent for evaluation | Closed, "refer to street inspector for evaluation" | **Pending.** Attach the order when the inspector writes one |
| Done on the spot | Closed, "street maintenance work completed" or "asphalted" | No change: these words say the work was done |

Where the link exists, the repair is fast: filing to finish took a median of 5 days, against a 3-day promise (*observed*). Linking costs the crew nothing; it makes the finish visible.

## 3. Each week: work the past-due list

Take about **25 rows from the top of the ranked list**: roughly 75 minutes (*assumed*). Also clear the Close-out list, the records already showing the work done.

| You find | Do this |
|---|---|
| **Done**: actual finish, or the street is repaired | Verify; close the work order (the request follows) |
| **Waiting**: an order exists but isn't linked | Link or dispatch it; set Dispatch |
| **Missed**: no order, and the cave-in is still there | Create the repair order now; leave the request open |

On 13 October your ranked list held 4,106 requests, 1,173 of them cave-ins. Oldest first, 1 of the top 25 was life-safety; ranked, all 25 were (*observed*). For 1,196 of the 1,233 overdue cave-ins, no record says whether the repair was done (*observed*). The quarter should bring that to zero.

## 4. What the resident's status page shows

- **Today:** "Closed", "referred to street maintenance for repair work to be scheduled". Work order: none attached.
- **After:** "With Street Maintenance since" the referral date, the due date, "Not yet done", and the street repair order listed as open. The page already lists attached orders and their status (*observed*). It closes by itself when the order closes.

The "after" wording is our spec for the city's page; see the prototype at `site/status.html` (the cave-in). Figures and sources: [figures.csv](figures.csv).
