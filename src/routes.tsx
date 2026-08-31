import type { RouteObject } from 'react-router'
import { Layout } from './components/Layout'
import { Home } from './pages/Home'
import { Projects } from './pages/Projects'
import { Games } from './pages/Games'
import { Art } from './pages/Art'
import { Cv } from './pages/Cv'
import { Blog } from './pages/Blog'
import { Notes } from './pages/Notes'
import { DocPage } from './pages/DocPage'
import { Contact } from './pages/Contact'
import { SiteInfo } from './pages/SiteInfo'
import { NotFound } from './pages/NotFound'
import { site } from './data/site'
import { posts, notes, getDoc, loadDocHtml } from './lib/content'
import type { DocKind } from './lib/content'

/**
 * Bodies live in their own chunks, so they must be resolved before render.
 * A loader is the right seam: createStaticHandler runs it during prerender and
 * createBrowserRouter runs it before the route mounts, so one function covers
 * both without the component ever showing a loading state.
 */
function docLoader(kind: DocKind) {
  return async ({ params }: { params: { slug?: string } }) => {
    const slug = params.slug
    const doc = slug ? getDoc(slug) : undefined
    if (!doc || doc.kind !== kind) return { doc: null, html: '' }
    return { doc, html: await loadDocHtml(doc.slug) }
  }
}

export const routes: RouteObject[] = [
  {
    path: '/',
    Component: Layout,
    children: [
      { index: true, Component: Home },
      { path: 'projects', Component: Projects },
      { path: 'games', Component: Games },
      { path: 'art', Component: Art },
      { path: 'cv', Component: Cv },
      { path: 'blog', Component: Blog },
      { path: 'blog/:slug', element: <DocPage />, loader: docLoader('post') },
      { path: 'notes', Component: Notes },
      { path: 'notes/:slug', element: <DocPage />, loader: docLoader('note') },
      { path: 'contact', Component: Contact },
      { path: 'siteinfo', Component: SiteInfo },
      { path: '*', Component: NotFound },
    ],
  },
]

export interface PageMeta {
  path: string
  title: string
  description: string
}

const STATIC_PAGES: PageMeta[] = [
  { path: '/', title: site.title, description: site.description },
  {
    path: '/projects',
    title: `Projects - ${site.title}`,
    description: 'Hardware and software projects by Milo Tekchandani.',
  },
  {
    path: '/games',
    title: `Games - ${site.title}`,
    description: 'Games built in Godot, Roblox and C#.',
  },
  {
    path: '/art',
    title: `Art - ${site.title}`,
    description: 'Artwork made in Procreate over the years.',
  },
  { path: '/cv', title: `CV - ${site.title}`, description: 'Résumé of Milo Tekchandani.' },
  { path: '/blog', title: `Blog - ${site.title}`, description: 'Writing, published from Obsidian.' },
  {
    path: '/notes',
    title: `Notes - ${site.title}`,
    description: 'A published slice of my Obsidian vault.',
  },
  { path: '/contact', title: `Contact - ${site.title}`, description: 'How to reach me.' },
  { path: '/siteinfo', title: `Site info - ${site.title}`, description: 'How this site is built.' },
  { path: '/404', title: `Not found - ${site.title}`, description: 'Page not found.' },
]

/**
 * Every URL the prerenderer should emit. Dynamic routes are expanded here from
 * the generated content, so adding a note to the vault adds a page with no
 * routing change.
 */
export function allPages(): PageMeta[] {
  return [
    ...STATIC_PAGES,
    ...posts.map((post) => ({
      path: `/blog/${post.slug}`,
      title: `${post.title} - ${site.title}`,
      description: post.description ?? site.description,
    })),
    ...notes.map((note) => ({
      path: `/notes/${note.slug}`,
      title: `${note.title} - ${site.title}`,
      description: note.description ?? site.description,
    })),
  ]
}
