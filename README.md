# milotek.dev

Personal site, generated from Markdown and YAML by `build.py`.
Live at https://furfag.lol/MLGSwag/.

## Editing

Everything you would ever change lives in `content/`.

- `content/projects/<slug>.md`: one file per project. Front matter holds the title, summary, year, tags, repo, links and images; the body is Markdown.
- `content/posts/YYYY-MM-DD-<slug>.md`: one file per post. The date comes from the filename unless the front matter has one. `draft: true` hides a post.
- `content/pages/<slug>.md`: now, uses, colophon and any other standalone page. The slug becomes the URL.
- `content/home.md`: the intro paragraphs on the front page.
- `content/art.yaml`: the drawings on the art page. Full-size images go in `static/img/art/`, thumbnails in `static/img/art/thumbs/`.
- `content/buttons.yaml`: the 88x31 buttons in the footer. Drop the gif in `static/buttons/` and add a line.
- `content/site.yaml`: name, URL, navigation and social links.

Links in Markdown can be root-relative (`/colophon/`, `/static/img/foo.webp`).
The build rewrites them so the site works under a subpath.

## Building

```sh
uv run build.py
```

Output is written next to the sources (`index.html`, `blog/`, `projects/`, and so on) and committed, because GitHub Pages serves the repository root as-is.

## Previewing

```sh
python3 -m http.server 8723 --bind 127.0.0.1
```
