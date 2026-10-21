#!/bin/sh
# R1: trace the hand-offs. Reads build/stl.duckdb (read-only) and public files under data/raw/; writes build/R1/.
set -e
cd "$(dirname "$0")/../../.."
for s in 01_composition 02_fate 03_baseline_weeds 04_baseline_open 05_restate 06_checks 07_figures; do
  echo "== $s"
  .venv/bin/python -I scripts/night/R1/$s.py > build/R1/log_$s.txt 2>&1 || { tail -20 build/R1/log_$s.txt; exit 1; }
  tail -3 build/R1/log_$s.txt
done
