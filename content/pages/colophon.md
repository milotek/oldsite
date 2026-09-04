+++
title = "Colophon"
subtitle = "How this thing is put together"
+++

## Build

One Python script, 660 lines, no dependencies outside the standard library. It reads TOML and Markdown out of `content/`, writes plain HTML into the repo root, and GitHub Pages serves the files. No framework, no bundler, no lockfile to rot.

Adding a project means dropping a `.md` file into `content/projects/` with a TOML header. Adding a note is the same in `content/posts/`. Adding an 88x31 is a file in `static/buttons/` and three lines of TOML. I never have to open the generator to add anything to the site, which was the point.

Markdown gets rendered by 75 lines of hand-written parser. It covers what I write and nothing else.

## Type and colour

Inter for prose, JetBrains Mono for everything structural, both self-hosted as variable woff2 subsets. Two files, 80 KB together, no font CDN.

Catppuccin Mocha, with `#ffbdbd` as the only accent. It's the same palette my desktop runs, via Stylix and a base16 scheme.

## Behaviour

No JavaScript, no analytics, no cookies, no fonts or scripts fetched from anyone else's server. Every page is one HTML file and one stylesheet.

The grease pencil rings are SVG with an `feTurbulence` displacement filter, so the wobble is generated rather than drawn.

## Credit

Screenshots and drawings are mine. The C# game shots, the app screenshots and the drawings were rescued off my old Carrd site.

Made with a lot of help from Claude, which I mention because pretending otherwise would be daft. The [note about that](../notes/how-this-site-is-built/) has the details.
