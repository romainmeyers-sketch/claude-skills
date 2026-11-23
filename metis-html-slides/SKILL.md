---
name: metis-html-slides
description: >
  Generate HTML presentations as self-contained single files with sidebar
  navigation, scrollable sections, and interactive components. Use when the
  user wants a browser-viewable presentation. Ideal for internal decks,
  workshop materials, and strategy frameworks. Triggers on "html slides,"
  "html presentation," "browser deck," or when the user asks for HTML output
  instead of PPTX. Always validates against metis-brand-identity. Do NOT use
  for: PowerPoint files (metis-pptx); PDF documents (metis-pdf-creator);
  whitepapers (metis-whitepaper); proposals (metis-premier-proposal).
metadata:
  author: Metis Strategy
  version: 2.0.9
---

# HTML Presentation Skill — Metis Strategy

## 0. When to Use This Skill vs metis-pptx

| Scenario | Use this skill | Use metis-pptx |
|----------|---------------|----------------|
| Client needs to edit the deck in PowerPoint | No | Yes |
| Internal Metis review or workshop | Yes | Optional |
| Polished visual deliverable, no editing needed | Yes | Optional |
| Client explicitly asks for PPTX | No | Yes |
| Rapid prototyping / draft visualization | Yes | No |
| User says "html," "browser," or "web presentation" | Yes | No |
| Information-dense, scrollable content needed | Yes | No |
| Interactive elements (tabs, accordions, reveal) | Yes | No |

**If unsure, ask:** "Would you like this as an HTML presentation (viewable in any browser) or as a PowerPoint file?"

---

## 1. Brand Mode

**Before building, determine the brand:**

| Condition | Theme to use |
|-----------|-------------|
| Metis-branded deck (no client template) | `templates/metis-theme.css` (default) |
| Client-branded deck (client provides a .pptx template) | Extract theme with `scripts/extract_theme.py` |

### Extracting a Client Theme

```bash
PYTHON="C:/Users/$USER/AppData/Local/Programs/Python/Python312/python.exe"
"$PYTHON" "$SKILL_DIR/scripts/extract_theme.py" client_deck.pptx --output client-theme.css
```

This generates a CSS file with the client's colors, fonts, and spacing as CSS custom properties. Pass it to the build script with `--theme client-theme.css`.

---

## 2. Python Environment

> **Python is installed but NOT on the git bash PATH.** Use the full path:
> ```bash
> PYTHON="C:/Users/$USER/AppData/Local/Programs/Python/Python312/python.exe"
> ```
> **Do NOT** loop trying to install Python or add it to PATH.

Locate the skill directory:
```bash
SKILL_DIRS=(
    "$HOME/.metis/skills/.agents/skills/tessl__metis-html-slides"
    "$HOME/.metis/skills/.tessl/tiles/metis-strategy/metis-html-slides"
    ".tessl/tiles/metis-strategy/metis-html-slides"
)
for d in "${SKILL_DIRS[@]}"; do
    if [ -d "$d/templates" ]; then SKILL_DIR="$d"; break; fi
done
```

---

## 3. Architecture: Sections & Slides

### The Section Model

Every presentation is organized into **sections**. Each section appears as a numbered item in the persistent left sidebar. A section can contain one or more slides.

```
Sidebar                          Content Area
┌──────────────┐  ┌──────────────────────────────────────┐
│ METIS LOGO   │  │ § 1 · Executive Summary    ‹ 2/12 › │
│              │  │──────────────────────────────────────│
│ 01 ● Cover   │  │                                      │
│ 02 ○ Exec    │  │  Scrollable slide content here       │
│    Summary   │  │                                      │
│ 03 ○ Current │  │  Can extend beyond viewport          │
│    State     │  │                                      │
│   · Market   │  │                                      │
│   · Compete  │  │                                      │
│ 04 ○ Strategy│  │                                      │
│              │  │                                      │
│ ▓▓▓░░  2/12 │  │                                      │
└──────────────┘  └──────────────────────────────────────┘
```

### Key Concepts

- **Sections are sidebar entries.** Each gets a number (01, 02, ...) and a label.
- **Slides belong to sections.** One section can have multiple slides grouped under it.
- **Sub-labels** appear indented under the parent section when multiple slides share a section.
- **Scrollable content.** Slides can be longer than the viewport — the user scrolls within the section.
- **The build script auto-generates the sidebar** from `data-section-*` attributes on slide divs.

### Slide HTML Structure

Every slide div **must** include these data attributes:

```html
<!-- Single slide in a section (most common) -->
<div class="slide" data-section-num="1" data-section-title="Executive Summary">
  <div class="slide-content">
    <h1 class="slide-title">Executive Summary</h1>
    <p class="slide-subtitle">Key findings and recommendations</p>
    <!-- content here -->
  </div>
  <div class="slide-footer">
    <span>Proprietary &amp; Confidential — Metis Strategy LLC 2026</span>
    <span></span>
  </div>
</div>

<!-- Multiple slides grouped under one section -->
<div class="slide" data-section-num="2" data-section-title="Current State" data-sub-label="Market Analysis">
  <div class="slide-content">
    <h1 class="slide-title">Market Analysis</h1>
    <!-- content -->
  </div>
  <div class="slide-footer">
    <span>Proprietary &amp; Confidential — Metis Strategy LLC 2026</span>
    <span></span>
  </div>
</div>

<div class="slide" data-section-num="2" data-section-title="Current State" data-sub-label="Competitive Landscape">
  <div class="slide-content">
    <h1 class="slide-title">Competitive Landscape</h1>
    <!-- content -->
  </div>
  <div class="slide-footer">
    <span>Proprietary &amp; Confidential — Metis Strategy LLC 2026</span>
    <span></span>
  </div>
</div>
```

### Special Slide Types

**Cover slide** — Always the first slide. Uses dark navy background with the trajectory device.

```html
<div class="slide cover" data-section-num="0" data-section-title="Cover">
  <div class="slide-content">
    <div class="cover-brandline">Driving change. Elevating leaders.</div>
    <h1 class="slide-title"><strong>Digital Transformation</strong> Strategy</h1>
    <p class="slide-subtitle">Prepared for Acme Corporation</p>
    <p class="cover-detail">April 2026 | Confidential</p>
  </div>
  <div class="slide-footer">
    <span>Metis Strategy</span>
    <span></span>
  </div>
</div>
```

**Section divider** — Dark navy slide marking a new major section.

```html
<div class="slide divider" data-section-num="3" data-section-title="Strategic Recommendations">
  <div class="slide-content">
    <div class="section-number">Section 03</div>
    <h1 class="slide-title">Strategic Recommendations</h1>
    <p class="slide-subtitle">Three pathways to accelerate growth</p>
    <div class="divider-accent"></div>
  </div>
</div>
```

**Content slide** — The standard slide type.

```html
<div class="slide" data-section-num="3" data-section-title="Strategic Recommendations" data-sub-label="Vision & Objectives">
  <div class="slide-content">
    <h1 class="slide-title">Vision & Objectives</h1>
    <p class="slide-subtitle">A three-year digital transformation roadmap</p>
    <div class="grid-two-column animate-in">
      <!-- Components go here -->
    </div>
  </div>
  <div class="slide-footer">
    <span>Proprietary &amp; Confidential — Metis Strategy LLC 2026</span>
    <span></span>
  </div>
</div>
```

---

## 4. Build Workflow

### Phase 1: Plan the Deck

Create a slide-by-slide outline. For each slide, decide:
- **Section number and title** — which sidebar section does this belong to?
- **Sub-label** (if grouped) — what sub-item label appears in the sidebar?
- **Slide type:** cover, divider, or content
- **Layout grid:** which of the 6 grids (see Component Reference below)
- **Components:** which patterns to use
- **Content:** write the actual text, not placeholders

**Important planning guidance:**
- Aim for 6–12 sections in the sidebar. Too many makes navigation cluttered.
- Use section grouping (multiple slides per section) for deep-dive areas.
- Section divider slides are optional but recommended at major transitions.
- Every content slide should have a footer with the confidentiality notice.
- Use the scrollable nature of slides — a single "section" can hold substantial content if organized well.

### Phase 2: Write the Slides HTML

Create a Python script that writes an HTML file containing slide `<div>` elements. Every slide must include `data-section-num` and `data-section-title` attributes.

**Critical rules:**
- Every `<div class="slide">` is one slide
- Content goes inside `<div class="slide-content">`
- Use layout grid classes on a container div inside slide-content
- Compose components inside the grid
- Write **real content** — no placeholders
- **Never use emojis or decorative icons** — they are unprofessional and an AI telltale sign. Use typography, color accents, and whitespace for visual hierarchy instead.
- Apply Metis brand identity: confident, clean, forward-moving tone
- Use Open Sans Light for titles (CSS handles this), semibold for emphasis
- Lead with insight, not labels — slide titles should be declarative

### Phase 3: Build the Presentation

```bash
"$PYTHON" "$SKILL_DIR/scripts/build_deck.py" slides.html output.html \
    --title "Deck Title" \
    --subtitle "Prepared for Client | April 2026"

# With client theme:
"$PYTHON" "$SKILL_DIR/scripts/build_deck.py" slides.html output.html \
    --theme client-theme.css \
    --title "Client Deck" \
    --subtitle "Client Name"
```

The build script:
1. Reads the base HTML template
2. Inlines the theme CSS + component CSS
3. **Parses section metadata** from slide data attributes
4. **Auto-generates the sidebar navigation** with sections and sub-items
5. **Embeds the Metis logo** (base64-encoded from brand assets)
6. Base64-encodes any local images
7. Outputs a single self-contained HTML file

### Phase 4: QA

Open the output HTML in a browser and verify:
- Sidebar navigation works (clicking sections and sub-items)
- Progress bar updates as you navigate
- Section breadcrumb updates correctly
- Content scrolls properly for long sections
- Keyboard navigation works (arrows, Home/End, F for fullscreen)
- All interactive elements work (tabs, accordions, click-to-reveal)
- Metis branding is correct (colors, fonts, logo)
- No text overflow or layout issues

---

## 5. Component Reference

Read `references/components.md` for the full HTML/CSS component library with copy-paste code for all patterns. Also read `references/patterns.md` for the pattern guide.

**Available component categories:**
- Layout grids (7 types: full-width, two-column, sidebar+main, three-column, four-column, title+visual)
- Badges/tags, feature cards, status indicators, code badges, section labels
- Architecture/flow diagrams, capability grids
- Multi-color accent bars (6 variants)
- Structural elements (header bar, accent bar, content card, divider, illustrative tag)
- Content presentation (numbered callout, icon circle, card with header, category grid)
- Comparison (before/after)
- Process & flow (connected process, chevron flow)
- Timeline (30/60/90 backlog)
- Framework (framework stack)
- Narrative (pull quote)

---

## 6. Interactivity Tier

Read `references/components.md` (Interactivity section) for full HTML code snippets.

**Available interactive features:**
- **Entrance animations:** `.animate-in` (stagger), `.animate-fade` (subtle)
- **Hover effects:** `.hover-lift` (elevate), `.hover-glow` (accent border)
- **Click-to-reveal:** `.clickable-reveal` with `.reveal-trigger` + `.reveal-content`
- **Tabs:** `.tab-group` with `.tab-btn` + `.tab-panel`
- **Accordion:** `.accordion` with `.accordion-item` + `.accordion-trigger` + `.accordion-body`
- **Animated counters:** `.count-up` on `.large-label`
- **Tooltips:** `data-tooltip` attribute
- **Slide transitions:** `data-transition="fade|slide|zoom"`

These features are a key advantage over PPTX. Use them liberally.

---

## 7. Keyboard Navigation

The output HTML supports:
- **Arrow keys / Space** — next/previous slide
- **F** — toggle fullscreen
- **N** — toggle speaker notes
- **Home / End** — first/last slide
- **Click** — right 70% = next, left 30% = previous (in content area)
- **Swipe** — touch device support
- **Sidebar click** — jump to any section or sub-item

---

## 8. Speaker Notes

Add notes inside any slide (hidden by default, toggled with N key):

```html
<aside class="notes" style="display:none; padding: 1rem; background: #ffe; font-size: 0.8rem;">
  Talking points for this slide go here.
</aside>
```

---

## 9. Brand Assets

The Metis logo is automatically embedded by the build script from:
`G:\Shared drives\Knowledge Management\New Brand Assets\Metis Strategy Logo\Metis Strategy Black-Mint RGB Logo.png`

If the G: drive is not available, the build script falls back to a text-based logo.

For cover slides, you can reference the trajectory device graphic:
`G:\Shared drives\Knowledge Management\New Brand Assets\Graphic Devices\Metis Trajectory Device RGB.png`

Include it as an `<img>` inside the cover slide — the build script will base64-encode it:
```html
<img class="cover-device"
     src="G:/Shared drives/Knowledge Management/New Brand Assets/Graphic Devices/Metis Trajectory Device RGB.png"
     alt="">
```

---

## 10. Component Selection Guide

| Content type | Component class | Grid |
|---|---|---|
| 3-5 key points | `.feature-card` or `.numbered-callout` | `grid-full-width` or `grid-two-column` |
| Capabilities / deliverables | `.card-with-header` or `.capability-grid` | `grid-three-column` |
| Status labels / categories | `.tag-row` with `.tag` elements | Any grid |
| System architecture | `.flow-diagram` with `.flow-node` | `grid-full-width` |
| Tech identifiers | `.code-badge` | Inline |
| Category headers | `.section-label` | Above content blocks |
| Phased approach | `.phased-approach` or `.tab-group` | `grid-full-width` |
| Process / steps | `.connected-process` or `.chevron-flow` | `grid-full-width` |
| Timeline | `.backlog-30-60-90` or `.swimlane-roadmap` | `grid-full-width` |
| Pricing / tiers | `.tiered-table` | `grid-full-width` |
| Before vs after | `.before-after` | `grid-full-width` |
| Model options | `.three-option` | `grid-full-width` |
| Operating model | `.radial-diagram` | `grid-full-width` |
| Framework | `.framework-stack` | `grid-full-width` |
| Maturity | `.maturity-journey` | `grid-full-width` |
| Key quote | `.pull-quote` | `grid-full-width` |
| Benefits list | `.benefits-blocks` or `.feature-card` | `grid-full-width` or `grid-two-column` |
| Dense feature list | `.capability-grid` | `grid-full-width` |

---

## Troubleshooting

### Sidebar navigation not rendering
- **Cause:** JavaScript disabled in browser or HTML file not saved as UTF-8.
- **Fix:** Ensure the browser has JavaScript enabled. Save the HTML file with UTF-8 encoding (default for the build script).

### Fonts not loading (fallback serif appearing)
- **Cause:** Google Fonts CDN not reachable (offline or VPN restriction).
- **Fix:** For offline use, download Open Sans font files and embed as base64 in the `<style>` block. The build script can do this automatically with the `--embed-fonts` flag.

### File too large to email (>10 MB)
- **Cause:** Embedded images (base64-encoded photos) inflate file size.
- **Fix:** Compress images before embedding, or link to external image URLs instead of base64. Target <5 MB for email-friendly presentations.

### Interactive features not working (tabs, accordion, reveal)
- **Cause:** JavaScript block at the end of the HTML was truncated or malformed.
- **Fix:** Check that the closing `</script>` tag is present. The build script places all interactivity JS at the bottom of the file. If regenerating, ensure the full script block is included.

### Brand colors look wrong
- **Cause:** CSS variables not matching metis-brand-identity canonical values.
- **Fix:** Verify `--color-primary: #20216f`, `--color-accent: #3cdbc0` in the `:root` block. See metis-brand-identity skill for canonical values.
