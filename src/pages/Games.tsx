import Entry from '../components/Entry'
import PageHead from '../components/PageHead'
import { games, gamesIntro } from '../data/games'

export default function Games() {
  return (
    <>
      <PageHead title="games" description={gamesIntro} />

      <div className="page-head">
        <h1>Games</h1>
        <p className="lede">{gamesIntro}</p>
      </div>

      <div className="entries">
        {games.map((game) => (
          <Entry key={game.slug} entry={game} />
        ))}
      </div>
    </>
  )
}
