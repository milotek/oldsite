---
title: This site is a sticker sheet
date: 2026-09-04
summary: How the site got built, why every box on it peels, and what is actually under the hood.
---

So, new site. The old one was a carrd export with an "under construction" gif on it, and it had been under construction since 2024. Time.

Here's how this one happened, honestly. I wrote one brief (who I am, what I've built, the colours, no waffle) and handed it to 10 copies of Claude Code at once. Each copy got the same brief plus one seed idea, and had to go from an empty folder to a live GitHub Pages deploy without asking me anything. Then I picked my favourite. This is the one whose seed was "a sticker sheet".

I could've built it by hand. But I wanted to see 10 takes side by side, and I'd never have drawn 10 of them myself.

## Why stickers

Every box on this page is a die-cut sticker on a backing sheet. Hover one and the corner peels. That's the whole idea, and I think it earns its keep because it does 2 jobs at once: it's a grid of cards (a portfolio has to be one), and it has a bit of personality without a paragraph about "my journey".

The 88x31 buttons at the bottom are stickers too, obviously. They were the original stickers of the web.

## What it's actually made of

- One Python script, `tools/build.py`, standard library only. It reads TOML and Markdown and writes plain HTML.
- Projects, jobs, buttons, drawings and socials live in `content/*.toml`. Adding a project is about 6 lines and a rebuild. I don't want to touch HTML to add a thing.
- Posts are Markdown files in `posts/` with front matter, so they can come straight out of my Obsidian vault.
- One stylesheet. No JavaScript at all. The peel is a `clip-path` polygon that cuts the corner off the sticker on hover, plus a gradient triangle for the curled-over bit.
- Catppuccin Mocha with `#ffbdbd` as the only accent, lifted from the stylix theme in my NixOS flake. Same fonts as my desktop too (Montserrat and Source Sans 3), self-hosted.

The whole repo, fonts and pictures included, is under 2 MB and there's nothing to `npm install`. (That was the bit I cared about most, if you ask me.)

## Things I'd flag

The Markdown parser is about 60 lines and only knows headings, lists, links, code and emphasis. That's fine for a blog with 1 post. If it annoys me later I'll swap in python-markdown and not much else changes.

Also: a sticker sheet with nothing peeled off it looks unused. So one corner on the front page is already lifted. Go find it.
