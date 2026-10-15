// E6 landing: the name, one sentence, three doors. No statistics here; they live on the screens behind the doors.
import { state, h, $ } from './common.js';
import { boot, finish } from './app.js';

const DOORS = [
  { href: 'queue.html', part: 'List', color: 'var(--late)', name: 'Forestry’s list',
    desc: 'Every request past the date the city gave, oldest first, on a map.', foot: 'Runs today on public data' },
  { href: 'citystat.html', part: 'Count', color: 'var(--done)', name: 'CityStat, with one column',
    desc: 'The grade CityStat already publishes, with one column: closings that say done.', foot: 'Runs today on public data' },
  { href: 'status.html', part: 'Link', color: 'var(--promise)', name: 'A resident’s page',
    desc: 'What the status page says today, and once the crew’s work order is attached.', foot: 'Needs the work order attached' },
];

async function main() {
  await boot('index.html');
  const cfg = state.config;
  const doors = h('div', { class: 'doors' }, ...DOORS.map((d) => h('a', { class: 'door', href: d.href },
    h('span', { class: 'bar', style: `background:${d.color}` }),
    h('span', { class: 'part' }, h('i', { style: `background:${d.color}` }), d.part),
    h('span', { class: 'dname', text: d.name }),
    h('span', { class: 'ddesc', text: d.desc }),
    h('span', { class: 'dfoot' }, h('span', { text: d.foot }), h('b', { 'aria-hidden': 'true', text: '→' })))));
  $('#main').append(h('div', { class: 'wrap land' },
    h('h1', { class: 'name', text: cfg.product_name }),
    h('p', { class: 'tagline', text: cfg.product_tagline }),
    h('p', { class: 'say', text: 'St. Louis gives every 311 request a completion date; these three screens show which of those promises it kept, on the city’s own data and in systems it already runs.' }),
    doors,
    h('div', { class: 'land-links' },
      h('a', { href: 'data.html', text: 'Get the data' }),
      h('a', { href: cfg.links?.case || '../README.md', text: cfg.links?.case_label || 'Read the full case' }))));
  finish();
}

main();
