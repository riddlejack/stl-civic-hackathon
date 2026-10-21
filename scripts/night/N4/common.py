"""Shared setup for N4 scripts: DuckDB view `c` over the 2023-2026 parquet built by 00_load.py.

Definitions (T-COMMON): resident channels = WEB, PHONE, EMAIL, CHAT, TWITTER, LETTER;
staff = NSO. Closed = STATUS CLOSED with DATETIMECLOSED. Days = fractional calendar days.
Business days = weekdays (Mon-Fri) after the init date up to and including the close date;
no holiday calendar (the city's is not published in the file).
"""
import duckdb, json, os
ROOT = '.'
P = f'{ROOT}/build/N4/csb_2023_2026.parquet'
OUT = f'{ROOT}/build/N4'
RES = "('WEB','PHONE','EMAIL','CHAT','TWITTER','LETTER')"


def connect():
    con = duckdb.connect()
    con.execute("""
    CREATE TABLE cal AS
    SELECT CAST(d AS DATE) AS d,
           sum(CASE WHEN isodow(d) <= 5 THEN 1 ELSE 0 END) OVER (ORDER BY d) AS bidx
    FROM range(DATE '2022-01-01', DATE '2028-01-01', INTERVAL 1 DAY) r(d)
    """)
    con.execute(f"""
    CREATE VIEW c AS SELECT x.*,
      trim(x.problemcode) AS pc,
      year(x.t_init) || ' Q' || quarter(x.t_init) AS q_init,
      year(x.t_closed) || ' Q' || quarter(x.t_closed) AS q_closed,
      epoch(x.t_closed - x.t_init) / 86400.0 AS days,
      date_diff('day', CAST(x.t_init AS DATE), CAST(x.t_closed AS DATE)) AS cdays,
      epoch(x.t_promise - x.t_init) / 86400.0 AS promise_days,
      ci2.bidx - ci1.bidx AS bdays
    FROM '{P}' x
    LEFT JOIN cal ci1 ON ci1.d = CAST(x.t_init AS DATE)
    LEFT JOIN cal ci2 ON ci2.d = CAST(x.t_closed AS DATE)
    """)
    return con


def show(con, sql, n=200):
    rel = con.sql(sql)
    cols = rel.columns
    rows = rel.fetchall()
    w = [max([len(str(c))] + [len(fmt(r[i])) for r in rows[:n]]) for i, c in enumerate(cols)]
    print(' | '.join(str(c).ljust(w[i]) for i, c in enumerate(cols)))
    for r in rows[:n]:
        print(' | '.join(fmt(v).ljust(w[i]) for i, v in enumerate(r)))
    if len(rows) > n:
        print(f'... {len(rows)} rows')
    return cols, rows


def fmt(v):
    if isinstance(v, float):
        return f'{v:.4f}'
    return str(v)
