"""N4: the CityStat views that are counts or averages rather than on-time shares.

1. CSB ward map (avg days to close, requests, closed; 1 Jan 2024 - 30 Jun 2026), plus CityStat's
   2026-only claim (Ward 4 quickest at 6.5 days, Ward 9 slowest at 13.7), plus a within-type
   (type-mix-adjusted) version: each ward's average if it had the citywide mix of request types.
2. CSB tow-related requests by quarter and status (closed/open as CityStat drew them).
3. Snow/ice requests by week and average completion days.
Variants: snapshot (closures before 1 Jul 2026 only vs the whole file to 13 Oct 2026);
one row per distinct REQUESTID (the file repeats a request once per caller) or every row;
same-day same-address same-type repeats dropped or kept; staff-entered (NSO) kept or dropped.
Writes build/N4/other_metrics.json.
"""
import sys, json, collections, datetime as dt
sys.path.insert(0, './scripts/night/N4')
from common import connect, OUT
from citystat_targets import WARD_MAP, TOWING, SNOW, QS

con = connect()
con.execute("""CREATE TEMP TABLE b AS
  SELECT *, CASE WHEN regexp_matches(trim(ward), '^[0-9]+$') AND CAST(trim(ward) AS INT) BETWEEN 1 AND 14
                 THEN lpad(CAST(CAST(trim(ward) AS INT) AS VARCHAR), 2, '0') END AS w14,
    (lag(CAST(t_init AS DATE)) OVER (PARTITION BY probaddress, pc ORDER BY t_init) = CAST(t_init AS DATE)) AS same_day_repeat,
    row_number() OVER (PARTITION BY requestid ORDER BY callertype NULLS LAST) AS rn
  FROM c""")
out = {}

# ---------- 1. ward map
VARIANTS = {
    'all_file': "TRUE",
    'all_snap0701': "TRUE",
    'no_nso_snap0701': "coalesce(callertype,'') <> 'NSO'",
    'dedup_snap0701': "NOT coalesce(same_day_repeat, FALSE)",
    'distinct_id_snap0701': "rn = 1",
    'notcanc_snap0701': "NOT (status='CANCEL' AND (t_cancel IS NULL OR t_cancel < '2026-07-01'))",
    'no_nuisance_snap0701': "coalesce(grp,'') <> 'Nuisance Complaint'",
}
ward_res = {}
for name, flt in VARIANTS.items():
    snap = "TIMESTAMP '2026-10-14'" if name == 'all_file' else "TIMESTAMP '2026-07-01'"
    rows = con.execute(f"""SELECT w14, count(*) n,
        count(*) FILTER (status='CLOSED' AND t_closed < {snap}) cl,
        avg(days) FILTER (status='CLOSED' AND t_closed < {snap}) avgd
      FROM b WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01' AND {flt} GROUP BY 1 ORDER BY 1""").fetchall()
    d = {r[0]: dict(n=r[1], closed=r[2], avg_days=round(r[3], 2)) for r in rows}
    tot_n = sum(v['n'] for v in d.values()); tot_c = sum(v['closed'] for v in d.values())
    errs = [abs(d[w]['avg_days'] - WARD_MAP[w][0]) for w in WARD_MAP if w and w in d]
    nerr = [abs(d[w]['n'] - WARD_MAP[w][1]) / WARD_MAP[w][1] * 100 for w in WARD_MAP if w and w in d]
    ward_res[name] = dict(by_ward=d, total_n=tot_n, total_closed=tot_c, closed_share=round(tot_c / tot_n, 4),
                          avg_days_mae=round(sum(errs) / len(errs), 2), n_mape_pct=round(sum(nerr) / len(nerr), 1))
    print(f"ward map {name:22s} total {tot_n:7d} closed {tot_c:7d} ({tot_c/tot_n:.3f})  avg-days MAE {ward_res[name]['avg_days_mae']:.2f}  n MAPE {ward_res[name]['n_mape_pct']:.1f}%")
print('   CityStat total 286,148 closed 236,155 (0.825)')
best = min(ward_res, key=lambda k: ward_res[k]['avg_days_mae'] + 0.2 * ward_res[k]['n_mape_pct'])
print('   best variant:', best)
for w in [k for k in WARD_MAP if k]:
    v = ward_res[best]['by_ward'][w]
    print(f"   ward {w}: ours {v['avg_days']:6.2f} d / {v['n']:6d} / {v['closed']:6d}   CityStat {WARD_MAP[w][0]:6.2f} / {WARD_MAP[w][1]:6d} / {WARD_MAP[w][2]:6d}")

# 2026-only (CityStat text: "In 2026 ... quickest 6.5 days in Ward 4 ... slowest 13.7 days in Ward 9"; period end unstated)
y26 = {}
for lab, snap in (('closed_by_0701', "TIMESTAMP '2026-07-01'"), ('file', "TIMESTAMP '2026-10-14'")):
    rows = con.execute(f"""SELECT w14, count(*) FILTER (status='CLOSED' AND t_closed < {snap}) cl, avg(days) FILTER (status='CLOSED' AND t_closed < {snap})
      FROM b WHERE t_init >= '2026-01-01' AND t_init < '2026-07-01' AND w14 IS NOT NULL AND rn = 1 GROUP BY 1 ORDER BY 3""").fetchall()
    y26[lab] = [dict(ward=r[0], closed=r[1], avg_days=round(r[2], 2)) for r in rows]
    print(f"2026 H1 by ward ({lab}): fastest {rows[0][0]} {rows[0][2]:.1f} d, slowest {rows[-1][0]} {rows[-1][2]:.1f} d")

# within-type (type-mix-adjusted) average days, same period, closures before 1 Jul 2026
mix = con.execute("""WITH x AS (SELECT w14, pc, days FROM b WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01'
        AND status='CLOSED' AND t_closed < '2026-07-01' AND w14 IS NOT NULL AND rn = 1),
  city AS (SELECT pc, count(*) * 1.0 / sum(count(*)) OVER () AS wgt, avg(days) AS city_avg FROM x GROUP BY pc),
  wt AS (SELECT w14, pc, avg(days) AS ward_avg, count(*) AS n FROM x GROUP BY 1, 2)
  SELECT wt.w14,
    sum(city.wgt * CASE WHEN wt.n >= 5 THEN wt.ward_avg ELSE city.city_avg END) / sum(city.wgt) AS adj_avg,
    (SELECT avg(days) FROM x WHERE x.w14 = wt.w14) AS raw_avg
  FROM wt JOIN city USING (pc) GROUP BY wt.w14 ORDER BY 1""").fetchall()
within = [dict(ward=r[0], raw_avg_days=round(r[2], 2), type_mix_adjusted_avg_days=round(r[1], 2)) for r in mix]
for r in within:
    print(f"   ward {r['ward']}: raw {r['raw_avg_days']:6.2f}  type-mix adjusted {r['type_mix_adjusted_avg_days']:6.2f}")
out['ward_map'] = dict(citystat={k or 'Null': v for k, v in WARD_MAP.items()}, variants=ward_res, best_variant=best,
                       h1_2026_by_ward=y26, within_type=within,
                       note='within-type: each ward average weighted to the citywide request-type mix; ward-type cells with <5 closures use the citywide type average')

# ---------- 2. towing (Vehicle Towing requests, quarter of DATETIMEINIT)
tow = {}
for name, flt in (('all', 'TRUE'), ('dedup_same_day', 'NOT coalesce(same_day_repeat, FALSE)'), ('distinct_id', 'rn = 1'),
                  ('street_dept', "submitto LIKE 'STREET DEPT%'"), ('resident', "callertype IN ('WEB','PHONE','EMAIL','CHAT','TWITTER','LETTER')")):
    rows = con.execute(f"""SELECT q_init,
        count(*) FILTER (status='CLOSED' AND t_closed < '2026-07-01') closed_snap,
        count(*) FILTER (t_init < '2026-07-01' AND NOT (status='CLOSED' AND t_closed < '2026-07-01')
                          AND NOT (status='CANCEL' AND (t_cancel IS NULL OR t_cancel < '2026-07-01'))) open_snap
      FROM b WHERE pc='Vehicle Towing' AND q_init IN (SELECT unnest(?::VARCHAR[])) AND {flt} GROUP BY 1 ORDER BY 1""", [QS]).fetchall()
    tow[name] = [dict(q=r[0], closed=r[1], open=r[2]) for r in rows]
    mape = sum(abs(r[1] - t) / t for r, t in zip(rows, TOWING['closed'])) / len(rows) * 100
    print(f"towing {name:15s} closed MAPE {mape:5.1f}%  closed {[r[1] for r in rows]}  open {[r[2] for r in rows]}")
print(f"   CityStat closed {TOWING['closed']} open {TOWING['open']}")
res_tow = con.execute("""SELECT q_init, count(*) FILTER (status='CLOSED') closed,
    count(*) FILTER (status='CLOSED' AND publicresolution ILIKE '%towed%') towed_text,
    count(*) FILTER (status='CLOSED' AND publicresolution ILIKE '%tagged for tow%') tagged
  FROM b WHERE pc='Vehicle Towing' AND rn = 1 AND q_init IN (SELECT unnest(?::VARCHAR[])) GROUP BY 1 ORDER BY 1""", [QS + ['2026 Q3']]).fetchall()
out['towing'] = dict(citystat=TOWING, variants=tow,
                     closure_words=[dict(q=r[0], closed=r[1], closed_vehicle_towed=r[2], closed_tagged_for_tow=r[3]) for r in res_tow])

# ---------- 3. snow (Snow/Ice - Major St + Residnl), week starting Sunday
sd_all = {}
for name, flt in (('all', 'TRUE'), ('dedup_same_day', 'NOT coalesce(same_day_repeat, FALSE)'), ('distinct_id', 'rn = 1')):
    snow = con.execute(f"""SELECT CAST(date_trunc('week', t_init + INTERVAL 1 DAY) - INTERVAL 1 DAY AS DATE) wk, count(*) n,
        count(*) FILTER (status='CLOSED') cl, avg(days) FILTER (status='CLOSED') avgd
      FROM b WHERE pc IN ('Snow/Ice - Major St','Snow/Ice - Residnl') AND t_init >= '2024-12-28' AND t_init < '2026-02-15' AND {flt}
      GROUP BY 1 ORDER BY 1""").fetchall()
    sd_all[name] = {str(r[0]): dict(n=r[1], closed=r[2], avg_days=round(r[3], 2) if r[3] is not None else None) for r in snow}
for wk, n, a in SNOW:
    o = sd_all['all'].get(wk, {}); o2 = sd_all['dedup_same_day'].get(wk, {}); o3 = sd_all['distinct_id'].get(wk, {})
    print(f"snow week {wk}: ours all n {o.get('n')} avg {o.get('avg_days')} | same-day dedup n {o2.get('n')} avg {o2.get('avg_days')} | distinct id n {o3.get('n')} avg {o3.get('avg_days')}   CityStat n {n} avg {a}")
out['snow'] = dict(citystat=[dict(week=w, n=n, avg_days=a) for w, n, a in SNOW], ours=sd_all)

# ---------- 4. CityStat's "2026 is much faster" claim, like for like: requests filed Jan-Jun of each
# year, closures counted only if they happened before 1 July of that year (the age CityStat's 2026
# figure had), vs all closures to date.
lfl = []
for y in (2024, 2025, 2026):
    r = con.execute(f"""SELECT count(*) n,
        avg(days) FILTER (status='CLOSED' AND t_closed < TIMESTAMP '{y}-07-01') avg_by_jul1,
        count(*) FILTER (status='CLOSED' AND t_closed < TIMESTAMP '{y}-07-01') closed_by_jul1,
        avg(days) FILTER (status='CLOSED') avg_all, count(*) FILTER (status='CLOSED') closed_all
      FROM b WHERE t_init >= TIMESTAMP '{y}-01-01' AND t_init < TIMESTAMP '{y}-07-01' AND rn = 1""").fetchone()
    lfl.append(dict(year=y, filed=r[0], avg_days_closures_by_jul1=round(r[1], 2), closed_by_jul1=r[2],
                    avg_days_all_closures_to_13oct2026=round(r[3], 2), closed_to_date=r[4]))
    print(f"H1 {y}: avg days counting closures by 1 Jul {r[1]:.2f} ({r[2]} of {r[0]}); all closures to date {r[3]:.2f} ({r[4]})")
out['h1_like_for_like'] = lfl
for lab in ('closed_by_0701', 'file'):
    w4 = [x for x in y26[lab] if x['ward'] == '04']
    print(f"2026 H1 ward 04 ({lab}): {w4}")
for r in out['towing']['closure_words']:
    print('towing closure words', r)

json.dump(out, open(f'{OUT}/other_metrics.json', 'w'), indent=1, default=str)
