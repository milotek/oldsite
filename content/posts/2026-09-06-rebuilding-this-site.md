---
title: Rebuilding this site
summary: The old site was a carrd export. This one is Markdown, YAML and one Python script.
---
The old site was a carrd export, still linking to a GitHub username I'd stopped using. It had the Lockyn screenshots, a pile of drawings and a CV, and that was about it. This is the replacement.

Everything is content in a folder. Projects are Markdown files with a bit of YAML front matter for the tags, links and images. Posts are the same, straight out of my Obsidian vault. One Python script (Jinja2 for the templates, python-markdown for the bodies, and that's the whole dependency list) renders it to plain HTML and an Atom feed.

No JavaScript anywhere. Every link is relative, so the same output works on GitHub Pages under a subpath and straight off a local folder. Colours are Catppuccin Mocha with #ffbdbd as the one accent, which is what my desktop runs too.

Honest bit: the first version was generated with Claude Code from a brief I wrote, in one unattended run. The [colophon](/colophon/) has the details. If something reads wrong, tell me.
