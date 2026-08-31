import { useParams } from 'react-router'
import { projects, getProject } from '../data/projects'
import { Meta } from '../components/Meta'
import { PageHeader } from '../components/PageHeader'
import { Card } from '../components/Card'
import { LinkRow } from '../components/LinkRow'
import { NotFound } from './NotFound'

const ordered = [...projects].sort(
  (a, b) => Number(Boolean(b.featured)) - Number(Boolean(a.featured)),
)

export function Projects() {
  return (
    <>
      <Meta title="projects" description="Software and hardware projects by Milo Tekchandani." />
      <PageHeader
        title="projects"
        lede="Commercial apps, coursework that got out of hand, and one pet feeder."
      />
      <section className="card-grid">
        {ordered.map((project, index) => (
          <Card
            key={project.slug}
            to={`/projects/${project.slug}`}
            title={project.title}
            blurb={project.blurb}
            year={project.year}
            thumb={project.thumb}
            featured={project.featured}
            badge={project.status}
            eager={index < 2}
          />
        ))}
      </section>
    </>
  )
}

export function ProjectDetail() {
  const { slug } = useParams()
  const project = slug ? getProject(slug) : undefined

  if (!project) return <NotFound />

  return (
    <>
      <Meta title={project.title} description={project.blurb} />

      <section className="panel detail-head">
        <h1>{project.title}</h1>
        <p className="lede">{project.description ?? project.blurb}</p>
        <div className="tech-row">
          <span className="badge">{project.year}</span>
          <span className="badge accent">{project.status}</span>
          {project.tech.map((item) => (
            <span className="badge" key={item}>
              {item}
            </span>
          ))}
        </div>
        <LinkRow links={project.links} />
      </section>

      <section className="panel detail-body">
        <ul>
          {project.points.map((point) => (
            <li key={point}>{point}</li>
          ))}
        </ul>
      </section>

      {project.shots.length > 0 ? (
        <ul className="shots">
          {project.shots.map((shot) => (
            <li key={shot.src}>
              <figure>
                <img src={shot.src} alt={shot.alt} loading="lazy" />
                <figcaption>{shot.caption}</figcaption>
              </figure>
            </li>
          ))}
        </ul>
      ) : null}
    </>
  )
}
