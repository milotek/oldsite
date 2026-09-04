+++
title = "The new site"
date = "2026-09-04"
summary = "Why the carrd had to go, and what replaced it."
+++
My old site was a carrd export from 2024 and it showed. Four sections, a slideshow, and my phone number sat
there in plain text for anyone who scrolled.

So, new one. The only rule I set was that the work comes first and everything else is decoration.

It's one Python script with no dependencies. Markdown with TOML frontmatter goes in `content/`, plain HTML
comes out into the repo root, and GitHub Pages serves those files as they are. Adding a project is dropping
a file in `content/entries/`, which matters to me because my notes already live as Markdown in a vault repo
and I'd like to stop copying things between formats.

The front page is a git graph. Everything I've built sits on one of four lanes and the rail shows which
branch was open when. It's CSS borders and border-radius, no canvas, no SVG, no JavaScript anywhere on the
site. Whether the fiddling was worth it is a matter of opinion, and the opinion is mine.

Honest bit, since it's the sort of thing I'd want to know about someone else's site: I wrote the brief and
an AI agent built it. Then I read the diff, which is the only rule I properly care about. Code nobody has
read isn't finished work, however well it runs.

It's all at [github.com/milotek/wst15](https://github.com/milotek/wst15) if you want to nick the generator.
