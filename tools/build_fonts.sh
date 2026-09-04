#!/usr/bin/env bash
# Subset the desktop fonts out of the Nix store into assets/fonts as woff2.
# Run inside `nix-shell` so pyftsubset and brotli are on the path.
set -euo pipefail

out="$(dirname "$0")/../assets/fonts"
mkdir -p "$out"

ss="$(nix-build --no-out-link '<nixpkgs>' -A source-sans)/share/fonts/opentype"
ms="$(nix-build --no-out-link '<nixpkgs>' -A montserrat)/share/fonts/otf"
me="$(nix-build --no-out-link '<nixpkgs>' -A nerd-fonts.meslo-lg)/share/fonts/truetype/NerdFonts/MesloLG"

unicodes='U+0020-007E,U+00A0-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2010-2027,U+2030-203A,U+2044,U+2074,U+20AC,U+2122,U+2190-2199,U+2212,U+2215,U+2713,U+2717,U+2764,U+FEFF,U+FFFD'

sub() {
  pyftsubset "$1" --unicodes="$unicodes" --flavor=woff2 --layout-features='*' --output-file="$out/$2"
}

sub "$ss/SourceSans3-Regular.otf" source_sans_3_regular.woff2
sub "$ss/SourceSans3-It.otf" source_sans_3_italic.woff2
sub "$ss/SourceSans3-Semibold.otf" source_sans_3_semibold.woff2
sub "$ss/SourceSans3-Bold.otf" source_sans_3_bold.woff2
sub "$ms/Montserrat-Bold.otf" montserrat_bold.woff2
sub "$ms/Montserrat-SemiBold.otf" montserrat_semibold.woff2
sub "$me/MesloLGSNerdFontMono-Regular.ttf" meslo_lgs_nf_mono_regular.woff2
sub "$me/MesloLGSNerdFontMono-Bold.ttf" meslo_lgs_nf_mono_bold.woff2
sub "$me/MesloLGSNerdFontMono-Italic.ttf" meslo_lgs_nf_mono_italic.woff2
