-- DoneStat measures (N1). Plain DuckDB SQL over the tables build_db.py loads.
-- Every figure computed here is "our definition, from the public file".
-- A city analyst can run any of these views from the DuckDB command line:
--   duckdb build/stl.duckdb "SELECT * FROM receipt(<request_id>)"

-- ------------------------------------------------------------------ reference lists (reviewable)
CREATE TABLE type_family AS SELECT * FROM (VALUES
  ('Potholes - Residnl', 'pothole', true), ('Potholes - Major St', 'pothole', true), ('Potholes - Alley', 'pothole', true),
  ('Cave-Ins', 'cave_in', true), ('STREET-CAVEIN', 'cave_in', true), ('WALK-CAVEIN', 'cave_in', true), ('LAWN-CAVEIN', 'cave_in', true),
  ('Single Light Out', 'light', true), ('Whole Blk Lights Out', 'light', true), ('Light Damaged', 'light', true),
  ('Inspect City Tree', 'tree_city', true), ('City Tree Down', 'tree_city', true), ('City Tree Limb Down', 'tree_city', true),
  ('Stump Removal', 'tree_city', true), ('LRA Tree', 'tree_city', true), ('Tree Planting requst', 'tree_planting', false),
  ('Critical Sign', 'sign', true), ('Sign needs attention', 'sign', true),
  ('Weeds-Vacant Lot', 'weeds', false), ('Weeds-Vacant Bldg', 'weeds', false), ('Vcnt weed check-web', 'weeds', false),
  ('Weeds-Occupied Ppty', 'weeds', false), ('Weeds-Alley', 'weeds', false), ('High Grass in Park', 'weeds', false),
  ('Missed Cut - V Lot', 'weeds', false), ('Missed Cut - VBldg', 'weeds', false),
  ('Unsatisfy Cut - VLot', 'weeds', false), ('Unsatisfy Cut -VBldg', 'weeds', false),
  ('Illegal dumpg report', 'dumping', false), ('Debris-alley/street', 'dumping', false),
  ('Vehicle Towing', 'towing', false), ('Refuse not collected', 'refuse', false),
  ('Sidewalk Repair', 'sidewalk', false)
) t(problem_code, family, durable);

-- Ledger-joined weed codes: the city cuts vacant lots and vacant buildings.
CREATE TABLE weed_ledger_codes AS SELECT * FROM (VALUES
  ('Weeds-Vacant Lot'), ('Weeds-Vacant Bldg'), ('Vcnt weed check-web'),
  ('Missed Cut - V Lot'), ('Missed Cut - VBldg'), ('Unsatisfy Cut - VLot'), ('Unsatisfy Cut -VBldg')) t(problem_code);

-- CityStat goals observed on its pages (T-COMMON). Days, calendar.
CREATE TABLE citystat_goal AS SELECT * FROM (VALUES
  ('Potholes - Major St', 3.0), ('Potholes - Residnl', 8.0), ('Potholes - Alley', 17.0),
  ('Debris-alley/street', 3.0), ('Whole Blk Lights Out', 1.0), ('Critical Sign', 2.0)
) t(problem_code, goal_days);

-- Codes never shown below ward level (encampments, homeless and welfare calls,
-- discrimination complaints, legal claims, courts, police referrals). Decided on each code's usual
-- group and division, so one misrouted request cannot make a whole code sensitive.
CREATE TABLE sensitive_codes AS
WITH c AS (SELECT problem_code, mode(grp) AS grp, mode(submit_to) AS submit_to, any_value(type_name) AS type_name
           FROM requests WHERE problem_code IS NOT NULL GROUP BY problem_code)
SELECT problem_code, grp, submit_to FROM c
WHERE regexp_matches(upper(problem_code || ' ' || coalesce(type_name, '')), 'HOMELESS|ENCAMP|WELFARE|SHELTER|PANHANDL|DISCRIM|INMATE|INJURY|SLMPD|POLICE')
   OR problem_code ILIKE '%COURT%'  -- 'Misc-City Courts' sits in group 'Miscellaneous', so the group test missed it (N8 re-check R7)
   OR grp IN ('Discrimination', 'Legal Claims', 'Courts/Tickets/Jail', 'Human Services', 'SLMPD')
   OR upper(coalesce(submit_to, '')) LIKE 'DEPT HUMAN SVC%' OR upper(coalesce(submit_to, '')) LIKE 'CIVIL RIGHTS%'
   OR upper(coalesce(submit_to, '')) LIKE 'SLMPD%';

CREATE VIEW run_dates AS
SELECT CAST(max(value) FILTER (WHERE key = 'asof') AS DATE) AS asof_date,
       CAST(max(value) FILTER (WHERE key = 'asof_ts') AS TIMESTAMP) AS asof_ts,
       CAST(max(value) FILTER (WHERE key = 'ledger_max_date') AS DATE) AS ledger_max
FROM meta;

-- ------------------------------------------------------------------ request-level views
CREATE VIEW v_requests AS
SELECT r.*, c.closure_class, c.class_source, c.class_rule, f.family, coalesce(f.durable, false) AS durable
FROM requests r
LEFT JOIN closure_class c USING (request_id)
LEFT JOIN type_family f USING (problem_code);

-- promise: the city's own per-request promise date (PRJCOMPLETEDATE)
CREATE VIEW promise AS
SELECT r.request_id, r.problem_code, r.type_name, r.family, r.ward, r.ward_group, r.channel_group,
       r.init_year, r.init_quarter, r.tornado_period, r.submit_to, r.status_group, r.closure_class,
       r.ts_init, r.ts_promised, r.ts_closed, r.days_to_close, r.promise_days,
       r.ts_promised IS NOT NULL AS has_promise,
       r.ts_promised <= a.asof_ts AS promise_due,
       CASE WHEN r.ts_promised IS NOT NULL THEN r.status_group = 'closed' AND r.ts_closed <= r.ts_promised END AS closed_by_promise,
       CASE WHEN r.ts_promised IS NOT NULL THEN r.status_group = 'closed' AND r.closure_class = 'done' AND r.ts_closed <= r.ts_promised END AS done_by_promise,
       CASE WHEN r.status_group = 'closed' AND r.ts_promised IS NOT NULL
            THEN epoch(r.ts_closed - r.ts_promised) / 86400.0 END AS days_vs_promise,
       CASE WHEN g.goal_days IS NOT NULL AND r.status_group = 'closed' THEN r.days_to_close <= g.goal_days
            WHEN g.goal_days IS NOT NULL THEN false END AS within_citystat_goal,
       g.goal_days AS citystat_goal_days
FROM v_requests r CROSS JOIN run_dates a
LEFT JOIN citystat_goal g USING (problem_code);

-- refiled: the next request at the same normalised address and type, filed after this one closed
CREATE TABLE refiled_next AS
WITH c AS (SELECT request_id, addr_norm, problem_code, ts_closed FROM requests
           WHERE status_group = 'closed' AND addr_norm <> ''),
n AS (SELECT addr_norm, problem_code, ts_init AS next_init, request_id AS next_id FROM requests WHERE addr_norm <> '')
SELECT c.request_id, n.next_id, n.next_init, epoch(n.next_init - c.ts_closed) / 86400.0 AS days_to_next
FROM c ASOF LEFT JOIN n
  ON c.addr_norm = n.addr_norm AND c.problem_code = n.problem_code AND n.next_init > c.ts_closed;

CREATE VIEW refiled AS
SELECT x.request_id, r.problem_code, r.family, r.durable, r.ward, r.channel_group, r.init_year, r.init_quarter,
       r.closure_class, r.ts_closed, x.next_id, x.next_init, x.days_to_next,
       r.ts_closed + INTERVAL 14 DAY <= a.asof_ts AS window14_complete,
       r.ts_closed + INTERVAL 30 DAY <= a.asof_ts AS window30_complete,
       CASE WHEN r.durable THEN coalesce(x.days_to_next <= 14, false) END AS refiled_14,
       CASE WHEN r.durable THEN coalesce(x.days_to_next <= 30, false) END AS refiled_30,
       coalesce(x.days_to_next <= 30, false) AS came_back_30
FROM refiled_next x JOIN v_requests r USING (request_id) CROSS JOIN run_dates a;

-- request_ledger: weed requests vs grass cuts recorded on the matched parcel
CREATE TABLE request_ledger AS
WITH w AS (SELECT r.request_id, r.init_date, rp.pid
           FROM requests r JOIN request_parcel rp USING (request_id)
           WHERE r.problem_code IN (SELECT problem_code FROM type_family WHERE family = 'weeds'))
SELECT w.request_id, w.pid, w.init_date,
       count(c.service_date) FILTER (WHERE c.service_date >= w.init_date - 30 AND c.service_date < w.init_date) AS cuts_prev30,
       max(c.service_date) FILTER (WHERE c.service_date < w.init_date) AS last_cut_before,
       min(c.service_date) FILTER (WHERE c.service_date >= w.init_date) AS first_cut_after,
       count(c.service_date) FILTER (WHERE year(c.service_date) = year(w.init_date)) AS cuts_in_year,
       list_sort(list_distinct(list(c.service_date) FILTER (WHERE year(c.service_date) = year(w.init_date)))) AS cut_dates_in_year
FROM w LEFT JOIN cuts c ON c.parcel = w.pid
GROUP BY w.request_id, w.pid, w.init_date;

CREATE VIEW request_ledger_flags AS
SELECT l.*, a.ledger_max,
       date_diff('day', l.init_date, l.first_cut_after) AS days_to_first_cut,
       l.cuts_prev30 > 0 AS cut_prev30,
       CASE WHEN l.init_date + 30 <= a.ledger_max THEN coalesce(l.first_cut_after <= l.init_date + 30, false) END AS cut_within_30,
       CASE WHEN l.init_date + 60 <= a.ledger_max THEN coalesce(l.first_cut_after <= l.init_date + 60, false) END AS cut_within_60,
       coalesce(year(l.first_cut_after) = year(l.init_date), false) AS cut_by_season_end,
       l.cuts_in_year = 0 AS no_cut_in_season
FROM request_ledger l CROSS JOIN run_dates a;

-- weed requests graded by the ledger instead of the closure words: was the lot cut by the promised date?
CREATE VIEW weed_promise_ledger AS
SELECT r.request_id, r.problem_code, r.init_year, r.init_quarter, r.ward, r.channel_group, r.status_group, r.closure_class,
       CAST(r.ts_promised AS DATE) AS promised_date,
       CAST(r.ts_promised AS DATE) <= a.ledger_max AS promise_due_in_ledger,
       coalesce(l.first_cut_after <= CAST(r.ts_promised AS DATE), false) AS cut_by_promise,
       l.first_cut_after
FROM v_requests r JOIN request_ledger l USING (request_id) CROSS JOIN run_dates a
WHERE r.problem_code IN (SELECT problem_code FROM weed_ledger_codes) AND r.ts_promised IS NOT NULL;

-- request_wo: tree requests vs Cityworks tree work orders (1,500-row samples) at the
-- same normalised address or within 30 m (EPSG:3857 distance scaled by cos(latitude))
CREATE TABLE request_wo AS
WITH t AS (SELECT r.request_id, r.addr_norm, r.srx, r.sry, r.lat, r.ts_init FROM requests r
           WHERE r.problem_code IN (SELECT problem_code FROM type_family WHERE family IN ('tree_city', 'tree_planting'))),
w AS (SELECT w.*, a.addr_norm FROM wo_tree w LEFT JOIN addr_lookup a ON a.addr_raw = w.address),
by_addr AS (SELECT t.request_id, w.workorder_id, w.source, true AS addr_match, NULL::DOUBLE AS dist_m
            FROM t JOIN w ON t.addr_norm = w.addr_norm WHERE t.addr_norm <> ''),
by_xy AS (SELECT t.request_id, w.workorder_id, w.source, false AS addr_match,
                 sqrt((t.srx - w.x) ^ 2 + (t.sry - w.y) ^ 2) * cos(radians(t.lat)) AS dist_m
          FROM t JOIN w ON w.x BETWEEN t.srx - 40 AND t.srx + 40 AND w.y BETWEEN t.sry - 40 AND t.sry + 40
          WHERE t.lat IS NOT NULL),
m AS (SELECT request_id, workorder_id, source, bool_or(addr_match) AS addr_match, min(dist_m) AS dist_m
      FROM (SELECT * FROM by_addr UNION ALL SELECT * FROM by_xy WHERE dist_m <= 30)
      GROUP BY request_id, workorder_id, source),
-- removal and trim orders answer city-tree requests; planting orders answer planting requests
fam AS (SELECT r.request_id, f.family FROM requests r JOIN type_family f USING (problem_code))
SELECT m.request_id, m.workorder_id, m.source, m.addr_match, m.dist_m,
       w.description AS wo_description, w.status AS wo_status, w.priority AS wo_priority,
       w.proj_start, w.proj_finish, w.actual_finish,
       coalesce(w.proj_start, w.actual_finish) >= t.ts_init AS wo_dated_after_request
FROM m JOIN t USING (request_id) JOIN fam USING (request_id)
JOIN wo_tree w ON w.workorder_id = m.workorder_id AND w.source = m.source
WHERE (fam.family = 'tree_city' AND m.source IN ('tree_removal', 'tree_trim'))
   OR (fam.family = 'tree_planting' AND m.source IN ('planting_completed', 'planting_open'));

-- Dated orders (removals carry ProjStartDate) are split by whether they predate the request.
-- "Already open" uses N5's rule (COMMON 9, N8 conflict 3): same normalised address, order
-- started more than a day before the request was filed. Within 30 m reaches neighbouring
-- trees, so the 30 m counts are kept in separate columns and never called "this tree".
CREATE VIEW request_wo_summary AS
SELECT w.request_id,
       count(*) AS n_wo, count(*) FILTER (WHERE addr_match) AS n_wo_address, count(*) FILTER (WHERE dist_m <= 30) AS n_wo_30m,
       count(*) FILTER (WHERE source = 'tree_removal') AS n_removal, count(*) FILTER (WHERE source = 'tree_trim') AS n_trim,
       count(*) FILTER (WHERE source = 'tree_removal' AND addr_match AND proj_start < r.ts_init - INTERVAL 1 DAY)
         AS n_removal_open_before_request,
       count(*) FILTER (WHERE source = 'tree_removal' AND addr_match AND proj_start >= r.ts_init - INTERVAL 1 DAY)
         AS n_removal_dated_after_request,
       max(epoch(r.ts_init - proj_start) / 86400.0) FILTER (WHERE source = 'tree_removal' AND addr_match AND proj_start < r.ts_init - INTERVAL 1 DAY)
         AS days_oldest_removal_order_before_request,
       min(epoch(r.ts_init - proj_start) / 86400.0) FILTER (WHERE source = 'tree_removal' AND addr_match AND proj_start < r.ts_init - INTERVAL 1 DAY)
         AS days_recent_removal_order_before_request,
       count(*) FILTER (WHERE source = 'tree_removal' AND proj_start < r.ts_init - INTERVAL 1 DAY)
         AS n_removal_open_before_request_30m,
       list({'workorder_id': workorder_id, 'source': source, 'description': wo_description, 'status': wo_status,
             'proj_start': proj_start, 'proj_finish': proj_finish, 'actual_finish': actual_finish,
             'addr_match': addr_match, 'dist_m': round(dist_m, 1),
             'days_from_order_to_request': epoch(r.ts_init - coalesce(proj_start, actual_finish)) / 86400.0}
            ORDER BY coalesce(proj_start, actual_finish)) AS work_orders
FROM request_wo w JOIN requests r USING (request_id) GROUP BY w.request_id;

-- LRA lots closed "on schedule" with no cut billed after the request: N5's rule (COMMON 9,
-- N8 conflict 2): Weeds-Vacant Lot filed 2026, resident-filed, closed within 3 days as
-- "on schedule to be cut" or "added to rotation", on an LRA parcel, no cut billed after filing.
CREATE VIEW lra_onschedule_no_cut AS
SELECT r.request_id, rp.pid AS parcel, r.block_label, r.ward, r.init_date, r.ts_closed, r.ts_promised,
       l.first_cut_after, l.first_cut_after IS NULL AS no_cut_after_filing
FROM v_requests r JOIN request_parcel rp USING (request_id) JOIN request_ledger l USING (request_id)
WHERE r.problem_code = 'Weeds-Vacant Lot' AND r.init_year = 2026 AND r.channel_group = 'resident'
  AND r.status_group = 'closed' AND r.days_to_close <= 3 AND rp.is_lra
  AND (r.res_key LIKE 'on schedule to be cut%' OR r.res_key = 'added to rotation');

-- ------------------------------------------------------------------ aggregates
-- by_ward: type x ward x quarter x channel x class
CREATE TABLE by_ward AS
SELECT p.problem_code, any_value(p.type_name) AS type_name, p.ward, p.init_quarter, p.channel_group,
       coalesce(p.closure_class, p.status_group) AS class,
       count(*) AS n,
       median(p.days_to_close) AS median_days,
       avg(CAST(p.closed_by_promise AS INT)) AS share_closed_by_promise,
       avg(CASE WHEN p.promise_due THEN CAST(coalesce(p.done_by_promise, false) AS INT) END) AS share_done_by_promise_due,
       avg(CAST(p.status_group = 'open' AS INT)) AS open_share
FROM promise p WHERE p.init_year >= 2013
GROUP BY p.problem_code, p.ward, p.init_quarter, p.channel_group, coalesce(p.closure_class, p.status_group);

-- by_ward_type: the same without the class split, with class shares
CREATE TABLE by_ward_type AS
SELECT p.problem_code, any_value(p.type_name) AS type_name, p.ward, p.init_quarter, p.channel_group,
       count(*) AS n,
       count(*) FILTER (WHERE p.status_group = 'closed') AS n_closed,
       count(*) FILTER (WHERE p.status_group = 'open') AS n_open,
       count(*) FILTER (WHERE p.status_group = 'cancelled') AS n_cancelled,
       median(p.days_to_close) AS median_days,
       median(p.promise_days) AS median_promise_days,
       avg(CAST(p.closed_by_promise AS INT)) AS share_closed_by_promise,
       avg(CASE WHEN p.promise_due THEN CAST(coalesce(p.closed_by_promise, false) AS INT) END) AS share_closed_by_promise_due,
       avg(CASE WHEN p.promise_due THEN CAST(coalesce(p.done_by_promise, false) AS INT) END) AS share_done_by_promise_due,
       avg(CAST(p.status_group = 'open' AS INT)) AS open_share,
       avg(CASE WHEN p.status_group = 'closed' THEN CAST(p.closure_class = 'done' AS INT) END) AS share_closed_done,
       avg(CASE WHEN p.status_group = 'closed' THEN CAST(p.closure_class IN ('handed_off', 'converted') AS INT) END) AS share_closed_handoff
FROM promise p WHERE p.init_year >= 2013
GROUP BY p.problem_code, p.ward, p.init_quarter, p.channel_group;

-- Monday list: open requests past the city's own promise date (block level)
CREATE VIEW monday_list AS
SELECT r.request_id, r.problem_code, r.type_name, r.division AS division, r.ward, r.block_label,
       r.init_date AS filed, CAST(r.ts_promised AS DATE) AS promised,
       date_diff('day', CAST(r.ts_promised AS DATE), a.asof_date) AS days_past_promise,
       date_diff('day', r.init_date, a.asof_date) AS age_days,
       r.status, r.channel_group
FROM requests r CROSS JOIN run_dates a
WHERE r.status_group = 'open' AND r.ts_promised < a.asof_ts
  AND r.problem_code NOT IN (SELECT problem_code FROM sensitive_codes)
  AND upper(coalesce(r.submit_to, '')) NOT LIKE 'SLMPD%';

-- Illegal dumping repeat sites, last 365 days, block level
CREATE VIEW dumping_blocks AS
SELECT r.block_label, r.ward, count(*) AS n_requests,
       count(DISTINCT r.addr_norm) AS n_addresses,
       count(*) FILTER (WHERE r.problem_code = 'Illegal dumpg report') AS n_illegal_dumping_reports,
       count(*) FILTER (WHERE r.problem_code = 'Debris-alley/street') AS n_debris_reports,
       min(r.init_date) AS first_report, max(r.init_date) AS last_report,
       count(*) FILTER (WHERE r.status_group = 'closed') AS n_closed,
       count(*) FILTER (WHERE r.status_group = 'open') AS n_open,
       count(*) FILTER (WHERE r.closure_class = 'done') AS n_closed_done,
       count(*) FILTER (WHERE r.closure_class IN ('handed_off', 'converted')) AS n_closed_handoff,
       count(*) FILTER (WHERE r.closure_class = 'no_action') AS n_closed_no_action,
       median(r.days_to_close) AS median_days_to_close
FROM v_requests r CROSS JOIN run_dates a
WHERE r.family = 'dumping' AND r.init_date > a.asof_date - 365 AND r.block_label IS NOT NULL AND r.block_label <> ''
GROUP BY r.block_label, r.ward;

-- Mowing, 2026 season retrospective: rotation parcels and the longest gap between cuts.
-- Season = 1 Apr to 30 Sep (or the ledger's last date if earlier); the gap after the
-- last cut runs to the season end. Posting dates are batched weekly: good to about a week.
CREATE VIEW mowing_gaps AS
WITH a AS (SELECT least(DATE '2026-09-30', ledger_max) AS season_end, ledger_max FROM run_dates),
c AS (SELECT DISTINCT parcel, service_date FROM cuts
      WHERE service_type = 'Grass Maint' AND service_date >= DATE '2026-04-01'
        AND service_date <= (SELECT season_end FROM a)),
g AS (SELECT parcel, service_date,
             date_diff('day', lag(service_date) OVER (PARTITION BY parcel ORDER BY service_date), service_date) AS gap
      FROM c),
s AS (SELECT parcel, count(*) AS cuts_2026, min(service_date) AS first_cut, max(service_date) AS last_cut,
             max(gap) AS longest_gap_between_cuts FROM g GROUP BY parcel),
req AS (SELECT rp.pid AS parcel, count(*) AS weed_requests_2026, any_value(r.ward) AS ward_from_311
        FROM requests r JOIN request_parcel rp USING (request_id)
        WHERE r.problem_code IN (SELECT problem_code FROM weed_ledger_codes) AND r.init_year = 2026
        GROUP BY rp.pid)
SELECT s.*, date_diff('day', s.last_cut, a.season_end) AS days_from_last_cut_to_season_end,
       greatest(coalesce(s.longest_gap_between_cuts, 0), date_diff('day', s.last_cut, a.season_end)) AS longest_gap_incl_open,
       coalesce(req.weed_requests_2026, 0) AS weed_requests_2026,
       (s.parcel IN (SELECT parcel_id FROM lra)) AS is_lra,
       coalesce(lpad(CAST((SELECT max(l.ward) FROM lra l WHERE l.parcel_id = s.parcel) AS VARCHAR), 2, '0'), req.ward_from_311) AS ward
FROM s CROSS JOIN a LEFT JOIN req USING (parcel);

-- ------------------------------------------------------------------ the receipt
CREATE VIEW receipt_base AS
SELECT r.request_id, r.problem_code, r.type_name, r.family, r.grp AS service_group, r.division AS division,
       r.ward, r.neighborhood, r.channel_group,
       r.block_label AS public_address,
       'block' AS address_level,
       coalesce(rp.is_lra, false) AS is_lra,
       rp.method AS parcel_match_method,
       r.ts_init AS filed, r.ts_promised AS promised, r.promise_days, r.ts_invt_done AS investigation_done,
       r.ts_closed AS closed, r.ts_cancelled AS cancelled, r.status, r.status_group,
       r.resolution_public AS closed_with_words, r.closure_class, r.class_source, r.days_to_close,
       p.closed_by_promise, p.done_by_promise, p.days_vs_promise,
       lf.cuts_prev30 AS ledger_cuts_30d_before, lf.last_cut_before AS ledger_last_cut_before,
       lf.first_cut_after AS ledger_first_cut_after, lf.days_to_first_cut AS ledger_days_to_first_cut,
       lf.cut_dates_in_year AS ledger_cut_dates_same_year, lf.no_cut_in_season AS ledger_no_cut_in_season,
       lf.cut_within_30 AS ledger_cut_within_30, lf.cut_within_60 AS ledger_cut_within_60, lf.ledger_max,
       ws.n_wo AS work_orders_nearby, ws.work_orders,
       rf.next_id AS next_same_request_id, rf.next_init AS next_same_request_filed, rf.days_to_next AS days_to_next_same_request,
       (r.request_id IN (SELECT request_id FROM cw_potholes)) AS in_cityworks_pothole_sample,
       (r.problem_code IN (SELECT problem_code FROM sensitive_codes)) AS sensitive
FROM v_requests r
LEFT JOIN request_parcel rp USING (request_id)
LEFT JOIN promise p USING (request_id)
LEFT JOIN request_ledger_flags lf USING (request_id)
LEFT JOIN request_wo_summary ws USING (request_id)
LEFT JOIN refiled_next rf USING (request_id);

CREATE MACRO receipt(rid) AS TABLE SELECT * FROM receipt_base WHERE request_id = rid;

-- Parcel-level companion, for the city's own use inside the database only.
-- Never exported to build/out/ or the site (Jack's ruling, 13 Oct: blocks, not properties).
CREATE VIEW receipt_private AS
SELECT r.request_id, r.addr_norm AS exact_address, rp.pid AS parcel_id, rp.method AS parcel_match_method,
       rp.n_candidates, rp.is_lra
FROM requests r LEFT JOIN request_parcel rp USING (request_id);
