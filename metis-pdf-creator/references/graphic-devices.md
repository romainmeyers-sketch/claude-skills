# Metis Graphic Devices — Usage Guide

All graphic device files live at:
`G:/Shared drives/Knowledge Management/New Brand Assets/Graphic Devices/`

---

## The Most Important Rule

**All device PNGs have opaque white backgrounds.**

This means:
- ✅ They look great on white or light-colored page backgrounds
- ✅ They work well on `C.tealLight` (`#e8f8f5`) or `C.lightBg` (`#f4f6fa`) backgrounds
- ❌ They do NOT work on `C.darkBlue` or any dark background — placing them there
  produces a visible white rectangle around the device shape

For dark backgrounds, use the drawn trajectory fan (see pdfkit-helpers.md → Cover Page).

---

## Device Reference

### Single Arrow (`Metis SnglArrow Device RGB.png`)
A solid teal triangle pointing right. Clean and simple.

**Best uses:**
- Small accent (~13px wide) next to section eyebrow labels — draws the eye to section starts
- Inline bullet substitute in lists
- Small decorative marker in headers

**Placement:**
```javascript
// Next to eyebrow text (sectionHeader uses this pattern)
doc.image(GD + 'Metis SnglArrow Device RGB.png', x, y + 1, { width: 13 });
// Then offset eyebrow text to the right by ~17px
doc.fillColor(C.green).font('Helvetica-Bold').fontSize(7.5)
   .text('SECTION LABEL', x + 17, y, { characterSpacing: 1, lineBreak: false });
```

**Size guidance:** 12–16px wide for accents; up to 60px for standalone decorative use.

---

### Arrow Device Opaque (`Metis Arrow Device Opaque RGB.png`)
Multi-layered teal/blue/green arrow pointing right. The full Metis "direction of motion" motif.

**Best uses:**
- Large feature element on white-background pages
- Lower-right corner of content pages, partially cropped off edge (clip to page bounds)
- Hero element on white-background covers or section dividers

**Placement (large, lower-right):**
```javascript
doc.save();
doc.rect(0, 0, W, H).clip();   // clip prevents bleeding beyond page
doc.image(GD + 'Metis Arrow Device Opaque RGB.png', W * 0.3, H * 0.55, { width: 380 });
doc.restore();
```

**Note:** Because the white background blends into white pages, this works seamlessly —
the teal/blue stripes appear to float on the page.

---

### Trajectory Device (`Metis Trajectory Device RGB.png`)
Similar to Arrow Device but more elongated and slender. More energetic feeling.

**Best uses:** Same contexts as Arrow Device. Use Trajectory when you want a more dynamic,
forward-leaning feel; use Arrow when you want something more grounded and solid.

**Placement:** Same pattern as Arrow Device above.

---

### Nexus Device Opaque (`Metis Nexus Device Opaque RGB.png`)
Two mirrored arrow fans converging at a center point. Very wide, short aspect ratio.
Creates a "pinch point" or "convergence" visual metaphor — good for transitions.

**Best uses:**
- Horizontal section divider strip between major sections on a content page
- Full-width band as a visual break (render at content width, ~20–26px tall)

**Placement (section divider):**
```javascript
y += 6;
try {
  doc.image(GD + 'Metis Nexus Device Opaque RGB.png', ML + 10, y, { width: CW, height: 22 });
} catch(e) {}
y += 30;
```

**Size guidance:** Render at 22–28px tall to get a clean strip. Going taller starts to
look heavy. Render at full content width (CW = 508) for a balanced proportion.

---

### Energy Device (`Metis Energy Device RGB.png`)
A repeating grid of small arrow motifs. Very high visual density — best used sparingly.

**Best uses:**
- Subtle background texture in a panel or section (use at low opacity)
- Decorative band in a sidebar or pull-quote area

**Placement (background texture in a panel):**
```javascript
doc.save();
doc.opacity(0.08);
doc.image(GD + 'Metis Energy Device RGB.png', panelX, panelY, { width: panelW });
doc.restore();
```

**Warning:** At full opacity it overwhelms content. Keep opacity at 0.06–0.12 when used
as a background. Do not use on dark backgrounds.

---

## Drawn Trajectory Fan (dark backgrounds)

When you need the Metis directional device on a dark blue or colored background, draw it
using PDFKit path primitives. This version has been validated on the dark blue cover:

```javascript
// Tip of the fan (typically off the right edge)
const tipX = W + 30;
const tipY = H * 0.60;   // adjust to control where fan converges vertically

// Each layer: leftX (base), topY, bottomY, color, opacity
// Adjust opacities for subtle/bold variations
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
```

**Customization tips:**
- Move `tipY` up to push the fan higher on the page
- Increase `lx` values (e.g., `W * 0.2`) to push the fan base to the right (narrower spread)
- Increase opacity values for bolder, more dramatic effect
- Swap `C.medBlue` for `C.green` throughout for an all-green version

---

## Tasteful Usage Principles

- **Less is more.** One or two devices per document is ideal. The devices are bold by design;
  using all five in one PDF creates visual chaos.
- **Single Arrow accents** can appear multiple times (one per section header) without feeling heavy.
- **Nexus / Arrow / Trajectory** should appear once per document as a feature element.
- **Energy** should be a background detail at very low opacity, never a focal point.
- **Consistency:** If you use Arrow on page 2, don't switch to Trajectory on page 3 —
  pick one large device and use it consistently throughout the document.
