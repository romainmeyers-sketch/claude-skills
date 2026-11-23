---
name: metis-pdf-creator
description: >
  Creates professional, on-brand PDF documents for Metis Strategy using
  PDFKit (Node.js). Use for consultant guides, setup documents, reference
  cards, one-pagers, methodology overviews, CDLC materials, and internal
  reports. Trigger on "create a PDF," "build a branded document," "generate
  a guide," "make a one-pager," or any short-form branded document request.
  Also trigger when fixing or regenerating an existing Metis PDF. Always
  validates against metis-brand-identity. Do NOT use for: client proposals
  or case studies (metis-premier-proposal); whitepapers or thought leadership
  (metis-whitepaper); PowerPoint decks (metis-pptx).
metadata:
  author: Metis Strategy
  version: 0.2.1
---

# Metis PDF Creator

This skill produces polished, on-brand PDFs for Metis Strategy using PDFKit (Node.js).
It encodes hard-won lessons about Y-position tracking, graphic device usage, and brand
application so that PDFs come out right the first time.

## Workflow

1. **Gather content** from user (text, structure, data, any source material).
2. **Select layout pattern** from `references/pdfkit-helpers.md` (cover page, section pages, callouts).
3. **Apply brand tokens** (colors, fonts, logo) per metis-brand-identity standards.
4. **Generate PDF** using PDFKit Node.js script with explicit Y-tracking.
5. **Verify output** against brand checklist and Y-tracking rules. Open the PDF and confirm no overlap, correct colors, and proper page breaks.

## Toolchain

- **Runtime**: Node.js (`C:\Program Files\nodejs\node.exe` on the user's machine)
- **Library**: `pdfkit` npm package
- **Working dir**: `C:\Users\[username]\AppData\Local\Temp\cdlc-pdf\` (already has pdfkit installed)
  - If that directory doesn't exist, create a new one: `mkdir C:\temp\metis-pdf && cd C:\temp\metis-pdf && npm init -y && npm install pdfkit`
- **Graphic devices**: `G:/Shared drives/Knowledge Management/New Brand Assets/Graphic Devices/`
- **Logos**: `G:/Shared drives/Knowledge Management/New Brand Assets/Metis Strategy Logo/`
- **Output**: Save directly to the path the user specifies, or to the Context as Code folder by default:
  `G:/Shared drives/Knowledge Management/Capability Development/AI Working Group/Context as Code/`

To run a script: `"C:\Program Files\nodejs\node.exe" <script-name>.js`

---

## Brand Constants

Copy these verbatim into every PDF script:

```javascript
const C = {
  darkBlue:  '#20216f',  // Primary — headings, bars, cover background
  green:     '#3cdbc0',  // Accent — eyebrows, bullets, BrandLine, badges
  medBlue:   '#256ba2',  // Secondary — callout bars, step badges
  gray:      '#7b8692',  // Body text supporting, page labels
  tealLight: '#e8f8f5',  // Callout box backgrounds
  white:     '#ffffff',
  black:     '#000000',
};

const W = 612, H = 792;   // US Letter in points
const ML = 52, MR = 52;   // Left / right margins
const CW = W - ML - MR;   // Content width: 508

// Logo paths — use Black-Mint on white/light pages, White on dark backgrounds (cover)
const LOGO      = 'G:/Shared drives/Knowledge Management/New Brand Assets/Metis Strategy Logo/';
const LOGO_BM   = LOGO + 'Metis Strategy Black-Mint RGB Logo.png';   // content pages
const LOGO_WHT  = LOGO + 'Metis Strategy White RGB logo.png';        // cover page
```

BrandLine (footer text, never italic, always exact): **"Driving change. Elevating leaders."**

---

## Critical Y-Tracking Rules

Text-overlap bugs — the most common failure mode — all come from Y-position errors.
Follow these rules and overlaps will not occur:

1. **Every `.text()` call must use explicit `x, y` coordinates.** Never let PDFKit flow from
   its internal cursor position without specifying where you want the text to start.

2. **Read `doc.y` immediately after every text render** to get the true bottom of that element,
   then add your gap: `y = doc.y + 12;`

3. **Pre-measure boxes before drawing them.** For any container (callout, panel, role card):
   call `doc.heightOfString(text, { width, lineGap })` BEFORE drawing the rectangle, compute
   `boxH`, draw the rectangle at `(x, y, w, boxH)`, then render text inside at absolute
   coordinates. Never guess heights.

4. **Return `y + boxH + padding` from helper functions** — a deterministic value — not
   `doc.y + padding` which can drift due to cursor state.

5. **Avoid two-column layouts with independent y-variables.** If you must have columns,
   pre-measure both columns, take the max height, draw both at fixed positions, then advance
   `y` by `maxH + gap`.

6. **Check remaining page space before every block.** Before rendering any element (step row,
   callout, role card, section header), estimate its height and check if it fits above the
   footer bar at `H - 30`. If it does not fit, call `doc.addPage()` + `pageFurniture()` and
   reset `y = 30`. Use the `needsNewPage` helper (see `references/pdfkit-helpers.md`) to make
   this automatic. **This is the most common cause of content overrunning the page** — all
   other Y-tracking rules are useless if content flows past the bottom margin.

---

## Graphic Devices

Read `references/graphic-devices.md` for full placement guidance.

**The most important rule:** All Metis graphic device PNGs have **opaque white backgrounds**.
They look great on white or light-colored pages. They do **not** work on the dark blue cover —
placing them there produces a white rectangle. For dark backgrounds, simulate the device
using PDFKit path primitives (the trajectory fan pattern — see `references/graphic-devices.md`).

Device file paths (use forward slashes — Node.js handles them on Windows):

| Device | File | Best use |
|---|---|---|
| Single Arrow | `Metis SnglArrow Device RGB.png` | Small accent next to section eyebrows |
| Arrow (Opaque) | `Metis Arrow Device Opaque RGB.png` | Large feature on white-bg pages |
| Trajectory | `Metis Trajectory Device RGB.png` | Large feature on white-bg pages |
| Nexus (Opaque) | `Metis Nexus Device Opaque RGB.png` | Horizontal section divider strip |
| Energy | `Metis Energy Device RGB.png` | Textured background band |

Embed with: `doc.image(GD + 'filename.png', x, y, { width: w })`
Clip to page: wrap in `doc.save(); doc.rect(0,0,W,H).clip(); doc.image(...); doc.restore();`

---

## Standard Helper Functions

Read `references/pdfkit-helpers.md` for complete, copy-paste-ready implementations of all
helpers. **Use these verbatim** — they encode correct Y-tracking and have been validated.

| Function | Purpose |
|---|---|
| `needsNewPage(y, needed, label)` | **Call before every block.** Adds page + furniture if `y + needed > H - 30`; returns y |
| `pageFurniture(label)` | Green top bar, dark blue left bar, footer bar with small White logo + white BrandLine |
| `sectionHeader(eyebrow, title, x, y)` | Eyebrow + SnglArrow accent + H1 title; returns new y |
| `stepBadge(n, x, y, color)` | Numbered circle for step sequences |
| `stepRow(n, heading, body, x, y, badgeColor)` | Full step row; returns new y |
| `callout(x, y, w, label, text, bgColor, barColor)` | Pre-measured callout box; returns new y |

---

## Page Layout Pattern

```javascript
// ── Page N ────────────────────────────────────────────────────────────────────
doc.addPage({ size: 'LETTER', margin: 0 });
pageFurniture('DOCUMENT TITLE — PAGE N OF M');

let y = 30;
y = sectionHeader('Section Eyebrow', 'Section Title', ML + 10, y);

doc.fillColor(C.gray).font('Helvetica').fontSize(9.5)
   .text('Intro sentence here.', ML + 10, y, { width: CW });
y = doc.y + 16;

// Before EVERY block, check if it fits. Use needsNewPage for this:
y = needsNewPage(y, 80, 'DOCUMENT TITLE — PAGE N OF M');
y = stepRow(1, 'Step Title', 'Step body text...', ML + 10, y);

y = needsNewPage(y, 60, 'DOCUMENT TITLE — PAGE N OF M');
y = callout(ML + 10, y, CW, 'Callout', 'Text here.', C.tealLight, C.green);
```

**The `needsNewPage` call before every block is not optional.** Omitting it is the
single most common cause of content overrunning the page footer.

---

## Cover Page Pattern

The cover uses a full dark-blue background with a drawn trajectory fan (not PNG devices).
Read `references/pdfkit-helpers.md` → "Cover Page" section for the complete template.

Key elements: `doc.rect(0,0,W,H).fill(C.darkBlue)` → trajectory fan → **White logo** (top-left) →
eyebrow → bold title → subtitle → green rule → "Who this is for" panel → bullet benefits → footer.

---

## Troubleshooting

- **Content overrunning the page** is the #1 formatting failure. Call `needsNewPage(y, height, label)`
  before every block — step rows, callouts, cards, images, section headers. If you skip the
  guard, the block will render over the footer bar or off the page entirely.
- **`fillOpacity` chaining is fragile.** Use `doc.save().opacity(a)...doc.restore()` for
  transparent fills instead of chaining `.fillOpacity(0.1).fill(C.white).fillOpacity(1)`.
- **`require('pdf-parse')` is broken** (returns object, not function). Do not attempt to
  read back PDFs in Node.js scripts. Use Claude's native Read tool to inspect generated PDFs.
- **Apostrophes in single-quoted JS strings** cause SyntaxError. Use double-quoted strings
  for any text containing apostrophes, or escape them: `'Metis\'s approach'`.
- **`heightOfString` must use the same font/fontSize** as the subsequent `.text()` call —
  set the font before measuring, not after.
