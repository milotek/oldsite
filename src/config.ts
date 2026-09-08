export const site = {
  name: 'Milo Tekchandani',
  handle: 'milotek',
  role: 'Software Engineer Apprentice at Google, London',
  description:
    'Milo Tekchandani. Software engineer apprentice at Google, working on the Google Search app for Android. Projects, writing and art.',
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
  'backend and infrastructure on the Google Search app',
  'currently: page transitions for Android Search',
  'three keyboards, no consistent modifier keys',
  'no lake, no play',
  'runs NixOS on purpose',
  '1-indexed arrays are a crime',
  'draws sometimes',
  'de_lake enjoyer',
];

export interface Friend {
  name: string;
  href: string;
  button: string;
}

export const friends: Friend[] = [
  { name: 'bomberfish', href: 'https://bomberfish.ca', button: 'https://bomberfish.ca/button.gif' },
  { name: 'qwq', href: 'https://qwq.sh/', button: 'https://qwq.sh/88x31/hazelcaffe.png' },
  { name: 'dispherical', href: 'https://dispherical.com/', button: 'https://cdn.dispherical.com/88x31.png' },
  { name: 'zenfyr', href: 'https://zenfyr.dev/', button: 'https://zenfyr.dev/88_31/88_31.webp' },
  // notfire serves HTML to anything that does not look like a browser; the image is fine in one.
  { name: 'notfire', href: 'https://notfire.cc/home.html', button: 'https://notfire.cc/design/images/buttons/notfire-cc-88x31-af-darkv.gif' },
  { name: 'sneexy', href: 'https://sneexy.synth.download/', button: 'https://synth.download/assets/buttons/sneexy.svg' },
  { name: 'beeps', href: 'https://beeps.website/', button: 'https://beeps.website/assets/images/buttons/88x31.gif' },
  { name: 'hiijax', href: 'https://hiijax.net/', button: 'https://hiijax.net/buttons/hiijax_v1.gif' },
  { name: 'guigui', href: 'https://guigui.aerocity.site/', button: 'https://guigui.aerocity.site/88x31/guigui.png' },
];

// No button found on the site; listed as a text link until there is one.
export const friendsWithoutButtons: Omit<Friend, 'button'>[] = [
  { name: 'swifty', href: 'https://swiftyshq.neocities.org/main/' },
];
