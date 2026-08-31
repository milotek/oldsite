import { artworks } from '../data/art'
import { Meta } from '../components/Meta'
import { PageHeader } from '../components/PageHeader'
import { Gallery } from '../components/Gallery'

export function Art() {
  return (
    <>
      <Meta title="art" description="Artwork by Milo Tekchandani." />
      <PageHeader
        title="art"
        lede="Mostly Procreate on an iPad Pro with an Apple Pencil. A few in Pixelmator."
      />
      <Gallery items={artworks} />
    </>
  )
}
