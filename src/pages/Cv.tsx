import { cvUrl, site } from '../data/site'

/**
 * The previous site embedded the PDF through Adobe's viewer SDK with a
 * hardcoded client id. A plain <object> renders in every current browser's
 * built-in viewer, needs no third party script, and degrades to a download
 * link where it does not.
 */
export function Cv() {
  return (
    <div className="stack">
      <header>
        <p className="eyebrow">cv</p>
        <h1>Résumé</h1>
        <p className="lede">
          <a href={cvUrl} rel="noopener">
            Download the PDF
          </a>{' '}
          or read it below.
        </p>
      </header>

      <object data={cvUrl} type="application/pdf" width="100%" height="900">
        <p>
          Your browser will not display the PDF inline.{' '}
          <a href={cvUrl} rel="noopener">
            Download {site.name}&rsquo;s CV
          </a>
          .
        </p>
      </object>
    </div>
  )
}
