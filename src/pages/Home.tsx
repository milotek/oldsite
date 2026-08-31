import { Link } from 'react-router-dom'
import Icon from '../components/Icon'
import PageHead from '../components/PageHead'
import { nav, site, socials } from '../data/site'

const BLURBS: Record<string, string> = {
  '/projects': 'Lockyn, the AutoPet Feeder and EZcals.',
  '/games': 'A Godot EPQ, a Roblox roguelike and some C#.',
  '/cv': 'The short version, and a PDF to take away.',
  '/art': 'Years of drawings, mostly made in Procreate.',
  '/misc': 'A contribution graph and a track.',
}

export default function Home() {
  return (
    <>
      <PageHead />

      <section className="hero">
        <div>
          <h1>
            <span className="wave">👋</span> {site.name}
          </h1>
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
        {nav
          .filter((link) => link.to !== '/')
          .map((link) => (
            <li key={link.to}>
              <Link to={link.to} className="card">
                <h2>{link.label}</h2>
                <p>{BLURBS[link.to]}</p>
              </Link>
            </li>
          ))}
      </ul>
    </>
  )
}
