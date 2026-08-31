import { Link } from 'react-router'
import { Meta } from '../components/Meta'
import { BrokenImageIcon, HomeIcon, ProjectsIcon, BlogIcon } from '../components/Icons'

export function NotFound() {
  return (
    <div className="notfound">
      <Meta title="404" description="Page not found." />
      <div className="notfound-mark">
        <BrokenImageIcon />
        <h1>whoops</h1>
      </div>
      <p>That page does not exist.</p>
      <ul className="compact">
        <li>
          <Link to="/" className="nav-link" viewTransition>
            <HomeIcon />
            home
          </Link>
        </li>
        <li>
          <Link to="/projects" className="nav-link" viewTransition>
            <ProjectsIcon />
            projects
          </Link>
        </li>
        <li>
          <Link to="/blog" className="nav-link" viewTransition>
            <BlogIcon />
            blog
          </Link>
        </li>
      </ul>
    </div>
  )
}
