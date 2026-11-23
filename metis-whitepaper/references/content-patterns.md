# Whitepaper Content Patterns

## Table of Contents
1. [Document Narrative Arc](#1-document-narrative-arc)
2. [Page-Level Content Templates](#2-page-level-content-templates)
3. [Writing Voice](#3-writing-voice)
4. [Framework Diagram Descriptions](#4-framework-diagram-descriptions)
5. [Case Study Callout Format](#5-case-study-callout-format)
6. [Pull Quotes](#6-pull-quotes)
7. [Section Header Patterns](#7-section-header-patterns)
8. [Credits Page Format](#8-credits-page-format)

---

## 1. Document Narrative Arc

Every Metis whitepaper follows this macro structure:

```
PROBLEM / TENSION
  → The market context or challenge leaders face
  → Stakes: why this matters now, what's at risk

METIS FRAMEWORK / APPROACH
  → Metis's proprietary lens for addressing this challenge
  → Typically 2–4 numbered major sections

EVIDENCE & EXAMPLES
  → Real client examples (named or anonymized)
  → Data points with sources
  → "In our experience…" observations from Metis practice

PRACTICAL GUIDANCE
  → What leaders should actually do
  → Phased approaches, maturity models, prioritization tools

CALL TO ACTION
  → Invitation to engage with Metis
  → Resources / further reading
```

Within each major section, paragraphs follow this micro-arc:
**Insight → Evidence → Implication**
- Lead with the conclusion or recommendation, not the process
- Support with data or client example
- Close with the "so what" for the executive reader

---

## 2. Page-Level Content Templates

### Cover Page
- **Eyebrow**: Short subtitle in caps/small-caps (e.g., "THE METIS STRATEGY FRAMEWORK FOR…")
- **Title**: Large, 2–3 line display headline (e.g., "AI Smart: Maximizing AI Value with a Balanced Strategy")
- **Subtitle**: 1–2 sentence description of the framework and audience
- **No body text on cover** — photo + title + logo only

### Abstract / Introduction Page
Pattern: photo banner at top → horizontal rule → SnglArrow + eyebrow label → display hook → two-column body text
- **Hook**: A bold, declarative opening sentence. Not a question. Not "In today's world."
  - Good: "Artificial intelligence is arguably the most transformative force of modern business."
  - Bad: "AI is changing everything for companies today."
- **Opening body**: Problem statement in 2–3 short paragraphs. Set up the tension the whitepaper will resolve.
- **Metis POV paragraph**: Bold or italic lead-in sentence stating Metis's position, followed by explanation.
  - Example: *"We advise that digital and technology leaders take a measured approach, that they neither 'wait and see,' nor pursue AI at all costs."*

### Section Divider Page
Full-page teal-to-navy gradient (`linear-gradient(135deg, #20216f 0%, #256ba2 35%, #1a8a7a 60%, #3cdbc0 100%)`) with trajectory device overlay at 30% opacity. Contains:
- Section title in white text (no white pill/badge background) — `font-size: 22px; font-weight: 700; color: white;`
- Bold centered pull statement (1–2 sentences) below the title
- All text elements need `position:relative;z-index:1;` to sit above the background image

Content to write:
```
[SECTION NUMBER + TITLE]
[Pull statement: the one sentence that captures the section's core insight]
```
Example:
```
II. AI Funding

According to a recent study by Glean and TechStrong, companies spent 2.7% of their
IT budgets on Generative AI in 2024. In 2025, they're anticipated to spend 4.3%.
This doubling suggests a robust investment appetite that will no doubt catch the eye
of the CFO.
```

### Standard Content Page (Text-Only)
- Horizontal rule at top-left
- SnglArrow + section label (small, e.g., "AI Strategy")
- Large section headline
- Body text: 2 columns (landscape) or single column (portrait)
- Optional pull quote set apart in bold/larger text
- Optional framework diagram placeholder with "Source: Metis Strategy" caption
- Optional client example callout box

### Photo + Text Content Page
Left half: full-bleed photo (dark, atmospheric, or people-focused)
Right half: text content (section header + body)
OR:
Top half: full-bleed photo banner
Bottom half: text content in 2 columns

### Dark Navy Content Page
Used for:
- Multi-step frameworks ("5 Steps for Mitigating Risk")
- Key lists ("7 Signs That…")
- Phase descriptions within an operating model

White text on dark navy background.
Teal (#3cdbc0) used for step numbers, bullet points, and callout text.

### Conclusion / Recap Page
- Eyebrow: "Recap" or "Conclusion"
- Headline: Insight-led, not just "Conclusion" — e.g., "The Companies That Evolve Will Win"
- Body: 2–3 short paragraphs summarizing Metis's core recommendations
- Credits block (names only, or separate credits page)

---

## 3. Writing Voice

Metis whitepapers are **published thought leadership**, not client deliverables. The voice:

**DO:**
- Lead every section with a bold declarative statement
- Use "we" and "our work with clients" to establish Metis's practice authority
- Reference named companies where permission exists; use industry/segment descriptor otherwise ("a global retailer," "a Fortune 500 financial services firm")
- Use precise, vivid language: "5x efficiency gain" not "significant improvement"
- Write short paragraphs (3–5 sentences max) — each paragraph = one clear idea
- Use the active voice exclusively in recommendations: "We recommend," "Leaders should," "Organizations must"
- Headers should be declarative or evocative: "Funding Models" → "Funding the AI Journey" → better: "Why the Funding Model Must Evolve as AI Scales"

**DON'T:**
- Open paragraphs with "In today's," "As AI continues to," or "Organizations face"
- Use "utilize" (use "use"), "leverage" as a verb for non-mechanical things, "impactful"
- Write passive constructions: "it was found that" → "we found"
- Use academic hedging: "it could be argued," "this suggests"
- Reproduce frameworks from competitors or consultancies (McKinsey 3-horizon, Gartner quadrants, etc.) without full transformation and attribution
- **Cite or reference McKinsey, Bain, BCG, or Deloitte** — these are Metis Strategy competitors. Never use their research, reports, or frameworks as sources. Use industry analysts, academic research, developer surveys, and government/nonprofit sources instead
- **Overuse em dashes.** Frequent em dashes are a hallmark of AI-generated prose. Limit to one per page maximum. Replace them with a period and a new sentence, a colon, or a comma. Bad: "The platform team — not the product teams — owns this." Better: "The platform team owns this, not the product teams." Bad: "This matters — and it matters now." Better: "This matters. It matters now."

**On word count per page:**
- Landscape pages: ~150–250 words of body text per content page
- Portrait pages: ~200–350 words of body text per content page
- Section dividers: ~30–60 words (pull statement only)
- Avoid padding — empty white space with a strong photo is better than weak filler text

---

## 4. Framework Diagram Descriptions

When a whitepaper includes a proprietary framework, describe it precisely so a designer can build it:

**Template:**
```
[DIAGRAM NAME] (Source: Metis Strategy)

Type: [matrix / ladder / cycle / layered table / swimlane / 2x2]
Orientation: [horizontal / vertical]
Layers/Columns/Quadrants: [list each with label and description]
Color coding: [which elements are which brand colors]
Notes for designer: [any specific layout guidance]
```

**Example — AI Maturity Model:**
```
AI Maturity Model (Source: Metis Strategy)

Type: Horizontal progression ladder (5 levels)
Orientation: Horizontal left-to-right, with vertical "Value-Add" axis label on left
Levels: 1-Student, 2-Explorer, 3-Builder, 4-Scaler, 5-Commander
Each level: Number in circle → bold title → 3-4 bullet descriptors
Colors: Level circles in Dark Blue, text dark gray, background white/light gray
Axis arrow: Dark Blue, pointing up on left side ("Value-Add")
Notes: "Most Companies" label above Level 3 with dotted vertical line
```

---

## 5. Case Study Callout Format

Named company examples that are **one sentence** are woven into body text. Examples that span **two or more sentences** should be styled as callout boxes. This serves double duty: it gives the case study visual prominence AND fills page space that would otherwise be blank. On pages with photo+text split layouts, a callout box in the text column is especially effective.

**Inline format:**
> [Company], for example, [past tense action]. [Outcome/result]. [Why this is relevant to the reader's situation.]

Example:
> Ally Financial, as an example, deployed a bot to help its Agile product owners manage backlogs. The simple task of updating acceptance criteria for user stories with common requirements, such as security standards, can save significant time for a role that is often resource constrained.

**Box format** (for page-dominant examples):
```
[COMPANY / SECTOR] ← teal label
[Bold headline: what they did]
[2–3 sentences: context, action, outcome]
[Metis role or observation if relevant]
```

---

## 6. Pull Quotes

Select one pull quote per 2–3 pages. Rules:
- Must be the single strongest, most quotable sentence in the section
- Attributed to a Metis partner or named CIO/CDO interviewee if possible; otherwise unattributed
- Bold, slightly larger than body text (13–14pt vs 11pt body)
- Italicized on white pages; white bold text on dark pages
- Set apart with extra vertical space above and below

**Format in written content:**
Mark pull quotes clearly in the draft so the designer knows to call them out:
```
[PULL QUOTE] "You need the business to be in a place where they understand and
embrace it, and then you as a tech leader provide the guidance and technology to
take them with you." — Praveen Jonnala, CIO, CommScope [/PULL QUOTE]
```

---

## 7. Section Header Patterns

Every section header on a content page follows this visual hierarchy:

```
[Thin horizontal rule]
▶ [Section Label in small text, Metis Green]

[Large Section Headline]
```

When writing, annotate the hierarchy explicitly:
```
---[RULE]---
▶ AI Strategy  ← eyebrow (small, green)

I. AI Strategy  ← main headline (large)
```

On dark navy pages, eyebrow and headline are white; SnglArrow is teal.

**Eyebrow text rules:**
- Short: 1–3 words (section name, phase name, or topic label)
- Never the full section headline — just the category
- Examples: "Introduction," "AI Strategy," "Phase 1: Define," "Tech Leader Concerns," "Recap"

---

## 8. Credits / Closing Page Format

The closing page (before References/Endnotes) is a clean branded sign-off. Do NOT include individual author cards, headshot layouts, or "AI Working Group" text.

**Standard format:**
- Dark navy background with Energy device at 8% opacity as background texture
- Metis Strategy White-Mint logo centered vertically on page (height ~52px)
- Contact email in teal below: `info@metisstrategy.com`
- Copyright line at bottom: "Proprietary & Confidential, Metis Strategy LLC [YEAR]"

```html
<div class="page" style="background:var(--dark-blue);padding:56px 64px;display:flex;flex-direction:column;justify-content:space-between;">
  <img class="metis-m" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20White-Mint%20RGB%20Logo.png" alt="Metis Strategy" />

  <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;">
    <img src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20White-Mint%20RGB%20Logo.png" height="52" alt="Metis Strategy" />
    <p style="font-size:14px;color:var(--green);font-weight:600;">info@metisstrategy.com</p>
  </div>

  <div style="text-align:center;">
    <p style="font-size:10px;color:rgba(255,255,255,0.40);">Proprietary &amp; Confidential, Metis Strategy LLC [YEAR]</p>
  </div>
</div>
```

---

## 9. Endnote Citations

All whitepapers use numbered endnote citations. Never use inline parenthetical citations.

**In-text:** Place a superscript number immediately after the claim: `<sup class="fn">1</sup>`
- On dark pages: `<sup class="fn on-dark">1</sup>`

**References/Endnotes page:** The last page lists all sources as numbered entries:
```
1. Stack Overflow. 2025 Developer Survey: AI Tools & Developer Experience. 2025.
   https://survey.stackoverflow.co/2025/
2. GitHub. Octoverse 2024: The State of Open Source. 2024.
   https://octoverse.github.com/2024
```

**Source exclusion rule:** Never cite McKinsey, Bain, BCG, or Deloitte. These are Metis Strategy competitors. Preferred source types: industry analysts (Gartner, IDC, Forrester), academic (arXiv, university), developer surveys (Stack Overflow, JetBrains, GitHub), government/nonprofit (DORA, Linux Foundation, NIST), and vendor research (Microsoft Research, Google Research).
