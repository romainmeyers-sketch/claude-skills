#!/usr/bin/env python3
"""Pull every reviewer comment out of a .pptx into readable text.

Two jobs:
  1. Before editing, capture comments so they can be restored if a tool drops
     them. Editing surfaces that rewrite slide XML lose them silently.
  2. After a loss, recover the text from any older copy of the deck, including
     an autosave or a version from File, Info, Version History.

Usage:
    python extract_comments.py deck.pptx
    python extract_comments.py deck.pptx -o comments.md
"""

import argparse
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "p188": "http://schemas.microsoft.com/office/powerpoint/2018/8/main",
    "p223": "http://schemas.microsoft.com/office/powerpoint/2022/3/main",
}


def text_of(node):
    """All text in an element, in document order."""
    parts = [t.text or "" for t in node.iter() if t.tag.endswith("}t")]
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def authors(zf):
    """id -> display name, from either the modern or the legacy author list."""
    out = {}
    for part in ("ppt/authors.xml", "ppt/commentAuthors.xml"):
        try:
            root = ET.fromstring(zf.read(part))
        except Exception:
            continue
        for node in root.iter():
            if not node.tag.endswith("}author") and not node.tag.endswith("}cmAuthor"):
                continue
            aid = node.get("id") or node.get("{%s}id" % NS["p188"])
            name = node.get("name") or node.get("initials") or ""
            if aid:
                out[str(aid)] = name
    return out


def slide_for_part(zf, part):
    """Which slide a comment part belongs to, via the slide rels."""
    target = os.path.basename(part)
    for rel in zf.namelist():
        if not re.match(r"ppt/slides/_rels/slide\d+\.xml\.rels$", rel):
            continue
        try:
            body = zf.read(rel).decode("utf-8", "replace")
        except Exception:
            continue
        if target in body:
            m = re.search(r"slide(\d+)\.xml\.rels$", rel)
            if m:
                return int(m.group(1))
    return None


def extract(path):
    zf = zipfile.ZipFile(path)
    who = authors(zf)
    rows = []

    parts = [n for n in zf.namelist()
             if n.startswith("ppt/comments/") and n.endswith(".xml")]
    for part in sorted(parts):
        slide = slide_for_part(zf, part)
        try:
            root = ET.fromstring(zf.read(part))
        except Exception:
            continue
        for cm in root.iter():
            if not cm.tag.endswith("}cm"):
                continue
            aid = str(cm.get("authorId") or cm.get("idx") or "")
            rows.append({
                "slide": slide,
                "author": who.get(aid, aid or "unknown"),
                "created": cm.get("created") or cm.get("dt") or "",
                "text": text_of(cm),
                "part": part,
            })
    zf.close()
    rows.sort(key=lambda r: (r["slide"] or 999, r["created"]))
    return rows


def render(path, rows):
    out = ["# Comments in %s" % os.path.basename(path), ""]
    if not rows:
        out.append("No comments found in this file.")
        return "\n".join(out)
    out.append("%d comment%s. Keep this file until the deck is final." % (
        len(rows), "" if len(rows) == 1 else "s"))
    out.append("")
    current = object()
    for r in rows:
        if r["slide"] != current:
            current = r["slide"]
            out.append("")
            out.append("## Slide %s" % (current if current else "unattached"))
        stamp = (" (%s)" % r["created"][:10]) if r["created"] else ""
        out.append("- **%s**%s: %s" % (r["author"], stamp, r["text"] or "(empty)"))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path")
    ap.add_argument("-o", "--out", help="write markdown here")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        sys.exit("no such file: %s" % args.path)

    rows = extract(args.path)
    text = render(args.path, rows)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print("%d comment(s) -> %s" % (len(rows), args.out))
    else:
        print(text)


if __name__ == "__main__":
    main()
