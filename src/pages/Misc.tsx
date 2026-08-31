import { useState } from 'react'
import { comparison, soundcloudTrackId } from '../data/misc'
import { PageHead } from '../components/PageHead'
import { Meta } from '../components/Meta'

export function Misc() {
  const [player, setPlayer] = useState(false)

  return (
    <>
      <Meta title="Other stuff" description="The bits that do not belong on a portfolio." />
      <PageHead
        eyebrow="Other stuff"
        title="Other stuff"
        lede="The bits that do not belong on a portfolio, kept because taking them off would make this a worse website."
      />

      <section className="section" style={{ marginTop: 0 }}>
        <div className="section__head">
          <h2>Me versus Lukas</h2>
          <span className="eyebrow" style={{ margin: 0 }}>
            {comparison.caption}
          </span>
        </div>

        <div className="scroller">
          <table className="table">
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
      </section>

      <section className="section">
        <div className="section__head">
          <h2>A track</h2>
        </div>
        {player ? (
          <iframe
            title="SoundCloud player"
            width="100%"
            height="166"
            style={{ border: '1px solid var(--border)' }}
            allow="autoplay"
            src={`https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/${soundcloudTrackId}&auto_play=true&visual=false`}
          />
        ) : (
          <button className="button" type="button" onClick={() => setPlayer(true)}>
            &#9654; Load the SoundCloud player
          </button>
        )}
      </section>
    </>
  )
}
