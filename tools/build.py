#!/usr/bin/env python3
"""Render content/ and posts/ into index.html, blog/, feed.xml and 404.html."""

from __future__ import annotations

import datetime as dt
import html
import re
import shutil
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
POSTS = ROOT / "posts"


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def load(name: str) -> dict:
    return tomllib.loads((CONTENT / name).read_text())


# A deliberately small Markdown: headings, lists, quotes, fenced code, rules,
# and inline links, images, code, bold and italics. Enough for posts and the
# short sections; swap in python-markdown if it ever stops being enough.
def inline(text: str) -> str:
    text = esc(text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return text


BLOCK_START = re.compile(r"(```|#{1,6}\s|>|[-*]\s|\d+\.\s|---$)")


def markdown(text: str) -> str:
    out: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            lang = line[3:].strip()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{esc(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{esc(chr(10).join(buf))}</code></pre>")
            continue
        heading = re.match(r"(#{1,6})\s+(.*)", line)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue
        ordered = bool(re.match(r"\s*\d+\.\s+", line))
        if ordered or re.match(r"\s*[-*]\s+", line):
            pattern = r"\s*\d+\.\s+" if ordered else r"\s*[-*]\s+"
            items = []
            while i < len(lines) and re.match(pattern, lines[i]):
                items.append(re.sub(pattern, "", lines[i], count=1))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if line.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip())
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(buf))}</p></blockquote>")
            continue
        if line.strip() == "":
            i += 1
            continue
        if line.strip() == "---":
            out.append("<hr>")
            i += 1
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not BLOCK_START.match(lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out)


def load_post(path: Path) -> dict:
    text = path.read_text()
    meta: dict[str, str] = {}
    body = text
    if text.startswith("---\n"):
        _, front, body = text.split("---\n", 2)
        for entry in front.splitlines():
            if ":" in entry:
                key, value = entry.split(":", 1)
                meta[key.strip()] = value.strip().strip('"')
    date = dt.date.fromisoformat(meta.get("date") or path.stem[:10])
    slug = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    return {
        "slug": slug,
        "title": meta["title"],
        "date": date,
        "summary": meta.get("summary", ""),
        "body": markdown(body),
    }


SITE = load("site.toml")
SECTIONS = ["work", "projects", "blog", "drawings", "now", "buttons"]


def sticker(inner: str, cls: str = "", tag: str = "article", attrs: str = "") -> str:
    classes = " ".join(c for c in ["sk", cls] if c)
    return f'<{tag} class="{classes}"{attrs}><div class="sk-body">{inner}</div></{tag}>'


def section(slug: str, title: str, body: str, note: str = "") -> str:
    cut = f'<span class="cut">{esc(note)}</span>' if note else ""
    return (
        f'<section class="section {slug}" id="{slug}">'
        f'<div class="section-head"><h2 class="label">{esc(title)}</h2>{cut}</div>'
        f"{body}</section>"
    )


def page(*, title: str, body: str, rel: str, description: str, path: str) -> str:
    nav = "".join(f'<a class="label" href="{rel}#{s}">{s}</a>' for s in SECTIONS)
    canonical = SITE["url"] + path
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{esc(canonical)}">
<meta name="theme-color" content="#1e1e2e">
<link rel="canonical" href="{esc(canonical)}">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{esc(SITE['handle'])}" href="{rel}feed.xml">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
<main class="sheet">
<header class="strip">
<a class="brand" href="{rel}">milotek.dev</a>
<span class="strip-note">{esc(SITE['sheet'])} · peel from any corner</span>
<nav class="labels" aria-label="Sections">{nav}</nav>
</header>
{body}
<footer class="foot">
<span>© {dt.date.today().year} {esc(SITE['name'])}</span>
<a href="{rel}feed.xml">rss</a>
<a href="{rel}#colophon">colophon</a>
<a href="{esc(SITE['source'])}">source</a>
<span>printed on GitHub Pages · peel responsibly</span>
</footer>
</main>
</body>
</html>
"""


def render_hero() -> str:
    socials = "".join(f'<a href="{esc(s["href"])}">{esc(s["name"])}</a>' for s in SITE["social"])
    name = sticker(
        f'<div class="sk-text"><h1>{esc(SITE["name"])}</h1>'
        f'<p class="role">{esc(SITE["handle"])} · {esc(SITE["role"])}</p>'
        f'<p>{esc(SITE["tagline"])}</p><p>{esc(SITE["blurb"])}</p>'
        f'<div class="socials">{socials}</div></div>',
        "big hero",
        attrs=' style="--r:-1.2deg"',
    )
    photo = (
        '<article class="sk round" style="--r:2.5deg"><div class="sk-body">'
        f'<img src="assets/img/milo.webp" alt="{esc(SITE["name"])} with a dog" width="360" height="360"></div>'
        '<div class="mascot" title="the mascot"><img src="assets/img/mascot.webp" alt="A fox sticker holding a red panda plush" width="240" height="240"></div>'
        "</article>"
    )
    return f'<div class="grid">{name}{photo}</div>'


def render_work() -> str:
    jobs = load("work.toml")["job"]
    out = []
    for job in jobs:
        lines = "".join(f"<li>{esc(x)}</li>" for x in job["lines"])
        out.append(
            sticker(
                f'<div class="sk-text"><h3>{esc(job["org"])}</h3>'
                f'<p class="meta">{esc(job["title"])} · {esc(job["where"])} · <span class="when">{esc(job["when"])}</span></p>'
                f"<ul>{lines}</ul></div>",
                job.get("size", ""),
            )
        )
    return f'<div class="grid">{"".join(out)}</div>'


def render_projects() -> str:
    out = []
    for p in load("projects.toml")["project"]:
        img = ""
        if "image" in p:
            img = f'<img class="sk-img" src="assets/img/projects/{esc(p["image"])}" alt="{esc(p["name"])}" loading="lazy">'
        tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in p.get("tags", []))
        links = f'<a href="{esc(p["repo"])}">repo</a>'
        if "link" in p:
            links += f'<a href="{esc(p["link"])}">live</a>'
        out.append(
            sticker(
                f'{img}<div class="sk-text"><h3><a href="{esc(p["repo"])}">{esc(p["name"])}</a></h3>'
                f'<p>{esc(p["blurb"])}</p><div class="links">{links}</div>'
                f'<div class="tags">{tags}</div></div>',
                p.get("size", ""),
            )
        )
    return f'<div class="grid">{"".join(out)}</div>'


def render_art() -> str:
    out = []
    for piece in load("art.toml")["piece"]:
        out.append(
            sticker(
                f'<figure><img src="assets/img/art/{esc(piece["file"])}" alt="{esc(piece["caption"])}" loading="lazy">'
                f"<figcaption>{esc(piece['caption'])}</figcaption></figure>",
                "art-piece",
            )
        )
    return f'<div class="grid">{"".join(out)}</div>'


def post_card(post: dict, rel: str) -> str:
    return sticker(
        f'<div class="sk-text"><h3><a href="{rel}blog/{post["slug"]}/">{esc(post["title"])}</a></h3>'
        f'<p class="meta">{post["date"].isoformat()}</p><p>{esc(post["summary"])}</p></div>',
        "wide",
    )


def render_blog(posts: list[dict]) -> str:
    cards = "".join(post_card(p, "") for p in posts)
    return f'<div class="grid posts">{cards}</div>'


def render_notes() -> str:
    def note(slug: str, title: str, cls: str = "") -> str:
        body = markdown((CONTENT / f"{slug}.md").read_text())
        return sticker(f'<div class="sk-text" id="{slug}"><h3>{title}</h3>{body}</div>', cls)

    return '<div class="grid">' + note("now", "now", "peeled") + note("uses", "uses") + note("colophon", "colophon") + "</div>"


def render_buttons() -> str:
    out = []
    for b in load("buttons.toml")["button"]:
        img = f'<img src="assets/buttons/{esc(b["file"])}" alt="{esc(b["alt"])}" width="88" height="31">'
        if "href" in b:
            out.append(sticker(img, "b88", tag="a", attrs=f' href="{esc(b["href"])}" title="{esc(b["alt"])}"'))
        else:
            out.append(sticker(img, "b88", tag="span", attrs=f' title="{esc(b["alt"])}"'))
    mine = [b for b in load("buttons.toml")["button"] if b.get("mine")]
    snippet = ""
    if mine:
        first = mine[0]
        code = f'<a href="https://milotek.dev"><img src="{SITE["url"]}assets/buttons/{first["file"]}" alt="{first["alt"]}" width="88" height="31"></a>'
        snippet = f'<div class="b88-note">Want one for your site? Take the first one:<pre><code>{esc(code)}</code></pre></div>'
    return f'<div class="buttons">{"".join(out)}</div>{snippet}'


def build() -> None:
    posts = sorted((load_post(p) for p in POSTS.glob("*.md")), key=lambda p: p["date"], reverse=True)

    body = (
        render_hero()
        + section("work", "work", render_work())
        + section("projects", "projects", render_projects(), "✂ cut along the dotted line")
        + section("blog", "blog", render_blog(posts))
        + section("drawings", "drawings", render_art(), "procreate, mostly")
        + section("now", "now / uses / colophon", render_notes())
        + section("buttons", "buttons", render_buttons(), "88 × 31, the original stickers")
    )
    (ROOT / "index.html").write_text(
        page(title=f"{SITE['name']} · {SITE['handle']}", body=body, rel="", description=SITE["description"], path="")
    )

    blog_dir = ROOT / "blog"
    if blog_dir.exists():
        shutil.rmtree(blog_dir)
    blog_dir.mkdir()
    index_body = '<div class="grid posts">' + "".join(post_card(p, "../") for p in posts) + "</div>"
    (blog_dir / "index.html").write_text(
        page(title=f"blog · {SITE['handle']}", body=section("blog", "blog", index_body), rel="../", description="Posts by " + SITE["name"], path="blog/")
    )
    for post in posts:
        out_dir = blog_dir / post["slug"]
        out_dir.mkdir()
        article = sticker(
            f'<div class="sk-text"><h1>{esc(post["title"])}</h1><p class="meta">{post["date"].isoformat()} · <a href="../">all posts</a></p>'
            f'<div class="prose">{post["body"]}</div></div>',
            "full post",
            attrs=' style="--r:-0.6deg"',
        )
        (out_dir / "index.html").write_text(
            page(title=f"{post['title']} · {SITE['handle']}", body=f'<div class="grid">{article}</div>', rel="../../", description=post["summary"], path=f"blog/{post['slug']}/")
        )

    items = "".join(
        f"<item><title>{esc(p['title'])}</title><link>{SITE['url']}blog/{p['slug']}/</link>"
        f"<guid>{SITE['url']}blog/{p['slug']}/</guid>"
        f"<pubDate>{dt.datetime.combine(p['date'], dt.time(9), dt.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>"
        f"<description>{esc(p['summary'])}</description>"
        f"<content:encoded><![CDATA[{p['body']}]]></content:encoded></item>"
        for p in posts
    )
    (ROOT / "feed.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">'
        f"<channel><title>{esc(SITE['handle'])}</title><link>{SITE['url']}</link>"
        f"<description>{esc(SITE['description'])}</description><language>en-gb</language>"
        f'<atom:link href="{SITE["url"]}feed.xml" rel="self" type="application/rss+xml"/>'
        f"{items}</channel></rss>\n"
    )

    lost = sticker(
        '<div class="sk-text"><h1>404</h1><p class="meta">this sticker has been peeled off</p>'
        '<p>Whatever was here is gone, or never was. <a href="/wst4/">Back to the sheet.</a></p></div>',
        "wide post peeled",
        attrs=' style="--r:-3deg"',
    )
    (ROOT / "404.html").write_text(
        page(title=f"404 · {SITE['handle']}", body=f'<div class="grid">{lost}</div>', rel="/wst4/", description="Not found", path="404.html")
    )


if __name__ == "__main__":
    build()
    print("built")
