import { cvUrl } from '../data/site'
import { PageHead } from '../components/PageHead'
import { Meta } from '../components/Meta'

export function Cv() {
  return (
    <>
      <Meta title="CV" description="CV of Milo Tekchandani." />
      <PageHead
        eyebrow="Paperwork"
        title="CV"
        lede="Kept in the profile repo so it only ever exists in one place."
      />

      <div className="linkrow" style={{ marginTop: 0, marginBottom: '2rem' }}>
        <a className="button" href={cvUrl} rel="noreferrer">
          Download the PDF
        </a>
      </div>

      {/* A plain <object> rather than the Adobe viewer SDK the old site loaded.
          That pulled a third-party bundle and shipped a hardcoded client id in
          the markup, to render a PDF that every browser already renders. */}
      <object className="pdf" data={cvUrl} type="application/pdf" aria-label="CV of Milo Tekchandani">
        <p>
          Your browser will not display the PDF inline.{' '}
          <a href={cvUrl} rel="noreferrer">
            Download it instead.
          </a>
        </p>
      </object>
    </>
  )
}
