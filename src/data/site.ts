import type { IconName } from '../components/Icon'

export const site = {
  name: 'Milo Tekchandani',
  title: "milo's website",
  url: 'https://milotek.dev',
  description:
    "Milo Tekchandani's personal website and portfolio - code projects, games, artwork and CV.",
  tagline: 'personal website // code projects // portfolio',
  /**
   * The old site published a personal mobile number in plain text next to this
   * address, and pointed its mailto at the .com. Email only, on the right TLD.
   */
  email: 'milo@milotek.dev',
  copyright: 'milo tek - copyright 2025',
} as const

export interface NavLink {
  to: string
  label: string
  icon: IconName
}

export const nav: NavLink[] = [
  { to: '/', label: 'home', icon: 'home' },
  { to: '/projects', label: 'projects', icon: 'folder' },
  { to: '/games', label: 'games', icon: 'gamepad' },
  { to: '/cv', label: 'cv', icon: 'document' },
  { to: '/art', label: 'art', icon: 'palette' },
  { to: '/misc', label: 'misc', icon: 'info' },
]

export interface Social {
  label: string
  href: string
  icon: IconName
}

export const socials: Social[] = [
  { label: 'GitHub', href: 'https://github.com/pixeljammed', icon: 'github' },
  {
    label: 'LinkedIn',
    href: 'https://www.linkedin.com/in/milo-tekchandani-686602292/',
    icon: 'linkedin',
  },
  { label: 'Email', href: `mailto:${site.email}`, icon: 'email' },
  {
    label: 'Obsidian vault',
    href: 'https://github.com/pixeljammed/ObsidianVault/tree/main',
    icon: 'obsidian',
  },
  { label: 'Instagram', href: 'https://www.instagram.com/milo.tek/', icon: 'instagram' },
]

export const github = 'https://github.com/pixeljammed'
