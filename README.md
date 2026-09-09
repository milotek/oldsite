---

<p align="center">
    <img width="1080" height="720" src="/src/assets/art/thumbnail.jpg">
</p>

<h1 align="center">
    <a href="https://milotek.dev">milotek.dev</a>
</h1>

<p align="center">
    godawful """professional""" website
</p>

---



## Running it

```bash
npm install
cp .env.example .env    # fill in Last.fm if you want the listening card
npm run dev
npm run build
npm run check
```

`npm run dev` and `npm run build` both run `scripts/sync-vault.ts` first.
The build passes `--force` because the synced blog folder is regenerated every time and Astro's content cache would otherwise keep stale entries.

## Where things live

```
src/config.ts              identity, socials, splash lines, friends' buttons
src/content/projects/*.md  one file per project, frontmatter + write-up
src/data/art.ts            the art page
src/assets/                images, optimised at build time
scripts/sync-vault.ts      Obsidian vault -> src/content/blog (gitignored)
public/88x31.png           the button
```

## Blog

Posts come from `Personal/Blogs/` in the private ObsidianVault repo.
Clone it to `vault/` (gitignored) and the sync script picks it up.

A post is published when its frontmatter has a date:

```yaml
---
published: 2026-09-06
summary: One line for the index and the feed.
---
```

Anything without `published` is a draft and is left out of the build.
`PUBLISH_DRAFTS=1 npm run build` includes drafts, marked as such, for previewing.
The dev server always shows drafts.

Obsidian embeds (`![[file.png|300]]`), wikilinks and callouts are rewritten by the sync script.
Attachments are found anywhere in the vault by filename.

## Deploying under a subpath

The base path is not hardcoded anywhere.

```bash
SITE_URL=https://example.com SITE_BASE=/milo npm run build
```

Every internal link goes through `url()` in `src/lib/url.ts`, so nothing breaks when the path changes.
The GitHub Actions workflow reads `SITE_URL` and `SITE_BASE` from repository variables and `VAULT_TOKEN` from secrets.
