import Gallery from '../components/Gallery'
import PageHead from '../components/PageHead'
import { artIntro, artwork } from '../data/art'

export default function Art() {
  return (
    <>
      <PageHead title="art" description={artIntro} />

      <div className="page-head">
        <h1>Art</h1>
        <p className="lede">{artIntro}</p>
      </div>

      <Gallery items={artwork} />
    </>
  )
}
