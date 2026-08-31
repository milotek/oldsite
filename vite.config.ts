import { copyFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * GitHub Pages has no rewrite rules, so a deep link like /projects would 404
 * before the router ever loads. Pages does serve 404.html for unknown paths,
 * so shipping the app shell there is what makes client-side routes reachable.
 *
 * This runs at writeBundle rather than generateBundle because Vite's own HTML
 * plugin has not emitted index.html yet at the earlier hook.
 */
function spaFallback() {
  return {
    name: 'spa-fallback',
    writeBundle(options: { dir?: string }) {
      const dir = options.dir ?? 'dist'
      copyFileSync(resolve(dir, 'index.html'), resolve(dir, '404.html'))
    },
  }
}

export default defineConfig({
  plugins: [react(), spaFallback()],
})
