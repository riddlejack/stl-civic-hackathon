#!/usr/bin/env bash
# R2: re-reports by closing class, new traces, bounded extrapolation.
# Reads build/stl.duckdb (N1) and build/R1/* read-only; writes build/R2/.
# The hunt downloads (build/R2/private/raw/) must already be on disk; no network is used here.
set -euo pipefail
cd "$(dirname "$0")/../../.."
PY=".venv/bin/python -I"
$PY scripts/night/R2/01_rereport.py
$PY scripts/night/R2/02_summary.py > /dev/null
$PY scripts/night/R2/03_proxy_check.py > /dev/null
$PY scripts/night/R2/06_tree_planting.py > /dev/null
$PY scripts/night/R2/04_extrapolate.py > /dev/null
$PY scripts/night/R2/07_rereport_spatial.py > /dev/null
$PY scripts/night/R2/08_tornado_debris.py > /dev/null
$PY scripts/night/R2/05_figures.py
