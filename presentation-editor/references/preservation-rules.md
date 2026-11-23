# Preservation Rules

The protection half of the job. Read before any structural edit: adding,
removing, reordering, or resizing anything.

## Why this file exists

The most expensive failure in presentation work is not a wrong edit. It is a
right edit that also broke four things nobody checked before the deck went to a
client. Edits are visible. Collateral damage is not.

---

## The do-not-touch list

Never change these unless the user asked for that exact thing:

**Structure**
- Slide count, slide order, slide numbering
- Section breaks and section names
- Slide masters, slide layouts, theme parts
- Placeholder identity (a placeholder stays a placeholder)

**Brand frame**
- Logo, page furniture, footers, the deck's standing graphic devices
- Theme colors and theme fonts
- Cover and divider slides, when editing a content slide

**Content the user did not mention**
- Other slides, other sections, other tiles
- Speaker notes
- **Reviewer comments and comment threads.** These are the highest-value thing
  on a shared deck and the easiest to destroy. They live in separate package
  parts, most editing tools do not carry them, and they cannot be rebuilt from
  the slide text. Losing one is a defect even when the user said "change
  whatever you need". See the check in
  [qa-checklist.md](qa-checklist.md#a-pptx-gates).
- Source lines and citations
- Hidden slides and appendix material
- Alt text

**Metadata and wiring**
- Custom document properties
- Hyperlinks, bookmarks, anchors, element ids
- Chart source data ranges
- Runtime capability wiring and storage keys in HTML artifacts

If one of these genuinely must change to satisfy the brief, that is a decision
worth one line to the user before you make it, not after.

---

## Backups

Before any structural edit to a file on disk:

```bash
cp "deck.pptx" "deck.bak-$(date +%Y%m%d-%H%M).pptx"
```

Rules:

- One backup per editing session, not per edit. Do not litter the folder.
- Name it beside the original so the user finds it without being told.
- Mention it once, in the report, on the first structural edit only.
- Never delete a backup. The user decides when it is safe.
- On surfaces with no filesystem (add-in, some canvases), the substitute is:
  ask the user to save, and keep changes small enough to undo one step at a time.

---

## The minimum-diff ladder

Always start at the top rung that fully satisfies the brief. Going one rung lower
than needed is the single most common source of collateral damage.

| Rung | Technique | Use when |
|---|---|---|
| 1 | Edit a text run | Only the words or a number change |
| 2 | Edit a paragraph | The whole line changes, no inline formatting to lose |
| 3 | Change a shape property (fill, font size, weight) | A style change with no geometry effect |
| 4 | Move or resize a shape | Position or space changes |
| 5 | Clone a sibling and insert it | A new element joins an existing set |
| 6 | Rebalance a group (redistribute siblings) | Adding or removing changed the fit |
| 7 | Change the slide's internal layout | The structure genuinely no longer holds the content |
| 8 | Duplicate the slide and rebuild it | The layout cannot carry the new content at all |
| 9 | New slide from a layout | Nothing existing fits |

Rungs 7 to 9 are structural. They require a backup, a stated reason, and a
mention in the report.

**The test for going lower:** can you name the specific thing that breaks if you
stay at the higher rung? If not, stay higher.

---

## Blast radius discipline

Write the allowed-change list before editing. Anything that moves and is not on
the list is a defect.

A worked example, for "add a fifth step to the flow on slide 6":

```
Allowed to change:
  - slide 6, shapes in the flow group: x positions, widths
  - slide 6, flow group: one new shape cloned from step 4
  - slide 6, step number labels inside the flow group

Must not change:
  - slide 6 title, subtitle, source line, footer
  - every other shape on slide 6
  - slides 1 to 5 and 7 to 24
  - slide count, order, numbering
  - masters, layouts, theme
```

`compare.py --scope 6` enforces the slide-level half of this automatically. The
within-slide half is yours to check, using the before and after inventories.

---

## Cascade traps

Changes that look local and are not:

| Edit | Hidden cascade | Guard |
|---|---|---|
| Insert or delete a slide | Slide numbers, agenda slides, section rails, cross-references, "slide 12 shows" in notes | Search the deck text for the old numbers |
| Reorder steps in a sequence | Step numbers, arrows, connectors, reading order, the same sequence repeated elsewhere in the deck | Search for the step labels across all slides |
| Change a theme color | Every element bound to that theme slot, deck-wide | Change the shape fill, not the theme, unless the ask is global |
| Resize a placeholder | Autofit recomputes font size, text reflows, line count changes | Check the rendered result, not the XML |
| Rewrite a paragraph | Run-level formatting is lost: bold words, colored numbers, hyperlinks | Edit runs, not paragraphs |
| Change a CSS token | Every component using it, in both color schemes | Confirm the global change is wanted |
| Rename an element or id | Anchors, nav links, deep links, saved state | Keep ids stable, change labels only |
| Add a chart series | Palette reassignment across all series | Pin existing series colors first |
| Find and replace | Matches in notes, hidden slides, appendix | State the match count before running |

---

## Content is sacred

- Never delete content to solve a layout problem without the user agreeing first.
  Offer the cut, name what would go, and wait.
- Never "tighten" copy the user did not ask you to touch. Shortening is a content
  decision wearing a formatting costume.
- Never drop a source line, a footnote, or a caveat to make room. Those are the
  parts that make the deck defensible.
- Never replace a specific with a generic. "$4.2M in FY26" does not become
  "significant savings".
- If content must move off a slide, it moves somewhere: a second slide, the
  appendix, or the notes. Say where in the report.

---

## When you notice something else wrong

You will. A typo two slides over, a misaligned tile, an old date.

Do not fix it. Log it.

```
Noticed, not changed: slide 9 still says "Q2 target" where slides 8 and 10 say
"Q3". Want me to fix it?
```

This is not timidity. Unrequested fixes are indistinguishable from bugs when the
user reviews a diff, and they destroy trust in the report. The one exception is a
defect you introduced yourself, which you fix silently and immediately.
