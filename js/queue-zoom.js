// Past-due list: zoom and pan for the block map (wheel, drag, two-finger pinch, +/− and reset buttons).
// Works on the SVG viewBox, so the map stays one vector drawing; onZoom(k) lets the page keep dots a readable size.
export function zoomable(svg, base, onZoom, { max = 14 } = {}) {
  const vb = { ...base };
  let k = 1;
  const apply = () => {
    k = base.w / vb.w;
    svg.setAttribute('viewBox', `${vb.x} ${vb.y} ${vb.w} ${vb.h}`);
    onZoom(k);
  };
  const toSvg = (cx, cy) => {
    const m = svg.getScreenCTM();
    if (!m) return { x: vb.x + vb.w / 2, y: vb.y + vb.h / 2 };
    const p = new DOMPoint(cx, cy).matrixTransform(m.inverse());
    return { x: p.x, y: p.y };
  };
  const clampPan = () => {
    // keep some of the city in view
    const mx = vb.w * 0.6, my = vb.h * 0.6;
    vb.x = Math.min(Math.max(vb.x, base.x - mx), base.x + base.w - vb.w + mx);
    vb.y = Math.min(Math.max(vb.y, base.y - my), base.y + base.h - vb.h + my);
  };
  const zoomAt = (px, py, f) => {
    const nk = Math.min(max, Math.max(1, k * f));
    f = nk / k;
    if (nk === 1) { Object.assign(vb, base); apply(); return; }
    vb.x = px - (px - vb.x) / f; vb.y = py - (py - vb.y) / f;
    vb.w /= f; vb.h /= f;
    clampPan();
    apply();
  };
  const centre = () => ({ x: vb.x + vb.w / 2, y: vb.y + vb.h / 2 });

  svg.addEventListener('wheel', (e) => {
    e.preventDefault();
    const p = toSvg(e.clientX, e.clientY);
    zoomAt(p.x, p.y, Math.exp(-e.deltaY * (e.deltaMode ? 0.05 : 0.0018)));
  }, { passive: false });

  // drag to pan, two pointers to pinch; a drag never counts as a click on a dot
  const ptrs = new Map();
  let moved = false, start = null, pinch = null;
  svg.addEventListener('pointerdown', (e) => {
    if (e.button !== 0 && e.pointerType === 'mouse') return;
    ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (ptrs.size === 1) { moved = false; start = { x: e.clientX, y: e.clientY }; }
    if (ptrs.size === 2) {
      const [a, b] = [...ptrs.values()];
      pinch = { d: Math.hypot(a.x - b.x, a.y - b.y) };
    }
  });
  window.addEventListener('pointermove', (e) => {
    const prev = ptrs.get(e.pointerId);
    if (!prev) return;
    const cur = { x: e.clientX, y: e.clientY };
    if (start && Math.hypot(cur.x - start.x, cur.y - start.y) > 5) moved = true;
    if (ptrs.size === 1 && moved) {
      const m = svg.getScreenCTM();
      const s = m ? 1 / m.a : 1;
      vb.x -= (cur.x - prev.x) * s; vb.y -= (cur.y - prev.y) * s;
      clampPan();
      apply();
      svg.classList.add('panning');
    } else if (ptrs.size === 2 && pinch) {
      ptrs.set(e.pointerId, cur);
      const [a, b] = [...ptrs.values()];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      if (pinch.d > 0) {
        const mid = toSvg((a.x + b.x) / 2, (a.y + b.y) / 2);
        zoomAt(mid.x, mid.y, d / pinch.d);
      }
      pinch.d = d;
      moved = true;
    }
    ptrs.set(e.pointerId, cur);
  });
  const up = (e) => {
    if (!ptrs.has(e.pointerId)) return;
    ptrs.delete(e.pointerId);
    if (ptrs.size < 2) pinch = null;
    if (!ptrs.size) svg.classList.remove('panning');
  };
  window.addEventListener('pointerup', up);
  window.addEventListener('pointercancel', up);
  svg.addEventListener('click', (e) => { if (moved) { e.stopPropagation(); e.preventDefault(); moved = false; } }, true);

  return {
    zoomIn: () => { const c = centre(); zoomAt(c.x, c.y, 1.6); },
    zoomOut: () => { const c = centre(); zoomAt(c.x, c.y, 1 / 1.6); },
    reset: () => { Object.assign(vb, base); apply(); },
    k: () => k,
  };
}
