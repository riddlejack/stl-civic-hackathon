"""N3 step 6: which ward comparisons survive like for like?

Resident channels, wards 1-5 vs 10-14, before (1 Jan 2024 - 15 May 2025) and after (16 May 2025 - 13 Oct 2026).
For every type with >= 300 resident requests since the tornado, and for each like-for-like measure:
  L_done   median days, done-class closures (N2 classes)
  L_text1..3  median days, closures with the same closing words (the type's three most common texts, all periods)
we compute n each side, the ratio of medians (north / south), and a bootstrap 95% interval for the ratio
(2,000 resamples, seed 7). Also (c) share done by promise and closed by promise, the per-ward check
(how many of wards 10-14 have a median above the highest of wards 1-5, wards with n >= 20) and a batch-closure
indicator (share of closures entered on a day when >= 15 closures of the type were entered in that ward group).

A comparison is called ROBUST when, for the same measure, in BOTH periods: n >= 100 each side, ratio >= 1.5,
bootstrap lower bound > 1.2; and done-by-promise (or closed-by-promise for types with < 5% done-class closures)
is lower in wards 10-14 in both periods.
Also the city's own DATEINVTDONE ('investigation done') stamp: median days from filing, any status.
Writes build/N3/robust_comparisons.csv and build/N3/robust_shortlist.json.
Run: .venv/bin/python -I scripts/night/N3/06_robust.py
"""
import duckdb, os, csv, json, collections
import numpy as np
ROOT = '.'
REQ = os.path.join(ROOT, 'build/N3/req.parquet')
ASOF = '2026-10-13'
rng = np.random.default_rng(7)
con = duckdb.connect()
con.execute(f"""CREATE VIEW r AS SELECT * FROM '{REQ}' WHERE channel='resident' AND t_init >= '2024-01-01'
                AND ward BETWEEN '01' AND '14'""")
types = [t for t, in con.execute("""SELECT ptype FROM r WHERE t_init >= '2025-05-16' GROUP BY 1 HAVING count(*) >= 300
                                    ORDER BY count(*) DESC""").fetchall()]
# batch indicator per request (all channels count toward the day's volume)
con.execute(f"""CREATE TABLE batch AS WITH d AS (
   SELECT ptype, wgroup, t_closed::date AS dday, count(*) n FROM '{REQ}' WHERE status_group='closed' AND t_init >= '2024-01-01' GROUP BY ALL)
   SELECT q.request_id, (d.n >= 15) AS big FROM '{REQ}' q JOIN d ON q.ptype=d.ptype AND q.wgroup=d.wgroup AND q.t_closed::date=d.dday
   WHERE q.status_group='closed' AND q.t_init >= '2024-01-01'""")

def boot_ratio(a, b, B=2000):
    a, b = np.asarray(a), np.asarray(b)
    if len(a) < 10 or len(b) < 10: return None, None
    ra = np.median(rng.choice(a, (B, len(a))), axis=1); rb = np.median(rng.choice(b, (B, len(b))), axis=1)
    rat = rb / np.maximum(ra, 0.01)
    return float(np.percentile(rat, 2.5)), float(np.percentile(rat, 97.5))

rows_out = []
for t in types:
    texts = [x for x, in con.execute(f"""SELECT resolution FROM r WHERE ptype=? AND status_group='closed' AND resolution IS NOT NULL
                                         GROUP BY 1 ORDER BY count(*) DESC LIMIT 3""", [t]).fetchall()]
    measures = [('done-class', "class='done'"), ('investigation-done stamp (any status)', "t_invt IS NOT NULL AND t_invt >= t_init")] + [(f'text: {x}', "resolution = " + "'" + x.replace("'", "''") + "'") for x in texts]
    for period in ('before', 'after'):
        base = f"ptype = '{t.replace(chr(39), chr(39)*2)}' AND period = '{period}'"
        prom = dict(con.execute(f"""SELECT wgroup, avg(coalesce(class='done' AND t_closed <= t_promise, false)::INT) FROM r
             WHERE {base} AND t_promise <= TIMESTAMP '{ASOF}' GROUP BY 1""").fetchall())
        cprom = dict(con.execute(f"""SELECT wgroup, avg(coalesce(status_group='closed' AND t_closed <= t_promise, false)::INT) FROM r
             WHERE {base} AND t_promise <= TIMESTAMP '{ASOF}' GROUP BY 1""").fetchall())
        done_share = dict(con.execute(f"""SELECT wgroup, avg((class='done')::INT) FROM r WHERE {base} AND status_group='closed' GROUP BY 1""").fetchall())
        open_share = dict(con.execute(f"""SELECT wgroup, avg((status_group='open')::INT) FROM r WHERE {base} GROUP BY 1""").fetchall())
        for mname, cond in measures:
            d = collections.defaultdict(list)
            inv = mname.startswith('investigation')
            val = 'epoch(t_invt - t_init)/86400.0' if inv else 'days_close'; scope = 'TRUE' if inv else "status_group='closed'"
            for g, x in con.execute(f"SELECT wgroup, {val} FROM r WHERE {base} AND {scope} AND {cond}").fetchall(): d[g].append(x)
            S, N = d.get('w01-05', []), d.get('w10-14', [])
            wm = con.execute(f"""SELECT ward, median({val}), count(*) FROM r WHERE {base} AND {scope} AND {cond}
                                 GROUP BY 1 HAVING count(*) >= 20""").fetchall()
            south_w = [m for w, m, n in wm if w <= '05']; north_w = [m for w, m, n in wm if w >= '10']
            n_north_above = sum(m > max(south_w) for m in north_w) if south_w else None
            bt = con.execute(f"""SELECT q.wgroup, avg(b.big::INT) FROM r q JOIN batch b USING (request_id)
                                 WHERE {base.replace('ptype', 'q.ptype').replace('period', 'q.period')} AND q.status_group='closed' AND {cond.replace('class', 'q.class').replace('resolution', 'q.resolution')}
                                 GROUP BY 1""").fetchall()
            bt = {} if inv else dict(bt)
            mS = float(np.median(S)) if S else None; mN = float(np.median(N)) if N else None
            lo, hi = boot_ratio(S, N)
            rows_out.append(dict(ptype=t, measure=mname, period=period, n_south=len(S), n_north=len(N),
                med_south=None if mS is None else round(mS, 1), med_north=None if mN is None else round(mN, 1),
                ratio=None if not (S and N) else round(mN / max(mS, 0.01), 2),
                ci_lo=None if lo is None else round(lo, 2), ci_hi=None if hi is None else round(hi, 2),
                wards_south_n20=len(south_w), wards_north_n20=len(north_w), north_wards_above_all_south=n_north_above,
                done_by_promise_south=round(prom.get('w01-05', 0), 3), done_by_promise_north=round(prom.get('w10-14', 0), 3),
                closed_by_promise_south=round(cprom.get('w01-05', 0), 3), closed_by_promise_north=round(cprom.get('w10-14', 0), 3),
                done_share_south=round(done_share.get('w01-05', 0), 3), done_share_north=round(done_share.get('w10-14', 0), 3),
                open_south=round(open_share.get('w01-05', 0), 3), open_north=round(open_share.get('w10-14', 0), 3),
                batch_share_south=round(bt.get('w01-05', 0) or 0, 3), batch_share_north=round(bt.get('w10-14', 0) or 0, 3)))
with open(os.path.join(ROOT, 'build/N3/robust_comparisons.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows_out[0])); w.writeheader(); w.writerows(rows_out)

# robustness rule
by = collections.defaultdict(dict)
for r in rows_out: by[(r['ptype'], r['measure'])][r['period']] = r
short = []
for (t, m), pr in by.items():
    if set(pr) != {'before', 'after'}: continue
    ok = True; why = []
    for per in ('before', 'after'):
        r = pr[per]
        low_done = (r['done_share_south'] < 0.05 or r['done_share_north'] < 0.05)
        promise_gap = (r['closed_by_promise_north'] < r['closed_by_promise_south']) if low_done else (r['done_by_promise_north'] < r['done_by_promise_south'])
        c1 = r['n_south'] >= 100 and r['n_north'] >= 100; c2 = (r['ratio'] or 0) >= 1.5; c3 = (r['ci_lo'] or 0) > 1.2
        if not (c1 and c2 and c3 and promise_gap): ok = False
        why.append(f"{per}: n {r['n_south']}/{r['n_north']}, median {r['med_south']} vs {r['med_north']} (x{r['ratio']}, CI {r['ci_lo']}-{r['ci_hi']}), "
                   f"done-by-promise {r['done_by_promise_south']:.0%} vs {r['done_by_promise_north']:.0%}, closed-by-promise "
                   f"{r['closed_by_promise_south']:.0%} vs {r['closed_by_promise_north']:.0%}, north wards above all south {r['north_wards_above_all_south']}/{r['wards_north_n20']}")
    if ok: short.append(dict(ptype=t, measure=m, evidence=why))
    # also print near-misses: after-only robust
    elif all(k in pr for k in ('after',)):
        r = pr['after']
        if r['n_south'] >= 100 and r['n_north'] >= 100 and (r['ratio'] or 0) >= 1.5 and (r['ci_lo'] or 0) > 1.2:
            short.append(dict(ptype=t, measure=m, evidence=why, note='after-tornado only (fails before)'))
json.dump(short, open(os.path.join(ROOT, 'build/N3/robust_shortlist.json'), 'w'), indent=1)
for s in short:
    print(f"\n{s['ptype']} | {s['measure']} {s.get('note', 'ROBUST')}")
    for e in s['evidence']: print('   ', e)
