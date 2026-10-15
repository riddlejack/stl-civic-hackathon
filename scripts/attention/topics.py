"""Unsupervised topic pass used to derive issue categories from the material (no preset list).

Usage: python -I topics.py <items.jsonl> <group: news|reddit> <k>
Prints each NMF topic's top terms, size and example headlines.
"""
import json
import sys
import random
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.decomposition import NMF

path, group, k = sys.argv[1], sys.argv[2], int(sys.argv[3])
rows = [json.loads(l) for l in open(path, encoding="utf-8")]
if group == "news":
    rows = [r for r in rows if r["source_kind"] in ("news", "opinion_letters")]
else:
    rows = [r for r in rows if r["source_kind"] == "community_forum"]
docs = [(r["title"] + " " + r.get("snippet", "")[:160]).lower() for r in rows]
stop = list(ENGLISH_STOP_WORDS | {"st", "louis", "missouri", "stl", "saint", "says", "say", "new", "amp", "area",
                                  "fox", "ksdk", "just", "like", "know", "does", "anybody", "anyone", "looking",
                                  "https", "com", "www", "reddit", "ve", "don", "got", "today", "year", "years"})
vec = TfidfVectorizer(stop_words=stop, ngram_range=(1, 2), min_df=8, max_df=0.2, sublinear_tf=True)
X = vec.fit_transform(docs)
nmf = NMF(n_components=k, random_state=3, init="nndsvd", max_iter=300)
W = nmf.fit_transform(X)
terms = vec.get_feature_names_out()
top = W.argmax(axis=1)
strength = W.max(axis=1)
random.seed(5)
print(f"docs={len(docs)} vocab={len(terms)} unassigned(zero weight)={(strength == 0).sum()}")
for t in range(k):
    idx = [i for i in range(len(docs)) if top[i] == t and strength[i] > 0]
    words = ", ".join(terms[j] for j in nmf.components_[t].argsort()[::-1][:12])
    print(f"\nT{t:02d} n={len(idx)} | {words}")
    best = sorted(idx, key=lambda i: -strength[i])[:40]
    for i in random.sample(best, min(4, len(best))):
        print("     -", rows[i]["source"][:6], rows[i]["date"], rows[i]["title"][:100])
