"""E7: drop the blank frames Chrome paints for a moment during a page navigation, so the demo holds the previous page
instead of flashing white. Edits only the frame list in events.json (the JPEGs stay); run before zoom_follow.py.

    video/.venv/bin/python scripts/exec/E7/drop_blank_frames.py [video/out/demo_e7]

A frame counts as blank when its greyscale standard deviation is under 2 (a page with any text or rule is above 25).
"""
import json
import pathlib
import sys

import numpy as np
from PIL import Image

raw = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[3] / 'video/out/demo_e7')
ev = json.loads((raw / 'events.json').read_text())
keep, dropped = [], []
for t, f in ev['frames']:
    a = np.asarray(Image.open(raw / f).convert('L').resize((480, 270)), dtype=float)
    (dropped if a.std() < 2 and keep else keep).append([t, f])
ev['frames'] = keep
ev.setdefault('notes', []).append(f'drop_blank_frames.py removed {len(dropped)} blank navigation frames: {[d[0] for d in dropped]}')
(raw / 'events.json').write_text(json.dumps(ev))
print(f'kept {len(keep)} frames, dropped {len(dropped)} blank: {[d[0] for d in dropped]}')
