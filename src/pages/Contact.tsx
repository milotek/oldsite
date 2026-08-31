import { site, socials } from '../data/site'
import { PageHead } from '../components/PageHead'
import { Meta } from '../components/Meta'

export function Contact() {
  return (
    <>
      <Meta title="Contact" description="How to reach me." />
      <PageHead
        eyebrow="Say hello"
        title="Contact"
        lede="Email is the one I actually read. The rest are there for completeness."
      />

      <div className="detail">
        <div className="linkrow" style={{ marginTop: 0 }}>
          <a className="button" href={`mailto:${site.email}`}>
            {site.email}
          </a>
        </div>

        <ul style={{ marginTop: '2.5rem' }}>
          {socials
            .filter((social) => social.label !== 'Email')
            .map((social) => (
              <li key={social.label}>
                <a href={social.href} rel="me noreferrer">
                  {social.label}
                </a>{' '}
                <span className="eyebrow" style={{ display: 'inline', margin: 0 }}>
                  {social.handle}
                </span>
              </li>
            ))}
        </ul>

        <p style={{ marginTop: '2.5rem' }} className="lede">
          I like to keep my real self and my online persona a bit separate, so this is where the
          oversharing stops. Thanks for visiting.
        </p>

        <blockquote
          className="eyebrow"
          style={{ margin: '2rem 0 0', paddingLeft: '1rem', borderLeft: '2px solid var(--accent)' }}
        >
          "No lake, no play"
          <br />
          Lukas, on the release of CS2
        </blockquote>
      </div>
    </>
  )
}
