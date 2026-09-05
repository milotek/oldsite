"""A small Markdown subset renderer.

Stdlib only, on purpose: the site has to rebuild from a bare `python3` on any
machine, years from now, without a package index being reachable.
"""

import html
import re

_INLINE_CODE = re.compile(r"`([^`]+)`")
_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<![*\w])\*([^*]+)\*(?!\*)")
_AUTOLINK = re.compile(r"<((?:https?|mailto):[^>\s]+|[^>\s@]+@[^>\s]+)>")


def _inline(text):
    """Escape, then re-open the small set of tags we generate ourselves."""
    slots = []

    def stash(markup):
        slots.append(markup)
        return "\x00%d\x00" % (len(slots) - 1)

    text = _INLINE_CODE.sub(lambda m: stash("<code>%s</code>" % html.escape(m.group(1))), text)
    text = _IMAGE.sub(
        lambda m: stash(
            '<img src="%s" alt="%s"%s loading="lazy" decoding="async">'
            % (
                html.escape(m.group(2), quote=True),
                html.escape(m.group(1), quote=True),
                ' title="%s"' % html.escape(m.group(3), quote=True) if m.group(3) else "",
            )
        ),
        text,
    )
    text = _LINK.sub(
        lambda m: stash(
            '<a href="%s"%s>%s</a>'
            % (
                html.escape(m.group(2), quote=True),
                ' target="_blank" rel="noopener"' if "://" in m.group(2) else "",
                html.escape(m.group(1)),
            )
        ),
        text,
    )
    text = _AUTOLINK.sub(
        lambda m: stash(
            '<a href="%s">%s</a>'
            % (
                html.escape(m.group(1) if "://" in m.group(1) or m.group(1).startswith("mailto:") else "mailto:" + m.group(1), quote=True),
                html.escape(m.group(1).removeprefix("mailto:")),
            )
        ),
        text,
    )
    text = _BOLD.sub(lambda m: stash("<strong>%s</strong>" % html.escape(m.group(1))), text)
    text = _ITALIC.sub(lambda m: stash("<em>%s</em>" % html.escape(m.group(1))), text)

    text = html.escape(text)
    return re.sub(r"\x00(\d+)\x00", lambda m: slots[int(m.group(1))], text)


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", text).lower()).strip("-")


def render(source):
    lines = source.replace("\r\n", "\n").split("\n")
    out = []
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
            cls = ' class="language-%s"' % html.escape(lang, quote=True) if lang else ""
            out.append("<pre><code%s>%s</code></pre>" % (cls, html.escape("\n".join(body))))
            continue

        if re.fullmatch(r"(-{3,}|\*{3,})", stripped):
            out.append("<hr>")
            i += 1
            continue

        heading = re.match(r"(#{1,6})\s+(.*)", stripped)
        if heading:
            level = len(heading.group(1))
            body = _inline(heading.group(2).strip())
            out.append('<h%d id="%s">%s</h%d>' % (level, _slug(body), body, level))
            i += 1
            continue

        if stripped.startswith(">"):
            body = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                body.append(lines[i].strip()[1:].lstrip())
                i += 1
            out.append("<blockquote>%s</blockquote>" % render("\n".join(body)))
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\|[\s:|-]+\|", lines[i + 1].strip()):
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]

            head = cells(lines[i])
            i += 2
            body = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                body.append(cells(lines[i]))
                i += 1
            thead = "".join("<th>%s</th>" % _inline(c) for c in head)
            rows = "".join(
                "<tr>%s</tr>" % "".join("<td>%s</td>" % _inline(c) for c in row) for row in body
            )
            out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (thead, rows))
            continue

        bullet = re.match(r"([-*+]|\d+\.)\s+", stripped)
        if bullet:
            ordered = bullet.group(1)[-1] == "."
            items = []
            while i < len(lines) and re.match(r"\s*([-*+]|\d+\.)\s+", lines[i]):
                items.append(re.sub(r"^\s*([-*+]|\d+\.)\s+", "", lines[i]))
                i += 1
                # A wrapped continuation line belongs to the item above it.
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip():
                    items[-1] += " " + lines[i].strip()
                    i += 1
            tag = "ol" if ordered else "ul"
            out.append(
                "<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % _inline(x) for x in items), tag)
            )
            continue

        if stripped.startswith("<"):
            block = []
            while i < len(lines) and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append("\n".join(block))
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"\s*(#|>|```|[-*+]\s|\d+\.\s|\|)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % _inline(" ".join(para)))

    return "\n".join(out)


def plain(source, limit=280):
    """First paragraph, tags stripped. Used for feed and meta descriptions."""
    text = re.sub(r"<[^>]+>", "", render(source))
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    return text[: limit - 1] + "…" if len(text) > limit else text
