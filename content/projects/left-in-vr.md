---
title: Left 4 Dead 2 in VR
slug: left-in-vr
label: Fork
weight: 120
year: 2025
role: Contributor
status: Archived
summary: Picked up a dead L4D2 VR fork, merged the unmerged PRs, fixed PSVR2 rendering and added analogue movement.
stack: [C++, OpenVR, Source engine]
links:
  - label: GitHub
    url: https://github.com/milotek/left-in-vr
---

Someone built 6DoF VR support for Left 4 Dead 2, then vanished. There was a queue of open pull requests nobody was going to merge.

So I forked it, pulled them in, and added the things I needed for my hardware project: MSAA, analogue stick movement, and a fix for the distorted rendering on PSVR2.

Source engine C++ from 2009 with a VR runtime bolted to the side of it. Exactly as pleasant as that sounds.
