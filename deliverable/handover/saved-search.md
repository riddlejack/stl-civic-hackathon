# The overdue saved search: a Cityworks query specification

**For** the city's Cityworks administrator. One saved search per division (or one citywide, with a division field), listing every open request past its promised date with no finished job, sorted by the ranking. It is published with eURL to the city's ArcGIS portal and feeds the dashboard ([dashboard.md](dashboard.md)).

**Labels used below.** **[Documented]**: the Cityworks help says so (links in Sources). **[Observed]**: seen in the city's own Cityworks service or data. **[Our design]**: a proposal; adjust it. **[Not established]**: nobody outside the city can know it yet.

## 1. Scope: which request templates

- **Default:** every request template the division receives **[our design]**. Leave out the sensitive types the prototype never lists below ward level: homeless and welfare calls, discrimination complaints, legal claims, courts and police referrals (the `sensitive_codes` rule in `site/data/downloads/measures.sql`).
- **For the one-quarter test, start with three:**

| Test type | Division | What the search reads |
|---|---|---|
| Cave-ins | Street Department | Service requests, problem code `Cave-Ins` |
| Vacant-lot mowing | Forestry (some routed to the land bank) | Service requests, codes `Weeds-Vacant Lot`, `Missed Cut - V Lot`, `Unsatisfy Cut - VLot` |
| Tree removals | Forestry | **Work orders**: the existing "Tree Removal WOs" saved search, open and past `ProjectedFinishDate`, plus open `Inspect City Tree` requests |

Tree removals are counted on work orders because the request's 14-day date is the inspection's; the removal's own date is the work order's projected finish, which the template's Days to Complete sets **[documented]**.

## 2. Filters

| Filter | How | Label |
|---|---|---|
| Request not closed and not cancelled | Status not Closed or Cancelled. Keep Dispatch, Pending, New, Inspect, Scheduled and On Hold. In the 311 file these read "Disptch", "NEW", "Pending", "Inspect", "SCHEDULED", "ON HOLD" | statuses **[observed]**; filter **[our design]** |
| Promised date before today | `PrjCompleteDate` < today. The date comes from the request template's Duration; it is blank if no Duration is set | field **[documented]**; filled on 19,804 of 19,821 extracted values **[observed]**. Whether a saved search can hold a rolling "today" is **[not established]**; if it can't, filter by date in the dashboard |
| Filed on or after 1 Jan 2025 | `DateTimeInit` ≥ 2025-01-01, to match the 13 Oct baselines | **[our design]** |
| No linked work order with an actual finish | **Mostly enforced by Cityworks itself:** a request attached to a work order closes automatically when the work order closes, so once the practice holds, an open request has no closed work order | auto-close **[documented]** |
| …the leftovers | A work order with an Actual Finish that isn't yet closed, or a request with several work orders. Whether a request search can filter on a linked work order's fields is **[not established]**. Leave these in the list; the weekly review sorts them into "verify and close" | **[our design]** |

## 3. Output fields (block-level location only)

| Show | Field | Note |
|---|---|---|
| Request type | problem code and its description | |
| Division | the routing field (`SubmitTo` in the 311 file) | |
| Block | the hundred block and street, for example "4600 block of" a street | No native block field is known **[not established]**. Derive it in GIS from the address, then drop the address |
| Ward | ward | |
| Filed; promised; days past | `DateTimeInit`; `PrjCompleteDate`; today minus the promised date | |
| Status | as recorded | "Disptch" means sent to a crew, not done |
| Work order open | yes or no, where a link is visible | |
| Tier, score and why | see section 4 | |
| Request number | **staff layer only** | Staff need it to open the record. Leave it out of anything shared beyond staff |

**Leave out** the address, the caller's name and contact details, free-text comments and exact coordinates. Fields exposed through eURL appear in pop-ups to anyone who can see the layer **[documented]**. The layer also draws each record at its point **[inferred]**. So share it to staff only, and draw the map at block scale.

## 4. The sort: the ranking, in words

The full weights and tier map live in one editable file, `site/data/rank-weights.json`; the design is in `research/prioritisation-option.md` **[our design]**.

1. **Route first.** Records whose data already shows the work done, superseded by a later closed request, or administrative go to a separate **Close-out** list for the desk. They are not ranked.
2. **Score the rest, 0–100, from three things the city already records:**
   - **Hazard tier, by request type:** 60 points for life-safety, a blocked right of way or loss of an essential service (trees or limbs down, cave-ins, no water, dark signals, building collapse); 30 for a hazard that is not immediate (tree inspections, sidewalks, sewer laterals, exterior code); 0 for maintenance and nuisance.
   - **Lateness:** 1 point for every 12 days past the promised date, up to 30. A year late counts as much as one tier, so old nuisance work rises instead of waiting forever.
   - **Repeat reports:** 5 points for each extra open report of the same type at the same address, up to 10.
3. **Ties** go to the request furthest past its date.

Every row carries its "why" line, for example "tree limb down +60 · 538 days past +30 · 3 open reports here +10". No text, no demographics, no model. Four tier calls are flagged for divisions to review first: sirens not heard, lead inspections, sign needs attention and illegal use.

**In Cityworks.** No native ranking or escalation engine was found **[negative search]**. Inbox order comes from each saved search's sort field **[documented]**. Two ways to carry the rank:
- **Close, natively:** set each request template's default Priority to its tier (Priority is per template, a plain code list **[documented]**). Sort by Priority, then `PrjCompleteDate` oldest first. This drops the lateness cap and the repeat points, so a year-late tier-3 request never rises **[our design]**.
- **Exact:** compute the score outside Cityworks from the same fields, using the rule above (`scripts/exec/E7/rank.py` in the prototype). Sort the dashboard list on it **[our design]**.

## 5. Publish with eURL to the portal

1. Save the search (Office) or query (Respond). **Share** it through eURL, which gives a URL that shows the search as an "event layer" outside Cityworks **[documented]**. eURL is a licensed component. The city's query service calls itself an "AMS and PLL Event Service" and already feeds portal maps, so the licence appears to be held **[observed; inferred]**.
2. Choose the exposed fields (section 3) before sharing **[documented: exposed fields are visible in pop-ups]**.
3. Add the eURL to the city portal as an item. It acts like any other non-editable feature service and can feed Dashboards **[documented]**. The portal has ArcGIS Dashboards installed **[observed]**.
4. Share the item to a staff group, not to the public **[our design]**.
5. **Cloud move:** if the city moves to Cityworks Online, saved searches become Respond queries. Write the search as a Respond query and avoid database triggers or nightly jobs, which a migration removes **[reported, vendor]**.

## Sources

- Auto-close: [Close a Work Order, Cityworks 23](https://help.cityworks.com/AMS/OC/Content/AMS/OC/WorkOrder/CloseAWorkOrder.htm); [Close a Service Request, Cityworks 23](https://help.cityworks.com/AMS/OC/Content/AMS/OC/ServiceRequest/CloseAServiceRequest.htm)
- Create or attach a work order from a request: [Create an Attached Work Order](https://help.cityworks.com/AMS/15-8/Content/Online/AMS/15-8/WorkOrder/CreateAnAttachedWorkOrder.htm); [Associate a Work Order to a Service Request](https://help.cityworks.com/AMS/15-6/Content/ServiceRequest/AttachWO.htm); [Associate WO templates to an SR template (Admin)](https://help.cityworks.com/Admin/2-2/15-8/Content/2-2/ServiceRequests/AssociateWorkOrderTemplatestoaServiceRequestTemplate.htm)
- Promise date: [SR template fields (Duration → projected completion)](https://help.cityworks.com/Admin/3-4/Content/ServiceRequests/ServiceRequestTemplateFields.htm); [WO template fields (Days to Complete)](https://help.cityworks.com/Admin/3-8/Content/WorkOrders/WorkOrderTemplateFields.htm)
- Priority and inbox: [SR panel fields](https://help.cityworks.com/Respond/4-3/Content/Online/AMS/15-8/ServiceRequest/ServiceRequestPanelFields.htm); [Priority values](https://help.cityworks.com/Designer/OC/Content/Preferences/AddorEditPriorityValues.htm); [Saved search in the inbox](https://help.cityworks.com/Designer/OC/Content/ActionManager/AddaMessageQueueSavedSearchtotheInbox.htm)
- eURL and Dashboards: [Share a Query (eURL)](https://help.cityworks.com/Respond/3-4/15-8/Content/Online/eURLConfiguration/3-4/ShareAQuery.htm); [Trimble: Dashboards and eURL](https://www.trimble.com/en/blog/construction/article/how-to-visualize-data-with-arcgis-dashboards-and-cityworks-eurl) (vendor blog)
- Cloud move: [Trimble: migrating to Cityworks Online](https://www.trimble.com/en/blog/construction/article/5-tips-for-migrating-to-cityworks-online) (vendor blog)
- City status definitions (Dispatch, Pending, Closed): [archived 22 Jun 2025](https://web.archive.org/web/20250622131705/https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/status-definitions.cfm)
- St. Louis runs 23.10, and the saved searches: [the city's query service](https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer?f=json); research in `research/precedents-closed-loop.md` §A and `research/prioritisation-option.md` §1
