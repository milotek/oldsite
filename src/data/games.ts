import type { Link, Shot } from './projects'

export interface Game {
  slug: string
  title: string
  blurb: string
  year: string
  tech: string[]
  points: string[]
  links: Link[]
  shots: Shot[]
  /** YouTube id, embedded through youtube-nocookie and only on click. */
  video?: { id: string; title: string }
}

export const games: Game[] = [
  {
    slug: 'epq-platformer',
    title: 'Accessible platformer',
    blurb: 'An accessibility-focused platforming and exploration game.',
    year: '2024',
    tech: ['Godot', 'GDScript'],
    points: [
      'Extended Project Qualification: "An accessible platforming and exploration themed video game".',
      'Built in Godot over six months, on weekends during the first year of A levels.',
    ],
    links: [{ label: 'Related source', href: 'https://github.com/milotek/GodotGame' }],
    shots: [],
    video: { id: 'bz-V_AmdrWE', title: 'EPQ project video presentation' },
  },
  {
    slug: 'schism',
    title: 'Schism',
    blurb: 'Survival co-op horror roguelike. A Roblox hobby project.',
    year: '2024-2025',
    tech: ['Roblox', 'Luau'],
    points: [
      'Silly, for-fun messing around game.',
      'Source is proprietary, but some components are shared publicly.',
    ],
    links: [{ label: 'Pixeljam Studios', href: 'https://github.com/Pixeljam-Studios' }],
    shots: [],
  },
  {
    slug: 'csharp-collection',
    title: 'C# game collection',
    blurb: 'Battleships, Tetris and Blackjack, at three levels of complexity.',
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
      },
      { label: 'Tetris', href: 'https://github.com/milotek/Practice.NET/tree/main/TetrisWinForms' },
      { label: 'Blackjack', href: 'https://github.com/milotek/Practice.NET/tree/main/Blackjack' },
      {
        label: 'Evaluation (PDF)',
        href: 'https://github.com/milotek/Practice.NET/blob/main/Battleships/Battle%20Boats%20evaluation.pdf',
      },
    ],
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
]
