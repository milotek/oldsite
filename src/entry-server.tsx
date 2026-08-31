import { StrictMode } from 'react'
import { renderToString } from 'react-dom/server'
import { createStaticHandler, createStaticRouter, StaticRouterProvider } from 'react-router'
import { routes } from './routes'

export { allPages } from './routes'

/**
 * Render one URL to an HTML string. Called by scripts/prerender.ts once per
 * page; there is no server at runtime.
 */
export async function render(url: string): Promise<string> {
  const handler = createStaticHandler(routes)
  const context = await handler.query(new Request(`http://localhost${url}`))

  if (context instanceof Response) {
    throw new Error(`Unexpected redirect while prerendering ${url}`)
  }

  const router = createStaticRouter(handler.dataRoutes, context)

  return renderToString(
    <StrictMode>
      <StaticRouterProvider router={router} context={context} />
    </StrictMode>,
  )
}
