#!/usr/bin/env python3
"""Build the site.

Reads content/ (TOML plus Markdown) and writes plain HTML, an RSS feed and
index.json. Standard library only, so `python3 build.py` is the whole toolchain.

Every URL it writes is relative to the page emitting it, so the output works
from a filesystem, from a domain root, or from a subpath like /wst14/ without
being reconfigured. The one exception is 404.html, which is served for URLs at
unknown depths and therefore has to use BASE.
"""

from __future__ import annotations

import html
import json
import pathlib
import re
import shutil
import struct
import tomllib
from datetime import datetime, timezone
from email.utils import format_datetime
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUT = ROOT

# ---------------------------------------------------------------------------
# tiny markdown
# ---------------------------------------------------------------------------

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
EXTERNAL = re.compile(r"^(https?:|mailto:)")


def inline(text: str) -> str:
    """Escape, then re-introduce the handful of inline constructs we allow."""
    out = html.escape(text, quote=False)
    codes: list[str] = []

    def stash(m: re.Match[str]) -> str:
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    out = INLINE_CODE.sub(stash, out)
    out = LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', out)
    out = BOLD.sub(r"<strong>\1</strong>", out)
    out = ITALIC.sub(r"<em>\1</em>", out)
    out = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", out)
    return out


def markdown(src: str) -> str:
    lines = src.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    para: list[str] = []

    def flush() -> None:
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush()
            lang = stripped[3:].strip()
            i += 1
            body: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            cls = f' class="lang-{lang}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(body))}</code></pre>")
            i += 1
            continue

        if not stripped:
            flush()
            i += 1
            continue

        if m := re.match(r"^(#{1,4})\s+(.*)$", stripped):
            flush()
            level = len(m.group(1)) + 1  # h1 is the page title, posts start at h2
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        if re.match(r"^(-{3,}|\*{3,})$", stripped):
            flush()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("> "):
            flush()
            quote: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote.append(lines[i].strip()[2:])
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(quote))}</p></blockquote>")
            continue

        if re.match(r"^[-*]\s+", stripped) or re.match(r"^\d+[.)]\s+", stripped):
            flush()
            ordered = bool(re.match(r"^\d+[.)]\s+", stripped))
            items: list[str] = []
            pat = r"^\d+[.)]\s+" if ordered else r"^[-*]\s+"
            while i < len(lines) and re.match(pat, lines[i].strip()):
                items.append(re.sub(pat, "", lines[i].strip()))
                i += 1
            tag = "ol" if ordered else "ul"
            body = "".join(f"<li>{inline(x)}</li>" for x in items)
            out.append(f"<{tag}>{body}</{tag}>")
            continue

        para.append(stripped)
        i += 1

    flush()
    return "\n".join(out)


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


# ---------------------------------------------------------------------------
# image dimensions, so nothing on the page jumps while it loads
# ---------------------------------------------------------------------------


def image_size(path: pathlib.Path) -> tuple[int, int] | None:
    try:
        data = path.open("rb").read(64)
    except OSError:
        return None
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8 ":
            w, h = struct.unpack("<HH", data[26:30])
            return w & 0x3FFF, h & 0x3FFF
        if chunk == b"VP8L":
            b = struct.unpack("<I", data[21:25])[0]
            return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
        if chunk == b"VP8X":
            w = int.from_bytes(data[24:27], "little") + 1
            h = int.from_bytes(data[27:30], "little") + 1
            return w, h
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", data[6:10])
    return None


SIZE_CACHE: dict[str, tuple[int, int] | None] = {}


def dims(rel: str) -> str:
    if rel not in SIZE_CACHE:
        SIZE_CACHE[rel] = image_size(ROOT / rel)
    size = SIZE_CACHE[rel]
    return f' width="{size[0]}" height="{size[1]}"' if size else ""


# ---------------------------------------------------------------------------
# content
# ---------------------------------------------------------------------------


def load_toml(name: str) -> dict:
    return tomllib.loads((CONTENT / name).read_text(encoding="utf-8"))


SITE = load_toml("site.toml")
PROJECTS = load_toml("projects.toml")["project"]
ART = load_toml("art.toml")
BUTTONS = load_toml("buttons.toml")

BASE = urlparse(SITE["site"]["url"]).path or "/"
SITE_URL = SITE["site"]["url"].rstrip("/") + "/"


def load_posts() -> list[dict]:
    posts = []
    for path in sorted((CONTENT / "posts").glob("*.md"), reverse=True):
        raw = path.read_text(encoding="utf-8")
        m = re.match(r"^\+\+\+\n(.*?)\n\+\+\+\n(.*)$", raw, re.S)
        if not m:
            raise SystemExit(f"{path.name}: missing +++ front matter")
        meta = tomllib.loads(m.group(1))
        meta["slug"] = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        meta["html"] = markdown(m.group(2))
        meta["words"] = len(strip_tags(meta["html"]).split())
        posts.append(meta)
    return posts


POSTS = load_posts()

NAV = [
    ("projects", "projects/"),
    ("blog", "blog/"),
    ("art", "art/"),
    ("now", "now/"),
    ("uses", "uses/"),
    ("index", "index/"),
]


# ---------------------------------------------------------------------------
# page shell
# ---------------------------------------------------------------------------


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def shell(*, depth: int, title: str, desc: str, body: str, active: str = "", wide: bool = False,
          absolute: bool = False) -> str:
    r = BASE if absolute else ("./" if depth == 0 else "../" * depth)
    full_title = title if title == SITE["site"]["title"] else f"{title} // {SITE['site']['title']}"
    nav = "".join(
        f'<a href="{r}{href}"{" class=\"on\"" if active == label else ""}>{label}</a>'
        for label, href in NAV
    )
    counts = f"{len(PROJECTS)} projects, {len(POSTS)} post{'s' if len(POSTS) != 1 else ''}, {len(ART['art']['piece'])} drawings"
    return f"""<!DOCTYPE html>
<html lang="{SITE['site']['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#1e1e2e">
<meta name="color-scheme" content="dark">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE_URL}assets/img/avatar.webp">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="milo tek" href="{r}feed.xml">
<link rel="stylesheet" href="{r}assets/fonts/fonts.css">
<link rel="stylesheet" href="{r}assets/css/site.css">
</head>
<body data-root="{r}">
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap topbar">
    <a class="mark" href="{r}"><span class="mark-dot"></span>milo tek</a>
    <nav class="nav">{nav}</nav>
  </div>
  <div class="wrap">
    <form class="q" action="{r}index/" method="get" role="search">
      <label for="q" class="q-sigil">?</label>
      <input id="q" name="q" type="search" autocomplete="off" spellcheck="false"
             placeholder="search projects, art, writing" data-full="search {counts}"
             aria-label="Search the site">
      <kbd class="q-kbd">/</kbd>
    </form>
  </div>
</header>
<main id="main" class="wrap{' wide' if wide else ''}">
<div id="results" class="results" hidden></div>
<div id="page">
{body}
</div>
</main>
<footer class="foot">
  <div class="wrap foot-in">
    <p><a href="{r}colophon/">colophon</a> &middot; <a href="{r}feed.xml">rss</a> &middot; <a href="{r}index.json">index.json</a> &middot; <a href="{r}buttons/">buttons</a></p>
    <p class="muted">Milo Tekchandani &middot; London</p>
  </div>
</footer>
<script src="{r}assets/js/search.js" defer></script>
<script src="{r}assets/js/lightbox.js" defer></script>
</body>
</html>
"""


def write(rel: str, text: str) -> None:
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# fragments
# ---------------------------------------------------------------------------


def tag_list(tags: list[str], r: str) -> str:
    return "".join(f'<a class="tag" href="{r}index/?q={esc(t)}">{esc(t)}</a>' for t in tags)


def shot_src(shot: dict, thumb: bool = False) -> str:
    return f"assets/img/projects/{shot['src']}{'.thumb' if thumb else ''}.webp"


def project_card(p: dict, r: str, eager: bool = False) -> str:
    shots = p.get("shots") or []
    if shots:
        src = shot_src(shots[0], thumb=True)
        thumb = (f'<div class="card-shot"><img src="{r}{src}" alt="{esc(shots[0]["alt"])}"'
                 f'{dims(src)} loading="{"eager" if eager else "lazy"}" decoding="async"></div>')
    else:
        # No screenshot: draw a band anyway so the grid keeps its rhythm.
        thumb = f'<div class="card-shot blank"><span>{esc(p["slug"])}</span></div>' 
    return f"""<a class="card" href="{r}projects/{p['slug']}/">
  {thumb}
  <div class="card-body">
    <div class="card-head"><h3>{esc(p['title'])}</h3><span class="yr">{esc(p['year'])}</span></div>
    <p>{esc(p['blurb'])}</p>
    <div class="card-tags">{''.join(f'<span class="tag">{esc(t)}</span>' for t in p.get('tags', [])[:4])}</div>
  </div>
</a>"""


def row(kind: str, title: str, href: str, meta: str, blurb: str) -> str:
    return f"""<a class="row" href="{href}">
  <span class="row-kind">{esc(kind)}</span>
  <span class="row-main"><span class="row-title">{esc(title)}</span><span class="row-blurb">{esc(blurb)}</span></span>
  <span class="row-meta">{esc(meta)}</span>
</a>"""


def buttons_wall(r: str, limit: int | None = None) -> str:
    out = []
    mine = BUTTONS.get("mine", [])
    if limit:
        mine = mine[:limit]
    for b in mine:
        src = f"assets/img/buttons/{b['file']}.png"
        img = f'<img src="{r}{src}" alt="{esc(b["alt"])}" width="88" height="31" loading="lazy">'
        out.append(f'<a href="{esc(b["href"])}" class="btn88">{img}</a>' if b.get("href") else f'<span class="btn88">{img}</span>')
    for b in BUTTONS.get("wall", []):
        src = f"assets/img/buttons/{b['file']}"
        out.append(f'<a href="{esc(b["href"])}" class="btn88"><img src="{r}{src}" alt="{esc(b["alt"])}" width="88" height="31" loading="lazy"></a>')
    if limit is None:
        for _ in range(BUTTONS.get("slots", {}).get("empty", 0)):
            out.append('<span class="btn88 empty" aria-hidden="true">your<br>button</span>')
    return f'<div class="wall">{"".join(out)}</div>'


# ---------------------------------------------------------------------------
# pages
# ---------------------------------------------------------------------------


def page_home() -> None:
    r = "./"
    s, w = SITE["site"], SITE["work"]
    intro = "".join(f"<p>{inline(line)}</p>" for line in SITE["intro"]["lines"])
    links = "".join(
        f'<a class="link" href="{esc(l["href"])}"><span>{esc(l["label"])}</span><small>{esc(l["note"])}</small></a>'
        for l in SITE["links"]
    )
    featured = [p for p in PROJECTS if p.get("featured")]
    cards = "".join(project_card(p, r, eager=i < 3) for i, p in enumerate(featured))
    bullets = "".join(f"<li>{inline(b)}</li>" for b in w["bullets"])
    post = POSTS[0]
    now_items = "".join(f"<li>{inline(x)}</li>" for x in SITE["now"]["items"][:3])

    body = f"""<section class="hero">
  <img class="avatar" src="{r}assets/img/avatar.webp" alt="Milo's avatar, a white line drawing on pink" width="400" height="400">
  <div class="hero-text">
    <h1>Milo Tekchandani</h1>
    <p class="lede">{esc(s['tagline'])}</p>
    {intro}
  </div>
</section>

<section class="links">{links}</section>

<section class="block" id="work">
  <h2 class="label">currently</h2>
  <div class="job">
    <div class="job-head">
      <h3>{esc(w['role'])}, <span class="org">{esc(w['org'])}</span></h3>
      <span class="yr">{esc(w['period'])}</span>
    </div>
    <p class="job-meta">{esc(w['team'])} &middot; {esc(w['place'])}</p>
    <p>{esc(w['summary'])}</p>
    <ul class="ticks">{bullets}</ul>
  </div>
</section>

<section class="block">
  <div class="block-head"><h2 class="label">selected projects</h2><a class="more" href="{r}projects/">all {len(PROJECTS)} &rarr;</a></div>
  <div class="cards">{cards}</div>
</section>

<section class="block split">
  <div>
    <div class="block-head"><h2 class="label">writing</h2><a class="more" href="{r}blog/">blog &rarr;</a></div>
    <a class="post-teaser" href="{r}blog/{post['slug']}/">
      <h3>{esc(post['title'])}</h3>
      <p class="muted mono">{esc(post['date'])} &middot; {post['words']} words</p>
      <p>{esc(post['summary'])}</p>
    </a>
  </div>
  <div>
    <div class="block-head"><h2 class="label">now</h2><a class="more" href="{r}now/">more &rarr;</a></div>
    <ul class="ticks">{now_items}</ul>
  </div>
</section>

<section class="block">
  <div class="block-head"><h2 class="label">88x31</h2><a class="more" href="{r}buttons/">the wall &rarr;</a></div>
  {buttons_wall(r, limit=8)}
</section>
"""
    write("index.html", shell(depth=0, title=SITE["site"]["title"], desc=s["description"], body=body))


def page_projects() -> None:
    r = "../"
    cards = "".join(project_card(p, r, eager=i < 3) for i, p in enumerate(PROJECTS))
    body = f"""<h1>Projects</h1>
<p class="lede">{len(PROJECTS)} of them. Search or click a tag to narrow it down.</p>
<div class="cards">{cards}</div>"""
    write("projects/index.html", shell(depth=1, title="Projects", active="projects",
                                       desc=f"{len(PROJECTS)} projects by Milo Tekchandani.", body=body, wide=True))


def page_project(p: dict) -> None:
    r = "../../"
    links = "".join(f'<a class="pill" href="{esc(l["href"])}">{esc(l["label"])}</a>' for l in p.get("links", []))
    shots = ""
    for shot in p.get("shots", []) or []:
        full, thumb = shot_src(shot), shot_src(shot, thumb=True)
        shots += (f'<figure class="shot"><a href="{r}{full}">'
                  f'<img src="{r}{full}" srcset="{r}{thumb} 720w, {r}{full} 1400w"'
                  f' sizes="(max-width: 820px) 92vw, 640px" alt="{esc(shot["alt"])}"{dims(full)}'
                  f' loading="lazy" decoding="async"></a>'
                  f'<figcaption>{esc(shot["alt"])}</figcaption></figure>')
    body_md = markdown(p.get("body", "").strip()) if p.get("body") else ""
    meta = " &middot; ".join(filter(None, [esc(p["year"]), esc(p.get("kind", "")), esc(p.get("status", ""))]))
    body = f"""<article class="detail">
  <p class="crumb"><a href="{r}projects/">&larr; projects</a></p>
  <h1>{esc(p['title'])}</h1>
  <p class="muted mono">{meta}</p>
  <p class="lede">{esc(p['blurb'])}</p>
  <div class="tags">{tag_list(p.get('tags', []), r)}</div>
  {f'<div class="pills">{links}</div>' if links else ''}
  <div class="prose">{body_md}</div>
  {f'<div class="shots">{shots}</div>' if shots else ''}
</article>"""
    write(f"projects/{p['slug']}/index.html",
          shell(depth=2, title=p["title"], active="projects", desc=p["blurb"], body=body))


def page_blog() -> None:
    r = "../"
    items = "".join(
        f'<a class="post-teaser" href="{r}blog/{p["slug"]}/"><h3>{esc(p["title"])}</h3>'
        f'<p class="muted mono">{esc(p["date"])} &middot; {p["words"]} words</p>'
        f'<p>{esc(p["summary"])}</p></a>'
        for p in POSTS
    )
    body = f"""<h1>Blog</h1>
<p class="lede">Occasional. There's an <a href="{r}feed.xml">RSS feed</a>.</p>
<div class="post-list">{items}</div>"""
    write("blog/index.html", shell(depth=1, title="Blog", active="blog", desc="Writing by Milo Tekchandani.", body=body))


def page_post(p: dict) -> None:
    r = "../../"
    tags = tag_list(p.get("tags", []), r)
    body = f"""<article class="detail">
  <p class="crumb"><a href="{r}blog/">&larr; blog</a></p>
  <h1>{esc(p['title'])}</h1>
  <p class="muted mono">{esc(p['date'])} &middot; {p['words']} words</p>
  <div class="tags">{tags}</div>
  <div class="prose">{p['html']}</div>
</article>"""
    write(f"blog/{p['slug']}/index.html",
          shell(depth=2, title=p["title"], active="blog", desc=p["summary"], body=body))


def page_art() -> None:
    r = "../"
    pieces = ART["art"]["piece"]
    cells = ""
    for i, piece in enumerate(pieces):
        ext = piece.get("ext", "webp")
        full = f"assets/img/art/{piece['src']}.{ext}"
        thumb = f"assets/img/art/{piece['src']}.thumb.webp"
        pid = piece["src"]
        cells += f"""<figure class="art-cell" id="{pid}">
  <a href="{r}{full}" class="art-open" data-cap="{esc(piece['caption'])}" data-title="{esc(piece['title'])}">
    <img src="{r}{thumb}" alt="{esc(piece['title'])}"{dims(thumb)} loading="{'eager' if i < 4 else 'lazy'}" decoding="async">
  </a>
  <figcaption><b>{esc(piece['title'])}</b> <span class="muted mono">{esc(piece['year'])}</span><br>{esc(piece['caption'])}</figcaption>
</figure>"""
    body = f"""<h1 id="gallery">Art</h1>
<p class="lede">{inline(ART['art']['intro'])}</p>
<div class="art-grid">{cells}</div>"""
    write("art/index.html", shell(depth=1, title="Art", active="art",
                                  desc="Drawings by Milo Tekchandani.", body=body, wide=True))


def page_now() -> None:
    r = "../"
    items = "".join(f"<li>{inline(x)}</li>" for x in SITE["now"]["items"])
    body = f"""<h1>Now</h1>
<p class="muted mono">last updated {esc(SITE['now']['updated'])}</p>
<p class="lede">{esc(SITE['now']['intro'])}</p>
<ul class="ticks big">{items}</ul>
"""
    write("now/index.html", shell(depth=1, title="Now", active="now", desc="What Milo is working on right now.", body=body))


def page_uses() -> None:
    groups = ""
    for g in SITE["uses"]["group"]:
        items = "".join(f"<li>{inline(x)}</li>" for x in g["items"])
        groups += f'<section class="block"><h2 class="label">{esc(g["name"])}</h2><ul class="ticks">{items}</ul></section>'
    body = f"""<h1>Uses</h1>
<p class="lede">{inline(SITE['uses']['intro'])}</p>
{groups}"""
    write("uses/index.html", shell(depth=1, title="Uses", active="uses", desc="Milo's setup: NixOS, Hyprland, Ghostty, Neovim.", body=body))


def page_colophon() -> None:
    r = "../"
    lines = "".join(f"<p>{inline(x)}</p>" for x in SITE["colophon"]["lines"])
    body = f"""<h1>Colophon</h1>
<div class="prose">{lines}</div>
<section class="block">
  <h2 class="label">the numbers</h2>
  <ul class="ticks">
    <li>{len(PROJECTS)} projects, {len(POSTS)} post, {len(ART['art']['piece'])} drawings, {len(BUTTONS.get('mine', []))} buttons.</li>
    <li>One Python file, no dependencies.</li>
    <li>Fonts, images and scripts all served from this repo. Nothing phones home.</li>
  </ul>
</section>
<p><a class="pill" href="{r}index.json">index.json</a> <a class="pill" href="{r}feed.xml">feed.xml</a></p>"""
    write("colophon/index.html", shell(depth=1, title="Colophon", desc="How this site is built.", body=body))


def page_buttons() -> None:
    r = "../"
    body = f"""<h1>88&times;31</h1>
<p class="lede">{inline(SITE['buttons']['intro'])}</p>
{buttons_wall(r)}
<p class="muted">{inline(SITE['buttons']['mine_note'])}</p>
<section class="block">
  <h2 class="label">taking one</h2>
<pre><code>&lt;a href="{SITE_URL}"&gt;
  &lt;img src="{SITE_URL}assets/img/buttons/milo-tek.png"
       width="88" height="31" alt="milo tek"&gt;
&lt;/a&gt;</code></pre>
</section>
"""
    write("buttons/index.html", shell(depth=1, title="88x31 buttons", desc="Milo's 88x31 button wall.", body=body))


def records() -> list[dict]:
    out: list[dict] = []
    for p in PROJECTS:
        out.append({"k": "project", "t": p["title"], "u": f"projects/{p['slug']}/", "d": p["blurb"],
                    "g": p.get("tags", []), "y": p["year"], "s": p.get("status", "")})
    for p in POSTS:
        out.append({"k": "post", "t": p["title"], "u": f"blog/{p['slug']}/", "d": p["summary"],
                    "g": p.get("tags", []), "y": p["date"][:4], "s": p["date"]})
    for a in ART["art"]["piece"]:
        out.append({"k": "art", "t": a["title"], "u": f"art/#{a['src']}", "d": a["caption"],
                    "g": ["art", "drawing"], "y": a["year"], "s": ""})
    pages = [("Now", "now/", SITE["now"]["intro"]),
             ("Uses", "uses/", "NixOS, Hyprland, Ghostty, Neovim, and the rest of the setup."),
             ("Colophon", "colophon/", "How this site is built."),
             ("88x31 buttons", "buttons/", "The button wall. Take one."),
             ("Blog", "blog/", "All posts."),
             ("Projects", "projects/", "Every project."),
             ("CV (PDF)", "https://github.com/milotek/milotek/raw/main/CV.pdf", "The CV. Predates the Google job.")]
    for title, url, desc in pages:
        out.append({"k": "page", "t": title, "u": url, "d": desc, "g": [], "y": "", "s": ""})
    for l in SITE["links"]:
        out.append({"k": "link", "t": l["label"], "u": l["href"], "d": l["note"], "g": [], "y": "", "s": ""})
    return out


def page_index() -> None:
    r = "../"
    groups: dict[str, list[dict]] = {}
    for rec in records():
        groups.setdefault(rec["k"], []).append(rec)
    order = ["project", "post", "art", "page", "link"]
    sections = ""
    for kind in order:
        recs = groups.get(kind, [])
        if not recs:
            continue
        rows = "".join(
            row(kind, rec["t"], (rec["u"] if EXTERNAL.match(rec["u"]) else r + rec["u"]),
                rec["y"] or rec["s"], rec["d"])
            for rec in recs
        )
        sections += f'<section class="block"><h2 class="label">{kind}s &middot; {len(recs)}</h2><div class="rows">{rows}</div></section>'
    body = f"""<h1>The index</h1>
<p class="lede">Everything on the site in one list. Search filters it, or just scroll.</p>
{sections}"""
    write("index/index.html", shell(depth=1, title="The index", active="index",
                                    desc="Every project, post, drawing and page on the site.", body=body, wide=True))


def page_404() -> None:
    body = f"""<div class="notfound">
  <img src="{BASE}assets/img/under-construction.gif" alt="A stick figure next to two gears, captioned Under Construction" width="640" height="480">
  <h1>404</h1>
  <p class="lede">Nothing here. I drew this in 2024 for exactly this occasion.</p>
  <p><a class="pill" href="{BASE}">home</a> <a class="pill" href="{BASE}index/">the index</a></p>
</div>"""
    write("404.html", shell(depth=0, title="404", desc="Page not found.", body=body, absolute=True))


def feed() -> None:
    items = ""
    for p in POSTS:
        dt = datetime.strptime(p["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        link = f"{SITE_URL}blog/{p['slug']}/"
        items += f"""  <item>
    <title>{esc(p['title'])}</title>
    <link>{link}</link>
    <guid isPermaLink="true">{link}</guid>
    <pubDate>{format_datetime(dt)}</pubDate>
    <description>{esc(p['summary'])}</description>
    <content:encoded><![CDATA[{p['html']}]]></content:encoded>
  </item>
"""
    now = format_datetime(datetime.now(timezone.utc))
    write("feed.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
  <title>{esc(SITE['site']['title'])}</title>
  <link>{SITE_URL}</link>
  <description>{esc(SITE['site']['description'])}</description>
  <language>{SITE['site']['lang']}</language>
  <lastBuildDate>{now}</lastBuildDate>
  <atom:link href="{SITE_URL}feed.xml" rel="self" type="application/rss+xml"/>
{items}</channel>
</rss>
""")


def favicon() -> None:
    write("assets/favicon.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" rx="8" fill="#1e1e2e"/>
<circle cx="14" cy="14" r="7" fill="none" stroke="#ffbdbd" stroke-width="3"/>
<path d="M19.5 19.5 L26 26" stroke="#ffbdbd" stroke-width="3.5" stroke-linecap="round"/>
</svg>
""")


def main() -> None:
    favicon()
    page_home()
    page_projects()
    for p in PROJECTS:
        page_project(p)
    page_blog()
    for p in POSTS:
        page_post(p)
    page_art()
    page_now()
    page_uses()
    page_colophon()
    page_buttons()
    page_index()
    page_404()
    feed()
    write("index.json", json.dumps({"base": BASE, "records": records()}, separators=(",", ":")))
    (OUT / ".nojekyll").touch()
    print(f"built {len(PROJECTS)} projects, {len(POSTS)} posts, {len(ART['art']['piece'])} drawings")


if __name__ == "__main__":
    main()
