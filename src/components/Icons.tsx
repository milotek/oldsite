/**
 * The site's icon set.
 *
 * Drawn here rather than pulled from an icon font because the alternative was
 * a webfont request to fonts.gstatic.com on every page load, for glyphs that
 * amount to a few hundred bytes of path data. Everything is on a 24x24 grid so
 * the whole set lines up at any size.
 *
 * `.icon` is stroked and inherits `currentColor`; `.icon-brand` is solid,
 * because a logo redrawn as an outline is no longer the logo.
 */
type IconProps = { className?: string }

function Icon({ children, className }: IconProps & { children: React.ReactNode }) {
  return (
    <svg
      className={className ? `icon ${className}` : 'icon'}
      viewBox="0 0 24 24"
      aria-hidden="true"
      focusable="false"
    >
      {children}
    </svg>
  )
}

function Brand({ path, className }: IconProps & { path: string }) {
  return (
    <svg
      className={className ? `icon-brand ${className}` : 'icon-brand'}
      viewBox="0 0 24 24"
      aria-hidden="true"
      focusable="false"
    >
      <path d={path} />
    </svg>
  )
}

export function HomeIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M3 10.6 12 3.4l9 7.2" />
      <path d="M5.6 9.6V20h12.8V9.6" />
      <path d="M9.6 20v-5.6h4.8V20" />
    </Icon>
  )
}

export function ProjectsIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M12 3.2 3.4 7.8 12 12.4l8.6-4.6z" />
      <path d="M3.4 12 12 16.6 20.6 12" />
      <path d="M3.4 16.2 12 20.8l8.6-4.6" />
    </Icon>
  )
}

export function GamesIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <rect x="2.6" y="7" width="18.8" height="10" rx="4" />
      <path d="M7.4 10.6v2.8M6 12h2.8" />
      <circle cx="16.4" cy="11.2" r="0.9" />
      <circle cx="18.4" cy="13.4" r="0.9" />
    </Icon>
  )
}

export function ArtIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M12 3.2a8.8 8.8 0 1 0 0 17.6 2 2 0 0 0 1.55-3.28 1.7 1.7 0 0 1 1.32-2.78h1.68A4.25 4.25 0 0 0 20.8 10.5C20.8 6.4 16.86 3.2 12 3.2Z" />
      <circle cx="7.6" cy="11.4" r="1" />
      <circle cx="10.2" cy="7.6" r="1" />
      <circle cx="14.6" cy="8.2" r="1" />
    </Icon>
  )
}

export function BlogIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <rect x="3.6" y="4" width="16.8" height="16" rx="1.6" />
      <path d="M7.2 8.6h6M7.2 12h9.6M7.2 15.4h9.6" />
    </Icon>
  )
}

export function CvIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M13.8 3.2H7a1.6 1.6 0 0 0-1.6 1.6v14.4A1.6 1.6 0 0 0 7 20.8h10a1.6 1.6 0 0 0 1.6-1.6V8z" />
      <path d="M13.8 3.2V8h4.8" />
      <path d="M8.6 12.6h6.8M8.6 16h4.8" />
    </Icon>
  )
}

export function MiscIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <circle cx="12" cy="12" r="8.8" />
      <path d="M12 16.8v-4.4M12 8.2h.01" />
    </Icon>
  )
}

export function CalendarIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <rect x="3.6" y="5.2" width="16.8" height="15.2" rx="1.6" />
      <path d="M8.2 3.2v4M15.8 3.2v4M3.6 10h16.8" />
    </Icon>
  )
}

export function TrophyIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M8 4h8v5.2a4 4 0 0 1-8 0z" />
      <path d="M8 5.6H5.2v1.2a3.2 3.2 0 0 0 2.9 3.2M16 5.6h2.8v1.2a3.2 3.2 0 0 1-2.9 3.2" />
      <path d="M12 13.2V17M8.8 20h6.4" />
    </Icon>
  )
}

export function CodeIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M9 7.6 4.6 12 9 16.4M15 7.6 19.4 12 15 16.4" />
    </Icon>
  )
}

export function LinkIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M14 4h6v6M20 4l-8.6 8.6" />
      <path d="M18 14v5.2a1.6 1.6 0 0 1-1.6 1.6H5.6A1.6 1.6 0 0 1 4 19.2V8.4a1.6 1.6 0 0 1 1.6-1.6H10" />
    </Icon>
  )
}

export function DownloadIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M12 4v11M8 11.4l4 4 4-4M4.6 19.6h14.8" />
    </Icon>
  )
}

export function DocumentIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M13.8 3.2H7a1.6 1.6 0 0 0-1.6 1.6v14.4A1.6 1.6 0 0 0 7 20.8h10a1.6 1.6 0 0 0 1.6-1.6V8z" />
      <path d="M13.8 3.2V8h4.8" />
    </Icon>
  )
}

export function TagIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M3.6 11.6V4.8a1.2 1.2 0 0 1 1.2-1.2h6.8l8.8 8.8-8 8z" />
      <circle cx="8" cy="8" r="1.2" />
    </Icon>
  )
}

export function RssIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <circle cx="5.4" cy="18.6" r="1.2" />
      <path d="M4.8 12.4a6.8 6.8 0 0 1 6.8 6.8M4.8 6.2a13 13 0 0 1 13 13" />
    </Icon>
  )
}

export function MailIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <rect x="2.6" y="5" width="18.8" height="14" rx="1.6" />
      <path d="M3.2 6.6 12 13l8.8-6.4" />
    </Icon>
  )
}

export function PlayIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M8.4 5.4v13.2L19 12z" />
    </Icon>
  )
}

export function MusicIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M9.2 17.6V6.2l10.4-2v11.4" />
      <circle cx="6.6" cy="17.6" r="2.6" />
      <circle cx="17" cy="15.6" r="2.6" />
    </Icon>
  )
}

export function SparkIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="m12 3.4 2.2 5.3 5.3 2.2-5.3 2.2-2.2 5.3-2.2-5.3-5.3-2.2 5.3-2.2z" />
    </Icon>
  )
}

export function BrokenImageIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M20.4 12V6a1.6 1.6 0 0 0-1.6-1.6H5.2A1.6 1.6 0 0 0 3.6 6v12a1.6 1.6 0 0 0 1.6 1.6h7.4" />
      <path d="M3.6 14.6 7.4 11l3.2 3M14.4 11.4 16.6 9.4l3.8 3.4" />
      <path d="M16.4 16.2h5.2M19 13.6v5.2" />
    </Icon>
  )
}

export function ImageIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <rect x="3.6" y="4.4" width="16.8" height="15.2" rx="1.6" />
      <circle cx="8.8" cy="9.4" r="1.4" />
      <path d="M3.6 16.4 8.6 11.6l4.2 4 2.8-2.6 5.2 4.6" />
    </Icon>
  )
}

export function ArrowRightIcon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M4.6 12h14.8M13.4 6l6 6-6 6" />
    </Icon>
  )
}

// Brand marks below, path data from simple-icons.org (CC0 1.0).

export function GitHubIcon(props: IconProps) {
  return (
    <Brand
      {...props}
      path="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
    />
  )
}

export function LinkedInIcon(props: IconProps) {
  return (
    <Brand
      {...props}
      path="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"
    />
  )
}

export function InstagramIcon(props: IconProps) {
  return (
    <Brand
      {...props}
      path="M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558.788-.306 1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06zm0 3.678a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm7.846-10.405a1.441 1.441 0 0 1-2.88 0 1.44 1.44 0 0 1 2.88 0z"
    />
  )
}

export function SpotifyIcon(props: IconProps) {
  return (
    <Brand
      {...props}
      path="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"
    />
  )
}
