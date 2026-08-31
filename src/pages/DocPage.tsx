import { Link, useLoaderData } from 'react-router'
import { getDoc, formatDate, hrefFor } from '../lib/content'
import { Prose } from '../components/Prose'
import { NotFound } from './NotFound'
import type { Doc } from '../lib/content'

/**
 * Posts and notes render identically apart from their metadata line, so one
 * component serves both routes rather than two that drift apart.
 */
export function DocPage() {
  const { doc, html } = useLoaderData() as { doc: Doc | null; html: string }

  if (!doc) return <NotFound />

  return (
    <article className="stack">
      <header>
        <p className="eyebrow">{doc.kind === 'post' ? 'blog' : 'note'}</p>
        <h1>{doc.title}</h1>
        <div className="meta">
          {doc.date && <span>{formatDate(doc.date)}</span>}
          {doc.updated && doc.updated !== doc.date && (
            <span>updated {formatDate(doc.updated)}</span>
          )}
          <span>{doc.wordCount} words</span>
          {doc.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </div>
      </header>

      <Prose html={html} />

      {doc.backlinks.length > 0 && (
        <section className="backlinks">
          <h2>Linked from</h2>
          <ul>
            {doc.backlinks.map((slug) => {
              const source = getDoc(slug)
              if (!source) return null
              return (
                <li key={slug}>
                  <Link to={hrefFor(source)}>{source.title}</Link>
                </li>
              )
            })}
          </ul>
        </section>
      )}
    </article>
  )
}
