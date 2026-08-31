/**
 * Obsidian vault -> site content.
 *
 * Allowlist by design: a note ships only if its own frontmatter says
 * `publish: true`. A denylist would leak the first note dropped into the wrong
 * folder, and this vault holds daily journals, university work and coursework
 * drafts. The failure mode of a leak is permanent, so the filter fails closed.
 *
 * Emits src/content/docs.json plus the attachments those docs actually
 * reference. Nothing else in the vault is read into the output.
 */
import fs from 'node:fs/promises'
import { existsSync } from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import matter from 'gray-matter'
import GithubSlugger from 'github-slugger'
import { unified } from 'unified'
import remarkParse from 'remark-parse'
import remarkGfm from 'remark-gfm'
import remarkRehype from 'remark-rehype'
import rehypeSlug from 'rehype-slug'
import rehypeCallouts from 'rehype-callouts'
import rehypeShiki from '@shikijs/rehype'
import rehypeStringify from 'rehype-stringify'
import { visit } from 'unist-util-visit'
import type { Root as MdRoot, PhrasingContent, Image, Link, Text } from 'mdast'
import type { Root as HastRoot, Element, ElementContent } from 'hast'

/**
 * VAULT_PATH wins when set (CI always sets it). Otherwise try the places the
 * vault sits depending on whether this project is checked out on its own or
 * alongside a sibling vault clone, so `npm run vault` works either way.
 */
function resolveVault(): string {
  if (process.env.VAULT_PATH) return path.resolve(process.env.VAULT_PATH)
  const here = import.meta.dirname
  for (const candidate of ['../vault', '../../vault']) {
    const full = path.resolve(here, candidate)
    if (existsSync(full)) return full
  }
  return path.resolve(here, '../../vault')
}

const VAULT = resolveVault()
const OUT_DIR = path.resolve(import.meta.dirname, '../src/content')
const ASSET_OUT = path.resolve(import.meta.dirname, '../public/vault')
const ASSET_URL = '/vault'

/** Obsidian plugin state and VCS internals are never content. */
const SKIP_DIRS = new Set(['.obsidian', '.makemd', '.space', '.trash', '.git', 'node_modules'])
const MEDIA_EXT = new Set([
  '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.avif',
  '.mp4', '.webm', '.mp3', '.wav', '.ogg', '.pdf',
])

/** `[[target#heading|alias]]`, with a leading `!` for embeds. */
const WIKILINK = /(!?)\[\[([^\]|#]+?)(?:#([^\]|]+?))?(?:\|([^\]]+?))?\]\]/g

export type DocKind = 'post' | 'note'

export interface Heading {
  depth: number
  id: string
  text: string
}

export interface Doc {
  slug: string
  kind: DocKind
  title: string
  description?: string
  date?: string
  updated?: string
  tags: string[]
  html: string
  headings: Heading[]
  outbound: string[]
  backlinks: string[]
  wordCount: number
  vaultPath: string
}

interface RawNote {
  vaultPath: string
  basename: string
  data: Record<string, unknown>
  body: string
}

async function* walk(dir: string): AsyncGenerator<string> {
  let entries
  try {
    entries = await fs.readdir(dir, { withFileTypes: true })
  } catch {
    return
  }
  for (const entry of entries) {
    if (SKIP_DIRS.has(entry.name)) continue
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) yield* walk(full)
    else yield full
  }
}

function slugify(input: string): string {
  return new GithubSlugger().slug(input)
}

function asStringArray(value: unknown): string[] {
  if (Array.isArray(value)) return value.map(String)
  if (typeof value === 'string') return value.split(',').map((s) => s.trim()).filter(Boolean)
  return []
}

/** Frontmatter dates arrive as strings or as YAML-parsed Dates. */
function asDate(value: unknown): string | undefined {
  if (value instanceof Date) return value.toISOString().slice(0, 10)
  if (typeof value === 'string' && value.trim()) return value.trim().slice(0, 10)
  return undefined
}

function textOf(node: ElementContent | Element): string {
  if ('value' in node && typeof node.value === 'string') return node.value
  if ('children' in node && Array.isArray(node.children)) {
    return node.children.map((c) => textOf(c as ElementContent)).join('')
  }
  return ''
}

async function main() {
  console.log(`vault: ${VAULT}`)

  // ---- pass 1: read every note, but only to decide what is allowed out ----
  const allNotes: RawNote[] = []
  const assetsByBasename = new Map<string, string>()
  const assetsByRelPath = new Map<string, string>()

  let unnamed = 0

  for await (const file of walk(VAULT)) {
    const rel = path.relative(VAULT, file)
    const ext = path.extname(file).toLowerCase()

    // Detect markdown by suffix, not path.extname: Node reports extname('.md')
    // as '' because it reads a leading dot as a dotfile marker. Testing the
    // extension would silently skip these instead of rejecting them on purpose.
    if (file.toLowerCase().endsWith('.md')) {
      const basename = path.basename(file, '.md')
      if (basename === '' || basename === '.md') {
        // Obsidian leaves these behind when a note is created and never titled.
        unnamed++
        continue
      }
      const src = await fs.readFile(file, 'utf8')
      const { data, content } = matter(src)
      allNotes.push({
        vaultPath: rel,
        basename,
        data: data as Record<string, unknown>,
        body: content,
      })
      continue
    }

    if (MEDIA_EXT.has(ext)) {
      const base = path.basename(file).toLowerCase()
      // First writer wins; Obsidian resolves ambiguous basenames the same way.
      if (!assetsByBasename.has(base)) assetsByBasename.set(base, file)
      assetsByRelPath.set(rel.toLowerCase(), file)
    }
  }

  const published = allNotes.filter((n) => n.data.publish === true)
  console.log(`found ${allNotes.length} notes, ${published.length} flagged publish: true`)
  if (unnamed > 0) console.log(`skipped ${unnamed} untitled notes (filename is just ".md")`)

  if (published.length === 0) {
    console.log('\nnothing to publish. add `publish: true` to a note\'s frontmatter.')
  }

  // ---- pass 2: assign slugs and build the link index ----
  const docs = new Map<string, Doc>()
  const byBasename = new Map<string, Doc>()
  const byVaultPath = new Map<string, Doc>()

  for (const note of published) {
    const title = typeof note.data.title === 'string' ? note.data.title : note.basename
    const slug = typeof note.data.slug === 'string' ? note.data.slug : slugify(note.basename)
    const kind: DocKind = note.data.type === 'post' ? 'post' : 'note'

    const existing = docs.get(slug)
    if (existing) {
      throw new Error(
        `slug collision: "${slug}" claimed by both\n  ${existing.vaultPath}\n  ${note.vaultPath}\n` +
          `Set an explicit \`slug:\` in one note's frontmatter.`,
      )
    }

    const doc: Doc = {
      slug,
      kind,
      title,
      description: typeof note.data.description === 'string' ? note.data.description : undefined,
      date: asDate(note.data.date),
      updated: asDate(note.data.updated),
      tags: asStringArray(note.data.tags),
      html: '',
      headings: [],
      outbound: [],
      backlinks: [],
      wordCount: note.body.split(/\s+/).filter(Boolean).length,
      vaultPath: note.vaultPath,
    }

    docs.set(slug, doc)
    byBasename.set(note.basename.toLowerCase(), doc)
    byVaultPath.set(note.vaultPath.replace(/\.md$/i, '').toLowerCase(), doc)
  }

  const hrefFor = (doc: Doc) => (doc.kind === 'post' ? `/blog/${doc.slug}` : `/notes/${doc.slug}`)

  // ---- asset copying: only what published notes actually reference ----
  await fs.rm(ASSET_OUT, { recursive: true, force: true })
  await fs.mkdir(ASSET_OUT, { recursive: true })
  const copiedAssets = new Map<string, string>()

  async function publishAsset(ref: string): Promise<string | null> {
    const key = ref.toLowerCase()
    const source = assetsByRelPath.get(key) ?? assetsByBasename.get(path.basename(key))
    if (!source) return null

    const cached = copiedAssets.get(source)
    if (cached) return cached

    const bytes = await fs.readFile(source)
    const hash = crypto.createHash('sha256').update(bytes).digest('hex').slice(0, 8)
    const ext = path.extname(source)
    // Obsidian filenames are full of spaces; slugify so URLs need no escaping.
    const name = `${slugify(path.basename(source, ext))}-${hash}${ext}`
    await fs.writeFile(path.join(ASSET_OUT, name), bytes)
    const url = `${ASSET_URL}/${name}`
    copiedAssets.set(source, url)
    return url
  }

  const brokenLinks: { from: string; target: string }[] = []
  const missingAssets: { from: string; target: string }[] = []

  // ---- pass 3: render ----
  for (const note of published) {
    const doc = docs.get(
      typeof note.data.slug === 'string' ? note.data.slug : slugify(note.basename),
    )!
    const outbound = new Set<string>()

    const remarkWikiLinks = () => async (tree: MdRoot) => {
      const pendingAssets: { node: Image; ref: string }[] = []
      // Embed-created nodes are queued with their real target below; without
      // this the generic image walk re-queues them under their empty
      // placeholder url and reports a phantom missing attachment.
      const fromEmbed = new WeakSet<Image>()

      visit(tree, 'text', (node: Text, index, parent) => {
        if (!parent || index === undefined || !WIKILINK.test(node.value)) return
        WIKILINK.lastIndex = 0

        const out: PhrasingContent[] = []
        let cursor = 0
        let match: RegExpExecArray | null

        while ((match = WIKILINK.exec(node.value)) !== null) {
          const [full, bang, rawTarget, heading, alias] = match
          if (match.index > cursor) {
            out.push({ type: 'text', value: node.value.slice(cursor, match.index) })
          }
          cursor = match.index + full.length

          const target = rawTarget.trim()
          const label = (alias ?? target).trim()
          const isEmbed = bang === '!'
          const ext = path.extname(target).toLowerCase()

          if (isEmbed && MEDIA_EXT.has(ext)) {
            const image: Image = { type: 'image', url: '', alt: label }
            fromEmbed.add(image)
            pendingAssets.push({ node: image, ref: target })
            out.push(image)
            continue
          }

          const hit =
            byBasename.get(target.toLowerCase()) ??
            byVaultPath.get(target.replace(/\.md$/i, '').toLowerCase())

          if (hit) {
            outbound.add(hit.slug)
            const link: Link = {
              type: 'link',
              url: hrefFor(hit) + (heading ? `#${slugify(heading)}` : ''),
              children: [{ type: 'text', value: label }],
            }
            out.push(link)
          } else {
            // Unpublished or nonexistent target: degrade to plain text rather
            // than emit a link that 404s or hints at a private note's title.
            brokenLinks.push({ from: doc.slug, target })
            out.push({ type: 'text', value: label })
          }
        }

        if (cursor < node.value.length) {
          out.push({ type: 'text', value: node.value.slice(cursor) })
        }
        parent.children.splice(index, 1, ...out)
        return index + out.length
      })

      // Ordinary markdown images pointing at vault-relative paths.
      visit(tree, 'image', (node: Image) => {
        if (fromEmbed.has(node)) return
        if (/^(https?:)?\/\//.test(node.url) || node.url.startsWith('/')) return
        pendingAssets.push({ node, ref: decodeURIComponent(node.url) })
      })

      // Copying is async, so it runs after the synchronous walks. unified
      // awaits a transformer's promise, which is why this plugin can be async.
      for (const { node, ref } of pendingAssets) {
        const url = await publishAsset(ref)
        if (url) node.url = url
        else missingAssets.push({ from: doc.slug, target: ref })
      }
    }

    const rehypeCollectHeadings = () => (tree: HastRoot) => {
      visit(tree, 'element', (node: Element) => {
        if (!/^h[1-6]$/.test(node.tagName)) return
        const id = typeof node.properties?.id === 'string' ? node.properties.id : ''
        if (id) doc.headings.push({ depth: Number(node.tagName[1]), id, text: textOf(node) })
      })
    }

    const processor = unified()
      .use(remarkParse)
      .use(remarkGfm)
      .use(remarkWikiLinks)
      .use(remarkRehype)
      .use(rehypeSlug)
      .use(rehypeCollectHeadings)
      .use(rehypeCallouts)
      .use(rehypeShiki, { themes: { light: 'github-light', dark: 'github-dark' } })
      .use(rehypeStringify)

    doc.html = String(await processor.process(note.body))
    doc.outbound = [...outbound]
  }

  // ---- backlinks: invert the outbound graph ----
  for (const doc of docs.values()) {
    for (const target of doc.outbound) {
      docs.get(target)?.backlinks.push(doc.slug)
    }
  }

  await fs.mkdir(OUT_DIR, { recursive: true })
  const bodyDir = path.join(OUT_DIR, 'docs')
  await fs.rm(bodyDir, { recursive: true, force: true })
  await fs.mkdir(bodyDir, { recursive: true })

  const all = [...docs.values()].sort((a, b) => (b.date ?? '').localeCompare(a.date ?? ''))

  // Metadata and bodies are emitted separately so the client bundle carries
  // only the index. Rendered HTML for 500 notes would otherwise sit in the
  // entry chunk and be downloaded by everyone who loads any page.
  const index = all.map(({ html, ...meta }) => {
    void html
    return meta
  })
  await fs.writeFile(path.join(OUT_DIR, 'index.json'), JSON.stringify(index, null, 2))
  for (const doc of all) {
    await fs.writeFile(
      path.join(bodyDir, `${doc.slug}.json`),
      JSON.stringify({ html: doc.html }),
    )
  }

  // ---- report: the point is that you can eyeball exactly what escaped ----
  console.log(`\npublished ${all.length} docs (${all.filter((d) => d.kind === 'post').length} posts, ${all.filter((d) => d.kind === 'note').length} notes)`)
  for (const doc of all) console.log(`  ${doc.kind.padEnd(4)} /${doc.kind === 'post' ? 'blog' : 'notes'}/${doc.slug}  <- ${doc.vaultPath}`)
  console.log(`\nheld back ${allNotes.length - published.length} notes (no publish: true)`)
  console.log(`copied ${copiedAssets.size} attachments`)
  if (brokenLinks.length) {
    console.log(`\n${brokenLinks.length} wikilinks pointed at unpublished notes (rendered as plain text):`)
    for (const b of brokenLinks.slice(0, 20)) console.log(`  ${b.from} -> [[${b.target}]]`)
    if (brokenLinks.length > 20) console.log(`  ...and ${brokenLinks.length - 20} more`)
  }
  if (missingAssets.length) {
    console.log(`\n${missingAssets.length} attachments not found in the vault:`)
    for (const m of missingAssets.slice(0, 20)) console.log(`  ${m.from} -> ${m.target}`)
  }
}

main().catch((error) => {
  console.error(error)
  process.exit(1)
})
