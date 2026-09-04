#!/usr/bin/env python3
"""Builds the static site from content/ into the repo root.

Stdlib only, so `python3 build.py` works anywhere without a lockfile or a
node_modules. Output is committed, because GitHub Pages serves this repo as
plain files.
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
TEMPLATES = os.path.join(ROOT, "templates")

# Everything the build writes. Wiped before each run so a deleted content file
# actually disappears from the deploy instead of lingering as a stale page.
GENERATED = ["index.html", "404.html", "feed.xml", "projects", "blog", "art", "now", "uses", "colophon"]


# ---------------------------------------------------------------- loading


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_toml(name):
    with open(os.path.join(CONTENT, name), "rb") as f:
        return tomllib.load(f)


def load_doc(path):
    """A content file is TOML frontmatter between +++ fences, then Markdown."""
    raw = read(path)
    meta, body = {}, raw
    if raw.startswith("+++"):
        end = raw.index("+++", 3)
        meta = tomllib.loads(raw[3:end])
        body = raw[end + 3 :]
    meta["body"] = body.strip()
    # Filenames carry an ordering prefix (01-, 2026-09-04-) that has no business
    # being in a URL.
    name = re.sub(r"^(\d+-)+", "", os.path.splitext(os.path.basename(path))[0])
    meta["slug"] = meta.get("slug") or name
    return meta


def load_dir(name):
    d = os.path.join(CONTENT, name)
    if not os.path.isdir(d):
        return []
    return [load_doc(os.path.join(d, f)) for f in sorted(os.listdir(d)) if f.endswith(".md")]


# ---------------------------------------------------------------- markdown

INLINE = [
    (re.compile(r"`([^`]+)`"), lambda m: "<code>%s</code>" % html.escape(m.group(1))),
    (re.compile(r"!\[([^\]]*)\]\(([^)]+)\)"), lambda m: '<img src="%s" alt="%s">' % (m.group(2), html.escape(m.group(1)))),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1))),
    (re.compile(r"\*\*([^*]+)\*\*"), lambda m: "<strong>%s</strong>" % m.group(1)),
    (re.compile(r"(?<![\w*])\*([^*\n]+)\*(?!\w)"), lambda m: "<em>%s</em>" % m.group(1)),
]


def inline(text):
    out = html.escape(text, quote=False)
    for pattern, fn in INLINE:
        out = pattern.sub(fn, out)
    return out


def markdown(src):
    """A deliberately small subset: headings, paragraphs, lists, quotes, code, rules."""
    lines = src.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("```"):
            i += 1
            block = []
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(block)))
        elif re.match(r"^#{1,4} ", line):
            level = len(line) - len(line.lstrip("#"))
            out.append("<h%d>%s</h%d>" % (level + 1, inline(line[level:].strip()), level + 1))
            i += 1
        elif line.startswith("> "):
            block = []
            while i < len(lines) and lines[i].startswith("> "):
                block.append(lines[i][2:])
                i += 1
            out.append("<blockquote>%s</blockquote>" % markdown("\n".join(block)))
        elif re.match(r"^[-*] ", line):
            items = []
            while i < len(lines) and re.match(r"^[-*] ", lines[i]):
                items.append("<li>%s</li>" % inline(lines[i][2:].strip()))
                i += 1
            out.append("<ul>%s</ul>" % "".join(items))
        elif line.startswith("---"):
            out.append("<hr>")
            i += 1
        elif line.startswith("<"):
            block = []
            while i < len(lines) and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append("\n".join(block))
        else:
            # Always consume the opening line. A paragraph that starts with a
            # character which almost opens a block (#ffbdbd, *emphasis*) would
            # otherwise match nothing here and spin forever.
            block = [line.strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^([-*#>]|```)", lines[i]):
                block.append(lines[i].strip())
                i += 1
            out.append("<p>%s</p>" % inline(" ".join(block)))
    return "\n".join(out)


# ---------------------------------------------------------------- templating


def render(template, **vars):
    out = template
    for key, value in vars.items():
        out = out.replace("{{%s}}" % key, str(value))
    return out


def rel(depth, target):
    """Every URL is relative, because the site deploys under a subpath."""
    return ("../" * depth) + target if depth else target


# ---------------------------------------------------------------- helpers


def esc(s):
    return html.escape(str(s), quote=True)


def tag_list(tags):
    return "".join('<li>%s</li>' % esc(t) for t in tags)


def links_html(links, depth):
    parts = []
    for label, url in links:
        ext = ' rel="noopener"' if url.startswith("http") else ""
        parts.append('<a class="lnk" href="%s"%s>%s</a>' % (esc(url), ext, esc(label)))
    return "".join(parts)


def entry_links(entry, depth):
    out = []
    if entry.get("repo"):
        out.append(("source", entry["repo"]))
    for extra in entry.get("links", []):
        out.append((extra["label"], extra["url"]))
    return links_html(out, depth)


# ---------------------------------------------------------------- the log

LANES = ["main", "games", "systems", "apps"]


def build_graph(entries):
    """Assign each entry a lane and work out which lanes are drawn on each row.

    A lane is live from its first entry to its last, which is what makes the
    rail read like a branch that opens and merges back rather than a stack of
    unrelated dots.
    """
    span = {}
    for idx, e in enumerate(entries):
        lane = e.get("lane", "main")
        lo, hi = span.get(lane, (idx, idx))
        span[lane] = (min(lo, idx), max(hi, idx))
    for idx, e in enumerate(entries):
        lane = e.get("lane", "main")
        e["_x"] = LANES.index(lane) if lane in LANES else 0
        rows = []
        for other, (lo, hi) in span.items():
            x = LANES.index(other) if other in LANES else 0
            if x == 0:
                rows.append((0, "through"))
            elif lo <= idx <= hi:
                if lo == hi:
                    rows.append((x, "single"))
                elif idx == lo:
                    rows.append((x, "open"))
                elif idx == hi:
                    rows.append((x, "close"))
                else:
                    rows.append((x, "through"))
        e["_rail"] = sorted(rows)
    return entries


def rail_html(entry):
    parts = []
    for x, kind in entry["_rail"]:
        segments = {
            "open": ["open", "down"],
            "close": ["up", "close"],
            "single": ["open", "close"],
            "through": [""],
        }[kind]
        for seg in segments:
            parts.append('<i class="ln l%d %s" style="--x:%d"></i>' % (x, seg, x))
    parts.append('<i class="dot l%d" style="--x:%d"></i>' % (entry["_x"], entry["_x"]))
    return '<span class="rail">%s</span>' % "".join(parts)


def entry_row(entry, depth, tpl):
    title = esc(entry["title"])
    if entry.get("body"):
        href = rel(depth, "projects/%s/" % entry["slug"])
        title = '<a href="%s">%s</a>' % (href, title)
    shot = ""
    if entry.get("thumb"):
        shot = '<a class="shot" href="%s"><img loading="lazy" src="%s" alt="%s"></a>' % (
            rel(depth, "projects/%s/" % entry["slug"]) if entry.get("body") else rel(depth, entry["thumb"]),
            rel(depth, entry["thumb"]),
            esc(entry.get("thumb_alt", entry["title"])),
        )
    return render(
        tpl,
        rail=rail_html(entry),
        lane=esc(entry.get("lane", "main")),
        date=esc(entry.get("when", "")),
        title=title,
        blurb=markdown(entry.get("blurb", "")),
        tags=tag_list(entry.get("tags", [])),
        links=entry_links(entry, depth),
        shot=shot,
        classes="entry" + (" is-head" if entry.get("head") else ""),
    )


# ---------------------------------------------------------------- pages


def main():
    site = load_toml("site.toml")
    buttons = load_toml("buttons.toml")
    tpl = {name[:-5]: read(os.path.join(TEMPLATES, name)) for name in os.listdir(TEMPLATES)}

    for path in GENERATED:
        full = os.path.join(ROOT, path)
        if os.path.isdir(full):
            shutil.rmtree(full)
        elif os.path.isfile(full):
            os.remove(full)

    entries = load_dir("entries")
    entries.sort(key=lambda e: e["sort"], reverse=True)
    build_graph(entries)
    posts = sorted(load_dir("posts"), key=lambda p: p["date"], reverse=True)
    pages = {p["slug"]: p for p in load_dir("pages")}

    def nav(depth, current):
        items = []
        for item in site["nav"]:
            cls = ' class="on"' if item["slug"] == current else ""
            items.append('<a href="%s"%s>%s</a>' % (rel(depth, item["url"]) or "./", cls, esc(item["label"])))
        return "".join(items)

    def shell(path, title, desc, body, current="", depth=None):
        depth = path.count("/") if depth is None else depth
        page = render(
            tpl["base"],
            title=esc(title),
            desc=esc(desc),
            body=body,
            nav=nav(depth, current),
            root=rel(depth, "") or "./",
            year=datetime.now().year,
            name=esc(site["name"]),
            canonical=site["url"] + ("" if path == "index.html" else path[: -len("index.html")]),
            footer_links=links_html([(s["label"], s["url"]) for s in site["socials"]], depth),
            buttons=buttons_html(depth),
        )
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(page)

    def buttons_html(depth):
        out = []
        for b in buttons["button"]:
            img = '<img src="%s" width="88" height="31" alt="%s" loading="lazy">' % (rel(depth, b["src"]), esc(b["alt"]))
            out.append('<a class="b31" href="%s" title="%s"%s>%s</a>' % (
                esc(b["href"]), esc(b.get("title", b["alt"])),
                ' rel="noopener"' if b["href"].startswith("http") else "", img))
        return "".join(out)

    # -- home: the log
    rows = "".join(entry_row(e, 0, tpl["entry"]) for e in entries)
    home = render(
        tpl["home"],
        intro=markdown(pages["intro"]["body"]),
        socials=links_html([(s["label"], s["url"]) for s in site["socials"]], 0),
        entries=rows,
        count=len(entries),
    )
    shell("index.html", site["name"], site["description"], home, current="log", depth=0)

    # -- project pages
    for e in entries:
        if not e.get("body"):
            continue
        gallery = "".join(
            '<figure><a href="%s"><img loading="lazy" src="%s" alt="%s"></a><figcaption>%s</figcaption></figure>'
            % (rel(2, g["src"]), rel(2, g["src"]), esc(g.get("caption", e["title"])), esc(g.get("caption", "")))
            for g in e.get("gallery", [])
        )
        body = render(
            tpl["project"],
            title=esc(e["title"]),
            lane=esc(e.get("lane", "main")),
            date=esc(e.get("when", "")),
            blurb=markdown(e.get("blurb", "")),
            body=markdown(e["body"]),
            tags=tag_list(e.get("tags", [])),
            links=entry_links(e, 2),
            gallery=('<div class="gallery">%s</div>' % gallery) if gallery else "",
            back=rel(2, ""),
        )
        shell("projects/%s/index.html" % e["slug"], "%s / %s" % (e["title"], site["short"]), e.get("blurb", ""), body, current="log")

    # -- blog
    items = "".join(
        render(tpl["postitem"], url="%s/" % p["slug"], date=esc(p["date"]), title=esc(p["title"]), summary=esc(p.get("summary", "")))
        for p in posts
    )
    shell("blog/index.html", "blog / %s" % site["short"], "Writing by %s." % site["name"],
          render(tpl["blog"], items=items, feed=rel(1, "feed.xml")), current="blog")
    for p in posts:
        body = render(tpl["post"], title=esc(p["title"]), date=esc(p["date"]),
                      body=markdown(p["body"]), back=rel(2, "blog/"))
        shell("blog/%s/index.html" % p["slug"], "%s / %s" % (p["title"], site["short"]), p.get("summary", ""), body, current="blog")

    # -- standalone pages
    for slug, title in [("now", "now"), ("uses", "uses"), ("colophon", "colophon")]:
        page = pages[slug]
        body = render(tpl["page"], title=esc(page["title"]), body=markdown(page["body"]),
                      updated=esc(page.get("updated", "")))
        shell("%s/index.html" % slug, "%s / %s" % (title, site["short"]), page.get("summary", ""), body, current=slug)

    art = pages["art"]
    figures = "".join(
        '<figure><a href="%s"><img loading="lazy" src="%s" alt="%s" width="%d" height="%d"></a><figcaption>%s</figcaption></figure>'
        % (rel(1, g["full"]), rel(1, g["src"]), esc(g["caption"]), g["w"], g["h"], inline(g["caption"]))
        for g in art["piece"]
    )
    shell("art/index.html", "art / %s" % site["short"], art.get("summary", ""),
          render(tpl["art"], title=esc(art["title"]), body=markdown(art["body"]), figures=figures), current="art")

    # -- 404, relative paths cannot work here so it links home absolutely
    shell("404.html", "404 / %s" % site["short"], "Nothing here.",
          render(tpl["notfound"], home=site["base"]), depth=0)

    # -- feed
    now = format_datetime(datetime.now(timezone.utc))
    feed_items = "".join(
        "<item><title>%s</title><link>%s</link><guid isPermaLink=\"true\">%s</guid>"
        "<pubDate>%s</pubDate><description>%s</description></item>"
        % (esc(p["title"]), site["url"] + "blog/%s/" % p["slug"], site["url"] + "blog/%s/" % p["slug"],
           format_datetime(datetime.fromisoformat(p["date"]).replace(tzinfo=timezone.utc)),
           esc(p.get("summary", "")))
        for p in posts
    )
    with open(os.path.join(ROOT, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(render(read(os.path.join(TEMPLATES, "feed.xml")), title=esc(site["name"]), url=site["url"],
                       desc=esc(site["description"]), built=now, items=feed_items))

    print("built %d entries, %d posts" % (len(entries), len(posts)))


if __name__ == "__main__":
    main()
