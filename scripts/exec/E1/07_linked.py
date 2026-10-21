"""E1 step 7: where a request has work orders attached, what do they show? (no network)

For every sampled request whose page counter > 0 and whose related items were read (06_items.py):
  - work orders attached, split into those created on/after the filing date and those that predate it;
  - each work order joined by WorkOrderId to the Cityworks extracts
    (data/raw/cityworks-gap/extracts/layer_*_rows.json: Status, ActualFinishDate, DateWOClosed);
  - graded against the request's promise date as R1 did: done by promise / done late (days) /
    no finish (only where the promise passed by 13 Sep 2026, 30 days before the file's end) /
    not yet due. "Done" = the first finish among work orders created on or after filing:
    the extract's ActualFinishDate where joined, else the page's "Completed On or Before" date.
Output: build/E1/linked_by_service.csv, build/E1/linked_summary.json (no ids),
        build/E1/private/linked_requests.csv (ids).
Run: .venv/bin/python -I scripts/exec/E1/07_linked.py
"""
import csv, datetime as dt, glob, json, pathlib, statistics
from collections import defaultdict
from zoneinfo import ZoneInfo
import duckdb, pyarrow.parquet as pq

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / 'build' / 'E1'
ITEMS = ROOT / 'data' / 'raw' / 'stlouis-mo.gov' / 'csb-status-items'
CT = ZoneInfo('America/Chicago')
NEVER_CUTOFF = dt.date(2026, 9, 13)


def ms_date(v):
    return dt.datetime.fromtimestamp(v / 1000, tz=dt.timezone.utc).astimezone(CT).date() if v else None


cw = {}
for p in sorted(glob.glob(str(ROOT / 'data/raw/cityworks-gap/extracts/layer_*_rows.json'))):
    for r in json.load(open(p)):
        wid = str(r.get('WorkOrderId') or '')
        if not wid:
            continue
        cur = cw.setdefault(wid, dict(status=r.get('Status'), finish=ms_date(r.get('ActualFinishDate')),
                                      closed=ms_date(r.get('DateWOClosed')), cancelled=bool(r.get('IsCancelled')),
                                      category=r.get('WOCategory'), layers=0))
        cur['layers'] += 1

sample = {r['request_id']: r for r in pq.read_table(OUT / 'private' / 'linkage_sample.parquet').to_pylist()}
con = duckdb.connect(str(ROOT / 'build' / 'stl.duckdb'), read_only=True)
meta = {r[0]: r[1:] for r in con.execute(
    "SELECT request_id, init_date, CAST(ts_promised AS DATE), status_group FROM requests WHERE request_id IN (SELECT unnest(?))",
    [list(sample)]).fetchall()}

rows = []
for rid, s in sample.items():
    if not s['total_item']:
        continue
    f = ITEMS / f'{rid}.json'
    if not f.exists():
        rows.append(dict(request_id=rid, stratum=s['stratum'], family=s['family'], service=s['stratum_label'],
                         grade='items_not_read'))
        continue
    items = json.load(open(f))['items']
    init, promised, sg = meta[rid]
    wos = [i for i in items if i['item_type'] == 'WorkOrder']
    insp = [i for i in items if i['item_type'] == 'Inspection']
    post, pre = [], []
    for w in wos:
        c = dt.date.fromisoformat(w['created']) if w['created'] else None
        x = cw.get(w['item_id'])
        page_fin = dt.date.fromisoformat(w['status_date']) if w['status_date'] and (w['status_label'] or '').startswith('Completed') else None
        rec = dict(created=c, page_finish=page_fin, page_label=w['status_label'], template=w['template'],
                   cw_joined=x is not None, cw_finish=x['finish'] if x else None, cw_closed=x['closed'] if x else None,
                   cw_status=x['status'] if x else None)
        rec['finish'] = rec['cw_finish'] or page_fin
        (post if (c is None or c >= init) else pre).append(rec)
    fins = [w['finish'] for w in post if w['finish']]
    first = min(fins) if fins else None
    if not post:
        grade = 'inspection_only' if not wos else 'only_older_work_orders'
    elif first and promised and first <= promised:
        grade = 'done_by_promise'
    elif first and promised:
        grade = 'done_late'
    elif first:
        grade = 'done_no_promise'
    elif promised and promised <= NEVER_CUTOFF:
        grade = 'no_finish'
    else:
        grade = 'not_yet_due'
    rows.append(dict(request_id=rid, stratum=s['stratum'], family=s['family'], service=s['stratum_label'],
                     n_items=len(items), n_inspections=len(insp), n_wo=len(wos), n_wo_post=len(post), n_wo_pre=len(pre),
                     n_wo_joined=sum(w['cw_joined'] for w in post + pre),
                     n_wo_page_vs_cw_finish_agree=sum(1 for w in post + pre if w['cw_finish'] and w['page_finish'] and w['cw_finish'] == w['page_finish']),
                     n_wo_page_vs_cw_finish_both=sum(1 for w in post + pre if w['cw_finish'] and w['page_finish']),
                     templates='; '.join(sorted({w['template'] or '?' for w in post})),
                     first_finish=first, promised=promised, init=init,
                     days_late=(first - promised).days if first and promised and first > promised else None,
                     days_filing_to_finish=(first - init).days if first else None,
                     grade=grade))

with open(OUT / 'private' / 'linked_requests.csv', 'w', newline='') as f:
    keys = sorted({k for r in rows for k in r}, key=lambda k: (k != 'request_id', k))
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)

GRADES = ['done_by_promise', 'done_late', 'no_finish', 'not_yet_due', 'done_no_promise', 'inspection_only',
          'only_older_work_orders', 'items_not_read']


def summ(g):
    out = dict(n_linked=len(g), **{f'n_{k}': sum(r['grade'] == k for r in g) for k in GRADES})
    late = [r['days_late'] for r in g if r['grade'] == 'done_late']
    out['median_days_late'] = statistics.median(late) if late else None
    due = out['n_done_by_promise'] + out['n_done_late'] + out['n_no_finish']
    out['n_graded_due'] = due
    out['share_done_by_promise_of_due'] = round(out['n_done_by_promise'] / due, 3) if due else None
    out['n_wo_joined_to_cityworks'] = sum(r.get('n_wo_joined', 0) for r in g)
    out['n_wo'] = sum(r.get('n_wo', 0) for r in g)
    return out


by = defaultdict(list)
for r in rows:
    by[(r['stratum'], r['family'], r['service'])].append(r)
n_sampled = defaultdict(int)
for s_ in sample.values():
    n_sampled[s_['stratum']] += 1
svc = []
for k, v in sorted(by.items()):
    n = n_sampled[k[0]]
    wo = sum(1 for r in v if r.get('n_wo', 0) > 0)
    wo_post = sum(1 for r in v if r.get('n_wo_post', 0) > 0)
    svc.append(dict(stratum=k[0], family=k[1], service=k[2], n_sampled=n,
                    n_with_work_order=wo, share_with_work_order=round(wo / n, 3) if n else None,
                    n_with_post_filing_work_order=wo_post,
                    share_with_post_filing_work_order=round(wo_post / n, 3) if n else None, **summ(v)))
if svc:
    with open(OUT / 'linked_by_service.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(svc[0])); w.writeheader(); w.writerows(svc)
fam = defaultdict(list)
for r in rows:
    fam['tree' if r['stratum'] == 'H_tree' else r['family']].append(r)
agree_n = sum(r.get('n_wo_page_vs_cw_finish_both', 0) for r in rows)
agree_k = sum(r.get('n_wo_page_vs_cw_finish_agree', 0) for r in rows)
summary = dict(all=summ(rows), by_family={k: summ(v) for k, v in fam.items()},
               page_vs_cityworks_finish=dict(agree=agree_k, both=agree_n),
               templates_post_filing=dict(sorted(((t, sum(1 for r in rows if t in (r.get('templates') or '')))
                                                  for t in {t for r in rows for t in (r.get('templates') or '').split('; ') if t}),
                                                 key=lambda kv: -kv[1])))
json.dump(summary, open(OUT / 'linked_summary.json', 'w'), indent=1, default=str)
print(json.dumps(summary, indent=1, default=str))
