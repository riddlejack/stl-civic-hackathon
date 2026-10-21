#!/bin/sh
# N5 hero cases: rebuild from files on disk (run from the repo root). Imagery step fetches from MSDIS (keyless).
# Needs build/N5/private/hero_ids.json (git-ignored): the hero lots' parcel ids and the parcels 03 validates.
set -e
export CSB_DIR=build/csb-clean
PY=".venv/bin/python -I"
$PY scripts/night/N5/01_build_db.py
$PY scripts/night/N5/02_lot_candidates.py > build/N5/private/02_lot_candidates.log
$PY scripts/night/N5/03_lot_validate.py > build/N5/private/03_lot_validate.log
$PY scripts/night/N5/04_heroes.py > build/N5/private/04_heroes.log
$PY scripts/night/N5/05_imagery.py
$PY scripts/night/N5/06_publish.py
