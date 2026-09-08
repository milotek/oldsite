---
title: habits
blurb: A habit tracker that draws a GitHub-style activity grid, for a wall-mounted kiosk.
status: live
year: '2026'
tech: [Kotlin, Ktor, SQLite, Nix]
links:
  - { label: Live, href: 'https://habits.tek.rip' }
  - { label: Source, href: 'https://github.com/milotek/habits' }
order: 30
---

One Ktor file, one SQLite file, one Nix module. It runs on the mini PC and renders on a touchscreen.

Tapping a habit ticks it for today. Tapping again keeps counting and wraps back to zero, because on a touchscreen a mistap is inevitable and an undo button is one more thing to miss.

The NixOS module means enabling it on a host is a single line.
