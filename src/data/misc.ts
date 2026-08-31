/**
 * Served straight out of the profile repo so the graph stays current without
 * anything here needing to be rebuilt.
 */
export const contributionGraph =
  'https://raw.githubusercontent.com/pixeljammed/pixeljammed/refs/heads/main/profile-3d-contrib/profile-night-rainbow.svg'

export const soundcloudTrack = '1603513788'

export const soundcloudEmbed =
  `https://w.soundcloud.com/player/?url=${encodeURIComponent(
    `https://api.soundcloud.com/tracks/${soundcloudTrack}`,
  )}&show_artwork=true&show_comments=true&sharing=true&show_user=true&visual=false`

export const cv = {
  /** Vendored rather than framed from raw.githubusercontent, which serves the
   *  PDF as application/octet-stream and so downloads instead of rendering. */
  file: '/cv.pdf',
  source: 'https://github.com/pixeljammed/pixeljammed/blob/main/CV.pdf',
}
