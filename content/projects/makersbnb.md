---
title: MakersBNB
slug: makersbnb
label: Team project
weight: 70
year: 2025
role: Developer, team of six
status: Shipped
summary: An Airbnb clone in Flask, built test-first by a team of six over a week.
stack: [Python, Flask, PostgreSQL, Playwright, pytest]
cover: projects/makersbnb.webp
links:
  - label: GitHub
    url: https://github.com/milotek/makersbnb
gallery:
  - src: projects/makersbnb.webp
    caption: Listings view.
---

List a space, request a booking, approve or reject it, manage your reservations. The usual shape.

Flask and Postgres, with Basecoat UI on the front. Tests in pytest with Playwright driving a real browser for the feature specs, which is the only way you catch the bugs that live between the routes and the templates.

Six people, one week, 118 commits. The interesting part of a project this size isn't the code, it's keeping six branches from turning into a merge conflict museum.
