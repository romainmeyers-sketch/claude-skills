# Component Reference

Read `references/patterns.md` for the full pattern guide. Below is how each pattern maps to HTML/CSS classes.

## Layout Grids

| Grid | CSS Class | HTML Structure |
|------|-----------|---------------|
| Full Width | `grid-full-width` | Single content area |
| Two Column | `grid-two-column` | Two `<div>` children |
| Sidebar + Main | `grid-sidebar-main` | Two `<div>` children (1/3 + 2/3) |
| Main + Sidebar | `grid-main-sidebar` | Two `<div>` children (2/3 + 1/3) |
| Three Column | `grid-three-column` | Three `<div>` children |
| Four Column | `grid-four-column` | Four `<div>` children |
| Title + Visual | `grid-title-visual` | Description + `.visual-area` |

## Badges / Tags

Small uppercase pills for status labels, tech badges, or category markers.

```html
<div class="tag-row">
  <span class="tag tag-accent">Strategy</span>
  <span class="tag tag-secondary">Technology</span>
  <span class="tag tag-primary">Priority</span>
  <span class="tag tag-muted">In Progress</span>
</div>
```

Variants: `tag-primary`, `tag-accent`, `tag-secondary`, `tag-success`, `tag-orange`, `tag-red`, `tag-purple`, `tag-muted`

## Feature Cards

Clean typography-driven cards for highlighting capabilities, benefits, or key points. **Do not use emojis or icons.**

```html
<div class="feature-card hover-lift">
  <h3>Real-Time Analytics</h3>
  <p>Stream processing with sub-second latency for operational dashboards.</p>
</div>

<!-- Bordered variant with colored accent -->
<div class="feature-card bordered blue">
  <h3>Enterprise Security</h3>
  <p>SOC 2 Type II certified with end-to-end encryption.</p>
</div>
```

## Status Indicator

Animated status badge, useful on cover slides or dashboards.

```html
<div class="status-indicator">
  <div class="status-dot"></div>
  Project Active - On Track
</div>
```

## Code Badge

Monospace text in a colored pill. Use for model names, API endpoints, version numbers.

```html
<span class="code-badge primary">v2.4.1</span>
<span class="code-badge accent">api/v3/transform</span>
<span class="code-badge blue">claude-sonnet-4-6</span>
<span class="code-badge orange">openai/gpt-5.4</span>
```

## Section Labels

Small caps category headers placed above content blocks.

```html
<div class="section-label orange">Build Agent</div>
<div class="section-label primary">Primary Model</div>
<div class="section-label">Default</div>
```

## Architecture / Flow Diagrams

Vertical or horizontal flow diagrams with connected nodes. Use typography and structure to convey hierarchy.

```html
<div class="flow-diagram">
  <div class="flow-node emphasized">
    <h3>API Gateway</h3>
    <p>Request routing - Auth - Rate limiting</p>
    <div class="tag-row" style="margin-top:0.6rem;justify-content:center;">
      <span class="tag tag-accent">REST</span>
      <span class="tag tag-accent">GraphQL</span>
    </div>
  </div>

  <div class="flow-arrow down"></div>

  <div class="flow-node-group">
    <div class="flow-node">
      <h3>ML Service</h3>
      <p>Inference pipeline</p>
    </div>
    <div class="flow-node">
      <h3>Data Store</h3>
      <p>Persistent state</p>
    </div>
    <div class="flow-node">
      <h3>Analytics</h3>
      <p>Event processing</p>
    </div>
  </div>
</div>
```

## Capability Grid

Dense grid of small cards for listing tools, capabilities, or features.

```html
<div class="capability-grid">
  <div class="capability-card">
    <h4>read</h4>
    <p>Read file contents</p>
  </div>
  <div class="capability-card">
    <h4>write</h4>
    <p>Create or overwrite files</p>
    <div class="cap-badge">Core</div>
  </div>
  <div class="capability-card">
    <h4>exec</h4>
    <p>Shell commands</p>
    <div class="cap-badge">Windows</div>
  </div>
</div>
```

## Multi-Color Accent Bars

Six color variants for accent bars to distinguish categories:

```html
<div class="accent-bar">Default mint accent</div>
<div class="accent-bar blue">Blue accent</div>
<div class="accent-bar orange">Orange accent</div>
<div class="accent-bar red">Red accent</div>
<div class="accent-bar purple">Purple accent</div>
<div class="accent-bar green">Green accent</div>
```

## A. Structural Elements

**1. Header Bar**
```html
<div class="header-bar">Section Label</div>
<div class="header-bar secondary">Blue variant</div>
<div class="header-bar accent">Accent variant</div>
```

**2. Accent Left Bar**
```html
<div class="accent-bar">
  <p>Content with a mint left border</p>
</div>
```

**3. Content Card**
```html
<div class="content-card">
  <p>Content in a clean bordered card</p>
</div>
```

**4. Divider Line**
```html
<hr class="divider-line">
<hr class="divider-line subtle">
```

**5. Illustrative Tag**
```html
<span class="illustrative-tag">ILLUSTRATIVE</span>
```

## B. Content Presentation

**7. Numbered Callout**
```html
<div class="numbered-callout">
  <div class="number">01</div>
  <div class="callout-content">
    <h3>Title</h3>
    <p>Description text</p>
  </div>
</div>
```

**8. Icon Circle + Text**
```html
<div class="icon-circle-text">
  <div class="icon-circle">1</div>
  <div class="icon-content">
    <h3>Title</h3>
    <p>Description</p>
  </div>
</div>
```

**9. Card with Header**
```html
<div class="card-with-header hover-lift">
  <div class="card-header">Header Text</div>
  <div class="card-body">Body content</div>
</div>
```

**11. Category Grid**
```html
<div class="category-grid grid-three-column">
  <div class="category">
    <div class="cat-header">Category A</div>
    <div class="cat-item">Item 1</div>
    <div class="cat-item">Item 2</div>
  </div>
</div>
```

## D. Comparison

**20. Before/After**
```html
<div class="before-after">
  <div>
    <div class="state-header">Before</div>
    <ul><li>Pain point 1</li><li>Pain point 2</li></ul>
  </div>
  <div class="arrow">-></div>
  <div>
    <div class="state-header">After</div>
    <ul><li>Improvement 1</li><li>Improvement 2</li></ul>
  </div>
</div>
```

## E. Process & Flow

**22. Connected Process**
```html
<div class="connected-process">
  <div class="step">
    <div class="step-circle">1</div>
    <div class="step-title">Step Name</div>
    <div class="step-desc">Description</div>
  </div>
  <div class="step-connector"></div>
  <div class="step">
    <div class="step-circle">2</div>
    <div class="step-title">Step Name</div>
    <div class="step-desc">Description</div>
  </div>
</div>
```

**24. Chevron Flow**
```html
<div class="chevron-flow">
  <div class="chevron bg-primary">Step 1</div>
  <div class="chevron bg-secondary">Step 2</div>
  <div class="chevron bg-accent">Step 3</div>
</div>
```

## F. Timeline

**28. 30/60/90 Backlog**
```html
<div class="backlog-30-60-90">
  <div></div>
  <div class="period-header">30 Days</div>
  <div class="period-header">60 Days</div>
  <div class="period-header">90 Days</div>
  <div class="row-label">Milestone</div>
  <div class="backlog-cell">...</div>
  <div class="backlog-cell">...</div>
  <div class="backlog-cell">...</div>
</div>
```

## G. Framework

**31. Framework Stack**
```html
<div class="framework-stack">
  <div class="layer" style="background: var(--color-primary)">
    <div class="layer-info"><h3>Layer Name</h3><p>Description</p></div>
    <div class="layer-subs">
      <div class="layer-sub" style="background: rgba(255,255,255,0.2)">Sub-component</div>
    </div>
  </div>
</div>
```

## H. Narrative

**36. Pull Quote**
```html
<div class="pull-quote">
  <div class="quote-mark">"</div>
  <div class="quote-content">
    <blockquote>The quote text goes here.</blockquote>
    <cite>Attribution, Title</cite>
  </div>
</div>
```

---

# Interactivity Tier

HTML presentations should feel interactive and engaging. Use these features liberally; they are a key advantage over PPTX.

## Entrance Animations

Add `.animate-in` to any grid container to stagger-animate children when the slide appears:

```html
<div class="grid-three-column animate-in">
  <div class="feature-card">...</div>
  <div class="feature-card">...</div>
  <div class="feature-card">...</div>
</div>
```

Use `.animate-fade` for subtler fade-in without vertical movement.

## Hover Effects

```html
<div class="content-card hover-lift">Elevates on hover</div>
<div class="content-card hover-glow">Glows with accent border on hover</div>
```

## Click-to-Reveal (Progressive Disclosure)

```html
<div class="clickable-reveal">
  <div class="reveal-trigger">
    <h3>Predictive Maintenance</h3>
  </div>
  <div class="reveal-content">
    <p>Detailed description that appears when clicked...</p>
  </div>
</div>
```

## Tabs

```html
<div class="tab-group">
  <div class="tab-headers">
    <button class="tab-btn active">Phase 1</button>
    <button class="tab-btn">Phase 2</button>
    <button class="tab-btn">Phase 3</button>
  </div>
  <div class="tab-panel active">Phase 1 content...</div>
  <div class="tab-panel">Phase 2 content...</div>
  <div class="tab-panel">Phase 3 content...</div>
</div>
```

## Accordion

```html
<div class="accordion">
  <div class="accordion-item">
    <button class="accordion-trigger">Supply Chain</button>
    <div class="accordion-body">Detailed analysis...</div>
  </div>
  <div class="accordion-item">
    <button class="accordion-trigger">Engineering</button>
    <div class="accordion-body">Detailed analysis...</div>
  </div>
</div>
```

## Animated Counters

```html
<div class="large-label count-up">$4.2M</div>
<div class="large-label count-up">87%</div>
```

## Tooltips

```html
<div class="content-card" data-tooltip="Click to expand details">
  Summary content
</div>
```

## Slide Transitions

```html
<div class="slide" data-transition="fade">...</div>
<div class="slide" data-transition="slide">...</div>
<div class="slide" data-transition="zoom">...</div>
```

## Combining Features

A single slide can combine multiple interactive features:

```html
<div class="grid-three-column animate-in">
  <div class="feature-card bordered hover-lift">
    <div class="clickable-reveal">
      <div class="reveal-trigger"><h3>Predictive Maintenance</h3></div>
      <div class="reveal-content">
        <p>Full description with ROI and timeline...</p>
      </div>
    </div>
  </div>
</div>
```
