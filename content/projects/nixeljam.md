---
title: nixeljam
kicker: nixos · 2024 → now
status: live
featured: true
order: 1
tags: [nix, hyprland, home-manager]
links:
  - label: source
    url: https://github.com/milotek/nixeljam
  - label: the theme file
    url: https://github.com/milotek/nixeljam/blob/main/themes/pixeljam.nix
---
My NixOS flake, and where most of my commits go. Five hosts (pc, minipc, vps, work-mac, wsl), Hyprland, one Stylix theme file that colours everything, secrets in sops.[^1]

It started as a fork of [nixy](https://github.com/anotherhadi/nixy) in March 2024 and has drifted about 1,500 commits of my own since. Right now I'm rebuilding it on upstream's v6 base, one module at a time, without switching a single host until all three evaluate clean.

![The Hyprland desktop: two terminals over a foggy forest wallpaper, a clock reading 13:40](img/projects/nixeljam_desktop.webp "the desktop this site is copying") ![Neovim and a file tree in Zellij panes](img/projects/nixeljam_editor.webp "nvf + zellij") ![Several TUI panes: system monitor, file manager, music](img/projects/nixeljam_tui.webp "the tui side")

[^1]: this site's palette, fonts and accent all come from themes/pixeljam.nix.
