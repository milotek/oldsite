import type { RouteObject } from 'react-router'
import { Layout } from './components/Layout'
import { Home } from './pages/Home'
import { Projects, ProjectDetail } from './pages/Projects'
import { Games, GameDetail } from './pages/Games'
import { Art } from './pages/Art'
import { Cv } from './pages/Cv'
import { Contact } from './pages/Contact'
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
      { path: 'cv', Component: Cv },
      { path: 'misc', Component: Misc },
      { path: 'contact', Component: Contact },
      { path: 'colophon', Component: Colophon },
      { path: '*', Component: NotFound },
    ],
  },
]
