import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/projects' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      blurb: z.string(),
      status: z.enum(['live', 'in-progress', 'shipped', 'shelved', 'archived']),
      year: z.string(),
      tech: z.array(z.string()),
      links: z.array(z.object({ label: z.string(), href: z.string() })).default([]),
      featured: z.boolean().default(false),
      hobby: z.boolean().default(false),
      order: z.number().default(100),
      cover: image().optional(),
      images: z.array(z.object({ src: image(), alt: z.string() })).default([]),
    }),
});

// Populated by scripts/sync-vault.ts; empty until the vault has been synced.
const blog = defineCollection({
  loader: glob({
    pattern: '*/index.md',
    base: './src/content/blog',
    generateId: ({ entry }) => entry.split('/')[0]!,
  }),
  schema: z.object({
    title: z.string(),
    published: z.coerce.date(),
    summary: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { projects, blog };
