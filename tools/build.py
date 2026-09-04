#!/usr/bin/env python3
"""Render content/ and posts/ into the static pages committed at the repo root.

    nix-shell --run 'python3 tools/build.py'

Every page is Markdown with YAML frontmatter, so the same files open cleanly in Obsidian.
Footnotes become margin notes. A paragraph that is only images becomes a row of taped-in figures.
"""

import html
import re
import tomllib
from datetime import datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path

import markdown
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
POSTS = ROOT / "posts"
ASSETS = ROOT / "assets"

SITE = tomllib.loads((CONTENT / "site.toml").read_text())["site"]
TABS = tomllib.loads((CONTENT / "site.toml").read_text())["tab"]
SOCIALS = tomllib.loads((CONTENT / "site.toml").read_text())["social"]

MD = markdown.Markdown(extensions=["fenced_code", "footnotes", "tables", "attr_list", "md_in_html"])

FRONT = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.S)
FOOTNOTE_BLOCK = re.compile(r'<div class="footnote">.*?</div>', re.S)
FOOTNOTE_ITEM = re.compile(r'<li id="fn:([^"]+)">\s*<p>(.*?)&#160;<a class="footnote-backref".*?</a></p>\s*</li>', re.S)
FOOTNOTE_REF = re.compile(r'<sup id="fnref:([^"]+)"><a [^>]*>[^<]*</a></sup>')
IMG_PARAGRAPH = re.compile(r"<p>((?:\s*<img [^>]*/?>\s*)+)</p>")
IMG = re.compile(r'<img alt="([^"]*)" src="([^"]+)"(?: title="([^"]*)")? ?/?>')


def esc(text):
    return html.escape(str(text), quote=True)


def load(path):
    match = FRONT.match(path.read_text())
    if not match:
        raise SystemExit(f"{path}: missing frontmatter")
    return yaml.safe_load(match.group(1)) or {}, match.group(2)


def sidenotes(out):
    block = FOOTNOTE_BLOCK.search(out)
    if not block:
        return out
    notes = dict(FOOTNOTE_ITEM.findall(block.group(0)))
    out = out[: block.start()] + out[block.end() :]
    return FOOTNOTE_REF.sub(lambda m: f'<small class="note">{notes[m.group(1)]}</small>', out)


def figures(out, root):
    def paragraph(match):
        figs = []
        for alt, src, title in IMG.findall(match.group(1)):
            width, height = Image.open(ASSETS / src).size
            orient = orientation(width, height)
            caption = f"<figcaption>{title}</figcaption>" if title else ""
            figs.append(
                f'<figure class="taped {orient}" style="--w:{width}px"><img src="{root}assets/{src}" alt="{esc(alt)}" '
                f'width="{width}" height="{height}" loading="lazy">{caption}</figure>'
            )
        solo = " solo" if len(figs) == 1 else ""
        return f'<div class="pins{solo}">{"".join(figs)}</div>'

    return IMG_PARAGRAPH.sub(paragraph, out)


def orientation(width, height):
    if height > width * 1.15:
        return "portrait"
    if height > width * 0.85:
        return "square"
    return "landscape"


def render(src, root):
    MD.reset()
    return figures(sidenotes(MD.convert(src)), root)


def day(d):
    return f"{d.day} {d:%b %Y}"


def layout(*, title, body, root, active, leaf, description, path):
    tabs = "".join(
        f'<a href="{root}{t["href"]}"{" class=\"active\" aria-current=\"page\"" if t["key"] == active else ""}>{t["label"]}</a>'
        for t in TABS
    )
    buttons = "".join(
        (f'<a href="{b["url"]}">' if b.get("url") else "")
        + f'<img src="{root}assets/img/buttons/{b["img"]}" alt="{esc(b["alt"])}" width="88" height="31" loading="lazy">'
        + ("</a>" if b.get("url") else "")
        for b in tomllib.loads((CONTENT / "buttons.toml").read_text())["button"]
    )
    full_title = SITE["title"] if title == SITE["title"] else f"{title} · {SITE['title']}"
    canonical = SITE["base_url"] + path
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#1e1e2e">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE["base_url"]}assets/img/avatar.webp">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{esc(SITE["title"])} blog" href="{root}feed.xml">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<div class="book">
<nav class="tabs" aria-label="Sections">{tabs}</nav>
<div class="page">
<div class="rings" aria-hidden="true">{"<i></i>" * 18}</div>
<main>
{body}
</main>
<footer class="foot">
<div class="buttons">{buttons}</div>
<p class="colophon-line"><span class="mono">leaf {leaf}</span> · <a href="{root}feed.xml">rss</a> · <a href="{SITE["source"]}">source</a> · <a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
</footer>
</div>
</div>
</body>
</html>
"""


def write(rel, text):
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print("wrote", rel)


def project_card(meta, body, root, featured):
    links = " · ".join(f'<a href="{l["url"]}">{esc(l["label"])}</a>' for l in meta.get("links", []))
    tags = " ".join(f"<span>{esc(t)}</span>" for t in meta.get("tags", []))
    status = meta.get("status")
    stamp = f'<span class="status status-{status}">{status}</span>' if status else ""
    margin = f'<small class="note stamp">{esc(meta["kicker"])}{stamp}<span class="tags">{tags}</span></small>'
    if featured:
        return (
            f'<article class="project" id="{meta["slug"]}">'
            f"<h3>{margin}<a href=\"#{meta['slug']}\">{esc(meta['title'])}</a></h3>"
            f"{render(body, root)}"
            f'<p class="links">{links}</p></article>'
        )
    return (
        f'<li class="card" id="{meta["slug"]}">'
        f"<h4>{margin}{esc(meta['title'])}</h4>"
        f"{render(body, root)}"
        f'<p class="links">{links}</p></li>'
    )


def build_projects(root):
    entries = []
    for path in sorted(CONTENT.glob("projects/*.md")):
        meta, body = load(path)
        meta["slug"] = path.stem
        entries.append((meta, body))
    entries.sort(key=lambda e: e[0]["order"])
    featured = "".join(project_card(m, b, root, True) for m, b in entries if m.get("featured"))
    shortlist = "".join(project_card(m, b, root, False) for m, b in entries if not m.get("featured"))
    return featured, shortlist


def build_posts():
    posts = []
    for path in sorted(POSTS.glob("*.md"), reverse=True):
        meta, body = load(path)
        meta["slug"] = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        posts.append((meta, body))
    return posts


def hero(root):
    socials = "".join(f'<li><a href="{s["url"]}">{esc(s["label"])}</a></li>' for s in SOCIALS)
    return f"""<header class="hero">
<small class="note stamp">{esc(SITE["volume"])}</small>
<figure class="taped portrait polaroid"><img src="{root}assets/img/avatar.webp" alt="Milo's GitHub avatar: two white hands drawn on black" width="320" height="320"></figure>
<h1>{esc(SITE["name"])}</h1>
<p class="lede">{SITE["lede"]}</p>
<ul class="socials">{socials}</ul>
</header>"""


def build_home(posts):
    root = ""
    featured, shortlist = build_projects(root)
    work_meta, work_body = load(CONTENT / "pages" / "work.md")
    latest = posts[0][0]
    body = f"""{hero(root)}
<section id="work">
<h2><small class="note">§ 01</small>{esc(work_meta["title"])}</h2>
{render(work_body, root)}
</section>
<section id="projects">
<h2><small class="note">§ 02</small>Projects</h2>
{featured}
<h3 class="sub"><small class="note">§ 02b</small>Also in this notebook</h3>
<ul class="cards">{shortlist}</ul>
</section>
<section id="latest">
<h2><small class="note">§ 03</small>From the blog</h2>
<p><small class="note">{day(latest["date"])}</small><a href="blog/{latest["slug"]}/">{esc(latest["title"])}</a>. {esc(latest["summary"])} <a href="blog/">All posts.</a></p>
</section>"""
    write("index.html", layout(title=SITE["title"], body=body, root=root, active="projects", leaf=1, description=SITE["description"], path=""))


def build_blog(posts):
    root = "../"
    items = "".join(
        f'<li><small class="note">{day(m["date"])}</small><a href="{m["slug"]}/">{esc(m["title"])}</a><p>{esc(m["summary"])}</p></li>'
        for m, _ in posts
    )
    intro_meta, intro_body = load(CONTENT / "pages" / "blog.md")
    body = f"""<h1><small class="note stamp">{len(posts)} post{"s" if len(posts) != 1 else ""}</small>{esc(intro_meta["title"])}</h1>
{render(intro_body, root)}
<ul class="posts">{items}</ul>"""
    write("blog/index.html", layout(title="Blog", body=body, root=root, active="blog", leaf=2, description=intro_meta["description"], path="blog/"))
    for meta, src in posts:
        root = "../../"
        body = f"""<article class="post">
<h1><small class="note stamp">{day(meta["date"])}</small>{esc(meta["title"])}</h1>
<p class="lede">{esc(meta["summary"])}</p>
{render(src, root)}
<p class="back"><a href="../">← all posts</a></p>
</article>"""
        write(f"blog/{meta['slug']}/index.html", layout(title=meta["title"], body=body, root=root, active="blog", leaf="2, cont.", description=meta["summary"], path=f"blog/{meta['slug']}/"))


def build_feed(posts):
    items = []
    for meta, src in posts:
        url = f"{SITE['base_url']}blog/{meta['slug']}/"
        content = render(src, SITE["base_url"])
        items.append(
            f"<item><title>{esc(meta['title'])}</title><link>{url}</link><guid>{url}</guid>"
            f"<pubDate>{format_datetime(datetime.combine(meta['date'], time(9), timezone.utc))}</pubDate>"
            f"<description>{esc(content)}</description></item>"
        )
    write(
        "feed.xml",
        f'<?xml version="1.0" encoding="utf-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
        f"<title>{esc(SITE['title'])}</title><link>{SITE['base_url']}</link><description>{esc(SITE['description'])}</description>"
        f'<language>en-gb</language><atom:link href="{SITE["base_url"]}feed.xml" rel="self" type="application/rss+xml"/>'
        f"{''.join(items)}</channel></rss>\n",
    )


def build_sketches():
    root = "../"
    art = tomllib.loads((CONTENT / "art.toml").read_text())
    figs = []
    for piece in art["piece"]:
        width, height = Image.open(ASSETS / "img" / "art" / piece["file"]).size
        orient = orientation(width, height)
        figs.append(
            f'<figure class="taped {orient}" style="--w:{width}px"><img src="{root}assets/img/art/{piece["file"]}" alt="{esc(piece["alt"])}" '
            f'width="{width}" height="{height}" loading="lazy"><figcaption>{esc(piece["caption"])}</figcaption></figure>'
        )
    body = f"""<h1><small class="note stamp">{len(figs)} pieces</small>{esc(art["title"])}</h1>
{render(art["intro"], root)}
<div class="pins gallery">{"".join(figs)}</div>"""
    write("sketches/index.html", layout(title=art["title"], body=body, root=root, active="sketches", leaf=3, description=art["description"], path="sketches/"))


def build_pages():
    for path in sorted(CONTENT.glob("pages/*.md")):
        meta, body = load(path)
        if "tab" not in meta:
            continue
        tab = next(t for t in TABS if t["key"] == meta["tab"])
        root = "../"
        stamp = f'<small class="note stamp">{esc(meta["stamp"])}</small>' if meta.get("stamp") else ""
        html_body = f"<h1>{stamp}{esc(meta['title'])}</h1>\n{render(body, root)}"
        write(
            f"{tab['href']}index.html",
            layout(title=meta["title"], body=html_body, root=root, active=meta["tab"], leaf=TABS.index(tab) + 1, description=meta["description"], path=tab["href"]),
        )


def build_404():
    root = SITE["base_url"]
    body = f"""<h1><small class="note stamp">404</small>This leaf is missing</h1>
<p>Torn out, never written, or the link was wrong. <a href="{root}">Back to the front.</a></p>"""
    write("404.html", layout(title="Not found", body=body, root=root, active="", leaf="?", description="Page not found.", path="404.html"))


if __name__ == "__main__":
    posts = build_posts()
    build_home(posts)
    build_blog(posts)
    build_feed(posts)
    build_sketches()
    build_pages()
    build_404()
