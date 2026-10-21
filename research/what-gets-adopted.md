# E. What a city actually adopts

**Status: complete for this pass — 2026-10-14 00:15 UTC (13 Oct, 7:15 p.m. CDT).** Sections 1–4 are synthesised from nine part files, all now closed. The research was bounded, not exhaustive; gaps are listed under "Negative results and limits" and "Open items".

Facts only. No project ideas or solutions for the hackathon entry appear in this file. Patterns (§1, §2) are groupings of sourced cases; this thread's own judgment is kept under separate headings (§1.9, §2.13, §3.6).

## Summary (half page)

**Found.** 150 cases in three tables (§4): 41 where analysis of city-held data did or did not change a routine, 48 tools built outside government, 61 St. Louis items. Nearly every result figure is self-reported by the city, vendor or builder.

**What goes with adoption (§1).** A named senior insider asked for it or used it before any contract. The output dropped into a routine the crew already ran: work orders, inspection order, dig order, land sales. The data were already held. An auditor, court or law forced the question. Someone else paid for the start. The survivors ended up on a city domain, in an ordinance or under a paid contract, usually with the original builder kept on.

**What goes with dying (§2).** Builder-hosted tools lapse without notice when the builder's time, money or business changes; seven such domains now serve gambling or spam. No owner, budget line or contract inside a department. The grant ends. The administration or contractor changes. The model fails in the field or reflects who complains. Bias objections and "every ward" politics. Government builds or buys its own version once the method is proven.

**St. Louis (§3).** One outsider line reached a city contract: a 2017 hackathon → a volunteer vacancy portal named in the Mayor's plan → the Vacancy Collaborative → a $500,000 city contract (2023–25) → the same developer's trackers on the City's tornado site. Other routes seen: ordinance plus cooperation agreement (Brightside), a commissioned evaluation (WashU), donated imagery used once by Forestry, and philanthropy-funded posts later archived. No case was found of the City hosting outsider-built code. Today's gate is a department sponsor, the IT agency and the IT Project Governance Committee, under a July 2026 policy that bars unapproved AI tools.

**Not established.** How the tornado trackers were commissioned or paid for; any rule for accepting a free tool; the City's own account of the GeoSTL mowing work; the reason for most shutdowns; 2025–26 status of most adopted analytics cases. Outsider-built graffiti and dumping tools were not researched.

## Part files

| File | Content | State on 14 Oct 2026 UTC |
|---|---|---|
| `research/parts/E-stl-city-it.md` | Who owns IT and data; purchasing rules; AI, surveillance, accessibility, privacy, open-data policies; systems and vendors; recent pilots and partnerships | complete for this pass |
| `research/parts/E-precedents-analytics.md` | 33 raw-verified and 9 half-checked cases of analysis of city data (notes N1–N34); meta-studies M1–M7 | complete (bounded), 00:15 UTC |
| `research/parts/E-precedents-outsider-tools.md` | Liveness sweep of 70 URL checks; 25 tool cases and 2 context rows (notes C1–C23); published syntheses | complete (bounded), 00:13 UTC |
| `research/parts/E-outsider.d/themes.md` | 14 tools near trees, road condition, vacant lots (Cases 1–14) | paused, partial; merged here |
| `research/parts/E-outsider.d/startups-univ-intl.md` | 11 startup, university and non-US cases (§§1–11) | paused, partial; merged here |
| `research/parts/E-stl-civic-tech.md` | St. Louis civic-tech inventory, chronology, city expenditure check | complete (bounded), 00:10 UTC |
| `research/parts/E-stl-civic-tech.d/tornado-and-streets.md` | Outsider tornado tools; street, graffiti, dumping, reporting tools | paused, partial; merged here |
| `research/parts/E-stl-civic-tech.d/justice-and-universities.md` | Justice, housing-court and university work | paused, partial; merged here |
| `research/parts/E-stl-civic-tech.d/philanthropy-programmes.md` | Philanthropy and national programmes with the City | paused, partial; merged here |

Every URL, retrieval time and raw-file path sits in the part file named in the "Source (notes)" column of §4. Raw downloads are under `data/raw/adoption/`.

## Labels

- **O (observed)** — a thread loaded the page, file or API itself on 13–14 Oct 2026 UTC and read the raw text.
- **R (reported)** — a named source says so; not verified here. "Stated" means the source itself gave this as the reason.
- **H (half-checked)** — seen only in a search-result summary; not raw-verified. Do not rely on figures.
- **I (inferred)** — this thread's own conclusion.

Outcome words used in §4: *adopted, running*; *adopted, then retired*; *adopted, then replaced* (by a vendor or by the government's own system); *never adopted*; *pilot*; *unknown*.

## 1. Patterns that go with adoption

Each pattern is a grouping made by this thread. Each case line is a sourced fact; IDs point to §4.

### 1.1 A named senior insider asked for it, or was using it before any contract

- New Haven SeeClickFix (T34): the Chief Administrative Officer was signed up for alerts at launch and said the integration "sort of happened to us". *R, stated.*
- Boston Citizens Connect (T35): the two co-chairs of the Mayor's Office of New Urban Mechanics sponsored it. *R.*
- Los Angeles CleanStat (A10): Mayor's Executive Directive No. 8, led by a deputy mayor. *R.*
- Mobile blight index (A24) and Syracuse water mains (A4): the mayor's Bloomberg-funded innovation team was the internal partner; in Mobile the mayor asked for it. *R.*
- Boston CityScore (A7): the Mayor funded 20 EMTs and 10 ambulances after reading the score. *R, city's account.*
- Flint lead lines 2016–17 (A1): a small city team under a named lead "generally followed the model's predictions". *R.*
- Foodborne Chicago (T17): a named health-department employee worked on it and department staff operated it. *R.*
- Tempe graffiti (A28): the graffiti crew asked the city's GIS staff. *R.*
- DiscoverBPS (T8): the School Department pushed it forward. *R, city's account.*
- Memphis (A26): the city CIO approached the vendor. *R.*
- mRelief, Chicago (T47): the mayor's innovation team described the problem at a civic hack night and the mayor issued an open call. *R.*
- BlightStatus, New Orleans (T6): a blight system was the City's one stated goal for its Code for America fellowship. *R.*
- St. Louis vacancy portal (S1): the organisers say the 2017 hackathon was endorsed by Mayor Krewson and the Land Reutilization Authority (*R*); the Mayor's 2018 vacancy plan, on the City site, named the volunteers and said ITSA would establish the portal with them (*O*).
- St. Louis Cure Violence evaluation (S35): the Department of Health contracted and paid for it. *O.*

### 1.2 The output drops into a routine or system the front-line unit already runs

- Work-order systems: New Haven fed reports into Cityworks (T34); Boston photos land in the responsible crew's queue (T35); in Memphis a detection becomes a work ticket after a crew member confirms it (A26). *R.*
- Order of existing work: Flint dig order (A1); Chicago inspection order (A2); NYC illegal-conversion complaints re-ranked before inspection "without any additional inspector manpower" (A5, stated by the office's director); Chicago tree-trimming order (A17); Pittsburgh and Atlanta fire-inspection priority (A14, A15); New Orleans smoke-alarm canvass route (A6). *R.*
- Existing transactions and asset systems: Chicago Large Lots became the application for the city's $1 lot sales (T33); the NYC tree census became the Parks forestry system that foresters use daily (T25); Foodborne Chicago complaints entered the existing complaint-inspection queue (T17). *R.*
- St. Louis: Forestry overlaid donated Surdex imagery on its own tree-inventory points to find lost street trees (S20); the City counted 7,000+ SAVE Coalition structural inspections in its response (S22). *R / O.*

### 1.3 The data were already held by the city

- Stated as a deliberate rule in NYC: rely "upon what is already being collected" and do not ask agencies to change collection (A5). *R, stated.*
- Chicago trees used 311 requests and work records (A17); Chicago food inspections used inspections, 311, licences and weather (A2); Flint and Syracuse used parcel, pipe and break records with gaps filled by hand (A1, A4); Kansas City used existing cameras and data (A27); Adopt-a-Hydrant started from a hydrant list a city employee mentioned (T1). *R.*
- Counter-cases, kept: several adopted cases needed a new data collection first — Los Angeles street survey (A10), Mobile photo survey (A24), Philadelphia Litter Index (A16), Detroit parcel survey (A34), Memphis and Tempe vehicle imagery (A26, A28), NYC tree census (T25). *R.*

### 1.4 A complaint-driven system was shown to miss places that do not call

- Los Angeles: the complaint system "missed the areas where no one called" (A10). *R, stated.*
- Chicago trees: 75% of crew time went on 311 requests while about 206,000 parkway trees went untrimmed for 10+ years; completed requests ranged from 10,431 in one ward to 1,808 in another (A17). *O, Inspector General.*
- Mobile: code officers had waited for 311 complaints (A24). *R.*
- Memphis: residents reported about 20% of the potholes the city filled (2020 report) and 10–15% "historically" (2024 report) (A26). *R, city and vendor.*
- San José: the pilot flagged nearly 70% of issues before residents reported them (T28). *R, city.*
- St. Louis, stated aim only: CityStat's manager said the aim of per-lot mowing logs is to catch missed lots before residents call (S60). *R.*

### 1.5 Outside pressure or a triggering event

- Flint: the model was reinstated in 2019 after NRDC litigation and state pressure (A1). *R.*
- Chicago trees: an Inspector General advisory in 2019 preceded the 2023 change; a 2009 consultant report had sat unimplemented until then (A17). *O.*
- Chicago weed cutting: the Inspector General analysed the department's own work orders in 2020; the department agreed to give contractors weekly lists of city-owned lots and cut its complaint target from 42 to 21 days (A37). Whether the change held was not checked. *O.*
- NYC illegal conversions: fatal fires in 2011 (A5). *R.*
- A law or policy change set a deadline: California's AB 1793 required every district attorney to clear eligible convictions automatically, and about half the counties then used Clear My Record (T12); Boston paid for a DiscoverBPS rework when its assignment policy changed in 2013 (T8). *R, stated.*
- St. Louis: the Close the Workhouse campaign preceded a 2020 aldermanic bill and the 2021 emptying and defunding of the jail (S34); advocates and residents are credited by the Board in the 2024 surveillance ordinance (S37). *O / R.*

### 1.6 Someone else paid for the start

- Foundations and grants: Surtrac (Hillman, Heinz, R.K. Mellon; T40); Commonwealth Connect ($400,000 state grant, three years of running costs; T36); Cary wastewater pilot (Bloomberg Mayors Challenge; T41); San José ($260,000 Toyota Mobility Foundation; T28); Chicago Large Lots (LISC Chicago, Boeing, Knight; T33); Foodborne Chicago (Knight Prototype Fund; T17); Detroit parcel survey ($1.5M JPMorgan Chase Foundation; A34); Syracuse and Mobile innovation teams (Bloomberg; A4, A24). *R.*
- Very low price: Citizens Connect v1 about $25,000 with a developer working free (T35); Syracuse SQUID trial $2,000–$3,000 (T27); Adopt-a-Hydrant hosting $9 a month (T1); Nextdoor free to agencies (T39). *R.*
- St. Louis: 100 Resilient Cities paid for the Chief Resilience Officer for two years (S44); Bloomberg programmes paid for technical assistance and an innovation team (S48, S49); the Center for Community Progress gave technical assistance (S51); IKE kiosks were advertising-funded (S54, H); Surdex flew imagery pro bono (S20); a federal grant paid for SLMPD's research partner (S36). *O / R.*

### 1.7 It ended up on a city domain, in an ordinance, or under a paid contract

- City-hosted and alive on 13 Oct 2026: SF Adopt-a-Drain on `sfwater.org` (T3); LA Metro board agendas on `metro.net` (T21); NYC Tree Map on `nycgovparks.org` (T25); Great Starts on `boston.gov` (T8); ChiBlockBuilder, the City's portal (T33). *O.*
- Ordinance: Chicago adopted LargeLots.org by ordinance on 10 Dec 2014 (T33). *R.*
- Formal adoption by the body itself: the New York City Council "officially adopted Councilmatic" in 2017 with a Council-run version (T21; 2026 status not established). *R.*
- Paid contract or subscription: GetCalFresh (seven-county state contract in 2014, then $3.6M for all 58 counties in 2017; T13); SeeClickFix (about $5,000–$10,000 a year per government in 2011; T34); Remix and FixMyStreet Pro subscriptions (T38, T44); Allegheny screening tool by competitive contract (A22); Pittsburgh fire model "deployed on the City's servers" (A14). *R.*
- St. Louis: the Vacancy Collaborative's two-year, $500,000 CDA contract (S2; the ledger shows $499,949.59 paid FY2024–26 to Community Builders Network); Brightside by Ordinance 68331 with a cooperation agreement (S29); Right to Counsel by Ordinance 71694 and a contract with Legal Services of Eastern Missouri (S40); solar-ready and building-energy ordinances after the Bloomberg climate programme (S48). *O.*

### 1.8 The original builder stayed on

- DataMade built LargeLots.org and was then engaged under contract to build its successor (T33); a 2024 Chicago ordinance authorises master service agreements with the firm for public-facing applications (T21). *R.*
- The former Code for America fellow reworked DiscoverBPS as a paid partner (T8); Connected Bits appears still to host Boston's 311 endpoint (T35, I); the Flint researchers became BlueConduit (A1); Code for America keeps a paid outreach role after GetCalFresh applications moved to the State (T13). *R.*
- St. Louis: one developer (Dave Menninger, Public Goodness) built the Vacant Property Explorer, the tornado trackers on the City's recovery site, the Neighborhood Foresters' tree app and the Neighborhood Map (S2, S3, S13, S4). *O.* One of the 2018 portal's volunteer builders is now listed with the St. Louis Development Corporation and is vice-president of the Collaborative's board (S1). *O.*

### 1.9 This thread's judgment on §1 (kept separate)

- **I:** The adopted analytics cases mostly re-order work a crew already does. Few changed what the crew does.
- **I:** Three Chicago cases turn on an auditor analysing a department's own 311 and work-order data (trees, weeds, rodents). Two led to a changed routine.
- **I:** "Adopted" meant three different things: government launched it jointly; government paid for it later; government copied the function into its own system. Only the first two kept the outsider's tool alive.
- **I:** In the two best-documented outsider successes (New Haven, Boston) the decisive technical step was the link into the work-order system, not the resident-facing app.
- **I:** Durability evidence is thin. For most adopted analytics cases the last dated source is 2017–2020.
- **I:** Selection bias is likely: successes are written up by their owners; failures mostly leave no document.

## 2. Patterns that go with a project dying

### 2.1 Hosted by the outside builder; lapses without notice

- Liveness sweep, 13–14 Oct 2026 UTC, 70 URL checks: 18 failed at the network level and 12 more resolve to squatters, parking pages or expired hosting. Seven domains now serve gambling, towing, gaming or finance-blog content (`adoptahydrant.org`, `opentreemap.org`, `nycbigapps.com`, `cutgroup.org`, `wasmycartowed.com`, `citygram.org`, `citizinvestor.com`). *O.*
- OpenTreeMap went offline by Aug 2024 and took the Los Angeles, Edmonton and San Diego tree maps with it; San Francisco's instance is also gone (T23, T24). No reason was published. *O.*
- RoadBotics was bought by Michelin in 2022; Michelin's page says the product is discontinued by end of 2025 (T26). *O.*
- Adopt-a-Hydrant Boston, Adopt-a-Siren and Honolulu Answers, BlightStatus, Textizen, Motor City Mapping: original sites dead, no stated reason found (T1, T2, T7, T6, T10, A34). *O.*
- ClearStreets: the builders cite upkeep every snowfall and the end of a free mapping tier (T18). *R, stated.* SEPTAlking: its builder no longer had time (T46). *R, stated.*
- St. Louis: GlobalHack's domain is an essay-review site and its tax filings stop at 2017 (S8); YourSTLCourts times out (S9); OpenSTL's site loops, its Meetup is gone and a directory lists it "Inactive" (S5); the Regional Data Exchange portal times out (S11); the Clear My Record app returns "No such app" (S10); 36 of 40 SLU openGIS repositories are archived (S41). No closing statement was found for any of them. *O.*

### 2.2 No owner, budget line or contract inside a department

- First-generation app contests sat outside core departments, with no departmental money and nobody accountable (Apps for Democracy, NYC BigApps; T4, T16). *R, stated by Lee, Almirall and Wareham, 2016.*
- Surtrac: the city did "not contract or otherwise manage the pilot"; there was no data-sharing agreement; city engineers could not operate it; going from pilot to permanent use without procurement left next steps unclear (T40). *R, stated by city officials in an MIT thesis.*
- Chicago Strategic Subject List: "CPD did not develop a plan to sustain" the models (A3). *O, Inspector General.*
- Chicago's 2013 rat-prediction project "was abandoned"; the department told auditors in 2026 it no longer had the records (A18). No reason recorded. *O, Inspector General.*
- Philadelphia litter cabinet: measured litter but had no resources to act (A16). *R.*
- Hackathon projects in general: about 5% continue beyond five months; 7% show any activity at six months (two studies of general, not civic, hackathons). No civic-specific rate was found. *R.*
- St. Louis: no city adoption is reported for the 2013 "Continuum" shelter phone system or for any project from the 2014 and 2015 OpenDataSTL hackathons (S6); the GlobalHack VI winning team "had to return to reality and full time jobs" (S8, R, stated); students' traffic-calming analysis and the UMSL tax analysis drew no reported decision (S33, S58); the 2020 DHS smart-city pilot left no adoption found (S12). *O / R.*

### 2.3 The grant, pilot term or funder ended

- Chicago SSL: grant funding was "set to end in September 2019"; decommissioned 1 Nov 2019 (A3). *O / H.*
- Code for America ended its Brigade Network in 2023, citing difficulty raising multi-year money (T5). *R, stated.*
- Chicago's resident-testing programme (CUTGroup) ended when its host, City Tech, closed at the end of 2021; no reason found (T48). *R.*
- Philadelphia litter cabinet cut in a $649M budget gap (A16); Hackney dropped its tool as not worth further spending (A19). *R, stated.*
- Commonwealth Connect: one town reportedly did not renew when three grant-funded years ended (T36). *H, unverified.*
- St. Louis: the 100 Resilient Cities–funded Office of Resilience pages are archived, the newest item dated five weeks after the funder closed (S44); Equity Indicators has a 2018 baseline only (S45); the Vacancy Collaborative says it "returned to its roots as a volunteer-driven initiative" in 2026, the year city payments ended (S2); the Regional Data Alliance site is stale since 2022 (S11). *O; the causal links are I.*

### 2.4 The administration, contractor or champion changed

- Flint 2018: a new contractor had only a PDF map, not the scores; hit rate fell from 70% to 15% (A1). *R, stated.*
- Baltimore CitiStat: no reports published and a third of meetings cancelled in 2014 under a later mayor; analysts cut from nine to four (A9). *R.*
- Maryland StateStat discontinued after a change of governor (A40). *R.*
- New Orleans BlightStat was "no longer in operation" by May 2021; no reason found (A25). *O.*
- vTaiwan: an incoming administration withdrew the bill built on its recommendations (T43). *R.*
- Surtrac: the thesis attributes the unmanaged pilot to a programme "spearheaded by a former mayor" (T40). *R.*

### 2.5 The model or data did not hold up in the field

- DC rat burrows: predicted well against 311 data, failed a 100-site field test; Rodent Control declined to use it (A11). *O.*
- London shared houses: 4 of 12 boroughs had usable data (A13). Hackney: data "more limited than had initially been envisaged" (A19). *O / R, stated.*
- Chicago SSL: "Risk scores and tiers were unreliable" (A3). LAPD: effectiveness could not be measured (A20). *O / R.*
- Independent checks made adopted cases look weaker: IIT on Chicago food inspections (A2); The Lens found 52 of 300 "fixed" New Orleans properties still blighted (A25). *O.*
- Street Bump: sunk castings outnumbered potholes; a published critique noted uneven smartphone ownership (A8). *R.*
- Pittsburgh snow plow tracker: council members called it inaccurate (T30). *R.*
- St. Louis: prior ShotSpotter evaluations found few impacts, and coverage was expanded anyway (S36). *O / H.*

### 2.6 Bias objections, public trust and "every ward" politics

- Pittsburgh hot-spot policing ended despite favourable self-reported results; the Mayor cited bias (A21). *R, stated.*
- Flint 2018: the mayor asked the contractor to work in every council ward (A1). *R, stated.*
- Chicago trees: area-based trimming gives alderpeople less control; the change took from 2009 to 2023 (A17). *R / O headline only.*
- Boston start times withdrawn after opposition from parents and councillors (A23). *R.*
- LAPD programmes eroded public trust (A20); Nextdoor removed "Forward to Police" (T39). *R, stated.*
- Rotterdam and Amsterdam welfare models (A30, A31). *H.*
- San José reportedly dropped graffiti and encampment detection for capacity and privacy reasons (T28). *H.*
- St. Louis: the ShotSpotter contract was on hold until late 2024 while the City regulated surveillance technology (S36, S37). *O.*

### 2.7 Government built or bought its own once the method was proven

- ClearStreets retired when Chicago improved its own plow tracker (T18). *R, stated.*
- GetCalFresh applications moved to the State's BenefitsCal in 2025; a state official's stated reason is that it served one programme and the State's site serves many (T13). *O / R, stated.*
- Massachusetts ends its Biobot contract on 31 Jul 2026 to test in-house at a reported quarter of the cost; CDC moved to another vendor in 2023 (T41). *R, stated.*
- Taiwan built Join, run by civil servants (T43). *R.*
- 596 Acres removed its map, saying the City now publishes the data and staffs the function (T31). *O, builder's account.*
- San Francisco now runs its own street-tree map (T24); NYC replaced volunteer street-tree counts with vehicle LiDAR in 2025 (T25); Alaska's courts run their own text reminders (T11). *O.*
- St. Louis: the City issued tree-inventory RFPs in 2025 and 2026, one specifying a "LiDAR digital twin … or in-person inventory" (S16); the City's GIS vendor said after the tornado, "We're not trying to code new applications on the fly" (S21, R); the IT committee's stated goals include "reducing redundant systems and encouraging enterprise solutions" (§3.3). *O.*

### 2.8 Absorbed by a vendor

- Civic Insight into Accela (T6); Textizen into GovDelivery (T10); NextRequest and SeeClickFix into CivicPlus (T9, T34); Remix into Via (T38); Surtrac's spin-off into Miovision (T40); RoadBotics into Michelin, then discontinued (T26); OpenTreeMap's firm into Element 84, then offline (T23; acquisition H). *O / R.*
- Outcomes differ: SeeClickFix and Remix still run as vendor products; RoadBotics and OpenTreeMap ended.

### 2.9 Few people needed it, or developers chose the problem

- Apps for Democracy apps were more "cool" than useful (T4); BigApps entries followed developers' own interests (T16). *R, stated.*
- Adopt-a-Hydrant: "About 100 volunteers" for 13,000 hydrants, per the City (T1). *R.*
- CourtBot: uptake reported as slow (T11). *H.*
- Knight Foundation: tools without a clear government buyer face built-in funding obstacles. Sifry: some civic needs are not felt often enough to sustain a product. *R, stated.*
- St. Louis SeeClickFix: 518 resident reports from 2009 to 2026, none acknowledged, no agency request types configured (S27). *O.*

### 2.10 Analysis with no decision attached

- NYC tree pruning: a 22% drop in emergency clean-ups was found; no schedule or budget change was found (A12). *O.*
- vTaiwan: government is not required to act on results (T43). *R, stated by its co-creator.*
- New Orleans smoke alarms: a targeting estimate, no outcome measure found (A6). *O.*
- Vacant-lot greening and mowing studies: Philadelphia research found fewer gun assaults near greened lots, and a New Orleans study found no change in violent or property crime; no funding or practice change was tied to either (A39, A38). *O.*
- St. Louis: Equity Indicators baseline, never updated (S45); the Brown School preparedness study, no city response found (S25); the UMSL tax analysis, praise and a hiring pitch (S58). *O / R.*

### 2.11 The data source or the rules changed underneath the tool

- DiscoverBPS needed a paid rebuild after a 2013 policy change (T8). *R.*
- Chicago Councilmatic's scrapers reportedly broke when the City Clerk replaced its legislative system in 2023 (T21). *H.*
- ClearStreets depended on scraping the City's plow tracker and on a free mapping tier that ended (T18). *R, stated.*

### 2.12 What published reviews of the field say (the sources' own factors)

- **Lee, Almirall and Wareham, Communications of the ACM, 2016:** early app contests gave "meager results" because they ran outside core departments with no accountable owner or budget. Named improvements: coders working beside civil servants, internal offices with management attention, reusable hosted products. *R.* <https://web.archive.org/web/20231202020321/https://cacm.acm.org/magazines/2016/1/195725-open-data-and-civic-apps/fulltext>
- **Knight and Rita Allen Foundations, "Scaling Civic Tech", 2017:** the organisations that grew sell to government clients; tools with no clear buyer, or that do not address a government pain point, face built-in funding obstacles. *R.* <https://www.govtech.com/civic/report-civic-tech-struggles-with-sustainable-business-models-despite-making-gains.html>
- **Sifry and Stempeck, Civic Tech Graveyard, 2019:** early fundraising does not predict use; some civic needs are not felt often enough to sustain a product; owners close tools when another service does the job. Cites a study finding most failures trace to not involving users and to weak working relationships with the officials who hold the data. The directory held 1,053 entries on 14 Oct 2026 and has no cause-of-death field. *R / O.* <https://civictech.guide/learning-from-the-civic-tech-graveyard/>
- **McCann, "build with, not for", 2015:** start with people; cater to context; respond to need; build for best fit; prove it. *R.* <https://www.smartchicagocollaborative.org/wp-content/uploads/2015/10/experimental-modes.pdf>
- **Brookings study of 280 cities and counties, via Route Fifty, 2017:** most agencies had not managed to apply data to decisions; people and process mattered more than tools; pressure from elected officials raised data use; staff saw "little effect on their work" and no reward. *R, secondary.* <https://www.route-fifty.com/digital-government/2017/12/why-agencies-struggle-with-performance-analytics/303454/>
- **Casey, Wilson and Yokum, "A Cautionary Tail":** a model that tests well on 311 data can fail in the field; test in the field before use. *O.* <https://arxiv.org/pdf/1807.03860>
- **Behn, "The Five Big Errors of PerformanceStat":** no clear purpose; no one authorised to run the meetings; no dedicated analysts; no follow-up; no balance between brutal and bland. *O.* <https://www.governing.com/archive/The-Five-Big-Errors.html>
- **Preis, MIT thesis on university–city partnerships, 2019:** Pittsburgh officials credited a fire-risk model's success to a specific operational problem and a dedicated university team; they cited missing contracts, no single responsible employee and over-promising as the problems elsewhere. A former Chicago chief data officer is quoted that researchers always have their own research goals, distinct from the city's. *R.* <https://dspace.mit.edu/handle/1721.1/123931>
- **California state official on taking a tool in-house, 2025:** the fast test-and-fix loop the nonprofit ran will be among the hardest things to replace. *R.* <https://codeforamerica.org/news/shoulder-to-shoulder-building-capacity-for-state-owned-benefits-delivery-systems/>

### 2.13 This thread's judgment on §2 (kept separate)

- **I:** The commonest ending is silence, not rejection. Stated reasons exist mainly where builders wrote a closing notice or a journalist asked.
- **I:** A pilot placed on city infrastructure without a contract became harder to adopt later (Surtrac), not easier.
- **I:** Favourable numbers did not protect a tool (Pittsburgh hot spots, Flint 2018). Unfavourable numbers did not stop one with a department behind it (ShotSpotter in St. Louis).
- **I:** In St. Louis the philanthropy-funded items that left something in force ended in legislation or a contract. Those that ended in a plan, an index or a funded post are archived.
- **I:** Vehicle-camera detection took years to reach routine use: Memphis began in 2019, was still called a pilot in Dec 2024 and was reported in use in Jan 2026; San José began in late 2023 and was not operational in Feb 2026.
- **I:** Models built by outside partners on a grant or pilot left little behind when the partner left: Chicago's rat model has no surviving records, the Strategic Subject List had no sustainment plan, and Flint's scores did not survive a contractor change.

## 3. St. Louis's own path

Rows in 3.1–3.3 are sourced in `research/parts/E-stl-city-it.md`; section numbers refer to that file. Rows in 3.4 point to §4C.

### 3.1 Who would have to say yes

| Step | Who | What they control | Label |
|---|---|---|---|
| A department that wants it | Department director — for the hackathon's themes: Parks, Recreation and Forestry (Greg Hayes); Street Department (James Jackson); Public Safety (Shawn Dace), which contains the Citizens' Service Bureau | A project request must come from a department and name a **project sponsor**; outsiders cannot submit (§1) | O |
| Mayor's Office operations | Chief Operating Officer Ben Jonsson (oversees all departments; sits on the IT committee); Deputy COO Bryan Barroqueiro | Departmental priorities; a committee seat | O |
| Mayor's Office data | CityStat Program Manager Alex Price; Research Analyst Jasper Wilson | Metrics, dashboards and the "internal operational meetings" where service data is reviewed | O (roles); R (meetings) |
| Central IT | CIO Cindy Riordan (ITSA); CTO Simon Huang (Mayor's Office) | Approval of any software or SaaS on city computers; approval of any AI tool; integration with city systems; committee seats | O |
| IT Project Governance Committee | COO, CIO, CTO, Budget Director, Board of Public Service President, Supply Commissioner | Whether a "strategic project" proceeds and where it sits in ITSA's queue. It does not appropriate money or replace procurement. | O |
| Purchasing | Supply Commissioner Chris Carter; Comptroller (approves awards above $5,000) | Any purchase; sealed bids above $2,500; advertising above $5,000 | O |
| Professional services | Five-member selection committee (department, Mayor's, Comptroller's and Board of Aldermen President's appointees) | Any professional-service contract above $5,000 | O (1997 ordinance; amendment status not checked) |
| Outside money | Board of Estimate and Apportionment, then Board of Aldermen by ordinance | Accepting a grant and spending it | O (example ordinance) |
| Surveillance technology | Board of Aldermen, after a public hearing | Any city use of "surveillance technology" | O (summary); definition not read |

### 3.2 What the city's own documents make easy (facts)

- A request that "uses only existing software licenses and hardware" and can be done by existing staff is routed to an ITSA team as an enhancement, not to the committee (§1). *O*
- A purchase of up to $2,500 per transaction needs no bids or advertising, though the Supply Division still approves it (§2). *O*
- The city already publishes 72 open datasets and three APIs, and runs its website, 311 request form and open-data portal in-house (§§3–4). *O*
- The Mayor's Office has stood up its own site outside the main platform: the tornado recovery hub runs on WordPress on a separate `stl.gov` host (§4). *O*
- CityStat staff describe an existing routine in which dashboards go to internal operations meetings and data gaps are worked through with the department — for example, Forestry's vacant-lot mowing (§1). *R*
- The city has let an outside nonprofit work on an operational question (GeoSTL, vacant-lot mowing priority), and the COO has attended and praised a university analysis built on assessor data (§5). *R*
- The project request form asks which Mayor's priority a project serves; the five listed are Tornado Recovery, High-Quality City Services, Public Safety & Justice, Economic Transformation & Inclusive Growth, and Transparency & Good Governance (§1). *O*

### 3.3 What the city's own documents make hard (facts)

- "Use of any AI tool that has not been approved by ITSA" is prohibited for staff; approval needs a business case, costs, a procurement method, a data-retention plan and staff AI training. Tools whose terms let the vendor train on city data are prohibited outright. AI output may not be published without human verification (§3). *O*
- Requiring procurement is by itself a trigger for committee review, whatever the price (§1). *O*
- The committee's stated goals include "reducing redundant systems and encouraging enterprise solutions" (§1). *O*
- The rough-order-of-magnitude template requires hours from department subject-matter experts, change-management leads and trainers, and "annual or recurring costs" with a funding source (§1). *O*
- Forestry reported running at about 60% of seasonal mowing staff in August 2026; ITSA's page gives 44 employees (undated) (§1). *R / O*
- Public-facing web content must meet WCAG 2.1 AA; the federal compliance date for a city this size is reported as 26 April 2027 (§3). *O / R*
- Records and data entered into a city tool fall under the Missouri Sunshine Law (§3). *O*
- ARPA, which paid for the OneStopGov portal, reached its performance deadline; the city is processing final invoices (§5). *O*
- CityStat's public pages had no data later than 30 June 2026 on 13 October 2026 (sibling inventory). *O by sibling thread*

### 3.4 How outside work has reached the City before (facts)

| Route | St. Louis cases (§4C) | What the record shows | Label |
|---|---|---|---|
| Standing collaborative with city agencies as members, then a contract | S1, S2 | Sept 2017 OpenSTL hackathon, endorsed by Mayor Krewson and the LRA per the organisers (R) → named in the Mayor's 2018 vacancy plan → volunteer portal, July 2018 (12 datasets from 4 departments) → rebuilt by one developer as the Vacant Property Explorer (date not established) → CDA awarded a two-year, $500,000 contract in May 2023 from the 2017 Economic Development Sales Tax → a 30 Sep 2026 City notice for a $300,000 vacant-building fund cites the initiative and links the tool. Eleven city bodies, including ITSA and Forestry, are listed as participants. The tool stays on the builder's host. The ordinance, board item and contract document were not found. | O; R where marked |
| Outsider-hosted tracker embedded in an official city site | S3 | Parcel trackers on `tornadorecovery.stl.gov` are built and hosted by Public Goodness. No credit line, contract, press release or named official was found. No supplier named "Public Goodness" or "Menninger" appears in city expenditure lists for FY2023–FY2026. | O (pages, ledger); arrangement not established |
| Ordinance plus cooperation agreement | S29 | Ordinance 68331 (2009) created an Operation Brightside Agency inside Parks, Recreation and Forestry alongside the nonprofit. Graffiti reports go through the Citizens' Service Bureau. | O |
| Ordinance plus competitive contract with a nonprofit | S40 | Right to Counsel: Ordinance 71694; Legal Services of Eastern Missouri selected by RFP; ARPA-funded; contract ends 9/2026. | O |
| City commissions and pays for an evaluation | S35 | Department of Health contracted WashU to evaluate Cure Violence; the City hosts the report; providers were changed from 1 Sept 2023. | O / R |
| Federal grant with a named research partner | S36 | SLMPD and an SIUE professor on ShotSpotter, DOJ Smart Policing Initiative grant, 2021. | O |
| Donated data or labour used once by a department | S20, S22 | Surdex imagery overlaid on Forestry's tree inventory by a volunteering design firm and a WashU student; SAVE Coalition inspections. | R / O |
| Named partner in a federally funded city programme | S61 | Forest ReLeaf of Missouri is the planting partner in the City's Tree Canopy Expansion Program; the City page sends readers to the nonprofit's own site for results. | O |
| Philanthropy-funded post, team or technical assistance | S44, S48, S49, S51 | Resilience office (archived after the funder closed); climate programme (ordinances in force); innovation team of up to three staff (2024, three years); vacancy technical assistance (cited by the City in a 2023 RFP). | O |
| Free vendor channel, no procurement | S28 | Nextdoor partnership announced 16 Oct 2013; City agency page shows 5,583 updates. | O |
| Outside analysis presented to officials | S57, S58 | GeoSTL "working with the city for a few weeks" on mowing priority (Aug 2026); UMSL students presented to the COO and Assessor (May 2026). No decision or contract reported for either. | R |
| City links to an outside tool | S15 | Tree Equity Score and ParkServe linked from the sustainability page. | O |
| Grants, links and thanks to organisations, not their tools | S17, S18, S23, S24 | City listed Action St. Louis at $138,098; no evidence the hubs' intake data reached city systems. | O |
| No uptake found | S5–S12, S14, S27, S33, S38, S41 | See §2.1, §2.2, §2.9. | O |

Across every item checked, no case was found of the City hosting or maintaining outsider-built code. City money in the vacancy line went through a nonprofit; no direct City purchase of the software was found. *O (negative).*

Further facts on the vacancy line (all *O*, `E-stl-civic-tech.md` notes 2P-1 and 2P-2):
- City payments under the contract went to Community Builders Network of Metro St. Louis: $176,736.90 (FY2024), $256,512.52 (FY2025), $66,700.17 (FY2026); total $499,949.59. A supplier named "St. Louis Vacancy Collaborative" appears once, for $250.00 in FY2023.
- The Collaborative's site says that in 2026 it "returned to its roots as a volunteer-driven initiative", with "contract support" for its data tools.
- The Explorer's data file was last modified 30 Sep 2026; a City news item of the same date links the tool.
- The Neighborhood Foresters' tree app reads from the Vacancy Collaborative's database project, not from a City system (page source). No evidence was found that volunteer-entered tree records flow back to Forestry.
- The City's own tree-planting dataset says planting order follows ward funding and request age (`B-existing-tools.md` §2).

### 3.5 What was not found in St. Louis

- Any volunteer-built database, form or map absorbed into city systems after the May 2025 tornado. *Not found.*
- Any City account on SeeClickFix; any graffiti-tracking database at SLMPD or Brightside; any Waze data-sharing or pavement-AI pilot (one search each). *Not found.*
- City participation in What Works Cities (three searches; official list blocked to curl). *Not found.*
- An open-data policy, ordinance or executive order; a formal City–university data-sharing agreement. *Not found.*
- A city page linking the Neighborhood Foresters or their app, despite the group's statement that it "partner[s] with and answer[s] to the Forestry Division". *Not found.*
- "Not found" means searched and not seen. It does not mean absent.

### 3.6 This thread's judgment on §3 (kept separate from the facts above)

- **I:** The shortest documented route is a department sponsor plus the CityStat team, using data and licences the city already holds, so that the request is an "enhancement" rather than a "strategic project".
- **I:** Anything that asks city staff to use an AI tool directly needs ITSA approval first. Something whose output is ordinary data (a list, a file, a map layer) that staff review does not obviously require staff to "use an AI tool", but the policy's scope also names partners and volunteers "leveraging AI systems to provide services to the City", so the text does not settle it.
- **I:** The city's stated cost questions are about staff hours and recurring cost more than purchase price.
- **I:** The one outsider tool line that reached a city contract did so through a standing intermediary and one persistent developer over six years, not through a hackathon hand-off.
- **I:** The vacancy tool, the tornado trackers and the tree app share one developer and partly one database project, so the City's reliance on them has a single point of dependence.
- **I:** The tornado trackers probably grew out of that developer's existing vacancy work (same host; a tornado layer inside the Vacancy Explorer). No document confirms it.
- **Open:** whether a free, outsider-hosted tool counts as "procurement". No rule was found either way, and the tornado trackers show the City has embedded one.

## 4. Full case table

Status columns give what was loaded on 13–14 Oct 2026 UTC unless a date is shown. "Notes" names the part file and note where every URL and retrieval time is recorded: **AN** = `E-precedents-analytics.md`; **OT** = `E-precedents-outsider-tools.md`; **TH** = `E-outsider.d/themes.md`; **SU** = `E-outsider.d/startups-univ-intl.md`; **ST** = `E-stl-civic-tech.md`; **TS** = `E-stl-civic-tech.d/tornado-and-streets.md`; **JU** = `…/justice-and-universities.md`; **PH** = `…/philanthropy-programmes.md`; **IT** = `E-stl-city-it.md`.

### 4A. Analysis of city-held data (41)

| ID | City — case | Problem; data (city-held?) | Routine changed | Measured result (who measured) | Who did it → how adopted | Status | Outcome | Label | Source (notes) |
|---|---|---|---|---|---|---|---|---|---|
| A1 | Flint MI — lead service lines | Which homes have lead lines; parcel and water records, dig results (yes, poor) | Dig order followed model 2016–17; dropped 2018; reinstated 2019 | 70% hit rate 2017; 15% in 2018; 64% vs 3% in 2019 (modellers, NRDC attorney, press) | University researchers, later BlueConduit → small city team; reinstated after litigation | Not established | adopted, dropped, reinstated | O | <https://www.nextgov.com/artificial-intelligence/2019/01/how-ai-found-flints-lead-pipes-and-then-humans-lost-them/153905/> (AN N1) |
| A2 | Chicago — food-inspection forecasting | Inspection order; inspections, 311, licences, weather (yes) | Risk scores used in scheduling from 2015 | 7.4 days earlier in the city's simulation; IIT re-analysis disputes attribution and fairness | City IT with Allstate volunteers → in-house | Not established; repo last push Apr 2019 | adopted; current use unknown | O | <https://arxiv.org/pdf/1910.04906> (AN N2) |
| A3 | Chicago — Strategic Subject List | Gun-violence risk; arrest and victim records (yes) | Scores used for notifications | No effectiveness shown (Inspector General) | IIT with police → $3.8M federal grants | Decommissioned 1 Nov 2019 | adopted, then retired | O | <https://igchicago.org/wp-content/uploads/2020/01/OIG-Advisory-Concerning-CPDs-Predictive-Risk-Models-.pdf> (AN N3) |
| A4 | Syracuse NY — water-main breaks | Which mains will break; break history, pipe records (yes, gaps) | Risk list used for planning with road work | 33 breaks on riskiest 52 mains by end-2017 (project team) | UChicago DSSG → mayor's innovation team | Not established | adopted; current use unknown | O | <https://arxiv.org/pdf/1805.03597> (AN N4) |
| A5 | New York — illegal conversions | Which complaints are dangerous; 311, tax arrears, foreclosures (yes) | Complaints re-ranked before inspection | No figure verified in the source read | Mayor's Office of Data Analytics → central team serving the agency | Not established | adopted; current use unknown | O (method) | <https://beyondtransparency.org/chapters/part-4/beyond-open-data-the-data-driven-city/> via Wayback (AN N5) |
| A6 | New Orleans — smoke-alarm targeting | Where to canvass; census surveys plus fire incidents (partly) | Canvass route targeted by block group | Model estimate only: 2,890 vs 1,445 alarms per 10% canvassed (city) | City analytics office → fire department | Report now under an archived path | adopted; current use unknown | O | <https://nola.gov/performance-and-accountability/reports/nolalytics-reports/full-report-on-analytics-informed-smoke-alarm-outr/> (AN N6) |
| A7 | Boston — CityScore | Daily performance score; departmental metrics (yes) | Budget for 20 EMTs and 10 ambulances | None independent (city) | City analytics team → Mayor reads score | Page updated 30 Oct 2025 | adopted, running | O | <https://www.boston.gov/departments/analytics-team/cityscore> (AN N7) |
| A8 | Boston — Street Bump | Rough streets; new phone-sensor data (no) | City worked with utilities; 1,250 worst manhole covers fixed | False positives under 10% (city) | New Urban Mechanics with contractors and contest entrants | City page: "not currently active"; app URL 404 | adopted, then retired; no reason given | O | <https://www.boston.gov/departments/new-urban-mechanics/street-bump> (AN N8; TH 4) |
| A9 | Baltimore — CitiStat | Performance meetings; departmental data (yes) | Accountability meetings from 2000 | 2014: no reports, a third of meetings cancelled (Baltimore Sun via Governing) | Mayor's office | Lapsed, partly revived; contested 2023 | adopted, lapsed | O | <https://www.govtech.com/data/CitiStat-StateStat-Struggle-to-Stay-Alive-on-Their-Home-Turf.html> (AN N9) |
| A10 | Los Angeles — CleanStat | Street cleanliness; new quarterly survey (no) | Crews aimed at worst segments | 312 to 53 miles needing clean-up, 2016–2018 (Results for America from city data) | Mayor's office and Sanitation → executive directive | No post-2018 source found | adopted; current use unknown | O | <https://results4america.org/wp-content/uploads/2018/12/LosAngelesCaseStudy_Final.pdf> (AN N10) |
| A11 | Washington DC — rat burrows | Unreported burrows; 311 and property data (yes) | None | Field test of 100 sites failed (city lab) | The Lab @ DC with Rodent Control | Not adopted | never adopted | O | <https://thelabprojects.dc.gov/rats> (AN N11) |
| A12 | New York — tree pruning | Does block pruning cut emergencies; Parks records (yes) | None found | 22% fewer emergency clean-ups (volunteer) | DataKind volunteer; Parks asked | Not established | analysis only | O | <https://www.cio.com/article/289016/data-management-new-york-turns-to-big-data-to-solve-big-tree-problem.html> (AN N12) |
| A13 | London — unlicensed shared houses | Borough property data (yes, uneven) | None in phase 1 | 4 of 12 boroughs usable (GLA/Nesta) | ASI Data Science for GLA/Nesta | Phase 1 failed; office made permanent | never adopted (model) | O | <https://www.nesta.org.uk/report/piloting-the-london-office-of-data-analytics/> (AN N13) |
| A14 | Pittsburgh — commercial fire risk | Fire incidents, property data (yes) | Inspection priority via dashboard | 14 of 45 incidents in flagged properties vs 0.20% base (project team) | CMU Metro21 → Bureau of Fire; on city servers | Nothing dated after Apr 2020 | adopted; current use unknown | O | <https://www.cmu.edu/metro21/projects/smart-infrastructure/fire-risk-analysis.html> (AN N14; SU 6) |
| A15 | Atlanta — Firebird | Which buildings to fire-inspect; fire, licence, property data (yes) | 6,096 uninspected properties identified | Up to 71% true-positive rate (authors) | Georgia Tech → fire department | Not established | adopted; current use unknown | O | <https://arxiv.org/abs/1602.09067> (AN N15) |
| A16 | Philadelphia — Litter Index | New survey (no) | Informed cleaning plans | None found | Zero Waste and Litter Cabinet → mayor created it | Cabinet cut 2020; concluded 2024 | adopted, then retired | O | <https://whyy.org/articles/mayor-jim-kenney-kills-anti-litter-initiative-amid-coronavirus-budget-crunch/> (AN N16) |
| A17 | Chicago — tree trimming | Trimming order; 311 requests, work records (yes) | 311-driven to area-based, 2023 | About 31,000 to about 90,000 trims a year (city) | Consultant 2009; Inspector General 2019 → department redesign | 2023–2026 figures on city page | adopted, running | O | <https://igchicago.org/wp-content/uploads/2023/08/OIG-Advisory-Concerning-DSS-Inefficient-Tree-Trimming-Operations.pdf> (AN N17) |
| A18 | Chicago — rodent baiting | Baiting schedule; 31 types of 311 request (yes) | Preventive schedule from 2013 | "20 percent improvement" (department spokeswoman) | City IT with CMU lab | 2026 audit: the project "was abandoned"; records no longer held | adopted, then abandoned; no reason recorded | O | <https://igchicago.org/wp-content/uploads/2026/07/Audit-of-DSSs-Rat-Abatement-Program.pdf> (AN N18) |
| A19 | Hackney UK — early-help profiling | Council records (yes, limited) | Alerts ran alongside normal work | None; £361,400 spent (council) | Xantura (vendor) | Dropped 2019 | adopted, then retired | O | <https://www.hackneycitizen.co.uk/2019/10/30/town-hall-drops-pilot-programme-profiling-families-without-their-knowledge/> (AN N19) |
| A20 | Los Angeles — LASER, PredPol | Crime and arrest data (yes) | Patrol zones, offender lists | Inspector General could not measure effectiveness | LAPD with vendors | Ended 2019; PredPol 2020 (H) | adopted, then retired | O / H | <https://www.govtech.com/public-safety/LAPD-Pulls-Plug-on-Another-Data-Driven-Crime-Program.html> (AN N20) |
| A21 | Pittsburgh — hot-spot policing | Offences, 911 calls (yes) | Patrols sent to predicted spots | 34% and 24% drops (CMU's own) | CMU Metro21 → police pilot | Ended Dec 2019 | adopted, then retired | O | <https://www.nextgov.com/artificial-intelligence/2020/07/one-city-rejected-policing-algorithm-could-it-be-used-other-purposes/166987/> (AN N21) |
| A22 | Allegheny County PA — family screening tool | County data warehouse (yes) | Score shown to call screeners from 2016 | More accurate screen-ins, smaller racial gap (Stanford, via county summary) | Academics → competitive contract | Not established after 2019 | adopted; current use unknown | O | <https://analytics.alleghenycounty.us/wp-content/uploads/2019/05/Impact-Evaluation-Summary-from-16-ACDHS-26_PredictiveRisk_Package_050119_FINAL-5.pdf> (AN N22) |
| A23 | Boston — school start times | Student and route data (yes) | Start-time plan withdrawn Dec 2017 | Savings not raw-verified | MIT researchers → district contest | Start times reversed | partly adopted | O / H | <https://www.boston.com/news/education/2017/12/21/boston-school-start-end-time-change/> (AN N23) |
| A24 | Mobile AL — blight index | New photo survey joined to tax and code records (partly) | Code officers given a proactive workload | 926 then 1,256 properties found; no net change found | Bloomberg-funded innovation team; mayor asked | Not established | adopted; current use unknown | O | <https://www.route-fifty.com/digital-government/2017/03/city-enlists-instagram-in-blight-cleanup/303535/> (AN N24) |
| A25 | New Orleans — BlightStat | Code-enforcement data (yes) | Public monthly meetings; seizure policy | 52 of 300 "fixed" properties still blighted (The Lens) | City analytics office → mayor | "No longer in operation" as of May 2021 (state senate resolution) | adopted, then retired; no reason found | O | <https://www.legis.la.gov/legis/ViewDocument.aspx?d=1232263> (AN N25) |
| A26 | Memphis — vehicle-camera detection | Potholes, high grass, dumping; new video (no) | Detections become work tickets after a crew member confirms | About 90% accuracy (city official) | City with Google and a partner; CIO approached vendor; started 2019 | In use per Feb 2025 and Jan 2026 news reports; five vehicles | adopted, running | O | <https://statescoop.com/memphis-ai-video-tech-equipped-city-trucks-fix-infrastructure-issues/> (AN N26; TH 7) |
| A27 | Kansas City MO — pothole prediction | Traffic, weather, road data (yes) | Pilot on about six streets | No result found | City innovation office with a vendor; public works director asked | Nothing found after Mar 2018 | pilot; outcome unknown | O | <https://www.govtech.com/fs/How-Kansas-City-Mo-Is-Snuffing-Out-Potholes-Before-They-Appear.html> (AN N27) |
| A28 | Tempe AZ — graffiti detection | New vehicle imagery (no) | Crews see flagged sites before shift | 15.17 to 1.3 incidents per four miles, 2013–2019 (city audit; predates the tool) | City GIS with Arizona State; crew asked | Not established | adopted; current use unknown | O | <https://web.archive.org/web/20251109212628id_/https://www.esri.com/about/newsroom/arcnews/machine-learning-streamlines-graffiti-removal-in-tempe> (AN N28) |
| A29 | Kansas City MO — KCStat | Departmental data (yes) | Meetings postponed 2019 | n/a | City | Not established | unknown | H | (AN N29) |
| A30 | Rotterdam — welfare-fraud scores | Benefits records (yes) | Use halted | Bias found (press) | Vendor and city | Dead; date disputed | adopted, then retired | H | <https://www.lighthousereports.com/> (AN N29) |
| A31 | Amsterdam — welfare checks | Benefits records (yes) | Pilot ended | Bias persisted (press) | City | Dead | never adopted | H | <https://www.technologyreview.com/2025/06/11/1118233/amsterdam-fair-welfare-ai-discriminatory-algorithms-failure/> (AN N29) |
| A32 | England, four councils — children's social care | Case records (yes) | None | Models missed most at-risk children (research centre) | Research pilot | Not adopted | never adopted | H | (AN N29) |
| A33 | South Bend IN — 1,000 houses | Code-enforcement survey (partly) | Repair-or-demolish list | 1,016 addressed (city) | Mayor's task force | Completed 2015 | adopted, completed | H | (AN N29) |
| A34 | Detroit — Motor City Mapping | New survey of 370,000+ parcels (no) | Basis of the 2014 blight plan | No evaluation found; three sources give three parcel counts | Data Driven Detroit, nonprofit and a mapping firm → commissioned by a task force; $1.5M foundation grant | Public site fails TLS | adopted, then retired; no reason given | O | <https://datadrivendetroit.org/2014/05/27/detroit-blight-removal-task-force-releases-report/> (TH 14; AN N29) |
| A35 | Cincinnati — overdose response | EMS runs (yes) | Case made for more medic units | None found | City analytics office | Not established | unknown | H | (AN N29) |
| A36 | New York — FDNY FireCast | Multi-agency building data (yes) | Risk-ranked inspection lists | None verified | Fire department | Not established | unknown | H | (AN N29) |
| A37 | Chicago — weed cutting on vacant lots | Department work orders, property lists (yes; no reliable lot inventory) | Contractor given weekly lists of city lots; complaint target cut from 42 to 21 days | Goals not met at audit (Inspector General); no later figure | Inspector General, 2020 → department agreed | Not checked after 2020 | adopted; current use unknown | O | <https://igchicago.org/wp-content/uploads/2023/08/DSS-Weed-Cutting-Program-Audit.pdf> (AN N31) |
| A38 | New Orleans — Fight the Blight | Lot clean-up and mowing; code-enforcement and police records (yes) | None tied to the study | No change in violent or property crime; drug crime 5.7% lower (academic) | City programme from 2014; evaluated afterwards by university researchers | Not established | analysis only | O | <https://pmc.ncbi.nlm.nih.gov/articles/PMC6225884> (AN N33) |
| A39 | Philadelphia — vacant-lot greening (LandCare) | Tax, licensing and police records (yes) | None tied to the research | Fewer gun assaults near greened lots (Penn, 2011); 2018 trial figures H | Programme since 1999; Penn researchers | Programme status not checked | analysis only | O / H | <https://web.archive.org/web/20260114143715id_/https://whyy.org/articles/penn-study-finds-phs-vacant-land-program-reduces-assaults-and-vandalism/> (AN N30) |
| A40 | Maryland (state) — StateStat | Agency data (yes) | Regular meetings ended | n/a | Governor's office | Discontinued under the next governor; budget halved, staff nine to four | adopted, then retired | O | <https://www.govtech.com/data/CitiStat-StateStat-Struggle-to-Stay-Alive-on-Their-Home-Turf.html> (AN N9) |
| A41 | Flint and Genesee County MI — Clean & Green mowing | Land-bank records (yes) | Community groups paid to mow on a three-week cycle | Nearly 40% fewer assaults on maintained streets, 2009–13 (reported) | County land bank | Not established | unknown | H | <https://communityprogress.org/wp-content/uploads/2022/11/2023-vls-greening-and-community-safety.pdf> (AN N34) |

### 4B. Tools built outside city government (48)

| ID | City — tool | Problem; data | Routine changed in government | Measured result (who measured) | Builder → adoption path | Status | Outcome | Label | Source (notes) |
|---|---|---|---|---|---|---|---|---|---|
| T1 | Boston — Adopt-a-Hydrant | Residents shovel out hydrants; city hydrant list | None documented | "About 100 volunteers" (city); 500 hydrants (builder) | Code for America fellow with Fire and Emergency Management | Domain redirects to an unrelated site | adopted, then retired; no reason given | O / R | <https://www.boston.gov/departments/new-urban-mechanics/adopt-hydrant> (OT C1) |
| T2 | Honolulu — Adopt-a-Siren | Reuse of T1 | None found | None found | Code for America | DNS fails; last good archive copy 2023-04-17 | adopted, then retired; no reason given | O | (OT C1) |
| T3 | San Francisco — Adopt-a-Drain | Residents clear storm drains | Not checked | "7,909 Drains Adopted" on page | Reuse of the model, on the utility's own domain | Live | adopted, running | O | <https://adoptadrain.sfwater.org> (OT C1) |
| T4 | Washington DC — Apps for Democracy | Open-data app contest, 2008–2010 | None; contest discontinued | 47 apps for $50,000 in prizes (organisers) | Contest run outside core departments | Site times out | never adopted (as a class) | R | <https://www.govtech.com/pcio/Election-Turnover-Brings-Pink-Slips-to-Agency-Heads.html> (OT C2) |
| T5 | National — Code for America Brigade Network | About 60 volunteer chapters | n/a (context) | n/a | Fiscal sponsorship ended 2023 | Ended; successor alliance of 16 groups | context | R | <https://statescoop.com/code-for-america-local-brigades-ending/> (OT C3) |
| T6 | New Orleans — BlightStatus | Property code-enforcement status lookup | Public lookup of city data | None found | Code for America fellows 2012; the City's one stated fellowship goal → company (Civic Insight) → Accela | Site fails TLS | adopted, then replaced by vendor | O / R | <https://nola14.nytimes-institute.com/2014/05/27/hackers-help-track-crumbling-properties/> (OT C4) |
| T7 | Honolulu — Honolulu Answers | Plain-language answers to top searches | City site content | None found | Code for America fellows 2012 | DNS fails; last good archive copy 2014 | adopted, then retired; no reason given | O / R | <https://www.govtech.com/gov-experience/Want-Better-Answers-from-Your-City-Honolulu-Can-Help.html> (OT C5) |
| T8 | Boston — DiscoverBPS | School-choice lookup | Replaced a 28-page mailed pamphlet; later online registration | 28,500 users in 2014 (city) | New Urban Mechanics, Code for America, school district; fellow kept on as paid partner | Replaced by Great Starts on `boston.gov` | adopted, then replaced by city product | R | <https://www.boston.gov/departments/new-urban-mechanics/discover-bps> (OT C6) |
| T9 | Oakland — RecordTrac | Public-records requests | Records managers' workflow | None found | Code for America fellows 2013 → NextRequest (company) → CivicPlus | Oakland portal is a NextRequest instance | adopted, then replaced by vendor | O / R | <https://www.route-fifty.com/infrastructure/2015/08/public-record-requests-made-easy-for-government/293525/> (OT C7) |
| T10 | Philadelphia — Textizen | Text-message surveys | City pilot | None found | Code for America fellows 2012 → company → GovDelivery | Domain dead; product renamed | adopted, then replaced by vendor | R | <https://technical.ly/startups/textizen-govdelivery-acquisition/> (OT C8) |
| T11 | Atlanta, Anchorage, Tulsa — CourtBot | Court-date text reminders | Not established; Alaska courts now run their own reminders | None found | Code for America, then local brigades | Original domains parked; Anchorage instance answers | unknown / mixed | O | <https://courts.alaska.gov/tos/text-reminders.htm> (OT C9) |
| T12 | California counties — Clear My Record | Automated record clearance | District attorneys ran bulk eligibility checks | 144,000 convictions reduced or dismissed (builder) | Code for America with five elected district attorneys; free tool; a 2018 state law then required the automatic approach; about half of counties used it | Site says project "has currently ended" | adopted, then retired; no reason found | O / R | <https://nextcity.org/urbanist-news/using-tech-california-counties-cleared-140000-marijuana-related-convictions> (OT C10) |
| T13 | California — GetCalFresh | Food-benefit applications | State's primary online application channel 2019–2025; applications then moved to the State's own site; nonprofit keeps outreach role | 6.2 million people helped (builder) | Code for America → seven-county state contract 2014 → $3.6M for 58 counties, 2017 | Site redirects applicants to BenefitsCal | adopted, then replaced by government system | O / R | <https://cdss.ca.gov/inforesources/cdss-programs/calfresh-outreach/getcalfresh-transition> (OT C11) |
| T14 | Streetmix | Street-section design tool | None found | None | Code for America fellows; independent | Live; repo pushed 2026-10-11 | unknown (no adoption evidence) | O | <https://streetmix.net> (OT C12) |
| T15 | Oakland — Open Budget Oakland | Budget visualisation | None found | None | Volunteers | Live; newest cycle seen 2021–2023 | unknown | O | <https://openbudgetoakland.org/> (OT C13) |
| T16 | New York — BigApps | App contest | None found; organisers later had partner organisations write problem briefs | Some winners endured, many did not (press) | Contest | Domain serves gambling content | never adopted (as a class) | O / R | <https://thelivinglib.org/new-york-city-bigapps-winners-show-how-civic-tech-is-maturing/> (OT C14) |
| T17 | Chicago — Foodborne Chicago | Food-poisoning tweets → complaints | Complaints entered the inspection queue; staff replied to residents | 133 inspections from 193 complaints in 10 months; 20.3% with a critical violation vs 16.4% for other complaint inspections (health department and partners, MMWR) | Volunteers and Smart Chicago with a named department employee; Knight grant | Site 403 to curl; status not established | adopted; current use unknown | R | <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4584908/fullTextXML> (OT C15) |
| T18 | Chicago — ClearStreets | Plow tracking from scraped city data | City later added address search to its own tracker (link not claimed) | None | Volunteers, 2012–2019 | Site says no longer active | never adopted; function absorbed by city | R | <https://clearstreets.org/> (OT C16) |
| T19 | Chicago — sewage-in-river tracker | Sewer overflow alerts | None found | None | Volunteers | Site says inactive; data ends 1 Mar 2018 | never adopted | O | <http://istheresewageinthechicagoriver.com> (OT C17) |
| T20 | Chicago — SweepAround | Street-sweeping alerts | None found | None | Volunteers | Live under a new name, 2026 schedules | unknown | O | <https://sweeparound.us> (OT C18) |
| T21 | Los Angeles Metro, New York, Chicago — Councilmatic | Legislation browser | LA Metro instance on agency domain; NYC Council "officially adopted" it in 2017 | None | DataMade and a nonprofit; foundation money first, then agency partnerships; Chicago ordinance O2024-0008352 authorises master service agreements with the firm | LA Metro and Chicago live; both New York hosts fail | adopted, running (LA Metro); New York unknown; Chicago not a city service | O / R | <https://www.councilmatic.org> (OT C19) |
| T22 | Citizinvestor | Municipal crowdfunding | Four municipalities bought the white-label product | 37 of 76 projects funded; $282,737 collected (founders) | Startup | Closed June 2018; domain now a finance blog | adopted, then retired | R | <https://civictech.guide/learning-from-the-civic-tech-graveyard/> (OT C20) |
| T23 | Philadelphia and others — OpenTreeMap | Crowdsourced tree inventory | None found in Philadelphia | None independent | Azavea; federal and state grants plus subscriptions | Offline by Aug 2024; domain serves casino content | adopted, then retired; no reason given | O | <https://github.com/OpenTreeMap/otm-core/issues/3328> (TH 1) |
| T24 | San Francisco — Urban Forest Map | Shared street-tree inventory | Replaced by a city-hosted street-tree map | None | Nonprofit and city on OpenTreeMap | Domain points elsewhere | adopted, then replaced by city system | O / H | <https://sfpublicworks.org/services/street-tree-map> (TH 2) |
| T25 | New York — TreesCount!, TreeKIT, Tree Map | Street-tree census; volunteer field measurements | Census became the forestry management system used daily; map shows work orders | 666,134 street trees mapped, 2,200+ volunteers (Parks) | Volunteer method adopted by Parks; city-hosted | Live; activities dated 13 Oct 2026; street counts now by LiDAR | adopted, running | O | <https://www.nycgovparks.org/tree-map/learn/about> (TH 3) |
| T26 | Many US cities — RoadBotics | Pavement rating from phone video | Recurring survey contracts | "Over 250 governments" (company) | CMU spin-out 2016 → Michelin 2022 | Michelin: discontinued by end of 2025 | adopted, then retired by acquirer | O / R | <https://mobilityintelligence.michelin.com/us/road-assessments/> (TH 5) |
| T27 | Syracuse — SQUID | Street-quality sensor on a city truck | None found; later road-rating map used another source | Developer figures not raw-verified | ARGO Labs; found by the city innovation office; $2,000–$3,000 trial | No trace after 2016; repo 404 | pilot; never adopted (I) | R | <https://www.route-fifty.com/emerging-tech/2016/04/syracuse-data-potholes-rough-roads/127602/> (TH 6) |
| T28 | San José — road-safety camera pilot | Potholes, dumping, debris from city-vehicle cameras | None yet; staff typed results into 311 by hand in phase one | 97% pothole and 88% dumping accuracy (city) | Vendors under a $260,000 foundation grant | Not operational as of Feb 2026 | pilot | R | <https://statescoop.com/san-jose-california-ai-streets-pilot-projects/> (TH 8) |
| T29 | Carbin | Crowdsourced road roughness | None | None | MIT and Harvard researchers | Domain dead | never adopted | O / R | <https://news.mit.edu/2019/mit-concrete-sustainability-hub-app-reads-road-heartbeat-0228> (TH 9) |
| T30 | Pittsburgh — snow plow tracker | Public plow map (city-built; included for contrast) | Internal idle-time monitoring | Council members called it inaccurate | City with a telematics vendor | Reported removed, return planned (H) | adopted, then replaced | R / H | <https://www.wesa.fm/politics-government/2022-12-07/pittsburgh-approves-snow-plow-tracker-contract-despite-concerns-about-its-accuracy> (TH 10) |
| T31 | New York — 596 Acres, Living Lots | Map of vacant public land | Function moved to city garden programme and open data (builder's account) | About 30 sites made permanent (H) | Nonprofit, 2011–2014 | Map removed by builders | never adopted as a tool | O | <https://livinglotsnyc.org> (TH 11) |
| T32 | Philadelphia — Grounded in Philly | Vacant-lot map and legal help | None found | "140+ Vacant Lots Transformed" (site) | Public-interest law nonprofit | Live | unknown | O | <https://groundedinphilly.org> (TH 12) |
| T33 | Chicago — Large Lots, then ChiBlockBuilder | $1 sale of city-owned vacant lots | One-page application; volume forced the City to change its review | 1,250 lots sold by spring 2020 (builder) | Community organisation asked; foundations paid; DataMade built; City adopted by ordinance 10 Dec 2014; same builder on contract for successor | `largelots.org` dead; `chiblockbuilder.com` live | adopted, then replaced by same builder under contract | O / R | <https://datamade.us/blog/chi-block-builder/> (TH 13) |
| T34 | New Haven — SeeClickFix | Resident issue reports | Reports feed Cityworks; "universal front end" from 2012; parks tree-trimming workflow moved onto it | 151,347 requests resolved all time (site, observed) | Resident-founded startup; CAO used it first | Live as a CivicPlus product | adopted, running | O / R | <https://www.newhavenindependent.org/2013/11/22/seeclickfix_6_years/> (SU 1) |
| T35 | Boston — Citizens Connect, BOS:311 | Photo reports from phones | Photos land in the responsible crew's queue | App share of requests 6% in 2010, about 28% by 2014 (city) | Small firm for the mayor's innovation office; about $25,000 | Live | adopted, running | O / R | <https://www.boston.gov/departments/new-urban-mechanics/bos311-app> (SU 2) |
| T36 | Massachusetts — Commonwealth Connect | T35 spread to towns | 45 cities and towns live | 8,000 requests (state association) | $400,000 state grant; three funded years | Renewal count not found; one non-renewal unverified | unknown | R / H | <https://www.govtech.com/transportation/Bostons-Reporting-App-Expands-Statewide.html> (SU 2) |
| T37 | Open311 standard | Common API for service requests | None attributable | 4 of 31 registry endpoints answered at the listed address | Coalition of cities and nonprofits | Spec last pushed 2022-05-24 | running in some cities; registry unmaintained | O | <https://wiki.open311.org/GeoReport_v2/Servers/> (SU 3) |
| T38 | Transit agencies — Remix | Transit sketch planning | Used for agency planning | "450+" agencies (vendor) | Code for America fellows' side project → company → Via, $100M | Live as a Via product | adopted, running | O / R | <https://techcrunch.com/2021/03/09/via-buys-mapping-startup-remix-for-100-million/> (SU 4) |
| T39 | Many cities — Nextdoor agency accounts | Outbound posts to neighbourhoods | Broadcast channel only | None found | Company; free; agencies sign up | Live | adopted, running | O | <https://about.nextdoor.com/public-agency> (SU 5) |
| T40 | Pittsburgh — Surtrac | Adaptive traffic signals | 50 intersections by 2017; operations stayed with the university | About 40% less wait, 26% less travel time (developers) | CMU, foundation-funded → spin-off → Miovision | Street status 2025–26 not established | adopted; hand-over stalled; product now a vendor's | R | <https://dspace.mit.edu/handle/1721.1/123931> (SU 6) |
| T41 | Cary NC, Massachusetts, CDC — Biobot | Wastewater monitoring | Proof of concept in Cary; later state and federal supplier | One police investigation credited (agency) | MIT students → startup; Bloomberg grant for first pilot | Company live; CDC switched vendor 2023; Massachusetts in-house from 31 Jul 2026 | adopted, then replaced by government and another vendor | R | <https://www.bostonglobe.com/2026/07/04/metro/wastewater-monitoring-biobot-massachusetts/> (SU 7) |
| T42 | Seattle — Trash Track | Tagged waste tracking | None found | None | MIT lab | Project page live | never adopted (I; weak) | O | <https://senseable.mit.edu/trashtrack/> (SU 8) |
| T43 | Taiwan — vTaiwan | Online consensus process | Shaped ride-hailing rules 2015; no major decision since 2018 | 26 cases by 2018 (self-report) | Volunteers at a minister's invitation | Site live; government runs its own platform | adopted, then replaced by government system | R | <https://www.technologyreview.com/2018/08/21/240284/the-simple-but-ingenious-system-taiwan-uses-to-crowdsource-its-laws/> (SU 9) |
| T44 | UK councils — FixMyStreet Pro | Street-fault reporting | Integrates with councils' asset systems | "More than 30" authorities (vendor) | Charity's trading arm, hosted service | Sites returned a maintenance page on 13 Oct | adopted, running (provisional) | H | <https://www.societyworks.org/case-studies/oxfordshire/> (SU 10) |
| T45 | Barcelona — Decidim | Participation platform (city-commissioned, not outsider-built) | City planning process | About 500 instances (project) | City council; handed to an association 2019 | Project site live | adopted, running (provisional) | H | <https://decidim.org/usedby/> (SU 11) |
| T46 | Philadelphia — SEPTAlking | Transit app from a 2011 hackathon | None | None | One developer | Shut down 2013; builder had no time | never adopted | R | <https://technical.ly/civic-news/mark-headd-septalking-shut-down/> (OT resume pass) |
| T47 | Chicago — mRelief | Benefits eligibility screener by web and text | Introduced to six city service centres for caseworkers; screening time about 16 to about 4 minutes (co-founder) | 200,000+ people connected (builder) | Two volunteers after the mayor's innovation team described the problem; Knight seed grant; later contracts | Site live; current government clients not verified | adopted; current use unknown | R | <https://knightfoundation.org/articles/mrelief-uses-text-messaging-to-help-people-get-social-assistance> (OT C21) |
| T48 | Chicago — Smart Chicago, CUTGroup, City Tech (context) | Intermediary that funded and tested civic tools | n/a | n/a | Founded by the City and two foundations; merged 2017 | City Tech closed end of 2021; CUTGroup domain serves a lottery site | context; host closed, no reason found | R / O | <https://chihacknight.org/events/2022/04/26/meera-raja> (OT C22) |

### 4C. St. Louis (61)

"City" = City of St. Louis. "County" = St. Louis County, a separate government.

| ID | Item | Gov't | Who built; when | Evidence of government uptake | Status | Outcome | Label | Source (notes) |
|---|---|---|---|---|---|---|---|---|
| S1 | STL Vacancy Portal (prototype) | City | Volunteers from OpenSTL, Green City Coalition and Daugherty Business Solutions; Sept 2017 hackathon; live July 2018 | Hackathon endorsed by Mayor Krewson and LRA (organisers' account, R); Mayor's 2018 vacancy plan names the volunteers; 2019 resilience strategy marks it "Funded" with LRA and ITSA as leads | Superseded by S2 | endorsed; evolved | O / R | <https://stldata.org/project-stl-vacancy-portal/> (ST log; PH) |
| S2 | Vacant Property Explorer and the Vacancy Strategy Initiative | City | Public Goodness (Dave Menninger) for the Vacancy Collaborative and Legal Services of Eastern Missouri | CDA two-year, $500,000 contract, May 2023; $499,949.59 paid FY2024–26 via Community Builders Network; City news 30 Sep 2026 links the tool | Live; data file modified 30 Sep 2026; Collaborative volunteer-driven again in 2026 | city-funded and linked; running on builder's host | O | <https://www.stlouis-mo.gov/government/departments/community-development/news/cda-announces-vacancy-strategy-initiative-with-the-st-louis-vacancy-collaborative.cfm> (ST 2P-1, 2P-2) |
| S3 | STL Recovers parcel trackers | City | Public Goodness; start date not found | Embedded on `tornadorecovery.stl.gov`; arrangement, payer and approving official not found | Live | adopted, running; arrangement unknown | O | <https://tornadorecovery.stl.gov/dashboard/?demo> (TS A) |
| S4 | STL Neighborhood Map | City / regional | Menninger (volunteer) with SLU Law clinic and MU Extension | A city Planning staffer named among steerers; no link on the city neighbourhoods page | Live | unknown | O | <https://metromap.org/stl> (ST log) |
| S5 | OpenSTL (Code for America brigade) incl. VacantSearch | City / regional | Volunteers; GitHub org since 2013 | 2017 mayoral endorsement; nothing later found | Site loops; Meetup gone; listed "Inactive" | dormant | O | <https://civictech.guide/projects/openstl> (ST log) |
| S6 | OpenDataSTL hackathons, 2014 and 2015 | City | Volunteers | Neither press account reports adoption of any project | Event site times out | no adoption reported | O / R | <https://www.stlpr.org/economy-business/2015-05-31/altruistic-web-developers-spend-weekend-building-projects-to-help-st-louis> (ST log) |
| S7 | OpenSTL with the Recorder of Deeds, 2019 | City (elected office) | Volunteers with the Recorder | Joint presentation at a national conference; what was built not established | Recorder's external site live | unknown | R | <https://entrepreneurquarterly.com/st-louis-civic-tech-efforts-recognized-at-national-code-for-america-conference/> (ST log) |
| S8 | GlobalHack and its 2016 winner (Cemaritan) | City homeless-services network | Nonprofit hackathon; winning team, then paid developers | A shelter provider was to adopt in 2016; uptake not found | Domain is an essay-review site; tax data end 2017; product domain dead | dead; reason reported for the winning team | O / R | <https://www.globalhack.org/> (ST log) |
| S9 | YourSTLCourts; CivTech St. Louis | County | Collaborative with $200,000 from a national programme; launched 1 May 2017 | County was a partner; City court was not part of the launch and moved its cases to the state's CaseNet on 2 Jan 2025 | Site times out; last good archive copy 2021-04-19; code last pushed 2018 | used by County; now dead; no reason found | O / R | <https://statescoop.com/to-reduce-burden-on-the-courts-st-louis-county-expands-records-portal/> (JU; PH) |
| S10 | Clear My Record app for ArchCity Defenders | regional | OpenSTL volunteers, 2020 | None (nonprofit client) | Hosted app returns "No such app" | dead | O | <https://arch-city-cmr.herokuapp.com/> (JU) |
| S11 | St. Louis Regional Data Alliance; RDX portal | regional | UMSL centre; portal Aug 2020 with 420+ datasets | City named as a data source; 2023 City release cites its support for vacancy tools | Portal times out; site stale since 2022 | lapsed (I) | O | <https://blogs.umsl.edu/news/2020/08/26/newly-launched-st-louis-regional-data-exchange-brings-together-420-local-public-datasets-one-location/> (ST log) |
| S12 | SCIRA smart-city pilot; "Hacks and the City" | City | DHS S&T, a standards body and T-REX, 2018–2020 | City CTO took part in a two-day pilot | Project host gone | pilot only | O / H | <https://www.dhs.gov/archive/science-and-technology/news/2020/07/07/snapshot-scira-smart-cities-st-louis-leading-example> (ST log) |
| S13 | STL Neighborhood Foresters; MetroTreeLC app | City | Nonprofit; app by Public Goodness | Group says it "partner[s] with and answer[s] to the Forestry Division"; no city page or payment found; app reads from the Vacancy Collaborative's database, not a City system | Live | partner-run; city uptake unknown | O / R | <https://stlnf.org/> (ST log) |
| S14 | Tree Opportunity Mapping Tool | regional | University of Missouri and SLU, 2023 | None found | Live | no uptake found | O | <https://stltrees.datahubs.org/> (ST log) |
| S15 | Tree Equity Score; ParkServe | national | National nonprofits | Linked from the City sustainability page | Links present | city links only | O | <https://www.stlouis-mo.gov/government/departments/planning/sustainability/urban-vitality-ecology/> (ST log) |
| S16 | City tree-inventory RFPs (context: the City buying) | City | City; Aug–Sep 2025 and Feb–Mar 2026 | Second RFP asks for a "LiDAR digital twin … or in-person inventory"; awardees not found | RFP pages live | city procurement | O | <https://www.stlouis-mo.gov/government/departments/parks/documents/rfp-tree-inventory.cfm> (ST log) |
| S17 | The People's Response hub and intake forms | City | Action St. Louis and a partner; from 18 May 2025 for about six weeks | City listed Action St. Louis at $138,098 and thanked the effort; no evidence intake data reached the City | Hub closed June 2025; pages live | organisation funded; tool not taken up | O / R | <https://actionstl.org/tornado> (TS A) |
| S18 | 4theVille Emergency Hub | City | Neighbourhood nonprofits; three weeks from 17 May 2025 | Named in the City's annual report | Ended 7 June 2025 | thanked; no tool | O | <https://www.4theville.org/st-louis-tornado-response> (TS A) |
| S19 | Crisis Cleanup | City and wider | National volunteer platform; incident opened 17 May 2025 | City page gave its hotline through 30 May 2025 (H; page now 404) | Platform live; incident has no active number | adopted, then lapsed | O / H | <https://api.crisiscleanup.org/incidents> (TS A) |
| S20 | Surdex aerial imagery (pro bono) | City and County | Private firm; flight 17 May 2025 | Imagery shared with the City; overlaid on Forestry's tree inventory by a volunteering firm and a student | Public maps live | adopted (one-off use) | R | <https://source.washu.edu/2026/05/class-acts-amanda-kesler/> (TS A) |
| S21 | Esri disaster support | City | Existing GIS vendor | Whether a tornado dashboard was built not established | Article live | unknown | R | <https://www.stlmag.com/business/st-louis-geospatial-tornado-response/> (TS A) |
| S22 | Missouri SAVE Coalition inspections | State programme in the City | Volunteer engineers and architects | City credits 7,000+ structural safety inspections | Report read | adopted (used in response) | O | <https://tornadorecovery.stl.gov/wp-content/uploads/2026/05/STLRecovers_2025Report-1.pdf> (TS A) |
| S23 | United Way intake form and fund | regional | United Way, from 17 May 2025 | City "in partnership with the United Way" contracted $15.7M of long-term support | Form not checked | adopted as funding partner | O | <https://www.stlpr.org/health-science-environment/2025-05-17/st-louis-tornado-recovery-help> (TS A) |
| S24 | Community Foundation resource page and fund | regional | Foundation, May 2025 | Fund set up in coordination with the City | Page live | running | O | <https://stlgives.org/resources/> (TS A) |
| S25 | WashU Brown School preparedness study | City | University, published by Jan 2026 | No city response found | Article live | no uptake found | O | <https://www.stlpr.org/government-politics-issues/2026-01-05/washu-study-gaps-st-louis-emergency-preparedness-tornado> (TS A) |
| S26 | WashU "CLEAN STL" environmental monitoring | City | University; June 2026 | University says it is "formally partnering" with the City; department, agreement and money not established | Page live | announced partnership | R | <https://governmentrelations.wustl.edu/washu-partners-with-st-louis-to-expand-clean-stl-tornado-recovery-project/> (JU) |
| S27 | SeeClickFix | City | Company; resident posts since 2009 | 518 reports in the city bounding box, none acknowledged; no agency request types | Place page live; newest report 2026-04-06 | never adopted (I) | O | <https://seeclickfix.com/st-louis> (TS B) |
| S28 | Nextdoor agency partnership | City | Company; announced 16 Oct 2013 | City page shows 5,583 updates; police page 524 | Live | adopted, running | O | <https://nextdoor.com/agency-detail/mo/st-louis/city-of-st-louis/> (TS B) |
| S29 | Brightside St. Louis | City | Nonprofit since 1982 (H); Ordinance 68331, 2009 | Agency inside Parks, Recreation and Forestry plus cooperation agreement; $350,000 ARPA | Live | adopted, running (hybrid) | O | <https://www.stlouis-mo.gov/government/city-laws/board-bills/boardbill.cfm?BBId=4679> (TS B) |
| S30 | Dutchtown South illegal-dumping project | City neighbourhoods | Community corporation; $120,000 EPA grant, 2016 | No adoption step described | Outcome not checked | unknown | O | <https://www.stlpr.org/health-science-environment/2016-10-13/community-leaders-launch-initiative-to-clean-up-four-south-st-louis-neighborhoods> (TS B) |
| S31 | Trailnet crash reports | City and County | Nonprofit; annual | Claimed influence on corridor funding (H) | Report live, June 2026 | running; uptake not verified | O / H | <https://trailnet.org/blog/2025-state-of-our-streets/> (TS B) |
| S32 | Calm Streets | City | Trailnet with EPA funding, from 2014 | Nearly $1M in regional funds for one street, 2017; completion not checked | Pages live | adopted (one funded project) | O / R | <https://nextstl.com/2017/09/funding-approval-expected-st-louiss-first-calm-street-project/> (TS B) |
| S33 | WashU student evaluation of traffic calming | City | Two students with Trailnet; presented at T-REX, 2026 | None stated | Article live | no uptake found | O | <https://source.washu.edu/2026/08/caps-students-help-trailnet-create-safer-streets/> (TS B) |
| S34 | Close the Workhouse campaign | City | Legal and organising nonprofits; from 2018 | Aldermanic bill 17 Jul 2020; Mayor emptied and defunded the jail June–July 2021 | Campaign site live | adopted (policy) | O / R | <https://www.stlouis-mo.gov/government/departments/mayor/news/mayor-jones-statement-emptying-workhouse.cfm> (JU) |
| S35 | Cure Violence evaluation | City | WashU with other universities; 2021–2023 | Department of Health contracted and paid; City hosts the report; providers changed from 1 Sept 2023 | Report live | adopted (commissioned) | O / R | <https://www.stlouis-mo.gov/government/departments/public-safety/violence-prevention/documents/cure-violence-final-report-july-2023.cfm> (JU) |
| S36 | ShotSpotter evaluations | City (police) | SIUE professor with two police analysts | Federal grant names him research partner; presented to aldermen June 2024; coverage expanded | Report live | adopted (research partnership) | O / H | <https://www.siue.edu/ccsvp/pdf/SPIShotSpotterSLMPD2026.pdf> (JU) |
| S37 | Surveillance-technology ordinance 71842 | City | Board Bill 185; effective 6 May 2024 | Enacted; which outside analysis drove it not established | Ordinance page live | adopted (legislation) | O | <https://www.stlouis-mo.gov/government/city-laws/ordinances/ordinance.cfm?ord=71842> (JU) |
| S38 | Eviction Lab tracking page | regional | University lab | No city link found | Live | no uptake found | O | <https://evictionlab.org/eviction-tracking/st-louis-mo/> (JU) |
| S39 | Landlord Lawsuit List | regional | Public Goodness | None found | Live behind sign-in | unknown | O | <https://www.publicgoodness.org/stlcases/> (JU) |
| S40 | Right to Counsel (HELP-STL) | City | Ordinance 71694; Legal Services of Eastern Missouri by RFP; Aug 2024 | ARPA payments; CityStat publishes its figures | Live; contract ends 9/2026 | adopted, running | O | <https://www.stlouis-mo.gov/government/recovery/covid-19/arpa/projects/project.cfm?id=355> (JU) |
| S41 | SLU openGIS packages for City crime and 311 data | City data | One SLU professor, 2016–2022 | None found | 36 of 40 repos archived; package removed from CRAN 2021 | no uptake found; dead | O | <https://cran.r-project.org/web/packages/compstatr/index.html> (JU) |
| S42 | Forward Through Ferguson trackers | regional | Nonprofit | Not checked | Reports downloadable | unknown | O | <https://forwardthroughferguson.org/about/our-work/policy-data-2/> (JU) |
| S43 | Taylor Geospatial | regional / global | Research institute, 2022– | No City project found | Site live | no uptake found | O / H | <https://taylorgeospatial.org/> (JU) |
| S44 | 100 Resilient Cities; Office of Resilience | City | Rockefeller Foundation; office by Executive Order 56, 2016; strategy May 2019 | Chief Resilience Officer post fully funded for two years by the foundation | City pages archived; newest item 6 Sep 2019 | adopted, then lapsed | O | <https://www.stlouis-mo.gov/archives/resilience/index.cfm> (PH) |
| S45 | Equity Indicators | City | CUNY institute with foundations; announced 2017 | City-hosted baseline, score 45.57 | Archived; baseline only | adopted, then lapsed | O | <https://www.stlouis-mo.gov/archives/resilience/equity/index.cfm> (PH) |
| S46 | Resilience strategy actions 31–33 (smart-city strategy; vacancy portal; data infrastructure) | City | Mayor's Office, 2019 | Strategy states the City "currently lacks the necessary data infrastructure" | Implementation not checked | unknown | O | <https://resilientcitiesnetwork.org/downloadable_resources/Network/St-Louis-Resilience-Strategy-English.pdf> (PH) |
| S47 | Rockefeller Opportunity Zone initiative | City (development corporation) | Announced 6 Sep 2019; $920,000 incl. an embedded officer | Press release only | Post status not checked | unknown | O | <https://www.stlouis-mo.gov/government/departments/mayor/news/rockefeller-opportunity-zone.cfm> (PH) |
| S48 | Bloomberg American Cities Climate Challenge | City | 2018–2020 technical assistance | Solar-ready law (Dec 2019) credited by the City; building-energy ordinance 71132 (link H) | Ordinances in force; enforcement not checked | adopted, running | O / H | <https://www.stlouis-mo.gov/government/departments/mayor/news/solar-readiness-legislation-bb146.cfm> (PH) |
| S49 | Bloomberg American Sustainable Cities innovation team | City | Selected 12 Mar 2024; three years; up to three staff | Recovery Office lists an "Innovation Team" director; funding link is inferred | Running | adopted; current form not established | O / I | <https://www.developstlouis.org/news-media/basc> (PH; IT §5) |
| S50 | Bloomberg Harvard City Leadership Initiative | City (mayor) | Krewson 2018; Jones 2021–22 | Executive education; no product named | n/a | participated | O | <https://www.stlouis-mo.gov/government/departments/mayor/news/bloomberg-harvard-city.cfm> (PH) |
| S51 | Center for Community Progress technical assistance | City (land bank) | 2015–16; report June 2016 | Cited by the City in a 2023 vacancy-strategy RFP | Pages live | adopted (basis of later work) | O | <https://www.stlouis-mo.gov/government/departments/community-development/documents/rfp-for-vacancy-strategy.cfm> (PH) |
| S52 | Civic Tech and Data Collaborative | regional | National funders; $200,000, 2015 | City named as a member; product (S9) served County courts | Funder page 404 | county or region, not city | O | <https://www.govtech.com/dc/articles/Boston-St-Louis-Receive-Grants-To-Harness-Data-And-Technology.html> (PH) |
| S53 | "Federal Smart Cities Initiative"; first CTO | City | Announced Oct 2017; CTO hired Mar 2018 | CTO post persists; no published smart-city plan found | Releases live | adopted, running (post) | O | <https://www.stlouis-mo.gov/government/departments/mayor/news/cio-cto-appointments.cfm> (PH) |
| S54 | IKE Smart City kiosks | City with development corporation | Launched Jan 2020; advertising-funded (H) | City press releases quote the CTO | Vendor lists St. Louis; physical status not checked | adopted | O / H | <https://www.stlouis-mo.gov/government/departments/mayor/news/interactive-smart-city-digital-kiosks-launch.cfm> (PH) |
| S55 | US DOT Smart City Challenge, 2016 | City | Application only; not a finalist | n/a | Federal pages 403 | not selected | H | <https://www.transportation.gov/smartcity/applicant-list> (PH) |
| S56 | What Works Cities | — | — | No evidence of participation found in three searches | Official list 403 to curl | not established | O (negative) | <https://whatworkscities.bloomberg.org/cities/> (PH) |
| S57 | GeoSTL — vacant-lot mowing priority | City | Nonprofit; "working with the city for a few weeks" as of 26 Aug 2026 | No contract, department or result named | One news article | in progress; not established | R | <https://www.firstalert4.com/2026/08/26/st-louis-launches-ai-innovation-center-backed-by-tech-giants/> (IT §5) |
| S58 | UMSL students' tax analysis | City | Three classes using Assessor data; presented 12 May 2026 | COO and Assessor attended; praise and a hiring pitch; no decision reported | Article live | presented; no decision | R | <https://blogs.umsl.edu/news/2026/05/18/interdisciplinary-class-project/> (IT §5) |
| S59 | Spirit of St. Louis AI Innovation Center | regional | GeoSTL with corporate founders; launched 26 Aug 2026 | 20% of capacity reserved for civic projects; first competition expected November | Announced | new; no city use yet | R | <https://www.route-fifty.com/artificial-intelligence/2026/09/new-ai-center-announced-st-louis/415773/> (IT §5) |
| S60 | CityStat, incl. Forestry mowing analysis (context: city-built) | City | Mayor's Office; public launch 31 Mar 2026 | About 7,000 of 14,000 vacant lots mowed in the first 2026 rotation (city); crews to log each lot's status; modelled partly on Baltimore's system (news report) | Running; no outcome figure yet | city-built | O | <https://www.firstalert4.com/2026/07/09/first-alert-forward-what-can-st-louis-learn-baltimore-about-improving-services/> (PH) |
| S61 | Forest ReLeaf of Missouri — planting partner | City | Nonprofit; City Tree Canopy Expansion Program from Sept 2024 (federal grant) | Named on the City programme page; results delegated to the nonprofit's site; one $1,218.40 payment in FY2024 supplier lists, grant payment route not traced | City page live | adopted, running | O | <https://www.stlouis-mo.gov/government/departments/parks/forestry/trees/tree-canopy-program.cfm> (ST 2P-4; `B-existing-tools.md` §2) |

## Data rows actually retrieved in this thread

Under the project's evidence rule, only these count as retrieved data. Everything else above is pages and documents.

| Source | URL | Retrieved (UTC) | Rows | Date range |
|---|---|---|---|---|
| SeeClickFix issues in the City bounding box | <https://seeclickfix.com/api/v2/issues> (bounding box 38.532012 to 38.774288, −90.320515 to −90.166717) | 13 Oct 2026 23:26 and 23:32 | 519 unique issues (518 on the second pull) | 2009-10-06 to 2026-04-06 |
| City "Expenditures by Supplier" lists | <https://www.stlouis-mo.gov/government/departments/budget/transparency/expenditure/suppliers/index.cfm?fiscalYear=YYYY> | 14 Oct 2026 00:02 | 1,927 / 1,934 / 1,933 / 2,105 supplier rows | FY2023 / FY2024 / FY2025 / FY2026 |
| Open311 registry endpoints | <https://wiki.open311.org/GeoReport_v2/Servers/> | 13 Oct 2026 23:31–23:32 | 31 endpoints tested; 4 answered | n/a |
| Crisis Cleanup incidents | <https://api.crisiscleanup.org/incidents> | 13 Oct 2026 23:35 | 326 incidents | not recorded |
| Vacancy Explorer data file (header only; rows not downloaded) | <https://www.publicgoodness.org/stlv/csv/stl_vacancy_data.csv> | 13 Oct 2026 23:27 | not retrieved (6,812,286 bytes) | last modified 30 Sep 2026 |

## Facts file

`research/what-gets-adopted-facts.csv` has one row per figure in this report (199 rows): figure, qualifier, unit, description, the date it refers to, label, URL, case ID, who measured it, how the source was read, and the report section. Its labels are stricter than the row labels in §4: **observed** is kept for figures this thread counted or read in the system of record or governing document (ledger, ordinance, official notice, live counter, API); a result or usage figure that a source asserts is **reported** even when the page was read raw; model outputs are **estimated**; this thread's derivations are **inferred**. Six rows rest on search summaries only and are marked UNVERIFIED.

## Negative results and limits

- **Blocked to curl (HTTP 403):** codeforamerica.org, cacm.acm.org, cdc.gov/mmwr, oaklandca.gov, sanjoseca.gov, pittsburghpa.gov, alleghenycounty.us, datasmart.hks.harvard.edu, bloombergcities.jhu.edu, whatworkscities.bloomberg.org, transportation.gov, esri.com, theatlantic.com, nrdc.org, muckrock.com. The Wayback Machine returned 429 on most fallback attempts.
- **mySociety sites** (fixmystreet.com, societyworks.org) returned a maintenance page throughout the search; FixMyStreet figures are search summaries only.
- **Not researched (search budget ran out on 13 Oct):** outsider-built graffiti and illegal-dumping tools; Graffiti Tracker and similar; UMSL criminology work with police; St. Louis Fed tools; corporate pro bono beyond one firm; most national programmes other than Bloomberg and Rockefeller.
- **Looked for and not found:** a civic-hackathon survival rate; a deployment rate for Data Science for Social Good projects; the NYC "13% to 70%" vacate-order figure in the primary source read; a fire-death outcome for New Orleans; stated reasons for the end of BlightStatus, Honolulu Answers, Adopt-a-Hydrant Boston, OpenTreeMap, Motor City Mapping, YourSTLCourts, OpenSTL and GlobalHack.
- **Source discrepancies kept:** Street Bump castings four times (city) or eight times (Boston Globe) as common as potholes; Motor City Mapping parcel counts of 370,000+, 378,723 and 380,000; who built Citizens Connect (city page names Connected Bits; two trade sources name SeeClickFix); when CDC changed wastewater vendor (July or September 2023).
- **Corrected 14 Oct 2026:** §1.4 gave Memphis residents' share of potholes as "10–20%". The sources give 20% (Route Fifty, 2020) and 10–15% (StateTech, 2024); the line now says so.
- **Superseded within the part files:** `E-outsider.d/themes.md` records Memphis as unconfirmed after December 2024; `E-precedents-analytics.md` N26 later read February 2025 and January 2026 reports. The later reading is used here.
- **Sample limits:** cases were found by search, not sampled. Successes are over-documented by their owners. Counts in this file describe this sample only.

## Open items for one more pass

1. How the tornado trackers were commissioned: Board of Estimate and Apportionment minutes, the City contract portal and FY2027 expenditure data were not searched.
2. The surveillance ordinance's definition; the Technology Procurement Policy attachment; a city source for the GeoSTL work and for the innovation team's funding (`E-stl-city-it.md` §6).
3. Current (2025–26) status of adopted analytics cases outside Boston and Chicago.
4. Graffiti and dumping tools built by outsiders.
