import { useState } from 'react'
import { useParams } from 'react-router'
import { games, getGame } from '../data/games'
import { Meta } from '../components/Meta'
import { PageHeader } from '../components/PageHeader'
import { Card } from '../components/Card'
import { LinkRow } from '../components/LinkRow'
import { PlayIcon } from '../components/Icons'
import { NotFound } from './NotFound'

const ordered = [...games].sort(
  (a, b) => Number(Boolean(b.featured)) - Number(Boolean(a.featured)),
)

export function Games() {
  return (
    <>
      <Meta title="games" description="Games made by Milo Tekchandani." />
      <PageHeader
        title="games"
        lede="Six months in Godot, a Roblox roguelike, and three games in C# with a 14 page evaluation."
      />
      <section className="card-grid">
        {ordered.map((game, index) => (
          <Card
            key={game.slug}
            to={`/games/${game.slug}`}
            title={game.title}
            blurb={game.blurb}
            year={game.year}
            thumb={game.thumb}
            featured={game.featured}
            eager={index < 2}
          />
        ))}
      </section>
    </>
  )
}

export function GameDetail() {
  const { slug } = useParams()
  const game = slug ? getGame(slug) : undefined
  const [playing, setPlaying] = useState(false)

  if (!game) return <NotFound />

  return (
    <>
      <Meta title={game.title} description={game.blurb} />

      <section className="panel detail-head">
        <h1>{game.title}</h1>
        <p className="lede">{game.description ?? game.blurb}</p>
        <div className="tech-row">
          <span className="badge">{game.year}</span>
          {game.tech.map((item) => (
            <span className="badge" key={item}>
              {item}
            </span>
          ))}
        </div>
        <LinkRow links={game.links} />
      </section>

      <section className="panel detail-body">
        <ul>
          {game.points.map((point) => (
            <li key={point}>{point}</li>
          ))}
        </ul>
      </section>

      {game.video ? (
        <div className="video-frame">
          {playing ? (
            <iframe
              src={`https://www.youtube-nocookie.com/embed/${game.video.id}?autoplay=1`}
              title={game.video.title}
              allow="accelerometer; autoplay; encrypted-media; picture-in-picture"
              allowFullScreen
            />
          ) : (
            // Loading on click rather than on render, so visiting the page
            // costs nothing to YouTube and nothing to whoever is reading it.
            <button type="button" className="video-poster" onClick={() => setPlaying(true)}>
              <PlayIcon />
              <span>play {game.video.title}</span>
            </button>
          )}
        </div>
      ) : null}

      {game.shots.length > 0 ? (
        <ul className="shots">
          {game.shots.map((shot) => (
            <li key={shot.src}>
              <figure>
                <img src={shot.src} alt={shot.alt} loading="lazy" />
                <figcaption>{shot.caption}</figcaption>
              </figure>
            </li>
          ))}
        </ul>
      ) : null}
    </>
  )
}
