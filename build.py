#!/usr/bin/env python3
"""Builds the site. Reads content/, writes HTML next to it, no dependencies.

Output lands in the repo root because GitHub Pages serves the repo root, so
there is no separate publish directory to keep in sync.
"""

from __future__ import annotations

import html
import re
import shutil
import tomllib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import format_datetime
from urllib.parse import urljoin
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"

# Everything the generator writes, cleared before a build so a deleted piece of
# content cannot leave an orphan page behind in the repo.
OUTPUTS = ["index.html", "404.html", "feed.xml", "projects", "drawings", "notes", "about", "colophon"]


# --------------------------------------------------------------------------- md


def md_inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", out)
    return out


def markdown(src: str) -> str:
    """Enough Markdown for the things I actually write, and nothing else."""
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
            lang = stripped[3:].strip()
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{lang}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(body))}</code></pre>")
            continue

        if re.match(r"^-{3,}$", stripped):
            out.append("<hr>")
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            text = md_inline(m.group(2))
            slug = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
            out.append(f'<h{level} id="{slug}">{text}</h{level}>')
            i += 1
            continue

        if stripped.startswith("> "):
            body = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                body.append(lines[i].strip()[2:])
                i += 1
            out.append(f"<blockquote><p>{md_inline(' '.join(body))}</p></blockquote>")
            continue

        if re.match(r"^[-*]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
            ordered = bool(re.match(r"^\d+\.\s+", stripped))
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            pattern = r"^\d+\.\s+" if ordered else r"^[-*]\s+"
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                items.append(md_inline(re.sub(pattern, "", lines[i].strip())))
                i += 1
            body = "".join(f"<li>{it}</li>" for it in items)
            out.append(f"<{tag}>{body}</{tag}>")
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|```|>\s|[-*]\s|\d+\.\s|-{3,}$)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{md_inline(' '.join(para))}</p>")

    return "\n".join(out)


def read_doc(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("+++"):
        return {}, raw
    _, fm, body = raw.split("+++", 2)
    return tomllib.loads(fm), body.strip()


# ------------------------------------------------------------------------ model


@dataclass
class Project:
    slug: str
    meta: dict
    body: str

    @property
    def title(self) -> str:
        return self.meta["title"]

    @property
    def frames(self) -> list[dict]:
        return self.meta.get("frames", [])


@dataclass
class Post:
    slug: str
    meta: dict
    body: str


@dataclass
class Site:
    cfg: dict
    projects: list[Project] = field(default_factory=list)
    posts: list[Post] = field(default_factory=list)


def load() -> Site:
    cfg = tomllib.loads((CONTENT / "site.toml").read_text(encoding="utf-8"))
    site = Site(cfg=cfg)

    for path in sorted((CONTENT / "projects").glob("*.md")):
        meta, body = read_doc(path)
        site.projects.append(Project(slug=path.stem, meta=meta, body=body))

    roll_order = {r["id"]: n for n, r in enumerate(cfg["rolls"])}
    site.projects.sort(key=lambda p: (roll_order.get(p.meta["roll"], 99), p.meta.get("order", 99)))

    for path in sorted((CONTENT / "posts").glob("*.md")):
        meta, body = read_doc(path)
        site.posts.append(Post(slug=path.stem, meta=meta, body=body))
    site.posts.sort(key=lambda p: p.meta["date"], reverse=True)

    return site


# --------------------------------------------------------------------- template

# Displacement noise is what makes the grease pencil look drawn instead of
# plotted; without it every ring on the page is identical.
_WOBBLE = "".join(
    f'<filter id="wobble{i}"><feTurbulence type="fractalNoise" baseFrequency="{f}" '
    f'numOctaves="3" seed="{seed}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" '
    f'scale="{scale}" xChannelSelector="R" yChannelSelector="G"/></filter>'
    for i, (f, seed, scale) in enumerate([(0.021, 7, 6), (0.03, 41, 5), (0.016, 19, 8)])
)
DEFS = f'<svg class="defs" aria-hidden="true" focusable="false"><defs>{_WOBBLE}</defs></svg>'

# The one bit of me that is not about software. Small on purpose.
PAW = ('<svg class="paw" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
       '<ellipse cx="5.4" cy="9.6" rx="2.4" ry="3.2"/>'
       '<ellipse cx="10.8" cy="6.2" rx="2.5" ry="3.5"/>'
       '<ellipse cx="16.6" cy="7.4" rx="2.4" ry="3.3"/>'
       '<ellipse cx="20.8" cy="12.4" rx="2.1" ry="2.7"/>'
       '<path d="M11.6 12.2c3.5 0 6.4 2.9 6.4 5.6 0 2.1-1.8 3.3-3.9 3.3-1.3 0-1.9-.5-3.2-.5'
       's-1.9.5-3.2.5c-2.1 0-3.9-1.2-3.9-3.3 0-2.7 2.9-5.6 6.4-5.6z"/></svg>')


# A rough rectangle rather than an oval: a chinagraph mark follows the frame it
# is marking, and an oval hides too much of the picture underneath.
RING_PATH = (
    "M 24,28 C 70,16 236,13 279,21 C 291,54 292,148 283,177 C 238,190 62,192 21,179 "
    "C 10,148 9,52 19,25 C 44,16 118,13 168,15"
)
def ring(seed: int) -> str:
    return (f'<svg class="ring ring-{seed % 3}" viewBox="0 0 300 200" aria-hidden="true" '
            f'focusable="false"><path d="{RING_PATH}"/></svg>')


def page(site: Site, *, depth: int, title: str, desc: str, body: str, nav_key: str, wide: bool = False) -> str:
    cfg = site.cfg
    up = "../" * depth
    nav = "".join(
        '<a class="{cls}" href="{href}">{label}</a>'.format(
            cls="nav-link is-here" if item["href"] == nav_key else "nav-link",
            href=up + item["href"] if item["href"] else up or "./",
            label=html.escape(item["label"]),
        )
        for item in cfg["nav"]
    )
    full_title = title if title == cfg["title"] else f"{title} // {cfg['title']}"
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="{html.escape(cfg['author'])}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="{up}static/favicon.png">
<link rel="alternate" type="application/rss+xml" title="{html.escape(cfg['title'])} notes" href="{up}feed.xml">
<link rel="stylesheet" href="{up}static/style.css">
</head>
<body{' class="wide"' if wide else ''}>
{DEFS}
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <a class="brand" href="{up or './'}">{PAW} milo tek</a>
  <nav class="nav">{nav}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="foot-row">
    <span class="mono dim">{html.escape(cfg['author'])}</span>
    <span class="mono dim">sheet updated {cfg['updated']}</span>
    <span class="mono dim"><a href="{up}feed.xml">rss</a> &middot; <a href="{up}colophon/">colophon</a> &middot; <a href="https://github.com/milotek/wst17">source</a></span>
  </div>
</footer>
</body>
</html>
"""


def frame_html(*, up: str, img: str | None, number: str, title: str, meta: str, blurb: str,
               href: str | None, pick: bool, alt: str, seed: int = 0,
               slate: list[str] | None = None) -> str:
    """One frame on a sheet.

    A project with nothing I am allowed or able to photograph gets a typed slate
    instead of a picture, which carries the stack rather than leaving a hole.
    """
    cls = "frame" + (" is-pick" if pick else "") + (" is-blank" if not img else "")
    if img:
        inner = (
            f'<img src="{up}static/img/frame/{img}.jpg" alt="{html.escape(alt)}" '
            f'width="840" height="560" loading="lazy" decoding="async">'
        )
    else:
        meta_line = " / ".join(slate) if slate else ""
        inner = (
            '<span class="slate">'
            '<span class="slate-mark" aria-hidden="true">+</span>'
            f'<span class="slate-title mono">{html.escape(title)}</span>'
            '<span class="slate-rule"></span>'
            f'<span class="slate-meta mono">{html.escape(meta_line)}</span>'
            '<span class="slate-foot mono">no frame on this roll</span>'
            '</span>'
        )
    ring_html = ring(seed) if pick else ""
    window = f'<span class="window">{inner}{ring_html}</span>'
    if href:
        window = f'<a class="frame-link" href="{href}">{window}</a>'
    caption_title = f'<a href="{href}">{html.escape(title)}</a>' if href else html.escape(title)
    blurb_html = f'<p class="frame-blurb">{md_inline(blurb)}</p>' if blurb else ""
    meta_html = f'<span class="frame-meta mono">{html.escape(meta)}</span>' if meta else ""
    return f"""<figure class="{cls}">
{window}
<figcaption class="frame-cap">
  <span class="frame-no mono">{number}</span>
  <span class="frame-title">{caption_title}</span>
  {meta_html}
  {blurb_html}
</figcaption>
</figure>"""



def full_href(up: str, img: str) -> str:
    """Full-size copies keep their original extension; the GIFs are animated."""
    for ext in ("jpg", "gif", "png"):
        if (STATIC / "img" / "full" / f"{img}.{ext}").exists():
            return f"{up}static/img/full/{img}.{ext}"
    return f"{up}static/img/frame/{img}.jpg"


def sheet(edge: str, frames_html: str, *, ident: str = "", label: str = "", variant: str = "") -> str:
    head = f'<h2 class="roll-label" id="{ident}">{html.escape(label)}</h2>' if label else ""
    return f"""<section class="sheet">
{head}
<div class="edge"><span class="edge-text mono">{html.escape(edge)}</span></div>
<div class="strip{variant}">
{frames_html}
</div>
<div class="edge edge-flip"><span class="edge-text mono">{html.escape(edge)}</span></div>
</section>"""


# ----------------------------------------------------------------------- pages


def project_href(up: str, p: Project) -> str:
    return f"{up}projects/{p.slug}/"


def render_index(site: Site) -> str:
    cfg = site.cfg
    picks = [p for p in site.projects if p.meta.get("pick")]

    frames = []
    for n, p in enumerate(picks, start=1):
        img = p.frames[0]["img"] if p.frames else None
        frames.append(frame_html(
            up="", img=img, number=f"{n:02d}A", title=p.title,
            meta=p.meta.get("year", ""), blurb=p.meta.get("blurb", ""),
            href=project_href("", p), pick=True, alt=f"{p.title} screenshot", seed=n,
            slate=p.meta.get("stack"),
        ))

    links = "".join(
        '<li><span class="mono dim">{label}</span> <a href="{href}"{ext}>{handle}</a></li>'.format(
            label=html.escape(l["label"]),
            href=l["href"],
            handle=html.escape(l["handle"]),
            ext="" if l.get("local") else ' rel="me"',
        )
        for l in cfg["links"]
    )

    buttons = button_html("")

    latest = site.posts[0]
    counts = {}
    for p in site.projects:
        counts[p.meta["roll"]] = counts.get(p.meta["roll"], 0) + 1
    roll_lines = "".join(
        f'<li><a href="projects/#{r["id"]}">{html.escape(r["label"])}</a> '
        f'<span class="mono dim">{counts.get(r["id"], 0)} frames</span></li>'
        for r in cfg["rolls"]
    )

    body = f"""
<section class="hero">
  <div class="hero-main">
    <p class="kicker mono">Contact sheet // {html.escape(cfg['author'])}</p>
    <h1 class="hero-name">milo<span class="hero-dim">tek</span></h1>
    <p class="hero-line">Software Engineer (Apprentice) at <strong>Google</strong>, on the Search app for mobile. Backend and infrastructure. London.</p>
    <p class="hero-line dim">I'm 19. I build things at weekends too, and I draw. Below is one frame per project, marked up like a proof sheet: the ringed ones are the ones I'd print.</p>
    <p class="hero-cta"><a class="btn" href="projects/">All projects</a><a class="btn btn-ghost" href="static/cv.pdf">CV (PDF)</a></p>
  </div>
  <aside class="hero-side">
    <h2 class="side-h mono">Find me</h2>
    <ul class="linklist">{links}</ul>
  </aside>
</section>

{sheet("MILOTEK 400 // SELECTS // " + cfg['updated'].replace('-', ' '), "".join(frames), variant=" strip-selects")}

<section class="cols">
  <div class="col">
    <h2 class="side-h mono">The rolls</h2>
    <ul class="rolls">{roll_lines}</ul>
  </div>
  <div class="col">
    <h2 class="side-h mono">Latest note</h2>
    <p class="note-line"><a href="notes/{latest.slug}/">{html.escape(latest.meta['title'])}</a></p>
    <p class="dim">{html.escape(latest.meta.get('summary', ''))}</p>
    <p class="mono dim small">{latest.meta['date']} &middot; <a href="notes/">all notes</a></p>
  </div>
  <div class="col">
    <h2 class="side-h mono">Elsewhere</h2>
    <p class="dim">A wall of 88&times;31s, the way it should be.</p>
    {buttons}
  </div>
</section>
"""
    return page(site, depth=0, title=cfg["title"], desc=cfg["description"], body=body, nav_key="", wide=True)


def button_html(up: str) -> str:
    cfg = SITE.cfg
    out = []
    for b in cfg["buttons"]:
        img = (
            f'<img src="{up}static/buttons/{b["img"]}" alt="{html.escape(b["alt"])}" '
            f'width="88" height="31" loading="lazy">'
        )
        if b.get("href"):
            out.append(f'<a class="btn88" href="{b["href"]}" title="{html.escape(b.get("title", b["alt"]))}">{img}</a>')
        else:
            out.append(f'<span class="btn88" title="{html.escape(b["alt"])}">{img}</span>')
    out.append('<span class="btn88 btn88-slot" title="Room for yours"><span class="mono">your<br>88&times;31</span></span>')
    return f'<div class="buttons">{"".join(out)}</div>'


def render_projects(site: Site) -> str:
    cfg = site.cfg
    sections = []
    for roll in cfg["rolls"]:
        items = [p for p in site.projects if p.meta["roll"] == roll["id"]]
        if not items:
            continue
        frames = []
        for n, p in enumerate(items, start=1):
            img = p.frames[0]["img"] if p.frames else None
            frames.append(frame_html(
                up="../", img=img, number=f"{n:02d}A", title=p.title,
                meta=p.meta.get("year", ""), blurb=p.meta.get("blurb", ""),
                href=f"{p.slug}/", pick=bool(p.meta.get("pick")),
                alt=f"{p.title} screenshot", seed=n, slate=p.meta.get("stack"),
            ))
        sections.append(sheet(roll["edge"], "".join(frames), ident=roll["id"], label=roll["label"]))

    body = f"""
<section class="page-head">
  <p class="kicker mono">Four rolls // {len(site.projects)} frames</p>
  <h1>Projects</h1>
  <p class="lede">Work, apps, games and the small things. Ringed frames are the ones I'd print; everything else is here because it taught me something or it still runs.</p>
</section>
{''.join(sections)}
"""
    return page(site, depth=1, title="Projects", desc="Everything Milo Tekchandani has built, laid out as a contact sheet.", body=body, nav_key="projects/", wide=True)


def render_project(site: Site, p: Project) -> str:
    up = "../../"
    meta_rows = []
    for key, label in (("year", "Year"), ("kind", "Kind"), ("status", "Status")):
        if p.meta.get(key):
            meta_rows.append(f'<div class="spec"><dt class="mono">{label}</dt><dd>{html.escape(p.meta[key])}</dd></div>')
    if p.meta.get("stack"):
        stack = " &middot; ".join(html.escape(s) for s in p.meta["stack"])
        meta_rows.append(f'<div class="spec"><dt class="mono">Built with</dt><dd>{stack}</dd></div>')
    if p.meta.get("url"):
        meta_rows.append(
            f'<div class="spec"><dt class="mono">Source</dt>'
            f'<dd><a href="{p.meta["url"]}">{html.escape(p.meta.get("url_label", p.meta["url"]))}</a></dd></div>'
        )

    if p.frames:
        frames = "".join(
            frame_html(
                up=up, img=f["img"], number=f"{n:02d}A", title=f.get("caption", ""),
                meta="", blurb="", href=full_href(up, f["img"]),
                pick=False, alt=f"{p.title}: {f.get('caption', '')}",
            )
            for n, f in enumerate(p.frames, start=1)
        )
        edge = f"MILOTEK 400 // {p.title.upper()} // {p.meta.get('year', '')}"
        gallery = sheet(edge, frames)
    else:
        gallery = ""

    roll = next(r for r in site.cfg["rolls"] if r["id"] == p.meta["roll"])
    others = [q for q in site.projects if q.meta["roll"] == p.meta["roll"] and q.slug != p.slug]
    siblings = "".join(
        f'<li><a href="../{q.slug}/">{html.escape(q.title)}</a>'
        f'<span class="mono dim">{html.escape(q.meta.get("year", ""))}</span></li>'
        for q in others
    )
    source_btn = (
        f'<p class="aside-cta"><a class="btn btn-ghost" href="{p.meta["url"]}">View source</a></p>'
        if p.meta.get("url") else ""
    )
    body = f"""
<article class="project">
  <header class="page-head">
    <p class="kicker mono"><a href="../#{roll['id']}">{html.escape(roll['label'])}</a></p>
    <h1>{html.escape(p.title)}</h1>
    <p class="lede">{md_inline(p.meta.get('blurb', ''))}</p>
    <dl class="specs">{''.join(meta_rows)}</dl>
  </header>
  {gallery}
  <div class="project-body">
    <div class="prose">{markdown(p.body)}</div>
    <aside class="project-aside">
      {source_btn}
      <h2 class="side-h mono">Also in {html.escape(roll['label'])}</h2>
      <ul class="rolls">{siblings}</ul>
      <p class="backlink mono"><a href="../">&larr; back to the sheet</a></p>
    </aside>
  </div>
</article>
"""
    desc = p.meta.get("blurb", p.title)
    return page(site, depth=2, title=p.title, desc=desc, body=body, nav_key="projects/", wide=bool(p.frames))


def render_drawings(site: Site) -> str:
    cfg = tomllib.loads((CONTENT / "drawings.toml").read_text(encoding="utf-8"))
    frames = "".join(
        frame_html(
            up="../", img=f["img"], number=f"{n:02d}A", title=f["caption"],
            meta=f.get("year", ""), blurb=f.get("note", ""),
            href=full_href("../", f["img"]), pick=False, alt=f["caption"],
        )
        for n, f in enumerate(cfg["frame"], start=1)
    )
    body = f"""
<section class="page-head">
  <p class="kicker mono">One roll // {len(cfg['frame'])} frames</p>
  <h1>Drawings</h1>
  <p class="lede">{html.escape(cfg['intro'])}</p>
</section>
{sheet("MILOTEK 400 // ROLL 05 // DRAWINGS // 2022-2024", frames)}
<p class="backlink mono">Click any frame for the full size.</p>
"""
    return page(site, depth=1, title="Drawings", desc="Drawings by Milo Tekchandani, mostly Procreate.", body=body, nav_key="drawings/", wide=True)


def render_notes(site: Site) -> str:
    meta, _ = read_doc(CONTENT / "pages" / "notes-intro.md")
    items = "".join(
        f"""<li class="note-item">
  <span class="mono dim note-date">{p.meta['date']}</span>
  <a class="note-title" href="{p.slug}/">{html.escape(p.meta['title'])}</a>
  <p class="dim">{html.escape(p.meta.get('summary', ''))}</p>
</li>"""
        for p in site.posts
    )
    body = f"""
<section class="page-head">
  <p class="kicker mono">{len(site.posts)} note{'s' if len(site.posts) != 1 else ''} // <a href="../feed.xml">rss</a></p>
  <h1>{html.escape(meta['title'])}</h1>
  <p class="lede">{html.escape(meta['subtitle'])}</p>
</section>
<ul class="notes">{items}</ul>
"""
    return page(site, depth=1, title="Notes", desc="Occasional writing by Milo Tekchandani.", body=body, nav_key="notes/")


def render_post(site: Site, post: Post) -> str:
    body = f"""
<article class="prose post">
  <header class="page-head">
    <p class="kicker mono">{post.meta['date']}</p>
    <h1>{html.escape(post.meta['title'])}</h1>
  </header>
  {markdown(post.body)}
  <p class="backlink mono"><a href="../">&larr; all notes</a></p>
</article>
"""
    return page(site, depth=2, title=post.meta["title"], desc=post.meta.get("summary", ""), body=body, nav_key="notes/")


def render_page(site: Site, name: str, nav_key: str, extra: str = "") -> str:
    meta, src = read_doc(CONTENT / "pages" / f"{name}.md")
    body = f"""
<article class="prose page">
  <header class="page-head">
    <p class="kicker mono">{html.escape(meta['subtitle'])}</p>
    <h1>{html.escape(meta['title'])}</h1>
  </header>
  {markdown(src)}
  {extra}
</article>
"""
    return page(site, depth=1, title=meta["title"], desc=meta["subtitle"], body=body, nav_key=nav_key)


def render_404(site: Site) -> str:
    base = site.cfg["base_url"].split("//", 1)[1]
    base = base[base.index("/"):]
    body = f"""
<section class="page-head">
  <p class="kicker mono">404 // frame not on this roll</p>
  <h1>Nothing here</h1>
  <p class="lede">That page does not exist, or it did and I moved it.</p>
  <p class="hero-cta"><a class="btn" href="{base}">Back to the sheet</a></p>
</section>
"""
    out = page(site, depth=0, title="404", desc="Page not found.", body=body, nav_key="")
    # A 404 can be served from any depth, so its own asset and nav links have to
    # be absolute rather than relative to wherever the miss happened.
    return out.replace('href="static/', f'href="{base}static/').replace('href="./"', f'href="{base}"').replace(
        'href="projects/', f'href="{base}projects/').replace('href="drawings/', f'href="{base}drawings/').replace(
        'href="notes/', f'href="{base}notes/').replace('href="about/', f'href="{base}about/').replace(
        'href="colophon/', f'href="{base}colophon/').replace('href="feed.xml"', f'href="{base}feed.xml"')


def render_feed(site: Site) -> str:
    cfg = site.cfg
    base = cfg["base_url"]
    items = []
    for p in site.posts:
        dt = datetime.strptime(p.meta["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        link = f"{base}notes/{p.slug}/"
        # Feed readers have no page to resolve against, so the relative links a
        # post uses on the site have to be absolutised here.
        content = re.sub(
            r'href="(?!https?:|mailto:|#)([^"]+)"',
            lambda m: f'href="{urljoin(link, m.group(1))}"',
            markdown(p.body),
        )
        items.append(f"""  <item>
    <title>{html.escape(p.meta['title'])}</title>
    <link>{link}</link>
    <guid isPermaLink="true">{link}</guid>
    <pubDate>{format_datetime(dt)}</pubDate>
    <description>{html.escape(p.meta.get('summary', ''))}</description>
    <content:encoded><![CDATA[{content}]]></content:encoded>
  </item>""")
    return f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
  <title>{html.escape(cfg['title'])} // notes</title>
  <link>{base}</link>
  <atom:link href="{base}feed.xml" rel="self" type="application/rss+xml"/>
  <description>{html.escape(cfg['description'])}</description>
  <language>en-GB</language>
  <lastBuildDate>{format_datetime(datetime.strptime(cfg['updated'], '%Y-%m-%d').replace(tzinfo=timezone.utc))}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
"""


# ------------------------------------------------------------------------ write


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"  {path.relative_to(ROOT)}")


def main() -> None:
    global SITE
    SITE = load()
    site = SITE

    for name in OUTPUTS:
        target = ROOT / name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()

    print("building:")
    write(ROOT / "index.html", render_index(site))
    write(ROOT / "projects" / "index.html", render_projects(site))
    for p in site.projects:
        write(ROOT / "projects" / p.slug / "index.html", render_project(site, p))
    write(ROOT / "drawings" / "index.html", render_drawings(site))
    write(ROOT / "notes" / "index.html", render_notes(site))
    for post in site.posts:
        write(ROOT / "notes" / post.slug / "index.html", render_post(site, post))

    cv_note = (
        '<p class="cv-embed-wrap"><a class="btn" href="../static/cv.pdf">Download CV (PDF)</a></p>'
        '<object class="cv-embed" data="../static/cv.pdf" type="application/pdf">'
        '<p class="dim">Your browser will not embed the PDF. Use the download link above.</p></object>'
    )
    write(ROOT / "about" / "index.html", render_page(site, "about", "about/", cv_note))
    write(ROOT / "colophon" / "index.html", render_page(site, "colophon", "colophon/"))
    write(ROOT / "404.html", render_404(site))
    write(ROOT / "feed.xml", render_feed(site))
    (ROOT / ".nojekyll").touch()
    print(f"done: {len(site.projects)} projects, {len(site.posts)} notes")


if __name__ == "__main__":
    main()
