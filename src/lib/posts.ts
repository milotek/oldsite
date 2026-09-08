import { getCollection, type CollectionEntry } from 'astro:content';

// Drafts show in dev and in preview builds made with PUBLISH_DRAFTS=1, nowhere else.
const showDrafts = import.meta.env.DEV || import.meta.env.PUBLISH_DRAFTS === '1';

export async function getPosts(): Promise<CollectionEntry<'blog'>[]> {
  const posts = await getCollection('blog', (p) => showDrafts || !p.data.draft);
  return posts.sort((a, b) => b.data.published.getTime() - a.data.published.getTime());
}
