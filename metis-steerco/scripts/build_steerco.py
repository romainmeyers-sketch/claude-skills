#!/usr/bin/env python
"""
build_steerco.py — Generate a Metis-branded SteerCo deck from a JSON content file.

This script builds the MAIN DECK by construction, in the canonical SteerCo order:

    Cover
    -> Anchor summary       (3-column: What We Achieved / Working On / What's Next)
    -> Risks & Tradeoffs    (3-column table requiring leadership support)
    -> Leadership Decisions (numbered ask/decision table)
    -> [optional] Tradeoffs detail table
    -> Appendix divider
    -> [optional] appendix slides (bullets)
    -> Closing

The main deck contains ONLY summary, risks, and decisions. Everything else is
routed to the appendix, so the strict main-deck/appendix split (SteerCo Rule 5)
holds by construction — you cannot accidentally leave workplan detail up front.

Usage:
    PYTHON="C:/Users/<you>/AppData/Local/Programs/Python/Python312/python.exe"
    "$PYTHON" build_steerco.py content.json [output.pptx]

The master template and brand tokens are the same ones metis-pptx uses, so the
output is fully brand-consistent (green arrow, logo, footer, page numbers).
"""

import sys
import os
import io
import json
import zipfile

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# --------------------------------------------------------------------------- #
# Brand tokens (canonical Metis values, matching metis-pptx/metis-brand.md)
# --------------------------------------------------------------------------- #
DARK_NAVY  = RGBColor(0x20, 0x21, 0x6F)
METIS_BLUE = RGBColor(0x25, 0x6B, 0xA2)
MINT       = RGBColor(0x3C, 0xDB, 0xC0)
MET_GREEN  = RGBColor(0x00, 0x7D, 0x66)   # deep Metis green (anchor "achieved" header)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
DARK_GRAY  = RGBColor(0x4A, 0x4A, 0x4A)
MED_GRAY   = RGBColor(0xD9, 0xD9, 0xD9)
LIGHT_MINT = RGBColor(0xD6, 0xF7, 0xF2)
LIGHT_BLUE = RGBColor(0xCB, 0xE1, 0xF3)

# Anchor column tints (sampled from the reference leadership deck)
ANCHOR_BODY_GREEN  = RGBColor(0xDC, 0xED, 0xEA)
ANCHOR_BODY_BLUE   = RGBColor(0xCC, 0xE2, 0xF3)
ANCHOR_BODY_PURPLE = RGBColor(0xC6, 0xC6, 0xEE)

MASTER_PATH = (
    r"G:\Shared drives\Knowledge Management\New Brand Assets"
    r"\PowerPoint Templates\master.pptx"
)

# Anchor columns: header fill / body tint / bullet-marker color, left to right
# (What We Achieved / What We're Working On / What's Next), matching the
# reference leadership deck's icon-header + chevron + tinted-card treatment.
ANCHOR_HEADERS = [MET_GREEN, METIS_BLUE, DARK_NAVY]
ANCHOR_BODIES  = [ANCHOR_BODY_GREEN, ANCHOR_BODY_BLUE, ANCHOR_BODY_PURPLE]
ANCHOR_ACCENTS = ANCHOR_HEADERS
# Default Lucide icons per column (white, sit in a circular badge on the header)
ANCHOR_ICONS   = ["circle-check", "clipboard-list", "chevrons-right"]

# --------------------------------------------------------------------------- #
# Lucide icon support (shared with metis-pptx). Imported defensively so the
# generator still produces a deck if the icon renderer / network is missing.
# --------------------------------------------------------------------------- #
_ICONS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "metis-pptx", "scripts"))
if _ICONS_DIR not in sys.path:
    sys.path.insert(0, _ICONS_DIR)
try:
    from icons import add_lucide_icon as _add_lucide_icon
except Exception:
    _add_lucide_icon = None


def _hex(color):
    return "#" + str(color)


def _safe_add_icon(slide, name, left, top, size, color):
    """Add a Lucide icon; return the shape or None if unavailable.
    Never raises, so a missing renderer/network degrades gracefully to a
    text-only header band rather than failing the whole build."""
    if _add_lucide_icon is None or not name:
        return None
    try:
        return _add_lucide_icon(slide, name, Inches(left), Inches(top),
                                Inches(size), color=_hex(color))
    except Exception:
        return None


def _set_round(shape, radius_frac):
    """Set a rounded-rectangle corner radius (fraction of the short side)."""
    try:
        shape.adjustments[0] = radius_frac
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# Low-level helpers (mirrors metis-pptx conventions)
# --------------------------------------------------------------------------- #
def set_font(run, size=14, bold=False, color=DARK_GRAY, italic=False):
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.italic = italic


def no_shadow(shape):
    """Kill the inherited theme drop-shadow (House Style rule 1)."""
    shape.shadow.inherit = False
    return shape


def get_layout(prs, name):
    for layout in prs.slide_layouts:
        if layout.name == name:
            return layout
    raise ValueError(
        f"Layout '{name}' not found. Available: {[l.name for l in prs.slide_layouts]}"
    )


def set_placeholder_text(ph, text):
    """Set title placeholder text (idx=0 tolerates full-paragraph replace)."""
    ph.text = text


def add_paragraphs(tf, items, size=10, color=DARK_GRAY, bold=False,
                   bullet=False, first=True, space_after=3, align=PP_ALIGN.LEFT):
    """Write a list of strings as separate paragraphs into a text frame."""
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if (first and i == 0) else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        r = p.add_run()
        r.text = ("• " + item) if bullet else item
        set_font(r, size=size, bold=bold, color=color)
    return tf


# --------------------------------------------------------------------------- #
# Slide builders
# --------------------------------------------------------------------------- #
def add_cover(prs, meta):
    slide = prs.slides.add_slide(get_layout(prs, "Cover Page"))
    title = meta.get("project_title", "SteerCo Update")
    label = meta.get("label", "SteerCo Update")
    date = meta.get("date", "")
    cover_image = meta.get("cover_image")
    for ph in list(slide.placeholders):
        idx = ph.placeholder_format.idx
        if idx == 0:            # title
            set_placeholder_text(ph, title)
        elif idx == 1:          # top label line
            _safe_set(ph, label)
        elif idx == 2:          # date line
            _safe_set(ph, date)
        elif idx == 3:          # picture placeholder
            if cover_image and os.path.isfile(cover_image):
                ph.insert_picture(cover_image)
            else:
                # Remove empty picture placeholder so it doesn't render as a
                # white box on an otherwise finished cover.
                ph._element.getparent().remove(ph._element)
    return slide


def _safe_set(ph, text):
    """Set text on a styled placeholder while preserving its formatting."""
    tf = ph.text_frame
    if tf.paragraphs and tf.paragraphs[0].runs:
        tf.paragraphs[0].runs[0].text = text
        for extra in tf.paragraphs[0].runs[1:]:
            extra.text = ""
    else:
        run = tf.paragraphs[0].add_run()
        run.text = text


def add_content_slide(prs, title_text, subtitle_text, source=None):
    """Content slide on '1_Title Only' (green arrow, logo, footer inherited)."""
    slide = prs.slides.add_slide(get_layout(prs, "1_Title Only"))
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx == 0:
            set_placeholder_text(ph, title_text)
        else:
            # Remove any extra layout placeholders (body/text boxes) so no
            # empty "Click to add text" prompt survives into the deck.
            ph._element.getparent().remove(ph._element)
    if subtitle_text:
        sub = slide.shapes.add_textbox(Inches(0.50), Inches(0.92),
                                       Inches(12.33), Inches(0.40))
        sub.text_frame.word_wrap = True
        p = sub.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = subtitle_text
        set_font(r, size=13, bold=False, color=DARK_GRAY, italic=True)
    return slide


def add_section_divider(prs, title_text):
    slide = prs.slides.add_slide(get_layout(prs, "Section Divider"))
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0:
            set_placeholder_text(ph, title_text)
    return slide


def add_closing(prs, title_text="Thank You!"):
    slide = prs.slides.add_slide(get_layout(prs, "Closing Slide"))
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0:
            set_placeholder_text(ph, title_text)
    return slide


def add_takeaway(slide, text, top=6.05):
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.50), Inches(top),
        Inches(12.33), Inches(0.62))
    box.fill.solid()
    box.fill.fore_color.rgb = DARK_NAVY
    box.line.fill.background()
    no_shadow(box)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.30)
    tf.margin_right = Inches(0.30)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    set_font(r, size=13, bold=True, color=WHITE)
    return box


# --------------------------------------------------------------------------- #
# THE ANCHOR SLIDE — 3-column Achieved / In Progress / Next
# --------------------------------------------------------------------------- #
def _anchor_header(slide, left, top, width, height, text, header_color,
                   icon_name):
    """Draw one anchor column header: accent band + white circular icon badge
    + white left-aligned label, matching the reference leadership deck."""
    band = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top),
        Inches(width), Inches(height))
    band.fill.solid()
    band.fill.fore_color.rgb = header_color
    band.line.fill.background()
    no_shadow(band)
    _set_round(band, 0.14)

    # White circular icon badge on the left, with the accent-colored glyph
    badge_d = height - 0.16
    badge_left = left + 0.13
    badge_top = top + (height - badge_d) / 2.0
    text_left_pad = 0.13 + badge_d + 0.14
    icon = _safe_add_icon(slide, icon_name,
                          badge_left + badge_d * 0.22,
                          badge_top + badge_d * 0.22,
                          badge_d * 0.56, header_color)
    if icon is not None:
        badge = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(badge_left), Inches(badge_top),
            Inches(badge_d), Inches(badge_d))
        badge.fill.solid()
        badge.fill.fore_color.rgb = WHITE
        badge.line.fill.background()
        no_shadow(badge)
        # Keep the glyph on top of the badge (badge was added after the icon,
        # so move the icon to render immediately after the badge).
        badge._element.addnext(icon._element)
    else:
        text_left_pad = 0.16  # no badge rendered; center-pad the label instead

    # Header label (white, bold, left-aligned after the badge)
    lbl = slide.shapes.add_textbox(
        Inches(left + text_left_pad), Inches(top),
        Inches(width - text_left_pad - 0.10), Inches(height))
    ltf = lbl.text_frame
    ltf.word_wrap = True
    ltf.vertical_anchor = MSO_ANCHOR.MIDDLE
    ltf.margin_left = Inches(0.0)
    ltf.margin_top = Inches(0.02)
    ltf.margin_bottom = Inches(0.02)
    lp = ltf.paragraphs[0]
    lp.alignment = PP_ALIGN.LEFT
    lr = lp.add_run()
    lr.text = text
    set_font(lr, size=13.5, bold=True, color=WHITE)


def _anchor_chevron(slide, center_x, center_y):
    """A Metis-blue chevron connector between two anchor columns, signalling
    left-to-right flow (achieved -> working on -> next)."""
    w, h = 0.34, 0.46
    ch = slide.shapes.add_shape(
        MSO_SHAPE.CHEVRON, Inches(center_x - w / 2.0),
        Inches(center_y - h / 2.0), Inches(w), Inches(h))
    ch.fill.solid()
    ch.fill.fore_color.rgb = METIS_BLUE
    ch.line.fill.background()
    no_shadow(ch)


def add_anchor(prs, anchor):
    """The most important slide. Three equal columns communicate, left to right:
    what we achieved, what we're working on, and what's next / decisions needed.

    Styled to match the reference leadership deck: icon-badge headers in
    green / blue / navy, chevron connectors between columns, and body cards
    tinted to each header."""
    title = anchor.get("title", "Where We Are and What We Need From You")
    subtitle = anchor.get("subtitle", "")
    slide = add_content_slide(prs, title, subtitle)

    icons = anchor.get("column_icons", ANCHOR_ICONS)
    columns = [
        ("What We Achieved", anchor.get("achieved", []),
         ANCHOR_HEADERS[0], ANCHOR_BODIES[0], icons[0]),
        ("What We're Working On", anchor.get("in_progress", []),
         ANCHOR_HEADERS[1], ANCHOR_BODIES[1], icons[1]),
        ("What's Next", anchor.get("next", []),
         ANCHOR_HEADERS[2], ANCHOR_BODIES[2], icons[2]),
    ]

    left0 = 0.50
    gap = 0.30
    card_w = (12.33 - 2 * gap) / 3.0
    header_top = 1.68
    header_h = 0.58
    body_top = header_top + header_h + 0.14
    has_takeaway = bool(anchor.get("takeaway"))
    body_bottom = 5.95 if has_takeaway else 6.95
    body_h = body_bottom - body_top

    for i, (head, items, header_color, body_color, icon_name) in enumerate(columns):
        left = left0 + i * (card_w + gap)

        # Body card (tinted to the header, near-square corners, no shadow)
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(body_top),
            Inches(card_w), Inches(body_h))
        card.fill.solid()
        card.fill.fore_color.rgb = body_color
        card.line.fill.background()
        no_shadow(card)
        _set_round(card, 0.03)

        # Header band with icon badge + label
        _anchor_header(slide, left, header_top, card_w, header_h,
                       head, header_color, icon_name)

        # Chevron connector in the gap after every column except the last
        if i < len(columns) - 1:
            _anchor_chevron(slide, left + card_w + gap / 2.0,
                            header_top + header_h / 2.0)

        # Body items as bullets
        body = slide.shapes.add_textbox(
            Inches(left + 0.20), Inches(body_top + 0.18),
            Inches(card_w - 0.40), Inches(body_h - 0.34))
        tf = body.text_frame
        tf.word_wrap = True
        if not items:
            items = ["(none this cycle)"]
        for j, item in enumerate(items):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.space_after = Pt(8)
            marker = p.add_run()
            marker.text = "▪ "
            set_font(marker, size=11, bold=True, color=header_color)
            r = p.add_run()
            r.text = item
            set_font(r, size=11.5, bold=False, color=DARK_GRAY)

    if has_takeaway:
        add_takeaway(slide, anchor["takeaway"], top=6.15)
    return slide


# --------------------------------------------------------------------------- #
# DRAFT STORYLINE FOR THE NEXT STEERCO
# --------------------------------------------------------------------------- #
def _draft_tag(slide):
    tag = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.98), Inches(0.30),
        Inches(1.85), Inches(0.38))
    tag.fill.solid()
    tag.fill.fore_color.rgb = MED_GRAY
    tag.line.fill.background()
    no_shadow(tag)
    tf = tag.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "DRAFT — TEAM ALIGNMENT"
    set_font(r, size=9, bold=True, color=DARK_GRAY, italic=True)
    return tag


def add_next_storyline(prs, spec):
    """A forward-looking DRAFT slide: the storyline we intend to tell at the
    NEXT SteerCo. Lets the team work backward from the story they want to land.
    Rendered on every deck by default; fill it in as a working draft."""
    date = spec.get("date", "[next SteerCo date]")
    title = spec.get("title", "The Story We Want to Tell at the Next SteerCo")
    subtitle = spec.get(
        "subtitle",
        f"Draft storyline to align the team on where we aim to be by {date}")
    slide = add_content_slide(prs, title, subtitle)
    _draft_tag(slide)

    # Headline banner — the one-sentence message we aim to deliver next time
    headline = spec.get(
        "headline",
        "[Draft the single message you intend to deliver at the next SteerCo]")
    lbl = slide.shapes.add_textbox(Inches(0.50), Inches(1.45),
                                   Inches(12.33), Inches(0.28))
    lp = lbl.text_frame.paragraphs[0]
    lr = lp.add_run()
    lr.text = "THE HEADLINE WE ARE DRIVING TOWARD"
    set_font(lr, size=10, bold=True, color=METIS_BLUE)

    banner = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.50), Inches(1.75),
        Inches(12.33), Inches(0.85))
    banner.fill.solid()
    banner.fill.fore_color.rgb = LIGHT_MINT
    banner.line.fill.background()
    no_shadow(banner)
    btf = banner.text_frame
    btf.word_wrap = True
    btf.vertical_anchor = MSO_ANCHOR.MIDDLE
    btf.margin_left = Inches(0.30)
    btf.margin_right = Inches(0.30)
    bp = btf.paragraphs[0]
    bp.alignment = PP_ALIGN.CENTER
    br = bp.add_run()
    br.text = headline
    set_font(br, size=15, bold=True, color=DARK_NAVY)

    # Three supporting columns
    columns = [
        ("By Then We Expect to Have",
         spec.get("expected_achievements",
                  ["[What should be done by the next SteerCo — roll forward "
                   "from this week's What's Next]"])),
        ("Decisions We'll Likely Bring",
         spec.get("expected_decisions",
                  ["[The asks you anticipate needing from leadership next time]"])),
        ("What Must Go Right in Between",
         spec.get("watch_items",
                  ["[The milestones and risks that gate that story]"])),
    ]
    left0 = 0.50
    gap = 0.30
    card_w = (12.33 - 2 * gap) / 3.0
    top = 2.95
    card_h = 3.05
    header_h = 0.50
    for i, (head, items) in enumerate(columns):
        left = left0 + i * (card_w + gap)
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top),
            Inches(card_w), Inches(card_h))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.fill.background()
        no_shadow(card)
        band = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top),
            Inches(card_w), Inches(header_h))
        band.fill.solid()
        band.fill.fore_color.rgb = LIGHT_BLUE
        band.line.fill.background()
        no_shadow(band)
        btf = band.text_frame
        btf.vertical_anchor = MSO_ANCHOR.MIDDLE
        bp = btf.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        br = bp.add_run()
        br.text = head
        set_font(br, size=12, bold=True, color=DARK_NAVY)
        body = slide.shapes.add_textbox(
            Inches(left + 0.15), Inches(top + header_h + 0.10),
            Inches(card_w - 0.30), Inches(card_h - header_h - 0.20))
        tf = body.text_frame
        tf.word_wrap = True
        for j, item in enumerate(items):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.space_after = Pt(6)
            marker = p.add_run()
            marker.text = "▪ "
            set_font(marker, size=11, bold=True, color=METIS_BLUE)
            r = p.add_run()
            r.text = item
            set_font(r, size=11, bold=False, color=DARK_GRAY)

    # Footer note reinforcing this is a working draft
    note = slide.shapes.add_textbox(Inches(0.50), Inches(6.15),
                                    Inches(12.33), Inches(0.30))
    npf = note.text_frame.paragraphs[0]
    nr = npf.add_run()
    nr.text = ("Working draft to align the team on next time's narrative; "
               "refine before the next SteerCo and it becomes the spine of "
               "that deck.")
    set_font(nr, size=10, bold=False, color=DARK_GRAY, italic=True)
    return slide


# --------------------------------------------------------------------------- #
# Tables
# --------------------------------------------------------------------------- #
def _style_cell(cell, text, size=10, bold=False, color=DARK_GRAY,
                fill=None, italic=False, valign=MSO_ANCHOR.TOP):
    if fill is not None:
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
    else:
        cell.fill.background()
    cell.vertical_anchor = valign
    cell.margin_left = Inches(0.08)
    cell.margin_right = Inches(0.08)
    cell.margin_top = Inches(0.04)
    cell.margin_bottom = Inches(0.04)
    tf = cell.text_frame
    tf.word_wrap = True
    lines = text.split("\n") if isinstance(text, str) else list(text)
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(2)
        # Bold any leading "Implication:" / "Label:" prefix
        if line.startswith("Implication:"):
            r = p.add_run()
            r.text = "Implication: "
            set_font(r, size=size - 0.5, bold=True, color=DARK_NAVY, italic=True)
            r2 = p.add_run()
            r2.text = line[len("Implication:"):].strip()
            set_font(r2, size=size - 0.5, bold=False, color=DARK_GRAY, italic=True)
        else:
            r = p.add_run()
            r.text = line
            set_font(r, size=size, bold=bold, color=color, italic=italic)


def _add_table(slide, rows, cols, left, top, width, col_widths=None):
    gf = slide.shapes.add_table(rows, cols, Inches(left), Inches(top),
                                Inches(width), Inches(0.4))
    table = gf.table
    table.first_row = False
    table.horz_banding = False
    if col_widths:
        for c, w in enumerate(col_widths):
            table.columns[c].width = Inches(w)
    return table


RISK_HEADERS = [DARK_NAVY, METIS_BLUE, MET_GREEN]
RISK_BODIES  = [LIGHT_GRAY, ANCHOR_BODY_BLUE, ANCHOR_BODY_GREEN]
RISK_ICONS   = ["triangle-alert", "wrench", "handshake"]


def _number_badge(slide, left, top, d, number, fill=DARK_NAVY, size=11):
    """Small filled circle with a white number, used to tie risks to the
    decisions slide (risk N resolves to decision N)."""
    badge = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(left), Inches(top), Inches(d), Inches(d))
    badge.fill.solid()
    badge.fill.fore_color.rgb = fill
    badge.line.fill.background()
    no_shadow(badge)
    tf = badge.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0)
    tf.margin_right = Inches(0)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = str(number)
    set_font(r, size=size, bold=True, color=WHITE)
    return badge


def _card(slide, left, top, w, h, fill, radius=0.06):
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top),
        Inches(w), Inches(h))
    card.fill.solid()
    card.fill.fore_color.rgb = fill
    card.line.fill.background()
    no_shadow(card)
    _set_round(card, radius)
    return card


def _card_text(slide, left, top, w, h, segments, size=9.5,
               valign=MSO_ANCHOR.MIDDLE):
    """Text block inside a card. `segments` is a list of paragraphs, each a
    list of (text, kwargs-for-set_font) run tuples."""
    box = slide.shapes.add_textbox(Inches(left), Inches(top),
                                   Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    for i, runs in enumerate(segments):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(2)
        for text, kw in runs:
            r = p.add_run()
            r.text = text
            set_font(r, size=kw.get("size", size), bold=kw.get("bold", False),
                     color=kw.get("color", DARK_GRAY),
                     italic=kw.get("italic", False))
    return box


def add_risks_table(prs, risks):
    """'Risks & Tradeoffs Requiring Leadership Support' as a consulting-style
    card grid: three icon-badge header bands (matching the anchor treatment),
    one numbered card row per risk, and the implication as a highlighted
    italic line inside the leadership-ask card."""
    slide = add_content_slide(prs, risks.get("title",
                              "Risks & Tradeoffs Requiring Leadership Support"),
                              risks.get("subtitle", ""))
    data = risks.get("rows", [])
    if not data:
        return slide
    icons = risks.get("column_icons", RISK_ICONS)
    headers = ["What We Are Working Through",
               "What We Are Doing About It",
               "What We Need From This Group"]

    left0, gap = 0.50, 0.14
    col_w = [3.65, 3.95, 4.31]
    header_top, header_h = 1.52, 0.46
    rows_top = header_top + header_h + 0.12
    rows_bottom = 6.78
    vgap = 0.10
    n = len(data)
    row_h = (rows_bottom - rows_top - (n - 1) * vgap) / n

    lefts = [left0,
             left0 + col_w[0] + gap,
             left0 + col_w[0] + gap + col_w[1] + gap]
    for c in range(3):
        _anchor_header(slide, lefts[c], header_top, col_w[c], header_h,
                       headers[c], RISK_HEADERS[c], icons[c])

    body_size = 9.5 if n <= 4 else 9
    for ri, row in enumerate(data):
        top = rows_top + ri * (row_h + vgap)

        # Col 1 — the risk, numbered to map onto the decisions slide
        _card(slide, lefts[0], top, col_w[0], row_h, RISK_BODIES[0])
        badge_d = 0.30
        _number_badge(slide, lefts[0] + 0.10, top + 0.10, badge_d, ri + 1,
                      fill=DARK_NAVY, size=10)
        label = row.get("label", "")
        segs = []
        if label:
            segs.append([(label, dict(size=body_size + 0.5, bold=True,
                                      color=DARK_NAVY))])
        segs.append([(row.get("working_through", ""), dict(size=body_size))])
        _card_text(slide, lefts[0] + 0.10 + badge_d + 0.10, top + 0.06,
                   col_w[0] - badge_d - 0.36, row_h - 0.12, segs,
                   valign=MSO_ANCHOR.TOP if label else MSO_ANCHOR.MIDDLE)

        # Col 2 — what we're doing
        _card(slide, lefts[1], top, col_w[1], row_h, RISK_BODIES[1])
        _card_text(slide, lefts[1] + 0.14, top + 0.06,
                   col_w[1] - 0.28, row_h - 0.12,
                   [[(row.get("doing_done", ""), dict(size=body_size))]])

        # Col 3 — the ask + implication
        _card(slide, lefts[2], top, col_w[2], row_h, RISK_BODIES[2])
        segs = [[(row.get("needed", ""), dict(size=body_size))]]
        impl = row.get("implication", "")
        if impl:
            segs.append([
                ("If not: ", dict(size=body_size - 0.5, bold=True,
                                  color=DARK_NAVY, italic=True)),
                (impl, dict(size=body_size - 0.5, color=DARK_GRAY,
                            italic=True)),
            ])
        _card_text(slide, lefts[2] + 0.14, top + 0.06,
                   col_w[2] - 0.28, row_h - 0.12, segs)
    return slide


def _milestone_strip(slide, milestones, top, height=0.55):
    """Chevron milestone chain across the bottom of a slide: the simple
    forward-looking line the room leaves with. Last chevron is green (the
    outcome); the rest navy."""
    n = len(milestones)
    if not n:
        return
    gap = 0.06
    w = (12.33 - (n - 1) * gap) / n
    for i, text in enumerate(milestones):
        left = 0.50 + i * (w + gap)
        fill = MET_GREEN if i == n - 1 else DARK_NAVY
        ch = slide.shapes.add_shape(
            MSO_SHAPE.CHEVRON, Inches(left), Inches(top),
            Inches(w), Inches(height))
        ch.fill.solid()
        ch.fill.fore_color.rgb = fill
        ch.line.fill.background()
        no_shadow(ch)
        try:
            ch.adjustments[0] = 0.28
        except Exception:
            pass
        tf = ch.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.14)
        tf.margin_right = Inches(0.06)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        set_font(r, size=10.5, bold=True, color=WHITE)


PANEL_HEADERS = [MET_GREEN, METIS_BLUE, DARK_NAVY]
PANEL_BODIES  = [ANCHOR_BODY_GREEN, ANCHOR_BODY_BLUE, ANCHOR_BODY_PURPLE]


def add_panels_slide(prs, spec):
    """Generic consulting-style panel slide: optional statement banner up top,
    N icon-header panels (anchor visual language), optional navy takeaway
    callout at the bottom. Used for launch-scope and pilot-learnings slides."""
    slide = add_content_slide(prs, spec.get("title", ""),
                              spec.get("subtitle", ""))
    panels = spec.get("panels", [])
    top = 1.50

    banner = spec.get("banner")
    if banner:
        b = _card(slide, 0.50, top, 12.33, 0.72, LIGHT_MINT, radius=0.12)
        tf = b.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.30)
        tf.margin_right = Inches(0.30)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = banner
        set_font(r, size=13.5, bold=True, color=DARK_NAVY)
        top += 0.72 + 0.16

    bottom = 6.78
    callout = spec.get("callout")
    if callout:
        bottom -= (0.62 + 0.14)

    n = max(len(panels), 1)
    gap = 0.30
    w = (12.33 - (n - 1) * gap) / n
    header_h = 0.46
    body_top = top + header_h + 0.12
    body_h = bottom - body_top

    for i, panel in enumerate(panels):
        left = 0.50 + i * (w + gap)
        hc = PANEL_HEADERS[i % 3]
        bc = PANEL_BODIES[i % 3]
        _card(slide, left, body_top, w, body_h, bc, radius=0.04)
        _anchor_header(slide, left, top, w, header_h,
                       panel.get("header", ""), hc, panel.get("icon"))
        box = slide.shapes.add_textbox(
            Inches(left + 0.18), Inches(body_top + 0.14),
            Inches(w - 0.36), Inches(body_h - 0.28))
        tf = box.text_frame
        tf.word_wrap = True
        for j, item in enumerate(panel.get("items", [])):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.space_after = Pt(7)
            marker = p.add_run()
            marker.text = "▪ "
            set_font(marker, size=10.5, bold=True, color=hc)
            r = p.add_run()
            r.text = item
            set_font(r, size=10.5, bold=False, color=DARK_GRAY)

    if callout:
        add_takeaway(slide, callout, top=6.78 - 0.62)
    return slide


def add_decisions_table(prs, decisions):
    """'Leadership Decisions Needed' as consulting-style decision rows:
    numbered badge -> risk card -> chevron -> tinted decision card, so each
    row literally reads as 'this risk resolves to this decision'.

    Optional per-row `callout` renders as a slim mint band beneath that row
    (a message that travels with the decision, not a decision itself).
    Optional top-level `milestones` renders a chevron milestone chain across
    the bottom of the slide."""
    slide = add_content_slide(prs, decisions.get("title",
                              "Leadership Decisions Needed"),
                              decisions.get("subtitle", ""))
    data = decisions.get("rows", [])
    if not data:
        return slide
    milestones = decisions.get("milestones")

    left0 = 0.50
    badge_d = 0.42
    risk_left = left0 + badge_d + 0.14
    risk_w = 4.55
    chev_w = 0.40
    ask_left = risk_left + risk_w + 0.14 + chev_w + 0.14
    ask_w = 12.83 - ask_left

    # Mini column headers (small caps labels over each zone)
    hdr_top = 1.50
    for text, x, w in [("THE RISK", risk_left, risk_w),
                       ("THE DECISION WE NEED", ask_left, ask_w)]:
        box = slide.shapes.add_textbox(Inches(x), Inches(hdr_top),
                                       Inches(w), Inches(0.26))
        p = box.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = text
        set_font(r, size=10, bold=True, color=METIS_BLUE)

    rows_top = hdr_top + 0.34
    rows_bottom = 6.78 - ((0.55 + 0.16) if milestones else 0)
    vgap = 0.14
    callout_h, callout_gap = 0.40, 0.08
    n = len(data)
    extra = sum((callout_h + callout_gap) for row in data if row.get("callout"))
    row_h = (rows_bottom - rows_top - (n - 1) * vgap - extra) / n
    body_size = 10 if n <= 4 else 9.5

    y = rows_top
    for ri, row in enumerate(data):
        top = y
        mid_y = top + row_h / 2.0

        # Numbered badge, vertically centered on the row
        _number_badge(slide, left0, mid_y - badge_d / 2.0, badge_d, ri + 1,
                      fill=DARK_NAVY, size=13)

        # Risk card (neutral)
        _card(slide, risk_left, top, risk_w, row_h, LIGHT_GRAY)
        label = row.get("label", "")
        segs = []
        if label:
            segs.append([(label, dict(size=body_size, bold=True,
                                      color=DARK_NAVY))])
        segs.append([(row.get("risk", ""), dict(size=body_size - 0.5))])
        _card_text(slide, risk_left + 0.16, top + 0.06,
                   risk_w - 0.32, row_h - 0.12, segs)

        # Chevron: the risk resolves to the decision
        ch = slide.shapes.add_shape(
            MSO_SHAPE.CHEVRON, Inches(risk_left + risk_w + 0.14),
            Inches(mid_y - 0.23), Inches(chev_w), Inches(0.46))
        ch.fill.solid()
        ch.fill.fore_color.rgb = METIS_BLUE
        ch.line.fill.background()
        no_shadow(ch)

        # Decision card (navy-tinted: this is where the asks live, matching
        # the anchor's What's Next column)
        _card(slide, ask_left, top, ask_w, row_h, ANCHOR_BODY_PURPLE)
        _card_text(slide, ask_left + 0.16, top + 0.06,
                   ask_w - 0.32, row_h - 0.12,
                   [[(row.get("ask", ""), dict(size=body_size,
                                               color=DARK_NAVY))]])

        y += row_h
        callout = row.get("callout")
        if callout:
            band = _card(slide, risk_left, y + callout_gap,
                         12.83 - risk_left, callout_h, LIGHT_MINT,
                         radius=0.18)
            tf = band.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = Inches(0.20)
            p = tf.paragraphs[0]
            r = p.add_run()
            r.text = callout
            set_font(r, size=9.5, bold=False, color=DARK_NAVY, italic=True)
            y += callout_gap + callout_h
        y += vgap

    if milestones:
        _milestone_strip(slide, milestones, top=6.78 - 0.55)
    return slide


def add_generic_table(prs, spec):
    """Optional extra main-deck table, e.g. 'Protecting Pilot Capacity Creates
    Real Tradeoffs' (slide 8). Columns come straight from the spec."""
    slide = add_content_slide(prs, spec.get("title", "Tradeoffs"),
                              spec.get("subtitle", ""))
    headers = spec.get("headers", [])
    data = spec.get("rows", [])   # list of lists
    cols = len(headers)
    n = len(data) + 1
    total = 12.33
    col_widths = spec.get("col_widths") or [total / cols] * cols
    table = _add_table(slide, n, cols, 0.50, 1.45, total, col_widths=col_widths)
    for c, h in enumerate(headers):
        _style_cell(table.cell(0, c), h, size=10.5, bold=True,
                    color=WHITE, fill=DARK_NAVY, valign=MSO_ANCHOR.MIDDLE)
    for ri, row in enumerate(data, start=1):
        fill = WHITE if ri % 2 else LIGHT_GRAY
        for c in range(cols):
            val = row[c] if c < len(row) else ""
            _style_cell(table.cell(ri, c), val, size=9.5, fill=fill)
    return slide


def add_appendix_bullets(prs, spec):
    """Simple appendix content slide: title + subtitle + bullets.
    For richer appendix visuals (org charts, roadmaps, model diagrams),
    build them with metis-pptx and insert after the Appendix divider."""
    slide = add_content_slide(prs, spec.get("title", "Appendix"),
                              spec.get("subtitle", ""))
    bullets = spec.get("bullets", [])
    body = slide.shapes.add_textbox(Inches(0.50), Inches(1.55),
                                    Inches(12.33), Inches(5.0))
    tf = body.text_frame
    tf.word_wrap = True
    for j, item in enumerate(bullets):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        marker = p.add_run()
        marker.text = "▪ "
        set_font(marker, size=13, bold=True, color=MINT)
        r = p.add_run()
        r.text = item
        set_font(r, size=13.5, bold=False, color=DARK_GRAY)
    return slide


# --------------------------------------------------------------------------- #
# Save
# --------------------------------------------------------------------------- #
def clear_existing_slides(prs):
    """master.pptx ships with a brand reference slide. Remove any pre-existing
    slides so the deck contains only what we build here."""
    sldIdLst = prs.slides._sldIdLst
    for sldId in list(sldIdLst):
        rId = sldId.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        if rId and rId in prs.part.rels:
            prs.part.drop_rel(rId)
        sldIdLst.remove(sldId)


def save_clean(prs, output_path):
    buf = io.BytesIO()
    prs.save(buf)
    buf.seek(0)
    with zipfile.ZipFile(buf, "r") as zin:
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
            seen = set()
            for item in zin.infolist():
                if item.filename not in seen:
                    seen.add(item.filename)
                    zout.writestr(item, zin.read(item.filename))
    print(f"Saved: {output_path}")


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def build(content, output_path):
    if not os.path.isfile(MASTER_PATH):
        raise FileNotFoundError(
            f"Master template not found: {MASTER_PATH}\n"
            "Confirm the G: shared drive is mapped.")
    prs = Presentation(MASTER_PATH)
    clear_existing_slides(prs)

    meta = content.get("meta", {})

    # --- MAIN DECK (strict: summary -> panels/risks -> decisions only) ---
    add_cover(prs, meta)
    add_anchor(prs, content["anchor"])
    for spec in content.get("panel_slides", []):
        add_panels_slide(prs, spec)
    if content.get("risks"):
        add_risks_table(prs, content["risks"])
    if content.get("decisions"):
        add_decisions_table(prs, content["decisions"])
    for extra in content.get("main_tables", []):
        add_generic_table(prs, extra)

    # --- DRAFT storyline for the NEXT SteerCo (on by default) ---
    if meta.get("include_next_storyline", True):
        add_next_storyline(prs, content.get("next_storyline", {}))

    # --- APPENDIX (everything else) ---
    appendix = content.get("appendix", [])
    if appendix:
        add_section_divider(prs, "Appendix")
        for item in appendix:
            t = item.get("type", "bullets")
            if t == "divider":
                add_section_divider(prs, item.get("title", "Appendix"))
            elif t == "table":
                add_generic_table(prs, item)
            else:
                add_appendix_bullets(prs, item)

    add_closing(prs, meta.get("closing", "Thank You!"))

    save_clean(prs, output_path)
    print(f"Slides: {len(prs.slides._sldIdLst)}")


def main():
    if len(sys.argv) < 2:
        print("Usage: build_steerco.py content.json [output.pptx]")
        sys.exit(1)
    content_path = sys.argv[1]
    with open(content_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    output_path = sys.argv[2] if len(sys.argv) > 2 else \
        content.get("meta", {}).get("output", "SteerCo.pptx")
    build(content, output_path)


if __name__ == "__main__":
    main()
