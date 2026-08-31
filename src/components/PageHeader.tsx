import type { ReactNode } from 'react'

export function PageHeader({ title, lede }: { title: string; lede?: ReactNode }) {
  return (
    <div className="page-header">
      <h1>{title}</h1>
      {lede ? <p className="lede">{lede}</p> : null}
    </div>
  )
}
