---
name: metis-pptx
description: >
  Create or edit PowerPoint (.pptx) files. Two modes: (1) template-preserving
  editing when an existing .pptx is provided, (2) generation when a new
  Metis-branded deck is needed. Trigger on "slides," "deck," "presentation,"
  "PPT," or any .pptx request. Can receive pre-structured content from
  executive-slide-builder or metis-premier-proposal. Always validates output
  against metis-brand-identity. Do NOT use for: HTML/browser presentations
  (metis-html-slides); narrative reframing without file output
  (executive-slide-builder); PDF proposals (metis-premier-proposal);
  whitepapers (metis-whitepaper).
metadata:
  author: Metis Strategy
  version: 4.5.0
---

# PowerPoint Skill — Metis Strategy

## ⛔ STOP: FIRST ACTIONS FOR ANY NEW DECK (blocking gates)

**If the request is to build a NEW deck or new slides (Generation), your very
first actions, before any outline, plan, or build script, are:**

1. **Ask the §0.1 Speed Gate** (Design mode vs Fast mode) via `AskUserQuestion` and WAIT.
2. **Ask the §0.2 Intake** (deck type + real content vs. illustrative) and WAIT.

Both are mandatory. Present actual choices:

**§0.1 Speed Gate:**
- Design mode (per-slide pattern approval) vs Fast mode (auto-pick, review at end)

**§0.2 Intake:**
- **Pick a deck type** from the selector in `references/deck-presets.md`:
  Readout/leave-behind, Workshop/training, Presentation, BD/proposal,
  Current-state assessment, Exec/boardroom, or give custom dials. Each preset
  sets the density/variance dials, the structure, and where detail lives.
- **Confirm content:** do they have the real figures/names/dates, or is this a
  structural draft?

**In Cowork you MUST use the multiple-choice question tool
(AskUserQuestion), not plain prose.** In chat/code, ask inline and wait.

Both gates are mandatory **even if the brief already looks complete**. The user
may not know the dials or the design/fast fork exist, and silently defaulting
is the exact failure this skill exists to prevent. Do **not** generate a single
slide before the user answers both.

The only exceptions: (a) the user already stated a density/style preference, or
(b) the user explicitly says "use defaults / just build it", then proceed at
Fast mode as a **Readout/leave-behind** preset (Density 8 / Variance 6) and
state those assumptions in one line. **Editing** an existing deck (Section 1)
skips both gates.

---

## 0. Mode Gate

**Before doing anything else, determine which workflow to use.**

**Does an existing .pptx file need to be preserved?**

| Condition | Mode |
|-----------|------|
| User provides, attaches, or references an existing .pptx file (by path, filename, or description) | **Editing** → Section 1 |
| No existing file; user wants a new Metis-branded deck | **Generation** → Section 2 |

Examples:
- "Edit this deck" → **Editing**
- "Add slides to client_deck.pptx" → **Editing**
- "Update the content in proposal.pptx" → **Editing**
- "Use the Aflac template" → **Editing**
- "Take our proposal from last week and update it" → **Editing**
- "Build me a proposal deck" → **Generation**
- "Create a Metis pitch for Nationwide" → **Generation**
- "Make slides for the offsite" → **Generation**

**The test is simple: does a .pptx file exist that we need to preserve? If yes, use Editing. If no, use Generation.**

---

## 0.1 Speed Gate: ALWAYS ASK FIRST (mandatory, every invocation)

**Before any planning, library reads, build init, or code: ask the user one question via `AskUserQuestion`.** This fork sets process depth for the whole task. No exceptions, no skipping, regardless of phrasing in the trigger ("quick deck," "just build," "advanced," "impress them," caveman mode, ultracode mode, terse user prompts). Always ask.

**The question (verbatim):**

```
question: "How should I work on this deck?"
header:   "Build mode"
options:
  - label: "Design mode (recommended)"
    description: "I plan each content slide, surface 2-3 pattern candidates per slide with ASCII sketches, you pick, then I build. Slower, higher quality, you steer the visuals."
  - label: "Fast mode"
    description: "I pick patterns myself using the skill's library browse, build straight through, show you the result. Faster, no per-slide approval, you review at the end."
```

**Behavior after answer:**

| Answer | Build init (§2.5 Phase 1.0) | Pattern Confirmation Gate (Design mode only: confirm the chosen pattern/layout per slide before Phase 2 build) | Outline table Status column |
|---|---|---|---|
| Design mode | Run in full | Run in full, per-slide inline markdown batches | Required; all rows must reach `confirmed` before Phase 2 |
| Fast mode | Run in full (still mandatory) | Skipped entirely | Optional; agent fills `Chosen` directly, logs one-line autopick rationale per slide in chat |

**Hard rules:**

1. **This gate is a tool call, not a vibe.** If `AskUserQuestion` has not been called with the Build-mode question, the gate has not run. Do not proceed to intake, outline, build init, or any other step.
2. **Trigger phrasing never authorizes a skip.** "Just build it," "be quick," "advanced deck," "impress them," "fast," caveman mode, ultracode mode. None of these substitute for the user's explicit pick. Speed preference in surrounding chat is not a Fast mode selection. Ask anyway.
3. **Skipping any other mandatory step does NOT authorize skipping this one.** Each mandatory step is independent.
4. **If the user dismisses the question:** stop. Do not infer a default. Wait for explicit instruction.
5. **Re-entry:** if the user later says "actually let me pick the patterns" mid-Fast-mode build, switch to Design mode for remaining slides. For each unbuilt row, confirm the chosen pattern/layout with the user before building it.

**Why this gate exists.** Without an explicit fork, the model reads ambient signals and rationalizes skipping the per-slide gate to match perceived user tempo. That produces decks the user can't steer until after rebuild. Forcing the fork up front makes the trade-off the user's choice, not the model's inference.

**Sequence after Speed Gate:** Speed Gate (§0.1) → Intake (§0.2, deck type + dials) → Build init → Outline → Pattern Confirmation Gate (Design mode only: confirm the chosen pattern/layout with the user for each slide before building it) → Phase 2 build.

---

## 0.2 Intake: ask before building (do not skip)

Before generating a new deck (or a fresh set of slides), if the user has not
already specified these, **ask once, then build.** Do not silently assume the
defaults, surface them and let the user adjust. In Cowork, use the
multiple-choice question UI; in chat or code, ask inline. Keep it to one short
round, then proceed.

Ask:

1. **Deck type (the selector).** Have the user pick one preset from
   `references/deck-presets.md`. Each one sets the dials, the structure, and
   where detail lives:
   - *Readout / leave-behind* (D 8 / V 6), final deliverable, read without a presenter.
   - *Workshop / training* (D 7 / V 5), run a session; pre-read + live activities.
   - *Presentation* (D 5 / V 5), projected live working session.
   - *BD / proposal* (D 5 / V 6), win the work.
   - *Current-state assessment* (D 8 / V 6), evidence-heavy findings and maturity.
   - *Exec / boardroom* (D 2 / V 3), one decision per slide, depth in notes.
   - *Custom*, let the user give Density/Variance numbers directly.
2. **Real content vs. illustrative.** Ask whether the user has the actual
   figures, findings, names, and dates to use, or wants a structural draft.
   State plainly that **without real specifics the deck will read generic**, and
   offer to list exactly what you need (the numbers, the names, the dates). This
   is the single biggest driver of whether the output looks human.
3. **Only if still unclear:** audience and length.

After the user picks a preset, **read its section in `references/deck-presets.md`**
and follow its structure, dials, and detail-location rule. If the user says
"just build it" or "use your defaults," proceed as a **Readout/leave-behind**
(D 8 / V 6), work from whatever specifics are in the prompt, and **state both
assumptions in one line** before building. Never block on the questions, ask
once, then move.

---

## 0.3 Design dials (set before building; default for consulting work)

Two dials govern the *feel* of the deck. Read them before planning, and let the
user override either in their prompt ("make it cleaner / airier / busier").

| Dial | 1 | 10 | **Default for client deliverables** |
|---|---|---|---|
| **VARIANCE** (layout regularity) | perfectly symmetric, centered, equal columns | asymmetric, offset, irregular weighting | **6**, favor asymmetry and clear hierarchy over tidy equal grids |
| **DENSITY** (information per slide) | one idea, lots of white space, big type | packed: tables, multi-row frameworks, small type | **7**, a working deliverable, not a marketing slide |

Why the defaults are set high: AI decks default to ~VARIANCE 2 / DENSITY 3
(centered, sparse, big type), which is exactly the "marketing slide / AI slop"
look. Real Metis deliverables run dense and asymmetric. **Unless the user asks
for clean/airy, build at VARIANCE 6 / DENSITY 7.** A title slide or a single
pull-quote is the rare DENSITY-2 exception, not the norm.

What the dials change in practice:

- **DENSITY 7** means: a content slide usually carries a real table, a labeled
  diagram, or a 4-7 row framework with 10-11pt text, not 3-4 padded cards. If a
  slide has only one idea and a lot of empty space, it is under-built.
- **VARIANCE 6** means: weight content to one side, use a dominant element plus
  supporting detail, vary slide-to-slide structure. Avoid the reflexive
  centered, equal-column grid.

---

## 0.5 What a content slide actually needs, and what it does not

A Metis content slide needs exactly three things: a **title**, a **body that
carries real content**, and the **brand frame** (logo, page number, green
arrow, inherited from the layout). Everything else is an option you reach
for when the content calls for it, not a slot you fill every time.

This is a deliberate change from the older "every slide has the same five
slots" rule. Uniform slide structure is the single biggest reason AI-built
decks get recognized on sight: when every slide opens with an italic subtitle
and closes with a navy mantra bar, the deck announces that a machine made it.
Real Metis decks do not do this. In the LiveRamp final deliverable (53
slides), the bottom takeaway bar appears on **zero** slides, and the "so-what"
lives in the *title*, not a subtitle.

| Element | Status | When to use it |
|---|---|---|
| **Title** | Required | Always. Prefer a full-sentence claim that carries the so-what ("Evolving the AI operating model from ad hoc to hub-and-spoke"), not a bare label ("Operating Model"). |
| **Body** | Required | Always. Real content: numbers, names, dates, specifics. See §0.7. |
| **Brand frame** | Required | Always. Inherited from the layout. Never re-draw it. |
| **Subtitle / subhead** | Optional | Only when the title cannot hold the whole so-what. Use the layout's built-in Subhead placeholder (idx 14), styled as a short claim, not gray italic hedging. Many slides need none. |
| **Takeaway / kicker** | Rare | At most on a section-opener or a conclusion slide, and vary the form: a strong title, a left-margin kicker, a one-line footer. Do **not** put a navy mantra bar on every slide. |
| **Source line** | Encouraged | Whenever a slide states data, an external fact, or a research-backed claim, add a small "Source: ..." line at the bottom. In the LiveRamp deck, 27 of 53 slides cite a source. A visible source is one of the strongest signals that a human analyst built the slide. |

The test is no longer "did I write a mantra." It is: does every element on
this slide carry a specific, real piece of content, and would this slide look
out of place sitting next to the one before it? If two adjacent slides share
the same structure and density, change one of them (see §0.7).

The brand frame, title placeholder, and footer all come from the template's
slide layouts. Never re-draw them.

---

## 0.5.1 Design paths: native template layouts first

Before §0.6's hand-built paths, there is now a **primary path**: the
template's own built-in slide layouts. The 2025 Metis template ships **32
named layouts**: `Comparison`, `Three Content w/ Heading`, `Four Content
w/ Heading`, `Four Content Process`, `Icon box Four/Six Content`, `Content
with Caption`, `Two/Three Content Speaker Image`, `Four Content - 4 Photo`,
`Four Content Quote`, `Quote Rows`, `One Chart or Table`, `Three Chart`, plus
covers and dividers. They are human-designed, already on-brand, and varied.
The full catalog with placeholder maps is in
[`references/metis-layouts.md`](references/metis-layouts.md).

**Why this is the primary path:** the loudest "AI deck" tell is that every
slide is a hand-drawn rounded card with a mint accent bar, because the old
workflow used only `1_Title Only` + `Blank` and re-drew everything else in
python-pptx. Real consultants use the template's layouts; the LiveRamp deck
spans about ten of them. Driving content through native layouts gives you
variety and brand fidelity for free, and is far less brittle than freehand
shapes.

**Path choice is driven by what the content IS, not by a fixed default:**

First classify the slide:

- **Relationship / structure / concept**: anything where items *relate*
  (depend on, feed, surround, sit on top of, flow into, trade off against each
  other). Examples: a shared platform many functions draw on; a maturity
  progression; an operating-model evolution; a hub and its spokes.
  → **Lead with a diagram or metaphor** (Timesaver §0.6 Path B, or a bespoke
  diagram). A picture that *encodes the relationship* is the human move and
  beats any card grid. This is where AI decks fail worst: they flatten a
  relationship into N equal cards. Do not.

- **Flat enumeration**: genuinely parallel, independent items of equal weight
  with no relationship between them (e.g., four unrelated workstreams, a list of
  deliverables). → A **native template layout** (`references/metis-layouts.md`)
  is the cleanest path.

- **Data / evidence**: figures, comparisons, scorecards. → A **table or chart**
  (native `One Chart or Table` / `Three Chart`, or a hand-built table). Dense
  tables are good (DENSITY 7), not something to avoid.

Then build with the matching tool:

1. **Diagram / metaphor** (Timesaver §0.6 Path B, or bespoke from
   `metis-brand.md` primitives), for relationship/structure/concept slides.
2. **Native template layout** (`references/metis-layouts.md`), for flat
   enumeration and data slides.
3. **Component recipe** (`patterns.md` + `metis-brand.md`), only when neither
   fits and you must hand-build.

Path choice is driven by content type, not a fixed default: relationship or
concept slides get a diagram or metaphor (e.g., a "shared-foundation"
relationship becomes a foundation diagram, not four equal cards); native
layouts are for flat enumeration; tables and charts are for data. Either way,
the brand frame and palette stay fixed.

---

## 0.6 Concept-to-Shape: hand-built paths (after native layouts)

> **These are the hand-built fallback paths.** Try a native template layout
> first (§0.5.1, `references/metis-layouts.md`). Use the two paths below only
> when no native layout fits the content. When both are in play, the choice
> between them is as described here.

When hand-building, slide design has **two co-equal paths**, both grounded in
the same brand system (`metis-brand.md`). Choose per slide based on what the
content needs; neither path is the default or the fallback for the other:

- **Path A — Component recipes** (`references/patterns.md` + `references/metis-brand.md`)
  36 brand-agnostic component patterns with exact python-pptx code recipes.
- **Path B — Timesaver visual library** (this section)
  260 pre-designed slide structures spanning every chart type, framework,
  and narrative arc Metis Strategy uses. Catalog:
  [`references/timesaver_index.md`](references/timesaver_index.md).

Both paths use the same colors, fonts, master, and frame. The decision is
structural: does this content live naturally in cards/columns/boxes, or
does the *shape* itself express the thought?

### How to choose between the paths

Path A (`patterns.md`) and Path B (Timesaver) are **co-equal candidate libraries** —
neither is the default, neither is the fallback. Every content slide is a
candidate for either, and the right choice depends on what the slide's
structural relationships actually require.

The choice is not made by reading the slide title and pattern-matching keywords.
It's made by **looking at candidates from both libraries** against the slide's
articulated structural needs, and picking the one that fits best. If you find
yourself deciding "this is enumeration, so Path A" without ever loading a
Timesaver PNG, you've shortcut the choice.

Operationally, this means every content slide goes through:

1. **Articulate structural needs** from the slide content. (Done before any
   candidates are surfaced — see §2.5 Phase 1, "Structural needs first.")
2. **Browse both libraries** for candidates against those needs. patterns.md
   is read in full at build init; Timesaver candidates are loaded as PNGs via
   the multimodal Read tool. (See §0.6.1 for the worked example.)
3. **Pick** the candidate that best matches the locked needs. Either path is
   a legitimate winner — the rationale ties back to the needs, not to a
   preference for one library.

**Why both paths get equal weight:** patterns.md is faster to build with for
content that's genuinely card-shaped or column-shaped. Timesaver structures
carry meaning the components can't — a hub-and-spoke says something about
relationships, a house says something about dependencies. If you only consult
patterns.md, you produce slides that look right but miss the structural
metaphor. If you only consult Timesaver, you force shapes onto content that
doesn't need them. Browse both, every time.

**Bespoke metaphor** is the third option for content that doesn't fit either
library — see "Universal Closers & Metaphor Primitives" in `metis-brand.md`.
This is the fallback, not a default; it requires an explicit rationale that
neither library fits.

### Path B assets

The catalog ships in this skill:
[`references/timesaver_index.md`](references/timesaver_index.md) — 260 rows
with hand-written "Use when..." triggers.

PNG previews live on the shared drive:

`G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\timesaver_pngs\slide-{N}.png`

Every Metis machine has the G:\ drive mapped, so the path resolves
identically for everyone — no per-user setup, no rendering, no caching.

**Requirements:** Read access to `G:\Shared drives\Knowledge Management\New Brand Assets\` (default for all Metis staff).

### The thought-to-shape browse

1. **Read** [`references/timesaver_index.md`](references/timesaver_index.md). Scan the **"Use when..."** column. Find rows that match the thought.
2. **Load 2-4 candidate previews** via the multimodal Read tool from the shared-drive path above (slide-{N}.png for each candidate row).
3. **Pick the winner.** Then write python-pptx code that reproduces the layout — using the brand tokens from `metis-brand.md` (colors, fonts, master, margins).

**Examples of thought → shape:**

| Thought | Shape | Catalog ref |
|---|---|---|
| Three layers, each depending on the one below | **House** (foundation → body with pillars → roof) | slide 179 |
| Six things that reinforce each other | **Honeycomb / hex flywheel** | slide 155 |
| Three units forming a unified whole | **Triangle concept** | slide 160 |
| Now → near → far progression | **Linear process / chevron flow** | slide 114 |
| One center radiating to many capabilities | **Hub-and-spoke** (e.g., McKinsey 7-S) | slide 200 |
| Branching decision logic | **Decision tree** | slide 130 |
| Narrowing stages from broad to specific | **Funnel** | slide 167 |
| Two states being compared | **Comparison chart** or **Before/After** | slide 175 |

If neither path fits the thought, build a **bespoke metaphor** from
primitives (triangles, hexagons, chevrons, pillars). See `metis-brand.md`
"Universal Closers & Metaphor Primitives."

## 0.6.1 Worked example — both paths considered

The browse described above is a sequence of concrete tool calls in the
conversation, not an abstract recommendation. Below is what it looks like
end-to-end for one slide. Reproduce this shape for every content slide.

**Slide spec (generic):**

> "Build a content slide titled *Three layers of platform capability*. The slide
> describes a foundation layer, a middle services layer, and a top experience
> layer — each layer depends on the one below."

**Step 1 — Articulate structural needs from the content.**

Before surfacing any candidates, write the structural requirements. These are
content-derived, not library-derived:

- *Three discrete layers, stacked.*
- *Each layer depends on the layer below.*
- *Foundation is widest / most fundamental; top is narrowest / most user-facing.*

These are the locked criteria. The candidate that wins must match them.

**Step 2 — Surface candidates from both libraries.**

From `patterns.md`: a stacked-card layout (#9 Cards+Header, three rows) could
plausibly fit. Component is in conversation context already (patterns.md was
read at build init).

From `timesaver_index.md` (the "Concept slides — metaphors" section):
candidates include:

- `slide-179` (House chart) — "layered architecture (foundation → body → roof)"
- `slide-159` (Pyramid concept) — "broad base narrowing to a peak"
- `slide-185` (Level diagram) — "discrete graduated levels"

Load the candidate PNGs via the multimodal Read tool:

```
Read("G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\timesaver_pngs\slide-179.png")
Read("G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\timesaver_pngs\slide-185.png")
```

(House and Level Diagram are the closest matches to the locked needs;
Pyramid is a weaker match because the content doesn't imply narrowing.)

**Step 3 — Pick against the locked needs.**

`slide-179` (House) carries all three structural needs: stacked layers,
dependency (the body depends on the foundation, the roof depends on the body),
and the foundation-widest visual logic.

`slide-185` (Level Diagram) carries layers and graduated tiers, but the
dependency relationship is implicit and weaker.

`patterns.md #9` (Cards) carries layer enumeration but not dependency. The
cards sit side by side or in a grid — they don't structurally show one
depending on another.

**Pick: `timesaver slide-179` (House).** Rationale ties back to locked needs:
*"slide-179 is the only candidate that carries layered + dependency + foundation-widest visual semantics. The other candidates require external annotation to communicate dependency, which the House metaphor does intrinsically."*

**Step 4 — Reproduce the layout.**

Reproduce slide-179 in python-pptx using brand tokens from `metis-brand.md`.
Don't freehand the layout from memory; the candidate PNG is in conversation
context — refer to it for shape positions, hierarchy, label placement.

---

**Anti-patterns — what this workflow done wrong looks like:**

- **No PNG load.** Citing `timesaver slide-179` in the plan without ever
  calling the Read tool on the corresponding PNG. The citation is unverifiable
  and the build will be a freehand approximation, not a reproduction.
- **Single-library browse.** Considering only Timesaver candidates and
  ignoring patterns.md, or vice versa. Both libraries get loaded at build
  init; both get evaluated against the locked needs.
- **Reverse-engineered needs.** Articulating structural needs after the
  candidate is already chosen, so the needs conveniently match the pick.
  The Write of needs comes before the candidate Reads; the conversation log
  shows the order.
- **Generic rationale.** "House looks better" or "this fits the brand" — the
  rationale must reference specific structural needs and explain why the
  pick carries them better than the alternative.

---

## 0.7 Bias correction and pre-flight (read before every build)

The brand should be recognizable. *Claude* should not. LLMs have a strong
statistical pull toward a specific "deck-builder" look: centered, sparse,
big-type slides built from rounded cards with a colored accent bar, a number
chip, a hero stat, and one idea per card. That look is the slop. This section
names each bias and forces the human alternative. **Intentionality is the rule:
a container, a color, or a big number is allowed only when it carries meaning.**

### Bias 1: Cards by default (the "system-UI" tell)

The strongest visual tell is that the slide looks like an app dashboard: every
block is a rounded card with a colored edge bar and a numbered chip. Humans
building a strategy slide do not think in UI components.

- **Use a card (filled/outlined box) only when the box carries meaning**:
  elevation/grouping that genuinely separates content. Otherwise group with a
  **thin rule (`border-t` equivalent), a divider line, or plain whitespace**, as
  in the human "Key Recommendations" slide (icon + label + bullets in plain
  ruled rows, no cards).
- **No decorative edge accent bars.** A colored bar on the side of a box that
  means nothing is pure UI styling. Drop it.
- **No `01 / 02 / 03` number chips** as a default device. Number only when
  sequence matters (steps), and then plainly.
- **Even-column card grids (3-up / 4-up) are the exception, not the spine.** At
  most one per ~5 content slides, and only for true flat enumeration (§0.5.1).

### Bias 2: Relationships flattened into cards

When items *relate* (depend on / sit on / feed / surround), AI lists them as N
equal cards. The human move is a **diagram that encodes the relationship**
(foundation supporting consumers, hub and spokes, a progression). See §0.5.1:
lead conceptual slides with a diagram, not a grid.

### Bias 3: Low density (the marketing-slide tell)

AI defaults to one idea and lots of air. Build at **DENSITY 7** (§0.3): a
content slide usually carries a real table, a labeled diagram, or a 4-7 row
framework at 10-11pt. If a slide holds one idea and white space, it is
under-built; add the evidence, the detail, the next level down.

### Bias 4: Hero stats and decoration over substance

- **No giant hero numerals in a colored panel** (the `14 / 5 / 0` infographic
  device). State numbers inside a sentence, a small stat line, or a table.
- **Organic, real numbers.** `47.2%`, `$3.4M`, `Wave 1/2/3`, real system and
  team names, not round fakes (`50%`, `99.9%`) or generic placeholders
  ("Acme", "John Doe", "Function A").
- **Color encodes information, never decoration.** Accent color marks a
  current-vs-target, a category, a highlight that *means* something. If the
  color carries no information, it should not be there. The brand palette and
  frame stay fixed; this rule is about the *accent* choices on top of them.

### Bias 5: Typography and copy tells

- **Three or more distinct text sizes** per content slide; control hierarchy
  with weight and color, not one giant size. Avoid the oversized H1 that screams.
- **Put the so-what in the title** (a full sentence). Subtitle only when the
  title cannot hold it; never gray-italic hedging by reflex.
- **No em dashes** in slide copy (use commas, periods, parentheses, colons).
  **No colon-label house style** ("Challenge:/Why:"). **No triadic mantras**
  ("One team. One platform. One future."). **No filler verbs** (Elevate,
  Seamless, Unleash, Next-Gen); use concrete verbs.

### Working-document texture (do this, do not fake it)

- Add a small gray **`Source: ...` line** whenever a slide states data or a
  research claim (normal in real Metis decks: 27 of 53 LiveRamp slides).
- Keep honest markers where real: a `WIP` flag on a draft, a `v1` label, an
  "illustrative" note on a genuinely illustrative figure, but do **not**
  auto-stamp "illustrative / non-exhaustive" on every slide.

### Hard pre-flight checklist (every content slide must pass before saving)

```
[ ] DENSITY: carries a table, diagram, or 4-7 row framework, not 3-4 padded cards
[ ] RELATIONSHIP: relational content is a diagram, not a grid of equal cards
[ ] CARDS: every box earns its box (grouping/elevation); else ruled rows / whitespace
[ ] NO decorative accent bars, no 01/02 number chips, no hero-stat panel
[ ] COLOR: every accent color encodes something; brand frame + palette intact
[ ] TYPE: 3+ distinct text sizes; so-what is in the title; no reflex subtitle
[ ] CONTENT: real, organic specifics (numbers/names/dates); no round fakes or placeholders
[ ] SOURCE: a source line is present if the slide makes a data/research claim
[ ] COPY: no em dashes, no colon-label template, no triadic mantra, no filler verbs
[ ] VARIETY: not structurally identical to the previous slide
[ ] TAKEAWAY BAR: absent (allowed only on a rare section-open/close)
```

If a slide fails any line, fix it before moving on. Render and visually inspect
(Section 3); these tells are obvious in the image and easy to miss in code.

---

## 1. Editing Workflow

Use this workflow when an existing .pptx file is provided or referenced. This workflow
preserves the template's layouts, themes, formatting, and brand identity.

### 1.1 Python Environment

> **Python is installed but NOT on the git bash PATH.** Use the full path:
> ```bash
> PYTHON="C:/Users/$USER/AppData/Local/Programs/Python/Python312/python.exe"
> ```
> **Required packages:** `python-pptx`, `defusedxml`, `lxml`, `Pillow`, `pywin32`, `markitdown`
> **Do NOT** loop trying to install Python or add it to PATH. It is already installed.

All script paths below are relative to this skill's directory. Locate it with:
```bash
SKILL_DIRS=(
    "$HOME/.metis/skills/.agents/skills/tessl__metis-pptx"
    "$HOME/.metis/skills/.tessl/tiles/metis-strategy/metis-pptx"
    ".tessl/tiles/metis-strategy/metis-pptx"
)
for d in "${SKILL_DIRS[@]}"; do
    if [ -d "$d/scripts" ]; then SKILL_DIR="$d"; break; fi
done
```

### 1.2 Analyze the Existing Deck

Before making any changes, understand the deck:

```bash
# Visual overview — exports each slide as a PNG image
"$PYTHON" "$SKILL_DIR/scripts/visual_qa.py" input.pptx slide_images/

# Text content extraction
"$PYTHON" -m markitdown input.pptx
```

Review the exported slide images and extracted text to understand:
- How many slides exist and their order
- What layouts are used
- Where content lives on each slide
- The deck's visual style and brand

### 1.2.1 Slide-by-Slide Triage

After analyzing the deck, classify every slide into one of three categories **before making any changes**:

| Category | When to use | Action |
|----------|------------|--------|
| **Keep & Edit** | The slide's visual layout matches the new content structure (same number of items, same hierarchy, similar text lengths) | Edit text in place via XML |
| **Duplicate & Rebuild** | The slide's layout/grid is right but the content structure differs significantly (different number of items, different hierarchy, much longer/shorter text) | Duplicate the slide, strip content, rebuild using the layout's placeholders and shapes as a skeleton |
| **New Slide** | No existing slide has a layout that fits the new content, OR the source slide's visual structure is fundamentally incompatible (e.g., a manufacturing Gantt chart being reused for a strategic capability overview) | Create a new slide from a layout using `add_slide.py` with a `slideLayout`, then build content using patterns from `references/patterns.md` with extracted brand tokens |

**A slide is NOT reusable when:**
- It has a specialized visual structure (timeline, Gantt, matrix, process flow) that doesn't map to the new content's logical structure
- The source has N items but the new content has a significantly different count (e.g., 6 manufacturing stages vs. 3 strategic themes)
- It contains positioned shapes (arrows, connectors, icons) whose placement depends on the original content's meaning
- Replacing the text would require most items to be significantly longer or shorter than the originals, causing overflow or empty space

**A slide IS reusable when:**
- It's a standard layout (title + bullets, title + 3-column, section divider)
- The new content has the same number of items in the same visual hierarchy
- Text lengths are roughly comparable (within ~30% character count)
- The visual metaphor still applies (e.g., Start/Win/Stay chevrons work for both divisions)

Write out the triage as a table in your plan before starting any edits:

```
| Slide # | Current Content | New Content | Category | Rationale |
|---------|----------------|-------------|----------|-----------|
| 1 | PSG Title | CTD Title | Keep & Edit | Same layout, just text swap |
| 9 | Data & AI Timeline | Labeling Transformation | New Slide | Timeline axis doesn't apply; empty boxes |
| 15 | PSG Gantt Roadmap | CTD Roadmap | New Slide | Granular Gantt doesn't fit higher-level view |
```

### 1.3 Extract Brand Tokens (Non-Metis Decks)

If the deck is NOT Metis-branded, extract the client's brand tokens:

```bash
"$PYTHON" "$SKILL_DIR/scripts/extract_brand.py" input.pptx
```

This outputs a JSON dict with:
- **colors:** primary fills, text colors, accents
- **fonts:** title font, body font, caption font (with sizes)
- **content_area:** left, top, right, bottom boundaries
- **layouts:** all available slide layouts and which are used

Use these tokens when creating new slides so they match the client's style.

### 1.4 Unpack

Extract the .pptx for editing:

```bash
"$PYTHON" "$SKILL_DIR/scripts/unpack.py" input.pptx unpacked/
```

This extracts all XML files, pretty-prints them, and escapes smart quotes.

### 1.5 Structural Changes

**Complete ALL structural changes before editing content.**

**Duplicate a slide:**
```bash
"$PYTHON" "$SKILL_DIR/scripts/add_slide.py" unpacked/ slide2.xml
# Prints: Created slide5.xml from slide2.xml
# Prints: Add to presentation.xml <p:sldIdLst>: <p:sldId id="259" r:id="rId8"/>
```

**Create a slide from a layout:**
```bash
# See available layouts:
ls unpacked/ppt/slideLayouts/
"$PYTHON" "$SKILL_DIR/scripts/add_slide.py" unpacked/ slideLayout2.xml
```

**Delete a slide:** Remove its `<p:sldId>` from `<p:sldIdLst>` in `unpacked/ppt/presentation.xml`.

**Reorder slides:** Rearrange `<p:sldId>` elements in `<p:sldIdLst>`.

After adding slides, **update `presentation.xml`** by inserting the printed `<p:sldId>` element at the desired position in `<p:sldIdLst>`.

### 1.5.1 Safe Slide Deletion

Deleting slides requires cleanup beyond just removing the `<p:sldId>` entry. Follow this sequence:

1. **Remove the `<p:sldId>` element** from `<p:sldIdLst>` in `presentation.xml`
2. **Delete the slide XML file** (`ppt/slides/slideN.xml`)
3. **Delete the slide's .rels file** (`ppt/slides/_rels/slideN.xml.rels`)
4. **Remove the relationship entry** from `ppt/_rels/presentation.xml.rels` (the `<Relationship>` with the matching `rId`)
5. **Remove the Content-Type override** from `[Content_Types].xml` (the `<Override>` for `/ppt/slides/slideN.xml`)
6. **Run `clean.py`** to catch any remaining orphaned media, notes, or references

**Never delete slides using python-pptx's internal API** (`drop_rel()`, `sldIdLst.remove()`, etc.) — this leaves orphaned references that corrupt the file and make it unopenable in PowerPoint. Always delete via the unpacked XML approach above, then run `clean.py` before `pack.py`.

If you need to remove many slides and the XML approach is impractical, use **PowerPoint COM** to delete properly:
```python
import subprocess, win32com.client
was_running = "POWERPNT.EXE" in subprocess.check_output(
    ["tasklist", "/FI", "IMAGENAME eq POWERPNT.EXE", "/NH"],
    stderr=subprocess.DEVNULL, text=True)
ppt = win32com.client.DispatchEx('PowerPoint.Application')
pres = ppt.Presentations.Open(path, WithWindow=False)
for idx in sorted(indices_to_delete, reverse=True):
    pres.Slides(idx).Delete()
pres.Save()
pres.Close()
if not was_running:
    ppt.Quit()
```
COM handles all internal cleanup (relationships, content types, notes) automatically.

### 1.6 Edit Content

For each slide classified as "Keep & Edit" in triage (Section 1.2.1):

1. Read the slide XML: `unpacked/ppt/slides/slide{N}.xml`
2. Identify ALL content elements — text runs, images, charts
3. Replace each element with final content

**Use the Edit tool, not sed or Python scripts.** The Edit tool forces specificity.

#### 1.6.1 Content Authoring vs. Text Replacement

**This is NOT a find-and-replace exercise.** You are authoring new content that happens to live in an existing visual container. The distinction matters:

- **Text replacement** (wrong): "Find 'PSG' and replace with 'CTD' everywhere" — this misses context, leaves orphaned metrics, and produces hybrid content where some values are from the source deck and others are new
- **Content authoring** (right): Read each shape, understand what it communicates in the source deck, then write the equivalent new content from scratch using the target source materials

For every text shape you edit:
1. Read the source text and understand its **purpose** (is it a metric? a capability description? a label?)
2. Write the **new content from the target source materials**, not by modifying the source deck's text
3. Verify the new text fits the container (similar character count, similar line count)
4. Verify all quantitative values come from the target data, not leftover source numbers

#### 1.6.2 Formatting Preservation

When replacing text in XML, preserve the original formatting by keeping the `<a:rPr>` (run properties) element intact and only changing the `<a:t>` (text) element. If a shape has multiple runs with different formatting (e.g., a bold red label followed by regular black description), maintain that run structure.

**Common formatting failures to avoid:**
- Replacing a multi-run paragraph with a single run (loses inline formatting like bold labels)
- Changing text in a bulleted list without preserving `<a:buChar>` or `<a:buAutoNum>` on each `<a:pPr>`
- Writing longer text into a fixed-size shape without checking for overflow
- Clearing a text frame and rebuilding it (loses paragraph-level formatting like spacing, alignment, indentation, bullet style)

**When the new content has different structure than the old** (e.g., 3 bullets to 5 bullets), you must add or remove `<a:p>` elements. Copy the `<a:pPr>` (paragraph properties) from an existing paragraph to maintain consistent bullet style, indentation, and spacing.

### 1.7 Adding New Slides to Client Decks

When you need to create new slides that match the client's style:

1. **Read `references/patterns.md`** to pick the right grid pattern and component patterns
2. **Use the extracted brand tokens** (from step 1.3) for colors, fonts, and spacing
3. **Build the slide** using the client's coordinates and palette — NOT the Metis hardcoded values

For Metis-branded decks being edited, you may reference `references/metis-brand.md` for the code recipes.

### 1.7.1 Hybrid Workflow: Editing + Generation

Most real-world editing tasks are **hybrid**: some slides are edited in place, others need to be built from scratch. This is expected and correct — do not force every slide through the same workflow.

After completing triage (Section 1.2.1), you will typically have:
- **Keep & Edit slides** — process via the XML editing workflow (Sections 1.4-1.6)
- **New Slides** — process via a generation-like workflow but using the **client's brand tokens** instead of Metis brand constants

For New Slides in a client deck:
1. Create the slide from a layout: `"$PYTHON" "$SKILL_DIR/scripts/add_slide.py" unpacked/ slideLayoutN.xml`
2. Choose the right component pattern from `references/patterns.md`
3. Build the slide content using **extracted brand tokens** (colors, fonts, spacing from Section 1.3)
4. Write the content shapes into the new slide's XML using the Edit tool
5. Insert the `<p:sldId>` at the correct position in `presentation.xml`

**Key principle:** A deck that mixes edited originals with well-crafted new slides (using the same brand tokens) will look more cohesive than a deck where every slide is force-fit via text replacement into layouts that don't match the content.

When building new slides for a client deck, adapt the python-pptx component recipes from `references/metis-brand.md` by substituting the client's brand tokens for the Metis constants:
- Replace `DARK_NAVY` with the client's `primary_fill` color
- Replace `Calibri` with the client's `primary` font
- Replace Metis margins with the client's `content_area` boundaries

### 1.7.2 Build → Render → Inspect → Iterate → Inject (Surgical Single-Slide Editing)

Use this workflow when you need to **add a small number of new slides to an
existing deck without disturbing any prior slide**. It isolates new
construction in a sandbox file, forces visual review, and uses PowerPoint's
own `Slides.InsertFromFile` for the final commit — which preserves the
source master so brand framing carries over cleanly.

**Step 1 — Build the new slides in a separate sandbox file.**
- Start the sandbox from `master.pptx` (so the brand frame is inherited).
- Add only the new slides, picking shapes from the Timesaver library
  (see §0.6) or building bespoke metaphors from primitives.
- Save the build script as a reproducible Python file (e.g., `build_new_slides.py`).

**Step 2 — Render the new slides to PNG via PowerPoint COM.**
```python
import subprocess, win32com.client
was_running = "POWERPNT.EXE" in subprocess.check_output(
    ["tasklist", "/FI", "IMAGENAME eq POWERPNT.EXE", "/NH"],
    stderr=subprocess.DEVNULL, text=True)
ppt = win32com.client.DispatchEx("PowerPoint.Application")
ppt.Visible = 1
pres = ppt.Presentations.Open(SANDBOX_PATH, WithWindow=False)
for idx in NEW_SLIDE_INDICES:
    out = f"renders/slide-{idx}.png"
    pres.Slides(idx).Export(out, "PNG", 1920, 1080)
pres.Close()
if not was_running:
    ppt.Quit()
```

**Step 3 — Inspect each PNG via the multimodal Read tool. Iterate.**
- Read each PNG. Look for overlap, overflow, low-contrast, alignment issues
  (see §3.4 checklist).
- Fix the build script and re-render. The first render is almost never correct.
- Do not skip this step. Visual review must happen *before* you touch the
  target deck.

**Step 4 — Inject into the target deck via `Slides.InsertFromFile`.**
```python
import shutil, subprocess, win32com.client

# Always back up the target first
shutil.copyfile(TARGET, TARGET + ".bak_preInsert.pptx")

was_running = "POWERPNT.EXE" in subprocess.check_output(
    ["tasklist", "/FI", "IMAGENAME eq POWERPNT.EXE", "/NH"],
    stderr=subprocess.DEVNULL, text=True)
ppt = win32com.client.DispatchEx("PowerPoint.Application")
pres = ppt.Presentations.Open(TARGET, WithWindow=False)
# Slides.InsertFromFile(FileName, Index, SlideStart, SlideEnd)
#   Index = position AFTER which the new slides should appear
#   SlideStart..SlideEnd = source slide numbers (inclusive)
# Example: source slide 2 inserted after target position 5 → becomes new slide 6
pres.Slides.InsertFromFile(SANDBOX, 5, 2, 2)
pres.Save(); pres.Close()
if not was_running:
    ppt.Quit()
```

**Why this works:** `InsertFromFile` preserves the **source master** on the
inserted slides. As long as the sandbox uses Metis `master.pptx` branding,
the inserted slides land in the target with full Metis formatting — no XML
rewriting, no risk of corrupting prior slides, no re-doing brand tokens.

**Position math (the trap to avoid):** after each insert the deck shifts.
If you want final positions 6, 10, 11, the second `InsertFromFile`'s `Index`
value must be computed against the **post-insert-1 deck**, not the original.
Always print slide titles before/after each insert to verify positions.

### 1.8 Formatting Rules for XML Editing

- **Bold all headers, subheadings, and inline labels:** Use `b="1"` on `<a:rPr>`
- **Never use unicode bullets (•):** Use proper list formatting with `<a:buChar>` or `<a:buAutoNum>`
- **Multi-item content:** Create separate `<a:p>` elements for each item — never concatenate into one string
- **Smart quotes:** When adding new text with quotes, use XML entities:
  - Left double quote: `&#x201C;`
  - Right double quote: `&#x201D;`
  - Left single quote: `&#x2018;`
  - Right single quote: `&#x2019;`
- **Whitespace:** Use `xml:space="preserve"` on `<a:t>` with leading/trailing spaces

### 1.9 Template Adaptation Rules

- When source content has **fewer items** than the template: remove excess elements entirely, don't just clear text
- When replacing text with **longer content**: may overflow — test with visual QA
- When replacing text with **shorter content**: usually safe
- **Template slots ≠ source items:** If template has 4 items but you only need 3, delete the 4th group entirely

#### Overflow Decision Tree

Before committing a text replacement, compare the character count of old vs. new content:

| New vs. Old Length | Risk | Action |
|-------------------|------|--------|
| Within ~30% | Low | Replace and verify in QA |
| 30-60% longer | Medium | Replace, but check the shape has `wordWrap` and adequate height. Consider abbreviating. |
| >60% longer | High | Do NOT force-fit. Either abbreviate the content, or classify this slide as "New Slide" in triage and rebuild with a layout that fits. |
| Significantly shorter | Low | Replace, but remove any excess visual elements (extra bullet markers, connector lines) that now point at empty space |

**Never rely on PowerPoint's auto-shrink** (`<a:bodyPr fontScale="...">`) to handle overflow. If the text doesn't fit at the original font size, the slide needs redesign, not font shrinking.

### 1.10 Clean + Pack

```bash
"$PYTHON" "$SKILL_DIR/scripts/clean.py" unpacked/
"$PYTHON" "$SKILL_DIR/scripts/pack.py" unpacked/ output.pptx --original input.pptx
```

`clean.py` removes orphaned slides, media, and relationships.
`pack.py` validates, condenses XML, and repacks with auto-repair.

### 1.11 Visual QA

```bash
"$PYTHON" "$SKILL_DIR/scripts/visual_qa.py" output.pptx qa_images/
```

See Section 3 for the full QA process.

---

## 2. Generation Workflow

Use this workflow when building a new Metis-branded deck from scratch.

### 2.1 Asset Paths

**Resolve assets automatically, run this first:**

```bash
"$PYTHON" "<skill dir>/scripts/resolve_assets.py"
```

It probes every place assets can live, in order, **bundled** (`<skill>/assets/`)
→ **plugin** (`$CLAUDE_PLUGIN_ROOT/brand-assets/`) → **Metis G: drive**
(`G:\Shared drives\Knowledge Management\New Brand Assets\`) → override
(`$METIS_BRAND_ASSETS`), and prints a JSON map of the best available path for
`master`, `intro_slides`, `icon_lib`, `logo_white`, `logo_black_mint`, and
`timesaver_pngs`. **Use those paths in the build script.** On a Metis machine the
G: copies are picked up automatically; on a standalone install only `master`
resolves and the rest report `available: false`, degrade per §2.1.1. See
`references/asset-resolution.md` for the full map.

**Manual fallback, resolve the master template in this order:**
1. **Bundled (works standalone):** `<skill dir>/assets/master.pptx`, a copy of
   the 2025 template (32 layouts, blank) ships inside this skill. Use it when the
   plugin assets are not available. This makes generation work even when the
   skill is installed standalone (via the `.skill` package / Settings →
   Capabilities) rather than inside the `metis-skills` plugin.
2. **Plugin assets (full set):** `${CLAUDE_PLUGIN_ROOT}/brand-assets/master.pptx`
   , use when the skill is installed inside the `metis-skills` plugin; this is
   the only place the optional firm-overview and icon libraries live.

| Asset | Path |
|---|---|
| **Master template** (bundled, blank deck w/ 32 layouts) | `<skill dir>/assets/master.pptx` |
| **Master template** (plugin copy) | `${CLAUDE_PLUGIN_ROOT}/brand-assets/master.pptx` |
| **Firm overview slides** (8 slides, plugin only) | `${CLAUDE_PLUGIN_ROOT}/brand-assets/intro-slides.pptx` |
| **Icon Library** (manual, plugin only) | `${CLAUDE_PLUGIN_ROOT}/brand-assets/Icon_Lib.pptx` |
| **Icon Library** (programmatic, bundled, no asset dependency) | `scripts/icons.py` (Lucide, downloaded on demand, see §2.8) |
| **Logo (White)** | `G:\Shared drives\Knowledge Management\New Brand Assets\Metis Strategy Logo\Metis Strategy White RGB logo.png` |
| **Logo (Black-Mint)** | `G:\Shared drives\Knowledge Management\New Brand Assets\Metis Strategy Logo\Metis Strategy Black-Mint RGB Logo.png` |

> **Standalone note:** the bundled `assets/master.pptx` carries all 32 layouts
> and the brand frame, so native-layout generation (the default path) works
> fully. The firm-overview and manual icon library are not bundled (size); the
> programmatic Lucide icons (§2.8) have no such dependency and work standalone.

#### 2.1.1 Graceful degradation (when an asset is absent)

`resolve_assets.py` tells you what is available. Honor it, **never block or
error on a missing asset:**

| Asset reports `available: false` | What to do |
|---|---|
| `timesaver_pngs` | **Skip Path B reproduction.** Do not try to `Read` a `slide-{N}.png` (it will not exist). Build the diagram **bespoke** from primitives in `metis-brand.md`. Conceptual slides still get a real diagram. |
| `intro_slides` | Skip the optional firm-overview section; do not offer it. |
| `icon_lib` (manual) | Use drawn shape primitives, or the programmatic Lucide icons (§2.8), Lucide has no asset dependency and is unaffected by this row. |
| `logo_white` / `logo_black_mint` | No action needed, the bundled `master.pptx` already embeds the logo and green-arrow frame. |
| `master` | This should never happen (bundled). If it does, stop and report. |

The default build path (native layouts + bespoke diagrams + tables/charts +
programmatic icons) needs only `master`, which is always bundled. So a
standalone recipient gets a fully working skill; the plugin/G: assets only add
the Timesaver library, the firm overview, and the manual icon library on top.

### 2.2 Python Environment

> **Python is installed but NOT on the git bash PATH.** Use the full path:
> ```bash
> PYTHON="C:/Users/$USER/AppData/Local/Programs/Python/Python312/python.exe"
> "$PYTHON" build_deck.py
> ```
> **Required package:** `python-pptx` — if missing: `"$PYTHON" -m pip install python-pptx`
> **Do NOT** loop trying to install Python or add it to PATH. It is already installed.

### 2.3 Design System

Three design paths share the same brand system, in priority order (see §0.5.1):

- **Path 1 (Native template layouts, default):** Read `references/metis-layouts.md`.
  Add the slide from the layout whose placeholder structure matches the content,
  then fill placeholders. Use this whenever a layout reasonably fits, it is the
  most direct way to get human-varied, on-brand slides.
- **Path A (Component recipes, hand-built):** Read `references/patterns.md` for
  component selection and `references/metis-brand.md` for python-pptx recipes.
  For content no native layout supports.
- **Path B (Timesaver structures):** Read `references/timesaver_index.md` for the
  "Use when..." catalog and load PNG candidates (see §0.6). When the shape itself
  expresses the thought.

All three paths share the brand constants below.

**Key brand constants:**
- **Colors:** Dark Navy `#20216F`, Metis Blue `#256BA2`, Mint `#3CDBC0`, Dark Gray `#4A4A4A`, Light Gray `#F2F2F2`
- **Font:** Calibri only. Title 28pt bold navy, body 14pt dark gray, caption 11pt blue.
- **Margins:** Content area starts at (0.50", 1.10") and ends at (12.83", 6.80"). Slide is 13.33" x 7.50".

### 2.4 Layout selection

**First choice: a native template layout.** Read `references/metis-layouts.md`
and match the content to a layout's placeholder structure. Common picks:

| Content | Native layout |
|---|---|
| Single chart, table, or one big visual | `One Chart or Table` |
| Three charts side by side | `Three Chart` |
| Two-way comparison (current vs future, A vs B) | `Comparison` |
| 3 items with headings | `Three Content w/ Heading` |
| 4 items with headings | `Four Content w/ Heading` |
| 4-step process with sub-bullets | `Four Content Process` |
| 4 or 6 icon-led points | `Icon box Four/Six Content` |
| Big visual + side caption | `Content with Caption` |
| People / speakers (photo + bio) | `Two/Three Content Speaker Image` |
| 4 items each with a photo | `Four Content - 4 Photo` |
| Quotes (columns or rows) | `Four Content Quote` / `Quote Rows` |
| Section break | `Section Divider` / `Closing Slide` |
| Cover | `Cover Page` / `Alt Cover Page 1-3` |

**Fallback only when no native layout fits:** the hand-built grids in
`references/patterns.md` (Full Width, Two Column, Sidebar+Main, Three Column,
Title+Visual), with code in `references/metis-brand.md`. Reserve even-column
hand-built card grids for content that is genuinely parallel, they are the
most over-used AI layout (see §0.7).

### 2.5 Phased Build Workflow

#### Phase 1: Plan the Deck

##### 1.0a Classify each slide, then pick the path (per slide)

For each content slide, classify first (§0.5.1), then choose the path:

1. **Relationship / concept** → plan a **diagram or metaphor** (Timesaver §0.6
   Path B, or a bespoke diagram). Record the metaphor and load the candidate PNG.
2. **Flat enumeration** → plan a **native template layout**
   (`references/metis-layouts.md`); record the layout name.
3. **Data / evidence** → plan a **table or chart** (native `One Chart or Table`
   / `Three Chart`, or a hand-built table).

Do not route relationship content to a card layout because it is convenient.
The build-init step below primes the hand-built libraries because conceptual
slides will need them. Also set the **dials** (§0.3, default VARIANCE 6 /
DENSITY 7) and plan **variation across the deck** (density and slide type, §0.7),
not just component rotation. Every slide must pass the §0.7 pre-flight checklist.

##### 1.0 Build init (mandatory, once per deck before slide planning)

Before any slide-by-slide planning, prime the conversation with both candidate
libraries. This is the precondition that makes the per-slide browse in §0.6
meaningful — the agent can't compare candidates from two libraries it hasn't
loaded.

1. **Read `references/representatives.json`.** This file maps each Timesaver
   catalog section to 3–4 canonical exemplar slide-Ns. Load each listed PNG
   via the multimodal Read tool from
   `G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\timesaver_pngs\slide-{N}.png`.
   Total: ~50 PNG loads. These provide visual awareness of every catalog
   section, not just the one the agent's first instinct points at.

2. **Read `references/patterns.md` in full.** Components are in context
   alongside the Timesaver representatives.

After build init, both libraries are in conversation context. The per-slide
pick (§0.6) becomes a comparison against locked structural needs, not a
reach for one library by default.

**Why build init is mandatory:** the failure mode it prevents is content-type
misclassification. If the agent decides "this is enumeration, only browse the
Text-based section," it loads candidates only from one section and can't
recognize when a slide actually fits a metaphor it hasn't seen. Loading
representatives from every section eliminates that failure point.

**Build init applies to single-slide and quick-build tasks too — don't scope
it down.** A common rationalization is *"this is just one slide / a quick
draft / an iteration on an existing deck, the full sweep is overkill."* That
reasoning is wrong, and naming it here so it can be recognized when the
temptation appears: misclassification is a *per-slide* failure mode, not a
per-deck one. A single-slide planner that loads only candidates from the
section it thinks the slide belongs to has the same blind spot as a
single-slide planner that skips the catalog entirely. Scope-down variants of
this argument — *"single-slide is different,"* *"this is just a draft,"*
*"I'm iterating, full load is wasteful"* — all share the same shape and
should be recognized as the same shortcut. Single-slide planning pays the
same build-init cost as multi-slide planning. By design.

##### 1.1 Slide-by-slide outline

After build init, create the outline:

```
Slide 1: Cover (fixed) — "Client Name — Project Title"
Slide 2: Agenda (content, Grid 1) — 4 agenda items
Slide 3-12: Firm Overview (fixed, optional) — ask user if needed
Slide 13: Section Divider (fixed) — "Our Approach"
Slide 14: Three-Phase Process (content, Grid 4) — Discovery, Design, Deliver
...
```

For each content slide, the plan must include:

- **Structural needs** (written *first*, before any candidate is surfaced —
  see "Structural needs first" below)
- **patterns.md candidate** + corresponding component reference loaded (from
  the build-init full read)
- **timesaver candidate** + corresponding PNG loaded via multimodal Read
- **Chosen Source** — either path is legitimate
- **Why** — rationale tying the pick back to the locked structural needs

##### 1.2 Structural needs first (per content slide)

For each content slide, write the structural needs **before** surfacing
candidates. This is the bias-fighting step: by committing to what the slide
*structurally requires* before looking at what's available, the candidate
selection has to defend itself against the locked criteria, not against the
agent's preference for one library.

Format:

```
Slide content: <one-line summary of what the slide says>
Structural requirements (derived from content, not from libraries):
  1. <e.g., "show four parties around a center">
  2. <e.g., "imply bidirectional contribution">
  3. <e.g., "make the center smaller than the parties to signal stewardship">
```

Vague requirements (*"clean, on-brand, professional"*) are not valid. The
requirements must derive from the slide's actual content and structural
relationships — things a reviewer can match against any candidate.

##### 1.3 Both candidates with read evidence (per content slide)

For every content slide, the plan includes:

- A `patterns.md` candidate (component number + brief reason it fits the
  locked needs)
- A `timesaver` candidate (slide-N + brief reason it fits the locked needs,
  with the corresponding PNG loaded via Read)

Both candidates require **corresponding Read tool calls earlier in the
conversation**. For Timesaver candidates that's the PNG; for patterns.md
candidates that's the build-init full read of patterns.md (which already
covers the component). A citation without read evidence is not valid.

Then pick the chosen Source and write the rationale — referencing the locked
structural needs, not introducing new criteria at decision time.

##### 1.4 Visual Variety Rule

Apply during planning:

1. **No-repeat rule:** The primary component on slide N must differ from slide N-1 AND slide N-2. If three consecutive slides have the same content type (e.g., "key points"), use three different components from the rotation alternatives for that type (see Component Rotation Guide in patterns.md).
2. **Grid diversity:** Across any 5 consecutive content slides, use at least 2 different grid layouts. A deck where every content slide uses the same grid is monotonous even if the components vary.
3. **Rhythm breakers:** Every 3-4 content slides, insert one slide that uses a fundamentally different visual form — a pull quote (#36), a before/after (#20), a framework diagram (#31 or #32), a process visual (#22 or #24), or a Timesaver metaphor structure (e.g., House slide-179, Honeycomb slide-155, Decision Tree slide-130). These prevent the "wall of cards" effect.
4. **Write it in the outline:** The slide plan MUST include all the columns described in §1.1 — Structural needs, both candidate columns, Chosen Source, Why. See the example table below:

**Visual Variety Rule — apply during planning:**

1. **No-repeat rule:** The primary component on slide N must differ from slide N-1 AND slide N-2. If three consecutive slides have the same content type (e.g., "key points"), use three different components from the rotation alternatives for that type (see Component Rotation Guide in patterns.md).
2. **Grid diversity:** Across any 5 consecutive content slides, use at least 2 different grid layouts. A deck where every content slide uses the same grid is monotonous even if the components vary.
3. **Rhythm breakers:** Every 3-4 content slides, insert one slide that uses a fundamentally different visual form — a pull quote (#36), a before/after (#20), a framework diagram (#31 or #32), a process visual (#22 or #24), or a Timesaver metaphor structure (e.g., House slide-179, Honeycomb slide-155, Decision Tree slide-130). These prevent the "wall of cards" effect.
4. **Write it in the outline:** The slide plan MUST include a `Source` column naming either a `patterns.md` component number or a `timesaver slide-{N}` reference for each content slide:

```
| # | Title                        | Type    | Structural needs                            | patterns.md cand.       | timesaver cand.             | Chosen                      | Why                                                  |
|---|------------------------------|---------|---------------------------------------------|-------------------------|-----------------------------|-----------------------------|------------------------------------------------------|
| 1 | Cover                        | fixed   | —                                           | —                       | —                           | —                           | —                                                    |
| 2 | Agenda                       | content | 4 sequential topics, equal weight            | #7 Callout              | slide-23 (Four categories)  | #7 Callout                  | enumeration; no metaphor adds value                  |
| 3 | The Opportunity              | content | one bold claim + supporting context          | #36 Pull Quote          | slide-22 (Statements)       | #36 Pull Quote              | quote primacy fits hero framing better than 3-up     |
| 4 | Market Landscape             | content | 3 segments, equal weight, comparable         | #9 Cards+Header         | slide-23 (Four categories)  | #9 Cards+Header             | enumerative; comparison is implicit                  |
| 5 | Strategic Pillars            | content | foundation → body → roof; layered dependency | #9 Cards+Header (3-row) | slide-179 (House)           | timesaver slide-179 (House) | dependency relationship needs metaphor               |
| 6 | Transformation Roadmap       | content | 5-step linear progression                    | #22 Process             | slide-114 (Linear Process)  | #22 Process                 | both fit; #22 is faster build, picks tied            |
| 7 | Capability Ecosystem         | content | 6 reinforcing pieces around a center         | #9 Cards+Header         | slide-155 (Hex flywheel)    | timesaver slide-155 (Hex)   | reinforcement needs the radial structure             |
| 8 | Closing / Call to Action     | content | single mantra, hero scale                    | #36 Pull Quote          | slide-32 (Quote + Comm.)    | #36 Pull Quote              | single sentence beats elaborated quote               |
```

The plan must include **both** candidate columns for every content slide — a
patterns.md candidate AND a timesaver candidate — even when the chosen pick
is obvious. Filling in both columns forces consideration of both libraries
before the pick is made. The "Why" cell ties the choice back to the
"Structural needs" cell.

**Firm overview is optional.** Ask the user: "Should I include the Metis firm overview slides?"

#### Phase 2: Write the Build Script

Create a single Python script (`build_deck.py`). **Critical rules:**
- **Always start from `master.pptx`** — never open `intro-slides.pptx` directly as the base.
- **Use `'1_Title Only'` layout for content slides** — gives green arrow, logo, footer, page number.
- **Never use `'Blank'` for content slides** — it has none of the brand elements.
- **Use `'Section Divider'` layout for dividers** — navy background is built in.
- **Set titles via placeholder (idx=0)**, not `add_textbox()`.
- **Copy firm overview slides** from `intro-slides.pptx` using the `copy_slide_from()` helper.
- **Deduplicate the zip** before saving.

See `references/metis-brand.md` for the full boilerplate code including:
- `get_layout()` helper
- `add_content_slide()` helper
- `add_section_divider()` helper
- `copy_slide_from()` helper
- `save_clean()` helper

#### Phase 3: Build Content Slides

For each content slide, follow the path picked in Phase 1:

**Path A (component recipe):**
1. Add a content slide: `slide = add_content_slide("Title", "Subtitle")`
2. **Choose components from `references/patterns.md`** — every Path-A content slide MUST use at least one component. Plain text on white is never acceptable.
3. **Get the code recipe from `references/metis-brand.md`** and call the component functions.
4. Add content shapes below the title area (starting at y=1.10").

**Path B (Timesaver structure):**
1. Add a content slide: `slide = add_content_slide("Title", "Subtitle")`
2. **Read the chosen Timesaver PNG** from `G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\timesaver_pngs\slide-{N}.png` via the multimodal Read tool.
3. **Reproduce the layout in python-pptx** — shape positions, hierarchy, label placement — using brand tokens from `references/metis-brand.md` (colors, fonts, margins). Do not freehand colors or fonts.
4. Add content shapes below the title area (starting at y=1.10").
5. **Verify visual variety:** Before moving to the next slide, check:
   - Is the primary component different from the previous slide's primary component?
   - Has this exact grid+component combination appeared on any of the last 3 slides?
   - If either check fails, swap in an alternative component from the Component Rotation Guide in patterns.md.

**Every text element must have real content.** No placeholder text, no "Lorem ipsum."

#### Phase 4: Polish and Save

Before saving, verify:
- Every slide has a title
- No shapes contain placeholder text
- All fonts are Calibri
- All colors match the brand palette
- Content is within margin bounds (0.50" to 12.83" horizontal, 1.10" to 6.80" vertical)

### 2.6 Deck Structure Guidelines

**Proposals / BD Decks:**
1. Cover
2. Firm Overview (optional — ask user)
3. Our Understanding of Your Challenge (Grid 1)
4. Our Approach (Grid 4 or Grid 5)
5. Our Team (Grid 4)
6. Investment (Grid 5 with table)
7. Next Steps / Closing

**In-Project Deliverables:**
1. Cover
2. Agenda (Grid 1)
3. Section Divider + Content slides (repeat per section)
4. Key Findings / Recommendations (Grid 1 or Grid 2)
5. Next Steps
6. Appendix (Firm Overview here if included)

### 2.7 Common Patterns

**Bullet list with accent markers:**
```python
bullets = ["Finding one", "Finding two", "Finding three"]
y = 1.10
for b in bullets:
    marker = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.50), Inches(y + 0.05), Inches(0.12), Inches(0.12))
    marker.fill.solid()
    marker.fill.fore_color.rgb = MINT
    marker.line.fill.background()
    add_body(slide, b, 0.75, y, 12.08, 0.35)
    y += 0.45
```

**Highlighted callout box:**
```python
box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.50), Inches(y), Inches(12.33), Inches(1.50))
box.fill.solid()
box.fill.fore_color.rgb = LIGHT_GRAY
box.line.fill.background()
bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.50), Inches(y), Inches(0.06), Inches(1.50))
bar.fill.solid()
bar.fill.fore_color.rgb = MINT
bar.line.fill.background()
```

**Section divider:** Use the `'Section Divider'` layout — never draw navy rectangles manually.
```python
divider = prs.slides.add_slide(get_layout('Section Divider'))
for ph in divider.placeholders:
    if ph.placeholder_format.idx == 0:
        ph.text = "Section Title"
```

### 2.8 Graphical Icons (Lucide)

When a slide has card-based components (pattern #8b, #9, or custom cards),
**automatically include Lucide icons** unless the cards are inherently
numbered or ordered. Do not wait for the user to ask for icons.

**Module:** [`scripts/icons.py`](scripts/icons.py)
**Concept map:** [`references/icon-map.json`](references/icon-map.json)
**Reference:** [`references/icons.md`](references/icons.md)

#### Auto-icon rules (apply by default)

1. **Card-based slides get icons automatically.** When building slides with
   3+ cards (capabilities, categories, features, tools, phases with
   distinct identities), call `suggest_icon(title)` for each card and
   include the icon in the build. No explicit user request needed.
2. **Numbered/ordered items do NOT get icons.** If the cards represent a
   sequence where the number carries meaning (Step 1, Step 2, Step 3),
   use `icon_circle_text` with numbers instead.
3. **Mixed slides:** A slide can have numbered steps in the center column
   and icon-bearing category cards in a side column. The rule is per-group,
   not per-slide.
4. **One library per deck.** Once you use Lucide on one slide, use it on
   all icon-bearing slides in the deck.

#### Icon selection workflow

```python
from scripts.icons import suggest_icon, add_lucide_icon, lucide_icon_card

# Auto-select: scans title against references/icon-map.json
icon_name = suggest_icon("Security and Compliance")  # -> "shield-check"
icon_name = suggest_icon("Claude Agents")             # -> "bot"
icon_name = suggest_icon("Data Platform")             # -> "layers"

# If suggest_icon returns "circle-dot" (no match), pick manually from
# https://lucide.dev/icons/ or fall back to icon_circle_text.
```

#### Quick reference

```python
from scripts.icons import lucide_icon, add_lucide_icon, lucide_icon_card
from pptx.util import Inches

# Get a recolored PNG path
png = lucide_icon("shield-check", color="#20216F", size_px=256)

# Insert directly on a slide
add_lucide_icon(slide, "users", Inches(1), Inches(2),
                size=Inches(0.6), color="#256BA2")

# Component: icon + title + body card (drop-in for icon_circle_text
# when a real glyph communicates better than a numbered circle)
lucide_icon_card(slide,
                 icon="clipboard-check",
                 title="Confirm Requirements",
                 body="Validate de-ID and retention requirements.",
                 left=Inches(0.5), top=Inches(2), width=Inches(3.0))
```

#### Decision: Lucide icon vs. `icon_circle_text`

Both are valid. The choice is content-driven:

| Use a Lucide icon (DEFAULT for categories) | Use `icon_circle_text` (for ordered items) |
|---|---|
| Cards represent different *kinds* of things | Items are inherently numbered or sequential |
| Glyph is the natural anchor (capabilities, tools, platforms) | Number is the natural anchor (priorities, steps, pillars) |
| Timeline, capability map, categorized list | Ranked list, phased process, ordered pillars |

**When in doubt, use icons.** Most business content is categorical, not
sequential. Icons make slides scannable and visually distinct.

#### Brand alignment

- **Default color** for icon strokes is Dark Navy `#20216F`. For client decks
  with extracted brand tokens, pass `icon_color=brand["colors"]["primary_text"]`.
- **Default stroke width** is `2` (Lucide default). Bump to `2.5` only for
  board-level decks needing extra weight.
- **Keep one library per deck.** Don't mix Lucide with Font Awesome or
  hand-drawn icons. If Lucide is missing one concept, fall through the
  hierarchy in `references/icons.md` for the whole deck, not just one icon.

#### Dependencies

`scripts/icons.py` requires:
- Python: `python-pptx` plus ONE of:
  - `pycairo` (`pip install pycairo`) **recommended for Windows/macOS**,
    ships its own native binary, no system libcairo needed
  - `cairosvg` (`pip install cairosvg`) + system `libcairo`
    (macOS: `brew install cairo`; Linux: `apt-get install libcairo2`;
    Windows: GTK runtime or `cairocffi-precompiled`)

The module auto-detects which renderer is available. pycairo is tried
second but works out of the box on Windows. On first use, the helper
caches rendered PNGs under `~/.cache/metis-pptx/lucide/`.

#### Editing mode

In the **Editing Workflow** (Section 1), graphical icons are usually already
present in the source deck. Preserve them. Only call into the Lucide
helper when adding *new* slides where an icon belongs. For client decks,
pass the client's extracted primary color to keep the icon palette aligned
with the rest of the deck.

---

## 3. Visual QA (Both Modes)

**Assume there are problems. Your job is to find them.**

Full QA workflow (export scripts, content QA commands, visual checklist, verification loop): see `references/visual-qa.md`.

Quick reference:
```bash
"$PYTHON" "$SKILL_DIR/scripts/visual_qa.py" output.pptx qa_images/
"$PYTHON" "$SKILL_DIR/scripts/thumbnail.py" output.pptx
```

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Troubleshooting

### Text overflow or elements overlapping after generation
- **Cause:** Content longer than measured box height, or hardcoded Y positions.
- **Fix:** Use measure-first layout. Call `wrap()` on Paragraph objects before placing. Run visual QA to catch remaining issues.

### Brand colors don't match metis-brand-identity
- **Cause:** `references/metis-brand.md` drifted from canonical values.
- **Fix:** Verify DARK_NAVY is `#20216f` and MINT is `#3cdbc0`. Run `scripts/extract_brand.py` on a known-good Metis template to confirm.

### PowerPoint COM automation fails on visual_qa.py
- **Cause:** PowerPoint not installed, or COM server not registered.
- **Fix:** Visual QA requires desktop PowerPoint (not Office Online). Ensure PowerPoint is installed and not running when the script starts.

### Generated deck opens with "Repair" prompt in PowerPoint
- **Cause:** Invalid XML in slide relationships, often from duplicate slide IDs or malformed chart data.
- **Fix:** Check python-pptx version (>=0.6.21). Avoid reusing slide objects across presentations. Validate with `python-pptx` relationship inspector.

### Fonts render as fallback (Arial instead of Open Sans)
- **Cause:** Open Sans not installed on the machine, or font name misspelled in code.
- **Fix:** Install Open Sans from Google Fonts. Verify font name string is exactly `"Open Sans"` (case-sensitive in python-pptx).
