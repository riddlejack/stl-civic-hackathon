"""N5 step 2: the lot. Weeds-Vacant Lot requests in 2026 on LRA-owned parcels, resident channel,
closed within three days as 'on schedule to be cut' or 'added to rotation', joined to the forestry
ledger cuts on the same parcel. Writes build/N5/private/lot_candidates.csv and lot_counterexamples.csv and
prints the funnel (each filter's count) so the selection is reproducible.

Ledger cuts = SERVICETYPE in ('Grass Maint','Weed-Grass'). Ledger posting dates are batched (many
Sundays), so cut dates are precise to about a week.
"""
import duckdb, os
ROOT = '/Users/jackriddle/Desktop/stl-civic-hackathon'
con = duckdb.connect(os.path.join(ROOT, 'build/N5/private/n5.duckdb'))
LEDGER_END = con.execute("select max(t_service) from ledger").fetchone()[0]
print('ledger last service date', LEDGER_END)

con.execute("""
create or replace temp table w as
select c.*, coalesce(a.pid, l2.pid) as pid,
       case when a.pid is not null then 'msd' when l2.pid is not null then 'lra_address' end as pid_via,
       date_diff('second', t_init, t_closed)/86400.0 as days_to_close
from csbd c
left join a2p a using (addr_n)
left join (select lra_addr_n, min(pid) pid from lra group by 1) l2 on l2.lra_addr_n = c.addr_n and a.pid is null
where PROBLEMCODE = 'Weeds-Vacant Lot' and year(t_init) = 2026
""")
f = lambda q: con.execute(q).fetchone()
print('funnel:')
print(' 2026 Weeds-Vacant Lot requests', f("select count(*) from w"))
print(' with parcel match (msd / lra address)', f("select count(*) filter (where pid is not null), count(*) filter (where pid_via='msd'), count(*) filter (where pid_via='lra_address') from w"))
print(' on LRA parcel', f("select count(*) from w join lra using (pid)"))
print(' + resident channel', f("select count(*) from w join lra using (pid) where resident"))
print(' + closed', f("select count(*) from w join lra using (pid) where resident and STATUS='CLOSED'"))
print(' + on schedule / rotation', f("""select count(*) from w join lra using (pid) where resident and STATUS='CLOSED'
       and (lower(resolution) like '%schedule%' or lower(resolution) like '%rotation%')"""))
print(' + closed within 3 days', f("""select count(*) from w join lra using (pid) where resident and STATUS='CLOSED'
       and (lower(resolution) like '%schedule%' or lower(resolution) like '%rotation%') and days_to_close <= 3"""))

con.execute("""
create or replace temp table base as
select w.*, lra.Parcel_Status, lra.Usage, lra.NeighborhoodName, lra.lra_ward, lra.lra_address, lra.ACQUISITION_DATE,
       fmp.fmp_category
from w join lra using (pid) left join fmp using (pid)
where resident and STATUS='CLOSED' and (lower(resolution) like '%schedule%' or lower(resolution) like '%rotation%')
  and days_to_close <= 3
""")
# cuts per parcel
con.execute("""
create or replace temp table cuts as
select pid, t_service, stype from ledger where stype in ('Grass Maint','Weed-Grass')
""")
con.execute("""
create or replace temp table cand as
select b.REQUESTID, b.CALLERTYPE, b.WARD, b.lra_ward, b.NEIGHBORHOOD, b.NeighborhoodName, b.pid, b.addr_n, b.pid_via, b.lra_address,
       b.Parcel_Status, b.Usage, b.fmp_category, b.t_init, b.t_closed, b.t_promise, b.t_invdone, b.resolution,
       round(b.days_to_close, 2) as days_to_close, b.srx, b.sry,
       (select max(t_service) from cuts c where c.pid=b.pid and year(c.t_service)=2026 and c.t_service < b.t_init) as last_cut_before,
       (select min(t_service) from cuts c where c.pid=b.pid and c.t_service >= b.t_init) as first_cut_after,
       (select count(*) from cuts c where c.pid=b.pid and year(c.t_service)=2026) as cuts_2026,
       (select count(*) from cuts c where c.pid=b.pid and year(c.t_service)=2025) as cuts_2025,
       (select count(*) from csbd r where r.addr_n=b.addr_n and r.t_init > b.t_closed
           and r.PROBLEMCODE in ('Weeds-Vacant Lot','Weeds-Vacant Bldg','Weeds-Occupied Ppty')) as later_weed_requests,
       (select min(r.t_init) from csbd r where r.addr_n=b.addr_n and r.t_init > b.t_closed
           and r.PROBLEMCODE in ('Weeds-Vacant Lot','Weeds-Vacant Bldg','Weeds-Occupied Ppty')) as next_weed_request,
       (select count(*) from csbd r where r.addr_n=b.addr_n and year(r.t_init)=2026
           and r.PROBLEMCODE in ('Weeds-Vacant Lot','Weeds-Vacant Bldg','Weeds-Occupied Ppty')) as weed_requests_2026
from base b
""")
con.execute(f"""
create or replace temp table cand2 as
select *, date_diff('day', t_init, coalesce(first_cut_after, timestamp '{LEDGER_END}')) as days_without_cut,
       first_cut_after is null as no_cut_after
from cand
""")
print(' candidates (all with ledger join)', f("select count(*) from cand2"))
print(' no cut >= 60 days after request', f("select count(*) from cand2 where days_without_cut >= 60"))
print(' no cut at all after request (to ledger end)', f("select count(*) from cand2 where no_cut_after"))
print(' no 2026 cut at all on the parcel', f("select count(*) from cand2 where cuts_2026 = 0"))
print(' distinct parcels: all / no cut after a request / no 2026 cut', f("""select count(distinct pid),
       count(distinct pid) filter (where no_cut_after), count(distinct pid) filter (where cuts_2026 = 0) from cand2"""))
print(' requests filed before 15 Jul (>=90 days of ledger to look at): n / no cut after', f("""select count(*),
       count(*) filter (where no_cut_after) from cand2 where t_init < timestamp '2026-07-15'"""))
print(' cut within 7 days (counter-examples)', f("select count(*) from cand2 where date_diff('day', t_init, first_cut_after) <= 7"))
print(' ... of which promise met (cut by promise date)', f("select count(*) from cand2 where first_cut_after <= t_promise"))

funnel = dict(zip(['requests', 'parcels', 'no_cut_after_requests', 'no_cut_after_parcels', 'no_2026_cut_requests', 'no_2026_cut_parcels',
                   'ge60d_requests', 'cut_by_promise_requests', 'cut_within_7d_requests', 'before_15jul_requests', 'before_15jul_no_cut_requests'],
    con.execute("""select count(*), count(distinct pid), count(*) filter (where no_cut_after), count(distinct pid) filter (where no_cut_after),
        count(*) filter (where cuts_2026 = 0), count(distinct pid) filter (where cuts_2026 = 0), count(*) filter (where days_without_cut >= 60),
        count(*) filter (where first_cut_after <= t_promise), count(*) filter (where date_diff('day', t_init, first_cut_after) <= 7),
        count(*) filter (where t_init < timestamp '2026-07-15'), count(*) filter (where t_init < timestamp '2026-07-15' and no_cut_after) from cand2""").fetchone()))
funnel['weeds_vacant_lot_2026_requests'] = f("select count(*) from w")[0]
funnel['with_parcel_match'] = f("select count(*) from w where pid is not null")[0]
funnel['on_lra_parcel'] = f("select count(*) from w join lra using (pid)")[0]
funnel['ledger_end'] = str(LEDGER_END)
import json
json.dump(funnel, open(f'{ROOT}/build/N5/lot_funnel.json', 'w'), indent=1)
print(funnel)
con.execute(f"copy (select * from cand2 order by days_without_cut desc, later_weed_requests desc) to '{ROOT}/build/N5/private/lot_candidates.csv' (header)")
con.execute(f"copy (select * from cand2 where date_diff('day', t_init, first_cut_after) <= 7 order by date_diff('second', t_init, first_cut_after)) to '{ROOT}/build/N5/private/lot_counterexamples.csv' (header)")

print('\nTop by days without cut, with later requests:')
for r in con.execute("""select REQUESTID, WARD, NeighborhoodName, lra_address, Parcel_Status, fmp_category, t_init::date, t_closed::date,
        t_promise::date, resolution, last_cut_before::date, first_cut_after::date, days_without_cut, cuts_2026, cuts_2025,
        later_weed_requests, next_weed_request::date
        from cand2 where days_without_cut >= 60 order by no_cut_after desc, later_weed_requests desc, days_without_cut desc limit 40""").fetchall():
    print(r)
print('\nBy neighbourhood (candidates with >=60 days no cut):')
for r in con.execute("select NeighborhoodName, lra_ward, count(*) from cand2 where days_without_cut>=60 group by 1,2 order by 3 desc limit 15").fetchall():
    print(r)
