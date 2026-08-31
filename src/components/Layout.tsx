import { useEffect } from 'react'
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom'
import { nav, site } from '../data/site'
import Icon from './Icon'
import InteractiveGrid from './InteractiveGrid'

export default function Layout() {
  const { pathname } = useLocation()

  // A client-side route change keeps the old scroll offset, which lands you
  // halfway down the next page.
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return (
    <div className="shell">
      <InteractiveGrid />
      <a className="skip" href="#main">
        skip to content
      </a>

      <header className="header">
        <div className="wrap">
          <Link to="/" className="brand">
            milotek.dev
          </Link>
          <nav className="nav" aria-label="Main">
            {nav.map((link) => (
              <NavLink key={link.to} to={link.to} end={link.to === '/'}>
                <Icon name={link.icon} />
                {link.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main id="main" className="main">
        <div className="wrap">
          <Outlet />
        </div>
      </main>

      <footer className="footer">
        <div className="wrap">
          <span>{site.copyright}</span>
          <a href={`mailto:${site.email}`}>{site.email}</a>
        </div>
      </footer>
    </div>
  )
}
