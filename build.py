#!/usr/bin/env python3
"""Builds the site from content/ into the repository root.

Run `python3 build.py`. Output is committed because GitHub Pages serves this
repo's files directly.
"""

import email.utils
import html
import re
import shutil
import sys
import tomllib
from datetime import date, datetime, timezone
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"

# Everything the build writes. Cleared first so a deleted post cannot survive
# in the committed output.
OUTPUTS = ["index.html", "404.html", "feed.xml", "assets", "projects", "blog", "art", "now", "uses", "colophon", "cv"]


# ---------------------------------------------------------------- content ---

def read_doc(path):
    """A content file: TOML frontmatter between +++ fences, then Markdown."""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("+++"):
        raise SystemExit("%s: missing +++ frontmatter" % path)
    _, front, body = raw.split("+++", 2)
    doc = tomllib.loads(front)
    doc["body"] = body.strip()
    doc.setdefault("slug", path.stem)
    doc["source"] = path
    return doc


def load_dir(name):
    d = CONTENT / name
    return [read_doc(p) for p in sorted(d.glob("*.md"))] if d.is_dir() else []


site = tomllib.loads((CONTENT / "site.toml").read_text(encoding="utf-8"))
projects = load_dir("projects")
posts = sorted(load_dir("posts"), key=lambda p: p["date"], reverse=True)
pages = {p["slug"]: p for p in load_dir("pages")}
art = tomllib.loads((CONTENT / "art.toml").read_text(encoding="utf-8"))["piece"]

for p in projects:
    p.setdefault("weight", 100)
projects.sort(key=lambda p: (p["weight"], p["title"].lower()))


# ----------------------------------------------------------------- layout ---

def e(text):
    return html.escape(str(text), quote=True)


def rel(depth):
    """Prefix that walks back to the site root, so the build is base-path free."""
    return "../" * depth if depth else ""


def icon_links(links, depth, cls="linkrow"):
    if not links:
        return ""
    items = []
    for label, href in links:
        external = "://" in href or href.startswith("mailto:")
        target = ' target="_blank" rel="noopener"' if "://" in href else ""
        items.append(
            '<a class="pill" href="%s"%s>%s%s</a>'
            % (e(href), target, e(label), '<span class="ext" aria-hidden="true">&#8599;</span>' if external else "")
        )
    return '<div class="%s">%s</div>' % (cls, "".join(items))


NAV = [("projects", "projects/"), ("blog", "blog/"), ("art", "art/"), ("now", "now/"), ("cv", "cv/")]


def page(path, title, body, depth, description=None, active=None, wide=False):
    base = rel(depth)
    desc = description or site["description"]
    nav = "".join(
        '<a href="%s%s"%s>%s</a>' % (base, href, ' class="on"' if active == label else "", label)
        for label, href in NAV
    )
    buttons = "".join(
        '<a href="%s"%s title="%s"><img src="%simg/buttons/%s" width="88" height="31" alt="%s"></a>'
        % (e(b["href"]), ' target="_blank" rel="noopener"' if "://" in b["href"] else "", e(b["title"]), base + "assets/", e(b["file"]), e(b["title"]))
        for b in site["buttons"]
    )
    social = "".join(
        '<a href="%s" target="_blank" rel="noopener">%s</a>' % (e(s["href"]), e(s["name"]))
        for s in site["socials"]
    )
    doc = """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#1e1e2e">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="{base}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="{base}assets/css/site.css">
<link rel="alternate" type="application/rss+xml" title="{name} &middot; blog" href="{base}feed.xml">
</head>
<body>
<a class="skip" href="#main">skip to content</a>
<header class="topbar">
  <div class="wrap bar">
    <a class="brand" href="{base}index.html"><span class="brand-mark" aria-hidden="true"></span>milo tek</a>
    <nav class="nav">{nav}</nav>
  </div>
</header>
<main id="main" class="wrap{widecls}">
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <div class="buttons">{buttons}</div>
    <div class="footcols">
      <div><span class="lbl">elsewhere</span><div class="footlinks">{social}</div></div>
      <div><span class="lbl">this site</span><div class="footlinks"><a href="{base}uses/">uses</a><a href="{base}colophon/">colophon</a><a href="{base}feed.xml">rss</a><a href="{repo}" target="_blank" rel="noopener">source</a></div></div>
    </div>
    <p class="fineprint">&copy; {year} Milo Tekchandani. Built by hand in {city}.</p>
  </div>
</footer>
</body>
</html>
""".format(
        title=e(title),
        desc=e(desc),
        name=e(site["name"]),
        base=base,
        nav=nav,
        body=body,
        buttons=buttons,
        social=social,
        repo=e(site["repo"]),
        year=date.today().year,
        city=e(site["city"]),
        widecls=" wide" if wide else "",
    )
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


def section(label, title, body, extra=""):
    head = '<div class="sechead"><span class="lbl">%s</span>%s</div>' % (
        e(label),
        '<h2>%s</h2>%s' % (e(title), extra) if title else extra,
    )
    return '<section class="sec">%s%s</section>' % (head, body)


# --------------------------------------------------------------- projects ---

def project_media(p, depth):
    base = rel(depth) + "assets/img/projects/"
    if p.get("cover"):
        return '<div class="media cover %s"><img src="%s%s" alt="%s" loading="lazy" decoding="async"></div>' % (
            e(p.get("fit", "crop")), base, e(p["cover"]), e(p["title"])
        )
    shots = p.get("shots") or []
    if shots:
        imgs = "".join(
            '<img src="%s%s" alt="%s" loading="lazy" decoding="async">' % (base, e(s), e(p["title"]))
            for s in shots
        )
        return '<div class="media shots">%s</div>' % imgs
    return ""


def project_card(p, depth):
    tags = "".join('<span class="tag">%s</span>' % e(t) for t in p.get("tags", []))
    links = icon_links([(l["label"], l["href"]) for l in p.get("links", [])], depth)
    meta = [e(p[k]) for k in ("year", "status") if p.get(k)]
    media = project_media(p, depth)
    return (
        '<article class="card%s">%s<div class="cardbody">'
        '<div class="cardhead"><h3>%s</h3><span class="meta">%s</span></div>'
        "%s<div class=\"tags\">%s</div>%s</div></article>"
    ) % (
        "" if media else " nomedia",
        media,
        e(p["title"]),
        " &middot; ".join(meta),
        markdown.render(p["body"]),
        tags,
        links,
    )


# ------------------------------------------------------------------ pages ---

def build_home():
    featured = [p for p in projects if p.get("featured")]
    cards = "".join(project_card(p, 0) for p in featured)

    work = site["work"]
    worklinks = icon_links([(l["label"], l["href"]) for l in work.get("links", [])], 0)
    workblock = (
        '<div class="now-card"><div class="now-head"><h3>%s</h3><span class="meta">%s</span></div>'
        "%s%s</div>"
    ) % (e(work["title"]), e(work["period"]), markdown.render(work["body"]), worklinks)

    postlist = "".join(
        '<li><a href="blog/%s/"><time datetime="%s">%s</time><span class="ptitle">%s</span></a>'
        '<span class="psum">%s</span></li>'
        % (e(p["slug"]), p["date"].isoformat(), p["date"].strftime("%d %b %Y").lower(), e(p["title"]), e(p["summary"]))
        for p in posts[:3]
    )

    hero = """<section class="hero">
  <div class="hero-text">
    <p class="kicker">{kicker}</p>
    <h1>{headline}</h1>
    {intro}
    {links}
  </div>
  <div class="hero-art">
    <img src="assets/img/face.png" width="220" height="220" alt="Cartoon drawing of Milo holding a mug">
  </div>
</section>""".format(
        kicker=e(site["kicker"]),
        headline=e(site["headline"]),
        intro=markdown.render(site["intro"]),
        links=icon_links([(l["label"], l["href"]) for l in site["hero_links"]], 0, "linkrow big"),
    )

    body = "\n".join([
        hero,
        section("work", "", workblock),
        section("selected projects", "", cards,
                '<a class="more" href="projects/">all %d projects &rarr;</a>' % len(projects)),
        section("writing", "", '<ul class="postlist">%s</ul>' % postlist,
                '<a class="more" href="blog/">the blog &rarr;</a>'),
    ])
    page("index.html", "%s &middot; %s" % (site["name"], site["tagline"]), body, 0, active=None)


def build_projects():
    featured = [p for p in projects if p.get("featured")]
    rest = [p for p in projects if not p.get("featured")]
    body = [
        '<header class="pagehead"><h1>projects</h1><p>%s</p></header>' % e(site["projects_blurb"]),
        section("featured", "", "".join(project_card(p, 1) for p in featured)),
        section("everything else", "", "".join(project_card(p, 1) for p in rest)),
    ]
    scraps = site.get("scraps") or []
    if scraps:
        items = "".join(
            '<li><a href="%s" target="_blank" rel="noopener">%s</a> <span>%s</span></li>'
            % (e(s["href"]), e(s["name"]), e(s["note"]))
            for s in scraps
        )
        body.append(section("odds and ends", "", '<ul class="scraps">%s</ul>' % items))
    page("projects/index.html", "projects &middot; %s" % site["name"], "\n".join(body), 1,
         description=site["projects_blurb"], active="projects")


def build_blog():
    items = "".join(
        '<li><a href="%s/"><time datetime="%s">%s</time><span class="ptitle">%s</span></a>'
        '<span class="psum">%s</span></li>'
        % (e(p["slug"]), p["date"].isoformat(), p["date"].strftime("%d %b %Y").lower(), e(p["title"]), e(p["summary"]))
        for p in posts
    )
    body = (
        '<header class="pagehead"><h1>blog</h1><p>%s</p>'
        '<p class="feednote"><a href="../feed.xml">rss</a> if you want it.</p></header>'
        '<ul class="postlist big">%s</ul>' % (e(site["blog_blurb"]), items)
    )
    page("blog/index.html", "blog &middot; %s" % site["name"], body, 1,
         description=site["blog_blurb"], active="blog")

    for p in posts:
        article = (
            '<article class="post">'
            '<header class="pagehead"><p class="kicker"><time datetime="%s">%s</time></p><h1>%s</h1></header>'
            '<div class="prose">%s</div></article>'
            '<a class="more" href="../">&larr; all posts</a>'
        ) % (p["date"].isoformat(), p["date"].strftime("%d %B %Y").lower(), e(p["title"]), markdown.render(p["body"]))
        page("blog/%s/index.html" % p["slug"], "%s &middot; %s" % (p["title"], site["name"]), article, 2,
             description=p["summary"], active="blog")


def build_art():
    tiles = "".join(
        '<figure class="art"><a href="../assets/img/art/%s" target="_blank" rel="noopener">'
        '<img src="../assets/img/art/thumbs/%s" alt="%s" loading="lazy" decoding="async"></a>'
        '<figcaption>%s</figcaption></figure>'
        % (e(a["file"]), e(a["file"].rsplit(".", 1)[0] + ".jpg"), e(a["caption"]), e(a["caption"]))
        for a in art
    )
    body = (
        '<header class="pagehead"><h1>art</h1><p>%s</p></header><div class="gallery">%s</div>'
        % (e(site["art_blurb"]), tiles)
    )
    page("art/index.html", "art &middot; %s" % site["name"], body, 1,
         description=site["art_blurb"], active="art")


def build_prose(slug, active=None):
    p = pages[slug]
    body = (
        '<header class="pagehead"><h1>%s</h1>%s</header><div class="prose">%s</div>'
        % (e(p["title"]),
           '<p>%s</p>' % e(p["summary"]) if p.get("summary") else "",
           markdown.render(p["body"]))
    )
    page("%s/index.html" % slug, "%s &middot; %s" % (p["title"], site["name"]), body, 1,
         description=p.get("summary"), active=active)


def build_cv():
    p = pages["cv"]
    body = (
        '<header class="pagehead"><h1>cv</h1><p>%s</p>%s</header>'
        '<div class="prose">%s</div>'
        '<div class="pdf"><object data="../assets/files/CV.pdf#view=FitH" type="application/pdf">'
        '<p>Your browser will not embed the PDF. <a href="../assets/files/CV.pdf">Download it instead.</a></p>'
        "</object></div>"
    ) % (
        e(p.get("summary", "")),
        icon_links([("download pdf", "../assets/files/CV.pdf"), ("email me", "mailto:" + site["email"])], 1),
        markdown.render(p["body"]),
    )
    page("cv/index.html", "cv &middot; %s" % site["name"], body, 1, description=p.get("summary"), active="cv")


def build_404():
    body = (
        '<header class="pagehead"><h1>404</h1><p>That page is not here. It might never have been.</p></header>'
        # 404.html is served for any depth under the base path, so the way back
        # has to be the absolute site URL rather than a relative hop.
        '<div class="linkrow"><a class="pill" href="%s">home</a></div>' % e(site["url"])
    )
    page("404.html", "404 &middot; %s" % site["name"], body, 0)


def build_feed():
    base = site["url"].rstrip("/") + "/"
    now = email.utils.format_datetime(datetime.now(timezone.utc))
    entries = []
    for p in posts:
        stamp = email.utils.format_datetime(datetime(p["date"].year, p["date"].month, p["date"].day, 12, tzinfo=timezone.utc))
        link = "%sblog/%s/" % (base, p["slug"])
        entries.append(
            "<item><title>%s</title><link>%s</link><guid isPermaLink=\"true\">%s</guid>"
            "<pubDate>%s</pubDate><description>%s</description>"
            "<content:encoded><![CDATA[%s]]></content:encoded></item>"
            % (e(p["title"]), e(link), e(link), stamp, e(p["summary"]), markdown.render(p["body"]))
        )
    feed = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">\n'
        "<channel><title>%s</title><link>%s</link><description>%s</description>"
        '<language>en-gb</language><lastBuildDate>%s</lastBuildDate>'
        '<atom:link href="%sfeed.xml" rel="self" type="application/rss+xml"/>%s</channel></rss>\n'
        % (e(site["name"]), e(base), e(site["description"]), now, e(base), "".join(entries))
    )
    (ROOT / "feed.xml").write_text(feed, encoding="utf-8")


def main():
    for name in OUTPUTS:
        target = ROOT / name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()

    shutil.copytree(STATIC, ROOT / "assets")
    build_home()
    build_projects()
    build_blog()
    build_art()
    build_prose("now", active="now")
    build_prose("uses")
    build_prose("colophon")
    build_cv()
    build_404()
    build_feed()
    (ROOT / ".nojekyll").touch()
    print("built %d projects, %d posts, %d drawings" % (len(projects), len(posts), len(art)))


if __name__ == "__main__":
    sys.exit(main())
