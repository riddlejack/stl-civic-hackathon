"""N3 step 4: robustness of the decomposition.
(i) Same Kitagawa decomposition on days capped at 90 (mean of min(days, 90)), so long tails cannot drive it.
(ii) Median version by reweighting (DiNardo-Fortin-Lemieux style, sequential): ward B's median as observed;
     reweighted to ward A's type mix; reweighted to ward A's type x class mix; the remainder vs ward A's median
     is speed within the same type and class.
(iii) The (type, class) cells that carry the speed term in CityStat's mean.
Run: .venv/bin/python -I scripts/night/N3/04_reweight.py
"""
import duckdb, json, os, collections, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
REQ = os.path.join(ROOT, 'build/N3/req.parquet')
con = duckdb.connect()
W_CS = "t_init >= '2024-01-01' AND t_init < '2026-07-01' AND t_closed < '2026-07-10'"
W_RA = "t_init >= '2025-05-16' AND channel = 'resident'"
COMP = {'ward 1 vs ward 10': ("('01')", "('10')"), 'wards 1-5 vs 10-14': ("('01','02','03','04','05')", "('10','11','12','13','14')")}

def wmedian(x, w):
    o = np.argsort(x); x, w = x[o], w[o]; c = np.cumsum(w); return float(x[np.searchsorted(c, c[-1] / 2)])

def fetch(where, wards):
    return con.execute(f"SELECT ptype, class, days_close FROM '{REQ}' WHERE status_group='closed' AND {where} AND ward IN {wards}").fetchall()

out = {}
for sname, where in {'citystat_window_snapshot': W_CS, 'resident_after_tornado': W_RA}.items():
    for cname, (wa, wb) in COMP.items():
        A, B = fetch(where, wa), fetch(where, wb)
        nA, nB = len(A), len(B)
        tA = collections.Counter(t for t, _, _ in A); tB = collections.Counter(t for t, _, _ in B)
        cA = collections.Counter((t, c) for t, c, _ in A); cB = collections.Counter((t, c) for t, c, _ in B)
        xB = np.array([d for _, _, d in B]); xA = np.array([d for _, _, d in A])
        # weights: reweight B to A's type mix (types absent in B are lost: report coverage)
        w1 = np.array([(tA[t] / nA) / (tB[t] / nB) for t, _, _ in B])
        w2 = np.array([(cA[(t, c)] / nA) / (cB[(t, c)] / nB) for t, c, _ in B])
        cov1 = sum(tA[t] for t in tA if t in tB) / nA; cov2 = sum(cA[k] for k in cA if k in cB) / nA
        r = dict(median_A=float(np.median(xA)), median_B=float(np.median(xB)),
                 median_B_at_A_type_mix=wmedian(xB, w1), median_B_at_A_type_class_mix=wmedian(xB, w2),
                 coverage_type=cov1, coverage_type_class=cov2,
                 capped90_mean_A=float(np.minimum(xA, 90).mean()), capped90_mean_B=float(np.minimum(xB, 90).mean()),
                 capped90_mean_B_at_A_type_mix=float((np.minimum(xB, 90) * w1).sum() / w1.sum()),
                 capped90_mean_B_at_A_type_class_mix=float((np.minimum(xB, 90) * w2).sum() / w2.sum()),
                 mean_A=float(xA.mean()), mean_B=float(xB.mean()),
                 mean_B_at_A_type_mix=float((xB * w1).sum() / w1.sum()),
                 mean_B_at_A_type_class_mix=float((xB * w2).sum() / w2.sum()))
        out[f'{sname} | {cname}'] = r
        print(f"\n== {sname} | {cname}  (coverage of A's closures by B's cells: type {cov1:.1%}, type x class {cov2:.1%})")
        for m in ('median', 'capped90_mean', 'mean'):
            a, b = r[f'{m}_A'], r[f'{m}_B']; b1 = r[f'{m}_B_at_A_type_mix']; b2 = r[f'{m}_B_at_A_type_class_mix']
            g = b - a
            print(f"  {m:14s} A {a:6.2f}  B {b:6.2f}  gap {g:6.2f} | B at A's type mix {b1:6.2f} (mix {b - b1:+.2f})"
                  f" | B at A's type x class mix {b2:6.2f} (practice {b1 - b2:+.2f}) | left = speed {b2 - a:+.2f} ({(b2 - a) / g:.0%})")

# (iii) cells carrying the speed term, CityStat window, ward 1 vs 10
q = f"""WITH c AS (SELECT ward, ptype, class, count(*) n, avg(days_close) d, median(days_close) md FROM '{REQ}'
        WHERE status_group='closed' AND {W_CS} AND ward IN ('01','10') GROUP BY ALL),
     t AS (SELECT ward, ptype, sum(n) nt FROM c GROUP BY ALL),
     w AS (SELECT ward, sum(n) nw FROM c GROUP BY ALL)
SELECT a.ptype, a.class, a.n, round(a.d,1), round(a.md,1), b.n, round(b.d,1), round(b.md,1),
   ((ta.nt/wa.nw + tb.nt/wb.nw)/2) * ((a.n/ta.nt + b.n/tb.nt)/2) * (b.d - a.d) AS contrib
FROM c a JOIN c b ON a.ptype=b.ptype AND a.class=b.class AND a.ward='01' AND b.ward='10'
JOIN t ta ON ta.ward='01' AND ta.ptype=a.ptype JOIN t tb ON tb.ward='10' AND tb.ptype=b.ptype
JOIN w wa ON wa.ward='01' JOIN w wb ON wb.ward='10' ORDER BY contrib DESC LIMIT 15"""
print('\nspeed cells, ward 1 vs 10 (type, class, n1, mean1, median1, n10, mean10, median10, contribution days)')
cells = con.execute(q).fetchall()
for r in cells: print('  ', r[:8], round(r[8], 2))
out['speed_cells_ward1_vs_ward10'] = [dict(type=r[0], cls=r[1], n1=r[2], mean1=r[3], med1=r[4], n10=r[5], mean10=r[6], med10=r[7], contrib_days=round(r[8], 2)) for r in cells]
json.dump(out, open(os.path.join(ROOT, 'build/N3/decomposition_robustness.json'), 'w'), indent=1)
