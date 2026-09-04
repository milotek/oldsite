---
title: Uses
slug: uses
description: The software and hardware Milo Tekchandani actually uses.
updated: 2026-09-04
---

Three machines, one flake. If it can't be rebuilt from that flake it doesn't get
installed, which sounds dogmatic until the day a disk dies and you get the whole
thing back in twenty minutes.

## Desktop

- **NixOS**, everything declared in [nixeljam](https://github.com/milotek/nixeljam)
- **Hyprland**, with waybar, tofi, swaync and hyprlock
- **Neovim** for code, **Ghostty** for the terminal, **Zellij** on top of it
- **Chrome**, reluctantly, because of work
- **Stylix** paints every app from one base16 scheme so nothing clashes
- MesloLGS Nerd Font and Source Sans 3, which are also the two faces on this site

## Servers

- A mini PC at home runs **copyparty** (the [file server](https://files.tek.rip)),
  **Navidrome**, **slskd** and **Home Assistant**
- A cheap VPS owns the public ingress and runs **Caddy**. The front door lives on
  a box with a real IP, not behind someone else's tunnel
- **Tailscale** is the only admin path. No host has a public SSH port
- **sops** for anything that grants access, plaintext for everything else

## Writing and drawing

- **Obsidian**, in a repo the flake clones in
- **Procreate** on an iPad Pro with an Apple Pencil for anything on the art page
- Python for services, Bash for one-offs, and a hard line between the two
