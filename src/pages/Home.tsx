import { useState } from 'react'
import { Link } from 'react-router'
import { site, socials, webButton, tracks } from '../data/site'
import { projects } from '../data/projects'
import { games } from '../data/games'
import { artworks } from '../data/art'
import { posts } from '../lib/blog'
import { Meta } from '../components/Meta'
import { ContactCard } from '../components/ContactCard'
import {
  GitHubIcon,
  LinkedInIcon,
  InstagramIcon,
  SpotifyIcon,
  MailIcon,
  ArrowRightIcon,
  MusicIcon,
} from '../components/Icons'

const icons = {
  github: <GitHubIcon />,
  linkedin: <LinkedInIcon />,
  instagram: <InstagramIcon />,
  spotify: <SpotifyIcon />,
} as const

export function Home() {
  const [copied, setCopied] = useState(false)
  const [player, setPlayer] = useState(false)
  const latest = posts[0]

  const copyButton = async () => {
    try {
      await navigator.clipboard.writeText(webButton.snippet)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 1800)
    } catch {
      // Clipboard access can be refused outright; the snippet is visible in
      // the page source either way, so there is nothing useful to report.
    }
  }

  return (
    <>
      <Meta />

      <section className="panel about">
        <div className="about-text">
          <h1>hi, i'm milo</h1>
          <p>
            Software engineer apprentice at <strong>Google</strong>, in London. Before that: A
            levels, an EPQ that turned into a Godot game, and a pet feeder built to my neighbours'
            specification.
          </p>
          <p>
            I mostly write TypeScript and Swift, and I am dangerous enough in C# and GDScript to
            finish things. Two of the apps here are commercial; the rest exist because I wanted
            them to.
          </p>
          <p>
            I also draw. There are sixteen years of that in the <Link to="/art">gallery</Link>,
            kept around because deleting it felt worse than publishing it.
          </p>
        </div>
        <img
          className="about-portrait"
          src="/img/face.png"
          alt="Portrait of Milo Tekchandani."
          width={256}
          height={256}
        />
      </section>

      <section className="home-grid">
        <h2 className="home-grid-heading">what's here</h2>
        <h2 className="home-grid-heading secondary">find me</h2>

        <div className="home-stack">
          <Link className="summary-card" to="/projects" viewTransition>
            <span className="summary-count">{projects.length}</span>
            <span className="summary-label">
              projects <ArrowRightIcon />
            </span>
            <span className="summary-desc">
              Lockyn, EZcals and a pet feeder with an oak finish.
            </span>
          </Link>
          <Link className="summary-card" to="/games" viewTransition>
            <span className="summary-count">{games.length}</span>
            <span className="summary-label">
              games <ArrowRightIcon />
            </span>
            <span className="summary-desc">Godot, Roblox, and three games in C#.</span>
          </Link>
          <Link className="summary-card" to="/art" viewTransition>
            <span className="summary-count">{artworks.length}</span>
            <span className="summary-label">
              artworks <ArrowRightIcon />
            </span>
            <span className="summary-desc">Mostly Procreate, on an iPad, over many years.</span>
          </Link>
        </div>

        <div className="home-socials">
          {socials.map((social) => (
            <ContactCard
              key={social.label}
              compact
              platform={social.label}
              handle={social.handle}
              href={social.href}
              icon={icons[social.label as keyof typeof icons]}
            />
          ))}
        </div>
      </section>

      {latest ? (
        <section className="home-section">
          <h2>latest post</h2>
          <Link className="latest-post panel" to={`/blog/${latest.slug}`} viewTransition>
            <h3>{latest.title}</h3>
            {latest.description ? <p className="post-desc">{latest.description}</p> : null}
            <time dateTime={latest.date}>{latest.date}</time>
          </Link>
        </section>
      ) : null}

      <section className="home-section">
        <h2>get in touch</h2>
        <div className="contact-grid">
          <ContactCard
            platform="email"
            handle={site.email}
            href={`mailto:${site.email}`}
            icon={<MailIcon />}
          />
          <ContactCard
            platform="github"
            handle="@milotek"
            href="https://github.com/milotek"
            icon={<GitHubIcon />}
          />
          <ContactCard
            platform="linkedin"
            handle="Milo Tekchandani"
            href="https://www.linkedin.com/in/milo-tekchandani-686602292/"
            icon={<LinkedInIcon />}
          />
        </div>
        <p className="subt">
          I like keeping my real self and my online self a bit apart, so this is where the
          oversharing stops. Thanks for visiting.
        </p>
      </section>

      <section className="panel buttons-section">
        <div className="button-mine">
          <button type="button" className="web-button" onClick={copyButton}>
            <img src={webButton.src} alt="milotek.dev" width={88} height={31} />
          </button>
          <span className="subt">
            {copied
              ? 'copied - paste it wherever you like.'
              : 'click to copy the HTML. hotlinking is fine, I will not move it.'}
          </span>
        </div>

        <div className="button-track">
          {player ? (
            <audio controls autoPlay src={tracks[0]} preload="none">
              Your browser cannot play this file.
            </audio>
          ) : (
            <button type="button" className="button" onClick={() => setPlayer(true)}>
              <MusicIcon />
              play the track from the old site
            </button>
          )}
        </div>
      </section>
    </>
  )
}
