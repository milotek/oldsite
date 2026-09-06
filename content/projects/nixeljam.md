---
title: nixeljam
summary: One Nix flake for my desktop, a self-hosting mini PC, a VPS and a work Mac. Hyprland, base16 theming and a stack of server modules.
year: 2026
featured: true
order: 1
tags: [Nix, NixOS, Hyprland]
repo: https://github.com/milotek/nixeljam
image: static/img/projects/nixeljam.webp
image_alt: Hyprland desktop with two terminals and a clock over a mountain wallpaper
images:
  - src: static/img/projects/nixeljam-2.webp
    alt: File manager and terminal windows on the same desktop
    caption: Thunar, a terminal and cbonsai.
  - src: static/img/projects/nixeljam-3.webp
    alt: Neovim and a Spotify TUI side by side
    caption: Neovim and spotatui.
---
My NixOS configuration, built on top of [anotherhadi's Nixy](https://github.com/anotherhadi/nixy). One repo declares every machine I own: `pc`, `minipc`, `vps`, `work-mac` and a WSL host, each with its own flake and sops-encrypted secrets.

The desktop side is Hyprland with waybar, tofi, hyprlock and swaync, all themed from one base16 scheme through Stylix. Neovim is configured through nvf, the terminal is Ghostty, and zellij, starship and zsh do the rest.

The mini PC runs the self-hosted stuff as NixOS modules: Caddy in front, copyparty for the [file server](https://files.tek.rip), Gitea, AdGuard Home, Glance, fail2ban, the *arr stack, a game relay and the habits board below. Tailscale handles admin access.
