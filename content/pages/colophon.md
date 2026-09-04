+++
title = "colophon"
heading = "How this is built"
slug  = "colophon"
lead  = "How this site is put together."
+++

## The build

Static HTML from `build.py`, one Python file, standard library only. `tomllib` reads the config and a small Markdown renderer handles the prose. No node, no framework, no build cache, nothing to migrate in two years.

Everything on the site is a file in `content/`. A project is a `.md` with a TOML header and a couple of image lines. A post is a `.md` with a title and a date. Drawings are rows in `art.toml`, buttons are rows in `buttons.toml`. I never open the generator to add anything.

## Type and colour

Montserrat for headings, Source Sans 3 for body, MesloLGS Nerd Font for the labels. All three are subset and served from this domain, about 150 KB in total, and there are no third-party requests on any page.

The palette is Catppuccin Mocha with `#ffbdbd` as the only accent, taken straight out of `themes/pixeljam.nix` in my flake.

## Weight

One stylesheet, one small script, and the script only drives the preview pane on the front page. Turn JavaScript off and the site still works, it just gets a bit more scrolling.

Hosted on GitHub Pages. There's an [RSS feed](../feed.xml) if you want one.

## Buttons

I've got a [button wall](../buttons/). Take mine, and send me yours.
