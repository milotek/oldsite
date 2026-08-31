import type { ReactNode } from 'react'

export function PageHead({
  eyebrow,
  title,
  lede,
}: {
  eyebrow: string
  title: string
  lede?: ReactNode
}) {
  return (
    <div className="page-head">
      <p className="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      {lede ? <p className="lede">{lede}</p> : null}
    </div>
  )
}
