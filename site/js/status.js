// E6 "A resident's page": the lookup box, then one request with a Today / After toggle. Today is what the city's
// status page says (closing words from the 311 file and saved status pages, block level). After is an illustration:
// the request's own dates after the fix (the crew's work order attached; where there is no job, the request kept open and flagged). Dates and counts come from data/receipts.json (N5
// cases), data/statuspage.json (E3) and registered figures; no request numbers, nothing below the block.
import { state, h, $, clear, fmt, fig, load } from './common.js';
import { boot, finish, params, fnum, page } from './app.js';

const day = (s) => fmt.date(s, false);                 // 2 July
const full = (s) => fmt.date(s);                        // 2 July 2026
const quoted = (t) => (String(t || '').match(/"([^"]+)"/) || [])[1] || '';
const nextDay = (s) => { const d = new Date(`${s}T12:00:00`); d.setDate(d.getDate() + 1); return d.toISOString().slice(0, 10); };
const firstClause = (t) => String(t || '').split(/,\s*call csb/i)[0];
const pill = (kind, ...kids) => h('span', { class: `pill ${kind}` }, h('span', {}, ...kids));

let EX = {}, cur = 'lot', view = 'today', lookup = null;
let out, seg, chips;

async function main() {
  await boot('status.html', 'A resident’s page');
  const [R, S] = await Promise.all([load('receipts'), load('statuspage')]);
  EX = examples(R || {}, S || {});
  if (EX[params.get('ex')]) cur = params.get('ex');
  if (params.get('view') === 'after') view = 'after';
  render(S || {});
  finish();
}

// ------------------------------------------------------------------ the three examples
function examples(R, S) {
  const ex = {};
  const lot = R.cases?.['lot-1'];
  if (lot) {
    const f = lot.facts || {};
    const closed = lot.timeline.filter((e) => e.kind === 'closed');
    const [d1, d2] = f.weeds_requests_2026_filed || [];
    ex.lot = {
      chip: 'The lot', type: lot.type_label, block: lot.block, ward: lot.ward, filed: d1, what: 'A city-owned vacant lot',
      today: {
        status: [pill('handoff', 'Closed'), h('span', { class: 'plain', text: `\u201c${firstClause(quoted(closed[0]?.title))}\u201d` })],
        rows: [['Filed', full(d1)], ['Closed', h('span', {}, fnum('n5_lot1_minutes_to_close_jul02', { text: `${fig('n5_lot1_minutes_to_close_jul02')?.value ?? '–'} minutes` }), ' later')],
          ['Due by', full(fig('n5_lot1_promise_date')?.value)], ['Work order', 'None attached'],
          ['Reported again', h('span', {}, `${full(d2)}: closed `, fnum('n5_lot1_minutes_to_close_jul28', { text: `${fig('n5_lot1_minutes_to_close_jul28')?.value ?? '–'} minutes` }), ' later')]],
      },
      // research/north-taylor-mechanism.md: the lot had dropped off the cutting rounds, so at the hand-off there was no
      // crew job to link. Under the fix the request stays open, is flagged, and lands on the past-due list the day after its date.
      after: {
        status: [pill('promise', 'Open \u00b7 no crew job linked'), h('span', { class: 'sep', text: '\u00b7' }),
          h('span', { class: 'plain', text: `Due ${day(fig('n5_lot1_promise_date')?.value)}` })],
        rows: [['Flagged to Forestry', 'No cut scheduled for this lot'],
          ['Past-due list', pill('late', `On Forestry\u2019s past-due list since ${day(nextDay(fig('n5_lot1_promise_date')?.value))}`)],
          ['Reported again', `${full(d2)}: added to this open request`],
          ['Cuts on record', h('span', {}, fnum('n5_lot1_cuts_billed_2026'), ' this year')], ['Closes', 'When a cut is recorded']],
        note: 'Illustration on the request\u2019s own dates: the lot had dropped off the cutting rounds, so there was no crew job to link.',
      },
    };
  }
  const tree = R.cases?.['tree-2'];
  if (tree) {
    const t = Object.fromEntries(tree.timeline.map((e) => [e.kind + (e.kind === 'record' && /projected start/.test(e.title) ? '_start' : e.kind === 'record' && /projected finish/.test(e.title) ? '_finish' : e.kind === 'record' && /still/.test(e.title) ? '_last' : ''), e.date]));
    const f = tree.facts || {};
    ex.tree = {
      chip: 'The tree', type: tree.type_label || tree.type, block: tree.block, ward: tree.ward, filed: t.filed, what: 'A city tree already marked for removal',
      today: {
        status: [pill('handoff', 'Cancelled'), h('span', { class: 'plain', text: 'no public words' })],
        rows: [['Filed', full(t.filed)], ['Cancelled', `${full(t.cancelled)}, ${fmt.time(t.cancelled)}`], ['Due by', full(t.promised)], ['Work order', 'None shown']],
      },
      after: {
        status: [pill('promise', `On Forestry’s removal list since ${full(t.record_start)}`), h('span', { class: 'sep', text: '·' }),
          h('span', { class: 'plain', text: `Due ${full(t.record_finish)}` }), h('span', { class: 'sep', text: '·' }), pill('late', 'Not yet done')],
        rows: [['Work order', `Tree removal · priority ${f.wo_priority || '–'} · still open on ${full(t.record_last)}`],
          ['This request', 'Added to the open removal order instead of cancelled'], ['Closes', 'By itself, when the work order closes']],
        note: 'The removal order is real and was still open when its saved search was read on 13 October 2026; attaching this request to it is the illustration.',
      },
    };
  }
  const [before, , after] = S.panels || [];
  if (before && after) {
    const H = before.header || {};
    const val = (rows, k) => (rows || []).find((r) => r[0] === k) || [];
    const due = val(before.department, 'Dept Response Due By')[2];
    ex.cave = {
      chip: 'The cave-in', type: H.type, block: H.block, ward: H.ward, filed: H.submitted_on, what: 'A street cave-in',
      today: {
        status: [pill('handoff', 'Closed'), h('span', { class: 'plain', text: `\u201c${String(val(before.overview, 'Resolution')[1] || '').toLowerCase()}\u201d` })],
        rows: [['Filed', full(H.submitted_on)], ['Closed', full(val(before.overview, 'Status')[2])], ['Due by', full(due)], ['Work order', 'None attached']],
      },
      after: {
        status: [pill('promise', `With Street Maintenance since ${day(H.submitted_on)}`), h('span', { class: 'sep', text: '·' }),
          h('span', { class: 'plain', text: `Due ${day(due)}` }), h('span', { class: 'sep', text: '·' }), pill('late', 'Not yet done')],
        rows: [['Work order', 'Street repair · open'], ['Closes', 'By itself, when the work order closes']],
        note: 'Illustration. The real request was closed at the referral and nothing is attached, so no record says whether the repair was done.',
      },
    };
  }
  return ex;
}

// ------------------------------------------------------------------ page
function render(S) {
  const root = page(
    h('h1', { class: 'title', text: 'A resident’s page' }),
    h('p', { class: 'say', text: 'What the city’s status page tells a resident today, and what it would say after the fix: the crew’s work order attached, or the request kept open and flagged.' }));
  const input = h('input', { type: 'text', inputmode: 'numeric', placeholder: 'Type a 311 request number', 'aria-label': '311 request number', autocomplete: 'off' });
  const go = () => { const v = input.value.replace(/\D/g, ''); if (v) look(v); };
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(); });
  root.append(h('div', { class: 'st-look' }, input, h('button', { class: 'btn', type: 'button', text: 'Check a request', onclick: go })));
  chips = h('div', { class: 'chips' }, h('span', { class: 'lab', text: 'Or an example:' }),
    ...Object.entries(EX).map(([k, e]) => h('button', { class: 'chip', type: 'button', 'data-ex': k, text: e.chip, onclick: () => { lookup = null; cur = k; draw(); } })));
  seg = h('div', { class: 'seg big', role: 'group', 'aria-label': 'Today or after' },
    h('button', { type: 'button', 'data-v': 'today', text: 'Today', onclick: () => { view = 'today'; draw(); } }),
    h('button', { type: 'button', 'data-v': 'after', text: 'After the fix', onclick: () => { view = 'after'; draw(); } }));
  root.append(h('div', { class: 'st-bar' }, chips, seg));
  out = h('div');
  root.append(out);
  root.append(about(S));
  draw();
}

function draw() {
  chips.querySelectorAll('.chip').forEach((c) => c.classList.toggle('on', !lookup && c.dataset.ex === cur));
  seg.querySelectorAll('button').forEach((b) => b.classList.toggle('on', b.dataset.v === view));
  clear(out);
  if (lookup) { out.append(lookupCard(lookup)); return; }
  const e = EX[cur];
  if (!e) return;
  const v = e[view];
  const c = h('div', { class: 'card st-card' });
  c.append(h('div', { class: 'ty', text: e.what }),
    h('div', { class: 'what' }, e.type, view === 'after' ? h('span', { class: 'st-tag', text: 'Illustration' }) : null),
    h('div', { class: 'where', text: `${e.block} · ${fmt.ward(e.ward)}` }),
    h('div', { class: 'st-status' }, ...v.status),
    h('dl', { class: 'st-rows' }, ...v.rows.flatMap(([k, val]) => [h('dt', { text: k }), h('dd', {}, val)])));
  if (v.note) c.append(h('p', { class: 'st-tagline', text: v.note }));
  out.append(c);
  const u = new URL(location.href);
  u.searchParams.set('ex', cur); u.searchParams.set('view', view);
  history.replaceState(null, '', u);
}

// ------------------------------------------------------------------ the lookup (needs scripts/night/N6/serve.py)
async function look(num) {
  lookup = { pending: true };
  draw();
  try {
    const res = await fetch(`api/receipt/${encodeURIComponent(num)}`, { cache: 'no-store' });
    if (!(res.headers.get('content-type') || '').includes('json')) throw new Error('static');
    const r = await res.json();
    lookup = r.found && !r.withheld ? r : { msg: r.reason || 'Not found.' };
  } catch (e) {
    lookup = { msg: 'This copy of the page is static, so it cannot look up a number; the lookup runs against the weekly job’s database. Try an example.' };
  }
  view = 'today';
  draw();
}

function lookupCard(r) {
  const c = h('div', { class: 'card st-card' });
  if (r.pending) { c.append(h('p', { class: 'muted', text: 'Looking it up…' })); return c; }
  if (r.msg) { c.append(h('p', { style: 'font-size:20px;margin:0', text: r.msg })); return c; }
  const st = r.status_group === 'open' ? pill('promise', 'Open') : r.status_group === 'cancelled' ? pill('handoff', 'Cancelled') : pill('handoff', 'Closed');
  const rows = [['Filed', full(r.filed)], [r.status_group === 'cancelled' ? 'Cancelled' : 'Closed', r.closed || r.cancelled ? full(r.closed || r.cancelled) : '–'],
    ['Due by', full(r.promised)], ['Sent to', r.division || '–']];
  c.append(h('div', { class: 'ty', text: 'Your request' }), h('div', { class: 'what', text: r.type_name || r.problem_code }),
    h('div', { class: 'where', text: [r.public_address, fmt.ward(r.ward)].filter(Boolean).join(' · ') }),
    h('div', { class: 'st-status' }, st, r.closed_with_words ? h('span', { class: 'plain', text: `\u201c${String(r.closed_with_words).toLowerCase()}\u201d` }) : null),
    h('dl', { class: 'st-rows' }, ...rows.flatMap(([k, v]) => [h('dt', { text: k }), h('dd', { text: v })])),
    h('p', { class: 'st-tagline', text: view === 'after' ? 'After the fix, this page would show the crew job’s own status and close when the job does; with no job linked, it stays open.' : 'Block level only; the number you typed is not stored or shown.' }));
  return c;
}

// ------------------------------------------------------------------ About this page (collapsed)
function about(S) {
  const det = h('details', { class: 'how' }, h('summary', { text: 'About this page' }));
  det.append(h('div', { class: 'how-body' },
    h('div', {}, h('h3', { text: 'What “Today” shows' }),
      h('p', { text: 'The city’s own words: the status, closing words and dates from the 311 file and from saved copies of its public status page, redrawn here at block level. The request number is withheld and the address is cut to the block. This is a reconstruction, not a City page, and carries no City branding.' }),
      h('p', {}, 'The saved pages were not re-fetched: the City’s ', h('a', { href: S.source?.robots || 'https://www.stlouis-mo.gov/robots.txt', text: 'robots.txt' }), ' asks that service-request pages not be crawled.')),
    h('div', {}, h('h3', { text: 'What “After the fix” shows' }),
      h('p', { text: 'An illustration built on the request’s real dates: the crew’s work order is attached at the hand-off instead of the request being closed, so the status follows the job and the request closes when the work order closes. Where there is no job to attach, as for the lot, which had dropped off the cutting rounds, the request stays open, is flagged to the division and joins its past-due list the day after its date.' }),
      h('p', { text: 'Cityworks 23 closes a linked request by itself when its work order closes (vendor help, “Close a Work Order”); the City runs Cityworks 23.10, per its own query service. Forestry already attaches work orders to tree removals: ' },
        fnum('e3_status_tree_related_items'), ' items on the saved tree-removal page.')),
    h('div', {}, h('h3', { text: 'The examples' }),
      h('p', { text: 'The lot: a city-owned vacant lot reported twice in July 2026, closed within minutes both times, no cut on record this year. The tree: an inspection request cancelled while a removal order was already open at the address. The cave-in: a referral closed the day it was filed, with nothing attached.' }))));
  return det;
}

main();
