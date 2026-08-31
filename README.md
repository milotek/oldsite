# milotek.dev

Personal site and portfolio.
React 19, Vite 8, react-router 8, TypeScript.
Prerendered to static HTML at build time, so there is no server at runtime.

## Running it

```bash
npm install
npm run dev          # http://localhost:5173
npm run build        # -> dist/client, fully static
npm run typecheck
```

The blog and notes are generated from a private Obsidian vault.
Without it the build still succeeds and simply publishes nothing, so you do not need the vault to work on the rest of the site.

To develop against the fixture vault, which exercises every case in the pipeline:

```bash
VAULT_PATH=./fixtures/vault npm run dev
```

## Publishing from the vault

The vault repo stays private.
A note is published only if its own frontmatter says so:

```yaml
---
publish: true
type: post          # or: note
title: Google Does Not Use Lua
description: One line, used for the feed and the card.
date: 2026-03-14
tags: [google, lua]
---
```

Allowlist, not denylist.
Nothing lacking `publish: true` is read into the output, so a note filed in the wrong folder cannot leak.
`type: post` renders into `/blog`, `type: note` into `/notes`.

Every build prints exactly what escaped.
Read it before deploying:

```
found 516 notes, 0 flagged publish: true
skipped 5 untitled notes (filename is just ".md")
held back 516 notes (no publish: true)
```

To wire the vault into CI, add an `ed25519` deploy key to the `ObsidianVault` repo and store the private half as the `VAULT_DEPLOY_KEY` secret here.
The workflow picks it up automatically and skips the vault entirely when it is absent.

## Layout

```
scripts/build-vault.ts    Obsidian vault -> site content
scripts/prerender.ts      renders every route to static HTML, writes feeds
src/data/                 projects, games, art, identity - hand-maintained
src/content/              generated, gitignored
src/routes.tsx            route tree and the list of URLs to prerender
fixtures/vault/           small vault covering every pipeline case
```

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds and publishes to GitHub Pages.
The custom domain is kept in `public/CNAME`, which Vite copies into the build output.

The previous hand-written version of this site is in the history at `57ee054`.
