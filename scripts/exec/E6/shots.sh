#!/bin/sh
# E6 captures for the video: 1920x1080 at device scale 2 into build/E6/shots/ (needs serve.py on 8806).
#   scripts/exec/E6/shots.sh                  all ten
#   scripts/exec/E6/shots.sh one NAME URL [W H]
# The two crops (07, 08) use the page's card mode (?card=map, ?card=chart), which draws only that element.
cd "$(dirname "$0")/../../.." || exit 1
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT=${E6_SHOTS:-build/E6/shots}
BASE=${E6_BASE:-http://127.0.0.1:8806}
mkdir -p "$OUT"
shot() {
  "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=${3:-1920},${4:-1080} \
    --virtual-time-budget=15000 --screenshot="$OUT/$1.png" "$BASE/$2" >/dev/null 2>&1
  echo "$OUT/$1.png"
}
if [ "$1" = one ]; then shot "$2" "$3" "$4" "$5"; exit 0; fi
shot 01-landing "index.html"
shot 02-queue-forestry "queue.html?view=oldest"
shot 03-citystat "citystat.html"
shot 04-status-today "status.html?ex=lot&view=today"
shot 05-status-after "status.html?ex=lot&view=after"
shot 06-data "data.html"
shot 07-queue-map "queue.html?card=map" 900 1080
shot 08-citystat-chart "citystat.html?card=chart" 1400 760
shot 09-queue-ranked "queue.html"
# 10: a tight crop of 09, the ranked list's header and first four rows ("why this rank"), CSS box 497,381 to 1792,774
.venv/bin/python -I -c "from PIL import Image; Image.open('$OUT/09-queue-ranked.png').crop((994, 762, 3584, 1548)).save('$OUT/10-ranked-why.png')" && echo "$OUT/10-ranked-why.png"
