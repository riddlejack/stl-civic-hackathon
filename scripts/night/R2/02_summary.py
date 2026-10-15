"""R2 step 2: like-for-like summary of re-reports by closing class.

Reads build/R2/private/closure_measures.parquet (written by 01_rereport.py; one
row per 2025-26 closure, no ids or addresses) and writes
build/R2/rereport_summary.json and build/R2/rereport_type_compare.csv.

The crude pooled comparison is confounded by type mix (hand-offs are
concentrated in refuse, weeds, towing, vacant buildings), so the headline
compares classes WITHIN each type and then averages the within-type rates
with the same weights for both classes (the number of hand-off closures in
each type): direct standardisation to the hand-off mix. A Mantel-Haenszel
risk ratio (Greenland-Robins variance) is reported beside it.

Run: .venv/bin/python -I scripts/night/R2/02_summary.py
"""
import csv
import json
import math
import os

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, 'build', 'R2')
PQ = os.path.join(OUT, 'private', 'closure_measures.parquet')
ELIG = 300      # closures 2025-26 per type (R2 brief)
MIN_N = 30      # complete-window closures per class within a type to enter a comparison

con = duckdb.connect()
con.execute(f"""
CREATE VIEW m AS
SELECT *, coalesce(d_any <= 7, false) AS r7, coalesce(d_any <= 14, false) AS r14, coalesce(d_any <= 30, false) AS r30,
       coalesce(d_res <= 14, false) AS r14res, coalesce(d_guard <= 14, false) AS r14g, coalesce(dp <= 30, false) AS rp30,
       df IS NOT NULL AS rf
FROM '{PQ}' WHERE has_addr;
CREATE VIEW tot AS SELECT problem_code, count(*) AS n FROM '{PQ}' GROUP BY 1;
""")

# recurring by nature: collected on a weekly route, cleaned on a cycle, or regrows (COMMON correction 4)
RECURRING_SQL = "(division = 'REFUSE' OR problem_code IN ('Street Cleaning') OR family = 'weeds')"
CHRONIC_SQL = "(family = 'dumping')"

MEASURES = {
    # name: (window flag, outcome flag, extra filter)
    'rr7': ('w7', 'r7', 'true'),
    'rr14': ('w14', 'r14', 'true'),
    'rr30': ('w30', 'r30', 'true'),
    'rr14_resident': ('w14', 'r14res', 'true'),
    'rr14_guard24h': ('w14', 'r14g', 'true'),
    'rr14_first_report': ('w14', 'r14', 'prior365 = 0'),
    'rr30_after_promise': ('wp30', 'rp30', 'true'),
    'rr_filing_day15_44': ('wf', 'rf', 'true'),
}
SUBSETS = {
    'all_eligible_types': 'true',
    'excluding_recurring_and_chronic': f'NOT {RECURRING_SQL} AND NOT {CHRONIC_SQL}',
    'durable_fix_types': 'durable',
    'recurring_only': RECURRING_SQL,
}


def strata(measure, subset, cls_a, cls_b, kind=None):
    wcol, ycol, extra = MEASURES[measure]
    kfilter = f"AND (cls <> 'handoff' OR kind = '{kind}')" if kind else ''
    q = f"""
    SELECT problem_code,
           count(*) FILTER (WHERE cls = '{cls_a}') AS na, count(*) FILTER (WHERE cls = '{cls_a}' AND {ycol}) AS ya,
           count(*) FILTER (WHERE cls = '{cls_b}') AS nb, count(*) FILTER (WHERE cls = '{cls_b}' AND {ycol}) AS yb
    FROM m JOIN tot USING (problem_code)
    WHERE tot.n >= {ELIG} AND {wcol} AND {extra} AND ({subset}) {kfilter}
    GROUP BY 1
    HAVING count(*) FILTER (WHERE cls = '{cls_a}') >= {MIN_N} AND count(*) FILTER (WHERE cls = '{cls_b}') >= {MIN_N}
    """
    return con.execute(q).fetchall()


def compare(rows):
    """Standardise to group A's mix; Mantel-Haenszel RR with Greenland-Robins CI."""
    if not rows:
        return None
    W = sum(na for _, na, _, _, _ in rows)
    pa = sum(na * (ya / na) for _, na, ya, nb, yb in rows) / W
    pb = sum(na * (yb / nb) for _, na, ya, nb, yb in rows) / W
    var = sum((na / W) ** 2 * ((ya / na) * (1 - ya / na) / na + (yb / nb) * (1 - yb / nb) / nb)
              for _, na, ya, nb, yb in rows)
    se = math.sqrt(var)
    # Mantel-Haenszel risk ratio
    R = sum(ya * nb / (na + nb) for _, na, ya, nb, yb in rows)
    S = sum(yb * na / (na + nb) for _, na, ya, nb, yb in rows)
    rr = R / S if S else None
    if R and S:
        P = sum((na * nb * (ya + yb) - ya * yb * (na + nb)) / (na + nb) ** 2 for _, na, ya, nb, yb in rows)
        se_log = math.sqrt(P / (R * S))
        rr_ci = [round(rr * math.exp(-1.96 * se_log), 2), round(rr * math.exp(1.96 * se_log), 2)]
    else:
        rr_ci = None
    crude_a = sum(ya for _, na, ya, nb, yb in rows) / W
    crude_b = sum(yb for _, na, ya, nb, yb in rows) / sum(nb for _, na, ya, nb, yb in rows)
    higher = sum(1 for _, na, ya, nb, yb in rows if ya / na > yb / nb)
    sig_higher = sum(1 for _, na, ya, nb, yb in rows
                     if (ya / na - yb / nb) - 1.96 * math.sqrt((ya / na) * (1 - ya / na) / na + (yb / nb) * (1 - yb / nb) / nb + 1e-12) > 0)
    sig_lower = sum(1 for _, na, ya, nb, yb in rows
                    if (ya / na - yb / nb) + 1.96 * math.sqrt((ya / na) * (1 - ya / na) / na + (yb / nb) * (1 - yb / nb) / nb + 1e-12) < 0)
    return {
        'types': len(rows), 'n_a': W, 'n_b': sum(nb for _, na, ya, nb, yb in rows),
        'reports_a': sum(ya for _, na, ya, nb, yb in rows), 'reports_b': sum(yb for _, na, ya, nb, yb in rows),
        'std_rate_a_pct': round(100 * pa, 2), 'std_rate_b_pct': round(100 * pb, 2),
        'std_diff_pts': round(100 * (pa - pb), 2), 'std_diff_ci95_pts': [round(100 * (pa - pb - 1.96 * se), 2), round(100 * (pa - pb + 1.96 * se), 2)],
        'mh_rr': round(rr, 2) if rr else None, 'mh_rr_ci95': rr_ci,
        'crude_rate_a_pct': round(100 * crude_a, 2), 'crude_rate_b_pct': round(100 * crude_b, 2),
        'types_a_higher': higher, 'types_a_sig_higher': sig_higher, 'types_a_sig_lower': sig_lower,
    }


summary = {'definition': 'share of closures followed by another request at the same normalised address with the same PROBLEMCODE, '
                         'filed after the closure and within the window; closures filed 1 Jan 2025 to 13 Oct 2026; windows complete '
                         'before the file as-of time; types with >= 300 closures; a type enters a comparison only if both classes have '
                         f'>= {MIN_N} complete-window closures; rates standardised to the first class\'s type mix',
           'comparisons': {}}
for (a, b) in [('handoff', 'done'), ('no_action', 'done'), ('handoff', 'no_action')]:
    for sub, sql in SUBSETS.items():
        for meas in MEASURES:
            summary['comparisons'][f'{a}_vs_{b}|{sub}|{meas}'] = compare(strata(meas, sql, a, b))
for kind in ['crew_work', 'owner_enforcement', 'referral_elsewhere']:
    for sub, sql in SUBSETS.items():
        for meas in ['rr7', 'rr14', 'rr30', 'rr14_first_report', 'rr30_after_promise', 'rr_filing_day15_44']:
            summary['comparisons'][f'handoff[{kind}]_vs_done|{sub}|{meas}'] = compare(strata(meas, sql, 'handoff', 'done', kind))

# crude pooled rates by class, all types (no standardisation), for transparency
crude = con.execute("""
SELECT cls, count(*) FILTER (WHERE w14) AS n14, round(100.0 * count(*) FILTER (WHERE w14 AND r14) / count(*) FILTER (WHERE w14), 2) AS pct14,
       count(*) FILTER (WHERE w30) AS n30, round(100.0 * count(*) FILTER (WHERE w30 AND r30) / count(*) FILTER (WHERE w30), 2) AS pct30
FROM m GROUP BY 1 ORDER BY 1""").fetchall()
summary['crude_all_types'] = [dict(zip(['class', 'n14', 'pct14', 'n30', 'pct30'], r)) for r in crude]

# per-type comparison table (14 and 30 days), hand-off vs done and no_action vs done
rows = con.execute(f"""
SELECT problem_code, any_value(division) AS division, any_value(family) AS family, bool_or(durable) AS durable,
       bool_or({RECURRING_SQL}) AS recurring, bool_or({CHRONIC_SQL}) AS chronic,
       count(*) FILTER (WHERE cls='handoff' AND w14) AS h_n14, count(*) FILTER (WHERE cls='handoff' AND w14 AND r14) AS h_y14,
       count(*) FILTER (WHERE cls='done' AND w14) AS d_n14, count(*) FILTER (WHERE cls='done' AND w14 AND r14) AS d_y14,
       count(*) FILTER (WHERE cls='no_action' AND w14) AS x_n14, count(*) FILTER (WHERE cls='no_action' AND w14 AND r14) AS x_y14,
       count(*) FILTER (WHERE cls='handoff' AND w30) AS h_n30, count(*) FILTER (WHERE cls='handoff' AND w30 AND r30) AS h_y30,
       count(*) FILTER (WHERE cls='done' AND w30) AS d_n30, count(*) FILTER (WHERE cls='done' AND w30 AND r30) AS d_y30,
       count(*) FILTER (WHERE cls='handoff' AND w14 AND prior365=0) AS h_n14f, count(*) FILTER (WHERE cls='handoff' AND w14 AND prior365=0 AND r14) AS h_y14f,
       count(*) FILTER (WHERE cls='done' AND w14 AND prior365=0) AS d_n14f, count(*) FILTER (WHERE cls='done' AND w14 AND prior365=0 AND r14) AS d_y14f,
       round(100.0 * count(*) FILTER (WHERE prior365 > 0) / count(*), 1) AS pct_with_prior_report
FROM m JOIN tot USING (problem_code) WHERE tot.n >= {ELIG}
GROUP BY 1 ORDER BY h_n14 DESC""").fetchall()
cols = [d[0] for d in con.description]


def p(y, n):
    return round(100.0 * y / n, 1) if n else None


def verdict(hy, hn, dy, dn):
    if hn < MIN_N or dn < MIN_N:
        return 'too few to compare'
    a, b = hy / hn, dy / dn
    se = math.sqrt(a * (1 - a) / hn + b * (1 - b) / dn + 1e-12)
    if a - b - 1.96 * se > 0:
        return 'hand-off higher'
    if a - b + 1.96 * se < 0:
        return 'hand-off lower'
    return 'no clear difference'


with open(os.path.join(OUT, 'rereport_type_compare.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(cols + ['handoff_pct14', 'done_pct14', 'no_action_pct14', 'handoff_pct30', 'done_pct30',
                       'handoff_pct14_first', 'done_pct14_first', 'verdict14', 'verdict14_first_report'])
    verdicts = {}
    for r in rows:
        d = dict(zip(cols, r))
        v = verdict(d['h_y14'], d['h_n14'], d['d_y14'], d['d_n14'])
        vf = verdict(d['h_y14f'], d['h_n14f'], d['d_y14f'], d['d_n14f'])
        verdicts[v] = verdicts.get(v, 0) + 1
        w.writerow(list(r) + [p(d['h_y14'], d['h_n14']), p(d['d_y14'], d['d_n14']), p(d['x_y14'], d['x_n14']),
                              p(d['h_y30'], d['h_n30']), p(d['d_y30'], d['d_n30']),
                              p(d['h_y14f'], d['h_n14f']), p(d['d_y14f'], d['d_n14f']), v, vf])
summary['per_type_verdicts_14d'] = verdicts

# per type, the same-weeks (filing-anchored) window: closed within 14 days of filing, re-reported 15-44 days after filing
fw = con.execute(f"""
SELECT problem_code,
       count(*) FILTER (WHERE cls = 'handoff' AND wf) AS h_n, count(*) FILTER (WHERE cls = 'handoff' AND wf AND rf) AS h_y,
       count(*) FILTER (WHERE cls = 'done' AND wf) AS d_n, count(*) FILTER (WHERE cls = 'done' AND wf AND rf) AS d_y
FROM m JOIN tot USING (problem_code) WHERE tot.n >= {ELIG}
GROUP BY 1 HAVING count(*) FILTER (WHERE cls = 'handoff' AND wf) >= {MIN_N} AND count(*) FILTER (WHERE cls = 'done' AND wf) >= {MIN_N}
ORDER BY h_n DESC""").fetchall()
with open(os.path.join(OUT, 'rereport_filing_window_by_type.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['problem_code', 'handoff_n', 'handoff_rereported', 'done_n', 'done_rereported', 'handoff_pct', 'done_pct'])
    for r in fw:
        w.writerow(list(r) + [round(100.0 * r[2] / r[1], 1), round(100.0 * r[4] / r[3], 1)])
summary['filing_window_by_type'] = {r[0]: {'handoff_pct': round(100.0 * r[2] / r[1], 1), 'done_pct': round(100.0 * r[4] / r[3], 1),
                                           'handoff_n': r[1], 'done_n': r[3]} for r in fw}

# median days from filing to closure, by class (all 2025-26 closures, with or without address)
summary['median_days_to_close_by_class'] = {c: round(v, 2) for c, v in con.execute(
    f"SELECT cls, median(days_to_close) FROM '{PQ}' GROUP BY 1").fetchall()}

# by ward group (wards 1-5, 6-9, 10-14), hand-off vs done within type, 14 days
summary['by_ward_group_rr14'] = {wg: compare(strata('rr14', f"ward_group = '{wg}'", 'handoff', 'done')) for wg in ['1-5', '6-9', '10-14']}

json.dump(summary, open(os.path.join(OUT, 'rereport_summary.json'), 'w'), indent=1)
for k in ['handoff_vs_done|all_eligible_types|rr14', 'handoff_vs_done|all_eligible_types|rr7', 'handoff_vs_done|all_eligible_types|rr30',
          'handoff_vs_done|excluding_recurring_and_chronic|rr14', 'handoff_vs_done|durable_fix_types|rr14',
          'handoff_vs_done|recurring_only|rr7', 'handoff_vs_done|all_eligible_types|rr14_first_report',
          'handoff_vs_done|all_eligible_types|rr14_resident', 'handoff_vs_done|all_eligible_types|rr14_guard24h',
          'handoff_vs_done|all_eligible_types|rr30_after_promise', 'handoff_vs_done|all_eligible_types|rr_filing_day15_44',
          'handoff_vs_done|excluding_recurring_and_chronic|rr_filing_day15_44', 'no_action_vs_done|all_eligible_types|rr14',
          'handoff[crew_work]_vs_done|all_eligible_types|rr14', 'handoff[owner_enforcement]_vs_done|all_eligible_types|rr14',
          'handoff[referral_elsewhere]_vs_done|all_eligible_types|rr14']:
    print(k, summary['comparisons'][k])
print(verdicts)
