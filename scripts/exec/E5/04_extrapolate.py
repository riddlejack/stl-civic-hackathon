"""E5 step 4 (ESTIMATE): extend the E1 status-page shares to the whole of each sampled type.
E1 read 30 random status pages per type for the 10 largest open-past-promise types (strata O01-O10).
For those types, estimated pending = n_type x (sampled pages with a post-filing work order and no finish)/30,
estimated done = n_type x (sampled pages with a finish)/30; Wilson 95% intervals. Other types keep their
observed ledger classes. Output: build/E5/extrapolate.json
Run: .venv/bin/python -I scripts/exec/E5/04_extrapolate.py
"""
import json, math, pathlib
import duckdb
ROOT = pathlib.Path('/Users/jackriddle/Desktop/stl-civic-hackathon')
con = duckdb.connect()
con.execute(f"CREATE VIEW l AS SELECT * FROM '{ROOT / 'build/E5/private/ledger_rows.parquet'}'")
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d
rows = con.execute("""SELECT problem_code, count(*) n,
   count(*) FILTER (WHERE e1_sampled) s,
   count(*) FILTER (WHERE e1_sampled AND e1_grade = 'no_finish' AND e1_wo_post > 0) s_pend,
   count(*) FILTER (WHERE e1_sampled AND e1_grade IN ('done_late','done_by_promise')) s_done,
   count(*) FILTER (WHERE cls='b_pending_in_records') obs_b, count(*) FILTER (WHERE cls='a_done_after_filing') obs_a
 FROM l GROUP BY 1 HAVING count(*) FILTER (WHERE e1_sampled) > 0 ORDER BY n DESC""").fetchall()
out = []; est_b = est_a = 0; obs_b_s = obs_a_s = 0; n_s = 0
for pc, n, s, sp, sd, ob, oa in rows:
    lo, hi = wilson(sp, s)
    out.append({'type': pc, 'n': n, 'sampled': s, 'sampled_pending': sp, 'sampled_done': sd,
                'est_pending': round(n * sp / s), 'est_pending_lo': round(n * lo), 'est_pending_hi': round(n * hi),
                'est_done': round(n * sd / s), 'obs_b': ob, 'obs_a': oa})
    est_b += n * sp / s; est_a += n * sd / s; obs_b_s += ob; obs_a_s += oa; n_s += n
tot = con.execute("""SELECT count(*) FILTER (WHERE cls='b_pending_in_records'), count(*) FILTER (WHERE cls='a_done_after_filing') FROM l""").fetchone()
R = {'by_type': out, 'n_in_sampled_types': n_s,
     'est_pending_total': round(tot[0] - obs_b_s + est_b), 'est_done_total': round(tot[1] - obs_a_s + max(est_a, 0) + 0),
     'note': 'outside the 10 sampled types the observed ledger counts are kept; inside them the E1 share replaces the observed count'}
# keep observed done where it exceeds the E1-based estimate (records like the mowing ledger are not on status pages)
R['est_done_total_keep_max'] = round(tot[1] - obs_a_s + sum(max(r['est_done'], r['obs_a']) for r in out))
R['est_pending_total_keep_max'] = round(tot[0] - obs_b_s + sum(max(r['est_pending'], r['obs_b']) for r in out))
(ROOT / 'build/E5/extrapolate.json').write_text(json.dumps(R, indent=1))
for r in out: print(r)
print({k: v for k, v in R.items() if k != 'by_type'})
