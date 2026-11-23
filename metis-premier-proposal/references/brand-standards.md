<!-- Brand source: metis-brand-identity v0.2.2 | Synced: 2026-05-21 -->
# Metis Brand Standards for Proposal PDFs

Applied brand standards as used in the Citi CRS Proposal. These are the values you use in the build script — no guessing, no approximation.

---

## Colors

```python
from reportlab.lib.colors import HexColor, Color

DARK_NAVY   = HexColor('#20216f')  # Primary headings, section dividers, metric numbers on dark
MED_BLUE    = HexColor('#256ba2')  # Secondary accents, colored bands, 2x2 matrix cells
MINT        = HexColor('#3cdbc0')  # Highlights, accent bars, eyebrow labels, small arrows
GRAY        = HexColor('#7b8692')  # Body supporting text, captions, footer text
DARK_GRAY   = HexColor('#333333')  # Primary body text
LIGHT_BG    = HexColor('#f4f6fa')  # Card backgrounds, metric card backgrounds
TEAL_LIGHT  = HexColor('#e8f8f5')  # Callout box backgrounds
WHITE_CLR   = HexColor('#ffffff')
```

**Supplementary colors used in 2x2 matrices and pillar bands:**
- Light cool gray: `#e8eef5`
- Light mint: `#dff0ee`
- Deep teal: `#1a8a7a`
- Near-black navy: `#1a2040`

### Color role assignments

| Element | Color |
|---|---|
| Page titles (light pages) | DARK_NAVY |
| Page titles (dark pages) | WHITE_CLR |
| Body text | DARK_GRAY |
| Eyebrow labels | MINT |
| Subtitle / caption text | GRAY (or `Color(1,1,1,0.65)` on dark) |
| Metric card big number | MINT |
| Metric card label | GRAY |
| Callout label | MINT |
| Callout box background | TEAL_LIGHT |
| Callout box left bar | DARK_NAVY |
| Numbered badge (light pages) | DARK_NAVY |
| Numbered badge (proof points) | MINT |
| Pull quote left bar | MINT |
| Column header underline | MINT |
| Module card top accent | MINT |

---

## Typography

**Primary font:** Calibri (Windows fallback, matches Metis PowerPoint brand)
**Ideal font:** Open Sans from Google Fonts (matches whitepaper standard) — only if Playwright is in the stack; ReportLab uses registered TTF fonts, so Calibri is cleaner on Windows builds

### Register fonts at the top of the build script

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Calibri',         'C:/Windows/Fonts/calibri.ttf'))
pdfmetrics.registerFont(TTFont('Calibri-Bold',    'C:/Windows/Fonts/calibrib.ttf'))
pdfmetrics.registerFont(TTFont('Calibri-Italic',  'C:/Windows/Fonts/calibrii.ttf'))
pdfmetrics.registerFont(TTFont('Calibri-Light',   'C:/Windows/Fonts/calibril.ttf'))
```

### Size hierarchy

| Element | Font | Size | Leading | Notes |
|---|---|---|---|---|
| Cover title | Calibri-Bold | 32 | — | 2 lines max |
| Section divider title | Calibri-Bold | 26 | 32 | 1–2 lines |
| Page title | Calibri-Bold | 20 | 24 | Wraps to 2 lines if long |
| Compact page title | Calibri-Bold | 18 | 22 | For dense pages like Fiserv |
| Section subhead / big number | Calibri-Bold | 24 | — | Metric cards (auto-shrinks) |
| Body text | Calibri | 10.5–11 | 14.5–15.5 | Paragraphs, descriptions |
| Bullet items | Calibri | 10.5 | 15 | With item_gap 5–18pt |
| Small body / phase bullets | Calibri | 9–9.5 | 12.5–13.5 | Dense content |
| Callout body | Calibri | 9.5 | 13.5 | |
| Callout label | Calibri-Bold | 7.5 | — | Uppercase |
| Eyebrow | Calibri-Bold | 8.5 | — | Uppercase, letter-spaced if possible |
| Metric card label | Calibri | 7 | — | Uppercase, auto-shrinks |
| Figure caption | Calibri-Italic | 9 | — | |
| Footer | Calibri | 7–8.5 | — | Right-aligned |
| Copyright | Calibri | 7 | — | |

### Type rules

- **No italics in body text.** Italic is reserved for pull quotes, figure captions, and purpose statements in pillar cards.
- **No color besides the palette.** Never introduce red, orange, yellow — those would break the visual language.
- **No more than 3 type sizes in a single layout** (title, body, caption is the typical triad). Metric cards and callouts can add a 4th.

---

## Logos

All three logo variants are at `G:\Shared drives\Knowledge Management\New Brand Assets\Metis Strategy Logo\`:

```python
LOGO_DIR = 'G:/Shared drives/Knowledge Management/New Brand Assets/Metis Strategy Logo/'
LOGO_BM  = LOGO_DIR + 'Metis Strategy Black-Mint RGB Logo.png'   # Black wordmark + mint M
LOGO_WM  = LOGO_DIR + 'Metis Strategy White-Mint RGB logo.png'   # White wordmark + mint M (FOR DARK PAGES)
LOGO_W   = LOGO_DIR + 'Metis Strategy White RGB logo.png'        # All-white (rarely used)
```

### Placement rules

| Page type | Logo | Position | Size |
|---|---|---|---|
| Cover | LOGO_WM | Top-left, (48, H-60) | 100pt wide |
| Section divider | LOGO_WM | Top-left, (48, H-60) | 100pt wide |
| Content page (light bg) | LOGO_BM | Top-right, (W-90, H-32) | 70pt wide |
| Photo-banner header | LOGO_WM | Top-right, (W-90, H-32) | 70pt wide |
| Closing page | LOGO_WM | Top-left, (48, H-60) | 100pt wide |

### Critical helper function

Use this `place_image` pattern — plain `drawImage` with `width` only and `preserveAspectRatio=True` is unreliable across ReportLab versions:

```python
def place_image(path, x, y, w=None, h=None, mask='auto'):
    """Place an image. Specify w or h (or both). y is bottom edge.
    Computes the missing dimension from aspect ratio for consistent rendering."""
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

This uses PIL to read the image's aspect ratio, then passes explicit width AND height to `drawImage`. Without this, logos rendered as 0-height on some pages in the Citi build.

---

## Graphic Devices

At `G:\Shared drives\Knowledge Management\New Brand Assets\Graphic Devices\`:

```python
GD         = 'G:/Shared drives/Knowledge Management/New Brand Assets/Graphic Devices/'
TRAJECTORY = GD + 'Metis Trajectory Device RGB.png'
NEXUS      = GD + 'Metis Nexus Device Opaque RGB.png'
ENERGY     = GD + 'Metis Energy Device RGB.png'
ARROW_DEV  = GD + 'Metis Arrow Device Opaque RGB.png'
SNGL_ARROW = GD + 'Metis SnglArrow Device RGB.png'  # Small, 9pt accent next to eyebrows
```

### Device application rules

| Device | Where | Opacity | Notes |
|---|---|---|---|
| Trajectory | Cover, section dividers, closing page | 0.15–0.25 | Right-anchored, partially cropped off-page, NEVER flipped |
| Nexus | Our Approach divider (symmetry feels "collaborative") | 0.15–0.28 | Right-anchored |
| Energy | Subtle texture on content pages | 0.04–0.10 | Bottom-left or bottom-full-width |
| Arrow (opaque) | Lower-right feature on light content pages | 0.04 | Partially cropped off-page edge |
| Single arrow (small) | 9pt × 9pt next to every eyebrow label | 1.0 | Core brand element, always present |

### Opacity rules

These matter. The wrong opacity makes the device either invisible (too low) or competes with content (too high). Tested values:

- **Trajectory on cover:** 0.20
- **Trajectory on divider:** 0.15
- **Trajectory on closing:** 0.12
- **Nexus on divider:** 0.15
- **Energy as background texture:** 0.04
- **Arrow opaque as corner feature:** 0.04

### Common mistake: forgetting the single arrow next to eyebrows

Every eyebrow label on every content page should have the single-arrow device 9pt × 9pt to its left. It's a small detail that distinguishes a Metis document from generic PDF output.

```python
def eyebrow(text, y, x=48):
    c.setFont('Calibri-Bold', 8.5)
    c.setFillColor(MINT)
    try:
        c.drawImage(SNGL_ARROW, x, y - 1, width=9, height=9,
                    mask='auto', preserveAspectRatio=True)
    except: pass
    c.drawString(x + 14, y, text.upper())
```

---

## Stock Photography

B&W photo library at `G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\Metis PPT Images\`. Use these on photo-left problem pages and case study pages.

**Selection guidelines:**

| Topic | Recommended photos |
|---|---|
| Technology / office | `pexels-divinetechygirl-1181311-bw.jpg`, `pexels-pixabay-63320-bw.jpg` |
| Collaboration / people | `pexels-thecoachspace-2977547-bw.jpg` |
| Abstract / atmospheric | `chris-linnett-Rl8gOeq0xNM-unsplash-bw.jpg` |
| Architecture / structure | `pexels-pixabay-276299-bw.jpg`, `Metis_flatiron_bw2.jpg` (NYC) |
| Action / movement | `Metis_leap_bw_2.jpg` |

### Photo overlay requirement

B&W photos must always have a dark overlay to ensure text legibility:

```python
photo_w = W * 0.40
c.drawImage(PHOTO_BW, 0, 0, width=photo_w, height=H, mask=None)
c.setFillColor(Color(0, 0, 0, 0.50))  # 50% black overlay
c.rect(0, 0, photo_w, H, fill=1, stroke=0)
```

Overlay opacity 0.45–0.50 is the sweet spot. Below 0.40, text is hard to read. Above 0.55, photos look muddy.

---

## Brand Line

`"Driving change. Elevating leaders."`

Usage:
- Closing page, bottom-left, mint, 9pt Calibri (not bold)
- Optional inclusion in cover page footer

Never use in body text, callouts, or page titles.

---

## What You Do Not Use

Even though these are brand-adjacent, they are out of scope for proposal PDFs:

- Purple (`#762cb3`) — reserved for spoke/domain accents in hub-spoke diagrams built in PPTX
- Light blue background (`#cbe1f3`) — reserved for tag pills
- Tier gradient colors (`#D1E3F1` / `#A3C7E3` / `#75ABD5`) — only for pricing tables
- "METIS" without the M logo mark

Stick to the palette and devices above. The proposal should feel like a consistent artifact in a family of Metis materials, not a one-off design.
