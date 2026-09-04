#!/usr/bin/env bash
# Draws the 88x31 buttons listed in content/buttons.toml.
# Antialiasing is off and the sizes are hand-picked: Meslo's lowercase m
# collapses into a solid block below 11pt, so line 1 is 11 and line 2 is 10.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=assets/img/buttons
mkdir -p "$OUT"

FONT=$(command ls /nix/store/*nerd-fonts-meslo-lg*/share/fonts/truetype/NerdFonts/MesloLG/MesloLGSNerdFontMono-Bold.ttf | head -1)
BG='#181825'; FG='#ffbdbd'; DARK='#11111b'; DIM='#7f849c'

# name, block text, line 1 (max 9 chars), line 2 (max 10 chars)
button () {
  magick -size 88x31 xc:"$BG" \
    -fill "$FG" -draw "rectangle 0,0 17,30" \
    -font "$FONT" +antialias \
    -fill "$DARK" -pointsize 13 -gravity northwest -annotate +1+9  "$2" \
    -fill "$FG"   -pointsize 11 -gravity northwest -annotate +21+6 "$3" \
    -fill "$DIM"  -pointsize 10 -gravity northwest -annotate +21+17 "$4" \
    -fill none -stroke "$FG" -strokewidth 1 -draw "rectangle 0.5,0.5 87.5,30.5" \
    "$OUT/$1.png"
}

# name, line 1 (max 12 chars), line 2 (max 13 chars)
plain () {
  magick -size 88x31 xc:"$BG" \
    -font "$FONT" +antialias \
    -fill "$FG"  -pointsize 11 -gravity north -annotate +0+5  "$2" \
    -fill "$DIM" -pointsize 10 -gravity north -annotate +0+18 "$3" \
    -fill none -stroke "$FG" -strokewidth 1 -draw "rectangle 0.5,0.5 87.5,30.5" \
    "$OUT/$1.png"
}

button milotek    "MT" "milo tek" "furfag.lol"
button pixeljam   "PJ" "PIXELJAM" "STUDIOS"
button trashdump  "TD" "files"    "tek.rip"
button punchdrunk "PD" "punch"    "drunk.gg"
plain  nixos      "NixOS"      "one flake"
plain  catppuccin "catppuccin" "mocha"
plain  godot      "GODOT"      "engine"
plain  nojs       "no js"      "required"

echo "wrote $(command ls "$OUT" | wc -l) buttons to $OUT"
