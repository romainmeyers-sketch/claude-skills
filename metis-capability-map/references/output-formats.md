# Output Format Reference

This file contains the exact build instructions for each output format. Read the section
relevant to the user's requested format.

## Table of Contents
1. [XLSX Spreadsheet](#1-xlsx-spreadsheet)
2. [PPTX Deck](#2-pptx-deck)
3. [HTML Interactive View](#3-html-interactive-view)

---

## 1. XLSX Spreadsheet

The spreadsheet is the most data-rich output — it's the "source of truth" that other
formats can be derived from. Build it first when producing multiple formats.

### Column Structure

**Base columns (always included):**

| Column | Header              | Content                                    |
|--------|---------------------|--------------------------------------------|
| A      | Pillar              | "[Persona] Journey" / "Value Chain" / "[Internal] Journey" / "Supporting" |
| B      | L1 Capability       | Top-level capability or journey stage       |
| C      | L2 Capability Group | Capability group name                       |
| D      | L3 Capability       | Specific capability name                    |
| E      | Shared With         | Cross-reference (e.g., "Journey: Onboarding") or blank |

**Pillar order in rows:** [Persona] Journey → Value Chain → [Internal] Journey (if enabled) → Supporting

**Optional lens columns (append in this order when enabled):**

The column order flows logically: what it is → how mature → where it's going → who owns
it → investment decision. When multiple lenses are enabled, columns are shared (e.g.,
Current Maturity serves both maturity and investment lenses).

| Column | Header                | Lens              | Content                                    |
|--------|----------------------|-------------------|--------------------------------------------|
| +1     | Current Maturity (1-5)| Maturity/Investment | Empty dropdown (1-5), conditional formatting |
| +2     | Maturity Label       | Maturity          | Auto-fill formula: CHOOSE(Current, "Ad-hoc".."Optimized") |
| +3     | Target Maturity (1-5)| Investment        | Empty dropdown (1-5), conditional formatting |
| +4     | Maturity Gap         | Investment        | Formula: Target - Current. Conditional formatting (larger gap = darker red) |
| +5     | Strategic Initiative | Investment        | Free text — which strategy this supports   |
| +6     | Owner                | Ownership         | Free text — role/team/individual accountable|
| +7     | Investment Priority  | Investment        | Empty dropdown: Invest / Maintain / Divest / Sunset |

Column letters shift based on which lenses are enabled. If only Ownership is on, Owner
becomes column F. If all lenses are on, the sheet extends to column L.

### Styling

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule

wb = Workbook()

# ── Pillar colors (for row backgrounds) ──
# Pillar name for Journey varies by industry — use the persona-specific name
# e.g., "Guest Journey", "Patient Journey", "Customer Journey", "Subscriber Journey"
# Pillar order: Journey → Value Chain → Internal Journey (if enabled) → Supporting
PILLAR_FILLS = {
    journey_pillar_name:          PatternFill("solid", fgColor="E8F4FD"),  # light blue
    "Value Chain":                PatternFill("solid", fgColor="E8F8E8"),  # light green
    internal_journey_pillar_name: PatternFill("solid", fgColor="FFF5E6"),  # light amber (optional Pillar 4)
    "Supporting":                 PatternFill("solid", fgColor="F5F0FF"),  # light purple (always last)
}

# ── Header style ──
HEADER_FONT = Font(name="Calibri", bold=True, size=11, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="20206E")  # Dark Navy
HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)

# ── Maturity heat map (conditional formatting on Maturity column) ──
MATURITY_FILLS = {
    1: PatternFill("solid", fgColor="E74C3C"),  # Red - Ad-hoc
    2: PatternFill("solid", fgColor="E67E22"),  # Orange - Developing
    3: PatternFill("solid", fgColor="F1C40F"),  # Yellow - Defined
    4: PatternFill("solid", fgColor="2ECC71"),  # Green - Managed
    5: PatternFill("solid", fgColor="27AE60"),  # Dark Green - Optimized
}

# Apply conditional formatting for maturity column:
# ws.conditional_formatting.add(f'F2:F{max_row}', CellIsRule(...))
```

### Sheet Structure

- **Sheet 1: "Capability Map"** — Full L1/L2/L3 table with all base + enabled lens columns on one sheet
- **Sheet 2: "People Process Tools"** — (if enabled) L2-level breakdown of each capability across Process Maturity, Tool-set Maturity, People/Expertise Maturity, plus Org Reach and Performance Measurement, each with notes columns. Uses same 1-5 conditional formatting heat map colors.
- **Sheet 3: "Industry Benchmark"** — (if enabled) L2-level comparison: Company Maturity (avg of L3s) vs. Industry Average with Delta and Benchmark Insight. Delta column has conditional formatting: ≥0.3 green, ≤-0.5 orange, ≤-1.0 red.
- **Sheet 4: "Roadmap"** — (if enabled) Quarterly initiative sequencing with milestones, dependencies, and success metrics. Color-coded by half-year: Q1-Q2 green, Q3-Q4 blue, Q5-Q6 purple, Q7-Q8 orange.
- **Sheet 5: "Capability Definitions"** — (if enabled) L3-level definitions with Business Value, Example Activities, and Common Enterprise Tools columns.
- **Sheet 6: "Roadmap Summary"** — (if roadmap enabled) Aggregated initiative counts by quarter and pillar with key theme per quarter.
- **Sheet N-1: "Summary"** — Pivot-style summary: count of L2s and L3s per L1, avg maturity, avg gap, high-priority count, top initiative
- **Sheet N: "Journey ↔ Value Chain"** — Cross-reference matrix showing shared capabilities between pillars
- **Sheet 0: "README"** — (always included when any supplemental tab is enabled) Column reference guide explaining every column across all tabs. Place as the first sheet.

#### People Process Tools Column Structure

| Column | Header                      | Content                                               |
|--------|-----------------------------|-------------------------------------------------------|
| A      | Pillar                      | Same pillar names as Capability Map sheet              |
| B      | L1 Capability               | L1 name                                                |
| C      | L2 Capability               | L2 name (one row per L2)                               |
| D      | Process Maturity (1-5)      | 1-5 dropdown with conditional formatting               |
| E      | Process Notes               | Qualitative context on process state                   |
| F      | Tool-set Maturity (1-5)     | 1-5 dropdown with conditional formatting               |
| G      | Tool-set Notes              | Qualitative context on tools/systems                   |
| H      | People/Expertise Maturity (1-5) | 1-5 dropdown with conditional formatting           |
| I      | People Notes                | Qualitative context on skills, staffing, expertise     |
| J      | Org Reach (1-5)             | 1-5 dropdown with conditional formatting               |
| K      | Performance Measurement (1-5)| 1-5 dropdown with conditional formatting              |

#### Industry Benchmark Column Structure

| Column | Header              | Content                                               |
|--------|---------------------|-------------------------------------------------------|
| A      | Pillar              | Same pillar names as Capability Map sheet              |
| B      | L1 Capability       | L1 name                                                |
| C      | L2 Capability       | L2 name (one row per L2)                               |
| D      | Company Maturity    | Average of L3 current maturity scores for this L2      |
| E      | Industry Average    | Industry benchmark score (generated from first principles) |
| F      | Delta               | Formula: Company - Industry Average. Conditional formatting: ≥0.3=green, ≤-0.5=orange, ≤-1.0=red |
| G      | Benchmark Insight   | Brief qualitative insight explaining delta and strategic implications |

#### Roadmap Column Structure

| Column | Header              | Content                                               |
|--------|---------------------|-------------------------------------------------------|
| A      | Quarter             | Q1-Q8 dropdown, color-coded by half-year               |
| B      | Pillar              | Same pillar names as Capability Map sheet              |
| C      | L1 Capability       | L1 name                                                |
| D      | L2 Capability       | L2 name                                                |
| E      | Strategic Initiative | Action statement describing the change or investment   |
| F      | Current Maturity    | 1-5 with conditional formatting                        |
| G      | Target Maturity     | 1-5 with conditional formatting                        |
| H      | Gap                 | Target minus Current                                   |
| I      | Dependencies        | What must be in place before this can succeed          |
| J      | Milestone 1         | Single clear deliverable (planning/procurement phase)  |
| K      | Milestone 2         | Single clear deliverable (build/pilot phase)           |
| L      | Milestone 3         | Single clear deliverable (outcome/steady-state)        |
| M      | Success Metric      | Baseline → target format (e.g., "Win rate: 45% → 60%") |
| N      | Owner               | Executive accountable for delivery                     |
| O      | Investment Priority | High / Medium / Low dropdown                           |

Quarter color scheme:
- Q1-Q2: Green (#27AE60, #2ECC71) — Year 1 H1
- Q3-Q4: Blue (#256BA2, #3498DB) — Year 1 H2
- Q5-Q6: Purple (#8E44AD, #9B59B6) — Year 2 H1
- Q7-Q8: Orange (#E67E22, #F39C12) — Year 2 H2

#### Capability Definitions Column Structure

| Column | Header                  | Content                                               |
|--------|-------------------------|-------------------------------------------------------|
| A      | Pillar                  | Same pillar names as Capability Map sheet              |
| B      | L1 Capability           | L1 name                                                |
| C      | L2 Capability           | L2 name                                                |
| D      | L3 Capability           | L3 name                                                |
| E      | Definition              | Plain-language description (varied openers, not repetitive) |
| F      | Business Value          | Why it matters — framed for CFO/CEO/board              |
| G      | Example Activities      | Concrete examples of what doing this capability looks like |
| H      | Common Enterprise Tools | Representative platforms used by large enterprises (where relevant) |

### Build Tips

- Merge cells in columns A and B where the same L1 repeats across multiple L2/L3 rows
- Freeze the header row and first two columns
- Auto-fit column widths (min 15, max 40 characters)
- Add data validation dropdowns on all optional lens columns (Current/Target Maturity 1-5,
  Investment Priority Invest/Maintain/Divest/Sunset)
- Add filters on all columns
- For investment lens: apply conditional formatting on Gap column — larger gaps in darker
  red (gap ≥3 = #E74C3C, gap 2 = #E67E22, gap 1 = #F1C40F, gap 0 = #2ECC71)
- For investment priority: conditional formatting with colored fills (Invest=#27AE60 green,
  Maintain=#256BA2 blue, Divest=#E67E22 orange, Sunset=#E74C3C red) with white bold text

---

## 2. PPTX Deck

The deck is an executive presentation of the capability map. It uses the Metis Strategy
design system — read the `metis-pptx` skill's `references/design-system.md` for brand
constants and `references/layout-grids.md` for slide construction.

### Slide Sequence

```
Slide 1:  Cover — "[Company] Business Capability Map"
Slide 2:  Agenda — Overview of the three pillars
Slide 3:  Conceptual Model — The three-pillar diagram (full width)
Slide 4:  [Persona] Journey Overview — L1 stages as a horizontal flow
Slide 5+: [Persona] Journey Detail — One slide per L1 showing its L2/L3 table
Slide N:  Section Divider — "Value Chain"
Slide N+1: Value Chain Overview — L1 functions aligned to journey stages
Slide N+2+: Value Chain Detail — One slide per L1 showing its L2/L3 table
Slide P:  Section Divider — "[Internal Persona] Journey" (if Pillar 4 enabled)
Slide P+1+: [Internal Persona] Journey Detail — One slide per L1 showing its L2/L3 table
Slide M:  Section Divider — "Supporting Domains"
Slide M+1+: Supporting Detail — One slide per L1 showing its L2/L3 table
--- Optional lens slides (append before closing) ---
Slide Z-9: Roadmap Timeline (if roadmap enabled) — Horizontal swimlane timeline with
           quarters on x-axis and pillars as swim lanes. Each initiative is a colored bar.
Slide Z-8: Roadmap Summary (if roadmap enabled) — Table showing initiative count and
           key theme per quarter, with by-pillar breakdown.
Slide Z-7: Capability Definitions Appendix (if definitions enabled) — One slide per L1
           showing a table of L3 definitions with Common Tools column where relevant.
Slide Z-6: People/Process/Tools Summary (if PPT lens enabled) — Summary slide per pillar
           showing a table with Process / Tools / People columns and traffic-light indicators.
           Follow with detail slides per focus area showing strengths, needs/opportunities,
           and representative observations (matching the Metis capability assessment format).
Slide Z-5: Industry Benchmark Chart (if benchmark lens enabled) — Grouped bar chart showing
           Company Maturity vs. Industry Average by L1 capability, with delta annotations.
Slide Z-4: Industry Benchmark Key Gaps & Strengths (if benchmark lens enabled) — Summary
           slide listing top 5 gaps (largest negative delta) and top 3 strengths (largest
           positive delta) with benchmark insights.
Slide Z-3: Investment Matrix (if investment lens enabled) — 2x2 bubble chart:
           X-axis = Current Maturity (1-5), Y-axis = Strategic Importance
           Bubble color = Investment Priority (green=Invest, blue=Maintain, orange=Divest, red=Sunset)
           Plot L1 or L2 capabilities as bubbles
Slide Z-2: Ownership Summary (if ownership lens enabled) — Table grouped by owner,
           showing which L1/L2 capabilities each leader is accountable for.
           This is the operating model slide.
Slide Z-1: Maturity Summary (if maturity enabled) — Heat map overview across all pillars
Slide Z:   Closing slide
```

### Table Layout for Detail Slides

Each detail slide uses **Grid 5 (Title + Visual)** from the metis-pptx layout system.
The content area is a table:

```python
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor

# Table dimensions for capability detail
LEFT   = Inches(0.50)
TOP    = Inches(1.30)
WIDTH  = Inches(12.33)
HEIGHT = Inches(5.30)

# Column widths vary by which optional lenses are enabled:
# Base:            L2 (3.5") | L3 (5.5") | Shared (3.33")
# + Maturity:      L2 (3.0") | L3 (4.5") | Shared (2.5") | Maturity (1.33") | Label (1.0")
# + Investment:    Add Investment Priority tag as colored badge within L3 cell (no extra column)
# + Ownership:     L2 (3.0") | L3 (4.0") | Shared (2.0") | Owner (2.0") | [+ maturity cols]
# Adapt widths to fit — never exceed 12.33" total
```

### Table Cell Styling

```python
# Header row
HEADER_BG = RGBColor(0x20, 0x20, 0x6E)  # Dark Navy
HEADER_FONT_COLOR = RGBColor(0xFF, 0xFF, 0xFF)
HEADER_FONT_SIZE = Pt(11)

# Data rows — alternate between white and light gray
ROW_EVEN = RGBColor(0xFF, 0xFF, 0xFF)
ROW_ODD  = RGBColor(0xF2, 0xF2, 0xF2)

# Maturity cell backgrounds use the heat map colors from SKILL.md section 3

# Cell padding: use internal margins of 0.05" on all sides
# Font: Calibri 10pt for table cells, bold for L2 grouping rows
```

### Overview / Flow Slides

For the Journey Overview slide, render the L1 stages as a horizontal process flow:

```python
# Horizontal arrow flow for journey stages
stage_count = len(journey_l1s)
box_width = (12.33 - (stage_count - 1) * 0.15) / stage_count  # equal width, 0.15" gaps
box_height = 0.8

for i, stage in enumerate(journey_l1s):
    left = Inches(0.50 + i * (box_width + 0.15))
    top = Inches(2.0)
    # Rounded rectangle with Mint fill
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top),
        Inches(box_width), Inches(box_height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x3B, 0xDA, 0xC0)  # Mint
    # Add chevron arrow between stages (except after last)
```

---

## 3. HTML Interactive View

A single standalone HTML file with no external dependencies. Everything is inlined —
CSS, JS, and data.

### Features

- Collapsible tree: Pillar → L1 → L2 → L3 (click to expand/collapse)
- Color-coded pillar sections (blue/green/purple + amber for optional Pillar 4)
- Maturity badges with heat map colors (if maturity lens enabled)
- Investment priority pill badges (if investment lens enabled):
  - Invest = green pill, Maintain = blue pill, Divest = orange pill, Sunset = red pill
  - Gap indicator showing current → target maturity with arrow
  - Filterable: toolbar buttons to show only Invest / Maintain / Divest / Sunset
  - Gap analysis summary section at top showing count of capabilities per priority bucket
- Ownership labels (if ownership lens enabled):
  - Gray label beneath each L3 showing the owner
  - **"Group by Owner" toggle button** in the toolbar that reorganizes the entire map
    by owner instead of by pillar. When toggled, each owner becomes a collapsible section
    with their capabilities listed beneath, regardless of which pillar they belong to.
    This is the operating model view.
- People/Process/Tools view (if PPT lens enabled):
  - Toggle-able tab that shows L2 capabilities with Process / Tool-set / People maturity
    scores and qualitative notes
  - Same heat map colors as main maturity view
  - Expandable notes sections per L2
- Industry Benchmark view (if benchmark lens enabled):
  - Toggle-able tab showing Company vs. Industry Average with delta bars
  - Sortable columns (click to sort by delta, company maturity, etc.)
  - Filter buttons: "Show Gaps Only" (negative delta) / "Show Strengths Only" (positive)
  - Summary banner: count of capabilities above / at / below industry average
- Roadmap view (if roadmap enabled):
  - Toggle-able tab with Gantt-style timeline (quarters on x-axis, pillars as swim lanes)
  - Filterable by pillar, quarter, and investment priority
  - Clickable initiatives expand to show milestones, dependencies, and success metrics
  - Roadmap summary banner with initiative count and key theme per quarter
- Capability Definitions view (if definitions enabled):
  - Toggle-able tab with searchable definitions
  - Each L3 expands to show Business Value, Example Activities, and Common Tools
  - Filterable by pillar
- Search/filter bar that highlights matching capabilities
- Print-friendly CSS (`@media print` hides controls, expands all)
- Responsive layout (works on tablet/desktop)

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Company] Business Capability Map</title>
  <style>
    /* Inline all styles — no external CSS */
    :root {
      --navy: #20206E;
      --blue: #256BA2;
      --mint: #3BDAC0;
      --dark-gray: #4A4A4A;
      --light-gray: #F2F2F2;
      --journey-bg: #E8F4FD;
      --valuechain-bg: #E8F8E8;
      --supporting-bg: #F5F0FF;
      --internal-bg: #FFF5E6;
      --invest: #27AE60;
      --maintain: #256BA2;
      --divest: #E67E22;
      --sunset: #E74C3C;
    }
    body { font-family: Calibri, 'Segoe UI', sans-serif; margin: 0; padding: 20px; color: var(--dark-gray); }
    .header { background: var(--navy); color: white; padding: 24px 32px; border-radius: 8px; margin-bottom: 24px; }
    .pillar { margin-bottom: 20px; border-radius: 8px; overflow: hidden; }
    .pillar-header { padding: 16px 20px; font-size: 18px; font-weight: bold; cursor: pointer; }
    .l1-item { padding: 12px 20px 12px 32px; border-bottom: 1px solid #e0e0e0; cursor: pointer; }
    .l2-item { padding: 8px 20px 8px 52px; font-weight: 600; }
    .l3-item { padding: 6px 20px 6px 72px; display: flex; align-items: center; gap: 12px; }
    .maturity-badge {
      display: inline-block; padding: 2px 10px; border-radius: 12px;
      font-size: 12px; font-weight: 600; color: white;
    }
.collapsible-content { display: none; }
    .collapsible-content.open { display: block; }
    .search-bar { width: 100%; padding: 10px 16px; font-size: 14px; border: 1px solid #ccc; border-radius: 6px; margin-bottom: 16px; }
    .highlight { background: #FFF3CD; }
    .owner-label { font-size: 11px; color: #888; margin-top: 2px; }
    .investment-pill { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; color: white; }
    .investment-pill.invest { background: var(--invest); }
    .investment-pill.maintain { background: var(--maintain); }
    .investment-pill.divest { background: var(--divest); }
    .investment-pill.sunset { background: var(--sunset); }
    .gap-indicator { font-size: 11px; color: #666; }
    .toolbar { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
    .toolbar button { padding: 6px 14px; border: 1px solid #ccc; border-radius: 4px; background: white; cursor: pointer; font-size: 13px; }
    .toolbar button.active { background: var(--navy); color: white; border-color: var(--navy); }
    @media print { .search-bar, .toolbar { display: none; } .collapsible-content { display: block !important; } }
  </style>
</head>
<body>
  <div class="header">
    <h1>[Company] Business Capability Map</h1>
    <p>L1–L3 Capabilities across [Persona] Journey, Value Chain, and Supporting Domains</p>
  </div>
  <input type="text" class="search-bar" placeholder="Search capabilities..." id="search">
  <!-- Pillar sections rendered here by JS from inline data -->
  <script>
    const DATA = /* capability map JSON embedded here */;
    // Render tree, handle collapse/expand, search filtering
  </script>
</body>
</html>
```

### Data Format (embedded in HTML)

```json
{
  "company": "Acme Corp",
  "industry": "Luxury Hospitality",
  "lenses": ["maturity", "investment", "ownership"],
  "pillars": [
    {
      "name": "Guest Journey",
      "color": "#E8F4FD",
      "l1s": [
        {
          "name": "Discovery",
          "l2s": [
            {
              "name": "Brand Presence",
              "l3s": [
                {
                  "name": "Social Media Management",
                  "shared_with": "",
                  "maturity": null,
                  "investment_priority": null,
                  "current_maturity": null,
                  "target_maturity": null,
                  "strategic_initiative": "",
                  "owner": ""
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

Only include lens fields that are enabled. The `lenses` array tells the renderer which
optional UI elements to show (filter buttons, Group by Owner toggle, gap summary, etc.).

The script reads this JSON and builds the DOM dynamically. When ownership is enabled,
add a "Group by Owner" toggle that rebuilds the tree grouped by the `owner` field instead
of by pillar. When investment is enabled, add filter buttons for each priority level and
a summary bar showing capability counts per bucket.
