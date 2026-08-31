/**
 * Project entries, ported from the 2024 site with dead links repaired.
 *
 * Everything there linked through the `pixeljammed` account, which is now a
 * 0-repo placeholder named "MOVED TO @milotek". Those URLs only ever resolved
 * through GitHub's rename redirects, so they point at canonical paths here.
 * `HRSFC-Programs` became `Practice.NET` in the same move.
 */
export interface Link {
  label: string
  href: string
  /** Which glyph the link gets in the detail page's link row. */
  kind?: 'code' | 'doc' | 'demo' | 'link'
}

export interface Shot {
  src: string
  alt: string
  caption: string
}

export type Status = 'shipped' | 'in progress' | 'unreleased' | 'archived'

export interface Project {
  slug: string
  title: string
  blurb: string
  /** Longer copy for the detail page. Falls back to `blurb`. */
  description?: string
  status: Status
  year: string
  tech: string[]
  points: string[]
  links: Link[]
  shots: Shot[]
  /** Card thumbnail. Omitted when there is nothing worth showing. */
  thumb?: string
  featured?: boolean
}

export const projects: Project[] = [
  {
    slug: 'lockyn',
    title: 'Lockyn',
    blurb: 'Commercial mobile study app for GCSE and sixth form students.',
    description:
      'A study app for GCSE and sixth form students, built in React Native on top of Firebase. I designed and built the whole thing: onboarding, the home screen, and the per-topic summary pages students actually spend their time in. It started as an A level NEA, which is why it was never released - coursework cannot go public before results day.',
    // Results day has now passed, so this is a decision rather than a default.
    status: 'unreleased',
    year: '2025 - 2026',
    tech: ['TypeScript', 'React Native', 'Firebase'],
    points: [
      'Written in TypeScript and JavaScript, with Firebase for the back end.',
      'Designed UI covering onboarding, home, and per-topic summary screens.',
      'Built as an A level NEA project, so release was held until after results day.',
    ],
    links: [],
    thumb: '/shots/lockyn-home.jpg',
    featured: true,
    shots: [
      {
        src: '/shots/lockyn-landing.jpg',
        alt: 'Lockyn landing screen with the app name and a sign-in prompt.',
        caption: 'landing page',
      },
      {
        src: '/shots/lockyn-onboarding.jpg',
        alt: 'Lockyn onboarding flow asking the user to pick their subjects.',
        caption: 'onboarding',
      },
      {
        src: '/shots/lockyn-home.jpg',
        alt: 'Lockyn home screen listing study topics and progress.',
        caption: 'home',
      },
      {
        src: '/shots/lockyn-summary.jpg',
        alt: 'Lockyn per-topic summary screen showing revision notes.',
        caption: 'summary page',
      },
    ],
  },
  {
    slug: 'ezcals',
    title: 'EZcals',
    blurb: 'Calorie tracker built around logging a meal in as few taps as possible.',
    description:
      'Most calorie trackers lose you at the third screen. EZcals is built around one number: how long it takes to log a meal. Originally Swift and SwiftUI for iOS, rewritten in React Native in 2025 so it runs on Android too.',
    status: 'shipped',
    year: '2024 - 2025',
    tech: ['Swift', 'SwiftUI', 'React Native'],
    points: [
      'Mobile app for iOS and Android.',
      'Designed for speed of logging rather than breadth of features.',
      'Tracks calories and macros.',
      'Originally Swift and SwiftUI, rewritten in React Native in 2025 for cross-platform support.',
    ],
    links: [],
    thumb: '/shots/ezcals-home.gif',
    featured: true,
    shots: [
      {
        src: '/shots/ezcals-homepage.gif',
        alt: 'Animated walkthrough of the EZcals marketing homepage.',
        caption: 'homepage',
      },
      {
        src: '/shots/ezcals-onboarding.gif',
        alt: 'Animated walkthrough of the EZcals onboarding flow.',
        caption: 'onboarding',
      },
      {
        src: '/shots/ezcals-home.gif',
        alt: "Animated walkthrough of the EZcals home screen and today's log.",
        caption: 'home',
      },
    ],
  },
  {
    slug: 'autopet-feeder',
    title: 'AutoPet Feeder',
    blurb: 'An automated pet feeder, built to a real client specification.',
    description:
      'An automated pet feeder designed and built to a specification written by my neighbours, who are the sort of client who tells you exactly what they want and then changes it. A Raspberry Pi drives a servo behind a touchscreen, in a 3D printed ABS shell with an oak finish. The whole process is written up: prototypes, client spec, evaluation.',
    status: 'shipped',
    year: '2024',
    tech: ['Raspberry Pi', 'JavaScript', 'CAD', '3D printing'],
    points: [
      "IoT project designed and built to a neighbour's specification.",
      'Raspberry Pi driving a servo, with a touchscreen and USB-C power.',
      'ABS 3D printed shell with an oak finish.',
      'Full design document covering prototypes, client spec and evaluation.',
    ],
    links: [
      { label: 'Source', href: 'https://github.com/milotek/petfeeder', kind: 'code' },
      {
        label: 'Design document (PDF)',
        href: 'https://github.com/milotek/petfeeder/blob/master/Product%20Design%20NEA%20Edited.pdf',
        kind: 'doc',
      },
    ],
    shots: [],
  },
]

export function getProject(slug: string): Project | undefined {
  return projects.find((project) => project.slug === slug)
}
