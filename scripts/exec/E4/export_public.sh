#!/usr/bin/env bash
# Export a clean public copy of this repository: one commit, no history, no remote.
#
#   bash scripts/exec/E4/export_public.sh [DEST] [--retry-fixable] [--drop-failing] [--no-commit] [--no-ocr]
#
# DEST defaults to ../stl-civic-hackathon-public (beside the working repository).
# 1. Copies the files that scripts/exec/E4/ALLOWLIST.md admits ("-" rules beat "+" rules).
# 2. Adds README.md (from deliverable/README.md), LICENSE (MIT, Jack Riddle) and a .gitignore,
#    and the data tier: data/README.md, scripts/data/fetch_public.sh, data/MANIFEST.csv and the
#    vendored files in data/public/ (scripts/exec/E4/build_manifest.py).
# 3. Runs scripts/exec/E4/scan_public.py over the copy. Any hit stops the export before the
#    commit, unless --drop-failing is given: then failing files are deleted from the copy,
#    the scan is re-run, and the dropped files are listed in DEST/.git/e4-dropped.txt.
#    --retry-fixable ignores the "- path  # scan-fix: ..." rules, so files that failed only
#    on a small wording fix come back if their owner has fixed them.
# 4. git init + one commit in DEST. No remote is added and nothing is pushed.
#
# The working repository is only read. DEST must be outside it, and is wiped only if it is
# empty or was made by this script (marker DEST/.git/e4-public-export).
set -euo pipefail
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
DEST=""; DROP=0; COMMIT=1; OCR=""; RETRY=0
for arg in "$@"; do
  case "$arg" in
    --drop-failing) DROP=1 ;;
    --retry-fixable) RETRY=1 ;;
    --no-commit) COMMIT=0 ;;
    --no-ocr) OCR="--no-ocr" ;;
    -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
    -*) echo "export_public: unknown option $arg" >&2; exit 2 ;;
    *) DEST="$arg" ;;
  esac
done
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY="$(command -v python3)"
DEST="$("$PY" -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "${DEST:-$REPO/../stl-civic-hackathon-public}")"

case "$DEST/" in "$REPO/"*) echo "export_public: DEST $DEST is inside the working repository; refusing" >&2; exit 2 ;; esac
case "$REPO/" in "$DEST/"*) echo "export_public: the working repository is inside DEST $DEST; refusing" >&2; exit 2 ;; esac
mkdir -p "$DEST"
if [ -n "$(ls -A "$DEST")" ] && [ ! -f "$DEST/.git/e4-public-export" ]; then
  echo "export_public: $DEST is not empty and was not made by this script; refusing to wipe it" >&2; exit 2
fi
find "$DEST" -mindepth 1 -maxdepth 1 -exec rm -rf {} +

echo "export_public: $REPO -> $DEST"
"$PY" - "$REPO" "$DEST" "$HERE/ALLOWLIST.md" "$RETRY" <<'PY'
import os, re, shutil, sys
repo, dest, allow, retry = sys.argv[1:5]
block = re.search(r'```rules\n(.*?)```', open(allow, encoding='utf-8').read(), re.S).group(1)
rules, skipped = [], 0
for raw in block.splitlines():
    line, _, comment = raw.partition('#')
    line = line.strip()
    if retry == '1' and comment.strip().startswith('scan-fix:'):
        skipped += 1
        continue
    if line[:2] in ('+ ', '- '):
        rules.append((line[0], line[2:].strip()))
if skipped:
    print(f'export_public: --retry-fixable: ignoring {skipped} scan-fix exclusions')

def rx(pat):
    out, i = '', 0
    while i < len(pat):
        if pat.startswith('**/', i): out += '(?:.*/)?'; i += 3
        elif pat.startswith('**', i): out += '.*'; i += 2
        elif pat[i] == '*': out += '[^/]*'; i += 1
        elif pat[i] == '?': out += '[^/]'; i += 1
        else: out += re.escape(pat[i]); i += 1
    return re.compile(out + r'\Z')

inc = [rx(p) for s, p in rules if s == '+']
exc = [(rx(p), p) for s, p in rules if s == '-']
# folders a "-" rule removes whole, pruned before walking (data/raw alone is 8 GB)
prune = [rx(p[:-3]) for s, p in rules if s == '-' and p.endswith('/**')]
n = 0
for dp, dn, fn in os.walk(repo):
    rel_dir = os.path.relpath(dp, repo)
    rel_dir = '' if rel_dir == '.' else rel_dir + '/'
    dn[:] = [d for d in dn if not any(r.match(rel_dir + d) for r in prune)]
    for f in fn:
        rel = rel_dir + f
        if os.path.islink(os.path.join(dp, f)):
            continue
        if any(r.match(rel) for r, _ in exc) or not any(r.match(rel) for r in inc):
            continue
        os.makedirs(os.path.join(dest, rel_dir), exist_ok=True)
        shutil.copy2(os.path.join(dp, f), os.path.join(dest, rel))
        n += 1
print(f'export_public: copied {n} files')
PY

cp "$REPO/deliverable/README.md" "$DEST/README.md"
cat > "$DEST/LICENSE" <<EOF
MIT License

Copyright (c) $(date +%Y) Jack Riddle

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
cat > "$DEST/.gitignore" <<'EOF'
# The pipeline reads the city's files from data/raw/ and writes row-level copies to build/.
# Keep both out of git: they hold addresses and ids.
data/raw/
build/*/private/
*.duckdb
*.duckdb.wal
*.parquet
.venv/
__pycache__/
.DS_Store
.env
EOF

mkdir -p "$DEST/data" "$DEST/scripts/data"
cp "$HERE/public-data/README.md" "$DEST/data/README.md"
cp "$HERE/public-data/fetch_public.sh" "$DEST/scripts/data/fetch_public.sh"
chmod +x "$DEST/scripts/data/fetch_public.sh"
"$PY" "$HERE/build_manifest.py" "$DEST" --repo "$REPO" --vendor

git -C "$DEST" init -q
touch "$DEST/.git/e4-public-export"

SCAN=("$PY" "$HERE/scan_public.py" "$DEST" --repo "$REPO" --failing-files "$DEST/.git/e4-failing.txt")
[ -n "$OCR" ] && SCAN+=("$OCR")
if ! "${SCAN[@]}"; then
  if [ "$DROP" -eq 0 ]; then
    echo "export_public: scan failed; nothing committed. Fix the files at source, or add '-' lines to" >&2
    echo "  $HERE/ALLOWLIST.md, or re-run with --drop-failing. Failing files: $DEST/.git/e4-failing.txt" >&2
    exit 1
  fi
  echo "export_public: --drop-failing: removing these files from the copy:"
  while IFS= read -r rel; do
    [ -n "$rel" ] || continue
    echo "  - $rel"; rm -f "$DEST/$rel"
  done < "$DEST/.git/e4-failing.txt"
  cp "$DEST/.git/e4-failing.txt" "$DEST/.git/e4-dropped.txt"
  if grep -q '^site/' "$DEST/.git/e4-dropped.txt"; then
    echo "export_public: WARNING: site files were dropped; the public site will break or show mock data for:" >&2
    grep '^site/' "$DEST/.git/e4-dropped.txt" | sed 's/^/    /' >&2
  fi
  find "$DEST" -mindepth 1 -type d -empty -not -path "$DEST/.git" -not -path "$DEST/.git/*" -delete
  # rebuild the manifest so no row cites a dropped file
  rm -rf "$DEST/data/public" "$DEST/data/MANIFEST.csv"
  "$PY" "$HERE/build_manifest.py" "$DEST" --repo "$REPO" --vendor
  "${SCAN[@]}" || { echo "export_public: scan still fails after dropping; nothing committed" >&2; exit 1; }
fi

if [ "$COMMIT" -eq 1 ]; then
  NAME="${PUBLIC_GIT_NAME:-$(git -C "$REPO" config user.name || echo 'Jack Riddle')}"
  EMAIL="${PUBLIC_GIT_EMAIL:-$(git -C "$REPO" config user.email || true)}"
  git -C "$DEST" add -A
  git -C "$DEST" -c user.name="$NAME" -c user.email="$EMAIL" -c commit.gpgsign=false \
    commit -q -m "DoneStat: public snapshot, $(date '+%-d %b %Y %H:%M %Z')" \
    -m "Exported from the private working repository by scripts/exec/E4/export_public.sh. Raw data, databases and build/*/private/ are not included; see scripts/exec/E4/ALLOWLIST.md." \
    -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
  echo "export_public: committed $(git -C "$DEST" rev-parse --short HEAD) ($(git -C "$DEST" ls-files | wc -l | tr -d ' ') files)"
fi
echo "export_public: done. No remote was added. To publish, Jack adds one himself (GitHub) or zips $DEST (Dropbox)."
