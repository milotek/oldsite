import { useEffect, useRef } from 'react'

/**
 * A cursor-following cat, after the classic oneko.
 *
 * The original ships a 32x32 GIF sprite sheet; this draws the cat in SVG so
 * there is no binary asset to keep in sync and it stays crisp on any display.
 * The chase behaviour is the interesting part and is kept faithful: the cat
 * only moves once the cursor is far enough away, runs at a fixed speed rather
 * than easing (so it visibly falls behind fast movement), and sits down after
 * a period of stillness.
 *
 * Positioning is written straight to the DOM rather than through state. At
 * 60fps a setState per frame would re-render the whole subtree for a value
 * only this element reads.
 */
const SPEED = 10 // px per frame
const IDLE_DISTANCE = 48 // don't crowd the cursor
const SIT_AFTER_MS = 5000

export function Oneko() {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    const el = ref.current
    if (!el) return

    let catX = window.innerWidth / 2
    let catY = window.innerHeight / 2
    let mouseX = catX
    let mouseY = catY
    let frame = 0
    let lastMoved = performance.now()
    let raf = 0

    function onMove(event: MouseEvent) {
      mouseX = event.clientX
      mouseY = event.clientY
    }

    function tick(now: number) {
      const dx = mouseX - catX
      const dy = mouseY - catY
      const distance = Math.hypot(dx, dy)

      if (distance > IDLE_DISTANCE) {
        catX += (dx / distance) * Math.min(SPEED, distance - IDLE_DISTANCE)
        catY += (dy / distance) * Math.min(SPEED, distance - IDLE_DISTANCE)
        lastMoved = now
        frame += 1
      }

      const running = now - lastMoved < 100
      const sitting = now - lastMoved > SIT_AFTER_MS

      el!.style.transform = `translate3d(${Math.round(catX - 16)}px, ${Math.round(catY - 16)}px, 0)`
      el!.dataset.state = sitting ? 'sit' : running ? 'run' : 'idle'
      // Face the direction of travel; the drawing points right by default.
      el!.dataset.flip = dx < -1 ? 'true' : dx > 1 ? 'false' : (el!.dataset.flip ?? 'false')
      el!.dataset.step = String(Math.floor(frame / 4) % 2)

      raf = requestAnimationFrame(tick)
    }

    window.addEventListener('mousemove', onMove, { passive: true })
    raf = requestAnimationFrame(tick)

    return () => {
      window.removeEventListener('mousemove', onMove)
      cancelAnimationFrame(raf)
    }
  }, [])

  return (
    <div id="oneko" ref={ref} aria-hidden="true">
      <svg viewBox="0 0 32 32" width="32" height="32" shapeRendering="crispEdges">
        <g className="oneko__body">
          <path
            d="M8 12h2v-3h2v3h8v-3h2v3h2v10H8z"
            fill="var(--oneko-fur, #d8d8d8)"
            stroke="var(--oneko-line, #2a2a35)"
            strokeWidth="1"
          />
          <circle cx="13" cy="16" r="1.2" fill="var(--oneko-line, #2a2a35)" />
          <circle cx="19" cy="16" r="1.2" fill="var(--oneko-line, #2a2a35)" />
          <path d="M15 18h2l-1 1.5z" fill="var(--oneko-nose, #ff9db1)" />
          <path
            className="oneko__tail"
            d="M22 20c3 0 4-2 4-4"
            fill="none"
            stroke="var(--oneko-line, #2a2a35)"
            strokeWidth="1.6"
            strokeLinecap="round"
          />
          <rect className="oneko__leg oneko__leg--front" x="10" y="22" width="3" height="4" rx="1" fill="var(--oneko-fur, #d8d8d8)" stroke="var(--oneko-line, #2a2a35)" strokeWidth="0.8" />
          <rect className="oneko__leg oneko__leg--back" x="18" y="22" width="3" height="4" rx="1" fill="var(--oneko-fur, #d8d8d8)" stroke="var(--oneko-line, #2a2a35)" strokeWidth="0.8" />
        </g>
      </svg>
    </div>
  )
}
