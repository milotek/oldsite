import { useEffect, useRef } from 'react'
import { NavLink, Link } from 'react-router'
import {
  HomeIcon,
  ProjectsIcon,
  GamesIcon,
  ArtIcon,
  BlogIcon,
  CvIcon,
} from './Icons'

const links = [
  { to: '/', label: 'home', Icon: HomeIcon, end: true },
  { to: '/projects', label: 'projects', Icon: ProjectsIcon },
  { to: '/games', label: 'games', Icon: GamesIcon },
  { to: '/art', label: 'art', Icon: ArtIcon },
  { to: '/blog', label: 'blog', Icon: BlogIcon },
  { to: '/cv', label: 'cv', Icon: CvIcon },
]

/**
 * The sticky top bar.
 *
 * The bar itself is transparent - each item carries its own pill, and the
 * blur strip behind them is what separates the bar from whatever is scrolling
 * underneath. `.scrolled` widens the gap between the two groups, so leaving
 * the top of the page is legible without a border appearing from nowhere.
 */
export function Navbar() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    const element = ref.current
    if (!element) return

    let queued = false
    const update = () => {
      queued = false
      element.classList.toggle('scrolled', window.scrollY > 0)
    }
    const onScroll = () => {
      if (queued) return
      queued = true
      requestAnimationFrame(update)
    }

    update()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header className="navbar" ref={ref}>
      {/* Five stacked blurs, each masked shorter than the last. One strong
          backdrop-filter gives a hard edge where it stops; this gives a
          gradient. */}
      <div className="top-blur" aria-hidden="true">
        <div className="top-blur-layer" style={{ '--blur': '1px', '--mid': '50%', '--end': '100%' } as React.CSSProperties} />
        <div className="top-blur-layer" style={{ '--blur': '2px', '--mid': '40%', '--end': '80%' } as React.CSSProperties} />
        <div className="top-blur-layer" style={{ '--blur': '3px', '--mid': '30%', '--end': '60%' } as React.CSSProperties} />
        <div className="top-blur-layer" style={{ '--blur': '6px', '--mid': '20%', '--end': '40%' } as React.CSSProperties} />
        <div className="top-blur-layer" style={{ '--blur': '10px', '--mid': '10%', '--end': '20%' } as React.CSSProperties} />
      </div>

      <Link to="/" className="site-title-link" viewTransition>
        <h1 className="site-title panel">
          <img className="site-title-pfp" src="/img/face.png" alt="" width={256} height={256} />
          <span>milotek.dev</span>
        </h1>
      </Link>

      <nav className="navbar-nav" aria-label="Primary">
        {links.map(({ to, label, Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            viewTransition
            className={({ isActive }) => `nav-link panel${isActive ? ' active' : ''}`}
          >
            <Icon />
            <span className="nav-name">{label}</span>
          </NavLink>
        ))}
      </nav>
    </header>
  )
}
