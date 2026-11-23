# SOW Drafting Patterns

## Table of Contents
1. Template Extraction
2. Placeholder Replacement
3. Deliverables Table Construction
4. Invoice Schedule Table
5. Milestone Formatting
6. Section Numbering & Cross-References
7. Style & Formatting Rules
8. Scope Comparison Methodology
9. Standard Deliverable Formats
10. Standard Review & Acceptance Language

---

## 1. Template Extraction

Read the client SOW template with python-docx and catalog:
- Every paragraph with its style (Heading 1 = section header, Normal = body text)
- Placeholder patterns: `_____`, `[______]`, `$_______`, `ADD INVOICING SCHEDULE`
- Table structures (representative tables, signature blocks)
- Whether sections are numbered in the template or need numbering added

Read the proposal with pdfplumber (for PDF) or python-docx (for DOCX):
- Pricing options table (scope, duration, fees, deliverable matrix)
- Deliverable names and descriptions per workstream
- Key activities per workstream
- Timeline/Gantt information
- Team structure and working assumptions
- Client contacts named in the proposal

## 2. Placeholder Replacement

### Quote handling
Templates mix smart quotes and straight quotes unpredictably. Always attempt replacement with both:
```python
# Try straight quotes first
text.replace('("Supplier")', '("Supplier")')
# If that fails, try smart quotes
text.replace('\u201c\u201d', ...)
```

### Run-level replacement
When a placeholder spans multiple runs (common in Word), collapse into the first run:
```python
para.runs[0].text = new_text
for run in para.runs[1:]:
    run.text = ""
```

### Common placeholders to fill
| Placeholder | Source |
|---|---|
| SOW number (PRA_____) | Ask the consultant |
| Agreement number | Ask the consultant |
| Supplier name + entity type | From `firm-metadata.md` (Metis Strategy LLC, a Delaware LLC) |
| Supplier address | From `firm-metadata.md` |
| Supplier TIN/EIN | From `firm-metadata.md` |
| MSA date | Ask the consultant |
| SOW Effective Date | Ask the consultant |
| End date | Calculate from start date + duration in weeks |
| Fee amount ($_______) | From selected pricing option |
| Supplier Representative | Ask the consultant (varies per engagement) |
| Client Representative | From proposal's client contacts |

## 3. Deliverables Table Construction

Build a real Word table — never use bullet points or pseudo-table formatting. Structure:

| Column | Width | Content |
|---|---|---|
| Workstream | ~3cm | Group name, only shown on first row of group |
| Deliverable | ~3.5cm | Bold, specific deliverable name |
| Format | ~3.5cm | See Standard Deliverable Formats below |
| Level of Detail | ~5cm | What the deliverable contains, specific enough for acceptance |
| Target Audience | ~3.5cm | Who receives/reviews the deliverable |

### Table formatting
```python
# Header row: dark blue with white text
shading = OxmlElement('w:shd')
shading.set(qn('w:fill'), '1F3864')
shading.set(qn('w:val'), 'clear')
cell._tc.get_or_add_tcPr().append(shading)
run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

# All text: Arial 8pt in tables
run.font.name = 'Arial'
run.font.size = Pt(8)
```

### Table width
Set to 100% page width:
```python
tblW = OxmlElement('w:tblW')
tblW.set(qn('w:type'), 'pct')
tblW.set(qn('w:w'), '5000')
```

### Positioning
After creating a table (which appends to end of document), move it to the correct position:
```python
target_para._p.addnext(table._tbl)
```

## 4. Invoice Schedule Table

Use a 3-column table (Invoice #, Amount, Due Date) with the same dark blue header styling.

Key rules:
- Monthly invoicing = equal installments over the engagement duration
- First invoice due at end of first month, not at kickoff (unless explicitly agreed)
- Last invoice due date should align with engagement end date
- Verify the total of all installments equals the engagement fee exactly
- Check MSA payment terms before including Net 30/45/60 language in the SOW — if the MSA
  already governs payment terms, don't override them in the SOW

## 5. Milestone Formatting

Use separate paragraphs for each milestone phase, not one giant block:
```
Week 4: [Deliverable 1], [Deliverable 2]
Week 8: [Deliverable 3], [Deliverable 4]
...
```

If the client has provided updated milestones, use those. Otherwise derive from the proposal's
timeline/Gantt chart, grouping deliverables by their completion week.

## 6. Section Numbering & Cross-References

Number all Heading 1 sections sequentially: 1.0, 2.0, etc.

After numbering, scan the document for any cross-references to section letters or names
(e.g., "Section C above", "as described in the Deliverables section") and update them to use
the correct section number (e.g., "Section 3.0 (Deliverables) above").

## 7. Style & Formatting Rules

The most common formatting issue: template placeholders styled as Heading 1 get replaced with
body text but retain the bold/Heading 1 style.

**Rule:** Only actual section headers should be Heading 1. All body text, including filled-in
placeholder content, should be Normal style with Arial 11pt, not bold:
```python
para.style = doc.styles['Normal']
for run in para.runs:
    run.bold = False
    run.font.name = 'Arial'
    run.font.size = Pt(11)
```

Watch for:
- Template "numbered list" items that are actually Heading 1 — convert body text ones to Normal
- Highlighted text (yellow) from template instructions — remove all highlighting
- Blank paragraphs with Heading 1 style — convert to Normal

## 8. Scope Comparison Methodology

After drafting the SOW deliverables, compare each one against the proposal's original language:

For each deliverable:
1. Find the matching deliverable in the proposal
2. Compare the SOW's description against the proposal's activities and deliverable name
3. Identify any language in the SOW that goes beyond the proposal
4. Classify the risk: Low (clarifying detail), Medium (could be read as new scope), High (clearly
   new commitment)

Present as a table to the consultant before finalizing:
| Deliverable | Proposal Language | SOW Language | Risk |

Common patterns that signal scope creep:
- Adding "at least N" to quantities the proposal left unspecified
- Naming specific output types (e.g., "town hall content") not in the proposal
- Adding measurement/metrics language ("adoption metrics", "KPI tracking")
- Including formal assessment activities ("readiness evaluation", "maturity assessment")
  when the proposal used softer language ("identify", "assess")

Recommended softening techniques:
- "formal assessment" → "high-level assessment"
- "metrics" → "suggested indicators"
- "at least one cycle" → "one (1) cycle"
- "detailed plan" → "plan"

## 9. Standard Deliverable Formats

| Deliverable Type | Typical Format |
|---|---|
| Capability maps, org structures | PowerPoint slides or digital whiteboard (e.g., Miro) |
| Assessments, strategies | PowerPoint slides |
| Frameworks, plans, playbooks | Word document or PowerPoint slides |
| Financial/funding models | PowerPoint slides with supporting Excel model |
| Workforce/resourcing plans | Word document with supporting Excel model |
| Communications materials | PowerPoint slides |
| Facilitation materials | Word document or PowerPoint slides; facilitation guides |

Always include: "Alternative formats may be provided upon mutual agreement between Supplier
and Lumen."

## 10. Standard Review & Acceptance Language

### Review Cycle (3-stage)
> Each deliverable will follow a three-stage review process: (1) Initial Draft — Supplier delivers
> a working draft for [Client] core team review and feedback; (2) Revised Draft — Supplier
> incorporates [Client] feedback and delivers a revised version for final review; (3) Final
> Deliverable — Supplier delivers the final version incorporating all agreed-upon revisions.

### Acceptance Criteria
> Each deliverable will be deemed accepted upon written approval by the [Client] project sponsor
> (or designated representative) within five (5) business days of final delivery. If no response
> is received within the five (5) business day period, the deliverable will be deemed accepted.
> Rejection must include specific, actionable feedback aligned to the scope defined in this SOW.
