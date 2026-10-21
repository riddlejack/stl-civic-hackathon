# Hand-over package: keep the 311 request open until the crew's job is done

For a division supervisor and the city's Cityworks and GIS administrator. It runs on what St. Louis already has, Cityworks 23.10 and the city's ArcGIS portal: no new software, and no city data leaves the city. At the hand-off, the crew's work order is attached and the request is set to Dispatch or Pending instead of closed. Cityworks then closes the request itself when the work order closes. Requests past their date with no finished job go on a weekly list, most dangerous first.

**Labels:** *documented* (Cityworks help; links in [saved-search.md](saved-search.md)), *observed* (counted in the city's data), *our design* (a proposal to adjust), *not established* (unknowable from outside the city). Every figure, with its date and source: [figures.csv](figures.csv).

## What is in the package

| File | For | What it is |
|---|---|---|
| [practice-forestry.md](practice-forestry.md), [practice-streets.md](practice-streets.md), [practice-building.md](practice-building.md) | Each division | One page each: the hand-off, the status, the weekly list, what residents see |
| [saved-search.md](saved-search.md) | Cityworks admin | The overdue saved search: scope, filters, fields, sort, eURL publishing |
| [dashboard.md](dashboard.md) | GIS admin | The dashboard: map by block, ranked list, baseline counts, CityStat's added column |
| [sql.md](sql.md) | Analyst | The two SQL files and how to run them on the 311 file |

## Set it up in this order

1. **Test the auto-close on one request** (admin). Attach a work order to a request set to Dispatch, close the order, and check that the request closes. Then repeat with two orders: whether it closes on the first or the last is *not established*.
2. **Associate work-order templates with the request templates in scope.** Without this, the Create button doesn't appear on the request (*documented*).
3. **Build the overdue saved search** per division, and publish it with eURL to the portal for staff only.
4. **Build the dashboard** on that layer.
5. **Give each division its practice page**, and start the weekly review.
6. **In week 13, re-run the counts** and compare them with the baselines.

## The one-quarter test

| Request type | Overdue on 13 Oct 2026 (*observed*) | "No record either way" then |
|---|---|---|
| Tree removals (Forestry) | **1,630** open removal work orders past Forestry's projected finish | Behind them: 578 of 1,481 tree-inspection requests open past their date (39%) |
| Cave-ins (Street Department) | **1,233** requests open past the promised date | 1,196 (97%) |
| Vacant-lot mowing (Forestry) | **289** requests open past the promised date | 218 (75%) |

"No record either way" means no city record we found shows the work done or a crew job pending. The tree-removal count is of work orders, which are records already, so the test applies to the requests behind them. Sources: `build/E8/baselines.json`, `research/open-queue-reality-check.md`.

**What working looks like:**
- The "no record either way" share falls to zero for these types: every overdue request has its job attached, or a weekly-review outcome (done, waiting or missed).
- Overdue counts are compared with the baselines. They may rise at first, because requests once closed at the hand-off now stay open (*inferred*).
- None of these requests is closed by hand with hand-off words such as "removal work order created", "referred to street maintenance for repair work to be scheduled" or "on schedule to be cut".

**What it cannot promise:** faster crews. It makes every miss visible and ranked.

**Not established from outside:** whether custom statuses or field validation change the auto-close; whether Forestry's rotation cuts and Building's board-up orders are Cityworks work orders; how each division sorts its work today.
