"""N4 steps 1-2: the comparison table (metric x quarter x definition, ours vs CityStat, counts too)
and the Q3 2026 values CityStat has not published.

Fixed definitions (chosen before looking at Q3; B is picked by 01_definition_search.py):
  N  naive    : every row of the file filed in the quarter (the file repeats a request once per
                caller); on time = closed within the goal in elapsed days; cancelled and
                still-open count as not on time.
  C  common   : one row per distinct REQUESTID; closed requests only; on time = calendar-date
                difference (close date - filed date) <= goal. Parks: goal = the request's own
                PRJCOMPLETEDATE (date difference <= promise date difference).
  P  promise  : as C, but on time = closed at or before PRJCOMPLETEDATE (the city's own promise).
  B  best     : best-scoring combination for that metric among the 480 of 1,440 that use the live file
                (01_definition_search.py; snapshot axis fixed to 'none' so Q3 can be computed).
Fit is scored on 2024 Q1 - 2026 Q1 (nine quarters). 2026 Q2 is scored separately because
CityStat calls it preliminary.

Preliminary-quarter drift: for each past quarter, C as it would have read 13 days after the
quarter ended (the age of Q3 2026 on 13 Oct 2026) vs C on the full file. Used to say how far
the Q3 2026 closed-only figures can be expected to fall as late closures arrive.

Outputs: build/N4/citystat_comparison.csv (long), build/N4/citystat_fit.json,
         build/N4/q3_2026.json
"""
import sys, json, csv, importlib, datetime as dt, statistics
sys.path.insert(0, './scripts/night/N4')
from common import connect, OUT
from citystat_targets import METRICS, QS
ds = importlib.import_module('01_definition_search')

QS_ALL = QS + ['2026 Q3']
QEND = {f'{y} Q{q}': dt.datetime(y + (q == 4), (q * 3) % 12 + 1, 1) for y in (2024, 2025, 2026) for q in (1, 2, 3, 4)}
FILE_DATE = dt.datetime(2026, 10, 13)
LAG_Q3 = (FILE_DATE - QEND['2026 Q3']).days  # 12 full days into October; file runs to 13 Oct 00:33


def defs_for(key, search):
    m = METRICS[key]
    best = next(r for r in search[key]['ranked'] if r['snap'] == 'none')
    return {
        'N': dict(snap=None, dedup=None, denom='all', rule='frac', chan='any', qbasis='init'),
        'C': dict(snap=None, dedup='id', denom='closed', rule='cd', chan='any', qbasis='init'),
        'P': dict(snap=None, dedup='id', denom='closed', rule='prom', chan='any', qbasis='init'),
        'B': dict(snap=None, dedup=best['dedup'], denom=best['denom'], rule=best['rule'], chan=best['chan'], qbasis=best['qbasis']),
    }


def fit(series, m):
    d = [(s[1] - t) * 100 for s, t in zip(series[:9], m['share'][:9]) if s[1] is not None]
    nn = [abs(s[0] - t) / t * 100 for s, t in zip(series[:9], m['n'][:9])]
    return dict(share_mae_pp=round(sum(map(abs, d)) / len(d), 2), share_max_abs_pp=round(max(map(abs, d)), 1),
                mean_signed_pp=round(sum(d) / len(d), 2),
                quarters_within_5pp=sum(1 for x in d if abs(x) <= 5), quarters_scored=len(d),
                n_mape_pct=round(sum(nn) / len(nn), 1),
                q2_2026_diff_pp=round((series[9][1] - m['share'][9]) * 100, 1) if series[9][1] is not None else None)


def main():
    con = connect()
    search = json.load(open(f'{OUT}/definition_search.json'))
    long_rows, fits, q3 = [], {}, {}
    for key, m in METRICS.items():
        rows = ds.load(con, m['codes'])
        gaps = ds.prev_gap(rows)
        D = defs_for(key, search)
        fits[key] = dict(label=m['label'], page=m['page'], codes=m['codes'], goal_days=m['goal_days'], definitions=D, fit={})
        series = {}
        for name, d in D.items():
            s = ds.evaluate(rows, gaps, m['goal_days'], d['snap'], d['dedup'], d['denom'], d['rule'], d['chan'], qs=QS_ALL, qbasis=d['qbasis'])
            series[name] = s
            fits[key]['fit'][name] = fit(s, m)
            for i, q in enumerate(QS_ALL):
                cs_n = m['n'][i] if i < len(QS) else None
                cs_s = m['share'][i] if i < len(QS) else None
                long_rows.append(dict(metric=key, quarter=q, definition=name, ours_n=s[i][0],
                                      ours_share=None if s[i][1] is None else round(s[i][1], 4),
                                      citystat_n=cs_n, citystat_share=cs_s,
                                      diff_pp=None if (cs_s is None or s[i][1] is None) else round((s[i][1] - cs_s) * 100, 1)))
        # Q2 2026 under C at different snapshot dates
        snaps = {}
        for lab, sd in (('2026-07-01', dt.datetime(2026, 7, 1)), ('2026-07-15', dt.datetime(2026, 7, 15)),
                        ('2026-08-01', dt.datetime(2026, 8, 1)), ('file 2026-10-13', None)):
            for name in ('C', 'B'):
                d = D[name]
                s = ds.evaluate(rows, gaps, m['goal_days'], sd, d['dedup'], d['denom'], d['rule'], d['chan'], qs=['2026 Q2'], qbasis=d['qbasis'])
                snaps[f'{name} as of {lab}'] = dict(n=s[0][0], share=None if s[0][1] is None else round(s[0][1], 4))
        fits[key]['q2_2026_by_snapshot'] = snaps
        fits[key]['q2_2026_citystat'] = dict(n=m['n'][9], share=m['share'][9])
        # drift of closed-only share between quarter end + LAG and the full file, past quarters
        drift = []
        for q in QS[:9]:
            snap = QEND[q] + dt.timedelta(days=LAG_Q3)
            for name in ('C',):
                d = D[name]
                early = ds.evaluate(rows, gaps, m['goal_days'], snap, d['dedup'], d['denom'], d['rule'], d['chan'], qs=[q], qbasis=d['qbasis'])[0]
                final = series[name][QS_ALL.index(q)]
                if early[1] is not None and final[1] is not None:
                    drift.append(dict(q=q, early_n=early[0], early=round(early[1], 4), final_n=final[0], final=round(final[1], 4),
                                      drop_pp=round((early[1] - final[1]) * 100, 1)))
        fits[key]['closed_only_drift_at_lag_days'] = LAG_Q3
        fits[key]['closed_only_drift'] = drift
        drops = [x['drop_pp'] for x in drift]
        dfl = dict(D['C']); dfl['denom'] = 'notcanc'
        floor = ds.evaluate(rows, gaps, m['goal_days'], None, dfl['dedup'], 'notcanc', dfl['rule'], dfl['chan'], qs=['2026 Q3'])[0]
        bfl = D['B']
        floor_b = ds.evaluate(rows, gaps, m['goal_days'], None, bfl['dedup'], 'notcanc', bfl['rule'], bfl['chan'], qs=['2026 Q3'], qbasis=bfl['qbasis'])[0]
        i3 = QS_ALL.index('2026 Q3')
        q3[key] = dict(label=m['label'], goal_days=m['goal_days'],
                       C_closed_only=dict(n=series['C'][i3][0], share=series['C'][i3][1]),
                       B_best=dict(n=series['B'][i3][0], share=series['B'][i3][1], definition=D['B']),
                       P_promise=dict(n=series['P'][i3][0], share=series['P'][i3][1]),
                       C_if_open_close_late=dict(n=floor[0], share=floor[1]),
                       B_if_open_close_late=dict(n=floor_b[0], share=floor_b[1]),
                       N_all_requests=dict(n=series['N'][i3][0], share=series['N'][i3][1]),
                       expected_drop_pp_median=statistics.median(drops) if drops else None,
                       expected_drop_pp_max=max(drops) if drops else None,
                       citystat_q2_2026=dict(n=m['n'][9], share=m['share'][9]),
                       label_note='our definition, from the public file (311 CSV to 13 Oct 2026); Q3 2026 not published by CityStat')
        f = fits[key]['fit']
        print(f"\n{key}: " + '  '.join(f"{k}: MAE {v['share_mae_pp']:.1f}pp w5 {v['quarters_within_5pp']}/9 nMAPE {v['n_mape_pct']:.0f}% Q2d {v['q2_2026_diff_pp']}" for k, v in f.items()))
        print(f"   B = {D['B']}")
        print(f"   Q2 2026 snapshots: " + '; '.join(f"{k} {v['share']*100:.1f}%/{v['n']}" for k, v in snaps.items() if v['share'] is not None) + f"  | CityStat {m['share'][9]*100:.1f}%/{m['n'][9]}")
        print(f"   drift (C, {LAG_Q3}d after quarter end vs final): {drops}")
        print(f"   Q3 2026: C {series['C'][i3][1]*100:.1f}% of {series['C'][i3][0]} (floor {floor[1]*100:.1f}% of {floor[0]}); B {series['B'][i3][1]*100:.1f}%; P {series['P'][i3][1]*100:.1f}%; N {series['N'][i3][1]*100:.1f}% of {series['N'][i3][0]}")
    with open(f'{OUT}/citystat_comparison.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(long_rows[0].keys()))
        w.writeheader()
        w.writerows(long_rows)
    json.dump(fits, open(f'{OUT}/citystat_fit.json', 'w'), indent=1, default=str)
    json.dump(q3, open(f'{OUT}/q3_2026.json', 'w'), indent=1, default=str)
    # knock-out test summary
    for name in ('N', 'C', 'P', 'B'):
        ok = [k for k in METRICS if fits[k]['fit'][name]['share_mae_pp'] <= 5]
        cells = sum(fits[k]['fit'][name]['quarters_within_5pp'] for k in METRICS)
        tot = sum(fits[k]['fit'][name]['quarters_scored'] for k in METRICS)
        print(f"{name}: metrics with MAE<=5pp: {len(ok)}/{len(METRICS)}; metric-quarters within 5pp: {cells}/{tot}")


if __name__ == '__main__':
    main()
