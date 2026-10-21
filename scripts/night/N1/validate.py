#!/usr/bin/env python3
"""Validate build/stl.duckdb against the figures the project already established
(the figures established earlier on 13 Oct).
Writes build/N1/validation.json and prints a table: ours vs theirs, and the
definition each uses. Run after build_db.py."""
import json
import os

import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('STL_ROOT', os.path.abspath(os.path.join(HERE, '..', '..', '..')))
con = duckdb.connect(os.path.join(ROOT, 'build', 'stl.duckdb'), read_only=True)


def one(sql):
    return con.execute(sql).fetchone()


LFL = """SELECT round(median(days_to_close) FILTER (WHERE ward_group = '1-5'), 1),
                count(*) FILTER (WHERE ward_group = '1-5'),
                round(median(days_to_close) FILTER (WHERE ward_group = '10-14'), 1),
                count(*) FILTER (WHERE ward_group = '10-14'),
                sum(source_rows) FILTER (WHERE ward_group = '1-5'), sum(source_rows) FILTER (WHERE ward_group = '10-14')
         FROM requests WHERE problem_code = '{code}' AND channel_group = 'resident'
           AND ts_init >= TIMESTAMP '2025-05-16' AND status_group = 'closed' {extra}"""

checks = []


def add(cid, what, theirs, sql, fmt, note=''):
    try:
        row = one(sql)
        ours = fmt(row)
    except Exception as e:  # keep failures visible
        row, ours = None, f'ERROR {e}'
    checks.append({'id': cid, 'what': what, 'theirs': theirs, 'ours': ours, 'raw': row, 'note': note})


add('req_12m', 'Requests initiated in the 12 months to 12 Oct 2026', '112,859',
    "SELECT count(*), sum(source_rows) FROM requests WHERE ts_init >= TIMESTAMP '2025-10-13' AND ts_init < TIMESTAMP '2026-10-13'",
    lambda r: f'{r[0]:,} distinct ids ({r[1]:,} file rows)',
    'Ours counts one row per REQUESTID; the file repeats 34k ids (one row per caller).')
add('open_2023', 'Open requests initiated 2023 or later; of them over a year old', '21,292; 9,069',
    """SELECT count(*), count(*) FILTER (WHERE ts_init < (SELECT asof_ts FROM run_dates) - INTERVAL 365 DAY)
       FROM requests WHERE status_group = 'open' AND init_year >= 2023""",
    lambda r: f'{r[0]:,}; {r[1]:,}')
add('blank_12m', 'Closed or cancelled in the last 12 months with no resolution text', '14.6%',
    """SELECT round(100.0 * avg(CAST(resolution IS NULL AS INT)), 1), count(*) FROM requests
       WHERE status_group IN ('closed', 'cancelled') AND ts_init >= TIMESTAMP '2025-10-13'""",
    lambda r: f'{r[0]}% of {r[1]:,}')
add('repeat_12m', 'Requests in the last 12 months sharing address and code with another in the period', '23.7%',
    """WITH x AS (SELECT addr_norm, addr_raw, problem_code,
                       count(*) OVER (PARTITION BY addr_norm, problem_code) AS c,
                       count(*) OVER (PARTITION BY addr_raw, problem_code) AS c_raw
                FROM requests WHERE ts_init >= TIMESTAMP '2025-10-13' AND ts_init < TIMESTAMP '2026-10-13')
       SELECT round(100.0 * avg(CAST(c > 1 AND addr_norm <> '' AS INT)), 1),
              round(100.0 * avg(CAST(c_raw > 1 AND addr_raw IS NOT NULL AS INT)), 1), count(*) FROM x""",
    lambda r: f'{r[0]}% normalised address ({r[1]}% raw address text) of {r[2]:,}',
    'The original definition is not on disk; the normaliser merges spelling variants, which raises the share.')
add('refile_30', 'Closed 2025-26 with an address; re-filed (same address and code) within 30 days of closure',
    '190,856; 11,992 (6.3%)',
    """SELECT count(*), sum(CAST(came_back_30 AS INT)), round(100.0 * avg(CAST(came_back_30 AS INT)), 1),
              sum(r.source_rows)
       FROM refiled f JOIN requests r USING (request_id) WHERE f.init_year >= 2025""",
    lambda r: f'{r[0]:,}; {r[1]:,} ({r[2]}%) [file rows {r[3]:,}]',
    'Ours: distinct ids, next request strictly after closure within 30.0 days. Theirs counted file rows.')
add('weeds_2026', 'Weed requests on vacant property, 2026 (Weeds-Vacant Lot + Weeds-Vacant Bldg)', '4,658',
    """SELECT count(*), sum(source_rows) FROM requests
       WHERE problem_code IN ('Weeds-Vacant Lot', 'Weeds-Vacant Bldg') AND init_year = 2026""",
    lambda r: f'{r[0]:,} ids ({r[1]:,} rows)')
for wid, codes, theirs in [('weeds_lot_ledger', "('Weeds-Vacant Lot')", '35%; 63%; 26%'),
                           ('weeds_lotbldg_ledger', "('Weeds-Vacant Lot', 'Weeds-Vacant Bldg')", '(not established)')]:
    add(wid, f'Weeds {codes} 2026 closed "on schedule"/"rotation", filed by 15 Sep, parcel matched: cut within 30 d; any cut later in 2026; no 2026 cut',
        theirs,
        f"""SELECT round(100 * avg(CAST(coalesce(f.first_cut_after <= f.init_date + 30, false) AS INT)), 0),
              round(100 * avg(CAST(f.cut_by_season_end AS INT)), 0),
              round(100 * avg(CAST(f.no_cut_in_season AS INT)), 0), count(*)
           FROM request_ledger_flags f JOIN requests r USING (request_id)
           WHERE r.problem_code IN {codes} AND r.init_year = 2026
             AND r.status_group = 'closed' AND r.ts_init <= TIMESTAMP '2026-09-15'
             AND (r.res_key LIKE '%schedule%' OR r.res_key LIKE '%rotation%')""",
        lambda r: f'{r[0]:.0f}%; {r[1]:.0f}%; {r[2]:.0f}% (n={r[3]:,})',
        'Cuts on the filing day count as after. Vacant buildings are cut far less often than lots, so never pool them.')
add('tree_cancel', 'Inspect City Tree 2025-26: cancelled; cancelled with no text', '5,537; 5,415',
    """SELECT count(*) FILTER (WHERE status_group = 'cancelled'),
              count(*) FILTER (WHERE status_group = 'cancelled' AND resolution IS NULL),
              sum(source_rows) FILTER (WHERE status_group = 'cancelled'),
              sum(source_rows) FILTER (WHERE status_group = 'cancelled' AND resolution IS NULL)
       FROM requests WHERE problem_code = 'Inspect City Tree' AND init_year >= 2025""",
    lambda r: f'{r[0]:,}; {r[1]:,} ids ({r[2]:,}; {r[3]:,} file rows)')
add('tree_wo_match', 'Inspect City Tree 2025-26 address in tree WO sample: cancelled vs closed "work order created" vs baseline (potholes/refuse/containers)',
    '10.8% vs 2.4% (all closed) vs 1.9%',
    """WITH w AS (SELECT DISTINCT a.addr_norm FROM wo_tree w JOIN addr_lookup a ON a.addr_raw = w.address
                 WHERE w.source IN ('tree_removal', 'tree_trim') AND a.addr_norm <> ''),
       r AS (SELECT problem_code, status_group, res_key, addr_norm IN (SELECT addr_norm FROM w) AS hit
             FROM requests WHERE init_year >= 2025)
       SELECT round(100 * avg(CAST(hit AS INT)) FILTER (WHERE problem_code = 'Inspect City Tree' AND status_group = 'cancelled'), 1),
              round(100 * avg(CAST(hit AS INT)) FILTER (WHERE problem_code = 'Inspect City Tree' AND status_group = 'closed'), 1),
              round(100 * avg(CAST(hit AS INT)) FILTER (WHERE problem_code = 'Inspect City Tree' AND res_key LIKE '%work order created%'), 1),
              round(100 * avg(CAST(hit AS INT)) FILTER (WHERE problem_code IN ('Potholes - Residnl', 'Refuse not collected', 'Containr damaged')), 1)
       FROM r""",
    lambda r: f'{r[0]}% vs {r[1]}% (all closed; "work order created" only: {r[2]}%) vs {r[3]}%',
    'Ours uses every baseline request, theirs a 5,000 random sample. The 2.4% in the earlier figure is all closed requests, not only "work order created" ones.')
add('ledger_2026', 'Ledger 2026 Grass Maint: rows; parcels; LRA parcels', '37,543; 11,972; 7,425',
    """SELECT (SELECT count(*) FROM ledger WHERE service_type = 'Grass Maint' AND year(service_date) = 2026),
              count(DISTINCT parcel), count(DISTINCT parcel) FILTER (WHERE parcel IN (SELECT parcel_id FROM lra)), count(*)
       FROM cuts WHERE service_type = 'Grass Maint' AND year(service_date) = 2026""",
    lambda r: f'{r[0]:,} rows ({r[3]:,} distinct parcel-days); {r[1]:,}; {r[2]:,}',
    'Rows repeat in the ledger; a cut is a distinct parcel-day.')
add('ledger_rotation1', 'Parcels with a Grass Maint cut 6 Apr-26 May 2026 (CityStat first rotation 7,099)', '7,545',
    """SELECT count(DISTINCT parcel) FROM cuts WHERE service_type = 'Grass Maint'
       AND service_date BETWEEN DATE '2026-04-06' AND DATE '2026-05-26'""",
    lambda r: f'{r[0]:,}')
for code, goal, theirs in [('Potholes - Major St', 3, '48.6% of 494 (CityStat 44.5% of 443)'),
                           ('Potholes - Residnl', 8, '81.1% (CityStat 90.6%)'),
                           ('Potholes - Alley', 17, '82.9% (CityStat 98.2%)')]:
    add(f'citystat_q2_{code}', f'Q2 2026 {code}: initiated in quarter, closed within {goal} whole days', theirs,
        f"""SELECT round(100.0 * avg(CAST(status_group = 'closed' AND floor(days_to_close) <= {goal} AS INT)), 1), count(*), sum(source_rows)
            FROM requests WHERE problem_code = '{code}' AND ts_init >= TIMESTAMP '2026-04-01' AND ts_init < TIMESTAMP '2026-07-01'""",
        lambda r: f'{r[0]}% of {r[1]:,} ids ({r[2]:,} rows)')
add('promise_resid_q2', 'Residential potholes Q2 2026 closed by promise date, among closed', '83.3% of 978 closed',
    """SELECT round(100.0 * avg(CAST(closed_by_promise AS INT)), 1), count(*) FROM promise
       WHERE problem_code = 'Potholes - Residnl' AND status_group = 'closed'
         AND ts_init >= TIMESTAMP '2026-04-01' AND ts_init < TIMESTAMP '2026-07-01'""",
    lambda r: f'{r[0]}% of {r[1]:,} closed')
add('promise_populated', 'PRJCOMPLETEDATE populated; DATEINVTDONE populated (2024-26)', '~98%; ~85%',
    """SELECT round(100 * avg(CAST(ts_promised IS NOT NULL AS INT)), 1), round(100 * avg(CAST(ts_invt_done IS NOT NULL AS INT)), 1)
       FROM requests WHERE init_year >= 2024""",
    lambda r: f'{r[0]}%; {r[1]}%')
add('promise_offsets', 'Median promise offset (days): single light out, cave-ins, towing, potholes residential, alley, illegal dumping, debris, tree inspection, weeds lot, weeds bldg',
    '3, 3, 5, 8, 16, 10, 3, 14, 14, 90',
    """SELECT list(round(m, 0) ORDER BY k) FROM (
         SELECT CASE problem_code WHEN 'Single Light Out' THEN 1 WHEN 'Cave-Ins' THEN 2 WHEN 'Vehicle Towing' THEN 3
                WHEN 'Potholes - Residnl' THEN 4 WHEN 'Potholes - Alley' THEN 5 WHEN 'Illegal dumpg report' THEN 6
                WHEN 'Debris-alley/street' THEN 7 WHEN 'Inspect City Tree' THEN 8 WHEN 'Weeds-Vacant Lot' THEN 9
                WHEN 'Weeds-Vacant Bldg' THEN 10 END AS k, median(promise_days) AS m
         FROM requests WHERE init_year >= 2025 GROUP BY 1) WHERE k IS NOT NULL""",
    lambda r: ', '.join(str(int(x)) for x in r[0]))
# Like-for-like ward comparisons: resident channels, since 16 May 2025
add('lfl_cave_all', 'Cave-ins closed, wards 1-5 vs 10-14, median days (resident, since tornado)', '1.1 vs (not stated)',
    LFL.format(code='Cave-Ins', extra=''), lambda r: f'{r[0]} (n={r[1]}) vs {r[2]} (n={r[3]})')
add('lfl_cave_referred', 'Cave-ins closed "referred to street maintenance...", wards 1-5: n and median', '385; 0.8',
    LFL.format(code='Cave-Ins', extra="AND res_key LIKE 'referred to street maintenance%'"),
    lambda r: f'{r[1]}; {r[0]} (wards 10-14: n={r[3]}, {r[2]})')
add('lfl_cave_done', 'Cave-ins "work completed", wards 1-5 vs 10-14', '9.6 (n=44) vs 25.1 (n=137)',
    LFL.format(code='Cave-Ins', extra="AND res_key = 'work completed'"), lambda r: f'{r[0]} (n={r[1]}) vs {r[2]} (n={r[3]})')
add('lfl_cave_share', 'Cave-ins share closed, wards 1-5 vs 10-14 (resident, since tornado)', '75% vs 45%',
    """SELECT round(100 * avg(CAST(status_group = 'closed' AS INT)) FILTER (WHERE ward_group = '1-5'), 0),
              round(100 * avg(CAST(status_group = 'closed' AS INT)) FILTER (WHERE ward_group = '10-14'), 0)
       FROM requests WHERE problem_code = 'Cave-Ins' AND channel_group = 'resident' AND ts_init >= TIMESTAMP '2025-05-16'""",
    lambda r: f'{r[0]:.0f}% vs {r[1]:.0f}%')
add('lfl_tree_wo', 'Inspect City Tree "removal work order created", wards 1-5 vs 10-14', '125 vs 204',
    LFL.format(code='Inspect City Tree', extra="AND res_key = 'removal work order created'"),
    lambda r: f'{r[0]} (n={r[1]}) vs {r[2]} (n={r[3]})')
add('lfl_light_done', 'Single light out "work completed", wards 1-5 vs 10-14', '15.8 vs 42.1',
    LFL.format(code='Single Light Out', extra="AND res_key = 'work completed'"),
    lambda r: f'{r[0]} (n={r[1]}) vs {r[2]} (n={r[3]})')
add('lfl_tow_tagged', 'Towing "vehicle tagged for tow", wards 1-5 vs 10-14', '12.3 vs 41.0',
    LFL.format(code='Vehicle Towing', extra="AND res_key = 'vehicle tagged for tow'"),
    lambda r: f'{r[0]} (n={r[1]}) vs {r[2]} (n={r[3]})')
add('lfl_wholeblock', 'Whole-block lights out closed, wards 1-5 vs 10-14', '0.7 vs 0.7',
    LFL.format(code='Whole Blk Lights Out', extra=''), lambda r: f'{r[0]} (n={r[1]}) vs {r[2]} (n={r[3]})')

if __name__ == '__main__':
    out = os.path.join(ROOT, 'build', 'N1', 'validation.json')
    with open(out, 'w') as fh:
        json.dump(checks, fh, indent=1, default=str)
    for c in checks:
        print(f"{c['id']:28s} theirs: {c['theirs']:40s} ours: {c['ours']}")
