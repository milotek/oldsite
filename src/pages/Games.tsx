import { games } from '../data/games'

export function Games() {
  return (
    <div className="stack">
      <header>
        <p className="eyebrow">games</p>
        <h1>Games</h1>
        <p className="lede">Godot, Roblox and a pile of C#.</p>
      </header>

      <ul className="card-list">
        {games.map((g) => (
          <li key={g.slug} id={g.slug} className="card">
            <h3>{g.title}</h3>
            <p>{g.blurb}</p>
            <div className="meta">
              <span>{g.year}</span>
            </div>
            <div className="chip-row">
              {g.tech.map((t) => (
                <span key={t} className="tag">
                  {t}
                </span>
              ))}
            </div>
            <ul>
              {g.points.map((point) => (
                <li key={point}>{point}</li>
              ))}
            </ul>
            {g.links.length > 0 && (
              <div className="link-row">
                {g.links.map((l) => (
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
