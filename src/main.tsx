import { StrictMode } from 'react'
import { hydrateRoot, createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router'
import { routes } from './routes'
import './styles/app.css'

const router = createBrowserRouter(routes)
const container = document.getElementById('root')!

const app = (
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
)

// The prerendered pages ship real markup, so hydrate them. `npm run dev` has
// an empty root, and hydrating that would warn and throw away the tree.
if (container.hasChildNodes()) {
  hydrateRoot(container, app)
} else {
  createRoot(container).render(app)
}
