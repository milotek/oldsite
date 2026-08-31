import { useEffect, useRef } from 'react'

/*
 * Adapted from the InteractiveGrid on bomberfish.ca.
 * Copyright (c) 2025 Hariz Shirazi. MIT licensed - see THIRD_PARTY.md.
 *
 * Two deliberate departures from the original. It renders to a <canvas>
 * rather than a grid of <div>s, because the original repaints every cell of a
 * ~3500 element DOM grid each frame; and the side-ripples that spawn off the
 * wake are dropped, since they are the fiddliest part of the maths and the
 * least visible on screen. Hover glow, cursor wake and click ripples remain.
 */

const LERP = 6 // approach speed of the hover glow, per second

const HOVER_RADIUS = 2 // cells
const HOVER_BRIGHTNESS = 0.5
const HOVER_FALLOFF = 2

const WAKE_FADE = 2.2 // per second; slow enough to stay visible at low speeds
const WAKE_BRIGHTNESS = 0.4
const WAKE_LENGTH = 2 // along the direction of travel
const WAKE_WIDTH = 4 // perpendicular to it
const WAKE_HOVER_FACTOR = 0.5
const WAKE_PRESSED_FACTOR = 0.9

const RIPPLE_SPEED = 12 // cells per second
const RIPPLE_MAX_RADIUS = 9
const RIPPLE_WIDTH = 2
const RIPPLE_BRIGHTNESS = 0.5
const RIPPLE_FALLOFF = 5 // higher fades the ring faster as it travels

interface Ripple {
  x: number
  y: number
  r: number
}

interface WakePoint {
  x: number
  y: number
  dx: number
  dy: number
  intensity: number
  brightness: number
}

export default function InteractiveGrid() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)')
    // Touch has no meaningful hover, and the effect is pure decoration, so it
    // is not worth the battery on a device that cannot show it.
    const finePointer = window.matchMedia('(any-hover: hover) and (any-pointer: fine)')
    if (reduceMotion.matches || !finePointer.matches) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const styles = getComputedStyle(document.documentElement)
    const cell = parseInt(styles.getPropertyValue('--grid-size'), 10) || 28
    const lineColour = styles.getPropertyValue('--line').trim() || '#313244'
    const glowColour = styles.getPropertyValue('--accent').trim() || '#ffbdbd'

    let cols = 0
    let rows = 0
    let glow = new Float32Array(0)
    let target = new Float32Array(0)
    let ripples: Ripple[] = []
    let wake: WakePoint[] = []

    let cursorCol = -1
    let cursorRow = -1
    let hovering = false
    let pressed = false
    let lastCol = -1
    let lastRow = -1
    let raf: number | null = null
    let last = 0

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2)
      const w = window.innerWidth
      const h = window.innerHeight
      canvas.width = Math.floor(w * dpr)
      canvas.height = Math.floor(h * dpr)
      canvas.style.width = `${w}px`
      canvas.style.height = `${h}px`
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      cols = Math.ceil(w / cell) + 1
      rows = Math.ceil(h / cell) + 1
      glow = new Float32Array(cols * rows)
      target = new Float32Array(cols * rows)
    }

    const updateTargets = () => {
      target.fill(0)
      if (!hovering || cursorCol < 0) return
      for (let dr = -HOVER_RADIUS; dr <= HOVER_RADIUS; dr += 1) {
        for (let dc = -HOVER_RADIUS; dc <= HOVER_RADIUS; dc += 1) {
          const r = cursorRow + dr
          const c = cursorCol + dc
          if (r < 0 || r >= rows || c < 0 || c >= cols) continue
          const manhattan = Math.abs(dr) + Math.abs(dc)
          if (manhattan > HOVER_RADIUS) continue
          const progress = manhattan / (HOVER_RADIUS + 1)
          target[r * cols + c] = 0.7 * (1 - progress) ** HOVER_FALLOFF * HOVER_BRIGHTNESS
        }
      }
    }

    const draw = (time: number) => {
      const dt = Math.min((time - last) / 1000, 0.1)
      last = time

      ripples.forEach((rip) => {
        rip.r += RIPPLE_SPEED * dt
      })
      ripples = ripples.filter((rip) => rip.r < RIPPLE_MAX_RADIUS)

      wake.forEach((w) => {
        w.intensity -= WAKE_FADE * dt
      })
      wake = wake.filter((w) => w.intensity > 0.01)

      let moving = ripples.length > 0 || wake.length > 0

      const w = canvas.clientWidth
      const h = canvas.clientHeight
      ctx.clearRect(0, 0, w, h)

      // Static lattice first, so lit cells sit on top of it.
      ctx.strokeStyle = lineColour
      ctx.lineWidth = 1
      ctx.beginPath()
      for (let c = 0; c <= cols; c += 1) {
        const x = c * cell + 0.5
        ctx.moveTo(x, 0)
        ctx.lineTo(x, h)
      }
      for (let r = 0; r <= rows; r += 1) {
        const y = r * cell + 0.5
        ctx.moveTo(0, y)
        ctx.lineTo(w, y)
      }
      ctx.stroke()

      ctx.fillStyle = glowColour
      for (let r = 0; r < rows; r += 1) {
        for (let c = 0; c < cols; c += 1) {
          const i = r * cols + c
          let v = glow[i]!
          const t = target[i]!
          const delta = t - v
          if (Math.abs(delta) > 0.0004) {
            v += delta * LERP * dt
            moving = true
          } else {
            v = t
          }
          glow[i] = v

          let intensity = v

          for (const rip of ripples) {
            const dist = Math.hypot(c - rip.x, r - rip.y)
            const diff = Math.abs(dist - rip.r)
            if (diff >= RIPPLE_WIDTH) continue
            const fade = (1 - rip.r / RIPPLE_MAX_RADIUS) ** RIPPLE_FALLOFF
            intensity += (1 - diff / RIPPLE_WIDTH) * fade * RIPPLE_BRIGHTNESS
          }

          for (const point of wake) {
            const relX = c - point.x
            const relY = r - point.y
            // Project onto the direction of travel so the trail is short
            // along it and wide across it, like a wake behind a boat.
            const along = relX * point.dx + relY * point.dy
            const across = relX * -point.dy + relY * point.dx
            const d = Math.hypot(along / WAKE_LENGTH, across / WAKE_WIDTH)
            if (d >= 1) continue
            intensity = Math.max(
              intensity,
              (1 - d) * point.intensity * WAKE_BRIGHTNESS * point.brightness,
            )
          }

          if (intensity < 0.004) continue
          ctx.globalAlpha = Math.min(intensity, 1)
          ctx.fillRect(c * cell + 1, r * cell + 1, cell - 1, cell - 1)
        }
      }
      ctx.globalAlpha = 1

      raf = moving || hovering ? requestAnimationFrame(draw) : null
    }

    const start = () => {
      if (raf === null) {
        last = performance.now()
        raf = requestAnimationFrame(draw)
      }
    }

    const onPointerMove = (e: PointerEvent) => {
      if (e.pointerType !== 'mouse') return
      const c = Math.floor(e.clientX / cell)
      const r = Math.floor(e.clientY / cell)
      hovering = true
      if (c === cursorCol && r === cursorRow) return

      if (lastCol >= 0) {
        let dx = c - lastCol
        let dy = r - lastRow
        const len = Math.hypot(dx, dy)
        if (len > 0) {
          dx /= len
          dy /= len
        } else {
          dx = 1
          dy = 0
        }
        wake.push({
          x: c,
          y: r,
          dx,
          dy,
          intensity: 1,
          brightness: pressed ? WAKE_PRESSED_FACTOR : WAKE_HOVER_FACTOR,
        })
      }
      lastCol = c
      lastRow = r
      cursorCol = c
      cursorRow = r
      updateTargets()
      start()
    }

    const onPointerDown = (e: PointerEvent) => {
      if (e.pointerType !== 'mouse') return
      // Let a click on a link be a click on a link, not a splash.
      if ((e.target as Element | null)?.closest('a, button')) return
      pressed = true
      start()
    }

    const onPointerUp = (e: PointerEvent) => {
      if (e.pointerType !== 'mouse' || !pressed) return
      pressed = false
      ripples.push({ x: Math.floor(e.clientX / cell), y: Math.floor(e.clientY / cell), r: 0 })
      start()
    }

    const onPointerLeave = () => {
      hovering = false
      pressed = false
      cursorCol = -1
      cursorRow = -1
      lastCol = -1
      lastRow = -1
      updateTargets()
      start()
    }

    let resizeTimer: ReturnType<typeof setTimeout>
    const onResize = () => {
      clearTimeout(resizeTimer)
      resizeTimer = setTimeout(() => {
        resize()
        start()
      }, 150)
    }

    resize()
    document.body.classList.add('grid-live')
    start()

    document.addEventListener('pointermove', onPointerMove, { passive: true })
    document.addEventListener('pointerdown', onPointerDown, { passive: true })
    document.addEventListener('pointerup', onPointerUp, { passive: true })
    document.addEventListener('pointerleave', onPointerLeave)
    window.addEventListener('resize', onResize)

    return () => {
      if (raf !== null) cancelAnimationFrame(raf)
      clearTimeout(resizeTimer)
      document.body.classList.remove('grid-live')
      document.removeEventListener('pointermove', onPointerMove)
      document.removeEventListener('pointerdown', onPointerDown)
      document.removeEventListener('pointerup', onPointerUp)
      document.removeEventListener('pointerleave', onPointerLeave)
      window.removeEventListener('resize', onResize)
    }
  }, [])

  return <canvas ref={canvasRef} className="grid-canvas" aria-hidden="true" />
}
