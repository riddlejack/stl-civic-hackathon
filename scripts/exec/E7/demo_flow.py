"""E7: record the site demo for the video (RESTRUCTURE-v5 item 15), reusing video/tools/record_demo.py's recorder.

    PORT=8823 .venv/bin/python -I scripts/night/N6/serve.py --no-bridge &      # a free port
    python3 -I scripts/exec/E7/demo_flow.py --base http://127.0.0.1:8823
    video/.venv/bin/python video/tools/zoom_follow.py --raw video/out/demo_e7 --out video/renders/demo_zoom.mp4 --hold 2.4
    video/.venv/bin/python video/tools/zoom_follow.py --raw video/out/demo_e7 --out video/renders/demo_raw.mp4 --zoom 1.0 --inset 1.0

Flow, slow, holding 2-3 s on each view: the queue opens on Forestry, Oldest first; click Ranked; hover the top row's
"why this rank"; click that row's block on the map (the list filters); go to A resident's page and switch Today to
"After the fix"; go to CityStat and point at the "Closing says done" column.

Output (video/out/demo_e7/, gitignored): frame_NNNNN.jpg at 3840x2160 and events.json in record_demo.py's format.
Hovers (no click) are logged as zero-distance "scrolls" labelled "hover:..." so zoom_follow.py eases in on them as it
does on a scroll; zoom_follow.py draws no mark for a scroll, so nothing false appears on screen.
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

OUT = ROOT / 'video/out/demo_e7'
VW, VH = rd.VW, rd.VH


PACE = 1.0   # take 6 (--pace 0.7): shorter moves and holds; a hold of 2 s or more never drops under 2 s


async def hover(rec, label, s):
    s = max(2.0, s * PACE) if s >= 2.0 else s
    t0 = time.time()
    await rec.idle(s)
    rec.scrolls.append([t0, time.time(), *rec.pos, f'hover:{label}'])


async def main():
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8823')
    ap.add_argument('--dpr', type=float, default=2.0)
    ap.add_argument('--out', default=str(OUT), help='raw output folder (take 6: video/out/demo6)')
    ap.add_argument('--with-data', action='store_true', help='take 6: end on the Data page (downloads, then the sources list)')
    ap.add_argument('--pace', type=float, default=1.0)
    a = ap.parse_args()
    global PACE
    PACE = a.pace
    OUT = pathlib.Path(a.out)
    rd.OUT = OUT
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(channel='chrome', headless=True, args=['--hide-scrollbars', f'--force-device-scale-factor={a.dpr:g}'])
        ctx = await browser.new_context(viewport={'width': VW, 'height': VH}, device_scale_factor=a.dpr)
        page = await ctx.new_page()
        await page.goto(f'{a.base}/queue.html?view=oldest', wait_until='networkidle')
        await page.wait_for_function("document.querySelectorAll('table.q tbody tr td.days').length > 10", timeout=30000)
        await page.wait_for_timeout(600)
        cdp = await ctx.new_cdp_session(page)
        rec = rd.Rec(page, cdp, a.dpr)
        _move = rec.move
        async def paced_move(x, y, dur=0.7, arc=0.12):
            await _move(x, y, dur=max(0.6, dur * PACE), arc=arc)
        rec.move = paced_move
        cdp.on('Page.screencastFrame', rec.on_frame)
        rec.pos = (VW * 0.55, VH * 0.42)
        await page.mouse.move(*rec.pos)
        await cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 88, 'maxWidth': int(VW * a.dpr), 'maxHeight': int(VH * a.dpr), 'everyNthFrame': 1})
        await page.evaluate("document.body.style.outline='0px solid transparent'")

        # 1. Forestry, oldest first: read the headline and the first rows
        rec.mark('queue: Forestry, oldest first')
        await rec.idle(1.2)
        b = await page.locator('table.q tbody tr').first.bounding_box()
        await rec.move(b['x'] + 260, b['y'] + b['height'] / 2, dur=1.2)
        await hover(rec, 'oldest rows', 3.0)

        # 2. Ranked
        x, y = await rd.center_of(page, '.seg.small button[data-view="ranked"]')
        await rec.move(x, y, dur=1.0)
        await rec.idle(0.25)
        await rec.click('Ranked')
        rec.mark('ranked')
        await rec.idle(2.2)

        # 3. hover the top row's "why this rank"
        b = await page.locator('table.q tbody tr .why').first.bounding_box()
        await rec.move(b['x'] + min(360, b['width'] * 0.45), b['y'] + 12, dur=1.1)
        await hover(rec, 'why this rank', 3.6)

        # 4. click the top row's block on the map; the list filters to it
        blk = await page.locator('table.q tbody tr td.blk').first.inner_text()
        pt = await page.evaluate("""(blk) => {
            const cs = [...document.querySelectorAll('.q-map svg circle')];
            const pick = cs.filter(c => c.dataset.block === blk).concat(cs.sort((a, b) => b.getAttribute('r') - a.getAttribute('r')));
            // the dot may sit under a neighbour; try points inside it before falling back to the largest clear dot
            for (const c of pick) {
                const b = c.getBoundingClientRect(), cx = b.x + b.width / 2, cy = b.y + b.height / 2, r = b.width / 2;
                for (const [dx, dy] of [[0, 0], [0.5, 0], [-0.5, 0], [0, 0.5], [0, -0.5], [0.35, 0.35], [-0.35, -0.35], [0.35, -0.35], [-0.35, 0.35]]) {
                    const x = cx + dx * r, y = cy + dy * r;
                    if (document.elementFromPoint(x, y) === c) return [x, y, c.dataset.block];
                }
            }
            return null;
        }""", blk)
        await rec.move(pt[0], pt[1], dur=1.3, arc=-0.10)
        await hover(rec, 'map dot', 1.2)               # the dot's tooltip shows the block
        await rec.click(f'block: {pt[2]}')
        rec.mark('block picked')
        await rec.idle(0.8)
        lb = await page.locator('table.q tbody tr').first.bounding_box()
        await rec.move(lb['x'] + 300, lb['y'] + lb['height'] / 2, dur=1.1)
        await hover(rec, 'filtered list', 3.0)

        # 5. A resident's page: Today, then after the fix
        x, y = await rd.center_of(page, '.nav a[href="status.html"]')
        await rec.move(x, y, dur=1.2)
        await rec.idle(0.2)
        await rec.click("A resident's page")
        await page.wait_for_selector('.st-card .st-status .pill', timeout=15000)
        rec.mark('status: today')
        b = await page.locator('.st-card .st-status').first.bounding_box()
        await rec.move(b['x'] + 260, b['y'] + b['height'] / 2, dur=1.0)
        await hover(rec, 'today', 3.0)
        x, y = await rd.center_of(page, '.seg.big button[data-v="after"]')
        await rec.move(x, y, dur=1.0)
        await rec.idle(0.25)
        await rec.click('After the fix')
        rec.mark('status: after')
        await rec.idle(0.6)
        b = await page.locator('.st-card .st-status').first.bounding_box()
        await rec.move(b['x'] + 420, b['y'] + b['height'] / 2, dur=1.0)
        await hover(rec, 'after', 3.6)

        # 6. CityStat: the "Closing says done" column
        x, y = await rd.center_of(page, '.nav a[href="citystat.html"]')
        await rec.move(x, y, dur=1.1)
        await rec.idle(0.2)
        await rec.click('CityStat')
        await page.wait_for_selector('table.cs th.added', timeout=15000)
        rec.mark('citystat')
        await rec.idle(0.9)
        x, y = await rd.center_of(page, 'table.cs th.added')
        await rec.move(x, y, dur=1.2)
        await hover(rec, 'closing says done header', 2.2)
        b = await page.locator('table.cs tbody tr td.added').first.bounding_box()
        await rec.move(b['x'] + b['width'] * 0.6, b['y'] + b['height'] / 2, dur=0.9)
        await hover(rec, 'debris 15.0', 3.0)
        await rec.idle(0.8)

        if a.with_data:
            # 7. the Data page: the downloads, then a calm scroll to the sources list
            x, y = await rd.center_of(page, '.nav a[href="data.html"]')
            await rec.move(x, y, dur=1.1)
            await rec.idle(0.2)
            await rec.click('Data')
            await page.wait_for_selector('table.src tbody tr', timeout=15000)
            rec.mark('data: downloads')
            await rec.idle(0.8)
            b = await page.locator('.dl-grid .dl').first.bounding_box()
            await rec.move(b['x'] + b['width'] * 0.5, b['y'] + b['height'] * 0.45, dur=1.0)
            await hover(rec, 'downloads', 2.6)
            top = await page.evaluate("(() => { const e = [...document.querySelectorAll('h2.sec')].find(h => h.textContent.startsWith('Public sources')); return e.getBoundingClientRect().top; })()")
            sx, sy = VW * 0.40, VH * 0.55
            await rec.move(sx, sy, dur=0.8)
            await rec.wheel(max(0, top - 70), 'scroll to sources', dur=2.4)
            rec.mark('data: sources')
            await rec.idle(0.6)
            b = await page.locator('table.src tbody tr').first.bounding_box()
            await rec.move(b['x'] + 260, b['y'] + b['height'] / 2, dur=1.0)
            await hover(rec, 'sources', 3.2)
            await rec.idle(0.6)

        await cdp.send('Page.stopScreencast')
        await asyncio.sleep(0.3)
        await browser.close()

    t0 = rec.frames[0][0]
    ev = {'viewport': [VW, VH], 'dpr': a.dpr, 'url': a.base,
          'frames': [[round(f[0] - t0, 4), f[1]] for f in rec.frames],
          'cursor': [[round(t - t0, 4), round(x, 1), round(y, 1)] for t, x, y in rec.cursor],
          'clicks': [[round(t - t0, 4), round(x, 1), round(y, 1), l] for t, x, y, l in rec.clicks],
          'scrolls': [[round(s - t0, 4), round(e - t0, 4), round(x, 1), round(y, 1), l] for s, e, x, y, l in rec.scrolls],
          'marks': [[round(t - t0, 4), l] for t, l in rec.marks]}
    gaps = [b[0] - a_[0] for a_, b in zip(ev['frames'], ev['frames'][1:])]
    ev['stats'] = {'frames': len(ev['frames']), 'duration_s': round(ev['frames'][-1][0], 2), 'max_gap_s': round(max(gaps), 3) if gaps else None}
    (OUT / 'events.json').write_text(json.dumps(ev))
    print(json.dumps({'stats': ev['stats'], 'clicks': ev['clicks'], 'marks': ev['marks']}, indent=1))


if __name__ == '__main__':
    asyncio.run(main())
