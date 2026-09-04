#!/usr/bin/env python3
"""Staple content/ and posts/ into index.html, blog/, feed.xml and 404.html.

Standard library only. Run from anywhere: python3 tools/build.py
"""

import html
import re
import tomllib
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
POSTS = ROOT / "posts"


# ---------- markdown (the subset these pages use) ----------

INLINE_RULES = [
    (re.compile(r"!\[([^\]]*)\]\(([^)]+)\)"), r'<img src="\2" alt="\1">'),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\w)\*(.+?)\*(?!\w)"), r"<em>\1</em>"),
]


def inline(text):
    # Code spans are pulled out first so nothing inside them gets styled.
    spans = []

    def stash(m):
        spans.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, html.escape(text, quote=False))
    for rule, repl in INLINE_RULES:
        text = rule.sub(repl, text)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)


def markdown(src):
    out, para, list_tag, in_code = [], [], None, False

    def flush_para():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()

    def close_list():
        nonlocal list_tag
        if list_tag:
            out.append(f"</{list_tag}>")
            list_tag = None

    for line in src.splitlines():
        if line.startswith("```"):
            flush_para()
            close_list()
            in_code = not in_code
            out.append("<pre><code>" if in_code else "</code></pre>")
            continue
        if in_code:
            out.append(html.escape(line))
            continue
        stripped = line.strip()
        if not stripped:
            flush_para()
            close_list()
            continue
        m = re.match(r"(#{1,3})\s+(.*)", stripped)
        if m:
            flush_para()
            close_list()
            level = len(m.group(1)) + 1
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue
        if stripped in ("---", "***"):
            flush_para()
            close_list()
            out.append("<hr>")
            continue
        if stripped.startswith("> "):
            flush_para()
            close_list()
            out.append(f"<blockquote><p>{inline(stripped[2:])}</p></blockquote>")
            continue
        m = re.match(r"([-*]|\d+\.)\s+(.*)", stripped)
        if m:
            flush_para()
            tag = "ol" if m.group(1)[0].isdigit() else "ul"
            if list_tag != tag:
                close_list()
                out.append(f"<{tag}>")
                list_tag = tag
            out.append(f"<li>{inline(m.group(2))}</li>")
            continue
        para.append(stripped)
    flush_para()
    close_list()
    return "\n".join(out)


def front_matter(text):
    meta = {}
    if text.startswith("---"):
        _, block, text = text.split("---", 2)
        for line in block.strip().splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, text.strip()


# ---------- data ----------

def load():
    site = tomllib.loads((CONTENT / "site.toml").read_text())
    projects = tomllib.loads((CONTENT / "projects.toml").read_text())["project"]
    art = tomllib.loads((CONTENT / "art.toml").read_text())["art"]
    buttons = tomllib.loads((CONTENT / "buttons.toml").read_text())["button"]
    pages = {p.stem: markdown((CONTENT / p.name).read_text()) for p in CONTENT.glob("*.md")}
    posts = []
    for path in sorted(POSTS.glob("*.md"), reverse=True):
        meta, body = front_matter(path.read_text())
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        posts.append({**meta, "slug": slug, "html": markdown(body)})
    return site, projects, art, buttons, pages, posts


def pretty_date(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%-d %B %Y")


# ---------- html pieces ----------

def e(text):
    return html.escape(text, quote=True)


def head(site, title, description, root, canonical):
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="{e(site['name'])}">
<meta name="theme-color" content="#11111b">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{e(site['url'] + canonical)}">
<meta property="og:image" content="{e(site['url'] + 'assets/img/avatar.webp')}">
<link rel="canonical" href="{e(site['url'] + canonical)}">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{e(site['title'])} blog" href="{root}feed.xml">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
"""


def masthead(site, root, items):
    links = "".join(f'<a href="{href}">{e(label)}</a>' for label, href in items)
    return f"""<nav class="masthead" aria-label="contents">
<a class="brand" href="{root}"><b>{e(site['title'])}</b> <span>{e(site['issue'])}</span></a>
<div class="masthead-links">{links}</div>
</nav>
"""


def folio(site, num, side):
    running = site["title"] + " · " + site["issue"] if side == "verso" else site["date"]
    return f'<footer class="folio"><span class="running">{e(running)}</span><span class="num">{num}</span></footer>'


def riso(src, alt, caption="", href=None, cls=""):
    img = f'<img src="{e(src)}" alt="{e(alt)}" loading="lazy">'
    inner = f'<a class="riso" href="{e(href)}">{img}</a>' if href else f'<span class="riso">{img}</span>'
    cap = f"<figcaption>{e(caption)}</figcaption>" if caption else ""
    return f'<figure class="copy {cls}">{inner}{cap}</figure>'


def tags(items):
    return '<ul class="tags">' + "".join(f"<li>{e(t)}</li>" for t in items) + "</ul>"


def linkrow(items):
    if not items:
        return ""
    return '<p class="links">' + " ".join(f'<a href="{e(l["url"])}">{e(l["label"])}</a>' for l in items) + "</p>"


def project_feature(p):
    figs = "".join(riso(i["src"], i["alt"], i.get("caption", "")) for i in p.get("images", []))
    figs_cls = "figs figs-" + str(len(p.get("images", [])))
    return f"""<section class="project feature" id="{e(slugify(p['name']))}">
<p class="kicker">{e(p['kicker'])}</p>
<h3>{e(p['name'])}</h3>
<div class="{figs_cls}">{figs}</div>
{markdown(p['blurb'])}
{tags(p.get('tags', []))}
{linkrow(p.get('links', []))}
</section>"""


def project_short(p):
    img = p.get("images", [None])[0]
    fig = riso(img["src"], img["alt"], img.get("caption", ""), cls="thumb") if img else ""
    return f"""<section class="project short" id="{e(slugify(p['name']))}">
{fig}
<div>
<p class="kicker">{e(p['kicker'])}</p>
<h3>{e(p['name'])}</h3>
{markdown(p['blurb'])}
{linkrow(p.get('links', []))}
</div>
</section>"""


def project_small(p):
    return f"""<li class="ad" id="{e(slugify(p['name']))}">
<b>{e(p['name'])}</b> <span class="kicker">{e(p['kicker'])}</span>
{markdown(p['blurb'])}
{linkrow(p.get('links', []))}
</li>"""


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# ---------- pages of the zine ----------

def build_pages(site, projects, art, buttons, pages, posts, root=""):
    """Return (id, title, html) for every inner page, in reading order."""
    inner = []

    inner.append(("hello", "hello", "hello", f"""
<p class="kicker">hello</p>
<h2 class="title">Hiya.</h2>
<figure class="copy portrait tape"><span class="riso"><img src="{root}assets/img/me.png" alt="A stick figure self portrait labelled Me, frowning" width="180" height="280"></span><figcaption>self portrait, accurate</figcaption></figure>
{pages['hello']}
<p class="pull">Photocopied with care.</p>
"""))

    inner.append(("work", "the day job", "work", f"""
<p class="kicker">the day job</p>
<h2 class="title">Search, for mobile.</h2>
{pages['work']}
<p class="links"><a href="{e(site['cv'])}">cv.pdf</a> <a href="https://www.linkedin.com/in/fired/">linkedin</a></p>
<figure class="copy skyline"><span class="riso"><img src="https://raw.githubusercontent.com/milotek/milotek/main/profile-3d-contrib/profile-night-rainbow.svg" alt="3D bar chart of a year of GitHub contributions" loading="lazy"></span><figcaption>commit skyline, regenerated nightly by a GitHub Action in my profile repo</figcaption></figure>
"""))

    features = [p for p in projects if p["size"] == "feature"]
    shorts = [p for p in projects if p["size"] == "short"]
    smalls = [p for p in projects if p["size"] == "small"]

    for i in range(0, len(features), 2):
        chunk = features[i:i + 2]
        intro = ""
        if i == 0:
            intro = '<p class="kicker">projects</p><h2 class="title">Things I\'ve built.</h2><p class="standfirst">Software, hardware and games, biggest first. Hover the pictures for colour.</p>'
        inner.append((f"projects-{i // 2 + 1}", "projects" if i == 0 else "projects, continued", "projects" if i == 0 else None, intro + "".join(project_feature(p) for p in chunk)))

    inner.append(("projects-shorts", "games and shaders", None, '<p class="kicker">projects · games and shaders</p>' + "".join(project_short(p) for p in shorts)))

    inner.append(("classifieds", "classifieds", None, f"""
<p class="kicker">classifieds</p>
<h2 class="title">Smaller, weirder, on GitHub.</h2>
<ul class="ads">{"".join(project_small(p) for p in smalls)}</ul>
<p class="links"><a href="https://github.com/milotek?tab=repositories">all repos</a></p>
"""))

    art_items = "".join(
        f'<li>{riso(f"{root}assets/img/art/{a["file"]}_thumb.webp", a["title"], a["caption"], href=f"{root}assets/img/art/{a["file"]}.webp")}</li>'
        for a in art
    )
    inner.append(("art", "art", "art", f"""
<p class="kicker">art</p>
<h2 class="title">Drawn, mostly in Procreate.</h2>
<ul class="gallery">{art_items}</ul>
<div class="mascot">
<img src="{root}assets/img/wawawa.gif" alt="An orange cartoon cat saying wawawa" width="120" height="120">
<p>wawawa.gif, found on my file server. Fairly sure I didn't draw it. Holding the spot until I do.</p>
</div>
"""))

    inner.append(("now", "now and uses", "now", f"""
<p class="kicker">now</p>
<h2 class="title">Lately.</h2>
{pages['now']}
<p class="kicker">uses</p>
{pages['uses']}
"""))

    post_items = "".join(
        f'<li><a href="{root}blog/{e(p["slug"])}.html"><b>{e(p["title"])}</b></a><span class="kicker">{e(pretty_date(p["date"]))}</span><p>{e(p["summary"])}</p></li>'
        for p in posts
    )
    inner.append(("blog", "blog", "blog", f"""
<p class="kicker">blog</p>
<h2 class="title">Written down.</h2>
<ul class="posts">{post_items}</ul>
<p class="standfirst">One post so far, about this site. Posts are Markdown files in a folder; the feed is real.</p>
<p class="links"><a href="{root}blog/">blog index</a> <a href="{root}feed.xml">rss</a></p>
"""))

    contact_items = "".join(
        f'<li><a href="{e(l["url"])}">{e(l["label"])}</a><span>{e(l["note"])}</span></li>' for l in site["links"]
    )
    inner.append(("contact", "contact", "contact", f"""
<p class="kicker">contact</p>
<h2 class="title">Say hi.</h2>
<ul class="contacts">{contact_items}</ul>
<p class="cvbox"><a href="{e(site['cv'])}">Download the CV (pdf)</a></p>
<p class="pull">Email is best. I do read it.</p>
"""))

    if len(inner) % 2:
        inner.append(("blank", "notes", None, '<p class="blank">This page intentionally left blank.</p>'))
    return inner


def cover(site, contents, root=""):
    toc = "".join(f'<li><a href="#{e(pid)}"><span>{e(title)}</span><i></i><b>{num}</b></a></li>' for pid, title, num in contents)
    return f"""<section class="sheet cover-sheet" id="cover">
<article class="page cover">
<p class="strip"><span>{e(site['issue'])}</span><span>{e(site['date'])}</span><span>free · take one</span></p>
<h1 class="masthead-title">{e(site['title'])}</h1>
<p class="tagline">{e(site['tagline'])}</p>
<figure class="copy cover-art tape"><span class="riso"><img src="{root}assets/img/avatar.webp" alt="Black and white drawing of a figure with raised clawed hands" width="480" height="480"></span></figure>
<p class="kicker">in this issue</p>
<ol class="toc">{toc}</ol>
<div class="barcode" aria-hidden="true"><span></span><small>milotek.dev</small></div>
</article>
</section>
"""


def back_cover(site, buttons, pages, num, root=""):
    btns = "".join(
        (f'<a href="{e(b["url"])}"><img src="{root}assets/buttons/{e(b["img"])}" alt="{e(b["alt"])}" width="88" height="31"></a>'
         if b.get("url") else f'<img src="{root}assets/buttons/{e(b["img"])}" alt="{e(b["alt"])}" width="88" height="31">')
        for b in buttons
    )
    snippet = e(f'<a href="{site["url"]}"><img src="{site["url"]}assets/buttons/milotek.png" alt="milo tek" width="88" height="31"></a>')
    return f"""<section class="sheet back-sheet" id="back">
<article class="page back">
<p class="kicker">back page · buttons</p>
<div class="buttons">{btns}</div>
<p class="snippet"><span>link back:</span><code>{snippet}</code></p>
<p class="kicker">colophon</p>
{pages['colophon']}
<p class="tiny">© {e(site['name'])} 2024 to 2026. No cookies, no analytics, one staple short of a magazine.</p>
<img class="moose" src="{root}assets/img/moose.png" alt="" width="48" height="48">
{folio(site, num, "verso")}
</article>
</section>
"""


def build_index(site, projects, art, buttons, pages, posts):
    inner = build_pages(site, projects, art, buttons, pages, posts)
    contents = [(pid, title, i + 2) for i, (pid, title, _, _) in enumerate(inner)]
    nav = [(label, f"#{pid}") for pid, _, label, _ in inner if label] + [("back page", "#back")]
    back_num = len(inner) + 2
    contents.append(("back", "back page", back_num))

    spreads = []
    for i in range(0, len(inner), 2):
        left, right = inner[i], inner[i + 1]
        ln, rn = i + 2, i + 3
        spreads.append(f"""<section class="sheet spread">
<article class="page verso" id="{e(left[0])}">{left[3]}{folio(site, ln, "verso")}</article>
<div class="fold" aria-hidden="true"><i class="staple"></i><i class="staple"></i></div>
<article class="page recto" id="{e(right[0])}">{right[3]}{folio(site, rn, "recto")}</article>
</section>
""")

    out = head(site, f"{site['title']} · {site['tagline']}", site["description"], "", "")
    out += masthead(site, "", nav)
    out += '<main class="desk">\n' + cover(site, contents) + "".join(spreads) + back_cover(site, buttons, pages, back_num) + "</main>\n"
    out += "</body>\n</html>\n"
    (ROOT / "index.html").write_text(out)
    return contents


def build_post(site, post):
    root = "../"
    out = head(site, f"{post['title']} · {site['title']}", post["summary"], root, f"blog/{post['slug']}.html")
    out += masthead(site, root, [("home", root), ("blog", root + "blog/"), ("rss", root + "feed.xml")])
    out += f"""<main class="desk">
<section class="sheet single-sheet">
<article class="page single">
<p class="kicker">blog · {e(pretty_date(post['date']))}</p>
<h1 class="title">{e(post['title'])}</h1>
<p class="standfirst">{e(post['summary'])}</p>
<div class="prose">{post['html']}</div>
<p class="links"><a href="{root}blog/">more posts</a> <a href="{root}#blog">back to the zine</a></p>
<footer class="folio"><span class="running">{e(site['title'])} · blog</span><span class="num">{e(post['slug'])}</span></footer>
</article>
</section>
</main>
</body>
</html>
"""
    (ROOT / "blog" / f"{post['slug']}.html").write_text(out)


def build_blog_index(site, posts):
    root = "../"
    items = "".join(
        f'<li><a href="{e(p["slug"])}.html"><b>{e(p["title"])}</b></a><span class="kicker">{e(pretty_date(p["date"]))}</span><p>{e(p["summary"])}</p></li>'
        for p in posts
    )
    out = head(site, f"blog · {site['title']}", "Posts by Milo Tekchandani.", root, "blog/")
    out += masthead(site, root, [("home", root), ("rss", root + "feed.xml")])
    out += f"""<main class="desk">
<section class="sheet single-sheet">
<article class="page single">
<p class="kicker">blog</p>
<h1 class="title">Written down.</h1>
<ul class="posts">{items}</ul>
<p class="links"><a href="{root}feed.xml">rss</a> <a href="{root}#blog">back to the zine</a></p>
<footer class="folio"><span class="running">{e(site['title'])} · blog</span><span class="num">index</span></footer>
</article>
</section>
</main>
</body>
</html>
"""
    (ROOT / "blog" / "index.html").write_text(out)


def build_feed(site, posts):
    items = []
    for p in posts:
        url = f"{site['url']}blog/{p['slug']}.html"
        stamp = format_datetime(datetime.strptime(p["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc))
        body = p["html"].replace("../", site["url"])
        items.append(f"""<item>
<title>{e(p['title'])}</title>
<link>{e(url)}</link>
<guid>{e(url)}</guid>
<pubDate>{stamp}</pubDate>
<description>{e(p['summary'])}</description>
<content:encoded><![CDATA[{body}]]></content:encoded>
</item>""")
    now = format_datetime(datetime.now(timezone.utc))
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
<title>{e(site['title'])} · blog</title>
<link>{e(site['url'])}</link>
<atom:link href="{e(site['url'])}feed.xml" rel="self" type="application/rss+xml"/>
<description>{e(site['description'])}</description>
<language>en-gb</language>
<lastBuildDate>{now}</lastBuildDate>
{"".join(items)}
</channel>
</rss>
"""
    (ROOT / "feed.xml").write_text(feed)


def build_404(site):
    out = head(site, f"missing page · {site['title']}", "That page fell out of the zine.", "", "404.html")
    out += masthead(site, "", [("home", "./")])
    out += f"""<main class="desk">
<section class="sheet single-sheet">
<article class="page single">
<p class="kicker">404</p>
<h1 class="title">This page fell out.</h1>
<p>Staples only hold so much. <a href="./">Back to the cover.</a></p>
<footer class="folio"><span class="running">{e(site['title'])}</span><span class="num">?</span></footer>
</article>
</section>
</main>
</body>
</html>
"""
    (ROOT / "404.html").write_text(out)


def main():
    site, projects, art, buttons, pages, posts = load()
    (ROOT / "blog").mkdir(exist_ok=True)
    contents = build_index(site, projects, art, buttons, pages, posts)
    for post in posts:
        build_post(site, post)
    build_blog_index(site, posts)
    build_feed(site, posts)
    build_404(site)
    print("pages:", ", ".join(f"{n} {t}" for _, t, n in contents))
    print("posts:", len(posts))


if __name__ == "__main__":
    main()
