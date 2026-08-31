import type { Entry as EntryData } from '../data/types'

export default function Entry({ entry }: { entry: EntryData }) {
  const shotClass = entry.shotShape ? `figures ${entry.shotShape}` : 'figures'

  return (
    <article className="entry" id={entry.slug}>
      <div className="entry-head">
        <h2>{entry.title}</h2>
        {entry.status && <span className="status">{entry.status}</span>}
      </div>

      <p>{entry.summary}</p>

      <ul className="points">
        {entry.points.map((point) => (
          <li key={point}>{point}</li>
        ))}
      </ul>

      {entry.links && (
        <ul className="entry-links">
          {entry.links.map((link) => (
            <li key={link.href}>
              <a href={link.href}>{link.label}</a>
            </li>
          ))}
        </ul>
      )}

      {entry.video && (
        <div className="frame">
          <iframe
            title={entry.video.title}
            src={`https://www.youtube-nocookie.com/embed/${entry.video.youtubeId}?rel=0`}
            allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            loading="lazy"
          />
        </div>
      )}

      {entry.shots && (
        <ul className={shotClass}>
          {entry.shots.map((shot) => (
            <li key={shot.src}>
              <figure>
                <img src={shot.src} alt={shot.alt} loading="lazy" />
                <figcaption>{shot.caption}</figcaption>
              </figure>
            </li>
          ))}
        </ul>
      )}
    </article>
  )
}
