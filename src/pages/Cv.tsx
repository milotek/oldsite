import { cvUrl, cvSource } from '../data/site'
import { Meta } from '../components/Meta'
import { PageHeader } from '../components/PageHeader'
import { CodeIcon, DownloadIcon } from '../components/Icons'

export function Cv() {
  return (
    <>
      <Meta title="cv" description="CV of Milo Tekchandani." />
      <PageHeader title="cv" lede="Edited in the profile repo, refreshed into this one on every deploy." />

      <div className="linkrow">
        <a className="button" href={cvUrl} download>
          <DownloadIcon />
          download the PDF
        </a>
        <a className="button" href={cvSource} rel="noreferrer">
          <CodeIcon />
          source repo
        </a>
      </div>

      {/* A plain <object>, not the Adobe viewer SDK the 2024 site loaded. That
          pulled a third-party bundle and shipped a hardcoded client id in the
          markup, to render a PDF every browser already renders - as long as it
          is served with the right content type, which is why this points at
          the local copy rather than at raw.githubusercontent.com. */}
      <object
        className="pdf panel"
        data={cvUrl}
        type="application/pdf"
        aria-label="CV of Milo Tekchandani"
      >
        <p>
          Your browser will not display the PDF inline.{' '}
          <a href={cvUrl} download>
            Download it instead.
          </a>
        </p>
      </object>
    </>
  )
}
