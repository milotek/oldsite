+++
title = "fastgains"
roll = "apps"
order = 2
year = "2024 - 2025"
kind = "Mobile app"
status = "on ice"
blurb = "A calorie tracker built to be closed again in ten seconds."
stack = ["Swift", "React Native", "Supabase", "Postgres"]
+++

Calorie tracking, minus the ceremony. Log a food, see the numbers, put the phone down.

Every tracker I tried wanted an account, a subscription and forty seconds of my attention per meal, which is exactly how you get people to stop logging by week two. So the whole design brief was time-to-log.

Swift and SwiftUI first, then rewritten in React Native so it ran on Android too. Self-hosted Supabase on Docker behind it, Postgres for the data, a nutrition API for the food database.

Shelved when I started at Google. It works, it's just not finished.
