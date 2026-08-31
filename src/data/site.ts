/**
 * Single source of truth for identity and contact details.
 *
 * The previous site published a mobile number in plain text on the landing
 * page and pointed its mailto at milo@milotek.com (wrong TLD). Both are fixed
 * here, and the number is gone rather than moved.
 */
export const site = {
  name: 'Milo Tekchandani',
  handle: 'milotek',
  url: 'https://milotek.dev',
  title: 'milotek.dev',
  description: 'Milo Tekchandani - software engineer. Projects, games and artwork.',
  role: 'Software engineer apprentice at Google, London',
  email: 'milo@milotek.dev',
} as const

export interface SocialLink {
  label: string
  href: string
  handle: string
}

export const socials: SocialLink[] = [
  { label: 'GitHub', href: 'https://github.com/milotek', handle: '@milotek' },
  {
    label: 'LinkedIn',
    href: 'https://www.linkedin.com/in/milo-tekchandani-686602292/',
    handle: 'Milo Tekchandani',
  },
  { label: 'Email', href: 'mailto:milo@milotek.dev', handle: 'milo@milotek.dev' },
  { label: 'Instagram', href: 'https://www.instagram.com/milo.tek/', handle: '@milo.tek' },
  {
    label: 'Spotify',
    href: 'https://open.spotify.com/user/31zsvravykeeizwyelb673odcu4q',
    handle: 'milotek',
  },
]

export const cvUrl = 'https://raw.githubusercontent.com/milotek/milotek/main/CV.pdf'

/**
 * Two tracks carried over from the old landing page. The player is opt-in, so
 * these are only ever fetched after a click; `preload="none"` on the element
 * keeps 6 MB of audio off the critical path.
 */
export const tracks = ['/audio/music.mp3', '/audio/music_2.mp3'] as const
