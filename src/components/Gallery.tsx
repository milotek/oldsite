import { useEffect, useRef, useState } from 'react'
import type { Artwork } from '../data/art'

/**
 * The artwork grid and its viewer.
 *
 * The viewer is a real <dialog>, so Escape, focus trapping and the top layer
 * are the browser's job rather than ours. Full-size files are only requested
 * once something is opened; the grid itself loads thumbnails.
 */
export function Gallery({ items }: { items: Artwork[] }) {
  const [open, setOpen] = useState<Artwork | null>(null)
  const dialogRef = useRef<HTMLDialogElement>(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    if (open && !dialog.open) dialog.showModal()
    if (!open && dialog.open) dialog.close()
  }, [open])

  return (
    <>
      <ul className="gallery">
        {items.map((item) => (
          <li key={item.thumb}>
            <a
              className="gallery-item"
              href={item.full}
              onClick={(event) => {
                // Modified clicks and middle clicks should still open the file
                // directly, which is what the href is there for.
                if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return
                event.preventDefault()
                setOpen(item)
              }}
            >
              <figure>
                <img src={item.thumb} alt={item.alt} loading="lazy" />
                <figcaption>{item.caption}</figcaption>
              </figure>
            </a>
          </li>
        ))}
      </ul>

      <dialog className="lightbox" ref={dialogRef} onClose={() => setOpen(null)}>
        {open ? (
          <>
            <img src={open.full} alt={open.alt} />
            <div className="lightbox-bar">
              <span>{open.caption}</span>
              <button type="button" className="button" onClick={() => setOpen(null)}>
                close
              </button>
            </div>
          </>
        ) : null}
      </dialog>
    </>
  )
}
