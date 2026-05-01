#!/usr/bin/env bash
# Turns build/icon-1024.png → build/icon.icns (Mac) + build/icon.ico (Windows)
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD="$ROOT/build"
SRC="$BUILD/icon-1024.png"
ICONSET="$BUILD/icon.iconset"

echo "Creating Mac iconset …"
rm -rf "$ICONSET"
mkdir -p "$ICONSET"

sips -z 16   16   "$SRC" --out "$ICONSET/icon_16x16.png"       > /dev/null
sips -z 32   32   "$SRC" --out "$ICONSET/icon_16x16@2x.png"    > /dev/null
sips -z 32   32   "$SRC" --out "$ICONSET/icon_32x32.png"       > /dev/null
sips -z 64   64   "$SRC" --out "$ICONSET/icon_32x32@2x.png"    > /dev/null
sips -z 128  128  "$SRC" --out "$ICONSET/icon_128x128.png"     > /dev/null
sips -z 256  256  "$SRC" --out "$ICONSET/icon_128x128@2x.png"  > /dev/null
sips -z 256  256  "$SRC" --out "$ICONSET/icon_256x256.png"     > /dev/null
sips -z 512  512  "$SRC" --out "$ICONSET/icon_256x256@2x.png"  > /dev/null
sips -z 512  512  "$SRC" --out "$ICONSET/icon_512x512.png"     > /dev/null
cp "$SRC"                        "$ICONSET/icon_512x512@2x.png"

iconutil -c icns "$ICONSET" -o "$BUILD/icon.icns"
echo "✓  Created build/icon.icns"

echo "Creating Windows .ico …"
python3 "$ROOT/scripts/create_ico.py"
echo "✓  Created build/icon.ico"

echo ""
echo "All icons ready."
