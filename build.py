#!/usr/bin/env python3
"""Generates the site into the repo root. No dependencies, no build cache.

Layout lives here. Content lives in content/ and nothing in this file should
need editing to add a project, a drawing, a link or a post.
"""

import html
import os
import re
import shutil
import tomllib
from datetime import datetime, timezone
from email.utils import format_datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
POSTS = os.path.join(CONTENT, "posts")


# ---------------------------------------------------------------- markdown

FENCE = re.compile(r"^```(\w*)\s*$")


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r'<img src="\2" alt="\1" loading="lazy">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def markdown(text):
    """A deliberately small subset: enough for posts and blurbs, nothing more."""
    out, lines, i = [], text.split("\n"), 0
    para, listbuf, listtag = [], [], None

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    def flush_list():
        nonlocal listtag
        if listbuf:
            out.append(f"<{listtag}>" + "".join(f"<li>{inline(x)}</li>" for x in listbuf) + f"</{listtag}>")
            listbuf.clear()
            listtag = None

    while i < len(lines):
        line = lines[i]
        m = FENCE.match(line)
        if m:
            flush_para(); flush_list()
            i += 1
            code = []
            while i < len(lines) and not FENCE.match(lines[i]):
                code.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
            continue
        if not line.strip():
            flush_para(); flush_list()
            i += 1
            continue
        if line.startswith("#"):
            flush_para(); flush_list()
            level = len(line) - len(line.lstrip("#"))
            out.append(f"<h{level + 1}>{inline(line[level:].strip())}</h{level + 1}>")
            i += 1
            continue
        if line.strip() in ("---", "***"):
            flush_para(); flush_list()
            out.append("<hr>")
            i += 1
            continue
        if line.startswith("> "):
            flush_para(); flush_list()
            out.append(f"<blockquote><p>{inline(line[2:])}</p></blockquote>")
            i += 1
            continue
        m = re.match(r"^\s*([-*])\s+(.*)$", line)
        if m:
            flush_para()
            if listtag not in (None, "ul"):
                flush_list()
            listtag = "ul"
            listbuf.append(m.group(2))
            i += 1
            continue
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            flush_para()
            if listtag not in (None, "ol"):
                flush_list()
            listtag = "ol"
            listbuf.append(m.group(1))
            i += 1
            continue
        flush_list()
        para.append(line.strip())
        i += 1

    flush_para(); flush_list()
    return "\n".join(out)


# ---------------------------------------------------------------- content

def load(name):
    with open(os.path.join(CONTENT, name), "rb") as f:
        return tomllib.load(f)


def load_posts():
    posts = []
    for name in sorted(os.listdir(POSTS)):
        if not name.endswith(".md"):
            continue
        raw = open(os.path.join(POSTS, name), encoding="utf-8").read()
        meta, body = {}, raw
        if raw.startswith("---"):
            _, front, body = raw.split("---", 2)
            for line in front.strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
        meta["slug"] = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name[:-3])
        meta["body"] = body.strip()
        posts.append(meta)
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    return posts


# ---------------------------------------------------------------- pieces

def rel(depth, path):
    return ("../" * depth) + path


E = html.escape


def roundel(depth, size=30):
    return (
        f'<svg class="roundel" width="{size}" height="{size}" viewBox="0 0 120 120" '
        f'aria-hidden="true"><circle cx="60" cy="60" r="42" fill="none" stroke="currentColor" '
        f'stroke-width="17"/><rect x="2" y="50" width="116" height="20" fill="currentColor"/></svg>'
    )


def head(depth, title, description, site, extra_class=""):
    b = lambda p: rel(depth, p)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<meta name="theme-color" content="#1e1e2e">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:type" content="website">
<link rel="icon" href="{b('assets/favicon.svg')}" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{E(site['profile']['handle'])}" href="{b('feed.xml')}">
<link rel="stylesheet" href="{b('assets/css/site.css')}">
</head>
<body class="{extra_class}">
<a class="skip" href="#main">skip to content</a>
"""


def site_header(depth, site):
    b = lambda p: rel(depth, p)
    p = site["profile"]
    quick = "".join(
        f'<a href="{E(l["href"])}">{E(l["label"])}</a>'
        for l in site["link"] if l.get("quick")
    )
    return f"""<header class="bar">
  <a class="mark" href="{b('index.html')}">
    {roundel(depth)}
    <span class="mark-name">{E(p['handle'])}</span>
  </a>
  <nav class="bar-links" aria-label="quick links">{quick}</nav>
</header>
"""


def site_footer(depth, site):
    b = lambda p: rel(depth, p)
    p = site["profile"]
    year = datetime.now().year
    links = " ".join(
        f'<a href="{E(l["href"])}">{E(l["label"])}</a>' for l in site["link"]
    )
    return f"""<footer class="foot">
  <div class="foot-links">{links}</div>
  <p class="foot-note">{E(p['handle'])}, {year}. <a href="{b('index.html#colophon')}">colophon</a> &middot; <a href="{b('feed.xml')}">rss</a></p>
</footer>
</body>
</html>
"""


def chips(items, cls="chip"):
    return "".join(f'<span class="{cls}">{E(x)}</span>' for x in items)


def linkrow(links):
    if not links:
        return ""
    out = []
    for l in links:
        ext = ' rel="noopener"' if l["href"].startswith("http") else ""
        out.append(f'<a class="go" href="{E(l["href"])}"{ext}>{E(l["label"])}</a>')
    return '<p class="entry-links">' + "".join(out) + "</p>"


def shots(project):
    imgs = project.get("shot", [])
    if not imgs:
        return ""
    cells = []
    for s in imgs:
        cap = s.get("caption", "")
        tall = " tall" if s.get("tall") else ""
        cells.append(
            f'<a class="shot{tall}" href="{E(s["src"])}" title="{E(cap)}">'
            f'<img src="{E(s["src"])}" alt="{E(cap or project["title"])}" loading="lazy" decoding="async">'
            f'<span>{E(cap)}</span></a>'
        )
    return '<div class="strip">' + "".join(cells) + "</div>"


def entry(project):
    title = E(project["title"])
    links = project.get("link", [])
    primary = next((l for l in links if l.get("primary")), None)
    heading = f'<a href="{E(primary["href"])}" rel="noopener">{title}</a>' if primary else title
    meta = []
    if project.get("period"):
        meta.append(f'<span class="when">{E(project["period"])}</span>')
    if project.get("status"):
        meta.append(f'<span class="status">{E(project["status"])}</span>')
    if project.get("private"):
        meta.append('<span class="status status--shut">private repo</span>')
    bullets = ""
    if project.get("details"):
        bullets = "<ul class=\"details\">" + "".join(
            f"<li>{inline(d)}</li>" for d in project["details"]
        ) + "</ul>"
    tech = f'<p class="tech">{chips(project.get("tech", []))}</p>' if project.get("tech") else ""
    return f"""  <li class="entry" id="{E(project['id'])}">
    <h3>{heading}</h3>
    <p class="meta">{''.join(meta)}</p>
    <p class="summary">{inline(project['summary'])}</p>
    {bullets}
    {tech}
    {shots(project)}
    {linkrow(links)}
  </li>
"""


def section(sid, name, note, inner, kicker=None):
    k = f'<p class="kicker">{E(kicker)}</p>' if kicker else ""
    n = f'<p class="note">{inline(note)}</p>' if note else ""
    return f"""<section class="sect" id="{sid}">
  <header class="sect-head">
    {k}
    <h2><span class="bullet"></span>{E(name)}</h2>
    {n}
  </header>
  {inner}
</section>
"""


def stops(projects):
    return '<ol class="stops">\n' + "".join(entry(p) for p in projects) + "</ol>\n"


# ---------------------------------------------------------------- pages

def diagram(sections):
    items = []
    last = len(sections) - 1
    for i, (sid, label) in enumerate(sections):
        cls = "stop"
        if i in (0, last):
            cls += " stop--end"
        items.append(
            f'<li class="{cls}"><a href="#{sid}"><span class="dot"></span>'
            f'<span class="label">{E(label)}</span></a></li>'
        )
    return (
        '<nav class="diagram" aria-label="sections of this page">\n'
        '  <ol>' + "".join(items) + "</ol>\n</nav>\n"
    )


def build_index(site, projects, art, posts):
    p = site["profile"]
    lines = [("work", "work"), ("projects", "projects"), ("games", "games"),
             ("art", "art"), ("writing", "writing"), ("now", "now"), ("uses", "uses")]

    avatar = ""
    if p.get("avatar"):
        avatar = (f'<img class="avatar" src="{E(p["avatar"])}" alt="{E(p.get("avatar_alt", ""))}" '
                  f'width="120" height="120">')

    primary = "".join(
        f'<a class="big-link" href="{E(l["href"])}" rel="noopener">{E(l["label"])}'
        f'<span>{E(l.get("note", ""))}</span></a>'
        for l in site["link"] if l.get("hero")
    )

    hero = f"""<section class="hero">
  <div class="hero-text">
    <p class="kicker">{E(p['role'])} &middot; {E(p['location'])}</p>
    <h1>{E(p['name'])}</h1>
    {markdown(p['intro'])}
    <div class="big-links">{primary}</div>
  </div>
  {avatar}
</section>
"""

    by_line = {}
    for pr in projects:
        by_line.setdefault(pr["line"], []).append(pr)

    body = [hero, diagram(lines)]

    body.append(section("work", "work", site["copy"]["work_note"], stops(by_line.get("work", []))))
    body.append(section("projects", "projects", site["copy"]["projects_note"], stops(by_line.get("projects", []))))
    body.append(section("games", "games", site["copy"]["games_note"], stops(by_line.get("games", []))))

    smalls = by_line.get("small", [])
    if smalls:
        rows = "".join(
            f'<li><a href="{E(s["link"][0]["href"])}" rel="noopener">{E(s["title"])}</a>'
            f'<span>{inline(s["summary"])}</span></li>' for s in smalls
        )
        body.append(f"""<section class="sect sect--tight" id="smaller">
  <header class="sect-head"><h2><span class="bullet bullet--small"></span>smaller things</h2></header>
  <ul class="minor">{rows}</ul>
</section>
""")

    tiles = "".join(
        f'<figure class="plate"><a href="{E(a["src"])}">'
        f'<img src="{E(a["src"])}" alt="{E(a["caption"])}" loading="lazy" decoding="async"></a>'
        f'<figcaption>{inline(a["caption"])}</figcaption></figure>' for a in art
    )
    body.append(section("art", "art", site["copy"]["art_note"],
                        f'<div class="gallery">{tiles}</div>'))

    post_rows = "".join(
        f'<li class="entry entry--post"><h3><a href="blog/{E(po["slug"])}.html">{E(po["title"])}</a></h3>'
        f'<p class="meta"><span class="when">{E(po["date"])}</span></p>'
        f'<p class="summary">{inline(po.get("summary", ""))}</p></li>' for po in posts
    )
    body.append(section(
        "writing", "writing", site["copy"]["writing_note"],
        f'<ol class="stops">{post_rows}</ol>'
        f'<p class="entry-links entry-links--loose"><a class="go" href="blog/index.html">all posts</a>'
        f'<a class="go" href="feed.xml">rss</a></p>'))

    now = site["now"]
    now_items = "".join(f"<li>{inline(x)}</li>" for x in now["items"])
    body.append(section("now", "now", None,
                        f'<div class="panel"><ul class="ticks">{now_items}</ul>'
                        f'<p class="stamp">updated {E(now["updated"])}</p></div>',
                        kicker="what I'm on with"))

    groups = "".join(
        f'<div class="uses-group"><h3>{E(g["group"])}</h3><ul>'
        + "".join(f"<li>{inline(x)}</li>" for x in g["items"]) + "</ul></div>"
        for g in site["uses"]
    )
    body.append(section("uses", "uses", None, f'<div class="uses">{groups}</div>'))

    btns = "".join(
        (f'<a href="{E(b["href"])}" rel="noopener">' if b.get("href") else "<span>")
        + f'<img src="{E(b["src"])}" alt="{E(b["alt"])}" width="88" height="31" title="{E(b.get("title", b["alt"]))}">'
        + ("</a>" if b.get("href") else "</span>")
        for b in site["button"]
    )
    body.append(f"""<section class="sect sect--tight" id="buttons">
  <header class="sect-head"><h2><span class="bullet bullet--small"></span>buttons</h2>
  <p class="note">{inline(site['copy']['buttons_note'])}</p></header>
  <div class="buttons">{btns}</div>
</section>
""")

    body.append(f"""<section class="sect sect--tight" id="colophon">
  <header class="sect-head"><h2><span class="bullet bullet--small"></span>colophon</h2></header>
  <div class="prose prose--small">{markdown(site['colophon']['body'])}</div>
  <p class="terminus"><svg viewBox="0 0 64 64" width="26" height="26" aria-hidden="true">
    <ellipse cx="32" cy="42" rx="15" ry="12"/><ellipse cx="14" cy="24" rx="7" ry="9"/>
    <ellipse cx="27" cy="16" rx="7" ry="10"/><ellipse cx="42" cy="17" rx="7" ry="10"/>
    <ellipse cx="54" cy="27" rx="7" ry="9"/></svg><span>end of the line</span></p>
</section>
""")

    html_out = (head(0, f"{p['handle']} - {p['tagline']}", p["description"], site)
                + site_header(0, site)
                + '<main id="main">\n' + "\n".join(body) + "</main>\n"
                + site_footer(0, site))
    write("index.html", html_out)


def build_blog(site, posts):
    p = site["profile"]
    rows = "".join(
        f'<li class="entry entry--post"><h3><a href="{E(po["slug"])}.html">{E(po["title"])}</a></h3>'
        f'<p class="meta"><span class="when">{E(po["date"])}</span></p>'
        f'<p class="summary">{inline(po.get("summary", ""))}</p></li>' for po in posts
    )
    body = f"""<section class="sect sect--lead">
  <header class="sect-head"><p class="kicker">writing</p><h2><span class="bullet"></span>posts</h2>
  <p class="note">{inline(site['copy']['writing_note'])}</p></header>
  <ol class="stops">{rows}</ol>
  <p class="entry-links entry-links--loose"><a class="go" href="../feed.xml">rss</a></p>
</section>
"""
    write("blog/index.html",
          head(1, f"writing - {p['handle']}", "Posts by " + p["name"], site)
          + site_header(1, site) + f'<main id="main">{body}</main>' + site_footer(1, site))

    for po in posts:
        article = f"""<article class="post">
  <header class="post-head">
    <p class="kicker"><a href="index.html">writing</a> &middot; {E(po['date'])}</p>
    <h1>{E(po['title'])}</h1>
  </header>
  <div class="prose">{markdown(po['body'])}</div>
  <p class="entry-links entry-links--loose"><a class="go" href="index.html">more posts</a>
  <a class="go" href="../index.html">home</a></p>
</article>
"""
        write(f"blog/{po['slug']}.html",
              head(1, f"{po['title']} - {p['handle']}", po.get("summary", ""), site)
              + site_header(1, site) + f'<main id="main">{article}</main>' + site_footer(1, site))


def build_feed(site, posts):
    base = site["profile"]["base_url"].rstrip("/") + "/"
    # Stamped from the newest post rather than the clock, so rebuilding without
    # writing anything produces no diff.
    latest = datetime.strptime(posts[0]["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    now = format_datetime(latest)
    items = []
    for po in posts:
        url = base + f"blog/{po['slug']}.html"
        when = datetime.strptime(po["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        items.append(f"""  <item>
    <title>{E(po['title'])}</title>
    <link>{E(url)}</link>
    <guid isPermaLink="true">{E(url)}</guid>
    <pubDate>{format_datetime(when)}</pubDate>
    <description>{E(po.get('summary', ''))}</description>
  </item>""")
    feed = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{E(site['profile']['handle'])}</title>
  <link>{E(base)}</link>
  <atom:link href="{E(base)}feed.xml" rel="self" type="application/rss+xml"/>
  <description>{E(site['profile']['description'])}</description>
  <language>en-gb</language>
  <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
"""
    write("feed.xml", feed)


def build_404(site):
    p = site["profile"]
    # Pages serves this file for any missing path under the project, at any depth,
    # so relative URLs would resolve against the wrong directory.
    home = "/" + p["base_url"].split("//", 1)[1].split("/", 1)[1]
    body = f"""<section class="sect sect--lead lost">
  <p class="kicker">404</p>
  <h1>this stop is closed</h1>
  <p class="summary">Nothing at this address. Try the <a href="{E(home)}">front page</a>.</p>
  <img class="lost-img" src="{E(home)}assets/img/under_construction.webp"
       alt="A drawing of Milo next to two cogs, captioned UNDER CONSTRUCTION" width="600" height="450">
</section>
"""
    write("404.html", head(0, "404 - " + p["handle"], "Page not found", site)
          + site_header(0, site) + f'<main id="main">{body}</main>' + site_footer(0, site))


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  {path} ({len(text) // 1024} KB)")


def main():
    site = load("site.toml")
    projects = load("projects.toml")["project"]
    art = load("art.toml")["piece"]
    posts = load_posts()
    print("building:")
    build_index(site, projects, art, posts)
    build_blog(site, posts)
    build_feed(site, posts)
    build_404(site)
    print(f"done: {len(projects)} projects, {len(art)} drawings, {len(posts)} posts")


if __name__ == "__main__":
    main()
