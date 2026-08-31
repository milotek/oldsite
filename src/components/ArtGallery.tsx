import { useEffect, useRef, useState } from 'react'
import type { Artwork } from '../data/art'

/**
 * Uses <dialog> rather than a hand-rolled overlay so focus trapping, Escape
 * handling and inertness of the background come from the platform.
 */
export function ArtGallery({ items }: { items: Artwork[] }) {
  const [active, setActive] = useState<number | null>(null)
  const dialogRef = useRef<HTMLDialogElement>(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    if (active !== null && !dialog.open) dialog.showModal()
    if (active === null && dialog.open) dialog.close()
  }, [active])

  const current = active === null ? null : items[active]

  function step(delta: number) {
    setActive((i) => (i === null ? null : (i + delta + items.length) % items.length))
  }

  return (
    <>
      <ul className="gallery">
        {items.map((art, i) => (
          <li key={art.thumb}>
            <button
              type="button"
              className="gallery__btn"
              onClick={() => setActive(i)}
              aria-label={`Open full size: ${art.caption}`}
            >
              <img src={art.thumb} alt={art.alt} loading="lazy" decoding="async" />
              <span className="gallery__caption">{art.caption}</span>
            </button>
          </li>
        ))}
      </ul>

      <dialog
        ref={dialogRef}
        className="lightbox"
        onClose={() => setActive(null)}
        onClick={(e) => {
          // Clicks land on the dialog itself only when they hit the backdrop.
          if (e.target === dialogRef.current) setActive(null)
        }}
        onKeyDown={(e) => {
          if (e.key === 'ArrowRight') step(1)
          if (e.key === 'ArrowLeft') step(-1)
        }}
      >
        {current && (
          <>
            <img src={current.full} alt={current.alt} />
            <div className="lightbox__bar">
              <span>{current.caption}</span>
              <span>
                <button type="button" className="lightbox__close" onClick={() => step(-1)}>
                  prev
                </button>{' '}
                <button type="button" className="lightbox__close" onClick={() => step(1)}>
                  next
                </button>{' '}
                <button type="button" className="lightbox__close" onClick={() => setActive(null)}>
                  close
                </button>
              </span>
            </div>
          </>
        )}
      </dialog>
    </>
  )
}
