import PageHead from '../components/PageHead'
import { contributionGraph, soundcloudEmbed } from '../data/misc'
import { github } from '../data/site'

export default function Misc() {
  return (
    <>
      <PageHead title="misc" description="Odds and ends - a contribution graph and a track." />

      <div className="page-head">
        <h1>Misc</h1>
        <p className="lede">Odds and ends that do not belong anywhere else.</p>
      </div>

      <div className="entries">
        <section className="entry">
          <h2>Contributions</h2>
          <p>
            Generated nightly from my <a href={github}>GitHub profile</a>.
          </p>
          <img
            src={contributionGraph}
            alt="An isometric 3D rendering of my GitHub contribution graph."
            loading="lazy"
            style={{ marginTop: 'var(--s5)', width: '100%' }}
          />
        </section>

        <section className="entry">
          <h2>Something to listen to</h2>
          <div className="frame" style={{ aspectRatio: 'auto', height: '166px', marginTop: 'var(--s5)' }}>
            <iframe title="SoundCloud player" src={soundcloudEmbed} loading="lazy" allow="autoplay" />
          </div>
        </section>
      </div>
    </>
  )
}
