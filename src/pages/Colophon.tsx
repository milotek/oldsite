import { site } from '../data/site'
import { Meta } from '../components/Meta'
import { PageHeader } from '../components/PageHeader'

export function Colophon() {
  return (
    <>
      <Meta title="colophon" description="How this site is built." />
      <PageHeader title="colophon" lede="What the site is made of, and what changed on the way here." />

      <section className="panel detail-body">
        <h2>build</h2>
        <ul>
          <li>React and TypeScript, bundled by Vite. No UI framework, no CSS-in-JS.</li>
          <li>
            A single-page app on GitHub Pages. <code>vite build</code>, then the built{' '}
            <code>index.html</code> is copied to <code>404.html</code> so deep links resolve.
          </li>
          <li>
            Titles use React 19's native <code>&lt;title&gt;</code> hoisting, so there is no helmet
            library and no second table of titles to keep in step with the routes.
          </li>
          <li>
            Projects, games and art are typed arrays in <code>src/data</code>. Adding work means
            adding an object, never a new page.
          </li>
          <li>
            Blog posts are Markdown in <code>src/blog</code>, named{' '}
            <code>YYYY-MM-DD-slug.md</code>. Files prefixed <code>draft-</code> are excluded from
            the bundle rather than hidden after the fact.
          </li>
          <li>
            Icons are drawn by hand on a 24x24 grid, so nothing here fetches a webfont from a
            third party. Brand marks come from simple-icons.
          </li>
          <li>
            The background grid is a canvas: the dim lattice is rasterised once per resize, and
            only lit cells are stroked per frame.
          </li>
        </ul>

        <h2>colours</h2>
        <ul>
          <li>
            Catppuccin Mocha, with <code>#ffbdbd</code> in place of maroon as the accent.
          </li>
          <li>
            The surface and overlay scales are extended past what Catppuccin ships, because a
            layout built from stacked bordered panels needs more steps than three.
          </li>
        </ul>

        <h2>changed from the old site</h2>
        <ul>
          <li>The phone number is gone. It was published in plain text on the landing page.</li>
          <li>
            <code>milo@milotek.com</code> corrected to <code>{site.email}</code>.
          </li>
          <li>
            Links repointed from <code>pixeljammed</code> to <code>milotek</code>, and{' '}
            <code>HRSFC-Programs</code> to <code>Practice.NET</code>. The old ones only resolved
            through GitHub's rename redirects.
          </li>
          <li>Google Analytics removed.</li>
          <li>
            The Adobe PDF viewer SDK, and the client id hardcoded next to it, replaced with a
            plain <code>&lt;object&gt;</code>.
          </li>
          <li>
            Gallery alt text is separate from the visible caption. The old markup used one string
            for both, so every caption read like alt text.
          </li>
          <li>
            YouTube, SoundCloud and audio embeds load on click, so a visit costs nothing to third
            parties.
          </li>
        </ul>

        <h2>credit</h2>
        <p>
          The design is a deliberate homage to{' '}
          <a href="https://bomberfish.ca" rel="noreferrer">
            bomberfish.ca
          </a>
          , whose source is public.
        </p>

        <p className="subt">
          {__GIT_REV__} &middot; built {new Date(__BUILD_TIME__).toISOString().slice(0, 10)}
        </p>
      </section>
    </>
  )
}
