/**
 * Art gallery, carried over from the previous site.
 *
 * `alt` describes the image for a screen reader; `caption` is the visible
 * label. They differ deliberately: the old site collapsed them into one
 * string, which made every caption read like alt text.
 *
 * Filenames say what the picture is. The originals were Carrd's content
 * hashes, which tell you nothing when you are looking for one file.
 */
export interface Artwork {
  thumb: string
  full: string
  alt: string
  caption: string
}

export const artworks: Artwork[] = [
  {
    thumb: '/art/de_dust2_fullbright.jpg',
    full: '/art/de_dust2_fullbright_full.jpg',
    alt: 'A picture of the famous level de_dust2 from the video game counter-strike.',
    caption: 'de_dust2 in mat_fullbright',
  },
  {
    thumb: '/art/old_profile_picture.jpg',
    full: '/art/old_profile_picture_full.jpg',
    alt: 'My old profile picture on websites.',
    caption: 'My old profile picture on websites.',
  },
  {
    thumb: '/art/quick_sketch.gif',
    full: '/art/quick_sketch_full.gif',
    alt: 'Quick sketch I made in under a minute for my friend.',
    caption: 'Quick sketch I made in under a minute for my friend.',
  },
  {
    thumb: '/art/steam_profile_commission.jpg',
    full: '/art/steam_profile_commission_full.jpg',
    alt: 'My friend\'s steam profile picture, drawn by request.',
    caption: 'My friend\'s steam profile picture, drawn by request.',
  },
  {
    thumb: '/art/hardware_vs_software_poster.jpg',
    full: '/art/hardware_vs_software_poster_full.jpg',
    alt: 'Poster made for Computer Science competition explaining Hardware vs Software differences in 1st term.',
    caption: 'Poster made for Computer Science competition explaining Hardware vs Software differences in 1st term.',
  },
  {
    thumb: '/art/geometry_dash_anniversary.jpg',
    full: '/art/geometry_dash_anniversary_full.jpg',
    alt: 'I don\'t even know what this one is supposed to represent, but it\'s worth chucking in for padding. Geometry Dash 10 Year Anniversary fan artwork.',
    caption: 'I don\'t even know what this one is supposed to represent, but it\'s worth chucking in for padding. Geometry Dash 10 Year Anniversary fan artwork.',
  },
  {
    thumb: '/art/de_lake.jpg',
    full: '/art/de_lake_full.jpg',
    alt: 'Artwork of the counter-strike map DE_LAKE. My favourite map.',
    caption: 'Artwork of the counter-strike map DE_LAKE. My favourite map.',
  },
  {
    thumb: '/art/epq_antagonist.jpg',
    full: '/art/epq_antagonist_full.jpg',
    alt: 'Concept character art of the antagonist for my EPQ.',
    caption: 'Concept character art of the antagonist for my EPQ.',
  },
  {
    thumb: '/art/epq_protagonist.jpg',
    full: '/art/epq_protagonist_full.jpg',
    alt: 'Concept character art of the protaganist for my EPQ.',
    caption: 'Concept character art of the protaganist for my EPQ.',
  },
  {
    thumb: '/art/friends_birthday.jpg',
    full: '/art/friends_birthday_full.jpg',
    alt: 'Me and my friends. Drawn for someone\'s birthday!',
    caption: 'Me and my friends. Drawn for someone\'s birthday!',
  },
  {
    thumb: '/art/giraffe.jpg',
    full: '/art/giraffe_full.jpg',
    alt: 'Cute giraffe - made with Pixelmator Pro to demonstrate the app.',
    caption: 'Cute giraffe - made with Pixelmator Pro to demonstrate the app.',
  },
  {
    thumb: '/art/pygame_title_screen.jpg',
    full: '/art/pygame_title_screen_full.jpg',
    alt: 'Title screen background for a pygame project.',
    caption: 'Title screen background for a pygame project.',
  },
  {
    thumb: '/art/pygame_sunset.jpg',
    full: '/art/pygame_sunset_full.jpg',
    alt: '"Sunset" stage background for a pygame project.',
    caption: '"Sunset" stage background for a pygame project.',
  },
  {
    thumb: '/art/pygame_space.jpg',
    full: '/art/pygame_space_full.jpg',
    alt: '"Space" stage background for a pygame project.',
    caption: '"Space" stage background for a pygame project.',
  },
  {
    thumb: '/art/pygame_underground.jpg',
    full: '/art/pygame_underground_full.jpg',
    alt: '"Underground" stage background for a pygame project.',
    caption: '"Underground" stage background for a pygame project.',
  },
  {
    thumb: '/art/pygame_world.jpg',
    full: '/art/pygame_world_full.jpg',
    alt: '"World" stage background for a pygame project.',
    caption: '"World" stage background for a pygame project.',
  },
]
