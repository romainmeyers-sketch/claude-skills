"""
starter_buyer.py — Starter build script for a named-buyer Metis proposal PDF.

Buyer mode: named prospect, prepared_for line, problem framing from the
buyer's own transcript language, next-steps page with commitment callout.

Uses the same flat `sections:` dispatch as starter_capabilities.py but with
buyer-mode close discipline (explicit CTA, kickoff week, procurement step).

Authoring flow:
  1. Fill in scripts/_brief_template.md first. Buyer mode: audience is a
     named person; mirror transcript language in titles and pull quotes.
     Do not start YAML before the brief is complete.
  2. Copy `starter_buyer_copy.yaml` to your project folder and rename.
  3. Edit the sections list. Each section has a `type` matching one of the
     RENDERERS below. Content pages must declare `intent:`.
  4. Run this script. Verify with `scripts/verify.py --mode all`.
  5. Run the polish pass (see references/polish-pass.md) before shipping.

Buyer mode expects at minimum: cover (with prepared_for), problem_framing,
at least one module block, next_steps (3 steps + commitment), closing.

Run:
  PYTHON="C:/Users/Andrew Krusell/AppData/Local/Programs/Python/Python312/python.exe"
  "$PYTHON" starter_buyer.py [path/to/copy.yaml]
"""
import os
import sys
import yaml
from datetime import date

from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import helpers as H
from helpers import (
    W, H as PH,
    DARK_NAVY, MED_BLUE, MINT, DARK_TEAL, NEAR_BLACK, GRAY, DARK_GRAY,
    LIGHT_BG, TEAL_LIGHT, WHITE_CLR,
    LOGO_BM, LOGO_WM, TRAJECTORY, NEXUS, PHOTO_DIR,
    register_fonts, new_page, gradient_bg,
    logo_top_left, logo_top_right, draw_rect, eyebrow,
    section_divider, activities_deliverables_page,
    modules_overview_page, pillars_page_block,
    minicase_pair_page, signature_visual_page, process_timeline_page,
    quote_led_page, comparative_page, metric_dense_page,
    callout_box, metric_card, numbered_item,
    pull_quote, footer_light,
    measure_body_text, measure_callout_height, distribute_y_positions,
    section_title, section_subtitle, page_label, closing_page,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
COPY_FILE = sys.argv[1] if len(sys.argv) > 1 else 'starter_buyer_copy.yaml'

with open(COPY_FILE, 'r', encoding='utf-8') as f:
    COPY = yaml.safe_load(f)

CLIENT_NAME = COPY.get('client_name', 'Client')
TODAY = date.today().strftime('%Y-%m-%d')
OUTPUT_FILE = COPY.get('output_file') or \
    f'{CLIENT_NAME.replace(" ", "-")}-Proposal_{TODAY}.pdf'

register_fonts()
c = rl_canvas.Canvas(OUTPUT_FILE, pagesize=(W, PH))
H.c = c


# ---------------------------------------------------------------------------
# Renderers — one per content_type. Same shapes as starter_capabilities.
# ---------------------------------------------------------------------------
def render_cover(s, pg):
    c.setPageSize((W, PH))
    gradient_bg()
    if s.get('photo'):
        try:
            c.saveState()
            c.setFillAlpha(0.15)
            c.drawImage(s['photo'], 0, 0, width=W, height=PH, mask=None)
            c.restoreState()
        except Exception as e:
            print(f'  WARNING: cover photo: {e}')
    try:
        c.saveState()
        c.setFillAlpha(0.22)
        c.drawImage(TRAJECTORY, W * 0.58, -PH * 0.1,
                    width=W * 0.55, height=PH * 1.2,
                    mask='auto', preserveAspectRatio=True)
        c.restoreState()
    except Exception:
        pass
    logo_top_left(LOGO_WM)
    c.setFont('Calibri-Bold', 9)
    c.setFillColor(MINT)
    c.drawString(48, 130, s['eyebrow'].upper())
    c.setFont('Calibri-Bold', 32)
    c.setFillColor(WHITE_CLR)
    c.drawString(48, 88, s['title_line_1'])
    c.drawString(48, 50, s['title_line_2'])
    c.setFont('Calibri-Light', 12)
    c.setFillColor(Color(1, 1, 1, 0.75))
    c.drawString(48, 20, s.get('prepared_for') or s.get('tagline') or '')
    c.setFont('Calibri', 7)
    c.setFillColor(Color(1, 1, 1, 0.35))
    c.drawRightString(W - 48, 10,
                      'Proprietary & Confidential  |  © 2026 Metis Strategy LLC')


def render_problem_framing(s, pg):
    new_page()
    photo_w = W * 0.40
    if s.get('photo'):
        try:
            c.drawImage(s['photo'], 0, 0, width=photo_w, height=PH, mask=None)
            c.setFillColor(Color(0, 0, 0, 0.50))
            c.rect(0, 0, photo_w, PH, fill=1, stroke=0)
        except Exception:
            draw_rect(0, 0, photo_w, PH, DARK_NAVY)
    else:
        draw_rect(0, 0, photo_w, PH, DARK_NAVY)

    logo_top_right()
    content_x = photo_w + 24
    content_w = W - content_x - 48
    ty = PH - 48
    eyebrow(s['eyebrow'], ty, x=content_x)
    ty -= 18
    c.setFont('Calibri-Bold', 20)
    c.setFillColor(DARK_NAVY)
    c.drawString(content_x, ty - 20, s['title'])
    ty -= 34

    pull_h = pull_quote(content_x, ty, s['pull_quote'], content_w)
    ty -= pull_h + 10

    items = s['numbered_items']
    items_bottom_limit = 100
    item_heights = [
        10.5 + 4 + measure_body_text(item['body'], content_w - 34,
                                     size=9.5, leading=13.5)
        for item in items
    ]
    positions = distribute_y_positions(items, ty, items_bottom_limit, item_heights)
    for i, item in enumerate(items):
        numbered_item(content_x, positions[i], i + 1,
                      item['title'], item['body'], content_w)

    metrics = s['metrics']
    metric_w = content_w / len(metrics) - 8
    for i, m in enumerate(metrics):
        mx = content_x + i * (metric_w + 12)
        metric_card(mx, 28, metric_w, 56, m['number'], m['label'])

    footer_light(CLIENT_NAME, page_label(pg, CLIENT_NAME))


def render_section_divider(s, pg):
    section_divider(
        s['title'],
        s.get('subtitle'),
        device_path=NEXUS if s.get('device_path') == 'nexus' else TRAJECTORY,
        client_name=CLIENT_NAME,
        page_label=page_label(pg, CLIENT_NAME),
        style=s.get('style', 'device'),
        number_text=s.get('number_text'),
        photo_path=s.get('photo_path'),
    )


def render_modules_overview(s, pg):
    modules_overview_page(
        s['eyebrow'], s['title'], s.get('subtitle'),
        s['modules'],
        callout=s.get('callout'),
        doc_label=CLIENT_NAME, pg_num=pg,
    )


def render_activities_deliverables(s, pg):
    activities_deliverables_page(
        eyebrow_text=s['eyebrow'],
        title_text=s['title'],
        subtitle_text=s.get('subtitle'),
        activities=s['activities'],
        deliverables=s['deliverables'],
        callouts=[(co['label'], co['body']) for co in s.get('callouts', [])],
        client_name=CLIENT_NAME,
        page_label=page_label(pg, CLIENT_NAME),
    )


def render_pillars(s, pg):
    new_page()
    logo_top_right()
    ty = PH - 48
    eyebrow(s['eyebrow'], ty)
    ty -= 20
    ty -= section_title(s['title'], ty)
    sub_h = section_subtitle(s.get('subtitle'), ty, width=W - 96)
    ty -= sub_h + 18
    reserved = 0
    if s.get('callout'):
        reserved = measure_callout_height(s['callout']['body'], W - 96) + 14
    pillars_page_block(s['pillars'], ty, 40 + reserved)
    if s.get('callout'):
        h = measure_callout_height(s['callout']['body'], W - 96)
        callout_box(48, 30 + h, W - 96, s['callout']['label'], s['callout']['body'])
    footer_light(CLIENT_NAME, page_label(pg, CLIENT_NAME))


def render_timeline(s, pg):
    callout = s.get('callout') or {}
    process_timeline_page(
        s['eyebrow'], s['title'], s.get('subtitle'),
        s['stages'],
        callout_label=callout.get('label'),
        callout_body=callout.get('body'),
        doc_label=CLIENT_NAME, pg_num=pg,
    )


def render_signature_image(s, pg):
    callout = s.get('callout') or {}
    signature_visual_page(
        s['eyebrow'], s['title'], s.get('subtitle'),
        s['image'],
        callout_label=callout.get('label'),
        callout_body=callout.get('body'),
        doc_label=CLIENT_NAME, pg_num=pg,
    )


def render_quote(s, pg):
    quote_led_page(
        s.get('eyebrow', ''), s['quote'],
        attribution=s.get('attribution'),
        context=s.get('context'),
        doc_label=CLIENT_NAME, pg_num=pg,
    )


def render_comparative(s, pg):
    comparative_page(
        s['eyebrow'], s['title'], s.get('subtitle'),
        s['left'], s['right'],
        doc_label=CLIENT_NAME, pg_num=pg,
    )


def render_metric_dense(s, pg):
    metric_dense_page(
        s['eyebrow'], s['title'], s.get('subtitle'),
        s['metrics'],
        narrative=s.get('narrative'),
        doc_label=CLIENT_NAME, pg_num=pg,
    )


def render_minicase_pair(s, pg):
    minicase_pair_page(
        s['eyebrow'], s['title'], s.get('subtitle'),
        s['cases'],
        doc_label=CLIENT_NAME, pg_num=pg,
    )


def render_proof_overview(s, pg):
    new_page()
    photo_w = W * 0.40
    if s.get('photo'):
        try:
            c.drawImage(s['photo'], 0, 0, width=photo_w, height=PH, mask=None)
            c.setFillColor(Color(0, 0, 0, 0.55))
            c.rect(0, 0, photo_w, PH, fill=1, stroke=0)
        except Exception:
            draw_rect(0, 0, photo_w, PH, DARK_NAVY)
    else:
        draw_rect(0, 0, photo_w, PH, DARK_NAVY)

    c.setFont('Calibri-Bold', 44)
    c.setFillColor(MINT)
    c.drawString(30, PH - 170, s.get('photo_big_line_1', ''))
    c.setFont('Calibri-Light', 12)
    c.setFillColor(WHITE_CLR)
    c.drawString(30, PH - 195, s.get('photo_big_line_2', ''))
    draw_rect(30, PH - 215, 40, 2, MINT)
    c.setFont('Calibri-Bold', 10)
    c.setFillColor(WHITE_CLR)
    c.drawString(30, PH - 235, s.get('photo_subtitle', ''))

    logo_top_right()
    content_x = photo_w + 24
    content_w = W - content_x - 48
    ty = PH - 48
    eyebrow(s['eyebrow'], ty, x=content_x)
    ty -= 20
    c.setFont('Calibri-Bold', 20)
    c.setFillColor(DARK_NAVY)
    c.drawString(content_x, ty - 20, s['title'])
    ty -= 36

    ctx_style = ParagraphStyle('ctx', fontName='Calibri', fontSize=10.5,
                               leading=14.5, textColor=DARK_GRAY)
    p = Paragraph(s['context'], ctx_style)
    pw, ph = p.wrap(content_w, 80)
    p.drawOn(c, content_x, ty - ph)
    ty -= ph + 14

    callout_h = measure_callout_height(s['relevance_body'], content_w)
    metrics_h = 56
    metrics_y = 30 + callout_h + 10 + metrics_h
    phases_bottom = metrics_y + 16

    phases = s['phases']
    phase_h_each = (ty - phases_bottom) / len(phases)
    for i, phase in enumerate(phases):
        py = ty - (i + 1) * phase_h_each
        badge_r = 10
        c.setFillColor(MINT)
        c.circle(content_x + badge_r, py + phase_h_each / 2 + 2, badge_r, fill=1, stroke=0)
        c.setFont('Calibri-Bold', 9)
        c.setFillColor(DARK_NAVY)
        c.drawCentredString(content_x + badge_r, py + phase_h_each / 2 - 1, str(i + 1))
        text_x = content_x + badge_r * 2 + 10
        text_w = content_w - (badge_r * 2 + 10)
        c.setFont('Calibri-Bold', 10.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(text_x, py + phase_h_each - 14, phase['title'])
        body_style = ParagraphStyle('pb', fontName='Calibri', fontSize=9,
                                    leading=12.5, textColor=DARK_GRAY)
        p = Paragraph(phase['body'], body_style)
        pw, pph = p.wrap(text_w, 60)
        p.drawOn(c, text_x, py + phase_h_each - 16 - pph)

    metrics = s['metrics']
    metric_w = content_w / len(metrics) - 6
    for i, m in enumerate(metrics):
        mx = content_x + i * (metric_w + 9)
        metric_card(mx, metrics_y - metrics_h, metric_w, metrics_h,
                    m['number'], m['label'])

    callout_box(content_x, 30 + callout_h, content_w,
                s['relevance_label'], s['relevance_body'])
    footer_light(CLIENT_NAME, page_label(pg, CLIENT_NAME))


def render_next_steps(s, pg):
    new_page()
    logo_top_right()
    ty = PH - 48
    eyebrow(s['eyebrow'], ty)
    ty -= 20
    ty -= section_title(s['title'], ty)
    sub_h = section_subtitle(s.get('subtitle'), ty, width=W - 96)
    ty -= sub_h + 16

    steps = s['steps']
    step_w = (W - 96 - 16 * (len(steps) - 1)) / len(steps)
    commitment_h = 0
    if s.get('commitment'):
        commitment_h = measure_callout_height(s['commitment']['body'], W - 96) + 14
    step_bottom = 40 + commitment_h

    for i, step in enumerate(steps):
        sx = 48 + i * (step_w + 16)
        step_h = ty - step_bottom
        draw_rect(sx, step_bottom, step_w, step_h, LIGHT_BG)
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
        pw, ph = p.wrap(step_w - 24, 999)
        p.drawOn(c, sx + 12, ty - 78 - ph)

    if s.get('commitment'):
        h = measure_callout_height(s['commitment']['body'], W - 96)
        callout_box(48, 30 + h, W - 96,
                    s['commitment']['label'], s['commitment']['body'])
    footer_light(CLIENT_NAME, page_label(pg, CLIENT_NAME))


def render_closing(s, pg):
    # Buyer-mode closing uses shared helpers.closing_page for consistency.
    closing_page(
        name=s['name'],
        role=s['role'],
        email=s['email'],
        client_name=CLIENT_NAME,
    )


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------
RENDERERS = {
    'cover':                  render_cover,
    'problem_framing':        render_problem_framing,
    'section_divider':        render_section_divider,
    'modules_overview':       render_modules_overview,
    'activities_deliverables': render_activities_deliverables,
    'pillars':                render_pillars,
    'timeline':               render_timeline,
    'signature_image':        render_signature_image,
    'quote':                  render_quote,
    'comparative':            render_comparative,
    'metric_dense':           render_metric_dense,
    'minicase_pair':          render_minicase_pair,
    'proof_overview':         render_proof_overview,
    'next_steps':             render_next_steps,
    'closing':                render_closing,
}

_NO_INTENT = {'cover', 'section_divider', 'closing', 'next_steps'}


# ---------------------------------------------------------------------------
# Render loop
# ---------------------------------------------------------------------------
_layout_history = []
_has_next_steps = False
for i, section in enumerate(COPY['sections']):
    ctype = section.get('type')
    if ctype not in RENDERERS:
        raise ValueError(
            f'Unknown content_type "{ctype}" at section {i + 1}. '
            f'Valid types: {sorted(RENDERERS.keys())}'
        )
    if ctype not in _NO_INTENT and not section.get('intent'):
        print(f'  WARNING: section {i + 1} ({ctype}) missing "intent:" — '
              f'consult references/content-rules.md.')
    if ctype == 'next_steps':
        _has_next_steps = True
    _layout_history.append(ctype)
    if (len(_layout_history) >= 3
            and _layout_history[-1] == _layout_history[-2] == _layout_history[-3]):
        print(f'  WARNING: layout "{ctype}" appears 3 times in a row at section '
              f'{i + 1}. Consider breaking with a divider or alternate pattern.')
    RENDERERS[ctype](section, i + 1)

if not _has_next_steps:
    print('  WARNING: buyer-mode proposal should include a next_steps section '
          'with a concrete CTA. Consider adding one before closing.')

c.save()
print(f'\nBuilt: {OUTPUT_FILE}')
print(f'Pages: {c.getPageNumber()}')
print(f'\nNext: PYTHON scripts/verify.py --pdf {OUTPUT_FILE} --mode all')
