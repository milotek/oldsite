+++
title = "nixeljam"
lane = "systems"
when = "2026"
sort = "2026-09"
tags = ["nix", "nixos", "hyprland", "sops"]
repo = "https://github.com/milotek/nixeljam"
blurb = "My NixOS setup. Five hosts, one flake, one theme, and about thirty self-hosted services."
+++
Every machine I own is declared in here: desktop, mini PC, a VPS, a WSL install and a work Mac. One flake,
one theme, `nixos-rebuild` and it's the same everywhere.

It started as a fork of anotherhadi's nixy and has drifted a long way since. Most of the drift lives in
`server-modules/`: Caddy, copyparty, Navidrome, Gitea, AdGuard Home, Home Assistant, Pelican for game
servers, and a pile of smaller things.

Secrets go through sops. Everything else stays plaintext, because encrypting a hostname buys you nothing and
costs you a config you can read.

The colours on this website come out of `themes/pixeljam.nix` in that repo, which is the same file that
paints my terminal.
