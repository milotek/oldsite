export interface Artwork {
  /** Display-size image for the grid. `_full` is the original behind the lightbox. */
  src: string
  full: string
  alt: string
  caption: string
}

export const artIntro =
  'Art I have made over the years, mostly in Procreate on an iPad Pro with an Apple Pencil.'

export const artwork: Artwork[] = [
  {
    src: '/art/de_dust2_fullbright.jpg',
    full: '/art/de_dust2_fullbright_full.jpg',
    alt: 'A drawing of the level de_dust2 from Counter-Strike.',
    caption: 'de_dust2 in mat_fullbright',
  },
  {
    src: '/art/de_lake.jpg',
    full: '/art/de_lake_full.jpg',
    alt: 'A drawing of the Counter-Strike map de_lake.',
    caption: 'de_lake, my favourite map',
  },
  {
    src: '/art/epq_protagonist.jpg',
    full: '/art/epq_protagonist_full.jpg',
    alt: 'Concept character art of the protagonist for my EPQ game.',
    caption: 'EPQ protagonist concept art',
  },
  {
    src: '/art/epq_antagonist.jpg',
    full: '/art/epq_antagonist_full.jpg',
    alt: 'Concept character art of the antagonist for my EPQ game.',
    caption: 'EPQ antagonist concept art',
  },
  {
    src: '/art/hardware_vs_software_poster.jpg',
    full: '/art/hardware_vs_software_poster_full.jpg',
    alt: 'Poster explaining the differences between hardware and software.',
    caption: 'Poster for a Computer Science competition, explaining hardware vs software',
  },
  {
    src: '/art/friends_birthday.jpg',
    full: '/art/friends_birthday_full.jpg',
    alt: 'A drawing of me and my friends.',
    caption: "Me and my friends, drawn for someone's birthday",
  },
  {
    src: '/art/steam_profile_commission.jpg',
    full: '/art/steam_profile_commission_full.jpg',
    alt: "A friend's Steam profile picture, drawn by request.",
    caption: "A friend's Steam profile picture, drawn by request",
  },
  {
    src: '/art/old_profile_picture.jpg',
    full: '/art/old_profile_picture_full.jpg',
    alt: 'My old profile picture.',
    caption: 'My old profile picture on websites',
  },
  {
    src: '/art/quick_sketch.gif',
    full: '/art/quick_sketch_full.gif',
    alt: 'A quick sketch drawn for a friend.',
    caption: 'Quick sketch I made in under a minute for a friend',
  },
  {
    src: '/art/giraffe.jpg',
    full: '/art/giraffe_full.jpg',
    alt: 'A cute cartoon giraffe.',
    caption: 'Cute giraffe, made with Pixelmator Pro to demonstrate the app',
  },
  {
    src: '/art/geometry_dash_anniversary.jpg',
    full: '/art/geometry_dash_anniversary_full.jpg',
    alt: 'Geometry Dash 10 year anniversary fan artwork.',
    caption: 'Geometry Dash 10 year anniversary fan art',
  },
  {
    src: '/art/pygame_title_screen.jpg',
    full: '/art/pygame_title_screen_full.jpg',
    alt: 'Title screen background art for a pygame project.',
    caption: 'Title screen background for a pygame project',
  },
  {
    src: '/art/pygame_sunset.jpg',
    full: '/art/pygame_sunset_full.jpg',
    alt: 'Sunset stage background art for a pygame project.',
    caption: '"Sunset" stage background',
  },
  {
    src: '/art/pygame_space.jpg',
    full: '/art/pygame_space_full.jpg',
    alt: 'Space stage background art for a pygame project.',
    caption: '"Space" stage background',
  },
  {
    src: '/art/pygame_underground.jpg',
    full: '/art/pygame_underground_full.jpg',
    alt: 'Underground stage background art for a pygame project.',
    caption: '"Underground" stage background',
  },
  {
    src: '/art/pygame_world.jpg',
    full: '/art/pygame_world_full.jpg',
    alt: 'World stage background art for a pygame project.',
    caption: '"World" stage background',
  },
]
