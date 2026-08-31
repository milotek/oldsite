import { useCallback, useEffect, useRef, useState } from 'react'
import { artworks } from '../data/art'

/**
 * Thumbnails open the full-resolution file in a native <dialog>.
 *
 * <dialog showModal> is doing real work here: it supplies the focus trap, the
 * inert background, the Escape handler and the backdrop for free. Hand-rolling
 * a modal to get the same behaviour is how accessible galleries stop being
 * accessible.
 */
export function Gallery() {
  const [open, setOpen] = useState<number | null>(null)
  const dialogRef = useRef<HTMLDialogElement>(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    if (open === null) dialog.close()
    else if (!dialog.open) dialog.showModal()
  }, [open])

  const step = useCallback((delta: number) => {
    setOpen((current) =>
      current === null ? null : (current + delta + artworks.length) % artworks.length,
    )
  }, [])

  useEffect(() => {
    if (open === null) return
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'ArrowRight') step(1)
      if (event.key === 'ArrowLeft') step(-1)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, step])

  const current = open === null ? null : artworks[open]

  return (
    <>
      <ul className="gallery">
        {artworks.map((art, index) => (
          <li key={art.thumb}>
            <figure>
              <button type="button" onClick={() => setOpen(index)}>
                <img src={art.thumb} alt={art.alt} loading="lazy" />
              </button>
              <figcaption>{art.caption}</figcaption>
            </figure>
          </li>
        ))}
      </ul>

      <dialog
        className="lightbox"
        ref={dialogRef}
        onClose={() => setOpen(null)}
        onClick={(event) => {
          // Clicking the backdrop lands on the dialog itself, never a child.
          if (event.target === dialogRef.current) setOpen(null)
        }}
      >
        {current ? (
          <>
            <button className="lightbox__btn lightbox__btn--close" type="button" onClick={() => setOpen(null)}>
              close
            </button>
            <img src={current.full} alt={current.alt} />
            <div className="lightbox__bar">
              <button className="lightbox__btn" type="button" onClick={() => step(-1)}>
                &larr;
              </button>
              <span>
                {String((open ?? 0) + 1).padStart(2, '0')} / {artworks.length} &middot;{' '}
                {current.caption}
              </span>
              <button className="lightbox__btn" type="button" onClick={() => step(1)}>
                &rarr;
              </button>
            </div>
          </>
        ) : null}
      </dialog>
    </>
  )
}
