---
title: The old site was a Carrd export
slug: building-this-site
date: 2026-09-04
summary: Why this one exists, what it's made of, and the one decision that did all the work.
tags: [site, meta]
---

My old site was a Carrd page I exported to static HTML in 2024 and then never
touched. It listed a pet feeder, a study app and some C# coursework, and by this
year roughly none of that was the most interesting thing I'd done.

So this. Static HTML out of a Python script, no dependencies, no framework, no
build tooling I'd have to migrate off in two years. Content is TOML and Markdown
in a `content/` folder. If I want to add a project I add a `[[project]]` block
and drop a screenshot next to it. That was the whole requirement, honestly:
adding a thing should not involve opening a template.

The layout is an engineering drawing. Sheet frame, ruler down the top edge,
sheet numbers in the nav, and a proper title block in the corner with the fields
a real drawing carries. Projects are plates with part numbers. It's a
conceit, but it earns its keep, because a drawing sheet is already a format for
putting technical work in front of someone in a fixed order with the metadata
attached.

One accent colour, `#ffbdbd`, pulled out of the base16 scheme my desktop runs
on. Everything else is Catppuccin Mocha. Fonts are the two my terminal and
editor use, subset and served from here.

Last thing, since I'd want to know: I had ten of these built in parallel by
agents off one brief, looked at all ten, and kept this one. Every line of it got
read before it went up. The alternative was another two years of the Carrd
export, and I think we can all agree on how that was going.
