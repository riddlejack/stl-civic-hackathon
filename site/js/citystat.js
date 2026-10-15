// E6 "CityStat, with one column": the nine 311 measures CityStat publishes, rebuilt from the public file, with the
// added column (on time only when the closing words say the work was done; labelled "Closing says done", per
// research/closure-class-review.md: not graded against each request's promise date, not a record of work done). One chart, the lead measure (alley and street debris). Every value is a
// registered figure: e3_citystat_<m>_q2_published (reported), n4_q2_2026_<m>_ours (rebuilt), e3_citystat_<m>_q2_done_on_time.
import { state, h, $, fig, load } from './common.js';
import { s } from './charts.js';
import { boot, finish, card, fnum, fval, pct1, page } from './app.js';

const LEAD = 'debris_alley_street';
const pubId = (m) => `e3_citystat_${m}_q2_published`;
const doneId = (m) => `e3_citystat_${m}_q2_done_on_time`;
const splitLabel = (l) => {
  const m = String(l).match(/^(.*?),?\s+((?:repaired|cleaned|completed|within)\b.*)$/);
  return m ? [m[1], m[2]] : [l, ''];
};

async function main() {
  await boot('citystat.html', 'CityStat, with one column');
  const sb = await load('scoreboard');
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
    h('h1', { class: 'title', text: 'CityStat, with one column' }),
    h('p', { class: 'say', text: 'The nine 311 measures CityStat publishes, rebuilt from the city’s own file, with one column added: on time only when the closing words say the work was done. With work orders linked, this becomes done by the promise.' }));
  const chartCard = h('div', { class: 'card cs-chart' });
  const tableCard = h('div', { class: 'card cs-table' });
  root.append(h('div', { class: 'cs-grid' }, chartCard, tableCard));
  chart(chartCard, lead, false);
  table(tableCard, [lead, ...metrics.filter((m) => m !== lead)]);
  root.append(h('div', { class: 'cs-actions' },
    h('a', { class: 'btn ghost', href: 'data/downloads/measures.sql', download: '', text: 'Download the SQL' }),
    h('a', { class: 'btn ghost', href: 'data/downloads/closure_class.sql', download: '', text: 'Closing-word classes (SQL)' }),
    h('a', { class: 'btn ghost', href: 'data/downloads/scoreboard.csv', download: '', text: 'Every request type (CSV)' })));
  root.append(about(sb.citystat));
  finish();
}

// ------------------------------------------------------------------ the chart: published vs done, lead measure
function chart(box, m, big) {
  const pair = fig('e3_citystat_debris_published_vs_done')?.value || {};
  box.append(h('h2', { text: 'Alley and street debris, cleaned within 3 days' }),
    h('p', { class: 'sub', text: 'Requests filed April to June 2026 (Q2), share closed within the goal' }));
  const bars = [
    { label: 'On time, as CityStat published it', id: pubId(m.metric), v: fval(pubId(m.metric)), color: 'var(--promise)' },
    { label: 'Closing says it was cleaned, within 3 days', id: doneId(m.metric), v: fval(doneId(m.metric)), color: 'var(--done)' },
  ];
  const W = 760, L = 0, R = 150, bh = big ? 70 : 64, gap = big ? 80 : 74, top = 34;
  const H = top + bars.length * (bh + gap) + 10;
  const x = (v) => L + v * (W - L - R);
  const svg = s('svg', { viewBox: `0 -4 ${W} ${H + 34}`, role: 'img', 'aria-label': `CityStat published ${pct1(bars[0].v)} on time; closing says it was cleaned, within 3 days, ${pct1(bars[1].v)}` });
  // a baseline with ticks under the bars; no gridlines through the value labels
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
}

// ------------------------------------------------------------------ the nine measures
function table(box, metrics) {
  const t = h('table', { class: 'cs' });
  t.append(h('thead', {}, h('tr', {}, h('th', { text: 'CityStat measure, Q2 2026' }), h('th', { text: 'Published' }), h('th', { class: 'rb', text: 'Rebuilt' }),
    h('th', { class: 'added' }, 'Closing says done', h('small', { text: 'within CityStat’s goal' })))));
  const tb = h('tbody');
  for (const m of metrics) {
    const [name, goal] = splitLabel(m.label);
    tb.append(h('tr', { class: m.metric === LEAD ? 'lead' : '' },
      h('td', { class: 'm' }, name, goal ? h('small', { text: goal }) : null),
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
      h('p', { text: 'CityStat’s own test (closed within its goal, closed requests only, by quarter filed) with one change: a closing counts only if its words say the work was done. It is not graded against each request’s promise date and is not a record of the work itself; with work orders linked, the same column becomes done by the promise. Closing words are classed by the published closing-word table (open to review). Same denominator as the published share.' })),
    h('div', {}, h('h3', { text: 'Published and rebuilt' }),
      h('p', {}, 'Published: CityStat’s Q2 2026 values as shown on its pages (last updated 30 June 2026). Rebuilt: the same measure from the city’s open 311 file; request counts match CityStat’s within 0.2% for ',
        fnum('n4_repro_counts_exact_C', { text: `${fval('n4_repro_counts_exact_C')} of 9` }), ' measures.')),
    h('div', {}, h('h3', { text: 'Parks' }),
      h('p', { text: 'The done column grades closed parks requests against each request’s own promise date; the rebuilt column includes open requests, so the two use different denominators.' }))));
  return det;
}

main();
