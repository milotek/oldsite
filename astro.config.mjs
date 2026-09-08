// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// The site deploys under a subpath that is not decided yet, so both halves of
// the public URL come from the environment and default to the bare domain.
const site = process.env.SITE_URL || 'https://milotek.dev';
const base = process.env.SITE_BASE || '/';

export default defineConfig({
  site,
  base,
  trailingSlash: 'always',
  integrations: [sitemap()],
});
