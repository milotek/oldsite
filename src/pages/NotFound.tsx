import { Link } from 'react-router'

export function NotFound() {
  return (
    <div className="stack">
      <p className="eyebrow">404</p>
      <h1>Not found</h1>
      <p className="lede">
        That page does not exist. Try <Link to="/">the front page</Link>.
      </p>
    </div>
  )
}
