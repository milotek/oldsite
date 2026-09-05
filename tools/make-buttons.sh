#!/usr/bin/env bash
# Regenerates the 88x31 buttons. Rendering is deliberately aliased: the classic
# button look falls apart the moment the text gets antialiased at this size.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=assets/buttons
FONT="MesloLGS-Nerd-Font-Bold"
ACC="#ffbdbd"; BG="#181825"; DIM="#6c7086"; TXT="#cdd6f4"

btn() { # name  bg  border  line1  colour1  line2  colour2
  magick -size 88x31 "xc:$2" \
    -fill none -stroke "$3" -strokewidth 1 -draw "rectangle 0,0 87,30" \
    -font "$FONT" -pointsize 9 -antialias +antialias -stroke none \
    -fill "$5" -gravity north -annotate +0+6 "$4" \
    -fill "$7" -gravity north -annotate +0+16 "$6" \
    "$OUT/$1.png"
}

btn milo-tek       "$BG" "$ACC" "milo tek"  "$ACC" "furfag.lol" "$DIM"
btn pixeljam       "$BG" "#45475a" "PIXELJAM" "$TXT" "studios"  "$ACC"
btn trashdump      "$BG" "#45475a" "trashdump" "$ACC" "files.tek.rip" "$DIM"
btn yours-here     "#11111b" "#313244" "your button" "$DIM" "here :3" "#45475a"

# Variant with the moose on the left, for anyone who prefers a graphic button.
magick -size 88x31 "xc:$BG" \
  \( assets/img/site/avatar.webp -resize 29x29! \) -gravity west -geometry +1+0 -composite \
  -font "$FONT" -pointsize 9 -antialias +antialias \
  -fill "$ACC" -gravity northeast -annotate +6+6 "milo" \
  -fill "$DIM" -gravity northeast -annotate +6+16 "tek" \
  -fill none -stroke "$ACC" -strokewidth 1 -draw "rectangle 0,0 87,30" \
  "$OUT/milo-tek-moose.png"

echo "wrote:"; ls -l "$OUT"
