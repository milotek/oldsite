---
title: nixeljam
slug: nixeljam
order: 10
group: Software
year: 2026
role: Solo
status: Live
blurb: My whole computer as one flake. Four machines, one config, Hyprland and Stylix doing the theming so nothing drifts.
tags:
  - Nix
  - NixOS
  - Hyprland
links:
  - GitHub | https://github.com/milotek/nixeljam
---

A desktop, a mini PC, a VPS and a work Mac, all built from the same repo. Modules are split into what a machine can do and what this particular machine is, which is the split that stops a config calcifying around one box.

Theming runs through Stylix off a single base16 scheme, so the terminal, the bar, the editor and the lock screen agree without me maintaining five colour files. Secrets go through sops. Everything else stays plaintext, because encrypting a hostname buys nothing.

Started from [nixy](https://github.com/anotherhadi/nixy) and diverged a long way.
