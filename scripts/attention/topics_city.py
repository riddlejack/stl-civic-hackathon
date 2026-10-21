"""Second topic pass: only items whose text names the City of St. Louis or a city institution,
with sports, weather forecasts and single-crime incident reports screened out, so that smaller
civic themes are not drowned. Usage: python -I topics_city.py <items.jsonl> <k>"""
import json, re, sys, random
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.decomposition import NMF
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
k = int(sys.argv[2])
CITY = re.compile(r"\b(st\.? ?louis(?! county| cardinals| blues| city sc| battlehawks| zoo| area)|stl\b|city hall|alderm[ae]n|alderwoman|alderperson|mayor|slmpd|slps|city of st|north city|south city|downtown|comptroller|citizens.? service|csb|refuse|forestry|lra\b|land reutilization|sldc|city justice center|workhouse)", re.I)
NOISE = re.compile(r"\b(cardinals|blues|battlehawks|city sc|chiefs|mizzou|billikens|inning|homer|playoff|forecast|charged|sentenced|pleads|shot|shooting|homicide|killed|stabb|crash|robbery|carjack|missing|endangered|recipe|restaurant|concert|festival|tickets)\b", re.I)
sel = []
for r in rows:
    t = r["title"] + " " + r.get("snippet", "")[:160]
    if r["source_kind"] == "legislative" or (CITY.search(t) and not NOISE.search(t)):
        sel.append(r)
docs = [(r["title"] + " " + r.get("snippet", "")[:160]).lower() for r in sel]
stop = list(ENGLISH_STOP_WORDS | {"st", "louis", "missouri", "stl", "saint", "says", "say", "new", "amp", "area", "city",
                                  "just", "like", "know", "does", "anyone", "looking", "https", "com", "www", "ve", "don",
                                  "got", "today", "year", "years", "mayor", "downtown"})
vec = TfidfVectorizer(stop_words=stop, ngram_range=(1, 2), min_df=5, max_df=0.15, sublinear_tf=True)
X = vec.fit_transform(docs)
nmf = NMF(n_components=k, random_state=3, init="nndsvd", max_iter=300)
W = nmf.fit_transform(X)
terms = vec.get_feature_names_out(); top = W.argmax(axis=1); st = W.max(axis=1)
random.seed(5)
import collections
print("selected", len(sel), collections.Counter(r["source"] for r in sel))
for t in range(k):
    idx = [i for i in range(len(docs)) if top[i] == t and st[i] > 0]
    print(f"\nC{t:02d} n={len(idx)} | " + ", ".join(terms[j] for j in nmf.components_[t].argsort()[::-1][:11]))
    best = sorted(idx, key=lambda i: -st[i])[:30]
    for i in random.sample(best, min(3, len(best))):
        print("     -", sel[i]["source"][:6], sel[i]["date"], sel[i]["title"][:95])
