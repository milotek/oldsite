#!/usr/bin/env python3
"""Builds the site from content/ into the repo root.

Standard library only. Run `python3 build.py` and commit whatever changes.
Nothing in here needs editing to add a project, a post, a drawing or a button:
that is all files under content/.
"""

import html
import json
import re
import shutil
import tomllib
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
SRC = ROOT / "src"

# Directories this script owns. They get wiped on every build, so nothing
# hand-written may live in them.
GENERATED = ["projects", "blog", "art", "now", "uses", "colophon", "buttons"]


# --------------------------------------------------------------------------
# Markdown. A deliberately small subset: what the content actually uses.
# --------------------------------------------------------------------------

INLINE = [
    (re.compile(r"`([^`]+)`"), lambda m: "<code>%s</code>" % html.escape(m.group(1))),
    (re.compile(r"!\[([^\]]*)\]\(([^)]+)\)"),
     lambda m: '<img src="%s" alt="%s" loading="lazy">' % (m.group(2), html.escape(m.group(1)))),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1))),
    (re.compile(r"\*\*([^*]+)\*\*"), lambda m: "<strong>%s</strong>" % m.group(1)),
    (re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])"), lambda m: "<em>%s</em>" % m.group(1)),
]


def inline(text):
    out = html.escape(text, quote=False)
    # Code first so nothing rewrites the inside of a span of code.
    for pattern, repl in INLINE:
        out = pattern.sub(repl, out)
    return out


def markdown(text):
    lines = text.split("\n")
    out, i = [], 0
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
                buf.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(buf)))
            continue

        if stripped.startswith("<"):
            buf = []
            while i < len(lines) and lines[i].strip():
                buf.append(lines[i])
                i += 1
            out.append("\n".join(buf))
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            out.append("<h%d>%s</h%d>" % (level, inline(stripped[level:].strip()), level))
            i += 1
            continue

        if stripped in ("---", "***"):
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                buf.append(lines[i].strip()[2:])
                i += 1
            out.append("<blockquote>%s</blockquote>" % markdown("\n".join(buf)))
            continue

        bullet = re.match(r"^([-*]|\d+\.)\s+", stripped)
        if bullet:
            ordered = bullet.group(1)[0].isdigit()
            items = []
            while i < len(lines) and re.match(r"^([-*]|\d+\.)\s+", lines[i].strip()):
                items.append(re.sub(r"^([-*]|\d+\.)\s+", "", lines[i].strip()))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
            continue

        buf = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(("#", ">", "```", "<")):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(buf)))

    return "\n".join(out)


def plain(text, limit=240):
    """First paragraph, stripped of markup, for previews and feed summaries."""
    para = ""
    for block in text.strip().split("\n\n"):
        block = block.strip()
        if block and not block.startswith(("#", "<", "```", "-", ">")):
            para = block
            break
    para = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", para)
    para = re.sub(r"[`*]", "", para).replace("\n", " ")
    if len(para) > limit:
        para = para[:limit].rsplit(" ", 1)[0] + "..."
    return para


def read_entry(path):
    """A content file: TOML between +++ fences, Markdown after."""
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("+++"):
        _, front, body = raw.split("+++", 2)
        meta = tomllib.loads(front)
    meta.setdefault("slug", path.stem)
    meta["body"] = body.strip()
    return meta


# --------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------

E = html.escape


class Page:
    """Knows how deep it sits, so every URL it writes can stay relative."""

    def __init__(self, depth, absolute=False):
        self.depth = depth
        self.absolute = absolute

    def u(self, path=""):
        # 404.html is served for any missing path, so it cannot use relative
        # URLs. It gets the deploy path instead, which survives the domain
        # changing but not the subdirectory.
        if self.absolute:
            return BASE_PATH + path
        return ("../" * self.depth) + path if self.depth else (path or "./")


def head(page, title, description, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<meta name="theme-color" content="#11111b">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE['base_url']}assets/{SITE['avatar']}">
<link rel="icon" href="{page.u('favicon.png')}">
<link rel="apple-touch-icon" href="{page.u('assets/img/site/icon-180.png')}">
<link rel="alternate" type="application/rss+xml" title="milo tek" href="{page.u('feed.xml')}">
<link rel="stylesheet" href="{page.u('style.css')}">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def hud(page, active=""):
    items = []
    for item in SITE["nav"]:
        href = item["href"]
        target = page.u("") + href if href.startswith("#") else page.u(href)
        cls = ' class="on"' if item["label"] == active else ""
        items.append(f'<a{cls} href="{target}">{E(item["label"])}</a>')
    return f"""<header class="hud">
<a class="mark" href="{page.u('')}"><span class="sq" aria-hidden="true"></span>milo tek</a>
<nav class="nav">{''.join(items)}</nav>
</header>
"""


def footer(page):
    links = "".join(
        f'<li><a href="{E(l["url"])}" rel="me">{E(l["label"])}</a></li>' for l in SITE["links"]
    )
    pages = "".join(
        f'<li><a href="{page.u(i["href"])}">{E(i["label"])}</a></li>'
        for i in SITE["nav"] if not i["href"].startswith("#")
    )
    strip = "".join(
        f'<img src="{page.u("assets/" + b["img"])}" width="88" height="31" alt="{E(b["alt"])}">'
        for b in BUTTONS["mine"][:3]
    )
    year = datetime.now().year
    return f"""<footer class="foot">
<div class="foot-grid">
<div>
<p class="tag">elsewhere</p>
<ul class="plain">{links}</ul>
</div>
<div>
<p class="tag">pages</p>
<ul class="plain">{pages}<li><a href="{page.u('buttons/')}">buttons</a></li><li><a href="{page.u('feed.xml')}">rss</a></li></ul>
</div>
<div class="foot-end">
<img class="mascot" src="{page.u('assets/' + SITE['mascot'])}" width="72" height="72" alt="{E(SITE['mascot_alt'])}">
<a class="foot-buttons" href="{page.u('buttons/')}" title="button wall">{strip}</a>
<p class="fine">{E(SITE['full_name'])} &middot; London &middot; {year}</p>
</div>
</div>
</footer>
</body>
</html>
"""


def shell(page, title, description, body, active="", extra=""):
    return head(page, title, description, extra) + hud(page, active) + body + footer(page)


def chips(items):
    return "".join(f"<li>{E(x)}</li>" for x in items)


def shot(page, project, cls="rw-shot"):
    """A project's thumbnail, or a typed slate when there is nothing to show."""
    if project.get("thumb"):
        return (f'<span class="{cls}"><img src="{page.u("assets/" + project["thumb"])}" '
                f'width="800" height="450" loading="lazy" alt=""></span>')
    return f'<span class="{cls} slate"><span>{E(project.get("slate", project["title"]))}</span></span>'


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

def build_index(projects, posts):
    page = Page(0)
    groups = []
    index = 0
    data = []
    for group in SITE["groups"]:
        members = [p for p in projects if p.get("group") == group["id"]]
        if not members:
            continue
        rows = []
        for p in members:
            href = page.u(f"projects/{p['slug']}/")
            data.append({
                "title": p["title"],
                "group": group["label"],
                "year": p.get("year", ""),
                "tagline": p.get("tagline", ""),
                "stack": p.get("stack", []),
                "blurb": plain(p["body"]),
                "href": href,
                "thumb": page.u("assets/" + p["thumb"]) if p.get("thumb") else "",
                "slate": p.get("slate", ""),
                "links": [{"label": l["label"], "url": l["url"]} for l in p.get("links", [])],
            })
            rows.append(f"""<a class="rw" href="{href}" data-i="{index}">
<span class="rw-n">{index + 1:02d}</span>
{shot(page, p)}
<span class="rw-body">
<span class="rw-title">{E(p['title'])}</span>
<span class="rw-tag">{E(p.get('tagline', ''))}</span>
<span class="rw-stack">{''.join(f'<i>{E(s)}</i>' for s in p.get('stack', [])[:4])}</span>
</span>
<span class="rw-year">{E(p.get('year', ''))}</span>
</a>""")
            index += 1
        groups.append(f"""<section class="rgroup">
<h2 class="rgroup-h"><span>{E(group['label'])}</span><span class="rgroup-note">{E(group.get('note', ''))}</span></h2>
{''.join(rows)}
</section>""")

    first = data[0]
    pane_shot = (f'<img id="pshot" src="{first["thumb"]}" width="800" height="450" alt="">'
                 if first["thumb"] else f'<span id="pshot-slate">{E(first["slate"])}</span>')

    intro = "".join(f"<p>{E(line)}</p>" for line in SITE["intro"])
    actions = "".join(
        f'<a class="btn{" btn-primary" if a.get("primary") else ""}" href="{E(a["url"])}">{E(a["label"])}</a>'
        for a in SITE["actions"]
    )
    facts = "".join(
        f'<div><dt>{E(f["k"])}</dt><dd>{E(f["v"])}</dd></div>' for f in SITE["facts"]
    )

    latest = posts[0]
    writing = f"""<section class="writing">
<div class="sec-head"><span class="tag">writing</span><span class="rule"></span><a class="more" href="{page.u('blog/')}">all posts</a></div>
<a class="postcard" href="{page.u('blog/' + latest['slug'] + '/')}">
<span class="postcard-date">{E(latest['date'])}</span>
<span class="postcard-title">{E(latest['title'])}</span>
<span class="postcard-sum">{E(latest.get('summary', plain(latest['body'])))}</span>
<span class="postcard-go">read it</span>
</a>
</section>"""

    body = f"""<main id="main">
<section class="hero">
<div class="hero-main">
<p class="eyebrow">United Kingdom &middot; 19 &middot; software engineer</p>
<h1 class="name">milo tek</h1>
<div class="lead">{intro}</div>
<div class="actions">{actions}</div>
</div>
<aside class="idcard">
<div class="idcard-frame">
<img src="{page.u('assets/' + SITE['avatar'])}" width="480" height="480" alt="{E(SITE['avatar_alt'])}">
<span class="tick tl"></span><span class="tick tr"></span><span class="tick bl"></span><span class="tick br"></span>
</div>
<p class="idcard-name">{E(SITE['full_name'])}</p>
<dl class="stats">{facts}</dl>
</aside>
</section>

<section class="select" id="select">
<div class="sec-head"><span class="tag">select</span><span class="rule"></span><span class="count">{len(data)} entries</span><span class="hint">&uarr;&darr; to browse</span></div>
<div class="select-grid">
<div class="roster" id="roster">{''.join(groups)}</div>
<aside class="pane" id="pane">
<div class="pane-shot" id="pane-shot">{pane_shot}</div>
<p class="pane-kicker"><span id="pgroup">{E(first['group'])}</span><span id="pyear">{E(first['year'])}</span></p>
<h3 class="pane-title" id="ptitle">{E(first['title'])}</h3>
<p class="pane-tag" id="ptag">{E(first['tagline'])}</p>
<ul class="chips" id="pstack">{chips(first['stack'])}</ul>
<p class="pane-body" id="pbody">{E(first['blurb'])}</p>
<div class="pane-foot"><a class="btn btn-primary" id="popen" href="{first['href']}">open</a><span class="pane-links" id="plinks"></span></div>
</aside>
</div>
</section>

{writing}
</main>
<script id="roster-data" type="application/json">{json.dumps(data)}</script>
<script src="{page.u('select.js')}" defer></script>
"""
    write("index.html", shell(page, f"{SITE['title']} - {SITE['tagline']}", SITE["description"], body, active="work"))


def build_projects(projects):
    for p in projects:
        page = Page(2)
        group = next((g["label"] for g in SITE["groups"] if g["id"] == p.get("group")), "")
        meta = [("year", p.get("year")), ("role", p.get("role")), ("group", group)]
        rows = "".join(f"<div><dt>{k}</dt><dd>{E(v)}</dd></div>" for k, v in meta if v)
        if p.get("stack"):
            rows += f'<div class="wide"><dt>stack</dt><dd><ul class="chips">{chips(p["stack"])}</ul></dd></div>'
        links = "".join(
            f'<a class="btn" href="{E(l["url"])}">{E(l["label"])}</a>' for l in p.get("links", [])
        )
        shots = "".join(
            f'<figure class="shot"><a href="{page.u("assets/" + i["src"])}">'
            f'<img src="{page.u("assets/" + i["src"])}" alt="{E(i.get("alt", ""))}" loading="lazy"></a></figure>'
            for i in p.get("images", [])
        )
        gallery = f'<div class="shots">{shots}</div>' if shots else ""
        body = f"""<main id="main" class="wrap">
<p class="crumb"><a href="{page.u('')}#select">&larr; everything else</a></p>
<header class="phead">
<p class="eyebrow">{E(group)}</p>
<h1>{E(p['title'])}</h1>
<p class="phead-tag">{E(p.get('tagline', ''))}</p>
<dl class="meta">{rows}</dl>
{f'<div class="actions">{links}</div>' if links else ''}
</header>
{gallery}
<div class="prose">{markdown(p['body'])}</div>
</main>"""
        write(f"projects/{p['slug']}/index.html",
              shell(page, f"{p['title']} - {SITE['title']}", p.get("tagline", SITE["description"]), body, active="work"))


def build_blog(posts):
    page = Page(1)
    items = "".join(f"""<a class="postrow" href="{page.u('blog/' + p['slug'] + '/')}">
<span class="postrow-date">{E(p['date'])}</span>
<span class="postrow-body"><span class="postrow-title">{E(p['title'])}</span>
<span class="postrow-sum">{E(p.get('summary', plain(p['body'])))}</span></span>
</a>""" for p in posts)
    body = f"""<main id="main" class="wrap">
<header class="phead">
<p class="eyebrow">blog</p>
<h1>Posts</h1>
<p class="phead-tag">Rarely. Only when there's something to say. There's an <a href="{page.u('feed.xml')}">RSS feed</a>.</p>
</header>
<div class="postlist">{items}</div>
</main>"""
    write("blog/index.html", shell(page, f"Blog - {SITE['title']}", "Posts by milo tek.", body, active="blog"))

    for p in posts:
        sub = Page(2)
        body = f"""<main id="main" class="wrap">
<p class="crumb"><a href="{sub.u('blog/')}">&larr; all posts</a></p>
<header class="phead">
<p class="eyebrow">{E(p['date'])}</p>
<h1>{E(p['title'])}</h1>
</header>
<article class="prose">{markdown(p['body'])}</article>
</main>"""
        write(f"blog/{p['slug']}/index.html",
              shell(sub, f"{p['title']} - {SITE['title']}", p.get("summary", ""), body, active="blog"))


def build_art():
    page = Page(1)
    tiles = "".join(f"""<figure class="art">
<a href="{page.u('assets/img/art/' + a['file'] + '.webp')}">
<img src="{page.u('assets/img/art/' + a['file'] + '-t.webp')}" alt="{E(a['caption'])}" loading="lazy">
</a>
<figcaption>{E(a['caption'])}</figcaption>
</figure>""" for a in ART["art"])
    body = f"""<main id="main" class="wrap">
<header class="phead">
<p class="eyebrow">art</p>
<h1>Drawings</h1>
<p class="phead-tag">{E(ART['lead'])}</p>
</header>
<div class="artgrid">{tiles}</div>
</main>"""
    write("art/index.html", shell(page, f"Art - {SITE['title']}", ART["lead"], body, active="art"))


def build_buttons():
    page = Page(1)

    def wall(rows):
        out = []
        for b in rows:
            if b.get("empty"):
                out.append('<span class="b88 empty" aria-hidden="true">yours?</span>')
                continue
            img = (f'<img src="{page.u("assets/" + b["img"])}" width="88" height="31" '
                   f'alt="{E(b["alt"])}" title="{E(b.get("title", b["alt"]))}">')
            out.append(f'<a class="b88" href="{E(b["url"])}">{img}</a>' if b.get("url") else f'<span class="b88">{img}</span>')
        return "".join(out)

    body = f"""<main id="main" class="wrap">
<header class="phead">
<p class="eyebrow">88 x 31</p>
<h1>Buttons</h1>
<p class="phead-tag">{E(BUTTONS['lead'])}</p>
</header>
<h2 class="tag">mine</h2>
<div class="wall">{wall(BUTTONS['mine'])}</div>
<h2 class="tag">things I like</h2>
<p class="note">I drew these myself. None of them are official.</p>
<div class="wall">{wall(BUTTONS['theirs'])}</div>
<h2 class="tag">taking one</h2>
<div class="prose">
<p>Hotlinking is fine, I'm not going to notice. If you'd rather not, save it.</p>
<pre><code>&lt;a href="https://furfag.lol/"&gt;
  &lt;img src="https://furfag.lol/assets/img/buttons/milotek.png"
       width="88" height="31" alt="milo tek"&gt;
&lt;/a&gt;</code></pre>
<p>Got one of your own? <a href="mailto:milo@milotek.dev">Send it over</a> and it goes on the wall.</p>
</div>
</main>"""
    write("buttons/index.html", shell(page, f"Buttons - {SITE['title']}", BUTTONS["lead"], body))


def build_pages(pages):
    for p in pages:
        page = Page(1)
        updated = f'<p class="stamp">Last updated {E(p["updated"])}</p>' if p.get("updated") else ""
        body = f"""<main id="main" class="wrap">
<header class="phead">
<p class="eyebrow">{E(p['title'])}</p>
<h1>{E(p.get('heading', p['title']))}</h1>
{f'<p class="phead-tag">{E(p["lead"])}</p>' if p.get('lead') else ''}
</header>
<div class="prose">{markdown(p['body'])}</div>
{updated}
</main>"""
        write(f"{p['slug']}/index.html",
              shell(page, f"{p['title']} - {SITE['title']}", p.get("lead", SITE["description"]), body, active=p["slug"]))


def build_404():
    page = Page(0, absolute=True)
    body = f"""<main id="main" class="wrap notfound">
<img src="{page.u('assets/img/site/under-construction.gif')}" width="360" alt="A stick figure next to some cogs, captioned under construction">
<h1>404</h1>
<p class="phead-tag">Nothing here. The drawing is from 2024 and it still applies.</p>
<p class="actions"><a class="btn btn-primary" href="{page.u('')}">back to the front</a></p>
</main>"""
    write("404.html", shell(page, f"404 - {SITE['title']}", "Page not found.", body))


def build_feed(posts):
    base = SITE["base_url"]
    items = []
    for p in posts:
        stamp = datetime.strptime(p["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        link = f"{base}blog/{p['slug']}/"
        items.append(f"""<item>
<title>{E(p['title'])}</title>
<link>{link}</link>
<guid isPermaLink="true">{link}</guid>
<pubDate>{format_datetime(stamp)}</pubDate>
<description>{E(p.get('summary', plain(p['body'])))}</description>
</item>""")
    feed = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>{E(SITE['title'])}</title>
<link>{base}</link>
<atom:link href="{base}feed.xml" rel="self" type="application/rss+xml"/>
<description>{E(SITE['description'])}</description>
<language>en-gb</language>
<lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>
{''.join(items)}
</channel>
</rss>
"""
    write("feed.xml", feed)


# --------------------------------------------------------------------------

def write(path, text):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def main():
    global SITE, ART, BUTTONS, BASE_PATH
    SITE = tomllib.loads((CONTENT / "site.toml").read_text(encoding="utf-8"))
    ART = tomllib.loads((CONTENT / "art.toml").read_text(encoding="utf-8"))
    BUTTONS = tomllib.loads((CONTENT / "buttons.toml").read_text(encoding="utf-8"))
    BASE_PATH = "/" + SITE["base_url"].split("//", 1)[1].split("/", 1)[1]

    projects = sorted((read_entry(f) for f in (CONTENT / "projects").glob("*.md")),
                      key=lambda p: p.get("order", 999))
    posts = sorted((read_entry(f) for f in (CONTENT / "posts").glob("*.md")),
                   key=lambda p: p["date"], reverse=True)
    pages = [read_entry(f) for f in (CONTENT / "pages").glob("*.md")]

    for name in GENERATED:
        shutil.rmtree(ROOT / name, ignore_errors=True)

    build_index(projects, posts)
    build_projects(projects)
    build_blog(posts)
    build_art()
    build_buttons()
    build_pages(pages)
    build_404()
    build_feed(posts)

    shutil.copy(SRC / "style.css", ROOT / "style.css")
    shutil.copy(SRC / "select.js", ROOT / "select.js")
    (ROOT / ".nojekyll").touch()

    print(f"built {len(projects)} projects, {len(posts)} posts, {len(pages)} pages, {len(ART['art'])} drawings")


if __name__ == "__main__":
    main()
