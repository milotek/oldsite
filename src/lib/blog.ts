import { marked } from 'marked'

/**
 * Posts are Markdown files in `src/blog`, named `YYYY-MM-DD-slug.md`.
 *
 * The date and slug come from the filename rather than the frontmatter, so a
 * post cannot end up with two different dates depending on where you look,
 * and the directory sorts chronologically in any file listing.
 *
 * Files whose name starts with `draft-` are excluded from the bundle entirely
 * by the glob, so a draft is not shipped and then hidden - it is never built.
 */

export interface Post {
  slug: string
  date: string
  title: string
  description?: string
  tags: string[]
  /** Optional cover, used as the bleed behind the row in the post list. */
  image?: string
  html: string
}

const files = import.meta.glob<string>(['../blog/*.md', '!../blog/draft-*.md'], {
  eager: true,
  query: '?raw',
  import: 'default',
})

const FILENAME = /\/(\d{4}-\d{2}-\d{2})-(.+)\.md$/

/**
 * A deliberately small frontmatter reader: `key: value` pairs and
 * `[a, b, c]` lists, which is all any post here needs. Bringing in a YAML
 * parser to read four scalars would be the larger of the two mistakes.
 */
function parseFrontmatter(source: string): [Record<string, string | string[]>, string] {
  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/)
  if (!match) return [{}, source]

  const data: Record<string, string | string[]> = {}
  for (const line of match[1].split(/\r?\n/)) {
    const pair = line.match(/^([A-Za-z][\w-]*)\s*:\s*(.*)$/)
    if (!pair) continue

    const key = pair[1]
    const raw = pair[2].trim()

    if (raw.startsWith('[') && raw.endsWith(']')) {
      data[key] = raw
        .slice(1, -1)
        .split(',')
        .map((item) => item.trim().replace(/^['"]|['"]$/g, ''))
        .filter(Boolean)
    } else {
      data[key] = raw.replace(/^['"]|['"]$/g, '')
    }
  }

  return [data, source.slice(match[0].length)]
}

function toPost(path: string, source: string): Post | null {
  const name = path.match(FILENAME)
  if (!name) return null

  const [data, body] = parseFrontmatter(source)
  const tags = data.tags
  const title = data.title

  return {
    slug: name[2],
    date: name[1],
    title: typeof title === 'string' && title ? title : name[2].replace(/-/g, ' '),
    description: typeof data.description === 'string' ? data.description : undefined,
    tags: Array.isArray(tags) ? tags : [],
    image: typeof data.image === 'string' ? data.image : undefined,
    html: marked.parse(body, { async: false }),
  }
}

export const posts: Post[] = Object.entries(files)
  .map(([path, source]) => toPost(path, source))
  .filter((post): post is Post => post !== null)
  .sort((a, b) => b.date.localeCompare(a.date))

export function getPost(slug: string): Post | undefined {
  return posts.find((post) => post.slug === slug)
}
