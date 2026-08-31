import { Link } from 'react-router'
import { CalendarIcon, ImageIcon, TrophyIcon } from './Icons'

/**
 * The card used for both projects and games.
 *
 * Entries without a thumbnail get a flat tinted field rather than a stock
 * placeholder image: an honest empty state reads better in a grid than the
 * same grey photo repeated three times.
 */
export function Card({
  to,
  title,
  blurb,
  year,
  thumb,
  featured,
  badge,
  eager,
}: {
  to: string
  title: string
  blurb: string
  year: string
  thumb?: string
  featured?: boolean
  badge?: string
  eager?: boolean
}) {
  return (
    <Link to={to} className="card" viewTransition>
      {thumb ? (
        <div className="card-image">
          <img src={thumb} alt="" loading={eager ? 'eager' : 'lazy'} />
        </div>
      ) : (
        <div className="card-image empty">
          <ImageIcon />
        </div>
      )}
      <div className="card-body">
        <p className="card-meta">
          <CalendarIcon />
          <span>{year}</span>
          {badge ? <span className="badge">{badge}</span> : null}
          {featured ? (
            <span className="badge accent">
              <TrophyIcon />
              featured
            </span>
          ) : null}
        </p>
        <h3 className="card-title">{title}</h3>
        <p className="card-blurb">{blurb}</p>
      </div>
    </Link>
  )
}
