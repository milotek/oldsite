import { site } from '../data/site'

/**
 * React 19 hoists title/meta rendered anywhere in the tree into <head>, so
 * per-page metadata needs no helmet library and no effect.
 */
export default function PageHead({
  title,
  description,
}: {
  title?: string
  description?: string
}) {
  const full = title ? `${title} // ${site.title}` : site.title
  return (
    <>
      <title>{full}</title>
      <meta name="description" content={description ?? site.description} />
      <meta property="og:title" content={full} />
      <meta property="og:description" content={description ?? site.description} />
      <meta property="og:type" content="website" />
      <meta property="og:site_name" content={site.title} />
    </>
  )
}
