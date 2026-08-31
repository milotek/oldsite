import { Link } from 'react-router'
import { projects } from '../data/projects'
import { games } from '../data/games'
import { artworks } from '../data/art'
import { Entry } from '../components/Entry'
import { Meta } from '../components/Meta'

export function Home() {
  return (
    <>
      <Meta />
      <section className="hero">
        <div>
          <p className="eyebrow">Milo Tekchandani</p>
          <h1>
            I make <em>things</em>.
          </h1>
          <div className="hero__text">
            <p>
              Mostly software. Occasionally out of wood and a Raspberry Pi.
            </p>
            <p>
              <strong>Software engineer apprentice at Google, in London.</strong> Before that: A
              levels, an EPQ that turned into a Godot game, and a pet feeder built to a
              neighbour's spec.
            </p>
            <p>
              This is where the work lives. Commercial apps, hobby games, and a decade of drawings
              I keep around because deleting them felt worse.
            </p>
          </div>
        </div>
        <img
          className="hero__portrait"
          src="/img/face.png"
          alt="Portrait of Milo Tekchandani."
          width={320}
          height={320}
        />
      </section>

      <section className="section">
        <div className="section__head">
          <h2>Projects</h2>
          <Link to="/projects" viewTransition>
            all {projects.length} &rarr;
          </Link>
        </div>
        <ul className="entries">
          {projects.map((project, index) => (
            <Entry
              key={project.slug}
              index={index}
              to={`/projects/${project.slug}`}
              title={project.title}
              blurb={project.blurb}
              year={project.year}
              tech={project.tech}
              status={project.status}
            />
          ))}
        </ul>
      </section>

      <section className="section">
        <div className="section__head">
          <h2>Games</h2>
          <Link to="/games" viewTransition>
            all {games.length} &rarr;
          </Link>
        </div>
        <ul className="entries">
          {games.map((game, index) => (
            <Entry
              key={game.slug}
              index={index}
              to={`/games/${game.slug}`}
              title={game.title}
              blurb={game.blurb}
              year={game.year}
              tech={game.tech}
            />
          ))}
        </ul>
      </section>

      <section className="section">
        <div className="section__head">
          <h2>Art</h2>
          <Link to="/art" viewTransition>
            all {artworks.length} &rarr;
          </Link>
        </div>
        <ul className="shots">
          {artworks.slice(0, 4).map((art) => (
            <li key={art.thumb}>
              <figure>
                <img src={art.thumb} alt={art.alt} loading="lazy" />
                <figcaption>{art.caption}</figcaption>
              </figure>
            </li>
          ))}
        </ul>
      </section>
    </>
  )
}
