---
title: How this notebook got built
date: 2026-09-04
summary: A rebuild of milotek.dev as a field notebook, done in one sitting by an AI agent I pointed at my GitHub. Here's what it did and what I'd change.
---
My old site was a Carrd export from 2024. Under construction gif, phone number in the header, a projects list that stopped at sixth form. It had to go.

## The honest bit

I didn't write this one by hand. I wrote a brief, pointed ten copies of Claude at it, and each got a different seed idea. This one drew "field notebook" and ran with it: ruled paper, tabs down the side, screenshots taped in at an angle, margin notes in the terminal font.[^1]

I'm comparing the ten and keeping the one I hate least. If you're reading this, it won.

## What it's made of

The whole site is Markdown files with YAML frontmatter, the same format Obsidian uses. A project looks like this:

```markdown
---
title: nixeljam
kicker: nixos · 2024 → now
status: live
featured: true
order: 1
tags: [nix, hyprland]
links:
  - label: source
    url: https://github.com/milotek/nixeljam
---
My NixOS flake. Five hosts, one theme file...

![the desktop](img/projects/nixeljam_desktop.webp "the desktop this site is copying")
```

A 250-line Python script turns that folder into HTML. Footnotes become margin notes, which is the part I'm most pleased with.[^2] A paragraph that's only images becomes a row of taped-in figures. Everything else is the python-markdown library doing what it already does.

No JavaScript, because nothing here needs it. No framework, because I don't want to migrate off it in two years.

## The theme

Colours come from `themes/pixeljam.nix` in my NixOS config: Catppuccin Mocha with `#ffbdbd` as the accent. The fonts are the ones on my desktop, pulled out of the Nix store, subsetted to Latin and served from here. The site looks like my terminal because it's built from the same file.

## Deploying under a subpath

GitHub Pages serves this from `/wst5/`, so every link is relative. The build script works out how many `../` each page needs. That's it. No base tag, no config option, nothing to forget.

## What I'd still change

The CV linked from the front page is the pre-Google one. Lockyn is still "unreleased", which it has been for two years now. And the Now page will rot unless I actually update it, which is a me problem, not a build problem.

If you want the build script, it's in [the repo](https://github.com/milotek/wst5). Take it.

[^1]: the seed was one sentence. "a reader should be able to name the metaphor in one glance."
[^2]: like this one. in obsidian it's just a footnote, so the posts still read fine in the vault.
