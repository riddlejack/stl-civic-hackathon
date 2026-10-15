// "For city staff": the Monday brief. One printable page from the same weekly job.
import { state, h, $, clear, fmt, fig, howWeKnow, load, loadConfig, loadFigures, mockBanner, nav, footer, setRunLine, updateMockCount } from './common.js';
import { lineChart } from './charts.js';

const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

async function main() {
  await loadConfig();
  nav('brief.html'); // E3: the brief left the nav; it is reachable from the methods page
  await loadFigures();
  const [run, B, sb] = await Promise.all(['run', 'brief', 'scoreboard'].map(load));
  setRunLine(run);
  const sheet = h('article', { class: 'sheet', id: 'brief' });
  $('#main').append(sheet);
  try { render(sheet, B, sb, run); } catch (e) { console.error(e); sheet.append(h('p', { text: `The brief failed to render (${e.message}).` })); }
  mockBanner(sheet, ['brief']);
  footer();
  updateMockCount();
  document.body.dataset.ready = '1';
}

function render(sheet, B, sb, run) {
  const wk = B.week || {};
  const head = h('header', { class: 'memo-head' });
  head.append(h('div', { class: 'row' },
    h('div', {}, h('h1', { text: 'Monday brief' }), h('div', { class: 'sub', text: `City services, week to ${fmt.date(wk.this_to)} · data through ${fmt.date(B.asof)}` })),
    h('div', { class: 'memo-actions' }, h('button', { class: 'btn ghost', type: 'button', text: 'Print', onclick: () => window.print() }))));
  const ms = B.meeting_source || {};
  head.append(h('dl', {},
    h('dt', { text: 'For' }), h('dd', {}, 'The weekly cabinet data review (', h('a', { href: ms.url, text: `reported at CityStat's launch, ${ms.date}` }), ')'),
    h('dt', { text: 'From' }), h('dd', { text: "The weekly job: plain SQL over files the city already publishes (311, the Forestry billing ledger, the land bank inventory, Cityworks saved searches). No AI runs in it." }),
    h('dt', { text: 'Note' }), h('dd', { text: 'Independent prototype, not a City document. Block level only; no request numbers or addresses.' })));
  sheet.append(head);

  // 1. what slipped
  const comp = B.compliance || {};
  const rows = comp.rows || [];
  const slipped = rows.filter((r) => r.change_pts !== null && r.change_pts <= -10).slice(0, 10);
  sheet.append(h('h2', {}, h('span', { class: 'n', text: '1' }), 'What slipped since last week'));
  sheet.append(h('p', { class: 'lede', text: `Share of requests closed by the date the city itself promised, for requests due ${fmt.date(wk.this_from, false)} to ${fmt.date(wk.this_to, false)} against the week before. Services with at least 20 due in each week; ${rows.length} qualify, and these fell by 10 points or more.` }));
  const t = h('table', { class: 't' });
  t.append(h('thead', {}, h('tr', {}, h('th', { text: 'Service' }), h('th', { class: 'r', text: 'Promise' }), h('th', { class: 'r', text: 'Due this week' }),
    h('th', { class: 'r', text: 'Closed by promise, this week' }), h('th', { class: 'r', text: 'Last week' }), h('th', { class: 'r', text: 'Change' }), h('th', { class: 'r', text: 'Closed as done' }))));
  const tb = h('tbody');
  for (const r of slipped) {
    tb.append(h('tr', {}, h('td', { class: 'svc', text: r.service }), h('td', { class: 'r', text: `${Math.round(r.promise_days)} d` }), h('td', { class: 'r', text: fmt.int(r.n_this) }),
      h('td', { class: 'r', text: fmt.pct(r.kept_this) }), h('td', { class: 'r', text: fmt.pct(r.kept_last) }),
      h('td', { class: 'r down', text: `${r.change_pts > 0 ? '+' : ''}${fmt.num(r.change_pts, 0)} pts` }), h('td', { class: 'r', text: fmt.pct(r.done_this) })));
  }
  if (!slipped.length) tb.append(h('tr', {}, h('td', { colspan: 7, text: 'No service fell by 10 points or more this week.' })));
  t.append(tb);
  sheet.append(t, h('div', { style: 'margin-top:6px' }, howWeKnow(comp.figure_id)));

  // E3: the July pothole callout was removed (the Q3 column stays in the scoreboard table only).

  // 2. first-step waits by ward
  const fs = B.first_step || {};
  sheet.append(h('h2', {}, h('span', { class: 'n', text: '2' }), 'First-step waits by ward'));
  const n3t = fig('n3_towing_tagged_median_after'), n3c = fig('n3_cavein_referral_median_after');
  sheet.append(h('p', { class: 'lede', text: `Median days from a resident's request to the first step, same request type and same closing words, since the May 2025 tornado. Where the work is recorded as done, the wards are served at about the same speed; the wait is for someone to look.${n3t && n3c ? ` Wards 1–5 against 10–14: towing tag ${fmt.num(n3t.value.wards_1_5, 1)} vs ${fmt.num(n3t.value.wards_10_14, 1)} days; cave-in referral ${fmt.num(n3c.value.wards_1_5, 1)} vs ${fmt.num(n3c.value.wards_10_14, 1)} days.` : ''}` }));
  const wt = h('table', { class: 't wardgrid' });
  wt.append(h('thead', {}, h('tr', {}, h('th', { text: 'Ward' }), h('th', { class: 'r', text: 'Towing: “vehicle tagged for tow”' }), h('th', { class: 'bar', text: '' }),
    h('th', { class: 'r', text: 'Cave-in: “referred to street maintenance”' }), h('th', { class: 'bar', text: '' }))));
  const wtb = h('tbody');
  const mx = 70;
  const bar = (v, c) => h('div', { class: 'minibar' }, h('span', { style: `width:${Math.min(100, ((v || 0) / mx) * 100)}%;background:${c}` }));
  for (const w of fs.wards || []) {
    const tt = w.towing_tag, cv = w.cavein_referral;
    const north = +w.ward >= 10;
    const c = north ? css('--c-north') : +w.ward <= 5 ? css('--c-south') : '#9a988f';
    wtb.append(h('tr', {}, h('td', { class: 'svc', style: 'white-space:nowrap', text: `Ward ${+w.ward}` }),
      h('td', { class: 'r', text: tt ? `${fmt.num(tt.median_days, 1)} d (n ${tt.n})` : '–' }), h('td', { class: 'bar' }, bar(tt?.median_days, c)),
      h('td', { class: 'r', text: cv ? `${fmt.num(cv.median_days, 1)} d (n ${cv.n})` : '–' }), h('td', { class: 'bar' }, bar(cv?.median_days, c))));
  }
  wt.append(wtb);
  sheet.append(wt, h('p', { class: 'fine', style: 'margin:6px 0 0', text: "Ward as published in the file's WARD column; requests with a blank ward are left out, so a city analyst can reproduce every row from the CSV." }),
    h('div', { style: 'margin-top:6px;display:flex;gap:16px' }, howWeKnow(fs.figure_id), howWeKnow(fs.n3_figures || [], 'How we know (ward groups)')));

  // 3. three lists
  sheet.append(h('h2', {}, h('span', { class: 'n', text: '3' }), 'Three lists for this week, block level'));
  (B.lists || []).forEach((L, i) => {
    const blk = h('div', { class: 'listblock' });
    blk.append(h('h3', { text: `${String.fromCharCode(97 + i)}. ${L.title}` }));
    blk.append(h('p', { class: 'meta' }, h('span', { class: 'sum', text: L.summary }), ` · ${L.owner} · `, h('a', { href: L.csv, download: '', text: 'all rows (CSV)' }), ' · ', howWeKnow(L.figure_id)));
    blk.append(h('p', { class: 'meta', style: 'margin-top:-6px', text: `${L.scope}${L.summary_note ? ' ' + L.summary_note.charAt(0).toUpperCase() + L.summary_note.slice(1) + '.' : ''}` }));
    const lt = h('table', { class: 't' });
    const labels = { block: 'Block', ward: 'Ward', lots: 'Lots', requests: 'Requests', first_filed: 'First filed', last_filed: 'Last filed', referrals: 'Referrals',
      first_referred: 'First referred', days_since_first: 'Days since', cancelled_requests: 'Cancelled requests', order_open_days: 'Removal order open (days)' };
    lt.append(h('thead', {}, h('tr', {}, ...L.columns.map((c) => h('th', { class: c === 'block' ? '' : 'r', text: labels[c] || c })))));
    const ltb = h('tbody');
    for (const r of (L.rows || []).slice(0, 6)) {
      ltb.append(h('tr', {}, ...L.columns.map((c) => h('td', { class: c === 'block' ? 'svc' : 'r',
        text: c === 'ward' ? +r[c] || '–' : /filed|referred/.test(c) ? fmt.dateShort(r[c]) : typeof r[c] === 'number' ? fmt.int(r[c]) : (r[c] ?? '–') }))));
    }
    lt.append(ltb);
    blk.append(lt);
    sheet.append(blk);
  });

  sheet.append(h('div', { class: 'memo-foot' },
    h('div', { text: `Also on file: ${fmt.int(B.monday_total)} open requests are past the city's own promise date, all years (the full Monday list, block level). ` }),
    h('a', { href: B.monday_csv || 'data/downloads/monday_list.csv', download: '', text: 'Download the full Monday list (CSV)' }),
    h('div', { style: 'margin-top:8px', text: state.config.footer })));
}

main();
