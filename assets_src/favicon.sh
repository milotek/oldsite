#!/usr/bin/env bash
# Favicon: a single 35mm frame with its sprocket holes, in the site accent.
set -eu
magick -size 128x128 xc:'#11111b' \
  -fill '#ffbdbd' \
  -draw 'roundrectangle 12,34 115,93 3,3' \
  -fill '#11111b' -draw 'roundrectangle 20,44 107,83 2,2' \
  -fill '#ffbdbd' \
  -draw 'roundrectangle 16,16 32,28 3,3  roundrectangle 40,16 56,28 3,3  roundrectangle 64,16 80,28 3,3  roundrectangle 88,16 104,28 3,3' \
  -draw 'roundrectangle 16,99 32,111 3,3 roundrectangle 40,99 56,111 3,3 roundrectangle 64,99 80,111 3,3 roundrectangle 88,99 104,111 3,3' \
  static/favicon.png
magick static/favicon.png -resize 32x32 -define icon:auto-resize=32,16 static/favicon.ico
