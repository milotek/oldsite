#!/usr/bin/env python3
"""Build the site.

    python3 build.py

Reads content/ (TOML + Markdown), writes HTML to the repo root and copies
static/ to assets/. No dependencies, so this keeps working on whatever Python
happens to be on the machine in five years.
"""

from __future__ import annotations

import html
import os
import re
import shutil
import tomllib
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
ASSETS = ROOT / "assets"
# Images are not copied: they are already at the URL they are served from, so a
# Markdown file can write img/thing.webp and mean it in the vault too.
IMG = ROOT / "img"

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
BUILD_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")


# --------------------------------------------------------------------------
# markdown
#
# A vendored subset instead of a library because the build has to run with a
# bare interpreter, including inside a GitHub Action with nothing installed.
# --------------------------------------------------------------------------

def _inline(text: str, rel: str) -> str:
    spans: list[str] = []

    def stash(m):
        spans.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)",
                  lambda m: f'<img src="{link(m.group(2), rel)}" alt="{m.group(1)}" loading="lazy">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  lambda m: f'<a href="{link(m.group(2), rel)}"{ext(m.group(2))}>{m.group(1)}</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)
    return text


def markdown(src: str, rel: str = "") -> str:
    out: list[str] = []
    lines = src.replace("\r\n", "\n").split("\n")
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            lang = line[3:].strip()
            body = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{lang}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(body))}</code></pre>")
            continue
        if re.match(r"^(-{3,}|\*{3,})$", line.strip()):
            out.append("<hr>")
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1)) + 1  # the page title owns h1
            out.append(f"<h{lvl}>{_inline(m.group(2).strip(), rel)}</h{lvl}>")
            i += 1
            continue
        if line.startswith(">"):
            body = []
            while i < n and lines[i].startswith(">"):
                body.append(lines[i].lstrip(">").strip())
                i += 1
            out.append(f"<blockquote>{markdown(chr(10).join(body), rel)}</blockquote>")
            continue
        m = re.match(r"^\s*([-*]|\d+\.)\s+", line)
        if m:
            ordered = m.group(1)[-1] == "."
            items: list[str] = []
            while i < n and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i]))
                i += 1
                while i < n and lines[i].startswith("  ") and lines[i].strip():
                    items[-1] += " " + lines[i].strip()
                    i += 1
            tag = "ol" if ordered else "ul"
            body = "".join(f"<li>{_inline(x, rel)}</li>" for x in items)
            out.append(f"<{tag}>{body}</{tag}>")
            continue
        para = []
        while i < n and lines[i].strip() and not re.match(r"^(#{1,4}\s|```|>|\s*([-*]|\d+\.)\s)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{_inline(' '.join(para), rel)}</p>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# urls
#
# The site deploys under a subpath, so every internal URL is relative to the
# page it appears on and `rel` is the walk back up to the root.
# --------------------------------------------------------------------------

def link(url: str, rel: str) -> str:
    if re.match(r"^([a-z]+:|//|#)", url):
        return url
    return rel + url


def ext(url: str) -> str:
    return ' target="_blank" rel="noopener"' if url.startswith("http") else ""


def pretty_date(iso: str) -> str:
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


# --------------------------------------------------------------------------
# content
# --------------------------------------------------------------------------

def load_toml(name: str) -> dict:
    with open(CONTENT / name, "rb") as fh:
        return tomllib.load(fh)


SITE = load_toml("site.toml")
PROJECTS = load_toml("projects.toml")["project"]
ART = load_toml("art.toml")
BUTTONS = load_toml("buttons.toml")
USES = load_toml("uses.toml")
WORKSPACES = SITE["workspace"]
BASE_PATH = re.sub(r"^[a-z]+://[^/]+", "", SITE["url"]) or "/"


def load_posts() -> list[dict]:
    posts = []
    for path in sorted((CONTENT / "posts").glob("*.md"), reverse=True):
        raw = path.read_text(encoding="utf-8")
        m = re.match(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$", raw, re.S)
        if not m:
            raise SystemExit(f"{path.name}: missing +++ TOML front matter")
        meta = tomllib.loads(m.group(1))
        meta["body"] = m.group(2).strip()
        meta["slug"] = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        meta["path"] = f"blog/{meta['slug']}/"
        posts.append(meta)
    return posts


POSTS = load_posts()


# --------------------------------------------------------------------------
# chrome
# --------------------------------------------------------------------------

def window(title: str, body: str, span: str = "wide", meta: str = "", cls: str = "",
           wid: str = "", h: int = 2) -> str:
    right = f'<span class="win__meta">{meta}</span>' if meta else ""
    ident = f' id="{wid}"' if wid else ""
    return (
        f'<section class="win win--{span} {cls}"{ident}>'
        f'<div class="win__bar"><span class="win__dot" aria-hidden="true"></span>'
        f'<h{h} class="win__title">{title}</h{h}>{right}</div>'
        f'<div class="win__body">{body}</div>'
        f"</section>"
    )


def bar(active: str, rel: str) -> str:
    pills = []
    for ws in WORKSPACES:
        is_on = ws["name"] == active
        on_cls = " is-active" if is_on else ""
        current = ' aria-current="page"' if is_on else ""
        href = (rel + ws["path"]) or "./"
        pills.append(
            f'<a class="ws{on_cls}" href="{href}"{current} data-key="{ws["key"]}">'
            f'<span class="ws__key">{ws["key"]}</span>'
            f'<span class="ws__name">{ws["name"]}</span></a>'
        )
    return (
        '<header class="bar">'
        f'<nav class="bar__ws" aria-label="Sections">{"".join(pills)}</nav>'
        '<div class="bar__status">'
        '<span class="mod mod--host">milo@london</span>'
        '<button class="mod mod--keys" type="button" id="keys-toggle" aria-expanded="false">?</button>'
        '<span class="mod mod--clock" id="clock" aria-hidden="true">--:--</span>'
        "</div></header>"
    )


def keys_panel() -> str:
    rows = "".join(
        f'<div><kbd>{ws["key"]}</kbd><span>{ws["name"]}</span></div>' for ws in WORKSPACES
    )
    return (
        '<div class="keys" id="keys" hidden>'
        '<div class="keys__inner"><p class="keys__head">keybinds</p>'
        f'<div class="keys__grid">{rows}<div><kbd>?</kbd><span>this</span></div>'
        '<div><kbd>Esc</kbd><span>close</span></div></div></div></div>'
    )


def footer(rel: str) -> str:
    return (
        '<footer class="foot">'
        f'<span>milo tek</span><span class="foot__sep">/</span>'
        f'<a href="{rel}feed.xml">rss</a><span class="foot__sep">/</span>'
        '<a href="https://github.com/milotek/wst13" target="_blank" rel="noopener">source</a>'
        f'<span class="foot__sep">/</span><span>built {pretty_date(BUILD_DATE)}</span>'
        "</footer>"
    )


def page(*, title: str, desc: str, active: str, depth: int, body: str, head: str = "",
         rel: str | None = None) -> str:
    rel = "../" * depth if rel is None else rel
    full = title if title == SITE["title"] else f"{title} / {SITE['title']}"
    return f"""<!DOCTYPE html>
<html lang="{SITE['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#11111b">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:site_name" content="{esc(SITE['title'])}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{esc(SITE['title'])}" href="{rel}feed.xml">
<link rel="stylesheet" href="{rel}assets/css/style.css">
{head}</head>
<body>
<a class="skip" href="#main">skip to content</a>
{bar(active, rel)}
<main class="workspace" id="main">
{body}
</main>
{footer(rel)}
{keys_panel()}
<script src="{rel}assets/js/wm.js" defer></script>
</body>
</html>
"""


# --------------------------------------------------------------------------
# fragments
# --------------------------------------------------------------------------

def tags(project: dict) -> str:
    return "".join(f'<span class="tag">{esc(t)}</span>' for t in project.get("tags", []))


def project_links(project: dict, rel: str) -> str:
    out = []
    if project.get("repo"):
        out.append(f'<a class="lnk" href="{project["repo"]}" target="_blank" rel="noopener">repo</a>')
    if project.get("link"):
        name = project.get("linkname", "site")
        out.append(f'<a class="lnk" href="{project["link"]}" target="_blank" rel="noopener">{esc(name)}</a>')
    if not out:
        out.append('<span class="lnk lnk--dead">private</span>')
    return f'<p class="links">{"".join(out)}</p>'


def shots(project: dict, rel: str, limit: int | None = None) -> str:
    imgs = project.get("images", [])[: limit or None]
    if not imgs:
        return ""
    cls = "shots" + (" shots--phone" if project["slug"] == "lockyn" else "")
    cells = "".join(
        f'<a class="shot" href="{link(im["src"], rel)}">'
        f'<img src="{link(im["src"], rel)}" alt="{esc(im["alt"])}" loading="lazy" decoding="async"></a>'
        for im in imgs
    )
    return f'<div class="{cls}">{cells}</div>'


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------

def build_home() -> str:
    rel = ""
    wins = []

    links = "".join(
        f'<a class="lnk" href="{l["url"]}"{ext(l["url"])}>{esc(l["name"])}</a>'
        for l in SITE["link"]
    )
    wins.append(window(
        "~/whoami",
        f'<div class="hero">'
        f'<img class="hero__pfp" src="{rel}{SITE["avatar"]}" alt="Milo, drawn." width="120" height="120">'
        f'<div class="hero__text"><h1 class="hero__name">{esc(SITE["title"])}</h1>'
        f'<p class="hero__tag">{esc(SITE["tagline"])}</p>'
        f'{markdown(SITE["intro"]["body"], rel)}'
        f'<p class="links links--wrap">{links}</p></div></div>',
        span="twothirds",
        cls="win--focus",
        h=0,
    ))

    now = SITE["now"]
    items = "".join(f"<li>{_inline(x, rel)}</li>" for x in now["items"])
    wins.append(window(
        "~/now",
        f'<ul class="ticks">{items}</ul>',
        span="third",
        meta=pretty_date(now["updated"]),
    ))

    work = SITE["work"]
    points = "".join(f"<li>{_inline(p, rel)}</li>" for p in work["points"])
    wins.append(window(
        "~/work",
        f'<p class="role"><strong>{esc(work["role"])}</strong> at {esc(work["org"])}, {esc(work["place"])}.</p>'
        f'<p class="dim">{esc(work["team"])}</p>'
        f'<ul class="ticks">{points}</ul>',
        span="half",
    ))

    feat = [p for p in PROJECTS if p.get("featured")]
    cards = "".join(
        f'<a class="card" href="{rel}projects/#{p["slug"]}">'
        + (f'<img class="card__img" src="{link(card_src(p), rel)}" alt="" loading="lazy" decoding="async">'
           if card_src(p) else '<span class="card__img card__img--none" aria-hidden="true"></span>')
        + f'<span class="card__name">{esc(p["name"])}</span>'
        f'<span class="card__blurb">{esc(p["blurb"])}</span></a>'
        for p in feat
    )
    feat_win = window(
        "~/projects --featured",
        f'<div class="cards">{cards}</div>'
        f'<p class="more"><a class="lnk" href="{rel}projects/">all {len(PROJECTS)} projects</a></p>',
        span="wide",
    )

    posts = "".join(
        f'<li class="entry"><a href="{rel}{p["path"]}">'
        f'<span class="post__date">{pretty_date(p["date"])}</span>'
        f'<span class="post__title">{esc(p["title"])}</span></a>'
        f'<p class="row__blurb">{esc(p.get("summary", ""))}</p></li>'
        for p in POSTS[:3]
    )
    blog_win = window(
        "~/blog",
        f'<ul class="entries">{posts}</ul>'
        f'<p class="more"><a class="lnk" href="{rel}blog/">everything</a>'
        f'<a class="lnk" href="{rel}feed.xml">rss</a></p>',
        span="half",
    )

    wins.append(blog_win)
    wins.append(feat_win)

    thumbs = "".join(
        f'<a class="strip__cell" href="{rel}art/#{a["file"]}">'
        f'<img src="{rel}img/art/{a["file"]}_thumb.webp" alt="{esc(a["title"])}" loading="lazy" decoding="async"></a>'
        for a in ART["piece"][:8]
    )
    wins.append(window(
        "~/art",
        f'<div class="strip">{thumbs}</div>'
        f'<p class="more"><a class="lnk" href="{rel}art/">the rest</a></p>',
        span="twothirds",
    ))

    wins.append(window("~/buttons", buttons_body(rel), span="third"))
    return "\n".join(wins)


def card_src(project: dict) -> str:
    """`card` overrides the thumbnail when the first screenshot crops badly."""
    if project.get("card"):
        return project["card"]
    imgs = project.get("images")
    return imgs[0]["src"] if imgs else ""


def buttons_body(rel: str) -> str:
    def render(b):
        img = (f'<img class="btn88" src="{rel}img/buttons/{b["file"]}" alt="{esc(b["alt"])}" '
               f'width="88" height="31" loading="lazy">')
        if b.get("url"):
            return f'<a href="{b["url"]}"{ext(b["url"])}>{img}</a>'
        return img

    mine = [b for b in BUTTONS["button"] if b.get("mine")]
    theirs = [b for b in BUTTONS["button"] if not b.get("mine")]
    return (
        f'<p class="dim">{esc(BUTTONS["mine"]["note"])}</p>'
        f'<div class="btnwall">{"".join(render(b) for b in mine)}</div>'
        '<p class="dim btnwall__label">and some I like:</p>'
        f'<div class="btnwall">{"".join(render(b) for b in theirs)}</div>'
    )


def build_projects() -> str:
    rel = "../"
    wins = [window(
        "~/projects",
        '<p>Work I would actually show someone. The big ones first, the rest underneath, '
        'and the truly mediocre left on GitHub where it belongs.</p>',
        span="wide",
        cls="win--slim",
        h=1,
    )]
    for p in [x for x in PROJECTS if x.get("featured")]:
        body = (
            f'<p class="blurb">{esc(p["blurb"])}</p>'
            f'{shots(p, rel)}'
            f'{markdown(p.get("body", ""), rel)}'
            f'<div class="tags">{tags(p)}</div>'
            f'{project_links(p, rel)}'
        )
        wins.append(window(esc(p["name"]), body, span="half", meta=esc(p["year"]), wid=p["slug"]))

    rows = []
    for p in [x for x in PROJECTS if not x.get("featured")]:
        rows.append(
            f'<li class="row" id="{p["slug"]}">'
            f'<div class="row__head"><span class="row__name">{esc(p["name"])}</span>'
            f'<span class="row__year">{esc(p["year"])}</span></div>'
            f'<p class="row__blurb">{esc(p["blurb"])}</p>'
            f'<div class="row__foot"><div class="tags">{tags(p)}</div>{project_links(p, rel)}</div>'
            f'</li>'
        )
    wins.append(window(
        "~/projects/smaller",
        f'<ul class="rows">{"".join(rows)}</ul>'
        '<p class="more"><a class="lnk" href="https://github.com/milotek?tab=repositories" '
        'target="_blank" rel="noopener">everything else on github</a></p>',
        span="wide",
    ))
    return "\n".join(wins)


def build_blog_index() -> str:
    rel = "../"
    items = "".join(
        f'<li class="entry"><a href="{rel}{p["path"]}">'
        f'<span class="post__date">{pretty_date(p["date"])}</span>'
        f'<span class="post__title">{esc(p["title"])}</span></a>'
        f'<p class="row__blurb">{esc(p.get("summary", ""))}</p></li>'
        for p in POSTS
    )
    counts: dict[str, int] = {}
    for p in POSTS:
        for t in p.get("tags", []):
            counts[t] = counts.get(t, 0) + 1
    tag_rows = "".join(
        f'<div class="kv"><dt>{esc(t)}</dt><dd>{n}</dd></div>'
        for t, n in sorted(counts.items())
    )
    return "\n".join([
        window(
            "~/blog",
            f'<p class="dim">Posts live as Markdown files in <code>content/posts/</code>, '
            f'one file each, TOML header on top.</p>'
            f'<ul class="entries">{items}</ul>',
            span="twothirds",
            h=1,
        ),
        window(
            "~/blog/tags",
            f'<dl class="kvs kvs--tight">{tag_rows}</dl>'
            f'<p class="links"><a class="lnk" href="{rel}feed.xml">rss feed</a></p>',
            span="third",
            cls="win--side",
        ),
    ])


def build_post(post: dict) -> str:
    rel = "../../"
    tag_line = "".join(f'<span class="tag">{esc(t)}</span>' for t in post.get("tags", []))
    words = len(re.sub(r"[^\w\s]", " ", post["body"]).split())
    side = [
        ("written", pretty_date(post["date"])),
        ("words", f"{words:,}"),
        ("read", f"~{max(1, round(words / 220))} min"),
    ]
    rows = "".join(f'<div class="kv"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in side)
    return "\n".join([
        window(
            f'~/blog/{esc(post["slug"])}',
            f'<article class="prose"><h1 class="prose__title">{esc(post["title"])}</h1>'
            f'<p class="prose__meta">{pretty_date(post["date"])}<span class="tags">{tag_line}</span></p>'
            f'{markdown(post["body"], rel)}</article>',
            span="twothirds",
            meta=pretty_date(post["date"]),
            cls="win--read",
            h=0,
        ),
        window(
            "~/blog/meta",
            f'<dl class="kvs kvs--tight">{rows}</dl>'
            f'<div class="tags tags--block">{tag_line}</div>'
            f'<p class="links"><a class="lnk" href="{rel}blog/">all posts</a>'
            f'<a class="lnk" href="{rel}feed.xml">rss</a></p>',
            span="third",
            cls="win--side",
        ),
    ])


def build_art() -> str:
    rel = "../"
    cells = "".join(
        f'<figure class="piece" id="{a["file"]}">'
        f'<a href="{rel}img/art/{a["file"]}.webp">'
        f'<img src="{rel}img/art/{a["file"]}_thumb.webp" alt="{esc(a["caption"])}" loading="lazy" decoding="async"></a>'
        f'<figcaption><span class="piece__title">{esc(a["title"])}</span>'
        f'<span class="piece__cap">{esc(a["caption"])}</span></figcaption></figure>'
        for a in ART["piece"]
    )
    return window(
        "~/art",
        f'<p class="dim">{esc(ART["note"])}</p><div class="gallery">{cells}</div>',
        span="wide",
        h=1,
    )


def build_uses() -> str:
    wins = [window("~/uses", f'<p>{esc(USES["intro"])}</p>', span="wide", cls="win--slim", h=1)]
    for g in USES["group"]:
        rows = "".join(
            f'<div class="kv"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in g["rows"]
        )
        wins.append(window(f'~/uses/{esc(g["name"])}', f'<dl class="kvs">{rows}</dl>', span="third"))
    return "\n".join(wins)


def build_colophon(stats: list[tuple[str, str]]) -> str:
    rel = "../"
    body = markdown((CONTENT / "colophon.md").read_text(encoding="utf-8"), rel)
    rows = "".join(f'<div class="kv"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in stats)
    return "\n".join([
        window("~/colophon", body, span="twothirds", cls="win--read", h=1),
        window("~/colophon/numbers", f'<dl class="kvs kvs--tight">{rows}</dl>',
               span="third", cls="win--side"),
    ])


def build_404() -> str:
    rel = BASE_PATH
    return window(
        "~/404",
        f'<div class="lost"><img src="{rel}img/under_construction.webp" '
        'alt="A stick figure standing next to some gears, captioned UNDER CONSTRUCTION." width="480">'
        '<div><h1 class="hero__name">404</h1>'
        '<p>Nothing here. I drew this one in about 2024 for the old site and never '
        'found another use for it, so here it is.</p>'
        f'<p class="links"><a class="lnk" href="{rel}">go home</a></p></div></div>',
        span="wide",
        h=0,
    )


# --------------------------------------------------------------------------
# feed
# --------------------------------------------------------------------------

def build_feed() -> str:
    base = SITE["url"].rstrip("/") + "/"
    items = []
    for p in POSTS:
        url = base + p["path"]
        body = markdown(p["body"], base)
        pub = format_datetime(datetime.strptime(p["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc))
        items.append(
            "<item>"
            f"<title>{esc(p['title'])}</title>"
            f"<link>{esc(url)}</link>"
            f"<guid isPermaLink=\"true\">{esc(url)}</guid>"
            f"<pubDate>{pub}</pubDate>"
            f"<description>{esc(p.get('summary', ''))}</description>"
            f"<content:encoded><![CDATA[{body}]]></content:encoded>"
            "</item>"
        )
    now = format_datetime(datetime.now(timezone.utc))
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" '
        'xmlns:content="http://purl.org/rss/1.0/modules/content/">\n<channel>'
        f"<title>{esc(SITE['title'])}</title>"
        f"<link>{esc(base)}</link>"
        f"<description>{esc(SITE['description'])}</description>"
        f"<language>{esc(SITE['lang'])}</language>"
        f"<lastBuildDate>{now}</lastBuildDate>"
        f'<atom:link href="{esc(base)}feed.xml" rel="self" type="application/rss+xml"/>'
        + "".join(items) +
        "</channel>\n</rss>\n"
    )


# --------------------------------------------------------------------------
# write
# --------------------------------------------------------------------------

def write(path: str, text: str) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"  {path:<44} {len(text.encode()) / 1024:6.1f} kB")


def kb(n: int) -> str:
    return f"{n / 1024:.0f} kB"


def main() -> None:
    print("assets")
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    shutil.copytree(STATIC, ASSETS)
    print("  static/ -> assets/")

    print("pages")
    write("index.html", page(
        title=SITE["title"], desc=SITE["description"],
        active="home", depth=0, body=build_home()))
    write("projects/index.html", page(
        title="projects", desc="Things Milo Tekchandani has built: NixOS, mobile apps, shaders, games and hardware.",
        active="projects", depth=1, body=build_projects()))
    write("blog/index.html", page(
        title="blog", desc="Writing by Milo Tekchandani.",
        active="blog", depth=1, body=build_blog_index()))
    for post in POSTS:
        write(f"{post['path']}index.html", page(
            title=post["title"], desc=post.get("summary", ""),
            active="blog", depth=2, body=build_post(post)))
    write("art/index.html", page(
        title="art", desc="Drawings by Milo Tekchandani, mostly Procreate.",
        active="art", depth=1, body=build_art()))
    write("uses/index.html", page(
        title="uses", desc="The machine, the window manager and the rest of it.",
        active="uses", depth=1, body=build_uses()))

    stats = [
        ("projects", str(len(PROJECTS))),
        ("posts", str(len(POSTS))),
        ("drawings", str(len(ART["piece"]))),
        ("buttons", str(len(BUTTONS["button"]))),
        ("build script", f"{len(open(__file__).read().splitlines())} lines"),
        ("dependencies", "0"),
        ("third-party requests", "0"),
        ("cookies", "0"),
        ("css", kb((STATIC / "css" / "style.css").stat().st_size)),
        ("js", kb((STATIC / "js" / "wm.js").stat().st_size)),
        ("fonts", kb(sum(f.stat().st_size for f in (STATIC / "fonts").glob("*.woff2")))),
        ("images", str(sum(1 for _ in IMG.rglob("*.*")))),
        ("home page html", kb((ROOT / "index.html").stat().st_size)),
        ("build time", "under a second"),
    ]
    write("colophon/index.html", page(
        title="colophon", desc="How this site is built, and what it is built out of.",
        active="colophon", depth=1, body=build_colophon(stats)))
    # A 404 is served for any depth of URL, so it is the one page that has to
    # use absolute paths taken from the deploy URL.
    write("404.html", page(
        title="404", desc="Nothing here.",
        active="home", depth=0, body=build_404(), rel=BASE_PATH))
    write("feed.xml", build_feed())
    (ROOT / ".nojekyll").write_text("")

    total = sum(f.stat().st_size for f in ROOT.rglob("*")
                if f.is_file() and ".git" not in f.parts)
    print(f"done. {kb(total)} on disk.")


if __name__ == "__main__":
    main()
