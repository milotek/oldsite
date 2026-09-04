+++
title = "my website is my desktop"
date = "2026-09-04"
summary = "Why the new site looks like a tiling window manager, and what is actually holding it up."
tags = ["meta", "nix", "web"]
+++

The old site was a carrd export. It had a slideshow, an "under construction" GIF I drew
myself, and a copyright notice that said 2025. It did the job for about a year and then it
just sat there getting older.

So: new one. Three rules going in. Projects first, because that is what people come for.
No waffle. And it has to look like something I would actually run.

# the metaphor

It is my desktop.

There is a bar across the top with workspaces on it, numbered, exactly like Hyprland.
Every section of the site is a workspace. Press 1 through 6 and you move between them
without touching the mouse. Each block of content sits in a window with a title bar and a
border, and when you hover one it takes the focus colour.

I went back and forth on whether that is too cute for a site that is meant to help me get
hired. I decided it isn't, for one reason: it is honest. I spend my day in a tiling WM
that I built out of a Nix flake, and the pink you are looking at is `base0D` from
`themes/pixeljam.nix`. Same colour, same rounding, same gaps. If I repaint my desktop
tomorrow I change one variable here and it follows.

A generic dark portfolio would have told you less about me and taken the same week.

# what is underneath

One Python script. About 500 lines, zero dependencies, no build tooling.

Content lives in `content/`. Projects are TOML tables. Posts are Markdown files with a
little TOML header. `python3 build.py` turns them into HTML, drops a feed out the other
end, and I commit the result. GitHub Pages serves flat files.

That is deliberate. I have watched enough personal sites die because the owner came back
after eight months, ran the install, and got a wall of peer dependency errors. Nothing
here can rot like that. The Python on this machine in 2030 will still run it.

Adding a project is adding six lines of TOML. Writing a post is dropping a file in a
folder. Neither one makes me open a code editor, which matters more than it sounds like
it should, because the friction is the reason the old site never got updated.

The next step is pointing the posts folder at my Obsidian vault so writing a post and
writing a note are the same action.

# the bit people leave out

An agent did the first pass. It read my GitHub, my file server and the old carrd export,
and it wrote the markup, the CSS and most of the copy.

I read the diff. All of it. That is the deal I have with these things and it is the only
part that actually matters, because code nobody has read is not finished work, however
well it runs. It got some project descriptions wrong and invented a bit of enthusiasm I do
not have, and I cut those.

# still broken

The `now` section will be out of date within a month, they always are. The button wall has
room in it and I want more real ones. The art page stops in 2024 and I should draw
something.

Anyway. It loads in under a second and it does not ask you about cookies. Good enough.
