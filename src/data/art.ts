import type { ImageMetadata } from 'astro';
import dust2 from '../assets/art/c6ba2180.jpg';
import lake from '../assets/art/2f297d23.jpg';
import antagonist from '../assets/art/bd5efe96.jpg';
import protagonist from '../assets/art/2dbfb7f8.jpg';
import friends from '../assets/art/191a6b44.jpg';
import title from '../assets/art/4a026d2f.jpg';
import sunset from '../assets/art/7ff9075b.jpg';
import space from '../assets/art/6bfcf853.jpg';
import underground from '../assets/art/f2891b7b.jpg';
import world from '../assets/art/5a9c5a0a.jpg';

export interface Artwork {
  src: ImageMetadata;
  alt: string;
  caption: string;
}

// `alt` describes the picture; `caption` is what a person reads next to it.
export const artworks: Artwork[] = [
  {
    src: title,
    alt: 'Dithered pixel art of purple mountains under a full moon at dusk',
    caption: 'Title screen for a pygame project',
  },
  {
    src: lake,
    alt: 'Black ink line sketch of the Counter-Strike map de_lake, with a #BringBackLake caption',
    caption: 'de_lake sketch',
  },
  {
    src: antagonist,
    alt: 'Character concept sheet for my EPQ',
    caption: 'EPQ game project concept art',
  },
  {
    src: sunset,
    alt: 'Dithered pixel art of an orange sunset over a dark sea',
    caption: 'Sunset stage background, same pygame project.',
  },
  {
    src: dust2,
    alt: 'Sketch of the Counter-Strike map de_dust2 at sunset, in flat shading',
    caption: 'de_dust2 in mat_fullbright.',
  },
  {
    src: protagonist,
    alt: 'Character concept sheet for my EPQ',
    caption: 'More EPQ game project concept art',
  },
  {
    src: space,
    alt: 'Pixel art of the Earth from orbit with the sun, a comet and stars',
    caption: 'Space stage background.',
  },
  {
    src: friends,
    alt: 'A grid of eighteen small hand-drawn portraits of friends, each labelled with a name',
    caption: 'Everyone, for someone’s birthday.',
  },
  {
    src: underground,
    alt: 'Pixel art of a dark rock wall with a skull and glowing blue ore',
    caption: 'Underground stage background.',
  },
  {
    src: world,
    alt: 'Pixel art of a bright blue sky with clouds over grass',
    caption: 'World stage background.',
  },
];
