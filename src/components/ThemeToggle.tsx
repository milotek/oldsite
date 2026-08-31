import { useEffect, useState } from 'react'

type Theme = 'light' | 'dark'

/**
 * The initial theme is applied by an inline script in index.html so there is
 * no flash before hydration. This component only mirrors and mutates it, and
 * deliberately reads nothing during render so SSR and the client agree.
 */
export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme | null>(null)

  useEffect(() => {
    const current = document.documentElement.dataset.theme
    if (current === 'light' || current === 'dark') {
      setTheme(current)
      return
    }
    setTheme(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
  }, [])

  function toggle() {
    const next: Theme = theme === 'dark' ? 'light' : 'dark'
    document.documentElement.dataset.theme = next
    localStorage.setItem('theme', next)
    setTheme(next)
  }

  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={toggle}
      aria-label={theme ? `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme` : 'Switch theme'}
    >
      {theme === 'dark' ? 'light' : 'dark'}
    </button>
  )
}
