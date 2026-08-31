import { Link } from 'react-router-dom'
import Icon from '../components/Icon'
import PageHead from '../components/PageHead'
import { site, socials } from '../data/site'

const CARDS = [
  { to: '/projects', title: 'projects', blurb: 'Lockyn, the AutoPet Feeder and EZcals.' },
  { to: '/games', title: 'games', blurb: 'A Godot EPQ, a Roblox roguelike and some C#.' },
  { to: '/cv', title: 'cv', blurb: 'The short version, and a PDF to take away.' },
  { to: '/art', title: 'art', blurb: 'Years of drawings, mostly made in Procreate.' },
  { to: '/misc', title: 'misc', blurb: 'A contribution graph and a track.' },
]

export default function Home() {
  return (
    <>
      <PageHead />

      <section className="hero">
        <div>
          <h1>{site.name}</h1>
          <p className="tagline">{site.tagline}</p>

          <ul className="socials">
            {socials.map((social) => (
              <li key={social.href}>
                <a href={social.href}>
                  <Icon name={social.icon} />
                  {social.label}
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div className="hero-banner">
          <img
            src="/img/under_construction.gif"
            alt='A hand-drawn stick figure next to two cogs and the words "under construction".'
            width={640}
            height={480}
          />
        </div>
      </section>

      <ul className="cards">
        {CARDS.map((card) => (
          <li key={card.to}>
            <Link to={card.to} className="card">
              <h2>{card.title}</h2>
              <p>{card.blurb}</p>
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}
