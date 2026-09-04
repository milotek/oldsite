#!/usr/bin/env python3
"""Draw the 88x31 buttons described in content/buttons.toml.

Needs ImageMagick and a PCF bitmap font. Bitmap fonts matter here: at 88x31
anything anti-aliased turns to mush, so we render 5x8 pixels-on-a-grid and
never scale. Output is committed, so this only needs running when the TOML
changes.
"""
import gzip, pathlib, shutil, subprocess, sys, tempfile, tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/buttons"
BORDER = "#45475a"

# fc-match won't give us a specific pixel size, so look for the classic
# misc-fixed 5x8 by name and fall back to whatever the system calls "Fixed".
FONT_CANDIDATES = ["5x8.pcf.gz", "5x8-ISO8859-1.pcf.gz"]


def find_font(tmp: pathlib.Path) -> str:
    roots = ["/usr/share/fonts", "/run/current-system/sw/share/X11/fonts", "/nix/store"]
    for name in FONT_CANDIDATES:
        for root in roots:
            base = pathlib.Path(root)
            if not base.is_dir():
                continue
            for hit in base.glob(f"**/misc/{name}"):
                dest = tmp / "5x8.pcf"
                with gzip.open(hit, "rb") as f, open(dest, "wb") as o:
                    shutil.copyfileobj(f, o)
                return str(dest)
    sys.exit("no misc-fixed 5x8 PCF font found; install xorg.fontmiscmisc")


def draw(font: str, b: dict) -> None:
    dest = OUT / f"{b['file']}.png"
    cmd = [
        "magick", "-size", "88x31", f"xc:{b['bg']}",
        "-font", font, "-pointsize", "8", "+antialias",
        # left badge block
        "-fill", b["badge_bg"], "-draw", "rectangle 0,0 23,30",
        "-fill", b["badge_fg"], "-gravity", "northwest",
        "-annotate", "+4+11", b["badge"],
        # right hand text, two lines on the 8px grid
        "-fill", b["fg"], "-gravity", "northwest",
        "-annotate", "+27+9", b["line1"],
        "-annotate", "+27+20", b["line2"],
        # 1px frame last so nothing paints over it. Four filled rectangles
        # rather than a stroked outline: a stroke lands half on each pixel and
        # leaves grey corners at this size.
        "-fill", BORDER, "-stroke", "none",
        "-draw", "rectangle 0,0 87,0",
        "-draw", "rectangle 0,30 87,30",
        "-draw", "rectangle 0,0 0,30",
        "-draw", "rectangle 87,0 87,30",
        str(dest),
    ]
    subprocess.run(cmd, check=True)
    print("wrote", dest.relative_to(ROOT))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = tomllib.loads((ROOT / "content/buttons.toml").read_text())
    with tempfile.TemporaryDirectory() as td:
        font = find_font(pathlib.Path(td))
        for b in data.get("mine", []):
            draw(font, b)


if __name__ == "__main__":
    main()
