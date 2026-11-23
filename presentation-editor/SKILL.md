---
name: presentation-editor
description: >
  Edits presentations that already exist. Turns a short informal ask ("add
  System Demo to the E2E view", "move this after Sprint Review", "add this
  metric", "make this less crowded", "fix the spacing", "tighten slide 4") into
  a precise change brief, makes the smallest correct edit, and runs QA proving
  nothing else moved. Works on .pptx files, the PowerPoint add-in, Claude Design
  and canvas surfaces, HTML artifact decks, and dashboard visuals. Protects
  everything the user did not ask to change, including reviewer comments, slide
  order, template, and the formatting of untouched elements. Trigger whenever
  the user asks to change, add to, move, remove, reword, restyle, compress or
  clean up something in a deck or design that already exists, especially when
  the request is one line long. Do NOT use for: building a new deck from
  scratch (metis-pptx); whitepapers (metis-whitepaper); PDFs
  (metis-pdf-creator); SOWs or MSAs (metis-legal-drafting); prose rewriting with
  no visual surface (metis-humanizer).
metadata:
  author: Romain Meyers / Metis Strategy
  version: 1.0.0
---

# Presentation Editor

**Scope: decks and designs that already exist.** Building something from
scratch is a different job and belongs to the builder skills, see section 8.
Adding a slide to an existing deck is an edit and stays here.

Three jobs, in this order, every time:

1. **Prompt Engineer.** Turn a short informal ask into an explicit change brief.
2. **Presentation / Design Editor.** Make that change, and only that change.
3. **Quality Controller.** Prove the change landed and prove nothing else moved.

## Prime directive

> Understand the intent, make only the appropriate changes, and protect
> everything the user did not ask you to change.

When intent and preservation pull against each other, preservation wins. A
correct edit that also silently reflowed four other slides is a failed edit.

---

## 0. The loop

```
LOCATE    -> what artifact, which surface, which element
READ      -> inventory the current state (blocking gate, never skip)
TRANSLATE -> write the Change Brief
SCOPE     -> declare the blast radius before touching anything
EDIT      -> smallest diff that satisfies the brief
QA        -> verify the intended change, then verify nothing else moved
REPORT    -> one short block: what changed, what was protected, what to check
```

Short prompts are the normal case, not an exception. Do not ask the user to
write a longer prompt. Do the translation yourself, state your reading in one
line, and proceed.

---

## 1. LOCATE: target and surface

Work out **which artifact** and **which surface** before anything else.

| Signal | Surface | Playbook |
|---|---|---|
| A `.pptx` / `.potx` path, filename, or "the deck in Downloads" | Existing PowerPoint file | [A](references/surface-playbooks.md#a-existing-pptx-file) |
| The deck is open in PowerPoint and you act through the Office add-in, no filesystem access to the file | PowerPoint add-in | [B](references/surface-playbooks.md#b-powerpoint-add-in-live-deck) |
| Claude Design, a canvas, a design doc, a Miro board, or design MCP tools are in session | Claude Design / canvas | [C](references/surface-playbooks.md#c-claude-design-and-canvas-surfaces) |
| A published artifact URL, or an `.html` deck file | HTML artifact deck | [D](references/surface-playbooks.md#d-html-artifact-decks) |
| A chart, KPI row, metric tile, status board, scorecard | Dashboard / visual | [E](references/surface-playbooks.md#e-presentation-style-dashboards-and-visuals) |
| Nothing exists yet | Not this skill: hand off | [F](references/surface-playbooks.md#f-new-presentation-creation-not-this-skill) |

**Ambiguous target.** If two artifacts could plausibly be meant, prefer in this
order: the file edited most recently in this session, then the file the user last
named, then the most recently modified matching file on disk. Name the one you
picked in the report. Only ask when the candidates sit in different client
folders or different formats, because guessing wrong there wastes real work.

**"This", "that", "here", "it".** Resolve from the last thing the user pointed
at: the slide you last showed, the element last discussed, the file last opened.
See [intent-translation.md](references/intent-translation.md#resolving-this-that-here).

---

## 2. READ: ground truth before any edit (blocking gate)

**Never edit an artifact you have not inspected in this session.** Not a single
text run. Your model of the deck from three turns ago is not ground truth, and a
deck the user touched in PowerPoint since then has moved on.

For a `.pptx` or an `.html` deck:

```bash
PYTHON="C:/Users/romain/AppData/Local/Programs/Python/Python312/python.exe"
SKILL="$HOME/.claude/skills/presentation-editor"
"$PYTHON" "$SKILL/scripts/inventory.py" "deck.pptx" -o before.json --print
```

Write the inventory to a file in the scratchpad, not just to the screen. It is
your **before snapshot** for QA, and without it step 6 cannot run.

For add-in and canvas surfaces, read the live state through that surface's own
tools before touching anything.

---

## 3. TRANSLATE: the Change Brief

This is the Prompt Engineer job. Write the brief internally every time, even for
a three-word ask. Five fields:

| Field | Question it answers |
|---|---|
| **Target** | Which artifact, which slide or section, which element. Be exact: "slide 7, the 4-column process row, column 3". |
| **Action** | One verb from the taxonomy: add, insert, move, reorder, remove, replace, reword, compress, expand, restyle, align, emphasize, split, merge. |
| **Content** | The literal text, number, or object involved, and where it came from. |
| **Constraints** | What must stay true: template, layout, column count, brand tokens, slide count, numbering, sibling formatting. |
| **Blast radius** | The complete list of things allowed to change. Anything not on this list is a defect if it moves. |

Then show the user **one line**, not the table:

> Adding "System Demo" as a fifth step in the E2E flow on slide 6, resizing the
> five chevrons to keep the same band width. Nothing else on the slide changes.

Verb taxonomy, deixis rules, and worked examples of short prompts live in
[intent-translation.md](references/intent-translation.md).

### The one-question rule

Ask at most **one** clarifying question, and only when two readings would produce
materially different work that is not cheap to undo. Otherwise pick the most
likely reading, state it in the one-liner, and proceed. A stated assumption the
user can correct in four words beats a question that stalls the task.

Ask when:
- The change would delete content that exists nowhere else.
- The target could be two different client deliverables.
- The user references content you do not have ("add this metric" with no metric
  in the thread, no attachment, and no obvious source).

Never ask for:
- Formatting details you can read off the neighbouring elements.
- Confirmation that an explicit instruction means what it says.
- Permission to do the thing you were just asked to do.

---

## 4. SCOPE: the preservation contract

Fix the blast radius before editing. These defaults hold unless the user says
otherwise:

- Slide count, slide order, and slide numbering do not change.
- Template, masters, layouts, and theme do not change.
- Fonts, sizes, colors, and spacing of untouched elements do not change.
- Content the user did not mention is not rewritten, shortened, or "improved".
- Speaker notes, sources, footers, and page furniture survive.
- **Reviewer comments survive.** No edit request authorises losing one.
- No em dashes are introduced in any copy you write.

The do-not-touch list, backup protocol, and the minimum-diff ladder are in
[preservation-rules.md](references/preservation-rules.md). Read that file before
any structural edit: adding, removing, reordering, or resizing anything.

---

## 5. EDIT

Follow the playbook for the surface. Two rules sit above all of them.

**Minimum diff.** Use the least invasive technique that fully satisfies the
brief. Change text before you change a box, change a box before you change a
layout, change a layout before you rebuild a slide. The ladder is in
[preservation-rules.md](references/preservation-rules.md#the-minimum-diff-ladder).

**Match the neighbours.** New elements inherit formatting from their siblings,
not from your defaults. A fifth chevron looks like the other four: same height,
same fill, same font, same gap. Clone a sibling, then change its content. Do not
hand-author a new shape when a sibling can be copied.

**Fill the layout, do not draw on top of it.** Text goes in the slide layout's
own placeholders, never in a floating text box added beside them. Bullets come
from PowerPoint's list formatting, never from a "•" or "-" typed into the text.
Both rules, and the checks that catch them, are in
[placeholders-and-bullets.md](references/placeholders-and-bullets.md). Read it
before writing content onto any slide.

For crowding, spacing, and "make this cleaner" asks, work down the ranked
techniques in [density-and-layout.md](references/density-and-layout.md). Cutting
content is the last resort, never the first move, and never silently.

---

## 6. QA: prove it (blocking gate)

Two questions, both answered with evidence, before you report done.

**Did the intended change land?**

**Did anything else move?**

```bash
"$PYTHON" "$SKILL/scripts/inventory.py" "deck.pptx" -o after.json
"$PYTHON" "$SKILL/scripts/compare.py" before.json after.json --scope 6
```

`compare.py` exits non-zero when it finds a change outside the declared scope.
That is a defect to fix, not a note to add to the report. Treat unexplained
collateral change the same way you would treat a crash.

Then run the surface gates and the visual pass in
[qa-checklist.md](references/qa-checklist.md). Never report "done" from code
alone. Look at the rendered slide, section, or page.

---

## 7. REPORT

Short, plain, honest. Four lines at most:

```
Changed:   Slide 6, E2E flow: added "System Demo" as step 4 of 5; chevrons
           resized 1.9" to 1.5" to hold the band width.
Protected: 23 other slides byte-identical; slide 6 title, source line and
           footer untouched.
Check:     "System Demo" is the longest label and sits at 11pt, one point under
           its siblings. Say the word and I will drop all five to 11pt.
File:      Downloads\Lumen_PI_Planning_v4.pptx
```

If something did not work, say so with what you saw. If you assumed something,
that is the "Check" line. Never claim a QA pass you did not run.

---

## 8. Hand-offs

This skill owns intent, scoping, and QA. It borrows mechanics from others.

| Need | Skill |
|---|---|
| `.pptx` unpack / edit / repack mechanics, layouts, patterns, COM render | `metis-pptx` |
| Building a brand-new deck | `metis-pptx`. Hand it over in one line and stop. This skill does not build decks. |
| HTML presentation build or rebuild | `metis-html-slides` |
| Scrolling narrative page, build note, newsletter | `metis-narrative-scroll` |
| Story order, executive framing, the "so what" for a slide | `executive-slide-builder` |
| Color, type, logo, brand compliance check | `metis-brand-identity` |
| Any chart, KPI tile, or dashboard visual | `dataviz` |
| Published artifact page design and runtime capabilities | `artifact-design`, `artifact-capabilities` |
| SteerCo anchor and weekly roll-forward | `metis-steerco` |

Hand off the **Change Brief**, not the raw prompt. The other skill should never
have to re-derive intent.

---

## 9. Hard rules

1. No edit without a read first, in this session.
2. No structural edit without a backup copy of the file. On a deck carrying
   reviewer comments, get that copy made BEFORE the first edit, not after.
3. No "while I was in there" improvements. Log them in the report as an offer.
4. No silent deletion, ever. If content has to go, say what went and where.
   Reviewer comments are never on the table, on any surface, under any scope.
5. No rebuild of a slide that an in-place edit can satisfy.
6. No new artifact URL when the user asked to change an existing one.
7. No "done" without the compare step and a look at the rendered result.
8. No em dashes in any copy written for the user.
