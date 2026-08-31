import type { Entry } from './types'

export const projectsIntro = 'Both hardware and software projects.'

export const projects: Entry[] = [
  {
    slug: 'lockyn',
    title: 'Lockyn',
    summary: 'Commercial mobile studying app for GCSE and sixth form students.',
    status: 'To be released 2026',
    points: [
      'Written in TypeScript and JavaScript, with Firebase for the back end.',
      'Fluent, professionally designed UI.',
      "Can't release until after A level results day - it's an NEA project.",
    ],
    shotShape: 'tall',
    shots: [
      {
        src: '/shots/lockyn_landing.jpg',
        alt: 'Lockyn landing screen: a pink to blue gradient circle above the text "welcome to lockyn" and a sign in with email button.',
        caption: 'landing page',
      },
      {
        src: '/shots/lockyn_onboarding.jpg',
        alt: 'Lockyn onboarding screen.',
        caption: 'onboarding',
      },
      { src: '/shots/lockyn_home.jpg', alt: 'Lockyn home screen.', caption: 'home' },
      {
        src: '/shots/lockyn_summary.jpg',
        alt: 'Lockyn study session summary screen.',
        caption: 'summary page',
      },
    ],
  },
  {
    slug: 'autopet-feeder',
    title: 'AutoPet Feeder',
    summary: 'Hardware project - a fully automated luxury pet feeder.',
    points: [
      "IoT project designed and tailored to a client's specification - my neighbours.",
      'Custom designed, developed and engineered software and hardware.',
      'Powered by a Raspberry Pi, a servo and JavaScript.',
      'Touchscreen and USB-C power for ease of use.',
      'ABS plastic 3D printed shell with an oak wood finish.',
    ],
    links: [
      {
        label: 'Full design document',
        href: 'https://github.com/pixeljammed/petfeeder/blob/master/Product%20Design%20NEA%20Edited.pdf',
      },
      { label: 'Source on GitHub', href: 'https://github.com/pixeljammed/petfeeder' },
    ],
    shotShape: 'wide',
    shots: [
      {
        src: '/shots/petfeeder_cardboard_prototype.jpg',
        alt: 'Slide titled "Cardboard prototype iteration model #1" showing photographs of a cardboard mock-up of the feeder alongside written client feedback.',
        caption: 'cardboard prototype, iteration #1',
      },
      {
        src: '/shots/petfeeder_second_model.jpg',
        alt: 'Slide showing a flatter second design model with separate food and water compartments, with annotated cut nets and evaluation notes.',
        caption: 'second model - flatter, more portable',
      },
      {
        src: '/shots/petfeeder_electronics.jpg',
        alt: 'Slide titled "Electronic Equipment // Raspberry PI Stuff" showing photographs of a Raspberry Pi 3B with a 3.5 inch touchscreen and a parts price list.',
        caption: 'Raspberry Pi internals and parts list',
      },
      {
        src: '/shots/petfeeder_completed.jpg',
        alt: 'Photographs of the completed 3D printed feeder shell in white ABS with an oak wood lid.',
        caption: 'completed exterior',
      },
      {
        src: '/shots/petfeeder_slide_deck.jpg',
        alt: 'Contact sheet of every slide in the Product Design NEA document.',
        caption: 'the full design document',
      },
    ],
  },
  {
    slug: 'ezcals',
    title: 'EZcals',
    summary:
      'Source available calorie tracking app for people wanting to lose or gain weight.',
    points: [
      'Mobile application for iOS and Android.',
      'Designed for ease of use and simplicity, to cut down the time spent logging food.',
      'Logs calories, protein, fat and the rest.',
      'Originally written entirely in Swift and SwiftUI; rewritten in React Native for cross-platform support in 2025.',
    ],
  },
]
