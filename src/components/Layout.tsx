import { NavLink, Outlet, useLocation } from 'react-router'
import { useEffect } from 'react'
import { site, socials } from '../data/site'
import { Chrome } from './Chrome'

const NAV = [
  { to: '/', label: 'index', end: true },
  { to: '/projects', label: 'projects' },
  { to: '/games', label: 'games' },
  { to: '/art', label: 'art' },
  { to: '/cv', label: 'cv' },
  { to: '/misc', label: 'other stuff' },
  { to: '/contact', label: 'contact' },
]

export function Layout() {
  const { pathname } = useLocation()

  // A client-side navigation keeps the scroll position of the page it left,
  // which lands the visitor halfway down the next one.
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return (
    <div className="shell">
      <a className="skip" href="#main">
        Skip to content
      </a>
      <div className="spectrum" aria-hidden="true" />

      <header className="rail">
        <div>
          <NavLink to="/" className="rail__mark">
            milo tek
            <span>chandani</span>
          </NavLink>
          <p className="rail__role">{site.role}</p>
        </div>

        <nav aria-label="Primary">
          <ul className="rail__nav">
            {NAV.map((item, index) => (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  end={item.end}
                  viewTransition
                  data-index={String(index + 1).padStart(2, '0')}
                >
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        <div className="rail__foot">
          <ul className="rail__socials">
            {socials.map((social) => (
              <li key={social.label}>
                <a href={social.href} rel="me noreferrer">
                  {social.label.toLowerCase()}
                </a>
              </li>
            ))}
          </ul>
          <p className="rail__legal">
            {site.url.replace('https://', '')}
            <br />
            <NavLink to="/colophon" viewTransition>
              colophon
            </NavLink>
          </p>
        </div>
      </header>

      <main className="main" id="main">
        <Outlet />
      </main>

      <Chrome />
    </div>
  )
}
