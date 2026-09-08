---
title: CollisionSounds
blurb: Material-aware impact sounds for Roblox, borrowed from the Source engine.
status: shipped
year: '2025'
tech: [Luau, Roblox]
links:
  - { label: Source, href: 'https://github.com/milotek/CollisionSounds' }
  - { label: Release, href: 'https://github.com/milotek/CollisionSounds/releases' }
hobby: true
order: 120
---

Things that hit each other should sound like what they are made of. This module plays a sound per material, scales the volume by impact speed, picks a soft or hard variant, and can spawn particles. Each instance deletes itself once its part goes to sleep, so it costs nothing while nothing is moving.
