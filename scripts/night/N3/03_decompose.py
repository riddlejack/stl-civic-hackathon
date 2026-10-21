"""N3 step 3: decompose the ward gap in CityStat's own metric (mean days to close over closed requests)
into (1) mix of request types, (2) closing practice within type (shares of closure classes),
(3) speed within the same type and closure class (split: done-class closures vs all other classes).

Two-stage Kitagawa (symmetric, exact, no residual):
  M_W = sum_t s_Wt * m_Wt          s = type share of W's closed requests, m = mean days for type t in W
  m_Wt = sum_c q_Wtc * d_Wtc       q = class share of type-t closures in W, d = mean days in that class
  M_B - M_A = sum_t (s_Bt - s_At) * avg(m_At, m_Bt)                          [type mix]
            + sum_t avg(s_At, s_Bt) * sum_c (q_Btc - q_Atc) * avg(d_Atc, d_Btc) [closing practice]
            + sum_t avg(s_At, s_Bt) * sum_c avg(q_Atc, q_Btc) * (d_Btc - d_Atc) [speed, same type and class]
  A cell present on one side only contributes all of its weight to the mix term at that level.

Scenarios: CityStat's window and population (all channels, initiated 1 Jan 2024 - 30 Jun 2026, closed by a
July 2026 snapshot) for ward 1 vs ward 10 and wards 1-5 vs 10-14; and the same with closure status as of the
file date (13 Oct 2026); and resident channels after the tornado.
Run: .venv/bin/python -I scripts/night/N3/03_decompose.py
"""
import duckdb, json, os, collections
ROOT = '.'
REQ = os.path.join(ROOT, 'build/N3/req.parquet')
con = duckdb.connect()
SCEN = {
 'citystat_window_snapshot_2026-07-10': "t_init >= '2024-01-01' AND t_init < '2026-07-01' AND t_closed < '2026-07-10'",
 'citystat_window_status_2026-10-13': "t_init >= '2024-01-01' AND t_init < '2026-07-01'",
 'resident_after_tornado_status_2026-10-13': "t_init >= '2025-05-16' AND channel = 'resident'",
}
COMPARE = {'ward 1 vs ward 10': (["'01'"], ["'10'"]),
           'wards 1-5 vs 10-14': (["'01'", "'02'", "'03'", "'04'", "'05'"], ["'10'", "'11'", "'12'", "'13'", "'14'"])}

CLASSCOL = 'class'
def cells(where, wards):
    q = f"""SELECT ptype, {CLASSCOL}, count(*) n, avg(days_close) d FROM '{REQ}'
            WHERE status_group='closed' AND {where} AND ward IN ({','.join(wards)}) GROUP BY 1,2"""
    out = collections.defaultdict(dict)
    for t, c, n, d in con.execute(q).fetchall(): out[t][c] = (n, d)
    return out

def decompose(A, B):
    NA = sum(n for t in A for n, _ in A[t].values()); NB = sum(n for t in B for n, _ in B[t].values())
    def tstats(X, N, t):
        if t not in X: return None
        nt = sum(n for n, _ in X[t].values()); return nt / N, sum(n * d for n, d in X[t].values()) / nt, nt
    MA = sum(n * d for t in A for n, d in A[t].values()) / NA
    MB = sum(n * d for t in B for n, d in B[t].values()) / NB
    mix = practice = 0.0; speed = collections.Counter(); per_type = []
    for t in set(A) | set(B):
        a, b = tstats(A, NA, t), tstats(B, NB, t)
        if a is None or b is None:
            s, m = (b if a is None else a)[:2]; sign = 1 if a is None else -1
            mix += sign * s * m; per_type.append((t, sign * s * m, 0, 0)); continue
        sA, mA, nA = a; sB, mB, nB = b
        tmix = (sB - sA) * (mA + mB) / 2; sbar = (sA + sB) / 2
        tprac = tspeed = 0.0
        for c in set(A[t]) | set(B[t]):
            ca, cb = A[t].get(c), B[t].get(c)
            qa = ca[0] / nA if ca else 0; qb = cb[0] / nB if cb else 0
            if ca and cb:
                tprac += (qb - qa) * (ca[1] + cb[1]) / 2
                sp = (qa + qb) / 2 * (cb[1] - ca[1]); tspeed += sp; speed[c] += sbar * sp
            else:
                d = (cb or ca)[1]; tprac += (qb - qa) * d
        mix += tmix; practice += sbar * tprac
        per_type.append((t, tmix, sbar * tprac, sbar * tspeed))
    per_type.sort(key=lambda r: -abs(sum(r[1:])))
    return dict(A_mean=MA, B_mean=MB, gap=MB - MA, n_A=NA, n_B=NB, type_mix=mix, closing_practice=practice,
                speed_done=speed.get('done', 0.0), speed_other=sum(v for k, v in speed.items() if k != 'done'),
                speed_by_class=dict(speed),
                check=mix + practice + sum(speed.values()),
                top_types=[dict(type=t, mix=round(a, 2), practice=round(b, 2), speed=round(c, 2)) for t, a, b, c in per_type[:12]])

results = {}
for variant, col in (('', 'class'), (' | enforcement notices as own class', 'class_enf_separate')):
  CLASSCOL = col
  for sname, where in SCEN.items():
    for cname, (wa, wb) in COMPARE.items():
        r = decompose(cells(where, wa), cells(where, wb))
        results[f'{sname} | {cname}{variant}'] = r
        print(f"\n== {sname} | {cname}{variant}")
        print(f"  mean days A {r['A_mean']:.2f} (n {r['n_A']})  B {r['B_mean']:.2f} (n {r['n_B']})  gap {r['gap']:.2f}  check {r['check']:.2f}")
        for k in ('type_mix', 'closing_practice', 'speed_done', 'speed_other'):
            print(f"  {k:18s} {r[k]:7.2f}  ({r[k] / r['gap']:.0%})")
        print('  speed by class', {k: round(v, 2) for k, v in r['speed_by_class'].items()})
        for x in r['top_types'][:8]: print('   ', x)
json.dump(results, open(os.path.join(ROOT, 'build/N3/decomposition.json'), 'w'), indent=1, default=float)
