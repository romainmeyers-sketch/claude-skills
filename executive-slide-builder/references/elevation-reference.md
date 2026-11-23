# Elevation Reference Guide

Detailed templates, formats, and examples for the Executive Elevation
workflow. Read this file when operating in Elevation Mode — specifically
when populating the Four Anchors, building the translation table, or
documenting traceability.

---

## Section 1: Anchor Templates

### Anchor 1 — Value Stream Frame Template

Ask: *How does this organization describe the journey from winning a
customer to keeping one?*

Document in this format:

| Zone Name | What it covers | Primary metric |
|---|---|---|
| [Client's term for acquiring customers] | [Activities: sales, quoting, onboarding, etc.] | [Revenue / New bookings / Win rate] |
| [Client's term for delivering value] | [Activities: manufacturing, service delivery, operations] | [Margin / EBITA / Cost reduction] |
| [Client's term for retaining customers] | [Activities: account management, CX, renewals] | [Retention / NPS / CAS / Renewal rate] |

If the client does not have a named value stream framework, build one
from their strategic priorities and validate with a stakeholder before
proceeding.

Cross-cutting capabilities — platforms, data infrastructure, AI
foundations — span all zones and should be treated as foundation, not
assigned to one column.

---

### Anchor 2 — Portfolio Proof Point

Ask: *What has the organization already spent on digital or AI, and
what has it gotten back?*

This may be explicit (a published ROI figure) or may require calculation
from scattered investment and benefit figures across multiple documents.

Document as: **[Total benefit] from [portfolio/program name] at
[total investment]**

If no proof point exists yet (early-stage programs), identify the
closest proxy:
- A pilot result
- A single system's measured impact
- A validated target with a committed timeline

---

### Anchor 3 — Naming Convention Patterns

Common patterns (pick the one that fits the client's voice):

| Pattern | Example | Best for |
|---|---|---|
| Intelligent [Function] | Intelligent Manufacturing | AI-augmented operations |
| AI-Enabled [Activity] | AI-Enabled Tech Transfer | Process transformation |
| Autonomous [Process] | Autonomous Order-to-Cash | End-to-end automation |
| Connected [Asset/System] | Connected Supply Network | Infrastructure/integration plays |
| Digital [Capability] | Digital Customer Engagement | Digitization without AI emphasis |
| Predictive [Domain] | Predictive Quality | Analytics and forecasting |
| Smart [Function] | Smart Logistics | Consumer-friendly contexts |

Pick one or two patterns that fit the client's language and apply them
consistently. Do not mix patterns on the same slide.

---

### Anchor 4 — Time Horizon Label Formats

Common formats:

| Generic Horizon | Example Label A | Example Label B |
|---|---|---|
| Active and delivering today | "Live" / "Delivered" | "Foundation" |
| Building and deploying this year | "Scaling" / "In Flight" | "Expand" |
| Full value landing next year | "Realizing" / "Transforming" | "Accelerate" |
| Structural change, 2+ years | "Elevating" / "Reimagining" | "Future State" |

If the client already uses specific horizon language in their strategy
materials, use their words exactly — do not introduce new labels.

---

## Section 2: Translation Table

The translation table is client-specific and must be built fresh for
each engagement. This is the format — populate it during Step E1 using
the client's source materials.

| Technical / System Level | Executive Level | Value Stream Zone | Primary Outcome |
|---|---|---|---|
| [System 1] + [System 2] + [System 3] | [Capability Name] | [Zone] | [Metric + direction] |
| [Product A] + [Product B] | [Capability Name] | [Zone] | [Metric + direction] |
| [Platform] + [Analytics tool] | [Capability Name] | [Zone] | [Metric + direction] |

**How to build the table:**
1. List every system, product, and platform from the source audit (E1)
2. Group items that serve the same business function
3. Apply the naming convention (Anchor 3) to name each group
4. Assign to a value stream zone (Anchor 1)
5. Attach the primary outcome from the business sentence (E2)

Once built, this table becomes the single reference for anyone working
on executive materials for that client. It eliminates inconsistency and
speeds up future work significantly.

---

## Section 3: Traceability Formats

### Claim-Level Traceability

Every number, outcome, and timeline on a slide needs a source record.
This does not appear on the slide itself — it lives in the working file
behind it.

For each claim, capture:

| Field | What to record |
|---|---|
| **Claim** | The exact text as it appears on the slide |
| **Source document** | Document name and version or date |
| **Location** | Slide number, page, or section heading |
| **Claim type** | Actual · Target · Projection · Inferred |
| **Last verified** | Date the source was last checked |
| **Owner** | The internal stakeholder responsible for this number |

### Translation-Level Traceability

For each row in the translation table, capture the derivation chain:

```
[Executive Claim on Slide]
  ← derived from: [Capability Name at Layer 2]
  ← derived from: [Program / Solution at Layer 3]
  ← derived from: [Systems / Products at Layers 4–5]
  ← sourced from: [Document name, location, date]
  ← claim type: [Actual / Target / Projection / Inferred]
```

This chain makes it possible to answer "where does that number come
from?" in three seconds during an executive challenge — and to update
the slide immediately if a source document changes.

### Gap-Level Traceability

Gaps — value stream zones or capabilities with no mapped outcome —
must be documented, not just left blank or removed. A gap is one of
three things:

- **True gap:** The capability does not exist yet. Document that this
  was searched for and not found.
- **Timing gap:** The capability exists but its value lands in a later
  horizon. Document which horizon and why.
- **Data gap:** The capability exists and delivers value, but no
  quantified outcome could be located in source material. Document
  what was searched, what was found, and what would be needed to fill it.

Undocumented gaps become liabilities in executive settings. A leader
who asks "what about X?" should never receive the answer "we didn't
look at that."
