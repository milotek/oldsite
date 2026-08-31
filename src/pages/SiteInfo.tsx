import { docs } from '../lib/content'
import { artworks } from '../data/art'
import { projects } from '../data/projects'
import { games } from '../data/games'

export function SiteInfo() {
  return (
    <div className="stack">
      <header>
        <p className="eyebrow">siteinfo</p>
        <h1>About this site</h1>
      </header>

      <ul className="card-list">
        <li className="card">
          <h3>Build</h3>
          <div className="meta">
            <span>v{__APP_VERSION__}</span>
            <span>commit {__GIT_REV__}</span>
            <span>built {new Date(__BUILD_TIME__).toISOString().replace('T', ' ').slice(0, 16)}</span>
          </div>
        </li>
        <li className="card">
          <h3>Stack</h3>
          <p>
            React 19 and Vite 8, routed with react-router 8, prerendered to static HTML by a
            script in <code>scripts/prerender.ts</code>. No server at runtime.
          </p>
        </li>
        <li className="card">
          <h3>Content</h3>
          <div className="meta">
            <span>{docs.filter((d) => d.kind === 'post').length} posts</span>
            <span>{docs.filter((d) => d.kind === 'note').length} notes</span>
            <span>{projects.length} projects</span>
            <span>{games.length} games</span>
            <span>{artworks.length} artworks</span>
          </div>
          <p>
            Posts and notes are generated from an Obsidian vault by{' '}
            <code>scripts/build-vault.ts</code>, which publishes only notes whose frontmatter
            says <code>publish: true</code>.
          </p>
        </li>
      </ul>
    </div>
  )
}
