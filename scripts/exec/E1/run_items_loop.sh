#!/bin/sh
# Re-run the related-items reader every 2 minutes while the page fetcher runs, then once more.
cd "$(dirname "$0")/../../.."
while pgrep -f scripts/exec/E1/02_fetch.py > /dev/null; do
  .venv/bin/python -I scripts/exec/E1/06_items.py >> build/E1/private/items_run.log 2>&1
  sleep 120
done
.venv/bin/python -I scripts/exec/E1/06_items.py >> build/E1/private/items_run.log 2>&1
echo "items loop finished $(date)" >> build/E1/private/items_run.log
