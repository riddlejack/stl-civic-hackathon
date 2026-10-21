"""N3 step 8: charts (PNG, matplotlib) into build/N3/.
  N3-decomposition-ward1-vs-ward10.png  CityStat's ward 1 vs ward 10 gap split into its parts (one bar)
  N3-towing-by-ward.png                 the top robust comparison: towing, per ward, same closing words, promise line
  N3-done-class-by-type.png             done-class medians, wards 1-5 vs 10-14, after the tornado (where the gap is not)
  N3-single-light-by-quarter.png        single light out, done-class median by quarter (why it is not robust)
Palette: the dataviz skill's reference categorical order (validated light mode; low-contrast slots direct-labelled).
Run: .venv/bin/python -I scripts/night/N3/08_charts.py
"""
import json, os, csv, duckdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = '.'
OUT = os.path.join(ROOT, 'build/N3')
REQ = os.path.join(OUT, 'req.parquet')
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'
S1, S2, S3, S4, S5, GRAY = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#a3a29d'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.edgecolor': GRID, 'axes.labelcolor': INK2,
                     'xtick.color': INK2, 'ytick.color': INK2, 'figure.facecolor': SURF, 'axes.facecolor': SURF,
                     'savefig.facecolor': SURF})
SOURCE = 'Source: City of St. Louis CSB 311 file (csb.zip), one row per REQUESTID; closure classes from N2. N3 analysis, 13 Oct 2026.'

def style(ax, grid_axis='x'):
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, lw=0.8); ax.set_axisbelow(True)

# 1. decomposition bar
dec = json.load(open(os.path.join(OUT, 'decomposition.json')))['citystat_window_snapshot_2026-07-10 | ward 1 vs ward 10']
sb = dec['speed_by_class']
parts = [('Ward 1 average', dec['A_mean'], GRAY),
         ('Mix of request types', dec['type_mix'], S4),
         ('Closing words used\n(share hand-off, no-action...)', dec['closing_practice'], S5),
         ('Slower: closures recording\nwork done', sb.get('done', 0), S3),
         ('Slower: hand-off closures\n(referred, tagged, scheduled)', sb.get('handed_off', 0), S1),
         ('Slower: no-action and\nother closures', sum(v for k, v in sb.items() if k not in ('done', 'handed_off')), S2)]
fig, ax = plt.subplots(figsize=(10, 3.8))
left = 0
# (label y, ha, x offset) per segment, placed by hand so labels do not collide
place = [(-0.45, 'center', 0), (0.85, 'right', -0.3), (-0.45, 'right', 0.6), (0.45, 'center', 0), (-0.45, 'center', 0.8), (0.45, 'center', 0)]
for i, (lab, v, col) in enumerate(parts):
    ax.barh(0, v, left=left, color=col, edgecolor=SURF, linewidth=2, height=0.5)
    mid = left + v / 2; ytxt, ha, dx = place[i]
    ax.annotate(f'{lab}\n{v:+.1f} d' if i else f'{lab}\n{v:.1f} d', xy=(mid, 0.25 if ytxt > 0 else -0.25), xytext=(mid + dx, ytxt),
                ha=ha, va='bottom' if ytxt > 0 else 'top', fontsize=8.5, color=INK,
                arrowprops=dict(arrowstyle='-', color=INK2, lw=0.6))
    left += v
ax.axvline(dec['B_mean'], color=INK, lw=1, ls=':')
ax.text(dec['B_mean'], -0.95, f"Ward 10 average {dec['B_mean']:.1f} d", ha='right', fontsize=9, color=INK)
ax.set_ylim(-1.1, 1.35); ax.set_yticks([]); ax.set_xlim(0, 36); ax.set_xlabel('mean days to close (CityStat\'s metric)')
style(ax)
ax.set_title("CityStat's ward gap (ward 1 vs ward 10) is mostly slower handling of the same request, closed the same way",
             loc='left', fontsize=11, color=INK)
fig.text(0.01, 0.01, 'All channels, filed 1 Jan 2024-30 Jun 2026, closed by 10 Jul 2026 (reproduces CityStat 17.2 vs 35.1 to within 2 days). '
         'Kitagawa two-level decomposition; exact.\n' + SOURCE, fontsize=7, color=INK2)
fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(os.path.join(OUT, 'N3-decomposition-ward1-vs-ward10.png'), dpi=160); plt.close(fig)

# 2. towing by ward
con = duckdb.connect()
q = f"""SELECT ward, count(*) FILTER (WHERE resolution='vehicle tagged for tow') n1,
          median(days_close) FILTER (WHERE resolution='vehicle tagged for tow') m1,
          count(*) FILTER (WHERE t_invt IS NOT NULL AND t_invt >= t_init) n2,
          median(epoch(t_invt - t_init)/86400.0) FILTER (WHERE t_invt IS NOT NULL AND t_invt >= t_init) m2
        FROM '{REQ}' WHERE channel='resident' AND ptype='Vehicle Towing' AND period='after' AND ward BETWEEN '01' AND '14'
        GROUP BY 1 ORDER BY 1"""
rows = con.execute(q).fetchall()
fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
for ax, (idx_n, idx_m, title) in zip(axes, [(1, 2, 'Days to "vehicle tagged for tow" (same closing words)'),
                                           (3, 4, 'Days to the "investigation done" stamp (DATEINVTDONE):\nabout 1 day in wards 1-5 although tags take 6-15 days there,\nso this stamp marks a desk step, not the visit')]):
    for w, *vals in rows:
        r = (w,) + tuple(vals); n, m = r[idx_n], r[idx_m]
        col = S1 if w <= '05' else (S2 if w >= '10' else GRAY)
        ax.bar(int(w), m, color=col, width=0.7, edgecolor=SURF, linewidth=2)
        ax.text(int(w), m + 0.8, f'{m:.0f}', ha='center', fontsize=8, color=INK)
        ax.text(int(w), -4.5, f'n {n}', ha='center', fontsize=6.5, color=INK2)
    ax.axhline(5, color=INK, lw=1, ls='--'); ax.text(14.55, 6.2, 'city promise:\n5 days', ha='left', va='bottom', fontsize=8, color=INK)
    ax.set_xticks(range(1, 15)); ax.set_xlabel('ward'); ax.set_title(title, loc='left', fontsize=10, color=INK)
    ax.set_ylim(-6, 65); ax.set_xlim(0.4, 16.3); style(ax, 'y')
axes[0].set_ylabel('median days, resident requests')
axes[0].text(1, 58, 'wards 1-5', color=S1, fontsize=9, fontweight='bold'); axes[0].text(6, 58, 'wards 6-9', color=INK2, fontsize=9, fontweight='bold')
axes[0].text(10.6, 50, 'wards 10-14', color=S2, fontsize=9, fontweight='bold')
fig.suptitle('Towing requests: the north waits longer for the same first step (filed 16 May 2025-13 Oct 2026)', x=0.01, ha='left', fontsize=11, color=INK)
fig.text(0.01, 0.01, 'Promise = PRJCOMPLETEDATE minus filing, 5 days for every towing request. Same gap before the tornado (16 vs 36 days tagged, wards 1-5 vs 10-14).\n' + SOURCE, fontsize=7, color=INK2)
fig.tight_layout(rect=(0, 0.06, 1, 0.95)); fig.savefig(os.path.join(OUT, 'N3-towing-by-ward.png'), dpi=160); plt.close(fig)

# 3. done-class dumbbell, after the tornado, n >= 100 each side
rc = [r for r in csv.DictReader(open(os.path.join(OUT, 'robust_comparisons.csv')))
      if r['measure'] == 'done-class' and r['period'] == 'after' and int(r['n_south']) >= 100 and int(r['n_north']) >= 100]
prom = {r['ptype']: float(r['promise_days_median']) for r in csv.DictReader(open(os.path.join(OUT, 'like_for_like_by_group.csv')))
        if r['period'] == 'after' and r['unit'] == 'w01-05' and r['promise_days_median']}
rc.sort(key=lambda r: float(r['med_north']) / max(float(r['med_south']), 0.01))
fig, ax = plt.subplots(figsize=(9, 0.42 * len(rc) + 1.6))
for i, r in enumerate(rc):
    s, n = float(r['med_south']), float(r['med_north'])
    ax.plot([s, n], [i, i], color=GRID, lw=2, zorder=1)
    ax.scatter([s], [i], s=60, color=S1, zorder=3, edgecolor=SURF, linewidth=1.5)
    ax.scatter([n], [i], s=60, color=S2, zorder=3, edgecolor=SURF, linewidth=1.5)
    if r['ptype'] in prom: ax.scatter([prom[r['ptype']]], [i], marker='|', s=120, color=INK, zorder=2)
    ax.text(51, i, f"x{float(r['ratio']):.1f}  (n {r['n_south']}/{r['n_north']})", va='center', fontsize=8, color=INK2)
ax.set_yticks(range(len(rc))); ax.set_yticklabels([r['ptype'] for r in rc], fontsize=8.5)
ax.set_xlim(0, 62); ax.set_xlabel('median days to close, closures whose words record the work as done')
ax.scatter([], [], color=S1, label='wards 1-5'); ax.scatter([], [], color=S2, label='wards 10-14')
ax.scatter([], [], marker='|', color=INK, s=120, label='city promise (median)')
ax.legend(loc='lower left', bbox_to_anchor=(0, 1.0), ncol=3, frameon=False, fontsize=8.5); style(ax)
ax.set_title('Where the closing words say the work was done, most types show little ward gap\n(resident requests filed 16 May 2025-13 Oct 2026)', loc='left', fontsize=11, color=INK, pad=24)
fig.text(0.01, 0.01, SOURCE, fontsize=7, color=INK2)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(OUT, 'N3-done-class-by-type.png'), dpi=160); plt.close(fig)

# 4. single light out by quarter
q = f"""SELECT date_trunc('quarter', t_init)::DATE qq, wgroup, count(*) FILTER (WHERE class='done') n,
          median(days_close) FILTER (WHERE class='done') m
        FROM '{REQ}' WHERE channel='resident' AND ptype='Single Light Out' AND wgroup IN ('w01-05','w10-14')
        AND t_init >= '2024-01-01' AND t_init < '2026-07-01' GROUP BY ALL ORDER BY 1"""
d = {}
for qq, g, n, m in con.execute(q).fetchall(): d.setdefault(g, []).append((qq, m, n))
fig, ax = plt.subplots(figsize=(9, 3.6))
for g, col, lab in (('w01-05', S1, 'wards 1-5'), ('w10-14', S2, 'wards 10-14')):
    xs = [x for x, _, _ in d[g]]; ys = [y for _, y, _ in d[g]]
    ax.plot(xs, ys, color=col, lw=2, marker='o', ms=6, label=lab, markeredgecolor=SURF)
ax.axhline(3, color=INK, lw=1, ls='--'); ax.text(d['w01-05'][-1][0], 5.5, 'city promise: 3 days', ha='right', fontsize=8, color=INK)
ax.axvline(duckdb.sql("SELECT DATE '2025-05-16'").fetchone()[0], color=INK2, lw=0.8, ls=':')
ax.text(duckdb.sql("SELECT DATE '2025-05-20'").fetchone()[0], 60, 'tornado', fontsize=8, color=INK2)
ax.set_ylabel('median days, "work completed"'); ax.legend(frameon=False, fontsize=8.5, loc='upper left'); style(ax, 'y')
ax.set_title('Single light out: the ward gap is a two-quarter episode (Oct 2025-Mar 2026), not a standing pattern', loc='left', fontsize=11, color=INK)
fig.text(0.01, 0.01, 'Resident requests by quarter filed, done-class closures; quarters after Jun 2026 omitted (a third of north requests still open).\n' + SOURCE, fontsize=7, color=INK2)
fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(os.path.join(OUT, 'N3-single-light-by-quarter.png'), dpi=160); plt.close(fig)
print('charts written')
