# Metis Strategy: Presentation Guide (PowerPoint)

Use this reference whenever creating or reviewing a PowerPoint presentation for Metis Strategy.

---

## Standard Slide Furniture (Required on Every Content Slide)

These elements appear on virtually every Metis content slide. Include them by default unless told otherwise.

### Confidentiality Footer
Bottom of every content slide:
> **"Proprietary & Confidential, Metis Strategy LLC [YEAR]"**
- Font: Calibri, 9pt, Gray (`#7b8692`), left-aligned
- Position: bottom-left, y ≈ 5.3" on a 16x9 slide

### Source Attribution
Most content slides include a source line:
> **"Source: Metis Strategy Research & Analysis"**
- Font: Calibri, 9pt, Gray, bottom of slide near the confidentiality footer
- Omit only on pure methodology or section divider slides

### Page Number
Every content slide has a page number (not the title or closing slide).
- Font: Calibri, 10pt, Gray, bottom-right or top-right corner

### Title Slide Header
When preparing a deck **for a client**, the title slide should include:
> **"Prepared for [Client Name] | [Month Year] | [Engagement Title]"**

### Slide Category Labels
Use small labels in the top-left area to categorize slide types:
- **"Client Example."** — for case study or reference slides
- **"Illustrative."** — for hypothetical or scenario-based content
These labels appear in a small, muted style (Gray or Medium Blue, 10–12pt)

---

## Slide Structure

### "Sandwich" Layout Pattern
The most common Metis deck structure uses a dark-light-dark sandwich:
- **Title slide**: Dark Blue (`#20216f`) background
- **Content slides**: Light (`#f4f6fa` or white) background
- **Section dividers / closing slide**: Dark Blue background

Committing fully to dark throughout (all slides dark) is also acceptable for a premium feel.

### Recommended Slide Count & Flow
1. **Title slide** — Client name, engagement title, date, "Prepared by Metis Strategy"
2. **Agenda / Table of Contents** — 3–5 items max
3. **Context / Challenge** — What the client is facing
4. **Approach / Framework** — How Metis addresses it
5. **Findings / Recommendations** — The insight-led core
6. **Next Steps** — Clear, numbered, owned actions
7. **Closing slide** — Dark background, BrandLine, contact info

---

## Slide Layout Patterns

Use varied layouts — don't repeat the same structure slide after slide.

### Two-Column Split
Text/insight on left, supporting visual or stat on right. Good for approach slides.

### Stat Callout Cards
3 cards in a row with a large number (52–60pt), label below, and supporting note. Anchor card backgrounds in White; use a thin Metis Green top border as the accent.

### Full-Width Content Row
For lists of 4–6 items: icon or number in a colored circle, bold header, 1–2 sentence description. Works well on light backgrounds.

### Dark Feature Slide
Dark Blue background, large quote or single insight in White/Metis Green, supporting detail below. Use for impact moments, key findings, or section headers.

### Timeline / Process Flow
Numbered steps with a horizontal connector line in Metis Green. Each step: bold label + 1-line description.

---

## Programmatic Implementation (pptxgenjs)

When writing PowerPoint code with pptxgenjs, follow these rules:

### Color Values — NEVER use `#` prefix
```javascript
// ✅ Correct
color: "20216f"
fill: { color: "3cdbc0" }

// ❌ Wrong — corrupts the file
color: "#20216f"
```

### Standard Color Constants
```javascript
const METIS = {
  darkBlue:    "20216f",  // Primary dark background
  metisGreen:  "3cdbc0",  // Primary brand accent
  mediumGreen: "53a092",
  darkGreen:   "007d66",
  lightBlue:   "00bdef",
  mediumBlue:  "256ba2",
  white:       "ffffff",
  gray:        "7b8692",
  lightBg:     "f4f6fa",  // Light slide background
};
```

### Font
Use `"Calibri"` as the font face in pptxgenjs (Open Sans requires manual installation; Calibri is the approved Microsoft fallback).

### Shadow Objects — Never Reuse
```javascript
// ✅ Correct — fresh object each time
const makeShadow = () => ({ type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.1 });
slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });

// ❌ Wrong — second call gets already-mutated values
const shadow = { ... };
slide.addShape(..., { shadow });
slide.addShape(..., { shadow }); // corrupted
```

### Accent Bars
Use thin left-edge or top-edge rectangles in Metis Green or Dark Blue to anchor cards and sections:
```javascript
// Left accent bar on a card
slide.addShape(pres.shapes.RECTANGLE, {
  x: cardX, y: cardY, w: 0.08, h: cardH,
  fill: { color: "3cdbc0" }, line: { color: "3cdbc0" }
});
```

---

## Using Graphic Devices in PowerPoint

All graphic device files are in the `assets/` folder of this skill. Reference them with:
```javascript
slide.addImage({ path: "<skill-assets-path>/trajectory_device.png", ... });
```

### Trajectory Device (`assets/trajectory_device.png`)
A fan of green/blue streaks pointing to the right — use on title or section slides.
- Position bleeding off the right edge for a dynamic feel
- On dark backgrounds at 45% transparency over a Dark Blue overlay
- Never point left or downward

```javascript
// Example: right-bleed on title slide
slide.addImage({
  path: "assets/trajectory_device.png",
  x: 4.5, y: 0.5, w: 6, h: 4.5,
  transparency: 15
});
```

### Energy Device (`assets/energy_device.png`)
Repeating arrow pattern — use as a background texture or to bookend an image.
- Always flows to the right
- Crop freely; works on both light and dark backgrounds
- Place at 20–40% transparency when used as wallpaper

```javascript
slide.addImage({
  path: "assets/energy_device.png",
  x: 0, y: 3.5, w: 10, h: 2.5,
  transparency: 65
});
```

### Nexus Device (`assets/nexus_device.png`)
Symmetric starburst expanding from center — represents the intersection of technology and business.
- Always horizontal orientation — never rotate
- Use on Dark Blue backgrounds only (or white/transparent)
- Place text in the darkest area for legibility

### Arrow Device (`assets/arrow_device.png`)
Solid Metis Green arrow — use to direct the eye to a headline or key insight.
- Points right or left only (never up/down at an angle)
- Scale to match the text it accompanies
- Use sparingly — one per slide maximum

---

## Slide Title Treatment

On **light slides**: Dark Blue title, 32–40pt, Bold, left-aligned. No decorative lines under the title.
On **dark slides**: White title or Metis Green title, same specs.

Do NOT put a line under slide titles — this is a common AI-generated slide mistake. Use whitespace instead.

---

## Common Mistakes to Avoid

- Using `#` prefix with hex colors in pptxgenjs (corrupts file)
- Reusing shadow objects across multiple shapes (corrupts second shape)
- Decorative lines under titles
- All slides the same layout (vary cards, columns, callouts)
- Centering body text (left-align paragraphs)
- Using light text on light backgrounds or dark text on dark backgrounds
- Placing the BrandLine as body text — it belongs near the logo or as a sign-off only
- Introducing any color outside the Metis palette
