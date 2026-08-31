/**
 * Render every route to static HTML.
 *
 * Deliberately hand-written rather than pulled from a plugin: the established
 * option (vite-react-ssg) peers on react-router 6, which would have pinned the
 * whole app a major version back. This is the entire mechanism, and it is
 * short enough to read.
 */
import fs from 'node:fs/promises'
import path from 'node:path'
import { Feed } from 'feed'

const ROOT = path.resolve(import.meta.dirname, '..')
const CLIENT = path.join(ROOT, 'dist/client')
const SERVER = path.join(ROOT, 'dist/server/entry-server.js')

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

async function main() {
  const template = await fs.readFile(path.join(CLIENT, 'index.html'), 'utf8')
  // The route tree and page list come from the SSR bundle; site config is
  // read straight from source since tsx can import .ts directly.
  const { render, allPages } = await import(SERVER)
  const { site } = await import('../src/data/site.ts')

  const pages = allPages() as { path: string; title: string; description: string }[]
  let written = 0

  for (const page of pages) {
    const html = await render(page.path)
    const canonical = `${site.url}${page.path === '/' ? '' : page.path}`

    const head = [
      `<title>${escapeHtml(page.title)}</title>`,
      `<meta name="description" content="${escapeHtml(page.description)}" />`,
      `<link rel="canonical" href="${canonical}" />`,
      `<meta property="og:type" content="website" />`,
      `<meta property="og:title" content="${escapeHtml(page.title)}" />`,
      `<meta property="og:description" content="${escapeHtml(page.description)}" />`,
      `<meta property="og:url" content="${canonical}" />`,
      `<meta name="twitter:card" content="summary" />`,
    ].join('\n    ')

    const out = template.replace('<!--app-head-->', head).replace('<!--app-html-->', html)

    // '/404' becomes 404.html (what static hosts look for); everything else
    // becomes <route>/index.html so URLs need no extension.
    const target =
      page.path === '/404'
        ? path.join(CLIENT, '404.html')
        : path.join(CLIENT, page.path, 'index.html')

    await fs.mkdir(path.dirname(target), { recursive: true })
    await fs.writeFile(target, out)
    written++
  }

  console.log(`prerendered ${written} pages`)
  await writeFeeds()
}

async function writeFeeds() {
  // Reads the generated JSON straight from disk rather than importing
  // src/lib/content.ts: that module uses import.meta.glob, which only exists
  // after Vite transforms it, and this script runs in plain Node under tsx.
  const { site } = await import('../src/data/site.ts')
  const contentDir = path.join(ROOT, 'src/content')
  const index = JSON.parse(
    await fs.readFile(path.join(contentDir, 'index.json'), 'utf8'),
  ) as { slug: string; kind: string; title: string; description?: string; date?: string }[]

  const posts = index
    .filter((doc) => doc.kind === 'post')
    .sort((a, b) => (b.date ?? '').localeCompare(a.date ?? ''))

  const feed = new Feed({
    title: site.title,
    description: site.description,
    id: site.url,
    link: site.url,
    language: 'en',
    copyright: `${new Date().getFullYear()} ${site.name}`,
    feedLinks: {
      rss: `${site.url}/rss.xml`,
      atom: `${site.url}/atom.xml`,
      json: `${site.url}/feed.json`,
    },
    author: { name: site.name, email: site.email, link: site.url },
  })

  for (const post of posts) {
    const body = JSON.parse(
      await fs.readFile(path.join(contentDir, 'docs', `${post.slug}.json`), 'utf8'),
    ) as { html: string }

    feed.addItem({
      title: post.title,
      id: `${site.url}/blog/${post.slug}`,
      link: `${site.url}/blog/${post.slug}`,
      description: post.description,
      content: body.html,
      date: post.date ? new Date(`${post.date}T00:00:00Z`) : new Date(),
      author: [{ name: site.name, link: site.url }],
    })
  }

  await fs.writeFile(path.join(CLIENT, 'rss.xml'), feed.rss2())
  await fs.writeFile(path.join(CLIENT, 'atom.xml'), feed.atom1())
  await fs.writeFile(path.join(CLIENT, 'feed.json'), feed.json1())
  console.log(`wrote 3 feeds with ${posts.length} posts`)
}

main().catch((error) => {
  console.error(error)
  process.exit(1)
})
