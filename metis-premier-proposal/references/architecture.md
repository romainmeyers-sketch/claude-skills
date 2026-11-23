# Architecture: Why ReportLab, Why Measure-First, Why YAML

This document captures the core technical decisions of the proposal PDF skill and the empirical reasoning behind each. Every decision here was learned the hard way during the Citi CRS Proposal engagement.

---

## Decision 1: ReportLab, Not HTML + Playwright

### What we tried first

HTML + CSS + Playwright. The assumption was that a web layout engine could produce a fixed-page proposal.

### What went wrong

**Vertical spacing was chronically broken.** Over five iterations of the Citi proposal, content consistently crowded at the top of each page with 100–300pt of dead whitespace at the bottom. Multiple attempted fixes failed:

1. `display: flex; flex-direction: column; justify-content: space-between` — works in browsers, unreliable in Playwright's print renderer when child heights are variable
2. `flex: 1` on inner grids — does not force child cells to grow
3. `min-height` on containers — adds height without distributing content
4. Adding spacer divs with `flex: 1` — works on some pages, not others, depends on nesting depth

The root cause is that CSS was designed for reflowable web content, not fixed-page documents. Flexbox distributes free space based on flex factors, but only works reliably when:
- The parent has an explicit height
- The flex children are also flex containers or have explicit dimensions
- No `position: absolute` breaks out of normal flow

In a proposal PDF, you have mixed content types (images, text blocks, callouts, grids) with variable heights, and the "right" distribution is not mechanical — it is design judgment. CSS cannot encode that judgment.

### Why ReportLab works

ReportLab is a PDF-native library where every element is placed at an explicit (x, y) coordinate. There is no layout engine, no reflow, no "what should the browser do?" Every coordinate is a decision you made.

Two capabilities make the measure-first pattern possible:

1. **`Paragraph.wrap(width, height)`** — returns the actual wrapped height of a text block before you draw it. You can size containers based on measured content.
2. **`canvas.stringWidth(text, font, size)`** — returns the pixel width of a string. You can auto-shrink fonts to fit cards.

With these two primitives you can write code that predicts the final layout before drawing anything, then computes positions that eliminate both overflow and whitespace.

### When HTML + Playwright IS the right stack

- Long-form whitepapers with flowing text (use `metis-whitepaper`)
- Web content that reflows for multiple screen sizes
- Documents where typography and inline layout matter more than page-level design

For proposals, executive briefs, and sales decks where every page is a hand-designed artifact, use ReportLab.

---

## Decision 2: Measure-First, Not Size-First

### The wrong pattern (cost 10+ iterations in Citi engagement)

```python
# Set container height first, then pour content in
card_h = (available_height - gutters) / rows
for item in items:
    p = Paragraph(item, style)
    p.wrap(card_w, 300)  # measure AFTER sizing
    p.drawOn(c, x, y)     # may overflow card
```

**What breaks:**
- If text is longer than expected, it overflows the card into adjacent cards (page 8 of Citi deck had 11 confirmed overlaps)
- If text is shorter, there is dead whitespace inside the card
- There is no way to know until you render

### The right pattern

```python
# Measure all content first, size container to fit tallest
heights = []
for item in items:
    p = Paragraph(item, style)
    pw, ph = p.wrap(card_w, 500)  # measure FIRST
    heights.append(ph + padding)

card_h = max(heights)  # size AFTER measuring

# Now place cards at calculated positions
for i, item in enumerate(items):
    cy = top_y - (i + 1) * card_h - i * gap
    draw_card(item, cx, cy, card_w, card_h)
```

**Why it works:**
- No card is smaller than its content
- All cards in a row are the same height (uniform grid)
- You can compute final page fill before drawing anything
- If content is too tall for the page, you can detect it before rendering and alert the user

### Where to apply this pattern

Apply measure-first to:
- Activities / deliverables two-column pages (measure both columns, use dynamic `item_gap` to fill vertical space)
- Multi-card grids (module cards, pillar cards, step cards, case study cards)
- Image pages (measure callout heights, then size image to fill remaining space)
- Numbered item lists (measure each item, use `distribute_y_positions` to spread evenly)

Helper functions in `scripts/helpers.py`:
- `measure_bullet_list(items, width, ...)` — returns total height without drawing
- `measure_body_text(text, width, ...)` — returns wrapped height
- `measure_callout_height(text, width, ...)` — predicts callout box height
- `distribute_y_positions(top_y, bottom_y, block_heights, min_gap)` — even distribution
- `fitted_card(x, y_top, w, title, body, ...)` — card sized to measured content

### Use `stringWidth` for font auto-scaling

Big numbers on metric cards have variable width (`"3"` vs `"Hyper Personalization"`). Without auto-scaling, long strings overflow the card.

```python
def metric_card(x, y, w, h, number, label):
    num_str = str(number)
    inner_w = w - 16
    num_font_size = 24
    while num_font_size > 11:
        text_w = c.stringWidth(num_str, 'Calibri-Bold', num_font_size)
        if text_w <= inner_w:
            break
        num_font_size -= 1
    c.setFont('Calibri-Bold', num_font_size)
    c.drawCentredString(x + w/2, y + h - 8 - num_font_size, num_str)
```

Every component that accepts user-authored text should be robust to length variance.

---

## Decision 3: YAML for Content, Python for Layout

### The problem

During the Citi build, the user (Andrew) wanted to tweak copy throughout the document. Every change required editing Python strings, which is:
- Error-prone (escaping, indentation)
- Intimidating for non-engineers
- Hard to review in a diff
- Mixes concerns (content with layout logic)

### The solution

Separate files:

- `<project>-copy.yaml` — all editable text, structured as `page_N_<slug>: { eyebrow, title, subtitle, activities, deliverables, callouts, metrics }`
- `build_proposal.py` — imports `yaml`, loads the file at the top, references `COPY['page_N_slug']['eyebrow']` everywhere

### Benefits

1. **Non-engineer editable.** Andrew can open the YAML in any text editor and tweak text without touching Python.
2. **Diff-friendly.** Every content change is a clean diff in one file.
3. **Forces structure.** Writing YAML forces you to identify every editable element up front, which produces cleaner code.
4. **Separation of concerns.** When a bug is in layout, you look in Python. When it's in copy, you look in YAML.

### YAML conventions

- **String quoting:** Use double quotes for strings containing apostrophes. Reserve single quotes for pure strings.
- **Bold in bullets:** Use `<b>text</b>` HTML tags inside strings. ReportLab's Paragraph renders these.
- **Em dashes:** Never use them. See `content-rules.md`.
- **Keys:** Use `page_N_<slug>` format. The N makes ordering explicit; the slug makes the key self-documenting.

Sample structure:

```yaml
page_5_module_a_overview:
  eyebrow: "MODULE A | OPERATING MODEL DESIGN"
  title: "Product Operating Model for CRS"
  subtitle: "Define the target-state operating model..."
  activities:
    - "First activity..."
    - "<b>Bold emphasis</b> on key phrase..."
  deliverables:
    - "First deliverable..."
  callouts:
    - label: "KEY INSIGHT"
      body: "The operating model is the unlock..."
```

### Wiring YAML into Python

At the top of the build script:

```python
import yaml

COPY_PATH = "G:/My Drive/Vault/_working/<project>/<project>-copy.yaml"
with open(COPY_PATH, 'r', encoding='utf-8') as _f:
    COPY = yaml.safe_load(_f)
```

Then in each page builder:

```python
_p5 = COPY['page_5_module_a_overview']
activities_deliverables_page(
    _p5['eyebrow'], _p5['title'], _p5['subtitle'],
    _p5['activities'], _p5['deliverables'],
    bottom_callouts=[(c['label'], c['body']) for c in _p5['callouts']],
)
```

Pattern: load once, reference by structured path.

---

## Decision 4: Separate Working Files from Deliverables

The vault's global CLAUDE.md enforces this, but it matters here specifically:

- **All intermediate artifacts** (build script, YAML, cropped slide images, verification PNGs, unpacked source PPTX, intermediate PDFs) live in `G:\My Drive\Vault\_working\<project>\`
- **Only the final PDF** lands on the shared drive at `G:\Shared drives\BizDev Collaboration\<Client>\<Year>\`

**Why:** Shared drives represent the firm's finished work. Intermediate artifacts are clutter and confuse other consultants who see them. Clients occasionally get access to shared drive folders — unpacked source files are embarrassing to be found.

**Additional rule:** The build script should write its PDF output to the `_working` folder first, then the deploy step copies to the shared drive. If the shared drive copy is locked (user has the PDF open), the build still succeeds.

---

## Decision 5: Always Render to PNG and Look

Bbox analysis catches overlaps but misses:
- Duplicate titles from uncropped slide images
- Image cropping issues (partial titles, partial footers)
- Color contrast problems on dark backgrounds
- Font rendering issues
- Graphic device opacity that is too low or too high
- Whitespace that feels wrong but is not technically "empty"

**The rule:** after every build, render each meaningful page to PNG at 1.5x or 2x zoom and use the Read tool to view it. This takes 30 seconds and catches issues that cost hours to discover after deployment.

Implementation in `scripts/verify.py`:

```python
for idx, label in problem_pages:
    pix = doc[idx].get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    pix.save(f'{out_dir}/{label}.png')
```

Then read each PNG and assess. Do not declare done without this step.
