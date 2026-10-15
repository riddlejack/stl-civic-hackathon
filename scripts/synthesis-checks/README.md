# Synthesis-session checks (13 Oct 2026)

Reconstructions of the inline checks run during the synthesis thread, so the figures in
`research/synthesis.md` sections 8–9 can be reproduced. Setup:

```bash
mkdir -p build/csb-unzipped && unzip -o -q data/raw/stlouis-mo.gov/files/csb.zip -d build/csb-unzipped
cd scripts/synthesis-checks && python3 -I 01_refile_after_closure.py
```

Each script prints the figures recorded in `research/synthesis-notes.md` (expect exact matches
for 01, 03, 04, 05, 06, 07; 02 depends on the address normaliser and should match within a point).
No personal data is read.
