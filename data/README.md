# Data

Every figure in this repository comes from files that the City of St. Louis, or the
Metropolitan St. Louis Sewer District (MSD), publish. `MANIFEST.csv` lists each file the
scripts and reports use: where it came from, when it was retrieved, its size and SHA-256,
how many rows it has, which figures or reports use it, and which of three tiers it is in.

## The three tiers

**1. In this repository (`data/public/`).** Small files the city publishes that a figure
uses directly, copied unchanged. The manifest's `published_as` column gives the path. A file
is copied only if it is under 5 MB, comes from the city, and passes the same privacy scan as
the rest of the repository (`scripts/exec/E4/scan_public.py`).

**2. Downloaded by a script.** Files too large for GitHub (the 311 file is 128 MB, the
Forestry ledger 293 MB), and files that hold exact addresses, parcel numbers or request
numbers. Run

    bash scripts/data/fetch_public.sh
    bash scripts/night/N1/run_all.sh

The first command downloads them from the city into `data/raw/` (about 600 MB, one request
a second). The second rebuilds the database and every export. The city updates most of
these files every day, so a new download gives today's numbers. Compare a file's SHA-256 with
the manifest to see whether it has changed since our run. `fetch_public.sh --check` asks each
source for its size or row count without downloading anything.

**3. Listed but not published.** The manifest names these so that every claim can be
traced to its source, but the rows are not in this repository:

- *The Cityworks extracts* read on 14 October 2026 under the City's authorisation at the
  hackathon office hours. That authorisation covered reading the data for this entry, not
  republishing it, and every row carries a work-order or request number that leads to an
  address. What is published: the retrieval manifest
  (`research/cityworks-retrieval-manifest.csv`) and the aggregate tables
  (`research/cityworks-*-aggregate*.csv` and `.json`, `research/cityworks-department-gap-matrix.csv`).
- *The 311 status-page sample* (1,440 pages read on 14 October). Each page shows a request
  number that leads to an address. What is published: the sample design
  (`build/E1/sample_strata.csv`, `build/E1/sample_meta.json`) and the results by service and
  division (`build/E1/service_table.csv` and the `linkage_*` tables).
- Other files that hold addresses, ids or coordinates and that the pipeline does not need,
  and a few sources whose download address was not logged. The note column says which.

## What is never here

No personal data: no names, owner fields, staff fields or e-mail addresses; no request,
work-order or parcel numbers; nothing more precise than a block ("1700 block of N Taylor Av").
The download script does not ask for person-name fields: the MSD parcel query leaves out
the owner field, and the Cityworks saved searches ask only for the operational fields the
pipeline uses. Personal data that the city's systems expose publicly is not used here in any
form and is not listed.

## Reading the manifest

| Column | Meaning |
|---|---|
| `name` | What the file is |
| `url` | Where it was downloaded from |
| `retrieved_central` | When, in Central time: from the retrieval log where one exists, otherwise the file's time on disk (the note says so) |
| `bytes`, `sha256` | Size and fingerprint of the file as used. For a folder or file pattern: the total size, and a fingerprint of the list of its files' fingerprints |
| `rows` | Data rows, where known; for a folder, the number of files |
| `used_by` | The figures and the files in this repository that read or cite it |
| `tier` | `vendored`, `fetched by script` or `not published` |
| `path` | Where the scripts expect it, under `data/raw/` |
| `published_as` | For vendored files, the copy in `data/public/` |
| `note` | Why a file is in its tier, and any caveat |
