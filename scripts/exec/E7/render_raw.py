"""E7: render the unzoomed demo (full screen, cursor and click ripples drawn, no camera moves) from a record_demo-format
recording. Uses video/tools/zoom_follow.py's cursor sprite and easing so it matches the zoomed version.

    video/.venv/bin/python scripts/exec/E7/render_raw.py --raw video/out/demo_e7 --out video/renders/demo_raw.mp4

Why not zoom_follow.py --zoom 1.0 --inset 1.0: at exactly 1.0 its shadow crop box can come out a hair below zero from
floating-point rounding, and PIL refuses a negative box ("box offset can't be negative"). The video tool is left as is.
"""
import argparse
import bisect
import importlib.util
import json
import pathlib
import subprocess

import numpy as np
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('zoom_follow', ROOT / 'video/tools/zoom_follow.py')
zf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(zf)

ap = argparse.ArgumentParser()
ap.add_argument('--raw', default=str(ROOT / 'video/out/demo_e7'))
ap.add_argument('--out', default=str(ROOT / 'video/renders/demo_raw.mp4'))
ap.add_argument('--fps', type=int, default=30)
a = ap.parse_args()
raw = pathlib.Path(a.raw)
ev = json.loads((raw / 'events.json').read_text())
VW, VH = ev['viewport']
W, H = 1920, 1080
k = W / VW
ft = [f[0] for f in ev['frames']]
fn = [f[1] for f in ev['frames']]
cur = np.array([[c[0], c[1], c[2]] for c in ev['cursor']])
n_out = int((max(ft[-1], cur[-1, 0]) + 0.25) * a.fps)


def cursor_at(t):
    i = np.searchsorted(cur[:, 0], t)
    if i <= 0:
        return cur[0, 1:]
    if i >= len(cur):
        return cur[-1, 1:]
    t0, t1 = cur[i - 1, 0], cur[i, 0]
    u = 0 if t1 == t0 else (t - t0) / (t1 - t0)
    return cur[i - 1, 1:] * (1 - u) + cur[i, 1:] * u


ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(a.fps), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', a.out], stdin=subprocess.PIPE)
sprites, cache = {}, {}
for j in range(n_out):
    t = j / a.fps
    i = max(0, bisect.bisect_right(ft, t) - 1)
    if i not in cache:
        cache.clear()
        cache[i] = Image.open(raw / fn[i]).convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
    frame = cache[i].copy()
    over = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    for ck in ev['clicks']:
        u = (t - ck[0]) / 0.45
        if 0 <= u <= 1:
            rx, ry, rr = ck[1] * k, ck[2] * k, (10 + 30 * zf.smoother(u)) * k
            d.ellipse([rx - rr, ry - rr, rx + rr, ry + rr], outline=(255, 216, 102, int(200 * (1 - u))), width=3)
    c = cursor_at(t)
    pressed = any(0 <= t - ck[0] < 0.14 for ck in ev['clicks'])
    size = int(round(24 * k * (0.86 if pressed else 1.0)))
    if size not in sprites:
        sprites[size] = zf.cursor_sprite(size)
    sp, (hx, hy) = sprites[size]
    over.alpha_composite(sp, (int(round(c[0] * k - hx)), int(round(c[1] * k - hy))))
    ff.stdin.write(Image.alpha_composite(frame, over).convert('RGB').tobytes())
ff.stdin.close()
ff.wait()
print(json.dumps({'out': a.out, 'frames': n_out, 'seconds': round(n_out / a.fps, 2)}))
