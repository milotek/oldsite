import { useParams } from 'react-router'
import { getProject, projects } from '../data/projects'
import { Entry } from '../components/Entry'
import { Detail } from '../components/Detail'
import { PageHead } from '../components/PageHead'
import { NotFound } from './NotFound'
import { Meta } from '../components/Meta'

export function Projects() {
  return (
    <>
      <Meta title="Projects" description="Hardware and software projects by Milo Tekchandani." />
      <PageHead
        eyebrow="Work"
        title="Projects"
        lede="Hardware and software, built for coursework, for clients, and for the hell of it."
      />
      <ul className="entries">
        {projects.map((project, index) => (
          <Entry
            key={project.slug}
            index={index}
            to={`/projects/${project.slug}`}
            title={project.title}
            blurb={project.blurb}
            year={project.year}
            tech={project.tech}
            status={project.status}
          />
        ))}
      </ul>
    </>
  )
}

export function ProjectDetail() {
  const { slug } = useParams()
  const project = slug ? getProject(slug) : undefined
  if (!project) return <NotFound />

  return (
    <Detail
      backTo="/projects"
      backLabel="projects"
      eyebrow="Project"
      title={project.title}
      blurb={project.blurb}
      year={project.year}
      tech={project.tech}
      status={project.status}
      points={project.points}
      links={project.links}
      shots={project.shots}
    />
  )
}
