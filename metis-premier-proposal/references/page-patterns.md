# Page Patterns

Fifteen proven layout templates. Nine were established for the Citi CRS Proposal (patterns 1–9). Six more (patterns 10–15) were added after the AI PM Capabilities deck to support more varied narratives. Each pattern specifies positioning, typography, and the minimum content required. Code snippets use the helpers defined in `scripts/helpers.py`.

Page dimensions: **W = 13.33" (959.76pt), H = 7.5" (540pt)**. All coordinates in ReportLab convention (y increases upward from bottom).

---

## 1. Cover Page

**Purpose:** Opening page with client name, proposal title, prepared-for line.

**Layout:**
- Full-bleed dark navy gradient background (`#20216f → #256ba2 → #1a8a7a → #3cdbc0`)
- B&W stock photo at 15–20% opacity as subtle texture
- Trajectory device, right-anchored, 55% width, 20% opacity, partially off-page
- Logo (White-Mint RGB) top-left at 100pt width
- Content stack bottom-left: eyebrow → title (2 lines) → prepared-for line
- Small confidential mark bottom-right

**Code skeleton:**
```python
new_page()
gradient_bg()
try:
    c.saveState(); c.setFillAlpha(0.15)
    c.drawImage(PHOTO_BW, 0, 0, width=W, height=H)
    c.restoreState()
except: pass
try:
    c.saveState(); c.setFillAlpha(0.2)
    c.drawImage(TRAJECTORY, W*0.58, -H*0.1, width=W*0.55, height=H*1.2,
                mask='auto', preserveAspectRatio=True)
    c.restoreState()
except: pass
c.setFont('Calibri-Bold', 9); c.setFillColor(MINT)
c.drawString(48, 120, COPY['cover']['eyebrow'])
c.setFont('Calibri-Bold', 32); c.setFillColor(WHITE_CLR)
c.drawString(48, 80, COPY['cover']['title_line_1'])
c.drawString(48, 44, COPY['cover']['title_line_2'])
c.setFont('Calibri-Light', 12); c.setFillColor(Color(1,1,1,0.75))
c.drawString(48, 18, COPY['cover']['prepared_for'])
place_image(LOGO_WM, 48, H - 60, w=100)
```

**Key rules:**
- Logo must be White-Mint (never Black-Mint) on dark backgrounds
- Trajectory device opacity between 0.18 and 0.25 (stronger is too loud, weaker is invisible)
- Title is 2 lines of 32pt bold
- Eyebrow is 9pt, bold, mint, letter-spaced if possible

---

## 2. Section Divider Page

**Purpose:** Mark major sections (Our Approach, Module B, Proof Points).

**Layout:**
- Dark navy gradient background
- Nexus or trajectory device, right 50%, 28% opacity
- Logo (White-Mint) top-left
- Vertically centered: mint accent bar (50pt wide, 3pt tall) → title (26pt, may wrap) → subtitle (12pt Light, 65% opacity)

**Critical rule that was missed in Citi v1:**
The mint accent bar must be placed **above the top of the title glyphs**, not at the title's baseline. Measure the title block height first, place the bar 12pt above the top, then draw the title.

```python
def section_divider(title_text, subtitle_text=None, device_path=TRAJECTORY):
    new_page()
    gradient_bg()
    try:
        c.saveState(); c.setFillAlpha(0.15)
        c.drawImage(device_path, W*0.55, H*0.1, width=W*0.5, height=H*0.8,
                    mask='auto', preserveAspectRatio=True)
        c.restoreState()
    except: pass
    place_image(LOGO_WM, 48, H - 60, w=100)

    title_font_size = 26
    title_leading = 32
    lines = title_text.split('\n')
    title_block_h = title_leading * len(lines)
    title_center_y = H / 2
    title_top_y = title_center_y + title_block_h / 2
    title_bottom_y = title_center_y - title_block_h / 2

    # Bar ABOVE title glyphs
    bar_y = title_top_y + 12
    draw_rect(48, bar_y, 50, 3, MINT)

    c.setFont('Calibri-Bold', title_font_size); c.setFillColor(WHITE_CLR)
    baseline_y = title_top_y - title_font_size * 0.85
    for line in lines:
        c.drawString(48, baseline_y, line)
        baseline_y -= title_leading

    if subtitle_text:
        style = ParagraphStyle('ds', fontName='Calibri-Light', fontSize=12,
                               leading=17, textColor=Color(1,1,1,0.65))
        p = Paragraph(subtitle_text, style)
        pw, ph = p.wrap(450, 100)
        p.drawOn(c, 48, title_bottom_y - ph - 16)
    footer_dark()
```

### Divider style variants

`section_divider()` accepts a `style` argument:

- **`style='device'`** (default) — dark gradient + trajectory/nexus device. The Citi-era baseline.
- **`style='numbered'`** — huge mint module number on the left (e.g., `'03'`), title stack to the right. Use when running a long sequence of modules where the buyer loses track of where they are. Pass `number_text='03'`.
- **`style='photo'`** — full-bleed B&W photo overlaid with dark navy at ~72% opacity, title stack on top. Use to change texture partway through a deck that has three or more device-style dividers. Pass `photo_path='...'`.

Mix dividers deliberately. Three device-style dividers in a row feels like a template; alternating styles varies the reading texture without breaking brand.

---

## 3. Photo-Left + Content-Right (Problem Framing or Case Study)

**Purpose:** Problem statement with supporting visual; or case study with big number.

**Layout:**
- Left 38–40% of width: B&W photo with black 45–50% overlay
- Right 60–62%: logo top-right, eyebrow, title, numbered items or phase timeline, metric cards, callout at bottom

**For the problem-framing version (Citi page 2):**
Numbered items use `distribute_y_positions` to spread evenly across available space. Metric cards pinned to bottom at fixed y=28.

**For case study version (Citi pages 17–19):**
Big number overlay on the photo (client size indicator, e.g., "$16B+", "Top-25"). Phase timeline uses `numbered_item` with mint badge color.

**Key rule:** The photo-right content container is `position: absolute` internally — you are drawing at fixed coordinates. Use `distribute_y_positions` for anything with more than 2 content blocks.

---

## 4. Modular Engagement Grid (2x2 Module Cards)

**Purpose:** Show the four proposed workstreams as equal-weight options.

**Layout:**
- Header: eyebrow → title → subtitle
- 2x2 grid of module cards with mint top-accent bars and light gray fills
- Bottom: callout box explaining flexibility / engagement structure

**Measure-first rule:**
Compute body height for each of the 4 cards. Size all cards to the height of the tallest so the grid is visually balanced.

```python
card_w = (W - 96 - 24) / 2  # two columns, 24pt gutter
body_heights = [measure_body_text(m_body, card_w - 2*padding, size=11, leading=15.5) for m_title, m_body in modules]
max_body_h = max(body_heights)
card_h_content = padding + title_h + title_gap + max_body_h + padding
# If measured height + gaps fits the page, use it; else expand to fill
```

---

## 5. Activities / Deliverables Two-Column Page (Module Overview)

**Purpose:** Show activities and deliverables for a module, plus one or two bottom callouts.

**Layout:**
- Header: eyebrow → title → subtitle
- Two columns of bullet lists with mint column-header underlines
- Bottom: 0–2 callout boxes stacked

**Critical measure-first rule:**
Use dynamic `item_gap` to fill available space. Measure natural height of both lists (item_gap=0), calculate available space after accounting for callouts, then distribute remaining space as gap between items:

```python
act_natural = measure_bullet_list(activities, col_w, size=10.5, leading=15, item_gap=0)
del_natural = measure_bullet_list(deliverables, col_w, size=10.5, leading=15, item_gap=0)
natural_max = max(act_natural, del_natural)
bullets_available = ty - bottom_limit - callouts_total - gap_to_callouts
longer_count = max(len(activities), len(deliverables))
gap = max(6, (bullets_available - natural_max) / (longer_count - 1))
gap = min(gap, 18)  # cap
```

See `activities_deliverables_page()` in `scripts/helpers.py` for the full implementation.

---

## 6. Image + Annotation (Framework or Diagram Page)

**Purpose:** Embed a slide screenshot (hub-and-spoke diagram, framework model) with context.

**Layout:**
- Header: eyebrow → title → subtitle
- Centered image, sized to fill remaining height
- Bottom: callout explaining application to this client

**Measure-first rule:**
Measure the callout height first, then size the image to fill the space above it:

```python
callout_h = measure_callout_height(annotation_text, W - 96)
top_of_image = ty
bottom_of_image = 30 + callout_h + 14
avail_h = top_of_image - bottom_of_image
img_w = W - 72
img_h = img_w / img_aspect
if img_h > avail_h:
    img_h = avail_h
    img_w = img_h * img_aspect
img_x = 48 + (avail_w - img_w) / 2
img_y = bottom_of_image + (avail_h - img_h) / 2
c.drawImage(img_path, img_x, img_y, width=img_w, height=img_h, mask='auto')
callout_box(48, 30 + callout_h, W - 96, 'APPLICATION', annotation_text)
```

**Critical rule on slide images:**
**Crop the source slide image to remove its original title, subtitle, and footer before embedding.** If you embed a PPTX slide that has "Data and AI Management Maturity Assessment Model" as its title, and your page title is the same thing, you get duplicate headers and look unprofessional. See `scripts/crop_slide.py`.

---

## 7. Slim Header + Full-Width Image Page (Hub-and-Spoke, Big Diagrams)

**Purpose:** Showcase a wide diagram that deserves maximum horizontal real estate.

**Layout:**
- Slim 70pt dark navy header bar across the top with logo top-right, eyebrow + 20pt title bottom-left
- Full-width image below header, sized to fill remaining height
- Pull quote or callout at bottom

Useful for hub-and-spoke diagrams, layered framework visuals, and data tables that benefit from full horizontal width.

---

## 8. Four-Column Card Layout (Pillars or Cross-Cutting Summary)

**Purpose:** Show four parallel concepts (like the Change Management pillars: Leadership & Governance, Readiness, Communications, Capability Building).

**Layout per card:**
- Colored band at top (54pt tall) with centered white title text
- Body: italic purpose statement (centered, 9.5pt)
- Sub-bullets below the purpose (9pt, left-aligned)
- Card has 1.2pt colored border matching the band

**Band color rotation:** Blue (`#256ba2`), Mint (`#3cdbc0`), Dark Teal (`#1a8a7a`), Near-Black (`#1a2040`). Text color flips: White on blue/teal/black, Dark Navy on mint.

**Rule on rounded bands:**
The band is a rounded rect. To get a band with rounded top and square bottom, draw the full rounded rect, then overdraw the bottom half with a square rectangle:

```python
c.roundRect(cx, band_y, col_w, band_h, 6, fill=1, stroke=0)
c.rect(cx, band_y, col_w, band_h / 2, fill=1, stroke=0)  # squares the bottom
```

---

## 9. Closing Page (Thank You + Contact)

**Purpose:** Final page with thanks and contact info.

**Layout:**
- Dark navy gradient background
- Trajectory device, low opacity (10–15%)
- Logo (White-Mint) top-left
- Left-aligned, vertically centered: "Thank you." (32pt bold) → mint accent bar → name → role (mint) → email → brandline → copyright

```python
new_page(); gradient_bg()
try:
    c.saveState(); c.setFillAlpha(0.12)
    c.drawImage(TRAJECTORY, W*0.55, H*0.05, width=W*0.5, height=H*0.9,
                mask='auto', preserveAspectRatio=True)
    c.restoreState()
except: pass
place_image(LOGO_WM, 48, H - 60, w=100)
c.setFont('Calibri-Bold', 32); c.setFillColor(WHITE_CLR)
c.drawString(48, H/2 + 30, 'Thank you.')
draw_rect(48, H/2 + 18, 50, 3, MINT)
c.setFont('Calibri-Bold', 15); c.setFillColor(WHITE_CLR)
c.drawString(48, H/2 - 4, name)
c.setFont('Calibri', 11); c.setFillColor(MINT)
c.drawString(48, H/2 - 22, role)
c.setFont('Calibri', 11); c.setFillColor(Color(1,1,1,0.7))
c.drawString(48, H/2 - 40, email)
c.setFont('Calibri', 9); c.setFillColor(MINT)
c.drawString(48, 30, 'Driving change. Elevating leaders.')
c.setFont('Calibri', 7); c.setFillColor(Color(1,1,1,0.35))
c.drawString(48, 14, '© 2026 Metis Strategy LLC. All rights reserved. Proprietary & Confidential.')
```

---

## 10. Minicase Pair (2-up Proof Cards)

**Purpose:** Show two small proof points side-by-side — tight product-level results with a dollar number, label, product name, and two-sentence body.

**Layout:**
- Header: eyebrow → title → subtitle
- Two equal cards filling the remaining height
- Each card: colored band header (badge text) → big mint number → small label → thin divider → product name → centered body

**Helper:** `minicase_pair_page(eyebrow_text, title_text, subtitle_text, cases, doc_label, pg_num)`

Each case dict:
```python
{
  'badge': 'SaaS',                    # short tag in the header band
  'big_number': '$2.4M',              # mint, auto-shrunk to fit width
  'number_label': 'Annual savings',   # small caps under the number
  'product_title': 'Customer Analytics',
  'body': 'One to two sentences on what this proof delivered.',
  'badge_color': 'DARK_NAVY',         # key in _BADGE_COLOR_MAP, or a Color
}
```

**Rule:** keep the body to two sentences max. Use the big number to carry the weight, not the prose. Works best when paired with a second minicase page so the reader sees four proofs in the section, not two.

---

## 11. Signature Visual (Image-Led Hero)

**Purpose:** Make the anchor framework / diagram that carries the thesis the entire page. Use once per deck, maximum twice. See `narrative-planning.md` step 4.

**Layout:**
- Header: eyebrow → title → subtitle
- Full-width cropped image, centered in remaining vertical space
- Optional bottom callout (label + body)

**Helper:** `signature_visual_page(eyebrow_text, title_text, subtitle_text, image_path, callout_label, callout_body, doc_label, pg_num)`

**Critical rule:** crop the source image so it contains only the diagram — no source slide title, no source footer, no source logo. The PDF supplies those. See `scripts/crop_slide.py`.

---

## 12. Process Timeline (Horizontal Numbered Stages)

**Purpose:** Render a 3–6 stage process natively rather than embedding a raster. The advantage is the timeline can carry a callout, remain editable from YAML, and not duplicate titles that might live in the source slide.

**Layout:**
- Header: eyebrow → title → subtitle
- Horizontal mint rule across the content area
- Numbered dark-navy circles on the rule (mint numeral)
- Stage title + short body below each circle
- Optional bottom callout

**Helper:** `process_timeline_page(eyebrow_text, title_text, subtitle_text, stages, callout_label, callout_body, doc_label, pg_num)`

Stage dicts: `{'title': 'Intake', 'body': 'Align on outcomes and scope.'}`

Best for 4 or 5 stages. With 6 the text gets tight; with 3 the page looks thin unless the bodies carry weight.

---

## 13. Quote-Led Page

**Purpose:** Anchor a section with a single hero pull quote — buyer voice, market insight, or thesis statement. Use sparingly. A deck with three quote-led pages is a lazy deck.

**Layout:**
- Logo top-right, small eyebrow top-left
- Vertically centered: mint accent bar → large italic quote (24pt) → attribution (— Name, Title) → optional short context paragraph

**Helper:** `quote_led_page(eyebrow_text, quote, attribution, context, doc_label, pg_num)`

**Rule:** the quote must carry the page by itself. If you need the body context paragraph to explain why the quote matters, the quote is not strong enough on its own — pick a better quote or use a different pattern.

---

## 14. Comparative Two-Column

**Purpose:** Before/after, our-way/their-way, old/new framings. Renders side-by-side with a clear asymmetric weight — the preferred side gets the TEAL_LIGHT fill and DARK_NAVY header; the contrast side gets LIGHT_BG with a GRAY header.

**Layout:**
- Header: eyebrow → title → subtitle
- Two equal columns with header strip + bullet list
- Left column is visually lighter (contrast); right column is the preferred state

**Helper:** `comparative_page(eyebrow_text, title_text, subtitle_text, left, right, doc_label, pg_num)`

Where:
```python
left = {'header': 'Traditional Consulting', 'bullets': ['...', '...']}
right = {'header': 'Metis Embedded PM', 'bullets': ['...', '...']}
```

**Rule:** keep bullet counts equal between columns. Asymmetric bullet counts read as "we had more points on our side" — cheap. Let the content win.

---

## 15. Metric-Dense

**Purpose:** A standalone outcome / impact page. 4–6 metric cards across a single horizontal band, with an explanatory narrative paragraph below.

**Layout:**
- Header: eyebrow → title → subtitle
- Single row of metric cards (`metric_card` helper) spanning the content width
- Paragraph of 2–4 sentences below, explaining what the metrics represent

**Helper:** `metric_dense_page(eyebrow_text, title_text, subtitle_text, metrics, narrative, doc_label, pg_num)`

Metric dicts: `{'number': '$350M+', 'label': 'Portfolio value'}`

**Rule:** each metric must be independently defensible. If a number cannot stand on its own — if it needs the narrative paragraph to make sense — it does not belong on a metric card.

---

## Anti-Patterns (Don't Do These)

### Full-bleed slide screenshot pasted into a PDF frame
Page looks like a screenshot, not a designed document. Slide has its own title, the PDF has a title above it, and you get duplicate headers. If you need a slide's visual, crop the screenshot to show only the diagram (no title, no footer, no logo) and embed it as a figure with a caption.

### Numbered item loops with fixed spacing
`ty -= item_h + gap` in a loop, where `item_h` is approximated but `gap` is fixed. Any variance in body text length creates overlap with adjacent items. Use `distribute_y_positions` instead.

### Text-only proof point pages
Every proof point page must have at least one visual anchor: photo, metric cards, diagram, or phase timeline. Text-only pages read as low-effort.

### Metric cards with fixed font size for the big number
Long labels overflow. Use `stringWidth` to auto-shrink:

```python
num_font_size = 24
while num_font_size > 11:
    text_w = c.stringWidth(num_str, 'Calibri-Bold', num_font_size)
    if text_w <= inner_w: break
    num_font_size -= 1
```

### Cover page without a visible logo
The logo must be White-Mint (not Black-Mint) and placed prominently (top-left at 100pt wide, not 80pt). Verify visually — several Citi iterations had the logo "placed" but effectively invisible due to size or render issues.
