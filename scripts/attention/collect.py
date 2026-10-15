"""Collectors for the attention-over-time thread (prompt D).

Each collector pulls headline-level records only (headline, date, outlet, URL,
short snippet) and writes JSONL plus a manifest under data/raw/attention/<source>/.
No full article text is requested or stored. No logins, no accounts.

Usage: python3 -I collect.py <source> <out_root>
"""
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (research; stl-civic-hackathon)"
START = dt.date(2024, 10, 1)
END = dt.date(2026, 10, 13)
SNIP = 240


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url, retries=5, pause=2.0, timeout=60, want_headers=False):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                return (body, dict(r.headers)) if want_headers else body
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (400, 401, 403, 404):
                break
            if e.code == 429:  # site asked us to slow down: wait, then retry
                time.sleep(45 * (i + 1))
        except Exception as e:  # timeouts, resets
            last = repr(e)
        time.sleep(pause * (i + 1))
    raise RuntimeError(f"{last} for {url}")


def clean(s, n=SNIP):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n]


class Out:
    def __init__(self, root, source, meta):
        self.dir = os.path.join(root, source)
        os.makedirs(self.dir, exist_ok=True)
        self.path = os.path.join(self.dir, "items.jsonl")
        self.f = open(self.path, "w", encoding="utf-8")
        self.n = 0
        self.dates = []
        self.meta = dict(meta, source=source, started=now(), errors=[], requests=0)

    def write(self, row):
        self.f.write(json.dumps(row, ensure_ascii=False) + "\n")
        self.n += 1
        if row.get("date"):
            self.dates.append(row["date"][:10])
        if self.n % 100 == 0:
            self.f.flush()

    def close(self):
        self.f.close()
        self.meta.update(
            finished=now(), rows=self.n,
            date_min=min(self.dates) if self.dates else None,
            date_max=max(self.dates) if self.dates else None,
        )
        with open(os.path.join(self.dir, "manifest.json"), "w") as m:
            json.dump(self.meta, m, indent=1)
        print(json.dumps({k: self.meta[k] for k in ("source", "rows", "date_min", "date_max", "requests")}),
              "errors:", len(self.meta["errors"]))


def wp(root, source, base, extra="", kind="news"):
    """WordPress REST API: public posts endpoint, excerpt only."""
    url0 = (f"{base}/wp-json/wp/v2/posts?per_page=100&orderby=date&order=asc"
            f"&after={START}T00:00:00&_fields=id,date_gmt,link,title,excerpt,categories{extra}")
    out = Out(root, source, {"url_pattern": url0 + "&page=N", "kind": kind})
    try:
        cats = {}
        for p in range(1, 4):
            c = json.loads(get(f"{base}/wp-json/wp/v2/categories?per_page=100&page={p}&_fields=id,slug"))
            cats.update({x["id"]: x["slug"] for x in c})
            if len(c) < 100:
                break
    except Exception as e:
        cats = {}
        out.meta["errors"].append(f"categories: {e}")
    page = 1
    while True:
        try:
            body, hdr = get(f"{url0}&page={page}", want_headers=True)
        except Exception as e:
            out.meta["errors"].append(str(e))
            break
        out.meta["requests"] += 1
        rows = json.loads(body)
        out.meta["api_total"] = hdr.get("X-WP-Total") or hdr.get("x-wp-total")
        for r in rows:
            out.write({
                "source": source, "id": r["id"], "date": r["date_gmt"] + "Z",
                "title": clean(r["title"]["rendered"], 400), "url": r["link"],
                "snippet": clean(r.get("excerpt", {}).get("rendered", "")),
                "section": "|".join(cats.get(c, str(c)) for c in r.get("categories", [])),
            })
        if len(rows) < 100:
            break
        page += 1
        time.sleep(0.4)
    out.close()


def stlpr(root):
    """St. Louis Public Radio monthly sitemaps: URL + date in path; title from slug."""
    out = Out(root, "stlpr", {"url_pattern": "https://www.stlpr.org/sitemap-YYYYMM.xml", "kind": "news",
                             "note": "title is derived from the URL slug, not the published headline; no snippet"})
    y, m = START.year, START.month
    pat = re.compile(r"<loc>(https://www\.stlpr\.org/([a-z0-9-]+(?:/[a-z0-9-]+)?)/(\d{4}-\d{2}-\d{2})/([^<]+))</loc>")
    seen = set()
    while (y, m) <= (END.year, END.month):
        try:
            t = get(f"https://www.stlpr.org/sitemap-{y}{m:02d}.xml").decode("utf-8", "replace")
            out.meta["requests"] += 1
            for url, section, d, slug in pat.findall(t):
                if url in seen or not (str(START) <= d <= str(END)):
                    continue
                seen.add(url)
                out.write({"source": "stlpr", "id": url, "date": d, "title": slug.replace("-", " "),
                           "url": url, "snippet": "", "section": section})
        except Exception as e:
            out.meta["errors"].append(str(e))
        y, m = (y, m + 1) if m < 12 else (y + 1, 1)
        time.sleep(0.5)
    out.close()


def stltoday(root, source, section):
    """Post-Dispatch public search feed in RSS form (title, description, pubDate, link).
    The JSON form of the same feed returns full article bodies and is deliberately not used.
    The site answers HTTP 429 after short bursts, so requests are paced and a 429 means a long wait."""
    base = ("https://www.stltoday.com/search/?f=rss&t=article&l=100&s=start_time&sd=asc"
            f"&c[]={urllib.parse.quote(section)}")
    out = Out(root, source, {"url_pattern": base + "&d1=YYYY-MM-DD&d2=YYYY-MM-DD&o=N", "kind": "news",
                             "throttled_429": 0})
    seen = set()
    d = START
    item = re.compile(r"<item>(.*?)</item>", re.S)
    delay = [10.0]

    def tag(x, name):
        mm = re.search(rf"<{name}[^>]*>(.*?)</{name}>", x, re.S)
        return mm.group(1) if mm else ""

    def fetch(url):
        for attempt in range(8):
            time.sleep(delay[0])
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    return r.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    out.meta["throttled_429"] += 1
                    delay[0] = min(delay[0] * 1.5, 60)
                    print("429; waiting 10 min; delay now", delay[0], flush=True)
                    time.sleep(600)
                else:
                    print("HTTP", e.code, flush=True)
            except Exception as e:
                print("ERR", repr(e), flush=True)
        raise RuntimeError("gave up: " + url)

    while d <= END:
        d2 = min(d + dt.timedelta(days=6), END)
        o = 0
        while True:
            try:
                t = fetch(f"{base}&d1={d}&d2={d2}&o={o}")
            except Exception as e:
                out.meta["errors"].append(str(e))
                break
            out.meta["requests"] += 1
            items = item.findall(t)
            for x in items:
                url = html.unescape(tag(x, "link")).strip()
                if not url or url in seen:
                    continue
                seen.add(url)
                try:
                    pd = dt.datetime.strptime(tag(x, "pubDate").strip(), "%a, %d %b %Y %H:%M:%S %z")
                    date = pd.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    date = str(d)
                path = urllib.parse.urlparse(url).path.strip("/").split("/")
                out.write({"source": source, "id": url, "date": date,
                           "title": clean(re.sub(r"<!\[CDATA\[|\]\]>", "", tag(x, "title")), 400), "url": url,
                           "snippet": clean(re.sub(r"<!\[CDATA\[|\]\]>", "", tag(x, "description"))),
                           "section": "/".join(path[:-1])})
            print(d, o, len(items), out.n, flush=True)
            if len(items) < 100:
                break
            o += 100
        d = d2 + dt.timedelta(days=1)
    out.close()


def reddit(root):
    """r/StLouis submissions via the Arctic Shift third-party archive (reddit.com itself was not queried)."""
    base = ("https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=StLouis&limit=auto&sort=asc"
            "&fields=id,created_utc,title,score,num_comments,link_flair_text,selftext,url")
    out = Out(root, "reddit_stlouis", {"url_pattern": base + "&after=EPOCH", "kind": "community",
                                       "note": "third-party archive; selftext truncated to a snippet before saving"})
    after = int(dt.datetime(START.year, START.month, START.day, tzinfo=dt.timezone.utc).timestamp())
    stop = int(dt.datetime(END.year, END.month, END.day, 23, 59, tzinfo=dt.timezone.utc).timestamp())
    seen = set()
    while after < stop:
        try:
            rows = json.loads(get(f"{base}&after={after}")).get("data") or []
        except Exception as e:
            out.meta["errors"].append(str(e))
            break
        out.meta["requests"] += 1
        new = 0
        for r in rows:
            if r["id"] in seen or r["created_utc"] > stop:
                continue
            seen.add(r["id"])
            new += 1
            st = r.get("selftext") or ""
            out.write({
                "source": "reddit_stlouis", "id": r["id"],
                "date": dt.datetime.fromtimestamp(r["created_utc"], dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "title": clean(r.get("title"), 400), "url": f"https://www.reddit.com/r/StLouis/comments/{r['id']}/",
                "snippet": "" if st in ("[removed]", "[deleted]") else clean(st),
                "section": r.get("link_flair_text") or "", "score": r.get("score"),
                "num_comments": r.get("num_comments"), "removed": st in ("[removed]", "[deleted]"),
            })
        if not rows or new == 0:
            break
        after = max(r["created_utc"] for r in rows)
        time.sleep(0.6)
    out.close()


def gdelt(root, source, domain):
    """GDELT DOC 2.0 article list for one outlet domain, weekly windows, >=8 s apart."""
    q = urllib.parse.quote(f'domain:{domain} "st. louis"')
    base = f"https://api.gdeltproject.org/api/v2/doc/doc?query={q}&mode=artlist&maxrecords=250&format=json&sort=datedesc"
    out = Out(root, source, {"url_pattern": base + "&startdatetime=..&enddatetime=..", "kind": "news",
                             "note": "titles are GDELT machine-extracted; window counts in windows[]", "windows": []})
    seen = set()
    d = START
    while d <= END:
        d2 = min(d + dt.timedelta(days=7), END + dt.timedelta(days=1))
        url = f"{base}&startdatetime={d:%Y%m%d}000000&enddatetime={d2:%Y%m%d}000000"
        arts = None
        time.sleep(12)
        try:
            body = get(url, retries=3).decode("utf-8", "replace")
            out.meta["requests"] += 1
            arts = json.loads(body).get("articles", []) if body.strip().startswith("{") else None
        except Exception as e:
            print(d, "ERR", e, flush=True)
        if arts is None:
            out.meta["errors"].append(f"{d}: no data")
        else:
            out.meta["windows"].append([str(d), len(arts)])
            print(d, len(arts), flush=True)
            for a in arts:
                if a["url"] in seen:
                    continue
                seen.add(a["url"])
                s = a["seendate"]
                out.write({"source": source, "id": a["url"], "date": f"{s[:4]}-{s[4:6]}-{s[6:8]}T{s[9:11]}:{s[11:13]}:00Z",
                           "title": clean(a.get("title"), 400), "url": a["url"], "snippet": "",
                           "section": "/".join(urllib.parse.urlparse(a["url"]).path.strip("/").split("/")[:3])})
        d = d2
    out.close()


def boa(root):
    """Board of Aldermen board bills: session listings then each bill page (title, summary, intro date)."""
    base = "https://www.stlouis-mo.gov/government/city-laws/board-bills/"
    out = Out(root, "boa_bills", {"url_pattern": base + "index.cfm?sessionBB=SESSION and boardbill.cfm?bbDetail=true&BBId=N",
                                 "kind": "public_meeting"})
    for session in ("2024-2025", "2025-2026", "2026-2027"):
        try:
            t = get(f"{base}index.cfm?sessionBB={session}").decode("utf-8", "replace")
            out.meta["requests"] += 1
        except Exception as e:
            out.meta["errors"].append(str(e))
            continue
        bills = re.findall(r'boardbill\.cfm\?bbDetail=true&(?:amp;)?BBId=(\d+)">\s*BB\s*([\w.]+)\s*</a>\s*<br>\s*([^<]*)', t)
        out.meta[f"listed_{session}"] = len(bills)
        for bbid, num, title in bills:
            url = f"{base}boardbill.cfm?bbDetail=true&BBId={bbid}"
            try:
                p = get(url).decode("utf-8", "replace")
                out.meta["requests"] += 1
            except Exception as e:
                out.meta["errors"].append(str(e))
                continue
            p = re.sub(r"<script.*?</script>|<style.*?</style>", "", p, flags=re.S)
            txt = clean(p, 10 ** 6)
            m = re.search(r"Introduced:\s*(\d{2})/(\d{2})/(\d{4})", txt)
            s = re.search(r"Summary\s+(.*?)\s+(?:Download|Overview)", txt)
            c = re.search(r"assigned to the\s+(.*?Committee)", txt)
            if not m:
                out.meta["errors"].append(f"no intro date BBId={bbid}")
                continue
            out.write({"source": "boa_bills", "id": f"{session}/BB{num}", "date": f"{m.group(3)}-{m.group(1)}-{m.group(2)}",
                       "title": clean(title, 400), "url": url, "snippet": clean(s.group(1)) if s else "",
                       "section": c.group(1) if c else "", "session": session})
            time.sleep(0.25)
    out.close()


if __name__ == "__main__":
    src, root = sys.argv[1], sys.argv[2]
    if src == "fox2":
        wp(root, "fox2", "https://fox2now.com", "&categories=28577,426060346,18079722")
    elif src == "stlamerican":
        wp(root, "stlamerican", "https://www.stlamerican.com")
    elif src == "nextstl":
        wp(root, "nextstl", "https://nextstl.com")
    elif src == "stlpr":
        stlpr(root)
    elif src == "stltoday_local":
        stltoday(root, "stltoday_local", "news/local*")
    elif src == "stltoday_opinion":
        stltoday(root, "stltoday_opinion", "opinion*")
    elif src == "reddit":
        reddit(root)
    elif src == "gdelt_ksdk":
        gdelt(root, "gdelt_ksdk", "ksdk.com")
    elif src == "gdelt_kmov":
        gdelt(root, "gdelt_kmov", "firstalert4.com")
    elif src == "boa":
        boa(root)
    else:
        sys.exit("unknown source")
