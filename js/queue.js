// Past-due list: what a division head opens on Monday. Every division (or one), one headline, filters, the
// block-level map and the list. Counts are registered figures (e3_queue_*, e5_*, e7_*); the map dots and the list
// rows come from the same rows (data/ranked.json from scripts/exec/E7/rank.py), block level, no request numbers.
// Ranked (default) scores each request by the hazard of its type, days past the date and repeat reports; the
// weights start from data/rank-weights.json and can be changed on the page (this browser only). Oldest first is
// the same rows by days past the date; Close-out holds the records with evidence they are done, superseded or
// administrative (counts only). Design: research/prioritisation-option.md.
// v8: filters (type, hazard tier, days past, repeats, work order) drive both the map and the list, with counts;
// the map zooms and pans (queue-zoom.js); the ranking panel is always visible and editable.
import { state, h, $, clear, fmt, load, showTip, hideTip } from './common.js';
import { s } from './charts.js';
import { boot, finish, card, params, ftxt, fnum, page } from './app.js';
import { zoomable } from './queue-zoom.js';

const MAIN = [['all', 'All divisions'], ['FORESTRY', 'Forestry'], ['STREET DEPT, 510', 'Streets'], ['BUILDING DIV', 'Building Division'], ['LRA', 'Land bank (LRA)'],
  ['WATER DIV', 'Water Division'], ['TRAFFIC DIVISION, 511', 'Traffic']];
const OTHER = [['VECTOR CNTRL', 'Vector Control'], ['Tornado, Recovery', 'Tornado recovery'], ['BLDG LEAD INSP', 'Lead inspection'],
  ['BLDG TRADES', 'Building trades'], ['CITY EMRGCY MNG', 'Emergency management'], ['TREAS PRKG SVC', 'Treasurer, parking']];
const NAMES = Object.fromEntries([...MAIN, ...OTHER]);
const STATUS = { Disptch: 'Dispatched', NEW: 'New', Pending: 'Pending', Inspect: 'Inspection', SCHEDULED: 'Scheduled', Reinsp: 'Reinspection',
  Letter: 'Letter sent', 'ON HOLD': 'On hold', Extended: 'Extended', Refer: 'Referred', Hearing: 'Hearing', 'BPS APPROVED': 'Approved' };
// days past the date: the three bins of the map legend
const BIN_COL = ['var(--late-1)', 'var(--late-2)', 'var(--late-3)'];
const BIN_LABEL = ['Up to 90 days', '91 to 365 days', 'More than a year'];
const binOf = (d) => (d > 365 ? 2 : d > 90 ? 1 : 0);
const PAGE = 60;
const VIEWS = [['ranked', 'Ranked'], ['oldest', 'Oldest first'], ['closeout', 'Close-out']];
const KEYS = ['code', 'tier', 'bin', 'rep', 'wo'];

const Q = { div: 'all', block: null, shown: PAGE, view: 'ranked', rows: [], loaded: false,
  F: Object.fromEntries(KEYS.map((k) => [k, new Set()])), typeQuery: '' };

async function main() {
  // start the list's data at once; the headline and the map draw from queue.json while it arrives
  const later = Promise.all([load('ranked'), fetch('data/rank-weights.json', { cache: 'no-cache' }).then((r) => r.json())]);
  await boot('queue.html', 'Past-due list');
  const navLink = document.querySelector('.nav a[href="queue.html"]');
  if (navLink) navLink.textContent = 'Past-due list';
  Q.d = await load('queue');
  const want = params.get('div');
  if (want && NAMES[want]) Q.div = want;
  if (VIEWS.some(([v]) => v === params.get('view'))) Q.view = params.get('view');
  if (card === 'map') { renderMapCard(); finish(); return; }
  render();
  const [R, W] = await later;
  Q.R = R; Q.W0 = W; Q.W = JSON.parse(JSON.stringify(W));
  Object.assign(state.figures, R.figures || {});           // e7_* figures, registered in build/E7/figures.json
  Q.rows = decode(R, W);
  rescore();
  Q.loaded = true;
  buildRankPanel();
  drawDef();
  recompute();
  fit();
  finish();
}

// ------------------------------------------------------------------ rows and the score (the same rule as scripts/exec/E7/rank.py)
function tierOf(code, W) {
  const o = (W.tier_overrides || {})[code];
  if (o) return +o;
  if ((W.tiers['1'].codes || []).includes(code)) return 1;
  if ((W.tiers['2'].codes || []).includes(code)) return 2;
  return 3;
}
function decode(R, W) {
  const c = Object.fromEntries(R.cols.map((k, i) => [k, i]));
  return R.rows.map((x) => {
    const [code, name] = R.codes[x[c.code_i]];
    const days = x[c.days], n = x[c.repeat_n];
    return { division: R.divisions[x[c.division_i]], problem_code: code, type_name: name, code, block: x[c.block], ward: x[c.ward],
      filed: x[c.filed], promised: x[c.promised], days, status: x[c.status], repeat_n: n, mates: x[c.block_mates],
      wo_open: !!x[c.wo_open], wo: x[c.wo_open] ? 1 : 0, rep: n > 1 ? 1 : 0, bin: binOf(days), tier: tierOf(code, W),
      bulk: n > (W.bulk_check_over || 10) };
  });
}
function rescore() {
  const W = Q.W;
  const dpp = Math.max(1, +W.lateness.days_per_point || 1);
  for (const r of Q.rows) {
    r.H = +W.tier_points[String(r.tier)] || 0;
    r.D = Math.min(Math.floor(r.days / dpp), +W.lateness.cap || 0);
    r.R = Math.min((+W.repeats.points_per_extra_report || 0) * (r.repeat_n - 1), +W.repeats.cap || 0);
    r.score = r.H + r.D + r.R;
  }
}
const times = (n) => (n === 2 ? 'twice' : `${n} times`);
function whyParts(r) {
  const parts = [[`${Q.W.tiers[String(r.tier)].short}`, r.H], [`${fmt.int(r.days)} days past the date`, r.D]];
  if (r.repeat_n > 1) parts.push([`reported ${times(r.repeat_n)}`, r.R]);
  return parts;
}
function whyText(r) {
  const bits = whyParts(r).map(([t, p]) => `${t} · +${p}`);
  if (r.wo_open) bits.push('work order open');
  if (r.bulk) bits.push('many reports at one address: check');
  if (r.mates) bits.push(`${r.mates} more overdue on this block`);
  return bits.join(' · ');
}

// ------------------------------------------------------------------ filtering (faceted counts: each option counts the rows that pass every other filter)
const divInfo = (div) => (Q.d.divisions || []).find((x) => x.division === div);
const pastId = (div) => (div === 'all' ? 'e3_queue_past_promise' : divInfo(div)?.figures.past);
function divBase() {
  if (Q.baseDiv !== Q.div) { Q.base = Q.div === 'all' ? Q.rows : Q.rows.filter((r) => r.division === Q.div); Q.baseDiv = Q.div; }
  return Q.base;
}
const anyFilter = () => KEYS.some((k) => Q.F[k].size);
function recompute() {
  if (!Q.loaded) return;
  const base = divBase();
  const counts = Object.fromEntries(KEYS.map((k) => [k, new Map()]));
  const inc = (k, v) => counts[k].set(v, (counts[k].get(v) || 0) + 1);
  const out = [];
  for (const r of base) {
    let fails = 0, fk = null;
    for (const k of KEYS) {
      const S = Q.F[k];
      if (S.size && !S.has(r[k])) { fails++; fk = k; if (fails > 1) break; }
    }
    if (!fails) { out.push(r); for (const k of KEYS) inc(k, r[k]); }
    else if (fails === 1) inc(fk, r[fk]);
  }
  Q.counts = counts;
  Q.filtered = out;
  sortRows();
  drawFilters();
  drawDots();
  drawList();
}
function sortRows() {
  Q.filtered.sort(Q.view === 'oldest' ? (a, b) => b.days - a.days : (a, b) => b.score - a.score || b.days - a.days);
}
let timer = null;
const soon = (fn, ms = 70) => { clearTimeout(timer); timer = setTimeout(fn, ms); };
function toggle(k, v) {
  const S = Q.F[k];
  if (S.has(v)) S.delete(v); else S.add(v);
  Q.shown = PAGE; Q.block = null;
  soon(recompute);
}
function clearFilters() {
  for (const k of KEYS) Q.F[k].clear();
  Q.block = null; Q.shown = PAGE; Q.typeQuery = '';
  if (Q.typeSearch) Q.typeSearch.value = '';
  recompute();
}

// ------------------------------------------------------------------ page
function render() {
  const root = page();
  Q.seg = h('div', { class: 'seg', role: 'group', 'aria-label': 'Division' });
  Q.dl = h('button', { class: 'btn ghost', type: 'button', onclick: downloadCSV });
  root.append(h('div', { class: 'q-top' }, h('div', { class: 'q-title-row' }, h('h1', { class: 'q-title', text: 'Past-due list' }), Q.seg), Q.dl));
  Q.head = h('div', { class: 'q-head' });
  root.append(Q.head);
  Q.side = h('aside', { class: 'q-side', 'aria-label': 'Filters and ranking' });
  Q.mapCard = h('div', { class: 'card q-map' });
  Q.listCard = h('div', { class: 'card q-list' });
  Q.grid = h('div', { class: 'q-layout' }, Q.side, Q.mapCard, Q.listCard);
  root.append(Q.grid);
  root.append(howBuilt());
  buildPicker();
  buildFilters();
  Q.rankCard = h('div', { class: 'card q-rank' }, h('h2', { text: 'How the ranking works' }), h('p', { class: 'fine', text: 'Loading the weights…' }));
  Q.side.append(Q.rankCard);
  buildMap(Q.mapCard);
  buildList();
  update();
  fit();
  window.addEventListener('resize', () => soon2(() => fit()));
}
let t2 = null;
const soon2 = (fn) => { clearTimeout(t2); t2 = setTimeout(fn, 80); };

// On a wide screen the filters, the map and the list share one viewport: each takes the height left under the
// headline; the map's width follows the city's shape; the filters and the list scroll inside their cards.
function fit(again = false) {
  const grid = Q.grid, svg = Q.svg;
  const sc = Q.listCard.querySelector('.q-scroll');
  if (window.innerWidth < 1180) {
    grid.style.gridTemplateColumns = ''; svg.style.height = ''; svg.style.maxHeight = '';
    Q.side.style.maxHeight = ''; Q.listCard.style.height = ''; sc.style.maxHeight = ''; sc.style.flex = '';
    return;
  }
  const top = grid.getBoundingClientRect().top + window.scrollY;
  const H = Math.max(600, window.innerHeight - top - 24);
  const m = Q.d.map || {};
  svg.style.maxHeight = 'none';
  const extra = Q.mapCard.offsetHeight - svg.getBoundingClientRect().height;
  const sh = H - extra;
  svg.style.height = `${sh}px`;
  const w = Math.round(sh * (m.width + 20) / (m.height + 20)) + 36;
  const side = window.innerWidth >= 1500 ? 340 : 300;
  grid.style.gridTemplateColumns = `${side}px ${Math.max(300, w)}px minmax(0, 1fr)`;
  Q.side.style.maxHeight = `${H}px`;
  Q.listCard.style.height = `${H}px`;
  sc.style.maxHeight = 'none'; sc.style.flex = '1'; sc.style.minHeight = '0';
  // the new column width can rewrap the map's caption: measure once more
  if (!again) fit(true);
}

function buildPicker() {
  for (const [div, label] of MAIN) Q.seg.append(h('button', { type: 'button', 'data-div': div, text: label, onclick: () => pickDiv(div) }));
  Q.menu = h('div', { class: 'menu', role: 'menu', hidden: true }, ...OTHER.map(([v, t]) => h('button', { type: 'button', role: 'menuitem', 'data-div': v, text: t,
    onclick: () => { Q.menu.hidden = true; pickDiv(v); } })));
  Q.other = h('button', { type: 'button', class: 'other', 'aria-haspopup': 'menu', text: 'Other ▾', onclick: (e) => { e.stopPropagation(); Q.menu.hidden = !Q.menu.hidden; } });
  document.addEventListener('click', () => { Q.menu.hidden = true; });
  Q.seg.append(h('span', { class: 'menu-wrap' }, Q.other, Q.menu));
}

function pickDiv(div) {
  Q.div = div; Q.block = null; Q.shown = PAGE;
  // a type that the new division never sees would silently empty the list
  Q.F.code.clear();
  update();
}

function update() {
  Q.seg.querySelectorAll('button[data-div]').forEach((b) => b.classList.toggle('on', b.dataset.div === Q.div));
  const inOther = OTHER.some(([v]) => v === Q.div);
  Q.other.textContent = `${inOther ? NAMES[Q.div] : 'Other'} ▾`;
  Q.other.classList.toggle('on', inOther);
  Q.dl.textContent = 'Download this list (CSV)';
  clear(Q.head);
  Q.head.append(h('h2', { class: 'headline' }, h('span', { class: 'headline-key', 'aria-hidden': 'true' }),
    `${NAMES[Q.div]}: `, h('span', { class: 'num' }, fnum(pastId(Q.div))), ' requests past the date the city gave'));
  Q.def = h('p', { class: 'q-def' });
  Q.head.append(Q.def);
  drawDef();
  if (Q.loaded) recompute(); else { drawDots(); drawList(); }
}

function drawDef() {
  clear(Q.def);
  const C = Q.R?.closeout;
  const co = C ? C.groups.reduce((a, g) => a + (Q.div === 'all' ? g.n : (g.by_division || {})[Q.div] || 0), 0) : null;
  if (Q.view === 'closeout') Q.def.append('Records with evidence the work is done, superseded or paperwork: a desk can verify and close them, no crew needed.');
  else {
    Q.def.append(Q.view === 'ranked' ? 'Still open after the date the city set, ranked by the hazard of the request type, how far past the date it is, and repeat reports.'
      : 'Still open after the completion date the city set (“Dept Response Due By”), furthest past it first.');
    if (Q.loaded) {
      Q.def.append(' ', h('span', { class: 'q-recon' }, Q.div === 'all' ? fnum('e7_ranked_public_n') : fmt.int(divBase().length), ' are listed here; ',
        Q.div === 'all' ? fnum('e7_closeout_n') : fmt.int(co), ' with evidence the work is done or superseded are under Close-out',
        Q.div === 'all' ? '; sensitive types are counted, never listed.' : '.'));
    }
  }
  const u = new URL(location.href);
  if (Q.div !== 'all') u.searchParams.set('div', Q.div); else u.searchParams.delete('div');
  if (Q.view !== 'ranked') u.searchParams.set('view', Q.view); else u.searchParams.delete('view');
  history.replaceState(null, '', u);
}

// ------------------------------------------------------------------ filters
function buildFilters() {
  const C = h('div', { class: 'card q-filters' });
  Q.clearBtn = h('button', { class: 'linkish', type: 'button', text: 'Clear filters', onclick: clearFilters });
  C.append(h('div', { class: 'qf-head' }, h('h2', { text: 'Filters' }), Q.clearBtn));
  Q.fsum = h('p', { class: 'qf-sum', text: 'Loading the list…' });
  C.append(Q.fsum);
  // request type: a searchable checklist
  Q.typeBtn = h('button', { type: 'button', class: 'qf-typebtn', 'aria-expanded': 'false', text: 'Any request type ▾',
    onclick: () => { Q.typePop.hidden = !Q.typePop.hidden; Q.typeBtn.setAttribute('aria-expanded', String(!Q.typePop.hidden)); if (!Q.typePop.hidden) { drawTypeList(); Q.typeSearch.focus(); } } });
  Q.typeSearch = h('input', { type: 'search', class: 'qf-search', placeholder: 'Find a request type', 'aria-label': 'Find a request type',
    oninput: (e) => { Q.typeQuery = e.target.value; drawTypeList(); } });
  Q.typeList = h('div', { class: 'qf-typelist' });
  Q.typePop = h('div', { class: 'qf-pop', hidden: true }, Q.typeSearch, Q.typeList);
  Q.typeChips = h('div', { class: 'qf-chips' });
  C.append(h('div', { class: 'qf-group' }, h('div', { class: 'qf-label', text: 'Request type' }), Q.typeBtn, Q.typePop, Q.typeChips));
  Q.groups = {};
  const group = (k, label) => {
    const box = h('div', { class: 'qf-opts' });
    Q.groups[k] = box;
    C.append(h('div', { class: 'qf-group' }, h('div', { class: 'qf-label', text: label }), box));
  };
  group('tier', 'Hazard tier');
  group('bin', 'Days past the date');
  group('rep', 'Repeat reports');
  group('wo', 'Work order');
  Q.side.append(C);
}

function optionsFor(k) {
  if (k === 'tier') return [1, 2, 3].map((t) => [t, Q.W ? Q.W.tiers[String(t)].short : `Tier ${t}`, h('i', { class: `qf-tier t${t}`, 'aria-hidden': 'true' })]);
  if (k === 'bin') return [0, 1, 2].map((b) => [b, BIN_LABEL[b], h('i', { class: 'qf-sw', style: `background:${BIN_COL[b]}`, 'aria-hidden': 'true' })]);
  if (k === 'rep') return [[0, 'Reported once'], [1, 'Reported more than once']];
  if (k === 'wo') return [[1, 'Work order open'], [0, 'No open work order']];
  return [];
}

function drawFilters() {
  const n = Q.filtered.length, all = divBase().length;
  clear(Q.fsum);
  Q.fsum.append(h('b', { text: fmt.int(n) }), ` of ${fmt.int(all)} listed requests${Q.div === 'all' ? '' : ' in ' + NAMES[Q.div]}`);
  Q.clearBtn.disabled = !anyFilter();
  for (const k of ['tier', 'bin', 'rep', 'wo']) {
    const box = Q.groups[k];
    clear(box);
    for (const [v, label, icon] of optionsFor(k)) {
      const c = Q.counts[k].get(v) || 0;
      const on = Q.F[k].has(v);
      box.append(h('button', { type: 'button', class: `qf-opt${on ? ' on' : ''}${c ? '' : ' zero'}`, 'aria-pressed': String(on), onclick: () => toggle(k, v) },
        icon || null, h('span', { class: 'qf-t', text: label }), h('span', { class: 'qf-n', text: fmt.int(c) })));
    }
  }
  const sel = [...Q.F.code];
  Q.typeBtn.textContent = `${sel.length ? `${sel.length} request type${sel.length === 1 ? '' : 's'}` : 'Any request type'} ▾`;
  clear(Q.typeChips);
  for (const code of sel) Q.typeChips.append(h('button', { type: 'button', class: 'filterchip qf-chip', onclick: () => toggle('code', code) },
    code, h('span', { class: 'qf-n', text: fmt.int(Q.counts.code.get(code) || 0) }), h('b', { text: '×' })));
  if (!Q.typePop.hidden) drawTypeList();
}

function drawTypeList() {
  if (!Q.loaded) return;
  const q = Q.typeQuery.trim().toLowerCase();
  const names = Object.fromEntries(Q.R.codes);
  const all = new Map(Q.counts.code);
  for (const c of Q.F.code) if (!all.has(c)) all.set(c, 0);
  let list = [...all.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  if (q) list = list.filter(([c]) => c.toLowerCase().includes(q) || String(names[c] || '').toLowerCase().includes(q));
  clear(Q.typeList);
  if (!list.length) { Q.typeList.append(h('p', { class: 'fine', text: 'No request type matches.' })); return; }
  for (const [code, n] of list.slice(0, 120)) {
    const cb = h('input', { type: 'checkbox', checked: Q.F.code.has(code), onchange: () => toggle('code', code) });
    cb.checked = Q.F.code.has(code);
    Q.typeList.append(h('label', { class: 'qf-type', title: names[code] || code }, cb, h('span', { class: 'qf-t', text: code }), h('span', { class: 'qf-n', text: fmt.int(n) })));
  }
}

// ------------------------------------------------------------------ the ranking panel (always visible; weights editable here)
const SLIDERS = [
  ['Life-safety (tier 1)', (W) => W.tier_points, '1', 0, 100, 1, 'points'],
  ['Hazard, not immediate (tier 2)', (W) => W.tier_points, '2', 0, 100, 1, 'points'],
  ['Maintenance (tier 3)', (W) => W.tier_points, '3', 0, 100, 1, 'points'],
  ['Days past the date per point', (W) => W.lateness, 'days_per_point', 1, 60, 1, 'days'],
  ['Most points for lateness', (W) => W.lateness, 'cap', 0, 100, 1, 'points'],
  ['Points per extra report', (W) => W.repeats, 'points_per_extra_report', 0, 30, 1, 'points'],
  ['Most points for repeats', (W) => W.repeats, 'cap', 0, 60, 1, 'points'],
];
function buildRankPanel() {
  const P = Q.rankCard;
  clear(P);
  P.append(h('h2', { text: 'How the ranking works' }));
  Q.formula = h('p', { class: 'hr-formula' });
  P.append(Q.formula);
  Q.sliders = [];
  const box = h('div', { class: 'hr-sliders' });
  for (const [label, obj, key, min, max, step, unit] of SLIDERS) {
    const num = h('input', { type: 'number', min, max, step, class: 'hr-num', 'aria-label': label });
    const rng = h('input', { type: 'range', min, max, step, 'aria-label': label });
    const set = (v) => {
      v = Math.min(max, Math.max(min, Math.round(+v || 0)));
      obj(Q.W)[key] = v; num.value = v; rng.value = v;
      drawFormula();
      soon(() => { rescore(); recompute(); }, 110);
    };
    rng.addEventListener('input', () => set(rng.value));
    num.addEventListener('change', () => set(num.value));
    Q.sliders.push(() => { num.value = obj(Q.W)[key]; rng.value = obj(Q.W)[key]; });
    box.append(h('label', { class: 'hr-row' }, h('span', { class: 'hr-lab' }, label, h('span', { class: 'hr-unit', text: ` (${unit})` })), rng, num));
  }
  P.append(box);
  Q.resetBtn = h('button', { class: 'btn ghost hr-reset', type: 'button', text: 'Reset weights', onclick: () => {
    Q.W = JSON.parse(JSON.stringify(Q.W0)); Q.sliders.forEach((f) => f()); drawFormula(); rescore(); recompute(); } });
  P.append(h('div', { class: 'hr-actions' }, Q.resetBtn, h('span', { class: 'fine', text: 'Changes re-rank this page only.' })));
  Q.sliders.forEach((f) => f());
  drawFormula();
  const W = Q.W0;
  P.append(h('p', { class: 'fine', text: 'Nothing else is used: no text, no demographics, no model. Block neighbours are shown beside a row, not scored.' }),
    h('details', { class: 'hr-types' }, h('summary', { text: 'Which request types are in tiers 1 and 2' }),
      ...['1', '2'].map((t) => h('p', { class: 'fine' }, h('b', { text: `Tier ${t} (${W.tiers[t].short}): ` }), W.tiers[t].codes.join(' · '))),
      h('p', { class: 'fine', text: 'Every other type is tier 3.' }),
      h('p', { class: 'fine', text: `Review first: ${(W.review_first || []).join('; ')}.` })),
    h('p', { class: 'fine' }, 'Default weights: ', h('a', { href: 'data/rank-weights.json', text: 'rank-weights.json' }), '. We don’t know how divisions prioritise today; this is a transparent starting point.'));
}
function drawFormula() {
  const W = Q.W, t = W.tier_points;
  clear(Q.formula);
  const b = (x) => h('b', { text: String(x) });
  Q.formula.append('Score = ', b(t['1']), ' points if the request type is life-safety, ', b(t['2']), ' if a hazard that is not immediate, ', b(t['3']),
    ' otherwise; + 1 point for every ', b(W.lateness.days_per_point), ' days past the date the city gave (at most ', b(W.lateness.cap), '); + ',
    b(W.repeats.points_per_extra_report), ' for each extra open report of the same type at the same address (at most ', b(W.repeats.cap),
    '). Ties go to the request furthest past its date.');
  clear(Q.strip);
  Q.strip.append(h('b', { class: 'qs-k', text: 'How the ranking works: ' }), 'score = ', b(t['1']), ' life-safety, ', b(t['2']), ' hazard, ', b(t['3']),
    ' otherwise + 1 per ', b(W.lateness.days_per_point), ' days past the date (max ', b(W.lateness.cap), ') + ', b(W.repeats.points_per_extra_report),
    ' per extra report (max ', b(W.repeats.cap), '). ', h('button', { class: 'linkish', type: 'button', text: 'Change the weights', onclick: () => {
      Q.rankCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      Q.rankCard.classList.remove('flash'); void Q.rankCard.offsetWidth; Q.rankCard.classList.add('flash');
      setTimeout(() => Q.rankCard.querySelector('input[type=range]')?.focus({ preventScroll: true }), 400);
    } }));
  const changed = JSON.stringify([W.tier_points, W.lateness, W.repeats]) !== JSON.stringify([Q.W0.tier_points, Q.W0.lateness, Q.W0.repeats]);
  Q.rankCard.classList.toggle('edited', changed);
  if (Q.resetBtn) Q.resetBtn.disabled = !changed;
}

// ------------------------------------------------------------------ the map
function blockXY() {
  if (Q.xy) return Q.xy;
  const m = Q.d.map || {};
  Q.xy = new Map();
  for (const d of m.dots || []) Q.xy.set(d[6], [d[0], d[1]]);
  for (const l of Object.values(m.dots_by_div || {})) for (const d of l) if (!Q.xy.has(d[6])) Q.xy.set(d[6], [d[0], d[1]]);
  return Q.xy;
}

function buildMap(P, big = false) {
  const m = Q.d.map || {};
  const base = { x: -10, y: -10, w: m.width + 20, h: m.height + 20 };
  const svg = s('svg', { viewBox: `${base.x} ${base.y} ${base.w} ${base.h}`, preserveAspectRatio: 'xMidYMid meet', role: 'img',
    'aria-label': 'Map of requests past the date the city gave, one dot per block, with ward outlines' });
  Q.svg = svg;
  const gw = s('g');
  for (const w of m.wards || []) gw.append(s('path', { d: w.d, class: 'ward' }));
  Q.wlabs = [];
  for (const w of m.wards || []) {
    const t = s('text', { x: w.label_xy[0], y: w.label_xy[1] + 9, 'text-anchor': 'middle', class: 'wlab' }, String(+w.ward));
    Q.wlabs.push(t); gw.append(t);
  }
  Q.dots = s('g');
  svg.append(gw, Q.dots);
  Q.k = 1;
  const box = h('div', { class: 'q-mapbox' }, svg);
  P.append(box);
  if (!big) {
    const Z = zoomable(svg, base, onZoom);
    box.append(h('div', { class: 'q-zoom', role: 'group', 'aria-label': 'Map zoom' },
      h('button', { type: 'button', 'aria-label': 'Zoom in', title: 'Zoom in', text: '+', onclick: Z.zoomIn }),
      h('button', { type: 'button', 'aria-label': 'Zoom out', title: 'Zoom out', text: '−', onclick: Z.zoomOut }),
      h('button', { type: 'button', 'aria-label': 'Reset the map', title: 'Reset the map', class: 'rs', text: 'Reset', onclick: Z.reset })));
    // one listener for every dot: the tooltip and the block filter
    Q.dots.addEventListener('pointermove', (e) => {
      const c = e.target.closest('circle'); if (!c) return;
      const a = Q.dotInfo?.get(c.dataset.block); if (!a) return;
      showTip(e, [{ head: c.dataset.block }, { value: fmt.int(a.n), label: `request${a.n === 1 ? '' : 's'} past the date${anyFilter() ? ' (filtered)' : ''}` },
        { value: `${fmt.int(a.old)} days`, label: 'the oldest is past it' }, ...(a.t1 ? [{ value: fmt.int(a.t1), label: 'life-safety' }] : [])]);
    });
    Q.dots.addEventListener('pointerleave', hideTip);
    Q.dots.addEventListener('click', (e) => {
      const c = e.target.closest('circle'); if (!c) return;
      const b = c.dataset.block;
      Q.block = Q.block === b ? null : b; Q.shown = PAGE;
      Q.dots.querySelectorAll('circle.sel').forEach((x) => x.classList.remove('sel'));
      if (Q.block) c.classList.add('sel');
      drawList();
    });
  }
  P.append(h('div', { class: 'legend', style: 'margin-top:12px' },
    h('span', { style: 'color:var(--muted)', text: 'Oldest on the block, days past the date:' }),
    ...[0, 1, 2].map((b) => h('span', {}, h('span', { class: 'sw', style: `background:${BIN_COL[b]}` }), BIN_LABEL[b].replace('Up to', 'up to').replace('More', 'more')))));
  if (!big) {
    Q.mapNote = h('p', { class: 'fine', style: 'margin:8px 0 0', text: 'One dot per block, sized by its requests. Scroll or pinch to zoom, drag to pan; click a block to list it.' });
    P.append(Q.mapNote);
  }
}

const rBase = (n) => Math.min(40, 7 * Math.sqrt(n));
function onZoom(k) {
  Q.k = k;
  const f = Math.pow(k, 0.6);
  for (const c of Q.dots.children) c.setAttribute('r', (c._rb / f).toFixed(2));
  const fs = `${(26 / Math.pow(k, 0.8)).toFixed(1)}px`;
  for (const t of Q.wlabs) t.style.fontSize = fs;
}

function drawDots() {
  // before the list's data arrives: the precomputed dots for the division (every past-due request on the block)
  let list;
  if (!Q.loaded) {
    const m = Q.d.map || {};
    list = (Q.div === 'all' ? m.dots || [] : (m.dots_by_div || {})[Q.div] || []).map(([x, y, n, , old, , block]) => ({ x, y, n, old, block, t1: 0 }));
  } else {
    const xy = blockXY();
    const agg = new Map();
    for (const r of Q.filtered) {
      if (!r.block) continue;
      let a = agg.get(r.block);
      if (!a) { const p = xy.get(r.block); if (!p) continue; agg.set(r.block, a = { x: p[0], y: p[1], n: 0, old: 0, t1: 0, block: r.block }); }
      a.n++; if (r.days > a.old) a.old = r.days; if (r.tier === 1) a.t1++;
    }
    list = [...agg.values()];
    if (Q.block && !agg.has(Q.block)) Q.block = null;
  }
  Q.dotInfo = new Map(list.map((a) => [a.block, a]));
  const f = Math.pow(Q.k || 1, 0.6);
  const frag = document.createDocumentFragment();
  for (const a of list.sort((p, q) => q.n - p.n)) {
    const rb = rBase(a.n);
    const c = s('circle', { cx: a.x, cy: a.y, r: (rb / f).toFixed(2), fill: BIN_COL[binOf(a.old)], class: a.block === Q.block ? 'sel' : null, 'data-block': a.block });
    c._rb = rb;
    frag.append(c);
  }
  clear(Q.dots);
  Q.dots.append(frag);
  if (Q.mapNote && Q.loaded) {
    Q.mapNote.textContent = `${fmt.int(list.length)} blocks${anyFilter() ? ' match the filters' : ''}. One dot per block, sized by its requests. Scroll or pinch to zoom, drag to pan; click a block to list it.`;
  }
}

function renderMapCard() {
  // video crop: the map alone, with the headline as its caption
  const root = h('div', { style: 'padding:36px 40px 28px;height:100vh;display:flex;flex-direction:column' });
  root.append(h('div', { style: 'font-size:30px;font-weight:720;letter-spacing:-0.02em;line-height:1.15' },
    h('span', { class: 'headline-key', 'aria-hidden': 'true', style: 'width:16px;height:16px;margin-right:12px' }),
    `${NAMES[Q.div]}: ${ftxt(pastId(Q.div))} requests past the date the city gave`));
  const P = h('div', { class: 'q-map', style: 'flex:1;min-height:0;display:flex;flex-direction:column;padding:16px 0 0;position:static' });
  root.append(P);
  $('#main').append(root);
  buildMap(P, true);
  const box = P.querySelector('.q-mapbox');
  box.style.flex = '1'; box.style.minHeight = '0'; box.style.display = 'flex';
  const svg = P.querySelector('svg');
  svg.style.flex = '1'; svg.style.minHeight = '0'; svg.style.maxHeight = 'none'; svg.style.height = '100%';
  drawDots();
}

// ------------------------------------------------------------------ the list
function buildList() {
  Q.viewSeg = h('div', { class: 'seg small', role: 'group', 'aria-label': 'Order' },
    ...VIEWS.map(([v, t]) => h('button', { type: 'button', 'data-view': v, text: t, onclick: () => { Q.view = v; Q.shown = PAGE; drawDef(); if (Q.loaded) sortRows(); drawList(); } })));
  Q.chip = h('span');
  Q.count = h('span', { class: 'q-count' });
  Q.listCard.append(h('div', { class: 'q-list-head' },
    h('div', { style: 'display:flex;gap:14px;align-items:center;flex-wrap:wrap' }, Q.viewSeg, Q.chip), Q.count));
  // the rule in one line, always in view above the ranked list; the full panel (with the weights) is beside it
  Q.strip = h('div', { class: 'q-strip', hidden: true });
  Q.listCard.append(Q.strip);
  Q.table = h('table', { class: 'q' });
  Q.thead = h('thead');
  Q.tbody = h('tbody');
  Q.table.append(Q.thead, Q.tbody);
  Q.closeBox = h('div', { class: 'closeout', hidden: true });
  Q.more = h('div', { class: 'q-more' });
  Q.scroll = h('div', { class: 'q-scroll' }, Q.table, Q.closeBox, Q.more);
  Q.listCard.append(Q.scroll);
}

function head(cols) {
  clear(Q.thead);
  Q.thead.append(h('tr', {}, ...cols.map((c) => h('th', { text: c }))));
}

function drawCloseout() {
  const C = Q.R?.closeout || { groups: [] };
  const box = Q.closeBox;
  clear(box);
  const inDiv = (g) => (Q.div === 'all' ? g.n : (g.by_division || {})[Q.div] || 0);
  const total = C.groups.reduce((a, g) => a + inDiv(g), 0);
  box.append(h('p', { class: 'co-lead' }, h('b', { text: fmt.int(total) }), ` ${Q.div === 'all' ? '' : NAMES[Q.div] + ' '}records to verify and close (of `, fnum('e7_closeout_n'), ' citywide). Counts only; the records stay in the city’s queue. The filters apply to the listed requests, not to these.'));
  for (const g of C.groups) {
    const n = inDiv(g);
    if (!n) continue;
    const types = g.by_type.filter(([d]) => Q.div === 'all' || d === Q.div);
    const byType = {};
    for (const [, t, k] of types) byType[t] = (byType[t] || 0) + k;
    const top = Object.entries(byType).sort((a, b) => b[1] - a[1]).slice(0, 6);
    box.append(h('div', { class: 'co-group' },
      h('div', { class: 'co-n tnum', text: fmt.int(n) }),
      h('div', {}, h('div', { class: 'co-title', text: g.title }), h('div', { class: 'co-why', text: g.why }),
        h('div', { class: 'co-types', text: top.map(([t, k]) => `${t} ${fmt.int(k)}`).join(' · ') }))));
  }
}

const norm = (x) => String(x || '').toLowerCase().replace(/[^a-z]/g, '');
const same = (a, b) => !a || norm(a) === norm(b);
const listRows = () => (Q.block ? Q.filtered.filter((r) => r.block === Q.block) : Q.filtered);

function drawList() {
  Q.viewSeg.querySelectorAll('button').forEach((b) => b.classList.toggle('on', b.dataset.view === Q.view));
  Q.strip.hidden = !(Q.loaded && Q.view === 'ranked');
  if (!Q.loaded) { clear(Q.tbody); Q.tbody.append(h('tr', {}, h('td', { colspan: 5, class: 'st', text: 'Loading the list…' }))); return; }
  Q.table.hidden = Q.view === 'closeout';
  Q.closeBox.hidden = Q.view !== 'closeout';
  clear(Q.chip);
  if (Q.block && Q.view !== 'closeout') Q.chip.append(h('button', { class: 'filterchip', type: 'button', onclick: () => { Q.block = null; Q.shown = PAGE; drawDots(); drawList(); } }, Q.block, h('b', { text: '×' })));
  clear(Q.more);
  if (Q.view === 'closeout') { Q.count.textContent = ''; drawCloseout(); Q.more.style.display = 'none'; return; }
  const rows = listRows();
  Q.count.textContent = `${fmt.int(rows.length)} request${rows.length === 1 ? '' : 's'}`;
  clear(Q.tbody);
  if (!rows.length) {
    Q.tbody.append(h('tr', {}, h('td', { colspan: 5, class: 'st q-empty' }, 'No request matches these filters. ', h('button', { class: 'linkish', type: 'button', text: 'Clear filters', onclick: clearFilters }))));
    Q.more.style.display = 'none';
    return;
  }
  if (Q.view === 'ranked') drawRanked(rows); else drawOldest(rows);
  if (rows.length > Q.shown) Q.more.append(h('button', { class: 'btn ghost', type: 'button', text: `Show more (${fmt.int(rows.length - Q.shown)} left)`, onclick: () => { Q.shown += PAGE * 2; drawList(); } }));
  Q.more.style.display = rows.length > Q.shown ? '' : 'none';
}

function drawOldest(rows) {
  head(['Days past', 'Type · what the request says', 'Block', 'Due by', 'City status']);
  for (const r of rows.slice(0, Q.shown)) {
    Q.tbody.append(h('tr', {},
      h('td', { class: 'days' }, h('i', { style: `background:${BIN_COL[r.bin]}`, 'aria-hidden': 'true' }), fmt.int(r.days)),
      h('td', { class: 'req' }, h('b', { class: 'typ', text: r.problem_code || r.type_name }),
        same(r.problem_code, r.type_name) ? null : h('span', { class: 'says', text: r.type_name })),
      h('td', { class: 'blk', text: r.block || 'block not recorded' }),
      h('td', { class: 'due', text: fmt.dateShort(r.promised) }),
      h('td', { class: 'st', text: STATUS[r.status] || r.status || '–' })));
  }
}

function drawRanked(rows) {
  head(['Score', 'Type · why this rank', 'Block', 'Due by', 'City status']);
  for (const r of rows.slice(0, Q.shown)) {
    const why = h('span', { class: 'why' });
    whyParts(r).forEach(([t, p], i) => why.append(i ? ' · ' : '', t, ' ', h('b', { class: 'pts', text: `+${p}` })));
    if (r.wo_open) why.append(' · ', h('span', { class: 'tag', text: 'work order open' }));
    if (r.bulk) why.append(' · ', h('span', { class: 'tag', text: 'many reports at one address: check' }));
    if (r.mates) why.append(h('span', { class: 'mates', text: ` · ${r.mates} more on this block` }));
    Q.tbody.append(h('tr', { title: whyText(r) },
      h('td', { class: 'days score' }, h('i', { class: `t${r.tier}`, 'aria-hidden': 'true' }), String(r.score)),
      h('td', { class: 'req' }, h('b', { class: 'typ', text: r.problem_code || r.type_name }), why),
      h('td', { class: 'blk', text: r.block || 'block not recorded' }),
      h('td', { class: 'due', text: fmt.dateShort(r.promised) }),
      h('td', { class: 'st', text: STATUS[r.status] || r.status || '–' })));
  }
}

function downloadCSV() {
  if (!Q.loaded) return;
  const rows = listRows().map((r) => ({ ...r, days_past_promise: r.days, why: whyText(r) }));
  const cols = ['division', 'problem_code', 'type_name', 'ward', 'block', 'filed', 'promised', 'days_past_promise', 'status', 'score', 'tier', 'repeat_n', 'wo_open', 'why'];
  const esc = (v) => (/[",\n]/.test(v ?? '') ? `"${String(v).replace(/"/g, '""')}"` : (v ?? ''));
  const text = [cols.join(','), ...rows.map((r) => cols.map((c) => esc(r[c])).join(','))].join('\n') + '\n';
  const name = Q.div === 'all' ? 'all-divisions' : NAMES[Q.div].toLowerCase().replace(/[^a-z]+/g, '-');
  const a = h('a', { href: URL.createObjectURL(new Blob([text], { type: 'text/csv' })), download: `past-due-${Q.view === 'oldest' ? 'oldest' : 'ranked'}-${name}${anyFilter() || Q.block ? '-filtered' : ''}.csv` });
  document.body.append(a); a.click(); a.remove();
}

// ------------------------------------------------------------------ How this list is built (collapsed)
function howBuilt() {
  const d = Q.d;
  const S = d.saved_search || {};
  const det = h('details', { class: 'how' }, h('summary', { text: 'How this list is built' }));
  const body = h('div', { class: 'how-body' });
  const fval = (id) => state.figures[id]?.value;
  // 1. what the records show, all divisions (E5)
  const mixParts = [['done', 'var(--done)', 'a record shows the work done'], ['pending', 'var(--promise)', 'a city work order is still pending'],
    ['superseded', 'var(--line-2)', 'possibly superseded by a later request'], ['admin', 'var(--line-2)', 'likely an administrative leftover'],
    ['no_record', 'var(--norecord)', 'no record either way']];
  const mix = h('div', { class: 'mix', role: 'img', 'aria-label': 'What the records show for all requests past the date' },
    ...mixParts.map(([k, c]) => h('span', { style: `width:${(fval(`e5_queue_${k}_share`) || 0) * 100}%;background:${c}` })));
  body.append(h('div', {},
    h('h3', {}, 'What the records show, all ', fnum('e3_queue_past_promise'), ' requests'),
    mix,
    h('div', { style: 'display:grid;gap:4px' }, ...mixParts.map(([k, c, t]) => h('div', {}, h('span', { class: 'key', style: `background:${c}` }), fnum(`e5_queue_${k}_share`, { d: 1 }), ` ${t}`))),
    h('p', { style: 'margin-top:10px', text: 'Checked against every completion or work record on disk (mowing ledger, Forestry and sidewalk work orders, board-ups, demolition permits, sampled status pages). A missing record does not mean the work was not done; it means no one can tell. It has been the normal state of the queue every year since 2019.' })));
  // 2. the definition and age
  const hist = h('div', { class: 'hist' });
  const mx = Math.max(...(d.hist || []).map((b) => fval(b.figure_id) || 0), 1);
  for (const b of d.hist || []) {
    hist.append(h('span', { text: b.key === '366+' ? 'over a year' : `${b.key} days` }),
      h('div', {}, h('div', { class: 'hb', style: `width:${(100 * (fval(b.figure_id) || 0)) / mx}%` })),
      h('span', { class: 'tnum', style: 'text-align:right' }, fnum(b.figure_id)));
  }
  body.append(h('div', {}, h('h3', { text: 'What “past the date” means' }), h('p', { text: d.definition || '' }),
    h('h3', { style: 'margin-top:14px', text: 'How far past it, all divisions' }), hist));
  // 3. the saved search and the SQL
  body.append(h('div', {}, h('h3', { text: 'The same list as a Cityworks saved search' }),
    h('dl', {}, h('dt', { text: 'Layer' }), h('dd', {}, h('a', { href: S.url, text: S.layer })),
      h('dt', { text: 'Where' }), h('dd', {}, h('pre', { text: S.expression })),
      h('dt', { text: 'Group by' }), h('dd', { text: S.group_by }),
      h('dt', { text: 'Order by' }), h('dd', { text: S.order_by })),
    h('h3', { style: 'margin-top:14px', text: 'From the public 311 file (DuckDB SQL)' }), h('pre', { text: S.public_sql }),
    h('p', { style: 'margin-top:10px' }, h('a', { href: d.csv || 'data/downloads/queue.csv', download: '', text: 'Every division, every row (CSV, block level)' }))));
  // 4. the city's own queue agrees; privacy
  body.append(h('div', {}, h('h3', { text: 'The city’s own active queue agrees' }),
    h('p', {}, 'Cityworks layer 18 (“Active SRs”) holds ', fnum('e3_queue_qe_past_promise_2025'), ' requests filed since 2025 past their date, for ',
      fnum('e3_queue_qe_codes'), ' request types (the public file, a day earlier: ', fnum('e3_queue_public_same_types'), '). The dates agree on ',
      fnum('e3_queue_qe_promise_match'), ' of ', fnum('e3_queue_qe_promise_both'), '. Read once; operational fields only; rows not published.'),
    h('h3', { style: 'margin-top:14px', text: 'Privacy' }),
    h('p', {}, 'Block level only: no request numbers, no house numbers. ', fnum('e3_queue_sensitive_excluded'),
      ' requests of sensitive types are counted in the totals and kept off the map, the list and the CSV. Each dot sits at the block’s centre (the mean of every request ever filed on it), snapped to a ',
      String((d.map || {}).grid_m || 60), ' m grid.')));
  det.append(body);
  return det;
}

main();
