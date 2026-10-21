#!/usr/bin/env python3
"""Privacy check over build/out/. Fails loudly if a
public export carries an e-mail address, a pooled (possibly personal) routing
value, an exact street address, an 11-digit parcel id, or a sensitive code at
block level. Writes build/N1/privacy_check.json."""
import glob, json, os, re, sys
import duckdb
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('STL_ROOT', os.path.abspath(os.path.join(HERE, '..', '..', '..')))
con = duckdb.connect(os.path.join(ROOT, 'build', 'stl.duckdb'), read_only=True)
pooled = {r[0] for r in con.execute("SELECT submit_to FROM requests WHERE division = 'Other (pooled)' AND submit_to IS NOT NULL GROUP BY 1").fetchall()}
sensitive = {r[0] for r in con.execute("SELECT problem_code FROM sensitive_codes").fetchall()}
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
EXACT = re.compile(r'^\d{1,5}[A-Z]? (?!block of)[A-Z0-9 .]+$')   # "1234 EXAMPLE AV" but not "1200 block of EXAMPLE AV"
PARCEL = re.compile(r'(?<!\d)\d{11}(?!\d)')
ADDR_KEYS = {'public_address', 'block_label', 'address', 'addr', 'location'}
ID_KEYS = {'request_id', 'requestid', 'next_same_request_id', 'workorder_id', 'parcel_id', 'pid', 'handle', 'lra_parcel_id'}
REQ_IDS = {r[0] for r in con.execute("SELECT request_id FROM requests").fetchall()}
HOUSE_IN_LABEL = re.compile(r'(?<![A-Za-z0-9])\d{3,}(?![A-Za-z0-9])')
SEVEN = re.compile(r'(?<![\d.])\d{7}(?![\d.])')
CODE_KEYS = {'problem_code'}
issues = []
N1_FILES = ['scoreboard_n1.json', 'ward_like_for_like.json', 'register_counts.json', 'monday_list.json', 'monday_list.csv', 'mowing_2026.json', 'run.json',
            'dumping_blocks.json', 'receipts.json', 'by_ward.json', 'meta.json']


def walk(o, path, fname, block_level):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str):
                if k in ADDR_KEYS | {'block'} and EXACT.match(v.strip()):
                    issues.append((fname, path + '.' + k, 'exact address', v))
                if k in ADDR_KEYS | {'block'} and HOUSE_IN_LABEL.search(re.sub(r'^\d+ block of ', '', v.strip())):
                    issues.append((fname, path + '.' + k, 'house number inside a block label', v))
                if block_level and k in CODE_KEYS and v in sensitive:
                    issues.append((fname, path + '.' + k, 'sensitive code at block level', v))
            if k in ID_KEYS:
                issues.append((fname, path + '.' + k, 'id field in public export', '[id]'))
            walk(v, path + '.' + str(k), fname, block_level)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            walk(x, f'{path}[{i}]', fname, block_level)


for f in N1_FILES:
    p = os.path.join(ROOT, 'build', 'out', f)
    if not os.path.exists(p):
        continue
    text = open(p).read()
    for m in EMAIL.findall(text):
        issues.append((f, '', 'e-mail', m))
    for name in pooled:
        if name and name in text and len(name) > 4:
            issues.append((f, '', 'pooled routing value (may be a person)', '[redacted in log]'))
    for m in PARCEL.findall(text):
        issues.append((f, '', '11-digit number (parcel id?)', m))
    hits = [m for m in SEVEN.findall(text) if int(m) in REQ_IDS]
    if hits:
        issues.append((f, '', f'{len(hits)} seven-digit numbers equal to request ids', '[ids]'))
    if f.endswith('.csv') and 'request_id' in text.splitlines()[0]:
        issues.append((f, 'header', 'request_id column', ''))
    if f.endswith('.csv'):
        import csv as _csv, io as _io
        for i, row in enumerate(_csv.DictReader(_io.StringIO(text)), 2):
            lab = row.get('block_label') or row.get('block') or ''
            if HOUSE_IN_LABEL.search(re.sub(r'^\d+ block of ', '', lab.strip())):
                issues.append((f, f'row {i}', 'house number inside a block label', lab))
            if (row.get('division') or '').upper().startswith('SLMPD') or 'SLMPD' in (row.get('problem_code') or '').upper():
                issues.append((f, f'row {i}', 'police-routed row in public list', ''))
    if f.endswith('.json'):
        block_level = f in ('monday_list.json', 'dumping_blocks.json', 'receipts.json', 'mowing_2026.json')
        walk(json.loads(text), '$', f, block_level)
# figures.json merges other stages' figures: report, do not fail
fig_issues = []
fp = os.path.join(ROOT, 'build', 'out', 'figures.json')
if os.path.exists(fp):
    t = open(fp).read()
    fig_issues = [('figures.json', '', 'e-mail', m) for m in EMAIL.findall(t)] + \
                 [('figures.json', '', '11-digit number (parcel id?)', m) for m in PARCEL.findall(t)] + \
                 [('figures.json', '', 'seven-digit number equal to a request id (may be a count)', m)
                  for m in SEVEN.findall(t) if int(m) in REQ_IDS]
out = {'checked': N1_FILES, 'issues': issues, 'figures_json_warnings': fig_issues,
       'pooled_values_checked': len(pooled), 'sensitive_codes_checked': len(sensitive)}
json.dump(out, open(os.path.join(ROOT, 'build', 'N1', 'privacy_check.json'), 'w'), indent=1)
print(f'privacy_check: {len(issues)} issues in N1 exports; {len(fig_issues)} warnings in merged figures.json')
for i in issues[:20]:
    print('  ', i)
for i in fig_issues[:10]:
    print('   warn', i)
sys.exit(1 if issues else 0)
