# wst

My personal website, drawn to look like my desktop.

Plain HTML, one CSS file, one JS file, no build step.
Open `index.html` in a browser, or serve the directory with anything that serves files.

## Where the numbers come from

The colours, rounding, gaps, border size, blur and wallpaper in `style.css` are copied from `themes/pixeljam.nix` in [nixeljam](https://github.com/milotek/nixeljam).
If the desktop theme changes, `:root` in `style.css` is the second place to change.

## Content

- Projects, games and art are hand-written in `index.html`.
- `assets/cv.pdf` is a copy of the CV in the [milotek](https://github.com/milotek/milotek) profile repo. Replace it when that one changes.
- The "git log" window on the home workspace reads GitHub's public events feed at page load. Nothing else talks to the network.

## Deploying

GitHub Pages serves the `main` branch from the repo root. `.nojekyll` stops Pages from running Jekyll over it.
