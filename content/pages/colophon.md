---
title: Colophon
tab: colophon
stamp: how it's made
description: How Milo Tekchandani's website is built and hosted.
---
**Paper.** Catppuccin Mocha, accent `#ffbdbd`, lifted from the theme file in my NixOS flake. The margin rule is the accent at half opacity. The ruled lines are `surface0`.

**Type.** Source Sans 3 for the body, Montserrat for headings, MesloLGS Nerd Font Mono for the margin notes. They're the fonts my desktop uses, subsetted to Latin with fonttools and served from here.[^1]

**Build.** One Python script (`tools/build.py`) with python-markdown, PyYAML and Pillow, all pinned by `shell.nix`. Every project, page and post is a Markdown file with YAML frontmatter. Footnotes become margin notes. A paragraph of images becomes a row of taped-in figures.

**Hosting.** GitHub Pages, static files straight from the repo, no build on their side. Every URL is relative so it survives living under a subpath.

**JavaScript.** None. **Analytics.** None. **Cookies.** None.

**Buttons.** The 88x31s in the footer are real ones from the [dabamos archive](https://cyber.dabamos.de/88x31/), plus one I drew in ImageMagick. Room for more.

**Source.** [github.com/milotek/wst5](https://github.com/milotek/wst5). Steal the build script if you like, it's about 250 lines.

[^1]: ~250 kb of woff2 for nine faces. cheaper than one hero image.
