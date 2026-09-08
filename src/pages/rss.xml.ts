import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getPosts } from '../lib/posts';
import { site } from '../config';
import { url } from '../lib/url';

export async function GET(context: APIContext) {
  const posts = await getPosts();
  return rss({
    title: `${site.handle} blog`,
    description: 'Writing by Milo Tekchandani.',
    // Astro.site is the bare origin; the feed has to point at the subpath.
    site: new URL(url(''), context.site),
    trailingSlash: true,
    items: posts.map((p) => ({
      title: p.data.title,
      pubDate: p.data.published,
      description: p.data.summary,
      link: url(`blog/${p.id}/`),
    })),
  });
}
