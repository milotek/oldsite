---
title: AutoPet Feeder
slug: petfeeder
order: 3
group: Selected
featured: true
year: 2023
role: Design and build
status: Delivered
blurb: An automated cat feeder, designed and built to a real client's spec. The client was my neighbours. They still use it.
tags:
  - Raspberry Pi
  - CAD
  - 3D printing
  - Embedded
links:
  - Design document | https://github.com/milotek/petfeeder/blob/main/Product%20Design%20NEA%20Edited.pdf
images:
  - /assets/img/projects/petfeeder-built.jpg | The finished unit, ABS shell with an oak lid
  - /assets/img/projects/petfeeder-prototype.jpg | Cardboard prototype, iteration one
  - /assets/img/projects/petfeeder-electronics.jpg | Raspberry Pi, touchscreen and servo
  - /assets/img/projects/petfeeder-design.jpg | Working out the hopper geometry
---

My neighbours travel and their cat does not. So I interviewed them, wrote a spec, and spent a term of Product Design turning it into a box that drops the right amount of food at the right time.

The shell is 3D printed ABS with an oak top, sized around the hopper rather than the other way round, which took three cardboard prototypes to get right. Inside there's a Raspberry Pi, a servo and a touchscreen, powered over USB-C so they can plug it into anything.

The scheduling daemon is [petfeedd](https://github.com/rebeccathedev/petfeedd), which I deployed rather than wrote. The design, the mechanism, the enclosure and the client work were mine, and the full document covering all of it is linked above.
