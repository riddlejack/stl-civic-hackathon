#!/bin/sh
# E3 captures: full-page PNGs at 1920 wide into build/E3/shots/ (needs serve.py running on 8806).
#   scripts/exec/E3/shots.sh            all pages
#   scripts/exec/E3/shots.sh one NAME URL [HEIGHT]
cd "$(dirname "$0")/../../.." || exit 1
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT=build/E3/shots
mkdir -p "$OUT"
shot() { "$CH" --headless=new --disable-gpu --hide-scrollbars --window-size=1920,${3:-1080} --virtual-time-budget=12000 --screenshot="$OUT/$1.png" "http://127.0.0.1:8806/$2" >/dev/null 2>&1; echo "$OUT/$1.png"; }
if [ "$1" = one ]; then shot "$2" "$3" "$4"; exit 0; fi
# index.html sections are at least one screen tall (min-height 100vh), so the residents page is captured per section.
shot 01-queue "queue.html"
shot 01b-queue-street "queue.html?div=STREET%20DEPT%2C%20510"
shot 01c-queue-full "queue.html" 2400
shot 02-status "status.html"
shot 02b-status-full "status.html" 2300
shot 03-landing "index.html?only=lead"
shot 03b-receipt "index.html?only=receipt" 1500
shot 04-scoreboard "index.html?only=scoreboard"
shot 04b-scoreboard-full "index.html?only=scoreboard" 2600
shot 05-dumping "index.html?only=dumping"
shot 06-methods "methods.html"
shot 06b-methods-full "methods.html" 7000
shot 06c-methods-register "methods.html#register" 1700
shot 06d-methods-appendix "methods.html#fairness" 1900
shot 07-brief-full "brief.html" 2600
