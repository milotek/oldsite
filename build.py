#!/usr/bin/env python3
"""Generate the site from content/ into the repository root.

Standard library only. Run `python3 build.py` and commit what changes.
"""

from __future__ import annotations

import html
import re
import shutil
import sys
import tomllib
from dataclasses import dataclass
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
OUT = ROOT

# Anything the generator owns. Removed before every build so a renamed page
# cannot leave a stale copy of itself behind.
MANAGED = ["assets", "projects", "blog", "art", "now", "uses", "colophon"]
MANAGED_FILES = ["index.html", "404.html", "feed.xml"]


# --------------------------------------------------------------------------
# markdown
# --------------------------------------------------------------------------

_CODE_SPAN = re.compile(r"`([^`]+)`")
_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_EM = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")


def inline(text: str, rel: str = "") -> str:
    """Render inline markdown. Code spans are pulled out first so their
    contents cannot be re-parsed as emphasis or links."""
    spans: list[str] = []

    def stash(m: re.Match[str]) -> str:
        spans.append(html.escape(m.group(1)))
        return f"\x00{len(spans) - 1}\x00"

    text = _CODE_SPAN.sub(stash, text)
    text = html.escape(text, quote=False)

    def image(m: re.Match[str]) -> str:
        src, alt, title = m.group(2), m.group(1), m.group(3)
        if not src.startswith(("http", "/", ".")):
            src = rel + "assets/" + src
        cap = f' title="{html.escape(title, quote=True)}"' if title else ""
        return f'<img src="{src}" alt="{html.escape(alt, quote=True)}" loading="lazy"{cap}>'

    def link(m: re.Match[str]) -> str:
        label, url = m.group(1), m.group(2)
        extra = ' rel="noopener"' if url.startswith("http") else ""
        return f'<a href="{url}"{extra}>{label}</a>'

    text = _IMAGE.sub(image, text)
    text = _LINK.sub(link, text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _EM.sub(r"<em>\1</em>", text)
    for i, span in enumerate(spans):
        text = text.replace(f"\x00{i}\x00", f"<code>{span}</code>")
    return text


def markdown(text: str, rel: str = "") -> str:
    """A deliberately small Markdown subset: headings, paragraphs, lists,
    blockquotes, fenced code, rules, and raw HTML lines."""
    out: list[str] = []
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            i += 1
            block: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(block)) + "</code></pre>")
            continue

        if stripped in ("---", "***", "___"):
            out.append('<hr class="rule-mark">')
            i += 1
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            body = stripped[level:].strip()
            level = min(max(level, 2), 4)
            out.append(f"<h{level}>{inline(body, rel)}</h{level}>")
            i += 1
            continue

        if stripped.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>" + markdown("\n".join(block), rel) + "</blockquote>")
            continue

        if re.match(r"^[-*] ", stripped) or re.match(r"^\d+\. ", stripped):
            ordered = bool(re.match(r"^\d+\. ", stripped))
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while i < len(lines):
                cur = lines[i].strip()
                if re.match(r"^[-*] ", cur) or re.match(r"^\d+\. ", cur):
                    items.append(re.sub(r"^([-*]|\d+\.) ", "", cur))
                    i += 1
                elif cur and lines[i].startswith(("  ", "\t")) and items:
                    items[-1] += " " + cur
                    i += 1
                else:
                    break
            body = "".join(f"<li>{inline(x, rel)}</li>" for x in items)
            out.append(f"<{tag}>{body}</{tag}>")
            continue

        if stripped.startswith("<"):
            block = []
            while i < len(lines) and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append("\n".join(block))
            continue

        para: list[str] = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(
            ("#", ">", "```", "<")
        ) and not re.match(r"^([-*] |\d+\. )", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para), rel)}</p>")

    return "\n".join(out)


# --------------------------------------------------------------------------
# content loading
# --------------------------------------------------------------------------


@dataclass
class Doc:
    meta: dict
    body: str


def read_frontmatter(path: Path) -> Doc:
    """Markdown with flat YAML frontmatter, which is what Obsidian writes.
    Values are strings, dates, or inline `[a, b]` lists."""
    raw = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = raw
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            head = raw[3:end]
            body = raw[end + 4 :]
            for line in head.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or ":" not in line:
                    continue
                key, _, value = line.partition(":")
                meta[key.strip()] = _scalar(value.strip())
    return Doc(meta=meta, body=body.strip())


def _scalar(value: str):
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_scalar(v.strip()) for v in inner.split(",")]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return date.fromisoformat(value)
    if value in ("true", "false"):
        return value == "true"
    return value


def load_toml(name: str) -> dict:
    with (CONTENT / name).open("rb") as fh:
        return tomllib.load(fh)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def rel_for(depth: int) -> str:
    return "../" * depth if depth else ""


def esc(value) -> str:
    return html.escape(str(value), quote=True)


@dataclass
class Sheet:
    code: str
    label: str
    path: str
    depth: int = 0


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------


def plate_head(code: str, title: str, right: str = "") -> str:
    tail = f'<span class="ph-right">{esc(right)}</span>' if right else ""
    return (
        '<div class="plate-head">'
        f'<span class="ph-code">{esc(code)}</span>'
        f'<h2 class="ph-title">{esc(title)}</h2>'
        '<span class="ph-line" aria-hidden="true"></span>'
        f"{tail}</div>"
    )


def nav_html(sheets: list[Sheet], current: str, rel: str) -> str:
    items = []
    for sheet in sheets:
        active = " aria-current=\"page\"" if sheet.path == current else ""
        cls = " nav-on" if sheet.path == current else ""
        items.append(
            f'<a class="nav-item{cls}" href="{rel}{sheet.path}"{active}>'
            f'<span class="nav-code">{esc(sheet.code)}</span>'
            f'<span class="nav-label">{esc(sheet.label)}</span></a>'
        )
    return '<nav class="sheet-nav" aria-label="Sheets">' + "".join(items) + "</nav>"


def title_block(site: dict, sheet_code: str, total: int, page_title: str, rel: str, built: date) -> str:
    cells = [
        ("Drawn by", site["name"]),
        ("Role", f'{site["role"]}, {site["employer"]}'),
        ("Location", site["location"]),
        ("Contact", site["email"]),
        ("Title", page_title),
        ("Sheet", f'{sheet_code} of {total - 1:02d}'),
        ("Scale", "1:1"),
        ("Rev", f'{site["revision"]} · {built.isoformat()}'),
    ]
    body = "".join(
        f'<div class="tb-cell"><b>{esc(k)}</b><span>{esc(v)}</span></div>' for k, v in cells
    )
    stamp = (
        '<div class="tb-cell tb-stamp">'
        f'<img src="{rel}assets/{site["avatar"]}" alt="" width="56" height="56">'
        "<b>Approved</b></div>"
    )
    return f'<div class="titleblock">{stamp}{body}</div>'


def links_row(site: dict, rel: str) -> str:
    items = []
    for link in site["links"]:
        note = f'<span class="lk-note">{esc(link["note"])}</span>' if link.get("note") else ""
        items.append(
            f'<a class="lk" href="{esc(link["url"])}" rel="noopener me">'
            f'<span class="lk-label">{esc(link["label"])}</span>{note}</a>'
        )
    return '<div class="links-row">' + "".join(items) + "</div>"


def page(
    *,
    site: dict,
    sheets: list[Sheet],
    sheet: Sheet,
    title: str,
    description: str,
    main: str,
    built: date,
    canonical_path: str,
) -> str:
    rel = rel_for(sheet.depth)
    full_title = title if title == site["title"] else f'{title} · {site["title"]}'
    url = site["url"].rstrip("/") + "/" + canonical_path
    head_links = "".join(
        f'<link rel="preload" href="{rel}assets/fonts/{f}" as="font" '
        f'type="font/woff2" crossorigin>'
        for f in ("meslo-regular.woff2", "sourcesans-regular.woff2")
    )
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#11111b">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{esc(url)}">
<link rel="icon" href="{rel}assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{rel}assets/img/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="{esc(site['title'])}" href="{rel}feed.xml">
{head_links}<link rel="stylesheet" href="{rel}assets/site.css">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="{esc(site['url'].rstrip('/'))}/assets/img/apple-touch-icon.png">
<meta name="twitter:card" content="summary">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="sheet">
<header class="sheet-head">
<div class="ruler" aria-hidden="true"></div>
<div class="head-row">
<a class="wordmark" href="{rel}">{esc(site["title"])}</a>
<p class="sheet-id">Sheet {esc(sheet.code)} <span aria-hidden="true">·</span> Rev {esc(site["revision"])}</p>
</div>
{nav_html(sheets, sheet.path, rel)}
</header>
<main id="main">
{main}
</main>
<footer class="sheet-foot">
{links_row(site, rel)}
{title_block(site, sheet.code, len(sheets), title, rel, built)}
<p class="foot-note">Drawn in London. Source at <a href="https://github.com/milotek" rel="noopener">github.com/milotek</a>. <a href="{rel}feed.xml">RSS</a>.</p>
</footer>
</div>
</body>
</html>
"""


# --------------------------------------------------------------------------
# sections
# --------------------------------------------------------------------------


def project_part(index: int) -> str:
    return f"PT-{index:02d}"


def project_card(project: dict, index: int, rel: str) -> str:
    images = project.get("images", [])
    if images:
        first = images[0]
        shape = first.get("shape", "wide")
        thumb = (
            f'<div class="card-shot shot-{esc(shape)}">'
            f'<img src="{rel}assets/{esc(first["src"])}" alt="{esc(first["alt"])}" loading="lazy" decoding="async">'
            "</div>"
        )
    else:
        # Keeps the row grid honest when a project has nothing to photograph.
        thumb = f'<div class="card-shot card-shot-empty"><span>{project_part(index)}</span></div>'
    org = f' <span class="sep">·</span> {esc(project["org"])}' if project.get("org") else ""
    spec = (
        f'<p class="card-spec">{esc(project["kind"])}{org} '
        f'<span class="sep">·</span> {esc(project["years"])} '
        f'<span class="sep">·</span> {esc(project["status"])}</p>'
    )
    stack_html = "".join(f"<li>{esc(s)}</li>" for s in project.get("stack", []))
    return (
        f'<a class="card" href="{rel}projects/{esc(project["slug"])}/">'
        f'{thumb}'
        '<div class="card-body">'
        "<div class=\"card-main\">"
        f'<span class="part">{project_part(index)}</span>'
        f'<h3 class="card-title">{esc(project["title"])}</h3>'
        f'{spec}'
        f'<p class="card-summary">{esc(project["summary"])}</p>'
        "</div>"
        '<div class="card-meta">'
        f'<ul class="card-stack">{stack_html}</ul>'
        '<span class="card-more">Open sheet</span>'
        "</div></div></a>"
    )


def gallery(images: list[dict], rel: str) -> str:
    if not images:
        return ""
    cells = []
    for image in images:
        shape = image.get("shape", "wide")
        caption = image.get("caption", "")
        cap = f'<figcaption>{esc(caption)}</figcaption>' if caption else ""
        cells.append(
            f'<figure class="fig fig-{esc(shape)}">'
            f'<a href="{rel}assets/{esc(image["src"])}">'
            f'<img src="{rel}assets/{esc(image["src"])}" alt="{esc(image["alt"])}" loading="lazy" decoding="async">'
            f"</a>{cap}</figure>"
        )
    return '<div class="figs">' + "".join(cells) + "</div>"


def buttons_block(buttons: dict, rel: str) -> str:
    cells = []
    for button in buttons.get("mine", []):
        img = (
            f'<img src="{rel}assets/{esc(button["src"])}" alt="{esc(button["alt"])}" '
            f'width="88" height="31" loading="lazy">'
        )
        title = esc(button.get("title", button["alt"]))
        if button.get("url"):
            cells.append(f'<a class="btn88" href="{esc(button["url"])}" rel="noopener" title="{title}">{img}</a>')
        else:
            cells.append(f'<span class="btn88" title="{title}">{img}</span>')
    for _ in range(int(buttons.get("vacant", 0))):
        cells.append('<span class="btn88 btn88-vacant" aria-hidden="true">vacant</span>')
    note = f'<p class="legend-note">{esc(buttons.get("mine_note", ""))}</p>' if buttons.get("mine_note") else ""
    return f'<div class="legend">{note}<div class="btn88-row">' + "".join(cells) + "</div></div>"


def post_row(post: Doc, rel: str) -> str:
    meta = post.meta
    when = meta["date"]
    return (
        f'<a class="row" href="{rel}blog/{esc(meta["slug"])}/">'
        f'<span class="row-date">{when.isoformat()}</span>'
        f'<span class="row-main"><span class="row-title">{esc(meta["title"])}</span>'
        f'<span class="row-summary">{esc(meta.get("summary", ""))}</span></span>'
        "</a>"
    )


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build() -> None:
    built = date.today()
    site = load_toml("site.toml")
    work = load_toml("work.toml")
    projects = load_toml("projects.toml")["project"]
    art = load_toml("art.toml")
    buttons = load_toml("buttons.toml")

    sheets = [Sheet(code=s["code"], label=s["label"], path=s["path"]) for s in site["sheets"]]
    by_path = {s.path: s for s in sheets}
    for sheet in sheets:
        sheet.depth = sheet.path.count("/")

    posts = sorted(
        (read_frontmatter(p) for p in (CONTENT / "posts").glob("*.md")),
        key=lambda d: d.meta["date"],
        reverse=True,
    )
    pages = {p.stem: read_frontmatter(p) for p in (CONTENT / "pages").glob("*.md")}

    for name in MANAGED:
        shutil.rmtree(OUT / name, ignore_errors=True)
    for name in MANAGED_FILES:
        (OUT / name).unlink(missing_ok=True)

    shutil.copytree(STATIC, OUT / "assets")

    def render(sheet: Sheet, *, title, description, main, canonical, depth=None):
        target = Sheet(sheet.code, sheet.label, sheet.path, depth if depth is not None else sheet.depth)
        return page(
            site=site,
            sheets=sheets,
            sheet=target,
            title=title,
            description=description,
            main=main,
            built=built,
            canonical_path=canonical,
        )

    # ---- index ----------------------------------------------------------
    rel = ""
    intro = pages["index"]
    role = work["role"][0]
    highlights = "".join(f"<li>{esc(h)}</li>" for h in role.get("highlights", []))
    featured = [(i, p) for i, p in enumerate(projects, start=1) if p.get("featured")]

    hero_specs = [
        ("Name", site["name"]),
        ("Post", f'{site["role"]}, {site["employer"]}'),
        ("Station", site["location"]),
        ("Status", "Open to interesting problems"),
    ]
    specs = "".join(
        f'<div class="spec"><b>{esc(k)}</b><span>{esc(v)}</span></div>' for k, v in hero_specs
    )

    main = f"""
<section class="hero">
<div class="hero-text">
<p class="hero-kicker">{esc(site["name"])} <span aria-hidden="true">·</span> {esc(site["location"])}</p>
<h1 class="hero-title">{esc(site["title"])}</h1>
<div class="hero-body">{markdown(intro.body, rel)}</div>
</div>
<figure class="portrait">
<img src="assets/img/avatar_large.webp" alt="Milo's avatar: a cartoon figure with cat ears holding a mug." width="220" height="220">
<figcaption>Fig. 1 <span aria-hidden="true">·</span> not to scale</figcaption>
</figure>
<div class="specs">{specs}</div>
</section>

<section class="block">
{plate_head("A", "Current work")}
<article class="worksheet">
<div class="work-main">
<h3 class="work-title">{esc(role["title"])} <span class="at">at</span> {esc(role["org"])}</h3>
<p class="card-spec">{esc(role["team"])} <span class="sep">·</span> {esc(role["location"])} <span class="sep">·</span> {esc(role["years"])}</p>
<div class="work-body">{markdown(role["summary"], rel)}</div>
<ul class="ticks">{highlights}</ul>
</div>
</article>
</section>

<section class="block">
{plate_head("B", "Selected projects", f"{len(projects)} total")}
<div class="cards">{"".join(project_card(p, i, rel) for i, p in featured)}</div>
<p class="more"><a href="projects/">Every project on sheet 01</a></p>
</section>

<section class="block">
{plate_head("C", "Notes")}
<div class="rows">{"".join(post_row(p, rel) for p in posts[:3])}</div>
<p class="more"><a href="blog/">All notes, and the feed</a></p>
</section>

<section class="block">
{plate_head("D", "Legend")}
{buttons_block(buttons, rel)}
</section>
"""
    write(OUT / "index.html", render(by_path[""], title=site["title"], description=site["description"], main=main, canonical=""))

    # ---- projects index -------------------------------------------------
    sheet = by_path["projects/"]
    rel = rel_for(sheet.depth)
    cards = "".join(project_card(p, i, rel) for i, p in enumerate(projects, start=1))
    main = f"""
<section class="page-head">
<p class="hero-kicker">Sheet {esc(sheet.code)}</p>
<h1 class="hero-title">Projects</h1>
<p class="page-lede">Things I have actually finished, or am actually still working on. Ordered by how much of me is in them.</p>
</section>
<section class="block">
{plate_head("A", "Parts list", f"{len(projects)} items")}
<div class="cards">{cards}</div>
</section>
"""
    write(
        OUT / "projects" / "index.html",
        render(sheet, title="Projects", description="Projects by Milo Tekchandani: apps, game engines, shaders, hardware and system configuration.", main=main, canonical="projects/"),
    )

    # ---- project sheets -------------------------------------------------
    for index, project in enumerate(projects, start=1):
        depth = 2
        rel = rel_for(depth)
        links = "".join(
            f'<a class="lk" href="{esc(l["url"])}" rel="noopener"><span class="lk-label">{esc(l["label"])}</span>'
            + (f'<span class="lk-note">{esc(l["note"])}</span>' if l.get("note") else "")
            + "</a>"
            for l in project.get("links", [])
        )
        links_html = f'<div class="links-row">{links}</div>' if links else ""
        stack = "".join(f'<li>{esc(s)}</li>' for s in project.get("stack", []))
        facts = [
            ("Part", project_part(index)),
            ("Medium", project["kind"]),
            ("Dates", project["years"]),
            ("Status", project["status"]),
        ]
        if project.get("org"):
            facts.append(("Studio", project["org"]))
        facts_html = "".join(
            f'<div class="spec"><b>{esc(k)}</b><span>{esc(v)}</span></div>' for k, v in facts
        )
        main = f"""
<section class="page-head">
<p class="hero-kicker"><a href="{rel}projects/">Projects</a> <span aria-hidden="true">/</span> {esc(project_part(index))}</p>
<h1 class="hero-title">{esc(project["title"])}</h1>
<p class="page-lede">{esc(project["summary"])}</p>
<div class="specs">{facts_html}</div>
{links_html}
</section>
<section class="block">
{plate_head("A", "Notes")}
<div class="prose">{markdown(project["body"], rel)}</div>
<ul class="chips">{stack}</ul>
</section>
{f'<section class="block">{plate_head("B", "Plates")}{gallery(project.get("images", []), rel)}</section>' if project.get("images") else ""}
<p class="more"><a href="{rel}projects/">Back to the parts list</a></p>
"""
        write(
            OUT / "projects" / project["slug"] / "index.html",
            render(
                by_path["projects/"],
                title=project["title"],
                description=project["summary"],
                main=main,
                canonical=f'projects/{project["slug"]}/',
                depth=depth,
            ),
        )

    # ---- art ------------------------------------------------------------
    sheet = by_path["art/"]
    rel = rel_for(sheet.depth)
    cells = []
    for piece in art["piece"]:
        thumb = piece["src"].replace("img/art/", "img/art/thumb/")
        cells.append(
            '<figure class="art">'
            f'<a href="{rel}assets/{esc(piece["src"])}">'
            f'<img src="{rel}assets/{esc(thumb)}" alt="{esc(piece["alt"])}" loading="lazy" decoding="async" width="520" height="520">'
            "</a>"
            "<figcaption>"
            f'<span class="art-title">{esc(piece["title"])}</span>'
            f'<span class="art-year">{esc(piece["year"])}</span>'
            f'<span class="art-caption">{esc(piece["caption"])}</span>'
            "</figcaption></figure>"
        )
    main = f"""
<section class="page-head">
<p class="hero-kicker">Sheet {esc(sheet.code)}</p>
<h1 class="hero-title">Art</h1>
<div class="page-lede">{markdown(art["intro"], rel)}</div>
</section>
<section class="block">
{plate_head("A", "Plates", f'{len(art["piece"])} items')}
<div class="art-grid">{"".join(cells)}</div>
</section>
"""
    write(
        OUT / "art" / "index.html",
        render(sheet, title="Art", description="Drawings and concept art by Milo Tekchandani, mostly Procreate.", main=main, canonical="art/"),
    )

    # ---- blog index -----------------------------------------------------
    sheet = by_path["blog/"]
    rel = rel_for(sheet.depth)
    main = f"""
<section class="page-head">
<p class="hero-kicker">Sheet {esc(sheet.code)}</p>
<h1 class="hero-title">Notes</h1>
<p class="page-lede">Occasional. There is an <a href="{rel}feed.xml">RSS feed</a> if you want to know when that changes.</p>
</section>
<section class="block">
{plate_head("A", "Entries", f"{len(posts)} total")}
<div class="rows">{"".join(post_row(p, rel) for p in posts)}</div>
</section>
"""
    write(
        OUT / "blog" / "index.html",
        render(sheet, title="Notes", description="Writing by Milo Tekchandani.", main=main, canonical="blog/"),
    )

    # ---- posts ----------------------------------------------------------
    for post in posts:
        depth = 2
        rel = rel_for(depth)
        meta = post.meta
        tags = "".join(f"<li>{esc(t)}</li>" for t in meta.get("tags", []))
        main = f"""
<article class="post">
<section class="page-head">
<p class="hero-kicker"><a href="{rel}blog/">Notes</a> <span aria-hidden="true">/</span> <time datetime="{meta["date"].isoformat()}">{meta["date"].isoformat()}</time></p>
<h1 class="hero-title">{esc(meta["title"])}</h1>
<p class="page-lede">{esc(meta.get("summary", ""))}</p>
</section>
<div class="prose">{markdown(post.body, rel)}</div>
<ul class="chips">{tags}</ul>
</article>
<p class="more"><a href="{rel}blog/">Back to notes</a></p>
"""
        write(
            OUT / "blog" / meta["slug"] / "index.html",
            render(
                by_path["blog/"],
                title=meta["title"],
                description=meta.get("summary", site["description"]),
                main=main,
                canonical=f'blog/{meta["slug"]}/',
                depth=depth,
            ),
        )

    # ---- standalone pages ----------------------------------------------
    for stem in ("now", "uses", "colophon"):
        doc = pages[stem]
        sheet = by_path[f"{stem}/"]
        rel = rel_for(sheet.depth)
        updated = doc.meta.get("updated")
        stamp = (
            f'<p class="hero-kicker">Sheet {esc(sheet.code)} <span aria-hidden="true">·</span> '
            f'updated <time datetime="{updated.isoformat()}">{updated.isoformat()}</time></p>'
            if isinstance(updated, date)
            else f'<p class="hero-kicker">Sheet {esc(sheet.code)}</p>'
        )
        main = f"""
<section class="page-head">
{stamp}
<h1 class="hero-title">{esc(doc.meta["title"])}</h1>
</section>
<section class="block">
<div class="prose">{markdown(doc.body, rel)}</div>
</section>
"""
        write(
            OUT / stem / "index.html",
            render(sheet, title=doc.meta["title"], description=doc.meta.get("description", site["description"]), main=main, canonical=f"{stem}/"),
        )

    # ---- feed -----------------------------------------------------------
    base = site["url"].rstrip("/")
    items = []
    for post in posts:
        meta = post.meta
        when = datetime.combine(meta["date"], datetime.min.time(), tzinfo=timezone.utc)
        link = f'{base}/blog/{meta["slug"]}/'
        items.append(
            "<item>"
            f"<title>{esc(meta['title'])}</title>"
            f"<link>{esc(link)}</link>"
            f'<guid isPermaLink="true">{esc(link)}</guid>'
            f"<pubDate>{format_datetime(when)}</pubDate>"
            f"<description>{esc(meta.get('summary', ''))}</description>"
            "</item>"
        )
    feed = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>{esc(site["title"])}</title>
<link>{esc(base)}/</link>
<atom:link href="{esc(base)}/feed.xml" rel="self" type="application/rss+xml"/>
<description>{esc(site["description"])}</description>
<language>en-GB</language>
<lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>
{"".join(items)}
</channel>
</rss>
"""
    write(OUT / "feed.xml", feed)

    # ---- 404 ------------------------------------------------------------
    # Served for any missing path under the site root, so its links have to be
    # absolute rather than relative to wherever the miss happened.
    root = "/" + site["url"].rstrip("/").split("/", 3)[-1].strip("/")
    root = (root.rstrip("/") + "/") if root != "/" else "/"
    nav = "".join(
        f'<a class="nav-item" href="{root}{s.path}"><span class="nav-code">{esc(s.code)}</span>'
        f'<span class="nav-label">{esc(s.label)}</span></a>'
        for s in sheets
    )
    write(
        OUT / "404.html",
        f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sheet not found · {esc(site["title"])}</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#11111b">
<link rel="icon" href="{root}assets/img/favicon.png" type="image/png">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
<div class="sheet">
<header class="sheet-head">
<div class="ruler" aria-hidden="true"></div>
<div class="head-row">
<a class="wordmark" href="{root}">{esc(site["title"])}</a>
<p class="sheet-id">Sheet 404 <span aria-hidden="true">·</span> Rev {esc(site["revision"])}</p>
</div>
<nav class="sheet-nav" aria-label="Sheets">{nav}</nav>
</header>
<main id="main">
<section class="page-head">
<p class="hero-kicker">Error 404</p>
<h1 class="hero-title">This sheet was never drawn</h1>
<p class="page-lede">Nothing lives at that address. The sheet index above will get you somewhere real.</p>
</section>
</main>
<footer class="sheet-foot">
<p class="foot-note">Drawn in London. Source at <a href="https://github.com/milotek" rel="noopener">github.com/milotek</a>.</p>
</footer>
</div>
</body>
</html>
""",
    )

    (OUT / ".nojekyll").touch()

    count = sum(1 for _ in OUT.rglob("*.html"))
    print(f"built {count} pages, {len(projects)} projects, {len(posts)} posts")


if __name__ == "__main__":
    try:
        build()
    except Exception as exc:  # surfaced plainly; this only ever runs by hand
        print(f"build failed: {exc}", file=sys.stderr)
        raise
