// "A resident's page": each example twice, side by side. Left, a replica of the city's own status page as a resident
// sees it today (its field labels and wording, block level, request number withheld). Right, the same request with the
// fix: open until the crew's job is done, the job and its due date, past-due flags, repeat reports joined, a short
// timeline and what happens next. Content comes from data/resident.json (written from the N5 receipts, the E3 saved page
// and E1's reading of 1,440 status pages); registered figures keep their "How we know" links. On a phone the two sides
// become a toggle. The lookup box needs scripts/night/N6/serve.py; a static copy says so.
import { h, clear, fmt, load } from './common.js';
import { boot, finish, params, fnum, page } from './app.js';

const mdY = (s) => { const m = String(s || '').match(/^(\d{4})-(\d{2})-(\d{2})/); return m ? `${m[2]}/${m[3]}/${m[1]}` : ''; };
const short = (s) => fmt.dateShort(s);
const nb = (t) => String(t || '').replace(/(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/g, '$1\u00a0$2');
const pill = (kind, text) => h('span', { class: `pill ${kind}` }, h('span', { text }));
const LOCAL = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
const STATIC_MSG = 'Lookup runs on the city’s systems; try the examples.';

let D = { examples: [], page: {} }, EX = {}, cur = 'lot', side = 'today', lookup = null;
let out, seg, chips, lookNote;

async function main() {
  await boot('status.html', 'A resident’s page');
  D = (await load('resident').catch(() => null)) || D;
  for (const e of D.examples || []) EX[e.key] = e;
  if (EX[params.get('ex')]) cur = params.get('ex');
  if (params.get('view') === 'after' || params.get('view') === 'fix') side = 'fix';
  render();
  finish();
}

// ------------------------------------------------------------------ page
function render() {
  const root = page(
    h('h1', { class: 'title', text: 'A resident’s page' }),
    h('p', { class: 'say', text: 'What the city’s status page shows a resident today, beside the same request with the fix: open until the crew’s job is done.' }));

  const input = h('input', { type: 'text', inputmode: 'numeric', placeholder: 'Type a 311 request number', 'aria-label': '311 request number', autocomplete: 'off' });
  const go = () => { const v = input.value.replace(/\D/g, ''); if (v) look(v); };
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(); });
  lookNote = h('p', { class: 'rp-looknote', text: LOCAL ? '' : STATIC_MSG });

  chips = h('div', { class: 'chips', role: 'group', 'aria-label': 'Examples' }, h('span', { class: 'lab', text: 'Examples:' }),
    ...Object.values(EX).map((e) => h('button', { class: 'chip', type: 'button', 'data-ex': e.key, text: e.chip, onclick: () => { lookup = null; cur = e.key; draw(); } })));
  root.append(h('div', { class: 'rp-bar' }, chips,
    h('div', { class: 'rp-look' }, h('div', { class: 'st-look' }, input, h('button', { class: 'btn', type: 'button', text: 'Check a request', onclick: go })), lookNote)));

  seg = h('div', { class: 'seg big rp-seg', role: 'group', 'aria-label': 'Today or with the fix' },
    h('button', { type: 'button', 'data-v': 'today', text: 'Today', onclick: () => { side = 'today'; draw(); } }),
    h('button', { type: 'button', 'data-v': 'fix', text: 'With the fix', onclick: () => { side = 'fix'; draw(); } }));
  root.append(seg);
  out = h('div', { class: 'rp-out' });
  root.append(out, about());
  draw();
}

function draw() {
  chips.querySelectorAll('.chip').forEach((c) => c.classList.toggle('on', !lookup && c.dataset.ex === cur));
  seg.querySelectorAll('button').forEach((b) => b.classList.toggle('on', b.dataset.v === side));
  clear(out);
  if (lookup) { out.append(lookupView(lookup)); return; }
  const e = EX[cur];
  if (!e) return;
  out.append(h('div', { class: 'rp-grid', 'data-side': side }, todayCol(e), fixCol(e)));
  const u = new URL(location.href);
  u.searchParams.set('ex', cur); u.searchParams.set('view', side === 'fix' ? 'after' : 'today');
  history.replaceState(null, '', u);
}

// ------------------------------------------------------------------ Today: the city's page, replicated
function colHead(kind, kicker, pills, sub) {
  return h('div', { class: `rp-head ${kind}` },
    h('div', { class: 'rp-kicker', text: kicker }),
    h('div', { class: 'rp-pills' }, ...pills),
    sub ? h('div', { class: 'rp-sub', text: sub }) : null);
}

const field = (label, ...val) => h('p', { class: 'cp-f' }, h('strong', { text: `${label}: ` }), ...val);

function todayCol(e) {
  const t = e.today, P = D.page || {};
  const statusWord = t.tooltip
    ? h('span', { class: 'cp-tip', title: P.closed_tooltip, text: t.status })
    : h('span', { text: t.status });
  const overview = [field('Status', statusWord, ` on ${mdY(t.status_on)}`), field('Dept Investigation Completed On', mdY(t.invt_done))];
  if (t.overview_resolution) overview.push(field('Resolution', t.overview_resolution));

  const actions = [];
  if (t.actions?.csb_line) actions.push(h('p', { class: 'cp-f' }, h('strong', { text: 'Resolution: ' }), 'For detailed information, ', h('span', { class: 'cp-link', text: 'please contact the Citizens’ Service Bureau.' })));
  if (t.actions?.resolution) actions.push(h('h4', { text: 'Resolution' }), field('Resolution', t.actions.resolution), field('Details', t.actions.details));

  const replica = h('div', { class: 'cp', 'aria-label': 'Replica of the city’s status page' },
    h('div', { class: 'cp-band' }, h('span', { text: 'Check Status of a Service Request' }), h('span', { class: 'cp-rep', text: 'Replica · not the City’s site' })),
    h('div', { class: 'cp-body' },
      h('div', { class: 'cp-h1' }, 'Service Request ', h('span', { class: 'cp-withheld', text: 'withheld' })),
      h('p', { class: 'cp-sum' }, h('span', { class: 'cp-lab', text: t.problem_type }), ' at ', h('span', { class: 'cp-lab', text: e.block }), ' submitted on ', h('span', { class: 'cp-lab', text: mdY(t.submitted) })),
      h('h3', { text: 'Overview' }), h('div', { class: 'cp-block' }, ...overview),
      t.tooltip ? h('p', { class: 'cp-note' }, h('span', { class: 'cp-q', text: `“${P.closed_tooltip}”` }), ' ', P.closed_tooltip_note) : null,
      actions.length ? h('h3', { text: 'Actions Taken' }) : null, actions.length ? h('div', { class: 'cp-block' }, ...actions) : null,
      h('h3', { text: 'Details' }),
      h('div', { class: 'cp-block cp-two' },
        h('div', {}, h('h4', { text: 'Request' }),
          field('Service Request (SR) ID', h('span', { class: 'cp-withheld', text: 'withheld' })),
          field('Location', e.block), field('Request Initiated', mdY(t.submitted)), field('Problem Type', t.problem_type)),
        h('div', {}, h('h4', { text: 'Department' }), field('Dept To Receive SR', t.division), field('Dept Response Due By', mdY(t.due)))),
      h('h3', { text: 'Related Items' }),
      h('p', { class: 'cp-f cp-none' }, 'none ', h('span', { class: 'cp-note', text: `(${P.related_none_note})` }))));

  const missing = h('div', { class: 'rp-missing' }, h('div', { class: 'rp-mh', text: 'Not on this page' }),
    h('ul', {}, ...(t.missing || []).map(([d, txt]) => h('li', {}, d ? h('b', { text: `${short(d)}: ` }) : null, txt))));

  return h('section', { class: 'rp-col rp-today', 'aria-label': 'Today' },
    colHead('today', 'Today', [pill('handoff', t.status)], t.headline),
    h('div', { class: 'rp-label', text: P.replica_label }),
    replica, missing,
    h('p', { class: 'rp-src', text: t.source }));
}

// ------------------------------------------------------------------ With the fix
function factValue(e, k, v) {
  // Registered figures keep their "How we know" link.
  if (e.key === 'cave' && k === 'Past its date') return h('span', {}, fnum('e3_status_cavein_days_past_promise', { text: '75 days' }), v.replace(/^75 days/, ''));
  return v;
}

function fixCol(e) {
  const f = e.fix;
  const facts = h('dl', { class: 'rp-facts' }, ...f.facts.map(([k, v, tone, illus]) =>
    h('div', { class: `rp-fact ${tone || ''}` }, h('dt', {}, k, illus ? h('span', { class: 'st-tag rp-illus', text: 'Illustration' }) : null), h('dd', {}, factValue(e, k, v)))));

  const steps = h('ol', { class: 'rp-steps' }, ...f.timeline.map(([lab, txt, st]) =>
    h('li', { class: `rp-step ${st}` }, h('span', { class: 'rp-dot', 'aria-hidden': 'true' }), h('div', { class: 'rp-sl', text: lab }), h('div', { class: 'rp-st', text: nb(txt) }))));

  const reports = h('div', { class: 'rp-reports' }, h('div', { class: 'rp-mh', text: 'Reports on this request' }),
    h('ul', {}, ...f.reports.map(([d, txt, kind]) => h('li', { class: kind }, h('b', { text: short(d) }), h('span', { text: txt })))));

  return h('section', { class: 'rp-col rp-fix', 'aria-label': 'With the fix' },
    colHead('fix', 'With the fix', f.status.map(([k, t]) => pill(k, t)), null),
    h('div', { class: 'rp-label' }, h('span', { class: 'st-tag', text: 'Illustration' }), ' On this request’s own dates'),
    h('div', { class: 'card rp-card' },
      h('div', { class: 'rp-what' }, h('div', { class: 'ty', text: e.what }), h('div', { class: 'rp-type', text: e.today.problem_type }),
        h('div', { class: 'rp-where', text: `${e.block} · ${fmt.ward(e.ward)}` })),
      facts, steps, reports,
      h('div', { class: 'rp-next' }, h('div', { class: 'rp-mh', text: 'What happens next' }), h('p', { text: f.next }))),
    h('p', { class: 'rp-src', text: f.note }));
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
  } catch (err) {
    lookup = { msg: STATIC_MSG };
    lookNote.textContent = STATIC_MSG;
  }
  draw();
}

function lookupView(r) {
  const c = h('div', { class: 'card rp-card rp-lookup' });
  if (r.pending) { c.append(h('p', { class: 'muted', text: 'Looking it up…' })); return c; }
  if (r.msg) {
    c.append(h('p', { class: 'rp-msg', text: r.msg }),
      h('div', { class: 'chips' }, ...Object.values(EX).map((e) => h('button', { class: 'chip', type: 'button', text: e.chip, onclick: () => { lookup = null; cur = e.key; draw(); } }))));
    return c;
  }
  const word = r.status_group === 'open' ? 'Open' : r.status_group === 'cancelled' ? 'Cancelled' : 'Closed';
  const rows = [['Request Initiated', mdY(r.filed)], [word === 'Cancelled' ? 'Cancelled' : 'Closed', mdY(r.closed || r.cancelled) || '–'],
    ['Dept To Receive SR', r.division || '–'], ['Dept Response Due By', mdY(r.promised) || '–']];
  c.append(h('div', { class: 'ty', text: 'Your request, today' }), h('div', { class: 'rp-type', text: r.type_name || r.problem_code }),
    h('div', { class: 'rp-where', text: [r.public_address, fmt.ward(r.ward)].filter(Boolean).join(' · ') }),
    h('div', { class: 'rp-pills' }, pill(word === 'Open' ? 'promise' : 'handoff', word),
      r.closed_with_words ? h('span', { class: 'rp-words', text: `“${String(r.closed_with_words).toLowerCase()}”` }) : null),
    h('dl', { class: 'rp-facts' }, ...rows.map(([k, v]) => h('div', { class: 'rp-fact' }, h('dt', { text: k }), h('dd', { text: v })))),
    h('p', { class: 'rp-src', text: 'With the fix, this request would stay open, linked to the crew’s work order and its due date, and close when the work is recorded. Block level only; the number you typed is not stored or shown.' }));
  return c;
}

// ------------------------------------------------------------------ About this page (collapsed)
function about() {
  const P = D.page || {};
  const det = h('details', { class: 'how' }, h('summary', { text: 'About this page' }));
  det.append(h('div', { class: 'how-body' },
    h('div', {}, h('h3', { text: 'Today: a replica' }),
      h('p', {}, 'The left side copies the field labels and wording of the city’s ', h('a', { href: P.status_url, text: 'status page' }),
        ', as read on 1,440 pages on 14 October 2026: “Closed” and its closing words, or, for refuse, bulky items and weeds “on schedule to be cut”, the line asking residents to contact the Citizens’ Service Bureau instead. It is a replica inside this prototype, not the City’s site: the request number is withheld and the address is cut to the block.')),
    h('div', {}, h('h3', { text: 'With the fix' }),
      h('p', { text: 'The right side is an illustration on the request’s own dates, with the fix in place: at the hand-off the request is linked to the crew’s work order, shows that order and its due date, goes on the department’s weekly past-due list when the date passes, takes in repeat reports instead of opening new requests, and closes when the work is recorded.' }),
      h('p', { text: 'Most of this exists already: Forestry attaches its removal orders to tree requests, and Cityworks, which the City runs, can close a linked request when its work order closes. The lot’s request closed in ' },
        fnum('n5_lot1_minutes_to_close_jul02', { text: '13 minutes' }), '; its cuts billed in 2026: ', fnum('n5_lot1_cuts_billed_2026'), '.')),
    h('div', {}, h('h3', { text: 'The examples' }),
      h('p', { text: 'The North Taylor lot: a city-owned vacant lot reported twice in July 2026 and closed within minutes both times, with no cut on record this year. The tree: an inspection request cancelled while a removal order at the address was already open. The cave-in: a referral closed the day it was filed, with nothing attached.' }))));
  return det;
}

main();
