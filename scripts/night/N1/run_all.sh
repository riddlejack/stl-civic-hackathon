#!/usr/bin/env bash
# DoneStat pipeline (N1): rebuild build/stl.duckdb and build/out/ from the public files on disk.
# Needs Python 3 with duckdb, pyarrow, numpy and matplotlib (all free). No key, no network.
#   bash scripts/night/N1/run_all.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
PY="${PYTHON:-$ROOT/.venv/bin/python}"
mkdir -p "$ROOT/build/N1" "$ROOT/build/out"
start=$(date +%s)
"$PY" -I "$ROOT/scripts/night/N1/normalise.py"
"$PY" -I "$ROOT/scripts/night/N1/build_db.py"
"$PY" -I "$ROOT/scripts/night/N1/export.py"
"$PY" -I "$ROOT/scripts/night/N1/validate.py" > "$ROOT/build/N1/validation.txt"
"$PY" -I "$ROOT/scripts/night/N1/match_rates.py" > "$ROOT/build/N1/match_rates.txt"
"$PY" -I "$ROOT/scripts/night/N1/privacy_check.py"
end=$(date +%s)
echo "run_all.sh finished in $((end - start)) s" | tee "$ROOT/build/N1/run_seconds.txt"
