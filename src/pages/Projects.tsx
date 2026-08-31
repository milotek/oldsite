import { projects } from '../data/projects'

export function Projects() {
  return (
    <div className="stack">
      <header>
        <p className="eyebrow">projects</p>
        <h1>Things I have built</h1>
        <p className="lede">Hardware and software, most of them shipped to somebody.</p>
      </header>

      <ul className="card-list">
        {projects.map((p) => (
          <li key={p.slug} id={p.slug} className="card">
            <h3>{p.title}</h3>
            <p>{p.blurb}</p>
            <div className="meta">
              <span className={`status status--${p.status}`}>{p.status}</span>
              <span>{p.year}</span>
            </div>
            <div className="chip-row">
              {p.tech.map((t) => (
                <span key={t} className="tag">
                  {t}
                </span>
              ))}
            </div>
            <ul>
              {p.points.map((point) => (
                <li key={point}>{point}</li>
              ))}
            </ul>
            {p.links.length > 0 && (
              <div className="link-row">
                {p.links.map((l) => (
                  <a key={l.href} href={l.href} rel="noopener">
                    {l.label}
                  </a>
                ))}
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
