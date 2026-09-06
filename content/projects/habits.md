---
title: habits
summary: A habit tracker that renders as a GitHub-style activity grid, for a wall-mounted kiosk. Kotlin, Ktor and SQLite in two files.
year: 2026
featured: true
order: 2
tags: [Kotlin, Ktor, SQLite, Nix]
repo: https://github.com/milotek/habits
image: static/img/projects/habits.webp
image_alt: Eight habit rows of grey cells, one coloured icon per row, on a dark background
links:
  - label: Live board
    url: https://habits.tek.rip
---
One Ktor server, one SQLite file. Each habit is a row of 365 cells, coloured by how far through that day's target you got, so it reads like a contributions graph on the wall.

Ticking happens from a phone: tap the icon and it posts to `/tick/<slug>`. Tapping past the target wraps back to zero, because a wall display has no room for an undo button. The kiosk view reloads itself every minute to pick up ticks made elsewhere.

It ships as a Nix package with a NixOS module, so running it is one line in nixeljam.
