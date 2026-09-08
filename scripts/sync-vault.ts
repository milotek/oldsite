/**
 * Turns the Obsidian vault's Personal/Blogs folder into Astro content.
 *
 * Obsidian markdown is not CommonMark: embeds, wikilinks and callouts all need
 * rewriting, and attachments live wherever Obsidian dropped them. Doing that
 * here, before the markdown processor sees the file, keeps the site independent
 * of whichever processor Astro ships next.
 *
 * A post is published only when its frontmatter carries `published: YYYY-MM-DD`.
 * Everything else in the folder is a draft and is skipped unless PUBLISH_DRAFTS=1.
 */
import { copyFile, mkdir, readdir, readFile, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { parse as parseYaml } from 'yaml';

const VAULT = process.env.VAULT_DIR ?? 'vault';
const POSTS = path.join(VAULT, 'Personal', 'Blogs');
const OUT = path.join('src', 'content', 'blog');
const includeDrafts = process.env.PUBLISH_DRAFTS === '1';

const IMAGE_EXT = new Set(['.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif', '.svg']);

async function* walk(dir: string): AsyncGenerator<string> {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* walk(full);
    else yield full;
  }
}

async function indexAttachments(): Promise<Map<string, string>> {
  const map = new Map<string, string>();
  for await (const file of walk(VAULT)) {
    if (path.extname(file) === '.md') continue;
    map.set(path.basename(file), file);
  }
  return map;
}

function slugify(s: string): string {
  return s
    .toLowerCase()
    .replace(/['’]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function splitFrontmatter(raw: string): { data: Record<string, unknown>; body: string } {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!m) return { data: {}, body: raw };
  const data = (parseYaml(m[1]!) as Record<string, unknown> | null) ?? {};
  return { data, body: raw.slice(m[0].length) };
}

interface Post {
  slug: string;
  title: string;
  published?: Date;
  summary?: string;
  body: string;
  attachments: Map<string, string>;
}

function rewriteEmbeds(body: string, attachments: Map<string, string>, used: Map<string, string>): string {
  // `![[file.png|300]]`, or `![[file.png\|300]]` inside a table cell.
  return body.replace(/!\[\[([^\]|\\]+)(?:\\?\|[^\]]*)?\]\]/g, (_, target: string) => {
    const name = target.trim();
    const source = attachments.get(name);
    if (!source) {
      console.warn(`  missing attachment: ${name}`);
      return '';
    }
    const local = slugify(path.parse(name).name) + path.extname(name).toLowerCase();
    used.set(local, source);
    if (IMAGE_EXT.has(path.extname(local))) return `![${path.parse(name).name}](./${local})`;
    return `[${name}](./${local})`;
  });
}

function rewriteWikilinks(body: string): string {
  // Notes elsewhere in the vault are private, so a wikilink degrades to text.
  return body.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (_, target: string, label?: string) => label ?? target);
}

function dropEmptyLinks(body: string): string {
  return body.replace(/\[([^\]]+)\]\(\s*\)/g, '$1');
}

const LIST_ITEM = /^\s*(?:[-*+]|\d+[.)])\s/;
const BLOCK_START = /^(?:\s|#|>|\||```|<|---|!\[)/;

/**
 * Obsidian renders a single newline as a line break and starts a new paragraph
 * straight after a list; CommonMark joins the first and swallows the second
 * into the last list item. Rewrite to what the author saw in the editor.
 */
function matchObsidianLineBreaks(body: string): string {
  const lines = body.split('\n');
  const out: string[] = [];
  let inFence = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]!;
    const next = lines[i + 1];
    if (/^\s*```/.test(line)) inFence = !inFence;
    out.push(line);
    if (inFence || next === undefined || !next.trim() || !line.trim()) continue;
    if (LIST_ITEM.test(line) && !LIST_ITEM.test(next) && !BLOCK_START.test(next)) {
      out.push('');
      continue;
    }
    const plain = (l: string) => !BLOCK_START.test(l) && !LIST_ITEM.test(l);
    if (plain(line) && plain(next) && !line.endsWith('  ')) {
      out[out.length - 1] = line + '  ';
    }
  }
  return out.join('\n');
}

function rewriteCallouts(body: string): string {
  const lines = body.split('\n');
  const out: string[] = [];
  for (let i = 0; i < lines.length; i++) {
    const head = lines[i]!.match(/^>\s*\[!(\w+)\]([-+]?)\s*(.*)$/);
    if (!head) {
      out.push(lines[i]!);
      continue;
    }
    const [, type, fold, rawTitle] = head;
    const kind = type!.toLowerCase();
    const title = rawTitle?.trim() || kind[0]!.toUpperCase() + kind.slice(1);
    const inner: string[] = [];
    while (i + 1 < lines.length && /^>/.test(lines[i + 1]!)) {
      inner.push(lines[++i]!.replace(/^>\s?/, ''));
    }
    const tag = fold ? 'details' : 'aside';
    const open = fold === '+' ? ' open' : '';
    out.push(`<${tag} class="callout" data-callout="${kind}"${open}>`);
    out.push(fold ? `<summary>${title}</summary>` : `<p class="callout-title">${title}</p>`);
    out.push('', ...inner, '', `</${tag}>`);
  }
  return out.join('\n');
}

async function readPost(file: string, attachments: Map<string, string>): Promise<Post | undefined> {
  const raw = await readFile(file, 'utf8');
  if (!raw.trim()) return undefined;
  const { data, body } = splitFrontmatter(raw);
  const stem = path.parse(file).name;
  const aliases = Array.isArray(data.aliases) ? (data.aliases as string[]) : [];
  const title = typeof data.title === 'string' ? data.title : (aliases[0] ?? stem);
  const published = data.published ? new Date(String(data.published)) : undefined;
  const used = new Map<string, string>();
  let text = rewriteEmbeds(body, attachments, used);
  text = rewriteWikilinks(text);
  text = dropEmptyLinks(text);
  text = rewriteCallouts(text);
  text = matchObsidianLineBreaks(text);
  return {
    slug: slugify(stem),
    title,
    published,
    summary: typeof data.summary === 'string' ? data.summary : undefined,
    body: text.trim() + '\n',
    attachments: used,
  };
}

async function writePost(post: Post) {
  const dir = path.join(OUT, post.slug);
  await mkdir(dir, { recursive: true });
  for (const [local, source] of post.attachments) {
    await copyFile(source, path.join(dir, local));
  }
  const fm = [
    '---',
    `title: ${JSON.stringify(post.title)}`,
    `published: ${(post.published ?? new Date()).toISOString().slice(0, 10)}`,
    post.summary ? `summary: ${JSON.stringify(post.summary)}` : undefined,
    `draft: ${post.published ? 'false' : 'true'}`,
    '---',
    '',
  ].filter((l) => l !== undefined);
  await writeFile(path.join(dir, 'index.md'), fm.join('\n') + post.body);
}

async function main() {
  try {
    await stat(POSTS);
  } catch {
    console.warn(`No vault at ${POSTS}; the blog will be empty.`);
    await mkdir(OUT, { recursive: true });
    return;
  }
  await rm(OUT, { recursive: true, force: true });
  await mkdir(OUT, { recursive: true });
  const attachments = await indexAttachments();
  let published = 0;
  let drafts = 0;
  for (const entry of await readdir(POSTS)) {
    if (path.extname(entry) !== '.md') continue;
    const post = await readPost(path.join(POSTS, entry), attachments);
    if (!post) continue;
    if (!post.published && !includeDrafts) {
      drafts++;
      continue;
    }
    await writePost(post);
    published++;
  }
  console.log(`vault: ${published} post(s) written, ${drafts} draft(s) skipped`);
}

await main();
