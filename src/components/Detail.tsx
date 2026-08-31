import type { ReactNode } from 'react'
import { Link } from 'react-router'
import type { Link as LinkData, Shot, Status } from '../data/projects'
import { PageHead } from './PageHead'
import { Meta } from './Meta'

/**
 * The body shared by a project page and a game page: bullets, links, and a
 * screenshot strip. Both data shapes already agree on these fields, so the
 * page components below stay a handful of lines each.
 */
export function Detail({
  backTo,
  backLabel,
  eyebrow,
  title,
  blurb,
  year,
  tech,
  status,
  points,
  links,
  shots,
  children,
}: {
  backTo: string
  backLabel: string
  eyebrow: string
  title: string
  blurb: string
  year: string
  tech: string[]
  status?: Status
  points: string[]
  links: LinkData[]
  shots: Shot[]
  children?: ReactNode
}) {
  return (
    <article>
      <Meta title={title} description={blurb} />
      <Link className="back" to={backTo} viewTransition>
        &larr; {backLabel}
      </Link>

      <PageHead eyebrow={eyebrow} title={title} lede={blurb} />

      <div className="detail">
        <div className="entry__meta">
          {status ? <span className={`status status--${status}`}>{status}</span> : null}
          <span>{year}</span>
          {tech.map((item) => (
            <span className="tag" key={item}>
              {item}
            </span>
          ))}
        </div>

        <ul>
          {points.map((point) => (
            <li key={point}>{point}</li>
          ))}
        </ul>

        {links.length > 0 ? (
          <div className="linkrow">
            {links.map((link) => (
              <a className="button" key={link.href} href={link.href} rel="noreferrer">
                {link.label}
              </a>
            ))}
          </div>
        ) : (
          <p className="eyebrow">No public source for this one.</p>
        )}
      </div>

      {children}

      {shots.length > 0 ? (
        <ul className="shots">
          {shots.map((shot) => (
            <li key={shot.src}>
              <figure>
                <img src={shot.src} alt={shot.alt} loading="lazy" />
                <figcaption>{shot.caption}</figcaption>
              </figure>
            </li>
          ))}
        </ul>
      ) : null}
    </article>
  )
}
