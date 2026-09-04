# milotek.dev, the sticker sheet

My personal site.
Every element is a die-cut sticker on a backing sheet, and hovering one peels its corner.
Plain HTML and one stylesheet, no JavaScript, generated from a folder of content files.

## Editing content

Everything you'd want to change lives in `content/` and `posts/`:

- `content/site.toml`: name, role, tagline, socials, the site URL used by the feed.
- `content/work.toml`: one `[[job]]` per sticker in the work section.
- `content/projects.toml`: one `[[project]]` per sticker; `size` is `big`, `wide`, `normal` or `small`.
- `content/art.toml`: the drawings. Images go in `assets/img/art/`.
- `content/buttons.toml`: the 88x31 wall. Files go in `assets/buttons/`.
- `content/now.md`, `uses.md`, `colophon.md`: the three text stickers near the bottom.
- `posts/YYYY-MM-DD-slug.md`: blog posts, with `title`, `date` and `summary` in the front matter.

Then rebuild:

```sh
python3 tools/build.py
```

That writes `index.html`, `blog/`, `feed.xml` and `404.html`.
The script only uses the Python standard library (3.11 or newer, for `tomllib`).
Its Markdown is a small subset: headings, lists, quotes, fenced code, links, images, bold and italics.

## Theme

Catppuccin Mocha with the accent set to `#ffbdbd`, taken from `themes/pixeljam.nix` in [nixeljam](https://github.com/milotek/nixeljam).
Fonts are Montserrat and Source Sans 3, self-hosted as WOFF2 in `assets/fonts/`.

## Deploying

GitHub Pages serves `main` from the repo root under a subpath, so every link in the generated HTML is relative.
`.nojekyll` stops Pages from running Jekyll over it.
Commit the build output alongside the sources.
