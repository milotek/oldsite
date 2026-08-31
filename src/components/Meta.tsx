import { site } from '../data/site'

/**
 * Per-page document title and description.
 *
 * React 19 hoists <title> and <meta> to <head> wherever they are rendered, so
 * a page declares its own metadata inline and there is no helmet library and
 * no separate table of titles to keep in sync with the routes.
 */
export function Meta({ title, description }: { title?: string; description?: string }) {
  return (
    <>
      <title>{title ? `${title} - ${site.title}` : site.title}</title>
      <meta name="description" content={description ?? site.description} />
    </>
  )
}
