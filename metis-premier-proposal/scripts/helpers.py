"""
helpers.py — Reusable layout components for Metis premier proposal PDFs.

Usage: from helpers import *  (then set `c` and page dimensions before calling)

Caller must set module-level `c` (ReportLab canvas) and W, H before calling most functions.
"""
import os
from reportlab.lib.colors import HexColor, Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

# ---------------------------------------------------------------------------
# Page dimensions (landscape 13.33" × 7.5")
# ---------------------------------------------------------------------------
W = 960.0   # 13.33in × 72
H = 540.0   # 7.50in × 72

# ---------------------------------------------------------------------------
# Brand colors
# ---------------------------------------------------------------------------
DARK_NAVY  = HexColor('#20216f')
MED_BLUE   = HexColor('#256ba2')
MINT       = HexColor('#3cdbc0')
DARK_TEAL  = HexColor('#1a8a7a')
NEAR_BLACK = HexColor('#1a2040')
GRAY       = HexColor('#7b8692')
DARK_GRAY  = HexColor('#333333')
LIGHT_BG   = HexColor('#f4f6fa')
TEAL_LIGHT = HexColor('#e8f8f5')
WHITE_CLR  = HexColor('#ffffff')

# ---------------------------------------------------------------------------
# Asset paths — shared drives
# ---------------------------------------------------------------------------
LOGO_DIR  = 'G:/Shared drives/Knowledge Management/New Brand Assets/Metis Strategy Logo/'
LOGO_BM   = LOGO_DIR + 'Metis Strategy Black-Mint RGB Logo.png'
LOGO_WM   = LOGO_DIR + 'Metis Strategy White-Mint RGB logo.png'
LOGO_W    = LOGO_DIR + 'Metis Strategy White RGB logo.png'

GD         = 'G:/Shared drives/Knowledge Management/New Brand Assets/Graphic Devices/'
TRAJECTORY = GD + 'Metis Trajectory Device RGB.png'
NEXUS      = GD + 'Metis Nexus Device Opaque RGB.png'
ENERGY     = GD + 'Metis Energy Device RGB.png'
ARROW_DEV  = GD + 'Metis Arrow Device Opaque RGB.png'
SNGL_ARROW = GD + 'Metis SnglArrow Device RGB.png'

PHOTO_DIR  = 'G:/Shared drives/Knowledge Management/New Brand Assets/PPT Assets/Metis PPT Images/'

# ---------------------------------------------------------------------------
# Canvas reference — set by the build script before calling helpers
# ---------------------------------------------------------------------------
c = None  # set this: helpers.c = canvas_obj


# ---------------------------------------------------------------------------
# Font registration
# ---------------------------------------------------------------------------
def register_fonts():
    pdfmetrics.registerFont(TTFont('Calibri',        'C:/Windows/Fonts/calibri.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Bold',   'C:/Windows/Fonts/calibrib.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Italic', 'C:/Windows/Fonts/calibrii.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Light',  'C:/Windows/Fonts/calibril.ttf'))


# ---------------------------------------------------------------------------
# Core drawing primitives
# ---------------------------------------------------------------------------
def draw_rect(x, y, w, h, color, alpha=1.0):
    c.saveState()
    c.setFillColor(color)
    if alpha < 1.0:
        c.setFillAlpha(alpha)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.restoreState()


def place_image(path, x, y, w=None, h=None, mask='auto'):
    """Place image at (x, y) — y is bottom edge. Computes missing dimension from aspect."""
    try:
        if w is not None and h is None:
            img = PILImage.open(path)
            aspect = img.size[0] / img.size[1]
            h = w / aspect
        elif h is not None and w is None:
            img = PILImage.open(path)
            aspect = img.size[0] / img.size[1]
            w = h * aspect
        c.drawImage(path, x, y, width=w, height=h, mask=mask, preserveAspectRatio=True)
    except Exception as e:
        print(f'  WARNING: Could not place image {os.path.basename(path)}: {e}')


def new_page():
    c.showPage()
    c.setPageSize((W, H))


def gradient_bg():
    """Dark navy → mid blue gradient fill for cover/divider/closing pages."""
    steps = 40
    for i in range(steps):
        t = i / steps
        r = int(0x20 + t * (0x25 - 0x20))
        g = int(0x21 + t * (0x6b - 0x21))
        b = int(0x6f + t * (0xa2 - 0x6f))
        draw_rect(0, H * (1 - (i + 1) / steps), W, H / steps + 1,
                  Color(r / 255, g / 255, b / 255))


# ---------------------------------------------------------------------------
# Footers
# ---------------------------------------------------------------------------
def footer_light(client_name, page_label=None):
    c.setFont('Calibri', 7.5)
    c.setFillColor(GRAY)
    label = page_label or ''
    c.drawRightString(W - 48, 10, label)
    c.drawString(48, 10, f'Proprietary & Confidential  |  © 2026 Metis Strategy LLC')


def footer_dark(client_name='', page_label=None):
    c.setFont('Calibri', 7.5)
    c.setFillColor(Color(1, 1, 1, 0.35))
    label = page_label or ''
    c.drawRightString(W - 48, 10, label)
    c.drawString(48, 10, f'Proprietary & Confidential  |  © 2026 Metis Strategy LLC')


# ---------------------------------------------------------------------------
# Eyebrow label (with small arrow device)
# ---------------------------------------------------------------------------
def eyebrow(text, y, x=48):
    c.setFont('Calibri-Bold', 8.5)
    c.setFillColor(MINT)
    try:
        c.drawImage(SNGL_ARROW, x, y - 1, width=9, height=9,
                    mask='auto', preserveAspectRatio=True)
    except Exception:
        pass
    c.drawString(x + 14, y, text.upper())
    return y


# ---------------------------------------------------------------------------
# Logo placement helpers
# ---------------------------------------------------------------------------
def logo_top_left(variant=LOGO_WM):
    place_image(variant, 48, H - 60, w=100)


def logo_top_right(variant=LOGO_BM):
    place_image(variant, W - 118, H - 32, w=70)


# ---------------------------------------------------------------------------
# Measurement utilities
# ---------------------------------------------------------------------------
def measure_paragraph(text, width, font='Calibri', size=11, leading=15.5):
    style = ParagraphStyle('m', fontName=font, fontSize=size, leading=leading)
    p = Paragraph(text, style)
    _, ph = p.wrap(width, 9999)
    return ph


def measure_body_text(text, width, size=11, leading=15.5):
    return measure_paragraph(text, width, 'Calibri', size, leading)


def measure_bullet_list(items, width, size=10.5, leading=15, item_gap=0):
    total = 0
    for i, item in enumerate(items):
        h = measure_paragraph(f'• {item}', width, 'Calibri', size, leading)
        total += h
        if i < len(items) - 1:
            total += item_gap
    return total


def measure_callout_height(text, width, label='KEY INSIGHT', size=9.5, leading=13.5):
    style = ParagraphStyle('co', fontName='Calibri', fontSize=size, leading=leading)
    p = Paragraph(text, style)
    _, ph = p.wrap(width - 48, 9999)
    return ph + 28  # padding + label row


# ---------------------------------------------------------------------------
# Dynamic vertical distribution
# ---------------------------------------------------------------------------
def distribute_y_positions(items, top_y, bottom_y, item_heights):
    """Return list of y-positions (top of each item) distributed evenly."""
    total_h = sum(item_heights)
    available = top_y - bottom_y
    if len(items) <= 1:
        return [top_y - item_heights[0] / 2]
    gap = (available - total_h) / (len(items) - 1)
    gap = max(gap, 6)
    positions = []
    y = top_y
    for h in item_heights:
        positions.append(y)
        y -= h + gap
    return positions


# ---------------------------------------------------------------------------
# Metric card
# ---------------------------------------------------------------------------
def metric_card(x, y, w, h, number_str, label_str, bg_color=LIGHT_BG):
    """Draw a metric card. number_str is the big value, label_str is the caption."""
    draw_rect(x, y, w, h, bg_color)
    inner_w = w - 16
    cx = x + w / 2

    num_font_size = 24
    while num_font_size > 11:
        text_w = c.stringWidth(number_str, 'Calibri-Bold', num_font_size)
        if text_w <= inner_w:
            break
        num_font_size -= 1

    c.setFont('Calibri-Bold', num_font_size)
    c.setFillColor(MINT)
    c.drawCentredString(cx, y + h - num_font_size - 6, number_str)

    lbl_size = 7
    while lbl_size > 5:
        text_w = c.stringWidth(label_str.upper(), 'Calibri', lbl_size)
        if text_w <= inner_w:
            break
        lbl_size -= 0.5
    c.setFont('Calibri', lbl_size)
    c.setFillColor(GRAY)
    c.drawCentredString(cx, y + 5, label_str.upper())


# ---------------------------------------------------------------------------
# Callout box
# ---------------------------------------------------------------------------
def callout_box(x, y_top, w, label, body_text, size=9.5, leading=13.5):
    """Draw callout box. y_top is the top edge. Returns height drawn."""
    style = ParagraphStyle('cb', fontName='Calibri', fontSize=size, leading=leading,
                           textColor=DARK_GRAY)
    p = Paragraph(body_text, style)
    pw, ph = p.wrap(w - 48, 999)
    box_h = ph + 28
    box_y = y_top - box_h
    draw_rect(x, box_y, w, box_h, TEAL_LIGHT)
    draw_rect(x, box_y, 3, box_h, DARK_NAVY)
    c.setFont('Calibri-Bold', 7.5)
    c.setFillColor(MINT)
    c.drawString(x + 12, box_y + box_h - 14, label.upper())
    p.drawOn(c, x + 12, box_y + 8)
    return box_h


# ---------------------------------------------------------------------------
# Pull quote
# ---------------------------------------------------------------------------
def pull_quote(x, y, text, width, size=11):
    """Draw pull quote with mint left bar. Returns height consumed."""
    style = ParagraphStyle('pq', fontName='Calibri-Bold', fontSize=size, leading=size * 1.45,
                           textColor=DARK_NAVY)
    p = Paragraph(f'<i>{text}</i>', style)
    pw, ph = p.wrap(width - 16, 999)
    draw_rect(x, y - ph - 8, 3, ph + 6, MINT)
    p.drawOn(c, x + 12, y - ph - 4)
    return ph + 12


# ---------------------------------------------------------------------------
# Numbered item
# ---------------------------------------------------------------------------
def numbered_item(x, y, number, title, body, col_w, badge_color=DARK_NAVY,
                  title_size=10.5, body_size=9.5):
    """Draw a numbered item with badge. Returns height consumed."""
    badge_r = 9
    c.setFillColor(badge_color)
    c.circle(x + badge_r, y - badge_r, badge_r, fill=1, stroke=0)
    c.setFont('Calibri-Bold', 8)
    c.setFillColor(WHITE_CLR)
    c.drawCentredString(x + badge_r, y - badge_r - 3, str(number))

    text_x = x + badge_r * 2 + 8
    text_w = col_w - (badge_r * 2 + 8)

    c.setFont('Calibri-Bold', title_size)
    c.setFillColor(DARK_NAVY)
    c.drawString(text_x, y - title_size + 2, title)

    style = ParagraphStyle('ni', fontName='Calibri', fontSize=body_size,
                           leading=body_size * 1.4, textColor=DARK_GRAY)
    p = Paragraph(body, style)
    pw, ph = p.wrap(text_w, 999)
    p.drawOn(c, text_x, y - title_size - 4 - ph)
    return title_size + 4 + ph + 8


# ---------------------------------------------------------------------------
# Column header
# ---------------------------------------------------------------------------
def column_header(x, y, text, width, size=10.5):
    c.setFont('Calibri-Bold', size)
    c.setFillColor(DARK_NAVY)
    c.drawString(x, y, text)
    draw_rect(x, y - 3, width, 1.5, MINT)
    return size + 8


# ---------------------------------------------------------------------------
# Bullet list
# ---------------------------------------------------------------------------
def bullet_list(x, y_top, items, col_w, size=10.5, leading=15, item_gap=8):
    """Draw bullet list. Returns final y after last item."""
    y = y_top
    style = ParagraphStyle('bl', fontName='Calibri', fontSize=size, leading=leading,
                           textColor=DARK_GRAY)
    for i, item in enumerate(items):
        p = Paragraph(f'• {item}', style)
        pw, ph = p.wrap(col_w, 999)
        p.drawOn(c, x, y - ph)
        y -= ph
        if i < len(items) - 1:
            y -= item_gap
    return y


# ---------------------------------------------------------------------------
# Section divider page
# ---------------------------------------------------------------------------
def section_divider(title_text, subtitle_text=None, device_path=TRAJECTORY,
                    client_name='', page_label=None,
                    style='device', number_text=None, photo_path=None):
    """
    Section divider page. Three styles:
      - 'device' (default): dark gradient + trajectory/nexus device right 50%.
      - 'numbered': giant mint module number on left, title to the right.
                    Pass number_text (e.g., '03'). Falls back to 'device' if missing.
      - 'photo':   full-bleed B&W photo at ~30% opacity behind title.
                   Pass photo_path. Falls back to 'device' if missing.
    """
    if style == 'numbered' and not number_text:
        style = 'device'
    if style == 'photo' and not photo_path:
        style = 'device'

    new_page()

    if style == 'photo':
        try:
            c.drawImage(photo_path, 0, 0, width=W, height=H, mask=None,
                        preserveAspectRatio=True)
        except Exception:
            draw_rect(0, 0, W, H, DARK_NAVY)
        c.setFillColor(Color(0x20 / 255, 0x21 / 255, 0x6f / 255, 0.72))
        c.rect(0, 0, W, H, fill=1, stroke=0)
    else:
        gradient_bg()
        try:
            c.saveState()
            c.setFillAlpha(0.15)
            c.drawImage(device_path, W * 0.55, H * 0.1,
                        width=W * 0.5, height=H * 0.8,
                        mask='auto', preserveAspectRatio=True)
            c.restoreState()
        except Exception:
            pass

    logo_top_left(LOGO_WM)

    title_font_size = 26
    title_leading = 32
    lines = title_text.split('\n')
    title_block_h = title_leading * len(lines)
    title_center_y = H / 2
    title_top_y = title_center_y + title_block_h / 2
    title_bottom_y = title_center_y - title_block_h / 2

    if style == 'numbered':
        num_size = 180
        c.setFont('Calibri-Bold', num_size)
        c.setFillColor(MINT)
        c.setFillAlpha(0.85)
        c.drawString(48, title_center_y - num_size * 0.38, number_text)
        c.setFillAlpha(1.0)
        title_x = 48 + c.stringWidth(number_text, 'Calibri-Bold', num_size) + 32
        bar_y = title_top_y + 12
        draw_rect(title_x, bar_y, 50, 3, MINT)
        c.setFont('Calibri-Bold', title_font_size)
        c.setFillColor(WHITE_CLR)
        baseline_y = title_top_y - title_font_size * 0.85
        for line in lines:
            c.drawString(title_x, baseline_y, line)
            baseline_y -= title_leading
        if subtitle_text:
            sstyle = ParagraphStyle('ds', fontName='Calibri-Light', fontSize=12,
                                    leading=17, textColor=Color(1, 1, 1, 0.65))
            p = Paragraph(subtitle_text, sstyle)
            pw, ph = p.wrap(W - title_x - 48, 100)
            p.drawOn(c, title_x, title_bottom_y - ph - 16)
    else:
        bar_y = title_top_y + 12
        draw_rect(48, bar_y, 50, 3, MINT)
        c.setFont('Calibri-Bold', title_font_size)
        c.setFillColor(WHITE_CLR)
        baseline_y = title_top_y - title_font_size * 0.85
        for line in lines:
            c.drawString(48, baseline_y, line)
            baseline_y -= title_leading
        if subtitle_text:
            sstyle = ParagraphStyle('ds', fontName='Calibri-Light', fontSize=12,
                                    leading=17, textColor=Color(1, 1, 1, 0.65))
            p = Paragraph(subtitle_text, sstyle)
            pw, ph = p.wrap(450, 100)
            p.drawOn(c, 48, title_bottom_y - ph - 16)

    footer_dark(client_name, page_label)


# ---------------------------------------------------------------------------
# Activities / Deliverables two-column page
# ---------------------------------------------------------------------------
def activities_deliverables_page(eyebrow_text, title_text, subtitle_text,
                                 activities, deliverables,
                                 callouts=None,
                                 client_name='', page_label=None):
    """
    Two-column layout: Activities (left) / Deliverables (right).
    callouts: list of (label, body) tuples, max 2.
    """
    new_page()
    logo_top_right()

    ty = H - 48
    eyebrow(eyebrow_text, ty)
    ty -= 18

    c.setFont('Calibri-Bold', 20)
    c.setFillColor(DARK_NAVY)
    c.drawString(48, ty - 20, title_text)
    ty -= 32

    if subtitle_text:
        style = ParagraphStyle('st', fontName='Calibri', fontSize=10.5,
                               leading=15, textColor=GRAY)
        p = Paragraph(subtitle_text, style)
        pw, ph = p.wrap(W - 96, 60)
        p.drawOn(c, 48, ty - ph)
        ty -= ph + 10

    col_w = (W - 96 - 24) / 2
    col_right_x = 48 + col_w + 24

    callouts = callouts or []
    callout_total = 0
    for lbl, body in callouts:
        callout_total += measure_callout_height(body, W - 96) + 8

    bottom_limit = 30 + callout_total + (12 if callouts else 0)

    ty -= 20
    ty_col = ty

    act_natural = measure_bullet_list(activities, col_w, size=10.5, leading=15, item_gap=0)
    del_natural = measure_bullet_list(deliverables, col_w, size=10.5, leading=15, item_gap=0)
    natural_max = max(act_natural, del_natural)
    bullets_available = ty_col - bottom_limit
    longer_count = max(len(activities), len(deliverables))
    if longer_count > 1:
        gap = (bullets_available - natural_max) / (longer_count - 1)
        gap = max(6, min(gap, 18))
    else:
        gap = 8

    column_header(48, ty_col, 'Activities', col_w)
    ty_col -= 20
    bullet_list(48, ty_col, activities, col_w, size=10.5, leading=15, item_gap=gap)

    column_header(col_right_x, ty, 'Deliverables', col_w)
    bullet_list(col_right_x, ty - 20, deliverables, col_w, size=10.5, leading=15, item_gap=gap)

    callout_y = 30 + callout_total
    for lbl, body in callouts:
        h = callout_box(48, callout_y + measure_callout_height(body, W - 96),
                        W - 96, lbl, body)
        callout_y -= h + 8

    footer_light(client_name, page_label)


# ---------------------------------------------------------------------------
# Closing page
# ---------------------------------------------------------------------------
def closing_page(name, role, email, client_name=''):
    new_page()
    gradient_bg()
    try:
        c.saveState()
        c.setFillAlpha(0.12)
        c.drawImage(TRAJECTORY, W * 0.55, H * 0.05, width=W * 0.5, height=H * 0.9,
                    mask='auto', preserveAspectRatio=True)
        c.restoreState()
    except Exception:
        pass
    logo_top_left(LOGO_WM)

    c.setFont('Calibri-Bold', 32)
    c.setFillColor(WHITE_CLR)
    c.drawString(48, H / 2 + 30, 'Thank you.')
    draw_rect(48, H / 2 + 18, 50, 3, MINT)

    c.setFont('Calibri-Bold', 15)
    c.setFillColor(WHITE_CLR)
    c.drawString(48, H / 2 - 4, name)

    c.setFont('Calibri', 11)
    c.setFillColor(MINT)
    c.drawString(48, H / 2 - 22, role)

    c.setFont('Calibri', 11)
    c.setFillColor(Color(1, 1, 1, 0.7))
    c.drawString(48, H / 2 - 40, email)

    c.setFont('Calibri', 9)
    c.setFillColor(MINT)
    c.drawString(48, 30, 'Driving change. Elevating leaders.')

    c.setFont('Calibri', 7)
    c.setFillColor(Color(1, 1, 1, 0.35))
    c.drawString(48, 14, '© 2026 Metis Strategy LLC. All rights reserved. Proprietary & Confidential.')


# ---------------------------------------------------------------------------
# Shared primitives (consolidated from per-deck build.py files)
# ---------------------------------------------------------------------------
def section_title(text, y, size=20, color=None):
    """Draw a section title at top-of-page. Returns vertical space consumed."""
    c.setFont('Calibri-Bold', size)
    c.setFillColor(color or DARK_NAVY)
    c.drawString(48, y - size, text)
    return size + 4


def section_subtitle(text, y, width=None, size=10.5, color=None):
    """Draw a section subtitle under the title. Returns height consumed."""
    if not text:
        return 0
    width = width if width is not None else (W - 96)
    style = ParagraphStyle('st', fontName='Calibri', fontSize=size,
                           leading=size * 1.42, textColor=color or GRAY)
    p = Paragraph(text, style)
    pw, ph = p.wrap(width, 120)
    p.drawOn(c, 48, y - ph)
    return ph


def page_label(page_num, doc_label):
    """Standard right-aligned page label string."""
    return f'Page {page_num}  |  Metis Strategy  |  {doc_label}'


def pillar_card(x, y, w, h, title, purpose, bullets, band_color, text_color,
                band_h=40, title_size=10.5):
    """
    Pillar card used in 4-column pillar layouts.
    Rounded top band, square bottom; italic purpose + bullets beneath a thin rule.
    """
    draw_rect(x, y, w, h, LIGHT_BG)
    c.setStrokeColor(band_color)
    c.setLineWidth(1.2)
    c.rect(x, y, w, h, fill=0, stroke=1)

    c.setFillColor(band_color)
    c.roundRect(x, y + h - band_h, w, band_h, 6, fill=1, stroke=0)
    c.rect(x, y + h - band_h, w, band_h / 2, fill=1, stroke=0)

    size = title_size
    while size > 8 and c.stringWidth(title, 'Calibri-Bold', size) > w - 12:
        size -= 0.5
    c.setFont('Calibri-Bold', size)
    c.setFillColor(text_color)
    c.drawCentredString(x + w / 2, y + h - band_h / 2 - 3, title)

    inner_w = w - 20
    inner_x = x + 10
    content_top = y + h - band_h - 12

    style_p = ParagraphStyle('pp', fontName='Calibri-Italic', fontSize=9.5,
                             leading=13, textColor=DARK_NAVY, alignment=1)
    p = Paragraph(purpose, style_p)
    pw, ph = p.wrap(inner_w, 999)
    p.drawOn(c, inner_x, content_top - ph)
    cursor_y = content_top - ph - 10

    draw_rect(inner_x + inner_w * 0.30, cursor_y, inner_w * 0.40, 0.6, band_color)
    cursor_y -= 8

    style_b = ParagraphStyle('pb', fontName='Calibri', fontSize=9,
                             leading=12.5, textColor=DARK_GRAY)
    for b in bullets or []:
        p = Paragraph(f'• {b}', style_b)
        pw, ph = p.wrap(inner_w, 999)
        p.drawOn(c, inner_x, cursor_y - ph)
        cursor_y -= ph + 3


def pillars_page_block(pillars, top_y, bottom_y,
                       band_colors=None, text_colors=None,
                       col_gap=12):
    """
    Render up to 4 pillar cards in a row across the content width.
    Wraps pillar_card; use inside an already-laid-out page.
    """
    bands = band_colors or [MED_BLUE, MINT, DARK_TEAL, NEAR_BLACK]
    texts = text_colors or [WHITE_CLR, DARK_NAVY, WHITE_CLR, WHITE_CLR]
    n = min(len(pillars), 4)
    col_w = (W - 96 - col_gap * (n - 1)) / n if n else 0
    col_h = top_y - bottom_y
    for i, pillar in enumerate(pillars[:n]):
        cx = 48 + i * (col_w + col_gap)
        pillar_card(
            cx, bottom_y, col_w, col_h,
            pillar['title'], pillar.get('purpose', ''),
            pillar.get('bullets', []),
            bands[i % len(bands)], texts[i % len(texts)],
        )


# ---------------------------------------------------------------------------
# Modules overview — auto-pick grid layout by module count (Theme B)
# ---------------------------------------------------------------------------
def modules_overview_page(eyebrow_text, title_text, subtitle_text, modules,
                          callout=None, doc_label='', pg_num=None):
    """
    Render the 'engagement structure' page. Grid layout selected by module count:
      3 → single row of 3
      4 → 2x2
      5 → 3 top + 2 bottom (bottom row centered under the top row)
      6 → 3x2
      7+ → raises ValueError (consolidate first)
    """
    n = len(modules)
    if n < 3:
        raise ValueError(f'modules_overview_page expects 3+ modules, got {n}')
    if n > 6:
        raise ValueError(
            f'modules_overview_page expects 3–6 modules, got {n}. '
            f'Consolidate before rendering — the grid does not balance beyond 6.'
        )

    new_page()
    logo_top_right()

    ty = H - 48
    eyebrow(eyebrow_text, ty)
    ty -= 20
    ty -= section_title(title_text, ty)
    sub_h = section_subtitle(subtitle_text, ty, width=W - 96)
    ty -= sub_h + 16

    callout_reserved = 0
    if callout:
        callout_reserved = measure_callout_height(callout['body'], W - 96) + 20

    grid_top = ty
    grid_bottom = 30 + callout_reserved
    grid_h = grid_top - grid_bottom

    band_colors = [MED_BLUE, MINT, DARK_TEAL, NEAR_BLACK, MED_BLUE, DARK_TEAL]
    text_colors = [WHITE_CLR, DARK_NAVY, WHITE_CLR, WHITE_CLR, WHITE_CLR, WHITE_CLR]

    def _card(cx, cy, card_w, card_h, mod, color_i):
        draw_rect(cx, cy, card_w, card_h, LIGHT_BG)
        band_h = 38
        c.setFillColor(band_colors[color_i])
        c.roundRect(cx, cy + card_h - band_h, card_w, band_h, 6, fill=1, stroke=0)
        c.rect(cx, cy + card_h - band_h, card_w, band_h / 2, fill=1, stroke=0)
        c.setFont('Calibri-Bold', 11)
        c.setFillColor(text_colors[color_i])
        c.drawCentredString(cx + card_w / 2, cy + card_h - band_h / 2 - 3, mod['title'])
        padding = 14
        body_style = ParagraphStyle('mc', fontName='Calibri', fontSize=10,
                                    leading=14, textColor=DARK_GRAY)
        p = Paragraph(mod['body'], body_style)
        pw, ph = p.wrap(card_w - padding * 2, 999)
        p.drawOn(c, cx + padding, cy + card_h - band_h - 12 - ph)

    gutter = 20
    if n == 3:
        card_w = (W - 96 - gutter * 2) / 3
        card_h = min(grid_h, 260)
        cy = grid_bottom + (grid_h - card_h) / 2
        for i, mod in enumerate(modules):
            cx = 48 + i * (card_w + gutter)
            _card(cx, cy, card_w, card_h, mod, i)
    elif n == 4:
        card_w = (W - 96 - gutter) / 2
        card_h = (grid_h - gutter) / 2
        for i, mod in enumerate(modules):
            col = i % 2
            row = i // 2
            cx = 48 + col * (card_w + gutter)
            cy = grid_bottom + (1 - row) * (card_h + gutter)
            _card(cx, cy, card_w, card_h, mod, i)
    elif n == 5:
        card_w = (W - 96 - gutter * 2) / 3
        card_h = (grid_h - gutter) / 2
        for i, mod in enumerate(modules[:3]):
            cx = 48 + i * (card_w + gutter)
            cy = grid_bottom + card_h + gutter
            _card(cx, cy, card_w, card_h, mod, i)
        bottom_row = modules[3:]
        bottom_total_w = 2 * card_w + gutter
        bottom_start_x = 48 + (W - 96 - bottom_total_w) / 2
        for i, mod in enumerate(bottom_row):
            cx = bottom_start_x + i * (card_w + gutter)
            _card(cx, grid_bottom, card_w, card_h, mod, 3 + i)
    else:  # n == 6
        card_w = (W - 96 - gutter * 2) / 3
        card_h = (grid_h - gutter) / 2
        for i, mod in enumerate(modules):
            col = i % 3
            row = i // 3
            cx = 48 + col * (card_w + gutter)
            cy = grid_bottom + (1 - row) * (card_h + gutter)
            _card(cx, cy, card_w, card_h, mod, i)

    if callout:
        callout_h = measure_callout_height(callout['body'], W - 96)
        callout_box(48, 30 + callout_h, W - 96, callout['label'], callout['body'])

    footer_light(doc_label, page_label(pg_num, doc_label) if pg_num else None)


# ---------------------------------------------------------------------------
# Pattern: minicase pair page (Theme C)
# ---------------------------------------------------------------------------
_BADGE_COLOR_MAP = {
    'DARK_NAVY': DARK_NAVY,
    'MED_BLUE': MED_BLUE,
    'MINT': MINT,
    'DARK_TEAL': DARK_TEAL,
    'NEAR_BLACK': NEAR_BLACK,
}


def minicase_pair_page(eyebrow_text, title_text, subtitle_text, cases,
                       doc_label='', pg_num=None):
    """
    Two side-by-side minicase cards. Each case: {badge, big_number, number_label,
    product_title, body, badge_color}. badge_color is a key in _BADGE_COLOR_MAP
    or a ReportLab Color.
    """
    new_page()
    logo_top_right()
    ty = H - 48
    eyebrow(eyebrow_text, ty)
    ty -= 20
    ty -= section_title(title_text, ty)
    sub_h = section_subtitle(subtitle_text, ty, width=W - 96)
    ty -= sub_h + 20

    card_gap = 24
    card_w = (W - 96 - card_gap) / 2
    card_bottom = 48
    card_h = ty - card_bottom

    for i, case in enumerate(cases[:2]):
        cx = 48 + i * (card_w + card_gap)
        cy = card_bottom
        draw_rect(cx, cy, card_w, card_h, LIGHT_BG)
        bc = case.get('badge_color', 'DARK_NAVY')
        band_color = _BADGE_COLOR_MAP.get(bc, bc) if isinstance(bc, str) else bc
        c.setStrokeColor(band_color)
        c.setLineWidth(1.5)
        c.rect(cx, cy, card_w, card_h, fill=0, stroke=1)

        badge_h = 34
        c.setFillColor(band_color)
        c.roundRect(cx, cy + card_h - badge_h, card_w, badge_h, 6, fill=1, stroke=0)
        c.rect(cx, cy + card_h - badge_h, card_w, badge_h / 2, fill=1, stroke=0)
        c.setFont('Calibri-Bold', 9.5)
        txt_color = DARK_NAVY if band_color == MINT else WHITE_CLR
        c.setFillColor(txt_color)
        c.drawCentredString(cx + card_w / 2, cy + card_h - badge_h / 2 - 3,
                            case['badge'].upper())

        inner_w = card_w - 32
        inner_x = cx + 16
        cursor_y = cy + card_h - badge_h - 24

        big_num = case['big_number']
        num_size = 44
        while num_size > 24 and c.stringWidth(big_num, 'Calibri-Bold', num_size) > inner_w:
            num_size -= 1
        c.setFont('Calibri-Bold', num_size)
        c.setFillColor(MINT)
        c.drawCentredString(cx + card_w / 2, cursor_y - num_size + 4, big_num)
        cursor_y -= num_size + 18

        c.setFont('Calibri', 8.5)
        c.setFillColor(GRAY)
        c.drawCentredString(cx + card_w / 2, cursor_y, case['number_label'].upper())
        cursor_y -= 16

        draw_rect(inner_x + inner_w * 0.30, cursor_y, inner_w * 0.40, 0.6, band_color)
        cursor_y -= 14

        c.setFont('Calibri-Bold', 12)
        c.setFillColor(DARK_NAVY)
        c.drawCentredString(cx + card_w / 2, cursor_y, case['product_title'])
        cursor_y -= 20

        body_style = ParagraphStyle('mcb', fontName='Calibri', fontSize=10.5,
                                    leading=14.8, textColor=DARK_GRAY, alignment=1)
        p = Paragraph(case['body'], body_style)
        pw, ph = p.wrap(inner_w, 999)
        p.drawOn(c, inner_x, cursor_y - ph)

    footer_light(doc_label, page_label(pg_num, doc_label) if pg_num else None)


# ---------------------------------------------------------------------------
# Pattern: signature visual page (Theme C)
# ---------------------------------------------------------------------------
def signature_visual_page(eyebrow_text, title_text, subtitle_text, image_path,
                          callout_label=None, callout_body=None,
                          doc_label='', pg_num=None):
    """
    Full-width hero image with header + optional bottom callout.
    The image is the thesis-anchor visual; crop it in advance to remove any
    source title/footer before passing.
    """
    new_page()
    logo_top_right()
    ty = H - 48
    eyebrow(eyebrow_text, ty)
    ty -= 20
    ty -= section_title(title_text, ty)
    sub_h = section_subtitle(subtitle_text, ty, width=W - 96)
    ty -= sub_h + 16

    if callout_body:
        callout_h_ = measure_callout_height(callout_body, W - 96)
        bottom_limit = 30 + callout_h_ + 14
    else:
        bottom_limit = 48

    img_top = ty
    avail_h = img_top - bottom_limit
    avail_w = W - 96

    try:
        pil_img = PILImage.open(image_path)
        aspect = pil_img.size[0] / pil_img.size[1]
    except Exception:
        aspect = 2000 / 865

    img_w = avail_w
    img_h = img_w / aspect
    if img_h > avail_h:
        img_h = avail_h
        img_w = img_h * aspect
    img_x = 48 + (avail_w - img_w) / 2
    img_y = bottom_limit + (avail_h - img_h) / 2

    try:
        c.drawImage(image_path, img_x, img_y, width=img_w, height=img_h,
                    mask='auto', preserveAspectRatio=True)
    except Exception as e:
        print(f'  WARNING: signature_visual_page image: {e}')
        draw_rect(img_x, img_y, img_w, img_h, LIGHT_BG)

    if callout_body:
        h_ = measure_callout_height(callout_body, W - 96)
        callout_box(48, 30 + h_, W - 96, callout_label or 'APPLICATION', callout_body)

    footer_light(doc_label, page_label(pg_num, doc_label) if pg_num else None)


# ---------------------------------------------------------------------------
# Pattern: process timeline page (Theme C)
# ---------------------------------------------------------------------------
def process_timeline_page(eyebrow_text, title_text, subtitle_text, stages,
                          callout_label=None, callout_body=None,
                          doc_label='', pg_num=None):
    """
    Horizontal numbered-stage timeline. stages: list of {title, body}. 3–6 works best.
    Renders as a connected row of numbered circles with title + short body below.
    """
    new_page()
    logo_top_right()
    ty = H - 48
    eyebrow(eyebrow_text, ty)
    ty -= 20
    ty -= section_title(title_text, ty)
    sub_h = section_subtitle(subtitle_text, ty, width=W - 96)
    ty -= sub_h + 30

    if callout_body:
        callout_h_ = measure_callout_height(callout_body, W - 96)
        bottom_limit = 30 + callout_h_ + 20
    else:
        bottom_limit = 48

    n = max(1, len(stages))
    col_gap = 16
    col_w = (W - 96 - col_gap * (n - 1)) / n
    badge_r = 18
    timeline_y = ty - badge_r

    draw_rect(48 + badge_r, timeline_y, W - 96 - badge_r * 2, 2, MINT)

    for i, stage in enumerate(stages):
        col_x = 48 + i * (col_w + col_gap)
        center_x = col_x + col_w / 2
        c.setFillColor(DARK_NAVY)
        c.circle(center_x, timeline_y + 1, badge_r, fill=1, stroke=0)
        c.setFont('Calibri-Bold', 14)
        c.setFillColor(MINT)
        c.drawCentredString(center_x, timeline_y - 4, str(i + 1))

        title_y = timeline_y - badge_r - 14
        c.setFont('Calibri-Bold', 11)
        c.setFillColor(DARK_NAVY)
        c.drawCentredString(center_x, title_y, stage['title'])

        body_style = ParagraphStyle('pt', fontName='Calibri', fontSize=9,
                                    leading=12.5, textColor=DARK_GRAY, alignment=1)
        p = Paragraph(stage.get('body', ''), body_style)
        pw, ph = p.wrap(col_w - 8, 200)
        p.drawOn(c, col_x + 4, title_y - 8 - ph)

    if callout_body:
        h_ = measure_callout_height(callout_body, W - 96)
        callout_box(48, 30 + h_, W - 96, callout_label or 'HOW THIS COMES TOGETHER', callout_body)

    footer_light(doc_label, page_label(pg_num, doc_label) if pg_num else None)


# ---------------------------------------------------------------------------
# Pattern: quote-led page (Theme C)
# ---------------------------------------------------------------------------
def quote_led_page(eyebrow_text, quote, attribution=None, context=None,
                   doc_label='', pg_num=None):
    """
    Hero pull quote, centered vertically, with optional attribution and
    a short supporting paragraph below. Use sparingly — reserve for lines
    that carry the thesis.
    """
    new_page()
    logo_top_right()
    ty = H - 48
    if eyebrow_text:
        eyebrow(eyebrow_text, ty)

    quote_style = ParagraphStyle('qq', fontName='Calibri-Bold', fontSize=24,
                                 leading=32, textColor=DARK_NAVY, alignment=0)
    p = Paragraph(f'<i>&ldquo;{quote}&rdquo;</i>', quote_style)
    qw, qh = p.wrap(W - 120, 400)

    block_top = H / 2 + qh / 2 + 10
    draw_rect(48, block_top + 8, 80, 4, MINT)
    p.drawOn(c, 60, block_top - qh)

    y_cursor = block_top - qh - 18
    if attribution:
        c.setFont('Calibri-Bold', 11)
        c.setFillColor(DARK_NAVY)
        c.drawString(60, y_cursor, f'— {attribution}')
        y_cursor -= 22

    if context:
        ctx_style = ParagraphStyle('qc', fontName='Calibri', fontSize=10.5,
                                   leading=15, textColor=DARK_GRAY)
        p2 = Paragraph(context, ctx_style)
        pw, ph2 = p2.wrap(W - 120, 180)
        p2.drawOn(c, 60, y_cursor - ph2)

    footer_light(doc_label, page_label(pg_num, doc_label) if pg_num else None)


# ---------------------------------------------------------------------------
# Pattern: comparative two-column page (Theme C)
# ---------------------------------------------------------------------------
def comparative_page(eyebrow_text, title_text, subtitle_text,
                     left, right, doc_label='', pg_num=None):
    """
    Side-by-side comparison. left/right: {header, bullets: [...]}. Use for
    before/after, our-way/traditional, old/new framings.
    """
    new_page()
    logo_top_right()
    ty = H - 48
    eyebrow(eyebrow_text, ty)
    ty -= 20
    ty -= section_title(title_text, ty)
    sub_h = section_subtitle(subtitle_text, ty, width=W - 96)
    ty -= sub_h + 22

    gap = 24
    col_w = (W - 96 - gap) / 2
    col_bottom = 48
    col_h = ty - col_bottom

    configs = [
        (48, left, GRAY, LIGHT_BG, DARK_GRAY),
        (48 + col_w + gap, right, DARK_NAVY, TEAL_LIGHT, DARK_NAVY),
    ]

    for cx, col_data, header_color, fill_color, body_color in configs:
        draw_rect(cx, col_bottom, col_w, col_h, fill_color)
        header_h = 36
        draw_rect(cx, col_bottom + col_h - header_h, col_w, header_h, header_color)
        c.setFont('Calibri-Bold', 11)
        c.setFillColor(WHITE_CLR)
        c.drawCentredString(cx + col_w / 2, col_bottom + col_h - header_h / 2 - 3,
                            col_data['header'].upper())

        inner_x = cx + 16
        inner_y_top = col_bottom + col_h - header_h - 14
        bullets = col_data.get('bullets', [])
        bstyle = ParagraphStyle('cmp', fontName='Calibri', fontSize=10.5,
                                leading=15, textColor=body_color)
        cursor = inner_y_top
        for b in bullets:
            p = Paragraph(f'• {b}', bstyle)
            pw, ph = p.wrap(col_w - 32, 400)
            p.drawOn(c, inner_x, cursor - ph)
            cursor -= ph + 8

    footer_light(doc_label, page_label(pg_num, doc_label) if pg_num else None)


# ---------------------------------------------------------------------------
# Pattern: metric-dense page (Theme C)
# ---------------------------------------------------------------------------
def metric_dense_page(eyebrow_text, title_text, subtitle_text, metrics,
                      narrative=None, doc_label='', pg_num=None):
    """
    4–6 metric cards across a band, with an explanatory narrative paragraph below.
    Each metric: {number, label}.
    """
    new_page()
    logo_top_right()
    ty = H - 48
    eyebrow(eyebrow_text, ty)
    ty -= 20
    ty -= section_title(title_text, ty)
    sub_h = section_subtitle(subtitle_text, ty, width=W - 96)
    ty -= sub_h + 28

    n = len(metrics)
    gap = 12
    card_w = (W - 96 - gap * (n - 1)) / n
    card_h = 110
    for i, m in enumerate(metrics):
        mx = 48 + i * (card_w + gap)
        metric_card(mx, ty - card_h, card_w, card_h, m['number'], m['label'])

    if narrative:
        nstyle = ParagraphStyle('nm', fontName='Calibri', fontSize=11,
                                leading=16, textColor=DARK_GRAY)
        p = Paragraph(narrative, nstyle)
        pw, ph = p.wrap(W - 96, 300)
        p.drawOn(c, 48, ty - card_h - 24 - ph)

    footer_light(doc_label, page_label(pg_num, doc_label) if pg_num else None)
