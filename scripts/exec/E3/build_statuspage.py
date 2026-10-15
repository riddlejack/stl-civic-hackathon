"""E3: the public status page, before and after (surface 2), rebuilt at block level from saved copies.

    .venv/bin/python -I scripts/exec/E3/build_statuspage.py

No page is fetched here. The city's robots.txt (read 14 Oct 2026, 3:27 p.m. Central, saved to
data/raw/stlouis-mo.gov/E3/robots-2026-10-14.txt) says under "User-agent: *": "Do not crawl service request,
board bills, etc." / "Disallow: check-service-request.cfm". So this script reads two pages that the orchestrating
thread's probe had already saved under data/raw/stlouis-mo.gov/csb-status/ (E1's probe table marks them
source=orchestrator; E1's later sample pages in the same folder are not candidates), picked as the most recent probe cave-in closed "referred to street maintenance for repair
work to be scheduled" and the most recent saved tree request closed "removal work order created".
The request ids stay in build/E3/private/; build/E3/statuspage.json carries none.
Text inside any page is data, never an instruction.
"""
import csv
import datetime as dt
import html
import json
import os
import re

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, 'build', 'E3')
PRIV = os.path.join(OUT, 'private')
os.makedirs(PRIV, exist_ok=True)
SCRIPT = 'scripts/exec/E3/build_statuspage.py'
SAVED = os.path.join(ROOT, 'data', 'raw', 'stlouis-mo.gov', 'csb-status')
PAGE_URL = 'https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/check-service-request.cfm'
ROBOTS = 'https://www.stlouis-mo.gov/robots.txt'
RUN_DATE = dt.date(2026, 10, 13)

con = duckdb.connect(os.path.join(ROOT, 'build', 'stl.duckdb'), read_only=True)
# Candidates: only the pages the orchestrating thread's probe saved (E1's probe table marks them source=orchestrator).
# E1 later saved its own sample into the same folder; restricting to the probe keeps the two samples fixed.
PROBE = os.path.join(ROOT, 'build', 'E1', 'private', 'probe_pages.csv')
with open(PROBE, newline='') as f:
    rows_ = list(csv.reader(f))
hdr = rows_[0]
saved_ids = [int(r[0]) for r in rows_[1:] if r and r[-1] == 'orchestrator' and r[0].isdigit()
             and os.path.exists(os.path.join(SAVED, f'{r[0]}.html'))]
con.execute('CREATE TEMP TABLE saved(id BIGINT)')
con.executemany('INSERT INTO saved VALUES (?)', [(i,) for i in saved_ids])


def pick(code, words):
    r = con.execute("""SELECT r.request_id FROM requests r JOIN saved s ON s.id = r.request_id
                       WHERE r.problem_code = ? AND r.resolution_public = ? ORDER BY r.ts_init DESC LIMIT 1""", [code, words]).fetchone()
    return r[0] if r else None


ids = {'cavein': pick('Cave-Ins', 'referred to street maintenance for repair work to be scheduled'),
       'tree': pick('Inspect City Tree', 'removal work order created')}
assert all(ids.values()), ids
with open(os.path.join(PRIV, 'status_sample_ids.json'), 'w') as f:
    json.dump(ids, f)


def text_of(path):
    t = open(path, encoding='utf-8', errors='replace').read()
    t = re.sub(r'(?is)<script.*?</script>|<style.*?</style>', '', t)
    t = re.sub(r'<[^>]+>', '\n', t)
    t = html.unescape(t)
    return [ln.strip() for ln in t.splitlines() if ln.strip()]


def after(lines, label, n=1):
    for i, ln in enumerate(lines):
        if ln == label:
            return lines[i + n] if i + n < len(lines) else None
    return None


def mdy(s):
    m = re.search(r'(\d{2})/(\d{2})/(\d{4})', s or '')
    return f'{m.group(3)}-{m.group(1)}-{m.group(2)}' if m else None


def parse(rid):
    path = os.path.join(SAVED, f'{rid}.html')
    L = text_of(path)
    page = {'path_private': os.path.relpath(path, ROOT)}
    i = next(k for k, ln in enumerate(L) if ln == 'Copy direct link')
    # header block: "Service Request <id>", problem type, "at", address, "submitted on", date
    page['problem_type'] = L[i - 5]
    page['submitted_on'] = mdy(L[i - 1])
    st = after(L, 'Status:')
    page['status'] = st
    page['status_on'] = mdy(after(L, 'Status:', 2))
    page['investigation_done'] = mdy(after(L, 'Dept Investigation Completed On:'))
    page['resolution'] = after(L, 'Resolution:')
    page['resolution_details'] = after(L, 'Details:')
    page['dept'] = after(L, 'Dept To Receive SR:')
    page['due_by'] = mdy(after(L, 'Dept Response Due By:'))
    k = L.index('Dept Response Due By:')
    nums = []
    for ln in L[k + 2:k + 5]:
        if ln.isdigit():
            nums.append(int(ln))
        else:
            break
    page['related_count'] = nums[0] if nums else None
    page['related_heading'] = 'Related Items' in L[k + 2:k + 6]
    page['related_text'] = next((ln for ln in L[k + 2:k + 8] if ln.startswith('Inspections and work orders')), None)
    otp = []
    for ln in L[L.index('On This Page') + 1:L.index('On This Page') + 5]:
        if ln in otp:
            break
        otp.append(ln)
    page['on_this_page'] = otp
    # comments under Actions Taken (date line, then text)
    com = []
    if 'Comments' in L:
        c = L.index('Comments')
        j = c + 1
        while j + 1 < len(L) and re.match(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$', L[j]):
            com.append({'date': mdy(L[j]), 'text': L[j + 1]})
            j += 2
    page['comments'] = com
    page['saved_copy_time'] = dt.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
    return page


def file_row(rid):
    r = con.execute("""SELECT block_label, ward, neighborhood, ts_init, ts_closed, ts_promised, problem_code, type_name, submit_to
                       FROM requests WHERE request_id = ?""", [rid]).fetchone()
    cols = ['block_label', 'ward', 'neighborhood', 'ts_init', 'ts_closed', 'ts_promised', 'problem_code', 'type_name', 'submit_to']
    return dict(zip(cols, r))


def block(lbl):
    m = re.match(r'^\s*(\d+)\s+block of\s+(.+)$', lbl or '', re.I)
    if not m:
        return None
    words = []
    for w in m.group(2).replace('.', '').split():
        words.append(w.upper() if w.upper() in ('N', 'S', 'E', 'W') else w.capitalize())
    return f'{(int(m.group(1)) // 100) * 100} block of {" ".join(words)}'


P = {k: parse(v) for k, v in ids.items()}
F = {k: file_row(v) for k, v in ids.items()}
for k in P:
    assert P[k]['due_by'] == str(F[k]['ts_promised'])[:10], (k, P[k]['due_by'], F[k]['ts_promised'])

FIGS, DECISIONS = [], []


def figure(fid, value, unit, period, definition, derivation, label='observed', note=''):
    FIGS.append({'id': fid, 'value': value, 'unit': unit, 'period': period, 'definition': definition, 'label': label,
                 'source_sql_or_script': SCRIPT, 'note': note, 'derivation': derivation, 'owner': 'E3'})
    return fid


SAVED_NOTE = (f"the City's public status page ({PAGE_URL}), saved copy taken on 14 Oct 2026 by the orchestrating thread's probe "
              '(file time {t} Central); not re-fetched, because robots.txt disallows check-service-request.cfm')
cv, tr = P['cavein'], P['tree']
figure('e3_status_cavein_related_items', cv['related_count'] or 0, 'items attached', 'sample cave-in request, filed and closed July 2026',
       'Inspections and work orders listed under "Related Items" on the status page of one cave-in closed "Referred to street maintenance for repair work to be scheduled".',
       f"Read from {SAVED_NOTE.format(t=cv['saved_copy_time'])}. The page shows no Related Items heading and a count of {cv['related_count'] or 0}.")
figure('e3_status_tree_related_items', tr['related_count'], 'items attached', 'sample tree request, filed May 2026, closed June 2026',
       'Inspections and work orders listed under "Related Items" on the status page of one tree request closed "Removal work order created".',
       f"Read from {SAVED_NOTE.format(t=tr['saved_copy_time'])}. The page shows the heading 'Related Items', the line 'Inspections and work orders attached to this request.' and a count of {tr['related_count']}. Only the count is read; the list itself loads from a related-items address that the City's robots.txt disallows, and E3 did not call it.")
promised = dt.date.fromisoformat(cv['due_by'])
days_past = (RUN_DATE - promised).days
figure('e3_status_cavein_days_past_promise', days_past, 'days past promise', f'from the promised date to {RUN_DATE.isoformat()}',
       'For the sample cave-in: calendar days from its promised date ("Dept Response Due By") to 13 Oct 2026, the figure the proposed page would show while the repair is open.',
       f"Promised {cv['due_by']} on the page and in the 311 file (they agree); {RUN_DATE.isoformat()} minus that date is {days_past} days. "
       'Whether the repair is in fact still open is not known: the request was closed at the referral and no work order is attached, which is the point of the page.',
       label='inferred', note='Illustration of the proposed page. Assumes the repair work order would still be open on 13 Oct 2026.')

# E1's sample (read-only; never edited here)
e1 = {}
pp = os.path.join(ROOT, 'build', 'E1', 'probe_summary.json')
if os.path.exists(pp):
    with open(pp) as f:
        e1 = json.load(f)
if e1:
    figure('e3_status_probe_handoff_with_items', e1['handoff']['n_with_item'], 'pages with items attached', '14 Oct 2026 probe',
           'Hand-off closings (cave-in referred, towing tagged, weeds on schedule) whose status page lists any attached inspection or work order, in the probe pages.',
           f"build/E1/probe_summary.json (E1, read-only): {e1['handoff']['n_with_item']} of {e1['handoff']['n']} hand-off pages show attached items.",
           note=f"of {e1['handoff']['n']} pages; a probe, not a sample")
    figure('e3_status_probe_handoff_pages', e1['handoff']['n'], 'pages', '14 Oct 2026 probe', 'Hand-off status pages in the probe.', 'build/E1/probe_summary.json (E1).')
    figure('e3_status_probe_tree_with_items', e1['tree_removal']['n_with_item'], 'pages with items attached', '14 Oct 2026 probe',
           'Tree requests closed "removal work order created" whose status page lists attached items, in the probe pages.',
           f"build/E1/probe_summary.json (E1, read-only): {e1['tree_removal']['n_with_item']} of {e1['tree_removal']['n']} tree-removal pages show attached items ({', '.join(map(str, e1['tree_removal']['items']))}).")
    figure('e3_status_probe_tree_pages', e1['tree_removal']['n'], 'pages', '14 Oct 2026 probe', 'Tree-removal status pages in the probe.', 'build/E1/probe_summary.json (E1).')

# E1's stratified sample of status pages (read-only): one row per service and closing words
sample_rows = []
stp = os.path.join(ROOT, 'build', 'E1', 'service_table.csv')
if os.path.exists(stp):
    with open(stp, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try:
                n, wo, anyi = int(r['n']), int(r['work_order'] or 0), int(r['any_item'] or 0)
            except (ValueError, KeyError):
                continue
            sid = r['stratum'].lower()
            per = '14 Oct 2026 sample of status pages (E1)'
            src_ = ("E1's stratified random sample of the City's public status pages (build/E1/service_table.csv, read-only), "
                    f"service '{r['service']}', closing words '{r['closing_words']}': {n} pages sampled from {r.get('population') or '?'} requests.")
            f_n = figure(f'e3_status_e1_{sid}_pages', n, 'pages sampled', per, f"Status pages sampled for {r['service']} closed '{r['closing_words']}'.", src_)
            f_wo = figure(f'e3_status_e1_{sid}_work_order', wo, 'pages with a work order attached', per,
                          f"Sampled status pages for {r['service']} closed '{r['closing_words']}' that list an attached work order.",
                          src_ + f" {wo} list a work order; {anyi} list any attached item (inspections included).", note=f"of {n} pages")
            f_any = figure(f'e3_status_e1_{sid}_any_item', anyi, 'pages with any item attached', per,
                           f"Sampled status pages for {r['service']} closed '{r['closing_words']}' that list any attached inspection or work order.", src_)
            row = {'stratum': r['stratum'], 'group': r['group'], 'service_code': r['service'], 'closing_words': r['closing_words'], 'division': r['division'],
                   'pages': f_n, 'work_order': f_wo, 'any_item': f_any, 'wo_share': wo / n if n else 0}
            if wo:
                dbp, late = int(r.get('done_by_promise') or 0), int(r.get('done_late') or 0)
                row['done_by_promise'] = figure(f'e3_status_e1_{sid}_done_by_promise', dbp, 'work orders finished by the promise date', per,
                                                f"Of the sampled {r['service']} requests with an attached work order, those whose work order finished on or before the request's promised date.",
                                                src_ + f" Of {wo} with a work order: {dbp} finished by the promise, {late} finished later (median {r.get('median_days_late') or '?'} days late), {r.get('no_finish') or 0} with no finish recorded.",
                                                note=f'of {wo} with a work order')
                row['done_late'] = figure(f'e3_status_e1_{sid}_done_late', late, 'work orders finished after the promise date', per,
                                          f"Of the sampled {r['service']} requests with an attached work order, those finished after the promised date.", src_)
            sample_rows.append(row)
    sample_rows.sort(key=lambda x: (-x['wo_share'], x['stratum']))

DECISIONS += [
    {'id': 'e3-status-e1-sample', 'decision': "The status page's footer shows E1's stratified sample (build/E1/service_table.csv) when it exists: per service and closing words, pages sampled, pages with a work order attached, and, where work orders exist, how many finished by the promise. It replaced the 12-page probe once E1's sample landed.",
     'why': "E1's sample overturned the probe for cave-ins: 16 of 40 referred cave-ins carry an attached work order. The page must show the measured rate, not the anecdote. Numbers come from e3_status_e1_* figures written from E1's table at build time.",
     'alternative_rejected': 'Keeping the probe line (0 of 6 hand-offs), which E1 superseded.', 'owner': 'E3'},
    {'id': 'e3-status-no-fetch', 'decision': 'The status page is rebuilt from two copies already saved by the orchestrating thread; E3 fetched no status page.',
     'why': "The city's robots.txt, read by E3 at 3:27 p.m. on 14 Oct (saved copy in data/raw/stlouis-mo.gov/E3/), disallows check-service-request.cfm for every user agent with the comment 'Do not crawl service request'. The rule lacks a leading slash, so parsers call it allowed, but the owner's intent is plain (E1 reached the same reading at 3:24 p.m.). The brief's condition, 'allowed by robots.txt', is not met.",
     'alternative_rejected': 'Fetching two fresh pages as briefed (one request each), or calling the related-items address that the City\'s robots.txt disallows.', 'owner': 'E3'},
    {'id': 'e3-status-own-page', 'decision': 'The before/after is its own page, site/status.html, linked from the residents door.',
     'why': 'It is surface 2 of the demo and needs a full 1920x1080 screen of three panels side by side; inside index.html it would push the receipt and scoreboard down.',
     'alternative_rejected': 'A section of index.html.', 'owner': 'E3'},
    {'id': 'e3-status-after-is-illustration', 'decision': "The 'after' panel is labelled a proposal and its days-past-promise figure is labelled inferred, with the assumption stated.",
     'why': 'The sample cave-in was closed at the referral, so nothing on record says whether the repair was done. The panel shows what the page would show while a work order is open; it does not claim this repair is undone.',
     'alternative_rejected': 'Presenting the after panel as this request\'s actual state.', 'owner': 'E3'},
]

fmtd = lambda s: s
panels = [
    {'key': 'before', 'tag': 'Today', 'title': 'A cave-in, referred', 'caption': 'This page ends at the hand-off. The repair, if it was done, is not on it.',
     'header': {'type': cv['problem_type'], 'block': block(F['cavein']['block_label']), 'ward': F['cavein']['ward'], 'submitted_on': cv['submitted_on']},
     'overview': [['Status', f"{cv['status']}", cv['status_on']], ['Dept Investigation Completed On', None, cv['investigation_done']], ['Resolution', cv['resolution'], None]],
     'details_text': cv['resolution_details'],
     'department': [['Dept To Receive SR', cv['dept'], None], ['Dept Response Due By', None, cv['due_by']]],
     'related': {'shown': cv['related_heading'], 'figure_id': 'e3_status_cavein_related_items', 'text': cv['related_text']},
     'comments': cv['comments'], 'on_this_page': cv['on_this_page']},
    {'key': 'tree', 'tag': 'Today', 'title': 'A tree removal, same page', 'caption': 'Forestry attaches its work orders, so the same page already follows the job past the hand-off.',
     'header': {'type': tr['problem_type'], 'block': block(F['tree']['block_label']), 'ward': F['tree']['ward'], 'submitted_on': tr['submitted_on']},
     'overview': [['Status', f"{tr['status']}", tr['status_on']], ['Dept Investigation Completed On', None, tr['investigation_done']], ['Resolution', tr['resolution'], None]],
     'details_text': tr['resolution_details'],
     'department': [['Dept To Receive SR', tr['dept'], None], ['Dept Response Due By', None, tr['due_by']]],
     'related': {'shown': tr['related_heading'], 'figure_id': 'e3_status_tree_related_items', 'text': tr['related_text']},
     'comments': tr['comments'], 'on_this_page': tr['on_this_page']},
    {'key': 'after', 'tag': 'Proposed', 'title': 'The cave-in, under the four rules', 'caption': 'The same page doing for every service what it does for trees: the request stays open until the work is finished.',
     'header': {'type': cv['problem_type'], 'block': block(F['cavein']['block_label']), 'ward': F['cavein']['ward'], 'submitted_on': cv['submitted_on']},
     'overview': [['Status', 'With Street Maintenance', None], ['Since', None, cv['status_on']], ['Promised by', None, cv['due_by']],
                  ['Days past the promise', None, None, 'e3_status_cavein_days_past_promise']],
     'details_text': 'Inspected and referred to Street Maintenance. A repair work order is attached and open. The system closes this request when the work order closes.',
     'department': [['Dept To Receive SR', cv['dept'], None], ['Dept Response Due By', None, cv['due_by']],
                    ['Done by the promised date', 'Not yet: work order open', None]],
     'related': {'shown': True, 'proposed': True, 'text': 'Inspections and work orders attached to this request.',
                 'items': [{'kind': 'Inspection', 'status': 'Completed', 'date': cv['investigation_done']},
                           {'kind': 'Work order: street repair', 'status': 'Open', 'date': cv['status_on'], 'due': cv['due_by']}]},
     'comments': [], 'on_this_page': ['Actions Taken', 'Details', 'Related Items']},
]
payload = {
    'label': "Reconstruction of the City's public status page, block level; sample request",
    'source': {'page': PAGE_URL, 'robots': ROBOTS, 'robots_read': '2026-10-14 15:27 Central',
               'saved': 'Saved copies taken on 14 Oct 2026 by the orchestrating thread\'s probe; not re-fetched (robots.txt disallows check-service-request.cfm).'},
    'asof': RUN_DATE.isoformat(),
    'panels': panels,
    'probe': ['e3_status_probe_handoff_with_items', 'e3_status_probe_handoff_pages', 'e3_status_probe_tree_with_items', 'e3_status_probe_tree_pages'] if e1 else [],
    'sample': [{k: v for k, v in r.items() if k != 'wo_share'} for r in sample_rows],
    'sample_source': 'build/E1/service_table.csv (E1, stratified random sample of status pages, 14 Oct 2026)' if sample_rows else None,
    'rules': ['Attach a work order at every hand-off.', 'Close the request on actual finish, not at hand-off (the city\'s own towing rule, for every service).',
              'Carry the promise date to the job.', 'Work the overdue list oldest-first, seen weekly by the cabinet.'],
}
with open(os.path.join(OUT, 'statuspage.json'), 'w') as f:
    json.dump({'meta': {'built_at': dt.datetime.now().strftime('%Y-%m-%d %H:%M'), 'script': SCRIPT}, **payload}, f, indent=1, default=str)


def merge(path, items, key):
    old = []
    if os.path.exists(path):
        with open(path) as f:
            old = json.load(f).get(key, [])
    new_ids = {it['id'] for it in items}
    with open(path, 'w') as f:
        json.dump({key: [it for it in old if it['id'] not in new_ids] + items}, f, indent=1, default=str)


merge(os.path.join(OUT, 'figures.json'), FIGS, 'figures')
merge(os.path.join(OUT, 'decisions.json'), DECISIONS, 'decisions')
print({k: {kk: v for kk, v in P[k].items() if kk not in ('path_private',)} for k in P})
print('days past', days_past, 'figures', len(FIGS))
