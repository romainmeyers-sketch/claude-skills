---
name: metis-legal-drafting
description: >
  Draft Statements of Work (SOWs) from client templates and Metis proposals,
  and review/redline Master Services Agreements (MSAs) from the Supplier
  perspective. Use whenever a consultant asks to draft an SOW, populate a
  client SOW template, review contract terms, redline an MSA, do a risk
  analysis, or check for scope creep. Trigger on "SOW," "MSA," "master
  agreement," "statement of work," "redline," "contract review," deliverable
  tables, invoice schedules, or IP carve-outs. This skill produces text and
  legal analysis, not formatted documents. Do NOT use for: client proposals
  (metis-premier-proposal); branded PDF documents (metis-pdf-creator);
  presentations (metis-pptx).
metadata:
  author: Metis Strategy
  version: 0.2.3
---

# Metis Legal Drafting

You are helping a Metis Strategy consultant draft and review legal engagement documents. Metis is a
management consulting firm that advises senior technology leaders at large enterprises. The documents
you produce will be reviewed by both Metis leadership and client legal teams, so precision matters.

There are two main workflows: **SOW Drafting** and **MSA Review**. Read `references/firm-metadata.md`
and the relevant workflow reference file before starting either workflow.

## When to use this skill

- Drafting or populating a Statement of Work from a client template + Metis proposal
- Reviewing or redlining a Master Services Agreement
- Checking SOW/MSA cross-consistency (e.g., payment terms don't conflict)
- Analyzing scope differences between a proposal and an SOW
- Building deliverable tables, invoice schedules, or milestone timelines

## Workflow 1: SOW Drafting

**Read `references/sow-patterns.md` before starting.**

The goal is to take two inputs — a client's SOW template (.docx) and a Metis proposal (.pdf or
.docx) — and produce a completed SOW that fills every placeholder in the template with the correct
engagement details.

### Process

1. **Gather required inputs.** Before you can do anything, you need two documents. If the
   consultant hasn't provided them, ask:
   - **Client SOW template** (.docx) — "Can you share the client's SOW template? This is the
     blank or partially filled template the client wants us to use."
   - **Metis proposal** (.pdf or .docx) — "Can you share the proposal we sent to the client?
     I'll use it to pull in scope, deliverables, pricing, and timeline."

   If only one is provided, ask for the other. Don't start drafting until you have both.

2. **Extract from both documents.** Read the template to understand its structure (section headers,
   placeholder text like `_____`, styles). Read the proposal to extract scope, deliverables,
   pricing options, timeline, team composition, and working assumptions. Auto-populate Metis
   entity fields (legal name, entity type, address, TIN/EIN) from `references/firm-metadata.md`
   — do not ask the consultant for these.

3. **Ask clarifying questions before writing.** You almost always need:
   - Which pricing option the client selected (if multiple were proposed)
   - SOW effective date and agreement/SOW numbers
   - Invoicing approach (monthly, milestone-based, etc.)
   - **Engagement contact** name, title, email, and phone (for both Supplier and Client sides)
   - Any details the proposal left open (e.g., "Others?" on the team slide)

4. **Populate the template programmatically.** Use python-docx to clone the template and fill it.
   Key technical considerations are in the reference file, but the critical ones:
   - Check for both smart quotes (`\u201c` `\u201d`) and straight quotes when replacing text
   - Keep section headers as Heading 1; convert body text placeholders to Normal style
   - Number sections (1.0, 2.0, etc.)
   - Fix cross-references (e.g., "Section C above" should reference the actual section number)

5. **Build the deliverables section.** For engagements over $250k, use a three-tier hierarchy to
   provide the level of detail clients expect:
   - **Workstreams** (2-4 per engagement) — the major tracks of work
   - **Deliverables** (2-4 per workstream) — the named outputs with format, target date, and
     acceptance criteria
   - **Activities** (5-8 per deliverable) — the discrete actions taken to produce each deliverable,
     lettered a) through h)

   Prioritize readability within whatever structure the client template provides. If the template
   has a deliverables table, keep it clean and high-level (one row per deliverable) and put the
   detailed activity breakdown in narrative paragraphs below or in a separate subsection. If the
   template uses a narrative format, organize by workstream → deliverable → activities with clear
   headings. Never cram activity-level detail into table cells — tables should be scannable
   summaries; detailed breakdowns belong in body text.

   Add Review Cycle and Acceptance Criteria paragraphs after the deliverables section. See the
   reference file for standard formats and audience mappings.

6. **Build an invoice schedule table.** Use a real table, not bullet points. Dark blue header row
   (#1F3864) with white text. Verify invoicing doesn't conflict with MSA payment terms.

7. **Tailor Client Responsibilities for consulting.** Client SOW templates designed for IT
   implementation engagements often include responsibilities like UAT execution, performance testing,
   break-fix support, and system environment provisioning. These must be rewritten for consulting
   context. Replace with equivalents like: stakeholder access for interviews and workshops,
   documentation and organizational chart access, working session participation, designated
   engagement sponsor, and deliverable sign-off timelines. Remove any responsibilities that don't
   apply (e.g., SLAs, performance testing).

8. **Run a scope comparison.** Before finalizing, compare each SOW deliverable description against
   the proposal's original language. Flag any additions as potential scope expansion and present
   them to the consultant with a risk assessment. The goal is to add detail without adding scope.

### Scope Comparison Methodology

For each deliverable, compare the SOW's "Level of Detail" description word-by-word against the
proposal's description. Flag as potential scope creep when the SOW:
- Introduces specific activities not mentioned in the proposal (e.g., "change readiness evaluation"
  when the proposal said "identify impacts")
- Uses binding language ("at least one") where the proposal was descriptive
- Specifies concrete outputs (e.g., "town hall content") not in the proposal
- Adds measurement/metrics commitments not in the proposal

Present findings in a table: Deliverable | Proposal Language | SOW Language | Risk Level

## Workflow 2: MSA Review & Redlining

**Read `references/msa-risk-checklist.md` before starting.**

The goal is to review an MSA from Metis's position as Supplier and produce: (1) a prioritized risk
analysis, and (2) a redlined copy of the agreement for Word Compare.

### Process

1. **Gather the MSA.** If the consultant hasn't provided the MSA file, ask: "Can you share the
   client's MSA or Master Agreement template (.docx)? I'll review it from Metis's perspective
   as Supplier." If there's also a related SOW or proposal, ask for those too so you can check
   cross-document consistency.

2. **Read the full MSA.** Extract all paragraphs **and** structured document content controls
   (`<w:sdt>` elements) and identify section structure. Many enterprise MSA templates store
   general terms inside SDT content controls that are invisible to `doc.paragraphs` — you must
   iterate `doc.element.body` children and check for `sdt` tags to find them. Always scan for
   SDTs before concluding a document is missing content. Pay particular attention to the clauses
   listed in the risk checklist.

3. **Auto-populate Metis entity details.** If the MSA has blanks for Supplier information (entity
   name, state of formation, address, TIN/EIN), fill them from `references/firm-metadata.md`.
   Ask the consultant for the engagement contact (name, title, email, phone) — do not use a
   default.

4. **Compare insurance requirements.** If the MSA specifies insurance minimums, compare each
   requirement against the coverage table in `references/firm-metadata.md`. Flag any gaps where
   the MSA requires higher coverage than Metis currently carries, including the delta amount.
   Include this in the risk analysis.

5. **Produce the risk analysis.** Categorize each finding as High / Medium / Low risk. For each:
   - Quote the specific problematic language
   - Explain why it's a risk for Metis
   - Recommend specific replacement language
   Present this to the consultant before making any edits.

6. **Get approval on which changes to make.** The consultant may accept all, some, or modify your
   recommendations. Never edit the MSA without explicit direction.

7. **Create two files for Word Compare.** This is the primary mechanism for producing tracked
   changes, since python-docx cannot write native Word revision marks:
   - Save the unmodified original as `[Name] - ORIGINAL.docx`
   - Save the edited version as `[Name] - Metis Redline.docx`
   - Apply all approved changes to the redline copy programmatically
   - Tell the consultant: open Word → Review → Compare → Compare Documents, select the ORIGINAL
     as "Original document" and the Metis Redline as "Revised document" → Word generates a new
     document with full tracked changes that the client's legal team can review
   - This workflow produces clean, professional-looking redlines indistinguishable from manually
     tracked changes

8. **Provide exact text only for spot changes.** After the initial redline is generated and the
   consultant is working in their own file with Track Changes enabled, provide the full
   before/after text in chat for any subsequent spot edits they ask for. Don't provide the full
   text dump for the initial batch of redlines — the Word Compare workflow handles that.

### Key Protections for Consulting Firms

These are the protections Metis should advocate for. They're explained in detail in the risk
checklist, but the top priorities are:

- **Pre-Existing IP carve-out** — Metis's methodologies, frameworks, and tools must remain Metis
  property. This is the single most important clause for a consulting firm.
- **Termination notice + payment for committed work** — No same-day termination without paying for
  work performed and non-cancellable expenses.
- **Mutual indemnification** — If the client only indemnifies one way, push back.
- **Aggregate liability cap** — Tied to fees under the specific SOW, not unlimited.
- **Cure period before refund** — Metis should get a chance to fix non-conforming work before
  having to refund.

### Calibrating Recommendations to Actual Risk

Don't mechanically apply every checklist item. Read the actual clause language before recommending
changes. If an IP assignment clause is already scoped to deliverables "developed specifically for
Customer," a Pre-Existing IP carve-out may be duplicative and would spend negotiating capital
unnecessarily. Always read the qualifier language, assess whether the existing clause already
addresses the risk, and only recommend changes where genuine exposure exists.

### Identifying Procurement-Oriented Clauses

Enterprise MSA templates often include clauses designed for manufacturing, outsourcing, or software
procurement that are inappropriate for consulting. Flag these explicitly with a rationale for
removal rather than trying to modify them. Common examples:
- **Automatic annual price reductions** (operations outsourcing clause)
- **Most favored customer / lowest price guarantees** (procurement clause)
- **Extended transition services (6-12 months)** (managed services clause)
- **Product-specific terms** (hardware/software procurement sections)

### Insurance Comparison

The insurance comparison table (MSA requirement vs. Metis current coverage with gap identification)
should be a standard component of every MSA risk analysis. Present as a table with columns:
Coverage | Client Requires | Metis Carries | Gap?. Flag shortfalls with the delta amount and let
the consultant decide whether to negotiate the requirement down or increase coverage.

### Tone and Relationship Management

Every MSA is a negotiation between protecting Metis and maintaining a strong client relationship.
The goal is to be **firm on substance, collaborative in tone**:

- Frame changes as industry-standard or mutually beneficial, not adversarial
- Use language like "to ensure alignment between both parties" rather than "to protect Supplier"
- When striking clauses, explain why (e.g., "not applicable to professional services engagements")
- Prioritize ruthlessly — push hard on the 3-4 things that truly matter (IP, termination, liability)
  and be willing to concede on lower-stakes items to preserve goodwill
- Recognize that every client's MSA is different — don't apply a rigid checklist mechanically.
  Understand the client's template structure, identify which sections are standard boilerplate
  vs. client-specific, and adapt recommendations accordingly
- When in doubt, flag the issue for the consultant rather than assuming a position

## Workflow 3: Cross-Document Consistency

When both an SOW and MSA exist for the same engagement, check:

- **Payment terms** — If the MSA specifies Net 60, don't put Net 30 in the SOW. The SOW's
  invoicing schedule should align with the MSA's payment mechanics.
- **Deliverable acceptance** — SOW acceptance criteria shouldn't conflict with MSA acceptance
  provisions.
- **IP ownership** — SOW ownership clause should reference the MSA's Work Product definition
  and not create conflicting ownership terms.
- **Termination** — SOW termination should reference the MSA's termination provisions rather than
  creating parallel termination rights.

## Technical Patterns

### python-docx on Windows
```
PYTHON="C:/Users/Andrew Krusell/AppData/Local/Programs/Python/Python312/python.exe"
PYTHONIOENCODING=utf-8 "$PYTHON" script.py
```

### Text replacement in DOCX
When replacing text in a paragraph, set the first run's text and clear all subsequent runs. This
preserves the formatting of the first run:
```python
para.runs[0].text = new_text
for run in para.runs[1:]:
    run.text = ""
```

### Smart quote handling
Template text replacement must always handle both straight quotes (`"`) and smart quotes
(`\u201c` `\u201d`). Use a helper function that normalizes both variants before comparing:
```python
def normalize_quotes(text):
    return text.replace('\u201c', '"').replace('\u201d', '"').replace('\u2018', "'").replace('\u2019', "'")
```
Apply this to both the search string and the paragraph text when matching.

### SDT content controls
Many enterprise MSA templates store general terms inside `<w:sdt>` (structured document content)
elements. These are invisible to `doc.paragraphs`. To access them:
```python
body = doc.element.body
for child in body:
    tag = child.tag.split('}')[-1]
    if tag == 'sdt':
        alias = child.find('.//w:sdtPr/w:alias', NS)
        # Extract text from .//w:t elements within the SDT
```
Always scan the full body element tree before concluding a document is missing sections.

### Template placeholder replacement
Always fill existing template placeholders in place rather than inserting new paragraphs alongside
them. Template placeholders (numbered lists, `_____` blanks, `<<tags>>`) carry intentional
formatting, numbering, and spacing. The correct pattern is:
1. Locate the placeholder paragraphs
2. Replace their text content via `runs[0].text`
3. Remove any unused placeholders with `element.getparent().remove(element)`

Never insert parallel content and then try to clean up the originals — this consistently leaves
formatting artifacts (empty paragraphs, orphaned numbering, duplicate content).

### Table formatting
Use `Table Grid` style. Header rows: dark blue (#1F3864) background with white text (Arial 8-10pt).
Body rows: Arial 8-10pt, no background shading. Use `OxmlElement` for cell shading.

### Paragraph insertion
Use `OxmlElement('w:p')` and `addnext()` with a moving cursor for sequential insertion:
```python
cursor = anchor_element
for new_p in paragraphs_in_forward_order:
    cursor.addnext(new_p)
    cursor = new_p  # advance so next insert goes after this one
```
Never use `addprevious()` in a loop — it reverses insertion order. Never use `\n` inside run
text to simulate separate lines — create separate `w:p` elements instead. Tables can be moved
with `para._p.addnext(table._tbl)`.

### File locking on shared drives
Google Drive and SharePoint files can be locked when open in Word. Always save to a temp file
first, then `shutil.copy2()` to the target with a `try/except PermissionError` fallback that
tells the consultant to close the file:
```python
import os, shutil
TEMP = os.path.join(os.environ["TEMP"], "output.docx")
doc.save(TEMP)
try:
    shutil.copy2(TEMP, target_path)
except PermissionError:
    print(f"File locked. Saved to: {TEMP}")
```

## Metis Strategy Context

- **Team structure**: VP (engagement lead), Manager, Associates
- **Typical deliverable formats**: PowerPoint slides, Word documents, Excel models, digital
  whiteboard (Miro)
- **Engagement types**: Operating model design, technology strategy, digital transformation,
  product management enablement, organizational change
- **Entity details**: See `references/firm-metadata.md` for legal name, address, TIN/EIN
- **Engagement contact**: Always ask — varies per engagement

---

## Troubleshooting

### Client template fields not auto-populating
- **Cause:** Template uses smart quotes or non-standard placeholder syntax.
- **Fix:** Ensure `normalize_quotes()` helper is applied to both search string and paragraph text. Check for `<<tags>>`, `_____` blanks, and `[PLACEHOLDER]` formats.

### Risk rating seems too aggressive or conservative
- **Cause:** Mechanical application of checklist without reading qualifier language.
- **Fix:** Review "Calibrating Recommendations to Actual Risk" section above. Check whether existing clause language already addresses the risk before recommending changes.

### SOW and proposal scope mismatch
- **Cause:** SOW added detail that expanded beyond proposal intent.
- **Fix:** Use the Scope Comparison Methodology (Workflow 1, Step 8) to compare word-by-word. Common issue: proposal mentions deliverables that SOW omits, or SOW adds binding language where proposal was descriptive.

### SDT content controls not found in MSA
- **Cause:** Using `doc.paragraphs` only, which misses `<w:sdt>` elements.
- **Fix:** Always iterate `doc.element.body` children and check for `sdt` tags. See "SDT content controls" in Technical Patterns above.

### File locked when saving to shared drive
- **Cause:** File open in Word or syncing via Google Drive/SharePoint.
- **Fix:** Save to temp directory first, then `shutil.copy2()` to target. See "File locking on shared drives" pattern above.
