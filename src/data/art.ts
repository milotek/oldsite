/**
 * Art gallery, carried over from the previous site.
 *
 * `alt` describes the image for screen readers; `caption` is the visible
 * label. They differ deliberately - the old site collapsed them into one
 * string, which made captions read like alt text.
 */
export interface Artwork {
  thumb: string
  full: string
  alt: string
  caption: string
}

export const artworks: Artwork[] = [
  {
    thumb: '/art/c6ba2180.jpg',
    full: '/art/c6ba2180_original.jpg',
    alt: 'A picture of the famous level de_dust2 from the video game counter-strike.',
    caption: 'de_dust2 in mat_fullbright',
  },
  {
    thumb: '/art/3525b230.jpg',
    full: '/art/3525b230_original.jpg',
    alt: 'My old profile picture on websites.',
    caption: 'My old profile picture on websites.',
  },
  {
    thumb: '/art/df7348ff.gif',
    full: '/art/df7348ff_original.gif',
    alt: 'Quick sketch I made in under a minute for my friend.',
    caption: 'Quick sketch I made in under a minute for my friend.',
  },
  {
    thumb: '/art/4ed02664.jpg',
    full: '/art/4ed02664_original.jpg',
    alt: 'My friend\'s steam profile picture, drawn by request.',
    caption: 'My friend\'s steam profile picture, drawn by request.',
  },
  {
    thumb: '/art/12468312.jpg',
    full: '/art/12468312_original.jpg',
    alt: 'Poster made for Computer Science competition explaining Hardware vs Software differences in 1st term.',
    caption: 'Poster made for Computer Science competition explaining Hardware vs Software differences in 1st term.',
  },
  {
    thumb: '/art/39249b05.jpg',
    full: '/art/39249b05_original.jpg',
    alt: 'I don\'t even know what this one is supposed to represent, but it\'s worth chucking in for padding. Geometry Dash 10 Year Anniversary fan artwork.',
    caption: 'I don\'t even know what this one is supposed to represent, but it\'s worth chucking in for padding. Geometry Dash 10 Year Anniversary fan artwork.',
  },
  {
    thumb: '/art/2f297d23.jpg',
    full: '/art/2f297d23_original.jpg',
    alt: 'Artwork of the counter-strike map DE_LAKE. My favourite map.',
    caption: 'Artwork of the counter-strike map DE_LAKE. My favourite map.',
  },
  {
    thumb: '/art/bd5efe96.jpg',
    full: '/art/bd5efe96_original.jpg',
    alt: 'Concept character art of the antagonist for my EPQ.',
    caption: 'Concept character art of the antagonist for my EPQ.',
  },
  {
    thumb: '/art/2dbfb7f8.jpg',
    full: '/art/2dbfb7f8_original.jpg',
    alt: 'Concept character art of the protaganist for my EPQ.',
    caption: 'Concept character art of the protaganist for my EPQ.',
  },
  {
    thumb: '/art/191a6b44.jpg',
    full: '/art/191a6b44_original.jpg',
    alt: 'Me and my friends. Drawn for someone\'s birthday!',
    caption: 'Me and my friends. Drawn for someone\'s birthday!',
  },
  {
    thumb: '/art/d1bc936a.jpg',
    full: '/art/d1bc936a_original.jpg',
    alt: 'Cute giraffe - made with Pixelmator Pro to demonstrate the app.',
    caption: 'Cute giraffe - made with Pixelmator Pro to demonstrate the app.',
  },
  {
    thumb: '/art/4a026d2f.jpg',
    full: '/art/4a026d2f_original.jpg',
    alt: 'Title screen background for a pygame project.',
    caption: 'Title screen background for a pygame project.',
  },
  {
    thumb: '/art/7ff9075b.jpg',
    full: '/art/7ff9075b_original.jpg',
    alt: '"Sunset" stage background for a pygame project.',
    caption: '"Sunset" stage background for a pygame project.',
  },
  {
    thumb: '/art/6bfcf853.jpg',
    full: '/art/6bfcf853_original.jpg',
    alt: '"Space" stage background for a pygame project.',
    caption: '"Space" stage background for a pygame project.',
  },
  {
    thumb: '/art/f2891b7b.jpg',
    full: '/art/f2891b7b_original.jpg',
    alt: '"Underground" stage background for a pygame project.',
    caption: '"Underground" stage background for a pygame project.',
  },
  {
    thumb: '/art/5a9c5a0a.jpg',
    full: '/art/5a9c5a0a_original.jpg',
    alt: '"World" stage background for a pygame project.',
    caption: '"World" stage background for a pygame project.',
  },
]
