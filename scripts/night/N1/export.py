#!/usr/bin/env python3
"""DoneStat pipeline, step 2 (N1): build/stl.duckdb -> build/out/*.json, *.csv.

Everything written here is aggregated or block level. Request-level exact
addresses and parcel ids never leave the database (see receipt_private).
Also writes build/out/figures.json: N1's own figures (computed live, so a
weekly run refreshes them) merged with every build/N*/figures.json present.

Run: .venv/bin/python -I scripts/night/N1/export.py
"""
import csv
import datetime as dt
import glob
import json
import os
import shutil
import sys

import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('STL_ROOT', os.path.abspath(os.path.join(HERE, '..', '..', '..')))
OUT = os.path.join(ROOT, 'build', 'out')
DB = os.path.join(ROOT, 'build', 'stl.duckdb')
SCRIPT = 'scripts/night/N1/export.py'
os.makedirs(OUT, exist_ok=True)
con = duckdb.connect(DB, read_only=True)

SRC_311 = "311 service requests (City of St. Louis open data, csb.zip yearly CSVs, invalid UTF-8 bytes dropped, one row per REQUESTID)"
SRC_LEDGER = "the Forestry Division's service ledger (forestry-service-records.csv, cuts = 'Grass Maint' and 'Weed-Grass' rows)"
SRC_MSD = "MSD's parcel address file (msd_parcels_stl_city_attrs.jsonl, owner names never read)"
SRC_CW = "Cityworks tree work-order samples (city map server saved searches, 1,500 rows each, staff fields removed)"


def rows(sql, params=None):
    cur = con.execute(sql, params or [])
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def one(sql):
    return con.execute(sql).fetchone()


def clean(v):
    if isinstance(v, float):
        return None if v != v else round(v, 4)
    if isinstance(v, (dt.datetime, dt.date)):
        return v.isoformat()
    if isinstance(v, list):
        return [clean(x) for x in v]
    if isinstance(v, dict):
        return {k: clean(x) for k, x in v.items()}
    return v


def dump(name, obj, contract=None, sources=(), notes=()):
    """Write build/out/<name> with the site's envelope (site/DATA-CONTRACT.md)."""
    if isinstance(obj, dict):
        srcs = []
        for sp in ('build/stl.duckdb',) + tuple(sources):
            fp = os.path.join(ROOT, sp)
            srcs.append({'path': sp, 'mtime': dt.datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%Y-%m-%d %H:%M')
                         if os.path.exists(fp) else None})
        obj = {'meta': {'contract': f"{contract or name.rsplit('.', 1)[0]}/1", 'mock': False,
                        'built_at': META['built_at'], 'sources': srcs, 'notes': list(notes)}, **obj}
    with open(os.path.join(OUT, name), 'w') as fh:
        json.dump(clean(obj), fh, indent=1, default=str)
    print(f'wrote build/out/{name}')


META = {r['key']: r['value'] for r in rows("SELECT key, value FROM meta")}
ASOF = META['asof']
RUN = {'asof': ASOF, 'ledger_max_date': META['ledger_max_date'], 'built_at': META['built_at'],
       'closure_class_source': META['closure_class_source'], 'n2_code_file_mtime': META.get('n2_code_file_mtime'),
       'definition_note': 'Our definitions, computed from the public files; not City figures.',
       'privacy': 'Aggregated or block level only (house number rounded down to the hundred). No names, no staff fields.'}
SENS = "(SELECT problem_code FROM sensitive_codes)"

MAIN_TYPES = ['Weeds-Vacant Lot', 'Weeds-Vacant Bldg', 'Inspect City Tree', 'Cave-Ins', 'Single Light Out',
              'Vehicle Towing', 'Potholes - Residnl', 'Illegal dumpg report', 'Refuse not collected',
              'Whole Blk Lights Out']
MAIN_SQL = '(' + ', '.join("'" + t.replace("'", "''") + "'" for t in MAIN_TYPES) + ')'

# ------------------------------------------------------------------ scoreboard
def scoreboard():
    types = [r['problem_code'] for r in rows(f"""
        SELECT problem_code FROM requests WHERE init_year >= 2025 AND problem_code IS NOT NULL
        GROUP BY 1 HAVING count(*) >= 300 ORDER BY count(*) DESC""")]
    sel = """count(*) AS n,
             median(promise_days) AS promise_days,
             count(*) FILTER (WHERE status_group = 'closed') AS n_closed,
             count(*) FILTER (WHERE status_group = 'open') AS n_open,
             count(*) FILTER (WHERE status_group = 'cancelled') AS n_cancelled,
             median(days_to_close) AS median_days_to_close,
             avg(CASE WHEN promise_due THEN CAST(coalesce(closed_by_promise, false) AS INT) END) AS closed_by_promise_of_due,
             avg(CASE WHEN status_group = 'closed' THEN CAST(closed_by_promise AS INT) END) AS closed_by_promise_of_closed,
             avg(CASE WHEN promise_due THEN CAST(coalesce(done_by_promise, false) AS INT) END) AS done_by_promise_of_due,
             avg(CASE WHEN status_group = 'closed' THEN CAST(closure_class = 'done' AS INT) END) AS closed_share_done,
             avg(CASE WHEN status_group = 'closed' THEN CAST(closure_class IN ('handed_off', 'converted') AS INT) END) AS closed_share_handoff,
             avg(CASE WHEN status_group = 'closed' THEN CAST(closure_class = 'no_action' AS INT) END) AS closed_share_no_action,
             avg(CASE WHEN status_group = 'closed' THEN CAST(closure_class = 'blank' AS INT) END) AS closed_share_blank,
             any_value(citystat_goal_days) AS citystat_goal_days,
             avg(CAST(within_citystat_goal AS INT)) AS within_citystat_goal_of_all"""
    by_q = rows(f"""SELECT problem_code, any_value(type_name) AS type_name, init_quarter AS quarter, {sel}
                    FROM promise WHERE init_year >= 2025 AND problem_code IN (SELECT unnest(?))
                    GROUP BY problem_code, init_quarter ORDER BY problem_code, quarter""", [types])
    total = rows(f"""SELECT problem_code, any_value(type_name) AS type_name, '2025-01-01 to {ASOF}' AS quarter, {sel}
                     FROM promise WHERE init_year >= 2025 AND problem_code IN (SELECT unnest(?))
                     GROUP BY problem_code ORDER BY n DESC""", [types])
    ledger_check = rows("""SELECT problem_code, init_quarter AS quarter, count(*) AS n_parcel_matched_promise_passed,
                                avg(CAST(cut_by_promise AS INT)) AS ledger_cut_by_promise,
                                avg(CAST(status_group = 'closed' AND closure_class IN ('handed_off', 'converted') AS INT)) AS closed_as_handoff
                         FROM weed_promise_ledger WHERE promise_due_in_ledger AND init_year >= 2023
                         GROUP BY ALL ORDER BY problem_code, quarter""")
    coverage = rows("""SELECT year(service_date) AS year, count(*) AS cut_rows, count(DISTINCT parcel) AS parcels
                       FROM cuts WHERE service_date >= DATE '2019-01-01' GROUP BY 1 ORDER BY 1""")
    ledger_total = rows("""SELECT problem_code, count(*) AS n_parcel_matched_promise_passed,
                                avg(CAST(cut_by_promise AS INT)) AS ledger_cut_by_promise,
                                avg(CAST(status_group = 'closed' AND closure_class IN ('handed_off', 'converted') AS INT)) AS closed_as_handoff
                         FROM weed_promise_ledger WHERE promise_due_in_ledger AND init_year = 2026
                         GROUP BY ALL ORDER BY n_parcel_matched_promise_passed DESC""")
    dump('scoreboard_n1.json', {'run': RUN,
        'ledger_check': {'definition': "Weed and missed-cut requests on vacant lots and buildings, matched to a parcel, whose promised date has passed by the ledger's last date: share with a grass cut recorded on the parcel between filing and the promised date (forestry ledger; posting dates batched weekly).",
                         'totals_period': '2026 filings only: the 2025 ledger is thin (13,168 cut rows on 8,780 parcels vs 46,346 on 16,118 in 2026), so 2025 is shown by quarter but not totalled',
                         'ledger_coverage_by_year': coverage,
                         'totals': ledger_total, 'by_quarter': ledger_check},
        'columns': {
        'promise_days': "median days between filing and the city's own promised date (PRJCOMPLETEDATE)",
        'closed_by_promise_of_due': 'closed on or before the promised date, among requests whose promised date has passed (open and cancelled count as not closed)',
        'closed_by_promise_of_closed': 'closed on or before the promised date, among closed requests',
        'done_by_promise_of_due': "closed with words that record finished work (N2 class 'done') on or before the promised date, among requests whose promised date has passed; the column CityStat lacks",
        'closed_share_handoff': "share of closures whose words record a hand-off or a work order (N2 classes 'handed_off' + 'converted')",
        'within_citystat_goal_of_all': "closed within CityStat's published goal, among all requests (six types only)"},
        'totals': total, 'by_quarter': by_q},
        notes=['Pipeline scoreboard. The site reads N4\'s build/N4/scoreboard.json; this file adds the weeds ledger check and lets a weekly run refresh the same measures.'])


# ------------------------------------------------------------------ ward like-for-like
def ward_lfl():
    types = ['Cave-Ins', 'Inspect City Tree', 'Single Light Out', 'Vehicle Towing', 'Whole Blk Lights Out',
             'Potholes - Residnl', 'Refuse not collected', 'Sidewalk Repair', 'Illegal dumpg report', 'Weeds-Vacant Lot']
    base = """FROM v_requests WHERE channel_group = 'resident' AND problem_code IN (SELECT unnest(?))
              AND ts_init >= TIMESTAMP '2025-05-16' AND ward IS NOT NULL"""
    overall = rows(f"""SELECT problem_code, ward_group, count(*) AS n,
                         avg(CAST(status_group = 'closed' AS INT)) AS share_closed,
                         median(days_to_close) AS median_days_closed
                       {base} GROUP BY 1, 2 ORDER BY 1, 2""", [types])
    by_class = rows(f"""SELECT problem_code, ward_group, closure_class, count(*) AS n, median(days_to_close) AS median_days
                        {base} AND status_group = 'closed' GROUP BY 1, 2, 3 ORDER BY 1, 2, 3""", [types])
    texts = rows(f"""WITH t AS (SELECT problem_code, res_key, count(*) AS n {base} AND status_group = 'closed' GROUP BY 1, 2),
                     top AS (SELECT * FROM t QUALIFY row_number() OVER (PARTITION BY problem_code ORDER BY n DESC) <= 5)
                     SELECT r.problem_code, any_value(r.resolution_public) AS closed_with_words, any_value(r.closure_class) AS closure_class, r.ward_group,
                            count(*) AS n, median(r.days_to_close) AS median_days
                     FROM v_requests r JOIN top USING (problem_code, res_key)
                     WHERE r.channel_group = 'resident' AND r.ts_init >= TIMESTAMP '2025-05-16' AND r.status_group = 'closed'
                       AND r.ward IS NOT NULL
                     GROUP BY r.problem_code, r.res_key, r.ward_group ORDER BY 1, 2, 4""", [types])
    per_ward = rows(f"""SELECT problem_code, ward, closure_class, count(*) AS n, median(days_to_close) AS median_days
                        {base} AND status_group = 'closed' GROUP BY 1, 2, 3 ORDER BY 1, 2, 3""", [types])
    dump('ward_like_for_like.json', {'run': RUN,
         'scope': 'Resident channels (WEB, PHONE, EMAIL, CHAT, TWITTER, LETTER), filed on or after 16 May 2025 (the tornado), one row per request.',
         'why': 'Time-to-close mixes paperwork closures (referred, scheduled) with finished work; compare the same closure words across wards.',
         'overall': overall, 'by_class': by_class, 'by_resolution_text': texts, 'by_ward_class': per_ward})


# ------------------------------------------------------------------ register counts
def register():
    fam = rows(f"""
      WITH r AS (SELECT * FROM v_requests WHERE ts_init > (SELECT asof_ts FROM run_dates) - INTERVAL 365 DAY)
      SELECT problem_code, any_value(type_name) AS type_name, any_value(family) AS family, any_value(division) AS division,
             count(*) AS n_12m,
             avg(CAST(ts_promised IS NOT NULL AS INT)) AS share_with_promise,
             median(promise_days) AS promise_days,
             avg(CAST(status_group = 'closed' AS INT)) AS share_closed,
             avg(CAST(status_group = 'cancelled' AS INT)) AS share_cancelled,
             avg(CAST(status_group = 'open' AS INT)) AS share_open,
             avg(CASE WHEN status_group = 'closed' THEN CAST(closure_class = 'done' AS INT) END) AS closed_share_done,
             avg(CASE WHEN status_group = 'closed' THEN CAST(closure_class IN ('handed_off', 'converted') AS INT) END) AS closed_share_handoff,
             avg(CASE WHEN status_group = 'closed' THEN CAST(closure_class = 'no_action' AS INT) END) AS closed_share_no_action,
             avg(CASE WHEN status_group IN ('closed', 'cancelled') THEN CAST(resolution IS NULL AS INT) END) AS share_blank_outcome,
             CASE WHEN problem_code IN (SELECT problem_code FROM weed_ledger_codes) THEN 'forestry ledger (cuts by parcel)'
                  WHEN any_value(family) IN ('tree_city', 'tree_planting') THEN 'Cityworks tree work orders (sample only)'
                  WHEN any_value(family) = 'pothole' THEN 'Cityworks pothole layer (sample; same request ids, no extra completion field)'
                  ELSE 'none on disk' END AS completion_record_joined
      FROM r GROUP BY problem_code HAVING count(*) >= 100 ORDER BY n_12m DESC""")
    rates = rows("""
      SELECT r.problem_code, count(*) AS n, count(rp.request_id) AS n_parcel_matched,
             count(rp.request_id) / count(*) AS parcel_match_rate
      FROM requests r LEFT JOIN request_parcel rp USING (request_id)
      WHERE r.problem_code IN (SELECT problem_code FROM type_family WHERE family = 'weeds') AND r.init_year >= 2025
      GROUP BY 1 ORDER BY n DESC""")
    wo = rows("""
      SELECT r.problem_code, r.status_group, count(*) AS n, count(s.request_id) AS n_with_wo,
             count(s.request_id) / count(*) AS share_with_wo_nearby,
             count(*) FILTER (WHERE s.n_removal_open_before_request > 0) AS n_same_address_removal_order_already_open,
             count(*) FILTER (WHERE s.n_removal_dated_after_request > 0 AND coalesce(s.n_removal_open_before_request, 0) = 0) AS n_same_address_removal_order_dated_after,
             median(s.days_recent_removal_order_before_request) AS median_days_order_open_before_request,
             count(*) FILTER (WHERE s.n_removal_open_before_request_30m > 0) AS n_removal_order_within_30m_already_open
      FROM requests r LEFT JOIN request_wo_summary s USING (request_id)
      WHERE r.problem_code IN (SELECT problem_code FROM type_family WHERE family IN ('tree_city', 'tree_planting'))
        AND r.init_year >= 2025
      GROUP BY 1, 2 ORDER BY 1, 2""")
    dump('register_counts.json', {'run': RUN, 'window': f'requests filed in the 365 days to {ASOF}',
         'types': fam, 'weed_parcel_match_2025_26': rates, 'tree_workorder_match_2025_26': wo,
         'tree_note': "Most tree requests that sit near a removal order were filed while that order was already open (N5; COMMON correction 9): residents reporting a tree the city already knows must come down. 'Converted to a work order' is the rare pattern. Work orders are 1,500-row samples, so all counts are lower bounds."})


# ------------------------------------------------------------------ Monday list
def monday():
    full = rows(f"""SELECT request_id, problem_code, type_name, division, ward, block_label, filed, promised,
                          days_past_promise, age_days, status, channel_group
                   FROM monday_list ORDER BY division, ward, days_past_promise DESC""")
    # COMMON correction 10: no request ids in public files. The city's own copy, with ids,
    # is build/N1/private/monday_list_with_ids.csv (a division would work from that one).
    priv = os.path.join(ROOT, 'build', 'N1', 'private')
    os.makedirs(priv, exist_ok=True)
    for path, data in [(os.path.join(priv, 'monday_list_with_ids.csv'), full),
                       (os.path.join(OUT, 'monday_list.csv'), [{k: v for k, v in r.items() if k != 'request_id'} for r in full])]:
        with open(path, 'w', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0].keys()) if data else ['problem_code'])
            w.writeheader()
            for r in data:
                w.writerow({k: clean(v) for k, v in r.items()})
    print('wrote build/out/monday_list.csv (no ids) and build/N1/private/monday_list_with_ids.csv')
    lst = [{k: v for k, v in r.items() if k != 'request_id'} for r in full]
    summary = rows("""SELECT division, problem_code, ward, count(*) AS n_open_past_promise,
                             median(days_past_promise) AS median_days_past_promise,
                             count(*) FILTER (WHERE age_days > 365) AS n_over_a_year
                      FROM monday_list GROUP BY 1, 2, 3 ORDER BY n_open_past_promise DESC""")
    recent = [r for r in lst if r['filed'] and r['filed'] >= dt.date.fromisoformat(ASOF) - dt.timedelta(days=365)]
    mow = rows("""SELECT ward, count(*) AS rotation_lots_2026,
                         count(*) FILTER (WHERE longest_gap_incl_open > 90) AS lots_with_gap_over_90_days,
                         count(*) FILTER (WHERE longest_gap_incl_open > 90 AND is_lra) AS lra_lots_with_gap_over_90_days,
                         count(*) FILTER (WHERE longest_gap_incl_open > 42) AS lots_with_gap_over_42_days,
                         count(*) FILTER (WHERE cuts_2026 = 1) AS lots_cut_once,
                         median(longest_gap_incl_open) AS median_longest_gap_days
                  FROM mowing_gaps GROUP BY ward ORDER BY ward NULLS LAST""")
    mow_blocks = rows("""SELECT a.block_label AS block, g.ward, count(*) AS lots_with_gap_over_90_days,
                                max(g.longest_gap_incl_open) AS longest_gap_days,
                                sum(g.weed_requests_2026) AS weed_requests_2026,
                                count(*) FILTER (WHERE g.is_lra) AS of_which_lra
                         FROM mowing_gaps g
                         JOIN (SELECT pid, any_value(PROP_ADD) AS prop_add FROM parcels GROUP BY pid) p ON p.pid = g.parcel
                         JOIN addr_lookup a ON a.addr_raw = p.prop_add
                         WHERE g.longest_gap_incl_open > 90
                         GROUP BY 1, 2 ORDER BY weed_requests_2026 DESC, longest_gap_days DESC LIMIT 300""")
    by_ward_n = rows("SELECT ward, count(*) AS n FROM monday_list GROUP BY ward ORDER BY ward NULLS LAST")
    by_type_n = rows("SELECT type_name AS type, problem_code, count(*) AS n FROM monday_list GROUP BY 1, 2 ORDER BY n DESC")
    contract_rows = [{'type_name': r['type_name'], 'problem_code': r['problem_code'], 'division': r['division'],
                      'ward': r['ward'], 'block': r['block_label'], 'filed': r['filed'], 'promised': r['promised'],
                      'days_past_promise': r['days_past_promise'], 'age_days': r['age_days'], 'status': r['status']}
                     for r in recent]
    mowing = {'season': '2026', 'title': 'Mowing rotation, 2026 season (retrospective)',
              'definition': "Parcels with at least one 'Grass Maint' cut in the forestry ledger between 1 Apr and 30 Sep 2026 (the rotation). Gap = longest stretch between consecutive cuts, or from the last cut to 30 Sep. Flag: more than 90 days, about one and a half of the city's own observed cycles (median longest gap between cuts 54 days); BUILD-SPEC's 42-day threshold flags almost every lot because the rotation itself runs about eight weeks. Posting dates are batched weekly, so gaps are good to about a week. Ward from the LRA inventory or a matched 311 request; blank where neither exists.",
              'rows': [{'ward': m['ward'], 'parcels_on_rotation': m['rotation_lots_2026'],
                        'parcels_gap_over_42d': m['lots_with_gap_over_42_days'],
                        'parcels_gap_over_90d': m['lots_with_gap_over_90_days'],
                        'lra_parcels_gap_over_90d': m['lra_lots_with_gap_over_90_days'],
                        'parcels_cut_once': m['lots_cut_once'],
                        'median_longest_gap': m['median_longest_gap_days']} for m in mow],
              'blocks_top_300': mow_blocks}
    dump('monday_list.json', {'asof': ASOF,
         'definition': "Open requests (status neither closed nor cancelled) whose city-set promised date (PRJCOMPLETEDATE) is before the run date. Block level, no request ids. Excludes encampment, homeless, welfare-check, discrimination, legal-claim and court codes.",
         'n_total': len(lst), 'rows_scope': 'rows filed in the 365 days to the run date; the CSV has every row, all years',
         'by_ward': by_ward_n, 'by_type': by_type_n, 'summary': summary, 'rows': contract_rows,
         'csv': 'downloads/monday_list.csv', 'mowing': mowing}, contract='monday')
    dump('mowing_2026.json', mowing, contract='mowing')


# ------------------------------------------------------------------ dumping
def dumping():
    blocks = rows("""SELECT * FROM dumping_blocks WHERE n_requests >= 3 ORDER BY n_requests DESC""")
    summ = one("""SELECT count(*), count(*) FILTER (WHERE n_requests >= 3), count(*) FILTER (WHERE n_requests >= 10),
                         sum(n_requests), sum(n_requests) FILTER (WHERE n_requests >= 3) FROM dumping_blocks""")
    out = rows("""SELECT problem_code, closure_class, count(*) AS n, median(days_to_close) AS median_days
                  FROM v_requests WHERE family = 'dumping' AND status_group = 'closed'
                    AND init_date > (SELECT asof_date FROM run_dates) - 365
                  GROUP BY 1, 2 ORDER BY 1, n DESC""")
    contract_blocks = [{'block': b['block_label'], 'ward': b['ward'], 'n_requests': b['n_requests'],
                        'n_addresses': b['n_addresses'], 'n_illegal_dumping_reports': b['n_illegal_dumping_reports'],
                        'n_debris_reports': b['n_debris_reports'], 'first_report': b['first_report'],
                        'last_report': b['last_report'], 'n_closed_done': b['n_closed_done'],
                        'n_closed_handoff': b['n_closed_handoff'], 'n_closed_no_action': b['n_closed_no_action'],
                        'n_open': b['n_open'], 'median_days_to_close': b['median_days_to_close']} for b in blocks[:200]]
    dump('dumping_blocks.json', {'window': f'filed in the 365 days to {ASOF}',
         'definition': "Requests coded 'Illegal dumpg report' or 'Debris-alley/street', grouped by block (house number rounded down to the hundred) and ward. Repeat block = 3 or more requests in the window.",
         'summary': {'requests': summ[3], 'blocks': summ[0], 'repeat_blocks': summ[1], 'blocks_10plus': summ[2],
                     'requests_on_repeat_blocks': summ[4], 'share_repeat': summ[4] / summ[3] if summ[3] else None},
         'outcomes': out, 'blocks': contract_blocks}, contract='dumping')


# ------------------------------------------------------------------ receipts
def fmt_date(v):
    if v is None:
        return None
    d = v.date() if isinstance(v, dt.datetime) else v
    return f"{d.day} {d.strftime('%B %Y')}"


def days(n):
    n = int(n)
    return f'{n} day' if n == 1 else f'{n} days'


def receipt_line(r):
    """Template sentence for the receipt card. No AI; plain string rules."""
    parts = []
    if r['status_group'] == 'closed':
        day = int(r['days_to_close']) if r['days_to_close'] is not None else None
        words = f"“{r['closed_with_words']}”" if r['closed_with_words'] else 'no words at all'
        parts.append(f"Closed on day {day} with {words}." if day is not None else f"Closed with {words}.")
    elif r['status_group'] == 'cancelled':
        words = f"“{r['closed_with_words']}”" if r['closed_with_words'] else 'no explanation'
        parts.append(f"Cancelled with {words}.")
    else:
        parts.append(f"Still open (status {r['status']}).")
    if r['promised']:
        if r['status_group'] == 'closed' and r['days_vs_promise'] is not None:
            parts.append(f"The city's own promised date was {fmt_date(r['promised'])}; it closed "
                         + ('before it.' if r['days_vs_promise'] <= 0 else f"{days(r['days_vs_promise'])} after it."))
        else:
            parts.append(f"The city's own promised date was {fmt_date(r['promised'])}.")
    if r['family'] == 'weeds' and r['parcel_match_method']:
        yr = r['filed'].year
        if r['ledger_first_cut_after'] and r['ledger_first_cut_after'].year == yr:
            parts.append(f"Its forestry ledger first records a cut on this lot on {fmt_date(r['ledger_first_cut_after'])}, "
                         f"{days(r['ledger_days_to_first_cut'])} after the request.")
        elif r['filed'].date() <= r['ledger_max']:
            parts.append(f"Its forestry ledger records no cut on this lot after the request in {yr}"
                         + (" (but the 2025 ledger is incomplete, so this is not proof)." if yr == 2025 else "."))
    if r['family'] in ('tree_city', 'tree_planting'):
        wos = r['work_orders'] or []
        dated = [w for w in wos if w.get('days_from_order_to_request') is not None]
        same_before = [w for w in dated if w.get('source') == 'tree_removal' and w.get('addr_match')
                       and w['days_from_order_to_request'] > 1]
        near_before = [w for w in dated if w.get('source') == 'tree_removal' and not w.get('addr_match')
                       and w['days_from_order_to_request'] > 1]
        after = [w for w in dated if w['days_from_order_to_request'] <= 1]
        if same_before:
            w = min(same_before, key=lambda x: x['days_from_order_to_request'])
            parts.append(f"A Forestry removal order at this address was already open, started {days(w['days_from_order_to_request'])} "
                         f"before this request (status {w['status']} in the city's sample).")
        elif after:
            w = after[0]
            parts.append(f"A Forestry work order ({w['description']}, {w['status']}) dated "
                         f"{days(max(0, -w['days_from_order_to_request']))} after this request appears at or within 30 m of this location.")
        elif near_before:
            parts.append("A Forestry removal order for a tree within 30 m (possibly a neighbouring tree) was already open when this request was filed.")
        elif wos:
            w = wos[0]
            parts.append(f"An undated Forestry work order ({w['description']}, {w['status']}) appears at or within 30 m of this location.")
        else:
            parts.append("No Forestry work order appears at this location in the city's published sample (a sample, so this is not proof of none).")
    if r['next_same_request_filed'] is not None and r['days_to_next_same_request'] is not None and r['days_to_next_same_request'] <= 30:
        parts.append(f"The same problem was reported again at this address {days(r['days_to_next_same_request'])} after closure.")
    return ' '.join(parts)


def timeline(r):
    """Contract shape: [{date, kind, title, detail, source, label}]."""
    def ev(date, kind, title, detail, source):
        return {'date': date, 'kind': kind, 'title': title, 'detail': detail, 'source': source, 'label': 'observed'}
    out = [ev(r['filed'], 'filed', 'Filed with 311', f"{r['type_name'] or r['problem_code']}, {r['public_address']}", '311 (DATETIMEINIT)')]
    if r['investigation_done']:
        out.append(ev(r['investigation_done'], 'record', 'Investigation recorded done', None, '311 (DATEINVTDONE)'))
    if r['promised']:
        out.append(ev(r['promised'], 'promised', "The city's own promised date", f"{days(r['promise_days'])} after filing" if r['promise_days'] is not None else None, '311 (PRJCOMPLETEDATE)'))
    if r['closed']:
        out.append(ev(r['closed'], 'closed', 'Closed', r['closed_with_words'] or '(no words)', '311 (DATETIMECLOSED, PUBLICRESOLUTION)'))
    if r['cancelled']:
        out.append(ev(r['cancelled'], 'cancelled', 'Cancelled', r['closed_with_words'] or '(no words)', '311 (DATECANCELLED)'))
    for d in (r['ledger_cut_dates_same_year'] or []):
        out.append(ev(d, 'record', 'Grass cut recorded on this lot', 'Posting date; the ledger posts in weekly batches', 'Forestry service ledger'))
    for w in (r['work_orders'] or []):
        d = w.get('proj_start') or w.get('actual_finish')
        already = (w.get('days_from_order_to_request') or 0) > 1
        out.append(ev(d, 'record', f"Forestry work order: {w.get('description')} ({w.get('status')})",
                      ('at this address' if w.get('addr_match') else f"{w.get('dist_m')} m away, possibly another tree")
                      + ('; already open when the request was filed' if already else ''), 'Cityworks work-order sample'))
    if r['next_same_request_filed']:
        out.append(ev(r['next_same_request_filed'], 'refiled', 'Same problem reported again at this address',
                      f"{days(r['days_to_next_same_request'])} after closure" if r['days_to_next_same_request'] is not None else None, '311'))
    return sorted(out, key=lambda e: str(e['date']))


def receipts():
    # N5 keeps hero request ids private (build/N5/private/heroes_private.json): a request id
    # leads back to the exact address in the city's own file. Hero receipts therefore go to
    # build/N1/private/, and the public file carries only the hashed random sample.
    hero_ids = []
    hp = os.path.join(ROOT, 'build', 'N5', 'private', 'heroes_private.json')
    if os.path.exists(hp):
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in ('request_id', 'request_ids', 'requestid'):
                        for x in (v if isinstance(v, list) else [v]):
                            try:
                                hero_ids.append(int(x))
                            except (TypeError, ValueError):
                                pass
                    else:
                        walk(v)
            elif isinstance(o, list):
                for x in o:
                    walk(x)
        walk(json.load(open(hp)))
    sample = [r['request_id'] for r in rows(f"""
        SELECT request_id FROM requests WHERE problem_code IN {MAIN_SQL} AND status_group = 'closed' AND init_year >= 2025
          AND problem_code NOT IN {SENS} AND block_label IS NOT NULL AND block_label <> ''
        QUALIFY row_number() OVER (PARTITION BY problem_code ORDER BY hash(request_id, 20261013)) <= 20""")]
    ids = list(dict.fromkeys(hero_ids + sample))
    rs = rows(f"SELECT * FROM receipt_base WHERE request_id IN (SELECT unnest(?)) AND NOT sensitive", [ids])
    out = {}
    for r in rs:
        rec = {k: r[k] for k in ('problem_code', 'type_name', 'division', 'ward', 'neighborhood',
                                 'channel_group', 'public_address', 'address_level', 'is_lra', 'filed', 'promised',
                                 'promise_days', 'investigation_done', 'closed', 'cancelled', 'status', 'status_group',
                                 'closed_with_words', 'closure_class', 'class_source', 'days_to_close',
                                 'closed_by_promise', 'done_by_promise', 'days_vs_promise',
                                 'ledger_cuts_30d_before', 'ledger_first_cut_after', 'ledger_days_to_first_cut',
                                 'ledger_no_cut_in_season', 'ledger_cut_within_30', 'ledger_cut_within_60',
                                 'work_orders_nearby', 'next_same_request_filed',
                                 'days_to_next_same_request', 'in_cityworks_pothole_sample')}
        rec['parcel_matched'] = r['parcel_match_method'] is not None
        rec['ledger_cut_dates_same_year'] = r['ledger_cut_dates_same_year']
        rec['work_orders'] = [{k: w[k] for k in ('source', 'description', 'status', 'proj_start',
                                                 'proj_finish', 'actual_finish', 'addr_match', 'dist_m',
                                                 'days_from_order_to_request')}
                              for w in (r['work_orders'] or [])]
        rec['timeline'] = timeline(r)
        rec['summary_line'] = receipt_line(r)
        rec['is_hero'] = r['request_id'] in hero_ids
        rec['_request_id'] = r['request_id']  # removed before anything public is written
        out[str(r['request_id'])] = rec
    heroes = {k: v for k, v in out.items() if v['is_hero']}
    # COMMON correction 10: public receipts are keyed by an opaque sequence number; the
    # key to request ids stays in build/N1/private/receipts_key.json.
    pub_items = sorted([v for v in out.values() if not v['is_hero']], key=lambda v: (v['problem_code'], str(v['filed'])))
    key, public = {}, {}
    for i, v in enumerate(pub_items, 1):
        seq = f'R{i:03d}'
        key[seq] = v.pop('_request_id')
        public[seq] = v
    for v in heroes.values():
        v.pop('_request_id', None)
    with open(os.path.join(ROOT, 'build', 'N1', 'private', 'receipts_key.json'), 'w') as fh:
        json.dump({'note': 'PRIVATE: maps public receipt numbers to city request ids. Do not publish.', 'key': key}, fh, indent=1)
    os.makedirs(os.path.join(ROOT, 'build', 'N1', 'private'), exist_ok=True)
    with open(os.path.join(ROOT, 'build', 'N1', 'private', 'receipts_heroes.json'), 'w') as fh:
        json.dump(clean({'run': RUN, 'note': 'PRIVATE: hero request ids from build/N5/private/heroes_private.json. Do not publish.',
                         'missing': [i for i in hero_ids if str(i) not in out], 'receipts': heroes}), fh, indent=1, default=str)
    print(f'wrote build/N1/private/receipts_heroes.json ({len(heroes)} hero receipts)')
    lst = []
    for seq, v in public.items():
        v = dict(v)
        v['receipt_no'] = seq
        v['line'] = v.pop('summary_line')
        v.pop('is_hero', None)
        v['image'] = None
        lst.append(v)
    public = lst
    dump('receipts.json', {'run': RUN, 'n': len(public), 'heroes': [],
                           'sample_rule': '20 closed requests filed 2025-26 per main type, chosen by a fixed hash of the request id',
                           'privacy': 'Block level for every request, LRA lots included (13 Oct ruling). No request, work-order or parcel ids (COMMON correction 10): receipts are numbered R001... Sensitive codes excluded. Uncommon free text withheld; e-mail addresses removed. Hero cases are in build/N5/heroes.json (block level, no ids).',
                           'receipts': public}, contract='receipts',
         notes=['Hero receipts come from build/N5/heroes.json; the bridge fills heroes.'])


# ------------------------------------------------------------------ by ward (compact)
def by_ward():
    data = rows(f"""SELECT problem_code, ward, init_quarter AS quarter, channel_group, n, n_closed, n_open, n_cancelled,
                           median_days, median_promise_days, share_closed_by_promise, share_closed_by_promise_due,
                           share_done_by_promise_due, open_share, share_closed_done, share_closed_handoff
                    FROM by_ward_type WHERE init_quarter >= '2024Q1' AND problem_code IN {MAIN_SQL}
                    ORDER BY problem_code, ward, quarter, channel_group""")
    dump('by_ward.json', {'run': RUN, 'types': MAIN_TYPES, 'rows': data,
                          'note': 'Full type x ward x quarter x channel x class table is by_ward in build/stl.duckdb.'})


# ------------------------------------------------------------------ figures
FIGS = []


def fig(fid, sql, unit, period, definition, derivation, label='observed', note='', pick=lambda r: r[0]):
    try:
        r = one(sql)
        value = clean(pick(r))
    except Exception as e:
        value, note = None, f'ERROR {e}'
    FIGS.append({'id': fid, 'value': value, 'unit': unit, 'period': period, 'definition': definition,
                 'label': label, 'source_sql_or_script': f'{SCRIPT} (figure {fid}); views in scripts/night/N1/measures.sql',
                 'note': note, 'derivation': derivation, 'owner': 'N1'})


def figures():
    p12 = f"13 Oct 2025 to {ASOF}"
    fig('n1_requests_12m', """SELECT count(*) FROM requests WHERE ts_init > (SELECT asof_ts FROM run_dates) - INTERVAL 365 DAY""",
        'requests', p12, 'Distinct 311 request ids filed in the 365 days to the run date.',
        f"{SRC_311}. Counted distinct request ids; the city's CSV repeats about 7% of ids once per caller, so row counts run higher.")
    fig('n1_open_backlog_2023plus', """SELECT count(*) FROM requests WHERE status_group = 'open' AND init_year >= 2023""",
        'requests', f'filed 2023 to {ASOF}, open on {ASOF}', 'Requests filed since 1 Jan 2023 whose status is neither closed nor cancelled.',
        f"{SRC_311}. Status compared case-insensitively (the file has 'Closed' beside 'CLOSED').")
    fig('n1_open_over_a_year', """SELECT count(*) FROM requests WHERE status_group = 'open' AND init_year >= 2023
        AND ts_init < (SELECT asof_ts FROM run_dates) - INTERVAL 365 DAY""",
        'requests', f'open on {ASOF}', 'Of the open backlog filed since 2023, those filed more than 365 days before the run date.',
        f"{SRC_311}. Age measured from the filing time to the latest filing time in the file.")
    fig('n1_promise_populated', """SELECT avg(CAST(ts_promised IS NOT NULL AS INT)) FROM requests WHERE init_year >= 2024""",
        'share', f'filed 2024 to {ASOF}', "Share of requests carrying the city's own promised completion date (PRJCOMPLETEDATE).",
        f"{SRC_311}. PRJCOMPLETEDATE is a fixed offset per request type (3 days for a light out, 90 for weeds at a vacant building).")
    fig('n1_open_past_promise', """SELECT count(*) FROM monday_list""", 'requests', f'open on {ASOF}',
        "Open requests whose city-set promised date has passed (the Monday list), all years, sensitive codes excluded.",
        f"{SRC_311}. Open = status neither closed nor cancelled; compared with PRJCOMPLETEDATE at the run date.")
    fig('n1_open_past_promise_12m', """SELECT count(*) FROM monday_list WHERE age_days <= 365""", 'requests', f'open on {ASOF}',
        "Monday-list requests filed in the last 365 days.", f"{SRC_311}. As n1_open_past_promise, restricted to the last year's filings.")
    # closure mix 2025-26
    fig('n1_closed_2025_26', """SELECT count(*) FROM requests WHERE status_group = 'closed' AND init_year >= 2025""",
        'requests', f'filed 1 Jan 2025 to {ASOF}', 'Closed requests (STATUS CLOSED with a close time), one per request id.',
        f"{SRC_311}.")
    fig('n1_closed_handoff_share_2025_26', """SELECT avg(CAST(closure_class IN ('handed_off', 'converted') AS INT)) FROM v_requests
        WHERE status_group = 'closed' AND init_year >= 2025""", 'share', f'filed 1 Jan 2025 to {ASOF}',
        "Share of closures whose public words record a hand-off (scheduled, referred, added to rotation, tagged, sent elsewhere) or a work order, rather than finished work.",
        f"{SRC_311}, each closure's PUBLICRESOLUTION text looked up in N2's reviewed class table (research/chapters/N2-closure-classes.csv). Cross-check of N2's headline from the pipeline.")
    fig('n1_closed_done_share_2025_26', """SELECT avg(CAST(closure_class = 'done' AS INT)) FROM v_requests
        WHERE status_group = 'closed' AND init_year >= 2025""", 'share', f'filed 1 Jan 2025 to {ASOF}',
        "Share of closures whose words record finished work (N2 class 'done').", f"{SRC_311}, classed with N2's reviewed table.")
    fig('n1_done_by_promise_due_2025_26', """SELECT avg(CAST(coalesce(done_by_promise, false) AS INT)) FROM promise
        WHERE init_year >= 2025 AND promise_due""", 'share', f'filed 1 Jan 2025 to {ASOF}, promised date passed',
        "Of requests whose promised date has passed, the share closed with words recording finished work on or before that date; open and cancelled count as not done.",
        f"{SRC_311}: PRJCOMPLETEDATE compared with DATETIMECLOSED, closure words classed with N2's table.")
    fig('n1_closed_by_promise_due_2025_26', """SELECT avg(CAST(coalesce(closed_by_promise, false) AS INT)) FROM promise
        WHERE init_year >= 2025 AND promise_due""", 'share', f'filed 1 Jan 2025 to {ASOF}, promised date passed',
        "Of requests whose promised date has passed, the share closed (any words) on or before it.", f"{SRC_311}.")
    # re-filed
    fig('n1_came_back_30_2025_26', """SELECT avg(CAST(came_back_30 AS INT)) FROM refiled WHERE init_year >= 2025 AND window30_complete""",
        'share', f'closed requests filed 1 Jan 2025 to {ASOF}, 30-day window complete',
        "Share of closed requests followed by another request for the same problem code at the same normalised address within 30 days of closure (all types; recurrence, not proof of a false closure).",
        f"{SRC_311}, matched to itself by normalised address and problem code (scripts/night/N1/normalise.py).",
        note='Research phase quoted 6.3% of 190,856 file rows; per request id and with complete windows the share is higher because the denominator shrinks.')
    fig('n1_came_back_30_count_2025_26', """SELECT count(*) FILTER (WHERE came_back_30), count(*) FROM refiled WHERE init_year >= 2025""",
        'requests', f'closed requests filed 1 Jan 2025 to {ASOF}', 'Closed requests that came back within 30 days, and all closed requests with an address.',
        f"{SRC_311}, self-joined by normalised address and code.", pick=lambda r: {'came_back': r[0], 'closed_with_address': r[1]})
    fig('n1_refiled_14_durable_2025_26', """SELECT avg(CAST(refiled_14 AS INT)) FROM refiled WHERE init_year >= 2025 AND durable AND window14_complete""",
        'share', f'closed requests filed 1 Jan 2025 to {ASOF}, 14-day window complete',
        "Durable fixes only (potholes, cave-ins, street lights, city trees, signs): share re-filed for the same problem at the same address within 14 days of closure, the 'closure did not hold' measure.",
        f"{SRC_311}, self-joined by normalised address and code; durable types listed in measures.sql (type_family).")
    for code, key in [('Potholes - Major St', 'pothole_major'), ('Cave-Ins', 'cave_in'), ('Single Light Out', 'single_light')]:
        fig(f'n1_refiled_14_{key}', f"""SELECT avg(CAST(refiled_14 AS INT)), count(*) FROM refiled
            WHERE init_year >= 2025 AND problem_code = '{code}' AND window14_complete""", 'share',
            f'closed requests filed 1 Jan 2025 to {ASOF}', f"{code}: re-filed at the same address within 14 days of closure.",
            f"{SRC_311}, self-joined by normalised address and code.", pick=lambda r: r[0], note='')
    # weeds and the ledger
    fig('n1_weed_parcel_match_lot', """SELECT count(rp.request_id) / count(*) FROM requests r LEFT JOIN request_parcel rp USING (request_id)
        WHERE r.problem_code = 'Weeds-Vacant Lot' AND r.init_year >= 2025""", 'share', f'filed 1 Jan 2025 to {ASOF}',
        "Weeds-Vacant Lot requests matched to a parcel id (the knock-out test: at least 80%).",
        f"{SRC_311} matched to parcels through {SRC_MSD}, the LRA inventory and Forestry's maintenance list, by normalised address (exact, number range, or street type ignored when unique).")
    fig('n1_weed_parcel_match_bldg', """SELECT count(rp.request_id) / count(*) FROM requests r LEFT JOIN request_parcel rp USING (request_id)
        WHERE r.problem_code = 'Weeds-Vacant Bldg' AND r.init_year >= 2025""", 'share', f'filed 1 Jan 2025 to {ASOF}',
        "Weeds-Vacant Bldg requests matched to a parcel id.", f"As n1_weed_parcel_match_lot.")
    for code, key in [('Weeds-Vacant Lot', 'lot'), ('Weeds-Vacant Bldg', 'bldg')]:
        fig(f'n1_weeds_{key}_onschedule_ledger', f"""SELECT count(*),
               avg(CAST(coalesce(f.first_cut_after <= f.init_date + 30, false) AS INT)),
               avg(CAST(f.cut_by_season_end AS INT)), avg(CAST(f.no_cut_in_season AS INT))
            FROM request_ledger_flags f JOIN requests r USING (request_id)
            WHERE r.problem_code = '{code}' AND r.init_year = 2026 AND r.status_group = 'closed'
              AND r.ts_init <= TIMESTAMP '2026-09-15' AND (r.res_key LIKE '%schedule%' OR r.res_key LIKE '%rotation%')""",
            'shares', 'filed 1 Jan to 15 Sep 2026; ledger to ' + META['ledger_max_date'],
            f"{code} requests filed 1 Jan to 15 Sep 2026 and closed 'on schedule to be cut' OR 'added to rotation' (the two closing texts pooled), parcel matched: share with a cut recorded on the parcel within 30 days of filing; by the end of the data in 2026; and with no cut on the parcel at all in 2026. For 'on schedule to be cut' alone see n1_weeds_{key}_onschedule_only_no_cut_2026.",
            f"{SRC_311} joined to {SRC_LEDGER} by parcel id through {SRC_MSD}. A cut is a distinct parcel, date and service type (the ledger repeats rows). Ledger dates are posted in weekly batches, so the 30-day window is good to about a week.",
            pick=lambda r: {'n': r[0], 'cut_within_30_days': r[1], 'cut_by_season_end': r[2], 'no_cut_in_2026': r[3]},
            note="Pools 'on schedule to be cut' and 'added to rotation'. Do not describe this share as 'closed on schedule' alone (N8 finding 2).")
        fig(f'n1_weeds_{key}_onschedule_only_no_cut_2026', f"""SELECT avg(CAST(f.no_cut_in_season AS INT)), count(*),
               count(*) FILTER (WHERE f.no_cut_in_season),
               avg(CAST(coalesce(f.first_cut_after <= f.init_date + 30, false) AS INT)),
               avg(CAST(f.cut_by_season_end AS INT))
            FROM request_ledger_flags f JOIN requests r USING (request_id)
            WHERE r.problem_code = '{code}' AND r.init_year = 2026 AND r.status_group = 'closed'
              AND r.ts_init <= TIMESTAMP '2026-09-15' AND r.res_key LIKE 'on schedule to be cut%'""",
            'share', 'filed 1 Jan to 15 Sep 2026; ledger to ' + META['ledger_max_date'],
            f"{code} requests filed 1 Jan to 15 Sep 2026, closed with the words 'on schedule to be cut' (only; 'added to rotation' excluded), parcel matched: share with no grass cut billed on the parcel at any time in 2026.",
            f"{SRC_311} joined to {SRC_LEDGER} by parcel id through {SRC_MSD}; a cut is a distinct parcel, date and service type. The ledger is a billing record posted in weekly batches, so no charge is not proof of no cut. Corrects the earlier pooled figure, which also counted 'added to rotation' closures (N8 finding 2).",
            pick=lambda r: r[0])
        FIGS[-1]['n'] = None
        try:
            rr = con.execute(FIGS[-1]['_sql'] if '_sql' in FIGS[-1] else f"""SELECT count(*), count(*) FILTER (WHERE f.no_cut_in_season),
                   avg(CAST(coalesce(f.first_cut_after <= f.init_date + 30, false) AS INT)), avg(CAST(f.cut_by_season_end AS INT))
                FROM request_ledger_flags f JOIN requests r USING (request_id)
                WHERE r.problem_code = '{code}' AND r.init_year = 2026 AND r.status_group = 'closed'
                  AND r.ts_init <= TIMESTAMP '2026-09-15' AND r.res_key LIKE 'on schedule to be cut%'""").fetchone()
            FIGS[-1].update({'n': rr[0], 'n_no_cut_in_2026': rr[1], 'cut_within_30_days': round(rr[2], 4),
                             'cut_by_season_end': round(rr[3], 4)})
            FIGS[-1]['note'] = (f"{rr[1]:,} of {rr[0]:,} requests. Same requests: cut within 30 days {rr[2]:.1%}, any cut later in 2026 {rr[3]:.1%}. "
                                "Value is a 0-1 share.")
        except Exception as e:
            FIGS[-1]['note'] = f'ERROR {e}'
    fig('n1_weeds_cut_by_promise', "SELECT 0", 'share', f"filed 1 Jan to {ASOF} 2026, promised date on or before {META['ledger_max_date']}",
        "Weeds-Vacant Lot and Weeds-Vacant Bldg requests filed in 2026 and matched to a parcel: share with a grass cut recorded on the parcel between filing and the city's own promised date (14 days for lots, 90 for buildings).",
        f"{SRC_311} joined to {SRC_LEDGER} by parcel id through {SRC_MSD}; promised date = PRJCOMPLETEDATE. Ledger posting dates are batched weekly. 2026 only, because the 2025 ledger is thin (13,168 cut rows vs 46,346 in 2026).",
        pick=lambda r: None)
    vals = con.execute("""SELECT problem_code, count(*), avg(CAST(cut_by_promise AS INT)),
            avg(CAST(status_group = 'closed' AND closure_class IN ('handed_off', 'converted') AS INT)) FROM weed_promise_ledger
        WHERE promise_due_in_ledger AND init_year = 2026 AND problem_code IN ('Weeds-Vacant Lot', 'Weeds-Vacant Bldg')
        GROUP BY 1""").fetchall()
    FIGS[-1]['value'] = {code: {'n': n, 'cut_by_promise': round(v, 4), 'closed_as_handoff': round(h, 4)} for code, n, v, h in vals}
    fig('n1_ledger_coverage_by_year', """SELECT list({'year': y, 'cuts_distinct_parcel_days': n, 'ledger_rows': rws, 'parcels': p} ORDER BY y) FROM (
            SELECT year(service_date) AS y, count(*) AS n, sum(ledger_rows) AS rws, count(DISTINCT parcel) AS p FROM cuts
            WHERE service_date >= DATE '2019-01-01' GROUP BY 1)""", 'cuts / rows / parcels', '2019-2026',
        "Grass cuts ('Grass Maint' + 'Weed-Grass') per year in the forestry ledger: distinct parcel, date and service type; the raw ledger rows behind them; and the parcels covered.",
        f"{SRC_LEDGER}. The ledger repeats rows (most pre-2021 legacy rows appear twice), so cuts are counted as distinct parcel, date and type. 2025 is about a third of a normal year; whether cuts went unrecorded or unbilled after the 16 May tornado is not known from the file.",
        label='observed', note='Negative result: do not use 2025 ledger figures as evidence of no cut. Use cuts_distinct_parcel_days, not ledger_rows, for any count of cuts (N8 finding 10).')
    fig('n1_ledger_2026', """SELECT (SELECT count(*) FROM ledger WHERE service_type = 'Grass Maint' AND year(service_date) = 2026),
               count(*), count(DISTINCT parcel), count(DISTINCT parcel) FILTER (WHERE parcel IN (SELECT parcel_id FROM lra))
        FROM cuts WHERE service_type = 'Grass Maint' AND year(service_date) = 2026""", 'rows / cuts / parcels', f"2026 to {META['ledger_max_date']}",
        "Grass Maint in the forestry ledger in 2026: raw ledger rows; distinct cuts (parcel and date); the parcels they cover; and how many of those are LRA (city land bank) parcels.",
        f"{SRC_LEDGER}, parcel ids looked up in the LRA inventory (LRA_INVENTORY.csv). The ledger repeats rows, so 'charges' or 'cuts' must be the distinct count, not the row count.",
        pick=lambda r: {'ledger_rows': r[0], 'cuts_distinct_parcel_days': r[1], 'parcels': r[2], 'lra_parcels': r[3]},
        note="Say 'about 31,500 grass cuts billed on 11,971 parcels', not '37,543 cuts' (37,543 is ledger rows; N8 finding 10).")
    fig('n1_mowing_gaps', """SELECT count(*), median(longest_gap_between_cuts), count(*) FILTER (WHERE longest_gap_incl_open > 42),
               count(*) FILTER (WHERE longest_gap_incl_open > 90), count(*) FILTER (WHERE cuts_2026 = 1),
               count(*) FILTER (WHERE longest_gap_incl_open > 90 AND is_lra),
               count(*) FILTER (WHERE longest_gap_between_cuts > 90)
        FROM mowing_gaps""", 'parcels / days', '1 Apr to 30 Sep 2026',
        "Parcels on the 2026 mowing rotation (at least one Grass Maint cut 1 Apr-30 Sep); median longest gap between consecutive billed cuts; parcels that went more than 42 and more than 90 days without a billed cut (counting the run from the last cut to 30 Sep, so lots cut once count too); parcels cut once; LRA parcels over 90 days; and parcels with more than 90 days strictly between two cuts.",
        f"{SRC_LEDGER}, parcel ids looked up in the LRA inventory; a cut is a distinct parcel and date. Posting dates are batched weekly, so gaps are good to about a week.",
        pick=lambda r: {'rotation_parcels': r[0], 'median_longest_gap_between_cuts_days': r[1], 'gap_over_42_days': r[2],
                        'gap_over_90_days_counting_to_30_sep': r[3], 'cut_once': r[4], 'lra_gap_over_90_days': r[5],
                        'gap_over_90_days_strictly_between_cuts': r[6]},
        note="Say 'went more than 90 days without a billed cut (counting to 30 September)' (N8 finding 15d). The city's rotation runs about eight weeks between cuts, so BUILD-SPEC's 42-day threshold flags almost every lot.")
    # trees
    fig('n1_tree_cancel_2025_26', """SELECT count(*) FILTER (WHERE status_group = 'cancelled'),
        count(*) FILTER (WHERE status_group = 'cancelled' AND resolution IS NULL) FROM requests
        WHERE problem_code = 'Inspect City Tree' AND init_year >= 2025""", 'requests', f'filed 1 Jan 2025 to {ASOF}',
        "Inspect City Tree requests cancelled, and cancelled with no public words.", f"{SRC_311}.",
        pick=lambda r: {'cancelled': r[0], 'cancelled_no_words': r[1]})
    fig('n1_tree_cancel_wo_address', """WITH w AS (SELECT DISTINCT a.addr_norm FROM wo_tree w JOIN addr_lookup a ON a.addr_raw = w.address
            WHERE w.source IN ('tree_removal', 'tree_trim') AND a.addr_norm <> '')
        SELECT avg(CAST(addr_norm IN (SELECT addr_norm FROM w) AS INT)) FILTER (WHERE problem_code = 'Inspect City Tree' AND status_group = 'cancelled'),
               avg(CAST(addr_norm IN (SELECT addr_norm FROM w) AS INT)) FILTER (WHERE problem_code IN ('Potholes - Residnl', 'Refuse not collected', 'Containr damaged'))
        FROM requests WHERE init_year >= 2025""", 'shares', f'filed 1 Jan 2025 to {ASOF}',
        "Share of cancelled Inspect City Tree requests whose address appears in the tree removal or trim work-order sample, vs the same share for unrelated requests (residential potholes, refuse, damaged containers).",
        f"{SRC_311} matched by normalised address to {SRC_CW}. Samples cover 1,500 of 2,522 removals and 1,500 of 6,276 trims, so both shares are lower bounds.",
        pick=lambda r: {'cancelled_tree_requests': r[0], 'baseline_unrelated_requests': r[1]},
        note='Say "appear in Forestry\'s work orders about five times as often as unrelated requests", not "were converted".')
    fig('n1_tree_blank_cancel_order_already_open', """SELECT count(*) FILTER (WHERE s.n_removal_open_before_request > 0),
               median(s.days_recent_removal_order_before_request) FILTER (WHERE s.n_removal_open_before_request > 0),
               count(*) FILTER (WHERE s.n_removal_open_before_request_30m > 0),
               count(*)
        FROM requests r LEFT JOIN request_wo_summary s USING (request_id)
        WHERE r.problem_code = 'Inspect City Tree' AND r.status_group = 'cancelled' AND r.resolution IS NULL AND r.init_year >= 2025""",
        'requests / days', f'filed 1 Jan 2025 to {ASOF}',
        "Inspect City Tree requests cancelled with no words, filed more than a day after a Forestry removal order at the same normalised address had started (the order still open in the city's sample); median days the most recent such order had been open; for comparison, the count when any removal order within 30 m is allowed; and all blank-cancelled requests.",
        f"{SRC_311} matched by identical normalised address to {SRC_CW} (removal orders, saved search 6955); Cityworks dates converted from UTC to Central. Lower bounds: the sample holds 1,500 of 2,522 open removal orders.",
        pick=lambda r: {'same_address_order_already_open': r[0], 'median_days_order_open': r[1],
                        'within_30m_order_already_open': r[2], 'blank_cancelled': r[3]},
        note="Public text: use the same-address count (N8 conflict 3); within 30 m reaches neighbouring trees. N5 registers 288 / 575 days (n5_tree_cancel_blank_wo_predates, n5_tree_predating_wo_median_age_days) for the same rule; N1's view gives one more request. Framing (COMMON 9): residents report a tree the city already knows must come down; the request is cancelled with no words; the order stays open.")
    fig('n1_lra_onschedule_no_cut', """SELECT count(*), count(DISTINCT parcel), count(*) FILTER (WHERE no_cut_after_filing),
               count(DISTINCT parcel) FILTER (WHERE no_cut_after_filing) FROM lra_onschedule_no_cut""",
        'requests / lots', f"filed 2026; ledger to {META['ledger_max_date']}",
        "Weeds-Vacant Lot requests filed in 2026 on land-bank (LRA) lots, resident-filed, closed within three days as 'on schedule to be cut' or 'added to rotation': requests and lots; and those with no grass cut billed on the lot at any time after filing.",
        f"{SRC_311} joined by parcel id (through {SRC_MSD}, the LRA inventory and Forestry's maintenance list) to {SRC_LEDGER}; LRA ownership from LRA_INVENTORY.csv. N5's rule (COMMON 9). Ledger dates posted in weekly batches; no charge is not proof of no cut.",
        pick=lambda r: {'requests': r[0], 'lots': r[1], 'no_cut_requests': r[2], 'no_cut_lots': r[3]},
        note="Public text uses N5's registered 94 requests on 75 lots (n5_funnel_no_cut_requests, n5_funnel_no_cut_lots; N8 conflict 2). N1's wider parcel join (90% vs N5's 83% of 2026 lot requests matched) finds a few more. Requests filed after mid-September have had little time.")
    # like for like
    for code, words, key in [('Single Light Out', 'work completed', 'light_done'), ('Vehicle Towing', 'vehicle tagged for tow', 'tow_tagged'),
                             ('Cave-Ins', 'work completed', 'cave_done'), ('Whole Blk Lights Out', None, 'wholeblock'),
                             ('Inspect City Tree', 'removal work order created', 'tree_wo')]:
        extra = f"AND res_key = '{words}'" if words else ''
        fig(f'n1_lfl_{key}', f"""SELECT median(days_to_close) FILTER (WHERE ward_group = '1-5'), count(*) FILTER (WHERE ward_group = '1-5'),
                   median(days_to_close) FILTER (WHERE ward_group = '10-14'), count(*) FILTER (WHERE ward_group = '10-14')
            FROM requests WHERE problem_code = '{code}' AND channel_group = 'resident' AND ts_init >= TIMESTAMP '2025-05-16'
              AND status_group = 'closed' {extra}""", 'median days', f'filed 16 May 2025 to {ASOF}, resident channels',
            f"{code}{' closed with the words ' + chr(8220) + words + chr(8221) if words else ' closed'}: median days from filing to closure in wards 1-5 vs wards 10-14.",
            f"{SRC_311}. Same request type and same closure words in both ward groups, so the comparison is like for like; wards from the file's WARD field.",
            pick=lambda r: {'wards_1_5_median_days': r[0], 'wards_1_5_n': r[1], 'wards_10_14_median_days': r[2], 'wards_10_14_n': r[3]})
    fig('n1_dumping_repeat_blocks', """SELECT count(*) FILTER (WHERE n_requests >= 3), count(*) FILTER (WHERE n_requests >= 10), sum(n_requests) FROM dumping_blocks""",
        'blocks', f'filed in the 365 days to {ASOF}', "Blocks with 3 or more, and 10 or more, illegal-dumping or alley/street-debris requests in a year; and all such requests.",
        f"{SRC_311}, addresses rounded down to the hundred block.",
        pick=lambda r: {'blocks_3plus': r[0], 'blocks_10plus': r[1], 'requests': r[2]})
    fig('n1_duplicate_rows', """SELECT sum(source_rows), count(*), count(*) FILTER (WHERE source_rows > 1) FROM requests""", 'rows / ids',
        '2008 to ' + ASOF, "Rows in the city's 311 CSVs, distinct request ids, and ids that appear on more than one row.",
        "Counted in the city's csb.zip yearly CSVs; repeated rows differ only in caller type (and, for 148 ids, the resolution text), so we keep one row per request.",
        pick=lambda r: {'rows': r[0], 'request_ids': r[1], 'ids_repeated': r[2]})
    fig('n1_build_seconds', "SELECT 0", 'seconds', ASOF, 'Wall time of run_all.sh on a 2024-era laptop.',
        'Measured by run_all.sh; see build/N1/manifest.json.', pick=lambda r: None, note='filled by run_all.sh')
    try:
        man = json.load(open(os.path.join(ROOT, 'build', 'N1', 'manifest.json')))
        FIGS[-1]['value'] = man.get('seconds')
        FIGS[-1]['note'] = 'build_db.py seconds; export adds a few more'
    except Exception:
        pass

    merged, seen, sources, retired = [], set(), {}, []
    for f in FIGS:
        merged.append(f)
        seen.add(f['id'])
    for path in sorted(glob.glob(os.path.join(ROOT, 'build', 'N*', 'figures.json'))):
        owner = os.path.basename(os.path.dirname(path))
        if owner == 'N1':
            continue
        try:
            data = json.load(open(path))
        except Exception as e:
            sources[owner] = f'unreadable: {e}'
            continue
        items = data if isinstance(data, list) else data.get('figures', [])
        k = 0
        for f in items:
            if not isinstance(f, dict) or 'id' not in f:
                continue
            f = dict(f)
            f.setdefault('owner', owner)
            if f.get('retired'):  # retired figures never reach the registry the site reads (N8 re-check R6)
                retired.append(f)
                continue
            if f['id'] in seen:
                f['id'] = f"{owner.lower()}_{f['id']}"
            if 'derivation' not in f:
                f['derivation_missing'] = True
            seen.add(f['id'])
            merged.append(f)
            k += 1
        sources[owner] = k
    dump('figures.json', {'run': RUN, 'merged_from': {'N1': len(FIGS), **sources},
                          'figures': {f['id']: f for f in merged if not f.get('retired')}}, contract='figures',
         sources=tuple(f'build/{o}/figures.json' for o in sources))
    # the record of retired figures, kept out of figures.json; N6's bridge adds its own retired figures here too
    with open(os.path.join(OUT, 'retired_figures.json'), 'w') as fh:
        json.dump({'about': "Figures retired from public use: kept for the record, never read by the site. Each carries "
                            "'retired': true and a note saying why and what replaces it. Written by scripts/night/N1/export.py "
                            "from every build/N*/figures.json; N6's bridge adds its own retired figures.",
                   'run': RUN, 'figures': {f['id']: clean(f) for f in retired}}, fh, indent=1, default=str)
    with open(os.path.join(ROOT, 'build', 'N1', 'figures.json'), 'w') as fh:
        json.dump(clean(FIGS), fh, indent=1, default=str)


def main():
    scoreboard()
    ward_lfl()
    register()
    monday()
    dumping()
    receipts()
    by_ward()
    dump('meta.json', RUN)
    dump('run.json', {'asof': META['asof_ts'][:16], 'ledger_max_date': META['ledger_max_date'], 'built_at': META['built_at'],
                      'closure_class_source': META['closure_class_source']}, contract='run')
    wards = os.path.join(ROOT, 'data', 'raw', 'city-services', 'arcgis', 'layers', 'maps8_BOUNDARIES_Wards.geojson')
    shutil.copyfile(wards, os.path.join(OUT, 'wards.geojson'))
    figures()


if __name__ == '__main__':
    main()
