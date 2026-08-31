/**
 * Project entries, ported from the previous site with dead links repaired.
 *
 * The old site linked everything through the `pixeljammed` account, which is
 * now a 0-repo placeholder named "MOVED TO @milotek". Those URLs only resolved
 * via GitHub's rename redirects, so they point at canonical paths here.
 */
export interface Link {
  label: string
  href: string
}

export interface Shot {
  src: string
  alt: string
  caption: string
}

export type Status = 'shipped' | 'in-progress' | 'unreleased' | 'archived'

export interface Project {
  slug: string
  title: string
  blurb: string
  status: Status
  year: string
  tech: string[]
  points: string[]
  links: Link[]
  shots: Shot[]
}

export const projects: Project[] = [
  {
    slug: 'lockyn',
    title: 'Lockyn',
    blurb: 'Commercial mobile study app for GCSE and sixth form students.',
    // Was gated on A level results day as an NEA project. Results day has now
    // passed, so this status needs a decision rather than a default.
    status: 'unreleased',
    year: '2025-2026',
    tech: ['TypeScript', 'React Native', 'Firebase'],
    points: [
      'Written in TypeScript and JavaScript, with Firebase for the back end.',
      'Designed UI covering onboarding, home, and per-topic summary screens.',
      'Built as an A level NEA project, so release was held until after results day.',
    ],
    links: [],
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
    slug: 'autopet-feeder',
    title: 'AutoPet Feeder',
    blurb: 'An automated pet feeder, built to a real client specification.',
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
      { label: 'Source', href: 'https://github.com/milotek/petfeeder' },
      {
        label: 'Design document (PDF)',
        href: 'https://github.com/milotek/petfeeder/blob/master/Product%20Design%20NEA%20Edited.pdf',
      },
    ],
    shots: [],
  },
  {
    slug: 'ezcals',
    title: 'EZcals',
    blurb: 'Calorie tracker built around logging a meal in as few taps as possible.',
    status: 'shipped',
    year: '2024-2025',
    tech: ['Swift', 'SwiftUI', 'React Native'],
    points: [
      'Mobile app for iOS and Android.',
      'Designed for speed of logging rather than breadth of features.',
      'Tracks calories and macros.',
      'Originally Swift and SwiftUI, rewritten in React Native in 2025 for cross-platform support.',
    ],
    links: [],
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
]

export function getProject(slug: string): Project | undefined {
  return projects.find((project) => project.slug === slug)
}
