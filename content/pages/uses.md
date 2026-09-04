---
title: Uses
tab: uses
stamp: the kit
description: The software and hardware Milo Tekchandani actually uses.
---
Everything here is declared in [nixeljam](https://github.com/milotek/nixeljam), so if it isn't in the flake I don't really use it.[^1]

**Desktop.** NixOS on a desktop with a dedicated Nvidia card, Hyprland on top, Stylix pushing one base16 scheme into everything. The scheme is Catppuccin Mocha with the accent swapped for `#ffbdbd`. Same as this site.

**Terminal.** Ghostty, Zellij, zsh. Neovim configured through nvf. MesloLGS Nerd Font at 12pt. Rosé Pine cursor, because the default one is ugly.

**Apps.** Chrome (yes, I know), Obsidian for notes and these blog posts, Spotify, Thunar when a GUI file manager is genuinely faster.

**Making things.** Godot, Blender, Roblox Studio via Proton wizardry. An iPad Pro and Procreate for anything drawn.

**Servers.** A minipc at home running copyparty (the [file server](https://files.tek.rip)), Navidrome and Home Assistant. A little ARM VPS with Caddy out front. Tailscale between all of it, and no public SSH anywhere.

**Other machines.** A work Mac, and a WSL host that exists mostly so the flake can say it supports WSL.

[^1]: hosts/ in the repo lists pc, minipc, vps, work-mac and wsl. that's the whole fleet.
