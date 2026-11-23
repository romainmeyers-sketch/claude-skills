# PDFKit Helper Functions — Metis PDF Creator

Validated, copy-paste-ready implementations. These encode correct Y-tracking and have
been tested against real Metis PDF outputs. Copy them verbatim into new scripts.

---

## Document Initialization

```javascript
const PDFDocument = require('pdfkit');
const fs          = require('fs');

const GD  = 'G:/Shared drives/Knowledge Management/New Brand Assets/Graphic Devices/';
const LOGO      = 'G:/Shared drives/Knowledge Management/New Brand Assets/Metis Strategy Logo/';
const LOGO_BM   = LOGO + 'Metis Strategy Black-Mint RGB Logo.png';   // content pages (white bg)
const LOGO_WHT  = LOGO + 'Metis Strategy White RGB logo.png';        // cover page (dark bg)
const OUT = 'G:/path/to/Output_Filename.pdf';  // set per document

const doc = new PDFDocument({ size: 'LETTER', margin: 0, info: {
  Title:  'Document Title Here',
  Author: 'Metis Strategy',
}});
doc.pipe(fs.createWriteStream(OUT));

// ... define helpers ... build pages ... then:
doc.end();
console.log('Done:', OUT);
```

---

## needsNewPage

**Call this before every block** (step row, callout, section header, role card, image, etc.).
Checks whether the next element fits on the current page. If not, adds a new page with
standard furniture and resets y. This is the primary defense against content overrunning
the page footer.

```javascript
const FOOTER_Y = H - 30;  // top of the dark blue footer bar

function needsNewPage(y, neededHeight, pageLabel) {
  if (y + neededHeight > FOOTER_Y) {
    doc.addPage({ size: 'LETTER', margin: 0 });
    pageFurniture(pageLabel);
    return 30;  // reset y to top of content area
  }
  return y;
}
```

**Usage — before every block, not just "large" ones:**
```javascript
y = needsNewPage(y, 80, 'GUIDE — PAGE 2 OF 3');   // 80pt estimate for a step row
y = stepRow(1, 'Title', 'Body text...', ML + 10, y);

y = needsNewPage(y, 100, 'GUIDE — PAGE 2 OF 3');  // 100pt estimate for a callout
y = callout(ML + 10, y, CW, 'Label', 'Text...', C.tealLight, C.green);
```

**How to estimate `neededHeight`:**
- Step row: ~70–90pt (depends on body length)
- Callout: use `doc.heightOfString()` + 58 (padding + label)
- Section header: ~45pt
- Role card: use `doc.heightOfString()` + 20
- When in doubt, overestimate — an early page break is always better than overrun

---

## pageFurniture

Draws the standard chrome on every non-cover page: green top bar, dark blue left bar,
footer bar with small White logo (bottom-left) and white BrandLine text. Call immediately after `doc.addPage()`.

```javascript
function pageFurniture(label) {
  doc.rect(0, 0, W, 6).fill(C.green);              // green top bar
  doc.rect(0, 6, 4, H - 36).fill(C.darkBlue);      // dark blue left bar
  doc.rect(0, H - 30, W, 30).fill(C.darkBlue);     // footer bar

  // Metis Strategy logo — small White variant in the far bottom-left of the dark blue footer.
  // 55pt wide (~16pt tall at ~3.5:1 aspect), vertically centered in the 30pt footer.
  // Placed at x=10 (flush left within the footer) to leave clear space before BrandLine text.
  try {
    doc.image(LOGO_WHT, 10, H - 26, { width: 55 });
  } catch(e) {}

  // BrandLine — white text on dark blue footer, spaced well right of the logo. Never italic.
  doc.fillColor(C.white).font('Helvetica').fontSize(7)
     .text('Driving change. Elevating leaders.', 78, H - 18, { lineBreak: false });

  doc.fillColor(C.white).font('Helvetica').fontSize(7)
     .text('METIS STRATEGY  |  INTERNAL', W - MR - 150, H - 18,
           { width: 150, align: 'right', lineBreak: false });

  if (label) {
    doc.fillColor(C.gray).font('Helvetica').fontSize(8)
       .text(label, W - MR - 200, 14, { width: 200, align: 'right', lineBreak: false });
  }
}
```

---

## stepBadge

Draws a numbered circle for step sequences.

```javascript
function stepBadge(n, x, y, color) {
  doc.circle(x + 10, y + 10, 10).fill(color || C.darkBlue);
  // y + 7 vertically centers 9pt cap-height digits inside the r=10 circle
  doc.fillColor(C.white).font('Helvetica-Bold').fontSize(9)
     .text(String(n), x + 1, y + 7, { width: 20, align: 'center', lineBreak: false });
}
```

---

## stepRow

Renders a numbered step (badge + heading + body). Returns y after the row + gap.

Y-tracking note: heading is placed at the explicit start `y`; body is placed at
`doc.y + 3` after heading renders; return value is `doc.y + 14` after body renders.
This is deterministic because both text calls use explicit coordinates.

```javascript
function stepRow(n, heading, body, x, y, badgeColor) {
  const indentX = x + 28;
  const textW   = W - indentX - MR;

  stepBadge(n, x, y, badgeColor || C.darkBlue);

  doc.fillColor(C.darkBlue).font('Helvetica-Bold').fontSize(10.5)
     .text(heading, indentX, y, { width: textW });

  doc.fillColor(C.black).font('Helvetica').fontSize(9.5)
     .text(body, indentX, doc.y + 3, { width: textW, lineGap: 2 });

  return doc.y + 14;
}
```

---

## callout

Draws a callout box with a colored left bar. Pre-measures text height so the box is
exactly the right size. Returns deterministic `y + boxH + 14` (not `doc.y`).

```javascript
function callout(x, y, w, label, text, bgColor, barColor) {
  const bColor = barColor || C.darkBlue;
  const bg     = bgColor  || C.tealLight;

  // MUST set font before measuring — heightOfString uses current font state
  doc.font('Helvetica').fontSize(9.5);
  const textH = doc.heightOfString(text, { width: w - 26, lineGap: 2 });
  const boxH  = 14 + 16 + textH + 14;   // top-pad + label-row + text + bottom-pad

  doc.roundedRect(x, y, w, boxH, 4).fill(bg);
  doc.rect(x, y, 4, boxH).fill(bColor);

  doc.fillColor(bColor).font('Helvetica-Bold').fontSize(7.5)
     .text(label.toUpperCase(), x + 14, y + 14,
           { width: w - 20, characterSpacing: 0.5, lineBreak: false });

  doc.fillColor(C.black).font('Helvetica').fontSize(9.5)
     .text(text, x + 14, y + 30, { width: w - 26, lineGap: 2 });

  return y + boxH + 14;
}
```

---

## sectionHeader

Renders an eyebrow label + SnglArrow accent + large section title. Returns new y.

```javascript
function sectionHeader(eyebrow, title, x, y) {
  // Small single arrow accent — safe to wrap in try/catch in case file is missing
  // Arrow PNG is 859×512 (aspect 1.68) — at width:13 it renders 7.74px tall.
  // y - 1 vertically centers it with the 7.5pt eyebrow text (cap center ≈ y + 2.7).
  try {
    doc.image(GD + 'Metis SnglArrow Device RGB.png', x, y - 1, { width: 13 });
  } catch(e) {}

  doc.fillColor(C.green).font('Helvetica-Bold').fontSize(7.5)
     .text(eyebrow.toUpperCase(), x + 17, y, { characterSpacing: 1, lineBreak: false });

  doc.fillColor(C.darkBlue).font('Helvetica-Bold').fontSize(16)
     .text(title, x, y + 16, { width: CW });

  return doc.y + 10;
}
```

---

## Cover Page Template

The cover uses a dark blue full-bleed background. Graphic device PNGs have opaque white
backgrounds and cannot be used here — instead, draw a trajectory fan using PDFKit paths.
The fan echoes the Metis Arrow/Trajectory device family on any background color.

```javascript
// ── PAGE 1: COVER ─────────────────────────────────────────────────────────────
doc.rect(0, 0, W, H).fill(C.darkBlue);
doc.rect(0, 0, W, 6).fill(C.green);   // green top bar

// Trajectory fan — layered translucent triangles pointing right
// Adjust tipY and layer opacities to taste
const tipX = W + 30;
const tipY = H * 0.60;
[
  { lx: 0, ty: H*0.27, by: H*1.03, c: C.green,   a: 0.07 },
  { lx: 0, ty: H*0.34, by: H*0.97, c: C.green,   a: 0.11 },
  { lx: 0, ty: H*0.40, by: H*0.92, c: C.medBlue, a: 0.19 },
  { lx: 0, ty: H*0.45, by: H*0.88, c: C.medBlue, a: 0.14 },
  { lx: 0, ty: H*0.49, by: H*0.85, c: C.green,   a: 0.12 },
  { lx: 0, ty: H*0.52, by: H*0.82, c: C.white,   a: 0.05 },
].forEach(({ lx, ty, by, c, a }) => {
  doc.save()
     .opacity(a)
     .moveTo(lx, ty).lineTo(tipX, tipY).lineTo(lx, by)
     .closePath().fill(c)
     .restore();
});

// Metis Strategy logo — White variant for the dark blue cover background
// Placed top-left, same position as content pages but using the white-on-dark version.
// Falls back to text if the logo file is missing.
try {
  doc.image(LOGO_WHT, ML + 6, 16, { width: 90 });
} catch(e) {
  doc.fillColor(C.white).font('Helvetica').fontSize(9)
     .text('METIS STRATEGY', ML + 6, 22, { characterSpacing: 2, lineBreak: false });
}

// Eyebrow (green, above title)
doc.fillColor(C.green).font('Helvetica').fontSize(11)
   .text('AI Enablement  |  Consultant Onboarding', ML + 6, H * 0.27);
   // Replace with appropriate category for your document

// Title — two lines, adjust fractional Y positions so title sits in upper half
doc.fillColor(C.white).font('Helvetica-Bold').fontSize(32)
   .text('Document Title Line One', ML + 6, H * 0.33);
doc.fillColor(C.white).font('Helvetica-Bold').fontSize(32)
   .text('Line Two if Needed', ML + 6, doc.y + 2);

// Subtitle
doc.fillColor(C.white).font('Helvetica').fontSize(12)
   .text('Subtitle or description of this document', ML + 6, doc.y + 10);

// Green divider rule
const ruleY = doc.y + 16;
doc.moveTo(ML + 6, ruleY).lineTo(ML + 180, ruleY)
   .strokeColor(C.green).lineWidth(1.5).stroke();

// "Who this is for" / context panel (semi-transparent white on dark blue)
const panelY    = ruleY + 14;
const panelText = 'Description of audience or context for this document.';
doc.font('Helvetica').fontSize(9.5);
const panelTextH = doc.heightOfString(panelText, { width: CW - 22, lineGap: 3 });
const panelH     = 14 + 16 + panelTextH + 14;

doc.save().opacity(0.14)
   .roundedRect(ML + 6, panelY, CW, panelH, 5).fill(C.white)
   .restore();
doc.rect(ML + 6, panelY, 4, panelH).fill(C.green);
doc.fillColor(C.green).font('Helvetica-Bold').fontSize(8.5)
   .text('WHO THIS IS FOR', ML + 18, panelY + 14, { characterSpacing: 0.8, lineBreak: false });
doc.fillColor(C.white).font('Helvetica').fontSize(9.5)
   .text(panelText, ML + 18, panelY + 30, { width: CW - 22, lineGap: 3 });

// Bullet list of benefits / takeaways
const bullY = panelY + panelH + 18;
doc.fillColor(C.green).font('Helvetica-Bold').fontSize(10)
   .text('After reading this document:', ML + 6, bullY);
let by = doc.y + 7;
['Benefit or takeaway one', 'Benefit or takeaway two', 'Benefit or takeaway three']
  .forEach(b => {
    doc.circle(ML + 14, by + 5, 2.5).fill(C.green);
    doc.fillColor(C.white).font('Helvetica').fontSize(9.5)
       .text(b, ML + 24, by, { width: CW - 20, lineGap: 2 });
    by = doc.y + 5;
  });

// Cover footer
doc.rect(0, H - 30, W, 30).fill(C.darkBlue);
doc.fillColor(C.green).font('Helvetica').fontSize(7)
   .text('Driving change. Elevating leaders.', ML + 6, H - 18, { lineBreak: false });
doc.fillColor(C.white).font('Helvetica').fontSize(7)
   .text('METIS STRATEGY  |  INTERNAL', W - MR - 150, H - 18,
         { width: 150, align: 'right', lineBreak: false });
```

---

## Nexus Divider Strip

Use between major sections on content pages (white background only):

```javascript
// Nexus device as full-width section divider
y += 6;
try {
  doc.image(GD + 'Metis Nexus Device Opaque RGB.png', ML + 10, y, { width: CW, height: 22 });
} catch(e) {}
y += 30;
```

---

## Role / Feature Card (left bar + label + description)

For multi-item breakdowns with color-coded left bars:

```javascript
const items = [
  { label: 'Role / Item One', desc: 'Description text here.', color: C.green   },
  { label: 'Role / Item Two', desc: 'Description text here.', color: C.medBlue },
  { label: 'Role / Item Three', desc: 'Description text here.', color: C.darkBlue },
];

items.forEach(item => {
  // Pre-measure before drawing
  doc.font('Helvetica').fontSize(9.5);
  const descH = doc.heightOfString(item.desc, { width: CW - 20, lineGap: 2 });
  const itemH = 16 + descH + 2;

  doc.rect(ML + 10, y, 4, itemH).fill(item.color);
  doc.fillColor(item.color).font('Helvetica-Bold').fontSize(9.5)
     .text(item.label, ML + 20, y, { lineBreak: false });
  doc.fillColor(C.black).font('Helvetica').fontSize(9.5)
     .text(item.desc, ML + 20, y + 16, { width: CW - 20, lineGap: 2 });
  y = doc.y + 10;
});
```

---

## Final Dark Callout (optional bottom-of-page closer)

```javascript
if (y + 72 < H - 30) {
  doc.font('Helvetica').fontSize(9);
  const ft  = 'Closing insight or memorable statement here.';
  const ftH = doc.heightOfString(ft, { width: CW - 28, lineGap: 2 });
  const fbH = 14 + 18 + ftH + 14;

  doc.roundedRect(ML + 10, y, CW, fbH, 5).fill(C.darkBlue);
  doc.fillColor(C.green).font('Helvetica-Bold').fontSize(9.5)
     .text('Bold lead-in statement.', ML + 22, y + 14, { width: CW - 24 });
  doc.fillColor(C.white).font('Helvetica').fontSize(9)
     .text(ft, ML + 22, y + 32, { width: CW - 28, lineGap: 2 });
}
```
