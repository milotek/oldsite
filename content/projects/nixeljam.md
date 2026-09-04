+++
title = "nixeljam"
roll = "work"
order = 2
year = "2025 - now"
kind = "NixOS configuration"
status = "live"
pick = true
url = "https://github.com/milotek/nixeljam"
url_label = "github.com/milotek/nixeljam"
blurb = "My whole machine, declared in one flake."
stack = ["Nix", "Hyprland", "Stylix", "sops"]
frames = [
  { img = "nixeljam1", caption = "the desktop" },
  { img = "nixeljam2", caption = "neovim + spotify" },
  { img = "nixeljam3", caption = "browser + files" },
]
+++

Every machine I own is described in this flake: packages, dotfiles, secrets, theming, server modules, the lot. Rebuild and it comes back exactly as it was.

The rule I hold myself to is that nothing gets installed unless it can be declared here. Mutable state that only exists on one box is the failure mode I actually care about, because it's invisible right up until the disk dies.

Theming runs through Stylix off a base16 scheme, so one palette change repaints the terminal, the editor, the bar and the browser at once. The accent on this website is the same pink.

Started as a fork of anotherhadi's Nixy and has drifted a long way since.
