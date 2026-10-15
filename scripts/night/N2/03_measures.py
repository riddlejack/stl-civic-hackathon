"""N2 step 3: closure-class measures per type and per division, and headline candidates.

Scope: requests filed 2025-01-01 .. 2026-10-12 (complete days) with STATUS = CLOSED,
from build/N2/private/csb_2024_2026.parquet (has addresses; not for publication). Class from classes.classify().
Days to close = (DATETIMECLOSED - DATETIMEINIT) in days.
Promise = PRJCOMPLETEDATE (the city's per-request promised completion date).
"By promise" = closed at or before PRJCOMPLETEDATE (rows with a promise only).
"Within one day" = closed <= 1.0 day after filing.

Outputs (build/N2/):
  closed_classed.parquet   one row per closed request with class (no address)
  by_type_class.csv        PROBLEMCODE x class measures
  by_type_wide.csv         one row per PROBLEMCODE: class shares, medians, promise
  by_division_class.csv    division x class measures
  headline.json            the headline candidates
Run: .venv/bin/python -I scripts/night/N2/03_measures.py
"""
import json, pathlib, sys
import duckdb

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from classes import classify, CLASSES  # noqa: E402

ROOT = HERE.parents[2]
B = ROOT / "build" / "N2"
P = B / "private" / "csb_2024_2026.parquet"
START, END = "2025-01-01", "2026-10-13"   # filed on or after START, before END

con = duckdb.connect()
pairs = con.execute(f"""SELECT DISTINCT PROBLEMCODE, PUBLICRESOLUTION FROM '{P}' WHERE STATUS='CLOSED'""").fetchall()
cls_rows = [(pc, txt, *classify(pc, txt)) for pc, txt in pairs]
con.execute("CREATE TABLE cls (PROBLEMCODE VARCHAR, PUBLICRESOLUTION VARCHAR, class VARCHAR, rule VARCHAR)")
con.executemany("INSERT INTO cls VALUES (?,?,?,?)", cls_rows)

con.execute(f"""
CREATE TABLE cc AS
SELECT r.REQUESTID, r.PROBLEMCODE, r.PLAIN_NAME, r.n_rows, r.channel,
  r.SUBMITTO,
  r.WARD, r.t_init, r.t_closed, r.t_promise, r.t_invdone,
  coalesce(trim(r.PUBLICRESOLUTION), '') AS resolution_text,
  c.class, c.rule,
  (epoch(r.t_closed) - epoch(r.t_init)) / 86400.0 AS days,
  (epoch(r.t_promise) - epoch(r.t_init)) / 86400.0 AS promise_days,
  (epoch(r.t_promise) - epoch(r.t_closed)) / 86400.0 AS days_left_at_close
FROM '{P}' r
JOIN cls c ON c.PROBLEMCODE = r.PROBLEMCODE AND c.PUBLICRESOLUTION IS NOT DISTINCT FROM r.PUBLICRESOLUTION
WHERE r.STATUS = 'CLOSED' AND r.t_init >= TIMESTAMP '{START}' AND r.t_init < TIMESTAMP '{END}'
""")
# division: SUBMITTO without trailing number; small divisions (<50 closures) pooled as OTHER
con.execute("""
CREATE TABLE divmap AS
WITH d AS (SELECT SUBMITTO, trim(regexp_replace(regexp_replace(coalesce(SUBMITTO,'(none)'), ',\\s*\\d*\\s*$', ''), ',$', '')) AS division,
                  count(*) n FROM cc GROUP BY 1)
SELECT SUBMITTO, CASE WHEN sum(n) OVER (PARTITION BY division) >= 50 THEN division ELSE 'OTHER (small)' END AS division FROM d
""")
con.execute("ALTER TABLE cc ADD COLUMN division VARCHAR")
con.execute("UPDATE cc SET division = d.division FROM divmap d WHERE cc.SUBMITTO IS NOT DISTINCT FROM d.SUBMITTO")
con.execute("ALTER TABLE cc DROP COLUMN SUBMITTO")
con.execute(f"COPY cc TO '{B/'closed_classed.parquet'}' (FORMAT parquet)")

def measures(group_cols):
    g = ", ".join(group_cols)
    return f"""
    WITH base AS (SELECT * FROM cc),
    grp AS (SELECT {g}, count(*) AS grp_n FROM base GROUP BY {g})
    SELECT {g}, class, count(*) AS n, round(count(*) / any_value(grp_n), 4) AS share,
      round(median(days), 2) AS median_days,
      round(avg(CASE WHEN t_promise IS NOT NULL THEN (t_closed <= t_promise)::INT END), 4) AS share_closed_by_promise,
      round(avg((days <= 1.0)::INT), 4) AS share_within_1_day,
      round(median(promise_days), 1) AS median_promise_days,
      round(median(days_left_at_close), 1) AS median_days_left_at_close,
      round(avg((t_promise IS NOT NULL)::INT), 4) AS share_with_promise
    FROM base JOIN grp USING ({g})
    GROUP BY {g}, class
    ORDER BY any_value(grp_n) DESC, {g}, n DESC
    """

con.execute(f"COPY ({measures(['PROBLEMCODE'])}) TO '{B/'by_type_class.csv'}' (HEADER)")
con.execute(f"COPY ({measures(['division'])}) TO '{B/'by_division_class.csv'}' (HEADER)")
con.execute(f"COPY ({measures(['division', 'PROBLEMCODE'])}) TO '{B/'by_division_type_class.csv'}' (HEADER)")

# wide per-type table
shares = ", ".join(f"round(avg((class='{c}')::INT),4) AS share_{c}" for c in CLASSES)
con.execute(f"""
COPY (
SELECT PROBLEMCODE, any_value(PLAIN_NAME) AS plain_name, mode(division) AS division, count(*) AS n_closed,
  round(avg((channel='resident')::INT),3) AS share_resident,
  {shares},
  round(avg((class IN ('handed_off','converted'))::INT),4) AS share_handoff_or_converted,
  round(avg((class='handed_off' AND rule<>'handed_off:enforcement')::INT),4) AS share_handoff_excl_enforcement,
  round(median(days),2) AS median_days_all,
  round(median(days) FILTER (WHERE class='done'),2) AS median_days_done,
  round(median(days) FILTER (WHERE class='handed_off'),2) AS median_days_handed_off,
  round(median(promise_days),1) AS median_promise_days,
  round(avg(CASE WHEN t_promise IS NOT NULL THEN (t_closed<=t_promise)::INT END),4) AS share_closed_by_promise,
  round(avg(CASE WHEN t_promise IS NOT NULL THEN (class='done' AND t_closed<=t_promise)::INT END),4) AS share_done_by_promise_of_closed,
  round(avg(CASE WHEN t_promise IS NOT NULL AND t_closed<=t_promise THEN (class IN ('handed_off','converted'))::INT END),4) AS handoff_share_of_on_time_closures,
  mode(resolution_text) AS top_text
FROM cc GROUP BY PROBLEMCODE ORDER BY n_closed DESC
) TO '{B/'by_type_wide.csv'}' (HEADER)""")

H = {}
def q1(sql):
    return con.execute(sql).fetchone()

H["scope"] = f"requests filed {START} to 2026-10-12 with STATUS CLOSED, from the city's 311 file (csb.zip, cleaned copy)"
H["n_closed"] = q1("SELECT count(*) FROM cc")[0]
for scope, where in [("all", "TRUE"), ("resident", "channel='resident'"), ("staff", "channel='staff'"),
                     ("excl_logging_only_public_nuisance", "PROBLEMCODE<>'Public Nuisance Rpt'")]:
    row = con.execute(f"""SELECT count(*),
        {', '.join(f"avg((class='{c}')::INT)" for c in CLASSES)},
        avg((class IN ('handed_off','converted'))::INT),
        avg((class='handed_off' AND rule<>'handed_off:enforcement')::INT) + avg((class='converted')::INT),
        avg((rule='handed_off:enforcement')::INT)
      FROM cc WHERE {where}""").fetchone()
    d = {"n": row[0]}
    for i, c in enumerate(CLASSES):
        d[f"share_{c}"] = round(row[1 + i], 4)
    d["share_handoff_or_converted"] = round(row[7], 4)
    d["share_handoff_or_converted_excl_enforcement"] = round(row[8], 4)
    d["share_enforcement_notice"] = round(row[9], 4)
    # of closures that state an outcome about the work (done, handed_off, converted)
    d["handoff_or_converted_share_of_done_handoff_converted"] = round(row[7] / (row[1] + row[7]), 4)
    H[f"mix_{scope}"] = d

# share of on-time (by promise) closures that are hand-offs
H["on_time_closures"] = dict(zip(
    ["n_on_time", "share_handoff_or_converted", "share_done", "share_no_action"],
    [round(x, 4) if isinstance(x, float) else x for x in q1("""
      SELECT count(*), avg((class IN ('handed_off','converted'))::INT), avg((class='done')::INT), avg((class='no_action')::INT)
      FROM cc WHERE t_promise IS NOT NULL AND t_closed <= t_promise""")]))

# hand-off closures closed before their promise date
H["handoff_before_promise"] = dict(zip(
    ["n_handoff_with_promise", "share_closed_before_promise", "median_days_to_close", "median_days_left_at_close"],
    [round(x, 4) if isinstance(x, float) else x for x in q1("""
      SELECT count(*), avg((t_closed <= t_promise)::INT), median(days), median(days_left_at_close)
      FROM cc WHERE class IN ('handed_off','converted') AND t_promise IS NOT NULL""")]))

# high-volume types that are mostly hand-offs
H["mostly_handoff_types"] = [dict(zip(["PROBLEMCODE", "n_closed", "share_handoff_or_converted", "top_text"], r)) for r in con.execute("""
  SELECT PROBLEMCODE, count(*) n, round(avg((class IN ('handed_off','converted'))::INT),3) s, mode(resolution_text)
  FROM cc GROUP BY 1 HAVING count(*) >= 500 AND avg((class IN ('handed_off','converted'))::INT) >= 0.5 ORDER BY n DESC""").fetchall()]

(B / "headline.json").write_text(json.dumps(H, indent=2, default=str))
print(json.dumps(H, indent=2, default=str))
