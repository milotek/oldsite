+++
title = "EZcals"
lane = "apps"
when = "2025"
sort = "2025-01"
tags = ["swift", "react native", "supabase", "postgres"]
blurb = "Calorie tracker aimed at the ten seconds after you've eaten, rather than the ten minutes before."
+++
Log a meal in about ten seconds. That was the whole brief, because every tracker I'd used wanted portion
sizes and macro targets before it would let me record a sandwich.

Started in Swift and SwiftUI for iOS, then rewritten in React Native so it runs on Android, desktop and web
off one codebase. Behind it, a self-hosted Supabase in Docker with Postgres underneath.
