#!/bin/sh
# Screenshot every section at 1920x1080 into build/N6/shots/ (needs serve.py running on 8806).
cd "$(dirname "$0")/../../.." || exit 1
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT=build/N6/shots
mkdir -p "$OUT"
shot() { "$CH" --headless=new --disable-gpu --hide-scrollbars --window-size=1920,${3:-1080} --virtual-time-budget=8000 --screenshot="$OUT/$1.png" "http://127.0.0.1:8806/$2" >/dev/null 2>&1; echo "$OUT/$1.png"; }
shot 01-landing "index.html?only=lead"
shot 02-receipt "index.html?only=receipt"
shot 03-scoreboard "index.html?only=scoreboard"
shot 03b-scoreboard-full "index.html?only=scoreboard" 2200
shot 04-fairness "index.html?only=fairness"
shot 04b-fairness-full "index.html?only=fairness" 1500
shot 05-dumping "index.html?only=dumping"
shot 06-brief "brief.html"
shot 06b-brief-full "brief.html" 2600
shot 07-methods "methods.html"
shot 07b-methods-full "methods.html" 4200
