+++
title = "RoRipper"
lane = "apps"
when = "2026"
sort = "2026-07-20"
tags = ["reverse engineering", "desktop", "sqlite", "in progress"]
blurb = "Pulling Roblox's local asset cache apart, so you can see and hear what your own client already downloaded."
+++
Roblox has spent years making user uploaded assets private: animations first, then audio, then meshes, images
and models. The stated reason is exploits and platform safety. The effect is that creators can't reuse their
own work, and anyone making a montage ends up screen recording sound effects.

The client still downloads all of it onto your machine. It lands in a SQLite database with three tables, in
a custom binary format, plus a temp folder full of extensionless files that are usually just `.ogg` in a hat.

RoRipper is meant to read that cache, work out what each file actually is, and show it to you with a preview
as new assets arrive. Right now it's a Svelte frontend and a pile of test scripts, so treat this as a
statement of intent. Credit to EmK530's BloxDump for the parts of the format I won't have to work out
myself.

Repo is private for now.
