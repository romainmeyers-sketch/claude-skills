# Slide Patterns Reference

Layout grids and component patterns for slide design. These patterns describe what to
build and when to use each pattern. They apply regardless of brand — use them for both
Metis-branded and client-branded presentations.

---

## Grid Patterns

Grids define the column structure within a slide's content area. The sidebar
occupies the left 280px; grids fill the remaining space. Content within a slide
can scroll vertically, so grids are not height-constrained.

### Grid 1: Full Width

**Best for:** Executive summaries, key findings, narratives, flow diagrams, architecture diagrams.

```
+----------------------------------------------------------+
|  Full-width content zone                                   |
|  100% of content width                                     |
+----------------------------------------------------------+
```

### Grid 2: Two Column (Equal)

**Best for:** Comparisons, before/after, feature cards side-by-side, pros/cons.

```
+----------------------------+----------------------------+
|  Left column (50%)         |  Right column (50%)        |
|                            |  [2rem gap]                |
+----------------------------+----------------------------+
```

### Grid 3: Sidebar + Main (1/3 + 2/3)

**Best for:** Key metric + explanation, sidebar callout + main content, icon + detail.

```
+----------------+------------------------------------------+
|  Sidebar (33%) |  Main content (66%)                      |
|                |  [2rem gap]                              |
+----------------+------------------------------------------+
```

### Grid 3b: Main + Sidebar (2/3 + 1/3)

**Best for:** Main content with supporting sidebar on the right.

```
+------------------------------------------+----------------+
|  Main content (66%)                      |  Sidebar (33%) |
|  [2rem gap]                              |                |
+------------------------------------------+----------------+
```

### Grid 4: Three Column

**Best for:** Three pillars, three phases, three options, feature card triads.

```
+------------------+------------------+------------------+
|  Column 1 (33%) |  Column 2 (33%) |  Column 3 (33%) |
|  [1.5rem gaps]                                        |
+------------------+------------------+------------------+
```

### Grid 5: Four Column

**Best for:** Dense capability grids, four-category comparisons.

```
+-------------+-------------+-------------+-------------+
|  Col 1 (25%)|  Col 2 (25%)|  Col 3 (25%)|  Col 4 (25%)|
|  [1.2rem gaps]                                         |
+-------------+-------------+-------------+-------------+
```

### Grid Selection Guide

| Content type | Grid | Why |
|---|---|---|
| Executive summary, key findings | Full Width | Narrative needs horizontal space |
| Current vs future, comparison | Two Column | Side-by-side is natural |
| KPI callout + explanation | Sidebar + Main | Big number draws the eye |
| Feature highlights | Main + Sidebar | Content left, supporting cards right |
| Phases, pillars, options | Three Column | Equal weight to each item |
| Process flow, architecture | Full Width | Maximum diagram area |
| Dense capabilities / tools | Four Column | Compact card grid |
| Feature cards | Two or Three Column | Cards need breathing room |

---

## Component Patterns

Organized into 10 categories (A–J). Each component describes a reusable visual pattern
for slide content. When building slides, compose 1-3 of these patterns together and
apply interactivity (hover, animation, click-to-reveal) wherever it adds value.

### A. Structural Elements

**1. Header Bar** — Full-width colored rectangle with contrasting text. Labels content sections visually. Variants: primary (navy), secondary (blue), accent (mint).

**2. Accent Left Bar** — Thin vertical bar on the left edge of a content block. Available in 6 colors: mint (default), blue, orange, red, purple, green. Use to distinguish categories.

**3. Content Card** — Bordered rounded rectangle with subtle shadow. The workhorse container. Pair with header bars, accent bars, icons, or hover effects.

**4. Horizontal Divider Line** — Thin horizontal line separator. Variants: accent (mint) or subtle (gray).

**5. Illustrative Tag** — Small uppercase tag in upper-right corner. Auto-add when content is directional or conceptual.

**6. Section Label** — Small caps, letter-spaced category header placed above content blocks. Available in 7 colors. Use to label categories, model tiers, or content types.

### B. Content Presentation

**7. Numbered Callout** — Large light-weight number + bold title + body text. Default for 3-5 key points.

**8. Icon Circle + Text** — Filled circle with number/letter + title + description. Polished numbered list.

**9. Card with Header** — Header bar top + card body below. Mini-card for grouped info with a clear label. Add `.hover-lift` for interactivity.

**10. Benefits Text Blocks** — Clean paired title + body in two columns, no boxes. For visual simplicity.

**11. Category Grid** — Header bars across top + stacked rows below. For capability maps and multi-category comparisons.

### C. Tiered / Pricing / Assessment

**12. Tiered Table** — Color-graded rows with graduated fill. For pricing or maturity levels.

**13. Harvey Balls** — Partially filled circles indicating capability levels (0-4).

**14. Heat Map Table** — Table with cells colored by intensity. For scoring and assessment views.

**15. Scorecard Grid** — Dense grid combining table structure with maturity indicators.

### D. Comparison & Matrix

**16. Split Panel** — Two zones with numbered items and shared center column. For challenge/solution pairs.

**17. Three Option Comparison** — Three equal zones with header, description, pros, cons. For comparing approaches.

**18. 2x2 Matrix** — Four quadrants with axis labels. For strategic positioning.

**19. Persona Columns** — Persona columns with stacked attribute rows. For role-based analysis.

**20. Before / After** — Two-state comparison with directional arrow. For evolution views.

### E. Process & Flow

**21. Phased Approach** — Three phase columns with activities and deliverables. Signature methodology slide.

**22. Connected Process** — Horizontal circles connected by lines with labels below. Default for 3-5 step processes.

**23. Stage Ribbon** — Horizontal colored blocks for stage labels. Graduated colors for progression.

**24. Chevron Flow** — Arrow/chevron shapes for journey or progression.

**25. Funnel** — Narrowing stages from wide (top) to narrow (bottom). Graduated colors.

**26. Radial Diagram** — Central circle with spoke elements arranged around it. For operating models.

**27. Input/Process/Output** — Three blocks: inputs (narrow), process (wide), outputs (narrow).

### F. Timeline & Roadmap

**28. 30/60/90 Backlog** — Three-column timeline with period headers and row labels.

**29. Swimlane Roadmap** — Time columns across top, swimlane rows down left. Colored bars show duration.

**30. Opportunity Map** — Grid with focus area rows and use case card cells.

### G. Framework / Conceptual

**31. Framework Stack** — Full-width horizontal bands with sub-component cards. For layered architectures.

**32. Hub and Spoke** — Central hub with domain circles around it. Uses radial-diagram CSS.

**33. Maturity Journey** — Ascending stages left to right with dots and labels.

**34. Pyramid / Venn** — Pyramid: layered hierarchy. Venn: overlapping circles for concept convergence.

### H. Narrative

**36. Pull Quote** — Decorative quotation mark + italic quote + attribution. For executive quotes.

### I. Navigation & Status (NEW)

**37. Badge / Tag Row** — Horizontal row of small uppercase pills. Use for status labels, tech badges, category markers. 8 color variants: primary, accent, secondary, success, orange, red, purple, muted.

**38. Status Indicator** — Animated green dot + text badge. For project status, system health, or live indicators on cover slides.

**39. Feature Card** — Title + description in a clean bordered card. Optional colored left border for category distinction. Add `.hover-lift` for interactivity. Default choice for highlighting capabilities, benefits, or key points. **No icons or emojis** — use typography and accent colors instead.

### J. Architecture & Systems (NEW)

**40. Flow Diagram** — Vertical or horizontal flow with connected nodes and arrow connectors. Nodes contain titles, descriptions, and optional tag rows. Use `.flow-node-group` for parallel branches. No icons — let structure and typography convey the hierarchy.

**41. Code Badge** — Monospace text in a colored pill. For model names, API endpoints, version numbers, tech identifiers. 7 color variants.

**42. Capability Grid** — Dense grid of small cards (3 or 4 columns). Each card: title + one-line description + optional badge. For listing tools, features, or capabilities.

---

## Component Selection Guide

| Content type | Default component(s) | Grid |
|---|---|---|
| 3-5 key points or findings | #39 Feature Card or #7 Numbered Callout | Two or Three Column |
| Capabilities, deliverables | #9 Card with Header or #42 Capability Grid | Three or Four Column |
| Status labels, categories | #37 Tag Row | Any (inline) |
| System architecture | #40 Flow Diagram | Full Width |
| Tech identifiers, versions | #41 Code Badge | Any (inline) |
| Category headers | #6 Section Label | Above content blocks |
| Phased approach | #21 Phased Approach or Tabs | Full Width |
| Process / steps | #22 Connected Process or #24 Chevron | Full Width |
| Timeline / roadmap | #29 Swimlane Roadmap or #28 30/60/90 | Full Width |
| Pricing / tiers | #12 Tiered Table | Full Width |
| Before vs after | #20 Before/After or #16 Split Panel | Full Width |
| Model options | #17 Three Option Comparison | Full Width |
| Operating model | #26 Radial Diagram | Full Width |
| Framework | #31 Framework Stack | Full Width |
| Maturity assessment | #33 Maturity Journey or #15 Scorecard | Full Width |
| Key quote | #36 Pull Quote | Full Width |
| Benefits list | #10 Benefits Blocks or #39 Feature Card | Full or Two Column |
| Dense feature list | #42 Capability Grid | Full Width |
| Project/system status | #38 Status Indicator | Cover or any |
| Conceptual hierarchy | #34 Pyramid | Full Width |
| Concept overlap | #34 Venn | Full Width |
