+++
title = "Rebuilding this site"
date = "2026-09-04"
summary = "The old site buried everything. The new one is a search box with a website attached."
tags = ["meta"]
+++

The old site was a carrd export, and it had one real problem: everything I'd made sat three taps down.
Name, then menu, then section, then finally a project.
Fine for a business card, useless for a portfolio.

So this one is built round a search box.
Projects, posts, drawings and pages are all just records with a title, a date and some tags, so I put them in one list and let you filter it.
Type `lua` and you get a modchart pack, a Roblox sound module and a GTA script.
Hit `/` from anywhere and the box takes focus.

Under it, everything lives in `content/`.
Projects are TOML blocks, posts are Markdown files with a TOML header, which is already how my Obsidian vault looks.
One Python script reads that and writes the site.
I never have to open a code file to add a project, which was the entire point.

The honest bit: I didn't hand-write this one.
I wrote a brief, pointed a coding agent at my GitHub, my old site and my file server, and let it build.
It dug out 15 drawings I'd forgotten were online.
The projects and the screenshots are real and you can go and check them.

The **now** page is seeded from what I've been pushing lately, so assume it's a week behind.
Three slots on the button wall are empty on purpose.
Send me one.
