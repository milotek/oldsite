+++
title = "lakeback"
lane = "systems"
when = "2026"
sort = "2026-07"
tags = ["kotlin", "agones", "cs2", "game servers"]
blurb = "Third-party matchmaking for CS2 wingman, on de_lake. Because de_lake deserves better."
+++
Wingman matchmaking for one map. It's my favourite map and Valve's queue barely admits it exists, so I'm
building the queue instead.

A Kotlin service in front of dedicated CS2 servers, scheduled with Agones, with MatchZy and
CounterStrikeSharp doing the in-game half. It stands on joedwards32's CS2 container image and the
MetaMod/CounterStrikeSharp stack, all credited in the repo.

Repo is private for now. lakeback.com is registered and parked.
