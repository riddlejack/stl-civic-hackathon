// CityStat, corrected: the nine 311 measures CityStat publishes, laid out as its department pages lay them out, each with
// two added series. "Published" is CityStat's own chart value (reported); "Rebuilt" is the same measure from the city's
// open 311 file (observed); "Closing says done" counts a request on time only when its closing words say the work was
// done (derived; per research/closure-class-review.md: not graded against each request's promise date, not a record of
// work done). Quarterly values: data/citystat_series.json (scripts/exec/citystat-clone/build_series.py). The lead chart
// and the summary table use registered figures: e3_citystat_<m>_q2_published, n4_q2_2026_<m>_ours,
// e3_citystat_<m>_q2_done_on_time.
import { h, $, fig, load, fmt, showTip, hideTip } from './common.js';
import { s } from './charts.js';
import { boot, finish, card, fnum, fval, pct1, page } from './app.js';

const LEAD = 'debris_alley_street';
const pubId = (m) => `e3_citystat_${m}_q2_published`;
const doneId = (m) => `e3_citystat_${m}_q2_done_on_time`;
const LATEST = '2026 Q2';
const SERIES = [
  { key: 'published', name: 'CityStat published', cls: 'pub' },
  { key: 'rebuilt', name: 'Rebuilt from the 311 file', cls: 'reb' },
  { key: 'says_done', name: 'Closing says done', cls: 'done' },
];
const splitLabel = (l) => {
  const m = String(l).match(/^(.*?),?\s+((?:repaired|cleaned|completed|within)\b.*)$/);
  return m ? [m[1], m[2]] : [l, ''];
};

async function main() {
  await boot('citystat.html', 'CityStat, corrected');
  const [sb, cs] = await Promise.all([load('scoreboard'), load('citystat_series')]);
  const metrics = sb?.citystat?.metrics || [];
  const lead = metrics.find((m) => m.metric === LEAD);
  if (card === 'chart') {
    const box = h('div', { class: 'cs-chart', style: 'padding:44px 56px' });
    $('#main').append(box);
    chart(box, lead, true);
    finish();
    return;
  }
  const root = page(
    h('h1', { class: 'title', text: 'CityStat, corrected' }),
    h('p', { class: 'say', text: 'Every 311 measure the mayor’s CityStat publishes, laid out as its department pages lay them out. Each chart keeps CityStat’s own quarterly values and adds two lines: the same measure rebuilt from the city’s open 311 file, and the share on time whose closing words say the work was done.' }));

  // the lead chart, and how to read the rest
  const chartCard = h('div', { class: 'card cs-chart' });
  chart(chartCard, lead, false);
  root.append(h('div', { class: 'cs-grid cs-lead' }, chartCard, guide(sb.citystat, cs)));

  // the clone: department by department, as CityStat groups them
  for (const d of cs.departments) root.append(department(d, cs));

  // the summary table and the downloads
  const tableCard = h('div', { class: 'card cs-table' });
  table(tableCard, [lead, ...metrics.filter((m) => m !== lead)]);
  root.append(h('section', { class: 'cs-dept' },
    h('div', { class: 'cs-dept-head' }, h('h2', { text: 'All nine measures, Q2 2026' })),
    tableCard,
    h('p', { class: 'cs-next', text: 'With work orders linked, this column becomes done by the promised date.' })));
  root.append(h('div', { class: 'cs-actions' },
    h('a', { class: 'btn ghost', href: 'data/downloads/measures.sql', download: '', text: 'Download the SQL' }),
    h('a', { class: 'btn ghost', href: 'data/downloads/closure_class.sql', download: '', text: 'Closing-word classes (SQL)' }),
    h('a', { class: 'btn ghost', href: 'data/downloads/scoreboard.csv', download: '', text: 'Every request type (CSV)' }),
    h('a', { class: 'btn ghost', href: 'data/citystat_series.json', download: '', text: 'These charts’ data (JSON)' })));
  root.append(about(sb.citystat));
  finish();
}

// ------------------------------------------------------------------ the lead chart: published vs closing says done
function chart(box, m, big) {
  const pair = fig('e3_citystat_debris_published_vs_done')?.value || {};
  box.append(h('h2', { text: 'Alley and street debris, cleaned within 3 days' }),
    h('p', { class: 'sub', text: 'Requests filed April to June 2026 (Q2), share closed within the goal' }));
  const bars = [
    { label: 'On time, as CityStat published it', v: fval(pubId(m.metric)), color: 'var(--promise)' },
    { label: 'Closing says it was cleaned, within 3 days', v: fval(doneId(m.metric)), color: 'var(--done)' },
  ];
  const W = 760, L = 0, R = 150, bh = big ? 70 : 64, gap = big ? 80 : 74, top = 34;
  const H = top + bars.length * (bh + gap) + 10;
  const x = (v) => L + v * (W - L - R);
  const svg = s('svg', { viewBox: `0 -4 ${W} ${H + 34}`, role: 'img', 'aria-label': `CityStat published ${pct1(bars[0].v)} on time; closing says it was cleaned, within 3 days, ${pct1(bars[1].v)}` });
  svg.append(s('line', { x1: x(0), x2: x(1), y1: H - 4, y2: H - 4, class: 'axis' }));
  for (const t of [0, 0.25, 0.5, 0.75, 1]) {
    svg.append(s('line', { x1: x(t), x2: x(t), y1: H - 4, y2: H + 2, class: 'axis' }),
      s('text', { x: x(t), y: H + 22, 'text-anchor': t === 0 ? 'start' : 'middle', class: 'tick' }, `${t * 100}%`));
  }
  svg.append(s('line', { x1: x(0), x2: x(0), y1: top - 6, y2: H - 4, class: 'axis' }));
  bars.forEach((b, i) => {
    const y = top + i * (bh + gap) + 26;
    const x1 = x(b.v || 0), r = 6;
    svg.append(s('text', { x: L, y: y - 12, class: 'lbl' }, b.label),
      s('path', { d: `M${L},${y}H${x1 - r}Q${x1},${y} ${x1},${y + r}V${y + bh - r}Q${x1},${y + bh} ${x1 - r},${y + bh}H${L}Z`, fill: b.color }),
      s('text', { x: x1 + 16, y: y + bh / 2 + 18, class: 'val' }, pct1(b.v)));
  });
  if (!big) svg.classList.add('grow');
  box.append(svg);
  box.append(h('p', { class: 'sub', style: 'margin-top:26px' }, 'Rebuilt from the city’s 311 file, the published grade comes out at ',
    fnum('e3_citystat_debris_published_vs_done', { text: pct1(pair.rebuilt) }), '.'));
  if (!big) box.append(source('Street Division'));
}

// ------------------------------------------------------------------ how to read the charts
function guide(C, cs) {
  const n = Object.keys(cs.measures).length, qs = cs.quarters;
  return h('div', { class: 'card cs-guide' },
    h('h2', { text: 'How to read each chart' }),
    h('ul', { class: 'cs-key' },
      h('li', {}, swatch('pub'), h('b', { text: 'CityStat published. ' }), 'Columns, as CityStat draws them: its own quarterly value, read from its charts on 13 October 2026. CityStat has not published Q3 2026.'),
      h('li', {}, swatch('reb'), h('b', { text: 'Rebuilt. ' }), 'The same measure computed from the city’s open 311 file. It lands within five points of CityStat on ',
        fnum(C.within5_figure, { text: '76 of 81' }), ' published quarters, so the method is CityStat’s own.'),
      h('li', {}, swatch('done'), h('b', { text: 'Closing says done. ' }), 'On time only when the closing words say the work was done. Closings whose words record a hand-off, a referral or no action do not count. Same requests, same goal.'),
      h('li', {}, swatch('goal'), h('b', { text: 'Goal. ' }), 'CityStat’s on-time target for the measure.')),
    h('p', { class: 'cs-cover', text: `${n} measures, ${qs[0]} to ${qs[qs.length - 1]}, by the quarter a request was filed. Hover a quarter for its three values.` }));
}
const swatch = (cls) => h('span', { class: `cs-sw ${cls}`, 'aria-hidden': 'true' });

// ------------------------------------------------------------------ one CityStat department page
function department(d, cs) {
  const sec = h('section', { class: 'cs-dept', id: d.id });
  sec.append(h('div', { class: 'cs-dept-head' },
    h('h2', { text: d.name }),
    h('a', { class: 'cs-src-link', href: d.page, target: '_blank', rel: 'noopener', text: `CityStat page ${d.path}` })));
  const grid = h('div', { class: 'cs-cards' });
  for (const c of d.charts) for (const id of c.measures) grid.append(measureCard(cs.measures[id], c, d));
  sec.append(grid);
  return sec;
}

function measureCard(M, c, d) {
  const by = Object.fromEntries(M.series.map((r) => [r.quarter, r]));
  const L = by[LATEST], Q3 = by['2026 Q3'];
  const box = h('article', { class: 'card cs-m', id: M.id });
  box.append(
    h('p', { class: 'cs-kick', text: c.measures.length > 1 ? `${c.title} · one of ${c.measures.length} in CityStat’s chart` : c.title }),
    h('h3', { text: M.name }),
    h('p', { class: 'cs-goal', text: `Goal: ${M.goal}, ${Math.round(M.target * 100)}% of requests` }));
  const stats = h('div', { class: 'cs-stats', role: 'group', 'aria-label': `${LATEST}, latest published quarter` },
    h('p', { class: 'cs-stats-head', text: `${LATEST}, latest published quarter` }),
    stat('pub', 'CityStat published', fnum(M.figures.published, { text: pct1(L.published) })),
    stat('reb', 'Rebuilt', M.figures.rebuilt ? fnum(M.figures.rebuilt, { text: pct1(L.rebuilt) }) : pct1(L.rebuilt)),
    stat('done', 'Closing says done', fnum(M.figures.says_done, { text: pct1(fval(M.figures.says_done) ?? L.says_done) })));
  box.append(stats);
  const plot = h('div', { class: 'cs-plot' });
  box.append(plot);
  seriesChart(plot, M);
  if (Q3) box.append(h('p', { class: 'cs-q3' }, h('b', { text: 'Q3 2026, not yet published: ' }),
    `rebuilt ${pct1(Q3.rebuilt)}; closing says done ${pct1(Q3.says_done)}.`));
  if (M.id === 'parks_all') box.append(h('p', { class: 'cs-note', text: 'Parks: CityStat grades each request against its own due date. The rebuilt line counts open requests as not on time; the closing-says-done line counts closed requests only, so the two use different denominators.' }));
  if (M.id === 'whole_block_lights') box.append(h('p', { class: 'cs-note', text: 'Lights: the rebuilt line uses 24 hours elapsed; CityStat’s exact clock is not stated, so this is the measure’s loosest fit.' }));
  box.append(source(d.name));
  return box;
}
const stat = (cls, label, num) => h('div', { class: `cs-stat ${cls}` }, h('span', { class: 'cs-stat-k' }, swatch(cls), label), h('span', { class: 'cs-stat-v' }, num));

function source(dept) {
  return h('p', { class: 'cs-source' }, 'Source: CityStat, ', dept, ' page (chart data read 13 Oct 2026; page last updated 30 June 2026). Rebuilt and closing-says-done: the city’s open 311 file (',
    h('a', { href: 'https://www.stlouis-mo.gov/data/upload/data-files/csb.zip', text: 'csb.zip' }), ', file of 13 Oct 2026), closed requests by quarter filed; closing words classed by the ',
    h('a', { href: 'data/downloads/closure_class.sql', text: 'published table' }), '.');
}

// ------------------------------------------------------------------ quarterly chart: columns + two lines + goal
function seriesChart(box, M) {
  let lastW = 0;
  const draw = () => {
    const W = Math.round(box.clientWidth);
    if (!W || W === lastW) return;
    lastW = W;
    box.replaceChildren();
    const narrow = W < 460;
    const rows = M.series, n = rows.length;
    const padL = 38, padR = 6, top = 12, bottom = narrow ? 40 : 42, H = narrow ? 210 : 240;
    const band = (W - padL - padR) / n;
    const cx = (i) => padL + band * (i + 0.5);
    const y = (v) => top + (1 - v) * (H - top - bottom);
    const base = y(0);
    const svg = s('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}`, class: 'cs-svg', role: 'img',
      'aria-label': `${M.name}, ${M.goal}: share on time by quarter. ${LATEST}: CityStat published ${pct1(rows.find((r) => r.quarter === LATEST)?.published)}, rebuilt ${pct1(rows.find((r) => r.quarter === LATEST)?.rebuilt)}, closing says done ${pct1(rows.find((r) => r.quarter === LATEST)?.says_done)}.` });
    // unpublished quarter: a quiet band
    rows.forEach((r, i) => { if (r.published === null) svg.append(s('rect', { x: padL + band * i + 1, y: top, width: band - 2, height: base - top, class: 'cs-unpub' })); });
    for (const t of [0, 0.25, 0.5, 0.75, 1]) {
      svg.append(s('line', { x1: padL, x2: W - padR, y1: y(t), y2: y(t), class: t ? 'cs-grid-l' : 'cs-base' }));
      if (t === 0 || t === 0.5 || t === 1 || !narrow) svg.append(s('text', { x: padL - 6, y: y(t) + 4, 'text-anchor': 'end', class: 'cs-tick' }, `${t * 100}%`));
    }
    // published columns, CityStat's form
    const cw = Math.min(22, band * 0.62);
    rows.forEach((r, i) => {
      if (r.published === null) return;
      const y1 = y(r.published), rr = Math.min(4, (base - y1), cw / 2), x0 = cx(i) - cw / 2;
      svg.append(s('path', { class: 'cs-col', d: `M${x0},${base}V${y1 + rr}Q${x0},${y1} ${x0 + rr},${y1}H${x0 + cw - rr}Q${x0 + cw},${y1} ${x0 + cw},${y1 + rr}V${base}Z` }));
    });
    // the goal
    svg.append(s('line', { x1: padL, x2: W - padR, y1: y(M.target), y2: y(M.target), class: 'cs-goal-l' }),
      s('text', { x: padL + 4, y: y(M.target) - 5, class: 'cs-goal-t' }, `Goal ${Math.round(M.target * 100)}%`));
    // the two added lines
    for (const [key, cls, ring] of [['rebuilt', 'reb', true], ['says_done', 'done', false]]) {
      const pts = rows.map((r, i) => ({ i, v: r[key] })).filter((p) => p.v !== null && p.v !== undefined);
      if (pts.length > 1) svg.append(s('path', { class: `cs-line ${cls}`, d: pts.map((p, k) => `${k ? 'L' : 'M'}${cx(p.i).toFixed(1)},${y(p.v).toFixed(1)}`).join('') }));
      for (const p of pts) svg.append(s('circle', { class: `cs-dot ${cls}${ring ? ' ring' : ''}`, cx: cx(p.i), cy: y(p.v), r: narrow ? 3.5 : 4 }));
    }
    // quarter axis: Q number, the year under each Q1
    rows.forEach((r, i) => {
      const [yr, q] = r.quarter.split(' ');
      svg.append(s('text', { x: cx(i), y: base + 16, 'text-anchor': 'middle', class: 'cs-tick' }, narrow ? q.slice(1) : q));
      if (q === 'Q1') svg.append(s('text', { x: cx(i) - band / 2 + 2, y: base + 33, class: 'cs-year' }, yr));
    });
    // hover: one target per quarter, the full column height
    const cross = s('line', { y1: top, y2: base, class: 'cs-cross' });
    svg.append(cross);
    rows.forEach((r, i) => {
      const hit = s('rect', { x: padL + band * i, y: top, width: band, height: base - top + 20, class: 'cs-hit', tabindex: '-1' });
      const tip = (e) => {
        cross.setAttribute('x1', cx(i)); cross.setAttribute('x2', cx(i)); cross.classList.add('on');
        showTip(e, [{ head: `${r.quarter}${r.published === null ? ', not yet published' : ''}` },
          { color: 'var(--cs-pub)', value: r.published === null ? '–' : pct1(r.published), label: `CityStat published${r.published_n ? ` (n ${fmt.int(r.published_n)})` : ''}` },
          { color: 'var(--cs-reb)', value: pct1(r.rebuilt), label: 'Rebuilt' },
          { color: 'var(--cs-done)', value: pct1(r.says_done), label: `Closing says done${r.n_closed ? ` (n ${fmt.int(r.n_closed)} closed)` : ''}` }]);
      };
      hit.addEventListener('pointermove', tip);
      hit.addEventListener('pointerleave', () => { cross.classList.remove('on'); hideTip(); });
      svg.append(hit);
    });
    box.append(svg);
  };
  draw();
  if ('ResizeObserver' in window) new ResizeObserver(() => draw()).observe(box);
}

// ------------------------------------------------------------------ the nine measures, Q2 2026
function table(box, metrics) {
  const t = h('table', { class: 'cs' });
  t.append(h('thead', {}, h('tr', {}, h('th', { text: 'CityStat measure, Q2 2026' }), h('th', { text: 'Published' }), h('th', { class: 'rb', text: 'Rebuilt' }),
    h('th', { class: 'added' }, 'Closing says done', h('small', { text: 'within CityStat’s goal' })))));
  const tb = h('tbody');
  for (const m of metrics) {
    const [name, goal] = splitLabel(m.label);
    tb.append(h('tr', { class: m.metric === LEAD ? 'lead' : '' },
      h('td', { class: 'm' }, h('a', { href: `#${m.metric}`, text: name }), goal ? h('small', { text: goal }) : null),
      h('td', {}, fnum(pubId(m.metric), { text: pct1(fval(pubId(m.metric))) })),
      h('td', { class: 'rb' }, m.q2_ours_figure ? fnum(m.q2_ours_figure, { d: 1 }) : '–'),
      h('td', { class: 'added' }, fnum(doneId(m.metric), { text: pct1(fval(doneId(m.metric))) }))));
  }
  t.append(tb);
  box.append(t);
}

// ------------------------------------------------------------------ About these numbers (collapsed)
function about(C) {
  const det = h('details', { class: 'how' }, h('summary', { text: 'About these numbers' }));
  det.append(h('div', { class: 'how-body' },
    h('div', {}, h('h3', { text: 'Closing says done' }),
      h('p', { text: 'CityStat’s own test (closed within its goal, closed requests only, by quarter filed) with one change: a closing counts only if its words say the work was done. It is not graded against each request’s promise date and is not a record of the work itself; with work orders linked, the same column becomes done by the promised date. Closing words are classed by the published closing-word table (open to review). Same denominator as the published share.' })),
    h('div', {}, h('h3', { text: 'Published and rebuilt' }),
      h('p', {}, 'Published: CityStat’s quarterly values as its charts show them (read 13 October 2026; pages last updated 30 June 2026). Rebuilt: the same measure from the city’s open 311 file; request counts match CityStat’s within 0.2% for ',
        fnum('n4_repro_counts_exact_C', { text: `${fval('n4_repro_counts_exact_C')} of 9` }), ' measures. Q3 2026 is ours alone: CityStat has not published it, and shares measured soon after a quarter ends only fall as late requests close.')),
    h('div', {}, h('h3', { text: 'Parks' }),
      h('p', { text: 'The done column grades closed parks requests against each request’s own promise date; the rebuilt column includes open requests, so the two use different denominators.' }))));
  return det;
}

main();
