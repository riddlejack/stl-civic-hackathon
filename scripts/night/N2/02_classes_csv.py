"""N2 step 2: write research/chapters/N2-closure-classes.csv.

One row per (PROBLEMCODE, closing text) seen on CLOSED requests initiated
2024-01-01 .. 2026-10-13, with its class and the rule or judgement used.
resolution_text is trim(PUBLICRESOLUTION) as in the city's file (internal
spacing kept; staff e-mail addresses removed). Blank closures appear with
resolution_text = "" and class blank.

Join advice for N1: classify(PROBLEMCODE, PUBLICRESOLUTION) in classes.py is
the source of truth and covers other years; this CSV is its output for
2024-2026. For a SQL join use trim(PUBLICRESOLUTION) = resolution_text, and
fall back to a text-only match (scripts/night/N2/text-classes in build/N2/)
for types/texts not listed.

Run: .venv/bin/python -I scripts/night/N2/02_classes_csv.py
"""
import csv, pathlib, sys
import duckdb

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from classes import classify, redact, norm, CLASSES  # noqa: E402

ROOT = HERE.parents[2]
P = ROOT / "build" / "N2" / "private" / "csb_2024_2026.parquet"
OUT = ROOT / "research" / "chapters" / "N2-closure-classes.csv"
OUT_TEXT = ROOT / "build" / "N2" / "text-classes.csv"

con = duckdb.connect()
rows = con.execute(f"""
  WITH c AS (SELECT PROBLEMCODE, coalesce(trim(PUBLICRESOLUTION), '') AS txt
             FROM '{P}' WHERE STATUS = 'CLOSED'),
       t AS (SELECT PROBLEMCODE, count(*) AS type_n FROM c GROUP BY 1)
  SELECT c.PROBLEMCODE, txt, count(*) AS n, any_value(type_n) AS type_n
  FROM c JOIN t USING (PROBLEMCODE)
  GROUP BY 1, 2
  ORDER BY type_n DESC, c.PROBLEMCODE, n DESC
""").fetchall()

out = []
unlisted = {}
for pc, txt, n, type_n in rows:
    cls, rule = classify(pc, txt)
    if "unlisted" in rule:
        unlisted[txt] = unlisted.get(txt, 0) + n
    out.append({
        "PROBLEMCODE": pc,
        "resolution_text": redact(txt),
        "class": cls,
        "n": n,
        "rule_or_judgement": rule + ("" if type_n >= 100 else "; type has <100 closures 2024-26"),
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["PROBLEMCODE", "resolution_text", "class", "n", "rule_or_judgement"])
    w.writeheader()
    w.writerows(out)

# text-only fallback table (for other years / unseen types): normalised text -> class
from classes import TEXT_RULES  # noqa: E402
with open(OUT_TEXT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["resolution_text_normalised", "class", "rule"])
    for t, (c, r) in sorted(TEXT_RULES.items()):
        w.writerow([t, c, r])

tot = sum(r["n"] for r in out)
by = {}
for r in out:
    by[r["class"]] = by.get(r["class"], 0) + r["n"]
print(f"rows written: {len(out)}; closures covered: {tot}")
for c in CLASSES:
    print(f"  {c:11s} {by.get(c,0):7d} {by.get(c,0)/tot:6.1%}")
print("unlisted texts:", len(unlisted), sum(unlisted.values()))
for t, n in sorted(unlisted.items(), key=lambda x: -x[1])[:40]:
    print(f"   {n:6d}  {t!r}")
