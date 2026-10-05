#!/bin/sh
# Renders a local HTML file to a PNG with headless Chrome.
# Usage: tools/render.sh <file.html[#hash]> <output.png> <width> <height>
set -eu

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE="${TMPDIR:-/tmp}/adamwhansen-render-profile"
SRC_FILE="${1%%#*}"
HASH=""
case "$1" in *"#"*) HASH="#${1#*#}" ;; esac
URL="file://$(cd "$(dirname "$SRC_FILE")" && pwd)/$(basename "$SRC_FILE")$HASH"

rm -f "$2"
# Pages should draw at a fixed size from the top-left corner: Chrome enforces a
# minimum window size and crops the screenshot to <width>×<height>.
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --default-background-color=00000000 \
  --user-data-dir="$PROFILE" --window-size="$3,$4" --screenshot="$2" "$URL" >/dev/null 2>&1 &

# Headless Chrome writes the screenshot but doesn't always exit, so wait for the file and stop it.
i=0
while [ ! -s "$2" ] && [ "$i" -lt 40 ]; do sleep 0.5; i=$((i + 1)); done
sleep 0.5
pkill -f "user-data-dir=$PROFILE" 2>/dev/null || true

if [ -s "$2" ]; then echo "wrote $2"; else echo "failed to render $1" >&2; exit 1; fi
