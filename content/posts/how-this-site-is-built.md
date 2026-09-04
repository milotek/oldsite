+++
title = "How this site is built"
date = "2026-09-05"
summary = "A contact sheet, a Python script, and no JavaScript."
+++

My old site was a Carrd export from 2024 with a phone number on the front page and links to a GitHub username I don't use any more. It had to go.

This one is laid out as a contact sheet, the thing photographers print when they want to see a whole roll at once and mark the good ones. It suits a portfolio, honestly. You get everything on one sheet, at one size, and the pink grease pencil says which ones I'd actually print. Nothing hides behind a hero section.

Underneath it's a Python script of about 660 lines with no dependencies. Content lives in `content/` as TOML and Markdown, output is plain HTML in the repo root, GitHub Pages serves the files. I wanted adding a project to mean writing one file, and now it does. My notes are already Markdown in an Obsidian vault, so this is the same shape as everything else I write.

No JavaScript on any page. No fonts or analytics fetched from someone else's server. Two self-hosted font files, one stylesheet, and images I've actually looked at.

Claude did most of the typing. I read every diff, which is the deal I've made with myself about agents: code nobody has read isn't finished work, however well it runs. It went through my GitHub and my file server, pulled out screenshots I'd forgotten existed, and got the palette from my NixOS theme rather than guessing. I moved things around after.

The [colophon](../../colophon/) has the boring specifics.
