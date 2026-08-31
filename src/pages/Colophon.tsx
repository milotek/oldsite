import { site } from '../data/site'
import { PageHead } from '../components/PageHead'
import { Meta } from '../components/Meta'

export function Colophon() {
  return (
    <>
      <Meta title="Colophon" description="How this site is built." />
      <PageHead
        eyebrow="How this works"
        title="Colophon"
        lede="What the site is made of, and what changed from the version before it."
      />

      <div className="detail">
        <h2 className="entry__title" style={{ marginTop: '2rem' }}>
          Build
        </h2>
        <ul>
          <li>React and TypeScript, bundled by Vite.</li>
          <li>
            A single-page app on GitHub Pages. <code>vite build</code>, then the built{' '}
            <code>index.html</code> is copied to <code>404.html</code> so deep links resolve.
          </li>
          <li>
            Page titles use React 19's native <code>&lt;title&gt;</code> hoisting, so there is no
            helmet library and no second table of titles to keep in step with the routes.
          </li>
          <li>
            Projects, games and art are typed arrays in <code>src/data</code>. Adding work is
            adding an object, never a new page.
          </li>
          <li>Plain CSS with custom properties. No utility framework, no CSS-in-JS.</li>
          <li>Fonts, palette and the audio-reactive chrome carried over from the 2025 site.</li>
        </ul>

        <h2 className="entry__title" style={{ marginTop: '2.5rem' }}>
          Changed from the old site
        </h2>
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
            The Adobe PDF viewer SDK, and the client id hardcoded next to it, replaced with a plain{' '}
            <code>&lt;object&gt;</code>.
          </li>
          <li>
            Gallery alt text is now separate from the visible caption. The old markup used one
            string for both, so captions read like alt text.
          </li>
          <li>
            YouTube and SoundCloud embeds load on click rather than on page load, so a visit costs
            nothing to third parties.
          </li>
        </ul>

        <p className="eyebrow" style={{ marginTop: '2.5rem' }}>
          {__GIT_REV__} &middot; built {new Date(__BUILD_TIME__).toISOString().slice(0, 10)}
        </p>
      </div>
    </>
  )
}
