#!/usr/bin/env bash
# One-off image prep: full-size view copies plus contact-sheet frames.
# Every frame is 840x560 (35mm, 3:2) because a contact sheet only reads as one
# if the grid is dead regular. Wide sources are cropped to fill; anything squarer
# than 1.2:1 is letterboxed onto film base instead, since cropping a phone
# screenshot or a portrait drawing to 3:2 throws away the subject.
set -eu
R=assets_src/raw
FULL=static/img/full
FRAME=static/img/frame
BASE='#0d0d15'
mkdir -p "$FULL" "$FRAME"

for src in "$R"/*.jpg "$R"/*.png "$R"/*.gif; do
  [ -e "$src" ] || continue
  base=$(basename "$src"); name="${base%.*}"
  case "$name" in cv|old_favicon) continue;; esac

  if [ "${base##*.}" = "gif" ]; then
    cp "$src" "$FULL/$name.gif"
  else
    magick "$src" -auto-orient -resize '1400x1400>' -strip -quality 84 "$FULL/$name.jpg"
  fi

  read -r w h <<< "$(identify -format '%w %h' "${src}[0]")"
  if [ "$(( w * 10 / h ))" -ge 12 ]; then
    magick "${src}[0]" -auto-orient -resize '840x560^' -gravity center -extent 840x560 \
      -strip -quality 82 "$FRAME/$name.jpg"
  else
    magick "${src}[0]" -auto-orient -resize '840x560' -background "$BASE" -gravity center \
      -extent 840x560 -strip -quality 82 "$FRAME/$name.jpg"
  fi
done
