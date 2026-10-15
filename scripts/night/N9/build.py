"""N9 build: merge the record of choices and the derivation chains, render the deliverables.

Inputs
  scripts/night/N9/seed_*.py            curated by N9 from project files and transcripts
  scripts/night/N9/merge_overrides.py    manual merge decisions after reviewing the merge log
  build/N*/decisions.json                each night agent's log of deliberate choices
  build/N*/figures.json, build/out/figures.json   the figure registry

Outputs (the only files this script writes)
  build/out/decisions.json
  build/out/derivations.json
  deliverable/choices.md
  deliverable/negative-results.md

Run from the repo root:  .venv/bin/python -I scripts/night/N9/build.py [--log merge-log-path]
Standard library only. Re-runnable: outputs are regenerated from inputs each time.
"""
import datetime as dt
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import seed_decisions  # noqa: E402
import seed_derivations  # noqa: E402
import seed_negatives  # noqa: E402
import seed_plain  # noqa: E402

try:
    import merge_overrides  # noqa: E402
    OVERRIDES = getattr(merge_overrides, "OVERRIDES", {})
    EXTRA_NEGATIVES = getattr(merge_overrides, "EXTRA_NEGATIVES", [])
    AGENT_PLAIN = getattr(merge_overrides, "AGENT_PLAIN", {})
    AGENT_STRENGTH = getattr(merge_overrides, "AGENT_STRENGTH", {})
    AGENT_CATEGORY = getattr(merge_overrides, "AGENT_CATEGORY", {})
    AGENT_STATUS = getattr(merge_overrides, "AGENT_STATUS", {})
    SANITIZE = getattr(merge_overrides, "SANITIZE", [])
    AGENT_TEXT = getattr(merge_overrides, "AGENT_TEXT", {})
except ImportError:
    OVERRIDES, EXTRA_NEGATIVES, AGENT_PLAIN, AGENT_STRENGTH, AGENT_CATEGORY, AGENT_STATUS, SANITIZE = {}, [], {}, {}, {}, {}, []
    AGENT_TEXT = {}

CATEGORIES = ["privacy", "ethics", "adoption", "method", "data source", "correction", "scope", "presentation"]
STRENGTH_ORDER = {"strong": 0, "moderate": 1, "minor": 2}
STOP = set("""a an and are as at be because but by can do does for from has have in into is it its
of on or our over per so than that the their them then there these they this to under up was we
were what when where which while who will with without not no only one all any each every own
also more most other same such very just""".split())


def now_central():
    # Central Daylight Time in October (UTC-5); no tz database needed.
    utc = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    return (utc - dt.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M CDT")


def tokens(text):
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {w for w in words if w not in STOP and len(w) > 2}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def as_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        out = []
        for v in x:
            out.append(v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
        return out
    if isinstance(x, dict):
        return [json.dumps(x, ensure_ascii=False)]
    parts = [p.strip() for p in re.split(r";\s+|\n", str(x)) if p.strip()]
    return parts or [str(x)]


def first(d, *keys):
    for k in keys:
        if k in d and d[k] not in (None, "", []):
            return d[k]
    return None


CAT_RULES = [
    ("privacy", r"\bblock[- ]level|\baddress|personal|owner name|staff (name|field)|privacy|hundred block|private/"),
    ("ethics", r"surveil|perpetrat|encampment|homeless|harm|exposed"),
    ("correction", r"\bcorrect|wrong|inflat|dedup|duplicate|retir|overstat|bug|mistake|fix(ed)?\b|soften"),
    ("adoption", r"policy|itsa|adopt|procure|city (could|can) run|licen[cs]e|cityStat team|sql file|no key"),
    ("data source", r"ledger|layer|dataset|\bfile\b|source|csv|saved search|cityworks|imagery|msdis|sentinel"),
    ("scope", r"\bdrop|out of scope|not built|cut from|excluded? from scope|defer"),
    ("presentation", r"\bsite\b|chart|display|label|video|page|colou?r|wording|headline"),
]


def infer_category(text):
    t = (text or "").lower()
    for cat, rx in CAT_RULES:
        if re.search(rx, t):
            return cat
    return "method"


def norm_category(c, text):
    if not c:
        return infer_category(text)
    c = str(c).strip().lower().replace("_", " ")
    aliases = {"data": "data source", "data-source": "data source", "datasource": "data source",
               "methods": "method", "methodology": "method", "definition": "method", "definitions": "method",
               "analysis": "method", "corrections": "correction", "display": "presentation",
               "design": "presentation", "communication": "presentation", "legal": "adoption",
               "policy": "adoption", "governance": "adoption", "process": "method", "pipeline": "method",
               "engineering": "method", "safety": "ethics"}
    c = aliases.get(c, c)
    return c if c in CATEGORIES else infer_category(text)


def load_agent_decisions():
    found = []
    paths = sorted(glob.glob(os.path.join(ROOT, "build", "N*", "decisions.json")))
    paths += sorted(glob.glob(os.path.join(ROOT, "research", "chapters", "N*-decisions.json")))
    seen_agents = set()
    for path in paths:
        if os.path.basename(path) == "decisions.json":
            agent = os.path.basename(os.path.dirname(path))
        else:
            agent = os.path.basename(path).split("-")[0]
        if agent in ("N9", "N10"):
            continue  # never merge our own output back in; N10's file is a change log of verification fixes, not choices
        if (agent, os.path.basename(path)) in seen_agents:
            continue
        seen_agents.add((agent, os.path.basename(path)))
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as e:  # keep going; report it
            found.append(dict(agent=agent, error=f"could not parse {path}: {e}"))
            continue
        items = data
        if isinstance(data, dict):
            items = first(data, "decisions", "items", "entries") or []
        for i, raw in enumerate(items if isinstance(items, list) else []):
            if not isinstance(raw, dict):
                continue
            decision = first(raw, "decision", "choice", "what")
            why = first(raw, "why", "reason", "rationale", "because")
            if isinstance(why, (list, dict)):
                why = "; ".join(as_list(why))
            alt = first(raw, "alternative_rejected", "alternative rejected", "alternative", "alternatives",
                        "rejected", "alternative_considered")
            if isinstance(alt, (list, dict)):
                alt = "; ".join(as_list(alt))
            where = first(raw, "shows_up_in", "where it shows up", "where_it_shows_up", "where",
                          "where_used", "used_in", "shows_up")
            evidence = as_list(first(raw, "evidence", "source", "sources", "evidence_source"))
            text_for_cat = f"{decision} {why} {alt}"
            found.append(dict(
                agent=agent, agent_id=str(first(raw, "id") or f"{agent}-{i+1}"),
                decision=str(decision or "").strip(), why=str(why or "").strip(),
                alternative_rejected=str(alt or "").strip(), shows_up_in=as_list(where),
                evidence=evidence, category=norm_category(first(raw, "category"), text_for_cat),
                strength=str(first(raw, "strength") or "").lower() or None,
                raw=raw, path=os.path.relpath(path, ROOT)))
    return found


def agent_new_id(agent, agent_id):
    slug = re.sub(r"[^a-z0-9]+", "-", agent_id.lower()).strip("-")
    a = agent.lower()
    if slug.startswith(a + "-"):
        slug = slug[len(a) + 1:]
    return f"{a}-{slug}"


def merge(seed, agent_items, log):
    decisions = [dict(d) for d in seed]
    by_id = {d["id"]: d for d in decisions}
    for d in decisions:
        d["plain"] = seed_plain.PLAIN.get(d["id"], "")
        d["agent_records"] = []
    for item in agent_items:
        if "error" in item:
            log.append(f"ERROR {item['agent']}: {item['error']}")
            continue
        key = f"{item['agent']}:{item['agent_id']}"
        tok = tokens(item["decision"] + " " + item["alternative_rejected"])
        scored = sorted(((jaccard(tok, tokens(d["decision"] + " " + d["alternative_rejected"])), d["id"])
                         for d in decisions if not d["id"].startswith(item["agent"].lower() + "-")),
                        reverse=True)[:3]
        override = OVERRIDES.get(key, "auto")
        target = None
        if override == "new":
            target = None
        elif override == "skip":
            log.append(f"SKIP  {key}: {item['decision'][:110]}")
            continue
        elif override != "auto":
            target = by_id.get(override)
        elif scored and scored[0][0] >= 0.30:
            target = by_id[scored[0][1]]
        # provenance pointer only; the agent's own wording stays in its file (some of it was corrected later)
        record = dict(agent=item["agent"], agent_id=item["agent_id"], file=item["path"])
        for k, v in AGENT_TEXT.get(key, {}).items():
            item[k] = v
        if target is not None:
            target["agent_records"].append(record)
            target["sources_merged"] = sorted(set(target["sources_merged"]) | {f"{item['agent']} ({item['path']})"})
            for e in item["evidence"] + [f"{item['path']} (id {item['agent_id']})"]:
                if e not in target["evidence"]:
                    target["evidence"].append(e)
            log.append(f"MERGE {key} -> {target['id']}  (top match {scored[0][0]:.2f}; override={override})"
                       f"\n      agent: {item['decision'][:150]}\n      seed:  {target['decision'][:150]}")
        else:
            nid = agent_new_id(item['agent'], item['agent_id'])
            while nid in by_id:
                nid += "-b"
            why = item["why"]
            ev = item["evidence"] or [f"{item['path']} (id {item['agent_id']})"]
            if f"{item['path']} (id {item['agent_id']})" not in ev:
                ev.append(f"{item['path']} (id {item['agent_id']})")
            plain = AGENT_PLAIN.get(key)
            if not plain:
                why_first = re.split(r"(?<=[.!?])\s+", why)[0] if why else ""
                plain = item["decision"] if not why_first else f"{item['decision'].rstrip('.')}. {why_first}"
            new = dict(id=nid, category=AGENT_CATEGORY.get(key, item["category"]), decision=item["decision"], why=why, evidence=ev,
                       alternative_rejected=item["alternative_rejected"] or "(not stated by the agent)",
                       shows_up_in=item["shows_up_in"], strength=AGENT_STRENGTH.get(key) or item["strength"] or "moderate",
                       decided_by=item["agent"], when="13-14 Oct 2026, night build", status=AGENT_STATUS.get(key, "in force"), top10=None,
                       sources_merged=[f"{item['agent']} ({item['path']})"], plain=plain, agent_records=[record])
            if new["strength"] not in STRENGTH_ORDER:
                new["strength"] = "moderate"
            decisions.append(new)
            by_id[nid] = new
            near = ", ".join(f"{i} {s:.2f}" for s, i in scored)
            log.append(f"NEW   {key} -> {nid} [{new['category']}]  (nearest: {near})\n      agent: {item['decision'][:150]}")
    return decisions


def load_figures():
    figs = {}
    origin = {}
    paths = sorted(glob.glob(os.path.join(ROOT, "build", "N*", "figures.json")))
    out_path = os.path.join(ROOT, "build", "out", "figures.json")
    if os.path.exists(out_path):
        paths.append(out_path)  # build/out wins (it is the merged registry the site reads)
    for p in paths:
        try:
            with open(p, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            continue
        items = data if isinstance(data, list) else (first(data, "figures", "items") or [])
        if isinstance(items, dict):
            items = [{**v, "id": k} if isinstance(v, dict) else dict(id=k, value=v) for k, v in items.items()]
        for f in items:
            if isinstance(f, dict) and f.get("id"):
                if f.get("retired"):  # retired figures stay in build/out/retired_figures.json, never in derivations (N8 re-check R6)
                    figs.pop(f["id"], None)
                    origin.pop(f["id"], None)
                    continue
                figs[f["id"]] = f
                origin[f["id"]] = os.path.relpath(p, ROOT)
    return figs, origin, os.path.exists(out_path)


def scan_usage(fig_ids):
    """Where each figure id is cited: N7's deliverables, the site's config, pages and scripts."""
    paths = [p for p in glob.glob(os.path.join(ROOT, "deliverable", "*.md"))
             if os.path.basename(p) not in ("choices.md", "negative-results.md")]
    paths += glob.glob(os.path.join(ROOT, "site", "*.html")) + glob.glob(os.path.join(ROOT, "site", "config.json"))
    paths += glob.glob(os.path.join(ROOT, "site", "js", "**", "*.js"), recursive=True)
    used = {}
    for p in paths:
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        rel = os.path.relpath(p, ROOT)
        for fid in fig_ids:
            if re.search(r"(?<![A-Za-z0-9_])" + re.escape(fid) + r"(?![A-Za-z0-9_])", text):
                used.setdefault(fid, []).append(rel)
    return used


def build_derivations(figs, origin, have_out):
    chains = []
    index = {}
    used = scan_usage(list(figs))
    for c in seed_derivations.DERIVATIONS:
        c = dict(c)
        rx = [re.compile(r, re.I) for r in c.pop("match")]
        attached = []
        for fid, f in figs.items():
            if fid in index:
                continue
            if any(r.search(fid) for r in rx):
                attached.append(dict(id=fid, value=f.get("value"), unit=f.get("unit"), period=f.get("period"),
                                     label=f.get("label"), definition=f.get("definition"),
                                     derivation=f.get("derivation"), note=f.get("note"),
                                     source_sql_or_script=f.get("source_sql_or_script"), registry=origin[fid],
                                     cited_in=used.get(fid, [])))
                index[fid] = c["id"]
        c["figures"] = attached
        c["cited_in"] = sorted({p for f in attached for p in f["cited_in"]})
        c["status"] = "linked to registry figures" if attached else "awaiting registry figure (value from research or orchestrator check)"
        chains.append(c)
    # every registry figure not covered by a chain still gets an entry, from its own fields
    for fid, f in sorted(figs.items()):
        if fid in index:
            continue
        der = f.get("derivation") or ""
        chains.append(dict(
            id=f"fig:{fid}", title=f.get("definition") or fid,
            headline=f"{f.get('value')} {f.get('unit') or ''}".strip(), label=f.get("label"),
            sources=[], joins=[], analysis=f.get("definition") or "", corrections=[],
            bounds=[f["note"]] if f.get("note") else [],
            plain=der or "(no derivation text in the registry entry: flagged for the producing agent)",
            script=f.get("source_sql_or_script"), status="auto: from the figure's own registry entry; no N9 chain",
            figures=[dict(id=fid, value=f.get("value"), unit=f.get("unit"), period=f.get("period"),
                          label=f.get("label"), registry=origin[fid], cited_in=used.get(fid, []))],
            cited_in=used.get(fid, [])))
        index[fid] = f"fig:{fid}"
    missing_der = sorted(fid for fid, f in figs.items() if not f.get("derivation"))
    cited_unknown = []
    for p in glob.glob(os.path.join(ROOT, "deliverable", "*.md")):
        for fid in re.findall(r"\{\{fig:([A-Za-z0-9_\-]+)\}\}", open(p, encoding="utf-8", errors="replace").read()):
            if fid not in figs and fid != "id":
                cited_unknown.append(f"{fid} ({os.path.relpath(p, ROOT)})")
    return dict(
        generated=now_central(),
        about="Derivation chains for the figures most likely to be shown: each source with file or URL, each join, the analysis, corrections applied and the negative results that bound it. 'plain' is the text for the site's 'How we know' link. Figures attach from build/out/figures.json and build/N*/figures.json by id.",
        registry_present=have_out,
        n_chains_curated=len(seed_derivations.DERIVATIONS),
        n_registry_figures=len(figs),
        figures_without_derivation_text=missing_der,
        figures_cited_in_deliverables_or_site=sorted(used),
        cited_ids_missing_from_registry=sorted(set(cited_unknown)),
        chains=chains,
        figure_index=index,
        retired_figures=[dict(figure=a, why=b, source=s) for a, b, s in seed_derivations.RETIRED_FIGURES],
    )


def sort_key(d):
    return (CATEGORIES.index(d["category"]) if d["category"] in CATEGORIES else 99,
            STRENGTH_ORDER.get(d["strength"], 3), d["id"])


def render_choices(decisions, counts, agents_seen):
    by_id = {d["id"]: d for d in decisions}
    L = []
    L.append("# Choices we made, and why\n")
    L.append(f"Generated {now_central()} by `scripts/night/N9/build.py` from `build/out/decisions.json`. "
             "Each choice links to the evidence that drove it; the full record (alternatives rejected, sources, "
             "where each shows up) is in that JSON file.\n")
    L.append("## Summary\n")
    cat_bits = ", ".join(f"{counts['by_category'].get(c, 0)} {c}" for c in CATEGORIES)
    L.append(f"{counts['total']} deliberate choices are recorded ({counts['by_strength'].get('strong', 0)} strong, "
             f"{counts['by_strength'].get('moderate', 0)} moderate, {counts['by_strength'].get('minor', 0)} minor): {cat_bits}. "
             f"{counts['seed']} were recovered from the project files and earlier session transcripts; "
             f"{counts['from_agents_new']} came new from tonight's agents ({', '.join(agents_seen) or 'none yet'}), "
             f"and {counts['from_agents_merged']} agent entries matched a choice already recorded and were merged into it. "
             "Most choices trace to a specific piece of evidence: a city policy, a field in the 311 file, a count that "
             "failed to reproduce, or a ruling by Jack. What could not be traced is listed in "
             "`research/chapters/N9-choices.md`.\n")
    L.append("## Ten choices that make this trustworthy\n")
    for t in seed_negatives.TOP10:
        L.append(f"{t['n']}. **{t['title']}.** {t['text']} _(record: {', '.join('`'+i+'`' for i in t['ids'] if i in by_id)})_")
    L.append("")
    names = {"privacy": "Privacy", "ethics": "Ethics", "adoption": "Adoption: what lets the city run it",
             "method": "Method", "data source": "Data sources", "correction": "Corrections to our own work",
             "scope": "Scope: what we built and what we dropped", "presentation": "Presentation"}
    for cat in CATEGORIES:
        items = sorted([d for d in decisions if d["category"] == cat], key=sort_key)
        if not items:
            continue
        L.append(f"## {names[cat]}\n")
        main = [d for d in items if d["strength"] != "minor"]
        small = [d for d in items if d["strength"] == "minor"]
        for d in main + ([None] if small else []) + small:
            if d is None:
                L.append("\nSmaller choices:\n")
                continue
            text = d.get("plain") or d["decision"]
            tag = d["strength"]
            extra = []
            if d.get("status") and d["status"] != "in force":
                extra.append(d["status"])
            if d.get("agent_records") and d["id"].split("-")[0] in [a.lower() for a in agents_seen]:
                extra.append(f"logged by {d['decided_by']}")
            elif d.get("agent_records"):
                extra.append("also logged by " + ", ".join(sorted({r['agent'] for r in d['agent_records']})))
            ex = f" _({'; '.join(extra)})_" if extra else ""
            L.append(f"- {text} [{tag}; `{d['id']}`]{ex}")
        L.append("")
    return "\n".join(L) + "\n"


def render_negatives(neg):
    L = ["# What we tested that did not hold\n"]
    L.append(f"Generated {now_central()} by `scripts/night/N9/build.py`. Each entry is two sentences: what we "
             "tested or expected, and what happened, with the source. Labels: observed (we checked it), reported "
             "(a source says so), inferred (our conclusion), observed absence (we looked and did not find it).\n")
    FIRST = ["neg-exit", "neg-status-text", "neg-ward-gap", "neg-mix-hypothesis", "neg-tree-conversion",
             "neg-citystat-definitions", "neg-satellite"]
    first_items = [n for i in FIRST for n in neg if n["id"] == i]
    rest = [n for n in neg if n["id"] not in FIRST]
    L.append("## Summary\n")
    groups = []
    for n in neg:
        if n["group"] not in groups:
            groups.append(n["group"])
    L.append(f"{len(neg)} negative or bounding results, in {len(groups)} groups: "
             + "; ".join(f"{g.lower()} ({sum(1 for n in neg if n['group']==g)})" for g in groups)
             + ". The seven that shaped the entry most come first: the exit test, the status-text test, our own "
             "inflated ward gap, the fairness twist that did not survive its own test, the tree conversions we could "
             "not prove, the CityStat definitions that did not reproduce at first, and the satellite check we dropped. "
             "None of these is hidden on the site; they are what the rest of the numbers are bounded by.\n")
    def item(n):
        # one top-level bullet per result, bold title first: the site's bridge (scripts/night/N6/bridge.py,
        # build_negative) splits sections into items on bullets and takes the bold text as the title
        return f"- **{n['title']}.** {n['text']} ({n['label']}; source: {n['source']})\n"
    L.append("## The seven that shaped the entry\n")
    for n in first_items:
        L.append(item(n))
    for g in groups:
        members = [n for n in rest if n["group"] == g]
        if not members:
            continue
        L.append(f"## {g}\n")
        for n in members:
            L.append(item(n))
    return "\n".join(L) + "\n"


def sanitize(obj):
    if isinstance(obj, str):
        for pat, rep in SANITIZE:
            obj = re.sub(pat, rep, obj)
        return obj
    if isinstance(obj, list):
        return [sanitize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    return obj


def main():
    log = []
    agent_items = load_agent_decisions()
    agents_seen = sorted({i["agent"] for i in agent_items if "error" not in i})
    decisions = merge(seed_decisions.DECISIONS, agent_items, log)
    decisions = sanitize(decisions)
    decisions.sort(key=sort_key)
    counts = dict(
        total=len(decisions),
        seed=len(seed_decisions.DECISIONS),
        from_agents_total=sum(1 for i in agent_items if "error" not in i),
        from_agents_new=sum(1 for d in decisions if d["id"] not in {s["id"] for s in seed_decisions.DECISIONS}),
        from_agents_merged=sum(len(d["agent_records"]) for d in decisions if d["id"] in {s["id"] for s in seed_decisions.DECISIONS}),
        by_category={c: sum(1 for d in decisions if d["category"] == c) for c in CATEGORIES},
        by_strength={s: sum(1 for d in decisions if d["strength"] == s) for s in STRENGTH_ORDER},
        agents_with_decisions_file=agents_seen,
    )
    out = dict(
        generated=now_central(),
        about="Every deliberate choice behind the entry, merged and de-duplicated from N9's recovery of the project files and session transcripts and from each night agent's build/N*/decisions.json. Fields: id, category, decision, why, evidence, alternative_rejected, shows_up_in, strength, plus plain (one-or-two-sentence version for the site), decided_by, when, status, top10 (rank group in the 'ten choices' list), sources_merged and agent_records (provenance).",
        counts=counts,
        top10=seed_negatives.TOP10,
        decisions=decisions,
    )
    os.makedirs(os.path.join(ROOT, "build", "out"), exist_ok=True)
    with open(os.path.join(ROOT, "build", "out", "decisions.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    figs, origin, have_out = load_figures()
    der = sanitize(build_derivations(figs, origin, have_out))
    with open(os.path.join(ROOT, "build", "out", "derivations.json"), "w", encoding="utf-8") as fh:
        json.dump(der, fh, indent=1, ensure_ascii=False)
    os.makedirs(os.path.join(ROOT, "deliverable"), exist_ok=True)
    with open(os.path.join(ROOT, "deliverable", "choices.md"), "w", encoding="utf-8") as fh:
        fh.write(render_choices(decisions, counts, agents_seen))
    neg = list(seed_negatives.NEGATIVES) + list(EXTRA_NEGATIVES)
    with open(os.path.join(ROOT, "deliverable", "negative-results.md"), "w", encoding="utf-8") as fh:
        fh.write(render_negatives(neg))
    print(json.dumps(counts, indent=1))
    print(f"derivations: {der['n_chains_curated']} curated chains, {len(der['chains'])} total; "
          f"{der['n_registry_figures']} registry figures; {len(der['figures_without_derivation_text'])} without derivation text; "
          f"build/out/figures.json present: {have_out}")
    print(f"negative results: {len(neg)}")
    if "--log" in sys.argv:
        p = sys.argv[sys.argv.index("--log") + 1]
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("\n".join(log) + "\n")
        print(f"merge log: {len(log)} lines -> {p}")


if __name__ == "__main__":
    main()
