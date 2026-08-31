import type { Entry } from './types'

export const gamesIntro =
  'Some games I have made. Most of them are publicly available on my GitHub.'

export const games: Entry[] = [
  {
    slug: 'epq',
    title: 'Extended Project Qualification',
    summary: 'An accessible platforming and exploration themed video game.',
    points: [
      'Made in the Godot engine.',
      'Developed over six months.',
      'Built at weekends across the first year of my A levels.',
    ],
    video: { title: 'EPQ project video presentation', youtubeId: 'bz-V_AmdrWE' },
  },
  {
    slug: 'schism',
    title: 'Schism',
    summary: 'Survival, co-op, horror, roguelike - a Roblox hobby project.',
    points: [
      'Silly, for-fun messing around game.',
      'Proprietary code, but feel free to look at some of the things we share.',
    ],
    links: [{ label: 'Pixeljam Studios', href: 'https://github.com/Pixeljam-Studios' }],
  },
  {
    slug: 'csharp-collection',
    title: 'C# Game Collection',
    summary: 'A few games made in C# / .NET to show my proficiency in the language.',
    points: [
      'Battleships, Tetris and Blackjack.',
      'Varying degrees of complexity, showing my development process.',
      'One text based game, one terminal GUI game, and one WinForms game.',
    ],
    links: [
      { label: 'Source on GitHub', href: 'https://github.com/pixeljammed/HRSFC-Programs' },
      {
        label: '14 page written evaluation',
        href: 'https://github.com/pixeljammed/HRSFC-Programs/blob/main/Battleships/Battle%20Boats%20evaluation.pdf',
      },
    ],
    shotShape: 'wide',
    shots: [
      {
        src: '/shots/csharp_battleships.jpg',
        alt: 'Battleships running in a terminal.',
        caption: 'Battleships',
      },
      {
        src: '/shots/csharp_tetris.jpg',
        alt: 'Tetris running as a WinForms application.',
        caption: 'Tetris',
      },
      {
        src: '/shots/csharp_blackjack.jpg',
        alt: 'Blackjack running in a terminal.',
        caption: 'Blackjack',
      },
    ],
  },
]
