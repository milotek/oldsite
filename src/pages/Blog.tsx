import { Link } from 'react-router'
import { posts, formatDate } from '../lib/content'

export function Blog() {
  return (
    <div className="stack">
      <header>
        <p className="eyebrow">blog</p>
        <h1>Writing</h1>
        <p className="lede">
          Written in Obsidian, published from the vault. Subscribe:{' '}
          <a href="/rss.xml">RSS</a>, <a href="/atom.xml">Atom</a>,{' '}
          <a href="/feed.json">JSON</a>.
        </p>
      </header>

      {posts.length === 0 ? (
        <p className="lede">
          Nothing published yet. Add <code>publish: true</code> and{' '}
          <code>type: post</code> to a note&rsquo;s frontmatter.
        </p>
      ) : (
        <ul className="card-list">
          {posts.map((post) => (
            <li key={post.slug} className="card">
              <h3>
                <Link to={`/blog/${post.slug}`}>{post.title}</Link>
              </h3>
              {post.description && <p>{post.description}</p>}
              <div className="meta">
                <span>{formatDate(post.date)}</span>
                {post.tags.map((tag) => (
                  <span key={tag} className="tag">
                    {tag}
                  </span>
                ))}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
