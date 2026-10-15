"""E8: record two public City of St. Louis CityStat pages for the video (research/brainstorm-v6.md idea 4, Appendix B),
with video/tools/record_demo.py's recorder. One page load each; nothing else on the site is requested.

    ~/lsat-coach/.venv/bin/python -I scripts/exec/E8/record_city.py streets     # -> video/out/city_citystat/
    ~/lsat-coach/.venv/bin/python -I scripts/exec/E8/record_city.py towing      # -> video/out/city_towing/

Both paths are allowed by https://www.stlouis-mo.gov/robots.txt (saved copy data/raw/stlouis-mo.gov/E3/robots-2026-10-14.txt).
No form, no login, no 311 status page. The page is loaded and rendered before the screencast starts (the Streets page's
debris dashboard is an embedded Tableau view, which takes several seconds); then the camera stays still, scrolls once,
calmly, to the passage, and holds while it is readable. Output follows record_demo.py's events.json format.
"""
import argparse
import asyncio
import importlib.util
import json
import pathlib
import shutil
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('record_demo', ROOT / 'video/tools/record_demo.py')
rd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rd)
from playwright.async_api import async_playwright  # noqa: E402

PAGES = {
    'streets': {'url': 'https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/streets.cfm',
                'text': 'increased to 79%', 'out': 'city_citystat', 'viz': 'tableau-viz[src*="Debris"]'},
    'towing': {'url': 'https://www.stlouis-mo.gov/government/departments/mayor/initiatives/citystat/street/towing.cfm',
               'text': 'does not necessarily indicate', 'out': 'city_towing'},
}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('page', choices=PAGES)
    ap.add_argument('--dpr', type=float, default=2.0)
    a = ap.parse_args()
    P = PAGES[a.page]
    OUT = ROOT / 'video/out' / P['out']
    rd.OUT = OUT
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True)
    VW, VH = rd.VW, rd.VH
    info = {}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(channel='chrome', headless=True, args=['--hide-scrollbars', f'--force-device-scale-factor={a.dpr:g}'])
        ctx = await browser.new_context(viewport={'width': VW, 'height': VH}, device_scale_factor=a.dpr)
        page = await ctx.new_page()
        t_load = time.time()
        resp = await page.goto(P['url'], wait_until='load', timeout=60000)
        info['http_status'] = resp.status if resp else None
        info['loaded_at'] = time.strftime('%Y-%m-%d %H:%M:%S %Z')
        if P.get('viz'):
            try:   # the Tableau component draws into an iframe; give it time to finish rendering
                await page.wait_for_selector(f"{P['viz']} iframe", timeout=30000)
                await page.wait_for_timeout(9000)
                info['viz_iframe'] = True
            except Exception as e:  # noqa: BLE001
                info['viz_iframe'] = f'not rendered: {e.__class__.__name__}'
        await page.wait_for_timeout(1500)
        info['load_seconds'] = round(time.time() - t_load, 1)
        # where to scroll: the debris heading, or the paragraph holding the towing sentence
        if P.get('anchor'):
            target = await page.evaluate(f"(() => {{ const e = document.querySelector('{P['anchor']}'); return e ? e.getBoundingClientRect().top + scrollY : null; }})()")
            lead = 110
        else:
            target = await page.evaluate("""(t) => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
                while (w.nextNode()) if (w.currentNode.nodeValue.includes(t)) { const e = w.currentNode.parentElement; return e.getBoundingClientRect().top + scrollY; }
                return null; }""", P['text'])
            lead = 300 if a.page == 'towing' else 60
        info['target_y'] = target
        cdp = await ctx.new_cdp_session(page)
        rec = rd.Rec(page, cdp, a.dpr)
        cdp.on('Page.screencastFrame', rec.on_frame)
        rec.pos = (VW * 0.72, VH * 0.62)
        await page.mouse.move(*rec.pos)
        await cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 90, 'maxWidth': int(VW * a.dpr), 'maxHeight': int(VH * a.dpr), 'everyNthFrame': 1})
        await page.evaluate("document.body.style.outline='0px solid transparent'")
        rec.mark('top of page')
        await rec.idle(2.0)
        if target is not None:
            dist = max(0, target - lead)
            # page-side scroll on every animation frame (smoothstep), so the position follows the clock; wheel events land
            # as uneven jumps in the screencast and read as stutter
            dur = 4.2 if a.page == 'streets' else 3.2
            t_s = time.time()
            task = asyncio.ensure_future(page.evaluate("""([d, T]) => new Promise(res => { const y0 = scrollY, t0 = performance.now();
                const f = (now) => { const u = Math.min(1, (now - t0) / T), e = u * u * (3 - 2 * u);
                  window.scrollTo({ top: y0 + d * e, behavior: 'instant' }); if (u < 1) requestAnimationFrame(f); else res(); };
                requestAnimationFrame(f); })""", [dist, dur * 1000]))
            while not task.done():
                rec.cursor.append([time.time(), *rec.pos])
                await asyncio.sleep(1 / 30)
            rec.scrolls.append([t_s, time.time(), *rec.pos, 'scroll to passage'])
            rec.mark('at passage')
            await rec.idle(1.0)
            if a.page == 'streets':
                # rest the cursor beside the dashboard, then hold
                # hover the last Alley/Street bar (Q2 2026) so the dashboard's own tooltip shows the published share
                vb = await page.evaluate("""(() => { const v = document.querySelector('tableau-viz[src*="Debris"]'); if (!v) return null;
                    const b = v.getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; })()""")
                info['viz_box'] = vb
                await rec.idle(2.0)
                if vb:
                    await rec.move(vb[0] + 288, vb[1] + 300, dur=1.4)
                    rec.mark('hover Q2 2026 alley/street bar')
                await rec.idle(5.0)
            else:
                await rec.idle(5.5)
        else:
            await rec.idle(6.0)
        await cdp.send('Page.stopScreencast')
        await asyncio.sleep(0.3)
        await browser.close()
    t0 = rec.frames[0][0]
    ev = {'viewport': [VW, VH], 'dpr': a.dpr, 'url': P['url'], 'page_info': info,
          'frames': [[round(f[0] - t0, 4), f[1]] for f in rec.frames],
          'cursor': [[round(t - t0, 4), round(x, 1), round(y, 1)] for t, x, y in rec.cursor],
          'clicks': [], 'scrolls': [[round(s - t0, 4), round(e - t0, 4), round(x, 1), round(y, 1), l] for s, e, x, y, l in rec.scrolls],
          'marks': [[round(t - t0, 4), l] for t, l in rec.marks]}
    (OUT / 'events.json').write_text(json.dumps(ev))
    print(json.dumps({'page': a.page, 'info': info, 'frames': len(ev['frames']), 'end': ev['cursor'][-1][0], 'marks': ev['marks']}, indent=1))


if __name__ == '__main__':
    asyncio.run(main())
