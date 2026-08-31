import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { execSync } from 'node:child_process'
import { readFileSync } from 'node:fs'

// Baked in at build time so /siteinfo can show what is actually deployed.
// Falls back to 'dev' outside a git checkout (e.g. a tarball build).
function gitRev(): string {
  try {
    return execSync('git rev-parse --short HEAD', { stdio: ['ignore', 'pipe', 'ignore'] })
      .toString()
      .trim()
  } catch {
    return 'dev'
  }
}

export default defineConfig({
  plugins: [react()],
  define: {
    __GIT_REV__: JSON.stringify(gitRev()),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    __APP_VERSION__: JSON.stringify(
      JSON.parse(readFileSync('./package.json', 'utf8')).version as string,
    ),
  },
  build: {
    // The prerender step reads this to map routes to their JS/CSS chunks.
    manifest: true,
  },
})
