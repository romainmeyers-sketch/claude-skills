#!/usr/bin/env python3
"""Snapshot the structure of a presentation so changes can be proved.

Works on .pptx files and on .html decks or artifacts. Emits one JSON shape for
both, so compare.py can diff either without caring which it got.

Usage:
    python inventory.py deck.pptx -o before.json --print
    python inventory.py deck.pptx --find "E2E"
    python inventory.py deck.html -o before.json

Output schema:
    {
      "file": str, "kind": "pptx"|"html", "unit_label": "slide"|"section",
      "tokens": {...},                     # html only: :root custom properties
      "units": [
        {"index": 1, "id": str, "name": str, "layout": str, "digest": str,
         "notes_digest": str,
         "elements": [
            {"key": str, "name": str, "type": str, "ph": str|null,
             "pos": [left, top, width, height],   # inches, 3dp
             "text": str, "text_digest": str,
             "font": {"sizes": [...], "bold": [...], "colors": [...]},
             "fill": str|null, "extra": {...}, "digest": str}
         ]}
      ]
    }
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from html.parser import HTMLParser

EMU_PER_INCH = 914400


def digest(*parts):
    h = hashlib.sha1()
    for p in parts:
        h.update(repr(p).encode("utf-8", "replace"))
    return h.hexdigest()[:12]


def inches(v):
    if v is None:
        return None
    return round(v / EMU_PER_INCH, 3)


def norm_text(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


# --------------------------------------------------------------------------
# pptx
# --------------------------------------------------------------------------

def shape_font(shape):
    sizes, bolds, colors = set(), set(), set()
    if not getattr(shape, "has_text_frame", False):
        return {"sizes": [], "bold": [], "colors": []}
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            f = run.font
            try:
                if f.size is not None:
                    sizes.add(round(f.size.pt, 1))
            except Exception:
                pass
            try:
                if f.bold is not None:
                    bolds.add(bool(f.bold))
            except Exception:
                pass
            try:
                if f.color is not None and f.color.type is not None:
                    rgb = getattr(f.color, "rgb", None)
                    if rgb is not None:
                        colors.add(str(rgb))
            except Exception:
                pass
    return {
        "sizes": sorted(sizes),
        "bold": sorted(bolds),
        "colors": sorted(colors),
    }


def shape_fill(shape):
    try:
        fill = shape.fill
        if fill.type is None:
            return None
        if fill.type == 1:  # MSO_FILL.SOLID
            try:
                return str(fill.fore_color.rgb)
            except Exception:
                try:
                    return "theme:%s" % fill.fore_color.theme_color
                except Exception:
                    return "solid"
        if fill.type == 5:
            return "none"
        return "type:%s" % fill.type
    except Exception:
        return None


BULLET_RE = re.compile(r"^\s*[•▪◦·‣⁃*+-]\s+")


def typed_bullets(shape):
    """Paragraphs that start with a bullet character typed into the text.

    A real PowerPoint bullet lives in the paragraph's list formatting, not in
    the text. A typed one has no hanging indent, cannot be demoted with Tab,
    and ignores the template.
    """
    if not getattr(shape, "has_text_frame", False):
        return 0
    hits = 0
    for para in shape.text_frame.paragraphs:
        if BULLET_RE.match(para.text or ""):
            hits += 1
    return hits


def shape_extra(shape):
    extra = {}
    n = typed_bullets(shape)
    if n:
        extra["typed_bullets"] = n
    try:
        if getattr(shape, "has_table", False):
            tbl = shape.table
            extra["table"] = [len(tbl.rows), len(tbl.columns)]
            extra["cells"] = [
                norm_text(c.text) for r in tbl.rows for c in r.cells
            ]
    except Exception:
        pass
    try:
        if getattr(shape, "has_chart", False):
            ch = shape.chart
            extra["chart"] = str(ch.chart_type)
            extra["series"] = len(ch.plots[0].series) if ch.plots else 0
            try:
                extra["categories"] = [str(c) for c in ch.plots[0].categories]
            except Exception:
                pass
    except Exception:
        pass
    try:
        if shape.shape_type is not None and "PICTURE" in str(shape.shape_type):
            extra["image"] = getattr(shape, "name", "")
    except Exception:
        pass
    try:
        if shape.rotation:
            extra["rotation"] = round(shape.rotation, 1)
    except Exception:
        pass
    return extra


def walk_shapes(shapes, out, prefix=""):
    for shape in shapes:
        try:
            stype = str(shape.shape_type)
        except Exception:
            stype = "UNKNOWN"

        ph = None
        try:
            if shape.is_placeholder:
                ph = "%s/%s" % (
                    shape.placeholder_format.idx,
                    shape.placeholder_format.type,
                )
        except Exception:
            pass

        text = ""
        if getattr(shape, "has_text_frame", False):
            text = norm_text(shape.text_frame.text)

        pos = [
            inches(getattr(shape, "left", None)),
            inches(getattr(shape, "top", None)),
            inches(getattr(shape, "width", None)),
            inches(getattr(shape, "height", None)),
        ]
        font = shape_font(shape)
        fill = shape_fill(shape)
        extra = shape_extra(shape)

        el = {
            "key": "%s%s" % (prefix, shape.shape_id),
            "name": shape.name,
            "type": stype,
            "ph": ph,
            "pos": pos,
            "text": text,
            "text_digest": digest(text),
            "font": font,
            "fill": fill,
            "extra": extra,
        }
        el["digest"] = digest(el["name"], stype, ph, pos, text, font, fill, extra)
        out.append(el)

        if "GROUP" in stype:
            try:
                walk_shapes(shape.shapes, out, prefix=el["key"] + ".")
            except Exception:
                pass


def pptx_comments(path):
    """Map reviewer comments to slides by reading the package directly.

    Comments live in their own parts (ppt/comments/*.xml) and python-pptx does
    not surface them, so an editing pass can drop them and nothing notices.
    That has happened in real use, which is why this is tracked.
    """
    import zipfile

    result = {"total": 0, "by_slide": {}, "digest": digest("")}
    try:
        zf = zipfile.ZipFile(path)
    except Exception:
        return result

    names = zf.namelist()
    parts = [n for n in names if n.startswith("ppt/comments/")
             and n.endswith(".xml")]
    result["total"] = len(parts)

    bodies = []
    for part in sorted(parts):
        try:
            bodies.append(zf.read(part).decode("utf-8", "replace"))
        except Exception:
            pass
    result["digest"] = digest(bodies)

    # attach each comment part to its slide through the slide rels
    for rel in [n for n in names if re.match(
            r"ppt/slides/_rels/slide\d+\.xml\.rels$", n)]:
        try:
            body = zf.read(rel).decode("utf-8", "replace")
        except Exception:
            continue
        targets = re.findall(r'Target="([^"]*comments/[^"]+)"', body)
        if not targets:
            continue
        m = re.search(r"slide(\d+)\.xml\.rels$", rel)
        if m:
            result["by_slide"][m.group(1)] = len(targets)

    zf.close()
    return result


def inventory_pptx(path):
    try:
        from pptx import Presentation
    except ImportError:
        sys.exit("python-pptx is not installed for this interpreter.")

    comments = pptx_comments(path)

    prs = Presentation(path)
    units = []
    for i, slide in enumerate(prs.slides, start=1):
        elements = []
        walk_shapes(slide.shapes, elements)

        try:
            layout = slide.slide_layout.name
        except Exception:
            layout = ""

        title = ""
        for el in elements:
            if el["ph"] and "TITLE" in str(el["ph"]) and el["text"]:
                title = el["text"]
                break
        if not title and elements:
            title = elements[0]["text"]

        notes = ""
        try:
            if slide.has_notes_slide:
                notes = norm_text(slide.notes_slide.notes_text_frame.text)
        except Exception:
            pass

        all_text = norm_text(" ".join(e["text"] for e in elements if e["text"]))
        units.append({
            "index": i,
            "id": "slide%d" % i,
            "name": title[:90],
            "layout": layout,
            "notes_digest": digest(notes),
            "comments": comments["by_slide"].get(str(i), 0),
            "text_digest": digest(all_text),
            "text_len": len(all_text),
            "digest": digest([e["digest"] for e in elements], layout),
            "elements": elements,
        })

    return {
        "file": os.path.abspath(path),
        "kind": "pptx",
        "unit_label": "slide",
        "generated": datetime.now().isoformat(timespec="seconds"),
        "slide_size": [
            inches(prs.slide_width), inches(prs.slide_height)
        ],
        "comments": comments,
        "tokens": {},
        "units": units,
    }


# --------------------------------------------------------------------------
# html
# --------------------------------------------------------------------------

SEMANTIC_UNIT_TAGS = {"section", "article"}
# class tokens that mark a deck unit when no <section> tags exist
UNIT_CLASS_TOKENS = {"slide", "page", "panel", "step-section"}
# never treat chrome as a unit, whatever its class says
CHROME_CLASS_RE = re.compile(r"nav|sidebar|menu|rail|toc|drawer|overlay|modal")
ELEMENT_TAGS = {
    "h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "figcaption",
    "button", "a", "img", "svg", "canvas", "table", "blockquote", "summary",
}
VOID_TAGS = {"img", "br", "hr", "input", "meta", "link", "source", "col"}


def _classes(value):
    return set((value or "").split())


class DeckParser(HTMLParser):
    """Collects deck units and their content elements.

    Unit detection is two-tier on purpose: if the document uses <section> or
    <article>, those are the units and nothing else is. Only when it does not
    do we fall back to class tokens, and even then chrome (nav, sidebar, rails)
    is excluded. Without this a sidebar of "nav-section" divs swamps the
    snapshot with empty units and hides the real slides.
    """

    def __init__(self, use_semantic):
        super().__init__(convert_charrefs=True)
        self.use_semantic = use_semantic
        self.units = []
        self.unit_stack = []      # (unit, depth)
        self.el_stack = []        # (element, depth)
        self.depth = 0
        self.styles = []
        self.in_style = False
        self.fallback = []
        self.doc_text = []

    # -- helpers ----------------------------------------------------------
    def _attr(self, attrs, name):
        for k, v in attrs:
            if k == name:
                return v or ""
        return ""

    def _is_unit(self, tag, cls):
        if self.use_semantic:
            return tag in SEMANTIC_UNIT_TAGS
        if tag not in ("div", "section", "article", "li"):
            return False
        classes = _classes(cls)
        if not classes & UNIT_CLASS_TOKENS:
            return False
        return not CHROME_CLASS_RE.search(cls or "")

    @property
    def current(self):
        return self.unit_stack[-1][0] if self.unit_stack else None

    def _pool(self):
        return self.current["elements"] if self.current else self.fallback

    # -- parsing ----------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        if tag == "style":
            self.in_style = True
            return

        void = tag in VOID_TAGS
        if not void:
            self.depth += 1

        eid = self._attr(attrs, "id")
        cls = self._attr(attrs, "class")

        if self._is_unit(tag, cls):
            unit = {
                "index": len(self.units) + 1,
                "id": eid or "%s-%d" % (tag, len(self.units) + 1),
                "name": "",
                "layout": ("%s.%s" % (tag, cls.strip())).rstrip("."),
                "notes_digest": digest(""),
                "elements": [],
                "_text": [],
            }
            self.units.append(unit)
            self.unit_stack.append((unit, self.depth))
            return

        if tag in ELEMENT_TAGS:
            pool = self._pool()
            ordinal = sum(1 for e in pool if e["type"] == tag) + 1
            el = {
                "key": eid or "%s:%d" % (tag, ordinal),
                "name": eid or tag,
                "type": tag,
                "ph": None,
                "pos": [None, None, None, None],
                "text": "",
                "font": {"sizes": [], "bold": [], "colors": []},
                "fill": None,
                "extra": {"class": cls.strip(), "id": eid},
            }
            if tag == "img":
                el["extra"]["src"] = self._attr(attrs, "src")[:120]
            if tag == "a":
                el["extra"]["href"] = self._attr(attrs, "href")[:120]
            style = self._attr(attrs, "style")
            if style:
                el["extra"]["style"] = norm_text(style)
            pool.append(el)
            if void:
                self._finish(el)
            else:
                self.el_stack.append((el, self.depth))

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
            return
        if tag in VOID_TAGS:
            return

        while self.el_stack and self.el_stack[-1][1] >= self.depth:
            self._finish(self.el_stack.pop()[0])
        while self.unit_stack and self.unit_stack[-1][1] >= self.depth:
            self.unit_stack.pop()

        self.depth = max(0, self.depth - 1)

    def _finish(self, el):
        el["text"] = norm_text(el["text"])
        el["text_digest"] = digest(el["text"])
        el["digest"] = digest(el["name"], el["type"], el["text"], el["extra"])

    def handle_data(self, data):
        if self.in_style:
            self.styles.append(data)
            return
        # text bubbles to every open ancestor, so a <p> holding a link keeps
        # the link's words in its own digest
        for el, _ in self.el_stack:
            el["text"] += data
        # and to the unit itself, which catches text sitting in plain divs that
        # are not tracked as elements. Without this, a label change inside an
        # untracked wrapper is invisible to the compare step.
        if self.unit_stack:
            for unit, _ in self.unit_stack:
                unit["_text"].append(data)
        else:
            self.doc_text.append(data)

    def close(self):
        super().close()
        while self.el_stack:
            self._finish(self.el_stack.pop()[0])


def inventory_html(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read()

    use_semantic = re.search(r"<(section|article)[\s>]", raw, re.I) is not None
    parser = DeckParser(use_semantic)
    parser.feed(raw)
    parser.close()

    tokens = {}
    for block in parser.styles:
        for m in re.finditer(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;}]+)", block):
            tokens.setdefault(m.group(1), norm_text(m.group(2)))

    # an empty, unnamed unit is chrome that slipped through, not a slide
    units = [u for u in parser.units if u["elements"] or u.get("id")]
    if parser.fallback or parser.doc_text:
        units.append({
            "index": 0, "id": "document", "name": "(outside any section)",
            "layout": "document", "notes_digest": digest(""),
            "elements": parser.fallback,
            "_text": parser.doc_text,
        })
    units.sort(key=lambda u: u["index"])
    for i, u in enumerate(units, start=1):
        u["index"] = i

    for u in units:
        for el in u["elements"]:
            el.setdefault("text_digest", digest(el.get("text", "")))
            el.setdefault("digest", digest(el))
        heading = next(
            (e["text"] for e in u["elements"]
             if e["type"] in ("h1", "h2", "h3") and e["text"]), "")
        if not heading and u["id"] != "document":
            heading = next((e["text"] for e in u["elements"] if e["text"]), "")
        u["name"] = heading[:90]
        text = norm_text("".join(u.pop("_text", [])))
        u["text_digest"] = digest(text)
        u["text_len"] = len(text)
        u["digest"] = digest(
            [e["digest"] for e in u["elements"]], u["layout"], u["text_digest"])

    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    return {
        "file": os.path.abspath(path),
        "kind": "html",
        "unit_label": "section",
        "generated": datetime.now().isoformat(timespec="seconds"),
        "title": norm_text(title.group(1)) if title else "",
        "tokens": tokens,
        "units": units,
    }


# --------------------------------------------------------------------------

def summarise(inv):
    lines = []
    label = inv["unit_label"]
    lines.append("%s  (%s, %d %ss)" % (
        os.path.basename(inv["file"]), inv["kind"], len(inv["units"]), label))
    if inv.get("tokens"):
        lines.append("  tokens: %d custom properties" % len(inv["tokens"]))
    cm = (inv.get("comments") or {}).get("total", 0)
    if cm:
        lines.append("  comments: %d (these must survive the edit)" % cm)
    for u in inv["units"]:
        flag = ""
        if u.get("comments"):
            flag = "  [%d comment%s]" % (
                u["comments"], "" if u["comments"] == 1 else "s")
        lines.append("  [%d] %-44s %-22s %d elements%s" % (
            u["index"], (u["name"] or "(untitled)")[:44],
            (u["layout"] or "")[:22], len(u["elements"]), flag))
    return "\n".join(lines)


def find(inv, needle):
    needle = needle.lower()
    hits = []
    for u in inv["units"]:
        for el in u["elements"]:
            hay = " ".join([
                el.get("text", ""), el.get("name", ""),
                json.dumps(el.get("extra", {})),
            ]).lower()
            if needle in hay:
                hits.append((u, el))
    if not hits:
        return "no match for %r" % needle
    out = ["%d match(es) for %r" % (len(hits), needle)]
    for u, el in hits:
        pos = el["pos"]
        posy = ("  at %.2f,%.2f  %.2fx%.2f" % tuple(pos)) if all(
            p is not None for p in pos) else ""
        out.append("  %s %d | %s (%s)%s" % (
            inv["unit_label"], u["index"], el["name"], el["type"], posy))
        if el.get("text"):
            out.append("      %s" % el["text"][:110])
    return "\n".join(out)


def audit(inv):
    """Find the two defects that make a slide look machine-made.

    1. Body text in a floating text box instead of the layout's placeholder.
    2. Bullet characters typed into the text instead of real list formatting.
    """
    sw, sh = (inv.get("slide_size") or [None, None])[:2]
    floating, fake, offslide = [], [], []

    for u in inv["units"]:
        # the defect signature is an EMPTY body placeholder sitting next to a
        # text box full of body copy. A deck full of labelled diagrams uses
        # text boxes on purpose, and flagging those trains the wrong fix.
        empty_body = [
            el for el in u["elements"]
            if el.get("ph") and any(k in str(el["ph"]).upper() for k in
                                    ("BODY", "OBJECT", "SUBTITLE", "CONTENT"))
            and not (el.get("text") or "").strip()
        ]
        for el in u["elements"]:
            text = el.get("text") or ""
            is_box = "TEXT_BOX" in str(el.get("type", ""))
            if is_box and not el.get("ph") and len(text) > 60 and empty_body:
                floating.append((u, el))

            n = (el.get("extra") or {}).get("typed_bullets")
            if n:
                fake.append((u, el, n))

            # text that literally sits off the slide or over its edge
            p = el.get("pos") or []
            if sw and len(p) == 4 and all(v is not None for v in p) and text:
                left, top, w, hgt = p
                if left < -0.05 or top < -0.05 or \
                        left + w > sw + 0.05 or top + hgt > sh + 0.05:
                    offslide.append((u, el))

    out = []
    label = inv["unit_label"]
    if floating:
        out.append("BODY TEXT IN A FLOATING BOX (%d): the slide's own content "
                   "placeholder is empty" % len(floating))
        for u, el in floating:
            out.append("  %s %d | %s: %s" % (
                label, u["index"], el["name"], (el.get("text") or "")[:60]))
        out.append("")
    if offslide:
        out.append("TEXT OVER THE SLIDE EDGE (%d)" % len(offslide))
        for u, el in offslide:
            left, top, w, hgt = el["pos"]
            out.append("  %s %d | %s at %.2f,%.2f size %.2fx%.2f: %s" % (
                label, u["index"], el["name"], left, top, w, hgt,
                (el.get("text") or "")[:40]))
        out.append("")
    if fake:
        total = sum(n for _, _, n in fake)
        out.append("TYPED BULLETS (%d paragraph%s in %d shape%s): a dot in the "
                   "text, not a real list" % (
                       total, "" if total == 1 else "s",
                       len(fake), "" if len(fake) == 1 else "s"))
        for u, el, n in fake:
            out.append("  %s %d | %s: %d paragraph%s" % (
                label, u["index"], el["name"], n, "" if n == 1 else "s"))
        out.append("")
    if not out:
        return "AUDIT CLEAN: no floating body text boxes, no typed bullets."
    out.append("Fixes: move body copy into the layout's placeholder, let the "
               "layout supply the bullets, pull stray boxes back inside the "
               "slide. Each one is a change the user has to ask for, so report "
               "them rather than fixing them unasked.")
    out.append("See references/placeholders-and-bullets.md")
    return "\n".join(out)


def main():
    # deck text carries arrows, smart quotes and dashes that the Windows
    # console cannot encode; without this a clean report dies on one character
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path")
    ap.add_argument("-o", "--out", help="write JSON snapshot here")
    ap.add_argument("--print", dest="show", action="store_true",
                    help="print a human summary")
    ap.add_argument("--find", help="locate elements containing this text")
    ap.add_argument("--audit", action="store_true",
                    help="flag floating text boxes and typed bullets")
    ap.add_argument("--json", action="store_true", help="dump full JSON")
    args = ap.parse_args()

    ext = os.path.splitext(args.path)[1].lower()
    if ext in (".pptx", ".potx", ".pptm"):
        inv = inventory_pptx(args.path)
    elif ext in (".html", ".htm"):
        inv = inventory_html(args.path)
    else:
        sys.exit("unsupported file type: %s" % ext)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(inv, fh, indent=1)
        print("snapshot -> %s" % args.out)

    if args.find:
        print(find(inv, args.find))
    elif args.audit:
        print(audit(inv))
    elif args.json:
        print(json.dumps(inv, indent=1))
    elif args.show or not args.out:
        print(summarise(inv))


if __name__ == "__main__":
    main()
