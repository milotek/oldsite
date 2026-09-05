---
title: I rebuilt this site
slug: rebuilding-this-site
date: 2026-09-05
summary: The old one was a Carrd export from sixth form. This one is markdown files and a Python script.
tags: [meta]
---

My old site was a Carrd export. It did the job for about two years, in the sense that it was a URL I could put on a CV, but it was written before I had a job and it showed. Four screenshots of an app I couldn't release, some drawings, and a phone number.

So this is the replacement.

The whole thing is markdown files in `content/`. One file per project, one per post, one per drawing, each with a bit of YAML at the top for the title, the stack, the screenshots. A Python script reads them and writes plain HTML. No framework, no node_modules, nothing to migrate when whatever I picked goes out of fashion in eighteen months.

That constraint is the point, honestly. If adding a project means opening a template file, I won't do it. If it means dropping a `.md` next to fifteen others, I might. I keep my notes in Obsidian as markdown already, so the format is one I'm going to keep writing in whether or not this site exists.

The script has no dependencies. It parses enough YAML for front matter and enough markdown for the prose I actually write, and it emits every URL relative, so the site works under any path you drop it at. About 900 lines. You can read all of it if you're bored.

Colours are Catppuccin Mocha with `#ffbdbd` doing the accent work, which is the same palette I've had on my desktop for a while. Fonts are Source Sans 3 and JetBrains Mono, both self-hosted, so nothing phones home to Google when you load a page.

The buttons at the bottom are real 88x31s. Take one if you link me.
