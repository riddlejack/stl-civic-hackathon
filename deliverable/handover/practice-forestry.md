# Forestry: keep the request open until the crew's job is done

**For** Forestry supervisors and whoever takes 311 hand-offs. **Covers** tree inspections that become removals or trims, and vacant-lot mowing (Weeds-Vacant Lot, Missed Cut - V Lot, Unsatisfy Cut - VLot).

## 1. At the hand-off: attach the crew's job

- **Trees.** You already do this. All 40 sampled requests closed "removal work order created" list their work orders (*observed*). Keep doing it, for trims too ("trim work order created").
- **Vacant lots.** Today nothing is attached: 0 of 80 sampled vacant-lot and vacant-building requests closed "on schedule to be cut" show a work order (*observed*). Attach the lot's cut work order (Related Work Activities > Add), or create one from the request (> Create) (*documented*). Whether rotation cuts are kept as Cityworks work orders is *not established*.

## 2. Set the status; don't close it

| Situation | Today | Instead |
|---|---|---|
| Removal or trim order attached | Closed, "removal work order created" | **Dispatch.** Cityworks closes the request when the order closes (*documented*) |
| Lot with a cut order attached | Closed, "on schedule to be cut" | **Dispatch** |
| Lot with no crew job (off the rounds) | Closed, "on schedule to be cut" | **Pending.** Close by hand with "grass cut" once a cut is recorded |
| Same lot reported again | Closed again, same words | Note it on the open request; close the new one as a duplicate (*our design*) |

A tree request often carries several orders: removal, stump, sometimes planting. Whether the request closes on the first or the last is *not established*, so test one first. For removals, the date that counts is your projected finish on the work order, not the request's 14-day inspection date. The 1,630 baseline is counted that way.

## 3. Each week: work the past-due list

Take about **25 rows from the top of the ranked list**: roughly 75 minutes (*assumed*). Also clear the Close-out list, the records already showing the work done.

| You find | Do this |
|---|---|
| **Done**: actual finish, or a cut on record | Verify; close the work order (the request follows), or close with "grass cut" |
| **Waiting**: a job exists but isn't linked | Link or dispatch it; set Dispatch |
| **Missed**: no job, and the work is still needed | Re-dispatch, or put the lot back on the rounds; leave the request open |

On 13 October your ranked list held 4,350 requests. Oldest first, 9 of the top 25 were life-safety; ranked, all 25 were (*observed*).

## 4. What the resident's status page shows

- **Tree.** Today: "Closed", "removal work order created". After: open, "On Forestry's removal list since" the order date, due by your projected finish, "Not yet done", with the work order listed. It closes by itself when the order closes.
- **Lot.** Today: "Closed", and the page swaps the words for "please contact the Citizens' Service Bureau" (*observed*). After: "Open · no crew job linked · flagged to Forestry", on the past-due list from the day after its date, with repeat reports added. It closes when a cut is recorded.

The "after" wording is our spec for the city's page; see the prototype at `site/status.html`. Figures and sources: [figures.csv](figures.csv).
