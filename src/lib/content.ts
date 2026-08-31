/**
 * Typed access to whatever scripts/build-vault.ts last emitted.
 *
 * docs.json is generated and gitignored, so this module is the only place
 * that knows its shape. Everything downstream goes through these helpers.
 */
import indexJson from '../content/index.json'

export type DocKind = 'post' | 'note'

export interface Heading {
  depth: number
  id: string
  text: string
}

/** Metadata only. The rendered body is fetched separately by loadDocHtml. */
export interface Doc {
  slug: string
  kind: DocKind
  title: string
  description?: string
  date?: string
  updated?: string
  tags: string[]
  headings: Heading[]
  outbound: string[]
  backlinks: string[]
  wordCount: number
  vaultPath: string
}

export const docs = indexJson as Doc[]

/**
 * One chunk per document, resolved on demand. Vite turns each glob entry into
 * its own lazily-fetched module, so visiting a note downloads that note only.
 */
const bodies = import.meta.glob<{ default: { html: string } }>('../content/docs/*.json')

export async function loadDocHtml(slug: string): Promise<string> {
  const load = bodies[`../content/docs/${slug}.json`]
  if (!load) return ''
  return (await load()).default.html
}

const bySlug = new Map(docs.map((doc) => [doc.slug, doc]))

export const posts = docs
  .filter((doc) => doc.kind === 'post')
  .sort((a, b) => (b.date ?? '').localeCompare(a.date ?? ''))

export const notes = docs
  .filter((doc) => doc.kind === 'note')
  .sort((a, b) => a.title.localeCompare(b.title))

export function getDoc(slug: string): Doc | undefined {
  return bySlug.get(slug)
}

export function hrefFor(doc: Doc): string {
  return doc.kind === 'post' ? `/blog/${doc.slug}` : `/notes/${doc.slug}`
}

export function formatDate(iso?: string): string {
  if (!iso) return ''
  const date = new Date(`${iso}T00:00:00Z`)
  if (Number.isNaN(date.getTime())) return iso
  return date.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  })
}

export function allTags(): { tag: string; count: number }[] {
  const counts = new Map<string, number>()
  for (const doc of docs) {
    for (const tag of doc.tags) counts.set(tag, (counts.get(tag) ?? 0) + 1)
  }
  return [...counts.entries()]
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag))
}
