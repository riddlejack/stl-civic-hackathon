"""N4 step 4: promises kept. For every request type with >= 300 requests filed 1 Jan 2025 - 13 Oct 2026:
  promise    : PRJCOMPLETEDATE - DATETIMEINIT, the city's own per-request due date (modal offset, days)
  scored     : requests whose promise date had passed by the file's end and that were not cancelled
  kept       : closed at or before the promise date (any closing words)
  done-kept  : closed at or before the promise date with closing words N2 classes as "done"
  late       : closed after the promise date; median days late
  overdue    : still open with the promise date passed; median days overdue at 13 Oct 2026
Closing-word classes come from research/chapters/N2-closure-classes.csv (N2, written tonight),
joined on (raw PROBLEMCODE incl. trailing spaces, trimmed PUBLICRESOLUTION), falling back to N2's text-only map
build/N2/text-classes.csv on lower-cased whitespace-collapsed text. If N2's file is absent,
the column is left empty (no provisional rule set was needed: the file existed when this ran).
One row per distinct REQUESTID: the published file repeats a request once per caller (identical
except CALLERTYPE); a request counts as resident-channel if any copy is. No staff or personal fields are output (SUBMITTO is not used: it sometimes holds a person's name).
Writes build/N4/scoreboard.json and build/N4/scoreboard.csv.
"""
import sys, os, csv, json, re, datetime as dt
sys.path.insert(0, './scripts/night/N4')
from common import connect, OUT, ROOT
from citystat_targets import METRICS

N2_CSV = f'{ROOT}/research/chapters/N2-closure-classes.csv'
N2_TEXT = f'{ROOT}/build/N2/text-classes.csv'
CUT = dt.datetime(2026, 10, 13, 0, 33)  # last DATETIMEINIT in the file
CITYSTAT_GOALS = {c: (k, m['goal_days']) for k, m in METRICS.items() if m['goal_days'] for c in m['codes']}

con = connect()
n2_info = {}
if os.path.exists(N2_CSV):
    con.execute(f"""CREATE TABLE n2 AS SELECT PROBLEMCODE pcraw, resolution_text txt, class FROM read_csv('{N2_CSV}', header=true, all_varchar=true, strict_mode=false)""")
    n2_info['pair_rows'] = con.execute("SELECT count(*) FROM n2").fetchone()[0]
    n2_info['mtime'] = dt.datetime.fromtimestamp(os.path.getmtime(N2_CSV)).isoformat(timespec='seconds')
    if os.path.exists(N2_TEXT):
        con.execute(f"""CREATE TABLE n2t AS SELECT resolution_text_normalised t, class FROM read_csv('{N2_TEXT}', header=true, all_varchar=true)""")
    else:
        con.execute("CREATE TABLE n2t (t VARCHAR, class VARCHAR)")
    cls_sql = """coalesce(
        (SELECT any_value(class) FROM n2 WHERE n2.pcraw = x.problemcode AND coalesce(n2.txt,'') = coalesce(trim(x.publicresolution),'')),
        (SELECT any_value(class) FROM n2t WHERE n2t.t = lower(regexp_replace(trim(coalesce(x.publicresolution,'')), '\\s+', ' ', 'g'))),
        'unclassed')"""
else:
    cls_sql = "NULL"
    n2_info['missing'] = True

con.execute(f"""CREATE TEMP TABLE s AS
  SELECT x.*, CASE WHEN x.status = 'CLOSED' THEN {cls_sql} END AS cls
  FROM (SELECT *, row_number() OVER (PARTITION BY requestid ORDER BY callertype NULLS LAST) AS rn,
               bool_or(callertype IN ('WEB','PHONE','EMAIL','CHAT','TWITTER','LETTER')) OVER (PARTITION BY requestid) AS any_res
        FROM c WHERE t_init >= '2025-01-01') x
  WHERE x.rn = 1""")
types = con.execute("""SELECT pc, any_value(plain_name), any_value(grp), count(*) n FROM s GROUP BY pc HAVING count(*) >= 300 ORDER BY n DESC""").fetchall()
rows = []
for pc, plain, grp, n in types:
    r = con.execute(f"""
      WITH t AS (SELECT *, round(promise_days, 1) pd FROM s WHERE pc = ?),
      mode_pd AS (SELECT mode(pd) m FROM t WHERE pd IS NOT NULL)
      SELECT
        count(*) FILTER (t_promise IS NOT NULL) has_promise,
        (SELECT m FROM mode_pd) promise_mode,
        avg((abs(pd - (SELECT m FROM mode_pd)) <= 0.05)::INT) FILTER (pd IS NOT NULL) promise_at_mode,
        count(*) FILTER (status = 'CANCEL') cancelled,
        count(*) FILTER (t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{CUT}' AND status <> 'CANCEL') scored,
        count(*) FILTER (t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{CUT}' AND status = 'CLOSED' AND t_closed <= t_promise) kept,
        count(*) FILTER (t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{CUT}' AND status = 'CLOSED' AND t_closed <= t_promise AND cls = 'done') done_kept,
        count(*) FILTER (t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{CUT}' AND status = 'CLOSED' AND t_closed > t_promise) late,
        median(epoch(t_closed - t_promise) / 86400) FILTER (t_promise IS NOT NULL AND status = 'CLOSED' AND t_closed > t_promise) med_late,
        count(*) FILTER (t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{CUT}' AND status NOT IN ('CLOSED', 'CANCEL')) overdue_open,
        median(epoch(TIMESTAMP '{CUT}' - t_promise) / 86400) FILTER (t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{CUT}' AND status NOT IN ('CLOSED', 'CANCEL')) med_overdue,
        median(days) FILTER (status = 'CLOSED') med_days_closed,
        count(*) FILTER (status = 'CLOSED') closed,
        count(*) FILTER (status = 'CLOSED' AND cls = 'done') closed_done,
        count(*) FILTER (status = 'CLOSED' AND cls IN ('handed_off', 'converted')) closed_handed,
        count(*) FILTER (status = 'CLOSED' AND cls = 'no_action') closed_noaction,
        count(*) FILTER (status = 'CLOSED' AND cls IN ('blank', 'info_other', 'unclassed')) closed_other,
        count(*) FILTER (status = 'CLOSED' AND cls = 'unclassed') closed_unclassed,
        count(*) FILTER (t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{CUT}' AND status <> 'CANCEL'
                         AND any_res) scored_res,
        count(*) FILTER (t_promise IS NOT NULL AND t_promise <= TIMESTAMP '{CUT}' AND status = 'CLOSED' AND t_closed <= t_promise
                         AND any_res) kept_res
      FROM t""", [pc]).fetchone()
    (has_p, pmode, p_at_mode, canc, scored, kept, done_kept, late, med_late, od, med_od, med_days, closed,
     cdone, chand, cnoact, cother, cuncl, scored_res, kept_res) = r
    pct = lambda a, b: round(a / b, 4) if b else None
    cs = CITYSTAT_GOALS.get(pc)
    rows.append(dict(
        problemcode=pc, name=plain, category=grp, requests_2025_26=n,
        promise_populated_share=pct(has_p, n), promise_days=pmode, promise_fixed_share=round(p_at_mode, 3) if p_at_mode is not None else None,
        cancelled_share=pct(canc, n), scored=scored,
        kept_share=pct(kept, scored), done_kept_share=pct(done_kept, scored) if cls_sql != 'NULL' else None,
        late_share=pct(late, scored), median_days_late=round(med_late, 1) if med_late is not None else None,
        open_past_promise=od, open_past_promise_share=pct(od, scored), median_days_overdue=round(med_od, 1) if med_od is not None else None,
        median_days_to_close=round(med_days, 2) if med_days is not None else None,
        closed=closed, closed_done_share=pct(cdone, closed), closed_handed_off_share=pct(chand, closed),
        closed_no_action_share=pct(cnoact, closed), closed_other_share=pct(cother, closed), closed_unclassed=cuncl,
        resident_scored=scored_res, resident_kept_share=pct(kept_res, scored_res),
        citystat_metric=cs[0] if cs else None, citystat_goal_days=cs[1] if cs else None,
        promise_applies=bool(has_p / n >= 0.5),
        derivation=(f"311 requests (city open data, csb.zip, cleaned of invalid bytes, one row per request number) of type '{pc}' filed 1 Jan 2025 to 13 Oct 2026; "
                    f"each graded against its own PRJCOMPLETEDATE, the due date the city's system stamps on it ({pmode} days after filing on {round((p_at_mode or 0)*100)}% of rows), "
                    f"counting only requests whose due date had passed and that were not cancelled ({scored} of {n}). "
                    + ("Closing words classed done/handed off/no action by N2's rule set (research/chapters/N2-closure-classes.csv)." if cls_sql != 'NULL' else "No closing-word classes applied.")
                    + ("" if has_p / n >= 0.5 else " Fewer than half of these requests carry a due date, so the grade does not apply."))))
rows.sort(key=lambda d: -d['requests_2025_26'])
meta = dict(window='requests filed 2025-01-01 to 2026-10-13 (311 CSV, cleaned copy build/csb-clean), one row per distinct REQUESTID',
            scored_definition='promise date (PRJCOMPLETEDATE) on or before 2026-10-13 00:33 and status not CANCEL',
            kept='STATUS CLOSED and DATETIMECLOSED <= PRJCOMPLETEDATE',
            done_kept='kept, and the closing words are classed "done" by N2 (research/chapters/N2-closure-classes.csv)',
            n2=n2_info, label='observed (computed from the public file); done class is N2\'s rule set',
            types=len(rows))
json.dump(dict(meta=meta, rows=rows), open(f'{OUT}/scoreboard.json', 'w'), indent=1, default=str)
with open(f'{OUT}/scoreboard.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(json.dumps(meta, indent=1))
f = lambda v: '' if v is None else (f'{v*100:5.1f}%' if isinstance(v, float) and v <= 1 else str(v))
print(f"{'type':22s} {'n':>6s} {'prom':>5s} {'fix':>5s} {'scored':>6s} {'kept':>6s} {'done':>6s} {'mdlate':>6s} {'overdue':>7s} {'canc':>6s} {'uncl':>5s}")
for d in rows:
    print(f"{d['problemcode'][:22]:22s} {d['requests_2025_26']:6d} {str(d['promise_days']):>5s} {f(d['promise_fixed_share']):>6s} {d['scored']:6d} {f(d['kept_share']):>6s} {f(d['done_kept_share']):>6s} {str(d['median_days_late']):>6s} {d['open_past_promise']:7d} {f(d['cancelled_share']):>6s} {d['closed_unclassed']:5d}")
