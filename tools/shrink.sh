#!/usr/bin/env bash
# Turn a source image into the 1400px + 720px WebP pair the templates expect.
#   tools/shrink.sh screenshot.png assets/img/projects/thing-1
set -euo pipefail
src=$1
out=$2
magick "$src" -auto-orient -resize '1400x>' -quality 78 -define webp:method=6 "$out.webp"
magick "$src" -auto-orient -resize '720x>'  -quality 72 -define webp:method=6 "$out.thumb.webp"
echo "wrote $out.webp and $out.thumb.webp"
