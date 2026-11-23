---
name: metis-capability-map
description: >
  Generate L1-L3 business capability maps aligned to customer/guest/patient
  journey stages for any industry. Use for capability maps, capability models,
  value chain mapping, capability heat maps, maturity assessments, or
  operating model design around capabilities. Trigger on "map our
  capabilities," "capability gap analysis," "business architecture," "where
  should we invest," "who owns what capability," or "product operating model."
  Supports PPTX, XLSX, and HTML output. Validates visual output against
  metis-brand-identity. Do NOT use for: BD capabilities decks or proposals
  (metis-premier-proposal); general presentations (metis-pptx).
metadata:
  author: Metis Strategy
  version: 0.1.1
---

# Business Capability Mapping Skill

This skill generates comprehensive L1–L3 business capability maps organized around three
pillars — [Persona] Journey, Value Chain, and Supporting Domains — for any industry. The
journey pillar name adapts to the industry (e.g., "Guest Journey" for hospitality,
"Patient Journey" for healthcare, "Customer Journey" for B2B SaaS). The maps are designed
for C-suite and senior leaders at large enterprises who need a clean, executive-grade view
of organizational capabilities with optional maturity heat mapping.

---

## 1. Conceptual Model

Every capability map has three L1 categories. Understanding why they're separate — and
where they overlap — is the key to building maps that are both journey-centric and
holistically useful to leadership.

### Dynamic Journey Naming

The first pillar is named based on the primary user/customer of the business. Do NOT
default to "Guest Journey" — that only applies to hospitality. Identify the correct
persona from the industry context:

| Industry              | Pillar 1 Name        | Primary Persona   |
|-----------------------|----------------------|-------------------|
| Hospitality           | Guest Journey        | Hotel guest       |
| Healthcare            | Patient Journey      | Patient           |
| B2B SaaS              | Customer Journey     | Business buyer    |
| Telecommunications    | Subscriber Journey   | Subscriber        |
| Manufacturing         | Buyer Journey        | Industrial buyer  |
| Retail                | Shopper Journey      | Shopper           |
| Financial Services    | Client Journey       | Client            |
| Education             | Student Journey      | Student/Learner   |
| (Any other)           | Customer Journey     | Customer (default)|

When the user describes their industry, determine the right persona and pillar name
before generating. If ambiguous, ask: "Who is the primary end user of your product or
service?" Use that answer to name Pillar 1 throughout all outputs.

### The Three Pillars (+ Optional Fourth)

```
┌─────────────────────────────────────────────────────────────┐
│                   [PERSONA] JOURNEY                         │
│  L1: Awareness → Consideration → Purchase → Onboarding     │
│       → Usage/Experience → Retention/Renewal                │
│  (What the [persona] sees and feels at each stage)          │
├─────────────────────────────────────────────────────────────┤
│                        VALUE CHAIN                          │
│  L1: Strategy Dev → Marketing → Sales → Service Delivery   │
│       → Customer Success → Product/Service Innovation       │
│  (Internal functions that power each journey stage)         │
├─────────────────────────────────────────────────────────────┤
│                   SUPPORTING DOMAINS                        │
│  L1: Finance → HR/People → IT/Technology → Legal/Compliance │
│       → Facilities/Operations → Data & Analytics            │
│  (Cross-cutting functions that enable the value chain)      │
├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
│              [INTERNAL PERSONA] JOURNEY  (optional)         │
│  L1: Recruit → Onboard → Develop → Perform → Retain        │
│  (What the employee/provider/team member experiences)       │
└─────────────────────────────────────────────────────────────┘
```

### Optional: Internal Persona Journey (Pillar 4)

When enabled, this pillar captures the internal workforce experience — the stages an
employee, provider, or team member moves through. Like Pillar 1, the name adapts:

| Industry              | Pillar 4 Name          | Internal Persona      |
|-----------------------|------------------------|-----------------------|
| Healthcare            | Provider Journey       | Physician / Clinician |
| Hospitality           | Team Member Journey    | Hotel staff           |
| B2B SaaS              | Employee Journey       | Internal employee     |
| Manufacturing         | Workforce Journey      | Plant / line worker   |
| Retail                | Associate Journey      | Store associate       |
| (Any other)           | Employee Journey       | Employee (default)    |

This pillar is **off by default**. Only include it when the user requests it or when the
engagement context involves workforce transformation, talent strategy, or operating model
design. L2/L3 capabilities here often share with Supporting Domains (e.g., HR capabilities
appear in both) — tag those with `[shared:Supporting-L1-Name]`.

**[Persona] Journey** captures the outside-in view — the stages the primary user moves
through. Each stage has L2/L3 capabilities describing what the organization must be able
to do to deliver that stage well (e.g., Journey L1 "Awareness" → L2 "Brand Presence" →
L3 "Social Media Management").

**Value Chain** captures the inside-out operational view — the internal functions that
power the journey. These are aligned to journey stages, so some L2/L3 capabilities will
appear in both pillars. That duplication is intentional — it shows the same capability
from two perspectives (customer-facing vs. operational).

**Shared capability rules** — tag a capability as `[shared]` when:
- A Value Chain L3 directly enables a specific Journey stage (tag as `[shared:Journey-L1-Name]`)
- The same L3 capability name or function appears in both Journey and Value Chain pillars
- A Supporting Domain L3 is critical to a specific Value Chain function (tag as `[shared:VC-L1-Name]`)

Do NOT mark capabilities as shared just because they're loosely related. The link must be
direct and defensible — a C-suite leader should immediately understand why the connection
exists. In the XLSX Shared column, list the specific pillar and L1 it connects to (e.g.,
"Journey: Onboarding" rather than just "Yes"). In PPTX and HTML, render shared tags as
small colored badges showing the cross-reference.

**Supporting Domains** are cross-cutting — they don't map to a single journey stage but
enable the entire value chain. Finance, HR, IT, Legal, etc.

### L2 and L3 Depth

- **L2** = a capability group (e.g., "Digital Marketing")
- **L3** = a specific capability (e.g., "SEO & Content Optimization")

Each L3 capability can optionally carry additional data through **optional lenses**.
All lenses are off by default — include only what the user requests.

### Optional Lenses

All lenses add columns to the single Capability Map sheet. The column order flows
logically: **what it is → how mature → where it's going → who owns it → investment
decision**. When multiple lenses are enabled, columns appear in this order after the
base capability columns (Pillar, L1, L2, L3, Shared With):

1. Current Maturity (1-5) + Maturity Label — how mature is this capability today
2. Target Maturity (1-5) + Maturity Gap (formula) — where does it need to be
3. Strategic Initiative — what strategy this supports
4. Owner — who is accountable
5. Investment Priority — what to do about it

**Maturity Assessment**
- Current Maturity score (1–5): 1=Ad-hoc, 2=Developing, 3=Defined, 4=Managed, 5=Optimized
- Maturity Label auto-fills from the score via formula
- Leave scores empty for workshop use. Wire up dropdowns and conditional formatting.
- When investment lens is also enabled, maturity columns are shared (Current Maturity
  serves both lenses — do not duplicate).

**Investment Prioritization**
- **Current Maturity (1-5)**: Shared with maturity lens if both are enabled
- **Target Maturity (1-5)**: Where the capability needs to be
- **Maturity Gap**: Formula (Target - Current). Conditional formatting: larger gap = darker red
- **Strategic Initiative**: Which strategic priority this capability supports (free text)
- **Investment Priority**: Invest / Maintain / Divest / Sunset
- In PPTX: add an Investment Summary slide showing a 2x2 matrix (Strategic Importance
  vs. Current Maturity) with L1 capabilities plotted as bubbles. Detail slides show
  investment priority as colored tags (Invest=green, Maintain=blue, Divest=orange,
  Sunset=red) next to each L3.
- In HTML: add investment priority as colored pill badges next to each L3. Add a
  filterable view that lets users filter by investment priority. Include a gap analysis
  summary section at the top showing total capabilities by priority bucket.

**Capability Ownership**
- **Owner**: The role, team, or individual accountable for the capability (e.g., "VP
  Digital", "Product Ops", "Chief Medical Officer")
- In PPTX: add owner as a small label beneath each L3 capability in the detail tables.
  Add an Ownership Summary slide grouped by owner showing which capabilities roll up to
  each leader — this directly supports operating model and org design conversations.
- In HTML: show owner as a gray label beneath each L3. Add a "Group by Owner" toggle
  that reorganizes the entire map by owner instead of by pillar — this lets leaders see
  "what do I own?" at a glance.

### Supplemental Tabs (Separate Sheets)

These tabs provide deeper analytical views. They are generated as separate sheets in XLSX,
additional slides in PPTX, or toggle-able views in HTML.

**People / Process / Tools Assessment** (off by default — enable when user asks)

This tab breaks down each L2 capability across the three foundational dimensions of any
capability: People (skills & expertise), Process (how work gets done), and Tools (technology
& systems). This is based on the CMMI-aligned maturity model where capabilities comprise
an integrated set of processes, technologies, and deep expertise.

- Assessed at the **L2 level** (not L3) — L3 is too granular for this analysis
- Columns: Pillar | L1 | L2 | Process Maturity (1-5) | Process Notes | Tool-set Maturity
  (1-5) | Tool-set Notes | People/Expertise Maturity (1-5) | People Notes | Org Reach
  (1-5) | Performance Measurement (1-5)
- **Process Maturity**: 1=ad hoc, 2=repeatable but inconsistent, 3=standard and consistent,
  4=predictable and flexible, 5=continuously improved
- **Tool-set Maturity**: 1=manual/no tools, 2=individual steps automated, 3=some automation
  and standard tools, 4=appropriate automation across capability, 5=optimal automation with
  cross-capability integration
- **People/Expertise**: 1=insufficient expertise, 2=limited expertise, 3=select pockets of
  expertise, 4=sufficient expertise and staffing, 5=advanced expertise and fully staffed
- **Org Reach**: 1=ad hoc, 2=within team, 3=within department, 4=across organization,
  5=across organizational ecosystem
- **Performance Measurement**: 1=none, 2=activity tracked, 3=output measured, 4=outcomes
  measured, 5=business outcomes measured and controlled
- Notes columns provide qualitative context (e.g., "HRIS/HR technology org misalignment",
  "Data exists on different platforms; accessibility and integrity concerns")
- Apply the same 1-5 conditional formatting heat map colors to all maturity columns
- Leave all scores and notes empty for workshop use unless the user asks you to pre-populate
- In PPTX: render as a summary slide per pillar showing a table with Process / Tools / People
  columns and traffic-light indicators. Add a detail slide per focus area with strengths,
  needs/opportunities, and representative quotes (matching the Metis assessment format)
- In HTML: render as a separate toggle-able tab view with the same heat map colors and
  expandable notes

**Industry Benchmark** (off by default — enable when user asks)

This tab compares each L2 capability's maturity against industry averages, highlighting
where the organization is above, at, or below peer maturity. This is the slide that
makes C-suite leaders pay attention — it answers "how do we compare?"

- Assessed at the **L2 level** (same grain as People/Process/Tools)
- Columns: Pillar | L1 | L2 | Company Maturity (avg of L3s) | Industry Average | Delta |
  Benchmark Insight
- **Company Maturity**: Calculated as the average of L3 current maturity scores within
  that L2 (from the main Capability Map sheet)
- **Industry Average**: Generated from first principles based on industry knowledge.
  Consider company size, market position, and digital maturity when calibrating. Scores
  should be defensible in a C-suite presentation — cite industry reports, APQC benchmarks,
  or Gartner/Forrester frameworks when possible.
- **Delta**: Formula (Company - Industry Average). Positive = above peers, negative = gap.
- **Benchmark Insight**: Brief qualitative insight explaining the delta and what it means
  strategically (e.g., "Significantly below peers; #1 gap area. DAP and health scoring are
  standard at this ARR", "Above peers; key competitive differentiator — protect this
  investment")
- Apply conditional formatting to Delta column: ≥0.3 = green (strength), ≤-0.5 = orange
  (attention), ≤-1.0 = red (critical gap)
- In PPTX: render as a bar chart slide showing Company vs. Industry Average by L1, with
  delta annotations. Follow with a "Key Gaps & Strengths" summary slide listing the top 5
  gaps and top 3 strengths with benchmark insights.
- In HTML: render as a toggle-able tab with sortable columns. Include a filter to show
  only gaps (negative delta) or strengths (positive delta). Add a summary banner showing
  the count of capabilities above, at, and below industry average.

**Roadmap / Sequencing** (off by default — enable when user asks)

This tab sequences strategic initiatives across quarters, showing what to do when and
why. It transforms the capability gap analysis into an actionable implementation plan
that leadership can approve and fund.

- One row per strategic initiative (derived from the Capability Map sheet's Strategic
  Initiative column when investment lens is enabled, or generated fresh)
- Columns: Quarter | Pillar | L1 | L2 | Strategic Initiative | Current Maturity (1-5) |
  Target Maturity (1-5) | Gap | Dependencies | Milestone 1 | Milestone 2 | Milestone 3 |
  Success Metric | Owner | Investment Priority
- **Quarter**: Q1 through Q8 (2-year horizon). Color-coded by half-year:
  - Q1-Q2 = green (Year 1 H1), Q3-Q4 = blue (Year 1 H2),
  - Q5-Q6 = purple (Year 2 H1), Q7-Q8 = orange (Year 2 H2)
- **Dependencies**: What must be in place before this initiative can succeed. Critical
  for sequencing logic — later initiatives should reference earlier ones.
- **Milestones**: Three discrete columns (M1, M2, M3), each containing a single clear
  deliverable — not paragraphs. M1 is typically planning/procurement (month 1-2), M2 is
  build/pilot (month 3-4), M3 is the outcome/steady-state milestone (month 5-6).
- **Success Metric**: A specific, measurable outcome in **baseline → target** format so
  progress is actually trackable (e.g., "POC win rate: 45% → 60%", "Support tickets from
  new users: 85/mo → 50/mo"). Avoid vague metrics — every metric should have a number.
- Sequencing logic: quick wins and foundation-building in Q1-Q2, scale and expand in
  Q3-Q4, transformational initiatives in Q5+. Initiatives that depend on earlier work
  must be scheduled after their dependencies.
- In PPTX: render as a horizontal swimlane timeline with quarters on the x-axis and
  pillars as swim lanes. Each initiative is a colored bar spanning its quarter. Add a
  summary slide showing initiative count and key theme per quarter.
- In HTML: render as a toggle-able tab with a Gantt-style timeline view. Filterable by
  pillar, quarter, and investment priority. Clickable initiatives expand to show
  milestones, dependencies, and success metrics.
- Generate a **Roadmap Summary** sheet/slide aggregating initiative counts by quarter
  and pillar, with a key theme per quarter.

**Capability Definitions** (off by default — enable when user asks)

This tab provides plain-language definitions for each L3 capability, giving workshop
participants shared vocabulary and reducing scope debates during maturity assessments.

- One row per L3 capability (same grain as the main Capability Map sheet)
- Columns: Pillar | L1 | L2 | L3 | Definition | Business Value | Example Activities |
  Common Enterprise Tools
- **Definition**: A clear, concise description of what this capability is. Vary the
  language — do NOT start every definition with "The organizational ability to..." Use
  diverse openers: "Creating and distributing...", "Measuring and analyzing...",
  "Designing, testing, and evolving...", "Embedding security testing into...", etc.
  Written for a mixed audience of business and technology leaders.
- **Business Value**: Why this capability matters — the business outcome it drives or
  the risk it mitigates. Frame in terms a CFO, CEO, or board member would care about.
- **Example Activities**: Concrete examples of what "doing this capability" looks like
  in practice. Helps participants calibrate their maturity assessment.
- **Common Enterprise Tools**: Representative tools and platforms commonly used by large
  enterprises for this capability. Not prescriptive — included to ground conversations
  in what "good" looks like and to identify potential tool gaps. Only include where
  relevant (some capabilities like "Cultural Integration" don't have specific tools).
- In PPTX: render as an appendix section with one slide per L1 showing a table of L3
  definitions. Include a "Common Tools" column when tools are relevant.
- In HTML: render as a toggle-able tab with searchable definitions. Each L3 expands to
  show Business Value, Example Activities, and Common Tools.

**README** (always included when any supplemental tab is enabled)

A reference sheet explaining every column across all tabs. Generated automatically when
any supplemental tab is enabled. Includes the column name and a plain-language
description of its purpose, format, and how to interpret it.

---

## 2. Generation Workflow

### Step 1: Gather Context

Ask the user for:

1. **Industry & company type** — "What industry are you in, and roughly what does your
   company do?" (e.g., "luxury hospitality," "B2B SaaS fintech," "regional healthcare
   system"). This drives the journey stages and capability vocabulary.

2. **Journey stages** — "Do you have existing customer/guest journey stages, or should I
   generate industry-standard ones?" If they provide a journey map file, parse it.

3. **Scope** — "Should I include all three pillars (Journey, Value Chain, Supporting), or
   focus on a subset? Would you also like an internal [Employee/Provider] Journey pillar?"

4. **Optional lenses** — "Would you like any of these optional lenses?"
   - Maturity assessment (empty scores for workshop use)
   - Investment prioritization (invest/maintain/divest + current vs. target maturity gap)
   - Capability ownership (owner field for operating model / org design conversations)
   - People / Process / Tools assessment (separate tab breaking down each L2 across process,
     tool-set, and people/expertise maturity with qualitative notes)
   - Industry benchmark (separate tab comparing L2 maturity against industry averages with
     delta analysis and benchmark insights)
   - Roadmap / Sequencing (separate tab sequencing initiatives by quarter with milestones,
     dependencies, and trackable success metrics)
   - Capability definitions (separate tab with plain-language definitions, business value,
     example activities, and common enterprise tools for each L3)

5. **Output format** — "Which format: PPTX deck, XLSX spreadsheet, interactive HTML, or
   multiple?" Default to XLSX + PPTX if they don't specify.

### Input Modes

The skill supports three input modes. Detect which one the user is using and adapt:

**Mode A: Generate from scratch** — The user describes their industry/company and you
generate the full map from first principles. This is the default mode.

**Mode B: Refine an existing map** — The user uploads an existing capability map (XLSX,
CSV, PPTX, PDF, or pasted text). Read the file, parse the existing capabilities, and:
- Identify gaps (missing L2/L3 capabilities you'd expect for the industry)
- Flag potential overlaps or redundancies
- Suggest re-leveling (e.g., an L3 that should be an L2, or vice versa)
- Present a "gap analysis" summary before generating the improved version
- Preserve the user's original naming conventions where possible — don't rename
  capabilities they've already socialized with stakeholders unless they ask

**Mode C: Extend from a document** — The user uploads a strategy doc, org chart, annual
report, or journey map. Extract relevant context (business units, strategic priorities,
customer segments, pain points) and use it to inform a more tailored capability map.
Call out which capabilities were derived from the document vs. generated from industry
knowledge.

If the user provides a file (journey map, strategy doc, org chart, existing capability
map), read it and extract relevant context to inform the capability generation.

### Step 2: Generate the Capability Map

Build the map industry-by-industry from first principles — do not use a fixed template.
The map should feel tailored to the user's specific industry and company type.

**Process:**
1. Define L1 stages for each pillar based on the industry (include Pillar 4 if requested)
2. For each L1, generate 3–6 L2 capability groups
3. For each L2, generate 2–5 L3 specific capabilities
4. Tag shared capabilities between Journey and Value Chain with `[shared]`
5. For each enabled optional lens, add columns to the same Capability Map sheet (do not
   create separate tabs per lens). Leave all lens columns empty for workshop use:
   - **Maturity**: Current Maturity dropdown (1-5), Maturity Label formula (CHOOSE),
     conditional formatting for heat map colors.
   - **Investment**: Target Maturity dropdown (1-5), Maturity Gap formula (Target -
     Current), Strategic Initiative (free text), Investment Priority dropdown
     (Invest/Maintain/Divest/Sunset). If maturity lens is also enabled, share the
     Current Maturity column — do not duplicate it.
   - **Ownership**: Owner column (free text) for the client to populate during org
     design or operating model workshops.

**Naming conventions:**
- L1: Noun phrases (e.g., "Customer Onboarding," "Financial Management")
- L2: Noun phrases describing a capability group (e.g., "Digital Engagement," "Talent Acquisition")
- L3: Specific, actionable capability names (e.g., "Chatbot & Virtual Assistant Management," "Employer Brand Development")

**Quality bar for C-suite audiences:**
- Use business language, not technical jargon
- Each capability should be distinct — no overlapping L3s within the same L2
- Journey stages should reflect the actual customer experience, not internal process steps
- Value chain L1s should map clearly to journey stages (include the mapping in output)
- Generate enough L3 capabilities to be comprehensive without being exhaustive — let the industry and scope guide depth naturally

### Step 3: Build the Output

Read `references/output-formats.md` for format-specific build instructions. The general
approach:

- **XLSX**: Structured spreadsheet with columns for Pillar, L1, L2, L3, Shared With,
  plus optional lens columns (Maturity, Investment, Owner). Conditional formatting for
  heat maps. All optional columns have dropdowns pre-wired.
- **PPTX**: Executive deck using the metis-pptx skill's design system. Table/grid layout
  with color-coded cells. One slide per pillar + summary/overview slides. When investment
  lens is enabled, include a 2x2 investment matrix slide. When ownership is enabled,
  include an ownership summary slide grouped by leader.
- **HTML**: Standalone interactive page with collapsible L1→L2→L3 hierarchy, color-coded
  badges, and search/filter. When ownership is enabled, include a "Group by Owner" toggle.
  When investment is enabled, include filterable investment priority views and gap summary.
  No external dependencies.

---

## 3. Maturity Heat Map

When the user enables maturity scoring, apply this color scale to all visual outputs:

| Score | Label      | Color (Hex) | Meaning                                    |
|-------|------------|-------------|--------------------------------------------|
| 1     | Ad-hoc     | `#E74C3C`   | No repeatable process, reactive             |
| 2     | Developing | `#E67E22`   | Some processes emerging, inconsistent       |
| 3     | Defined    | `#F1C40F`   | Documented processes, consistently followed |
| 4     | Managed    | `#2ECC71`   | Measured and controlled, data-driven        |
| 5     | Optimized  | `#27AE60`   | Continuously improved, industry-leading     |

In XLSX, use conditional formatting on the Maturity column. In PPTX, use cell background
colors in the capability table. In HTML, use colored badges next to each L3.

---

## 4. Industry Adaptation

Do not hardcode capabilities. Generate them from first principles based on the user's
industry. Here are calibration examples to show the expected depth and vocabulary — use
these as a quality reference, not as templates to copy:

**Example: Manufacturing** (Pillar 1 = "Buyer Journey")
- Buyer Journey L1: Awareness → Specification → Quoting → Order → Production → Delivery → After-Sales Support
- Value Chain L1: Product Engineering → Sourcing & Procurement → Production Planning → Manufacturing Operations → Quality Management → Distribution & Logistics → Customer Service
- Supporting L1: Finance → HR → IT/OT → Legal & Compliance → EHS (Environment, Health, Safety) → Facilities

**Example: Travel & Hospitality** (Pillar 1 = "Guest Journey")
- Guest Journey L1: Discovery → Booking → Pre-Arrival → Arrival → Stay/Experience → Departure → Post-Stay/Loyalty
- Value Chain L1: Brand Strategy → Revenue Management → Reservations → Guest Services → F&B Operations → Property Operations → Loyalty & CRM
- Supporting L1: Finance → HR → IT → Legal → Procurement → Sustainability

**Example: B2B SaaS** (Pillar 1 = "Customer Journey")
- Customer Journey L1: Awareness → Evaluation → Purchase → Onboarding → Adoption → Expansion → Renewal
- Value Chain L1: Product Strategy → Product Development → Marketing → Sales → Customer Success → Support → Platform Operations
- Supporting L1: Finance → People Ops → Engineering Platform → Legal → Security → Data & Analytics

**Example: Telecommunications** (Pillar 1 = "Subscriber Journey")
- Subscriber Journey L1: Awareness → Plan Selection → Activation → Usage → Support → Upgrade/Renewal → Win-Back
- Value Chain L1: Network Strategy → Network Engineering & Build → Product & Service Development → Sales & Distribution → Service Provisioning → Network Operations → Customer Retention
- Supporting L1: Finance → HR → IT/BSS/OSS → Legal & Regulatory → Supply Chain → Real Estate & Facilities

---

## 5. Python Environment

> **CRITICAL: Python is installed but NOT on the git bash PATH.** You MUST use the full
> path every time. Do not attempt `python`, `python3`, or `py` — they will fail.
>
> ```bash
> PYTHON="C:/Users/manvi/AppData/Local/Programs/Python/Python312/python.exe"
> ```
>
> **Before generating any output file**, run this setup block exactly once per session:
> ```bash
> PYTHON="C:/Users/manvi/AppData/Local/Programs/Python/Python312/python.exe"
> "$PYTHON" --version  # Verify it works
> "$PYTHON" -m pip install --quiet openpyxl python-pptx  # Required packages
> ```
>
> **Required packages:**
> - `openpyxl` — for XLSX generation
> - `python-pptx` — for PPTX generation
>
> **Build pattern:** Always write the full Python script to a .py file first, then execute:
> ```bash
> "$PYTHON" build_capability_map.py
> ```
> Do NOT use inline Python (`python -c "..."`) for anything beyond trivial checks.
> Complex scripts must be written to files for debuggability.

---

## 6. Output-Specific Instructions

Read `references/output-formats.md` for detailed build instructions for each format.
That file contains the exact Python code patterns, column structures, and styling rules.

When building PPTX output, also read the `metis-pptx` skill's `references/design-system.md`
and `references/layout-grids.md` for brand constants and slide construction patterns.
The capability map deck should follow the same design system (colors, fonts, margins)
as all other Metis decks.

---

## Troubleshooting

### Python not found or packages missing
- **Cause:** Python not on PATH in git bash.
- **Fix:** Always use full path: `"C:/Users/manvi/AppData/Local/Programs/Python/Python312/python.exe"`. Run `"$PYTHON" -m pip install --quiet openpyxl python-pptx` before generating output.

### PPTX output has wrong brand colors
- **Cause:** Not reading metis-pptx brand constants.
- **Fix:** Read `metis-pptx` skill's `references/design-system.md` for canonical brand tokens. Canonical values: Dark Blue #20216f, Metis Green #3cdbc0.

### Capability map too shallow (missing L3 detail)
- **Cause:** Insufficient industry context provided by user.
- **Fix:** Ask the user for more specifics about their business lines, key products/services, and organizational structure. Aim for 3-5 L3 capabilities per L2.

### Journey pillar named incorrectly
- **Cause:** Default "Customer Journey" used without checking industry.
- **Fix:** Consult the Dynamic Journey Naming table in Section 1. Ask: "Who is the primary end user of your product or service?" if ambiguous.

### XLSX conditional formatting not showing maturity colors
- **Cause:** `openpyxl` conditional formatting applied to wrong range.
- **Fix:** Ensure the maturity column is identified by header name, not hardcoded column letter. Apply `PatternFill` directly to cells based on score value.
