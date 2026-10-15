"""Closure classes for N3.

If research/chapters/N2-closure-classes.csv exists (columns PROBLEMCODE, resolution_text, class, n,
rule_or_judgement), it is used: class looked up by (PROBLEMCODE, resolution_text), falling back to the
class N2 gave the same text most often for other types, then to the N3 first-pass rules below.
Otherwise the N3 first-pass rules are used and results are marked provisional.

N3 first-pass classes (my judgement, 13 Oct 2026; reviewable, one line per text):
  done        the closing text says the work was done (work completed, collection made, repairs made, towed)
  handed_off  scheduled, referred, queued, tagged, "will be", sent to another agency or division
  converted   a work order was created
  no_action   no violation / no problem / gone on inspection / not city property / unable to locate
  enforcement notice, ticket, summons, warning: the city acted; the fix is the owner's
              (reported inside handed_off when an N2-compatible class is needed)
  info_other  call for details, citizen contacted, investigation complete, permits
  blank       no closing text
"""
import csv, os, re
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
N2_PATH = os.path.join(ROOT, 'research/chapters/N2-closure-classes.csv')

def key(s):
    return re.sub(r'\s+', ' ', (s or '').strip().lower())

DONE = """work completed|collection made|container(s) replaced with new|container maintenance completed|animal(s) picked up
graffiti removed painted|graffiti removed power washed|graffiti removed painted and power washed|graffiti removed
container(s) placed|complete|repairs made|uprighted container|animal picked up|services completed|container moved
container removed|repairs completed|trash/litter/debris removed|grass cut|vehicle towed|removed and made safe
park maintenance complete|treated with rodentcide|bulk/debris items have been collected
trash/debris was cleaned in area and collection made|meter repaired|building was secured by city
building was re-secured by city|education and tnr completed|container was overloaded and had to be collected by special truck
hydrant cap replaced|hydrant maintenance complete|lead inspection completed|siren repaired|collection made by private hauler
asphalted|street maintenance work completed|treated with larvicide|treated with adulticide|stop box shut
teehead shut - owner to be billed|apprehended animal|destroy tap/service|work has complied with requested change"""
CONVERTED = """removal work order created|trim work order created|work order created"""
HANDED = """collection will be made next scheduled day|due to employee shortage, the routes will be completed in order, as soon possible
matter will be investigated and appropriate action taken|on schedule to be cut, call csb for details|vehicle tagged for tow
scheduled for repair by water department|work in progress|referred to board up crew|bulk will be picked up in correct week
approved for next available planting|added to rotation|referred to street maintenance for repair work to be scheduled
supervisor notified|report to modot|refer to street inspector for evaluation|added to sewer lateral repair program
repair work scheduled|sent to field|your street painting request has been evaluated and will be included in our seasonal striping plan.
referred to forestry|maintenance supervisor notified|reported to msd|not funded by traffic division, seeking outside funding support
on-going project, under construction by others|referred to proper department|matter is being investigated and appropriate action will be taken
on schedule to be cut, call forestry for details|vehicle not derelict, refer to treasurer for ticketing|work ticket issued to crew
major capital improvement project|contractor responsible has been notified to make repairs|repairs scheduled|parts on order
referred to water division|grass on schedule to be cut|referred to msd|responsibility of ameren ue|timing is under study
aldermanic funding support|already on sidewalk program|referred to trash task force|trash on schedule for pickup
referred to building division|no leaks detected - referred to street division for repair|referred to refuse division
sent to street maintenance for repair|work still in process|referred to traffic division
accident report has been forwarded to city counselor's office|extension given|referred to laclede gas
work being performed by board of public service|teehead leaking - scheduled for repair|sign on order|location added to sidewalk program
work being performed by msd|work being performed by water dept|sent to parking enforcement|turned over to insurance company
referred to community sanitation|referred to parks|work being performed by modot|waiting for parts
working with property owner - extension given|sent to sewer lateral program for inspection|reported to ameren|referred to modot
work being performed by laclede gas|refer to street division for repair|contact slmpd|work being performed by property owner
telecom responsible has been notified|referred to charter communications|will adjust timing|ameren signal outage|reported to modot
referred to court|aldermanic approval needed|building was occupied, will need police|camera request|violation notice under appeal
collection will be made;problem items removed from container|yard waste now on winter schedule"""
ENFORCE = """issued notice of violation|building already under notice|already under notice|confirmed violation, owner notified
summons issued|owner notified|secure notice sent|vehicle ticketed|re-instructional/ warning letter sent|issued fine
verbal re-instructional/ warning given|stop work order issued|instructional letter issued as a warning
letter sent to resident to verify status|violation issued to private hauler/owner|verbal advice given|given verbal advice
instructions issued to customer|cleared by arrest - illegal dumping|cleared by arrest - container violation
cleared by arrest - illegal dumping & container violation|cleared by arrest|cleared by arrest - accumulation of rubbish
cleared by arrest - no commercial container|stolen/police notified"""
NOACT = """vehicle gone upon inspection|no problem found|no forestry violations|no evidence of violation|no service necessary
patrolled area, no strays observed|no vehicle found|container sits in the proper space|meets minimum standards
inspector unable to gain access|unable to confirm violation|abated before inspection|no response at premise
citizen's responsibility to clean up trash|no response required at this time|vehicle gone upon reinspection
proper number of containers in alley|abated at time of inspection|container not blocking|not enough evidence to lead to arrest
not city property|no service to tree(s) necessary|canceled|owner's responsibility|citizen will need plumber to make repairs
animal not found|no jurisdiction|no leaks detected|animal(s) appear healthy|vehicle not derelict, no cause for complaint
no such address|permit found and current|shelter full, unable to accept animals|not responsibility of parks department
no violation found|no appropriate planting site|property not eligible for sidewalk program|no cause for complaint
no such address/incorrect address|secured at time of inspection|vehicle repaired upon reinspection
chased stray, unable to apprehend, will continue to monitor area|unable to remove, too high, no access or too dangerous
no witness(es)|no permit required|no water surfacing at time of inspection|unable to substantiate this claim|no graffiti found
vacant property|no evidence to lead to an arrest|animal(s) current on vaccination/registration
inspection not permitted by owner/occupant|restrooms closed|complaint unfounded|lead inspection not permitted|no lead hazards found
caller is not the witness|fountains closed|witness(es) refuses to assist in prosecution|wrong address|alderman did not provide funds
vendor is legal|block is on a "no mosquito spraying" list|added to no spray list|staff is unable to fulfill this request at this time
siren inspected and found operational, citizen may not hear siren when indoors|irrigation off|no access to roll-out container
incorrect information provided|see corrected address|completed by owner|need customer to provide exact address|need more info
more information needed|citizen contacted - appeal denied|permit denied|unable to contact citizen"""
INFO = """please call csb for details|citizen contacted|investigation complete|see lra comments|see sr comments
request investigated, please call nso for details|request investigated, please call for details|other - call csb for details
staff is addressing this concern, please call for details|citizen contacted - no response, left message|permit approved
permit issued|disseminated air pollution guidelines|recycling info sent|sent holiday schedule|need permit|restrooms open"""

RULES = {}
for cls, block in [('done', DONE), ('converted', CONVERTED), ('handed_off', HANDED), ('enforcement', ENFORCE),
                   ('no_action', NOACT), ('info_other', INFO)]:
    for line in block.split('\n'):
        for t in line.split('|'):
            t = key(t)
            if t: RULES[t] = cls

def first_pass(text):
    k = key(text)
    if not k: return 'blank'
    if k in RULES: return RULES[k]
    if k.startswith('more information is needed'): return 'no_action'
    if k.startswith('investigations complete'): return 'info_other'
    if 'work order created' in k: return 'converted'
    if re.search(r'\b(referred|refer|scheduled|will be|sent to|reported to|forwarded|on order)\b', k): return 'handed_off'
    if re.search(r'\b(no |not |unable|gone upon)', k): return 'no_action'
    if re.search(r'\b(completed|removed|repaired|collected|replaced)\b', k): return 'done'
    return 'unclassed'

def load_n2():
    """Returns (by_type_text, by_text) dicts from N2's CSV, or None if absent."""
    if not os.path.exists(N2_PATH): return None
    by_tt, votes = {}, {}
    with open(N2_PATH, newline='', encoding='utf-8', errors='replace') as fh:
        for r in csv.DictReader(fh):
            pt = (r.get('PROBLEMCODE') or '').strip(); tx = key(r.get('resolution_text')); cl = (r.get('class') or '').strip()
            try: n = int(float(r.get('n') or 0))
            except ValueError: n = 0
            by_tt[(pt, tx)] = cl
            votes.setdefault(tx, {}).setdefault(cl, 0); votes[tx][cl] += n
    by_text = {tx: max(v.items(), key=lambda kv: kv[1])[0] for tx, v in votes.items()}
    return by_tt, by_text

def classifier():
    """Returns (fn(ptype, text) -> class, source label)."""
    n2 = load_n2()
    if n2 is None:
        return (lambda pt, tx: first_pass(tx)), 'N3 first-pass rules (provisional; N2 file absent)'
    by_tt, by_text = n2
    def f(pt, tx):
        k = key(tx)
        c = by_tt.get(((pt or '').strip(), k))
        if c: return c
        if not k: return 'blank'
        return by_text.get(k) or first_pass(tx)
    return f, 'N2 closure classes (research/chapters/N2-closure-classes.csv), N3 rules where N2 has no row'
