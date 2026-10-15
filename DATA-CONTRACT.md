# Site data contract (N6)

Written 13 Oct 2026, about 11:55 p.m. Central. This is the agreement between the
pipeline (N1 to N5, N9) and the site. If you export in these shapes, the site
picks your file up with no code change.

## How data reaches the page

```
build/out/*.json, build/N*/*.json, deliverable/*.md
        │   scripts/night/N6/bridge.py  (validate, adapt, cut to block level)
        ▼
site/data/<name>.json   ← the page reads these
site/mock/<name>.json   ← fallback when site/data/<name>.json is missing
```

- The page never reads `build/` directly. The bridge copies only the fields
  listed here, so nothing finer than a block reaches `site/`.
- Any section that ends up on a mock file shows a red **MOCK DATA** banner.
- `scripts/night/N6/serve.sh` runs the bridge, then serves `site/` on
  `http://127.0.0.1:8806/`. Re-run it after any upstream re-run.
- `site/data/status.json` records, per file, whether it is real, partial or
  mock and which upstream files it came from.

## The envelope (every file)

```json
{ "meta": { "contract": "<name>/1", "mock": false,
            "built_at": "2026-10-14 00:30 CDT",
            "sources": [{"path": "build/N4/scoreboard.json", "mtime": "..."}],
            "notes": ["free text, shown nowhere on the page"] },
  "...payload..." }
```

Mock files carry `"mock": true`. Dates are ISO (`2026-07-02` or
`2026-07-02 10:17`), Central time. Shares are 0–1 floats, never percents.

## Upstream preference order

For each file the bridge takes the first source that exists and passes
validation:

| site/data file | 1st choice (contract shape) | then (adapted) |
|---|---|---|
| `run.json` | `build/out/run.json` | `build/N1/manifest.json` → `meta` |
| `figures.json` | `build/out/figures.json` | every `build/N*/figures.json`, merged |
| (derivations) | `build/out/derivations.json` | `figure.derivation` field |
| `receipts.json` | `build/out/receipts.json` + `build/N5/heroes.json` | heroes only |
| `scoreboard.json` | `build/out/scoreboard.json` | `build/N4/scoreboard.json` + `build/N4/q3_2026.json` |
| `fairness.json` | `build/out/fairness.json` | `build/N3/decomposition.json` + `build/N3/robust_comparisons.csv` |
| `register.json` | `build/out/register.json` | `build/N2/register.json` |
| `monday.json` | `build/out/monday_list.json` (+ `mowing_2026.json`) | none |
| `dumping.json` | `build/out/dumping_blocks.json` | none |
| `decisions.json` | `build/out/decisions.json` + `deliverable/choices.md` | `build/N*/decisions.json` merged |
| `negative.json` | `deliverable/negative-results.md` | none |

## Payloads

### run.json
`{ asof, ledger_max_date, built_at }`. `asof` is the latest filing time in
the 311 file ("data through").

### figures.json
`{ figures: { <id>: Figure } }` where Figure is COMMON's registry entry:
`id, value, unit, period, definition, label (observed|reported|inferred|estimated),
source_sql_or_script, note, derivation`. `derivation` is one or two plain
sentences: sources joined, analysis, correction. If missing, the page builds
the "How we know" text from `definition`, `period`, `source_sql_or_script`
and `note`. `build/out/derivations.json` may be either
`{ <id>: "text" }`, `{ <id>: {text|derivation|chain: [...]}}` or a list of
`{id, derivation|text|chain}`; the bridge accepts all three.

Ids the page asks for by default are in `site/config.json` (`lead.figure_id`
and the `{id}` placeholders in the lead sentences). A missing id renders as
a dash with a red "mock" tag, never as an invented number.

### receipts.json
`{ receipts: [Receipt], heroes: [HeroSummary] }`

Receipt (N1 exports `receipt_base` rows; any subset of these columns works):

| field | type | note |
|---|---|---|
| `request_id` | string | the city's public REQUESTID |
| `problem_code`, `type_name` | string | |
| `ward` | "01".."14" | |
| `neighborhood` | string | |
| `public_address` | string | **block only**: "1200 block of Example St" |
| `filed`, `promised`, `closed`, `cancelled`, `investigation_done` | datetime | |
| `promise_days`, `days_to_close` | number | |
| `status`, `status_group` | string | open / closed / cancelled |
| `closed_with_words` | string | the city's PUBLICRESOLUTION, verbatim |
| `closure_class` | string | done / handed_off / converted / no_action / info_other / blank |
| `closed_by_promise`, `done_by_promise` | bool | |
| `ledger_first_cut_after`, `ledger_days_to_first_cut`, `ledger_no_cut_in_season`, `ledger_cut_within_30`, `ledger_cut_within_60`, `ledger_max` | | weed codes only |
| `work_orders_nearby` | int | tree codes only (sample) |
| `next_same_request_filed`, `days_to_next_same_request` | | same type, same address |
| `hero_id` | string | set by the bridge when the id belongs to an N5 case |
| `timeline` | `[{date, kind, title, detail, source, label}]` | built by the bridge if absent; `kind` ∈ filed, closed, cancelled, promised, record, refiled, today, history |
| `line` | string | the plain-English sentence; built from a template if absent |
| `image` | `{src, caption, date}` or null | path under `site/img/`; block-framed, no marker |

**Named examples (current receipts.json):** `{ examples: [{key, label, cases: [id]}], cases: {<id>: {id, role, type,
type_label, ward, neighborhood, block, what, story, facts, timeline, images: [{src, year, kind: naip|msdis,
source_label, licence, caption}]}} }`. No request ids. NAIP 2024 (public domain) is the default image;
MSDIS images are included only when `site/config.json` sets `"show_msdis_imagery": true`.

HeroSummary: `{ id, type, ward, neighborhood, block, request_ids, story_line }`
(the story line is rebuilt from the template so it never names a house
number).

### scoreboard.json
`{ window, rows: [Row], q3: [Q3] }`

Row: `problemcode, name, category, requests, promise_days, scored,
kept_share, done_kept_share, late_share, median_days_late,
open_past_promise, median_days_to_close, closed_done_share,
closed_handed_off_share, closed_no_action_share, citystat_metric,
citystat_goal_days`.
Q3: `metric, label, goal_days, citystat_q2_share, citystat_q2_n, q3_share,
q3_n, q3_definition, note` (Q3 2026 under N4's best-matching definition,
"our definition, from the public file").

### fairness.json
```
{ headline, sub,
  citystat: {a_label, b_label, a_days, b_days, period, label, source},
  decomposition_figure, reproduction_figures: [id], no_gap_figure,
  decompositions: [{ key, a_label, b_label, a_mean, b_mean, gap, n_a, n_b,
                     mix_share, speed_share,
                     components: [{key, group: mix|speed, label, days, share}] }],
  lead:   [{ type, title, words, step, figure_id, period, a_label, b_label,
             a_median, b_median, n_a, n_b, ratio, ci_lo, ci_hi,
             before: {a_median, b_median}, promise_days }],
  no_gap: [{ type, title, a_median, b_median, n_a, n_b, ratio, promise_days }] }
```
`components` must sum to `b_mean − a_mean` (the bridge checks within 0.1
day). The reading follows N3 (COMMON correction 2): same type, same closing
words, later, in the first step. Single light out is not robust and is never
shown; the towing "promise met" shares are disputed and not shown until N8
settles them.

### register.json
`{ columns: [{key, label, help}], rows: [{ id, service, cells: {<key>:
{state: yes|partial|no|na, text}}, filed, share_closed_done, record_source,
what_it_would_take }] }`. Column keys: `intake`, `promise`, `says_done`,
`record`, `joined`.

### monday.json
```
{ asof, definition,
  by_ward: [{ward, n}], by_type: [{type, n}],
  rows: [{request_id, type_name, division, ward, block, filed, promised,
          days_past_promise, age_days, status}],
  csv: "downloads/monday_list.csv",
  mowing: { season, title, definition, rows: [{ward, parcels_on_rotation,
            parcels_gap_over_42d, median_longest_gap}] } | null }
```
N1's `monday_list` view already has these columns; export it as
`build/out/monday_list.json` = `{meta, rows: [...]}` with `block_label` or
`block`. Sensitive codes excluded upstream. No row below block level.

### dumping.json
`{ window, summary: {requests, blocks, repeat_blocks, share_repeat},
  blocks: [{block, ward, n_requests, n_addresses, first_report, last_report,
  n_closed_done, n_closed_handoff, n_closed_no_action, n_open,
  median_days_to_close}] }` (N1 `dumping_blocks` view, top 200 by
`n_requests`).

### decisions.json
`{ ten: [{title, text}], decisions: [{id, category, decision, why,
evidence, alternative_rejected, shows_up_in, strength}] }`. `ten` comes from
the "Ten choices" list in `deliverable/choices.md`; if absent, the ten
`strength: strong` entries with the most `shows_up_in` mentions.

### negative.json
`{ items: [{title, text, group, featured}] }` from `deliverable/negative-results.md` (one item per bullet,
de-duplicated; `featured` marks "The seven that shaped the entry"). Items that describe exposed data are held back.

## Privacy rules the bridge enforces

- Addresses: house numbers are rounded down to the hundred block
  ("1234 EXAMPLE ST" → "1200 block of Example St"); any free text
  (stories, timeline events, closing words) is scanned for street addresses
  and rewritten the same way.
- Dropped outright: parcel ids, handles, latitude/longitude, SRX/SRY,
  `related_parcels`, anything under `build/*/private/`.
- Codes in N1's `sensitive_codes` table never appear below ward level.
