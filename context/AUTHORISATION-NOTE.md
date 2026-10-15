# Authorisation for reading City of St. Louis systems during the hackathon

**Jack to complete the bracketed fields in his own words. Until he does, every statement here is "reported by Jack" and the submission says so.**

## What was authorised

- **Date and time:** Wednesday 14 October 2026, [time] Central, at the hackathon office hours ([in person at T-REX / on the 2 p.m. Teams call]).
- **Who gave it:** [name and role; e.g. a member of the Mayor's Office / the organiser], speaking for [the City / the Mayor's Office / themselves].
- **What was said (as close to verbatim as Jack can recall):** "[…]"
- **Scope as Jack understood it:** reading publicly reachable City web pages and data services for this hackathon entry, including pages a robots.txt comment asks bots not to crawl, provided the use is to recommend improvements to City services and no personal data is collected.
- **What was not discussed or not covered:** [e.g. editing anything; systems behind a login; personal data; publishing raw data].
- **Written record:** [none / an email / a message; path or link if any].

## What was done under it (observed; maintained by the orchestrating thread)

| When (Central) | What | Rate and limits | Where the raw data sits | Public output |
|---|---|---|---|---|
| 14 Oct, 1:48–1:53 p.m. | Cityworks query service (`service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe`): 32 work-order searches, 4 service-request searches, operational fields only | Allowlisted client (`research/cityworks-gap-scripts/qe_client.py`); personal, contact, tax, staff, comment and free-text fields excluded | `data/raw/cityworks-gap/authorized/` (git-ignored) | Aggregates only, in `research/cityworks-*` |
| 14 Oct, about 2:55 p.m. | Ten public 311 status pages (`check-service-request.cfm`) read for the attached-items count | One per second | `data/raw/stlouis-mo.gov/csb-status/` (git-ignored) | Counts by closure type; no ids or addresses |
| 14 Oct, from about 3:25 p.m. (E1) | About 1,440 public 311 status pages, sampled by closure type, and the related-items endpoint (`a disallowed path …/dsp-related-items.cfc`) for requests with attached items | One per second; endpoint fields allowlisted (ids, types, statuses, dates); names, comments and free text dropped before saving | `data/raw/stlouis-mo.gov/csb-status/` and `csb-status-items/` (git-ignored) | Per-service attach rates and per-request fates at block level; no ids or addresses |

## Why this note exists

The City's `robots.txt` carries the comment "Do not crawl service request, board bills, etc." and the line `Disallow: check-service-request.cfm` (no leading slash, so it matches no URL under the standard), and it disallows a wildcard path. Reading these pages at scale goes against the webmaster's evident intent. Jack authorised it on the strength of what he was told at office hours, and the entry states that in its methods. The rule for every thread: one request per second, allowlisted fields, raw data in ignored folders, nothing public below block level, no personal data.

## What the submission says (draft wording; Jack edits)

"Beyond the open 311 file and the City's public map services, this entry read the City's Cityworks saved searches and public 311 status pages. City staff authorised this at the hackathon office hours on 14 October 2026 for the purpose of this entry. Reads were limited to one request per second and to operational fields; no personal data was collected; raw data is not published; every public figure is at block level or coarser."
