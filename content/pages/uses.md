+++
title = "uses"
slug = "uses"
summary = "The setup. Short version, because nobody needs the long one."
+++

## desktop

| | |
|---|---|
| os | NixOS, unstable channel |
| wm | Hyprland |
| terminal | Ghostty, with Zellij on top |
| shell | zsh |
| theme | catppuccin mocha, accent `#ffbdbd` |
| config | all of it lives in [nixeljam](https://github.com/milotek/nixeljam) |

New and niche is fine by me. A single maintainer with no bus factor is the thing that actually strands a config, rather than a project being young.

## code

Python first for anything that runs as a service, with uv resolving packages inside a Nix devshell. Flask over the alternatives, because it does what it's told and leaves the shape of the app to the app. Postgres unless the thing already shipped with SQLite.

Bash is for work that's mine and finite. The moment something is recurring or handed off, it's outgrown a shell script.

## boxes

Public ingress lives on a VPS with a real IP, behind Caddy. Admin interfaces are tailnet only, and no host has a public SSH port. Anything granting access goes through sops. Hostnames and ports stay in plain text, because encrypting those buys nothing and makes the config unreadable.

I self-host by default and pay only where the constraint is physical. There's a [file server](https://files.tek.rip) if you want to poke around.

## drawing

Procreate on an iPad Pro with an Apple Pencil. That's the whole pipeline.
