import { useEffect, useRef, useState } from 'react'
import type { Artwork } from '../data/art'

/**
 * Uses a native <dialog>, which brings the modal focus trap, the Escape
 * handler and the backdrop with it - none of which are worth reimplementing.
 */
export default function Gallery({ items }: { items: Artwork[] }) {
  const [open, setOpen] = useState<Artwork | null>(null)
  const dialog = useRef<HTMLDialogElement>(null)

  useEffect(() => {
    const el = dialog.current
    if (!el) return
    if (open && !el.open) el.showModal()
    if (!open && el.open) el.close()
  }, [open])

  return (
    <>
      <ul className="gallery">
        {items.map((item) => (
          <li key={item.src}>
            <button type="button" className="tile" onClick={() => setOpen(item)}>
              <figure>
                <img src={item.src} alt={item.alt} loading="lazy" />
                <figcaption>{item.caption}</figcaption>
              </figure>
            </button>
          </li>
        ))}
      </ul>

      <dialog ref={dialog} className="lightbox" onClose={() => setOpen(null)}>
        {open && (
          <figure>
            <form method="dialog">
              <button type="submit" aria-label="Close">
                close
              </button>
            </form>
            <img src={open.full} alt={open.alt} />
            <figcaption>{open.caption}</figcaption>
          </figure>
        )}
      </dialog>
    </>
  )
}
