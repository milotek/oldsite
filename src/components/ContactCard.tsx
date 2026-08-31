import type { ReactNode } from 'react'

export function ContactCard({
  platform,
  handle,
  href,
  icon,
  compact,
}: {
  platform: string
  handle: string
  href: string
  icon: ReactNode
  compact?: boolean
}) {
  const external = href.startsWith('http')

  if (compact) {
    return (
      <a
        className="contact-card compact"
        href={href}
        rel={external ? 'me noreferrer' : undefined}
      >
        {icon}
        <span className="contact-text">
          <span className="contact-platform">{platform}</span>
          <span className="contact-handle">{handle}</span>
        </span>
      </a>
    )
  }

  return (
    <a className="contact-card" href={href} rel={external ? 'me noreferrer' : undefined}>
      <p className="contact-platform">
        {icon}
        {platform}
      </p>
      <p className="contact-handle">{handle}</p>
    </a>
  )
}
