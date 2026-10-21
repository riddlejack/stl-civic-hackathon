"""N3 step 2: attach a closure class to every request; write build/N3/req.parquet and the class table used.

Run: .venv/bin/python -I scripts/night/N3/02_enrich.py
Uses N2's classes when research/chapters/N2-closure-classes.csv exists, else N3 first-pass rules (classes.py).
"""
import duckdb, os, re, sys, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classes import classifier
ROOT = '.'
PQ = os.path.join(ROOT, 'build/N3/csb.parquet')
OUT = os.path.join(ROOT, 'build/N3/req.parquet')
con = duckdb.connect()
cls, source = classifier()
pairs = con.execute(f"SELECT ptype, resolution, count(*) n, count(*) FILTER (WHERE status_group='closed') nc FROM '{PQ}' GROUP BY 1,2").fetchall()
rows = [(pt, res, cls(pt, res), n, nc) for pt, res, n, nc in pairs]
# N2 rule per (type, text), to allow the with/without-enforcement variant; coverage of N2's file
from classes import key, N2_PATH
rule = {}
if os.path.exists(N2_PATH):
    for r in csv.DictReader(open(N2_PATH, newline='', encoding='utf-8', errors='replace')):
        rule[((r['PROBLEMCODE'] or '').strip(), key(r['resolution_text']))] = r['rule_or_judgement']
cov_hit = sum(nc for pt, res, n, nc in pairs if ((pt or '').strip(), key(res)) in rule)
print('closures (2023-2026) whose (type, text) is in N2 file:', cov_hit, 'of', sum(nc for *_, nc in pairs))
con.execute("CREATE TABLE cmap (ptype VARCHAR, resolution VARCHAR, class VARCHAR, n BIGINT, nc BIGINT, n2_rule VARCHAR)")
con.executemany("INSERT INTO cmap VALUES (?,?,?,?,?,?)", [r + (rule.get(((r[0] or '').strip(), key(r[1]))),) for r in rows])
con.execute(f"""
COPY (
  SELECT r.*,
    CASE WHEN r.status_group <> 'closed' THEN NULL ELSE coalesce(m.class, 'blank') END AS class,
    CASE WHEN r.status_group <> 'closed' THEN NULL WHEN m.n2_rule = 'handed_off:enforcement' THEN 'enforcement'
         ELSE coalesce(m.class, 'blank') END AS class_enf_separate,
    epoch(r.t_closed - r.t_init)/86400.0 AS days_close,
    CASE WHEN r.t_promise IS NOT NULL THEN epoch(r.t_promise - r.t_init)/86400.0 END AS promise_days,
    CASE WHEN r.t_init < TIMESTAMP '2025-05-16' THEN 'before' ELSE 'after' END AS period,
    CASE WHEN r.ward IN ('01','02','03','04','05') THEN 'w01-05' WHEN r.ward IN ('06','07','08','09') THEN 'w06-09'
         WHEN r.ward IN ('10','11','12','13','14') THEN 'w10-14' END AS wgroup
  FROM '{PQ}' r LEFT JOIN cmap m ON m.ptype IS NOT DISTINCT FROM r.ptype AND m.resolution IS NOT DISTINCT FROM r.resolution
) TO '{OUT}' (FORMAT parquet)""")
print('class source:', source)
print(con.execute(f"SELECT class, count(*) FROM '{OUT}' WHERE t_init >= '2024-01-01' AND status_group='closed' GROUP BY 1 ORDER BY 2 DESC").fetchall())
unc = con.execute("SELECT resolution, sum(nc) FROM cmap WHERE class='unclassed' GROUP BY 1 ORDER BY 2 DESC").fetchall()
print('unclassed texts:', unc[:30])
# class table used (closed requests 2024+ only counts in nc are all-years 2023-26); redact emails and phone numbers
red = lambda s: re.sub(r'\b\d{3}[- ]\d{3}[- ]\d{4}\b|\b\d{3}-\d{4}\b', '[phone]', re.sub(r'\S+@\S+', '[email]', s or ''))
with open(os.path.join(ROOT, 'build/N3/closure-classes-used.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['PROBLEMCODE', 'resolution_text', 'class', 'n_closed_2023_2026', 'source'])
    for pt, res, c, n, nc in sorted(rows, key=lambda r: (-(r[4] or 0), r[0] or '', r[1] or '')):
        if nc: w.writerow([pt, red(res), c, nc, 'N2' if 'N2 closure' in source else 'N3 first-pass'])
json.dump({'class_source': source}, open(os.path.join(ROOT, 'build/N3/class_source.json'), 'w'))
