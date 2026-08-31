import { Link } from 'react-router'
import { notes } from '../lib/content'

export function Notes() {
  return (
    <div className="stack">
      <header>
        <p className="eyebrow">notes</p>
        <h1>Notes</h1>
        <p className="lede">
          A slice of my Obsidian vault. Only notes explicitly marked{' '}
          <code>publish: true</code> appear here; everything else stays private.
        </p>
      </header>

      {notes.length === 0 ? (
        <p className="lede">Nothing published yet.</p>
      ) : (
        <ul className="card-list">
          {notes.map((note) => (
            <li key={note.slug} className="card">
              <h3>
                <Link to={`/notes/${note.slug}`}>{note.title}</Link>
              </h3>
              {note.description && <p>{note.description}</p>}
              <div className="meta">
                <span>{note.wordCount} words</span>
                {note.backlinks.length > 0 && <span>{note.backlinks.length} backlinks</span>}
                {note.tags.map((tag) => (
                  <span key={tag} className="tag">
                    {tag}
                  </span>
                ))}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
