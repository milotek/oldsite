import { Link } from 'react-router-dom'
import PageHead from '../components/PageHead'

export default function NotFound() {
  return (
    <>
      <PageHead title="not found" />

      <div className="page-head">
        <h1>404</h1>
        <p className="lede">
          Nothing here. <Link to="/">Back to the start</Link>.
        </p>
      </div>
    </>
  )
}
