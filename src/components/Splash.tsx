import { useEffect, useState } from 'react'

const MESSAGES = [
  'no lake, no play',
  'built on a thinkpad',
  'now with 100% fewer marquees',
  'still nice at tetr.io',
  'the vault is mostly private, sorry',
  'ask me about surf physics',
  'compiled at least once',
  'de_dust2 in mat_fullbright',
]

/**
 * Rendered empty on the server and filled in after mount: picking at render
 * time would bake one message into every prerendered page and then mismatch
 * on hydration.
 */
export function Splash() {
  const [index, setIndex] = useState<number | null>(null)

  useEffect(() => {
    setIndex(Math.floor(Math.random() * MESSAGES.length))
  }, [])

  if (index === null) return <span className="splash" aria-hidden="true" />

  return (
    <button
      type="button"
      className="splash"
      title="click for another"
      onClick={() => setIndex((i) => ((i ?? 0) + 1) % MESSAGES.length)}
    >
      {MESSAGES[index]}
    </button>
  )
}
