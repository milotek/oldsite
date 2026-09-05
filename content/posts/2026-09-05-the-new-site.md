---
title: the new site
date: 2026-09-05
summary: Why the old one had to go, and what this one is made of.
---

My old site was a Carrd export. It was fine in 2024 and it aged like milk, so here's the replacement.

The whole thing is one Python script with no dependencies. Content lives in two TOML files and a folder
of Markdown. Adding a project means adding a block to `projects.toml`, adding a post means dropping an
`.md` in `content/posts/`, and neither of those makes me open a HTML file. That was the actual
requirement. I'll happily write a generator once if it means I never hand-edit markup again.

The layout is a line diagram. Each section is a line, each project is a stop on it, and the thing at the
top of the page is both the map and the navigation. I'm in London, those diagrams are everywhere, and
the shape happens to fit a list of projects that split into a few threads.

Colours are Catppuccin Mocha with `#ffbdbd` over the top, which is the accent my desktop already runs, so
the site and the machine that made it match. Type is Source Sans 3 and MesloLGS, subset locally down to
about 100 KB for the pair. No JavaScript at all. It's static files sat on GitHub Pages.

One rule I gave myself: if a project here has no link, that's because the repo is private, and I've said
so on the card rather than quietly linking nothing. Same with the screenshots. They're all real, and the
`habits` one is a live grab of the thing running on my wall, empty boxes and all.
