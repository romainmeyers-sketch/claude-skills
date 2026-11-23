---
name: metis-premier-proposal
description: >
  Produce premier client-ready proposals, capability decks, and case studies
  for Metis Strategy BD work. Use when the user asks to create, build, draft,
  or iterate on a proposal, capabilities deck, case study, BD follow-up, or
  pitch document. Trigger on "proposal," "capabilities deck," "case study,"
  "BD follow-up," or "proposal" with BD context (transcript, prospect,
  champion, buyer). Output is a 16:9 landscape PDF (10-25 pages) with
  ReportLab layout. For executive reframing of proposal content, hand off to
  executive-slide-builder. For PowerPoint output, hand off to metis-pptx.
  Always validates against metis-brand-identity. Do NOT use for: whitepapers
  (metis-whitepaper); one-pagers (metis-pdf-creator); SOWs/MSAs
  (metis-legal-drafting); capability maps (metis-capability-map).
metadata:
  author: Metis Strategy
  version: 1.0.3
---

# metis-premier-proposal

Produce premier client-ready proposals, capabilities decks, and case studies for Metis Strategy BD work. This skill encodes lessons from eight iterations of the Citi CRS Proposal (where HTML + Playwright and slide-screenshot pasting both failed) and the AI PM Capabilities deck (which exposed the need for narrative-first planning and flexible layout variety). ReportLab with coordinate-based placement and a measure-first layout pattern is what actually works for fixed-page designed documents.

## Output Specification

- **Format:** PDF, 16:9 landscape
- **Dimensions:** 13.33" x 7.5" (matches PowerPoint slide aspect ratio)
- **Typical length:** 10–25 pages (mode-dependent)
- **File size target:** 5–15 MB
- **Engine:** ReportLab with coordinate-based placement
- **Content source:** YAML file (flat `sections:` list) + Python dispatch

## Pick Your Mode

Three modes, three starter scripts. Mode shapes the entire document: close discipline, language, what to include, what to omit.

| Mode | Starter | Length | When to use |
|---|---|---|---|
| **buyer** | `starter_buyer.py` | 18–25 pp | Named prospect, post-discovery-call follow-up. Close with concrete CTA (scoping session, kickoff week, procurement step). |
| **capabilities** | `starter_capabilities.py` | 18–22 pp | Reusable marketing asset. No named prospect. Close with contact, no procurement language. |
| **casestudy** | `starter_casestudy.py` | 10–14 pp | Single engagement deep dive. Proof-forward. Close with "what good looks like" and team credit (anonymized). |

**Mode differences matter:**
- **Language mirroring** is a hard rule only in buyer mode. Use the buyer's transcript vocabulary verbatim in titles and pull quotes. Capabilities mode uses industry-neutral language. Case-study mode mirrors the engagement's language.
- **Problem framing** differs: buyer mode anchors in the buyer's own quoted pain; capabilities anchors in market dynamics with industry-typical metrics; case-study uses setup/situation, not problem framing.
- **Closing** differs: buyer ends on CTA, capabilities on contact block, case-study on credit plus what-good-looks-like.

## Workflow

### 1. Gather Inputs

Before any planning, collect:

- **Transcript** of any discovery call (buyer mode). Extract the buyer's actual words and phrasings.
- **Source material** such as prior proposal decks, relevant client case studies, and Metis IP decks.
- **Industry context** — financial services, healthcare, technology. This drives case study selection.
- **Named stakeholders** mentioned in the conversation (partners, blockers, champions). Verify spelling.

### 2. Consultant Planning Phase — Brief Before Draft

**Do not start writing YAML until you have a thesis and a sketch. Jumping to YAML first is the single biggest quality trap.**

Fill in `scripts/_brief_template.md` in the project's working folder, renamed to `brief.md`. The brief captures: audience, thesis, three-sentence summary, signature visual, three golden proof points, natural cleavage, narrative sketch, pacing map, kill list.

Every checkbox in the brief must be ticked before YAML drafting begins. See `references/narrative-planning.md` for the full planning loop (audience → thesis → signature visual → source triage → natural cleavage → sketch → reverse-outline → pacing → kill list).

**Source triage and kill-your-darlings disposition:** Read all source material first. Extract the 3–5 details that carry the thesis. Cut everything else, even the good stuff. A tight deck that lands beats a complete deck that doesn't. The skill's scaffolding implicitly encourages filling slots; subtract on purpose.

### 3. Write YAML Content File

Every piece of editable text goes in a flat `sections:` list. Each section declares:

```yaml
- type: pillars                    # dispatch key → renderer
  intent: "Show we own PM, not advise on it"  # one-line "so what?"
  eyebrow: "Module B"
  title: "Four Pillars of Embedded Product Management"
  # ...content_type-specific fields
```

- **`type`** is required. Missing or unknown types raise an error with the valid list.
- **`intent`** is required on all content pages (covers, dividers, and closings are exempt). It does not render. Its purpose: force the author to name the job of the page before drafting copy. At polish-pass time, re-read each page and ask: "does the copy actually do what intent says?"

Valid content types: `cover`, `problem_framing`, `section_divider`, `modules_overview`, `activities_deliverables`, `pillars`, `timeline`, `signature_image`, `quote`, `comparative`, `metric_dense`, `minicase_pair`, `proof_overview`, `next_steps`, `closing`. See `references/page-patterns.md` for each.

**Module count follows the story, not the template.** The `modules_overview` helper auto-picks the grid:
- 3 modules → wide 3-column row
- 4 → 2×2 (current Citi default)
- 5 → 3-top + 2-bottom staggered
- 6 → 3×2
- 7+ → raises `ValueError`

Each module typically gets 2–3 pages. Do not pad a 1-page idea to 3 pages because other modules have 3. See `references/content-rules.md` structural consistency section.

### 4. Extract and Crop Slide Images (if needed)

If embedding visuals from an existing PPTX:

1. Export slides as PNG using `scripts/crop_slide.py` or PowerPoint's native export
2. **Crop out the slide's own title, subtitle, and footer** — otherwise the rendered page will have duplicate titles
3. Save cropped versions with a `-cropped` suffix in the project's `_working` folder

Use the `signature_image` content type to render cropped visuals as a hero page with caption and callout.

### 5. Build with ReportLab (Measure-First Pattern)

The core technical rule: **measure content before placing containers**. See `references/architecture.md`. Helpers in `scripts/helpers.py` implement this pattern for bullet lists, callouts, cards, metric strips, and all the new pattern renderers.

Run the appropriate starter:

```bash
PYTHON="C:/Users/.../python.exe"
"$PYTHON" starter_buyer.py my-proposal-copy.yaml
# or starter_capabilities.py / starter_casestudy.py
```

The starter dispatches each section to its renderer and warns on missing `intent:` or three-in-a-row layout repetition.

### 6. Mechanical QA

Two verification passes:

```bash
# Overlaps + content rules + metadata
"$PYTHON" scripts/verify.py --pdf output.pdf --mode all

# Layout repetition (no pattern 3+ in a row)
"$PYTHON" scripts/verify.py --pdf output.pdf --mode repetition

# Reverse-outline: titles only, in sequence
"$PYTHON" scripts/verify.py --pdf output.pdf --mode titles

# Visual — render every page and eyeball it
"$PYTHON" scripts/verify.py --pdf output.pdf --mode render --out verify/
```

**Never declare the PDF done without visual verification.** Bbox analysis alone missed several critical issues in the Citi engagement.

### 7. Polish Pass — Three Passes Before Shipping

After mechanical QA passes, run the polish pass. See `references/polish-pass.md`.

- **Pass 1 — Does it land?** Read the full deck once, cold. Do you believe the thesis by page 5?
- **Pass 2 — Is every word pulling weight?** Read each page slowly. Cut 10%. Adjective audit. Re-read `intent` and ask: "does the copy do that?"
- **Pass 3 — Reverse-outline.** Run `--mode titles`. Read titles in sequence. Do they tell the story without the body copy? If yes, ship. If not, fix structure, not copy.

### 8. QA Checklist (Content Rules)

Before declaring content done (full list in `references/content-rules.md`):

- No em dashes (`—`, `\u2014`)
- No contractions in formal body text
- No absolute claims ("Zero", "Always", "Never", "Every")
- No named products from other client engagements
- Stakeholder names spelled correctly
- Transcript quotes appear at most twice
- Buyer's actual phrases in titles/subtitles/callouts (buyer mode)
- Case studies match prospect's industry or are industry-neutral
- Module page counts honest (2–3 typical, no padding)
- No layout pattern repeats 3+ times in a row
- Every module page has an `intent:` field
- Each callout label is 1–4 words, all caps
- Metric cards use round numbers with "+" or ranges
- Next Steps page has exactly 3 steps (buyer mode only)

### 9. Deploy

- Keep **all working files** (unpacked source, cropped images, intermediate PDFs, build scripts, `brief.md`) in `G:\My Drive\Vault\_working\<project>\`
- Copy **only the final PDF** to the shared drive: `G:\Shared drives\BizDev Collaboration\<Client>\<Year>\` (buyer mode) or the appropriate marketing folder (capabilities/casestudy)
- The vault's global CLAUDE.md has the rule: shared drives are for deliverables only, never intermediate artifacts.

## References

- `references/narrative-planning.md` — Consultant planning loop (audience → thesis → sketch → kill list)
- `references/polish-pass.md` — Three-pass critical re-read after mechanical QA
- `references/architecture.md` — Why ReportLab + measure-first pattern + YAML separation
- `references/page-patterns.md` — All 15 layout templates with code snippets
- `references/brand-standards.md` — Metis brand colors, fonts, logos, graphic devices
- `references/content-rules.md` — Editorial standards (no em dashes, no absolutes, intent per page, layout repetition, balance)
- `references/qa-process.md` — Verification workflow
- `references/failure-modes.md` — Things that broke during builds and how they were fixed

## Scripts

- `scripts/helpers.py` — Reusable layout helpers (measure_body_text, metric_card, activities_deliverables_page, section_divider with 3 styles, modules_overview_page auto-grid, and six pattern helpers: minicase_pair_page, signature_visual_page, process_timeline_page, quote_led_page, comparative_page, metric_dense_page)
- `scripts/verify.py` — Overlap, content, repetition, titles, render, metadata, and all-in-one checks
- `scripts/crop_slide.py` — Crop slide screenshots to remove titles/footers
- `scripts/starter_buyer.py` — Buyer-mode dispatch starter (+ `starter_buyer_copy.yaml` template)
- `scripts/starter_capabilities.py` — Capabilities-mode dispatch starter (+ `starter_capabilities_copy.yaml` template)
- `scripts/starter_casestudy.py` — Case-study-mode dispatch starter (+ `starter_casestudy_copy.yaml` template)
- `scripts/_brief_template.md` — Pre-build brief template (fill in before YAML)
- `scripts/starter_build.py` — DEPRECATED. Kept as a shim for legacy nested-key YAMLs.

## Reference Implementations

- **Buyer mode:** Citi CRS Proposal (April 2026), Andrew Krusell to Amresh Mathur.
  - `G:\My Drive\Vault\_working\citi-crs-proposal\citi-proposal-copy.yaml` (legacy nested format)
  - `G:\Shared drives\BizDev Collaboration\Citi\2026\Citi CRS Proposal - Metis Strategy 2026-04-15.pdf`
- **Capabilities mode:** AI PM Capabilities (April 2026).
  - `G:\My Drive\Vault\_working\ai-pm-capabilities-proposal\ai-pm-capabilities-v2.yaml` (new flat sections format — canonical example of the post-refactor shape)
  - `AI-PM-Capabilities-v2_Metis-Strategy.pdf` (22-page deck)

## Activation

When this skill is triggered, the first response to the user should confirm:
1. Mode selection (buyer / capabilities / casestudy)
2. Understanding of the client and context
3. The planned narrative sketch — not the page structure, but what the document argues
4. The content sources you will use
5. Whether you need any additional inputs (transcripts, case studies, stakeholder names)

Then draft `brief.md` in the working folder. **Never start coding the PDF before the brief is approved.** The Citi engagement lost multiple days to rebuilds because the approach was not settled upfront. The AI PM deck exposed the same failure mode: an unintended four-module shape propagated from the template because the narrative was not planned first.

---

## Troubleshooting

### ReportLab not installed
- **Cause:** Python environment missing the `reportlab` package.
- **Fix:** Run `"$PYTHON" -m pip install --quiet reportlab` before generating output. Also install `Pillow` for image handling.

### Photos not rendering in PDF (white rectangles)
- **Cause:** Photo path incorrect or file not accessible (G: drive not mounted).
- **Fix:** Verify photos exist at the expected path. Use absolute paths with forward slashes. If Drive unavailable, use dark gradient placeholders.

### PDF pages overlapping or misaligned
- **Cause:** Coordinate calculations not accounting for variable content height.
- **Fix:** Use measure-first layout pattern: calculate text height with `stringWidth()` and `wrap()` before placing elements. Never hardcode Y positions for variable-length content.

### Brief not approved before coding started
- **Cause:** Skipped the Activation step (confirm mode, narrative, sources).
- **Fix:** Always present the brief for approval first. This is the most common cause of full rebuilds. See Activation section above.

### Brand colors or fonts inconsistent
- **Cause:** Local brand constants diverged from metis-brand-identity canonical values.
- **Fix:** Verify against metis-brand-identity skill. Canonical: Dark Blue #20216f, Metis Green #3cdbc0, Open Sans primary, Calibri fallback.
