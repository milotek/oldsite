import { useEffect, useRef } from 'react'

/**
 * The grid behind everything.
 *
 * At rest it is a plain lattice barely brighter than the page. The cursor
 * lifts the cells near it toward the accent colour, drags a wake behind it,
 * and clicks send a ring outward.
 *
 * Drawn on a canvas rather than as a grid of divs. At a 28px cell a 1440x900
 * viewport is about 1,700 cells, and mutating that many inline styles every
 * frame is the kind of thing that shows up as jank on a laptop on battery.
 * The canvas draws the dim lattice once per resize into an offscreen buffer
 * and then, per frame, only strokes the handful of cells that are actually lit.
 */

const DECAY = 6 // intensity units per second

const HOVER_RADIUS = 2.4 // cells
const HOVER_STRENGTH = 0.55

const RIPPLE_SPEED = 13 // cells per second
const RIPPLE_MAX_RADIUS = 10
const RIPPLE_WIDTH = 1.8
const RIPPLE_STRENGTH = 0.6

const WAKE_FADE = 2.4 // per second
const WAKE_STRENGTH = 0.34
const WAKE_MAX = 26 // trail points retained

/** Lit cells are bucketed so a frame is a few stroked paths, not a few hundred. */
const BUCKETS = 6
const MIN_VISIBLE = 0.04

interface Ripple {
  x: number
  y: number
  radius: number
}

interface WakePoint {
  x: number
  y: number
  life: number
}

function parseColor(value: string): [number, number, number] {
  const rgb = value.match(/(\d+(?:\.\d+)?)/g)
  if (rgb && rgb.length >= 3) {
    return [Number(rgb[0]), Number(rgb[1]), Number(rgb[2])]
  }
  const hex = value.trim().replace('#', '')
  if (hex.length === 6) {
    return [
      parseInt(hex.slice(0, 2), 16),
      parseInt(hex.slice(2, 4), 16),
      parseInt(hex.slice(4, 6), 16),
    ]
  }
  return [255, 255, 255]
}

export function InteractiveGrid() {
  const hostRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const host = hostRef.current
    if (!host) return

    // The static CSS lattice on <html> is the no-JS fallback. Now that this
    // component is live it would double up, so hide it.
    document.body.classList.add('grid-live')

    const canvas = document.createElement('canvas')
    canvas.setAttribute('aria-hidden', 'true')
    host.appendChild(canvas)
    const ctx = canvas.getContext('2d', { alpha: true })
    if (!ctx) return

    const root = getComputedStyle(document.documentElement)
    const cell = parseInt(root.getPropertyValue('--grid-size'), 10) || 28
    const dim = parseColor(root.getPropertyValue('--grid-line'))
    const lit = parseColor(root.getPropertyValue('--accent'))

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)')

    let columns = 0
    let rows = 0
    let intensity = new Float32Array(0)
    let ripples: Ripple[] = []
    let wake: WakePoint[] = []
    let pointer: { x: number; y: number } | null = null
    let lastPointer: { x: number; y: number } | null = null
    let frame: number | null = null
    let last = 0

    // The dim lattice never changes between resizes, so it is rasterised once
    // and blitted, rather than re-stroked every frame.
    const backdrop = document.createElement('canvas')
    const backdropCtx = backdrop.getContext('2d')

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2)
      const width = window.innerWidth
      const height = window.innerHeight

      canvas.width = Math.floor(width * dpr)
      canvas.height = Math.floor(height * dpr)
      canvas.style.width = `${width}px`
      canvas.style.height = `${height}px`
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

      columns = Math.ceil(width / cell) + 1
      rows = Math.ceil(height / cell) + 1
      intensity = new Float32Array(columns * rows)

      if (!backdropCtx) return
      backdrop.width = canvas.width
      backdrop.height = canvas.height
      backdropCtx.setTransform(dpr, 0, 0, dpr, 0, 0)
      backdropCtx.clearRect(0, 0, width, height)
      backdropCtx.strokeStyle = `rgb(${dim[0]} ${dim[1]} ${dim[2]})`
      backdropCtx.lineWidth = 1
      backdropCtx.beginPath()
      for (let c = 0; c <= columns; c++) {
        const x = Math.round(c * cell) + 0.5
        backdropCtx.moveTo(x, 0)
        backdropCtx.lineTo(x, height)
      }
      for (let r = 0; r <= rows; r++) {
        const y = Math.round(r * cell) + 0.5
        backdropCtx.moveTo(0, y)
        backdropCtx.lineTo(width, y)
      }
      backdropCtx.stroke()
    }

    const add = (cx: number, cy: number, amount: number) => {
      if (cx < 0 || cy < 0 || cx >= columns || cy >= rows) return
      const index = cy * columns + cx
      // Saturating rather than summing: overlapping ripples should reinforce,
      // but two of them crossing must not produce a blown-out white square.
      intensity[index] = Math.min(1, Math.max(intensity[index], amount))
    }

    const stamp = (cx: number, cy: number, radius: number, strength: number) => {
      const span = Math.ceil(radius)
      for (let dy = -span; dy <= span; dy++) {
        for (let dx = -span; dx <= span; dx++) {
          const distance = Math.hypot(dx, dy)
          if (distance > radius) continue
          add(cx + dx, cy + dy, strength * (1 - distance / radius) ** 2)
        }
      }
    }

    const tick = (now: number) => {
      frame = requestAnimationFrame(tick)
      const delta = Math.min((now - last) / 1000, 0.05)
      last = now

      for (let i = 0; i < intensity.length; i++) {
        if (intensity[i] > 0) intensity[i] = Math.max(0, intensity[i] - DECAY * delta)
      }

      if (pointer) {
        stamp(pointer.x, pointer.y, HOVER_RADIUS, HOVER_STRENGTH)
      }

      for (const point of wake) {
        point.life -= WAKE_FADE * delta
        if (point.life > 0) stamp(point.x, point.y, 1.6, WAKE_STRENGTH * point.life)
      }
      wake = wake.filter((point) => point.life > 0)

      for (const ripple of ripples) {
        ripple.radius += RIPPLE_SPEED * delta
        const fade = 1 - ripple.radius / RIPPLE_MAX_RADIUS
        if (fade <= 0) continue
        const span = Math.ceil(ripple.radius + RIPPLE_WIDTH)
        for (let dy = -span; dy <= span; dy++) {
          for (let dx = -span; dx <= span; dx++) {
            const offset = Math.abs(Math.hypot(dx, dy) - ripple.radius)
            if (offset > RIPPLE_WIDTH) continue
            add(
              ripple.x + dx,
              ripple.y + dy,
              RIPPLE_STRENGTH * fade * (1 - offset / RIPPLE_WIDTH),
            )
          }
        }
      }
      ripples = ripples.filter((ripple) => ripple.radius < RIPPLE_MAX_RADIUS)

      draw()
    }

    const draw = () => {
      const width = window.innerWidth
      const height = window.innerHeight
      ctx.clearRect(0, 0, width, height)
      if (backdropCtx) ctx.drawImage(backdrop, 0, 0, width, height)

      ctx.lineWidth = 1
      for (let bucket = 1; bucket <= BUCKETS; bucket++) {
        const low = MIN_VISIBLE + ((bucket - 1) / BUCKETS) * (1 - MIN_VISIBLE)
        const high = MIN_VISIBLE + (bucket / BUCKETS) * (1 - MIN_VISIBLE)
        const t = (low + high) / 2

        let started = false
        for (let r = 0; r < rows; r++) {
          for (let c = 0; c < columns; c++) {
            const value = intensity[r * columns + c]
            if (value < low || value >= high) continue
            if (!started) {
              ctx.beginPath()
              started = true
            }
            const x = Math.round(c * cell) + 0.5
            const y = Math.round(r * cell) + 0.5
            ctx.moveTo(x, y)
            ctx.lineTo(x + cell, y)
            ctx.moveTo(x, y)
            ctx.lineTo(x, y + cell)
          }
        }
        if (!started) continue

        ctx.strokeStyle = `rgb(${Math.round(dim[0] + (lit[0] - dim[0]) * t)} ${Math.round(
          dim[1] + (lit[1] - dim[1]) * t,
        )} ${Math.round(dim[2] + (lit[2] - dim[2]) * t)})`
        ctx.stroke()
      }
    }

    const onPointerMove = (event: PointerEvent) => {
      const x = Math.floor(event.clientX / cell)
      const y = Math.floor(event.clientY / cell)
      pointer = { x, y }

      // One wake point per cell entered, not per event: a high-polling-rate
      // mouse fires often enough to pile a dozen points into one square.
      if (!lastPointer || lastPointer.x !== x || lastPointer.y !== y) {
        wake.push({ x, y, life: 1 })
        if (wake.length > WAKE_MAX) wake.shift()
        lastPointer = { x, y }
      }
    }

    const onPointerLeave = () => {
      pointer = null
      lastPointer = null
    }

    const onPointerDown = (event: PointerEvent) => {
      ripples.push({
        x: Math.floor(event.clientX / cell),
        y: Math.floor(event.clientY / cell),
        radius: 0,
      })
    }

    resize()

    if (reduceMotion.matches) {
      // The lattice still gets drawn; nothing animates on top of it.
      draw()
      window.addEventListener('resize', () => {
        resize()
        draw()
      })
      return () => {
        document.body.classList.remove('grid-live')
        canvas.remove()
      }
    }

    last = performance.now()
    frame = requestAnimationFrame(tick)
    window.addEventListener('resize', resize)
    window.addEventListener('pointermove', onPointerMove, { passive: true })
    window.addEventListener('pointerdown', onPointerDown, { passive: true })
    document.addEventListener('pointerleave', onPointerLeave)

    return () => {
      if (frame !== null) cancelAnimationFrame(frame)
      window.removeEventListener('resize', resize)
      window.removeEventListener('pointermove', onPointerMove)
      window.removeEventListener('pointerdown', onPointerDown)
      document.removeEventListener('pointerleave', onPointerLeave)
      document.body.classList.remove('grid-live')
      canvas.remove()
    }
  }, [])

  return <div className="interactive-grid" ref={hostRef} aria-hidden="true" />
}
