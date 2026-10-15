"""CityStat published values, transcribed from data/raw/citystat/tableau-extract.md
(Tableau getSummaryDataAsync, extracted 13 Oct 2026). Quarters 2024 Q1 .. 2026 Q2.
Each metric: problem codes in the 311 file, CityStat goal, unit of goal, published share and n.
"""
QS = [f'{y} Q{q}' for y in (2024, 2025) for q in (1, 2, 3, 4)] + ['2026 Q1', '2026 Q2']

METRICS = {
    'pothole_major': dict(page='/street/streets.cfm', label='Potholes, major streets, repaired within 3 days',
        codes=['Potholes - Major St'], goal_days=3,
        n=[543, 529, 838, 311, 921, 648, 329, 270, 703, 443],
        share=[.1731, .0624, .1396, .0129, .0923, .3056, .3647, .2593, .1849, .4447]),
    'pothole_residential': dict(page='/street/streets.cfm', label='Potholes, residential streets, repaired within 8 days',
        codes=['Potholes - Residnl'], goal_days=8,
        n=[920, 1025, 2575, 346, 711, 948, 437, 399, 969, 916],
        share=[.4109, .1405, .2637, .0173, .2236, .7162, .5126, .4261, .4386, .9061]),
    'pothole_alley': dict(page='/street/streets.cfm', label='Potholes, alleys, repaired within 17 days',
        codes=['Potholes - Alley'], goal_days=17,
        n=[78, 151, 145, 70, 147, 188, 99, 77, 126, 113],
        share=[.4872, .1788, .0966, .0286, .3878, .8777, .5859, .6104, .7063, .9823]),
    'debris_alley_street': dict(page='/street/streets.cfm', label='Debris, alley/street, cleaned within 3 days',
        codes=['Debris-alley/street'], goal_days=3,
        n=[825, 687, 1081, 609, 584, 1216, 1407, 441, 470, 546],
        share=[.5297, .4134, .4875, .3941, .1096, .7031, .5622, .5283, .7617, .7857]),
    'debris_vacant_bldg': dict(page='/street/streets.cfm', label='Debris, vacant building, cleaned within 14 days',
        codes=['Debris-Vacant Bldg'], goal_days=14,
        n=[109, 108, 104, 67, 92, 86, 93, 78, 77, 67],
        share=[.5963, .5463, .7115, .3881, .3261, .8140, .9247, .8974, .8831, .9552]),
    'debris_vacant_lot': dict(page='/street/streets.cfm', label='Debris, vacant lot, cleaned within 14 days',
        codes=['Debris-Vacant Lot'], goal_days=14,
        n=[156, 136, 128, 89, 118, 142, 161, 95, 114, 113],
        share=[.4295, .4926, .7109, .4045, .2288, .7535, .8261, .7474, .9211, .9735]),
    'whole_block_lights': dict(page='/street/traffic.cfm', label='Whole block lights out, completed within 24 hours',
        codes=['Whole Blk Lights Out'], goal_days=1,
        n=[349, 299, 413, 490, 640, 601, 482, 597, 420, 358],
        share=[.7350, .7833, .7947, .7592, .5281, .5574, .6639, .7379, .7833, .8017]),
    'critical_sign': dict(page='/street/traffic.cfm', label='Critical signs (Stop/Yield/One-Way/Do Not Enter), within 48 hours',
        codes=['Critical Sign'], goal_days=2,
        n=[181, 166, 124, 116, 210, 167, 152, 119, 95, 112],
        n_total=[212, 171, 132, 123, 225, 169, 177, 145, 104, 118],
        within=[57, 63, 18, 20, 96, 68, 73, 67, 66, 66],
        avg_days=[6.55, 5.83, 13.32, 9.32, 5.34, 6.93, 5.52, 3.47, 2.56, 5.40],
        share=[.3149, .3795, .1452, .1724, .4571, .4072, .4803, .5630, .6947, .5893]),
    'parks_all': dict(page='/parks/parks-division.cfm', label='All parks requests completed on time (per-type goal 5-30 days)',
        codes=['Dead Limbs in Park', 'Graffiti-Park Equip', 'Athletic Fields', 'Playground Equipment',
               'Trash in the Park', 'High Grass in Park', 'Misc-Parks Div', 'Park Restrooms',
               'Rec Bldg Maintenance', 'Park Sewer Problem', 'Cut Median-Pkwy', 'Park Lake',
               'Ballfield Benches', 'Fountains', 'Rec-Athletic Lights', 'Leaves in Park',
               'Maintain Bike Trail'],
        goal_days=None,  # per-type goal not published; PRJCOMPLETEDATE used as the per-request goal
        n=[92, 297, 298, 153, 242, 383, 352, 198, 166, 378],
        share=[.3804, .2256, .3188, .3268, .2107, .2298, .2670, .5101, .4398, .6746]),
}

ROUTING = dict(page='/public-safety/csb.cfm', label='CSB requests routed within 2.5 days (goal 95%)',
    n=[10664, 13110, 12469, 8262, 12967, 14884, 15678, 9304, 10643, 10853],
    share=[.9646, .9853, .9785, .9932, .9737, .9464, .9351, .9627, .9387, .9999])

PARKS = dict(page='/parks/parks-division.cfm', label='All parks requests on time (goal 80%)',
    n=[92, 297, 298, 153, 242, 383, 352, 198, 166, 378],
    share=[.3804, .2256, .3188, .3268, .2107, .2298, .2670, .5101, .4398, .6746])

TOWING = dict(page='/street/towing.cfm', label='CSB tow-related requests by quarter and status',
    closed=[1318, 1358, 1431, 1231, 1533, 1782, 2208, 1703, 1776, 1075],
    open=[0, 0, 0, 0, 0, 0, 16, 25, 105, 562])

WARD_MAP = {  # 2024-01-01 to 2026-06-30: avg days to close, requests, closed
    '01': (17.18, 23417, 19603), '02': (19.44, 21712, 17364), '03': (22.77, 19074, 16543),
    '04': (19.69, 21251, 17484), '05': (19.91, 19340, 15363), '06': (27.76, 18280, 14384),
    '07': (27.44, 22822, 18786), '08': (27.89, 20313, 16551), '09': (32.59, 12206, 9966),
    '10': (35.07, 19467, 15218), '11': (30.67, 16361, 13816), '12': (30.33, 25722, 21626),
    '13': (24.32, 28423, 24319), '14': (27.54, 17034, 14600), None: (13.82, 726, 532)}

SNOW = [('2024-12-29', 1, 1.80), ('2025-01-05', 639, 14.19), ('2025-01-12', 1709, 17.41),
        ('2025-01-19', 386, 11.24), ('2025-01-26', 51, 2.09), ('2026-01-11', 8, 0.30),
        ('2026-01-18', 21, 2.24), ('2026-01-25', 1334, 3.07), ('2026-02-01', 100, 1.10),
        ('2026-02-08', 1, 0.01)]
