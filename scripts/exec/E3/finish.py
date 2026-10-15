"""E3: record the site-level choices and write the facts table for research/chapters/E3-demo.md.

    .venv/bin/python -I scripts/exec/E3/finish.py

Writes (upserts) build/E3/decisions.json and writes build/E3/E3-demo-facts.csv (figure, value, unit, period, label, url),
one row per e3_* figure. The facts CSV sits in build/E3/ because this thread may write only one file under research/.
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, 'build', 'E3')

SITE = [
    {'id': 'e3-landing-lead', 'decision': "The landing leads with 'The city grades the hand-off, not the job.' and the CityStat alley-debris pair (78.6% as published; 15.0% done on time), with the hand-off share and the queue count as support. The closure mix bar is turned off.",
     'why': 'The brief fixed the headline and the pair; the pair is the strongest observed claim in the assessment (section 3). The mix bar repeated the 35% support figure and pushed the doors below the fold at 1920x1080.',
     'alternative_rejected': 'Keeping "Closed is not done" and the 35% hero (the 35% invites the forbidden reading "35% of jobs are not done").'},
    {'id': 'e3-pair-figure', 'decision': 'The lead pair is one registered figure with a two-part value {published, done_only, rebuilt}, plus scalar e3_citystat_* figures for each measure.',
     'why': 'The page asks for one figure id per lead; the two numbers must travel together with one derivation.',
     'alternative_rejected': 'Two unrelated lead figures.'},
    {'id': 'e3-done-column-goal', 'decision': "The added CityStat column ('Done on time') uses CityStat's own goal and denominator, counting only closings whose words say done; for parks, R1's closed-only grading against each request's promise date.",
     'why': "It changes one thing in CityStat's own test, so the gap is the closing words and nothing else. The city's promise date differs from the CityStat goal for some types (alley potholes 16 vs 17 days).",
     'alternative_rejected': "Grading CityStat's measures against PRJCOMPLETEDATE (changes two things at once)."},
    {'id': 'e3-q3-table-only', 'decision': 'The July-September pothole callout is removed from the landing and the brief; Q3 2026 appears only as a column in the scoreboard table, and the quarter-by-quarter chart stops at the last published quarter.',
     'why': 'Brief instruction; the callout carried the old lead and competed with the thesis.',
     'alternative_rejected': 'Keeping the callout below the fold.'},
    {'id': 'e3-fairness-appendix', 'decision': "Fairness moved, unchanged, to the methods page as 'Appendix: A separate finding: first-step waits by ward' (site/js/fairness.js holds the same render code).",
     'why': 'It is a separate finding with no tested cause; the assessment bars any equity claim from the main story.',
     'alternative_rejected': 'Deleting it (it is evidence and was asked about) or rewriting it (brief: unchanged in content).'},
    {'id': 'e3-nav-doors', 'decision': "Every page's nav carries three doors: For residents, The queue, For the CityStat team. The Monday brief left the nav and is linked from the methods page as 'The printable Monday brief'.",
     'why': 'Brief instruction; the three doors match the three surfaces.',
     'alternative_rejected': 'Keeping in-page anchors in the nav (seven items, the queue would not stand out).'},
    {'id': 'e3-register-attached', 'decision': "The register gains a sixth column, 'Work orders attached (public status page)', read at build time from E1's build/E1/linkage_by_service.csv: yes at 80% or more of sampled pages, partly at 20-79%, no below 20% (the count is in the hover text); services E1 has not sampled read 'not yet tested'.",
     'why': "E1's sample was still growing during this build, so the bridge reads whatever exists when it runs and never types a value.",
     'alternative_rejected': 'Copying E1 figures into the register by hand (would go stale).'},
    {'id': 'e3-statuspage-reconstruction-style', 'decision': "The status page is drawn in a neutral navy frame labelled 'Reconstruction' or 'Proposed', with the City's field names and wording, the block instead of the address and the request number withheld; no City logo or branding.",
     'why': 'It must read as the City page to make the point, without impersonating it.',
     'alternative_rejected': 'A screenshot of the live page (shows the address and number).'},
    {'id': 'e3-download-sizes', 'decision': 'Download sizes in data/downloads.json are stored in KB, not bytes.',
     'why': "The privacy scan flagged queue.csv's byte count because it equals a real request number (a false positive, but the gate is strict).",
     'alternative_rejected': 'Adding an allowlist to the scan (it has none on purpose).'},
]

p = os.path.join(OUT, 'decisions.json')
old = json.load(open(p)).get('decisions', []) if os.path.exists(p) else []
ids = {d['id'] for d in SITE}
with open(p, 'w') as f:
    json.dump({'decisions': [d for d in old if d['id'] not in ids] + [dict(d, owner='E3') for d in SITE]}, f, indent=1)

CSB = 'https://www.stlouis-mo.gov/data/upload/data-files/csb.zip'
QE = 'https://service.stlouis-mo.gov/cityworks/gis/1/1/rest/services/qe/FeatureServer/18'
CITYSTAT = 'https://www.stlouis-mo.gov/citystat/'
STATUS = 'https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/check-service-request.cfm'


def url(fid):
    if fid.startswith('e3_queue_qe'):
        return QE
    if fid.startswith('e3_status_probe'):
        return STATUS + ' (saved pages; build/E1/probe_summary.json)'
    if fid.startswith('e3_status'):
        return STATUS + ' (saved copy)'
    if fid.startswith('e3_citystat') and fid.endswith('_published'):
        return CITYSTAT
    if fid.startswith('e3_citystat'):
        return f'{CSB} and {CITYSTAT}'
    return CSB


figs = json.load(open(os.path.join(OUT, 'figures.json')))['figures']
with open(os.path.join(OUT, 'E3-demo-facts.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['id', 'figure', 'value', 'unit', 'date_it_refers_to', 'label', 'url'])
    for x in figs:
        v = json.dumps(x['value']) if isinstance(x['value'], dict) else x['value']
        w.writerow([x['id'], x['definition'], v, x['unit'], x['period'], x['label'], url(x['id'])])
print(len(SITE), 'site decisions;', len(figs), 'facts rows')
