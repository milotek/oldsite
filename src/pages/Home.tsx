import { Link } from 'react-router'
import { site, socials } from '../data/site'
import { projects } from '../data/projects'
import { games } from '../data/games'
import { posts } from '../lib/content'
import { formatDate } from '../lib/content'

export function Home() {
  return (
    <div className="stack">
      <section>
        <p className="eyebrow">personal site // code projects // portfolio</p>
        <h1>{site.name}</h1>
        <p className="lede">{site.role}</p>
        <p className="link-row">
          {socials.map((s) => (
            <a key={s.label} href={s.href} rel="me noopener">
              {s.label.toLowerCase()}
            </a>
          ))}
        </p>
      </section>

      <section>
        <h2>Selected work</h2>
        <ul className="card-list">
          {projects.slice(0, 3).map((p) => (
            <li key={p.slug} className="card">
              <h3>
                <Link to={`/projects#${p.slug}`}>{p.title}</Link>
              </h3>
              <p>{p.blurb}</p>
              <div className="meta">
                <span className={`status status--${p.status}`}>{p.status}</span>
                <span>{p.year}</span>
                <span>{p.tech.join(' / ')}</span>
              </div>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Games</h2>
        <ul className="card-list">
          {games.map((g) => (
            <li key={g.slug} className="card">
              <h3>
                <Link to={`/games#${g.slug}`}>{g.title}</Link>
              </h3>
              <p>{g.blurb}</p>
              <div className="meta">
                <span>{g.year}</span>
                <span>{g.tech.join(' / ')}</span>
              </div>
            </li>
          ))}
        </ul>
      </section>

      {posts.length > 0 && (
        <section>
          <h2>Writing</h2>
          <ul className="card-list">
            {posts.slice(0, 4).map((post) => (
              <li key={post.slug} className="card">
                <h3>
                  <Link to={`/blog/${post.slug}`}>{post.title}</Link>
                </h3>
                {post.description && <p>{post.description}</p>}
                <div className="meta">
                  <span>{formatDate(post.date)}</span>
                </div>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}
