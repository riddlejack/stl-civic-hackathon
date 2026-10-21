"""N4 step 1: for every CityStat metric that rests on 311 data, try candidate definitions and
score each against CityStat's published quarterly share and count (2024 Q1 - 2026 Q2).

Definition axes:
  snap   : the date the data were frozen. 'none' = file as downloaded 13 Oct 2026;
           '0701' = only closures before 1 Jul 2026 count (CityStat says "last updated June 30");
           '0801' = before 1 Aug 2026 ("validated Q2 data available on August 1st").
  dedup  : None = every row as published (the file repeats a request once per caller);
           'id' = one row per distinct REQUESTID; W (0 = same calendar day, 1, 3, 7, 14, 30) = drop
           a row if an earlier row with the same PROBADDRESS and problem code was filed within W
           days; 'idW' = distinct REQUESTID first, then the same W-day rule between requests.
  denom  : 'closed' = closed requests only (by snap);
           'notcanc' = closed + still open (open counts as late), cancelled excluded;
           'all' = every request initiated in the quarter (cancelled and open count as late).
  rule   : 'frac' fractional days <= goal; 'cd' calendar-date difference <= goal;
           'cdlt' calendar-date difference < goal; 'bd' weekdays <= goal; 'prom' closed by
           PRJCOMPLETEDATE (the city's own per-request promise date).
  chan   : 'any' or 'res' (resident channels only; NSO and INDETERMINATE dropped).
  qbasis : quarter of DATETIMEINIT ('init') or of DATETIMECLOSED ('closed', closed requests only).
Writes build/N4/definition_search.json (every combination, every metric) and prints the top 5.
Run: .venv/bin/python -I scripts/night/N4/01_definition_search.py
"""
import sys, json, itertools, datetime as dt, collections
sys.path.insert(0, './scripts/night/N4')
from common import connect, OUT
from citystat_targets import METRICS, QS

SNAPS = {'none': None, '0701': dt.datetime(2026, 7, 1), '0801': dt.datetime(2026, 8, 1)}
DEDUPS = [None, 0, 1, 3, 7, 14, 30, 'id', 'id0', 'id1', 'id7', 'id30']
DENOMS = ['closed', 'notcanc', 'all']
RULES = ['frac', 'cd', 'cdlt', 'bd', 'prom']
CHANS = ['any', 'res']
QBASES = ['init', 'closed']  # quarter of DATETIMEINIT or of DATETIMECLOSED
RES = {'WEB', 'PHONE', 'EMAIL', 'CHAT', 'TWITTER', 'LETTER'}


def load(con, codes):
    """One tuple per ROW of the published file. The file repeats a request once per caller
    (same REQUESTID, identical except CALLERTYPE), so rn numbers the copies of each REQUESTID and
    any_res says whether any copy came in through a resident channel."""
    return con.execute("""
      SELECT requestid, q_init, t_init, t_closed, t_cancel, status, probaddress, days, cdays, bdays,
             t_promise, callertype, pc, promise_days,
             date_diff('day', CAST(t_init AS DATE), CAST(t_promise AS DATE)) AS promise_cdays, q_closed,
             row_number() OVER (PARTITION BY requestid ORDER BY callertype NULLS LAST) AS rn,
             bool_or(callertype IN ('WEB','PHONE','EMAIL','CHAT','TWITTER','LETTER')) OVER (PARTITION BY requestid) AS any_res
      FROM c WHERE pc IN (SELECT unnest(?::VARCHAR[])) AND t_init >= '2023-09-01'
      ORDER BY probaddress, pc, t_init, requestid""", [codes]).fetchall()


def prev_gap(rows):
    """Two gap lists aligned with rows (days since the previous row / previous distinct request at
    the same address and problem code; 0 if the same calendar day; None if first):
      'row' : over every row of the file (a caller copy of the same request has gap 0)
      'id'  : over the first copy of each REQUESTID only (None for later copies)."""
    out = {}
    for mode in ('row', 'id'):
        gaps, last = [None] * len(rows), {}
        for i, r in enumerate(rows):
            if mode == 'id' and r[16] != 1:
                continue
            key = (r[6], r[12])
            if r[6] and key in last:
                g = (r[2] - last[key]).total_seconds() / 86400
                if r[2].date() == last[key].date():
                    g = min(g, 0.0)
                gaps[i] = g
            last[key] = r[2]
        out[mode] = gaps
    return out


def evaluate(rows, gaps, goal, snap, dedup, denom, rule, chan, qs=QS, qbasis='init'):
    """dedup: None = every row as published; 'id' = one row per REQUESTID;
    integer W = drop a row if an earlier row at the same address+code was filed within W days
    (0 = same calendar day; caller copies of one request are therefore also dropped);
    'idW' = one row per REQUESTID, then drop a request if an earlier distinct request at the same
    address+code was filed within W days."""
    agg = collections.defaultdict(lambda: [0, 0])
    if isinstance(dedup, str):
        W = None if dedup == 'id' else int(dedup[2:])
        g_list = gaps['id']
    else:
        W = dedup
        g_list = gaps['row']
    for i, (rid, q, ti, tc, tx, st, addr, days, cdays, bdays, tp, ct, pc, pdays, pcdays, qc, rn, anyres) in enumerate(rows):
        if isinstance(dedup, str) and rn != 1:
            continue
        if qbasis == 'closed':
            if st != 'CLOSED':
                continue
            q = qc
        if q not in qs:
            continue
        if snap is not None and ti >= snap:
            continue
        if chan == 'res' and not (anyres if isinstance(dedup, str) else ct in RES):
            continue
        g = g_list[i]
        if W is not None and g is not None and (g <= W if W > 0 else g <= 0):
            continue
        closed = st == 'CLOSED' and tc is not None and (snap is None or tc < snap)
        cancelled = st == 'CANCEL' and (snap is None or (tx is None or tx < snap))
        if denom == 'closed' and not closed:
            continue
        if denom == 'notcanc' and cancelled:
            continue
        if goal is None:  # per-request goal = the city's own promise date
            gf, gc = (pdays, pcdays) if pdays is not None else (-1, -1)
        else:
            gf = gc = goal
        if closed:
            if rule == 'frac':
                ok = days <= gf
            elif rule == 'cd':
                ok = cdays <= gc
            elif rule == 'cdlt':
                ok = cdays < gc
            elif rule == 'bd':
                ok = bdays <= gc
            else:
                ok = tp is not None and tc <= tp
        else:
            ok = False
        a = agg[q]
        a[0] += 1
        a[1] += ok
    return [(agg[q][0], agg[q][1] / agg[q][0] if agg[q][0] else None) for q in qs]


def score(res, m, upto=9):
    sh = [abs(r[1] - s) * 100 for r, s in zip(res[:upto], m['share'][:upto]) if r[1] is not None]
    nn = [abs(r[0] - n) / n * 100 for r, n in zip(res[:upto], m['n'][:upto])]
    within5 = sum(1 for x in sh if x <= 5)
    return sum(sh) / len(sh), sum(nn) / len(nn), within5


def main():
    con = connect()
    out = {}
    for key, m in METRICS.items():
        rows = load(con, m['codes'])
        gaps = prev_gap(rows)
        results = []
        for snap, dedup, denom, rule, chan, qb in itertools.product(SNAPS, DEDUPS, DENOMS, RULES, CHANS, QBASES):
            if qb == 'closed' and denom != 'closed':
                continue  # closed-quarter basis only makes sense for closed requests
            res = evaluate(rows, gaps, m['goal_days'], SNAPS[snap], dedup, denom, rule, chan, qbasis=qb)
            mae, mape, w5 = score(res, m)
            q2 = res[9]
            results.append(dict(snap=snap, dedup=dedup, denom=denom, rule=rule, chan=chan, qbasis=qb,
                                share_mae_pp_2024q1_2026q1=round(mae, 2), n_mape_pct=round(mape, 1),
                                quarters_within_5pp=w5,
                                q2_2026_share=q2[1], q2_2026_n=q2[0],
                                per_quarter=[{'q': q, 'n': r[0], 'share': r[1]} for q, r in zip(QS, res)]))
        results.sort(key=lambda d: d['share_mae_pp_2024q1_2026q1'] + 0.25 * d['n_mape_pct'])
        out[key] = dict(label=m['label'], goal_days=m['goal_days'], codes=m['codes'],
                        citystat_n=m['n'], citystat_share=m['share'], ranked=results)
        print(f"\n== {key}  (CityStat n {m['n']})")
        for d in results[:6]:
            print(f"  snap={d['snap']:4s} dedup={str(d['dedup']):4s} denom={d['denom']:7s} rule={d['rule']:4s} chan={d['chan']:3s} q={d['qbasis']:6s}"
                  f"  shareMAE={d['share_mae_pp_2024q1_2026q1']:5.2f}pp nMAPE={d['n_mape_pct']:5.1f}% w5={d['quarters_within_5pp']}/9"
                  f"  Q2'26 {d['q2_2026_share']*100 if d['q2_2026_share'] is not None else float('nan'):.1f}% of {d['q2_2026_n']}"
                  f" (CS {m['share'][9]*100:.1f}% of {m['n'][9]})")
        bc = min((r for r in results if r['qbasis'] == 'closed'), key=lambda d: d['share_mae_pp_2024q1_2026q1'])
        print(f"  best with quarter-of-closure basis: MAE {bc['share_mae_pp_2024q1_2026q1']} nMAPE {bc['n_mape_pct']} ({bc['dedup']} {bc['rule']} {bc['chan']})")
        best_share = min(results, key=lambda d: d['share_mae_pp_2024q1_2026q1'])
        print(f"  best on share alone: {best_share['snap']} dedup={best_share['dedup']} {best_share['denom']} {best_share['rule']} {best_share['chan']} "
              f"MAE {best_share['share_mae_pp_2024q1_2026q1']} nMAPE {best_share['n_mape_pct']}")
    json.dump(out, open(f'{OUT}/definition_search.json', 'w'), default=str, indent=1)


if __name__ == '__main__':
    main()
