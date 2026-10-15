// E6 "Forestry's list": what a division head opens on Monday. One division at a time (Forestry first), one headline,
// the block-level map, the list oldest first. Counts are registered figures (e3_queue_*, e5_*); the map dots and
// the list rows are rows of the same query (scripts/exec/E3/build_queue.py), block level, no request numbers.
// Everything explanatory sits behind "How this list is built".
// E7: three views of the same list. Ranked (default) scores each request by the hazard of its type, days past the
// date and repeat reports (data/ranked.json from scripts/exec/E7/rank.py; weights in data/rank-weights.json, applied
// here so a division can edit them); Oldest first is the list as before; Close-out holds the records with evidence
// they are done, superseded or administrative (counts only). Design: research/prioritisation-option.md.
import { state, h, $, clear, fmt, fig, bindTip, load } from './common.js';
import { s } from './charts.js';
import { boot, finish, card, params, ftxt, fval, fnum, page } from './app.js';

const MAIN = [['FORESTRY', 'Forestry'], ['STREET DEPT, 510', 'Streets'], ['BUILDING DIV', 'Building Division'], ['LRA', 'Land bank (LRA)'],
  ['WATER DIV', 'Water Division'], ['TRAFFIC DIVISION, 511', 'Traffic']];
const OTHER = [['VECTOR CNTRL', 'Vector Control'], ['Tornado, Recovery', 'Tornado recovery'], ['BLDG LEAD INSP', 'Lead inspection'],
  ['BLDG TRADES', 'Building trades'], ['CITY EMRGCY MNG', 'Emergency management'], ['TREAS PRKG SVC', 'Treasurer, parking'], ['all', 'All divisions']];
const NAMES = Object.fromEntries([...MAIN, ...OTHER]);
const STATUS = { Disptch: 'Dispatched', NEW: 'New', Pending: 'Pending', Inspect: 'Inspection', SCHEDULED: 'Scheduled', Reinsp: 'Reinspection',
  Letter: 'Letter sent', 'ON HOLD': 'On hold', Extended: 'Extended', Refer: 'Referred', Hearing: 'Hearing', 'BPS APPROVED': 'Approved' };
// age on the map: three steps of the late gold (bucket index from build_queue.py: 0-30, 31-90, 91-180, 181-365, 366+)
const STEP = ['var(--late-1)', 'var(--late-1)', 'var(--late-2)', 'var(--late-2)', 'var(--late-3)'];
const STEP_LABEL = [['var(--late-1)', 'up to 90 days'], ['var(--late-2)', '91 to 365 days'], ['var(--late-3)', 'more than a year']];
const dayStep = (d) => (d > 365 ? 4 : d > 90 ? 2 : 0);
const PAGE = 60;

const VIEWS = [['oldest', 'Oldest first'], ['ranked', 'Ranked'], ['closeout', 'Close-out']];
const Q = { div: 'FORESTRY', block: null, shown: PAGE, rows: [], view: 'ranked', ranked: [] };

async function main() {
  await boot('queue.html', 'Forestry’s list');
  Q.d = await load('queue');
  const want = params.get('div');
  if (want && (NAMES[want])) Q.div = want;
  if (VIEWS.some(([v]) => v === params.get('view'))) Q.view = params.get('view');
  if (card === 'map') { renderMapCard(); finish(); return; }
  // draw the headline and the map at once; the list fills in when its data (about 1-2 MB) has arrived
  render();
  const [csv, R, W] = await Promise.all([fetch(Q.d.csv || 'data/downloads/queue.csv').then((r) => r.text()), load('ranked'),
    fetch('data/rank-weights.json', { cache: 'no-cache' }).then((r) => r.json())]);
  Q.rows = parseCSV(csv);
  Q.R = R; Q.W = W;
  Object.assign(state.figures, R.figures || {});           // e7_* figures, registered in build/E7/figures.json
  Q.ranked = rankRows(R, W);
  Q.loaded = true;
  buildHowRank();
  if (params.get('how')) toggleHow(true);
  drawList();
  finish();
}

// ------------------------------------------------------------------ the score (the same rule as scripts/exec/E7/rank.py)
function tierOf(code, W) {
  const o = (W.tier_overrides || {})[code];
  if (o) return +o;
  if ((W.tiers['1'].codes || []).includes(code)) return 1;
  if ((W.tiers['2'].codes || []).includes(code)) return 2;
  return 3;
}
function rankRows(R, W) {
  const c = Object.fromEntries(R.cols.map((k, i) => [k, i]));
  const out = R.rows.map((x) => {
    const [code, name] = R.codes[x[c.code_i]];
    const days = x[c.days], n = x[c.repeat_n], tier = tierOf(code, W);
    const H = W.tier_points[String(tier)];
    const D = Math.min(Math.floor(days / W.lateness.days_per_point), W.lateness.cap);
    const Rp = Math.min(W.repeats.points_per_extra_report * (n - 1), W.repeats.cap);
    return { division: R.divisions[x[c.division_i]], problem_code: code, type_name: name, block: x[c.block], ward: x[c.ward],
      filed: x[c.filed], promised: x[c.promised], days, status: x[c.status], repeat_n: n, mates: x[c.block_mates], wo_open: !!x[c.wo_open],
      tier, H, D, R: Rp, score: H + D + Rp, bulk: n > (W.bulk_check_over || 10) };
  });
  return out.sort((a, b) => b.score - a.score || b.days - a.days);
}
const times = (n) => (n === 2 ? 'twice' : `${n} times`);
function whyParts(r) {
  const W = Q.W;
  const parts = [[`${W.tiers[String(r.tier)].short}`, r.H], [`${fmt.int(r.days)} days past the date`, r.D]];
  if (r.repeat_n > 1) parts.push([`reported ${times(r.repeat_n)}`, r.R]);
  return parts;
}
function whyText(r) {
  const bits = whyParts(r).map(([t, p]) => `${t} \u00b7 +${p}`);
  if (r.wo_open) bits.push('work order open');
  if (r.bulk) bits.push('many reports at one address: check');
  if (r.mates) bits.push(`${r.mates} more overdue on this block`);
  return bits.join(' \u00b7 ');
}

// ------------------------------------------------------------------ CSV (quoted fields; the bridge writes RFC 4180)
function parseCSV(text) {
  const out = []; let row = [], f = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
    else if (c === '"') q = true;
    else if (c === ',') { row.push(f); f = ''; }
    else if (c === '\n') { row.push(f); out.push(row); row = []; f = ''; }
    else if (c !== '\r') f += c;
  }
  if (f || row.length) { row.push(f); out.push(row); }
  const [head, ...rest] = out;
  return rest.filter((r) => r.length === head.length).map((r) => Object.fromEntries(head.map((k, i) => [k, r[i]])));
}

const divInfo = (div) => (Q.d.divisions || []).find((x) => x.division === div);
const pastId = (div) => (div === 'all' ? 'e3_queue_past_promise' : divInfo(div)?.figures.past);

// ------------------------------------------------------------------ page
function render() {
  const root = page();
  Q.seg = h('div', { class: 'seg', role: 'group', 'aria-label': 'Division' });
  Q.dl = h('button', { class: 'btn ghost', type: 'button', onclick: downloadCSV });
  root.append(h('div', { class: 'q-top' }, Q.seg, Q.dl));
  Q.head = h('div', { class: 'q-head' });
  root.append(Q.head);
  Q.mapCard = h('div', { class: 'card q-map' });
  Q.listCard = h('div', { class: 'card q-list' });
  root.append(h('div', { class: 'q-grid' }, Q.mapCard, Q.listCard));
  root.append(howBuilt());
  buildPicker();
  buildMap(Q.mapCard);
  buildList();
  update();
  fit();
  window.addEventListener('resize', fit);
}

// On a wide screen the map and the list share one viewport: the map takes the height left under the headline
// and its width follows the city's shape; the list scrolls inside its card.
function fit() {
  const grid = Q.mapCard.parentElement;
  const svg = Q.mapCard.querySelector('svg');
  if (window.innerWidth < 1180) { grid.style.gridTemplateColumns = ''; svg.style.height = ''; Q.listCard.querySelector('.q-scroll').style.maxHeight = ''; return; }
  const top = grid.getBoundingClientRect().top + window.scrollY;
  const H = Math.max(560, window.innerHeight - top - 28);
  const m = Q.d.map || {};
  const extra = Q.mapCard.offsetHeight - svg.getBoundingClientRect().height;
  const sh = H - extra;
  svg.style.height = `${sh}px`;
  svg.style.maxHeight = 'none';
  const w = Math.round(sh * (m.width + 20) / (m.height + 20)) + 36;
  grid.style.gridTemplateColumns = `${Math.max(340, w)}px 1fr`;
  Q.listCard.style.height = `${H}px`;
  Q.listCard.style.display = 'flex'; Q.listCard.style.flexDirection = 'column';
  const sc = Q.listCard.querySelector('.q-scroll');
  sc.style.maxHeight = 'none'; sc.style.flex = '1'; sc.style.minHeight = '0';
}

function buildPicker() {
  for (const [div, label] of MAIN) Q.seg.append(h('button', { type: 'button', 'data-div': div, text: label, onclick: () => pickDiv(div) }));
  // "Other": a small menu (a native select sizes itself to its longest option)
  Q.menu = h('div', { class: 'menu', role: 'menu', hidden: true }, ...OTHER.map(([v, t]) => h('button', { type: 'button', role: 'menuitem', 'data-div': v, text: t,
    onclick: () => { Q.menu.hidden = true; pickDiv(v); } })));
  Q.other = h('button', { type: 'button', class: 'other', 'aria-haspopup': 'menu', text: 'Other \u25BE', onclick: (e) => { e.stopPropagation(); Q.menu.hidden = !Q.menu.hidden; } });
  document.addEventListener('click', () => { Q.menu.hidden = true; });
  Q.seg.append(h('span', { class: 'menu-wrap' }, Q.other, Q.menu));
}

function pickDiv(div) { Q.div = div; Q.block = null; Q.shown = PAGE; update(); }

function update() {
  Q.seg.querySelectorAll('button[data-div]').forEach((b) => b.classList.toggle('on', b.dataset.div === Q.div));
  const inOther = OTHER.some(([v]) => v === Q.div);
  Q.other.textContent = `${inOther ? NAMES[Q.div] : 'Other'} \u25BE`;
  Q.other.classList.toggle('on', inOther);
  Q.dl.textContent = `Download ${Q.div === 'all' ? 'the full list' : NAMES[Q.div] + '’s list'} (CSV)`;
  // headline + definition
  clear(Q.head);
  Q.head.append(h('h1', { class: 'headline' }, h('span', { class: 'headline-key', 'aria-hidden': 'true' }),
    `${NAMES[Q.div]}: `, h('span', { class: 'num' }, fnum(pastId(Q.div))), ' requests past the date the city gave'));
  Q.def = h('p', { class: 'q-def' });
  Q.head.append(Q.def);
  drawDef();
  drawDots();
  drawList();
}

function drawDef() {
  clear(Q.def);
  if (Q.div === 'all' && Q.view !== 'ranked') Q.def.append('Still open after the date the city set; for ', fnum('e5_queue_no_record_share'), ' of them, no record says whether the work was done.');
  else if (Q.view === 'ranked') Q.def.append('Still open after the date the city set, ranked by the hazard of the request type, how far past the date it is, and repeat reports.');
  else if (Q.view === 'closeout') Q.def.append('Records with evidence the work is done, superseded or paperwork: a desk can verify and close them, no crew needed.');
  else Q.def.append('Still open after the completion date the city set (\u201cDept Response Due By\u201d), oldest first, by block.');
  const u = new URL(location.href);
  if (Q.div !== 'FORESTRY') u.searchParams.set('div', Q.div); else u.searchParams.delete('div');
  if (Q.view !== 'ranked') u.searchParams.set('view', Q.view); else u.searchParams.delete('view');
  history.replaceState(null, '', u);
}

// ------------------------------------------------------------------ the map
function buildMap(P, big = false) {
  const m = Q.d.map || {};
  const svg = s('svg', { viewBox: `-10 -10 ${m.width + 20} ${m.height + 20}`, preserveAspectRatio: 'xMidYMid meet', role: 'img',
    'aria-label': 'Map of requests past the date the city gave, one dot per block, with ward outlines' });
  const gw = s('g');
  for (const w of m.wards || []) gw.append(s('path', { d: w.d, class: 'ward' }));
  for (const w of m.wards || []) gw.append(s('text', { x: w.label_xy[0], y: w.label_xy[1] + 9, 'text-anchor': 'middle', class: 'wlab' }, String(+w.ward)));
  Q.dots = s('g');
  svg.append(gw, Q.dots);
  P.append(svg);
  P.append(h('div', { class: 'legend', style: 'margin-top:12px' },
    h('span', { style: 'color:var(--muted)', text: 'Days past the date:' }),
    ...STEP_LABEL.map(([c, t]) => h('span', {}, h('span', { class: 'sw', style: `background:${c}` }), t))));
  if (!big) P.append(h('p', { class: 'fine', style: 'margin:8px 0 0', text: 'One dot per block, sized by its requests. Click a block to list them.' }));
}

function drawDots() {
  const m = Q.d.map || {};
  const list = Q.div === 'all' ? m.dots || [] : (m.dots_by_div || {})[Q.div] || [];
  clear(Q.dots);
  const r = (n) => Math.min(40, 7 * Math.sqrt(n));
  for (const [x, y, n, bi, oldest, ward, block] of [...list].sort((a, b) => b[2] - a[2])) {
    const c = s('circle', { cx: x, cy: y, r: r(n), fill: STEP[bi], tabindex: 0, class: block === Q.block ? 'sel' : null, 'data-block': block });
    bindTip(c, () => [{ head: block }, { value: fmt.int(n), label: `request${n === 1 ? '' : 's'} past the date` }, { value: `${fmt.int(oldest)} days`, label: 'the oldest is past it' }]);
    const go = () => { Q.block = Q.block === block ? null : block; Q.shown = PAGE; drawDots(); drawList(); };
    c.addEventListener('click', go);
    c.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(); });
    Q.dots.append(c);
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
  const svg = P.querySelector('svg');
  svg.style.flex = '1'; svg.style.minHeight = '0'; svg.style.maxHeight = 'none';
  drawDots();
}

// ------------------------------------------------------------------ the list
function buildList() {
  Q.viewSeg = h('div', { class: 'seg small', role: 'group', 'aria-label': 'Order' },
    ...VIEWS.map(([v, t]) => h('button', { type: 'button', 'data-view': v, text: t, onclick: () => { Q.view = v; Q.shown = PAGE; drawDef(); drawList(); } })));
  Q.chip = h('span');
  Q.howBtn = h('button', { class: 'linkish', type: 'button', 'aria-expanded': 'false', text: 'How the ranking works', onclick: () => toggleHow() });
  Q.listCard.append(h('div', { class: 'q-list-head' },
    h('div', { style: 'display:flex;gap:14px;align-items:center;flex-wrap:wrap' }, Q.viewSeg, Q.chip), Q.howBtn));
  Q.howPanel = h('div', { class: 'how-rank', hidden: true });
  Q.listCard.append(Q.howPanel);
  Q.table = h('table', { class: 'q' });
  Q.thead = h('thead');
  Q.tbody = h('tbody');
  Q.table.append(Q.thead, Q.tbody);
  Q.closeBox = h('div', { class: 'closeout', hidden: true });
  Q.more = h('div', { class: 'q-more' });
  Q.listCard.append(h('div', { class: 'q-scroll' }, Q.table, Q.closeBox, Q.more));
}

function toggleHow(open) {
  const o = open ?? Q.howPanel.hidden;
  Q.howPanel.hidden = !o;
  Q.howBtn.setAttribute('aria-expanded', String(o));
  Q.howBtn.textContent = o ? 'Hide how the ranking works' : 'How the ranking works';
}

function buildHowRank() {
  const W = Q.W;
  const P = Q.howPanel;
  clear(P);
  const tierRow = (t) => h('div', { class: 'hr-tier' }, h('b', { text: `+${W.tier_points[t]}` }), h('span', {}, h('b', { text: `Tier ${t}: ` }), W.tiers[t].label));
  const types = h('details', { class: 'hr-types' }, h('summary', { text: 'Which request types are in tiers 1 and 2' }),
    ...['1', '2'].map((t) => h('p', { class: 'fine' }, h('b', { text: `Tier ${t}: ` }), W.tiers[t].codes.join(' \u00b7 '))),
    h('p', { class: 'fine', text: 'Every other type is tier 3.' }));
  P.append(h('div', { class: 'hr-grid' },
    h('div', {}, h('h3', { text: 'Score = hazard of the request type + lateness + repeats' }),
      tierRow('1'), tierRow('2'), tierRow('3'),
      h('div', { class: 'hr-tier' }, h('b', { text: `+1` }), h('span', { text: `per ${W.lateness.days_per_point} days past the date the city gave, up to +${W.lateness.cap} (a year late counts as one tier)` })),
      h('div', { class: 'hr-tier' }, h('b', { text: `+${W.repeats.points_per_extra_report}` }), h('span', { text: `per extra open report of the same type at the same address, up to +${W.repeats.cap}` })),
      h('p', { class: 'fine', text: 'Ties go to the request furthest past its date. Nothing else is used: no text, no demographics, no model. Block neighbours are shown beside a row, not scored.' }), types),
    h('div', {}, h('h3', { text: 'Before ranking' }),
      h('p', {}, fnum('e7_closeout_n'), ' records with evidence the work is done, superseded or administrative go to Close-out, so the ranked list holds ', fnum('e7_ranked_n'), ' requests.'),
      h('h3', { style: 'margin-top:14px', text: 'A starting point' }),
      h('p', { text: 'We don\u2019t know how divisions prioritise today; if your system lacks a ranking, this is a transparent starting point. Edit rank-weights.json to re-weight.' }),
      h('p', { class: 'fine', text: `Review first: ${(W.review_first || []).join('; ')}.` }))));
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
  box.append(h('p', { class: 'co-lead' }, h('b', { text: fmt.int(total) }), ` ${Q.div === 'all' ? '' : NAMES[Q.div] + ' '}records to verify and close (of `, fnum('e7_closeout_n'), ' citywide). Counts only; the records stay in the city\u2019s queue.'));
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
        h('div', { class: 'co-types', text: top.map(([t, k]) => `${t} ${fmt.int(k)}`).join(' \u00b7 ') }))));
  }
}

const norm = (x) => String(x || '').toLowerCase().replace(/[^a-z]/g, '');
const same = (a, b) => !a || norm(a) === norm(b);
const divRows = () => (Q.div === 'all' ? Q.rows : Q.rows.filter((r) => r.division === Q.div));

function drawList() {
  Q.viewSeg.querySelectorAll('button').forEach((b) => b.classList.toggle('on', b.dataset.view === Q.view));
  Q.howBtn.style.visibility = Q.view === 'ranked' ? '' : 'hidden';
  if (Q.view !== 'ranked') toggleHow(false);
  if (!Q.loaded) { clear(Q.tbody); Q.tbody.append(h('tr', {}, h('td', { colspan: 5, class: 'st', text: 'Loading the list\u2026' }))); return; }
  Q.table.hidden = Q.view === 'closeout';
  Q.closeBox.hidden = Q.view !== 'closeout';
  clear(Q.chip);
  if (Q.block && Q.view !== 'closeout') Q.chip.append(h('button', { class: 'filterchip', type: 'button', onclick: () => { Q.block = null; drawDots(); drawList(); } }, Q.block, h('b', { text: '\u00d7' })));
  clear(Q.more);
  if (Q.view === 'closeout') { drawCloseout(); Q.more.style.display = 'none'; return; }
  if (Q.view === 'ranked') { drawRanked(); return; }
  head(['Days past', 'Type \u00b7 what the request says', 'Block', 'Due by', 'City status']);
  let rows = divRows();
  if (Q.block) rows = rows.filter((r) => r.block === Q.block);
  rows = [...rows].sort((a, b) => b.days_past_promise - a.days_past_promise);
  clear(Q.tbody);
  for (const r of rows.slice(0, Q.shown)) {
    const d = +r.days_past_promise;
    Q.tbody.append(h('tr', {},
      h('td', { class: 'days' }, h('i', { style: `background:${STEP[dayStep(d)]}`, 'aria-hidden': 'true' }), fmt.int(d)),
      h('td', { class: 'req' }, h('b', { class: 'typ', text: r.problem_code || r.type_name }),
        same(r.problem_code, r.type_name) ? null : h('span', { class: 'says', text: r.type_name })),
      h('td', { class: 'blk', text: r.block || 'block not recorded' }),
      h('td', { class: 'due', text: fmt.dateShort(r.promised) }),
      h('td', { class: 'st', text: STATUS[r.status] || r.status || '–' })));
  }
  more(rows.length);
}

function more(n) {
  if (n > Q.shown) Q.more.append(h('button', { class: 'btn ghost', type: 'button', text: 'Show more', onclick: () => { Q.shown += PAGE * 2; drawList(); } }));
  Q.more.style.display = n > Q.shown ? '' : 'none';
}

function drawRanked() {
  head(['Score', 'Type \u00b7 why this rank', 'Block', 'Due by', 'City status']);
  let rows = Q.div === 'all' ? Q.ranked : Q.ranked.filter((r) => r.division === Q.div);
  if (Q.block) rows = rows.filter((r) => r.block === Q.block);
  clear(Q.tbody);
  for (const r of rows.slice(0, Q.shown)) {
    const why = h('span', { class: 'why' });
    whyParts(r).forEach(([t, p], i) => why.append(i ? ' \u00b7 ' : '', t, ' ', h('b', { class: 'pts', text: `+${p}` })));
    if (r.wo_open) why.append(' \u00b7 ', h('span', { class: 'tag', text: 'work order open' }));
    if (r.bulk) why.append(' \u00b7 ', h('span', { class: 'tag', text: 'many reports at one address: check' }));
    if (r.mates) why.append(h('span', { class: 'mates', text: ` \u00b7 ${r.mates} more on this block` }));
    Q.tbody.append(h('tr', { title: whyText(r) },
      h('td', { class: 'days score' }, h('i', { class: `t${r.tier}`, 'aria-hidden': 'true' }), String(r.score)),
      h('td', { class: 'req' }, h('b', { class: 'typ', text: r.problem_code || r.type_name }), why),
      h('td', { class: 'blk', text: r.block || 'block not recorded' }),
      h('td', { class: 'due', text: fmt.dateShort(r.promised) }),
      h('td', { class: 'st', text: STATUS[r.status] || r.status || '\u2013' })));
  }
  more(rows.length);
}

function downloadCSV() {
  const ranked = Q.view === 'ranked' && Q.loaded;
  const rows = ranked ? (Q.div === 'all' ? Q.ranked : Q.ranked.filter((r) => r.division === Q.div)).map((r) => ({ ...r, days_past_promise: r.days, why: whyText(r) })) : divRows();
  const cols = ranked ? ['division', 'problem_code', 'type_name', 'ward', 'block', 'filed', 'promised', 'days_past_promise', 'status', 'score', 'tier', 'repeat_n', 'why']
    : ['division', 'problem_code', 'type_name', 'ward', 'block', 'filed', 'promised', 'days_past_promise', 'status'];
  const esc = (v) => (/[",\n]/.test(v ?? '') ? `"${String(v).replace(/"/g, '""')}"` : (v ?? ''));
  const text = [cols.join(','), ...rows.map((r) => cols.map((c) => esc(r[c])).join(','))].join('\n') + '\n';
  const a = h('a', { href: URL.createObjectURL(new Blob([text], { type: 'text/csv' })), download: `list-${ranked ? 'ranked-' : ''}${Q.div === 'all' ? 'all-divisions' : NAMES[Q.div].toLowerCase().replace(/[^a-z]+/g, '-')}.csv` });
  document.body.append(a); a.click(); a.remove();
}

// ------------------------------------------------------------------ How this list is built (collapsed)
function howBuilt() {
  const d = Q.d;
  const S = d.saved_search || {};
  const det = h('details', { class: 'how' }, h('summary', { text: 'How this list is built' }));
  const body = h('div', { class: 'how-body' });
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
      fnum('e3_queue_qe_promise_match'), ' of ', fnum('e3_queue_qe_promise_both'), '. Read once with the city’s authorisation; operational fields only; rows not published.'),
    h('h3', { style: 'margin-top:14px', text: 'Privacy' }),
    h('p', {}, 'Block level only: no request numbers, no house numbers. ', fnum('e3_queue_sensitive_excluded'),
      ' requests of sensitive types are counted in the totals and kept off the map, the list and the CSV. Each dot sits at the block’s centre (the mean of every request ever filed on it), snapped to a ',
      String((d.map || {}).grid_m || 60), ' m grid.')));
  det.append(body);
  return det;
}

main();
