---
title: Uses
path: uses
eyebrow: Uses
updated: September 2026
summary: The tools, editor and desktop Milo Tekchandani actually uses.
lede: Everything here is declared in one flake, so this list is accurate by construction rather than by me remembering to update it.
---

## Desktop

NixOS, with Hyprland for the window manager. Waybar on top, tofi for launching things, swaync for notifications, hyprlock and hypridle guarding the screen.

Theming goes through Stylix off a single base16 scheme, so the terminal, the editor and the notification popups all agree with each other without me touching six config files.

## Terminal

Ghostty, running zsh with starship, zoxide, fzf, eza and direnv. Zellij for multiplexing. lazygit for anything git that isn't a one-liner.

## Editor

Neovim, configured through nvf so the whole setup is Nix rather than a pile of Lua I'd have to port to the next machine.

## Everything else

Obsidian for notes, all plain markdown in a git repo. Godot and Blender when I'm making something. Helium for browsing. Spotify, which is the one thing I pay for rather than self-host, because storing every album I like costs more than the subscription does.

## Servers

A VPS with a real public IP owns the front door. Everything administrative sits on the tailnet, and no host has a public SSH port. My files live on [copyparty](https://files.tek.rip), which is anonymously readable if you want a look.

## Fonts

MesloLGS Nerd Font for anything monospaced. Source Sans 3 for interfaces. This site uses Source Sans 3 too, with JetBrains Mono standing in for Meslo, which does not exist as a web font.
