---
title: lakeback
kicker: cs2 · kotlin · 2026
status: wip
featured: true
order: 2
tags: [kotlin, counterstrikesharp, agones, docker]
links:
  - label: lakeback.com
    url: https://lakeback.com
  - label: source
    url: https://github.com/milotek/lakeback
---
Third-party matchmaking for CS2 wingman, on de_lake only. Because lake deserves better.[^1]

Kotlin backend, a Discord bot, a game server image with MetaMod, CounterStrikeSharp and MatchZy, an updater, and Agones to schedule matches. Everything in one Gradle build, deployed with compose. The queue is the bit that's still missing, which I appreciate is the whole product.

![Ink sketch of the house and dock on de_lake, captioned Bring Back Lake](img/projects/../art/bring_back_lake.webp "the drawing that started it, 2023")

[^1]: valve dropped it from the wingman pool. i'm not over it.
