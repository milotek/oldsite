/**
 * Identity, contact details and the handful of site-wide constants.
 *
 * The 2024 site published a mobile number in plain text on the landing page
 * and pointed its mailto at milo@milotek.com, which is the wrong TLD. The
 * number is gone rather than moved, and the address is corrected here.
 */
export const site = {
  name: 'Milo Tekchandani',
  handle: 'milotek',
  url: 'https://milotek.dev',
  title: 'milotek.dev',
  description: 'Milo Tekchandani - software engineer. Projects, games, artwork and writing.',
  role: 'Software engineer apprentice at Google, London',
  email: 'milo@milotek.dev',
} as const

export interface SocialLink {
  label: string
  href: string
  handle: string
}

export const socials: SocialLink[] = [
  { label: 'github', href: 'https://github.com/milotek', handle: '@milotek' },
  {
    label: 'linkedin',
    href: 'https://www.linkedin.com/in/milo-tekchandani-686602292/',
    handle: 'Milo Tekchandani',
  },
  { label: 'instagram', href: 'https://www.instagram.com/milo.tek/', handle: '@milo.tek' },
  {
    label: 'spotify',
    href: 'https://open.spotify.com/user/31zsvravykeeizwyelb673odcu4q',
    handle: 'milotek',
  },
]

/**
 * The CV is served from this site, not linked straight at the profile repo.
 *
 * raw.githubusercontent.com returns PDFs as `application/octet-stream` with
 * `nosniff` and `x-frame-options: deny`, so no browser will ever render one
 * inline - an <object> pointed at it is a permanently blank box. The deploy
 * workflow refreshes `public/CV.pdf` from `cvSource` before every build, so
 * the profile repo stays the single place the file is edited.
 */
export const cvUrl = '/CV.pdf'
export const cvSource = 'https://github.com/milotek/milotek'

/**
 * The 88x31 to hotlink. The snippet is what gets copied when it is clicked,
 * so it has to be a complete, working anchor rather than just the image URL.
 */
export const webButton = {
  src: '/img/button.png',
  snippet: `<a href="https://milotek.dev/">\n  <img src="https://milotek.dev/img/button.png" alt="milotek.dev" title="milotek.dev" />\n</a>`,
}

/**
 * Two tracks carried over from the 2024 landing page, where they autoplayed.
 * Here the player is opt-in, so nothing is fetched until it is asked for.
 */
export const tracks = ['/audio/music.mp3', '/audio/music_2.mp3'] as const
