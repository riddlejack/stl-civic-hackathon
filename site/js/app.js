// E6: shared start-up for the five product screens. Reuses common.js (data loading, figures, "How we know",
// tooltip) and adds the E6 file (data/sources.json: E5 figures from build/E5/summary.json and the source manifest),
// card mode for the video crops, and the page title (name and tagline via common.js brand()).
import { state, h, $, fig, figText, howWeKnow, load, loadConfig, loadFigures, nav, brand, setRunLine, updateMockCount, footer } from './common.js';

export const params = new URLSearchParams(location.search);
export const card = params.get('card');

export async function boot(active, title) {
  await loadConfig();
  const b = brand(state.config);
  document.title = [title, b.name, title ? '' : b.tagline].filter(Boolean).join(' · ');
  if (card) document.body.classList.add('cardmode');
  nav(active);
  await loadFigures();
  const [run, e6] = await Promise.all([load('run'), load('sources').catch(() => null)]);
  if (e6?.figures) Object.assign(state.figures, e6.figures); // E5 ids, registered in build/E6/figures.json
  setRunLine(run);
  return { run, e6 };
}

export function finish() {
  if (!card) footer();
  updateMockCount();
  document.body.dataset.ready = '1';
}

// A registered figure as text; '–' when the id is missing (never an invented number).
export const ftxt = (id, opts) => { const f = fig(id); return f ? figText(f, opts) : '–'; };
export const fval = (id) => fig(id)?.value;
// The figure itself, clickable for "How we know" (a quiet dotted underline, no icon).
export const fnum = (id, opts = {}) => howWeKnow(id, '', { text: opts.text || ftxt(id, opts) });
export const pct1 = (v) => (typeof v === 'number' ? `${(v * 100).toFixed(1)}%` : '–');

export function page(...kids) {
  const m = $('#main');
  const w = h('div', { class: 'wrap page' }, ...kids);
  m.append(w);
  return w;
}
