+++
title = "uses"
heading = "What I use"
slug  = "uses"
lead  = "The setup. Most of it is declared in one flake."
+++

## Machines

Desktop, a mini PC, a VPS and a work mac. All four are hosts in [nixeljam](https://github.com/milotek/nixeljam), so a new box is a folder and a line in `flake.nix`.

## Desktop

NixOS with Hyprland, waybar, tofi and swaync. Stylix pushes one base16 scheme into everything, which is why my terminal, editor and this website are all the same shade of pink.

Ghostty for a terminal, zsh with starship, and zoxide, fzf, eza and direnv for the boring parts. Neovim through nvf. lazygit, because I'm not typing `git rebase --interactive` again.

## Writing code

Python first for anything that runs as a service, with uv for packages inside a Nix devshell. Flask for web. Postgres unless the app already shipped SQLite.

Godot and Unity for games. Blender when something needs to be a shape.

## Everything else

Obsidian for notes, in a repo the flake clones. Caddy in front of the self-hosted things, Tailscale for anything administrative, sops for anything that grants access.

Procreate on an iPad Pro with an Apple Pencil for the drawings.

Fonts: MesloLGS Nerd Font, Source Sans 3, Montserrat. Colours: Catppuccin Mocha with `#ffbdbd` swapped in for the accent.
