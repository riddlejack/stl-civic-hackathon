"""Rule-based tagger for the merged attention items.

Categories were derived from the material (two topic-model passes plus a read sample; see
research/attention-over-time.md section 2), then written as keyword rules so the tagging is
transparent and repeatable. An item can carry several issue tags.

Usage: python3 -I tag.py <items.jsonl> <tagged.jsonl>
"""
import collections
import json
import re
import sys

F = re.I

ISSUES = collections.OrderedDict([
    ("tornado_recovery", (r"tornado|\bfema\b|storm debris|debris (removal|pickup|cleanup)|disaster (relief|recovery|assistance|declaration)|storm (relief|victims|recovery|survivors)", r"tornado (watch|warning)s?\b(?!.*(recover|victim|damage|relief|siren))")),
    ("violent_crime", (r"\bshot\b|shooting|homicide|murder|stabb|carjack|gunfire|gun violence|shots fired|gunman|violent crime|domestic violence|fatally|\bslain\b|crime (rate|stats|statistic|numbers|wave|data)|killed in (a )?(drive|double|triple)", r"photo ?shoot|shot (put|clock)|flu shot|vaccine|shot at the|long shot|big shot|shot glass")),
    ("property_crime", (r"\bstealing\b|\bstole\b|\btheft|thieves|burglariz|robber(y|ies)|\brobbed\b|break[- ]ins?|burglar|car thef|stolen (car|vehicle|kia|hyundai)|auto theft|catalytic|porch pirate|package thef|shoplift|smash[- ]and[- ]grab|looting|copper thef|kia boys|theft ring|car prowl", None)),
    ("policing", (r"state (control|takeover|board)|police board|board of police|police control|local control|police (chief|commissioner|budget|staffing|shortage|overtime|recruit|accountab|oversight|misconduct|pursuit|chase|reform|union|contract|pay|response|substation|camera|surveillance|drone)|officers? (charged|fired|suspended|indicted|sued|acquitted|cleared|will not face)|justice assistance grant|chief (robert )?tracy|civilian oversight|officer[- ]involved|shot by (police|officer)|police (shooting|brutality|killing)|use of force|flock camera|license plate reader|shotspotter|cops? (charged|fired)", None)),
    ("jail_sheriff", (r"sheriff|city justice center|\bcjc\b|workhouse|\bjails?\b|jailed|detainee|corrections (commissioner|division)", None)),
    ("schools_slps", (r"\bslps\b|st\.? ?louis public schools|school (closure|closing|consolidation)s?|schools? (to|will|could|may) clos|superintendent|school board|school bus|borishade|charter school|school (transportation|enrollment|budget|audit)", None)),
    ("data_centers", (r"data cent(er|re)s?", None)),
    ("winter_storm_snow_removal", (r"\bsnow|sleet|\bicy\b|ice storm|winter storm|winter weather|\bplow|freezing rain|side streets|salt (truck|the |supply)|black ice|unplowed", r"snow ?cone|snow white")),
    ("flood_heat_storms", (r"flood|heat (wave|advisory|warning|index|dome)|excessive heat|extreme heat|heatwave|cooling (center|site|station)|severe (storm|weather|thunderstorm)|thunderstorm|\bhail\b|derecho|straight[- ]line winds|storm damage", None)),
    ("water_sewer", (r"water main|boil (water )?(advisory|order)|water (bill|rate|pressure|division|department|shutoff|shut-off|service|system|quality|outage)|lead (pipe|line|service line)s?|\bsewer|\bmsd\b|sinkhole|hydrant|stormwater|drinking water|fluorid|brown water|no water", None)),
    ("city_budget_taxes", (r"earnings tax|rams (settlement|money|funds)|settlement (money|funds|proceeds)|city budget|budget (deficit|shortfall|cuts|hearing|gap|proposal)|board of estimate|comptroller|property tax|sales tax|use tax|bond issue|\barpa\b|tax (increase|hike|abatement|incentive|break)|reassessment|pension|pay bill|city annual budget|appropriation", None)),
    ("traffic_safety", (r"pedestrian|cyclist|bicyclist|bike lane|hit[- ]and[- ]run|traffic (calming|violence|death|fatalit|enforcement|camera|signal|light|safety|stop)s?|speed (hump|bump|camera|limit|table)s?|red[- ]light|reckless driv|street racing|drag racing|speeding|\bcrash|wrong[- ]way|vision zero|complete streets|crosswalk|stop signs?|expired (temp )?tags|temp tags|sideshow|run(s|ning)? red|dangerous intersection|road rage|drunk driv|\bdwi\b|overturned|rollover|rolled over|head-on|collision|(struck|hit) by (a |an )?(car|vehicle|truck|suv|driver)|chang(e|ing) lanes|bad drivers", r"market crash|crash course|computer crash|crash pad")),
    ("streets_sidewalks_lights", (r"pothole|repav|resurfac|pavement|cave[- ]in|\bmodot\b|\bidot\b|road (conditions?|work|repairs?|closures?|closed|construction)|street (repairs?|conditions?|closures?|closed|paving|maintenance|lights?|sweeping|cleaning)|streetlights?|sidewalk|bridge (closure|closed|repair|replacement|inspection)|lights? (are |is )?(out|not working)|steel plates?|lane closures?|lanes? (closed|blocked)|\bcones\b|roads? (are|is) (terrible|awful|bad|trash)|crumbling (road|street|infrastructure)", None)),
    ("parking_towing", (r"parking (meter|ticket|enforcement|garage|rate|fine|district|permit|ban|minimum|fee|lot fee|app)s?|\bbooted\b|\btowed\b|tow lot|towing|parking (in|on) the (bike|side)|illegal(ly)? park", None)),
    ("vacant_derelict_buildings", (r"vacant|abandoned (building|house|home|propert|church|school|hospital|factory)|derelict|\bblight|demolition|demolish|condemned|\blra\b|land reutilization|land bank|board(ed|ing|s)?[- ]up|nuisance propert|problem propert|railway exchange|code enforcement|building (collapse|inspector|division|code)|\bcollapse[ds]?\b|squatter|slumlord|unsafe building|eyesore|crumbling building", r"vacant (seat|position|post|job)|vacanc(y|ies) on")),
    ("housing_tenants", (r"evict|tenant|landlord|rent (increase|hike|relief|control|assistance|prices)|rents (are|rise|rising)|affordable housing|housing (crisis|authority|trust|voucher|shortage|market|cost|discrimination|assistance)|section 8|short[- ]term rental|airbnb|public housing|apartments? (condemned|without|residents|complex (fire|condemned))|no heat|\bhud\b|rental (registry|license|inspection)|habitab|home repair|mortgage|foreclos|zoning code|minimum lot size|accessory dwelling", None)),
    ("homelessness", (r"homeless|unhoused|encampment|warming (center|shelter|site)|emergency shelters?|shelter beds|overnight shelter|panhandl|tent city|tiny homes?", None)),
    ("trash_dumping", (r"\btrash\b|garbage|\brefuse\b|dumpster|illegal dump|\bdumping|dumper|recycling|\blitter|bulk pickup|yard waste|tire dump|roll carts?", r"trash talk|refuse to|refuses|refused")),
    ("trees_overgrowth", (r"\btrees?\b|forestry|tree (limb|trimming|planting|removal|canopy)|\bstump|overgrown|\bweeds\b|(tall|high) grass|\bmowing|vacant lots?|uncut|bradford pear|emerald ash", r"christmas tree|family tree|tree lighting|dollar tree|money tree")),
    ("parks_rec", (r"parks? (department|division|maintenance|bathroom|restroom|ranger|funding|improvement|renovation|closed|closure|damage|cleanup|safety|board|master plan)|playground|rec(reation)? centers?|public pools?|city pools?|splash pad|forest park (forever|damage|recovery)|park (shooting|curfew)|city parks", None)),
    ("transit", (r"metrolink|metrobus|metro transit|bi-state|green line|bus (route|service|stop|riders|driver|rapid)s?|light rail|public transit|public transportation|\btransit\b|call-a-ride|streetcar|loop trolley|amtrak|high[- ]speed rail", None)),
    ("airport", (r"lambert|\bairport", None)),
    ("downtown", (r"downtown.*(vacan|office|safety|crime|hotel|millennium|at&t|railway exchange|convention|dome|peabody|leav|closing|closes|revitaliz|resident|cleanup|ambassador|\bcid\b|future|decline|empty|struggl|problem|plan|development|investment|business)|(vacan|office|safety|crime|hotel|millennium|at&t|convention|peabody|leav|closing|closes|revitaliz|decline|empty|struggl|development|investment|business).*downtown|greater st\.? louis inc|convention center|at&t tower|millennium hotel|america'?s center|\bthe dome\b|dome and convention", None)),
    ("development_incentives", (r"\bsldc\b|st\.? louis development corp|development proposals?|new (apartments|development|construction)|apartments? (planned|proposed)|tax increment|\btif\b|redevelop|development (agreement|plan|incentive|project)|developer|community improvement district|rezon|\bnga\b|paul mckee|land clearance|northside (grant|economic)|economic (justice|development)|ground ?breaking|\$[\d.]+ ?(m|million|b|billion) (project|development|investment|plan)", None)),
    ("immigration_enforcement", (r"\bice\b (agent|arrest|raid|detain|detention|deport|facility|activity|sighting|officer|enforcement|presence|out|protest)s?|protest.{0,40}\bice\b|anti-ice|\bice\b.*(immigra|detain|deport|agents)|immigration|deport|immigrant|refugee|asylum|border patrol|sanctuary", r"ice (cream|rink|skating|storm|hockey)")),
    ("public_health", (r"measles|outbreak|e\.? ?coli|salmonella|legionnaire|overdose|fentanyl|opioid|covid|norovirus|health (department|director|commissioner)|hospital (clos|cut|layoff)|mental health|lead poison|air quality|ozone|asthma|food (desert|insecurity|pantry|bank|assistance)|\bsnap\b|medicaid|maternal|infant mortality|\bhiv\b|vaccin|west nile|rabies|health care desert|radioactive|coldwater creek|pollution|contaminat", None)),
    ("utilities_power", (r"ameren|\bspire\b|utilities (disconnect|shut)|disconnect(ion)?s?\b|power outages?|without power|lost power|electric (bill|rate)s?|gas (bill|leak)s?|utility (bill|shutoff|assistance|rate)s?|energy assistance|liheap|broadband|internet (outage|access|service)", None)),
    ("animal_control", (r"stray rescue|animal rescue|stray (dog|cat|animal)s?|animal (control|shelter|abuse|cruelty|care|neglect)|care stl|dog (attack|bite|mauling|fighting)s?|loose dogs?|pit ?bulls? attack|feral|dogs? (rescued|seized|abandoned|dumped)|dumped (dog|puppy|puppies|cat)", None)),
    ("emergency_services", (r"\b911\b|dispatcher|911 dispatch|dispatch (center|times?|delays?)|\bems\b|ambulance|response times?|fire (department|chief|station|truck|engine)|firefighter|sirens?\b|\bcema\b|emergency management|paramedic", r"blues sirens")),
    ("fires", (r"\bfires?\b|\bblaze|house fire|on fire|burn(ed|ing) (building|house|home)|arson", r"fire(d|s)? (from|by|the|his|her|coach|manager)|\bfired\b|fire department|firefighter|fire chief|fire station|firework|fire hydrant|under fire|cease")),
    ("graffiti_vandalism", (r"graffiti|vandal|spray[- ]paint|defaced|tagged (with|by)", None)),
    ("city_services_workforce", (r"citizens'? service bureau|\bcsb\b|\b311\b|city (workers?|employees?|services|hiring|jobs|personnel|workforce|departments?|staffing|vacancies|website|permits?)|civil service|personnel (department|director)|permit(s|ting)? (delay|backlog|office|process|system)|building permits?|residency requirement|streets? department|refuse division|city hall (hours|closed|service|hiring)|hr chief|human resources (director|department)", None)),
    ("noise_fireworks_nuisance", (r"fireworks|noise (complaint|ordinance|pollution)|loud (music|cars?|exhaust|boom|bang|noise)|dirt bikes?|\batvs?\b|what was that (boom|noise|sound)|explosion sound|boom (just|heard)", r"fireworks (show|display|celebration|schedule|guide|events?)|4th of july fireworks|fair st")),
])

CITY_GOV = re.compile(r"\bmayor|alderm[ae]n|alderwoman|alderperson|aldermanic|city hall|mayoral|megan green|cara spencer|tishaura|\bward \d|\d+(st|nd|rd|th) ward|charter (commission|change|amendment|reform)|city counselor|circuit attorney|gabe gore|recorder of deeds|license collector|city treasurer|city of st\.? ?louis", F)

NEIGH = r"soulard|dutchtown|tower grove|the grove|central west end|\bcwe\b|the ville|\bbaden\b|carondelet|hyde park|old north|lafayette square|benton park|fox park|\bbevo\b|the hill\b|dogtown|midtown|penrose|walnut park|wells[- ]goodfellow|fountain park|kingsway|o'?fallon park|college hill|jeff[- ]?vander[- ]?lou|covenant blu|grand center|forest park|skinker|debaliviere|hamilton heights|gravois park|marine villa|holly hills|st\.? ?louis hills|lindenwood park|southampton|north hampton|princeton heights|boulevard heights|clifton heights|botanical heights|mckinley heights|compton heights|downtown west|columbus square|carr square|fairground park|greater ville|kingshighway|natural bridge|cherokee street|south grand|washington ave|laclede'?s landing|city museum|union station|enterprise center|busch stadium|lambert|america'?s center|gateway arch|riverfront|north riverfront|academy neighborhood|west end neighborhood|the patch|shaw neighborhood|tower grove park"
CITY = re.compile(r"(?<!east )(?<!e\. )(?<!e )st\.? ?louis(?!['’]?s? ?[- ]?(county|co\b|area|region|cardinals|blues|city sc|battlehawks|university|zoo|public radio|post[- ]dispatch|american\b|magazine|business journal))|\bstl\b(?! ?(county|area))|city of st\.? ?louis|city hall|alderm|aldermanic|slmpd|\bslps\b|north city|south city|downtown|city justice center|" + NEIGH, F)
ELSE = re.compile(r"st\.? ?louis (county|co\b)|\bcounty (police|council|executive|jail|health|prosecutor|library)|north county|south county|west county|st\.? ?charles|jefferson county|franklin county|lincoln county|warren county|metro[- ]east|illinois|\bill\.|east st\.? ?louis|belleville|\balton\b|granite city|collinsville|edwardsville|o'?fallon,? (mo|ill|missouri|illinois)|cahokia|madison county|st\.? ?clair|ferguson|florissant(?! ave)|hazelwood|kirkwood|webster groves|\bclayton\b(?! ave| road)|university city|\bu\.? ?city\b|maplewood|brentwood|chesterfield|ballwin|\bfenton|\barnold\b|festus|wentzville|st\.? ?peters|bridgeton|maryland heights|creve coeur|\bladue|\boverland\b|jennings|\bberkeley|pagedale|pine lawn|wellston|normandy|spanish lake|affton|\blemay\b|mehlville|oakville|\beureka\b|wildwood|des peres|town and country|crestwood|sunset hills|shrewsbury|richmond heights|olivette|st\.? ?ann\b|black jack|bellefontaine|dellwood|moline acres|kinloch|valley park|ellisville|warrenton|de soto|hillsboro|kansas city|jefferson city|cape girardeau|joplin|branson|lake of the ozarks|ozarks|\brolla\b|sedalia|southwest missouri|southeast missouri|mid-missouri|missouri (house|senate|legislat|lawmakers|supreme court|governor|attorney general|secretary of state|voters|highway patrol|state)|\bmo\.? (house|senate|legislat|lawmakers)|kehoe|statewide|\bmshp\b|highway patrol|congress|\btrump\b|white house|rockwood|parkway school|francis howell|riverview gardens|\bmizzou\b|chiefs", F)

KIND_RULES = [
    ("praise", re.compile(r"thank you|thanks to|shout ?out|kudos|great job|good job|appreciat|love (my|this|our) (city|neighborhood)|hats off|well done|\bpraise|celebrat|honor(ed|s)?\b|award", F)),
    ("complaint", re.compile(r"residents (say|want|demand|frustrat|complain|upset|fed up|angry|worr|concern|question|still)|neighbors (say|want|demand|frustrat|complain|upset|fed up|worr|concern)|frustrat|fed up|complain|concerns?\b|outrage|criticiz|critics|slam|blast|\bsues?\b|lawsuit|protest|demand|still (waiting|no|not|without|closed|broken)|eyesore|problem|fail(s|ed|ure|ing)?\b|broken|delay|backlash|why (is|are|does|do|can't|cant|hasn't|won't)|wtf|sick of|tired of|terrible|awful|worst|ridiculous|a joke|embarrass|unacceptable|rant|what the hell|out of control|ignored|neglect|no one (is|cares)|nobody (is|cares)|anyone else (notice|annoyed|having)|\bpsa\b|beware|warning:|scam", F)),
    ("incident", re.compile(r"\bshot\b|shooting|killed|dies|dead|death|crash|struck|\bfires?\b|blaze|collapse|break\b|breaks\b|outage|injured|stabb|carjack|robbed|stolen|arrest|charged|sentenced|pleads|convicted|indicted|found guilty|missing|evacuat|closed after|damage[ds]?\b|hits\b|\bhit\b|tornado (hits|tears|touches|damage)|storm (hits|damage)|flooding (hits|closes)|power out|without power|explosion|standoff|pursuit|chase", F)),
    ("announcement", re.compile(r"announc|declar|forms?\b|requir|hearing|install|authoriz|directs|to hire|to open|opens\b|opening|launch|approv|passes|passed|signs\b|signed|unveil|propos|plans?\b|\bset to\b|will (begin|start|open|close|hold|host|vote|consider)|introduc|awarded|awards \$|receives?|grant|funding|budget|appoint|names\b|named|hires|sworn|elect|vote[sd]?\b|ordinance|\bbill\b|begins|starts|schedule|deadline|how to|apply|available|expands?|reopen|new program|program|initiative|releases?|report (shows|finds)", F)),
]


def issues_for(text):
    tags = []
    for name, (inc, exc) in COMPILED.items():
        if inc.search(text) and not (exc and exc.search(text)):
            tags.append(name)
    return tags


def scope_for(row, text):
    if row["source_kind"] == "legislative":
        return "city"
    if CITY.search(text):
        return "city"
    if ELSE.search(text):
        return "elsewhere"
    return "unstated"


def kind_for(row, text):
    if row["source_kind"] == "legislative":
        return "announcement"
    for name, rx in KIND_RULES:
        if rx.search(text):
            return name
    return "other"


COMPILED = collections.OrderedDict((k, (re.compile(v[0], F), re.compile(v[1], F) if v[1] else None)) for k, v in ISSUES.items())


def tag_row(row):
    text = (row["title"] + " . " + row.get("snippet", "")).replace("’", "'")
    tags = issues_for(text)
    if not tags and CITY_GOV.search(text):
        tags = ["city_government_general"]
    row["issues"] = tags
    row["scope"] = scope_for(row, text)
    row["mention_kind"] = kind_for(row, text)
    return row


if __name__ == "__main__":
    n = 0
    c = collections.Counter()
    with open(sys.argv[2], "w", encoding="utf-8") as out:
        for line in open(sys.argv[1], encoding="utf-8"):
            r = tag_row(json.loads(line))
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
            c[(r["source_kind"], bool(r["issues"]), r["scope"])] += 1
    print("tagged", n)
    for k, v in sorted(c.items()):
        print(k, v)
