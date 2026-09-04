+++
title   = "CollisionSounds"
group   = "games"
year    = "2025"
role    = "solo"
tagline = "Roblox parts that sound like what they're made of when they hit things."
stack   = ["Lua", "Roblox"]
order   = 35
slate   = "roblox lua"
[[links]]
label = "source"
url   = "https://github.com/milotek/CollisionSounds"
+++

Drop-in module. It reads a part's material, picks a sound to match, and scales the volume off impact speed, with separate soft and hard hits. Source engine sounds by default, per-object overrides if you want a bouncy ball to go boing.

Roblox physics does not make this easy and the maths is still rough. It works well enough to be worth having.
