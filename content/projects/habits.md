---
title: habits
slug: habits
label: Project
weight: 90
year: 2026
role: Author
status: Early
summary: A habit tracker that renders as a GitHub-style activity grid, for a wall-mounted kiosk.
stack: [Kotlin, Nix, SQLite]
links:
  - label: GitHub
    url: https://github.com/milotek/habits
---

A habit tracker for a screen bolted to a wall. It draws the same green-square grid GitHub uses for contributions, because that grid works: you don't read it, you glance at it and instantly know whether you've been slacking.

Kotlin, with a Nix package and module so the kiosk host just enables it and it's there.

Very early. It renders and it stores things, which is most of what a habit tracker has to do.
