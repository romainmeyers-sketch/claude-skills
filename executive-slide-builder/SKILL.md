---
name: executive-slide-builder
description: >
  Executive storytelling, narrative structure, strategic framing, and
  translating technical content into C-Suite-ready language. This skill
  produces content strategy and narrative structure only, not files. Two
  modes: (1) Narrative Mode for content needing story structure, (2)
  Elevation Mode for technical material needing business translation.
  Trigger on "executive overview," "narrative arc," "structure the business
  case," "make this more executive," "elevate for the C-Suite," "translate
  to business language," "too technical," or "systems-level to
  executive-level." After content is structured, hand off to metis-pptx
  for .pptx output or metis-html-slides for browser output. Do NOT trigger
  on "create a deck" (metis-pptx); "create a PDF" (metis-pdf-creator);
  "write a whitepaper" (metis-whitepaper).
metadata:
  author: Metis Strategy
  version: 1.0.1
---

# Executive Slide Builder

This skill governs how to construct the narrative, select slide structures,
and write executive-quality content. Actual `.pptx` file generation is
handled by the `metis-pptx` skill — once the story is locked, this skill
produces a structured build brief that metis-pptx can execute directly.

**Scope boundary — read this first:**
This skill produces *narrative content and a build brief*. It does NOT
produce `.pptx` files, Python scripts, or any slide-generation code.
The `.pptx` build is owned entirely by the `metis-pptx` skill. When
this skill's workflow is complete, stop and present the build brief to
the user. Do not write `python-pptx` code, do not import `pptx`, do
not create `build_deck.py`, and do not attempt to generate a
PowerPoint file. If the user asks for the actual deck, tell them to
invoke `metis-pptx` with the build brief — or offer to do so on their
behalf by calling that skill. The division is: this skill decides
*what to say*; metis-pptx decides *how to render it*.

**What you get from this skill:**
1. A content map — the key messages, proof points, and what stays off the slide
2. A slide-by-slide outline — one job per slide, sequenced for narrative flow
3. Executive-quality draft copy — concise, quantitative, skimmable
4. A build brief — a structured handoff to metis-pptx for `.pptx` generation

The agent should not invent the story from scratch. It should:
- Gather the relevant context from source materials
- Infer the required narrative structure
- Reuse existing slide architectures from the asset library
- Draft concise, executive-style copy
- Iterate by tightening and simplifying rather than rebuilding

---

## Core Operating Principles

### 1) Context first, then content

Before drafting any slide, identify and review the relevant source
materials. The user's ask is rarely self-contained — real guidance lives in:
- Uploaded briefs, outlines, or transcripts
- Existing decks or meeting notes
- Spreadsheets or models (for numbers)
- Brand templates or visual frameworks

If source material is referenced indirectly, look for it rather than
defaulting to generic content.

### 2) Separate content truth from presentation truth

- **Content source of truth**: documents that determine facts, metrics,
  sequencing, recommendations, and claims
- **Presentation source of truth**: templates and framework slides that
  determine tone, layout, density, and visual structure

A style guide does not override facts. Content sources do not invent
new slide architectures when a reusable one already exists.

### 3) One slide, one job

Every slide has a single job. Before drafting, name it explicitly.
Anything that belongs to another section gets cut or moved — not squeezed in.

### 4) Reuse structure before inventing structure

Always search the shared asset library for an existing layout before
creating a new one. The library contains: slide skeletons, roadmap
layouts, comparison pages, phased transformation pages, business-case
structures, summary pages, KPI cards, and framework visuals.

**Shared asset library:**
- G drive: `G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\Metis_Timesaver Slides.pptx`
- Google Slides: `https://docs.google.com/presentation/d/1KtfpTOi0CTdySmzN4usaiHJJhXF63KoS/edit`

Map the user's outline onto the closest fitting structure from this deck
before writing any slide copy.

---

## The Five-Layer Model

Content exists at five layers. The goal in any executive-facing output
is always to reach Layer 1. This model is the diagnostic for mode
detection and the reference for naming, framing, and quality checks
throughout the workflow.

| Layer | Description | Example | What to do with it |
|---|---|---|---|
| 1 — Business Outcome | What it means for revenue, margin, or customers | "$X margin improvement" | Lead with this |
| 2 — Capability Name | What the capability does, in plain language | "Intelligent Operations" | Use as the primary label |
| 3 — Program / Solution | The named digital program or initiative | "Connected Manufacturing Program" | Supporting context only |
| 4 — Product / Tool | The named AI tool or product | "[Vendor product name]" | Internal reference; remove from exec slides |
| 5 — System / Technical | The underlying technology stack | "[Acronym], [Acronym], [Acronym]" | Never appears in C-Suite materials |

C-Suite audiences live at Layers 1 and 2. They do not need Layers 4
and 5. Layer 3 may appear as supporting context but should never lead.

**The executive test for every piece of content:**
"Can the most senior leader in the room not know what [system name]
means and still understand why this matters?" If the answer is no,
the content is not yet at the right level.

---

## Mode Detection

After reading source materials (during the Context Retrieval Protocol),
assess where the content sits on the Five-Layer Model:

- **Elevation Mode** — activates when source material is dominated by
  system names, acronyms, product/vendor names, technical architecture
  language, or when capabilities are described by what they *are* rather
  than what they *do for the business*. If most content sits at Layers
  3–5, elevation is needed. State this to the user:
  > "The source material is primarily at the systems and product level —
  > I'll run the elevation workflow to translate it to executive language
  > before building the narrative."

- **Narrative Mode** — activates when the content is already at Layers
  1–2 and the user's challenge is sequencing, emphasis, or story
  structure. State this to the user:
  > "This content is already at the business outcome level — I'll move
  > straight to narrative structure and slide sequencing."

If the assessment is wrong, the user corrects and the agent adjusts.
No extra decision point, no friction.

**Elevation Mode flow:**
Client Setup (4 Anchors) → E1: Audit → E2: Separate → E3: Value Stream
Map → E4: Name → E5: Time Horizons → E6: Headline → then into the
Required Workflow (Steps 1–10) → Completeness Check → So What Test →
Build Brief → metis-pptx

**Narrative Mode flow (unchanged):**
Context Retrieval → Steps 1–10 → Quality Bar → Build Brief → metis-pptx

---

## Context Retrieval Protocol

At the start of every session, actively locate the relevant context.
**Do not assume context from a previous session carries over.**

### Priority 1 — User-provided files in this session

Read any files the user has uploaded or referenced first — briefs,
outlines, transcripts, models, decks. These are the most authoritative.

### Priority 2 — PowerPoint template for this session

Before building any slide, confirm which template to use. Templates
change per client and engagement.

Ask:
> "Please share the PowerPoint template for this project — a file
> upload, Google Slides link, or file path. I'll use it to govern
> layout, colors, fonts, and slide density for everything I build."

If the user doesn't provide one, fall back to the shared asset library —
but flag this rather than defaulting silently.

When a template is provided:
- Read it before drafting
- Extract: color palette, fonts, title treatment, body text sizing,
  header/footer conventions, box and card structures, recurring layouts
- Treat those conventions as binding — do not introduce layouts, colors,
  or font styles not present in the template
- Flag explicitly if something the user wants can't be achieved within
  the template's constraints

### Priority 3 — Shared drive (for slide structures and brand assets)

For slide structure and reusable frameworks, consult:
`G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\Metis_Timesaver Slides.pptx`

This is the source of truth for layouts and visual structure. Use it
before inventing a new slide architecture.

### Priority 4 — Ask before guessing

If no relevant context can be found, tell the user specifically what is
missing and ask for it. Never silently proceed with assumed or cached context.

---

## How to Open a Session

When the user invokes `/executive-slide-builder` or signals a narrative
or elevation challenge, start here (if not already provided):

1. **Template:** "Please share the PowerPoint template for this project
   (file, link, or path). If you don't have one, I'll use the shared
   asset library."

2. **Project context:** "What's the client or project name, and who is
   the audience for this section?"

3. **Read source materials and detect mode.** After receiving context,
   read all source documents and assess the Five-Layer Model to determine
   Narrative Mode or Elevation Mode. State the mode to the user.

Wait for context before building a content map or drafting any slide.
The template governs everything visual; the audience governs everything
about emphasis and tone.

---

## Elevation Pre-Processing

*This section runs only in Elevation Mode. In Narrative Mode, skip
directly to the Required Workflow.*

The purpose of elevation is to translate source material written at the
systems or technical level into executive-ready content that leads with
business value, not technology. It is client-agnostic — the four anchors
make it specific to each organization.

### Client Setup: The Four Anchors

Complete these before running any elevation step. Everything downstream
depends on getting these right. Populate them from source documents,
stakeholder interviews, or existing strategy materials.

For detailed templates and formats for each anchor, read
`references/elevation-reference.md`, Section 1.

**Anchor 1 — The Value Stream Frame**
How the organization describes the journey from winning a customer to
keeping one. Find their version — it is almost always in a strategy
deck, annual operating plan, or investor presentation. Document the
zones, what each covers, and the primary metric for each. Cross-cutting
capabilities (platforms, data infrastructure, AI foundations) span all
zones and sit as foundation, not inside any single column.

**Anchor 2 — The Portfolio Proof Point**
The single most powerful number: the total return on the technology
portfolio — not any one system. This is the headline that gives every
capability claim credibility. Document as: [Total benefit] from
[portfolio/program name] at [total investment]. If no proof point
exists yet, identify the closest proxy.

**Anchor 3 — The Naming Convention**
The implicit naming style for digital and AI capabilities. Pick one or
two patterns that fit the client's voice and apply them consistently.
Inconsistent naming across slides is the most visible signal that
content is not yet executive-ready. See the reference file for common
naming patterns.

**Anchor 4 — The Time Horizon Labels**
The client's language for investment stages. Executives think in
horizons, not quarters. Find these from their STRAP, AOP, or board
materials. If the client already uses specific horizon language, use
their words exactly. See the reference file for common formats.

---

### Step E1 — Audit the Source Material

Read all source documents and extract into a working inventory. Do not
write anything yet.

**What to collect:**
- Every system name and acronym
- Every AI product or tool name
- Every digital program or initiative name
- Every stated business outcome with a number attached
- Every stated business outcome without a number
- Every investment figure tied to a program or initiative

**Flag immediately:**
- Capabilities that have systems but no stated business outcome
- Capabilities that have outcomes but no named system or program
- Any part of the client's value stream that has nothing mapped to it —
  these are genuine gaps that become questions or risks in the narrative

The gaps are often as important as the content. An empty column on an
executive slide asks a question the audience will ask out loud.

### Step E2 — Separate "What It Is" from "What It Does"

For every item in the inventory, write two sentences:

1. **Technical sentence:** What is this system or product, and how does
   it work?
2. **Business sentence:** What problem does it solve, and what does it
   change for the business?

Only the business sentence will appear in C-Suite materials. The
technical sentence is the internal reference for validating accuracy.

If the business sentence cannot be written, the capability is not yet
ready for executive consumption. Return to source documents or flag
for a stakeholder conversation.

### Step E3 — Apply the Value Stream Frame

Map every capability to a position in the client's value stream
(Anchor 1).

For each capability ask:
- Where in the value stream does this create value?
- Which primary metric does it move?
- Does the client already have a named column for this?

Cross-cutting capabilities span all zones and sit below as a foundation
layer, not inside any single column.

### Step E4 — Name at the Right Level

Apply the naming convention (Anchor 3) consistently.

**Rules:**
1. Drop all acronyms unless universally known at the executive level
2. Apply the client's naming convention consistently
3. Name to the outcome, not the feature — the name should imply what the
   capability *achieves*, not what it *is*
4. Check consistency across all slides — same capability, same name
5. Watch for premature naming — a building capability gets a name; a live
   capability gets a name *and* a number

### Step E5 — Map to Time Horizons

Using the client's horizon labels (Anchor 4), assign every capability
to the correct time window.

**Critical discipline:** never conflate deployment with value
realization. These are different events, often one year apart. Showing
both — correctly labeled — demonstrates that the author understands the
difference between activity and outcome.

### Step E6 — Build the Headline First

Before arranging capability content on a slide, write two things:

1. **The headline number** (from Anchor 2) — the total portfolio return.
   A single aggregated figure contextualizes every individual capability
   below it. Without it, the slide is a list. With it, the slide is a
   business case.

2. **The framing sentence** — one sentence that tells the executive what
   the slide is *arguing*, not just what it *contains*.
   - Not: "This slide shows our digital capabilities across the value stream"
   - Yes: "[Client name]'s digital investments are converting operational
     complexity into measurable commercial advantage — protecting revenue,
     expanding margin, and differentiating the customer experience."

Customize the framing sentence to the client's strategic priorities.

**After completing E6, proceed to the Required Workflow (Step 1) with
the elevated content as input.**

---

## Required Workflow

### Step 1: Name the slide's job

Before drafting anything, answer:
- What is this slide's single job in the deck?
- Is this one slide or a section of slides?
- What does the audience need to believe or decide after seeing it?
- Is there an outline that governs sequence?

If an outline exists, it governs section flow unless stakeholder feedback
explicitly overrides it.

### Step 2: Gather and read the source material

Actively find and review: brief, business case, outline, transcript or
feedback notes, models or spreadsheets for numeric support, prior slides,
reusable frameworks from the asset library.

If context is incomplete, look for it in connected files or referenced
folders before asking the user.

*In Elevation Mode, the translation table from pre-processing serves
as the primary content input for this step.*

### Step 3: Build a content map

Extract from the source material:
- Key messages (what must land)
- Major numbers and proof points
- Phase logic or chronology
- Internal vs. external value distinctions
- What stakeholders explicitly want emphasized
- What does **not** belong on this slide

Use the content map to determine hierarchy and visual prominence before
touching any slide structure.

*In Elevation Mode, the content map should already be at Layers 1–2.
If any Layer 3–5 content remains, send it back through Steps E2–E4
before proceeding.*

### Step 4: Select the right slide structure

Match the content map to a slide form from the asset library:
- Headline + proof points
- "Three forces" convergence
- Roadmap with phase columns
- Phased build / scale / expand
- Framework layering
- Business case / investment
- Executive summary with chart placeholder
- KPI summary / metric cards

Never force all content into the same format. Pick the structure that
serves the message.

### Step 5: Draft in executive prose

Write concisely, quantitatively, in active voice, easy to skim.

Rules:
- Short declarative bullets
- Lead with the action or outcome
- Use numbers when available
- One idea per bullet
- No paragraphs unless the user asked for narrative copy
- No jargon unless it appears in source materials
- Prefer "show, don't tell"

### Step 6: Let the visual do the heavy lifting

If a framework or chart carries the argument, reduce surrounding text.
Bullets should clarify: what is in focus, why it matters, what changes
from one phase or slide to the next.

Do not duplicate what the visual already shows.

### Step 7: Ground every number and stub every placeholder

All metrics, projections, and quantitative claims must trace back to
source material — never invented. If a number is uncertain, flag it
rather than guess.

When a final visual is not ready, create the slide shell with a clearly
labeled placeholder and stable surrounding copy. This lets the deck
move forward without waiting on the visual.

### Step 8: Sequence multi-slide sections intentionally

Before drafting individual slides, establish the narrative sequence:

> Frame the issue → Explain the model → Show the roadmap →
> Show the economics → Summarize for executives

Each slide should build on the one before it. If the sequence doesn't
hold up without a slide, that's a sign it shouldn't exist.

### Step 9: Produce a build brief for metis-pptx — STOP HERE

This is the final output of the executive-slide-builder skill. Once the
narrative structure and content are confirmed, produce a structured build
brief and present it to the user. This is where this skill's job ends.

Do not proceed to write Python code, generate `.pptx` files, or invoke
`python-pptx`. The build brief is the deliverable. If the user wants
the actual PowerPoint file, tell them:
> "The narrative and build brief are ready. Want me to hand this off to
> metis-pptx to generate the deck?"

If they say yes, invoke the `metis-pptx` skill with the build brief.
Do not attempt to replicate what metis-pptx does — it owns brand
colors, fonts, layout grids, component code, template files, and the
Python build script.

**Build brief format:**

```
DECK TYPE: [proposal / in-project deliverable / other]
TEMPLATE: [file path or "shared asset library fallback"]

SLIDE 1
  Title: [slide title]
  Job: [one sentence — what this slide must do]
  Layout: [layout name from asset library]
  Component: [component name from metis-pptx design system, e.g., "Phased Approach", "KPI Summary"]
  Content:
    - [bullet 1]
    - [bullet 2]
  Placeholder: [describe any visual placeholder, or "none"]

SLIDE 2
  ...
```

### Step 10: Iterate by tightening, not reinventing

On revision passes: shorten, sharpen, simplify, improve emphasis, reduce
clutter — but preserve the architecture if it is working.

Rebuild from scratch only if the existing structure is fundamentally wrong.

---

## Quality Gates

### Standard Quality Bar (Both Modes)

**Good output:**
- Clearly reflects source materials — nothing invented
- Uses a reusable slide pattern rather than an ad hoc one
- Feels executive and skimmable — key numbers are easy to find
- One job per slide, nothing bleeding into adjacent slides
- Build brief is specific enough for metis-pptx to execute without questions

**Weak output:**
- Reads like speaker notes
- Mixes multiple slide jobs on one page
- Invents unsupported claims or metrics
- Ignores the outline or existing slide structures
- Over-explains instead of structures
- Produces a vague handoff that requires re-clarification

### Completeness Check (Elevation Mode)

Run these four checks before finalizing any elevated output:

**Coverage:** Does every zone in the client's value stream have at least
one capability mapped? If a zone is empty, is that a genuine gap (name
it, flag it) or a timing issue (label it "in roadmap")?

**Outcome:** Does every capability have a stated business outcome? Are
outcomes attached to the realization year, not the deployment year? Do
individual outcomes add up directionally to the headline number?

**Naming:** Are all capability names consistent across every slide? Does
any name require technical knowledge to understand? Do all names follow
the convention from Anchor 3?

**Status:** Can an executive tell, at a glance, what is live versus
building versus aspirational? Is the organization's track record
visible — not just its roadmap?

### The "So What" Test (Both Modes)

Read the final content as if you are the most senior leader in the room,
seeing it for the first time. Ask for every element:

1. **"So what?"** — Does this create a business implication? If not, cut
   it or reframe it.
2. **"How much?"** — Is there a number? If not, is there a directional
   claim that is still defensible?
3. **"By when?"** — Is the time horizon clear?
4. **"Compared to what?"** — Is there a baseline or competitive context?

Any element that fails all four questions belongs in a backup or appendix
slide, not the executive version.

### Traceability (Both Modes — Critical in Elevation Mode)

Every claim in an executive-facing output must be traceable to a source.
This protects the author when a number is challenged, establishes the
difference between stated and inferred claims, and ensures source
document updates can be reflected systematically.

**Claim types — use precisely:**
- **Actual** — A measured result. The strongest claim. Can be stated as fact.
- **Target** — A stated goal with organizational commitment. Frame as a
  target, not a result.
- **Projection** — A modeled figure from assumptions. Carry a qualifier:
  "projected," "estimated," or "expected."
- **Inferred** — Derived logically from combining multiple sources. The
  highest-risk type. Must be validated with a stakeholder before appearing
  in executive output.

**Traceability check (add to Completeness Check):**
- Does every number have a source record with document name, location,
  and claim type?
- Is there at least one "Actual" claim visible — proof that something
  has been delivered, not just promised?
- Are all "Inferred" claims flagged for stakeholder validation?
- Are all gaps documented, even if they do not appear on the slide?
- If a source document is updated, is it clear which claims need revisiting?

For detailed traceability formats (claim-level, translation-level,
gap-level), read `references/elevation-reference.md`, Section 3.

---

## Troubleshooting

These appear regardless of client or industry. Watch for them in any
mode, but they are especially prevalent when elevating technical content.

| Failure Mode | What It Looks Like | Fix |
|---|---|---|
| System-led narrative | Slide organized by tool or product name | Reorganize by business capability; systems become footnotes |
| Outcome-free capability | Named capability with no metric or result | Attach a target, even directional: "reduces cycle time" |
| Conflated timelines | Deployment labeled as value realization | Separate build year from realization year; show both |
| Inconsistent naming | Same capability called two different things | Pick one name; apply everywhere |
| Unexplained gaps | A value stream zone with nothing mapped | Flag explicitly or label "in roadmap" |
| Over-promising | End-state vision in a year only foundations exist | Name to what is actually delivering; save the vision |
| Buried proof point | Portfolio ROI in appendix or absent | The portfolio return belongs in the headline |
| Alphabet soup | Executive slide full of internal acronyms | Acceptable only in operational materials, never C-Suite |
| Technology as the hero | Narrative leads with system, not business gain | Outcome first, technology in support |
| Premature precision | Specific dollars on early-build capabilities | Use ranges or directional language until validated |

---

## Revision Behavior

When the user says "make it punchier," "less salesy," "more executive,"
"keep the layout, change the wording," or "this belongs in another section":
- Preserve the architecture
- Refine tone and hierarchy
- Tighten wording
- Shift emphasis without losing factual grounding

---

## Writing Style

Concise executive prose: short claims, active voice, low jargon,
quantitative where possible, easy to skim. Prefer tight bullets over
explanatory paragraphs. Let charts and frameworks carry the argument —
use text only to clarify what matters, what changes, and why.
