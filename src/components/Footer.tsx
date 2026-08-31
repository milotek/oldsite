import { useEffect, useState } from 'react'
import { Link } from 'react-router'

/**
 * Version line, a couple of links that do not earn a place in the navbar, and
 * a splash message in the Minecraft sense: click it for a different one.
 *
 * The first render is fixed rather than random, so the initial paint is
 * deterministic; a real message is picked once on mount.
 */
const splashes = [
  'no lake, no play',
  'built on a train, probably',
  'CS2 sucks. Burn in heck.',
  'i like green apples',
  'ask me about the pet feeder',
  'Idiot Fart (see: other stuff)',
  'this footer took longer than the homepage',
  'godot, but only on weekends',
  'yes, the giraffe is mine',
  'shipping beats polishing, but only just',
  'sixteen years of drawings and one pet feeder',
  'hi lukas',
]

export function Footer() {
  const [splash, setSplash] = useState(splashes[0])

  useEffect(() => {
    setSplash(splashes[Math.floor(Math.random() * splashes.length)])
  }, [])

  const shuffle = () => {
    setSplash((current) => {
      let next = current
      while (next === current) next = splashes[Math.floor(Math.random() * splashes.length)]
      return next
    })
  }

  return (
    <footer className="footer subt">
      <div className="footer-links">
        <Link to="/misc" viewTransition>
          other stuff
        </Link>
        <Link to="/colophon" viewTransition>
          colophon
        </Link>
        <a href="mailto:milo@milotek.dev">email</a>
        <a href="https://github.com/milotek" rel="me noreferrer">
          github
        </a>
      </div>
      <span>
        milotek.dev ({__GIT_REV__}) &middot; built{' '}
        {new Date(__BUILD_TIME__).toISOString().slice(0, 10)}
      </span>
      <span
        className="splash"
        onClick={shuffle}
        onKeyDown={(event) => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault()
            shuffle()
          }
        }}
        role="button"
        tabIndex={0}
        title="click for another"
      >
        {splash}
      </span>
    </footer>
  )
}
