# Failure Modes

A catalog of every significant failure during the Citi CRS Proposal engagement, the root cause, and the fix. Read this before starting a new proposal — most of these took hours or days to diagnose the first time.

## Contents

Architecture failures (before choosing the right stack):
1. [PDFKit text-only PDF](#1-pdfkit-text-only-pdf-v1)
2. [Pasted slide screenshots](#2-pasted-slide-screenshots-v2)
3. [Vertical spacing persistently broken](#3-vertical-spacing-persistently-broken-v3v5-htmlplaywright)

Image embedding failures:
4. [Wrong slide image references](#4-wrong-slide-image-references-multiple-iterations)
5. [Duplicate titles from uncropped slide images](#5-duplicate-titles-from-uncropped-slide-images)
6. [Image cropping that partially cut off content](#15-image-cropping-that-partially-cut-off-content)

Component failures:
7. [Metric card text overflow](#6-metric-card-text-overflow)
8. [Metric card bbox overlap](#7-metric-card-bbox-overlap-false-ish-positive)
9. [Green accent bar crossing divider titles](#8-green-accent-bar-crossing-divider-titles)
10. [Pull quote double-drawn mint bar](#9-pull-quote-double-drawn-mint-bar)
11. [Logo not rendering on dark pages](#10-logo-not-rendering-on-dark-pages)

Structural and editorial failures:
12. [Structural inconsistency across modules](#11-structural-inconsistency-across-modules)
13. [Absolute claims that are not defensible](#12-absolute-claims-that-are-not-defensible)
14. [Overusing a specific anecdote](#13-overusing-a-specific-anecdote)
15. [Named product names from past engagements](#14-named-product-names-from-past-engagements)

Process failures:
16. [Build declared done before visual verification](#16-build-declared-done-before-visual-verification)
17. [YAML key name collision](#17-yaml-key-name-collision)
18. [Trying to fix shared drive file while user has it open](#18-trying-to-fix-shared-drive-file-while-user-has-it-open)

---

## 1. PDFKit text-only PDF (v1)

**What failed:** The first PDF attempt used Node's PDFKit library to draw colored rectangles and text. No brand assets, no embedded images, no photography. Output looked like a Word document with colored headers.

**Root cause:** Treating the proposal as a text document instead of a visual artifact. PDFKit is good for programmatic PDF generation, but it is not a design tool.

**Fix:** Use the metis-whitepaper approach (HTML + Playwright) or ReportLab. Do not write a PDF with raw primitives unless the output is a simple report.

**Lesson:** "Premium proposal" means every page has photography, graphic devices, and designed layouts. Not text boxes.

---

## 2. Pasted slide screenshots (v2)

**What failed:** After the text-only PDF, the second attempt pasted full slide screenshots from the source PPTX into PDF pages as framed images. The result was duplicated headers, inconsistent margins, and visual signals that screamed "screenshot gallery."

**Root cause:** Using slide images as full page content means every page has the slide's header AND the PDF's header, which doubles up.

**Fix:** Crop slide images to remove titles/footers before embedding, and use them as figures within designed pages. Not as entire pages.

**Lesson:** If you embed a PPTX slide, first crop it to just the diagram/visual content you want. The PDF page then has its own title, and the image is supporting content.

---

## 3. Vertical spacing persistently broken (v3–v5, HTML/Playwright)

**What failed:** Across five iterations of HTML + Playwright rendering, content crowded at the top of every page with 100–300pt of dead whitespace at the bottom.

**Root causes (compound):**
1. Initial CSS had content flowing naturally with no distribution mechanism
2. Adding `display: flex; flex-direction: column` helped some pages but not others
3. `margin-top: auto` on bottom elements only works if the parent is a flex container
4. Nested grids broke flex distribution
5. I incorrectly claimed "flexbox doesn't work in Playwright print" after a failed attempt, then REMOVED the flexbox, making things worse

**Fix:** Switch to ReportLab with coordinate-based placement. See `architecture.md` for the reasoning.

**Lesson:** If a fix is failing repeatedly, diagnose the mechanism instead of adding more patches. Print a test page with ONLY the layout pattern in question. Don't conclude "it doesn't work" without testing in isolation.

---

## 4. Wrong slide image references (multiple iterations)

**What failed:** Page 7 (POM Maturity Dimensions) showed the Module B divider image instead of the book-style dimensions diagram. Page 11 (Hub-and-Spoke) showed the responsibilities detail instead of the CRS-tailored current-to-target diagram. Page 12 (Data & AI Framework) showed the maturity assessment model instead of the actual framework.

**Root cause:** When slide images are exported from a PPTX, the numbering is sequential from the deck as it exists at export time. But during the build, the deck gets trimmed and reordered, and the mental mapping between "slide 14 in the 33-slide deck" and "slide-14.png from the 31-image export" can drift.

**Fix:**
1. After exporting slide images, open each PNG and label what it contains in a mapping document
2. Reference the mapping document in the build script comments
3. Visual verification catches mismatches — always render and look

**Lesson:** Slide image filenames are not self-documenting. Maintain a mapping between filename and visual content.

---

## 5. Duplicate titles from uncropped slide images

**What failed:** Pages 7, 11, 12 showed both a PDF-generated title ("Dimensions of Product Operating Model Maturity") and the same title embedded in the slide screenshot. Visually two identical headers stacked.

**Root cause:** The exported slide screenshots contain the original slide title, subtitle, and footer. Embedding them as-is on a page that also has a PDF title produces the duplication.

**Fix:** Before embedding, crop the slide image to remove the top ~120pt (title + subtitle) and bottom ~45pt (footer). Save as `<slide-N>-cropped.png`.

```python
from PIL import Image
img = Image.open(f'slide-{n}.png')
cropped = img.crop((0, 120, 2000, 1080))  # trim top 120, bottom 45
cropped.save(f'slide-{n}-cropped.png')
```

**Lesson:** Slide screenshots must always be cropped before embedding. If this step is skipped, the page will have duplicate titles regardless of layout quality.

---

## 6. Metric card text overflow

**What failed:** Metric cards like "3 Converging Efforts" and "Hyper Personalization" overflowed their card width because the 24pt big-number font could not fit the label in the card's ~180pt width.

**Root cause:** The `metric_card` function used `drawCentredString` with a fixed 24pt font. No auto-scaling.

**Fix:** Use `canvas.stringWidth` to check whether the text fits, and shrink the font until it does:

```python
num_font_size = 24
while num_font_size > 11:
    text_w = c.stringWidth(num_str, 'Calibri-Bold', num_font_size)
    if text_w <= inner_w:
        break
    num_font_size -= 1
```

**Lesson:** Every component that accepts user-authored text should be robust to string length. Auto-scaling is a one-time cost that prevents every "long label" bug.

---

## 7. Metric card bbox overlap (false-ish positive)

**What failed:** On pages 18 and 20, bbox overlap detection flagged the big number and small label within the same metric card as overlapping.

**Root cause:** Card was 48pt tall. The 24pt number's glyph descenders extended into the region where the 7pt label's ascenders lived, producing a tiny (3pt) bbox overlap that looked real to the detector but was not visually problematic.

**Fix:** Increase metric card height from 48pt to 56pt when large numbers are used. This eliminates the bbox overlap and provides better breathing room.

**Lesson:** Metric cards need vertical padding proportional to the big-number font size. As a rule: card height ≥ big_font_size × 2.3.

---

## 8. Green accent bar crossing divider titles

**What failed:** On section dividers, the green accent bar (at `y = H/2 + 20`) crossed through the title text (baseline at `y = H/2 + 10`). The bar intersected the top of the title glyphs.

**Root cause:** The bar was placed at a Y coordinate relative to the title's baseline, not relative to the top of the title glyph bounding box. Bold uppercase text at 26pt has glyphs that extend roughly 22pt above the baseline.

**Fix:** Measure the title block height first, compute the top of the glyph block, then place the bar 12pt above that top:

```python
title_font_size = 26
title_leading = 32
lines = title_text.split('\n')
title_block_h = title_leading * len(lines)
title_top_y = title_center_y + title_block_h / 2
bar_y = title_top_y + 12  # ABOVE the top of glyphs
```

**Lesson:** When placing decorative elements near text, think in terms of glyph boxes, not baselines. The baseline is ~20% of font size below the top of the glyph.

---

## 9. Pull quote double-drawn mint bar

**What failed:** Page 2 pull quote had the mint left bar drawing twice — once at a guessed 50pt height and once at the measured text height. The guessed-height bar extended below the actual text, intruding into the metric cards area below.

**Root cause:** Original `pull_quote` function drew a 50pt bar first as a "placeholder" and then another bar sized to the measured text. The first draw was never cleaned up.

**Fix:** Single draw, using the measured text height:

```python
def pull_quote(x, y, text, width, size=11):
    style = ParagraphStyle('pq', fontName='Calibri-Bold', fontSize=size, leading=size*1.45,
                           textColor=DARK_NAVY, fontStyle='italic')
    p = Paragraph(f'<i>{text}</i>', style)
    pw, ph = p.wrap(width - 16, 200)
    draw_rect(x, y - ph - 8, 3, ph + 6, MINT)  # SINGLE bar, sized to text
    p.drawOn(c, x + 12, y - ph - 4)
    return ph + 12
```

**Lesson:** Don't draw elements "speculatively" with hardcoded dimensions. Measure first, draw once.

---

## 10. Logo not rendering on dark pages

**What failed:** On the cover and section dividers, the call `place_image(LOGO_WM, 48, H - 50, w=80)` appeared to do nothing. Logo was completely absent from the rendered PDF.

**Root cause:** ReportLab's `drawImage` with `preserveAspectRatio=True` and `width=80, height=None` is inconsistently handled. On some builds it renders correctly; on others it renders as a 0-height image or fails silently.

**Fix:** Compute the height explicitly using PIL's image dimensions:

```python
def place_image(path, x, y, w=None, h=None, mask='auto'):
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
```

**Lesson:** Always pass explicit width AND height to `drawImage`. The `preserveAspectRatio` flag is not a substitute for explicit dimensions.

---

## 11. Structural inconsistency across modules

**What failed:** Module A had 4 pages (overview + POM concept + POM maturity + phased approach). Modules B, C, D each had 1–2 pages. This created visual imbalance and signaled that the four modules were not comparable in depth.

**Root cause:** Module A had more content readily available in the source material, so it got more pages. There was no structural constraint.

**Fix:** Delete the extra pages. Each module gets the same structure: divider (sometimes), overview (always), optional 1 content page. Keep page count per module within ±1.

When a page seems "useful" but breaks structural consistency, ask: is it more useful than the signal it sends about uneven scope? Usually the answer is no.

**Lesson:** Structural consistency across repeating sections is part of the content, not just the layout.

---

## 12. Absolute claims that are not defensible

**What failed:** Metric card labels included "Zero" ("Zero CRS digital sales metrics exist today") which was caught by the user as an unsupported absolute claim.

**Root cause:** When summarizing a buyer's pain point in 1–2 words, it is tempting to use superlatives. "Zero" is more dramatic than "Baseline". But the buyer didn't say "zero" — they said the business didn't have sales metrics "to even guide them". That's a rough statement, not a claim about literal zero.

**Fix:** Replace absolutes with descriptive words: "Baseline" (to be established), "Dozens" (of contracts), "Ongoing" (challenge), "Complex" (environment).

**Lesson:** Absolutes are legal/factual claims. If you can't defend them with evidence, don't use them.

---

## 13. Overusing a specific anecdote

**What failed:** The Samsung reference (the buyer's comment about Samsung's 14-day delivery vs. banking's slower pace) appeared in 3+ different places across early iterations. Andrew caught it as overindexing — repeated use of the same reference feels like a crutch.

**Root cause:** When you find a vivid quote from the buyer, it is tempting to use it everywhere because it lands. But repetition diminishes impact.

**Fix:** Use any specific quote or anecdote at most twice: once in the problem framing, and optionally once in a module callout for continuity.

**Lesson:** Vivid references have diminishing returns. One really strong placement is better than three mediocre placements.

---

## 14. Named product names from past engagements

**What failed:** Fiserv case study mentioned "Abiliti and DLO product teams" — both are Fiserv internal product names.

**Root cause:** When lifting details from a prior engagement deck, product names are often included naturally. They don't feel confidential in the source context, but in a new client's proposal they signal that Metis is careless with client details.

**Fix:** Scan past-engagement descriptions for product names, division names, internal code names, and buyer-side nicknames. Replace with generic terms ("priority product teams", "core business units").

**Lesson:** Every client detail should be one of: (a) aggregate numbers, (b) disguised to industry/size ("a $16B+ FinTech"), or (c) generic function ("product teams"). Never specific product names.

---

## 15. Image cropping that partially cut off content

**What failed:** Page 11 hub-and-spoke image had the original slide's subtitle partially visible at the top and the Metis logo partially visible at the bottom of the embedded image. Looked like cropping was done but incomplete.

**Root cause:** Crop region was set at (0, 120, 2000, 1075) — trimming the top 120pt (which covered title) and bottom 50pt. But the subtitle was at y=120–170 and the logo was at y=1020–1080. The crop missed both partially.

**Fix:** Open the cropped image, visually verify it's clean. Iterate on crop coordinates until the image shows ONLY the content you want, with no partial titles, subtitles, or footers.

```python
# Visually inspect the cropped image
img = Image.open('slide-10-cropped.png')
# Check top edge — should be clean content
# Check bottom edge — should be clean content
```

**Lesson:** Image cropping requires visual verification. Don't trust the coordinates alone.

---

## 16. Build declared done before visual verification

**What failed:** Multiple rounds of "the PDF is fixed" based on bbox overlap counts being zero. User would review and immediately find visual issues.

**Root cause:** Programmatic checks miss whole categories of issues. Declaring "zero overlaps" does not mean "visually correct".

**Fix:** The deployment gate requires BOTH:
1. Programmatic check passes (bbox, Y position, banned content)
2. Every content page rendered to PNG and visually reviewed

Neither alone is sufficient.

**Lesson:** Add visual verification to the definition of "done". Not doing so costs more time in the long run because issues surface during user review.

---

## 17. YAML key name collision

**What failed:** When adding a new "cross-client proof points" page between the existing Proof Points divider and the Ally case study, the YAML key was named `page_17_cross_client` while the Ally case remained `page_17_ally`. The parser happily loaded both since they were different keys, but the naming suggested a conflict.

**Root cause:** YAML keys include the page number, which is convenient for ordering but becomes confusing when pages are reordered.

**Fix:** Either use position-neutral keys (`ally_case_study`) or re-number all keys when reordering (bulk rename). Don't leave stale page numbers in keys.

**Lesson:** YAML key design matters for maintainability. Pick a convention and stick to it across restructuring.

---

## 18. Trying to fix shared drive file while user has it open

**What failed:** Multiple attempts to deploy the PDF to the shared drive returned "Device or resource busy" because the user had the PDF open in a viewer.

**Root cause:** Windows file locking prevents overwriting an open file.

**Fix:**
1. Build to `_working/` folder first (always succeeds)
2. Attempt copy to shared drive
3. If it fails, tell the user to close the viewer and retry, OR instruct them to copy manually

**Lesson:** Build and deploy should be separate steps. The build must succeed regardless of whether the shared drive is writable.

---

## Meta-Lesson

The single biggest cost across this engagement was **declaring work done before verifying it**. Every premature "it's fixed" was followed by user review catching the same class of issue. The cure is not more programmatic checks — it is the discipline of rendering to PNG and looking before saying the PDF is ready.

Second biggest cost: **switching tools prematurely**. HTML + Playwright was chosen first because it seemed sophisticated. It was the wrong tool. ReportLab was the right tool from the start, but the team had to learn that through failure. If the architecture decision had been made up front, multiple days would have been saved.

Third biggest cost: **not having a content file**. Until YAML was introduced, every copy change required editing Python strings, which was fragile and intimidated the user. Once YAML was in place, iterations became fast and low-risk.

The skill's first use on a new client should benefit from all three of these meta-lessons.
