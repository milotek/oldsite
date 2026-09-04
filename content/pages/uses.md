+++
title = "uses"
updated = "Updated September 2026"
summary = "The hardware, software and services Milo Tekchandani actually runs."
+++
None of this is a recommendation. It's just what's on the machines.

## desktop

NixOS with Hyprland, themed end to end by stylix off one base16 scheme. Accent is `#ffbdbd`, the rest is
roughly Catppuccin Mocha. Ghostty as the terminal, Zellij for multiplexing, Neovim via nvf, zsh with
starship, eza and zoxide.

MesloLGS Nerd Font for anything monospaced. Source Sans 3 for everything else.

## the boxes

- **pc** - desktop, Nvidia, games and anything heavy
- **minipc** - the one that actually matters. Files, music, DNS, home automation, game servers
- **vps** - the public ingress, because I'd rather own my own front door than rent a tunnel
- plus a WSL install and a work Mac, declared in the same flake

## services

Caddy in front. copyparty for files, Navidrome for music, Gitea, AdGuard Home, Home Assistant, Pelican for
game servers, Glance as the dashboard, and a few more I keep meaning to prune.

Anything public is public. Every admin panel is tailnet only, Tailscale is the only way in, and no host has
a public SSH port.

## making things

Godot and Unity for games, Roblox Studio when the project wants it. Blender for models. Procreate on an iPad
Pro with an Apple Pencil for drawing.

Obsidian for notes, in a git repo, because a vault that isn't in git is a vault you're going to lose.
