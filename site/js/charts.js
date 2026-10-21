// Hand-built SVG/HTML charts (no library, works offline). Mark specs from the dataviz method:
// bars <= 24px with 4px rounded data-ends, 2px surface gaps, 2px lines, >= 8px markers with a
// 2px surface ring, hairline solid grid, values in text tokens, tooltip on every mark.
import { h, fmt, bindTip } from './common.js';

const NS = 'http://www.w3.org/2000/svg';
export function s(tag, attrs = {}, ...kids) {
  const el = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) if (v !== null && v !== undefined) el.setAttribute(k, v);
  for (const kid of kids.flat()) if (kid) el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
  return el;
}
const txt = (x, y, str, cls, anchor = 'start', extra = {}) => s('text', { x, y, class: cls, 'text-anchor': anchor, ...extra }, String(str));
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

// Rounded-end bar path (horizontal): square at x0, 4px radius at the data end.
function hbarPath(x0, x1, y, hgt, r = 4) {
  const w = Math.max(0, x1 - x0);
  const rr = Math.min(r, w, hgt / 2);
  return `M${x0},${y}H${x0 + w - rr}Q${x0 + w},${y} ${x0 + w},${y + rr}V${y + hgt - rr}Q${x0 + w},${y + hgt} ${x0 + w - rr},${y + hgt}H${x0}Z`;
}
// Vertical column, rounded at the top.
function colPath(x, y1, y0, w, r = 4) {
  const hgt = Math.max(0, y0 - y1);
  const rr = Math.min(r, hgt, w / 2);
  return `M${x},${y0}V${y1 + rr}Q${x},${y1} ${x + rr},${y1}H${x + w - rr}Q${x + w},${y1} ${x + w},${y1 + rr}V${y0}Z`;
}

// ------------------------------------------------------------------ 100% stacked bar (HTML)
// segs: [{label, value (share), color, note}] ; labels inline only when they fit
export function stackBar(segs, { height = 28, showLabels = true, legend = true } = {}) {
  const total = segs.reduce((a, b) => a + (b.value || 0), 0) || 1;
  const bar = h('div', { style: `display:flex;gap:2px;height:${height}px;width:100%` });
  const labels = h('div', { style: 'display:flex;gap:2px;width:100%;margin-bottom:8px;align-items:flex-end' });
  segs.forEach((sg, i) => {
    const pct = (sg.value / total) * 100;
    const radius = i === 0 ? '4px 0 0 4px' : i === segs.length - 1 ? '0 4px 4px 0' : '0';
    const seg = h('div', { tabindex: '0', style: `flex:0 0 calc(${pct}% - 2px);background:${sg.color};border-radius:${radius};min-width:2px;cursor:default`, 'aria-label': `${sg.label} ${fmt.pct(sg.value / total)}` });
    bindTip(seg, () => [{ color: sg.color, value: fmt.pct(sg.value / total, 1), label: sg.label }, ...(sg.note ? [{ head: sg.note }] : [])]);
    bar.append(seg);
    const lab = h('div', { style: `flex:0 0 calc(${pct}% - 2px);min-width:2px;overflow:visible;white-space:nowrap` });
    if (showLabels && pct >= 9) {
      lab.append(h('div', { style: 'font-size:26px;font-weight:700;letter-spacing:-0.02em;line-height:1.1', text: fmt.pct(sg.value / total) }),
        h('div', { style: 'font-size:13.5px;color:var(--ink-2)', text: sg.label }));
    }
    labels.append(lab);
  });
  const wrap = h('div', {}, showLabels ? labels : null, bar);
  if (legend) {
    const lg = h('div', { class: 'legend' });
    segs.forEach((sg) => lg.append(h('span', {}, h('span', { class: 'sw', style: `background:${sg.color}` }), `${sg.label} ${fmt.pct(sg.value / total)}`)));
    wrap.append(lg);
  }
  return wrap;
}

// ------------------------------------------------------------------ inline percent bar (table cell)
export function pbar(value, color, { title } = {}) {
  const pct = Math.max(0, Math.min(1, value || 0)) * 100;
  const el = h('div', { class: 'pbar' },
    h('div', { class: 'track' }, h('div', { class: 'fill', style: `width:${pct}%;background:${color}` })),
    h('span', { class: 'val', text: value === null || value === undefined ? '–' : fmt.pct(value) }));
  if (title) bindTip(el, () => [{ color, value: fmt.pct(value, 1), label: title }]);
  return el;
}

// ------------------------------------------------------------------ dumbbell (ward groups)
// rows: [{label, sub, a, b, aLabel, bLabel, promise}] ; max days on the axis
export function dumbbell(container, rows, { max, rowH = 64, labelW = 0, promiseLabel = 'promise', ticks, labels = true } = {}) {
  const W = container.clientWidth || 800;
  const noAxis = Array.isArray(ticks) && ticks.length === 0;
  const padL = Math.max(labelW, 16), padR = 56, top = noAxis ? 4 : 24, bottom = noAxis ? 4 : 26;
  const H = top + rows.length * rowH + bottom;
  const mx = max || Math.max(...rows.map((r) => Math.max(r.a || 0, r.b || 0, r.promise || 0))) * 1.08;
  const x = (v) => padL + (Math.min(v, mx) / mx) * (W - padL - padR);
  const svg = s('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: 'img' });
  const tks = ticks || niceTicks(mx, 5);
  const g = s('g', { class: 'gridl' });
  const ax = s('g', { class: 'ax' });
  for (const t of tks) {
    g.append(s('line', { x1: x(t), x2: x(t), y1: top - 8, y2: H - bottom + 4 }));
    ax.append(txt(x(t), H - bottom + 18, t === 0 ? '0' : `${t} d`, '', 'middle'));
  }
  svg.append(g, ax);
  const cS = css('--c-south'), cN = css('--c-north'), surf = css('--surface');
  rows.forEach((r, i) => {
    const cy = top + i * rowH + rowH / 2;
    if (r.promise) {
      const px = x(r.promise);
      svg.append(s('line', { x1: px, x2: px, y1: cy - 12, y2: cy + 12, stroke: css('--ink'), 'stroke-width': 2 }),
        txt(px, cy + 26, `${promiseLabel} ${r.promise} d`, 'lbl-2', 'middle'));
    }
    svg.append(s('line', { x1: x(r.a), x2: x(r.b), y1: cy, y2: cy, stroke: css('--axis'), 'stroke-width': 2, 'stroke-linecap': 'round' }));
    for (const [v, c, lab, leftOf] of [[r.a, cS, r.aLabel, r.a <= r.b], [r.b, cN, r.bLabel, r.b < r.a]]) {
      const anchorLeft = leftOf && x(v) - padL > 34;
      const cx = x(v);
      const dot = s('circle', { cx, cy, r: 7, fill: c, stroke: surf, 'stroke-width': 2, tabindex: 0, class: 'mark-hover' });
      const hit = s('circle', { cx, cy, r: 14, class: 'hit' });
      const show = () => [{ head: `${r.label}${r.sub ? ' · ' + r.sub : ''}` }, { color: cS, value: fmt.days(r.a), label: r.aLabel }, { color: cN, value: fmt.days(r.b), label: r.bLabel }];
      bindTip(hit, show); bindTip(dot, show);
      svg.append(dot, hit);
      const lx = anchorLeft ? cx - 13 : cx + 13;
      if (!labels) continue;
      if (!(leftOf && !anchorLeft)) svg.append(txt(lx, cy + 5, fmt.num(v, 1), 'lbl-strong', anchorLeft ? 'end' : 'start'));
      else svg.append(txt(cx, cy - 13, fmt.num(v, 1), 'lbl-strong', 'middle'));
    }
  });
  container.append(svg);
  return svg;
}

export function niceTicks(max, n = 5) {
  const raw = max / n;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((st) => st >= raw) || raw;
  const out = [];
  for (let v = 0; v <= max + 1e-9; v += step) out.push(+v.toFixed(6));
  return out;
}

// ------------------------------------------------------------------ waterfall-in-one-bar (decomposition)
// base: {label, value}; comps: [{label, days, color}]; end: {label, value}
export function decompBar(container, base, comps, end, { height = 26 } = {}) {
  const W = container.clientWidth || 800;
  const top = 34, H = top + height + 46;
  const mx = end.value * 1.02;
  const x = (v) => (v / mx) * (W - 8);
  const svg = s('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}` });
  const surf = css('--surface');
  // base segment
  const b = s('rect', { x: 0, y: top, width: Math.max(0, x(base.value) - 2), height, fill: css('--c-other'), rx: 0 });
  bindTip(b, () => [{ color: css('--c-other'), value: fmt.days(base.value), label: base.label }]);
  svg.append(b);
  svg.append(txt(0, top - 10, `${base.label}: ${fmt.num(base.value, 1)} days`, 'lbl-ink'));
  let acc = base.value;
  comps.forEach((c, i) => {
    const x0 = x(acc), x1 = x(acc + c.days);
    const last = i === comps.length - 1;
    const el = last ? s('path', { d: hbarPath(x0, x1, top, height), fill: c.color })
      : s('rect', { x: x0, y: top, width: Math.max(0.5, x1 - x0 - 2), height, fill: c.color });
    el.setAttribute('tabindex', '0');
    bindTip(el, () => [{ color: c.color, value: `+${fmt.num(c.days, 2)} days`, label: c.label }, { head: `${fmt.pct(c.share)} of the gap` }]);
    svg.append(el);
    acc += c.days;
  });
  // end marker
  svg.append(txt(x(end.value), top - 10, `${end.label}: ${fmt.num(end.value, 1)} days`, 'lbl-ink', 'end'));
  // bracket over the gap
  const gx0 = x(base.value), gx1 = x(end.value);
  const by = top + height + 10;
  svg.append(s('path', { d: `M${gx0},${by}V${by + 6}H${gx1}V${by}`, fill: 'none', stroke: css('--axis'), 'stroke-width': 1 }));
  svg.append(txt((gx0 + gx1) / 2, by + 24, `the gap: ${fmt.num(end.value - base.value, 1)} days`, 'lbl-2', 'middle'));
  void surf;
  container.append(svg);
  return svg;
}

// ------------------------------------------------------------------ line chart over ordinal x (quarters, weeks)
// series: [{name, color, points:[{x, y}], dashed?, dots?:'ring'|'fill', line?:bool}]
export function lineChart(container, xs, series, { height = 300, yMax = 1, yFmt = (v) => fmt.pct(v), annotate = [], xLabel = (v) => v, xEvery = 1, goal = null } = {}) {
  const W = container.clientWidth || 800;
  const padL = 48, padR = 120, top = 18, bottom = 34;
  const H = height;
  const x = (i) => padL + (xs.length === 1 ? 0 : (i / (xs.length - 1)) * (W - padL - padR));
  const y = (v) => top + (1 - v / yMax) * (H - top - bottom);
  const svg = s('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}` });
  const g = s('g', { class: 'gridl' }), ax = s('g', { class: 'ax' });
  for (const t of niceTicks(yMax, 4)) {
    g.append(s('line', { x1: padL, x2: W - padR, y1: y(t), y2: y(t) }));
    ax.append(txt(padL - 8, y(t) + 4, yFmt(t), '', 'end'));
  }
  xs.forEach((v, i) => {
    const last = i === xs.length - 1;
    if (i % xEvery === 0 || (last && (i % xEvery) >= Math.ceil(xEvery / 2))) ax.append(txt(x(i), H - bottom + 20, xLabel(v), '', 'middle'));
  });
  ax.append(s('line', { x1: padL, x2: W - padR, y1: y(0), y2: y(0) }));
  svg.append(g, ax);
  if (goal !== null) {
    svg.append(s('line', { x1: padL, x2: W - padR, y1: y(goal.value), y2: y(goal.value), stroke: css('--ink'), 'stroke-width': 1, opacity: 0.5 }),
      txt(W - padR + 6, y(goal.value) + 4, goal.label, 'lbl-2'));
  }
  const surf = css('--surface');
  for (const se of series) {
    const pts = se.points.map((p) => ({ ...p, i: xs.indexOf(p.x) })).filter((p) => p.i >= 0 && p.y !== null && p.y !== undefined);
    if (se.line !== false && pts.length > 1) {
      const d = pts.map((p, k) => `${k ? 'L' : 'M'}${x(p.i)},${y(p.y)}`).join('');
      svg.append(s('path', { d, fill: 'none', stroke: se.color, 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }));
    }
    for (const p of pts) {
      const ring = se.dots === 'ring';
      svg.append(s('circle', { cx: x(p.i), cy: y(p.y), r: ring ? 7.5 : 4.5, fill: ring ? 'none' : se.color, stroke: ring ? se.color : surf, 'stroke-width': 2 }));
    }
    const lastP = pts[pts.length - 1];
    if (lastP && se.endLabel) svg.append(txt(x(lastP.i) + 10, y(lastP.y) + 4, se.endLabel, 'lbl-ink'));
  }
  for (const a of annotate) {
    const i = xs.indexOf(a.x);
    if (i < 0) continue;
    svg.append(txt(x(i) + (a.dx || 0), y(a.y) + (a.dy || -14), a.text, a.cls || 'lbl-strong', a.anchor || 'middle'));
  }
  // crosshair + tooltip
  const cross = s('line', { y1: top, y2: H - bottom, stroke: css('--axis'), 'stroke-width': 1, opacity: 0 });
  svg.append(cross);
  const hit = s('rect', { x: padL - 10, y: top, width: W - padL - padR + 20, height: H - top - bottom, class: 'hit' });
  svg.append(hit);
  hit.addEventListener('pointermove', (e) => {
    const r = svg.getBoundingClientRect();
    const px = e.clientX - r.left;
    let best = 0, bd = Infinity;
    xs.forEach((_, i) => { const d = Math.abs(x(i) - px); if (d < bd) { bd = d; best = i; } });
    cross.setAttribute('x1', x(best)); cross.setAttribute('x2', x(best)); cross.setAttribute('opacity', 1);
    const rows = [{ head: xLabel(xs[best], true) }];
    for (const se of series) {
      const p = se.points.find((q) => q.x === xs[best]);
      rows.push({ color: se.color, value: p && p.y !== null && p.y !== undefined ? yFmt(p.y, true) : '–', label: se.name + (p && p.n ? ` (n ${fmt.int(p.n)})` : '') });
    }
    import('./common.js').then((m) => m.showTip(e, rows));
  });
  hit.addEventListener('pointerleave', () => { cross.setAttribute('opacity', 0); import('./common.js').then((m) => m.hideTip()); });
  container.append(svg);
  return svg;
}

// ------------------------------------------------------------------ columns (one series)
export function columns(container, items, { height = 220, color, valueFmt = fmt.int, label = (d) => d.label } = {}) {
  const W = container.clientWidth || 600;
  const padL = 44, padR = 8, top = 22, bottom = 28;
  const mx = Math.max(...items.map((d) => d.value)) * 1.08 || 1;
  const bw = Math.min(24, ((W - padL - padR) / items.length) * 0.6);
  const step = (W - padL - padR) / items.length;
  const y = (v) => top + (1 - v / mx) * (height - top - bottom);
  const svg = s('svg', { width: W, height, viewBox: `0 0 ${W} ${height}` });
  const g = s('g', { class: 'gridl' }), ax = s('g', { class: 'ax' });
  for (const t of niceTicks(mx, 4)) { g.append(s('line', { x1: padL, x2: W - padR, y1: y(t), y2: y(t) })); ax.append(txt(padL - 8, y(t) + 4, valueFmt(t), '', 'end')); }
  svg.append(g, ax);
  const c = color || css('--c-bar');
  items.forEach((d, i) => {
    const cx = padL + step * i + step / 2;
    const p = s('path', { d: colPath(cx - bw / 2, y(d.value), y(0), bw), fill: c, tabindex: 0, class: 'mark-hover' });
    const hit = s('rect', { x: cx - step / 2, y: top, width: step, height: height - top - bottom, class: 'hit' });
    const rows = () => [{ head: label(d) }, { color: c, value: valueFmt(d.value), label: d.unit || '' }];
    bindTip(hit, rows); bindTip(p, rows);
    svg.append(p, hit, txt(cx, height - bottom + 18, d.short ?? label(d), '', 'middle', { class: 'ax' }));
    if (d.labelTop) svg.append(txt(cx, y(d.value) - 6, valueFmt(d.value), 'lbl-2', 'middle'));
  });
  svg.append(s('line', { x1: padL, x2: W - padR, y1: y(0), y2: y(0), stroke: css('--axis') }));
  container.append(svg);
  return svg;
}
