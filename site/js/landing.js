// v7 landing: the analysis is the product; the three screens show what its output looks like (residents,
// departments, City Hall, in the video's order), then the analysis and hand-over package.
import { state, h, $, fig, fmt, brand } from './common.js';
import { boot, finish, ftxt } from './app.js';

// Counts in the opening paragraph. 1,454,222 is registered (n1_duplicate_rows.request_ids); the ledger rows
// (2,252,031) and status pages (1,440) are from research/credibility-tally.md (observed, file of 13 Oct 2026).
const LEDGER_ROWS = 2252031;
const STATUS_PAGES = 1440;

const DOORS = [
  { href: 'status.html', part: 'For residents', color: 'var(--promise)', name: 'A status page that tells the truth',
    desc: 'What the 311 status page says today, and what it says once the request is tied to the crew’s job: open until the work is done.',
    foot: 'Today, and after the fix' },
  { href: 'queue.html', part: 'For departments', color: 'var(--late)', name: 'The past-due list, ranked by danger',
    desc: 'Every open request past the date the city gave, most dangerous first, on a map by block.',
    stat: () => `All divisions: ${ftxt('e3_queue_past_promise')} requests past the city’s date`,
    foot: 'Runs today on public data' },
  { href: 'citystat.html', part: 'For City Hall', color: 'var(--done)', name: 'CityStat with one more column',
    desc: 'The grades CityStat already publishes, beside one more column: closings that say the work was done.',
    foot: 'Runs today on public data' },
];

async function main() {
  await boot('index.html');
  const cfg = state.config;
  const b = brand(cfg);
  const requests = fmt.int(fig('n1_duplicate_rows')?.value?.request_ids ?? 1454222);

  const doors = h('div', { class: 'doors' }, ...DOORS.map((d) => h('a', { class: 'door', href: d.href },
    h('span', { class: 'bar', style: `background:${d.color}` }),
    h('span', { class: 'part' }, h('i', { style: `background:${d.color}` }), d.part),
    h('span', { class: 'dname', text: d.name }),
    h('span', { class: 'ddesc', text: d.desc }),
    d.stat ? h('span', { class: 'dstat', text: d.stat() }) : null,
    h('span', { class: 'dfoot' }, h('span', { text: d.foot }), h('b', { 'aria-hidden': 'true', text: '→' })))));

  const repo = cfg.links?.case || '../README.md';
  const pack = h('div', { class: 'door-quiet' },
    h('div', { class: 'dq-text' },
      h('span', { class: 'part', text: 'Under all three' }),
      h('a', { class: 'dname', href: 'data.html', text: 'The analysis and hand-over package' }),
      h('span', { class: 'ddesc', text: 'Plain SQL, the Cityworks saved search, the dashboard and one practice page per division; the downloads and every public source.' })),
    h('div', { class: 'dq-links' },
      h('a', { href: 'data.html', text: 'Data and downloads →' }),
      h('a', { href: cfg.links?.handover || 'https://github.com/riddlejack/stl-civic-hackathon/tree/HEAD/deliverable/handover', text: 'Hand-over package on GitHub →' }),
      h('a', { href: repo, text: `${cfg.links?.case_label || 'Read the full case'} →` })));

  $('#main').append(h('div', { class: 'wrap land' },
    h('h1', { class: b.tagline ? 'name' : 'name solo', text: b.name }),
    b.tagline ? h('p', { class: 'tagline', text: b.tagline }) : null,
    h('p', { class: 'say', text: `The product is the analysis: a request-by-request audit of the city’s own records (${requests} requests to 311, ${fmt.int(LEDGER_ROWS)} Forestry billing records, Cityworks work orders and ${fmt.int(STATUS_PAGES)} status pages), packaged as plain SQL and saved searches the city can run in Cityworks, CityStat and its 311 status page.` }),
    h('p', { class: 'say2', text: 'These screens show what that output looks like on real city data. They are a demo, not a replacement for the city’s 311 system.' }),
    doors,
    pack));
  finish();
}

main();
