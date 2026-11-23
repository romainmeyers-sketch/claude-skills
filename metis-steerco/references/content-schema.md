# SteerCo content JSON schema

The generator `scripts/build_steerco.py` reads one JSON file. See
`assets/steerco_content.example.json` for a complete, working instance.

## Top-level shape

```jsonc
{
  "meta":        { ... },   // cover + output settings
  "anchor":      { ... },   // REQUIRED — the 3-column summary slide
  "panel_slides": [ ... ],  // optional — consulting-style panel slides (launch scope, learnings)
  "risks":       { ... },   // optional — Risks & Tradeoffs card grid
  "decisions":   { ... },   // optional — Leadership Decisions rows
  "main_tables": [ ... ],   // optional — extra main-deck tables (use sparingly)
  "next_storyline": { ... },// optional — DRAFT storyline for the NEXT SteerCo
  "appendix":    [ ... ]    // optional — everything else, after the divider
}
```

Order in the deck is fixed by the generator: cover -> anchor -> panel_slides ->
risks -> decisions -> main_tables -> next_storyline -> Appendix divider ->
appendix items -> closing.

## panel_slides  (generic consulting panel slides)

For main-deck slides that are neither the anchor nor risks/decisions, e.g.
"launch scope" or "what the pilot taught us". Renders an optional mint
statement banner, N icon-header panels in the anchor visual language
(green / blue / navy), and an optional navy takeaway callout at the bottom.

```jsonc
{
  "title": "…",              // conclusion title
  "subtitle": "…",
  "banner": "…",             // optional one-sentence statement across the top
  "panels": [
    { "header": "…", "icon": "rocket",   // Lucide name, optional
      "items": ["…", "…"] }
  ],
  "callout": "…"             // optional navy takeaway bar at the bottom
}
```

Three panels read best; two also works. Banner and callout are each one
sentence.

## meta

```jsonc
{
  "label": "SteerCo Update",           // small line above the cover title
  "project_title": "…",                // cover title (the program name)
  "date": "July 14th, 2026",           // cover date line
  "cover_image": "C:/path/to.png",     // optional; omit to keep a clean cover
  "closing": "Thank You!",             // closing slide title
  "output": "SteerCo.pptx"             // default output filename
}
```

## anchor  (the most important slide — §0 of SKILL.md)

```jsonc
{
  "title": "…",           // executive conclusion, not a topic label
  "subtitle": "…",        // plain-language so-what
  "achieved":    ["…"],   // What We Achieved (mint column)
  "in_progress": ["…"],   // What We're Working On (blue column)
  "next":        ["…"],   // What's Next / the asks (navy column)
  "takeaway": "…"         // optional bottom navy bar; the one-sentence message
}
```

Keep each list item to one line. 3-5 items per column reads best.

## risks  (Risks & Tradeoffs Requiring Leadership Support)

Rendered as a consulting-style card grid, NOT a table: three icon-badge header
bands (navy / blue / green, same treatment as the anchor), one numbered card
row per risk, and the implication as a bold italic "If not:" line inside the
leadership-ask card. Risk numbers map onto the decisions slide (risk N
resolves to decision N), so keep the two lists in the same order.

```jsonc
{
  "title": "Risks & Tradeoffs Requiring Leadership Support",
  "subtitle": "…",
  "column_icons": ["triangle-alert", "wrench", "handshake"],  // optional Lucide overrides
  "rows": [
    {
      "label":           "Two-Or-Three-Word Bold Lead",  // optional but strongly recommended
      "working_through": "the risk / what we're wrestling with",
      "doing_done":      "what we're doing and what's already done",
      "needed":          "what leadership must provide",
      "implication":     "what happens if it isn't resolved"
    }
  ]
}
```

3-4 rows fit comfortably; at 5+ the body font drops a step. Keep each cell
to ~2 sentences.

## decisions  (Leadership Decisions Needed)

Rendered as decision rows, NOT a table: numbered navy badge -> neutral risk
card -> Metis-blue chevron -> navy-tinted decision card, so each row reads
"this risk resolves to this decision."

```jsonc
{
  "title": "Leadership Decisions Needed for Pilot Effectiveness",
  "subtitle": "…",
  "rows": [
    { "label":   "Same Lead as the Matching Risk", // optional bold lead
      "risk":    "the risk in one or two sentences",
      "ask":     "the SPECIFIC decision leadership must make",
      "callout": "…" }   // optional: slim mint band beneath this row for a
                         // message that travels with the decision (e.g.
                         // "teams are not locked"), NOT a separate decision
  ],
  "milestones": ["Names finalized Jul 29", "Pilot launches Aug 5",
                 "Teams executing Aug 12", "Lessons shape the next wave"]
                         // optional: chevron milestone chain across the
                         // bottom; last chevron renders green (the outcome)
}
```

Rows are auto-numbered. Make each `ask` a concrete, ownable decision, and
order rows to mirror the risks slide so the numbering lines up. 3 decisions
is the ideal count.

## main_tables  (optional, use sparingly)

Extra main-deck tables such as "Protecting Pilot Capacity Creates Real
Tradeoffs." Only for content leaders must weigh in on. Anything informational
goes in `appendix`.

```jsonc
{
  "title": "…",
  "subtitle": "…",
  "headers": ["Col A", "Col B", "Col C"],
  "col_widths": [3.0, 5.5, 3.83],   // optional inches; sums to ~12.33
  "rows": [ ["a1","b1","c1"], ["a2","b2","c2"] ]
}
```

## next_storyline  (DRAFT slide for the next SteerCo)

The forward-looking draft slide, rendered as the last main-deck slide. Omit the
whole block to get a fillable scaffold; set `meta.include_next_storyline: false`
to drop the slide entirely.

```jsonc
{
  "date": "July 28th, 2026",          // next SteerCo date (used in subtitle)
  "title": "…",                       // optional; sensible default provided
  "headline": "the one-sentence story we aim to tell next time",
  "expected_achievements": ["…"],     // "By Then We Expect to Have"
  "expected_decisions":    ["…"],     // "Decisions We'll Likely Bring"
  "watch_items":           ["…"]      // "What Must Go Right in Between"
}
```

In the weekly loop, next week's build rolls `expected_achievements` into the
fresh anchor's *What We Achieved* and `expected_decisions` into the fresh
*Leadership Decisions*.

## appendix  (everything else)

A list rendered after the Appendix divider. Each item is one of:

```jsonc
{ "type": "divider", "title": "Model Overview" }

{ "type": "bullets", "title": "…", "subtitle": "…", "bullets": ["…","…"] }

{ "type": "table", "title": "…", "subtitle": "…",
  "headers": ["…"], "rows": [ ["…"] ], "col_widths": [ … ] }
```

For appendix visuals that need more than bullets or a table (org charts,
roadmaps, operating-model diagrams), generate the deck first, then insert those
slides with **metis-pptx** (Editing mode) after the Appendix divider.
