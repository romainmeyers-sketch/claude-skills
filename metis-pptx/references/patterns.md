# Slide Patterns Reference (Brand-Agnostic)

Universal layout grids and component patterns for slide design. These patterns describe
WHAT to build and WHEN to use each pattern. They apply regardless of brand — use them
for both Metis-branded and client-branded presentations.

For Metis-specific code implementations, see `metis-brand.md`.
When editing a client deck, use these patterns but apply the client's own colors, fonts,
and spacing extracted via `scripts/extract_brand.py`.

> **For Metis generation, these are the *fallback* path.** The primary path is
> the template's native layouts (`metis-layouts.md`, SKILL.md §0.5.1). Reach for a
> hand-built grid/component only when no native layout fits the content. When you
> do, avoid making even-column card grids the spine of the deck, they are the
> most over-used AI layout. Favor asymmetry, varied density, and real specifics
> (SKILL.md §0.7).

---

## Grid Patterns

All grids assume a standard content zone between the title area (top ~15% of slide)
and footer area (bottom ~9% of slide), leaving ~76% of slide height for content.
Standard margins are ~3.75% of slide width on each side.

### Grid 1: Full Width

**Best for:** Executive summaries, key findings, narratives, recommendations, single visuals.

```
+----------------------------------------------------------+
|  Title                                                    |
+----------------------------------------------------------+
|                                                            |
|  Full-width content zone                                   |
|  100% of content width                                     |
|                                                            |
+----------------------------------------------------------+
```

Single content zone spanning the full width between margins.

### Grid 2: Two Column (Equal)

**Best for:** Comparisons, before/after, pros/cons, current vs future state.

```
+----------------------------+----------------------------+
|  Title                                                   |
+----------------------------+----------------------------+
|                            |                            |
|  Left column (48.5%)       |  Right column (48.5%)      |
|                            |                            |
|                            |  [~2.5% gutter]            |
+----------------------------+----------------------------+
```

Two equal zones with a small gutter between them.

### Grid 3: Sidebar + Main (1/3 + 2/3)

**Best for:** Key metric + explanation, sidebar callout + main content, icon + detail.

```
+----------------+------------------------------------------+
|  Title                                                     |
+----------------+------------------------------------------+
|                |                                          |
|  Sidebar (30%) |  Main content (66%)                      |
|                |                                          |
|                |  [~4% gutter]                            |
+----------------+------------------------------------------+
```

Narrow accent zone for a callout or big metric, with a wide main content zone.

### Grid 4: Three Column

**Best for:** Three pillars, three phases, three options, three team members.

```
+------------------+------------------+------------------+
|  Title                                                  |
+------------------+------------------+------------------+
|                  |                  |                  |
|  Column 1 (31%) |  Column 2 (31%) |  Column 3 (31%) |
|                  |                  |                  |
|  [~3% gutters]                                        |
+------------------+------------------+------------------+
```

Three equal zones — gives equal visual weight to each item.

### Grid 5: Title + Large Visual Area

**Best for:** Framework diagrams, process flows, org charts, large tables, timeline visuals.

```
+----------------------------------------------------------+
|  Title                                                    |
+----------------------------------------------------------+
|  Subtitle / description strip (~10% of content height)    |
+----------------------------------------------------------+
|                                                            |
|  Large visual area (~85% of content height)                |
|  Use for: tables, shape-based diagrams, charts             |
|                                                            |
+----------------------------------------------------------+
```

Maximizes diagram/visual space with a thin description strip above.

### Grid Selection Guide

| Content type | Grid | Why |
|---|---|---|
| Executive summary, key findings | 1 (Full Width) | Narrative needs horizontal space |
| Current vs future, comparison | 2 (Two Column) | Side-by-side is natural |
| KPI callout + explanation | 3 (Sidebar + Main) | Big number draws the eye |
| Phases, pillars, options | 4 (Three Column) | Equal weight to each item |
| Process flow, org chart, timeline | 5 (Title + Visual) | Maximum diagram area |
| Bullet list or recommendations | 1 (Full Width) | Simple content, full width |
| SWOT, matrix, quadrant | 5 (Title + Visual) | Shape-based diagram |
| Team / stakeholder intro | 4 (Three Column) | One column per person/group |

---

## Component Patterns

Organized into 8 categories. Each component describes a reusable visual pattern
for slide content. When building slides, compose 1-3 of these patterns together.

### A. Structural Elements

**1. Header Bar**
Full-width or column-width colored rectangle with contrasting text. Labels content sections visually. Use instead of bold text alone whenever you need to visually separate a section.

**2. Accent Left Bar**
Thin vertical bar on the left edge of a content block. Pair with callouts, findings, or key point blocks for visual emphasis.

**3. Content Card**
Rounded rectangle with light fill, no border. The workhorse container. Never use alone with plain text — always pair with a header bar, accent bar, or icon.

**4. Horizontal Divider Line**
Thin horizontal line as a separator. Use instead of whitespace when sections need clear visual boundaries.

**5. Illustrative / Non-Exhaustive Tag**
Small italic tag in the upper-right corner of the slide. Use **only** on a slide that is genuinely illustrative (a sample figure, a deliberately partial list). Do **not** auto-add it to every conceptual slide, a reflexive hedge tag on slide after slide is itself an "AI deck" tell (see SKILL.md §0.7).

### B. Content Presentation

**6. Large Letter / Number Label**
Oversized bold character (3x body font size) as a visual anchor. Replaces plain bullets for sets of 3-6 items. The letter/number sits at the left edge, with title and body text aligned to its right.

**7. Numbered Callout Block**
Large number (2.5x body font size) + bold title + body text. The default pattern for presenting 3-5 key points. Number anchors the left, title and body stack to its right.

**8. Icon Circle + Text**
Filled circle with a number/letter inside, paired with title + description to its right. Use for numbered lists where a more polished look is needed.

**8b. Graphical Icon Card (Lucide)**
Real graphical glyph (Lucide icon) paired with title + body in a clean card. Use when the icon itself is the visual anchor: categories, capabilities, process steps, anything where a number-in-a-circle would be less expressive than a shield, a server, a clipboard, etc. Helper: `scripts/icons.py::lucide_icon_card`. Reference: `references/icons.md`. Pick *either* #8 *or* #8b for a given slide. Never mix numbered circles and graphical icons in the same row.

**9. Content Card with Header**
Header bar on top + content card body below. A mini-card pattern. Good for grouping related information with a clear label.

**10. Key Benefits Text Blocks**
Clean paired title + body blocks in two columns, no boxes or backgrounds. For when visual simplicity is the goal.

**11. Category Grid**
Row of header bars across the top, stacked content rows below each. For capability maps, deliverable catalogs, and multi-category comparisons.

### C. Tiered / Pricing / Assessment

**12. Tiered Pricing Table**
Color-graded rows built from shapes. Tier labels on the left column with graduated fill colors (light to dark). Data cells in a neutral background. Column headers in a dark fill.

**13. Harvey Balls / Maturity Indicators**
Partially filled circles indicating capability/maturity levels (empty, quarter, half, three-quarter, full). Use graduated colors from light to dark.

**14. Heat Map Table**
Table with cells colored by value. Dark header row, labeled left column, and data cells with fill colors indicating intensity or score.

**15. Assessment Scorecard Grid**
Dense grid showing maturity across multiple dimensions. Combines table structure with maturity-level indicators.

### D. Comparison & Matrix

**16. Split Panel (Challenges / Solutions)**
Slide split into two zones with numbered items on each side and shared numbering in a center column. Shows parallel concepts (challenge-solution pairs).

**17. Push / Pull / Hybrid Comparison**
Three equal zones showing model options. Each zone: header bar, description, positives box, challenges box. For comparing 3 approaches.

**18. 2x2 Matrix**
Four quadrants with axis labels. Built as a 3x3 table: header row, header column, 4 content cells. For strategic positioning.

**19. Persona Comparison Columns**
3 persona columns with stacked rows. Header bars at top, row labels on the far left, content cards at each intersection. For role-based analysis.

**20. Before / After Evolution**
Two-state comparison with a directional arrow between them. Two equal columns with header bars and content below each.

### E. Process & Flow

**21. Phased Approach (Activities + Deliverables)**
Three phase columns with header bars, plus two labeled sections within each (activities and deliverables). Side labels indicate section type.

**22. Connected Circle Process**
Horizontal row of circles connected by lines, with titles and descriptions below each. Default for 3-5 step processes.

**23. Stage Ribbon**
Horizontal row of colored blocks with stage labels. Each block spans an equal portion of content width. Use graduated colors for progression.

**24. Chevron / Arrow Flow**
Horizontal arrow/chevron shapes for journey or progression. Each chevron contains a label. Use cycling brand colors for distinction.

**25. Funnel**
Narrowing stages from widest (top) to narrowest (bottom). Centered horizontal bars with label and description. Graduated colors.

**26. Radial / Lifecycle Diagram**
Central circle with items arranged in a ring around it. Central element = core concept; surrounding elements = related stages/domains. Trigonometric positioning.

**27. Input / Process / Output Flow**
Three blocks: Inputs (narrow), Process (wide, center), Outputs (narrow). Each block contains a label and nested content cards for individual items.

### F. Timeline & Roadmap

**28. 30/60/90 Day Backlog**
Three-column timeline with header bars for each period. Row labels on the left (Milestone, Objective, Activities). Content cards at each intersection.

**29. Swimlane Gantt / Roadmap**
Table with time columns across top and swimlane rows down the left. Colored bars span cells to show durations.

**30. Use Case Opportunity Map**
Grid where rows = focus areas (labeled left), cells = use case cards with annotations. For portfolio views across categories.

### G. Framework / Conceptual

**31. Layered Framework Stack**
Full-width horizontal bands for framework layers. Each band: name/description on the left, sub-component cards within the band. Sub-components use a lighter shade. Bands use graduated colors (dark to light, top to bottom).

**32. Hub-and-Spoke Diagram**
Central hub circle with surrounding domain circles. Hub = core concept; spokes = domain labels. Trigonometric positioning.

**33. Maturity Journey Curve**
Ascending stages left to right. Each stage: dot positioned progressively higher, label below, description beneath. Connecting lines show progression.

**34. Hexagon Grid / Pyramid / Venn**
- **Pyramid:** Layers from narrowest (top) to widest (bottom), centered. Graduated colors. For hierarchies.
- **Venn (2-circle):** Two overlapping circles with transparency, label in the overlap zone. For concept convergence.

### H. Narrative

**36. Pull Quote Block**
Large decorative quotation mark + italic quote text + attribution line below. For featuring executive quotes or impactful findings.

*(Note: Component #35 is not defined — numbering gap is intentional.)*

---

## Component Selection Guide

| Content type | Default component(s) | Why |
|---|---|---|
| 3-5 key points or findings | #7 Numbered Callout, #8 Icon Circle, or #8b Graphical Icon Card | Visual anchors replace bullets. Pick #8b when concepts are distinct categories rather than ordered priorities. |
| Capabilities, deliverables, workstreams | #9 Content Card with Header or #11 Category Grid | Structured grouping |
| Phased engagement approach | #21 Phased Approach | Signature methodology slide |
| Process / steps | #22 Connected Circle or #24 Chevron Flow | Shows progression |
| Timeline / roadmap | #29 Swimlane Gantt or #28 30/60/90 Backlog | Shows time dimension |
| Pricing / tiers | #12 Tiered Pricing Table | Color-graded rows |
| Before vs after / comparison | #20 Before/After or #16 Split Panel | Side-by-side |
| Model options / tradeoffs | #17 Push/Pull/Hybrid | Three-zone comparison |
| Operating model | #32 Hub-and-Spoke | Central + distributed |
| Framework / architecture | #31 Layered Stack | Horizontal bands |
| Maturity assessment | #33 Maturity Journey or #15 Scorecard | Shows progression |
| Key quote or executive statement | #36 Pull Quote | Visual emphasis |
| Methodology explanation | #27 Input/Process/Output | Three-block flow |
| Portfolio / opportunity view | #30 Use Case Map | Grid of cards |
| Benefits list | #10 Benefits Text Blocks | Clean two-column |
| Conceptual hierarchy | #34 Pyramid | Layered visual |
| Concept overlap | #34 Venn | Shows intersection |
| Persona analysis | #19 Persona Columns | Stacked row comparison |
| Challenges and solutions | #16 Split Panel | Numbered items both sides |
| Section divider | Use template's section divider layout | Built into template |
| Any directional content | Add #5 Illustrative Tag | Flags as conceptual |

---

## Component Rotation Guide

When multiple slides share the same content type, use different components from the
alternatives below. **Never use the same primary component on consecutive slides.**

### Rotation Alternatives by Content Type

| Content type | 1st choice | 2nd choice | 3rd choice | Notes |
|---|---|---|---|---|
| 3-5 key points | #7 Numbered Callout | #8 Icon Circle + Text *or* #8b Graphical Icon Card | #10 Benefits Text Blocks | Rotate across these to avoid "wall of numbered cards." Pick #8b when concepts are distinct categories rather than ordered priorities. |
| 3-5 key points (variant) | #9 Content Card w/ Header | #6 Large Letter Label | #3 Content Card + #2 Accent Bar | Use when you exhaust the first three |
| Capabilities / deliverables | #9 Content Card w/ Header | #11 Category Grid | #7 Numbered Callout | Cards and grids alternate well |
| Process / steps | #22 Connected Circle | #24 Chevron Flow | #27 Input/Process/Output | Circle vs. chevron vs. block gives visual contrast |
| Comparison / before-after | #20 Before/After Evolution | #16 Split Panel | #17 Push/Pull/Hybrid | Each uses a different spatial metaphor |
| Framework / architecture | #31 Layered Stack | #32 Hub-and-Spoke | #34 Pyramid | Horizontal bands vs. radial vs. vertical hierarchy |
| Timeline / roadmap | #29 Swimlane Gantt | #28 30/60/90 Backlog | #23 Stage Ribbon | Table vs. columns vs. linear bar |
| Benefits / value prop | #10 Benefits Text Blocks | #7 Numbered Callout | #9 Content Card w/ Header | Clean text vs. numbered vs. boxed |
| Quote / executive statement | #36 Pull Quote | #3 Content Card + #2 Accent Bar | Grid 3 sidebar with large quote mark | Quote block vs. accent card vs. sidebar layout |

### Slide Archetype Categories

Every content slide falls into one of these archetypes. Vary the archetype across
consecutive slides to create visual rhythm:

| Archetype | Description | Components | Feel |
|---|---|---|---|
| **A. Narrative** | Quote, key message, executive summary | #36, #10, Grid 1 full-width text | Open, spacious, text-forward |
| **B. Analytical** | Data, evidence, comparison, assessment | #20, #16, #14, #12, #18 | Structured, side-by-side, dense |
| **C. Conceptual** | Framework, model, architecture, journey | #31, #32, #33, #34, #26 | Diagrammatic, visual, abstract |
| **D. Itemized** | Key points, capabilities, benefits, phases | #7, #8, #9, #11, #21 | Repeated units, cards, columns |

**Ideal rhythm for a 10-slide keynote:** A - D - B - C - D - A - C - B - D - A

This sequence ensures no archetype appears twice in a row and each archetype
appears 2-3 times across 10 slides.
