---
title: Legacy Console Shaders
slug: legacy-console-shaders
label: Project
weight: 60
year: 2026
role: Author
status: Released
summary: A shader pack that makes modern Minecraft look like the Xbox 360 edition. Built against a mod from 2013.
stack: [GLSL]
cover: projects/shaders-1.webp
links:
  - label: GitHub
    url: https://github.com/milotek/minecraft-legacy-console-shaders
  - label: Video
    url: https://youtu.be/EzzUaDSsb3Q
gallery:
  - src: projects/shaders-1.webp
    caption: A torch-lit mineshaft, which is where the fog earns its keep.
  - src: projects/shaders-2.webp
    caption: Plains at midday.
  - src: projects/shaders-3.webp
    caption: Distance fog over a build.
  - src: projects/shaders-4.webp
    caption: Lamps and water at night.
---

Minecraft Legacy Console Edition had a look. Warm lighting, heavy fog, that particular blue on the water. This is an attempt to get it back.

Tested on 1.6.4 with ShadersModCore, which is a mod from before OptiFine shipped shader support at all. It works fine on modern Iris and OptiFine too, but the reason it exists is that I play old versions.

It's GLSL and it's short. The trick was working out that most of the feeling comes from the fog curve and the sky gradient, not from anything clever.
