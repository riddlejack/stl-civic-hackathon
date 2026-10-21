"""N3 step 5: like-for-like table. For every request type with >= 300 resident-channel requests initiated on or
after 16 May 2025: per ward and per ward group, before (1 Jan 2024 - 15 May 2025) and after (16 May 2025 - file
date) the tornado:
  (a) median days to close, all closures; (b) median days, done-class closures;
  (c) share done by the city's own promised date (PRJCOMPLETEDATE): done-class closure on or before the promise,
      denominator = every request whose promise date has passed by the file date (open, cancelled, handed-off and
      no-action all count as not done); also closed-by-promise in any class, for contrast;
  (d) open share; (e) hand-off share of closures (handed_off; converted reported separately); no-action share;
  plus median days of hand-off closures and of the type's most common closing text.
Writes build/N3/like_for_like_by_group.csv and build/N3/like_for_like_by_ward.csv.
Run: .venv/bin/python -I scripts/night/N3/05_type_tables.py
"""
import duckdb, os, csv
ROOT = '.'
REQ = os.path.join(ROOT, 'build/N3/req.parquet')
ASOF = '2026-10-13'
con = duckdb.connect()
con.execute(f"""CREATE VIEW r AS SELECT * FROM '{REQ}' WHERE channel='resident' AND t_init >= '2024-01-01'
                AND ward BETWEEN '01' AND '14'""")
types = [t for t, in con.execute("""SELECT ptype FROM r WHERE t_init >= '2025-05-16' GROUP BY 1 HAVING count(*) >= 300
                                    ORDER BY count(*) DESC""").fetchall()]
print(len(types), 'types:', types)
con.execute("CREATE TABLE types AS SELECT unnest(?) AS ptype", [types])
# modal closing text per type (after the tornado, resident)
con.execute("""CREATE TABLE modal AS SELECT ptype, arg_max(resolution, n) AS modal_text FROM
               (SELECT ptype, resolution, count(*) n FROM r WHERE status_group='closed' AND resolution IS NOT NULL GROUP BY 1,2)
               GROUP BY 1""")
METRICS = f"""
  count(*) AS n,
  count(*) FILTER (WHERE status_group='closed') AS n_closed,
  round(avg((status_group='open')::INT), 3) AS open_share,
  round(avg((status_group='cancelled')::INT), 3) AS cancel_share,
  round(quantile_cont(days_close, 0.5) FILTER (WHERE status_group='closed'), 1) AS med_all,
  count(*) FILTER (WHERE class='done') AS n_done,
  round(quantile_cont(days_close, 0.5) FILTER (WHERE class='done'), 1) AS med_done,
  round(avg((class='handed_off')::INT) FILTER (WHERE status_group='closed'), 3) AS handoff_share,
  round(avg((class='converted')::INT) FILTER (WHERE status_group='closed'), 3) AS converted_share,
  round(avg((class='no_action')::INT) FILTER (WHERE status_group='closed'), 3) AS noaction_share,
  round(avg((class='done')::INT) FILTER (WHERE status_group='closed'), 3) AS done_share_of_closed,
  count(*) FILTER (WHERE class='handed_off') AS n_handoff,
  round(quantile_cont(days_close, 0.5) FILTER (WHERE class='handed_off'), 1) AS med_handoff,
  count(*) FILTER (WHERE resolution = m.modal_text AND status_group='closed') AS n_modal,
  round(quantile_cont(days_close, 0.5) FILTER (WHERE resolution = m.modal_text AND status_group='closed'), 1) AS med_modal,
  round(quantile_cont(promise_days, 0.5), 1) AS promise_days_median,
  count(*) FILTER (WHERE t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{ASOF}') AS n_promise_passed,
  round(avg(coalesce(class='done' AND t_closed <= t_promise, false)::INT) FILTER (WHERE t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{ASOF}'), 3) AS done_by_promise,
  round(avg(coalesce(status_group='closed' AND t_closed <= t_promise, false)::INT) FILTER (WHERE t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{ASOF}'), 3) AS closed_by_promise
"""
for unit, col in (('group', 'wgroup'), ('ward', 'ward')):
    q = f"""SELECT r.ptype, m.modal_text, r.period, r.{col} AS unit, {METRICS}
            FROM r JOIN types USING (ptype) LEFT JOIN modal m USING (ptype)
            GROUP BY ALL ORDER BY r.ptype, r.period DESC, unit"""
    res = con.execute(q); cols = [d[0] for d in res.description]; rows = res.fetchall()
    with open(os.path.join(ROOT, f'build/N3/like_for_like_by_{unit}.csv'), 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(cols); w.writerows(rows)
    print(unit, len(rows), 'rows')
