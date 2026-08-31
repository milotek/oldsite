export interface Shot {
  src: string
  alt: string
  caption: string
}

export interface Link {
  label: string
  href: string
}

/** A project, game or piece of work with a write-up and optional screenshots. */
export interface Entry {
  slug: string
  title: string
  summary: string
  /** Rendered as a list; each string is one plain line of prose. */
  points: string[]
  status?: string
  links?: Link[]
  shots?: Shot[]
  /**
   * Phone screenshots and full-page document scans need very different column
   * widths; without this a portrait screenshot stretches to a comical height.
   */
  shotShape?: 'tall' | 'wide'
  video?: { title: string; youtubeId: string }
}
