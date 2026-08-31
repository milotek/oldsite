import type { RouteObject } from 'react-router'
import { Layout } from './components/Layout'
import { Home } from './pages/Home'
import { Projects, ProjectDetail } from './pages/Projects'
import { Games, GameDetail } from './pages/Games'
import { Art } from './pages/Art'
import { Blog, BlogPost } from './pages/Blog'
import { Cv } from './pages/Cv'
import { Misc } from './pages/Misc'
import { Colophon } from './pages/Colophon'
import { NotFound } from './pages/NotFound'

export const routes: RouteObject[] = [
  {
    path: '/',
    Component: Layout,
    children: [
      { index: true, Component: Home },
      { path: 'projects', Component: Projects },
      { path: 'projects/:slug', Component: ProjectDetail },
      { path: 'games', Component: Games },
      { path: 'games/:slug', Component: GameDetail },
      { path: 'art', Component: Art },
      { path: 'blog', Component: Blog },
      { path: 'blog/:slug', Component: BlogPost },
      { path: 'cv', Component: Cv },
      { path: 'misc', Component: Misc },
      { path: 'colophon', Component: Colophon },
      { path: '*', Component: NotFound },
    ],
  },
]
