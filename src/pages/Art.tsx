import { artworks } from '../data/art'
import { Gallery } from '../components/Gallery'
import { PageHead } from '../components/PageHead'
import { Meta } from '../components/Meta'

export function Art() {
  return (
    <>
      <Meta title="Art" description="Artwork made in Procreate over the years." />
      <PageHead
        eyebrow="Not code"
        title="Art"
        lede={
          <>
            {artworks.length} pieces from over the years, mostly drawn in{' '}
            <a href="https://procreate.com/procreate" rel="noreferrer">
              Procreate
            </a>{' '}
            on an iPad with an Apple Pencil. Click one for the full resolution file.
          </>
        }
      />
      <Gallery />
    </>
  )
}
