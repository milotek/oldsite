import { Link } from 'react-router'
import type { Status } from '../data/projects'

/**
 * One row in a list of work. Projects and games differ only in whether they
 * carry a status, so they share this rather than growing two near-identical
 * cards that drift apart.
 */
export function Entry({
  index,
  to,
  title,
  blurb,
  year,
  tech,
  status,
}: {
  index: number
  to: string
  title: string
  blurb: string
  year: string
  tech: string[]
  status?: Status
}) {
  return (
    <li className="entry">
      <span className="entry__index" aria-hidden="true">
        {String(index + 1).padStart(2, '0')}
      </span>
      <div className="entry__body">
        <h3 className="entry__title">
          <Link to={to} viewTransition>
            {title}
          </Link>
        </h3>
        <p className="entry__blurb">{blurb}</p>
        <div className="entry__meta">
          {status ? <span className={`status status--${status}`}>{status}</span> : null}
          <span>{year}</span>
          {tech.map((item) => (
            <span className="tag" key={item}>
              {item}
            </span>
          ))}
        </div>
      </div>
    </li>
  )
}
