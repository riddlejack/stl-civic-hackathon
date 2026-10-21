// Shared helpers: data loading with mock fallback, figures + "How we know", tooltip, formatting.
// Every string from a data file goes into the DOM with textContent (data is never markup).

export const state = { config: null, figures: {}, sources: {}, mock: new Set() };

// ------------------------------------------------------------------ DOM
export function h(tag, attrs = {}, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === 'class') el.className = v;
    else if (k === 'text') el.textContent = v;
    else if (k === 'style') el.setAttribute('style', v);
    else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? '' : v);
  }
  for (const kid of kids.flat()) {
    if (kid === null || kid === undefined || kid === false) continue;
    el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
  }
  return el;
}
export const $ = (sel, root = document) => root.querySelector(sel);
export function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); return el; }

// ------------------------------------------------------------------ format
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
export const fmt = {
  pct(v, d = 0) { return v === null || v === undefined || isNaN(v) ? '–' : `${(v * 100).toFixed(d)}%`; },
  pctp(v, d = 1) { return v === null || v === undefined || isNaN(v) ? '–' : `${Number(v).toFixed(d)}%`; },
  int(v) { return v === null || v === undefined || isNaN(v) ? '–' : Math.round(v).toLocaleString('en-US'); },
  num(v, d = 1) { return v === null || v === undefined || isNaN(v) ? '–' : Number(v).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }); },
  days(v) {
    if (v === null || v === undefined || isNaN(v)) return '–';
    if (v < 1 / 24) return `${Math.max(1, Math.round(v * 1440))} min`;
    if (v < 1) return `${(v * 24).toFixed(0)} h`;
    return `${Number(v).toFixed(v < 10 ? 1 : 0)} days`;
  },
  date(s, year = true) {
    if (!s) return '–';
    const m = String(s).match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (!m) return String(s);
    return `${+m[3]} ${MONTHS[+m[2] - 1]}${year ? ' ' + m[1] : ''}`;
  },
  dateShort(s) {
    const m = String(s || '').match(/^(\d{4})-(\d{2})-(\d{2})/);
    return m ? `${+m[3]} ${MONTHS[+m[2] - 1].slice(0, 3)} ${m[1]}` : (s || '–');
  },
  time(s) { const m = String(s || '').match(/(\d{2}):(\d{2})/); return m ? `${m[1]}:${m[2]}` : ''; },
  ward(w) { return w ? `Ward ${+w}` : 'ward unknown'; },
};

// figure value by unit
export function figText(f, opts = {}) {
  if (!f) return '–';
  const v = f.value;
  const u = String(f.unit || '').toLowerCase();
  if (typeof v !== 'number') return String(v ?? '–');
  if (u.startsWith('share') || u.includes('share of')) return fmt.pct(v, opts.d ?? 0);
  if (u.startsWith('%') || u.includes('% ') || u.endsWith('%')) return fmt.pctp(v, opts.d ?? 1);
  if (u.includes('day')) return `${fmt.num(v, opts.d ?? 1)} days`;
  if (Number.isInteger(v)) return fmt.int(v);
  return fmt.num(v, opts.d ?? 1);
}

// ------------------------------------------------------------------ data
async function getJSON(url) {
  const r = await fetch(url, { cache: 'no-cache' });
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  return r.json();
}

export async function loadConfig() {
  state.config = await getJSON('config.json');
  if (state.config.theme) document.documentElement.setAttribute('data-theme', state.config.theme);
  return state.config;
}

// Real file first (site/data, built by the bridge), then the schema'd mock.
export async function load(name) {
  try {
    const d = await getJSON(`data/${name}.json`);
    state.sources[name] = { path: `data/${name}.json`, mock: false, state: d.meta?.state || 'real', meta: d.meta };
    return d;
  } catch (e) {
    const d = await getJSON(`mock/${name}.json`);
    state.sources[name] = { path: `mock/${name}.json`, mock: true, state: 'mock', meta: d.meta };
    state.mock.add(name);
    return d;
  }
}

export async function loadFigures() {
  const d = await load('figures');
  state.figures = d.figures || {};
  state.figuresMock = !!d.meta?.mock;
  return state.figures;
}

export function fig(id) { return id ? state.figures[id] : null; }

// A number on the page: value + "How we know". Missing ids render a dash with a red mock tag.
export function figSpan(id, opts = {}) {
  const f = fig(id);
  const wrap = h('span', { class: opts.class || '' });
  if (!f) {
    wrap.append(h('span', { text: '–' }), h('span', { class: 'fig-mock', text: 'MOCK' }));
    return wrap;
  }
  wrap.append(h('span', { text: opts.text || figText(f, opts) }));
  if (state.figuresMock) wrap.append(h('span', { class: 'fig-mock', text: 'MOCK' }));
  return wrap;
}

// ------------------------------------------------------------------ mock banner
export function mockBanner(sectionEl, names) {
  const mocks = names.filter((n) => state.sources[n]?.mock);
  if (!mocks.length) return null;
  const b = h('div', { class: 'mock-banner', role: 'note' },
    h('strong', { text: 'MOCK DATA' }),
    h('span', { text: `This section is reading placeholder files (${mocks.map((m) => `mock/${m}.json`).join(', ')}). The numbers are not real.` }));
  sectionEl.prepend(b);
  return b;
}

// ------------------------------------------------------------------ How we know
let pop = null;
let popBtn = null;
function closePop() {
  if (pop) pop.remove();
  if (popBtn) popBtn.setAttribute('aria-expanded', 'false');
  pop = null; popBtn = null;
}
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closePop(); });
document.addEventListener('click', (e) => {
  if (pop && !pop.contains(e.target) && !e.target.closest('.hwk')) closePop();
});

const INFO_SVG = '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="7" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M8 7v4.2M8 4.6v.2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>';

// spec: a figure id, an array of ids, or an object {title, text, label, period, source, note}
// opts.text: render the button as the figure itself (a quiet dotted underline), no icon (E6 product screens).
export function howWeKnow(spec, label = 'How we know', opts = {}) {
  const btn = h('button', { class: opts.text ? 'hwk hwk-num' : 'hwk', type: 'button', 'aria-expanded': 'false', title: opts.text ? 'How we know' : null });
  if (opts.text) btn.append(document.createTextNode(opts.text));
  else {
    btn.innerHTML = INFO_SVG; // static icon markup, no data
    btn.append(document.createTextNode(label));
  }
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (popBtn === btn) { closePop(); return; }
    closePop();
    pop = buildPop(spec);
    document.body.append(pop);
    const r = btn.getBoundingClientRect();
    const w = pop.offsetWidth;
    let left = window.scrollX + r.left;
    if (left + w > window.scrollX + document.documentElement.clientWidth - 16) left = window.scrollX + document.documentElement.clientWidth - 16 - w;
    pop.style.left = `${Math.max(16, left)}px`;
    let top = window.scrollY + r.bottom + 8;
    if (r.bottom + pop.offsetHeight + 16 > window.innerHeight && r.top > pop.offsetHeight + 16) top = window.scrollY + r.top - pop.offsetHeight - 8;
    pop.style.top = `${top}px`;
    btn.setAttribute('aria-expanded', 'true');
    popBtn = btn;
  });
  return btn;
}

function figBlock(f) {
  const parts = [];
  const der = f.derivation || [f.definition, f.note].filter(Boolean).join(' ');
  parts.push(h('p', { text: der || 'No derivation recorded for this figure yet.' }));
  if (Array.isArray(f.derivation_chain) && f.derivation_chain.length) {
    const ol = h('ol', { style: 'margin:0 0 10px;padding-left:18px;font-size:13.5px;color:var(--ink-2)' });
    for (const step of f.derivation_chain.slice(0, 8)) {
      ol.append(h('li', { text: typeof step === 'string' ? step : (step.text || step.step || step.source || JSON.stringify(step)) }));
    }
    parts.push(ol);
  }
  const c = f.chain;
  if (c && (c.sources?.length || c.corrections?.length || c.bounds?.length)) {
    const sub = (title, items) => {
      if (!items || !items.length) return;
      parts.push(h('div', { style: 'font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:8px 0 2px', text: title }));
      const ul = h('ul', { style: 'margin:0 0 4px;padding-left:18px;font-size:13px;color:var(--ink-2)' });
      for (const it of items.slice(0, 5)) ul.append(h('li', { text: typeof it === 'string' ? it : (it.name || JSON.stringify(it)) }));
      parts.push(ul);
    };
    sub('Sources', c.sources);
    sub('Corrections applied', c.corrections);
    sub('What bounds it', c.bounds);
  }
  const dl = h('dl');
  const row = (k, v) => { if (v) dl.append(h('dt', { text: k }), h('dd', { text: String(v) })); };
  row('Figure', `${figText(f)}${f.unit ? ` (${f.unit})` : ''}`);
  row('Period', f.period);
  if (f.definition && f.derivation) row('Definition', f.definition);
  row('Label', f.label);
  row('Computed by', f.source_sql_or_script);
  if (f.note && f.derivation) row('Note', f.note);
  parts.push(dl);
  return parts;
}

function buildPop(spec) {
  const p = h('div', { class: 'hwk-pop', role: 'dialog', 'aria-label': 'How we know' });
  p.append(h('button', { class: 'x', type: 'button', 'aria-label': 'Close', text: '×', onclick: closePop }));
  const ids = typeof spec === 'string' ? [spec] : Array.isArray(spec) ? spec : null;
  if (ids) {
    const figs = ids.map((i) => fig(i)).filter(Boolean);
    p.append(h('h4', { text: 'How we know' }));
    if (!figs.length) p.append(h('p', { text: 'This figure is not in the registry yet (mock).' }));
    figs.forEach((f, i) => {
      if (i) p.append(h('hr', { style: 'border:0;border-top:1px solid var(--grid);margin:12px 0' }));
      p.append(...figBlock(f));
    });
    return p;
  }
  p.append(h('h4', { text: spec.title || 'How we know' }));
  if (spec.text) p.append(h('p', { text: spec.text }));
  const dl = h('dl');
  const row = (k, v) => { if (v) dl.append(h('dt', { text: k }), h('dd', { text: String(v) })); };
  row('Period', spec.period); row('Label', spec.label); row('Source', spec.source); row('Computed by', spec.script); row('Note', spec.note);
  if (dl.childNodes.length) p.append(dl);
  return p;
}

// ------------------------------------------------------------------ tooltip
const tip = h('div', { class: 'tip', role: 'tooltip' });
document.addEventListener('DOMContentLoaded', () => document.body.append(tip));
export function showTip(evt, rows) {
  clear(tip);
  for (const r of rows) {
    if (r.head) { tip.append(h('div', { class: 'k', text: r.head, style: 'margin-bottom:4px' })); continue; }
    const line = h('div', { class: 'row' });
    if (r.color) line.append(h('span', { class: 'key', style: `background:${r.color}` }));
    line.append(h('span', { class: 'v', text: r.value }), h('span', { class: 'k', text: r.label || '' }));
    tip.append(line);
  }
  tip.classList.add('on');
  const x = evt.clientX ?? (evt.target.getBoundingClientRect().left + 10);
  const y = evt.clientY ?? (evt.target.getBoundingClientRect().top);
  const w = tip.offsetWidth, hgt = tip.offsetHeight;
  tip.style.left = `${Math.min(x + 14, window.innerWidth - w - 12)}px`;
  tip.style.top = `${y - hgt - 12 < 8 ? y + 18 : y - hgt - 12}px`;
}
export function hideTip() { tip.classList.remove('on'); }
export function bindTip(el, rowsFn) {
  el.addEventListener('pointermove', (e) => showTip(e, rowsFn()));
  el.addEventListener('pointerleave', hideTip);
  el.addEventListener('focus', (e) => { const r = el.getBoundingClientRect(); showTip({ clientX: r.left + r.width / 2, clientY: r.top }, rowsFn()); });
  el.addEventListener('blur', hideTip);
}

// ------------------------------------------------------------------ nav + footer
// E6: the five product screens. The Monday brief (brief.html) is out of the nav; the README links it.
// v7: in the video's order (residents, departments, City Hall), then the data.
export const DOORS = [['status.html', 'A resident\u2019s page'], ['queue.html', 'Past-due list'], ['citystat.html', 'CityStat'], ['data.html', 'Data']];

// The name and the tagline from config. With no separate name, product_name holds the tagline (or
// product_tagline does): show it once, as the name. Setting product_name = "<Name>" and
// product_tagline = "Which promises did St. Louis keep?" then shows both, with no other edit.
export function brand(cfg = state.config) {
  const name = String(cfg?.product_name || '').trim();
  const tagline = String(cfg?.product_tagline || '').trim();
  if (!name) return { name: tagline, tagline: '' };
  return { name, tagline: tagline === name ? '' : tagline };
}

export function nav(active, links = DOORS) {
  const cfg = state.config;
  const b = brand(cfg);
  const ul = h('ul');
  for (const [href, label] of links) ul.append(h('li', {}, h('a', { href, text: label, class: href === active ? 'on' : '' })));
  const run = h('span', { class: 'runline', id: 'runline' });
  const mc = h('span', { class: 'mockcount', id: 'mockcount' });
  const n = h('nav', { class: 'nav' }, h('div', { class: 'wrap' },
    h('a', { class: 'brand', href: 'index.html', style: 'text-decoration:none' }, b.name,
      b.tagline ? h('span', { class: 'brand-sub', text: b.tagline }) : null,
      h('span', { class: 'tag', text: cfg.product_tag || 'Prototype' })),
    ul, run, mc));
  document.body.prepend(n);
  return n;
}
export function setRunLine(run) {
  const el = $('#runline');
  if (el && run) el.textContent = `Data through ${fmt.date(run.asof)}`;
}
export function updateMockCount() {
  const el = $('#mockcount');
  if (!el) return;
  const n = state.mock.size;
  el.textContent = n ? `MOCK DATA: ${n} file${n > 1 ? 's' : ''}` : '';
  el.classList.toggle('show', n > 0);
}
export function footer() {
  const links = [['index.html', 'Home'], ...DOORS];
  const repo = state.config.links?.case;
  if (/^https?:/.test(repo || '')) links.push([repo, 'Source on GitHub']);
  const f = h('footer', { class: 'foot' }, h('div', { class: 'wrap' },
    h('span', { text: state.config.footer }),
    h('span', {}, ...links.flatMap(([href, text], i) => [i ? ' · ' : null, h('a', { href, text })]))));
  document.body.append(f);
}

export function scrollToHash() {
  const only = new URLSearchParams(location.search).get('only');
  if (only) {
    // screenshot mode: show one section alone at the top of the page
    document.querySelectorAll('section.sec').forEach((sec) => { sec.style.display = sec.id === only ? '' : 'none'; });
    const f = document.querySelector('footer.foot'); if (f) f.style.display = 'none';
    window.scrollTo(0, 0);
    return;
  }
  const id = new URLSearchParams(location.search).get('section') || location.hash.slice(1);
  if (!id) return;
  const el = document.getElementById(id);
  if (el) { document.documentElement.style.scrollBehavior = 'auto'; el.scrollIntoView(); document.documentElement.style.scrollBehavior = ''; }
}

export function sectionHead(kicker, title, dek) {
  return [kicker ? h('p', { class: 'kicker', text: kicker }) : null, h('h2', { class: 'title', text: title }), dek ? h('p', { class: 'dek', text: dek }) : null];
}
