---
name: metis-whitepaper
description: >
  Produce Metis Strategy whitepapers, thought leadership PDFs with a specific
  structure, visual style, and editorial voice. Use whenever a user asks to
  create, draft, or structure a whitepaper, thought leadership paper, playbook,
  or long-form research report. Trigger on "whitepaper," "white paper,"
  "playbook," "thought leadership piece," "long-form report." Output is a
  polished, print-ready PDF via HTML/Playwright. Always validates against
  metis-brand-identity. Always use for whitepaper requests, even minimal ones.
  Do NOT use for: short reports or one-pagers (metis-pdf-creator); client
  proposals (metis-premier-proposal); PowerPoint decks (metis-pptx);
  browser presentations (metis-html-slides).
metadata:
  author: Metis Strategy
  version: 0.2.4
---

# Metis Strategy Whitepaper Skill

Metis whitepapers are published thought leadership documents that establish
Metis as the authoritative voice on a strategic topic for technology and digital executives.
The output is a **print-ready PDF** rendered from HTML via Playwright, closely matching
the visual style of published Metis whitepapers.

**Read all three reference files before producing output:**
- `references/content-patterns.md` — narrative structure, page templates, voice/tone, writing rules
- `references/page-layouts.md` — HTML/CSS templates for every page type, photo handling, rendering
- `references/diagram-builders.md` — SVG code for Metis framework diagrams (maturity ladders, matrices, phase flows, etc.)

The `scripts/` folder contains the rendering helper — use it directly rather than rewriting from scratch each time.

---

## Rendering Stack

| Layer | Tool | Notes |
|---|---|---|
| Layout | HTML + CSS | Full-bleed photos, multi-column text, dark navy pages, gradients |
| Typography | Google Fonts (Open Sans) | Loaded from CDN in the HTML head |
| Diagrams | Inline SVG | Built from code in `references/diagram-builders.md` |
| PDF export | Playwright (Node.js) | `scripts/render-whitepaper.js` handles this |

**One-time setup** (if Playwright is not yet installed in the working directory):
```bash
npm install playwright
npx playwright install chromium
```

---

## Brand Assets

All Metis brand assets live on the shared drive. Reference them using absolute `file://` paths in the HTML so Playwright can resolve them regardless of where `whitepaper.html` is saved.

**Brand root:** `G:\Shared drives\Knowledge Management\New Brand Assets`

| Asset | File | Usage |
|---|---|---|
| Trajectory device | `Graphic Devices\Metis Trajectory Device RGB.png` | Cover + section dividers as full-page background overlay at 30–35% opacity |
| Energy device | `Graphic Devices\Metis Energy Device RGB.png` | Background texture on content pages, 20–40% opacity |
| Arrow device (single) | `Graphic Devices\Metis SnglArrow Device RGB.png` | Inline callouts, pointing right only |
| Metis logo (white) | `Metis Strategy Logo\Metis Strategy White RGB logo.png` | Cover page, credits page |
| Metis logo (white-mint) | `Metis Strategy Logo\Metis Strategy White-Mint RGB Logo.png` | Credits/closing page (centered) |
| Metis logo (black-mint) | `Metis Strategy Logo\Metis Strategy Black-Mint RGB Logo.png` | Top-right corner on light-background pages |

**In HTML `src` attributes**, use the full `file://` URI with forward slashes and `%20` for spaces:
```
file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Graphic%20Devices/Metis%20Trajectory%20Device%20RGB.png
```

Or use the helper constant defined at the top of each generated HTML file:
```html
<script>
  const BRAND = "file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets";
</script>
```
Then reference assets as template literals in inline styles, or pre-resolve them before writing the HTML.

**Logo fallback:** If the logo cannot be resolved, render the wordmark as `<span style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.7);letter-spacing:0.06em;">METIS STRATEGY</span>`.

**Trajectory device rules (from brand guidelines):**
- Always points up and to the right — never rotate or flip
- On cover and divider pages: used as a full-page overlay at 30–35% opacity on top of a teal-to-navy gradient background (`linear-gradient(135deg, #20216f 0%, #256ba2 35%, #1a8a7a 60%, #3cdbc0 100%)`)
- Position: `position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0.3;pointer-events:none;`
- Do NOT place the trajectory device on the introduction/abstract page (page 2)
- Do not alter its colors

**Metis logo on every page:**
- Every page must display the Metis Strategy logo in the top-right corner
- On light-background pages: use `Metis Strategy Black-Mint RGB Logo.png`
- On dark-background pages: use `Metis Strategy White-Mint RGB Logo.png`
- CSS: `.metis-m { position: absolute; top: 22px; right: 28px; height: 22px; width: auto; }`
- Fallback: `<span style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.7);letter-spacing:0.06em;">METIS STRATEGY</span>`

---

## Input Folder Structure

The user provides a source folder. Typical structure:

```
whitepaper-source/
├── config.json              ← title, authors, orientation, short_title
├── brief.md                 ← overall outline and notes (optional)
├── content/                 ← one .md or .txt file per section
│   ├── 00-abstract.md
│   ├── 01-section1.md
│   └── ...
├── assets/
│   ├── photos/              ← .jpg/.png photos for page backgrounds/banners
│   ├── diagrams/            ← pre-made diagram images (optional)
│   └── data/                ← data files if charts need to be generated
│   └── brand/               ← auto-populated from skill bundle (trajectory_device, etc.)
└── (output goes here)
```

**On first run, copy the brand assets into the source folder:**
```bash
cp -r <skill-path>/assets/brand/ whitepaper-source/assets/brand/
```
This ensures Playwright can resolve `assets/brand/trajectory_device.png` relative to `whitepaper.html`.

**config.json format:**
```json
{
  "title": "AI Smart: Maximizing AI Value with a Balanced Strategy",
  "subtitle": "The Metis Strategy framework to guide technology executives through the ambiguity of AI",
  "short_title": "AI Smart",
  "orientation": "landscape",
  "authors": [
    { "name": "Chris Davis", "title": "West Coast Partner", "email": "chris.davis@metisstrategy.com", "phone": "+1 (609) 529-6452" }
  ],
  "contributors": ["Ben Calder", "Jasmeet Singh"],
  "cover_photo": "assets/photos/cover.jpg",
  "year": 2025
}
```

If the user has not organized their source folder this way, help them structure it before proceeding.

---

## Whitepaper Anatomy

| Page(s) | Type | Key Elements |
|---|---|---|
| 1 | Cover | Teal-to-navy gradient, B&W photo at 25% opacity, trajectory device overlay at 35%, eyebrow text, large title, Metis logo |
| 2 | Abstract / Introduction | Photo banner (no trajectory device), rule + SnglArrow + eyebrow, hook headline, 2-col body |
| 3–N | Section divider | Teal-to-navy gradient + trajectory device overlay at 30%, white section title text (no pill/background), bold pull statement |
| 4–N | Content pages | Various layouts — see `references/page-layouts.md` |
| N-1 | Conclusion | Recap eyebrow, insight headline, summary body |
| N | Credits / Closing | Dark navy, centered Metis Strategy White-Mint logo, info@metisstrategy.com, copyright line |
| N+1 | References / Endnotes | Numbered endnote entries (1–N) with author, title, year, and URL |

---

## Orientation

| Orientation | Page size | Use when |
|---|---|---|
| **Portrait (default)** | 816 × 1056px (8.5" × 11" at 96dpi) | Default for all whitepapers — dense, Word-document feel |
| **Landscape** | 1280 × 720px (or 13.33" × 7.5" at 96dpi) | Only when user specifically requests landscape or paper is diagram-forward |

---

## Brand Constants

```css
/* Copy directly into <style> tags */
:root {
  --dark-blue:  #20216f;
  --green:      #3cdbc0;
  --med-blue:   #256ba2;
  --gray:       #7b8692;
  --white:      #ffffff;
  --light-bg:   #f4f6fa;
  --teal-light: #e8f8f5;
}
```

**Footer format on every interior page:** `Page X | [Short Title]` — right-aligned, `var(--gray)`, 9pt.
**Top-right corner:** Small Metis M icon on every interior page.
**Never use** the BrandLine footer (`Driving change. Elevating leaders.`) inside a whitepaper.

---

## Step-by-Step Workflow

### 1. Gather requirements and length
Ask the user the following questions before proceeding:
- **Length**: "How long would you like the whitepaper to be? (e.g., 6–8 pages, 10–12 pages, 15+ pages)"
  - If the user does not answer or says "you decide," default to 15–28 pages
  - Adjust content density and number of sections to match the requested length
- **External research**: "Would you like me to conduct external research to support this whitepaper?"
  - If yes: "What topics, industries, or specific areas should I research? Any parameters or constraints?"
  - Perform web research, collect sources with URLs, and present findings to the user before outlining
  - **NEVER cite sources from McKinsey, Bain, BCG, or Deloitte** — these are Metis Strategy competitors. Use industry analysts (Gartner, IDC, Forrester), academic sources (arXiv, university research), developer surveys (Stack Overflow, JetBrains, GitHub), government/nonprofit research (DORA, Linux Foundation), and vendor research (Microsoft Research, etc.) instead.

### 2. Parse inputs
Read `config.json` and all content files in the source folder (if provided). Take inventory of available photos and assets. If content files are absent, ask the user for the content or offer to generate it from the brief.

### 3. Present outline and sources for approval
Produce a page-by-page outline table **before writing any content or HTML**. This is mandatory, not optional — even when the prompt seems detailed. Format:

| Page | Type | Layout | Headline / Content |
|---|---|---|---|
| 1 | Cover | Gradient + photo + trajectory overlay | Title, eyebrow, subtitle |
| 2 | Abstract | Photo banner + 2-col (no trajectory device) | Hook: "..." |
| 3 | Section I Divider | Gradient + trajectory overlay | "I. [Title]" / Pull statement |
| 4 | Content | Photo-left + text-right | "..." + pull quote + callout |
| ... | ... | ... | ... |
| N | Credits / Closing | Dark navy, centered logo + email | Metis Strategy logo, info@metisstrategy.com |
| N+1 | References | Numbered endnotes | Sources 1–N with URLs |

The **Layout** column is required. It prevents the common failure of defaulting to
identical two-column text pages throughout the whitepaper. Ensure layout variety: no
more than two consecutive pages should share the same layout type. See
"Visual Density Rules" below for the full list of layout types.

**In addition to the outline, present the user with a numbered list of all external sources you plan to cite**, including title, author/publisher, year, and URL. **Before presenting the list, fetch each URL and confirm it resolves to the expected document** — flag any 404, 403, redirect, or title/author mismatch for the user to resolve before drafting begins. Catching broken or hallucinated sources at this stage avoids rewriting claims later. This allows the user to approve, remove, or request additional sources before drafting begins.

**Wait for user approval** of both the outline and the source list before proceeding to step 4. Do not begin drafting until the user confirms.

### 4. Write content
For each section, follow the writing rules in `references/content-patterns.md`:
- Identify which pages need framework diagrams and note the diagram type
- Mark pull quotes with `[PULL QUOTE]...[/PULL QUOTE]`
- Note photo placements with `[PHOTO: description of ideal image]`
- Use numbered endnote citations throughout (see "Endnote Citation System" below)

### 5. Select / assign photos
Match available photos from `assets/photos/` to page placements. For missing photos, use a dark navy gradient placeholder — do not leave blank white space.

### 6. Build framework diagrams
For each diagram in the content, use the SVG generators in `references/diagram-builders.md`. If a diagram image already exists in `assets/diagrams/`, use it as an `<img>` tag instead.

### 7. Assemble HTML
Build a single HTML file (`whitepaper.html`) with one `.page` div per page. Use the CSS templates from `references/page-layouts.md`. Ensure:
- Metis Strategy logo appears in the top-right corner of every page
- Cover and divider pages use the teal-to-navy gradient with trajectory device overlay
- Introduction page (page 2) does NOT have the trajectory device
- All in-text citations use `<sup class="fn">N</sup>` superscript numbers
- A dedicated References/Endnotes page is included at the end with numbered entries
- Credits/closing page uses centered Metis logo + email (no author cards or "AI Working Group")

### 8. Citation audit & source verification

Two-part audit. Both parts are mandatory before the document is handed to
the user for review.

**Part A — Superscript coverage.** After assembling the HTML, perform a sentence-by-sentence audit of the entire document. For every sentence that contains a claim, statistic, quote, finding, or qualitative assertion that does not originate from Metis Strategy, verify that a `<sup class="fn">N</sup>` endnote superscript appears immediately after that sentence. Do not batch citations at the end of a paragraph — each cited claim gets its own superscript at the point of the claim.

- Walk through every page in order, reading each sentence
- Any externally-sourced number (e.g., "29% of developers…") must have a superscript
- Any paraphrased finding from a named source (e.g., "According to Stack Overflow…") must have a superscript
- Any quote from an external person or publication must have a superscript
- Qualitative claims attributed to external research (e.g., "studies show…") must have a superscript
- Metis-original insights, recommendations, and framework descriptions do NOT need citations
- After adding any missing superscripts, update the References/Endnotes page to include the new entries and verify all endnote numbers are sequential and match

First drafts routinely miss 5–15 citations.

**Part B — Double-source verification.** For each numbered endnote, confirm two things: (1) the URL resolves to the cited document, and (2) the in-text claim is actually supported by that document. Hallucinated or mis-attributed sources are invisible to the superscript audit and are the most common factual failure mode of AI-drafted whitepapers.

1. **Re-verify every URL resolves.** Fetch each endnote URL. Flag any 404,
   403, or redirect to a different document. Common failures:
   - Truncated URL slugs (e.g. `.../2024-04-11` missing the title slug)
   - `arxiv.org/abs/NNNN.NNNNN` where the ID was hallucinated — verify
     author and title match what the paper actually shows
   - IDC `my.idc.com/getdoc.jsp?containerId=...` pages that return the
     wrong document when the container ID is slightly off
2. **Pull a verbatim quote for every in-text claim.** For each `<sup
   class="fn">N</sup>` in the body, open the source and extract the exact
   sentence(s) that support the claim. Record them in a verification log,
   one entry per endnote. If you cannot find a supporting quote in the
   source, the claim is unsupported — rewrite it to match what the source
   actually says, or replace the source.
3. **Double-source anything behind an auth wall.** Gartner, IDC, and some
   vendor pages block automated fetchers (403). For these, confirm the
   claim via a second independent source (reputable coverage, press
   release cache, or the vendor's own blog). Never cite a source you
   cannot read.
4. **Watch for these hallucination patterns:**
   - Author names attached to arXiv papers — verify every time. "Et al."
     citations are especially prone to fabrication
   - "Peer-reviewed study" language applied to an arXiv preprint (see
     Critical Rule #19)
   - Exact-decimal figures ("4.2 percentage points", "31.9% CAGR") that
     sound authoritative — check they are present verbatim in the source
   - Round-number claims ("30% → 60% acceptance rate") that feel like
     stylized talking points rather than paper findings
   - Quotes attributed to a paper whose abstract does not contain them
5. **Deliverable:** a verification log with one entry per endnote, showing
   the verbatim source quote(s) supporting each claim. Attach it to the
   draft when handing the document to the author for review.

This step typically surfaces 2–5 source-level issues per draft. Fix them by rewriting the claim, swapping the source, or removing the citation — not by ignoring them.

### 9. Human review (spot edits)
Before rendering the final PDF, the user may want to edit wording, swap data points, or adjust phrasing. The HTML file is the editable source. Guide them:

**How to spot-edit `whitepaper.html`:**
1. Open the file in **Notepad** or **VS Code** (any text editor works)
2. Use **Find** (`Ctrl+F`) to locate the text you want to change — search for a unique phrase from the sentence
3. Edit the text directly; the surrounding HTML markup does not need to change for wording edits
4. Save (`Ctrl+S`), then re-render the PDF

**What's safe to edit in the HTML:**
- Any text between `>` and `<` tags — this is the content
- Numbers, statistics, company names, dates, titles
- Pull quotes, callout box text, footer page numbers

**What to leave alone (or ask the agent to change):**
- CSS class names and `style=""` attributes — these control layout
- SVG coordinates — these control diagram shapes
- The `<head>` section — this loads fonts and base styles

If the user has many edits, it's faster to give them back as a list and have the agent apply them all at once, then re-render.

### 10. Render to PDF
Run the renderer after edits are complete. Use Playwright (Node.js or Python):
```bash
node scripts/render-whitepaper.js whitepaper.html output.pdf portrait
```
Or with Python Playwright if Node.js is unavailable:
```python
from playwright.sync_api import sync_playwright
# See scripts/render-whitepaper.js for equivalent Python setup
```
The script handles page sizing, print backgrounds, and output path.

### 11. Final check and deliver
Open the PDF. Verify: no text overflow, photos loaded, trajectory device visible on cover/dividers only, Metis logo on every page, diagrams rendered, footer and page numbers correct, endnote numbers match References page. Fix any issues in the HTML, re-render, and deliver.

---

## Critical Rules

Read `references/critical-rules.md` for the full list of 19 mandatory rules. The top priorities:

1. **`Source: Metis Strategy`** caption below every framework diagram.
2. **Section divider page** before every major section (gradient + trajectory overlay).
3. **Produce the outline AND source list first**, always, before any content or HTML. Wait for user approval.
4. **Citation audit & source verification** after assembly (Parts A and B). First drafts routinely contain 2-5 hallucinated sources.
5. **Never cite McKinsey, Bain, BCG, or Deloitte** (competitors).
6. **Em dashes: one per page maximum.**
7. **Ask about length** before starting.

---

## Visual Density, Citations, and Rendering

Read `references/rendering-notes.md` for the complete visual density rules, endnote citation system, photo library, layout variety requirements, callout/metric card patterns, and Playwright rendering notes.

Key points:
- Every content page needs at least one visual anchor (photo, diagram, callout, pull quote, or metric cards).
- No more than two consecutive pages with the same layout type.
- Use real B&W photos from `G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\Metis PPT Images\`, not gradient placeholders.
- All citations use numbered endnotes with `<sup class="fn">N</sup>`, collected on a dedicated References page.
- Playwright landscape bug: do NOT set `landscape: true` when using explicit landscape dimensions.

---

## Troubleshooting

### Playwright not rendering
- **Cause:** Playwright or Chromium not installed in the working directory.
- **Fix:** Run `npm install playwright && npx playwright install chromium` in the working directory. Verify Node.js is available.

### Citations showing as broken links
- **Cause:** First drafts routinely contain 2-5 hallucinated or mis-attributed sources.
- **Fix:** Run Part B of the citation audit (source verification) before finalizing. Fetch each URL and confirm it resolves. See Step 8 in the workflow above.

### PDF pages blank or cut off
- **Cause:** CSS print media queries or page-break rules misconfigured.
- **Fix:** Ensure `page-break-before: always` is applied to each `.page` div. Check that the HTML has no unclosed tags that break the page flow.

### Trajectory device not visible on cover
- **Cause:** `file://` URI path has incorrect encoding or Drive not mounted.
- **Fix:** Verify `G:\Shared drives\Knowledge Management\New Brand Assets\Graphic Devices\Metis Trajectory Device RGB.png` exists. Use `%20` for spaces in `file://` URIs.

### Output file too large (>15 MB)
- **Cause:** Embedded photos without compression.
- **Fix:** 8-12 MB is normal for photo-heavy whitepapers. If excessive, compress photos before embedding or reduce photo resolution to 150 DPI for print.
