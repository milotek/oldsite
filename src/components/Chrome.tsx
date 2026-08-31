import { useCallback, useEffect, useRef, useState } from 'react'
import { tracks } from '../data/site'

type Theme = 'light' | 'dark'

/** One meter band per control button. */
const BANDS = 3

/**
 * The persistent control cluster: player, track swap, theme.
 *
 * The old landing page scaled three buttons to the audio spectrum. That is the
 * one genuinely distinctive thing the site had, so it survives, but as chrome
 * that outlives navigation rather than a trick on the front page.
 *
 * The analyser writes `--level` and a `--level-N` per band onto <html> from
 * inside a rAF loop. Driving those through React state instead would re-render
 * the whole tree sixty times a second to move three boxes.
 */
export function Chrome() {
  const [playing, setPlaying] = useState(false)
  const [track, setTrack] = useState(0)
  const [theme, setTheme] = useState<Theme | null>(null)

  const audioRef = useRef<HTMLAudioElement | null>(null)
  const contextRef = useRef<AudioContext | null>(null)
  const analyserRef = useRef<AnalyserNode | null>(null)
  const frameRef = useRef<number | null>(null)
  const levelRef = useRef(0)
  const bandsRef = useRef<number[]>(Array(BANDS).fill(0))

  // The inline script in index.html has already applied the stored theme to
  // <html> before first paint; this only syncs the button to it.
  useEffect(() => {
    const stored = localStorage.getItem('theme')
    if (stored === 'light' || stored === 'dark') {
      setTheme(stored)
      return
    }
    setTheme(matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
  }, [])

  const toggleTheme = useCallback(() => {
    const next: Theme = theme === 'dark' ? 'light' : 'dark'
    setTheme(next)
    document.documentElement.dataset.theme = next
    localStorage.setItem('theme', next)
  }, [theme])

  const stopMeter = useCallback(() => {
    if (frameRef.current !== null) cancelAnimationFrame(frameRef.current)
    frameRef.current = null
    const root = document.documentElement.style
    root.setProperty('--level', '0')
    for (let band = 1; band <= BANDS; band++) root.setProperty(`--level-${band}`, '0')
  }, [])

  const startMeter = useCallback(() => {
    const analyser = analyserRef.current
    if (!analyser) return
    const bins = new Uint8Array(analyser.frequencyBinCount)
    const root = document.documentElement.style

    // Asymmetric smoothing: snap up on a transient, fall away slowly, so the
    // meter pulses on the beat instead of jittering.
    const smooth = (previous: number, raw: number) =>
      raw > previous ? raw : previous * 0.86 + raw * 0.14

    const tick = () => {
      analyser.getByteFrequencyData(bins)

      // One band per button, low to high, as the 2025 site did. The top third
      // of the spectrum is nearly always empty in these tracks, so the bands
      // are taken from the lower two thirds to keep all three moving.
      const usable = Math.floor((bins.length * 2) / 3)
      const width = Math.floor(usable / BANDS)

      for (let band = 0; band < BANDS; band++) {
        let sum = 0
        for (let i = 0; i < width; i++) sum += bins[band * width + i]!
        const raw = sum / width / 255
        bandsRef.current[band] = smooth(bandsRef.current[band]!, raw)
        root.setProperty(`--level-${band + 1}`, bandsRef.current[band]!.toFixed(3))
      }

      // The strip reads the whole signal rather than one band.
      const overall = bandsRef.current.reduce((a, b) => a + b, 0) / BANDS
      levelRef.current = overall
      root.setProperty('--level', overall.toFixed(3))

      frameRef.current = requestAnimationFrame(tick)
    }

    frameRef.current = requestAnimationFrame(tick)
  }, [])

  const togglePlay = useCallback(async () => {
    const audio = audioRef.current
    if (!audio) return

    if (playing) {
      audio.pause()
      setPlaying(false)
      stopMeter()
      return
    }

    // Both the context and the graph are built on first play: an AudioContext
    // created before a user gesture starts suspended, and createMediaElementSource
    // may only be called once per element, so it is wired here and kept.
    if (!contextRef.current) {
      const context = new AudioContext()
      const analyser = context.createAnalyser()
      analyser.fftSize = 256
      context.createMediaElementSource(audio).connect(analyser)
      analyser.connect(context.destination)
      contextRef.current = context
      analyserRef.current = analyser
    }

    await contextRef.current.resume()
    try {
      await audio.play()
    } catch {
      return // Autoplay policy or a missing file. Leave the button as-is.
    }
    setPlaying(true)
    startMeter()
  }, [playing, startMeter, stopMeter])

  const nextTrack = useCallback(() => {
    setTrack((current) => (current + 1) % tracks.length)
  }, [])

  // Swapping the source resets the element, so playback has to be picked up
  // again. Skipped on the first render, where nothing is playing yet.
  useEffect(() => {
    const audio = audioRef.current
    if (!audio || !playing) return
    void audio.play().catch(() => setPlaying(false))
  }, [track, playing])

  useEffect(() => stopMeter, [stopMeter])

  /**
   * Hover and click sounds, delegated from the document.
   *
   * Gated on the player being on. Unsolicited noise on hover is hostile, but
   * a visitor who has already turned the music on has opted into the whole
   * sound design, so the cues come with it.
   */
  useEffect(() => {
    if (!playing) return

    const hover = new Audio('/audio/hover.wav')
    const click = new Audio('/audio/click.wav')
    hover.volume = 0.35
    click.volume = 0.5

    const cue = (sample: HTMLAudioElement) => (event: Event) => {
      const target = event.target as HTMLElement | null
      if (!target?.closest('a, button')) return
      sample.currentTime = 0
      void sample.play().catch(() => {})
    }

    const onOver = cue(hover)
    const onClick = cue(click)
    document.addEventListener('mouseover', onOver)
    document.addEventListener('click', onClick)

    return () => {
      document.removeEventListener('mouseover', onOver)
      document.removeEventListener('click', onClick)
    }
  }, [playing])

  return (
    <>
      <audio ref={audioRef} src={tracks[track]} loop preload="none" />
      <div className="chrome" data-playing={playing}>
        <button
          type="button"
          onClick={togglePlay}
          aria-pressed={playing}
          aria-label={playing ? 'Stop the music' : 'Play music'}
          title={playing ? 'Stop the music' : 'Play music'}
        >
          <span>{playing ? '■' : '▶'}</span>
        </button>
        <button
          type="button"
          onClick={nextTrack}
          aria-label={`Next track (${track + 1} of ${tracks.length})`}
          title="Next track"
        >
          <span>{'↻'}</span>
        </button>
        <button
          type="button"
          onClick={toggleTheme}
          aria-label={theme === 'dark' ? 'Switch to the light theme' : 'Switch to the dark theme'}
          title="Switch theme"
        >
          <span>{'◑'}</span>
        </button>
      </div>
    </>
  )
}
