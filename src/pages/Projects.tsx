import Entry from '../components/Entry'
import PageHead from '../components/PageHead'
import { projects, projectsIntro } from '../data/projects'
import { github } from '../data/site'

export default function Projects() {
  return (
    <>
      <PageHead title="projects" description={projectsIntro} />

      <div className="page-head">
        <h1>Projects</h1>
        <p className="lede">
          {projectsIntro} Everything open source lives on <a href={github}>GitHub</a>.
        </p>
      </div>

      <div className="entries">
        {projects.map((project) => (
          <Entry key={project.slug} entry={project} />
        ))}
      </div>
    </>
  )
}
