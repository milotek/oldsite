+++
title   = "The new site"
date    = "2026-09-05"
summary = "Why the old carrd is gone, what replaced it, and how the whole thing is a folder of text files."
+++

My old site was a carrd export from 2024 and it had started to embarrass me. Four screenshots of an app I never shipped, a CV that still said "student", and an art gallery where one of the captions was flat out wrong. So it's gone.

This one is a folder of text files and a Python script. `build.py` reads `content/`, walks over some TOML and Markdown, and writes plain HTML. Standard library only, no node, no framework, nothing that needs a lockfile. Adding a project is one `.md` file with a header on top, and I never have to open the generator to do it.

That last bit is the whole point, honestly. Every personal site I've built before died because updating it meant remembering how it worked. If the cost of adding something is "write a paragraph in a text editor", I might actually keep it current. My blog posts already live as Markdown in my Obsidian vault, so they drop straight in.

The front page is a select screen. Everything I've made is on one list, and on a wide screen the pane on the right fills in as you move down it. Arrow keys work. Turn JavaScript off and you get the same list with everything still on it, just longer.

Colours are Catppuccin Mocha with `#ffbdbd` pulled out of my Stylix theme, so the site matches my terminal, which matches my editor. Fonts are subset and served from here. There are no third party requests on any page, which took no effort and I'd rather it stayed that way.

One thing worth saying plainly: I didn't type most of this. I wrote a brief, handed it to a coding agent along with my GitHub, my old site and my file server, and had ten of them build a version each. This is the one I kept. Every fact on the site came out of something real (a README, my CV, the old carrd), and where nothing could be verified the page says so rather than making something up.

Anyway. It works, it's fast, and I can add to it without dreading it.
