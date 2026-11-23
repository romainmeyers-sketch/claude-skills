---
name: metis-brand-identity
description: >
  Metis Strategy brand identity reference and compliance layer. Automatically
  consulted by metis-pptx, metis-html-slides, metis-pdf-creator,
  metis-whitepaper, and metis-premier-proposal during output generation.
  Also use standalone when the user asks about "Metis colors," "our brand,"
  "on-brand," "Metis template," "client-facing" standards, or wants a brand
  compliance review of existing output. Covers color palette, typography,
  logo usage, graphic devices, photography treatment, and editorial voice.
  Do NOT use for creating documents or deliverables directly; use the
  appropriate output skill (metis-pptx, metis-pdf-creator, etc.) instead.
  When in doubt, apply the brand.
metadata:
  author: Metis Strategy
  version: 0.2.3
---

# Metis Strategy Brand Identity

Metis Strategy is a strategy and management consulting firm that propels leaders' companies and careers forward. The brand conveys focused trajectory, visionary direction, and dynamic momentum — every output should feel **confident, clean, forward-moving, and professional**.

**BrandLine:** "Driving change. Elevating leaders."

---

## Output-Type Quick Guide

Before diving into the full brand specs, read the right reference for your output type:

| Output | Read This |
|---|---|
| PowerPoint / PPTX deck | `references/presentations.md` — layout patterns, pptxgenjs code, graphic device placement |
| Word doc / PDF report | `references/reports.md` — document structure, python-docx code, page layout |
| Email / short copy | Use the Tone & Voice section below; no separate reference needed |

Both reference files include **ready-to-use code constants** for the full color palette.

---

## Color Palette

These are the exact values to use whenever applying color programmatically.

> ⚠️ In pptxgenjs, **never use the `#` prefix** — it corrupts the file. Use bare hex strings: `"20216f"` not `"#20216f"`.

### Primary Brand Anchors
| Name | HEX | RGB | Notes |
|---|---|---|---|
| **Metis Green** | `#3cdbc0` | 60, 219, 192 | Primary accent, headers, highlight elements |
| **Dark Blue** | `#20216f` | 32, 33, 111 | Primary dark background, headings on light slides |

### Sequence Greens
| Name | HEX | RGB | Pantone | CMYK |
|---|---|---|---|---|
| Metis Green | `#3cdbc0` | 60, 219, 192 | 333C | 54-0-34-0 |
| Medium Green | `#53a092` | 83, 160, 146 | 2241C | 65-8-42-6 |
| Dark Green | `#007d66` | 0, 125, 102 | 6157C | 69-13-58-19 |

### Sequence Blues
| Name | HEX | RGB | Pantone | CMYK |
|---|---|---|---|---|
| Light Blue | `#00bdef` | 0, 189, 239 | 298C | 65-3-0-0 |
| Medium Blue | `#256ba2` | 37, 107, 162 | 2151C | 85-48-1-7 |
| Dark Blue | `#20216f` | 32, 33, 111 | 273C | 98-97-0-37 |

### Neutrals
| Name | HEX | RGB |
|---|---|---|
| White | `#ffffff` | 255, 255, 255 |
| Light Background | `#f4f6fa` | 244, 246, 250 — use for light slide/page backgrounds |
| Gray | `#7b8692` | 123, 134, 146 |
| Black | `#000000` | 0, 0, 0 |

### Color Usage Principles
- **Metis Green and Dark Blue are the two anchors** — one or both should appear on every page/slide.
- Supporting colors (Medium Green, Light Blue, Medium Blue) are accent and secondary elements.
- Tints (opacity reductions) of any brand color are permitted for backgrounds and supporting shapes.
- Do not introduce colors outside this palette.
- When using light colors (Metis Green, Light Blue) for text, use SemiBold or Bold weight to maintain readability.

---

## Typography

### Primary Font: Open Sans *(all brand materials)*
Download: https://fonts.google.com/specimen/Open+Sans

| Role | Weight | Notes |
|---|---|---|
| Headlines & Titles | Light or SemiBold | Light for shorter, larger headlines |
| Secondary Headlines | Light | ~3pt smaller than primary headline |
| Subheads | Light, SemiBold, or Bold | ~3pt smaller than secondary headline |
| Body Copy (≥9pt) | Light | Line spacing 10/13pt — never tight |
| Body Copy (<9pt) | Regular | |

**Key rules:**
- Max three type sizes per layout — use scale and weight for hierarchy, not variety.
- Italics only in body copy, sparingly — never in headlines or subheads.
- The brand voice is balanced and understated; let scale and weight do the work.

### Microsoft Applications Fallback: Calibri
When Open Sans is unavailable (Word, PowerPoint, pptxgenjs), use Calibri with the same hierarchy logic. Body copy at 10–11pt / 13pt line spacing.

---

## The BrandLine

**"Driving change. Elevating leaders."**

Include on most client-facing materials. Acceptable placements:
- **Near the logo** — Open Sans Regular or Light
- **As a headline** — Open Sans Regular or SemiBold, large display size
- **As a sign-off** — Open Sans SemiBold, end of body copy
- **Separated by an image** — "Driving change." left / "Elevating leaders." right
- **Stacked** (space-constrained only) — two lines, as headline or sign-off

**Do not:** render in italics, non-brand color, with drop shadows or effects, or locked up as part of the logo.

---

## Graphic Devices

Metis Strategy has four proprietary graphic devices. The image files are in this skill's `assets/` folder. Their colors must never be altered.

### Trajectory Device
**File:** `assets/trajectory_device.png` (also `assets/trajectory_device_large.jpg`)
A fan of green/blue streaks converging to a right-pointing tip — represents thrust and forward direction.
- Use on title and section slides, bleeding off the right edge for dynamism
- On dark backgrounds: place at 45% transparency over a Dark Blue overlay
- Always points upward or forward — **never downward or to the left**
- Can be cropped on any edge; the tip may bleed off the page

### Energy Device
**File:** `assets/energy_device.png`
Repeating arrow pattern — conveys dynamic, collaborative energy. Use as a background texture or to bookend images.
- Always flows to the right
- Both devices must face the same direction when bookending
- Works on light and dark backgrounds; use at 20–65% transparency as wallpaper

### Nexus Device
**File:** `assets/nexus_device.png` (opaque) / `assets/nexus_device_transparent.png`
Symmetric starburst expanding from center — represents the intersection of technology and business.
- Always horizontal — **never rotate or angle**
- Background must be white/transparent or Dark Blue only
- Place messaging in the darkest areas for legibility

### Arrow Device
**File:** `assets/arrow_device.png` / `assets/arrow_device_single.png`
A solid Metis Green arrow used to direct the viewer's eye to content.
- Points right or left only — **never up, down, or at an angle**
- Scale to match the text it accompanies
- Use sparingly — one per slide/page maximum
- Do not recolor

---

## Logo

The Metis Strategy logo: wordmark "METIS STRATEGY" + reflective "M" icon (one side Metis Green).

**Primary colorway:** Black wordmark + Metis Green M on white background.

**Approved alternates:**
- White wordmark + Metis Green M on Dark Blue / Dark Green / Black
- White wordmark + White M on Metis Green or Gray
- White wordmark + White M over photography (highest-contrast area)

**Rules:** Min 54px (digital) / 0.75" (print). Clear space = ½ the M height on all sides. Never invert, rotate, add effects, or alter proportions.

---

## Iconography

- Source from Microsoft Office's built-in icon library for consistent style
- **Filled/solid only** — never outlined versions
- Single brand color per icon (no multicolor)
- Use purposefully — icons reinforce content, not decoration
- Sparingly — too many dilutes impact

---

## Photography

### Inspiring Leaders Photography
Portraits or collaboration shots conveying confidence and growth.
- **Rich, full-color**: saturated, vivid; increase brightness if too dark
- **Black & white**: high contrast, background as white as possible (used with Nexus device)

### Storytelling Imagery
Conceptual/abstract images (landscapes, motion). Always carry a color tint overlay:
- **Blue tint**: 60% opacity Light Blue (`#00bdef`) in Multiply blending mode
- **Green tint**: 80% opacity Metis Green (`#3cdbc0`) in Multiply blending mode

---

## Tone and Voice

Metis Strategy's voice should feel:
- **Confident and direct** — speak from expertise, not hedging
- **Forward-looking** — orient toward possibility, progress, and impact
- **Substantive** — grounded in insight, not buzzwords; say something real
- **Elevated but accessible** — senior executive audience; clear, precise, no jargon for its own sake

**In practice:**
- Lead with the insight or recommendation, not the process
- Use active voice
- Avoid filler: "it is worth noting that," "in order to," "at the end of the day"
- Headers should be declarative or evocative, not just labels
- The BrandLine captures the spirit: crisp, paired, punchy

**Punctuation:**
- **Never use em dashes (—) in any generated copy.** Rewrite the sentence, or use a comma, colon, parentheses, or a period instead. This applies to all deliverables: slides, PDFs, whitepapers, proposals, documents, and email.
- Do not substitute an en dash (–) or a double hyphen (--) as a stand-in for an em dash either. Use standard sentence punctuation.

---

## Quick Reference Checklist

Before finalizing any Metis output:

- [ ] Colors come only from the Metis palette (exact HEX values above)
- [ ] Metis Green (`#3cdbc0`) **or** Dark Blue (`#20216f`) anchors the primary accent or header
- [ ] Font is Open Sans (or Calibri in Microsoft/programmatic apps), with proper hierarchy
- [ ] Body copy has adequate line spacing (10/13pt equivalent)
- [ ] BrandLine present on client-facing or public-facing pieces
- [ ] Tone is confident, forward-looking, and substantive; leads with insight
- [ ] No em dashes (—) anywhere in the copy; use commas, colons, parentheses, or periods instead
- [ ] No unapproved colors, fonts, or design effects
- [ ] Icons (if used): filled, single-color, brand-colored
- [ ] Photography (if used): Inspiring Leaders or Storytelling Imagery treatment
- [ ] Graphic devices (if used): correct file from `assets/`, correct orientation, colors unaltered
- [ ] No decorative lines under titles (use whitespace instead)
- [ ] Every content slide has a page number
- [ ] "Proprietary & Confidential, Metis Strategy LLC [YEAR]" in footer of every content slide
- [ ] "Source: Metis Strategy Research & Analysis" included on data/analysis slides
- [ ] If prepared for a client: title slide reads "Prepared for [Client] | [Date] | [Title]"

---

## Troubleshooting

### Font not rendering correctly
- **Cause:** Open Sans not installed on the machine or not available in the output tool.
- **Fix:** Use Calibri as fallback in Microsoft/programmatic apps (Word, PowerPoint, pptxgenjs). For HTML/PDF outputs, load Open Sans via Google Fonts CDN. Body copy at 10-11pt / 13pt line spacing with either font.

### Colors look different on screen vs print
- **Cause:** Mint/Green (#3cdbc0) renders darker in CMYK print than on screen.
- **Fix:** For print-heavy materials, request a proof print before final delivery. Dark Blue (#20216f) is safe for both screen and print without adjustment.

### Brand asset files missing
- **Cause:** Google Drive for Desktop not running, or shared drive not mounted.
- **Fix:** All brand assets live on `G:\Shared drives\Knowledge Management\New Brand Assets\`. If Drive is unavailable, the skill still provides hex codes, font names, and rules inline. Trajectory device PNG is also in the skill's `assets/` folder.

### Output skill using wrong brand colors
- **Cause:** Some skills maintain local copies of brand specs that may drift from this canonical source.
- **Fix:** Verify colors against this skill's palette table. Canonical values: Dark Blue #20216f, Metis Green #3cdbc0. Report drift to the skill maintainer.
