#!/usr/bin/env python3
"""Builds the site: reads content/ and static/, writes HTML to the repo root.

GitHub Pages serves plain files from the repo root, so the output lives next to
the sources and is committed. Run `python3 build.py` after editing anything.
"""

from __future__ import annotations

import html
import re
import shutil
import sys
import tomllib
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
CONTENT = ROOT / "content"
STATIC = ROOT / "static"

# Generated files and directories, cleared on every build. Anything not listed
# here is source and never touched.
OUTPUTS = [
    "index.html",
    "404.html",
    "feed.xml",
    "sitemap.xml",
    "assets",
    "projects",
    "art",
    "blog",
    "now",
    "uses",
    "cv",
    "colophon",
]


# --------------------------------------------------------------------------
# content loading
# --------------------------------------------------------------------------


def parse_front_matter(raw: str) -> tuple[dict, str]:
    """Splits Obsidian-style `---` front matter from the body.

    Supports `key: value` and block lists of plain strings. That covers every
    field the templates read, and keeps a post copied out of the vault valid.
    """
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    head = raw[3:end]
    body = raw[end + 4 :].lstrip("\n")

    meta: dict = {}
    key = None
    for line in head.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and line.lstrip().startswith("- "):
            if key is None:
                continue
            meta.setdefault(key, [])
            if not isinstance(meta[key], list):
                meta[key] = []
            meta[key].append(unquote(line.lstrip()[2:].strip()))
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        meta[key] = unquote(value) if value else []
    return meta, body


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def as_list(value) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    return [part.strip() for part in value.split(",") if part.strip()]


def pipe_pairs(values: list[str]) -> list[tuple[str, str]]:
    """`label | target` entries, used for links and images."""
    out = []
    for entry in values:
        left, _, right = entry.partition("|")
        out.append((left.strip(), right.strip()))
    return out


def truthy(value) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def load_docs(folder: Path) -> list[dict]:
    docs = []
    for path in sorted(folder.glob("*.md")):
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        if truthy(meta.get("draft", "")):
            continue
        meta["slug"] = meta.get("slug") or path.stem
        meta["body"] = body
        docs.append(meta)
    return docs


# --------------------------------------------------------------------------
# markdown
# --------------------------------------------------------------------------

INLINE_CODE = re.compile(r"`([^`]+)`")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
EM = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def inline(text: str, base: str) -> str:
    slots: list[str] = []

    def stash(markup: str) -> str:
        slots.append(markup)
        return f"\x00{len(slots) - 1}\x00"

    text = INLINE_CODE.sub(lambda m: stash(f"<code>{esc(m.group(1))}</code>"), text)
    text = esc(text)
    text = IMAGE.sub(
        lambda m: stash(
            f'<img src="{url(m.group(2), base)}" alt="{m.group(1)}" loading="lazy">'
        ),
        text,
    )
    text = LINK.sub(
        lambda m: stash(f'<a href="{url(m.group(2), base)}">{m.group(1)}</a>'), text
    )
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = EM.sub(r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: slots[int(m.group(1))], text)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def markdown(src: str, base: str) -> str:
    lines = src.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            out.append(f"<pre><code>{esc(chr(10).join(code))}</code></pre>")
            continue

        if re.fullmatch(r"(-{3,}|\*{3,})", stripped):
            out.append("<hr>")
            i += 1
            continue

        heading = re.match(r"(#{1,6})\s+(.*)", stripped)
        if heading:
            level = len(heading.group(1))
            text = inline(heading.group(2), base)
            anchor = slugify(heading.group(2))
            out.append(f'<h{level} id="{anchor}">{text}</h{level}>')
            i += 1
            continue

        if stripped.startswith("> "):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(quote), base)}</p></blockquote>")
            continue

        bullet = re.match(r"([-*])\s+(.*)", stripped)
        number = re.match(r"\d+\.\s+(.*)", stripped)
        if bullet or number:
            tag = "ul" if bullet else "ol"
            items = []
            pattern = r"([-*])\s+(.*)" if bullet else r"\d+\.\s+(.*)"
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                match = re.match(pattern, lines[i].strip())
                items.append(match.group(2) if bullet else match.group(1))
                i += 1
            body = "".join(f"<li>{inline(item, base)}</li>" for item in items)
            out.append(f"<{tag}>{body}</{tag}>")
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not re.match(
            r"(#{1,6}\s|[-*]\s|\d+\.\s|>\s|```|-{3,}$)", lines[i].strip()
        ):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para), base)}</p>")

    return "\n".join(out)


def first_paragraph(body: str) -> str:
    for block in body.split("\n\n"):
        block = block.strip()
        if block and not block.startswith(("#", "-", ">", "!", "`")):
            return block
    return ""


# --------------------------------------------------------------------------
# templating
# --------------------------------------------------------------------------


def url(path: str, base: str) -> str:
    """Resolves a site-absolute path against the deploy base path."""
    if re.match(r"^(https?:|mailto:|#|data:)", path):
        return path
    return base + path.lstrip("/")


def layout(site, *, title, body, base, description="", page_class="", extra_head=""):
    nav = "".join(
        f'<a href="{url(item["href"], base)}">{esc(item["label"])}</a>'
        for item in site["nav"]
    )
    social = "".join(
        f'<a href="{esc(link["href"])}" rel="me">{esc(link["label"])}</a>'
        for link in site["links"]
    )
    full_title = title if title == site["title"] else f"{title} — {site['title']}"
    description = description or site["description"]
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="author" content="{esc(site["author"])}">
<meta name="theme-color" content="#1e1e2e">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{site["url"]}assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{url('/assets/img/favicon.png', base)}" type="image/png">
<link rel="apple-touch-icon" href="{url('/assets/img/apple-touch-icon.png', base)}">
<link rel="alternate" type="application/rss+xml" title="{esc(site["title"])}" href="{url('/feed.xml', base)}">
<link rel="stylesheet" href="{url('/assets/css/style.css', base)}">
{extra_head}</head>
<body class="{page_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="wrap bar">
    <a class="mark" href="{url('/', base)}">
      <img src="{url('/assets/img/favicon.png', base)}" alt="" width="26" height="26">
      <span>milo tek</span>
    </a>
    <nav>{nav}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-cols">
      <div>
        <h2>Elsewhere</h2>
        <div class="foot-links">{social}</div>
      </div>
      <div>
        <h2>This site</h2>
        <div class="foot-links">
          <a href="{url('/colophon/', base)}">Colophon</a>
          <a href="{url('/feed.xml', base)}">RSS</a>
          <a href="{esc(site["repo"])}">Source</a>
        </div>
      </div>
    </div>
    <p class="fine">&copy; {datetime.now().year} {esc(site["author"])}. Built by hand in {esc(site["place"])}.</p>
  </div>
</footer>
</body>
</html>
"""


def page(site, base, *, eyebrow, title, lede="", body="", wide=False):
    head = f'<p class="eyebrow">{esc(eyebrow)}</p>' if eyebrow else ""
    lede_html = f'<p class="lede">{inline(lede, base)}</p>' if lede else ""
    return f"""<div class="wrap{' wide' if wide else ''}">
  <div class="page-head">
    {head}
    <h1>{esc(title)}</h1>
    {lede_html}
  </div>
  {body}
</div>"""


def tag_list(tags: list[str]) -> str:
    if not tags:
        return ""
    chips = "".join(f"<li>{esc(tag)}</li>" for tag in tags)
    return f'<ul class="tags">{chips}</ul>'


def link_row(links: list[tuple[str, str]], base: str) -> str:
    if not links:
        return ""
    items = "".join(
        f'<a href="{esc(href)}">{esc(label)} <span aria-hidden="true">&rarr;</span></a>'
        for label, href in links
    )
    return f'<div class="linkrow">{items}</div>'



# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------


def project_card(project, base, *, compact=False) -> str:
    images = pipe_pairs(as_list(project.get("images")))
    links = pipe_pairs(as_list(project.get("links")))
    has_page = bool(project["body"].strip()) or len(images) > 1
    href = url(f"/projects/{project['slug']}/", base) if has_page else None

    shot = ""
    if images and not compact:
        src, caption = images[0]
        shot = (
            f'<div class="card-shot {esc(project.get("shot_fit", "cover"))}">'
            f'<img src="{url(src, base)}" alt="{esc(caption)}" loading="lazy"></div>'
        )

    title = esc(project["title"])
    if href:
        title = f'<a href="{href}">{title}</a>'

    meta = []
    if project.get("year"):
        meta.append(esc(project["year"]))
    if project.get("role"):
        meta.append(esc(project["role"]))
    meta_html = f'<p class="card-meta">{" &middot; ".join(meta)}</p>' if meta else ""

    return f"""<article class="card{' compact' if compact else ''}">
  {shot}
  <div class="card-body">
    <h3>{title}</h3>
    {meta_html}
    <p>{inline(project.get("blurb", ""), base)}</p>
    {tag_list(as_list(project.get("tags")))}
    {link_row(links, base)}
  </div>
</article>"""


def build_home(site, base, projects, posts, pages_by_slug):
    home = pages_by_slug["home"]
    featured = [p for p in projects if truthy(p.get("featured"))][:4]
    cards = "".join(project_card(p, base) for p in featured)

    post_items = ""
    for post in posts[:2]:
        post_items += f"""<a class="post-row" href="{url(f'/blog/{post["slug"]}/', base)}">
      <span class="post-date">{esc(post.get("date", ""))}</span>
      <span class="post-title">{esc(post["title"])}</span>
    </a>"""

    social = "".join(
        f'<a href="{esc(link["href"])}" rel="me">{esc(link["label"])}</a>'
        for link in site["links"]
    )

    return f"""<div class="wrap wide">
  <section class="hero">
    <img class="portrait" src="{url('/assets/img/avatar.png', base)}" alt="" width="120" height="114">
    <div>
      <h1>{esc(site["author_short"])}</h1>
      <p class="role">{inline(site["role"], base)}</p>
      {markdown(home["body"], base)}
      <div class="linkrow hero-links">{social}<a href="{url('/cv/', base)}">CV <span aria-hidden="true">&rarr;</span></a></div>
    </div>
  </section>

  <section class="block">
    <div class="block-head">
      <h2>Selected work</h2>
      <a href="{url('/projects/', base)}">All projects <span aria-hidden="true">&rarr;</span></a>
    </div>
    <div class="grid">{cards}</div>
  </section>

  <section class="block split">
    <div>
      <div class="block-head"><h2>Writing</h2><a href="{url('/blog/', base)}">All posts <span aria-hidden="true">&rarr;</span></a></div>
      <div class="post-list">{post_items}</div>
    </div>
    <div>
      <div class="block-head"><h2>Also here</h2></div>
      <div class="post-list">
        <a class="post-row" href="{url('/art/', base)}"><span class="post-date">art</span><span class="post-title">Drawings, concept art and backgrounds</span></a>
        <a class="post-row" href="{url('/now/', base)}"><span class="post-date">now</span><span class="post-title">What I'm doing at the moment</span></a>
        <a class="post-row" href="{url('/uses/', base)}"><span class="post-date">uses</span><span class="post-title">The kit I actually use</span></a>
      </div>
    </div>
  </section>
</div>"""


def build_projects(site, base, projects):
    groups: dict[str, list] = {}
    for project in projects:
        groups.setdefault(project.get("group", "Projects"), []).append(project)

    body = ""
    for name, items in groups.items():
        compact = all(not as_list(p.get("images")) for p in items)
        cards = "".join(project_card(p, base, compact=compact) for p in items)
        body += f"""<section class="block">
  <div class="block-head"><h2>{esc(name)}</h2></div>
  <div class="grid{' tight' if compact else ''}">{cards}</div>
</section>"""

    return page(
        site,
        base,
        eyebrow="Projects",
        title="Things I've built",
        lede=site["projects_lede"],
        body=body,
        wide=True,
    )


def build_project_page(site, base, project):
    images = pipe_pairs(as_list(project.get("images")))
    links = pipe_pairs(as_list(project.get("links")))
    gallery = ""
    if images:
        fit = project.get("shot_fit", "cover")
        shots = "".join(
            f'<figure class="{esc(fit)}">'
            f'<a href="{url(src, base)}"><img src="{url(src, base)}" alt="{esc(caption)}" loading="lazy"></a>'
            + (f"<figcaption>{esc(caption)}</figcaption>" if caption else "")
            + "</figure>"
            for src, caption in images
        )
        gallery = f'<div class="shots {esc(project.get("gallery", "wide"))}">{shots}</div>'

    meta = []
    if project.get("year"):
        meta.append(("Year", esc(project["year"])))
    if project.get("role"):
        meta.append(("Role", esc(project["role"])))
    if project.get("status"):
        meta.append(("Status", esc(project["status"])))
    meta_html = ""
    if meta:
        rows = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in meta)
        meta_html = f'<dl class="factsheet">{rows}</dl>'

    body = f"""{meta_html}
{tag_list(as_list(project.get("tags")))}
{link_row(links, base)}
<div class="prose">{markdown(project["body"], base)}</div>
{gallery}
<p class="backlink"><a href="{url('/projects/', base)}">&larr; All projects</a></p>"""

    return page(
        site,
        base,
        eyebrow="Project",
        title=project["title"],
        lede=project.get("blurb", ""),
        body=body,
    )


def build_art(site, base, art):
    items = ""
    for entry in art:
        src = entry["src"]
        stem, dot, ext = src.rpartition(".")
        items += f"""<figure>
  <a href="{url(src, base)}"><img src="{url(f"{stem}-thumb{dot}{ext}", base)}" alt="{esc(entry["caption"])}" loading="lazy"></a>
  <figcaption>{esc(entry["caption"])}{f' <span>{esc(entry["year"])}</span>' if entry.get("year") else ''}</figcaption>
</figure>"""
    return page(
        site,
        base,
        eyebrow="Art",
        title="Drawings",
        lede=site["art_lede"],
        body=f'<div class="gallery">{items}</div>',
        wide=True,
    )


def build_blog_index(site, base, posts):
    rows = ""
    for post in posts:
        rows += f"""<article class="entry">
  <p class="entry-date">{esc(post.get("date", ""))}</p>
  <h2><a href="{url(f'/blog/{post["slug"]}/', base)}">{esc(post["title"])}</a></h2>
  <p>{inline(post.get("summary") or first_paragraph(post["body"]), base)}</p>
</article>"""
    return page(
        site,
        base,
        eyebrow="Blog",
        title="Posts",
        lede=site["blog_lede"],
        body=f'<div class="entries">{rows}</div><p class="backlink"><a href="{url("/feed.xml", base)}">RSS feed</a></p>',
    )


def build_post(site, base, post):
    body = f"""<div class="prose">{markdown(post["body"], base)}</div>
<p class="backlink"><a href="{url('/blog/', base)}">&larr; All posts</a></p>"""
    return page(
        site,
        base,
        eyebrow=post.get("date", "Post"),
        title=post["title"],
        lede=post.get("summary", ""),
        body=body,
    )


def build_simple(site, base, doc, extra=""):
    body = f'<div class="prose">{markdown(doc["body"], base)}</div>{extra}'
    return page(
        site,
        base,
        eyebrow=doc.get("eyebrow", ""),
        title=doc["title"],
        lede=doc.get("lede", ""),
        body=body,
    )


def build_colophon(site, base, doc, buttons):
    mine = "".join(
        f'<img src="{url(b["src"], base)}" alt="{esc(b["alt"])}" width="88" height="31">'
        for b in buttons
        if truthy(b.get("mine"))
    )
    others = "".join(
        f'<a href="{esc(b["href"])}"><img src="{url(b["src"], base)}" alt="{esc(b["alt"])}" width="88" height="31"></a>'
        for b in buttons
        if not truthy(b.get("mine"))
    )
    extra = f"""<section class="block buttons">
  <div class="block-head"><h2>Take a button</h2></div>
  <p class="note">88&times;31. Hotlink it or save it, either is fine.</p>
  <div class="button-wall own">{mine}</div>
  <p class="note">Things I like. There is room for more.</p>
  <div class="button-wall">{others}</div>
</section>"""
    return build_simple(site, base, doc, extra)


def build_cv(site, base, doc):
    extra = f"""<div class="pdf">
  <object data="{url('/assets/cv.pdf', base)}#view=FitH" type="application/pdf">
    <p>Your browser will not show the PDF inline. <a href="{url('/assets/cv.pdf', base)}">Download it instead.</a></p>
  </object>
</div>"""
    return build_simple(site, base, doc, extra)


def build_feed(site, posts):
    now = format_datetime(datetime.now(timezone.utc))
    items = ""
    for post in posts:
        link = f"{site['url']}blog/{post['slug']}/"
        published = datetime.strptime(post["date"], "%Y-%m-%d").replace(
            tzinfo=timezone.utc
        )
        summary = post.get("summary") or first_paragraph(post["body"])
        items += f"""    <item>
      <title>{esc(post["title"])}</title>
      <link>{esc(link)}</link>
      <guid isPermaLink="true">{esc(link)}</guid>
      <pubDate>{format_datetime(published)}</pubDate>
      <description>{esc(summary)}</description>
    </item>
"""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{esc(site["title"])}</title>
    <link>{esc(site["url"])}</link>
    <atom:link href="{esc(site["url"])}feed.xml" rel="self" type="application/rss+xml"/>
    <description>{esc(site["description"])}</description>
    <language>en-gb</language>
    <lastBuildDate>{now}</lastBuildDate>
{items}  </channel>
</rss>
"""


def build_sitemap(site, paths):
    urls = "".join(f"  <url><loc>{esc(site['url'] + p)}</loc></url>\n" for p in paths)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>
"""


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------


def write(path: Path, text: str, written: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    written.append(str(path.relative_to(ROOT)))


def main() -> int:
    site = tomllib.loads((ROOT / "site.toml").read_text(encoding="utf-8"))
    base = site["base"]

    for name in OUTPUTS:
        target = ROOT / name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()

    shutil.copytree(STATIC, ROOT / "assets")

    projects = load_docs(CONTENT / "projects")
    projects.sort(key=lambda p: int(p.get("order", 999)))
    posts = load_docs(CONTENT / "posts")
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    pages = {doc["slug"]: doc for doc in load_docs(CONTENT / "pages")}
    art = tomllib.loads((CONTENT / "art.toml").read_text(encoding="utf-8"))["art"]
    buttons = tomllib.loads((CONTENT / "buttons.toml").read_text(encoding="utf-8"))[
        "button"
    ]

    written: list[str] = []
    routes = [""]

    def emit(route: str, title: str, body: str, description=""):
        target = ROOT / (route + "index.html") if route else ROOT / "index.html"
        write(
            target,
            layout(site, title=title, body=body, base=base, description=description),
            written,
        )
        routes.append(route)

    write(
        ROOT / "index.html",
        layout(
            site,
            title=site["title"],
            body=build_home(site, base, projects, posts, pages),
            base=base,
            page_class="home",
        ),
        written,
    )

    emit("projects/", "Projects", build_projects(site, base, projects))
    for project in projects:
        images = pipe_pairs(as_list(project.get("images")))
        if project["body"].strip() or len(images) > 1:
            emit(
                f"projects/{project['slug']}/",
                project["title"],
                build_project_page(site, base, project),
                project.get("blurb", ""),
            )

    emit("art/", "Art", build_art(site, base, art))
    emit("blog/", "Blog", build_blog_index(site, base, posts))
    for post in posts:
        emit(
            f"blog/{post['slug']}/",
            post["title"],
            build_post(site, base, post),
            post.get("summary", ""),
        )

    emit("now/", pages["now"]["title"], build_simple(site, base, pages["now"]))
    emit("uses/", pages["uses"]["title"], build_simple(site, base, pages["uses"]))
    emit("cv/", pages["cv"]["title"], build_cv(site, base, pages["cv"]))
    emit(
        "colophon/",
        pages["colophon"]["title"],
        build_colophon(site, base, pages["colophon"], buttons),
    )

    write(
        ROOT / "404.html",
        layout(
            site,
            title="Not found",
            body=build_simple(site, base, pages["404"]),
            base=base,
        ),
        written,
    )
    write(ROOT / "feed.xml", build_feed(site, posts), written)
    write(ROOT / "sitemap.xml", build_sitemap(site, routes), written)

    print(f"built {len(written)} files into {ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
