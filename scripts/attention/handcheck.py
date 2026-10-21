"""Compare hand labels for sample A with the tagger. Usage: python3 -I handcheck.py <derived_dir>"""
import json, sys, collections
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import tag
D = sys.argv[1]
items = json.load(open(f"{D}/handcheck_A_items.json"))
labels = {}
for line in open(f"{D}/handcheck_A_labels.txt"):
    i, iss, sc, kind = line.strip().split("|")
    labels[int(i)] = (set() if iss == "-" else set(iss.split(",")), {"C": "city", "E": "elsewhere", "U": "unstated"}[sc], kind)
tp = fp = fn = 0; any_tp = any_fp = any_fn = any_tn = 0
kind_ok = kind_n = 0; scope = collections.Counter(); miss = []; kinds = collections.Counter()
for i, r in enumerate(items):
    r = tag.tag_row(dict(r)); m = set(r["issues"]); h, hs, hk = labels[i]
    tp += len(m & h); fp += len(m - h); fn += len(h - m)
    if m and h: any_tp += 1
    elif m: any_fp += 1
    elif h: any_fn += 1
    else: any_tn += 1
    if m != h: miss.append((i, r["source"][:5], sorted(h), sorted(m), r["title"][:70]))
    if h:
        kind_n += 1; kind_ok += (hk == r["mention_kind"]); kinds[(hk, r["mention_kind"])] += 1
    if m or h: scope[(hs, r["scope"])] += 1
print(f"items={len(items)} hand-tagged={any_tp+any_fn} machine-tagged={any_tp+any_fp}")
print(f"item level: both={any_tp} machine-only(FP)={any_fp} hand-only(FN)={any_fn} neither={any_tn}")
print(f"tag level: tp={tp} fp={fp} fn={fn} precision={tp/(tp+fp):.2f} recall={tp/(tp+fn):.2f}")
print(f"kind accuracy on hand-tagged items: {kind_ok}/{kind_n}"); print(sorted(kinds.items(), key=lambda x: -x[1]))
print("scope (hand, machine):", sorted(scope.items(), key=lambda x: -x[1]))
for x in miss: print("  DIFF", x)
