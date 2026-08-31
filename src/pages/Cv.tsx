import PageHead from '../components/PageHead'
import { cv } from '../data/misc'

export default function Cv() {
  return (
    <>
      <PageHead title="cv" description="Milo Tekchandani's CV." />

      <div className="page-head">
        <h1>CV</h1>
        <p className="lede">
          <a href={cv.file} download>
            Download the PDF
          </a>{' '}
          or read the <a href={cv.source}>copy on GitHub</a>.
        </p>
      </div>

      {/* <object> degrades to its children where no PDF viewer exists, which is
          most mobile browsers - so the fallback link is the whole point. */}
      <object className="pdf" data={cv.file} type="application/pdf" aria-label="CV">
        <p className="muted" style={{ padding: 'var(--s5)' }}>
          Your browser will not display PDFs inline.{' '}
          <a href={cv.file} download>
            Download the CV
          </a>{' '}
          instead.
        </p>
      </object>
    </>
  )
}
