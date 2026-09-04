# milotek.dev, the zine

My personal site, laid out as a twelve page A5 zine.
Plain HTML and one stylesheet, no JavaScript, generated from a folder of content files.

## Editing content

Everything you'd want to change lives in `content/` and `posts/`:

- `content/site.toml`: name, tagline, issue, links, CV URL, the site URL used by the feed.
- `content/projects.toml`: one `[[project]]` per entry; `size` decides whether it gets a full feature, a short, or a classified.
- `content/art.toml`: the gallery. Images are `assets/img/art/<file>.webp` plus a `<file>_thumb.webp`.
- `content/buttons.toml`: the 88x31 wall on the back page. Files go in `assets/buttons/`.
- `content/*.md`: the prose for the hello, work, now, uses and colophon pages.
- `posts/YYYY-MM-DD-slug.md`: blog posts, with `title`, `date` and `summary` in the front matter.

Then rebuild:

```sh
python3 tools/build.py
```

That writes `index.html`, `blog/`, `feed.xml` and `404.html`.
Page numbers and the contents list on the cover are worked out from the pages that exist, so adding or removing one renumbers everything.
The script only uses the Python standard library (3.11 or newer, for `tomllib`).

## Theme

Colours are Catppuccin Mocha with the accent set to `#ffbdbd`, taken from `themes/pixeljam.nix` in [nixeljam](https://github.com/milotek/nixeljam).
The fonts are the same ones the desktop uses, subsetted to WOFF2 in `assets/fonts/`.

## Deploying

GitHub Pages serves `main` from the repo root, under a subpath, so every link in the generated HTML is relative.
`.nojekyll` stops Pages from running Jekyll over it.
Commit the build output alongside the sources.
