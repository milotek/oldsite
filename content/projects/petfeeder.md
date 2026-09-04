---
title: AutoPet Feeder
kicker: hardware · delivered 2024
status: done
featured: true
order: 4
tags: [raspberry pi, javascript, 3d printing, oak]
links:
  - label: source (forked from petfeedd)
    url: https://github.com/milotek/petfeeder
  - label: design document, 56 pages (pdf)
    url: https://github.com/milotek/milotek/raw/main/Product%20Design%20NEA%20Edited.pdf
---
A fully automated pet feeder built to my neighbours' spec, which made the requirements meetings very short. The client is a black labrador.

Raspberry Pi driving a servo, touchscreen on the front, USB-C for power. ABS 3D-printed shell with an oak lid because it lives in a kitchen and had to look like it belonged there. The software started as [rebeccathedev's petfeedd](https://github.com/rebeccathedev/petfeedd) and got bent to fit the hardware.[^1]

![The finished feeder: a white shell with a clear window for kibble and a solid oak lid](img/projects/petfeeder_finished.webp "finished, oak lid") ![A Raspberry Pi with a touchscreen attached, showing the desktop](img/projects/petfeeder_pi.webp "the brain") ![A black labrador chewing a stick on the grass](img/projects/petfeeder_client.webp "the client")

[^1]: product design a level. the pdf has the client interviews and the cardboard prototypes.
