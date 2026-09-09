export const site = {
  name: 'Milo Tekchandani',
  handle: 'milotek',
  role: 'Software Engineering @ Google, London',
  description:
    'Software Engineer @ Google, working on the Google Search app for Android and iOS.',
  email: 'milo@milotek.dev',
  phone: '+44 7745 011538',
  cv: 'https://github.com/milotek/milotek/raw/main/CV.pdf',
  github: 'milotek',
  lastfm: {
    user: import.meta.env.PUBLIC_LASTFM_USER as string | undefined,
    apiKey: import.meta.env.PUBLIC_LASTFM_API_KEY as string | undefined,
  },
  spotify: 'https://open.spotify.com/user/31zsvravykeeizwyelb673odcu4q',
} as const;

// The number is both the visible label and the keybind, so the bar and the
// keybind overlay have to agree on it; they both read this list.
export interface Workspace {
  key: string;
  name: string;
  path: string;
}

export const workspaces: Workspace[] = [
  { key: '1', name: 'home', path: '' },
  { key: '2', name: 'projects', path: 'projects/' },
  { key: '3', name: 'blog', path: 'blog/' },
  { key: '4', name: 'art', path: 'art/' },
];

export interface Social {
  label: string;
  href: string;
  handle: string;
}

export const socials: Social[] = [
  { label: 'Email', href: `mailto:${site.email}`, handle: site.email },
  { label: 'GitHub', href: 'https://github.com/milotek', handle: '@milotek' },
  { label: 'LinkedIn', href: 'https://www.linkedin.com/in/fired/', handle: 'in/fired' },
  { label: 'Instagram', href: 'https://www.instagram.com/milo.tek/', handle: '@milo.tek' },
  { label: 'Spotify', href: site.spotify, handle: 'milotek' },
];

// One shows under the name on each page load. Keep them true.
export const splashes = [
  'moron',
  'currently: page transitions for Android Search',
  'no lake, no play',
  'nixos user',
  'lua enjoyer',
  'draws sometimes',
  'de_lake player',
];

export interface Friend {
  name: string;
  href: string;
  button: string;
}

export const friends: Friend[] = [
  { name: 'test', href: 'https://bomberfish.ca', button: 'https://bomberfish.ca/button.gif' },
];