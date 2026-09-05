---
title: nixeljam
slug: nixeljam
label: Project
weight: 30
featured: 3
year: 2026 - now
role: Author
status: Active
summary: My whole machine as code. About 1,600 commits of NixOS and home-manager modules, all rebuildable from one flake.
stack: [Nix, Shell, GLSL, Python]
cover: projects/nixeljam-1.webp
links:
  - label: GitHub
    url: https://github.com/milotek/nixeljam
gallery:
  - src: projects/nixeljam-1.webp
    caption: Desktop, Hyprland, a couple of terminals.
  - src: projects/nixeljam-2.webp
    caption: Neovim, configured through nvf.
  - src: projects/nixeljam-3.webp
    caption: Another workspace, launcher open.
  - src: projects/nixeljam-4.webp
    caption: The server host's dashboard.
---

Every machine I own is declared here: desktop, laptop, VPS, the lot. One flake, one rebuild, and the box comes back exactly as it was.

The rule I hold myself to is that if it can't be declared and rebuilt from the flake, it doesn't get installed. Configured-by-clicking state is the thing that bites you, because it's invisible right up until the disk dies.

It's split into modules that a stranger could enable, with the personal detail pushed out into host config. Nobody else is going to enable them. Doing it anyway is what stops the whole thing calcifying around one laptop.

Started June 2026. Around 1,600 commits so far, which tells you something about me.
