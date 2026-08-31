import { Link } from 'react-router'
import { marquee } from '../data/misc'
import { PageHead } from '../components/PageHead'
import { Meta } from '../components/Meta'

/**
 * The old landing page was a wall of scrolling copypasta behind a photo. It is
 * funny exactly once, which makes it a bad front door and a good 404.
 */
export function NotFound() {
  return (
    <>
      <Meta title="Not found" description="Page not found." />
      <div className="wall" aria-hidden="true">
        {marquee.map((line) => (
          <p key={line.slice(0, 24)}>
            {line} {line}
          </p>
        ))}
      </div>

      <PageHead
        eyebrow="404"
        title="There is nothing here"
        lede="There used to be an actual website here, but I blew it up. This page is where the old one went."
      />

      <div className="linkrow" style={{ marginTop: 0 }}>
        <Link className="button" to="/" viewTransition>
          Back to the index
        </Link>
      </div>
    </>
  )
}
