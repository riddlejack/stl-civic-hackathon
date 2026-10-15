"""N3 step 1: reproduce CityStat's CSBRequestMap ward averages (avg days to close, requests, closed, closed share,
2024-01-01 to 2026-06-30) from the public 311 file, trying several definitions, and report which gets closest.

CityStat values are from data/raw/citystat/tableau-extract.md (extracted 13 Oct 2026).
Run: .venv/bin/python -I scripts/night/N3/01_citystat_ward.py
"""
import duckdb, json, os
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
PQ = os.path.join(ROOT, 'build/N3/csb.parquet')
CITYSTAT = {  # ward: (avg days, requests, closed)
 '01': (17.18, 23417, 19603), '02': (19.44, 21712, 17364), '03': (22.77, 19074, 16543), '04': (19.69, 21251, 17484),
 '05': (19.91, 19340, 15363), '06': (27.76, 18280, 14384), '07': (27.44, 22822, 18786), '08': (27.89, 20313, 16551),
 '09': (32.59, 12206, 9966), '10': (35.07, 19467, 15218), '11': (30.67, 16361, 13816), '12': (30.33, 25722, 21626),
 '13': (24.32, 28423, 24319), '14': (27.54, 17034, 14600)}
con = duckdb.connect()
con.execute(f"CREATE VIEW r AS SELECT * FROM '{PQ}'")

# definitions to try. each returns ward, requests, closed, avg_days
DEFS = {
 'A all channels, init in window, closed=STATUS CLOSED, mean days over closed':
   """SELECT ward, count(*) n, count(*) FILTER (WHERE status_group='closed') nc,
      avg(epoch(t_closed - t_init)/86400) FILTER (WHERE status_group='closed') avgd
      FROM r WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01' GROUP BY ward""",
 'B as A but closed = any DATETIMECLOSED (incl. status not CLOSED)':
   """SELECT ward, count(*) n, count(t_closed) nc, avg(epoch(t_closed - t_init)/86400) avgd
      FROM r WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01' GROUP BY ward""",
 'C as A, excluding auto-closed logging types (closed within 1 minute)':
   """SELECT ward, count(*) n, count(*) FILTER (WHERE status_group='closed') nc,
      avg(epoch(t_closed - t_init)/86400) FILTER (WHERE status_group='closed') avgd
      FROM r WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01'
      AND NOT (status_group='closed' AND epoch(t_closed - t_init) < 60) GROUP BY ward""",
 'D as A, closed requests with closed date <= 2026-06-30 only':
   """SELECT ward, count(*) n, count(*) FILTER (WHERE status_group='closed' AND t_closed < '2026-07-01') nc,
      avg(epoch(t_closed - t_init)/86400) FILTER (WHERE status_group='closed' AND t_closed < '2026-07-01') avgd
      FROM r WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01' GROUP BY ward""",
 'E resident channels only, as A':
   """SELECT ward, count(*) n, count(*) FILTER (WHERE status_group='closed') nc,
      avg(epoch(t_closed - t_init)/86400) FILTER (WHERE status_group='closed') avgd
      FROM r WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01' AND channel='resident' GROUP BY ward""",
 'F as A, days = DATETIMECLOSED date minus DATETIMEINIT date (whole days)':
   """SELECT ward, count(*) n, count(*) FILTER (WHERE status_group='closed') nc,
      avg(datediff('day', t_init::date, t_closed::date)) FILTER (WHERE status_group='closed') avgd
      FROM r WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01' GROUP BY ward""",
 'G as A, closed = STATUS CLOSED or CANCEL (cancel date as close)':
   """SELECT ward, count(*) n, count(*) FILTER (WHERE status_group IN ('closed','cancelled')) nc,
      avg(epoch(coalesce(t_closed, t_cancel) - t_init)/86400) FILTER (WHERE status_group IN ('closed','cancelled')) avgd
      FROM r WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01' GROUP BY ward""",
}
results = {}
for name, sql in DEFS.items():
    rows = {w: (n, nc, a) for w, n, nc, a in con.execute(sql).fetchall() if w in CITYSTAT}
    err_avg = sum(abs(rows[w][2] - CITYSTAT[w][0]) for w in CITYSTAT) / 14
    err_n = sum(abs(rows[w][0] - CITYSTAT[w][1]) / CITYSTAT[w][1] for w in CITYSTAT) / 14
    err_nc = sum(abs(rows[w][1] - CITYSTAT[w][2]) / CITYSTAT[w][2] for w in CITYSTAT) / 14
    results[name] = dict(mean_abs_err_avg_days=round(err_avg, 2), mean_rel_err_requests=round(err_n, 4),
                         mean_rel_err_closed=round(err_nc, 4),
                         ward01=[rows['01'][0], rows['01'][1], round(rows['01'][2], 2)],
                         ward10=[rows['10'][0], rows['10'][1], round(rows['10'][2], 2)],
                         per_ward={w: [rows[w][0], rows[w][1], round(rows[w][2], 2)] for w in sorted(rows)})
    print(f"\n{name}\n  mean |avg days err| {err_avg:.2f}; mean rel err requests {err_n:.3%}; closed {err_nc:.3%}")
    print('  ward  ours(n, closed, avg)   citystat(avg, n, closed)')
    for w in sorted(CITYSTAT):
        print(f"  {w}  {rows[w][0]:6d} {rows[w][1]:6d} {rows[w][2]:6.2f}   {CITYSTAT[w][0]:6.2f} {CITYSTAT[w][1]:6d} {CITYSTAT[w][2]:6d}")
tot = con.execute("SELECT count(*), count(*) FILTER (WHERE status_group='closed') FROM r WHERE t_init >= '2024-01-01' AND t_init < '2026-07-01'").fetchone()
print('\nall wards incl. null:', tot, ' CityStat total 286,148 / 236,155')
json.dump(results, open(os.path.join(ROOT, 'build/N3/citystat_reproduction.json'), 'w'), indent=1)
