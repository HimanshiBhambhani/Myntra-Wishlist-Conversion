#!/bin/bash
# Render each mockup to a PNG at exactly 390x844 (2x for retina-quality deck slides).
# Chrome's own updater can hang after a headless run, so we background it and kill on exit.

cd "$(dirname "$0")" || exit 1
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p render

for f in [0-9]*.html; do
  name="${f%.html}"
  rm -f "render/$name.png"
  "$CHROME" --headless --disable-gpu --no-sandbox \
    --user-data-dir="$PWD/.chrome-tmp" \
    --force-device-scale-factor=2 \
    --screenshot="$PWD/render/$name.png" \
    --window-size=454,908 \
    --hide-scrollbars \
    "file://$PWD/$f" >/dev/null 2>&1 &
  pid=$!
  # the screenshot lands well before Chrome finishes tearing down
  for _ in $(seq 1 40); do
    [ -s "render/$name.png" ] && break
    sleep 0.25
  done
  sleep 0.5
  kill "$pid" 2>/dev/null
  echo "rendered $name.png"
done

pkill -f "chrome-tmp" 2>/dev/null
rm -rf .chrome-tmp
exit 0
