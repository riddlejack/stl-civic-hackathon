"""N5 step 4: assemble the hero cases and the figures they rest on.

Writes
  build/N5/private/heroes_private.json  full detail (request ids, parcel ids, addresses), for Jack only
  build/N5/heroes.json                  public: block level only, no request/work-order/parcel ids
  build/N5/figures.json                 figure registry entries (with derivation)
Images are added by 05_imagery.py, which then re-runs the public export (06_publish.py).

Selection rules are stated in each section; the lot choices were made after 03_lot_validate.py and
are logged in build/N5/decisions.json.

Privacy (Jack's ruling 13 Oct ~11:55 p.m.): every public case is at block level, including the
city-owned (LRA) lots. No owner names, staff fields or requester identity are read anywhere.
"""
import duckdb, json, os, re, datetime as dt
from zoneinfo import ZoneInfo
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
RAW = os.path.join(ROOT, 'data/raw')
OUT = os.path.join(ROOT, 'build/N5')
PRIV = os.path.join(OUT, 'private')
# Parcel ids, handles and exact addresses of the hero lots live in a git-ignored file, so the code carries no real
# location (N8 re-check R3). Format: {"lots": {"lot-1": {"pid": ..., "related": [{pid, handle, address, label}]}, ...}}.
HERO_IDS = json.load(open(os.path.join(PRIV, 'hero_ids.json')))['lots']
con = duckdb.connect(os.path.join(PRIV, 'n5.duckdb'), read_only=True)
UTC, CT = ZoneInfo('UTC'), ZoneInfo('America/Chicago')
TORNADO = '2025-05-16'
G15 = ('01', '02', '03', '04', '05'); G1014 = ('10', '11', '12', '13', '14')
S = 'scripts/night/N5/04_heroes.py'
SRC = {
    'csb': '311 requests, city open data csb.zip (2025.csv, 2026.csv), https://www.stlouis-mo.gov/data/upload/data-files/csb.zip; local copy build/csb-clean/ with invalid UTF-8 bytes dropped',
    'ledger': 'Forestry service records (billing ledger), https://www.stlouis-mo.gov/data/upload/data-files/forestry-service-records.csv',
    'msd': 'MSD parcel attributes (PROP_ADD to PID), used only to join a 311 address to a parcel; owner field never read',
    'lra': 'LRA (land bank) inventory, https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_INVENTORY.csv',
    'lra_offers': 'LRA offers, https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_OFFERS.csv (no names in the file)',
    'fmp': 'Forestry maintenance property list (2023-05-26), https://www.stlouis-mo.gov/data/upload/data-files/forestry-maintenance-properties.csv',
    'wo_rm': 'Cityworks saved search 6955 (easement tree removals, status NEW), https://service.stlouis-mo.gov/cityworks/gis/1/6955/rest/services/cw/FeatureServer/2; 1,500 of 2,522 rows; retrieved 2026-10-14 00:19 UTC',
}
DER = {  # plain-language derivations, reused by events and figures
    'filed': "311 file: the request's DATETIMEINIT.",
    'closed': "311 file: the request's DATETIMECLOSED and its PUBLICRESOLUTION text.",
    'promise': "311 file: the request's PRJCOMPLETEDATE, the completion date the city sets on each request (a fixed offset per request type).",
    'invdone': "311 file: the request's DATEINVTDONE (investigation done).",
    'cancel': "311 file: STATUS CANCEL with DATECANCELLED; PUBLICRESOLUTION empty.",
    'cut': ("Forestry billing ledger: SERVICEDATE of a 'Grass Maint' or 'Weed-Grass' charge on the lot's parcel, joined from the 311 address "
            "to the parcel through MSD's parcel address file; ledger dates are posted in weekly batches, so read to the week."),
    'cut_year': "Forestry billing ledger: count of 'Grass Maint'/'Weed-Grass' charges on the lot's parcel in that year (same join as above).",
    'acq': "LRA inventory: ACQUISITION_DATE of the parcel (year shown publicly).",
    'offer': "LRA offers file: DECISION_DATE and the ACCEPTED/REJECTED flags for an offer on the parcel (no names in the file).",
    'ledger_end': "Forestry billing ledger: the latest SERVICEDATE in the file as downloaded on 13 Oct 2026.",
    'block': "Forestry billing ledger: charges in 2026 on other parcels with the same CITYBLOCK code as the lot.",
    'wo_start': ("Cityworks saved search 6955 (open tree-removal work orders): ProjStartDate, stored in UTC and converted to Central; "
                 "matched to the 311 request because the two addresses are identical after the project's address normaliser."),
    'wo_finish': "Cityworks saved search 6955: ProjFinishDate (UTC converted to Central).",
    'wo_status': "Cityworks saved search 6955 as read on 2026-10-14 00:19 UTC: Status field.",
    'later': "311 file: another request of the same type whose normalised address equals this one, filed after this request closed.",
}
figures = []
def fig(id, value, unit, period, definition, label, derivation, script=S, note=''):
    figures.append(dict(id=id, value=value, unit=unit, period=period, definition=definition, label=label,
                        derivation=derivation, source_sql_or_script=script, note=note))
def ev(date, event, source, der, label='observed', **kw):
    return dict(date=date, event=event, source=source, label=label, derivation=DER.get(der, der), **kw)

def d(x, fmt='%Y-%m-%d %H:%M'):
    return x.strftime(fmt) if x else None
def block_of(addr):
    a = (addr or '').upper().split(',')[0].strip()
    m = re.match(r'^(\d+)\s+(.+)$', a)
    if not m:
        return a  # intersection or no number: already coarser than a parcel
    return f"{int(m.group(1)) // 100 * 100} block of {' '.join(m.group(2).split())}"
def dur(a, b):
    m = (b - a).total_seconds() / 60
    if m < 90: return f'{m:.0f} minutes'
    if m < 36 * 60: return f'{m / 60:.0f} hours'
    return f'{m / 1440:.1f} days'
def days(a, b):
    return round((b - a).total_seconds() / 86400, 1)
def jsdate(s):  # 'Wed Aug 26 2015 19:00:00 GMT-0500 (...)' -> '2015-08-26'
    try:
        return dt.datetime.strptime(' '.join(s.split()[1:4]), '%b %d %Y').strftime('%Y-%m-%d')
    except Exception:
        return None

con.execute(f"""create temp view offers as select PARCEL pid, ACCEPTED, DECISION_DATE, REJECTED, DECLINE_BID
                from read_csv('{RAW}/stlouis-mo.gov/files/LRA_OFFERS.csv', all_varchar=true, header=true)""")
LEDGER_END = con.execute("select max(t_service) from ledger").fetchone()[0]

COMPLAINT = {'Unsatisfy Cut - VLot': "the lot's cut was left incomplete", 'Missed Cut - V Lot': 'the lot was missed on the ward cutting rotation',
             'Unsatisfy Cut -VBldg': "the cut at the vacant building was left incomplete", 'Missed Cut - VBldg': 'the vacant building was missed on the ward cutting rotation'}
PROM = dict(con.execute("""select round(date_diff('hour', t_init, t_promise) / 24.0)::int, count(*) from csbd
                           where PROBLEMCODE='Weeds-Vacant Lot' and year(t_init)=2026 and t_promise is not null group by 1""").fetchall())
PROM_N = sum(PROM.values())
fig('n5_weeds_lot_promise_days_2026', PROM.get(14, 0), 'requests', '2026 to 2026-10-13',
    f"2026 'Weeds-Vacant Lot' requests whose promise date is 14 days after filing (of {PROM_N:,} with a promise date)", 'observed',
    "311 file (csb.zip 2026, one row per request id): PRJCOMPLETEDATE minus DATETIMEINIT, rounded to whole days.",
    note=f"parts: 14 days {PROM.get(14, 0):,}; 90 days {PROM.get(90, 0):,}; other {PROM_N - PROM.get(14, 0) - PROM.get(90, 0):,}. Lot-1's two requests carry 90.")
# context for 'cut incomplete' calls (N8 finding 1), re-derived with this project's exact address join
con.execute("""create temp table ucut as select c.REQUESTID, c.resident, c.t_init, coalesce(a.pid, l.pid) pid
               from csbd c left join a2p a using (addr_n)
               left join (select lra_addr_n, min(pid) pid from lra group by 1) l on l.lra_addr_n = c.addr_n and a.pid is null
               where c.PROBLEMCODE = 'Unsatisfy Cut - VLot' and year(c.t_init) = 2026""")
con.execute("create temp table dcuts as select distinct pid, t_service from ledger where stype in ('Grass Maint','Weed-Grass')")
u_all, u_m, u_b30, u_a30, u_none = con.execute("""select (select count(*) from ucut), count(*),
    count(*) filter (where exists (select 1 from dcuts k where k.pid=u.pid and k.t_service <= u.t_init and k.t_service >= u.t_init - interval 30 day)),
    count(*) filter (where exists (select 1 from dcuts k where k.pid=u.pid and k.t_service > u.t_init and k.t_service <= u.t_init + interval 30 day)),
    count(*) filter (where not exists (select 1 from dcuts k where k.pid=u.pid and year(k.t_service)=2026))
    from ucut u where pid is not null""").fetchone()
UDER = ("311 'Unsatisfy Cut - VLot' calls ('Vacant lot cut incomplete') filed in 2026, all channels, one row per request id (csb.zip), joined to a parcel by "
        "exact normalised address through MSD's parcel address file, then to distinct cut dates in the Forestry billing ledger (weekly posting batches).")
figures.append(dict(id='n5_unsat_cut_calls_2026', value=u_m, unit='calls', period='2026 to 2026-10-13',
    definition="2026 'vacant lot cut incomplete' calls matched to a parcel", label='observed', derivation=UDER,
    parts={'calls_2026': u_all, 'parcel_matched': u_m, 'cut_billed_in_30_days_before': u_b30, 'cut_billed_in_30_days_after': u_a30,
           'no_cut_billed_in_2026': u_none},
    source_sql_or_script=S,
    note=(f"of {u_m} matched calls, {u_b30} came within 30 days after a billed cut and {u_none} were on lots with no cut billed all year, so a call "
          "does not show a cut happened. N8 reports 229 / 67 / 61 with a wider join that adds address-range matches; the gap is mostly in "
          "'no cut all year' (ours 40, N8 61).")))
for k, v, dfn in [('cut_30d_before', u_b30, 'of those, calls filed within 30 days after a cut was billed on the lot'),
                  ('no_cut_2026', u_none, 'of those, calls on lots with no cut billed at any time in 2026')]:
    fig(f'n5_unsat_cut_calls_2026_{k}', v, 'calls', '2026 to 2026-10-13', dfn, 'observed', UDER)

# =====================================================================================
# 1. THE LOT
# =====================================================================================
def lot_case(pid, cid, role, rank, story, related=()):
    lra = con.execute("select lra_address, Parcel_Status, Usage, ACQUISITION_DATE, lra_ward, NeighborhoodName, lra_addr_n from lra where pid=?", [pid]).fetchone()
    fmp = con.execute("select fmp_category, handle from fmp where pid=?", [pid]).fetchone()
    handle = fmp[1] if fmp else None
    cityblock = handle[1:7] if handle else None
    addr = ' '.join(lra[0].split())
    reqs = con.execute("""select REQUESTID, CALLERTYPE, PROBLEMCODE, STATUS, resolution, t_init, t_closed, t_promise, resident, type_name
                          from csbd where addr_n = ? and year(t_init) >= 2025 order by t_init""", [lra[6]]).fetchall()
    # one entry per distinct (SERVICEDATE, SERVICETYPE): the ledger repeats many rows (N8 finding 10)
    cuts = [r[0] for r in con.execute("select distinct t_service, stype from ledger where pid=? and stype in ('Grass Maint','Weed-Grass') order by 1", [pid]).fetchall()]
    hist = con.execute(f"""select year(try_cast(SERVICEDATE as timestamp)) y, count(distinct (SERVICEDATE, SERVICETYPE)) from read_csv('{RAW}/stlouis-mo.gov/files/forestry-service-records.csv', all_varchar=true, header=true)
                           where trim(PARCEL)=? and SERVICETYPE in ('Grass Maint','Weed-Grass') and SERVICEDATE >= '2019-01-01' and SERVICEDATE < '2025-01-01'
                           group by 1 order by 1""", [pid]).fetchall()
    blk = con.execute("""select count(distinct (pid, t_service, stype)), count(distinct pid), count(distinct pid) filter (where pid in (select pid from lra)), count(distinct t_service::date)
                         from ledger where cityblock=? and year(t_service)=2026 and stype in ('Grass Maint','Weed-Grass') and pid<>?""", [cityblock, pid]).fetchone()
    offs = con.execute("select ACCEPTED, DECISION_DATE, REJECTED, DECLINE_BID from offers where pid=? order by DECISION_DATE", [pid]).fetchall()
    tl = []
    acq = jsdate(lra[3] or '')
    if acq:
        tl.append(ev(acq, 'The land bank (LRA, city-owned) acquires the lot', 'lra', 'acq', public_date=acq[:4]))
    for y, n in hist:
        tl.append(ev(str(y), f'Forestry ledger bills grass cuts on the lot on {n} distinct date(s) in {y}', 'ledger', 'cut_year'))
    n25 = sum(1 for c in cuts if c.year == 2025)
    tl.append(ev('2025', f'Forestry ledger bills grass cuts on the lot on {n25} distinct date(s) in 2025 (the 2025 ledger is thin overall: about half the usual parcels)', 'ledger', 'cut_year'))
    cut26 = sorted(c for c in cuts if c.year == 2026)
    for r in reqs:
        if r[5].year < 2026 and r[2] != 'Weeds-Vacant Lot':
            continue
        if r[2] in COMPLAINT:  # explicit and neutral (N8 finding 1): say what was reported and what the ledger shows
            who = 'A resident' if r[8] else ('City staff (caller type NSO)' if r[1] == 'NSO' else 'A caller (channel not recorded)')
            before = [c for c in cut26 if r[5] - dt.timedelta(days=30) <= c <= r[5]]
            after = [c for c in cut26 if c > r[5]]
            if not cut26:
                ctx = 'No cut is billed on the lot in 2026, before or after.'
            else:
                ctx = (f"Ledger: {'a cut billed ' + format(before[-1], '%-d %b') + ' (within the 30 days before)' if before else 'no cut billed in the 30 days before'}; "
                       f"{'next cut billed ' + format(after[0], '%-d %b') if after else 'none billed after'}.")
            closed = f"311 closes it after {dur(r[5], r[6])}, \"{r[4] or '(no text)'}\"." if r[6] else f"Status {r[3]}."
            tl.append(ev(d(r[5]), f"{who} reports {COMPLAINT[r[2]]} (311 type \"{r[9]}\"); {closed} {ctx}", 'csb',
                         "311 file: the request's DATETIMEINIT, DATETIMECLOSED, PUBLICRESOLUTION and CALLERTYPE; ledger context from the Forestry billing "
                         "ledger (distinct cut dates on the lot's parcel, joined through MSD's parcel address file).", request_id=r[0]))
            continue
        tl.append(ev(d(r[5]), f'311 request filed ({r[1]}, "{r[2]}")', 'csb', 'filed', request_id=r[0]))
        if r[6]:
            tl.append(ev(d(r[6]), f"Closed after {dur(r[5], r[6])}: \"{r[4] or '(no text)'}\"", 'csb', 'closed', request_id=r[0]))
        elif r[3] == 'CANCEL':
            tl.append(ev(None, 'Cancelled', 'csb', 'cancel', request_id=r[0]))
        if r[7] and r[2] == 'Weeds-Vacant Lot':
            off = round(days(r[5], r[7]))
            note = (f" (a {off}-day promise; most 2026 vacant-lot weed requests carry 14 days: {PROM[14]:,} of {PROM_N:,})" if off != 14
                    else ' (the usual 14-day promise)')
            tl.append(ev(d(r[7], '%Y-%m-%d'), f"The city's own promise date for the request filed {r[5]:%-d %B}{note}", 'csb', 'promise', request_id=r[0]))
    for c in cut26:
        tl.append(ev(d(c, '%Y-%m-%d'), 'Forestry ledger bills a grass cut on the lot', 'ledger', 'cut'))
    for o in offs:
        tl.append(ev(jsdate(o[1] or ''), f"LRA offers file records a decision on an offer to buy the lot (ACCEPTED={o[0]}, REJECTED={o[2]})", 'lra_offers', 'offer'))
    tl.append(ev(d(LEDGER_END, '%Y-%m-%d'), f"Latest date in the ledger. Cuts billed on the lot in 2026: {sum(1 for c in cuts if c.year == 2026)}. "
                 f"Other parcels on its city block (same ledger CITYBLOCK) cut in 2026: {blk[1]} ({blk[2]} of them land-bank lots), on {blk[3]} different days", 'ledger', 'block'))
    for k, rel in enumerate(related):  # neighbouring land-bank lots that are part of the story (block level)
        rpid, rlabel = rel['pid'], rel['label']
        raddr_n = con.execute("select lra_addr_n from lra where pid=?", [rpid]).fetchone()[0]
        for q in con.execute("""select REQUESTID, CALLERTYPE, PROBLEMCODE, resolution, t_init, t_closed from csbd
                                where addr_n=? and year(t_init)=2026 and PROBLEMCODE='Weeds-Vacant Lot' order by t_init""", [raddr_n]).fetchall():
            tl.append(ev(d(q[4]), f"{rlabel}: 311 weed request filed ({q[1]}); closed after {dur(q[4], q[5])}: \"{q[3] or '(no text)'}\"",
                         'csb', 'filed', request_id=q[0], related=True))
        for (c,) in con.execute("select distinct t_service from ledger where pid=? and year(t_service)=2026 and stype in ('Grass Maint','Weed-Grass') order by 1", [rpid]).fetchall():
            tl.append(ev(d(c, '%Y-%m-%d'), f'{rlabel}: Forestry ledger bills a grass cut', 'ledger', 'cut', related=True))
    tl.sort(key=lambda e: e['date'] or '')
    w26 = [r for r in reqs if r[2] == 'Weeds-Vacant Lot' and r[5].year == 2026]
    return dict(
        id=cid, role=role, rank=rank, type='Weeds-Vacant Lot', ward=str(int(lra[4])), neighborhood=lra[5],
        place=dict(level='block', block=block_of(addr), what='a vacant lot owned by the city land bank (LRA)'),
        story=story,
        facts=dict(weeds_requests_2026=len(w26),
                   weeds_requests_2026_filed=[d(r[5], '%Y-%m-%d') for r in w26],
                   weeds_requests_2026_minutes_to_close=[round((r[6] - r[5]).total_seconds() / 60) if r[6] else None for r in w26],
                   weeds_requests_2026_promise=[d(r[7], '%Y-%m-%d') for r in w26], weeds_requests_2026_closed_on_schedule_within_3d=sum(
                       1 for r in w26 if r[6] and days(r[5], r[6]) <= 3 and r[4] and ('schedule' in r[4] or 'rotation' in r[4])),
                   cuts_billed_2026=sum(1 for c in cuts if c.year == 2026), cuts_billed_2025=n25,
                   cuts_billed_2019_2024={str(y): n for y, n in hist}, on_forestry_maintenance_list=fmp[0] if fmp else None,
                   other_parcels_on_city_block_cut_2026=blk[1], other_lra_parcels_on_city_block_cut_2026=blk[2],
                   distinct_cut_days_on_city_block_2026=blk[3], lra_offer_decisions=len(offs),
                   cut_complaint_calls_2026={k: sum(1 for r in reqs if r[2] == k and r[5].year == 2026) for k in COMPLAINT
                                             if any(r[2] == k and r[5].year == 2026 for r in reqs)}),
        timeline=tl, public_images=[],
        private=dict(parcel_id=pid, handle=handle, address=addr, lra_status=lra[1], lra_usage=lra[2], request_ids=[r[0] for r in reqs],
                     related=[dict(pid=x['pid'], handle=x['handle'], address=x['address']) for x in related],
                     related_handles=[x['handle'] for x in related]),
        sources={k: SRC[k] for k in ('csb', 'ledger', 'msd', 'lra', 'lra_offers', 'fmp')})

lots = [
    lot_case(HERO_IDS['lot-1']['pid'], 'lot-1', 'hero', 1,
             "Three city-owned vacant lots around the corner of N Taylor Av and Aldine Av in the Greater Ville (Ward 12) were reported together "
             "on 2 July and again on 28 July 2026, and every request closed within minutes as \"on schedule to be cut\"; the city's own ledger "
             "bills cuts on two of them within four weeks, and none on the third, on the 1700 block of N Taylor, all season: not by the city's own "
             "30 September promise date, and not after a 9 September call reporting that the lot's cut was left incomplete.",
             related=HERO_IDS['lot-1']['related']),
    lot_case(HERO_IDS['lot-2']['pid'], 'lot-2', 'hero', 2,
             "A city-owned vacant lot on the 8100 block of Church Rd in Baden (Ward 12) was reported four times between April and August 2026; "
             "each request closed within hours as \"on schedule to be cut\", and the city's ledger records no cut on it in 2026 at all."),
    lot_case(HERO_IDS['lot-3']['pid'], 'lot-3', 'hero', 3,
             "A city-owned vacant lot on the 1300 block of Arlington Av in Hamilton Heights (Ward 13) drew five weed reports in July and August 2026, "
             "each closed within a day as \"on schedule to be cut\", plus a staff report that it was missed on the cutting rotation and a resident call "
             "that its cut was left incomplete; the ledger, which billed cuts on it in every year but one from 1996 to 2024, "
             "shows none in 2025 or 2026, and the land bank's own offers file (an offer marked accepted in January 2026) may be why, an "
             "explanation 311 never gave."),
    lot_case(HERO_IDS['lot-counterexample']['pid'], 'lot-counterexample', 'counterexample', None,
             "The system working: a city-owned vacant lot on the 4000 block of Ashland Av in the Greater Ville (Ward 12), reported on "
             "11 September 2026, closed in three minutes as \"on schedule to be cut\", and the ledger bills a cut four days later."),
]

# =====================================================================================
# 2. THE LIGHT  (Single Light Out, resident channels, initiated on/after 16 May 2025, closed "work completed")
# Rule: per ward group, candidates within 0.5 day of the group's median days-to-close (one row per
# request); pick the pair filed closest together in time, same intake channel.
# =====================================================================================
def group_median(code, res, wards, table):
    return con.execute(f"""select count(*), median(date_diff('second',t_init,t_closed)/86400.0) from {table}
                           where PROBLEMCODE=? and resident and t_init>=timestamp '{TORNADO}' and STATUS='CLOSED' and resolution=? and WARD in {wards}""",
                       [code, res]).fetchone()
med = {}
for code, res, key in [('Single Light Out', 'work completed', 'light_wc'), ('Cave-Ins', 'work completed', 'cave_wc'),
                       ('Cave-Ins', 'referred to street maintenance for repair work to be scheduled', 'cave_ref')]:
    for gname, wards in (('w1_5', G15), ('w10_14', G1014)):
        n, m = group_median(code, res, wards, 'csbd')
        n2, m2 = group_median(code, res, wards, 'csb')
        med[(key, gname)] = (n, m)
        grp = "1-5" if gname == "w1_5" else "10-14"
        fig(f'n5_{key}_{gname}_median_days', round(m, 1), 'days', f'initiated {TORNADO} to 2026-10-13',
            f'{code} closed "{res}", resident channels, wards {grp}: median days from filing to closing (n={n} requests)', 'observed',
            f"311 requests (city open data, csb.zip 2025 and 2026 files, invalid bytes dropped), one row per request id (the files repeat {16042:,} ids), "
            f"resident channels only, filed on or after the 16 May 2025 tornado, closing text exactly \"{res}\"; ward from the 311 WARD field.",
            note=f'with duplicate request rows kept, as in COMMON.md: {round(m2, 1)} days, n={n2}')

def pick_pair(code, resA, wardsA, lo_hi_A, resB, wardsB, lo_hi_B):
    q = f"""select REQUESTID, CALLERTYPE, WARD, PROBADDRESS, addr_n, t_init, t_closed, t_promise, resolution,
                   date_diff('second',t_init,t_closed)/86400.0 dd
            from csbd where PROBLEMCODE=? and resident and t_init>=timestamp '{TORNADO}' and STATUS='CLOSED' and resolution=? and WARD in {{w}}
              and date_diff('second',t_init,t_closed)/86400.0 between ? and ?"""
    A = con.execute(q.format(w=wardsA), [code, resA, *lo_hi_A]).fetchall()
    B = con.execute(q.format(w=wardsB), [code, resB, *lo_hi_B]).fetchall()
    best = min(((abs((a[5] - b[5]).total_seconds()) + (0 if a[1] == b[1] else 1e9), a, b) for a in A for b in B), key=lambda t: t[0])
    return best[1], best[2], len(A), len(B)

def request_case(r, code, cid, role):
    rid, caller, ward, addr, addr_n, ti, tc, tp, res, dd = r
    later = con.execute("""select REQUESTID, t_init, STATUS, resolution from csbd where PROBLEMCODE=? and addr_n=? and t_init > ? and t_init <= ? + interval 60 day order by t_init""",
                        [code, addr_n, tc or ti, tc or ti]).fetchall()
    during = con.execute("select count(*) from csbd where PROBLEMCODE=? and addr_n=? and t_init > ? and t_init < ?", [code, addr_n, ti, tc or ti]).fetchone()[0]
    tl = [ev(d(ti), f'311 request filed ({caller})', 'csb', 'filed', request_id=rid),
          ev(d(tp, '%Y-%m-%d'), f"The city's own promise date: {days(ti, tp)} days after filing", 'csb', 'promise', request_id=rid)]
    if tc:
        tl.append(ev(d(tc), f'Closed after {round(dd, 1)} days: "{res}"', 'csb', 'closed', request_id=rid))
    for l in later:
        tl.append(ev(d(l[1]), f'Another {code} request on the same address, {days(tc, l[1])} days after this one closed ({l[2]}, "{l[3] or "(no text)"}")',
                     'csb', 'later', request_id=l[0]))
    tl.sort(key=lambda e: e['date'] or '')
    return dict(id=cid, role=role, type=code, ward=str(int(ward)), place=dict(level='block', block=block_of(addr)),
                days_to_close=round(dd, 1), promise_days=days(ti, tp) if tp else None,
                facts=dict(same_type_requests_at_address_while_open=during, same_type_requests_within_60d_after_close=len(later)),
                story='', timeline=tl, public_images=[], private=dict(request_ids=[rid], address=addr), sources={'csb': SRC['csb']})

mA, mB = med[('light_wc', 'w1_5')][1], med[('light_wc', 'w10_14')][1]
a, b, nA, nB = pick_pair('Single Light Out', 'work completed', G15, (mA - .5, mA + .5), 'work completed', G1014, (mB - .5, mB + .5))
light_a = request_case(a, 'Single Light Out', 'light-1', 'light-south')
light_b = request_case(b, 'Single Light Out', 'light-2', 'light-north')
light_a['story'] = (f"A single streetlight out on the {light_a['place']['block']} (Ward {int(a[2])}), reported {a[5]:%-d %B %Y} with the city's "
                    f"three-day promise, closed \"work completed\" after {light_a['days_to_close']} days, about the median for wards 1-5.")
light_b['story'] = (f"The same report on the {light_b['place']['block']} (Ward {int(b[2])}), filed {b[5]:%-d %B %Y} with the same three-day promise, "
                    f"closed \"work completed\" after {light_b['days_to_close']} days, about the median for wards 10-14: same words, same promise, "
                    f"{round(light_b['days_to_close'] / light_a['days_to_close'], 1)} times the wait.")
print('light pair', a[0], b[0], 'candidates', nA, nB)

# =====================================================================================
# 3. THE CAVE-IN PAIR: wards 1-5 closed "referred ... to be scheduled" within a day (median there 0.8 d)
# vs wards 10-14 closed "work completed" within a day of that group's median. Same pairing rule.
# =====================================================================================
REF = 'referred to street maintenance for repair work to be scheduled'
mR, mW = med[('cave_ref', 'w1_5')][1], med[('cave_wc', 'w10_14')][1]
ca, cb, nA, nB = pick_pair('Cave-Ins', REF, G15, (max(0, mR - .25), min(1.0, mR + .25)), 'work completed', G1014, (mW - 1, mW + 1))
cave_a = request_case(ca, 'Cave-Ins', 'cave-1', 'cave-paperwork')
cave_b = request_case(cb, 'Cave-Ins', 'cave-2', 'cave-work')
cave_a['story'] = (f"A cave-in on the {cave_a['place']['block']} (Ward {int(ca[2])}) closed in {cave_a['days_to_close']} days, which a time-to-close "
                   f"scoreboard counts as fast, but the closing words were \"{REF}\": a hand-off, and no public file we hold says when the repair happened.")
gap = (cb[5].date() - ca[5].date()).days
cave_b["story"] = (f"Filed {gap} days {'later' if gap >= 0 else 'earlier'}, a cave-in on the {cave_b['place']['block']} (Ward {int(cb[2])}) closed after {cave_b['days_to_close']} days "
                   f"with \"work completed\", which the same scoreboard counts as slow, though it is the only one of the two whose closure says the work was done.")
print('cave pair', ca[0], cb[0], 'candidates', nA, nB)

# =====================================================================================
# 4. THE TREE: "Inspect City Tree" cancelled with no text, resident channel, whose normalised address
# equals the address of an open removal work order in the Cityworks sample (saved search 6955) with a
# projected start within one hour of the 311 cancellation (WO dates UTC -> Central). Earliest such
# request (longest elapsed time). Block level.
# =====================================================================================
rows = con.execute("""select c.REQUESTID, c.CALLERTYPE, c.WARD, c.PROBADDRESS, c.t_init, c.t_cancel, c.t_invdone, c.t_promise,
                             w.woid, w.descr, w.priority, w.status, w.proj_start, w.proj_finish, c.resident
                      from csbd c join wo_rm w using (addr_n)
                      where c.PROBLEMCODE='Inspect City Tree' and c.STATUS='CANCEL' and coalesce(c.resolution,'')=''""").fetchall()
def mins_phrase(a, b):
    m = round((a - b).total_seconds() / 60)
    if m == 0:
        return 'the same minute'
    return ('a minute' if abs(m) == 1 else f'{abs(m)} minutes') + (' later' if m > 0 else ' earlier')
def ct(x):
    return x.replace(tzinfo=UTC).astimezone(CT).replace(tzinfo=None) if x else None
pairs = [(r, ct(r[12]), ct(r[13])) for r in rows]
n_cancel_blank = con.execute("select count(*) from csbd where PROBLEMCODE='Inspect City Tree' and STATUS='CANCEL' and coalesce(resolution,'')=''").fetchone()[0]
req_matched = {r[0] for r, s, f in pairs}
req_within_day = {r[0] for r, s, f in pairs if r[5] and s and abs((s - r[5]).total_seconds()) <= 86400}
req_wo_before = {r[0] for r, s, f in pairs if s and s < r[4] - dt.timedelta(days=1)} - req_within_day
TREE_DER = ("311 requests (csb.zip 2025 and 2026, one row per request id) of type 'Inspect City Tree' cancelled with no closing text, joined to the "
            "1,500-row public sample of open Forestry tree-removal work orders (Cityworks saved search 6955) where the two addresses are identical "
            "after the project's address normaliser; work-order dates converted from UTC to Central.")
fig('n5_tree_cancel_blank_requests', n_cancel_blank, 'requests', '2025-01-01 to 2026-10-13',
    '"Inspect City Tree" requests cancelled with no closing text', 'observed',
    "311 requests (csb.zip 2025 and 2026 files), one row per request id, STATUS CANCEL and empty PUBLICRESOLUTION.")
fig('n5_tree_cancel_blank_matched_removal_wo', len(req_matched), 'requests', '2025-01-01 to 2026-10-13',
    'of those, requests at the address of an open tree-removal work order in the public sample', 'observed', TREE_DER,
    note='the sample holds 1,500 of 2,522 removal work orders and address matching misses many, so a lower bound (COMMON correction 3)')
fig('n5_tree_cancel_blank_wo_within_24h', len(req_within_day), 'requests', '2025-01-01 to 2026-10-13',
    "of the matched, requests cancelled within 24 hours of the work order's projected start", 'observed', TREE_DER,
    note='read as: cancelled at the moment a removal work order was opened (inferred)')
fig('n5_tree_cancel_blank_wo_predates', len(req_wo_before), 'requests', '2025-01-01 to 2026-10-13',
    'of the matched, requests filed more than a day after an open removal work order at the address had started', 'observed', TREE_DER,
    note='read as: the tree was already on the removal list and the request was cancelled as a duplicate (inferred)')
ages = sorted(min((r[4] - s).total_seconds() / 86400 for r, s, f in pairs if r[0] == rid and s and s < r[4] - dt.timedelta(days=1))
              for rid in req_wo_before)
fig('n5_tree_predating_wo_median_age_days', round(ages[len(ages) // 2], 0), 'days', '2025-01-01 to 2026-10-13',
    'for those requests, median days the (most recent) open removal work order at the address had already been open when the 311 request was filed',
    'observed', TREE_DER, note=f'quartiles {ages[len(ages) // 4]:.0f} and {ages[3 * len(ages) // 4]:.0f} days; n={len(ages)}')
cands = sorted([(r, s, f) for r, s, f in pairs if r[14] and r[5] and s and abs((s - r[5]).total_seconds()) <= 3600], key=lambda t: t[0][4])
r, s, f = cands[0]
print('tree', r[0], 'candidates within 1 h', len(cands))
later_tree = con.execute("""select REQUESTID, PROBLEMCODE, t_init, STATUS, resolution from csbd where addr_n=(select addr_n from csbd where REQUESTID=?)
                            and t_init > ? and PROBLEMCODE in ('Inspect City Tree','City Tree Down','City Tree Limb Down','Stump Removal','Broken/Hanging Limb')
                            order by t_init""", [r[0], r[4]]).fetchall()
tl = [ev(d(r[4]), f'311 "Inspect City Tree" request filed ({r[1]})', 'csb', 'filed', request_id=r[0]),
      ev(d(r[7], '%Y-%m-%d'), f"The city's own promise date: {days(r[4], r[7])} days after filing", 'csb', 'promise', request_id=r[0])]
if r[6]:
    tl.append(ev(d(r[6]), 'Investigation recorded as done', 'csb', 'invdone', request_id=r[0]))
tl += [ev(d(s), f'A Forestry tree-removal work order at the same address shows its projected start (priority {r[10]})', 'wo_rm', 'wo_start', work_order_id=r[8]),
       ev(d(s), 'Read as: the inspection became a removal work order at this moment', 'wo_rm', 'wo_start', label='inferred'),
       ev(d(r[5]), '311 request cancelled, no public text', 'csb', 'cancel', request_id=r[0]),
       ev(d(f, '%Y-%m-%d'), "The work order's projected finish date", 'wo_rm', 'wo_finish', work_order_id=r[8]),
       ev('2026-10-13', f'The work order is still status "{r[11]}" when the saved search was read', 'wo_rm', 'wo_status', work_order_id=r[8])]
for l in later_tree:
    tl.append(ev(d(l[2]), f'Later tree request on the same address: {l[1]} ({l[3]}, "{l[4] or "(no text)"}")', 'csb', 'later', request_id=l[0]))
tl.sort(key=lambda e: (e['date'] or '', e['label']))
tree = dict(id='tree-1', role='tree', type='Inspect City Tree', ward=str(int(r[2])), place=dict(level='block', block=block_of(r[3])),
            story=(f"A resident asked Forestry to inspect a city tree on the {block_of(r[3])} (Ward {int(r[2])}) on {r[4]:%-d %B %Y}; "
                   f"{'the inspection was logged done on ' + format(r[6], '%-d %B') + ', ' if r[6] else ''}a Forestry removal work order at the same address "
                   f"shows a projected start of {s:%-I:%M %p} that day, and the 311 request was cancelled {mins_phrase(r[5], s)} with no words; the public "
                   f"record says \"cancelled\", the work order says removal by {f:%-d %B %Y}, and it was still open on 13 October 2026."),
            facts=dict(minutes_cancel_after_wo_start=round((r[5] - s).total_seconds() / 60, 1), wo_priority=r[10], wo_status_2026_10_13=r[11],
                       days_from_request_to_oct13_2026=days(r[4], dt.datetime(2026, 10, 13)), days_past_projected_finish=days(f, dt.datetime(2026, 10, 13))),
            timeline=tl, public_images=[], private=dict(request_ids=[r[0]], work_order_id=r[8], address=r[3],
            alternates=[dict(request_id=c[0][0], ward=c[0][2], block=block_of(c[0][3]), filed=d(c[0][4]), cancelled=d(c[0][5]), wo=c[0][8],
                             wo_priority=c[0][10], wo_start_ct=d(c[1]), wo_finish_ct=d(c[2], '%Y-%m-%d')) for c in cands[1:8]]),
            sources={'csb': SRC['csb'], 'wo_rm': SRC['wo_rm']})

# tree-2: the backlog version. Rule: resident channel, filed in 2026, cancelled with no text, at the address of an
# open removal work order that had started more than a day before the request; the one whose work-order age is
# nearest the median age (ties: latest filing). Block level.
med_age = ages[len(ages) // 2]
c2 = []
for r2, s2, f2 in pairs:
    if r2[14] and r2[4].year == 2026 and s2 and s2 < r2[4] - dt.timedelta(days=1):
        c2.append((abs((r2[4] - s2).total_seconds() / 86400 - med_age), -r2[4].timestamp(), r2, s2, f2))
c2.sort(key=lambda t: (t[0], t[1]))
_, _, r2, s2, f2 = c2[0]
n_same = con.execute("""select count(*) from csbd where PROBLEMCODE='Inspect City Tree' and addr_n=(select addr_n from csbd where REQUESTID=?)
                        and t_init >= ? """, [r2[0], s2]).fetchone()[0]
tl2 = [ev(d(s2), f'A Forestry tree-removal work order at this address shows its projected start (priority {r2[10]})', 'wo_rm', 'wo_start', work_order_id=r2[8]),
       ev(d(f2, '%Y-%m-%d'), "The work order's projected finish date", 'wo_rm', 'wo_finish', work_order_id=r2[8]),
       ev(d(r2[4]), f'311 "Inspect City Tree" request filed ({r2[1]}), {days(s2, r2[4]):.0f} days after the work order started', 'csb', 'filed', request_id=r2[0]),
       ev(d(r2[7], '%Y-%m-%d'), f"The city's own promise date: {days(r2[4], r2[7]):.0f} days after filing", 'csb', 'promise', request_id=r2[0]),
       ev(d(r2[5]), '311 request cancelled, no public text', 'csb', 'cancel', request_id=r2[0]),
       ev('2026-10-13', f'The work order is still status "{r2[11]}" when the saved search was read', 'wo_rm', 'wo_status', work_order_id=r2[8])]
tl2.sort(key=lambda e: e['date'] or '')
tree2 = dict(id='tree-2', role='tree-backlog', type='Inspect City Tree', ward=str(int(r2[2])), place=dict(level='block', block=block_of(r2[3])),
             story=(f"On {r2[4]:%-d %B %Y} a resident asked Forestry to inspect a city tree on the {block_of(r2[3])} (Ward {int(r2[2])}); "
                    f"Forestry already had an open removal work order there, started {days(s2, r2[4]):.0f} days earlier and due by {f2:%-d %B %Y}; "
                    f"the request was cancelled {dur(r2[4], r2[5])} later with no public words, so the public record never says the tree was already "
                    f"on the removal list ({n_same} inspection requests at that address since the work order started), and the work order was still open on 13 October 2026."),
             facts=dict(wo_age_days_at_request=round(days(s2, r2[4])), wo_priority=r2[10], wo_status_2026_10_13=r2[11],
                        inspect_requests_at_address_since_wo_start=n_same, days_past_projected_finish=days(f2, dt.datetime(2026, 10, 13))),
             timeline=tl2, public_images=[], private=dict(request_ids=[r2[0]], work_order_id=r2[8], address=r2[3]),
             sources={'csb': SRC['csb'], 'wo_rm': SRC['wo_rm']})
print('tree-2', r2[0], 'candidates', len(c2))

# ---------- lot figures (from 02_lot_candidates.py) ----------
fn = json.load(open(os.path.join(OUT, 'lot_funnel.json')))
LOT_DER = ("311 'Weeds-Vacant Lot' requests filed in 2026 (csb.zip, one row per request id) on land-bank (LRA) parcels, resident channels, closed within "
           "three days with \"on schedule to be cut\" or \"added to rotation\"; joined to the Forestry billing ledger by parcel through MSD's parcel address file "
           "(83% of 2026 requests matched a parcel); ledger dates are posted in weekly batches, so read to the week; ledger read to 13 Oct 2026.")
for i, v, u, dfn in [
    ('n5_lot_lra_on_schedule_requests', fn['requests'], 'requests', 'land-bank lot weed requests closed "on schedule" or "added to rotation" within 3 days'),
    ('n5_lot_lra_on_schedule_parcels', fn['parcels'], 'parcels', 'distinct land-bank lots behind those requests'),
    ('n5_lot_cut_by_promise', fn['cut_by_promise_requests'], 'requests', "of those requests, a cut billed on the lot by the request's own promise date"),
    ('n5_lot_cut_within_7d', fn['cut_within_7d_requests'], 'requests', 'of those requests, a cut billed within 7 days of filing'),
    ('n5_lot_no_cut_after_request', fn['no_cut_after_requests'], 'requests', 'of those requests, no cut billed on the lot at any time after filing, to 13 Oct 2026'),
    ('n5_lot_no_cut_after_request_parcels', fn['no_cut_after_parcels'], 'parcels', 'distinct lots with at least one such request'),
    ('n5_lot_no_cut_2026_parcels', fn['no_2026_cut_parcels'], 'parcels', 'lots with no cut billed at any time in 2026'),
    ('n5_lot_before_15jul_no_cut', fn['before_15jul_no_cut_requests'], 'requests', f"of {fn['before_15jul_requests']} such requests filed before 15 Jul 2026, no cut billed by 13 Oct"),
]:
    fig(i, v, u, '2026 season to 2026-10-13', dfn, 'observed', LOT_DER, script='scripts/night/N5/02_lot_candidates.py',
        note='a billing ledger is not an operations log: no charge is not proof of no cut')
con.execute(f"""create temp table py as select trim(PARCEL) pid, year(try_cast(SERVICEDATE as timestamp)) y, count(*) n
    from read_csv('{RAW}/stlouis-mo.gov/files/forestry-service-records.csv', all_varchar=true, header=true)
    where SERVICETYPE in ('Grass Maint','Weed-Grass') and SERVICEDATE >= '2022-01-01' and PARCEL is not null group by 1, 2""")
pcount = dict(con.execute("select y, count(distinct pid) from py group by 1").fetchall())
def dropoff(y0, y1):
    return con.execute(f"""with a as (select distinct pid from py where y={y0} and pid in (select pid from lra))
        select count(*), count(*) filter (where not exists (select 1 from py b where b.pid=a.pid and b.y={y1})) from a""").fetchone()
d24, d23, d22, d24_25 = dropoff(2024, 2026), dropoff(2023, 2024), dropoff(2022, 2023), dropoff(2024, 2025)
for y in (2024, 2025, 2026):
    fig(f'n5_ledger_parcels_cut_{y}', pcount[y], 'parcels', str(y) + (' to 2026-10-13' if y == 2026 else ''),
        'distinct parcels with a grass-cut charge in the Forestry ledger', 'observed',
        "Forestry billing ledger: distinct PARCEL values with a 'Grass Maint' or 'Weed-Grass' charge dated in the year.",
        note='2025 is thin (tornado year), so "no cut in 2025" is weak evidence; the hero cases rest on 2026' if y == 2025 else '')
fig('n5_lra_cut2024_none2026', d24[1], 'parcels', '2024 vs 2026', f'land-bank parcels with a cut billed in 2024 and none in 2026 (of {d24[0]:,})', 'observed',
    "Forestry billing ledger joined to the LRA inventory on parcel id; a parcel counts if it has a 'Grass Maint' or 'Weed-Grass' charge in 2024 and none dated 2026.",
    note=f'year-on-year baseline: {d23[1]:,} of {d23[0]:,} (2023 to 2024), {d22[1]:,} of {d22[0]:,} (2022 to 2023)')
fig('n5_dup_requestid_ids', 16042, 'request ids', '2025-2026 yearly files', 'request ids that appear on more than one row (234,374 rows, 216,532 distinct ids)', 'observed',
    "311 files 2025.csv and 2026.csv from csb.zip (invalid bytes dropped): count of REQUESTID values on two or more rows; most are exact copies, some differ only in CALLERTYPE.",
    script='scripts/night/N5/01_build_db.py', note='medians move slightly when deduplicated, e.g. single light out 15.8 -> 15.6 and 42.1 -> 41.0 days')

cases = lots + [light_a, light_b, tree, tree2, cave_a, cave_b]
heroes = dict(generated=dt.datetime.now(CT).strftime('%Y-%m-%d %H:%M %Z'),
              note=('Times are Central; Cityworks dates converted from UTC. Every case is at block level in public outputs (Jack, 13 Oct). '
                    'Request, work-order and parcel ids are kept only in this private file.'),
              ledger_end=d(LEDGER_END, '%Y-%m-%d'), cases=cases)
json.dump(heroes, open(os.path.join(PRIV, 'heroes_private.json'), 'w'), indent=1, default=str)
json.dump(figures, open(os.path.join(OUT, 'figures.json'), 'w'), indent=1, default=str)
print('wrote private heroes with', len(cases), 'cases;', len(figures), 'figures')
for c in cases:
    print('\n#', c['id'], c['private'].get('request_ids'), c.get('ward'), c['place']['block'])
    print(' ', c['story'])
