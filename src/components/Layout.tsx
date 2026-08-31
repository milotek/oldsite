import { NavLink, Link, Outlet, useLocation } from 'react-router'
import { useEffect } from 'react'
import { site } from '../data/site'
import { ThemeToggle } from './ThemeToggle'
import { Splash } from './Splash'
import { Oneko } from './Oneko'

const NAV = [
  { to: '/projects', label: 'projects' },
  { to: '/games', label: 'games' },
  { to: '/art', label: 'art' },
  { to: '/blog', label: 'blog' },
  { to: '/notes', label: 'notes' },
  { to: '/cv', label: 'cv' },
]

export function Layout() {
  const { pathname } = useLocation()

  // Client-side navigation leaves the scroll position where it was; a fresh
  // page should start at the top the way a document navigation would.
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return (
    <div className="shell">
      <a className="skip-link" href="#main">
        Skip to content
      </a>

      <header className="nav">
        <nav className="wrap nav__inner" aria-label="Primary">
          <Link to="/" className="nav__brand" viewTransition>
            milotek.dev
          </Link>
          {NAV.map((item) => (
            <NavLink key={item.to} to={item.to} className="nav__link" viewTransition>
              {item.label}
            </NavLink>
          ))}
          <ThemeToggle />
        </nav>
      </header>

      <main id="main" className="wrap">
        <Outlet />
      </main>

      <footer className="footer">
        <div className="wrap footer__row">
          <span>
            {site.name} &middot; <Link to="/siteinfo">v{__APP_VERSION__}</Link> (
            {__GIT_REV__})
          </span>
          <Splash />
        </div>
      </footer>

      <Oneko />
    </div>
  )
}
