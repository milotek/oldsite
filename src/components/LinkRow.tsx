import type { Link as ProjectLink } from '../data/projects'
import { CodeIcon, DocumentIcon, LinkIcon, PlayIcon } from './Icons'

const glyphs = {
  code: CodeIcon,
  doc: DocumentIcon,
  demo: PlayIcon,
  link: LinkIcon,
} as const

export function LinkRow({ links }: { links: ProjectLink[] }) {
  if (links.length === 0) return null

  return (
    <ul className="compact">
      {links.map((link) => {
        const Glyph = glyphs[link.kind ?? 'link']
        return (
          <li key={link.href}>
            <a href={link.href} rel="noreferrer">
              <Glyph />
              {link.label}
            </a>
          </li>
        )
      })}
    </ul>
  )
}
