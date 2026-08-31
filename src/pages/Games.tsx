import { useState } from 'react'
import { useParams } from 'react-router'
import { games } from '../data/games'
import { Entry } from '../components/Entry'
import { Detail } from '../components/Detail'
import { PageHead } from '../components/PageHead'
import { NotFound } from './NotFound'
import { Meta } from '../components/Meta'

export function Games() {
  return (
    <>
      <Meta title="Games" description="Games built in Godot, Roblox and C#." />
      <PageHead
        eyebrow="Work"
        title="Games"
        lede="Godot, Roblox and C#. One was coursework, one is a hobby, one is three games in a trenchcoat."
      />
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
    </>
  )
}

/**
 * Click-to-load rather than a bare <iframe>: an embed on mount pulls several
 * hundred KB of YouTube player and sets cookies for every visitor, including
 * the ones who never press play.
 */
function Video({ id, title }: { id: string; title: string }) {
  const [live, setLive] = useState(false)

  if (!live) {
    return (
      <button className="button" type="button" onClick={() => setLive(true)}>
        &#9654; Load the video from YouTube
      </button>
    )
  }

  return (
    <div className="embed">
      <iframe
        src={`https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`}
        title={title}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture"
        allowFullScreen
      />
    </div>
  )
}

export function GameDetail() {
  const { slug } = useParams()
  const game = games.find((item) => item.slug === slug)
  if (!game) return <NotFound />

  return (
    <Detail
      backTo="/games"
      backLabel="games"
      eyebrow="Game"
      title={game.title}
      blurb={game.blurb}
      year={game.year}
      tech={game.tech}
      points={game.points}
      links={game.links}
      shots={game.shots}
    >
      {game.video ? (
        <div className="linkrow">
          <Video id={game.video.id} title={game.video.title} />
        </div>
      ) : null}
    </Detail>
  )
}
