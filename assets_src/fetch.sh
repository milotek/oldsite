#!/usr/bin/env bash
# One-off asset gather. Sources are recorded here so the vendored files stay
# traceable. Screenshots and drawings that only exist on the old Carrd export
# were copied out of a clone of github.com/milotek/milotekold by hand; the four
# app GIFs in there turned out to be the same placeholder image four times, so
# they are not used.
set -u
OUT=assets_src/raw
mkdir -p "$OUT"
get() { # get <name> <url>
  [ -s "$OUT/$1" ] && { echo "have $1"; return; }
  curl -sL --max-time 90 -o "$OUT/$1" "$2" && echo "got  $1 $(stat -c%s "$OUT/$1")" || echo "FAIL $1"
}

RAW=https://raw.githubusercontent.com
get nixeljam1.png  "$RAW/milotek/nixeljam/main/.github/assets/screenshots/1.png"
get nixeljam2.png  "$RAW/milotek/nixeljam/main/.github/assets/screenshots/2.png"
get nixeljam3.png  "$RAW/milotek/nixeljam/main/.github/assets/screenshots/3.png"

get neosource_cover.png "$RAW/Pixeljam-Studios/neosource/main/Images/cover.png"
get neosource_bsp.jpg   "$RAW/Pixeljam-Studios/neosource/main/Images/bsp.jpg"
get neosource_csurf.jpg "$RAW/Pixeljam-Studios/neosource/main/Images/csurf.jpg"
get neosource_trick.jpg "$RAW/Pixeljam-Studios/neosource/main/Images/tricksurf.jpg"
get neosource_timer.jpg "$RAW/Pixeljam-Studios/neosource/main/Images/timer.jpg"
get neosource_map.jpg   "$RAW/Pixeljam-Studios/neosource/main/Images/mapping.jpg"

get airaccel.png "$RAW/Pixeljam-Studios/airaccel/main/_branding/github_banner.png"
get roxor.png    "$RAW/Pixeljam-Studios/ROXOR/main/roxor.png"

get makersbnb.png "https://files.catbox.moe/eiew9b.png"
get firestarter.png "https://files.catbox.moe/u53jex.png"

UA=https://github.com/user-attachments/assets
get shaders_hero.png "$UA/49467921-7366-4880-8841-9a2265d7769d"
get shaders_a.png    "$UA/244f0a2a-7027-4bdb-8a17-590ae8d48b3b"
get shaders_b.png    "$UA/d1a364a3-351c-47d8-ad33-758aa985a7a1"
get shaders_c.png    "$UA/5a33e4b7-6aac-493f-bd26-88dc9217ad99"
get shaders_d.png    "$UA/20c59e66-e885-4e09-92c5-1403067e9a98"
get roripper_temp.png "$UA/992cf74c-cd37-4604-93a7-8fb93491a239"

get simfiles_yt.jpg "https://img.youtube.com/vi/GO9Xfo2zVvQ/maxresdefault.jpg"
get shaders_yt.jpg  "https://img.youtube.com/vi/EzzUaDSsb3Q/maxresdefault.jpg"

get cv.pdf "https://github.com/milotek/milotek/raw/main/CV.pdf"
