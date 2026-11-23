# Metis Strategy: Reports & Documents Guide (Word / PDF)

Use this reference whenever creating a Word document or PDF report for Metis Strategy.

---

## Document Types

| Type | Typical Length | Primary Use |
|---|---|---|
| Executive Summary | 1–2 pages | Post-meeting recap, initial findings |
| Point of View (POV) | 2–4 pages | Thought leadership, client perspective |
| Proposal / SOW | 3–8 pages | New engagement scoping |
| Assessment Report | 5–15 pages | Findings, analysis, recommendations |
| One-Pager | 1 page | Intro materials, capability overview |

---

## Page Layout

- **Margins**: 1" top/bottom, 0.9" left/right
- **Header**: Metis Strategy logo (top-left) + document title (top-right, Gray, 9pt)
- **Footer**: "Driving change. Elevating leaders." (left, Metis Green, 9pt) + page number (right, Gray, 9pt)
- **Page size**: US Letter (8.5" × 11")

---

## Typography (Word / python-docx)

Use Calibri throughout (Open Sans requires separate font installation).

| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Document Title | Calibri | 24pt | Bold | Dark Blue `#20216f` |
| Section Header (H1) | Calibri | 16pt | Bold | Dark Blue `#20216f` |
| Subsection Header (H2) | Calibri | 13pt | Bold | Medium Blue `#256ba2` |
| Body Text | Calibri | 11pt | Regular | Black `#000000` |
| Caption / Label | Calibri | 9pt | Regular | Gray `#7b8692` |
| Call-out / Highlight | Calibri | 11pt | Bold | Metis Green `#3cdbc0` (on dark bg) or Dark Blue (on light bg) |

Line spacing: 1.15 for body text. Add 6pt space after paragraphs.

---

## Document Structure

### Cover Page
- Dark Blue background (`#20216f`)
- White document title, 28–32pt Bold
- Metis Green subtitle or engagement description, 16pt
- Client name and date, White, 12pt
- Trajectory Device image (right side, bleeding off edge)
- "Prepared by Metis Strategy" bottom-left, Gray

### Body Pages
- White background
- Dark Blue left border bar (0.15" wide) for section-starting pages
- Section headers in Dark Blue
- Key findings or callout boxes: light teal background (`#e8f8f5`) with Dark Blue left border

### Callout Box Pattern
Use for key insights, recommendations, or statistics:
```
┌─────────────────────────────────┐
│  ▌  Key Finding                 │  ← Dark Blue left bar, Metis Green label
│     Finding text here in body   │  ← Body text
└─────────────────────────────────┘
```

---

## Programmatic Implementation (python-docx)

### Color Constants
```python
METIS = {
    "dark_blue":    "20216F",
    "metis_green":  "3CDBC0",
    "medium_blue":  "256BA2",
    "gray":         "7B8692",
    "white":        "FFFFFF",
    "light_bg":     "E8F8F5",  # Tint for callout boxes
}
```

### Section Header Style
```python
from docx.shared import Pt, RGBColor
from docx.util import Inches

def add_section_header(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0x20, 0x21, 0x6F)  # Dark Blue
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
```

### Callout Box
```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_callout(doc, label, text):
    # Add shaded paragraph with left border
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    # Set shading
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), 'E8F8F5')
    pPr.append(shd)
    # Add label run
    label_run = p.add_run(label + "  ")
    label_run.bold = True
    label_run.font.color.rgb = RGBColor(0x20, 0x21, 0x6F)
    # Add body run
    body_run = p.add_run(text)
    body_run.font.size = Pt(11)
```

---

## Tone Reminders for Reports

- **Lead with insight**: Start sections with the conclusion, not the process.
- **Active voice**: "Metis recommends..." not "It is recommended that..."
- **Crisp headers**: Declarative ("AI Readiness Is Low in Three Critical Areas") not descriptive ("AI Readiness Assessment Results")
- **Avoid filler**: Cut "it is worth noting," "in order to," "at the end of the day"
- **Executive audience**: Write for a senior leader who has 90 seconds per page

---

## Common Mistakes to Avoid

- Using gray/generic color schemes instead of the Metis palette
- Long narrative paragraphs without visual breaks (use callouts, bullets, headers)
- Descriptive section headers instead of declarative/insight-led ones
- Missing BrandLine in the footer of client-facing documents
- Body text smaller than 10pt
- Inconsistent spacing between sections
