"""N4 step 3: which subset of the 311 file reproduces CityStat's CSB routing counts
(10,664 ... 10,853 requests per quarter, 2024 Q1 - 2026 Q2)?

Counted once per distinct REQUESTID (the file repeats a request once per caller; the first copy's
caller type is used). Search: every union of caller-type groups x every union of GRANDPARENT_NODE values
(quarter of DATETIMEINIT), scored by mean absolute percentage error over the 10 quarters.
Also tests single-axis candidates (status, has DATEINVTDONE, Nuisance logging excluded).
The file has no routing timestamp, so the share routed within 2.5 days cannot be
recomputed; DATEINVTDONE - DATETIMEINIT is tested as a proxy and reported as such.
Writes build/N4/routing_search.json.
"""
import sys, json, itertools, collections
sys.path.insert(0, '/Users/jackriddle/Desktop/stl-civic-hackathon/scripts/night/N4')
from common import connect, OUT
from citystat_targets import ROUTING, QS

con = connect()
CT = ['WEB', 'PHONE', 'NSO', 'INDETERMINATE', 'NULL', 'EMAIL', 'TWITTER', 'CHAT', 'OTHER']
rows = con.execute("""
  SELECT q_init,
    CASE WHEN callertype IS NULL THEN 'NULL'
         WHEN callertype IN ('WEB','PHONE','NSO','INDETERMINATE','EMAIL','TWITTER','CHAT') THEN callertype
         ELSE 'OTHER' END ct,
    coalesce(grandparent_node,'NULL') gp,
    (grp = 'Nuisance Complaint') nuis,
    count(*) n
  FROM (SELECT *, row_number() OVER (PARTITION BY requestid ORDER BY callertype NULLS LAST) rn FROM c) WHERE rn = 1
    AND q_init IN (SELECT unnest(?::VARCHAR[])) GROUP BY ALL""", [QS]).fetchall()
GP = sorted({r[2] for r in rows})
cube = collections.defaultdict(int)
for q, ct, gp, nuis, n in rows:
    cube[(q, ct, gp, nuis)] += n
target = ROUTING['n']


def seq(cts, gps, drop_nuis):
    return [sum(v for (q2, ct, gp, nu), v in cube.items() if q2 == q and ct in cts and gp in gps and not (drop_nuis and nu)) for q in QS]


def mape(s):
    return sum(abs(a - b) / b for a, b in zip(s, target)) / len(target) * 100

# pre-aggregate for speed
idx = {q: i for i, q in enumerate(QS)}
arr = collections.defaultdict(lambda: [0] * len(QS))
for (q, ct, gp, nu), v in cube.items():
    arr[(ct, gp, nu)][idx[q]] += v
res = []
for k in range(1, len(CT) + 1):
    for cts in itertools.combinations(CT, k):
        for m in range(1, len(GP) + 1):
            for gps in itertools.combinations(GP, m):
                for drop in (False, True):
                    s = [0] * len(QS)
                    for ct in cts:
                        for gp in gps:
                            for nu in ((False,) if drop else (False, True)):
                                a = arr.get((ct, gp, nu))
                                if a:
                                    s = [x + y for x, y in zip(s, a)]
                    res.append((mape(s), cts, gps, drop, s))
res.sort(key=lambda r: r[0])
print('CityStat routing n:', target)
for r in res[:15]:
    print(f'MAPE {r[0]:5.1f}%  ct={"+".join(r[1])}  gp={"+".join(r[2])}  drop_nuisance={r[3]}  {r[4]}')
whole = [sum(v for (q2, *_), v in cube.items() if q2 == q) for q in QS]
print('whole file', whole, f'MAPE {mape(whole):.1f}%')
# proxy for routing time: DATEINVTDONE - DATETIMEINIT <= 2.5 days among requests that have it
proxy = con.execute("""SELECT q_init, count(*) FILTER (t_invtdone IS NOT NULL) n,
   avg((epoch(t_invtdone - t_init)/86400 <= 2.5)::INT) FILTER (t_invtdone IS NOT NULL) AS sh
   FROM c WHERE q_init IN (SELECT unnest(?::VARCHAR[])) GROUP BY 1 ORDER BY 1""", [QS]).fetchall()
print('proxy DATEINVTDONE within 2.5 days:', [(q, n, round(s, 3)) for q, n, s in proxy])
json.dump(dict(citystat=ROUTING, whole_file=whole, whole_file_mape=mape(whole),
               top=[dict(mape=r[0], callertypes=r[1], grandparent_nodes=r[2], drop_nuisance=r[3], counts=r[4]) for r in res[:50]],
               combos_tested=len(res),
               invtdone_proxy=[dict(q=q, n=n, share_le_2_5d=s) for q, n, s in proxy]),
          open(f'{OUT}/routing_search.json', 'w'), indent=1)
