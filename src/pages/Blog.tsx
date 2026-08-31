import { Link, useParams } from 'react-router'
import { posts, getPost } from '../lib/blog'
import { Meta } from '../components/Meta'
import { PageHeader } from '../components/PageHeader'
import { TagIcon } from '../components/Icons'
import { NotFound } from './NotFound'

export function Blog() {
  return (
    <>
      <Meta title="blog" description="Writing by Milo Tekchandani." />
      <PageHeader title="blog" lede="Notes on things I have built, and things I got wrong." />

      <div className="panel">
        <p className="subt" style={{ margin: 0 }}>
          Opinions here are mine and do not reflect those of any employer, past, present or future.
        </p>
      </div>

      {posts.length === 0 ? (
        <p className="lede" style={{ marginTop: '1.5rem' }}>
          Nothing published yet.
        </p>
      ) : (
        <div className="blog-list">
          {posts.map((post) => (
            <article
              key={post.slug}
              className={`blog-item${post.image ? ' has-cover' : ''}`}
              style={post.image ? ({ '--cover': `url("${post.image}")` } as React.CSSProperties) : undefined}
            >
              <Link className="blog-link" to={`/blog/${post.slug}`} viewTransition>
                <h3>{post.title}</h3>
                {post.description ? <p className="post-desc">{post.description}</p> : null}
                <div className="post-footer">
                  {post.tags.length > 0 ? (
                    <div className="post-tags">
                      <TagIcon />
                      {post.tags.map((tag) => (
                        <span className="tag" key={tag}>
                          {tag}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span />
                  )}
                  <time dateTime={post.date}>{post.date}</time>
                </div>
              </Link>
            </article>
          ))}
        </div>
      )}
    </>
  )
}

export function BlogPost() {
  const { slug } = useParams()
  const post = slug ? getPost(slug) : undefined

  if (!post) return <NotFound />

  return (
    <>
      <Meta title={post.title} description={post.description} />

      <div className="page-header">
        <h1 className="post-title">{post.title}</h1>
        {post.description ? <p className="lede">{post.description}</p> : null}
        <div className="post-footer" style={{ justifyContent: 'flex-start', gap: '1rem' }}>
          <time dateTime={post.date}>{post.date}</time>
          {post.tags.length > 0 ? (
            <div className="post-tags">
              <TagIcon />
              {post.tags.map((tag) => (
                <span className="tag" key={tag}>
                  {tag}
                </span>
              ))}
            </div>
          ) : null}
        </div>
      </div>

      {/* The Markdown is compiled from files in this repository at build time.
          There is no user-submitted content anywhere in this pipeline. */}
      <article
        className="panel post-body"
        dangerouslySetInnerHTML={{ __html: post.html }}
      />

      <p style={{ marginTop: '1.5rem' }}>
        <Link to="/blog" viewTransition>
          back to all posts
        </Link>
      </p>
    </>
  )
}
