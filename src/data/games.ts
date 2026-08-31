import type { Link, Shot } from './projects'

export interface Game {
  slug: string
  title: string
  blurb: string
  description?: string
  year: string
  tech: string[]
  points: string[]
  links: Link[]
  shots: Shot[]
  thumb?: string
  featured?: boolean
  /** YouTube id. Embedded through youtube-nocookie, and only after a click. */
  video?: { id: string; title: string }
}

export const games: Game[] = [
  {
    slug: 'epq-platformer',
    title: 'Accessible platformer',
    blurb: 'An accessibility-focused platforming and exploration game.',
    description:
      'My Extended Project Qualification, titled "An accessible platforming and exploration themed video game". Six months in Godot, built on weekends through the first year of A levels. The interesting part was not the platforming; it was working out what "accessible" has to mean before you write any of it.',
    year: '2024',
    tech: ['Godot', 'GDScript'],
    points: [
      'Extended Project Qualification: "An accessible platforming and exploration themed video game".',
      'Built in Godot over six months, on weekends during the first year of A levels.',
    ],
    links: [
      { label: 'Related source', href: 'https://github.com/milotek/GodotGame', kind: 'code' },
    ],
    thumb: '/art/epq_protagonist.jpg',
    featured: true,
    shots: [],
    video: { id: 'bz-V_AmdrWE', title: 'EPQ project video presentation' },
  },
  {
    slug: 'csharp-collection',
    title: 'C# game collection',
    blurb: 'Battleships, Tetris and Blackjack, at three levels of complexity.',
    description:
      'Three games in C#, picked so the set shows a development process rather than one finished result: one text-based, one terminal GUI, one WinForms. Ships with a 14 page written evaluation, which is longer than some of the games.',
    year: '2023',
    tech: ['C#', '.NET', 'WinForms'],
    points: [
      'One text-based game, one terminal GUI game, and one WinForms game.',
      'Varying complexity, chosen to show the development process rather than one finished result.',
      'Ships with a 14 page written evaluation.',
    ],
    links: [
      {
        label: 'Battleships',
        href: 'https://github.com/milotek/Practice.NET/tree/main/Battleships',
        kind: 'code',
      },
      {
        label: 'Tetris',
        href: 'https://github.com/milotek/Practice.NET/tree/main/TetrisWinForms',
        kind: 'code',
      },
      {
        label: 'Blackjack',
        href: 'https://github.com/milotek/Practice.NET/tree/main/Blackjack',
        kind: 'code',
      },
      {
        label: 'Evaluation (PDF)',
        href: 'https://github.com/milotek/Practice.NET/blob/main/Battleships/Battle%20Boats%20evaluation.pdf',
        kind: 'doc',
      },
    ],
    thumb: '/shots/csharp-tetris.jpg',
    shots: [
      {
        src: '/shots/csharp-battleships.jpg',
        alt: 'Terminal output of the Battleships game showing a placed grid.',
        caption: 'Battleships',
      },
      {
        src: '/shots/csharp-tetris.jpg',
        alt: 'The WinForms Tetris game mid-play with stacked pieces.',
        caption: 'Tetris',
      },
      {
        src: '/shots/csharp-blackjack.jpg',
        alt: 'The Blackjack game showing a dealt hand and the running total.',
        caption: 'Blackjack',
      },
    ],
  },
  {
    slug: 'schism',
    title: 'Schism',
    blurb: 'Survival co-op horror roguelike. A Roblox hobby project.',
    description:
      'A silly, for-fun co-op horror roguelike on Roblox. The game itself is proprietary, but a few of the components we built for it are shared publicly under Pixeljam Studios.',
    year: '2024 - 2025',
    tech: ['Roblox', 'Luau'],
    points: [
      'Silly, for-fun messing around game.',
      'Source is proprietary, but some components are shared publicly.',
    ],
    links: [
      { label: 'Pixeljam Studios', href: 'https://github.com/Pixeljam-Studios', kind: 'code' },
    ],
    shots: [],
  },
]

export function getGame(slug: string): Game | undefined {
  return games.find((game) => game.slug === slug)
}
