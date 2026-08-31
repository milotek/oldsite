import { useState } from 'react'
import { comparison, soundcloudTrackId, quote } from '../data/misc'
import { Meta } from '../components/Meta'
import { PageHeader } from '../components/PageHeader'
import { PlayIcon } from '../components/Icons'

export function Misc() {
  const [player, setPlayer] = useState(false)

  return (
    <>
      <Meta title="other stuff" description="The bits that do not belong on a portfolio." />
      <PageHeader
        title="other stuff"
        lede="The parts that do not belong on a portfolio, kept because taking them off would make this a worse website."
      />

      <section className="panel">
        <h2>me versus Lukas</h2>
        <p className="subt">{comparison.caption}</p>
        <div className="scroller">
          <table>
            <thead>
              <tr>
                {comparison.columns.map((column, index) => (
                  <th key={index} scope="col">
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {comparison.rows.map((row) => (
                <tr key={row[0]}>
                  <th scope="row">{row[0]}</th>
                  <td>{row[1]}</td>
                  <td>{row[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <blockquote>
          {quote.text}
          <br />
          <span className="subt">{quote.attribution}</span>
        </blockquote>
      </section>

      <section className="panel" style={{ marginTop: '1rem' }}>
        <h2>a track</h2>
        {player ? (
          <iframe
            title="SoundCloud player"
            width="100%"
            height="166"
            style={{ border: '1px solid var(--surface2)' }}
            allow="autoplay"
            src={`https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/${soundcloudTrackId}&auto_play=true&visual=false`}
          />
        ) : (
          // Loaded on click, so visiting this page costs nothing to SoundCloud.
          <button type="button" className="button" onClick={() => setPlayer(true)}>
            <PlayIcon />
            load the SoundCloud player
          </button>
        )}
      </section>
    </>
  )
}
