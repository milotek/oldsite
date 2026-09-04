+++
title   = "habits"
group   = "systems"
year    = "2026"
role    = "solo"
tagline = "A habit tracker that draws itself as a GitHub contribution grid."
stack   = ["Kotlin", "SQLite", "Nix"]
order   = 11
slate   = "kotlin + kiosk"
[[links]]
label = "source"
url   = "https://github.com/milotek/habits"
+++

Small Kotlin service that renders habits as a GitHub-style activity grid, meant for a screen bolted to a wall rather than a phone.

It ships a `module.nix` and a `package.nix`, so it drops straight into the flake with the rest of my services instead of being one more thing installed by hand.
