// E6 "The data": every source with its URL, retrieval time, rows and use (E4's manifest, via data/e6.json), the
// downloads, the authorisation statement in the words of context/AUTHORISATION-NOTE.md, and the fetch script.
import { state, h, $, fmt, load } from './common.js';
import { boot, finish, page } from './app.js';

const DL = [
  ['queue.csv', 'The list, every division', 'Every open request past its date, filed since 1 Jan 2025, oldest first. Block level, no request numbers.'],
  ['scoreboard.csv', 'The scoreboard', 'For every request type: the promised date, closed by it, and closed by it with words saying the work was done.'],
  ['measures.sql', 'The measures (SQL)', 'Plain DuckDB SQL: the promise, the CityStat measures, the ledger and work-order joins, the list.'],
  ['closure_class.sql', 'Closing-word classes (SQL)', 'The city’s closing words mapped to done, handed off or no action.'],
  ['closure-classes.csv', 'Closing-word table', 'Every closing text with its class and the rule behind it: the table a person reviews.'],
  ['sources.csv', 'The source manifest', 'Every source below with its size, hash and the figures that use it.'],
  ['fetch_public.sh', 'The fetch script', 'Re-downloads every public source into data/raw/. Then run scripts/night/N1/run_all.sh.'],
];

const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
// "2026-10-13 18:10 CDT to 2026-10-13 19:36 CDT" -> "13 Oct 2026, 18:10\u201319:36"
function when(t) {
  const m = [...String(t || '').matchAll(/(\d{4})-(\d{2})-(\d{2}) (\d{2}:\d{2})/g)];
  if (!m.length) return t || '\u2013';
  const d = (x) => `${+x[3]} ${MON[+x[2] - 1]} ${x[1]}`;
  if (m.length === 1) return `${d(m[0])}, ${m[0][4]}`;
  const a = m[0], b = m[m.length - 1];
  return d(a) === d(b) ? `${d(a)}, ${a[4]}\u2013${b[4]}` : `${d(a)} ${a[4]} to ${d(b)} ${b[4]}`;
}
// keep the figure families ("N1 figures (78, ids n1_*)"); otherwise the first citing files
function use(t) {
  const parts = String(t || '').split(';').map((x) => x.trim()).filter(Boolean);
  const figs = parts.filter((x) => /figures \(/.test(x)).map((x) => x.replace(/, ids [^)]*\)/, ')'));
  if (figs.length) return figs.join(' \u00b7 ');
  return (parts[0] || '').replace(/^read or cited by /, 'Cited by ').replace(/(,[^,]+,[^,]+),.*$/, '$1, \u2026');
}

async function main() {
  const { e6 } = await boot('data.html', 'The data');
  const dls = await load('downloads').catch(() => ({ files: [] }));
  const kb = Object.fromEntries((dls.files || []).map((f) => [f.name, f.kb]));
  const S = e6?.sources || { published: [], withheld: [], counts: {} };
  const A = e6?.authorisation || {};
  const root = page(
    h('h1', { class: 'title', text: 'The data' }),
    h('p', { class: 'say', text: 'Every figure on these screens comes from the city’s own public files, re-downloadable with one script; what was read with the city’s permission is listed here and not republished.' }));

  root.append(h('div', { class: 'dl-grid' }, ...DL.map(([file, name, desc]) => h('a', { class: 'card dl', href: `data/downloads/${file}`, download: '' },
    h('b', { text: name }), h('span', { text: desc }), h('small', { text: `${file}${kb[file] ? ` · ${fmt.int(kb[file])} KB` : ''}` })))));

  root.append(h('h2', { class: 'sec', text: 'Public sources' }),
    h('p', { class: 'sec-say', text: `The ${S.published.length} public files the figures rest on. The fetch script downloads each again; the city updates them, so a fresh download gives today’s numbers.` }));
  const t = h('table', { class: 'src' });
  t.append(h('thead', {}, h('tr', {}, h('th', { text: 'Source' }), h('th', { text: 'Retrieved (Central)' }), h('th', { class: 'r', text: 'Rows' }), h('th', { class: 'r', text: 'Size' }), h('th', { text: 'How it is used' }))));
  const tb = h('tbody');
  for (const r of S.published) {
    tb.append(h('tr', {},
      h('td', { class: 'nm' }, r.name, r.url ? h('a', { href: r.url, text: r.url }) : null, r.published_as ? h('span', { class: 'fine', style: 'display:block', text: `A copy ships in the repository: ${r.published_as}` }) : null),
      h('td', { class: 'when', text: when(r.retrieved) }),
      h('td', { class: 'r', text: r.rows || '–' }),
      h('td', { class: 'r', text: r.size || '–' }),
      h('td', { class: 'use', text: use(r.used_by) })));
  }
  t.append(tb);
  root.append(h('div', { class: 'card tbl-wrap' }, t));

  // listed, not published (collapsed)
  const det = h('details', { class: 'how' }, h('summary', { text: `Listed, not published (${S.counts.not_published ?? S.withheld.length} files)` }));
  const t2 = h('table', { class: 'src' });
  t2.append(h('thead', {}, h('tr', {}, h('th', { text: 'Source' }), h('th', { text: 'Retrieved (Central)' }), h('th', { class: 'r', text: 'Files' }), h('th', { text: 'Why it is not shipped' }))));
  const tb2 = h('tbody');
  for (const g of S.withheld) {
    tb2.append(h('tr', {}, h('td', { class: 'nm' }, g.name, g.url ? h('a', { href: g.url, text: g.url }) : null), h('td', { class: 'when', text: when(g.retrieved) }),
      h('td', { class: 'r', text: String(g.files) }), h('td', { class: 'use', text: g.note || '' })));
  }
  t2.append(tb2);
  det.append(h('div', { class: 'card tbl-wrap', style: 'margin-bottom:8px' }, t2));
  root.append(det);

  // authorisation, in the note's words
  root.append(h('h2', { class: 'sec', text: 'What was read with the city’s permission' }));
  const auth = h('div', { class: 'card auth' });
  if (A.statement) auth.append(h('blockquote', { text: A.statement }));
  if ((A.authorised || []).length) auth.append(h('ul', {}, ...A.authorised.map((b) => h('li', { text: b }))));
  auth.append(h('p', { class: 'fine', style: 'margin:14px 0 0', text: `${A.status || ''} Source: ${A.source || 'context/AUTHORISATION-NOTE.md'}.` }));
  root.append(auth);

  root.append(h('h2', { class: 'sec', text: 'Run it yourself' }),
    h('div', { class: 'card auth' },
      h('pre', { style: 'margin:0;font:15px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre-wrap', text: 'bash scripts/data/fetch_public.sh\nbash scripts/night/N1/run_all.sh' }),
      h('p', { class: 'fine', style: 'margin:10px 0 0', text: 'Python 3 standard library, one request per second, no key or login. Every figure on these screens rebuilds from the files it downloads.' })));
  finish();
}

main();
