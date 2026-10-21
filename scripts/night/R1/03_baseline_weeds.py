"""R1 step 3a: does a weeds report change anything? Requested parcels vs same-block rotation parcels.

For every 2026 Weeds-Vacant Lot / Weeds-Vacant Bldg request closed "on schedule to be cut ..." or
"added to rotation" on a matched parcel, filed by 13 Sep 2026 (30 days of ledger left):
  requested: days from the filing date D to the next billed cut on the reported parcel (first cut >= D).
  control:   the same measure, from the same date D, for every other parcel on the same city block
             (ledger CITYBLOCK) that was cut at least once in 2026 (on the rotation) and had no weed request
             of any kind in the 60 days up to and including D.
Each request is one unit: the control side is the mean over that block's control parcels, so big blocks do
not dominate. Requests on blocks with no control parcel are dropped (counted).
Variants: (ii) requested parcels that were themselves cut at least once in 2026 (like the controls);
(iii) stratified by days since the parcel's last 2026 cut before D; (iv) other-block control: rotation
parcels in the same ward on city blocks with no weed request in the 60 days up to D.
Ledger dates are weekly posting batches: differences under a week are noise.

Outputs: build/R1/baseline_weeds.json, build/R1/baseline_weeds.csv
Run: .venv/bin/python -I scripts/night/R1/03_baseline_weeds.py
"""
import json, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import duckdb
from common import DB, OUT, NEVER_CUTOFF, q, write_csv

con = duckdb.connect()
con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
RES = {'definition': __doc__}

# city block per parcel: ledger CITYBLOCK (mode), else characters 2-7 of the MSD handle (checked below)
con.execute("CREATE TEMP TABLE lblock AS SELECT parcel, mode(cityblock) AS cityblock FROM s.ledger WHERE cityblock IS NOT NULL GROUP BY parcel")
chk = q(con, """SELECT count(*) n, avg(CAST(l.cityblock = substr(p.handle, 2, 6) AS INT)) agree
                FROM lblock l JOIN s.parcels p ON p.pid = l.parcel""")[0]
RES['cityblock_handle_check'] = chk
print('ledger CITYBLOCK vs handle[2:7] agreement', chk)
con.execute("""CREATE TEMP TABLE pblock AS
  SELECT p.pid AS parcel, coalesce(l.cityblock, substr(p.handle, 2, 6)) AS cityblock
  FROM s.parcels p LEFT JOIN lblock l ON l.parcel = p.pid""")

con.execute("CREATE TEMP TABLE c26 AS SELECT DISTINCT parcel, service_date AS d FROM s.cuts WHERE service_date BETWEEN DATE '2026-01-01' AND DATE '2026-10-13'")
con.execute("CREATE TEMP TABLE rot AS SELECT DISTINCT parcel FROM c26")
con.execute("""CREATE TEMP TABLE wreq AS
  SELECT DISTINCT rp.pid AS parcel, r.init_date AS d
  FROM s.requests r JOIN s.request_parcel rp USING (request_id)
  WHERE r.problem_code IN (SELECT problem_code FROM s.weed_ledger_codes)
     OR r.problem_code IN ('Weeds-Occupied Ppty', 'Debris-Vacant Lot', 'Debris-Vacant Bldg')""")

# target requests: one unit per (parcel, filing date)
con.execute(f"""
CREATE TEMP TABLE tgt AS
SELECT rp.pid AS parcel, r.init_date AS d, any_value(r.problem_code) AS problem_code, any_value(r.ward) AS ward,
       any_value(r.ward_group) AS ward_group, count(*) AS n_requests, bool_or(coalesce(rp.is_lra, false)) AS is_lra
FROM s.v_requests r JOIN s.request_parcel rp USING (request_id)
WHERE r.problem_code IN ('Weeds-Vacant Lot', 'Weeds-Vacant Bldg') AND r.init_year = 2026
  AND r.status_group = 'closed' AND (r.res_key LIKE 'on schedule to be cut%' OR r.res_key = 'added to rotation')
  AND r.init_date <= DATE '{NEVER_CUTOFF}'
GROUP BY rp.pid, r.init_date
""")
con.execute("""CREATE TEMP TABLE tgt2 AS
SELECT t.*, b.cityblock,
       (SELECT min(c.d) FROM c26 c WHERE c.parcel = t.parcel AND c.d >= t.d) AS next_cut,
       (SELECT max(c.d) FROM c26 c WHERE c.parcel = t.parcel AND c.d < t.d) AS prev_cut,
       t.parcel IN (SELECT parcel FROM rot) AS on_rotation
FROM tgt t LEFT JOIN pblock b USING (parcel)""")

# same-block controls
con.execute("""CREATE TEMP TABLE ctl AS
SELECT t.parcel AS tparcel, t.d, pb.parcel AS cparcel,
       (SELECT min(c.d) FROM c26 c WHERE c.parcel = pb.parcel AND c.d >= t.d) AS next_cut,
       (SELECT max(c.d) FROM c26 c WHERE c.parcel = pb.parcel AND c.d < t.d) AS prev_cut
FROM tgt2 t JOIN pblock pb ON pb.cityblock = t.cityblock AND pb.parcel <> t.parcel
WHERE pb.parcel IN (SELECT parcel FROM rot)
  AND NOT EXISTS (SELECT 1 FROM wreq w WHERE w.parcel = pb.parcel AND w.d BETWEEN t.d - 60 AND t.d)""")


def days(nc, d):
    return f"coalesce(date_diff('day', {d}, {nc}), 9999)"


con.execute(f"""CREATE TEMP TABLE ctl_agg AS
SELECT tparcel, d, count(*) AS n_ctl,
       avg(CAST({days('next_cut', 'd')} <= 7 AS INT)) AS c7, avg(CAST({days('next_cut', 'd')} <= 14 AS INT)) AS c14,
       avg(CAST({days('next_cut', 'd')} <= 30 AS INT)) AS c30, avg(CAST(next_cut IS NULL AS INT)) AS cnone,
       median({days('next_cut', 'd')}) AS cmed,
       avg(CASE WHEN prev_cut IS NULL THEN NULL ELSE date_diff('day', prev_cut, d) END) AS c_days_since_prev
FROM ctl GROUP BY tparcel, d""")
con.execute(f"""CREATE TEMP TABLE pair AS
SELECT t.*, a.n_ctl, a.c7, a.c14, a.c30, a.cnone, a.cmed, a.c_days_since_prev,
       CAST({days('t.next_cut', 't.d')} <= 7 AS INT) AS r7, CAST({days('t.next_cut', 't.d')} <= 14 AS INT) AS r14,
       CAST({days('t.next_cut', 't.d')} <= 30 AS INT) AS r30, CAST(t.next_cut IS NULL AS INT) AS rnone,
       {days('t.next_cut', 't.d')} AS rdays,
       CASE WHEN t.prev_cut IS NULL THEN 'no 2026 cut before' WHEN date_diff('day', t.prev_cut, t.d) < 14 THEN '0-13 d'
            WHEN date_diff('day', t.prev_cut, t.d) < 28 THEN '14-27 d' WHEN date_diff('day', t.prev_cut, t.d) < 56 THEN '28-55 d'
            ELSE '56+ d' END AS since_prev
FROM tgt2 t JOIN ctl_agg a ON a.tparcel = t.parcel AND a.d = t.d""")

RES['counts'] = q(con, """SELECT (SELECT count(*) FROM tgt) AS target_units, (SELECT sum(n_requests) FROM tgt) AS target_requests,
    (SELECT count(*) FROM tgt2 WHERE cityblock IS NULL) AS no_block,
    (SELECT count(*) FROM pair) AS units_with_controls, (SELECT sum(n_ctl) FROM pair) AS control_parcel_dates,
    (SELECT median(n_ctl) FROM pair) AS median_controls_per_unit""")[0]
print(RES['counts'])


def summarise(where, label):
    r = q(con, f"""SELECT count(*) AS n_units,
        round(avg(r7), 6) AS req_cut_7d, round(avg(c7), 6) AS ctl_cut_7d,
        round(avg(r14), 6) AS req_cut_14d, round(avg(c14), 6) AS ctl_cut_14d,
        round(avg(r30), 6) AS req_cut_30d, round(avg(c30), 6) AS ctl_cut_30d,
        round(avg(rnone), 6) AS req_no_cut_by_13oct, round(avg(cnone), 6) AS ctl_no_cut_by_13oct,
        median(rdays) AS req_median_days, median(cmed) AS ctl_median_days_of_block_medians,
        round(avg(r14) - avg(c14), 6) AS diff_14d, round(avg(r30) - avg(c30), 6) AS diff_30d
        FROM pair WHERE {where}""")[0]
    return {'group': label, **r}


rows = [summarise('TRUE', 'all (lots and buildings)'),
        summarise("problem_code = 'Weeds-Vacant Lot'", 'vacant lots'),
        summarise("problem_code = 'Weeds-Vacant Bldg'", 'vacant buildings'),
        summarise('on_rotation', 'requested parcel itself cut in 2026 (like controls)'),
        summarise("on_rotation AND problem_code = 'Weeds-Vacant Lot'", 'vacant lots, requested parcel cut in 2026'),
        summarise("on_rotation AND problem_code = 'Weeds-Vacant Bldg'", 'vacant buildings, requested parcel cut in 2026'),
        summarise('is_lra', 'land-bank (LRA) parcels'),
        summarise('NOT is_lra', 'other parcels')]
for wg in ('1-5', '6-9', '10-14'):
    rows.append(summarise(f"ward_group = '{wg}'", f'wards {wg}'))
    rows.append(summarise(f"ward_group = '{wg}' AND on_rotation", f'wards {wg}, requested parcel cut in 2026'))
for s in ('no 2026 cut before', '0-13 d', '14-27 d', '28-55 d', '56+ d'):
    rows.append(summarise(f"since_prev = '{s}'", f'days since requested parcel last cut: {s}'))
RES['same_block'] = rows
for r in rows:
    print(f"{r['group'][:52]:52s} n={r['n_units']:5d} 14d {r['req_cut_14d']} vs {r['ctl_cut_14d']} | 30d {r['req_cut_30d']} vs {r['ctl_cut_30d']} | none {r['req_no_cut_by_13oct']} vs {r['ctl_no_cut_by_13oct']} | med {r['req_median_days']} vs {r['ctl_median_days_of_block_medians']}")

# control parcels' own time since last cut, to see whether requested lots sit later in the cycle
RES['days_since_prev_cut'] = q(con, """SELECT median(date_diff('day', prev_cut, d)) FILTER (WHERE prev_cut IS NOT NULL) AS req_median_days_since_prev,
    avg(CAST(prev_cut IS NULL AS INT)) AS req_share_no_prev_2026, median(c_days_since_prev) AS ctl_mean_days_since_prev_median FROM pair""")[0]
print(RES['days_since_prev_cut'])

# (iv) other-block control in the same ward: rotation parcels on city blocks with no weed request in [D-60, D]
con.execute("""CREATE TEMP TABLE pward AS
  SELECT DISTINCT rp.pid AS parcel, r.ward FROM s.requests r JOIN s.request_parcel rp USING (request_id) WHERE r.ward IS NOT NULL
  UNION SELECT parcel_id, lpad(CAST(ward AS VARCHAR), 2, '0') FROM s.lra WHERE ward IS NOT NULL""")
con.execute("CREATE TEMP TABLE pward1 AS SELECT parcel, min(ward) AS ward FROM pward GROUP BY parcel")
con.execute("""CREATE TEMP TABLE rotw AS SELECT r.parcel, w.ward, b.cityblock FROM rot r JOIN pward1 w USING (parcel) JOIN pblock b USING (parcel)""")
con.execute("CREATE TEMP TABLE wreq_block AS SELECT DISTINCT b.cityblock, w.d FROM wreq w JOIN pblock b USING (parcel)")
con.execute("""CREATE TEMP TABLE dates AS SELECT DISTINCT d, ward FROM pair""")
con.execute(f"""CREATE TEMP TABLE other AS
SELECT x.d, x.ward, o.parcel,
       (SELECT min(c.d) FROM c26 c WHERE c.parcel = o.parcel AND c.d >= x.d) AS next_cut
FROM dates x JOIN rotw o ON o.ward = x.ward
WHERE NOT EXISTS (SELECT 1 FROM wreq_block wb WHERE wb.cityblock = o.cityblock AND wb.d BETWEEN x.d - 60 AND x.d)""")
con.execute(f"""CREATE TEMP TABLE other_agg AS SELECT d, ward, count(*) n_other,
   avg(CAST({days('next_cut', 'd')} <= 14 AS INT)) AS o14, avg(CAST({days('next_cut', 'd')} <= 30 AS INT)) AS o30,
   avg(CAST(next_cut IS NULL AS INT)) AS onone FROM other GROUP BY d, ward""")
RES['other_block_same_ward'] = q(con, """SELECT count(*) n_units, round(avg(p.r14), 6) req_14d, round(avg(p.c14), 6) same_block_14d, round(avg(o.o14), 6) other_block_14d,
    round(avg(p.r30), 6) req_30d, round(avg(p.c30), 6) same_block_30d, round(avg(o.o30), 6) other_block_30d,
    round(avg(p.rnone), 6) req_none, round(avg(p.cnone), 6) same_block_none, round(avg(o.onone), 6) other_block_none
    FROM pair p JOIN other_agg o ON o.d = p.d AND o.ward = p.ward""")
RES['other_block_same_ward_on_rotation'] = q(con, """SELECT count(*) n_units, round(avg(p.r14), 6) req_14d, round(avg(p.c14), 6) same_block_14d, round(avg(o.o14), 6) other_block_14d,
    round(avg(p.r30), 6) req_30d, round(avg(p.c30), 6) same_block_30d, round(avg(o.o30), 6) other_block_30d
    FROM pair p JOIN other_agg o ON o.d = p.d AND o.ward = p.ward WHERE p.on_rotation""")
print('other-block', RES['other_block_same_ward'], RES['other_block_same_ward_on_rotation'])

# simple sign test on paired 30-day outcome (requested cut within 30 d vs block control share)
RES['paired'] = q(con, """SELECT count(*) n, sum(CAST(r30 > c30 AS INT)) AS req_better_30, sum(CAST(r30 < c30 AS INT)) AS req_worse_30,
     sum(CAST(r14 > c14 AS INT)) AS req_better_14, sum(CAST(r14 < c14 AS INT)) AS req_worse_14 FROM pair""")[0]
print(RES['paired'])
write_csv(OUT / 'baseline_weeds.csv', rows)
(OUT / 'baseline_weeds.json').write_text(json.dumps(RES, indent=1, default=str))
print('wrote baseline_weeds.json')

# paired differences with a cluster bootstrap by city block (units on one block share controls)
import numpy as np
rows_p = con.execute("SELECT cityblock, r14 - c14, r30 - c30, on_rotation, problem_code FROM pair").fetchall()
rng = np.random.default_rng(20261014)


def boot(sel):
    data = [r for r in rows_p if sel(r)]
    blocks = {}
    for r in data:
        blocks.setdefault(r[0], []).append((r[1], r[2]))
    keys = list(blocks)
    arr = [np.array(blocks[k]) for k in keys]
    est14 = float(np.mean([x[1] for x in data])); est30 = float(np.mean([x[2] for x in data]))
    b14, b30 = [], []
    for _ in range(1000):
        pick = rng.integers(0, len(keys), len(keys))
        m = np.concatenate([arr[i] for i in pick])
        b14.append(m[:, 0].mean()); b30.append(m[:, 1].mean())
    return {'n_units': len(data), 'n_blocks': len(keys),
            'diff_14d': round(est14, 6), 'diff_14d_ci95': [round(float(np.percentile(b14, 2.5)), 6), round(float(np.percentile(b14, 97.5)), 6)],
            'diff_30d': round(est30, 6), 'diff_30d_ci95': [round(float(np.percentile(b30, 2.5)), 6), round(float(np.percentile(b30, 97.5)), 6)]}


RES['paired_diff_bootstrap'] = {
    'all': boot(lambda r: True),
    'on_rotation': boot(lambda r: r[3]),
    'on_rotation_lots': boot(lambda r: r[3] and r[4] == 'Weeds-Vacant Lot'),
    'on_rotation_buildings': boot(lambda r: r[3] and r[4] == 'Weeds-Vacant Bldg'),
}
print(json.dumps(RES['paired_diff_bootstrap'], indent=1))
(OUT / 'baseline_weeds.json').write_text(json.dumps(RES, indent=1, default=str))
