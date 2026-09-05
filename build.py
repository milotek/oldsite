#!/usr/bin/env python3
"""Builds the static site from content/ into the repository root.

Everything in content/ is a Markdown file with YAML front matter, so adding a
project or a post never means touching this file. Output lands next to the
sources because GitHub Pages serves this repo from /.

  python3 build.py
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"

# Generated paths, wiped on every build. Anything not listed here is hand-authored
# and must survive.
OUTPUT_DIRS = ["work", "blog", "art", "now", "uses", "colophon", "cv"]
OUTPUT_FILES = ["index.html", "404.html", "feed.xml", "sitemap.xml", "robots.txt"]


# --------------------------------------------------------------------------- #
# YAML front matter (the subset Obsidian writes)
# --------------------------------------------------------------------------- #

SCALAR_RE = re.compile(r"^(-?\d+)$")
FLOAT_RE = re.compile(r"^-?\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _scalar(raw: str):
    v = raw.strip()
    if not v:
        return ""
    if v[0] in "\"'" and v[-1] == v[0] and len(v) > 1:
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [_scalar(p) for p in _split_commas(inner)] if inner else []
    if v.startswith("{") and v.endswith("}"):
        out = {}
        for part in _split_commas(v[1:-1]):
            if ":" in part:
                k, _, rest = part.partition(":")
                out[k.strip()] = _scalar(rest)
        return out
    low = v.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "~"):
        return None
    if SCALAR_RE.match(v):
        return int(v)
    if FLOAT_RE.match(v):
        return float(v)
    return v


def _split_commas(s: str) -> list[str]:
    """Split on commas that sit outside quotes and brackets."""
    out, depth, quote, buf = [], 0, "", []
    for ch in s:
        if quote:
            if ch == quote:
                quote = ""
            buf.append(ch)
        elif ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch in "[{":
            depth += 1
            buf.append(ch)
        elif ch in "]}":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf))
    return [p.strip() for p in out if p.strip()]


def parse_yaml(text: str):
    """Enough YAML for front matter: nested maps, lists, lists of maps."""
    lines = [l for l in text.split("\n") if l.strip() and not l.lstrip().startswith("#")]
    value, _ = _parse_block(lines, 0, 0)
    return value


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _parse_block(lines, i, indent):
    if i < len(lines) and lines[i].lstrip().startswith("- "):
        return _parse_list(lines, i, indent)
    return _parse_map(lines, i, indent)


def _parse_map(lines, i, indent):
    out = {}
    while i < len(lines):
        line = lines[i]
        ind = _indent(line)
        if ind < indent:
            break
        stripped = line.strip()
        if stripped.startswith("- "):
            break
        key, _, rest = stripped.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest:
            out[key] = _scalar(rest)
            i += 1
            continue
        # Block value: look ahead for the child indent.
        if i + 1 < len(lines) and _indent(lines[i + 1]) > ind:
            child, i = _parse_block(lines, i + 1, _indent(lines[i + 1]))
            out[key] = child
        else:
            out[key] = ""
            i += 1
    return out, i


def _parse_list(lines, i, indent):
    out = []
    while i < len(lines):
        line = lines[i]
        ind = _indent(line)
        if ind < indent or not line.strip().startswith("- "):
            break
        body = line.strip()[2:].strip()
        if ":" in body and not body.startswith(("[", "{", '"', "'")):
            # A map item; its remaining keys are indented past the dash.
            key, _, rest = body.partition(":")
            item = {key.strip(): _scalar(rest)} if rest.strip() else {}
            i += 1
            if not rest.strip():
                item[key.strip()] = ""
            while i < len(lines) and _indent(lines[i]) > ind:
                sub, i = _parse_map(lines, i, _indent(lines[i]))
                item.update(sub)
            out.append(item)
        else:
            out.append(_scalar(body))
            i += 1
    return out, i


def read_doc(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            meta = parse_yaml(raw[3:end]) or {}
            body = raw[end + 4 :]
    meta = dict(meta)
    meta["body"] = body.strip("\n")
    meta.setdefault("slug", path.stem)
    meta["_source"] = str(path.relative_to(ROOT))
    return meta


# --------------------------------------------------------------------------- #
# Markdown (the subset the content actually uses)
# --------------------------------------------------------------------------- #

def _inline(text: str, here: str) -> str:
    out = html.escape(text, quote=False)
    # Code first, so nothing inside it gets mangled afterwards.
    codes: list[str] = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    out = re.sub(r"`([^`]+)`", stash, out)
    out = re.sub(
        r"!\[([^\]]*)\]\(([^)\s]+)\)",
        lambda m: f'<img src="{url(here, m.group(2))}" alt="{html.escape(m.group(1), quote=True)}" loading="lazy" decoding="async">',
        out,
    )
    out = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{url(here, m.group(2))}"{_ext(m.group(2))}>{m.group(1)}</a>',
        out,
    )
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", out)
    # Let hand-written entities through; escaping them turns &middot; into text.
    out = re.sub(r"&amp;(#?[a-zA-Z0-9]+);", r"&\1;", out)
    return out


def _ext(href: str) -> str:
    if href.startswith(("http://", "https://")):
        return ' target="_blank" rel="noopener"'
    return ""


def markdown(text: str, here: str) -> str:
    lines = text.split("\n")
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
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>")
            continue
        if stripped in ("---", "***"):
            out.append("<hr>")
            i += 1
            continue
        if stripped.startswith("<"):
            buf = []
            while i < len(lines) and lines[i].strip():
                buf.append(lines[i])
                i += 1
            out.append("\n".join(buf))
            continue
        m = re.match(r"^(#{2,4})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            text_ = _inline(m.group(2), here)
            anchor = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
            out.append(f'<h{level} id="{anchor}">{text_}</h{level}>')
            i += 1
            continue
        if stripped.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>" + _inline(" ".join(buf), here) + "</blockquote>")
            continue
        if re.match(r"^[-*]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
            ordered = bool(re.match(r"^\d+\.\s+", stripped))
            tag = "ol" if ordered else "ul"
            items = []
            pattern = r"^\d+\.\s+" if ordered else r"^[-*]\s+"
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                items.append(_inline(re.sub(pattern, "", lines[i].strip()), here))
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{x}</li>" for x in items) + f"</{tag}>")
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(
            r"^(#{2,4}\s|[-*]\s|\d+\.\s|>\s|```|---$|<)", lines[i].strip()
        ):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>" + _inline(" ".join(buf), here) + "</p>")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# URLs. Everything is emitted relative so the site works under any base path,
# including the /wst20/ subpath it is deployed to and file:// on a laptop.
# --------------------------------------------------------------------------- #

def url(here: str, target: str) -> str:
    if target.startswith(("http://", "https://", "mailto:", "#", "data:")):
        return target
    target = target.lstrip("/")
    here = here.strip("/")
    depth = len([p for p in here.split("/") if p])
    prefix = "../" * depth
    return (prefix + target) or "./"


def absolute(site: dict, target: str) -> str:
    if target.startswith(("http://", "https://", "mailto:")):
        return target
    return site["url"].rstrip("/") + "/" + target.lstrip("/")


# --------------------------------------------------------------------------- #
# Templates
# --------------------------------------------------------------------------- #

def e(s) -> str:
    return html.escape(str(s if s is not None else ""), quote=True)


def head(site: dict, here: str, title: str, description: str, extra_class: str = "") -> str:
    u = lambda p: url(here, p)
    canonical = absolute(site, here + "/" if here else "")
    full_title = title if title == site["title"] else f"{title} · {site['title']}"
    return f"""<!DOCTYPE html>
<html lang="en-GB" class="{extra_class}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="{e(site['name'])}">
<meta name="theme-color" content="#1e1e2e">
<link rel="canonical" href="{e(canonical)}">
<link rel="icon" href="{u('assets/img/site/favicon.png')}" type="image/png">
<link rel="apple-touch-icon" href="{u('assets/img/site/apple-touch-icon.png')}">
<link rel="alternate" type="application/rss+xml" title="{e(site['title'])}" href="{u('feed.xml')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(site['title'])}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:image" content="{e(absolute(site, 'assets/img/site/icon-512.png'))}">
<meta name="twitter:card" content="summary">
<link rel="preload" as="font" type="font/woff2" href="{u('assets/fonts/sourcesans3-400-latin.woff2')}" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{u('assets/fonts/jetbrainsmono-400-latin.woff2')}" crossorigin>
<link rel="stylesheet" href="{u('assets/css/main.css')}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(site: dict, here: str, current: str) -> str:
    u = lambda p: url(here, p)
    items = []
    for item in site["nav"]:
        active = ' aria-current="page"' if item["path"].strip("/") == current else ""
        items.append(f'<a href="{u(item["path"])}"{active}>{e(item["label"])}</a>')
    return f"""<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="{u('')}">
      <img src="{u('assets/img/site/avatar.webp')}" alt="" width="30" height="30">
      <span>milo tek</span>
    </a>
    <nav class="nav" aria-label="Primary">{''.join(items)}</nav>
  </div>
</header>
<main id="main">
"""


def footer(site: dict, here: str) -> str:
    u = lambda p: url(here, p)
    links = "".join(
        f'<li><a href="{e(l["url"])}"{_ext(l["url"])}>{e(l["label"])}<span>{e(l.get("handle", ""))}</span></a></li>'
        for l in site["links"]
    )
    pages = "".join(
        f'<li><a href="{u(p["path"])}">{e(p["label"])}</a></li>' for p in site["footer_nav"]
    )
    buttons = "".join(
        f'<a class="btn88" href="{e(b["url"])}"{_ext(b["url"])} title="{e(b.get("title", b["alt"]))}">'
        f'<img src="{u("assets/buttons/" + b["img"])}" alt="{e(b["alt"])}" width="88" height="31"></a>'
        if b.get("url")
        else f'<span class="btn88 btn88-empty" title="{e(b.get("title", b["alt"]))}">'
        f'<img src="{u("assets/buttons/" + b["img"])}" alt="{e(b["alt"])}" width="88" height="31"></span>'
        for b in site["buttons"]
    )
    year = datetime.now().year
    return f"""</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-col">
        <h2 class="eyebrow">Elsewhere</h2>
        <ul class="foot-links">{links}</ul>
      </div>
      <div class="foot-col">
        <h2 class="eyebrow">Pages</h2>
        <ul class="foot-links plain">{pages}</ul>
      </div>
      <div class="foot-col foot-buttons">
        <h2 class="eyebrow">Buttons</h2>
        <div class="buttons">{buttons}</div>
        <p class="foot-note">Take the top one if you link me. <a href="{u('assets/buttons/milo-tek.png')}">88&times;31 PNG</a>.</p>
      </div>
    </div>
    <p class="foot-base">
      <span>&copy; {year} {e(site['name'])}</span>
      <span><a href="{u('colophon/')}">Colophon</a> &middot; <a href="{u('feed.xml')}">RSS</a> &middot; <a href="{e(site['repo'])}" target="_blank" rel="noopener">Source</a></span>
    </p>
  </div>
</footer>
<script src="{u('assets/js/site.js')}" defer></script>
</body>
</html>
"""


def chips(items) -> str:
    if not items:
        return ""
    return '<ul class="chips">' + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def project_card(site: dict, here: str, p: dict, large: bool = False) -> str:
    u = lambda path: url(here, path)
    href = u(f"work/{p['slug']}/") if p.get("page", True) else (p["links"][0]["url"] if p.get("links") else "#")
    ext = "" if p.get("page", True) else _ext(href)
    if p.get("cover"):
        fit = p.get("cover_fit", "cover")
        cover = (
            f'<div class="card-shot fit-{fit}">'
            f'<img src="{u("assets/img/" + p["cover"])}" alt="" loading="lazy" decoding="async">'
            f"</div>"
        )
    else:
        # Nothing public to show. A typed panel beats a broken-looking empty card.
        cover = f'<div class="card-shot card-shot-blank"><span>{e(p["title"])}</span></div>'
    meta = []
    if p.get("year"):
        meta.append(e(p["year"]))
    if p.get("status"):
        meta.append(e(p["status"]))
    return f"""<article class="card{' card-lg' if large else ''}">
  <a class="card-hit" href="{href}"{ext}><span class="sr">{e(p['title'])}</span></a>
  {cover}
  <div class="card-body">
    <p class="card-meta">{' <span aria-hidden="true">/</span> '.join(meta)}</p>
    <h3 class="card-title">{e(p['title'])}</h3>
    <p class="card-sum">{e(p.get('summary', ''))}</p>
    {chips(p.get('stack'))}
  </div>
</article>"""


def section_head(eyebrow: str, title: str, more_href: str = "", more_label: str = "") -> str:
    more = f'<a class="more" href="{more_href}">{e(more_label)} <span aria-hidden="true">&rarr;</span></a>' if more_href else ""
    return f"""<div class="sec-head">
  <div><p class="eyebrow">{e(eyebrow)}</p><h2>{e(title)}</h2></div>
  {more}
</div>"""


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #

def build_home(site, projects, posts, art):
    here = ""
    u = lambda p: url(here, p)
    home = site["home"]
    featured = [p for p in projects if p.get("featured")]
    featured.sort(key=lambda p: p["featured"])
    cards = "".join(project_card(site, here, p, large=True) for p in featured[:4])

    post_items = ""
    for post in posts[:2]:
        post_items += f"""<a class="row" href="{u('blog/' + post['slug'] + '/')}">
  <span class="row-date">{e(post['date'])}</span>
  <span class="row-main"><strong>{e(post['title'])}</strong><span>{e(post.get('summary',''))}</span></span>
  <span class="row-go" aria-hidden="true">&rarr;</span>
</a>"""

    art_strip = "".join(
        f'<a href="{u("art/")}#{e(a["slug"])}"><img src="{u("assets/img/art/" + a["thumb"])}" alt="{e(a["caption"])}" loading="lazy" decoding="async"></a>'
        for a in art[:6]
    )

    links = "".join(
        f'<a class="link-card" href="{e(l["url"])}"{_ext(l["url"])}><span class="lc-label">{e(l["label"])}</span><span class="lc-handle">{e(l.get("handle",""))}</span></a>'
        for l in site["links"]
    )

    return (
        head(site, here, site["title"], site["description"])
        + header(site, here, "")
        + f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <p class="eyebrow">{e(home['eyebrow'])}</p>
      <h1>{e(site['name'])}</h1>
      <p class="lede">{markdown(home['lede'], here).replace('<p>','').replace('</p>','')}</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{u('work/')}">See the work</a>
        <a class="btn" href="{u('cv/')}">CV</a>
        <a class="btn btn-quiet" href="mailto:{e(site['email'])}">{e(site['email'])}</a>
      </div>
    </div>
    <aside class="hero-card">
      <img class="hero-avatar" src="{u('assets/img/site/avatar.webp')}" alt="A cartoon moose I drew" width="120" height="120">
      <p class="hero-status"><span class="dot" aria-hidden="true"></span>{e(home['status'])}</p>
      <dl class="hero-facts">
        {''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in home['facts'].items())}
      </dl>
    </aside>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {section_head('Selected work', 'Things I have built', u('work/'), 'All work')}
    <div class="grid grid-2">{cards}</div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    {section_head('Writing', 'From the blog', u('blog/'), 'All posts')}
    <div class="rows">{post_items}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {section_head('Drawings', 'I draw as well', u('art/'), 'Full gallery')}
    <div class="art-strip">{art_strip}</div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    {section_head('Contact', 'Find me')}
    <div class="link-grid">{links}</div>
  </div>
</section>
"""
        + footer(site, here)
    )


def build_work_index(site, projects):
    here = "work"
    u = lambda p: url(here, p)
    main = [p for p in projects if p.get("kind", "project") != "small"]
    small = [p for p in projects if p.get("kind") == "small"]
    cards = "".join(project_card(site, here, p) for p in main)
    small_rows = "".join(
        f"""<li><a href="{(p['links'][0]['url'] if p.get('links') else '#')}" target="_blank" rel="noopener">
        <strong>{e(p['title'])}</strong><span>{e(p.get('summary',''))}</span></a></li>"""
        for p in small
    )
    small_block = (
        f"""<div class="sec-sub">
      {section_head('Also', 'Smaller things')}
      <ul class="small-list">{small_rows}</ul>
    </div>"""
        if small
        else ""
    )
    return (
        head(site, here, "Work", site["work"]["description"])
        + header(site, here, "work")
        + f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Work</p>
    <h1>{e(site['work']['title'])}</h1>
    <p class="lede">{e(site['work']['lede'])}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="grid grid-3">{cards}</div>
    {small_block}
  </div>
</section>
"""
        + footer(site, here)
    )


def build_project(site, p, projects):
    here = f"work/{p['slug']}"
    u = lambda path: url(here, path)
    link_html = "".join(
        f'<a class="btn btn-small" href="{e(l["url"])}"{_ext(l["url"])}>{e(l["label"])}</a>'
        for l in p.get("links", [])
    )
    links = f'<div class="detail-actions">{link_html}</div>' if link_html else ""
    facts = []
    for key in ("year", "role", "status"):
        if p.get(key):
            facts.append(f'<div><dt>{key.title()}</dt><dd>{e(p[key])}</dd></div>')
    if p.get("stack"):
        facts.append(f'<div><dt>Built with</dt><dd>{e(", ".join(p["stack"]))}</dd></div>')

    gallery = ""
    if p.get("gallery"):
        items = "".join(
            f"""<figure class="shot">
  <a href="{u('assets/img/' + g['src'])}" class="lightbox" data-caption="{e(g.get('caption',''))}">
    <img src="{u('assets/img/' + g['src'])}" alt="{e(g.get('caption',''))}" loading="lazy" decoding="async">
  </a>
  {f'<figcaption>{e(g["caption"])}</figcaption>' if g.get('caption') else ''}
</figure>"""
            for g in p["gallery"]
        )
        cls = "shots shots-tall" if p.get("gallery_layout") == "tall" else "shots"
        gallery = f'<div class="{cls}">{items}</div>'

    idx = [x for x in projects if x.get("page", True)]
    pos = next((i for i, x in enumerate(idx) if x["slug"] == p["slug"]), 0)
    nxt = idx[(pos + 1) % len(idx)] if len(idx) > 1 else None
    nav = (
        f"""<nav class="prevnext"><a href="{u('work/' + nxt['slug'] + '/')}">
      <span class="eyebrow">Next project</span><strong>{e(nxt['title'])}</strong></a></nav>"""
        if nxt
        else ""
    )

    return (
        head(site, here, p["title"], p.get("summary", ""))
        + header(site, here, "work")
        + f"""
<article class="page-head detail">
  <div class="wrap">
    <p class="crumb"><a href="{u('work/')}">&larr; Work</a></p>
    <p class="eyebrow">{e(p.get('label', 'Project'))}</p>
    <h1>{e(p['title'])}</h1>
    <p class="lede">{e(p.get('summary',''))}</p>
    {links}
  </div>
</article>
<div class="wrap detail-body">
  <div class="prose">{markdown(p['body'], here)}</div>
  <aside class="facts"><dl>{''.join(facts)}</dl></aside>
</div>
<div class="wrap">{gallery}{nav}</div>
"""
        + footer(site, here)
    )


def build_blog_index(site, posts):
    here = "blog"
    u = lambda p: url(here, p)
    rows = "".join(
        f"""<a class="row" href="{u('blog/' + post['slug'] + '/')}">
  <span class="row-date">{e(post['date'])}</span>
  <span class="row-main"><strong>{e(post['title'])}</strong><span>{e(post.get('summary',''))}</span></span>
  <span class="row-go" aria-hidden="true">&rarr;</span>
</a>"""
        for post in posts
    )
    return (
        head(site, here, "Blog", site["blog"]["description"])
        + header(site, here, "blog")
        + f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Blog</p>
    <h1>{e(site['blog']['title'])}</h1>
    <p class="lede">{e(site['blog']['lede'])} There is an <a href="{u('feed.xml')}">RSS feed</a> if you want it.</p>
  </div>
</section>
<section class="sec"><div class="wrap"><div class="rows">{rows}</div></div></section>
"""
        + footer(site, here)
    )


def build_post(site, post):
    here = f"blog/{post['slug']}"
    u = lambda p: url(here, p)
    return (
        head(site, here, post["title"], post.get("summary", ""))
        + header(site, here, "blog")
        + f"""
<article class="page-head detail">
  <div class="wrap narrow">
    <p class="crumb"><a href="{u('blog/')}">&larr; Blog</a></p>
    <p class="eyebrow"><time datetime="{e(post['date'])}">{e(post['date'])}</time></p>
    <h1>{e(post['title'])}</h1>
  </div>
</article>
<div class="wrap narrow"><div class="prose">{markdown(post['body'], here)}</div></div>
"""
        + footer(site, here)
    )


def build_art(site, art):
    here = "art"
    u = lambda p: url(here, p)
    items = "".join(
        f"""<figure class="art-item" id="{e(a['slug'])}">
  <a class="lightbox" href="{u('assets/img/art/' + a['full'])}" data-caption="{e(a['caption'])}">
    <img src="{u('assets/img/art/' + a['thumb'])}" alt="{e(a['caption'])}" loading="lazy" decoding="async">
  </a>
  <figcaption>{e(a['caption'])}{f'<span>{e(a["tool"])}</span>' if a.get('tool') else ''}</figcaption>
</figure>"""
        for a in art
    )
    return (
        head(site, here, "Art", site["art"]["description"])
        + header(site, here, "art")
        + f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Art</p>
    <h1>{e(site['art']['title'])}</h1>
    <p class="lede">{e(site['art']['lede'])}</p>
  </div>
</section>
<section class="sec"><div class="wrap"><div class="art-grid">{items}</div></div></section>
"""
        + footer(site, here)
    )


def build_page(site, page):
    here = page["path"].strip("/")
    u = lambda p: url(here, p)
    updated = (
        f'<p class="updated">Last updated {e(page["updated"])}</p>' if page.get("updated") else ""
    )
    extra = ""
    if page.get("layout") == "cv":
        extra = f"""
<div class="wrap cv-sheet">
  <img src="{u('assets/img/site/cv-1.webp')}" alt="Page 1 of my CV" loading="lazy" decoding="async">
  <img src="{u('assets/img/site/cv-2.webp')}" alt="Page 2 of my CV" loading="lazy" decoding="async">
</div>"""
    return (
        head(site, here, page["title"], page.get("summary", ""))
        + header(site, here, here)
        + f"""
<section class="page-head">
  <div class="wrap narrow">
    <p class="eyebrow">{e(page.get('eyebrow', page['title']))}</p>
    <h1>{e(page['title'])}</h1>
    {f'<p class="lede">{e(page["lede"])}</p>' if page.get('lede') else ''}
    {updated}
  </div>
</section>
<div class="wrap narrow"><div class="prose">{markdown(page['body'], here)}</div></div>
{extra}
"""
        + footer(site, here)
    )


def build_404(site):
    here = ""
    u = lambda p: url(here, p)
    return (
        head(site, here, "Not found", "That page does not exist.")
        + header(site, here, "")
        + f"""
<section class="page-head notfound">
  <div class="wrap narrow">
    <p class="eyebrow">404</p>
    <h1>Nothing here</h1>
    <p class="lede">Wrong link, or I moved something. Both are plausible.</p>
    <p><a class="btn btn-primary" href="{u('')}">Back to the front page</a></p>
  </div>
</section>
"""
        + footer(site, here)
    )


def build_feed(site, posts):
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for post in posts:
        link = absolute(site, f"blog/{post['slug']}/")
        pub = datetime.strptime(str(post["date"]), "%Y-%m-%d").replace(tzinfo=timezone.utc)
        body = markdown(post["body"], f"blog/{post['slug']}")
        body = re.sub(r'(src|href)="((?!https?:|mailto:)[^"]+)"',
                      lambda m: f'{m.group(1)}="{absolute(site, m.group(2).replace("../", ""))}"', body)
        items.append(f"""  <item>
    <title>{e(post['title'])}</title>
    <link>{e(link)}</link>
    <guid isPermaLink="true">{e(link)}</guid>
    <pubDate>{pub.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <description>{e(post.get('summary',''))}</description>
    <content:encoded><![CDATA[{body}]]></content:encoded>
  </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
  <title>{e(site['title'])}</title>
  <link>{e(site['url'])}</link>
  <atom:link href="{e(absolute(site, 'feed.xml'))}" rel="self" type="application/rss+xml"/>
  <description>{e(site['description'])}</description>
  <language>en-GB</language>
  <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
"""


def build_sitemap(site, paths):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = "".join(
        f"  <url><loc>{e(absolute(site, p))}</loc><lastmod>{today}</lastmod></url>\n" for p in paths
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>
"""


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    site = parse_yaml((CONTENT / "site.yaml").read_text(encoding="utf-8"))

    projects = [read_doc(p) for p in sorted((CONTENT / "projects").glob("*.md"))]
    projects.sort(key=lambda p: (p.get("weight", 500), p["title"]))

    posts = [read_doc(p) for p in sorted((CONTENT / "posts").glob("*.md"))]
    posts = [p for p in posts if not p.get("draft")]
    posts.sort(key=lambda p: str(p["date"]), reverse=True)

    art = [read_doc(p) for p in sorted((CONTENT / "art").glob("*.md"))]
    art.sort(key=lambda a: (a.get("order", 500), a["slug"]))
    for a in art:
        a.setdefault("full", a["slug"] + ".webp")
        a.setdefault("thumb", a["slug"] + "_t.webp")

    pages = [read_doc(p) for p in sorted((CONTENT / "pages").glob("*.md"))]

    for d in OUTPUT_DIRS:
        shutil.rmtree(ROOT / d, ignore_errors=True)
    for f in OUTPUT_FILES:
        (ROOT / f).unlink(missing_ok=True)

    written = []

    def emit(rel_path: str, text: str):
        write(ROOT / rel_path, text)
        written.append(rel_path)

    emit("index.html", build_home(site, projects, posts, art))
    emit("work/index.html", build_work_index(site, projects))
    for p in projects:
        if p.get("page", True):
            emit(f"work/{p['slug']}/index.html", build_project(site, p, projects))
    emit("blog/index.html", build_blog_index(site, posts))
    for post in posts:
        emit(f"blog/{post['slug']}/index.html", build_post(site, post))
    emit("art/index.html", build_art(site, art))
    for page in pages:
        emit(f"{page['path'].strip('/')}/index.html", build_page(site, page))
    emit("404.html", build_404(site))
    emit("feed.xml", build_feed(site, posts))

    routes = ["" if p == "index.html" else p[: -len("index.html")] for p in written if p.endswith("index.html")]
    emit("sitemap.xml", build_sitemap(site, routes))
    emit("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {absolute(site, 'sitemap.xml')}\n")
    (ROOT / ".nojekyll").touch()

    print(f"built {len(written)} files: {len(projects)} projects, {len(posts)} posts, {len(art)} drawings")


if __name__ == "__main__":
    sys.exit(main())
