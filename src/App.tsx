import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import Art from './pages/Art'
import Cv from './pages/Cv'
import Games from './pages/Games'
import Home from './pages/Home'
import Misc from './pages/Misc'
import NotFound from './pages/NotFound'
import Projects from './pages/Projects'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="projects" element={<Projects />} />
        <Route path="games" element={<Games />} />
        <Route path="cv" element={<Cv />} />
        <Route path="art" element={<Art />} />
        <Route path="misc" element={<Misc />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}
