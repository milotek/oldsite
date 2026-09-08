---
title: nixeljam
blurb: The NixOS flake that runs my desktop, a self-hosting mini PC and a VPS.
status: live
year: 2026 to now
tech: [Nix, NixOS, home-manager, Hyprland, sops-nix, Tailscale]
links:
  - { label: Source, href: 'https://github.com/milotek/nixeljam' }
featured: true
order: 20
---

Every machine I own is a host in this flake. If it cannot be declared and rebuilt from here, it does not get installed.

- **pc**: the desktop. Hyprland, the pixeljam theme (the colours on this site) and far too many keybinds.
- **minipc**: the box under the TV. Copyparty for files, Navidrome for music, Home Assistant, AdGuard Home.
- **vps**: an aarch64 box with a real public IP. Caddy in front, Tailscale for admin, fail2ban, disko for the disk layout.

Secrets go through sops-nix. Admin access is tailnet-only, so no host exposes SSH to the internet. It started from anotherhadi's nixy and has been rebuilt piece by piece since.
