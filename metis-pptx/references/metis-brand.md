<!-- Brand source: metis-brand-identity v0.2.2 | Synced: 2026-05-21 -->
# Metis Brand Implementation Reference

Metis-specific code recipes for python-pptx slide generation. Contains exact colors,
fonts, coordinates, and component implementations for the Metis Strategy brand.

**This file is used ONLY in Generation mode** (new Metis-branded decks from scratch).
For brand-agnostic pattern guidance, see `patterns.md`.
When editing a client deck, do NOT use these Metis-specific values — extract the
client's brand tokens with `scripts/extract_brand.py` instead.

---

## Slide Dimensions

| Property | Value | EMU |
|---|---|---|
| Width | 13.33 inches | 12,192,000 |
| Height | 7.50 inches | 6,858,000 |

---

## Brand Colors

```python
from pptx.dml.color import RGBColor

DARK_NAVY  = RGBColor(0x20, 0x21, 0x6F)  # #20216f — titles, headings, dark backgrounds
METIS_BLUE = RGBColor(0x25, 0x6B, 0xA2)  # #256BA2 — callout bars, accents, subheadings
MINT       = RGBColor(0x3C, 0xDB, 0xC0)  # #3cdbc0 — highlights, bullet markers, dividers
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)  # #FFFFFF — text on dark backgrounds
LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)  # #F2F2F2 — content box backgrounds
DARK_GRAY  = RGBColor(0x4A, 0x4A, 0x4A)  # #4A4A4A — body text

# Tier gradient colors (for pricing/assessment tables)
TIER_LIGHT = RGBColor(0xD1, 0xE3, 0xF1)  # #D1E3F1 — Tier 1 / Foundational
TIER_MED   = RGBColor(0xA3, 0xC7, 0xE3)  # #A3C7E3 — Tier 2 / Strategic
TIER_DARK  = RGBColor(0x75, 0xAB, 0xD5)  # #75ABD5 — Tier 3 / Embedded

# Supplementary
LIGHT_BLUE_BG = RGBColor(0xCB, 0xE1, 0xF3)  # #CBE1F3 — tag backgrounds
LIGHT_MINT_BG = RGBColor(0xD6, 0xF7, 0xF2)  # #D6F7F2 — opportunity card backgrounds
PURPLE     = RGBColor(0x76, 0x2C, 0xB3)  # #762CB3 — spoke/domain accent (hub-spoke diagrams)
```

**Color roles:**
- **Slide title** — always `DARK_NAVY`
- **Body text** — always `DARK_GRAY`
- **Content box backgrounds** — `LIGHT_GRAY` (no border)
- **Accent bars / dividers** — `MINT` or `METIS_BLUE`
- **Section divider slides** — `DARK_NAVY` background, `WHITE` title
- **Cover slides** — `DARK_NAVY` background, `WHITE` text, `MINT` accents
- **Tier rows** — `TIER_LIGHT` → `TIER_MED` → `TIER_DARK` (light to dark gradient)

---

## Typography

Calibri only. No other fonts.

| Element | Size | Weight | Color | Usage |
|---|---|---|---|---|
| Slide title | 28pt | Bold | DARK_NAVY | One per slide, from layout placeholder |
| Section header | 20pt | Bold | DARK_NAVY | Within content area, introduces a block |
| Body text | 14pt | Regular | DARK_GRAY | Paragraphs, descriptions |
| Small body | 12pt | Regular | DARK_GRAY | Dense content, table cells, footnotes |
| Caption / label | 11pt | Regular/Bold | METIS_BLUE | Category labels, metadata |
| Metric / big number | 36pt | Bold | DARK_NAVY | KPI callouts, featured statistics |
| Large letter label | 42pt | Bold | DARK_NAVY | Visual anchors (A, B, C or 01, 02, 03) |
| Header bar text | 14pt | Bold | WHITE | Text inside navy header bars |
| Tag text | 10pt | Italic | DARK_GRAY | ILLUSTRATIVE, NON-EXHAUSTIVE tags |

```python
from pptx.util import Pt

def set_font(run, size=14, bold=False, color=DARK_GRAY, italic=False):
    run.font.name = 'Calibri'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    if italic:
        run.font.italic = True
```

---

## Spacing Constants

```python
from pptx.util import Inches

# Page margins
MARGIN_LEFT   = Inches(0.50)
MARGIN_TOP    = Inches(1.10)   # Below title area
MARGIN_RIGHT  = Inches(0.50)   # Right edge at 12.83"
MARGIN_BOTTOM = Inches(6.80)   # Above footer

# Title area (set via placeholder idx=0, not manually)
TITLE_LEFT    = Inches(0.35)
TITLE_TOP     = Inches(0.25)
TITLE_WIDTH   = Inches(12.60)
TITLE_HEIGHT  = Inches(0.50)

# Content area
CONTENT_LEFT  = Inches(0.50)
CONTENT_TOP   = Inches(1.10)
CONTENT_WIDTH = Inches(12.33)  # 13.33 - 0.50 - 0.50
CONTENT_HEIGHT= Inches(5.70)   # 6.80 - 1.10

# Gaps
GAP           = Inches(0.25)
COL_GAP       = Inches(0.30)
```

---

## Footer

Footers are inherited from the `1_Title Only` slide layout — do NOT create footer shapes manually.
The layout provides:
- Footer: "Proprietary & Confidential, Metis Strategy LLC 2026" at (9.85", 6.93")
- Slide number at (12.71", 6.93")
- Source line at (1.70", 6.93")

---

## Placeholder Text — Formatting Preservation

**Critical:** When setting text on slide layout placeholders, `ph.text = "..."` clears
ALL inherited formatting (font name, size, color, bold/italic, and sometimes position)
because python-pptx replaces the entire `<a:p>` (paragraph) XML tree.

**Safe pattern for any placeholder that inherits styling from the layout:**

```python
# WRONG — clears formatting:
ph.text = "My subtitle"

# RIGHT — preserves formatting:
tf = ph.text_frame
if tf.paragraphs and tf.paragraphs[0].runs:
    tf.paragraphs[0].runs[0].text = "My subtitle"
else:
    run = tf.paragraphs[0].add_run()
    run.text = "My subtitle"
```

**When `ph.text = ...` IS safe:** Title placeholders (idx=0) tolerate this because
PowerPoint re-applies title formatting on open. Subtitle and custom placeholders
(idx=14, etc.) do NOT — their formatting is only defined in the layout XML and is
lost permanently when the paragraph tree is replaced.

**Applies to:** `add_content_slide()` subtitle, section divider subtitles, any
custom placeholders added to layouts.

---

## Helper Functions

Define these at the top of your `build_deck.py` script, after the imports and
color constants. These are referenced throughout the build workflow.

### get_layout()

```python
def get_layout(name):
    """Find a slide layout by name. Raises ValueError if not found."""
    for layout in prs.slide_layouts:
        if layout.name == name:
            return layout
    available = [l.name for l in prs.slide_layouts]
    raise ValueError(f"Layout '{name}' not found. Available: {available}")
```

### add_content_slide()

```python
def add_content_slide(title_text, subtitle_text=None):
    """Add a hand-built content slide on the '1_Title Only' framed canvas.

    Use this for Path A / Path B slides (hand-built shapes or Timesaver
    metaphors). For most slides, prefer a NATIVE layout instead, see
    references/metis-layouts.md and SKILL.md §0.5.1.

    subtitle_text is OPTIONAL and off by default. Pass it only when the title
    cannot carry the so-what (SKILL.md §0.5); do not fill a subtitle by reflex,
    and do not style it as gray italic hedging.

    Sets the title via placeholder idx=0.
    When provided, sets the subtitle via placeholder idx=14, PRESERVING the
    layout's original formatting (font, size, color, position).

    IMPORTANT: Do NOT use ph.text = ... for the subtitle placeholder.
    That clears all inherited formatting from the layout master. Instead,
    access the first run of the first paragraph and set only the run's
    .text property, which preserves paragraph- and run-level formatting.
    """
    slide = prs.slides.add_slide(get_layout('1_Title Only'))
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx == 0:
            ph.text = title_text
        elif ph.placeholder_format.idx == 14:
            if subtitle_text:
                # --- FORMAT-PRESERVING subtitle assignment ---
                tf = ph.text_frame
                if tf.paragraphs:
                    p = tf.paragraphs[0]
                    if p.runs:
                        p.runs[0].text = subtitle_text
                    else:
                        run = p.add_run()
                        run.text = subtitle_text
                else:
                    ph.text = subtitle_text  # Fallback (should not happen)
            else:
                # An unfilled placeholder still shows "Click to add subtitle"
                # when the deck is opened in PowerPoint, so remove the shape
                # rather than leave it empty.
                sp = ph._element
                sp.getparent().remove(sp)
    return slide
```

### add_section_divider()

```python
def add_section_divider(title_text):
    """Add a section divider slide using the 'Section Divider' layout."""
    slide = prs.slides.add_slide(get_layout('Section Divider'))
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0:
            ph.text = title_text
    return slide
```

### copy_slide_from()

```python
import copy

def copy_slide_from(source_prs, source_slide_index):
    """Copy a slide from source_prs into the current presentation."""
    src_slide = source_prs.slides[source_slide_index]
    dest_layout = prs.slide_layouts[0]

    src_layout_name = src_slide.slide_layout.name
    for layout in prs.slide_layouts:
        if layout.name == src_layout_name:
            dest_layout = layout
            break

    new_slide = prs.slides.add_slide(dest_layout)
    for shape in src_slide.shapes:
        el = copy.deepcopy(shape._element)
        new_slide.shapes._spTree.append(el)

    for rel in src_slide.part.rels.values():
        if "image" in rel.reltype:
            new_slide.part.rels.get_or_add(rel.reltype, rel.target_part)

    return new_slide
```

### save_clean()

```python
def save_clean(prs, output_path):
    """Save the presentation with ZIP deduplication."""
    import zipfile, io, os

    buf = io.BytesIO()
    prs.save(buf)
    buf.seek(0)
    with zipfile.ZipFile(buf, 'r') as zin:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            seen = set()
            for item in zin.infolist():
                if item.filename not in seen:
                    seen.add(item.filename)
                    zout.writestr(item, zin.read(item.filename))
    print(f"Saved: {output_path}")
```

---

## Metis Grid Implementations

### Common Setup

```python
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# ALWAYS use '1_Title Only' layout for content slides.
# This gives you: green arrow, logo, footer, page number, source line.
# NEVER use 'Blank' — it has none of these brand elements.
slide = add_content_slide("Your Slide Title", "Optional subtitle text")

# Or manually if not using the helper:
slide = prs.slides.add_slide(get_layout('1_Title Only'))
for ph in slide.placeholders:
    if ph.placeholder_format.idx == 0:   # Title (with green arrow)
        ph.text = "Your Slide Title"
    elif ph.placeholder_format.idx == 14:  # Subhead
        # WARNING: Do NOT use ph.text = "..." here — it clears the
        # layout's formatting (font, size, color, position).
        # Instead, preserve formatting by setting only the run text:
        if ph.text_frame.paragraphs and ph.text_frame.paragraphs[0].runs:
            ph.text_frame.paragraphs[0].runs[0].text = "Brief description"
        else:
            run = ph.text_frame.paragraphs[0].add_run()
            run.text = "Brief description"
# Content area starts at y=1.10" below the title
```

### Grid 1: Full Width

```python
# Full-width text block
body = slide.shapes.add_textbox(
    Inches(0.50), Inches(1.10), Inches(12.33), Inches(5.70)
)
tf = body.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Your content here"
p.font.name = 'Calibri'
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(0x4A, 0x4A, 0x4A)

# For a highlighted box instead:
box = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.50), Inches(1.10), Inches(12.33), Inches(2.50)
)
box.fill.solid()
box.fill.fore_color.rgb = RGBColor(0xF2, 0xF2, 0xF2)
box.line.fill.background()
```

### Grid 2: Two Column (Equal)

```python
COL_W = Inches(6.02)
LEFT_X = Inches(0.50)
RIGHT_X = Inches(6.81)
TOP_Y = Inches(1.10)
COL_H = Inches(5.70)

# Left column header
left_hdr = slide.shapes.add_textbox(LEFT_X, TOP_Y, COL_W, Inches(0.40))
p = left_hdr.text_frame.paragraphs[0]
p.text = "Current State"
p.font.name = 'Calibri'; p.font.size = Pt(20); p.font.bold = True
p.font.color.rgb = RGBColor(0x20, 0x20, 0x6E)

# Left column body
left_body = slide.shapes.add_textbox(LEFT_X, Inches(1.60), COL_W, Inches(5.20))
left_body.text_frame.word_wrap = True

# Right column (same pattern, offset to RIGHT_X)
right_hdr = slide.shapes.add_textbox(RIGHT_X, TOP_Y, COL_W, Inches(0.40))
```

### Grid 3: Sidebar + Main (1/3 + 2/3)

```python
SIDE_X = Inches(0.50)
SIDE_W = Inches(3.84)
MAIN_X = Inches(4.64)
MAIN_W = Inches(8.19)
TOP_Y  = Inches(1.10)
COL_H  = Inches(5.70)

# Sidebar — often a callout box with a big metric
sidebar_box = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    SIDE_X, TOP_Y, SIDE_W, COL_H
)
sidebar_box.fill.solid()
sidebar_box.fill.fore_color.rgb = RGBColor(0xF2, 0xF2, 0xF2)
sidebar_box.line.fill.background()

# Big metric inside sidebar
tf = sidebar_box.text_frame
tf.word_wrap = True
tf.margin_left = Inches(0.20)
tf.margin_top = Inches(0.30)
p = tf.paragraphs[0]
p.text = "$4.2M"
p.font.name = 'Calibri'; p.font.size = Pt(36); p.font.bold = True
p.font.color.rgb = RGBColor(0x20, 0x20, 0x6E)

# Main content area
main_body = slide.shapes.add_textbox(MAIN_X, TOP_Y, MAIN_W, COL_H)
main_body.text_frame.word_wrap = True
```

### Grid 4: Three Column

```python
COL_W = Inches(3.88)
COL_H = Inches(5.70)
TOP_Y = Inches(1.10)
COL_POSITIONS = [Inches(0.50), Inches(4.68), Inches(8.85)]

for i, (col_x, heading, body_text) in enumerate(zip(
    COL_POSITIONS,
    ["Phase 1: Discover", "Phase 2: Design", "Phase 3: Deliver"],
    ["Description...", "Description...", "Description..."]
)):
    # Column header box (navy background, white text)
    hdr = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        col_x, TOP_Y, COL_W, Inches(0.50)
    )
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = RGBColor(0x20, 0x20, 0x6E)
    hdr.line.fill.background()
    tf = hdr.text_frame
    tf.margin_left = Inches(0.10)
    tf.margin_top = Inches(0.08)
    p = tf.paragraphs[0]
    p.text = heading
    p.font.name = 'Calibri'; p.font.size = Pt(16); p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Column body
    body = slide.shapes.add_textbox(
        col_x, Inches(1.70), COL_W, Inches(5.10)
    )
    body.text_frame.word_wrap = True
    p = body.text_frame.paragraphs[0]
    p.text = body_text
    p.font.name = 'Calibri'; p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(0x4A, 0x4A, 0x4A)
```

### Grid 5: Title + Large Visual Area

```python
# Subtitle/description
sub = slide.shapes.add_textbox(
    Inches(0.50), Inches(1.10), Inches(12.33), Inches(0.60)
)
sub.text_frame.word_wrap = True
p = sub.text_frame.paragraphs[0]
p.text = "Brief description of the visual below"
p.font.name = 'Calibri'; p.font.size = Pt(14)
p.font.color.rgb = RGBColor(0x4A, 0x4A, 0x4A)

# Large visual area — use for tables, diagrams, etc.
VISUAL_LEFT = Inches(0.50)
VISUAL_TOP  = Inches(1.95)
VISUAL_W    = Inches(12.33)
VISUAL_H    = Inches(4.85)

# Example: add a table
rows, cols = 5, 4
table_shape = slide.shapes.add_table(rows, cols, VISUAL_LEFT, VISUAL_TOP, VISUAL_W, VISUAL_H)
table = table_shape.table

# Style the header row
for cell in table.rows[0].cells:
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(0x20, 0x20, 0x6E)
    for p in cell.text_frame.paragraphs:
        p.font.name = 'Calibri'; p.font.size = Pt(12); p.font.bold = True
        p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
```

---

## Metis Component Recipes

Every component below is a python-pptx code recipe using Metis brand constants.

### A. Structural Elements

#### 1. Navy Header Bar

```python
def navy_header_bar(slide, text, left, top, width, height=Inches(0.45)):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = DARK_NAVY
    bar.line.fill.background()
    tf = bar.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_top = Inches(0.06)
    p = tf.paragraphs[0]
    p.text = text
    set_font(p.runs[0] if p.runs else p.add_run(), size=14, bold=True, color=WHITE)
    return bar
```

#### 2. Accent Left Bar

```python
def accent_bar(slide, left, top, height, color=MINT):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.06), height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    return bar
```

#### 3. Light Gray Content Card

```python
def gray_card(slide, left, top, width, height):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = LIGHT_GRAY
    box.line.fill.background()
    return box
```

#### 4. Horizontal Divider Line

```python
def divider_line(slide, left, top, width, color=MINT):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = color
    line.line.fill.background()
    return line
```

#### 5. Illustrative / Non-Exhaustive Tag

```python
def illustrative_tag(slide, text="ILLUSTRATIVE"):
    box = slide.shapes.add_textbox(Inches(11.5), Inches(0.85), Inches(1.5), Inches(0.3))
    p = box.text_frame.paragraphs[0]
    p.text = text
    run = p.runs[0] if p.runs else p.add_run()
    run.font.name = 'Calibri'
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = DARK_GRAY
```

### B. Content Presentation

#### 6. Large Letter / Number Label

```python
def large_label(slide, text, left, top, width=Inches(0.8), height=Inches(1.0)):
    box = slide.shapes.add_textbox(left, top, width, height)
    p = box.text_frame.paragraphs[0]
    p.text = text
    set_font(p.runs[0] if p.runs else p.add_run(), size=42, bold=True, color=DARK_NAVY)
    return box
```

#### 7. Numbered Callout Block

```python
def numbered_callout(slide, number, title, body, left, top, width=Inches(3.5)):
    num_box = slide.shapes.add_textbox(left, top, Inches(0.8), Inches(0.6))
    p = num_box.text_frame.paragraphs[0]
    p.text = f"{number:02d}"
    set_font(p.runs[0] if p.runs else p.add_run(), size=36, bold=True, color=DARK_NAVY)

    title_box = slide.shapes.add_textbox(left + Inches(0.9), top, width - Inches(0.9), Inches(0.4))
    p = title_box.text_frame.paragraphs[0]
    p.text = title
    set_font(p.runs[0] if p.runs else p.add_run(), size=16, bold=True, color=DARK_NAVY)

    body_box = slide.shapes.add_textbox(left + Inches(0.9), top + Inches(0.4), width - Inches(0.9), Inches(1.0))
    body_box.text_frame.word_wrap = True
    p = body_box.text_frame.paragraphs[0]
    p.text = body
    set_font(p.runs[0] if p.runs else p.add_run(), size=12, color=DARK_GRAY)
```

#### 8. Icon Circle + Text

```python
def icon_circle_text(slide, icon_text, title, body, left, top, circle_color=DARK_NAVY):
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, Inches(0.5), Inches(0.5))
    circle.fill.solid()
    circle.fill.fore_color.rgb = circle_color
    circle.line.fill.background()
    tf = circle.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = icon_text
    p.alignment = PP_ALIGN.CENTER
    set_font(p.runs[0] if p.runs else p.add_run(), size=14, bold=True, color=WHITE)

    title_box = slide.shapes.add_textbox(left + Inches(0.65), top, Inches(3.0), Inches(0.3))
    p = title_box.text_frame.paragraphs[0]
    p.text = title
    set_font(p.runs[0] if p.runs else p.add_run(), size=14, bold=True, color=DARK_NAVY)

    body_box = slide.shapes.add_textbox(left + Inches(0.65), top + Inches(0.3), Inches(3.0), Inches(0.7))
    body_box.text_frame.word_wrap = True
    p = body_box.text_frame.paragraphs[0]
    p.text = body
    set_font(p.runs[0] if p.runs else p.add_run(), size=12, color=DARK_GRAY)
```

#### 8b. Graphical Icon Card (Lucide)

Real graphical icon + title + body in a Metis-styled card. Drop-in
replacement for `icon_circle_text` when a Lucide glyph communicates the
concept better than a numbered circle.

```python
# Requires scripts/icons.py and `pip install cairosvg`
# System dep: libcairo (brew install cairo / apt-get install libcairo2)
from scripts.icons import lucide_icon_card

# Single card
lucide_icon_card(
    slide,
    icon="shield-check",       # Lucide name in kebab-case (lucide.dev/icons)
    title="Compliance & Risk",
    body="Validate retention rules against regulatory requirements.",
    left=Inches(0.5), top=Inches(2.0), width=Inches(3.0),
    # Optional brand overrides. Defaults to Metis Dark Navy + Dark Gray.
    # icon_color=DARK_NAVY, title_color=DARK_NAVY, body_color=DARK_GRAY,
)

# Row of four cards (typical layout)
for i, (name, title, body) in enumerate(items):  # items is a 4-tuple list
    lucide_icon_card(
        slide, name, title, body,
        left=Inches(0.5 + i * 3.15),
        top=Inches(2.0),
        width=Inches(3.0),
    )
```

**Icon selection:** see `references/icons.md` for the catalog naming guide.
Always use kebab-case (e.g., `shield-check`, `users-round`, `flask-conical`).

**Stroke consistency:** the helper renders every icon with `stroke-width=2`
by default. To override deck-wide, set the helper's default at import:

```python
from scripts import icons
icons.DEFAULT_STROKE_WIDTH = 2.5   # stronger weight for board-level decks
```

**Client decks:** pass extracted brand colors so icons match the client's
palette:

```python
brand = json.load(open("extracted_brand.json"))
client_navy = brand["colors"]["primary_text"]
lucide_icon_card(slide, "shield-check", "...", "...",
                 left=..., top=..., width=...,
                 icon_color=client_navy, title_color=client_navy)
```

#### 9. Content Card with Header

```python
def content_card(slide, header_text, body_text, left, top, width, body_height=Inches(1.5)):
    navy_header_bar(slide, header_text, left, top, width, Inches(0.40))
    card = gray_card(slide, left, top + Inches(0.40), width, body_height)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_top = Inches(0.08)
    p = tf.paragraphs[0]
    p.text = body_text
    set_font(p.runs[0] if p.runs else p.add_run(), size=12, color=DARK_GRAY)
    return card
```

#### 10. Key Benefits Text Blocks

```python
def benefits_two_col(slide, left_items, right_items, top=Inches(1.4)):
    """left_items / right_items: list of (title, body) tuples"""
    col_w = Inches(4.1)
    left_x = Inches(0.50)
    right_x = Inches(8.90)
    for items, x in [(left_items, left_x), (right_items, right_x)]:
        y_pos = top
        for title, body in items:
            t = slide.shapes.add_textbox(x, y_pos, col_w, Inches(0.25))
            p = t.text_frame.paragraphs[0]
            p.text = title
            set_font(p.runs[0] if p.runs else p.add_run(), size=14, bold=True, color=DARK_NAVY)

            b = slide.shapes.add_textbox(x, y_pos + Inches(0.25), col_w, Inches(1.2))
            b.text_frame.word_wrap = True
            p = b.text_frame.paragraphs[0]
            p.text = body
            set_font(p.runs[0] if p.runs else p.add_run(), size=12, color=DARK_GRAY)
            y_pos += Inches(1.8)
```

#### 11. Category Grid

```python
def category_grid(slide, categories, top=Inches(1.10)):
    """categories: list of (header, [row1, row2, ...]) tuples"""
    n = len(categories)
    col_w = (12.33 - (n - 1) * 0.20) / n
    for i, (header, rows) in enumerate(categories):
        x = Inches(0.50 + i * (col_w + 0.20))
        navy_header_bar(slide, header, x, top, Inches(col_w), Inches(0.50))
        if rows and len(rows) > 0:
            sub = slide.shapes.add_textbox(x, top + Inches(0.55), Inches(col_w), Inches(0.35))
            sub.text_frame.word_wrap = True
            p = sub.text_frame.paragraphs[0]
            p.text = rows[0]
            set_font(p.runs[0] if p.runs else p.add_run(), size=11, italic=True, color=DARK_GRAY)
        y = top + Inches(0.95)
        for row in rows[1:]:
            card = gray_card(slide, x, y, Inches(col_w), Inches(0.60))
            tf = card.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.08)
            tf.margin_top = Inches(0.05)
            p = tf.paragraphs[0]
            p.text = row
            set_font(p.runs[0] if p.runs else p.add_run(), size=11, color=DARK_GRAY)
            y += Inches(0.65)
```

### C. Tiered / Pricing / Assessment

#### 12. Tiered Pricing Table

```python
def tiered_table(slide, tiers, columns, top=Inches(1.30)):
    """
    tiers: list of (name, color, [cell_values])
    columns: list of column header strings
    """
    tier_w = Inches(1.5)
    first_col_x = Inches(0.30)
    col_start_x = Inches(1.90)
    n_cols = len(columns)
    col_w = (12.33 - 1.60) / n_cols if n_cols > 0 else Inches(2.0)
    row_h = Inches(0.90)

    for j, col_name in enumerate(columns):
        x = col_start_x + Inches(j * col_w)
        hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top, Inches(col_w), Inches(0.45))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = DARK_NAVY
        hdr.line.fill.background()
        tf = hdr.text_frame
        tf.margin_left = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = col_name
        set_font(p.runs[0] if p.runs else p.add_run(), size=11, bold=True, color=WHITE)

    lbl = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, first_col_x, top, tier_w, Inches(0.45))
    lbl.fill.solid()
    lbl.fill.fore_color.rgb = DARK_NAVY
    lbl.line.fill.background()
    tf = lbl.text_frame
    tf.margin_left = Inches(0.08)
    p = tf.paragraphs[0]
    p.text = "Tier"
    set_font(p.runs[0] if p.runs else p.add_run(), size=11, bold=True, color=WHITE)

    for i, (name, color, cells) in enumerate(tiers):
        y = top + Inches(0.50) + Inches(i * (row_h + 0.05))
        tier_cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, first_col_x, y, tier_w, row_h)
        tier_cell.fill.solid()
        tier_cell.fill.fore_color.rgb = color
        tier_cell.line.fill.background()
        tf = tier_cell.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = name
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, bold=True, color=DARK_NAVY)

        for j, val in enumerate(cells):
            x = col_start_x + Inches(j * col_w)
            cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(col_w), row_h)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_GRAY
            cell.line.fill.background()
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.08)
            tf.margin_top = Inches(0.05)
            p = tf.paragraphs[0]
            p.text = val
            set_font(p.runs[0] if p.runs else p.add_run(), size=11, color=DARK_GRAY)
```

#### 13. Harvey Balls / Maturity Indicators

```python
def harvey_ball(slide, level, left, top, size=Inches(0.30)):
    """level: 0=empty, 1=quarter, 2=half, 3=three-quarter, 4=full"""
    colors = {0: LIGHT_GRAY, 1: TIER_LIGHT, 2: TIER_MED, 3: TIER_DARK, 4: DARK_NAVY}
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    circle.fill.solid()
    circle.fill.fore_color.rgb = colors.get(level, LIGHT_GRAY)
    circle.line.color.rgb = DARK_GRAY
    circle.line.width = Pt(0.5)
    return circle
```

#### 14. Heat Map Table

```python
def heat_map_table(slide, headers, rows, left=CONTENT_LEFT, top=CONTENT_TOP, width=CONTENT_WIDTH):
    """rows: list of (label, [values]) where values are (text, color) tuples"""
    n_rows = len(rows) + 1
    n_cols = len(headers) + 1
    tbl_shape = slide.shapes.add_table(n_rows, n_cols, left, top, width, Inches(0.5 * n_rows))
    table = tbl_shape.table

    for j, h in enumerate(headers):
        cell = table.cell(0, j + 1)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        for p in cell.text_frame.paragraphs:
            set_font(p.runs[0] if p.runs else p.add_run(), size=11, bold=True, color=WHITE)

    for i, (label, values) in enumerate(rows):
        table.cell(i + 1, 0).text = label
        for p in table.cell(i + 1, 0).text_frame.paragraphs:
            set_font(p.runs[0] if p.runs else p.add_run(), size=11, bold=True, color=DARK_NAVY)
        for j, (text, color) in enumerate(values):
            cell = table.cell(i + 1, j + 1)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = color
            for p in cell.text_frame.paragraphs:
                set_font(p.runs[0] if p.runs else p.add_run(), size=10, color=DARK_GRAY)
```

#### 15. Assessment Scorecard Grid

Build as a table with colored cells — use `heat_map_table` with maturity-level colors (`TIER_LIGHT`, `TIER_MED`, `TIER_DARK`, `DARK_NAVY`).

### D. Comparison & Matrix

#### 16. Split Panel

```python
def split_panel(slide, left_label, left_items, right_label, right_items, top=Inches(1.10)):
    """items: list of (number, title, body) tuples"""
    mid = Inches(6.67)
    for i, ((ln, lt, lb), (rn, rt, rb)) in enumerate(zip(left_items, right_items)):
        y = top + Inches(i * 1.8)
        num = slide.shapes.add_textbox(mid - Inches(0.4), y, Inches(0.8), Inches(0.5))
        p = num.text_frame.paragraphs[0]
        p.text = f"{ln:02d}"
        p.alignment = PP_ALIGN.CENTER
        set_font(p.runs[0] if p.runs else p.add_run(), size=28, bold=True, color=DARK_NAVY)
        slide.shapes.add_textbox(Inches(1.5), y, Inches(3.4), Inches(0.3)).text_frame.paragraphs[0].text = lt
        slide.shapes.add_textbox(Inches(1.5), y + Inches(0.3), Inches(3.4), Inches(0.8)).text_frame.paragraphs[0].text = lb
        slide.shapes.add_textbox(Inches(8.4), y, Inches(3.4), Inches(0.3)).text_frame.paragraphs[0].text = rt
        slide.shapes.add_textbox(Inches(8.4), y + Inches(0.3), Inches(3.4), Inches(0.8)).text_frame.paragraphs[0].text = rb
```

#### 17. Push / Pull / Hybrid Comparison

```python
def three_option_comparison(slide, options, top=Inches(1.10)):
    """options: list of 3 (title, description, pros, cons) tuples"""
    positions = [Inches(0.50), Inches(4.60), Inches(8.70)]
    col_w = Inches(3.80)
    for i, (title, desc, pros, cons) in enumerate(options):
        x = positions[i]
        navy_header_bar(slide, title, x, top, col_w, Inches(0.40))
        d = slide.shapes.add_textbox(x, top + Inches(0.50), col_w, Inches(1.5))
        d.text_frame.word_wrap = True
        p = d.text_frame.paragraphs[0]
        p.text = desc
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, color=DARK_GRAY)
        pro_box = gray_card(slide, x, top + Inches(2.20), col_w, Inches(1.2))
        tf = pro_box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = f"Positives\n{pros}"
        set_font(p.runs[0] if p.runs else p.add_run(), size=11, bold=True, color=DARK_NAVY)
        con_box = gray_card(slide, x, top + Inches(3.50), col_w, Inches(1.2))
        tf = con_box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = f"Challenges\n{cons}"
        set_font(p.runs[0] if p.runs else p.add_run(), size=11, bold=True, color=DARK_NAVY)
```

#### 18. 2x2 Matrix

```python
def two_by_two_matrix(slide, x_labels, y_labels, quadrants, top=Inches(1.50)):
    tbl = slide.shapes.add_table(3, 3, Inches(1.5), top, Inches(10.0), Inches(4.5))
    table = tbl.table
    table.cell(0, 1).text = x_labels[0]
    table.cell(0, 2).text = x_labels[1]
    table.cell(1, 0).text = y_labels[0]
    table.cell(2, 0).text = y_labels[1]
    table.cell(1, 1).text = quadrants[0][0]
    table.cell(1, 2).text = quadrants[0][1]
    table.cell(2, 1).text = quadrants[1][0]
    table.cell(2, 2).text = quadrants[1][1]
    for cell in [table.cell(0, 1), table.cell(0, 2), table.cell(1, 0), table.cell(2, 0)]:
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        for p in cell.text_frame.paragraphs:
            set_font(p.runs[0] if p.runs else p.add_run(), size=12, bold=True, color=WHITE)
```

#### 19. Persona Comparison Columns

```python
def persona_columns(slide, personas, row_labels, top=Inches(1.10)):
    col_w = Inches(3.90)
    positions = [Inches(0.80), Inches(5.00), Inches(9.10)]
    for i, (name, _) in enumerate(personas):
        navy_header_bar(slide, name, positions[i], top, col_w, Inches(0.50))
    for r, label in enumerate(row_labels):
        y = top + Inches(0.60 + r * 1.5)
        lbl = slide.shapes.add_textbox(Inches(0.0), y, Inches(1.2), Inches(0.3))
        p = lbl.text_frame.paragraphs[0]
        p.text = label
        set_font(p.runs[0] if p.runs else p.add_run(), size=10, bold=True, color=METIS_BLUE)
        for i, (_, rows) in enumerate(personas):
            card = gray_card(slide, positions[i], y, col_w, Inches(1.3))
            tf = card.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.08)
            tf.margin_top = Inches(0.05)
            p = tf.paragraphs[0]
            p.text = rows[r] if r < len(rows) else ""
            set_font(p.runs[0] if p.runs else p.add_run(), size=11, color=DARK_GRAY)
```

#### 20. Before / After Evolution

```python
def before_after(slide, before_title, before_items, after_title, after_items, top=Inches(1.10)):
    col_w = Inches(5.50)
    navy_header_bar(slide, before_title, Inches(0.50), top, col_w)
    y = top + Inches(0.50)
    for item in before_items:
        b = slide.shapes.add_textbox(Inches(0.60), y, col_w - Inches(0.20), Inches(0.40))
        b.text_frame.word_wrap = True
        p = b.text_frame.paragraphs[0]
        p.text = f"• {item}"
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, color=DARK_GRAY)
        y += Inches(0.40)

    arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.10), Inches(3.0), Inches(1.10), Inches(0.60))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = MINT
    arrow.line.fill.background()

    navy_header_bar(slide, after_title, Inches(7.30), top, col_w)
    y = top + Inches(0.50)
    for item in after_items:
        b = slide.shapes.add_textbox(Inches(7.40), y, col_w - Inches(0.20), Inches(0.40))
        b.text_frame.word_wrap = True
        p = b.text_frame.paragraphs[0]
        p.text = f"• {item}"
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, color=DARK_GRAY)
        y += Inches(0.40)
```

### E. Process & Flow

#### 21. Phased Approach

```python
def phased_approach(slide, phases, top=Inches(1.10)):
    """phases: list of 3 (title, activities_text, deliverables_text)"""
    col_w = Inches(4.0)
    positions = [Inches(0.40), Inches(4.60), Inches(8.80)]
    act_label_y = top + Inches(0.80)
    del_label_y = top + Inches(3.50)

    for label, y in [("Activities", act_label_y), ("Deliverables", del_label_y)]:
        lbl = slide.shapes.add_textbox(Inches(0.05), y, Inches(0.35), Inches(0.3))
        p = lbl.text_frame.paragraphs[0]
        p.text = label
        set_font(p.runs[0] if p.runs else p.add_run(), size=9, bold=True, color=METIS_BLUE)

    for i, (title, activities, deliverables) in enumerate(phases):
        x = positions[i]
        navy_header_bar(slide, title, x, top, col_w, Inches(0.65))
        act = gray_card(slide, x, act_label_y, col_w, Inches(2.50))
        tf = act.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.10)
        tf.margin_top = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = activities
        set_font(p.runs[0] if p.runs else p.add_run(), size=11, color=DARK_GRAY)
        dlv = gray_card(slide, x, del_label_y, col_w, Inches(1.80))
        tf = dlv.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.10)
        tf.margin_top = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = deliverables
        set_font(p.runs[0] if p.runs else p.add_run(), size=11, color=DARK_GRAY)
```

#### 22. Connected Circle Process

```python
def connected_process(slide, steps, top=Inches(1.50)):
    """steps: list of (number, title, description)"""
    n = len(steps)
    spacing = 12.33 / n
    circle_size = Inches(0.60)

    for i, (num, title, desc) in enumerate(steps):
        cx = Inches(0.50 + i * spacing + spacing / 2) - circle_size / 2
        c = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx, top, circle_size, circle_size)
        c.fill.solid()
        c.fill.fore_color.rgb = DARK_NAVY
        c.line.fill.background()
        tf = c.text_frame
        p = tf.paragraphs[0]
        p.text = str(num)
        p.alignment = PP_ALIGN.CENTER
        set_font(p.runs[0] if p.runs else p.add_run(), size=16, bold=True, color=WHITE)

        if i < n - 1:
            line_x = cx + circle_size
            line_w = Inches(spacing) - circle_size
            ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                line_x, top + circle_size / 2 - Inches(0.015),
                line_w, Inches(0.03))
            ln.fill.solid()
            ln.fill.fore_color.rgb = MINT
            ln.line.fill.background()

        t = slide.shapes.add_textbox(Inches(0.50 + i * spacing), top + Inches(0.75),
                                      Inches(spacing), Inches(0.35))
        p = t.text_frame.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        set_font(p.runs[0] if p.runs else p.add_run(), size=14, bold=True, color=DARK_NAVY)

        d = slide.shapes.add_textbox(Inches(0.50 + i * spacing), top + Inches(1.15),
                                      Inches(spacing), Inches(2.5))
        d.text_frame.word_wrap = True
        p = d.text_frame.paragraphs[0]
        p.text = desc
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, color=DARK_GRAY)
```

#### 23. Stage Ribbon

```python
def stage_ribbon(slide, stages, top=Inches(1.10), height=Inches(0.55)):
    """stages: list of (label, color) tuples — use graduated brand colors"""
    n = len(stages)
    stage_w = 12.33 / n
    for i, (label, color) in enumerate(stages):
        x = Inches(0.50 + i * stage_w)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top, Inches(stage_w), height)
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()
        tf = bar.text_frame
        tf.margin_left = Inches(0.10)
        p = tf.paragraphs[0]
        p.text = label
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, bold=True, color=WHITE)
```

#### 24. Chevron / Arrow Flow

```python
def chevron_flow(slide, steps, top=Inches(2.50)):
    """steps: list of label strings"""
    n = len(steps)
    arrow_w = Inches(12.33 / n)
    arrow_h = Inches(0.80)
    colors = [DARK_NAVY, METIS_BLUE, MINT, TIER_MED, TIER_DARK]
    for i, label in enumerate(steps):
        x = Inches(0.50) + Inches(i * 12.33 / n)
        arrow = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, x, top, arrow_w, arrow_h)
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = colors[i % len(colors)]
        arrow.line.fill.background()
        tf = arrow.text_frame
        p = tf.paragraphs[0]
        p.text = label
        p.alignment = PP_ALIGN.CENTER
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, bold=True, color=WHITE)
```

#### 25. Funnel

```python
def funnel(slide, stages, left=Inches(2.0), top=Inches(1.30)):
    """stages: list of (label, description) from widest to narrowest"""
    n = len(stages)
    max_w = Inches(9.0)
    min_w = Inches(4.0)
    stage_h = Inches(0.70)
    gap = Inches(0.08)
    colors = [DARK_NAVY, METIS_BLUE, TIER_DARK, TIER_MED, MINT]

    for i, (label, desc) in enumerate(stages):
        w = max_w - Inches((max_w.inches - min_w.inches) * i / max(n - 1, 1))
        x = left + (max_w - w) / 2
        y = top + Inches(i * (stage_h.inches + gap.inches))
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, stage_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = colors[i % len(colors)]
        bar.line.fill.background()
        tf = bar.text_frame
        tf.margin_left = Inches(0.15)
        p = tf.paragraphs[0]
        p.text = f"{label}  —  {desc}"
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, bold=True, color=WHITE)
```

#### 26. Radial / Lifecycle Diagram

```python
import math

def radial_diagram(slide, center_text, items, center_x=6.67, center_y=3.75, radius=2.2):
    """items: list of (label, description) arranged around center"""
    cx, cy = Inches(center_x), Inches(center_y)
    size = Inches(1.8)
    center = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - size/2, cy - size/2, size, size)
    center.fill.solid()
    center.fill.fore_color.rgb = DARK_NAVY
    center.line.fill.background()
    tf = center.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = center_text
    p.alignment = PP_ALIGN.CENTER
    set_font(p.runs[0] if p.runs else p.add_run(), size=12, bold=True, color=WHITE)

    n = len(items)
    for i, (label, desc) in enumerate(items):
        angle = (2 * math.pi * i / n) - math.pi / 2
        ix = center_x + radius * math.cos(angle)
        iy = center_y + radius * math.sin(angle)
        box_w, box_h = Inches(2.2), Inches(1.0)
        box = gray_card(slide, Inches(ix) - box_w/2, Inches(iy) - box_h/2, box_w, box_h)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.08)
        tf.margin_top = Inches(0.05)
        p = tf.paragraphs[0]
        p.text = label
        set_font(p.runs[0] if p.runs else p.add_run(), size=11, bold=True, color=DARK_NAVY)
        if desc:
            p2 = tf.add_paragraph()
            p2.text = desc
            set_font(p2.runs[0] if p2.runs else p2.add_run(), size=9, color=DARK_GRAY)
```

#### 27. Input / Process / Output Flow

```python
def input_process_output(slide, inputs, process_steps, outputs, top=Inches(1.10)):
    """Each param is a list of strings"""
    block_h = Inches(3.5)
    positions = [(Inches(0.50), Inches(3.0), "Inputs", LIGHT_BLUE_BG),
                 (Inches(3.80), Inches(5.2), "Approach", LIGHT_BLUE_BG),
                 (Inches(9.30), Inches(3.0), "Outputs", LIGHT_BLUE_BG)]
    data = [inputs, process_steps, outputs]

    for (x, w, label, bg_color), items in zip(positions, data):
        block = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, top, w, block_h)
        block.fill.solid()
        block.fill.fore_color.rgb = bg_color
        block.line.fill.background()
        lbl = slide.shapes.add_textbox(x + Inches(0.15), top + Inches(0.10), w - Inches(0.30), Inches(0.30))
        p = lbl.text_frame.paragraphs[0]
        p.text = label
        set_font(p.runs[0] if p.runs else p.add_run(), size=14, bold=True, color=DARK_NAVY)
        y = top + Inches(0.50)
        for item in items:
            card = gray_card(slide, x + Inches(0.15), y, w - Inches(0.30), Inches(0.35))
            tf = card.text_frame
            tf.margin_left = Inches(0.08)
            p = tf.paragraphs[0]
            p.text = item
            set_font(p.runs[0] if p.runs else p.add_run(), size=10, color=DARK_GRAY)
            y += Inches(0.40)
```

### F. Timeline & Roadmap

#### 28. 30/60/90 Day Backlog

```python
def backlog_30_60_90(slide, periods, top=Inches(1.10)):
    """periods: list of 3 (label, objective, [activities])"""
    col_w = Inches(3.70)
    positions = [Inches(1.40), Inches(5.20), Inches(9.00)]
    row_labels = [("Milestone", Inches(1.30)), ("Objective", Inches(1.80)), ("Activities", Inches(3.10))]

    for label, y in row_labels:
        lbl = slide.shapes.add_textbox(Inches(0.30), y, Inches(1.0), Inches(0.3))
        p = lbl.text_frame.paragraphs[0]
        p.text = label
        set_font(p.runs[0] if p.runs else p.add_run(), size=11, bold=True, color=METIS_BLUE)

    for i, (label, objective, activities) in enumerate(periods):
        x = positions[i]
        navy_header_bar(slide, label, x, top, col_w, Inches(0.50))
        obj = gray_card(slide, x, Inches(1.80), col_w, Inches(0.80))
        tf = obj.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = objective
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, color=DARK_GRAY)
        act = gray_card(slide, x, Inches(3.10), col_w, Inches(3.0))
        tf = act.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.08)
        tf.margin_top = Inches(0.05)
        p = tf.paragraphs[0]
        p.text = "\n".join(f"• {a}" for a in activities)
        set_font(p.runs[0] if p.runs else p.add_run(), size=11, color=DARK_GRAY)
```

#### 29. Swimlane Gantt / Roadmap

```python
def swimlane_roadmap(slide, rows, time_columns, top=Inches(1.10)):
    n_cols = len(time_columns) + 1
    n_rows = len(rows) + 1
    tbl = slide.shapes.add_table(n_rows, n_cols, Inches(0.40), top,
                                  Inches(12.50), Inches(0.60 * n_rows))
    table = tbl.table

    for j, col in enumerate(time_columns):
        cell = table.cell(0, j + 1)
        cell.text = col
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        for p in cell.text_frame.paragraphs:
            set_font(p.runs[0] if p.runs else p.add_run(), size=11, bold=True, color=WHITE)

    for i, (label, bars) in enumerate(rows):
        cell = table.cell(i + 1, 0)
        cell.text = label
        cell.fill.solid()
        cell.fill.fore_color.rgb = LIGHT_GRAY
        for p in cell.text_frame.paragraphs:
            set_font(p.runs[0] if p.runs else p.add_run(), size=10, bold=True, color=DARK_NAVY)
        for start, span, text, color in bars:
            for s in range(span):
                c = table.cell(i + 1, start + s + 1)
                c.fill.solid()
                c.fill.fore_color.rgb = color
            first_cell = table.cell(i + 1, start + 1)
            first_cell.text = text
            for p in first_cell.text_frame.paragraphs:
                set_font(p.runs[0] if p.runs else p.add_run(), size=9, color=WHITE)
```

#### 30. Use Case Opportunity Map

```python
def opportunity_map(slide, focus_areas, top=Inches(1.10)):
    n = len(focus_areas)
    row_h = Inches(1.0)
    label_w = Inches(1.2)
    card_area_w = Inches(9.5)

    for i, (area, cases) in enumerate(focus_areas):
        y = top + Inches(i * (row_h + 0.10))
        lbl = slide.shapes.add_textbox(Inches(0.20), y, label_w, row_h)
        lbl.text_frame.word_wrap = True
        p = lbl.text_frame.paragraphs[0]
        p.text = area
        set_font(p.runs[0] if p.runs else p.add_run(), size=10, bold=True, color=DARK_NAVY)

        n_cases = len(cases)
        card_w = min(Inches(1.8), Inches(card_area_w.inches / max(n_cases, 1)))
        for j, (uc, roi) in enumerate(cases):
            cx = Inches(1.50 + j * (card_w + Inches(0.10)).inches)
            card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, y, card_w, row_h)
            card.fill.solid()
            # NOTE: #1B5079 is not a named brand constant; consider adding DARK_BLUE_ACCENT
            card.fill.fore_color.rgb = RGBColor(0x1B, 0x50, 0x79)
            card.line.fill.background()
            tf = card.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.06)
            tf.margin_top = Inches(0.05)
            p = tf.paragraphs[0]
            p.text = uc
            set_font(p.runs[0] if p.runs else p.add_run(), size=9, bold=True, color=WHITE)
            p2 = tf.add_paragraph()
            p2.text = roi
            set_font(p2.runs[0] if p2.runs else p2.add_run(), size=9, color=MINT)
```

### G. Framework / Conceptual

#### 31. Layered Framework Stack

```python
def framework_stack(slide, layers, top=Inches(1.10)):
    """layers: list of (name, description, [sub_components]) from top to bottom"""
    n = len(layers)
    layer_h = Inches(5.50 / n)
    gap = Inches(0.08)
    colors = [DARK_NAVY, METIS_BLUE, TIER_DARK, TIER_MED]

    for i, (name, desc, subs) in enumerate(layers):
        y = top + Inches(i * (layer_h + gap).inches)
        band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.50), y, Inches(12.33), layer_h)
        band.fill.solid()
        band.fill.fore_color.rgb = colors[i % len(colors)]
        band.line.fill.background()
        nm = slide.shapes.add_textbox(Inches(0.60), y + Inches(0.05), Inches(2.5), Inches(0.35))
        p = nm.text_frame.paragraphs[0]
        p.text = name
        set_font(p.runs[0] if p.runs else p.add_run(), size=14, bold=True, color=WHITE)
        d = slide.shapes.add_textbox(Inches(0.60), y + Inches(0.35), Inches(2.5), layer_h - Inches(0.40))
        d.text_frame.word_wrap = True
        p = d.text_frame.paragraphs[0]
        p.text = desc
        set_font(p.runs[0] if p.runs else p.add_run(), size=10, color=WHITE)
        if subs:
            sub_w = Inches(1.4)
            for j, sub in enumerate(subs):
                sx = Inches(3.50 + j * (sub_w + Inches(0.10)).inches)
                sub_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, y + Inches(0.15),
                                                  sub_w, layer_h - Inches(0.30))
                sub_box.fill.solid()
                # Dynamic lightening: lighten the band color by +40 per channel
                sub_box.fill.fore_color.rgb = RGBColor(
                    min(colors[i % len(colors)].red + 40, 255),
                    min(colors[i % len(colors)].green + 40, 255),
                    min(colors[i % len(colors)].blue + 40, 255))
                sub_box.line.fill.background()
                tf = sub_box.text_frame
                tf.word_wrap = True
                tf.margin_left = Inches(0.06)
                p = tf.paragraphs[0]
                p.text = sub
                set_font(p.runs[0] if p.runs else p.add_run(), size=9, color=WHITE)
```

#### 32. Hub-and-Spoke Diagram

```python
def hub_and_spoke(slide, hub_text, spokes, center_x=6.67, center_y=3.75, radius=2.5):
    """spokes: list of (label, color) tuples"""
    hub_size = Inches(1.6)
    hub = slide.shapes.add_shape(MSO_SHAPE.OVAL,
        Inches(center_x) - hub_size/2, Inches(center_y) - hub_size/2, hub_size, hub_size)
    hub.fill.solid()
    hub.fill.fore_color.rgb = DARK_NAVY
    hub.line.fill.background()
    tf = hub.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = hub_text
    p.alignment = PP_ALIGN.CENTER
    set_font(p.runs[0] if p.runs else p.add_run(), size=11, bold=True, color=WHITE)

    n = len(spokes)
    spoke_size = Inches(0.70)
    for i, (label, color) in enumerate(spokes):
        angle = (2 * math.pi * i / n) - math.pi / 2
        sx = center_x + radius * math.cos(angle)
        sy = center_y + radius * math.sin(angle)
        s = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            Inches(sx) - spoke_size/2, Inches(sy) - spoke_size/2, spoke_size, spoke_size)
        s.fill.solid()
        s.fill.fore_color.rgb = color
        s.line.fill.background()
        tf = s.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = label
        p.alignment = PP_ALIGN.CENTER
        set_font(p.runs[0] if p.runs else p.add_run(), size=9, bold=True, color=WHITE)
```

#### 33. Maturity Journey Curve

```python
def maturity_journey(slide, stages, top=Inches(1.50)):
    """stages: list of (name, description) from lowest to highest maturity"""
    n = len(stages)
    step_w = Inches(12.33 / n)
    base_y = Inches(4.50)
    rise = Inches(2.50)

    for i, (name, desc) in enumerate(stages):
        x = Inches(0.50) + Inches(i * step_w.inches)
        y_offset = rise * (i / max(n - 1, 1))
        dot_y = base_y - y_offset

        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, x + step_w / 2 - Inches(0.25),
                                      dot_y, Inches(0.50), Inches(0.50))
        dot.fill.solid()
        dot.fill.fore_color.rgb = DARK_NAVY
        dot.line.fill.background()

        lbl = slide.shapes.add_textbox(x, dot_y + Inches(0.55), step_w, Inches(0.30))
        p = lbl.text_frame.paragraphs[0]
        p.text = name
        p.alignment = PP_ALIGN.CENTER
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, bold=True, color=DARK_NAVY)

        d = slide.shapes.add_textbox(x, dot_y + Inches(0.85), step_w, Inches(1.5))
        d.text_frame.word_wrap = True
        p = d.text_frame.paragraphs[0]
        p.text = desc
        set_font(p.runs[0] if p.runs else p.add_run(), size=10, color=DARK_GRAY)

        if i < n - 1:
            ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                x + step_w / 2 + Inches(0.25), dot_y + Inches(0.25),
                step_w - Inches(0.50), Inches(0.02))
            ln.fill.solid()
            ln.fill.fore_color.rgb = MINT
            ln.line.fill.background()
```

#### 34. Hexagon Grid / Pyramid / Venn

**Pyramid:**

```python
def pyramid(slide, layers, left=Inches(3.0), top=Inches(1.30)):
    """layers: list of strings from top (narrowest) to bottom (widest)"""
    n = len(layers)
    max_w = Inches(7.0)
    min_w = Inches(2.5)
    layer_h = Inches(0.80)
    colors = [DARK_NAVY, METIS_BLUE, TIER_DARK, TIER_MED, MINT]

    for i, label in enumerate(layers):
        w = min_w + (max_w - min_w) * (i / max(n - 1, 1))
        x = left + (max_w - w) / 2
        y = top + Inches(i * (layer_h + Inches(0.05)).inches)
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, layer_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = colors[i % len(colors)]
        shape.line.fill.background()
        tf = shape.text_frame
        p = tf.paragraphs[0]
        p.text = label
        p.alignment = PP_ALIGN.CENTER
        set_font(p.runs[0] if p.runs else p.add_run(), size=12, bold=True, color=WHITE)
```

**Venn (2-circle):**

```python
def venn_diagram(slide, left_label, right_label, overlap_label,
                  center_x=6.67, center_y=3.75):
    size = Inches(3.5)
    offset = Inches(1.2)
    for label, dx, color in [(left_label, -offset, DARK_NAVY), (right_label, offset, METIS_BLUE)]:
        c = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            Inches(center_x) + dx - size/2, Inches(center_y) - size/2, size, size)
        c.fill.solid()
        c.fill.fore_color.rgb = color
        c.line.fill.background()
        # Set 50% transparency via XML
        from pptx.oxml.ns import qn
        c.fill._fill.find(qn('a:solidFill')).find(qn('a:srgbClr')).set('alpha', '50000')
    # Overlap label
    lbl = slide.shapes.add_textbox(Inches(center_x) - Inches(1.0), Inches(center_y) - Inches(0.15),
                                    Inches(2.0), Inches(0.30))
    p = lbl.text_frame.paragraphs[0]
    p.text = overlap_label
    p.alignment = PP_ALIGN.CENTER
    set_font(p.runs[0] if p.runs else p.add_run(), size=14, bold=True, color=WHITE)
```

### H. Narrative

#### 36. Pull Quote Block

```python
def pull_quote(slide, quote_text, attribution, top=Inches(2.00)):
    q = slide.shapes.add_textbox(Inches(0.50), top, Inches(1.0), Inches(1.0))
    p = q.text_frame.paragraphs[0]
    p.text = "\u201C"
    set_font(p.runs[0] if p.runs else p.add_run(), size=72, bold=True, color=MINT)

    qt = slide.shapes.add_textbox(Inches(1.50), top + Inches(0.30), Inches(10.0), Inches(2.5))
    qt.text_frame.word_wrap = True
    p = qt.text_frame.paragraphs[0]
    p.text = quote_text
    run = p.runs[0] if p.runs else p.add_run()
    run.font.name = 'Calibri'
    run.font.size = Pt(18)
    run.font.italic = True
    run.font.color.rgb = DARK_NAVY

    attr = slide.shapes.add_textbox(Inches(1.50), top + Inches(3.00), Inches(10.0), Inches(0.40))
    p = attr.text_frame.paragraphs[0]
    p.text = f"— {attribution}"
    set_font(p.runs[0] if p.runs else p.add_run(), size=14, color=DARK_GRAY)
```

*(Note: Component #35 is not defined — numbering gap is intentional.)*

---

## Universal Closers & Metaphor Primitives

Three recipes that show up on nearly every polished Metis content slide
regardless of the body component, plus a small library of shape primitives
for building bespoke metaphor diagrams when the Timesaver library doesn't
have a perfect match.

### Optional: Bottom Takeaway Bar (use rarely)

**Not a default. Reserve for rare emphasis**, a section-opener or a
conclusion slide, never on every content slide (see SKILL.md §0.5 and §0.7).
A navy mantra bar on every slide is one of the loudest "AI deck" tells, and it
appears on **zero** of the 53 slides in the LiveRamp deliverable. When a slide
needs a takeaway, prefer putting it in the title; use this bar only when the
emphasis genuinely warrants a full-width device. Full-width Dark Navy bar with
optional Mint left accent, white bold text, single line.

```python
def add_takeaway_bar(slide, text, y=6.05, with_mint_accent=True):
    """Optional emphasis bar. Use rarely (see SKILL.md §0.7), not as a closer on every slide."""
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.50), Inches(y), Inches(12.33), Inches(0.65)
    )
    bar.fill.solid(); bar.fill.fore_color.rgb = DARK_NAVY
    bar.line.fill.background()

    if with_mint_accent:
        accent = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.50), Inches(y), Inches(0.10), Inches(0.65)
        )
        accent.fill.solid(); accent.fill.fore_color.rgb = MINT
        accent.line.fill.background()

    txt = slide.shapes.add_textbox(Inches(0.75), Inches(y), Inches(12.00), Inches(0.65))
    txt.text_frame.word_wrap = True
    txt.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = txt.text_frame.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.LEFT
    run = p.runs[0] if p.runs else p.add_run()
    run.font.name = "Calibri"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = WHITE
```

**Writing the mantra:** It must fit on one line and be the slide's single
most important insight. If you can't compress the slide to one mantra,
the slide isn't focused enough — split it or cut content.

### Universal: KPI Stat Callout Block (2x3 grid)

Use for "by the numbers" slides — top row filled-bold (headline KPIs),
bottom row outlined (supporting metrics). Always followed by a takeaway bar.

```python
def add_kpi_grid_2x3(slide, top_stats, bottom_stats, y_top=1.80, h=1.85, gap=0.20):
    """
    top_stats / bottom_stats: list of 3 dicts with keys: stat, label, body.
    Top row: filled boxes (DARK_NAVY / METIS_BLUE / DARK_NAVY) with white text.
    Bottom row: light-gray boxes with MINT left accent and DARK_NAVY text.
    """
    col_w = (12.33 - 2 * gap) / 3
    row_fills = [DARK_NAVY, METIS_BLUE, DARK_NAVY]

    # Top row — filled, white text
    for i, s in enumerate(top_stats):
        x = 0.50 + i * (col_w + gap)
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y_top), Inches(col_w), Inches(h))
        box.fill.solid(); box.fill.fore_color.rgb = row_fills[i]
        box.line.fill.background()
        # Stat (large)
        _add_text(slide, x + 0.20, y_top + 0.20, col_w - 0.40, 0.90,
                  s["stat"], size=44, bold=True, color=WHITE)
        # Label
        _add_text(slide, x + 0.20, y_top + 1.00, col_w - 0.40, 0.35,
                  s["label"], size=14, bold=True, color=WHITE)
        # Body
        _add_text(slide, x + 0.20, y_top + 1.35, col_w - 0.40, 0.45,
                  s["body"], size=11, bold=False, color=WHITE)

    # Bottom row — outlined, gray bg, MINT accent
    y_bot = y_top + h + gap
    for i, s in enumerate(bottom_stats):
        x = 0.50 + i * (col_w + gap)
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y_bot), Inches(col_w), Inches(h))
        box.fill.solid(); box.fill.fore_color.rgb = LIGHT_GRAY
        box.line.fill.background()
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y_bot), Inches(0.08), Inches(h))
        accent.fill.solid(); accent.fill.fore_color.rgb = MINT
        accent.line.fill.background()
        _add_text(slide, x + 0.25, y_bot + 0.20, col_w - 0.40, 0.70,
                  s["stat"], size=32, bold=True, color=DARK_NAVY)
        _add_text(slide, x + 0.25, y_bot + 0.95, col_w - 0.40, 0.35,
                  s["label"], size=12, bold=True, color=DARK_NAVY)
        _add_text(slide, x + 0.25, y_bot + 1.30, col_w - 0.40, 0.50,
                  s["body"], size=10, bold=False, color=DARK_GRAY)

# Then call add_takeaway_bar(slide, "...mantra...") below.
```

`_add_text` is a small textbox helper (see `add_text()` patterns elsewhere
in this file).

### Metaphor Primitives

When the Timesaver doesn't have your shape, build it from primitives.
Available shapes in python-pptx that map to common metaphors:

| Metaphor | python-pptx shape | Notes |
|---|---|---|
| Roof of a house | `MSO_SHAPE.ISOSCELES_TRIANGLE` | Roof wider than body looks more like a house |
| Pillar / column | `MSO_SHAPE.RECTANGLE` | Add `MSO_SHAPE.RECTANGLE` cap on top + bottom in DARK_NAVY |
| Foundation slab | `MSO_SHAPE.RECTANGLE` filled DARK_NAVY | Wider than body, ~0.9" tall |
| Hexagon (flywheel cell) | `MSO_SHAPE.HEXAGON` | For 6-cell flywheels, stagger 3 above + 3 below |
| Chevron / time horizon | `MSO_SHAPE.CHEVRON` or `MSO_SHAPE.RIGHT_ARROW_CALLOUT` | Use graduated brand colors L→R |
| Funnel layer | `MSO_SHAPE.TRAPEZOID` (or alternating triangles) | Stack with each layer narrower than the one above |
| Pyramid layer | `MSO_SHAPE.TRAPEZOID` flipped or `MSO_SHAPE.RECTANGLE` graduated widths | |
| Bullseye ring | `MSO_SHAPE.OVAL` (concentric, no fill on outer rings) | |
| Gear | `MSO_SHAPE.GEAR_6` / `MSO_SHAPE.GEAR_9` | Built-in gear shapes |
| Radial spoke | `MSO_SHAPE.OVAL` (small) on a ring around a central `MSO_SHAPE.OVAL` | Use trig for placement |

### Recipe: House Metaphor (layered architecture)

The Timesaver has slide 179 ("House chart") — use that first. This recipe
is the fallback when you need to compose your own (e.g., custom number of
pillars, or a non-Metis-branded variant).

```python
def add_house_metaphor(slide, x=1.00, y=1.30, w=5.10, body_h=2.25,
                       roof_h=1.10, foundation_h=0.90,
                       roof_label="ROOF", body_label="BODY",
                       foundation_label="FOUNDATION", num_pillars=2):
    """Three-layer house: triangle roof + pillared body + foundation slab."""
    # Roof (triangle)
    roof = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE,
        Inches(x), Inches(y), Inches(w), Inches(roof_h))
    roof.fill.solid(); roof.fill.fore_color.rgb = MINT
    roof.line.fill.background()
    _add_text(slide, x, y + roof_h * 0.55, w, 0.40,
              roof_label, size=20, bold=True, color=DARK_NAVY,
              align=PP_ALIGN.CENTER)

    # Body (light interior)
    body_y = y + roof_h
    body = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(body_y), Inches(w), Inches(body_h))
    body.fill.solid(); body.fill.fore_color.rgb = LIGHT_GRAY
    body.line.fill.background()

    # Pillars
    pillar_w = 0.45
    inset = 0.0
    if num_pillars >= 2:
        for i in range(num_pillars):
            px = x + inset + i * (w - pillar_w - 2 * inset) / (num_pillars - 1)
            pillar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                Inches(px), Inches(body_y), Inches(pillar_w), Inches(body_h))
            pillar.fill.solid(); pillar.fill.fore_color.rgb = METIS_BLUE
            pillar.line.fill.background()
            # Cap top & bottom
            for cap_y in (body_y, body_y + body_h - 0.15):
                cap = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                    Inches(px - 0.05), Inches(cap_y), Inches(pillar_w + 0.10), Inches(0.15))
                cap.fill.solid(); cap.fill.fore_color.rgb = DARK_NAVY
                cap.line.fill.background()

    # Body label (centered in interior)
    _add_text(slide, x + 0.60, body_y + 0.40, w - 1.20, 0.50,
              body_label, size=20, bold=True, color=DARK_NAVY,
              align=PP_ALIGN.CENTER)

    # Foundation slab (wider than body)
    fnd_y = body_y + body_h
    fnd_x = x - 0.30
    fnd_w = w + 0.60
    fnd = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(fnd_x), Inches(fnd_y), Inches(fnd_w), Inches(foundation_h))
    fnd.fill.solid(); fnd.fill.fore_color.rgb = DARK_NAVY
    fnd.line.fill.background()
    # Mint ground line (thin strip on top of foundation)
    ground = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(fnd_x), Inches(fnd_y), Inches(fnd_w), Inches(0.05))
    ground.fill.solid(); ground.fill.fore_color.rgb = MINT
    ground.line.fill.background()
    _add_text(slide, fnd_x, fnd_y + foundation_h * 0.30, fnd_w, 0.40,
              foundation_label, size=16, bold=True, color=WHITE,
              align=PP_ALIGN.CENTER)
```

This recipe was used to build CAC slide 10 ("The Architecture of
Context-as-Code"). The Timesaver template (slide 179) is the simpler default
when you only need 4 generic pillars and a single roof label.
