# milotek.dev, notebook edition

My personal website, laid out as a field notebook.
Plain HTML and one stylesheet, no JavaScript, content in Markdown with YAML frontmatter.

Live at <https://furfag.lol/wst5/>.

## Editing

| What | Where |
| --- | --- |
| A project | `content/projects/<slug>.md` (`featured: true` for a full card, otherwise it goes in the shortlist) |
| A blog post | `posts/YYYY-MM-DD-<slug>.md` |
| Now, uses, colophon | `content/pages/<name>.md` (the `tab:` key puts it on the side) |
| Sketches | `content/art.toml` plus a file in `assets/img/art/` |
| 88x31 buttons | `content/buttons.toml` plus a gif in `assets/img/buttons/` |
| Name, socials, tab order | `content/site.toml` |

Footnotes (`[^1]`) render as margin notes.
A paragraph containing only images renders as a row of taped-in figures; the image title becomes the caption.
Image paths are relative to `assets/`.

## Building

```sh
nix-shell --run 'python3 tools/build.py'
```

Output is written next to the sources (`index.html`, `blog/`, `feed.xml`, and so on) and committed, so GitHub Pages only ever serves static files.

## Fonts

`assets/fonts/` holds Latin subsets of Source Sans 3, Montserrat and MesloLGS Nerd Font Mono, the same packages my NixOS flake installs.
Regenerate with `tools/build_fonts.sh` inside the same shell.
