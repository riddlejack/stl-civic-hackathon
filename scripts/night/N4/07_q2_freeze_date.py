"""N4: when did CityStat freeze its preliminary 2026 Q2 numbers? For each metric, rebuild the file as it
stood on each day from 28 Jun to 13 Oct 2026 (closures after that day ignored), count distinct closed
requests filed in Q2 (definition C), and find the day(s) whose count equals CityStat's published n.
Then compare the on-time share on that day with CityStat's published share.
Writes build/N4/q2_freeze.json.
"""
import sys, json
sys.path.insert(0, '/Users/jackriddle/Desktop/stl-civic-hackathon/scripts/night/N4')
from common import connect, OUT
from citystat_targets import METRICS

con = connect()
con.execute("""CREATE TEMP TABLE d AS SELECT * FROM (SELECT *, row_number() OVER (PARTITION BY requestid) rn
               FROM c WHERE q_init = '2026 Q2') WHERE rn = 1""")
out = {}
for k, m in METRICS.items():
    rows = con.execute("""WITH s AS (SELECT CAST(x AS TIMESTAMP) snap FROM range(TIMESTAMP '2026-06-28', TIMESTAMP '2026-10-14', INTERVAL 1 DAY) r(x))
      SELECT CAST(snap AS DATE), count(*) FILTER (status='CLOSED' AND t_closed < snap) n,
        avg((cdays <= coalesce(?, date_diff('day', CAST(t_init AS DATE), CAST(t_promise AS DATE))))::INT)
          FILTER (status='CLOSED' AND t_closed < snap) sh
      FROM s, d WHERE pc IN (SELECT unnest(?::VARCHAR[])) GROUP BY 1 ORDER BY 1""", [m['goal_days'], m['codes']]).fetchall()
    match = [r for r in rows if r[1] == m['n'][9]]
    near = min(rows, key=lambda r: (abs(r[1] - m['n'][9]), r[0]))
    out[k] = dict(citystat_n=m['n'][9], citystat_share=m['share'][9],
                  days_count_matches=[str(r[0]) for r in match],
                  nearest_day=str(near[0]), n_on_nearest=near[1], share_on_nearest=round(near[2], 4),
                  share_gap_pp_on_nearest=round((m['share'][9] - near[2]) * 100, 1),
                  final_n=rows[-1][1], final_share=round(rows[-1][2], 4))
    o = out[k]
    print(f"{k:22s} CityStat {m['n'][9]} / {m['share'][9]*100:.1f}%  count matches {o['days_count_matches'][:1]}..{o['days_count_matches'][-1:]}"
          f"  nearest {o['nearest_day']} n={near[1]} share {near[2]*100:.1f}% (CityStat minus ours {o['share_gap_pp_on_nearest']})  final {o['final_n']} / {o['final_share']*100:.1f}%")
json.dump(out, open(f'{OUT}/q2_freeze.json', 'w'), indent=1)
