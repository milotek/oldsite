#!/usr/bin/env bash
# Subset the three theme fonts out of the Nix store into assets/fonts as woff2.
# Run after bumping the font packages in the flake; the output is committed so
# GitHub Pages serves plain files.
set -euo pipefail
cd "$(dirname "$0")/.."

store() { nix build --no-link --print-out-paths "nixpkgs#$1"; }

MESLO="$(store nerd-fonts.meslo-lg)/share/fonts/truetype/NerdFonts/MesloLG"
SANS="$(store source-sans)/share/fonts/variable"
SERIF="$(store montserrat)/share/fonts/woff2"

LATIN='U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
# Every nerd-font glyph the pages use. Anything not listed here renders as tofu.
ICONS='U+E5FF,U+E613,U+E722,U+E73C,U+E755,U+E7B2,U+E7BA,U+E7EE,U+E81B,U+E843,U+EA84,U+EB06,U+F004,U+F017,U+F019,U+F03E,U+F040,U+F08E,U+F09B,U+F0AD,U+F0E0,U+F0E1,U+F0F4,U+F11B,U+F120,U+F121,U+F135,U+F16D,U+F179,U+F17B,U+F17C,U+F1B0,U+F1B2,U+F1B6,U+F1C1,U+F1FC,U+F1FF,U+F313,U+F408,U+F4A4,U+F465,U+F02D,U+F0C1,U+F0E7,U+F1C5,U+F2B6,U+E795,U+E6A1,U+E60B'

subset() { # src dst unicodes [extra pyftsubset args]
  local src=$1 dst=$2 unicodes=$3; shift 3
  pyftsubset "$src" --unicodes="$unicodes" --flavor=woff2 --layout-features='*' \
    --no-hinting --desubroutinize --output-file="$dst" "$@"
  echo "$(du -h "$dst" | cut -f1) $dst"
}

subset "$MESLO/MesloLGSNerdFontMono-Regular.ttf" assets/fonts/meslo-nf-mono.woff2 "$LATIN,$ICONS"
subset "$MESLO/MesloLGSNerdFontMono-Bold.ttf"    assets/fonts/meslo-nf-mono-bold.woff2 "$LATIN"
subset "$SANS/SourceSans3VF-Upright.otf" assets/fonts/source-sans-3.woff2 "$LATIN"
subset "$SANS/SourceSans3VF-Italic.otf"  assets/fonts/source-sans-3-italic.woff2 "$LATIN"
subset "$SERIF/Montserrat[wght].woff2"   assets/fonts/montserrat.woff2 "$LATIN"
