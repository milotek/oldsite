---
title: lakeback
blurb: Matchmaking and server infrastructure for 2v2 Counter-Strike 2 on de_lake.
status: in-progress
year: '2026'
tech: [Kotlin, Ktor, PostgreSQL, Terraform, GKE, Agones, Docker]
links:
  - { label: Source, href: 'https://github.com/milotek/lakeback' }
featured: true
order: 10
---

Valve removed de_lake from CS2. I did not take it well.

lakeback is a third-party matchmaking service for 2v2 wingman on the map, built the way I would want to build it at work: a Kotlin backend and the whole platform underneath it, declared in one repo.

- **Backend.** Ktor services for the queue, the matchmaker, Elo ratings, a ready-check store and a match state machine. Steam OpenID for sign-in. MatchZy webhooks feed results back in.
- **Servers.** Agones fleets on GKE run a custom CS2 image with MetaMod, CounterStrikeSharp and MatchZy. The image handles Agones readiness and health itself and leases a game server login token from a pool.
- **Infrastructure.** Terraform for GCP: a control plane module (GKE, Cloud SQL, Memorystore, buckets, DNS, IAM, Secret Manager) and a per-region module, so a new region is one more block.
- **Checks.** Unit tests for Elo, the matchmaker, the state machine and the webhook parser, plus one integration test that runs a whole match from queue to result.

The backend and infrastructure are done. The bot, the updater and the website are stubs, so nothing is live yet.
