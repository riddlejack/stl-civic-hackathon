# Public export allowlist (E4)

Written 14 Oct 2026, 4:16 p.m. onward (Central), by E4. `export_public.sh` reads the rules block
below; nothing outside an `+` rule is copied, and any `-` rule beats every `+` rule.

**Summary.** The public copy holds the site (without mocks), the pipeline and analysis scripts,
the research reports, fact tables and chapters, the deliverables that are not correspondence,
the context files a reader needs, the figure and decision registries under `build/`, the site
screenshots, and an MIT licence. It holds no raw data, no database or parquet file, nothing from
`build/*/private/`, and no file that fails `scan_public.py`.

Observed on the run after E3's fixes (14 Oct 2026, 5:00 p.m. Central, into a scratch folder,
`--retry-fixable --drop-failing`): 320 files in one commit, scan 0 hits after 6 reviewed accepts
(three reviewed strings, each also quoted in this file); 86 unfinished placeholders and 44
address-shaped docstring examples (none a real address) reported as warnings. The data tier
listed 118 sources: 14 fetched by script, 1 vendored, 103 listed but not published.

**Not settled.** Three files still fail on wording that describes the exposed data and are held
back until reworded: `research/synthesis.md` (line 24 and section 9d at line 449),
`research/chapters/N6-site.md` (line 76) and `research/chapters/N9-choices.md` (line 53). Fifteen
files are excluded for good, with the 13 other R2 hunt probes that import one of them. The 22 files
that failed earlier on a line or two were fixed upstream and are now included.

**Data tier (added 14 Oct, about 4:55 p.m., on the orchestrator's policy; first test numbers below).** The export also writes
`data/README.md` and `scripts/data/fetch_public.sh` (sources in `public-data/`), and runs
`build_manifest.py` to write `data/MANIFEST.csv` and copy vendored files to `data/public/`. A
source is listed when a file in the export names its `data/raw/` path. On a copy of the 4:36 p.m.
export: 72 sources, 14 fetched by script, 1 vendored (CityStat's chart tables), 57 listed but not
published; the manifest, README and fetch script scan clean. `fetch_public.sh --check` reached all
16 sources at about 4:45 p.m.; a test download of five of them matched the saved files' fields. Never
listed: `data/raw/voters/`, the audit's metadata folders for the city's hosted services, and
`data/raw/slmpd/`. The Cityworks extracts and the status-page sample are listed as not published;
their aggregates and the Cityworks retrieval manifest are copied by the rules below.

Patterns: paths are relative to the repository root; `*` matches within one folder, `**` across
folders. A `-` rule may carry a reason after `#`; a reason starting `scan-fix:` marks a file that
`--retry-fixable` tries again.

```rules
# ---- always out: raw data, private build files, binaries, environments ----
- .git/**
- .venv/**
- **/__pycache__/**
- **/*.pyc
- **/.DS_Store
- .claude/**
- data/**                        # raw downloads; git-ignored; never leave the machine
- build/*/private/**             # ids, exact addresses, parcel-tight images
- **/*.parquet
- **/*.duckdb
- **/*.duckdb.wal
- **/.env

# ---- site ----
+ site/**
- site/mock/**                   # fallback only; every page reads site/data first

# ---- scripts ----
+ scripts/**

# ---- research: reports, fact tables, chapters ----
+ research/*.md
+ research/*-facts.csv
+ research/attention-chart-*.png # charts the attention report embeds (aggregate counts)
+ research/chapters/**
- research/*/private/**

# ---- deliverables ----
+ deliverable/**
- deliverable/README.md          # copied to the repository root as README.md instead
- deliverable/email-to-mike-dropbox.md  # unsent correspondence to a named organiser
- deliverable/note-to-ben-v2.md         # unsent correspondence to a named city official
- deliverable/ask-to-ben.md             # unsent correspondence to a named city official
- deliverable/progress-report*.md       # check-ins to the organiser; quote Jack's inbox

# ---- context: only what a reader needs ----
+ context/HACKATHON_CONTEXT.md
+ context/BEN-PROBLEM-SETS.md
+ context/FRESH-EYES-ASSESSMENT.md
+ context/BRAINSTORM-shape.md
+ context/PITCH-ARCHITECTURE.md
+ context/AUTHORISATION-NOTE.md
+ context/question-standard.md

# ---- data behind the Cityworks and status-page claims: aggregates and retrieval manifests ----
+ research/cityworks-retrieval-manifest.csv
+ research/cityworks-*aggregate*.csv
+ research/cityworks-*aggregate*.json
+ research/cityworks-department-gap-matrix.csv
+ research/cityworks-extraction-validation.json
+ research/cityworks-pca-probes.json
+ build/E1/*.csv
+ build/E1/*.json
+ build/E1/service_table.md
- build/E1/probe_pages.csv       # one row per sampled status page; the sample is not published as rows

# ---- the data tier's sources; the export writes them to data/ and scripts/data/ ----
- scripts/exec/E4/public-data/**

# ---- registries under build/ ----
+ build/out/figures.json
+ build/*/figures.json
+ build/*/decisions.json
+ build/N2/closure_class.sql     # README names it as the closure-class SQL
+ build/N6/shots/**              # site screenshots; block level (checked by eye and OCR)
+ build/E3/shots/**
+ build/E6/shots/**              # E6: the rebuilt five screens and two video crops; block level
+ build/E6/E6-site-facts.csv     # E6: one row per figure the rebuilt screens show

# ---- excluded because they fail the scan (E4 local run, 14 Oct 2026) ----
# Permanent: the content itself is the problem.
- research/data-audit.md                          # scan: disclosure wording, real request and parcel ids, organiser e-mails, coordinates, the Cityworks query host
- research/data-audit-facts.csv                   # scan: same, row by row
- research/disclosure-verification-2026-10-13.md  # scan: the unsent disclosure itself
- research/disclosure-verification-2026-10-13-facts.csv  # scan: same
- research/synthesis-notes.md                     # scan: disclosure wording, a real request id, the Cityworks query host
- research/synthesis-facts.csv                    # scan: same
- research/chapters/N8-verification.md            # scan: describes the disclosure; quotes two leaked two-number labels
- research/cityworks-department-gap-matrix-facts.csv  # scan: source URLs on the Cityworks query host
- scripts/exec/E1/02_fetch.py                     # scan: fetches the robots-disallowed endpoint (authorised; see AUTHORISATION-NOTE)
- scripts/exec/E1/03_parse.py                     # scan: same endpoint path
- scripts/exec/E1/06_items.py                     # scan: same endpoint path
- scripts/exec/E1/09_facts.py                     # scan: same endpoint path
- scripts/night/N8/scan.py                        # scan: its keyword list names the disclosure's field names
- scripts/night/R2/hunt_*                         # scan: hunt_lib.py's never-fetch list names the host and path; hunt_d_open311.py holds a real request id; the other probes import hunt_lib
# Fixable: one or two lines each; the owner rewords at source and re-runs. Retry with --retry-fixable.
# 22 files fixed upstream on 14 Oct (E3 and the orchestrator) were removed from this list at 5:05 p.m.; the export run then included them and scanned clean.
- research/synthesis.md                           # scan-fix: section 9d (line 449) and line 24 describe the exposed tables; drop 9d and the clause
- research/chapters/N6-site.md                    # scan-fix: line 76 lists the words that describe the exposed data
- research/chapters/N9-choices.md                 # scan-fix: line 53 quotes the layer count from the disclosure
```

## Why each exclusion

| Path | Reason | Observed |
|---|---|---|
| `data/**` | Raw downloads (8.1 GB): 311 CSVs with addresses, parcel files, Cityworks rows. The pipeline expects them under `data/raw/`; a reader downloads them from the city. | git-ignored |
| `build/*/private/**` | Request ids, exact addresses and parcel ids by design (N8 finding 4). 10 such folders exist today. | `find build -name private` |
| `*.parquet`, `*.duckdb` | Row-level copies of the 311 file with addresses and SRX/SRY (`build/stl.duckdb` is 0.9 GB). | |
| `site/mock/**` | Synthetic fallback files; the page only reads them when `site/data/<name>.json` is missing (`site/js/common.js` line 79). | |
| `deliverable/README.md` | Copied to `README.md` at the root, where its root-relative links work. | |
| Correspondence drafts | `email-to-mike-dropbox.md`, `note-to-ben-v2.md`, `ask-to-ben.md` and `progress-report*.md` are unsent notes to named people and quote Jack's inbox. Publishing them before they are sent would pre-empt the conversation. Jack's call: remove the line to include one. | read 14 Oct, 4:30 p.m. |
| Other `research/` files | Not in the brief: aggregate CSVs and JSON beside the reports, `research/parts/`, `research/data-audit-parts/`, the `*-scripts/` folders. Add a `+` line to include one; the scan still runs. | |
| Other `context/` files | Hand-offs, night plans and thread inputs are working notes; `disclosure-draft.md` is the unsent disclosure. | |
| Other `build/` files | Logs, intermediate CSVs, `build/out/*` exports other than `figures.json` (`monday_list.csv` held two-number house addresses in N8's check), and `build/csb-clean/` (cleaned copies of the raw 311 CSVs). | |

Screenshots (`build/N6/shots`, `build/E3/shots`, `build/E6/shots`) are included: the brief excludes them only if
they show addresses, and they do not. They render site pages, which are block level; five were
checked by eye on 14 Oct (receipt twice, queue by street, status page before/after, Monday brief)
and show blocks and "number withheld" only, and the scan OCRs every image on each run. The N6 set
(01:19 a.m.) shows the older site layout. E6 (14 Oct, evening) added `build/E6/shots/` (the rebuilt five screens; block level, checked by eye) and its facts table.

## Reviewed hits the scan accepts

Each line is `path | category | exact text | reason`. The scan skips a hit only when all three
of path, category and text match. Keep this list short; fix at source where possible.

```accept
context/HACKATHON_CONTEXT.md | address | 911 Washington Avenue | the hackathon venue's public business address
research/what-gets-adopted-facts.csv | latlon | 38.774288, -90.320515 | corner of the city's bounding box in an API query, not a point
scripts/exec/E4/export_public.sh | email | noreply@anthropic.com | commit trailer; a no-reply address
```
