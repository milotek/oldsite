import { site, socials } from '../data/site'

export function Contact() {
  return (
    <div className="stack">
      <header>
        <p className="eyebrow">contact</p>
        <h1>Get in touch</h1>
      </header>

      <p>
        Email is best: <a href={`mailto:${site.email}`}>{site.email}</a>
      </p>

      <ul className="card-list">
        {socials.map((s) => (
          <li key={s.label} className="card">
            <h3>{s.label}</h3>
            <p>
              <a href={s.href} rel="me noopener">
                {s.handle}
              </a>
            </p>
          </li>
        ))}
      </ul>
    </div>
  )
}
