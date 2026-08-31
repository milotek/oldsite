import { site } from '../data/site'

/**
 * Per-page title and description.
 *
 * React 19 hoists <title> and <meta> into <head> from wherever they are
 * rendered, so a page states its own metadata inline. No helmet library, and
 * no second table of titles to keep in step with the route list.
 */
export function Meta({ title, description }: { title?: string; description?: string }) {
  return (
    <>
      <title>{title ? `${title} - ${site.title}` : site.title}</title>
      <meta name="description" content={description ?? site.description} />
    </>
  )
}
