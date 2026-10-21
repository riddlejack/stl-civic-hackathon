"""Merge raw attention pulls into one de-duplicated item file.

Usage: python3 -I merge.py <raw_root> <out_jsonl>
Writes one JSON line per item: source, source_kind, id, date, month, title, snippet, url, section,
plus reddit score/num_comments where present. Prints a per-source drop report.
"""
import collections
import json
import os
import re
import sys

START, END = "2024-10-01", "2026-10-13"
KIND = {
    "fox2": "news", "stlamerican": "news", "stlpr": "news", "nextstl": "news", "stltoday_local": "news",
    "stltoday_opinion": "opinion_letters", "reddit_stlouis": "community_forum", "boa_bills": "legislative",
}
# Sections that are not local reporting at all (national wire, listings, promos).
DROP_SECTION = {
    "stlpr": re.compile(r"^(npr|job-listing|job-posting|podcast/meet-me)$"),
    "stltoday_local": re.compile(r"brandavestudios|obituaries"),
}


def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def main(root, out_path):
    report = collections.OrderedDict()
    out = open(out_path, "w", encoding="utf-8")
    for src, kind in KIND.items():
        p = os.path.join(root, src, "items.jsonl")
        if not os.path.exists(p):
            continue
        rep = collections.Counter()
        seen_id, seen_title = set(), set()
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            rep["raw"] += 1
            d = r["date"][:10]
            if not (START <= d <= END):
                rep["out_of_window"] += 1
                continue
            if src in DROP_SECTION and DROP_SECTION[src].search(r.get("section", "")):
                rep["dropped_section"] += 1
                continue
            if r.get("removed") and not r.get("title"):
                rep["empty"] += 1
                continue
            if r["id"] in seen_id:
                rep["dup_id"] += 1
                continue
            seen_id.add(r["id"])
            # Same outlet, same normalised headline, same month = a re-post or an updated copy.
            # Board bills are exempt: identical short titles are separate bills.
            key = (norm(r["title"]), d[:7])
            if src != "boa_bills" and len(key[0]) > 15 and key in seen_title:
                rep["dup_title_same_month"] += 1
                continue
            seen_title.add(key)
            rep["kept"] += 1
            row = {"source": src, "source_kind": kind, "id": str(r["id"]), "date": d, "month": d[:7],
                   "title": r["title"], "snippet": r.get("snippet", ""), "url": r["url"],
                   "section": r.get("section", "")}
            for k in ("score", "num_comments", "removed", "session"):
                if k in r:
                    row[k] = r[k]
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
        report[src] = dict(rep)
    out.close()
    json.dump(report, open(out_path.replace(".jsonl", "_report.json"), "w"), indent=1)
    for k, v in report.items():
        print(k, v)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
