+++
title    = "nixeljam"
group    = "systems"
year     = "2026 - now"
role     = "solo"
tagline  = "My NixOS config. Every machine I own, declared once."
stack    = ["Nix", "NixOS", "home-manager", "Hyprland", "sops"]
thumb    = "img/proj/nixeljam-thumb.webp"
featured = true
order    = 10
[[links]]
label = "source"
url   = "https://github.com/milotek/nixeljam"
[[images]]
src = "img/proj/nixeljam-1.webp"
alt = "Hyprland desktop with a wallpaper, a clock widget and two terminals"
[[images]]
src = "img/proj/nixeljam-2.webp"
alt = "Neovim open next to a music player"
[[images]]
src = "img/proj/nixeljam-3.webp"
alt = "Browser and file manager tiled side by side"
[[images]]
src = "img/proj/nixeljam-4.webp"
alt = "Self-hosted server dashboard listing running services"
+++

Desktop and servers in one flake, split into `home`, `nixos`, `hosts`, `themes` and `server-modules`. Adding a machine is a folder and a line in `flake.nix`.

It started as a fork of [nixy](https://github.com/anotherhadi/nixy) and I've been pulling it apart since. The theming goes through Stylix and a base16 scheme, which is where the pink on this site comes from.

The rule I actually care about: if it can't be rebuilt from the flake, it doesn't get installed. Anything that grants access goes through sops. Everything else stays readable.
