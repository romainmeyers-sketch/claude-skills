"""
starter_build.py — DEPRECATED. Use starter_buyer.py or starter_capabilities.py.

This legacy script uses the old nested-keys YAML format (cover:, problem:,
module_a:, etc.). It is preserved so existing client YAMLs still build.

For new proposals, use:
  - starter_buyer.py        — named prospect, CTA, procurement step
  - starter_capabilities.py — reusable marketing asset, no prospect
  - starter_casestudy.py    — single engagement deep dive

The new starters use a flat `sections:` list with `type` + `intent` per page.
See references/narrative-planning.md for the consultant workflow and
references/content-rules.md for the intent-per-page rule.

Run (legacy format only):
  PYTHON="C:/Users/Andrew Krusell/AppData/Local/Programs/Python/Python312/python.exe"
  "$PYTHON" starter_build.py
"""
import sys as _sys_deprecation
print('DEPRECATION: starter_build.py uses the old YAML schema. '
      'New proposals should use starter_buyer.py or starter_capabilities.py.',
      file=_sys_deprecation.stderr)

import sys
import os
import yaml
from datetime import date
from reportlab.pdfgen import canvas as rl_canvas

# ---------------------------------------------------------------------------
# Path setup — add scripts/ to import path so helpers resolves
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import helpers as H
from helpers import (
    W, H as PH,
    DARK_NAVY, MED_BLUE, MINT, GRAY, DARK_GRAY, LIGHT_BG, TEAL_LIGHT, WHITE_CLR,
    LOGO_BM, LOGO_WM, TRAJECTORY, NEXUS, ENERGY, SNGL_ARROW,
    register_fonts, new_page, gradient_bg, place_image,
    logo_top_left, logo_top_right, draw_rect, eyebrow,
    section_divider, activities_deliverables_page, closing_page,
    callout_box, metric_card, numbered_item, column_header, bullet_list,
    pull_quote, footer_light, footer_dark,
)
from reportlab.lib.colors import Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

# ---------------------------------------------------------------------------
# Configuration — edit these
# ---------------------------------------------------------------------------
COPY_FILE   = 'example-proposal-copy.yaml'  # rename to your client YAML
CLIENT_NAME = 'Client Name'                  # used in footer
TODAY       = date.today().strftime('%Y-%m-%d')
OUTPUT_DIR  = '_working'
OUTPUT_FILE = f'{OUTPUT_DIR}/{CLIENT_NAME.lower().replace(" ", "-")}-proposal-{TODAY}.pdf'

# ---------------------------------------------------------------------------
# Load copy
# ---------------------------------------------------------------------------
with open(COPY_FILE, 'r', encoding='utf-8') as f:
    COPY = yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)
register_fonts()

c = rl_canvas.Canvas(OUTPUT_FILE, pagesize=(W, PH))
H.c = c  # inject canvas into helpers


# ---------------------------------------------------------------------------
# Page 1: Cover
# ---------------------------------------------------------------------------
c.setPageSize((W, PH))
gradient_bg()
try:
    c.saveState()
    c.setFillAlpha(0.15)
    c.drawImage(H.PHOTO_DIR + 'pexels-pixabay-63320-bw.jpg', 0, 0, width=W, height=PH)
    c.restoreState()
except Exception:
    pass
try:
    c.saveState()
    c.setFillAlpha(0.20)
    c.drawImage(TRAJECTORY, W * 0.58, -PH * 0.1, width=W * 0.55, height=PH * 1.2,
                mask='auto', preserveAspectRatio=True)
    c.restoreState()
except Exception:
    pass
logo_top_left(LOGO_WM)
c.setFont('Calibri-Bold', 8.5)
c.setFillColor(MINT)
c.drawString(48, 130, COPY['cover']['eyebrow'].upper())
c.setFont('Calibri-Bold', 32)
c.setFillColor(WHITE_CLR)
c.drawString(48, 88, COPY['cover']['title_line_1'])
c.drawString(48, 50, COPY['cover']['title_line_2'])
c.setFont('Calibri-Light', 12)
c.setFillColor(Color(1, 1, 1, 0.75))
c.drawString(48, 20, COPY['cover']['prepared_for'])
c.setFont('Calibri', 7)
c.setFillColor(Color(1, 1, 1, 0.35))
c.drawRightString(W - 48, 10, 'Proprietary & Confidential')
footer_dark()


# ---------------------------------------------------------------------------
# Page 2: Problem framing (photo-left + numbered items + metric cards)
# ---------------------------------------------------------------------------
new_page()
photo_w = W * 0.40
try:
    c.drawImage(H.PHOTO_DIR + 'pexels-divinetechygirl-1181311-bw.jpg',
                0, 0, width=photo_w, height=PH)
    c.setFillColor(Color(0, 0, 0, 0.50))
    c.rect(0, 0, photo_w, PH, fill=1, stroke=0)
except Exception:
    draw_rect(0, 0, photo_w, PH, DARK_NAVY)
logo_top_right()
content_x = photo_w + 24
content_w = W - content_x - 48
ty = PH - 48
eyebrow(COPY['problem']['eyebrow'], ty, x=content_x)
ty -= 18
c.setFont('Calibri-Bold', 20)
c.setFillColor(DARK_NAVY)
c.drawString(content_x, ty - 20, COPY['problem']['title'])
ty -= 34

pull_h = pull_quote(content_x, ty, COPY['problem']['pull_quote'], content_w)
ty -= pull_h + 8

items = COPY['problem']['numbered_items']
for i, item in enumerate(items):
    h = numbered_item(content_x, ty, i + 1, item['title'], item['body'], content_w)
    ty -= h + 4

metrics = COPY['problem']['metrics']
metric_w = content_w / len(metrics)
for i, m in enumerate(metrics):
    mx = content_x + i * metric_w
    metric_card(mx, 28, metric_w - 8, 56, m['number'], m['label'])

footer_light(CLIENT_NAME, f'Page 2 | {CLIENT_NAME} Proposal')


# ---------------------------------------------------------------------------
# Page 3: Our Approach divider
# ---------------------------------------------------------------------------
section_divider(
    COPY['approach_divider']['title'],
    COPY['approach_divider'].get('subtitle'),
    device_path=NEXUS,
    client_name=CLIENT_NAME,
    page_label=f'Page 3 | {CLIENT_NAME} Proposal',
)


# ---------------------------------------------------------------------------
# Page 4: Engagement overview (2x2 module cards)
# ---------------------------------------------------------------------------
new_page()
logo_top_right()
ty = PH - 48
eyebrow(COPY['modules_overview']['eyebrow'], ty)
ty -= 18
c.setFont('Calibri-Bold', 20)
c.setFillColor(DARK_NAVY)
c.drawString(48, ty - 20, COPY['modules_overview']['title'])
ty -= 38

modules = COPY['modules_overview']['modules']
card_w = (W - 96 - 24) / 2
card_h = 140
padding = 12
band_colors = [MED_BLUE, MINT, Color(0x1a/255, 0x8a/255, 0x7a/255), Color(0x1a/255, 0x20/255, 0x40/255)]
text_colors  = [WHITE_CLR, DARK_NAVY, WHITE_CLR, WHITE_CLR]

for i, mod in enumerate(modules):
    col = i % 2
    row = i // 2
    cx = 48 + col * (card_w + 24)
    cy = ty - (row + 1) * (card_h + 12)
    draw_rect(cx, cy, card_w, card_h, LIGHT_BG)
    c.roundRect(cx, cy + card_h - 38, card_w, 38, 6, fill=1, stroke=0)
    c.setFillColor(band_colors[i])
    c.roundRect(cx, cy + card_h - 38, card_w, 38, 6, fill=1, stroke=0)
    c.rect(cx, cy + card_h - 38, card_w, 19, fill=1, stroke=0)
    c.setFont('Calibri-Bold', 11)
    c.setFillColor(text_colors[i])
    c.drawCentredString(cx + card_w / 2, cy + card_h - 22, mod['title'])
    style = ParagraphStyle('mc', fontName='Calibri', fontSize=9.5, leading=13.5,
                           textColor=DARK_GRAY)
    p = Paragraph(mod['body'], style)
    pw, ph = p.wrap(card_w - padding * 2, 999)
    p.drawOn(c, cx + padding, cy + card_h - 44 - ph)

if COPY['modules_overview'].get('callout'):
    co = COPY['modules_overview']['callout']
    callout_box(48, 100, W - 96, co['label'], co['body'])

footer_light(CLIENT_NAME, f'Page 4 | {CLIENT_NAME} Proposal')


# ---------------------------------------------------------------------------
# Module A divider + overview (pages 5–6)
# ---------------------------------------------------------------------------
section_divider(
    COPY['module_a_divider']['title'],
    COPY['module_a_divider'].get('subtitle'),
    client_name=CLIENT_NAME,
    page_label=f'Page 5 | {CLIENT_NAME} Proposal',
)

activities_deliverables_page(
    eyebrow_text=COPY['module_a']['eyebrow'],
    title_text=COPY['module_a']['title'],
    subtitle_text=COPY['module_a'].get('subtitle'),
    activities=COPY['module_a']['activities'],
    deliverables=COPY['module_a']['deliverables'],
    callouts=[(co['label'], co['body']) for co in COPY['module_a'].get('callouts', [])],
    client_name=CLIENT_NAME,
    page_label=f'Page 6 | {CLIENT_NAME} Proposal',
)

# Add pages for Modules B, C, D following the same pattern...
# Each module: section_divider() + activities_deliverables_page()


# ---------------------------------------------------------------------------
# Proof Points divider + case studies
# ---------------------------------------------------------------------------
section_divider(
    COPY['proof_divider']['title'],
    COPY['proof_divider'].get('subtitle'),
    client_name=CLIENT_NAME,
    page_label=f'Page 15 | {CLIENT_NAME} Proposal',
)

# Add case study pages following photo-left pattern (page-patterns.md #3)...


# ---------------------------------------------------------------------------
# Next Steps
# ---------------------------------------------------------------------------
new_page()
logo_top_right()
ty = PH - 48
eyebrow(COPY['next_steps']['eyebrow'], ty)
ty -= 18
c.setFont('Calibri-Bold', 20)
c.setFillColor(DARK_NAVY)
c.drawString(48, ty - 20, COPY['next_steps']['title'])
ty -= 38

steps = COPY['next_steps']['steps']
step_w = (W - 96 - 32) / 3
for i, step in enumerate(steps):
    sx = 48 + i * (step_w + 16)
    draw_rect(sx, 100, step_w, ty - 108, LIGHT_BG)
    draw_rect(sx, ty - 6, step_w, 6, MINT)
    c.setFont('Calibri-Bold', 22)
    c.setFillColor(MINT)
    c.drawString(sx + 12, ty - 40, str(i + 1))
    c.setFont('Calibri-Bold', 11)
    c.setFillColor(DARK_NAVY)
    c.drawString(sx + 12, ty - 58, step['title'])
    style = ParagraphStyle('ns', fontName='Calibri', fontSize=9.5, leading=13.5,
                           textColor=DARK_GRAY)
    p = Paragraph(step['body'], style)
    p.wrap(step_w - 24, 999)
    p.drawOn(c, sx + 12, ty - 78 - 40)

if COPY['next_steps'].get('commitment'):
    co = COPY['next_steps']['commitment']
    callout_box(48, 100, W - 96, co['label'], co['body'])

footer_light(CLIENT_NAME, f'Page {len(c._pages)+1} | {CLIENT_NAME} Proposal')


# ---------------------------------------------------------------------------
# Closing page
# ---------------------------------------------------------------------------
closing_page(
    name=COPY['closing']['name'],
    role=COPY['closing']['role'],
    email=COPY['closing']['email'],
    client_name=CLIENT_NAME,
)


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
c.save()
print(f'\nBuilt: {OUTPUT_FILE}')
print(f'Pages: {len(c._pages)+1}')
print(f'\nNext: python scripts/verify.py --pdf {OUTPUT_FILE} --mode all --out verify/')
