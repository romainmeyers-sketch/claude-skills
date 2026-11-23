# QA Process

Verification workflow for proposal PDFs. The core lesson from the Citi engagement: **programmatic checks alone are not sufficient; every meaningful page must be rendered and visually reviewed before declaring the PDF done.**

---

## The Two-Pass Verification Model

### Pass 1: Programmatic Checks (fast, catches mechanical issues)

- Page count matches plan
- File size is reasonable (5–15 MB)
- Page dimensions are 13.33" × 7.5" landscape
- No text bounding boxes overlap
- Bottom-most text on each content page is > 85% of page height (i.e., content fills the page)
- No em dashes in text
- No instances of specific banned words ("Zero", "Always") unless cleared

### Pass 2: Visual Verification (required, catches everything else)

For every meaningful page (not just the ones that changed), render to PNG at 1.5–2x zoom and actually look at it. Use the Read tool to view each PNG.

**What visual review catches that bbox analysis misses:**
- Duplicate titles from uncropped slide images
- Logos that are placed but effectively invisible due to size or contrast
- Partially cropped images bleeding off page edges
- Graphic device opacity that is too low or too high
- Text overflowing a container (if the overflow happens inside the same text box bbox)
- Whitespace that is technically not "empty" (contains a transparent device) but feels wrong
- Alignment issues between adjacent cards or columns

**Do not skip this pass.** The Citi engagement repeatedly declared success based on bbox checks, then had user feedback flag exactly the issues that visual review would have caught.

---

## Programmatic Check Script

See `scripts/verify.py`. Usage:

```bash
# Overlap + Y-position check across all pages
python scripts/verify.py --pdf output.pdf --mode overlaps

# Render all pages to PNG for visual review
python scripts/verify.py --pdf output.pdf --mode render --out verify/

# Check for banned content (em dashes, absolutes)
python scripts/verify.py --pdf output.pdf --mode content
```

### Overlap detection logic

```python
import fitz

def rects_overlap(r1, r2, threshold=3):
    x_overlap = min(r1[2], r2[2]) - max(r1[0], r2[0])
    y_overlap = min(r1[3], r2[3]) - max(r1[1], r2[1])
    return x_overlap > threshold and y_overlap > threshold

doc = fitz.open(pdf_path)
for i, page in enumerate(doc):
    spans = []
    for b in page.get_text('dict')['blocks']:
        if 'lines' in b:
            for line in b['lines']:
                for span in line['spans']:
                    t = span['text'].strip()
                    if 'Page ' in t and 'Citi' in t: continue
                    if 'Proprietary' in t: continue
                    if len(t) < 2: continue
                    spans.append((span['bbox'], t))
    overlaps = 0
    for j, (b1, t1) in enumerate(spans):
        for k, (b2, t2) in enumerate(spans):
            if j >= k: continue
            if t1.strip() == t2.strip(): continue
            if rects_overlap(b1, b2):
                overlaps += 1
    if overlaps:
        print(f'Page {i+1}: {overlaps} overlaps')
```

**Threshold tuning:** threshold=3 (points) is right for proposals. Below that you get false positives from glyph descenders touching the next line's ascenders. Above that you miss small but real overlaps.

**Common false positive:** Metric cards where the big number (24pt font) has a bbox that extends slightly into the small label's ascender region. This is solved by making the card at least 56pt tall, not 48pt.

### Y-position check

For each content page (not dividers, not cover), find the bottom-most text line. It should be at y > 460pt (85% of the 540pt page height). If lower, there is likely excess whitespace.

```python
for i, page in enumerate(doc):
    max_y = 0
    for b in page.get_text('dict')['blocks']:
        if 'lines' in b:
            for line in b['lines']:
                for span in line['spans']:
                    y = span['origin'][1]
                    if y > max_y:
                        max_y = y
    pct = max_y / 540 * 100
    print(f'Page {i+1}: bottom text at {max_y:.0f}pt ({pct:.0f}%)')
```

**Caveat:** this check doesn't work for image-dominant pages because the bbox is only for text, not the image. For those pages, visual review is the only option.

### Banned content check

```python
banned = {
    'em_dash': ['—', '\u2014'],
    'absolutes': ['Zero', 'Never', 'Always', 'Every'],
    'ai_tells': ['leverage', 'utilize', 'impactful', 'synergies'],
}
for i, page in enumerate(doc):
    text = page.get_text()
    for category, words in banned.items():
        for w in words:
            if w in text:
                print(f'Page {i+1}: banned "{w}" ({category})')
```

Review hits manually — some may be legitimate (e.g., a word from a verbatim client quote).

---

## Visual Verification Workflow

### Step 1: Render all content pages

```python
import fitz
doc = fitz.open(pdf_path)
for i in range(len(doc)):
    pix = doc[i].get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    pix.save(f'verify/page-{i+1:02d}.png')
```

### Step 2: Use the Read tool to view each PNG

In Claude Code, the Read tool displays PNGs inline. Walk through each page and assess:

**Cover page checklist:**
- [ ] Metis logo visible at top-left (white-mint)
- [ ] Gradient fills the whole page
- [ ] Trajectory device visible at right edge, appropriate opacity
- [ ] Title is 2 lines, not awkwardly wrapped
- [ ] "Prepared for" line is correct name and date

**Section divider checklist:**
- [ ] Logo visible at top-left
- [ ] Green accent bar is ABOVE the title text (not crossing it)
- [ ] Title color contrast readable
- [ ] Subtitle fits without overflow
- [ ] Device visible but not overpowering

**Content page checklist:**
- [ ] Logo visible at top-right (black-mint for light pages)
- [ ] Eyebrow has the small arrow device to its left
- [ ] Title fits within 1–2 lines
- [ ] Subtitle if present is readable and legible
- [ ] All bullet items fit within columns, no wraps into adjacent column
- [ ] Callouts sit at the bottom with appropriate spacing above
- [ ] Footer reads "Page N | [Client] Proposal" in the correct location
- [ ] No content cropped off page edges

**Image page checklist:**
- [ ] Embedded image has NO duplicate title (original slide title was cropped)
- [ ] Image is sized to fill available vertical space
- [ ] Any annotation callout at the bottom is readable
- [ ] Image is not distorted or stretched
- [ ] Source label (Metis Strategy Research & Analysis) is visible if appropriate

**Proof point (case study) checklist:**
- [ ] Photo has dark overlay making text on it readable
- [ ] Big number on photo is accurate and attention-grabbing
- [ ] Numbered phase items don't overflow into metric cards area
- [ ] Metric cards all fit their numbers (auto-scale working)
- [ ] Relevance callout at bottom explains tie to prospect

**Closing page checklist:**
- [ ] Logo visible at top-left
- [ ] Name, role, email all correct and spelled right
- [ ] Brand line present (mint, bottom-left)
- [ ] Copyright year is current
- [ ] Trajectory device visible but low opacity

---

## Named People Check

Before every deployment, verify the spelling of every named person referenced in the proposal:

1. Buyer's name (on cover, in body)
2. Buyer's colleagues (in body, in callouts)
3. Proposer's name (closing page)
4. Any mentioned stakeholders (procurement, etc.)

Cross-reference against:
- The calendar invite for the discovery call
- The buyer's email domain / signature
- LinkedIn if available

This is a 2-minute check that prevents a "Neil Ciderman / Neil Seideman"-level credibility hit.

---

## Deployment Gate

The PDF is ready for deployment when:

- [ ] All programmatic checks pass (zero overlaps, all content pages > 85% fill)
- [ ] All pages have been visually reviewed
- [ ] All named people verified
- [ ] Content rules checklist complete (see `content-rules.md`)
- [ ] Working files are in `_working/`, NOT on shared drive
- [ ] Final PDF filename follows convention: `<Client> <Context> - Metis Strategy <YYYY-MM-DD>.pdf`
- [ ] Final PDF is copied to `G:\Shared drives\BizDev Collaboration\<Client>\<Year>\`

When the user reviews the shared drive copy, if they surface any issue, the debug loop should be:

1. Re-render the problem page to PNG
2. View it with the Read tool
3. Diagnose the specific issue
4. Make the specific fix (ideally in YAML for copy, or in the build script for layout)
5. Rebuild, re-verify, redeploy

---

## Build Reproducibility Test

Before declaring the skill stable for a new client, run a build-reproducibility test:

1. Build the PDF
2. Note the file size and page count
3. Build again (no code changes)
4. Confirm identical file size, page count, and output

If builds are not reproducible, there is a non-determinism bug. Common sources:
- Image loading order (PIL vs ReportLab caching)
- Font fallback randomness
- Embedded time stamps in PDF metadata

These matter when the user wants to diff before/after builds to see what changed. Reproducible builds make tiny edits trackable.
