#!/usr/bin/env bash
# Generates the 88x31s. Antialiasing is off on purpose: it is the only reason
# these read as buttons rather than as small pictures of words.
set -eu
OUT=static/buttons
mkdir -p "$OUT"
F="DejaVu-Sans-Condensed-Bold"

btn() { # btn <file> <block-bg> <block-glyph> <line1> <line2>
  local file=$1 bbg=$2 glyph=$3 l1=$4 l2=$5
  magick -size 88x31 xc:'#11111b' \
    -fill "$bbg" -draw 'rectangle 0,0 19,30' \
    +antialias -font "$F" \
    -fill '#11111b' -pointsize 15 -gravity NorthWest -annotate +6+7 "$glyph" \
    -fill '#cdd6f4' -pointsize 10 -annotate +24+5 "$l1" \
    -fill '#ffbdbd' -pointsize 10 -annotate +24+17 "$l2" \
    -fill none -stroke '#313244' -strokewidth 1 -draw 'rectangle 0.5,0.5 87.5,30.5' \
    "$OUT/$file"
}

btn milotek.png  '#ffbdbd' 'm' 'milo tek'   'furfag.lol'
btn nixos.png    '#89b4fa' 'N' 'powered by' 'NixOS'
btn godot.png    '#94e2d5' 'G' 'made with'  'Godot'
btn handmade.png '#f9e2af' '<' 'hand-made'  'plain HTML'
btn source.png   '#fab387' 'V' 'valve'      'SOURCE'
btn nojs.png     '#a6e3a1' '0' 'zero'       'javascript'
btn pixeljam.png '#cba4f7' 'P' 'pixeljam'   'studios'
