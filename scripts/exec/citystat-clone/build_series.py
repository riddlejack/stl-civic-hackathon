"""CityStat clone: the nine 311 measures CityStat publishes, by quarter, with two added series.

    .venv/bin/python -I scripts/exec/citystat-clone/build_series.py

Writes site/data/citystat_series.json. For each measure and quarter (2024 Q1 .. 2026 Q3):
  published  CityStat's on-time share as its chart shows it (reported; Tableau summary data extracted
             13 Oct 2026, data/raw/citystat/tableau-extract.md, transcribed in scripts/night/N4/citystat_targets.py).
             None for 2026 Q3: CityStat's pages say "last updated June 30th, 2026".
  rebuilt    the same measure from the city's open 311 file (observed; N4 chosen definition, as carried in
             site/data/scoreboard.json citystat.metrics[].series and q3_share).
  says_done  on time AND the closing words say the work was done (derived). Same query as
             scripts/night/R1/05_restate.py (ontime_done_only_share), grouped by quarter filed instead of pooled,
             run read-only against build/stl.duckdb. Closed requests only, calendar days, CityStat's goal;
             parks use each request's own due date. Checked against the registered Q2 2026 / Q3 2026 values in
             build/R1/restated_citystat.csv before writing. Not graded against each request's promise date, and not
             a record of the work itself (research/closure-class-review.md).
Nothing in build/ or other site/ files is changed.
"""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts' / 'night' / 'N4'))
from citystat_targets import METRICS, QS  # noqa: E402  (read-only import of the transcribed CityStat values)

DB = ROOT / 'build' / 'stl.duckdb'
OUT = ROOT / 'site' / 'data' / 'citystat_series.json'
R1 = ROOT / 'build' / 'R1' / 'restated_citystat.csv'
SCORE = ROOT / 'site' / 'data' / 'scoreboard.json'
QUARTERS = QS + ['2026 Q3']

# How CityStat groups and titles them (page, chart worksheet, on-time target), from tableau-extract.md.
DEPTS = [
    dict(id='streets', name='Street Division', page='https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/streets.cfm',
         path='/street/streets.cfm',
         charts=[dict(id='potholes', title='Pothole repair', worksheet='PotholeRepairOpetion1',
                      measures=['pothole_major', 'pothole_residential', 'pothole_alley']),
                 dict(id='debris', title='Debris removal', worksheet='DebrisRemovalv2',
                      measures=['debris_alley_street', 'debris_vacant_bldg', 'debris_vacant_lot'])]),
    dict(id='traffic', name='Traffic and Lighting', page='https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/traffic.cfm',
         path='/street/traffic.cfm',
         charts=[dict(id='lights', title='Whole block lights out', worksheet='WholeBlockLightsOut', measures=['whole_block_lights']),
                 dict(id='signs', title='Critical signs', worksheet='CriticalSign', measures=['critical_sign'])]),
    dict(id='parks', name='Parks Division', page='https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/parks/parks-division.cfm',
         path='/parks/parks-division.cfm',
         charts=[dict(id='parks', title='All parks requests', worksheet='Parks-On-TimePercentage', measures=['parks_all'])]),
]
TITLES = {  # CityStat's measure name, the time goal, the on-time target
    'pothole_major': ('Potholes, major streets', 'repaired within 3 days', 0.80),
    'pothole_residential': ('Potholes, residential streets', 'repaired within 8 days', 0.80),
    'pothole_alley': ('Potholes, alleys', 'repaired within 17 days', 0.80),
    'debris_alley_street': ('Debris, alley and street', 'cleaned up within 3 days', 0.80),
    'debris_vacant_bldg': ('Debris, vacant building', 'cleaned up within 14 days', 0.80),
    'debris_vacant_lot': ('Debris, vacant lot', 'cleaned up within 14 days', 0.80),
    'whole_block_lights': ('Whole block lights out', 'completed within 24 hours', 0.80),
    'critical_sign': ('Critical signs (Stop, Yield, One-Way, Do Not Enter)', 'completed within 48 hours', 0.75),
    'parks_all': ('All parks requests', 'completed on time (goal set per request type)', 0.80),
}


def says_done_by_quarter():
    import duckdb
    con = duckdb.connect()
    con.execute(f"ATTACH '{DB}' AS s (READ_ONLY)")
    out = {}
    for key, m in METRICS.items():
        if key == 'whole_block_lights':
            ontime = "epoch(r.ts_closed - r.ts_init) <= 86400"
        elif m['goal_days'] is None:
            ontime = ("date_diff('day', r.init_date, CAST(r.ts_closed AS DATE)) <= "
                      "date_diff('day', r.init_date, CAST(r.ts_promised AS DATE))")
        else:
            ontime = f"date_diff('day', r.init_date, CAST(r.ts_closed AS DATE)) <= {m['goal_days']}"
        codes = ','.join("'" + c + "'" for c in m['codes'])
        rows = con.execute(f"""
          WITH c AS (
            SELECT r.request_id, r.closure_class, ({ontime}) AS on_time,
                   (year(r.init_date) || ' Q' || quarter(r.init_date)) AS qf
            FROM s.v_requests r
            WHERE r.problem_code IN ({codes}) AND r.status_group = 'closed')
          SELECT qf, count(*) AS n_closed, avg(CAST(on_time AS INT)) AS ontime,
                 avg(CAST(on_time AND closure_class = 'done' AS INT)) AS says_done
          FROM c GROUP BY qf""").fetchall()
        out[key] = {qf: dict(n_closed=n, ontime_closed=round(o, 4), says_done=round(d, 4)) for qf, n, o, d in rows}
    return out


def main():
    sb = {m['metric']: m for m in json.loads(SCORE.read_text())['citystat']['metrics']}
    r1 = {}
    with open(R1, newline='') as f:
        for r in csv.DictReader(f):
            q = r['period'][:7]
            if r['period'].startswith(('2026 Q2', '2026 Q3')):
                r1[(r['metric'], q)] = float(r['ontime_share_counting_only_done'])
    try:
        done = says_done_by_quarter()
        done_note = 'by quarter, recomputed from build/stl.duckdb with the R1 query'
    except Exception as e:  # database missing or locked: fall back to the two registered quarters
        print(f'duckdb unavailable ({e}); says_done limited to 2026 Q2 and Q3')
        done = {m: {q: dict(says_done=round(v, 4)) for (mm, q), v in r1.items() if mm == m} for m in METRICS}
        done_note = 'only 2026 Q2 and 2026 Q3 (build/R1/restated_citystat.csv); duckdb was unavailable'

    # the check: our quarterly recompute must equal the registered R1 values
    for (m, q), v in r1.items():
        got = done[m].get(q, {}).get('says_done')
        assert got is not None and abs(got - v) < 5e-4, (m, q, got, v)

    measures = {}
    for key, m in METRICS.items():
        name, goal, target = TITLES[key]
        reb = {s['quarter']: s['ours_share'] for s in sb[key]['series']}
        series = []
        for q in QUARTERS:
            i = QS.index(q) if q in QS else None
            rb = reb.get(q)
            if q == '2026 Q3' and rb is None:
                rb = sb[key].get('q3_share')
            d = done[key].get(q, {})
            series.append(dict(quarter=q,
                               published=m['share'][i] if i is not None else None,
                               published_n=m['n'][i] if i is not None else None,
                               rebuilt=round(rb, 4) if rb is not None else None,
                               says_done=d.get('says_done'),
                               n_closed=d.get('n_closed')))
        measures[key] = dict(id=key, name=name, goal=goal, target=target, cityStat_label=m['label'],
                             mean_gap_pp=sb[key].get('mean_gap_pp'), series=series,
                             figures=dict(published=f'e3_citystat_{key}_q2_published', rebuilt=sb[key].get('q2_ours_figure'),
                                          says_done=f'e3_citystat_{key}_q2_done_on_time'))
    doc = dict(
        about=('CityStat\'s nine 311 on-time measures, by quarter filed, with the rebuilt value and the share whose closing '
               'words say the work was done. Built by scripts/exec/citystat-clone/build_series.py.'),
        quarters=QUARTERS,
        labels=dict(published='reported: CityStat chart data (Tableau summary data, extracted 13 Oct 2026; pages last updated 30 June 2026)',
                    rebuilt='observed: rebuilt from the city\'s open 311 file (file of 13 Oct 2026), N4 definition',
                    says_done=('derived: closed within CityStat\'s goal AND closing words say the work was done; closed requests only, '
                               'by quarter filed; ' + done_note)),
        sources=dict(citystat='https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/',
                     file_311='https://www.stlouis-mo.gov/data/upload/data-files/csb.zip',
                     closing_classes='data/downloads/closure_class.sql', measures_sql='data/downloads/measures.sql'),
        departments=DEPTS,
        measures=measures)
    OUT.write_text(json.dumps(doc, indent=1))
    print(f'wrote {OUT.relative_to(ROOT)}: {len(measures)} measures x {len(QUARTERS)} quarters')
    for k, m in measures.items():
        print(f"{k:20s}", ' '.join(f"{s['quarter'][-4:]}:{s['published'] or 0:.2f}/{s['rebuilt'] or 0:.2f}/{s['says_done'] if s['says_done'] is not None else '-'}" for s in m['series'][-3:]))


if __name__ == '__main__':
    main()
