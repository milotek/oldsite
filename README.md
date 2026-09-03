# milotek.dev

My personal website.
Plain HTML, one stylesheet, one small script, no build step.
Open `index.html` in a browser or serve the directory with anything that serves files.

## Theme

`theme.css` is generated, never edited.
Every colour, font, corner radius, gap and border width comes from `themes/pixeljam.nix` in [nixeljam](https://github.com/milotek/nixeljam), evaluated by Nix:

```sh
tools/theme_from_nix.py > theme.css
```

The fonts are the desktop's fonts, subsetted out of the same Nix packages into `assets/fonts`:

```sh
nix shell --impure --expr 'with import <nixpkgs> {}; python3.withPackages (p: [ p.fonttools p.brotli ])' --command tools/build_fonts.sh
```

Both outputs are committed so GitHub Pages only ever serves static files.

## Content

Projects, art and the front page are hand-written in their HTML files.
The CV and the pet feeder design document are linked from the [milotek](https://github.com/milotek/milotek) profile repo rather than copied, so there is one copy to keep current.
The contribution graph on the front page is the SVG that repo regenerates nightly.

## Deploying

GitHub Pages serves `main` from the repo root.
`.nojekyll` stops Pages from running Jekyll over it.
