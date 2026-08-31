import { ArtGallery } from '../components/ArtGallery'
import { artworks } from '../data/art'

export function Art() {
  return (
    <div className="stack">
      <header>
        <p className="eyebrow">art</p>
        <h1>Artwork</h1>
        <p className="lede">
          Made over the years, mostly in{' '}
          <a href="https://procreate.com/procreate" rel="noopener">
            Procreate
          </a>{' '}
          on an iPad with an Apple Pencil.
        </p>
      </header>
      <ArtGallery items={artworks} />
    </div>
  )
}
