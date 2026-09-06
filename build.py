#!/usr/bin/env python3
"""Render content/ into the repository root. Run with `uv run build.py`."""

from __future__ import annotations

import datetime as dt
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.S)
DATED_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")
# Authors write root-relative links (`/colophon/`, `/static/img/x.webp`) in
# Markdown; the site lives under a subpath, so they are rewritten per page.
ROOT_LINK = re.compile(r'(href|src)="/(?!/)')


def is_external(url: str) -> bool:
    return "://" in url or url.startswith("mailto:")


def load_markdown(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(text)
    meta = yaml.safe_load(match.group(1)) if match else None
    body = text[match.end():] if match else text
    md = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists"])
    return {**(meta or {}), "body": md.convert(body), "source": path}


def load_posts() -> list[dict]:
    posts = []
    for path in sorted((CONTENT / "posts").glob("*.md")):
        post = load_markdown(path)
        if post.get("draft"):
            continue
        dated = DATED_NAME.match(path.stem)
        post.setdefault("date", dt.date.fromisoformat(dated.group(1)) if dated else None)
        post.setdefault("slug", dated.group(2) if dated else path.stem)
        if post["date"] is None:
            raise SystemExit(f"{path}: needs a date in the front matter or the filename")
        post["url"] = f"blog/{post['slug']}/"
        posts.append(post)
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def load_projects() -> list[dict]:
    projects = []
    for path in sorted((CONTENT / "projects").glob("*.md")):
        project = load_markdown(path)
        project.setdefault("slug", path.stem)
        project["url"] = f"projects/{project['slug']}/"
        for key, default in (("tags", []), ("links", []), ("images", []), ("featured", False), ("order", 999)):
            project.setdefault(key, default)
        projects.append(project)
    return sorted(projects, key=lambda p: (p["order"], p["title"].lower()))


def load_pages() -> list[dict]:
    pages = []
    for path in sorted((CONTENT / "pages").glob("*.md")):
        page = load_markdown(path)
        page.setdefault("slug", path.stem)
        page["url"] = f"{page['slug']}/"
        pages.append(page)
    return pages


def main() -> None:
    site = yaml.safe_load((CONTENT / "site.yaml").read_text(encoding="utf-8"))
    site["base_path"] = urlparse(site["url"]).path
    buttons = yaml.safe_load((CONTENT / "buttons.yaml").read_text(encoding="utf-8"))
    art = yaml.safe_load((CONTENT / "art.yaml").read_text(encoding="utf-8"))
    home = load_markdown(CONTENT / "home.md")
    posts, projects, pages = load_posts(), load_projects(), load_pages()

    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["date"] = lambda d: d.strftime("%-d %B %Y")

    for stale in ("blog", "projects", "art", *(p["slug"] for p in pages)):
        shutil.rmtree(ROOT / stale, ignore_errors=True)

    def render(template: str, out: str, **context) -> None:
        depth = out.count("/")
        rel = "../" * depth
        path = out.removesuffix("index.html")
        context.setdefault("body", None)
        if context["body"]:
            context["body"] = Markup(ROOT_LINK.sub(rf'\1="{rel}', context["body"]))

        def link(url: str) -> str:
            return url if is_external(url) else (rel + url.lstrip("/")) or "./"

        html = env.get_template(template).render(
            site=site, rel=rel, path=path, link=link, buttons=buttons,
            posts=posts, projects=projects, pages=pages, year=dt.date.today().year, **context,
        )
        target = ROOT / out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    render("index.html", "index.html", section="home", body=home["body"], featured=[p for p in projects if p["featured"]])
    render("projects.html", "projects/index.html", section="projects", title="Projects")
    for project in projects:
        render("project.html", project["url"] + "index.html", section="projects", title=project["title"],
               description=project.get("summary"), project=project, body=project["body"])
    render("blog.html", "blog/index.html", section="blog", title="Blog")
    for post in posts:
        render("post.html", post["url"] + "index.html", section="blog", title=post["title"],
               description=post.get("summary"), post=post, body=post["body"])
    render("art.html", "art/index.html", section="art", title="Art", art=art)
    for page in pages:
        render("page.html", page["url"] + "index.html", section=page["slug"], title=page["title"],
               description=page.get("summary"), page=page, body=page["body"])
    render("feed.xml", "feed.xml")
    render("404.html", "404.html", title="Not found")
    print(f"built {len(projects)} projects, {len(posts)} posts, {len(pages)} pages")


if __name__ == "__main__":
    main()
