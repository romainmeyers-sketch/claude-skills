# Surface Playbooks

One playbook per surface. The loop in SKILL.md does not change. What changes is
how you read, how you edit, and what can silently break.

Shared setup for the script-driven surfaces:

```bash
PYTHON="C:/Users/romain/AppData/Local/Programs/Python/Python312/python.exe"
SKILL="$HOME/.claude/skills/presentation-editor"
```

---

## A. Existing .pptx file

The default surface. Highest risk of collateral damage, so the strictest process.

### Read

```bash
"$PYTHON" "$SKILL/scripts/inventory.py" "deck.pptx" -o before.json --print
```

The inventory gives you slide count, layout per slide, every shape with position
in inches, size, text, font size, and fill. Use it to find your target by text
match instead of guessing an index:

```bash
"$PYTHON" "$SKILL/scripts/inventory.py" "deck.pptx" --find "E2E"
```

For anything visual (crowding, alignment, overlap), also render. `metis-pptx`
ships the COM renderer:

```bash
"$PYTHON" "$HOME/.claude/skills/metis-pptx/scripts/visual_qa.py" deck.pptx qa/
```

### Back up

Always, before a structural edit. Never overwrite the user's only copy.

```bash
cp "deck.pptx" "deck.bak-$(date +%Y%m%d-%H%M).pptx"
```

### Edit

Two routes. Pick the lighter one that works.

**Route 1: python-pptx in place.** For text changes, number changes, position and
size changes, and cloning a sibling shape. Fast, surgical, and it leaves the rest
of the package untouched. Preferred for most edits from this skill.

**Route 2: `metis-pptx` unpack / edit XML / repack.** For anything python-pptx
cannot express cleanly: new slides from layouts, slide duplication, reordering
the slide list, grouped shapes, SmartArt, chart XML. Follow `metis-pptx` section
1.4 onward. Do not invent your own unpack.

Rules that hold on both routes:

- Clone a sibling to create a new element, then change its content. Do not build
  shapes from scratch when a sibling exists.
- Edit the run, not the paragraph, when only some words change. Rewriting a
  paragraph drops run-level formatting such as a bolded word or a colored number.
- Keep placeholder shapes as placeholders. Replacing a placeholder with a text
  box breaks the layout inheritance and the brand frame.
- Never touch `slideMaster`, `slideLayout`, or `theme` parts for a content edit.
- If a text change makes text overflow its box, fix it by the ladder in
  [density-and-layout.md](density-and-layout.md), not by silently shrinking the font.

### QA

```bash
"$PYTHON" "$SKILL/scripts/inventory.py" "deck.pptx" -o after.json
"$PYTHON" "$SKILL/scripts/compare.py" before.json after.json --scope 6
```

Then the gates in [qa-checklist.md](qa-checklist.md#a-pptx-gates), and a look at
the rendered slide. File must open in PowerPoint without a repair prompt: if
`compare.py` reports a slide count change you did not intend, stop and restore
the backup.

---

## B. PowerPoint add-in (live deck)

Claude is acting inside PowerPoint through the Office add-in. There is no file
path, no Python, no unpack, and no reliable undo you control. The user's own undo
stack is the only safety net, and every action you take consumes it.

**This skill may not be loaded on that surface.** The add-in does not read the
local Claude Code skills folder, so typing the skill name into the add-in panel
is plain text, not an invocation. When the user wants this discipline inside
PowerPoint, give them the block in [addin-preamble.md](addin-preamble.md) to
paste ahead of their request, or do the edit from Claude Code against the saved
file instead.

### What changes

| Constraint | Consequence |
|---|---|
| No filesystem access to the .pptx | `inventory.py` and `compare.py` are unavailable. Your before snapshot is a written inventory you produce by reading the deck through the add-in. |
| Edits apply live | No staging, no draft. Every step is visible to the user immediately. |
| Undo is the user's | Batch small. One logical change per action, so a bad step is one Ctrl+Z away. |
| Selection matters | "This" often means the user's current selection. Confirm what is selected before acting on it. |

### Process

1. **Ask the user to save first** when the change is structural (adding, deleting
   or reordering slides). One line: "Save now so you have a clean restore point."
2. **Read the target slide fully** through the add-in and write the inventory into
   the conversation: shapes, their text, their order. This written snapshot is
   your before state.
3. **State the brief** in one line and act.
4. **Make one change at a time.** Re-read the slide after each change rather than
   assuming the result.
5. **Never bulk-apply across slides** in one action. A loop over 20 slides with a
   wrong selector is unrecoverable at this surface.
6. **Report by comparing** to the written snapshot, element by element, and tell
   the user which single Ctrl+Z reverses the last step.

### Do not

- Do not re-create a slide to change a word on it.
- Do not apply a theme, template, or "reset layout" action. Those cascade deck-wide.
- Do not use find-and-replace across the whole deck unless the user asked for
  exactly that, and then state the match count before running it.
- **Do not reach for raw slide XML when a text or shape edit will do.** Writing
  XML back into a live slide is the step that most often drops reviewer
  comments, and at this surface there is no snapshot to catch it. If XML is
  genuinely the only route, count the comments on that slide first, say so, and
  re-check the count straight after.

### Placing text and bullets at this surface

Two defects show up constantly when the add-in writes content, whether it is
filling a slide it just made or adding to one that exists:

1. **Text lands in a floating text box** instead of the layout's placeholder,
   often outside the content area.
2. **Bullets are typed characters**, a "•" or "-" in the text, instead of
   PowerPoint's own list formatting.

Both rules and the checks that catch them are in
[placeholders-and-bullets.md](placeholders-and-bullets.md). Read it before
writing any content at this surface. The short version: fill the layout's own
boxes, never add a text box for content that has a placeholder, and never type
a bullet character.

### Comments at this surface: blocking gate

**This has already destroyed real work twice.** The add-in's slide-XML and
script tools rewrite the slide part, and the comment relationships do not
survive. Prose warnings did not prevent it, so this is a gate, not a guideline.

**Before the first edit of an add-in session, ask whether the deck has
comments.** You often cannot see them through the add-in's own tools, so ask
the user rather than assuming.

If the deck has comments, or the user does not know:

1. **Stop and get a copy made first.** One line: "This deck has comments and the
   tools I have here can drop them. Do File, Save a Copy first, then I will
   edit." Wait for confirmation. Do not start the edit before it.
2. **Never use a slide-XML rewrite or a script that replaces shapes wholesale.**
   Text edits and single shape property edits only. If the change genuinely
   cannot be made that way, say so and offer to do it from Claude Code against
   the saved file instead, where the comment check runs automatically.
3. **Check immediately after the edit**, and say the result out loud, before
   anything else. Not in the final report.
4. **If comments are gone, say it in your very next message.** Do not continue
   the task. Recovery gets harder by the minute:
   - `Ctrl+Z` in PowerPoint, straight away, is the best option.
   - Or close the deck **without saving**, if nothing else is unsaved.
   - Or File, Info, Version History, and open the version from before the edit.
   - Or, from any older copy of the file, recover the text with:
     `python scripts/extract_comments.py old_copy.pptx -o comments.md`
     That gives back author, date, slide, and full text, so the comments can be
     re-added by hand. It does not restore the threads themselves.

The rule behind all of this: a reviewer comment is somebody else's words, and it
cannot be reconstructed from the slide. It outranks the edit that was requested.

---

## C. Claude Design and canvas surfaces

Covers Claude Design, design docs, and canvas or board tools available in the
session (for example the Miro `canvas_*` tools, or `DesignSync` when present).

**Claude Design may not expose the skill picker.** If the user reports that the
skill cannot be called there, give them the block in
[design-preamble.md](design-preamble.md) to paste ahead of their request, and
have them confirm the skill is enabled in claude.ai Settings, Capabilities,
Skills, not merely uploaded.

### Read

Read the existing design before proposing anything:

- Load the surface's own read tool first. For Miro `canvas_*` tools, call the
  canvas composer skill tool before any write, as that server instructs.
- Capture the **design tokens actually in use**: color values, type scale,
  spacing rhythm, corner radius, shadow policy, icon style. The user's house
  style (no shadows, no accent bars, curved takeaways, descriptive title plus
  subtitle, top-to-bottom flow) is the default when the surface does not
  contradict it.
- Capture the **component vocabulary**: what a card looks like here, what a
  section header looks like here. New elements join that vocabulary.

### Edit

- Change the smallest node that satisfies the brief. Do not regenerate a frame to
  move one element inside it.
- Keep named layers, frames, and groups intact. Names are how the user navigates.
- Respect the existing grid. If elements sit on a 12-column grid at 24px gutters,
  the new element does too.
- When the surface only accepts a full-document write (SVG or markdown in, whole
  document out), rebuild from the exact current state you just read, apply your
  one change, and diff your output against what you read before sending it. This
  is where whole sections get silently dropped.

### QA

- Re-read the design after writing and confirm element count, names, and
  positions of everything you did not intend to touch.
- Check both light and dark rendering if the surface supports both.
- Confirm the change is visible at the zoom level the user actually works at.

---

## D. HTML artifact decks

Covers published Artifacts and `.html` deck files, including decks built by
`metis-html-slides` and `metis-narrative-scroll`.

### Read

For a published Artifact the user wants changed, read it first with the Artifact
tool (`action: "read"`) and build the edit from the version that comes back. For
a local file, run the inventory script, which parses sections, headings, and
element counts:

```bash
"$PYTHON" "$SKILL/scripts/inventory.py" "deck.html" -o before.json --print
```

### Edit

- **Update in place.** Republish to the same URL by passing the same `url`, or
  rewrite the same file path. Creating a second artifact when the user asked for
  a change is a defect, not a convenience.
- Edit the section, not the document. Target the smallest block that contains the
  change.
- Keep the CSS custom properties as the single source of truth. Change a token
  value if the user wants a global change; add an inline style only for a genuine
  one-off, and say so.
- Do not restructure the DOM to achieve a visual change that CSS can deliver.
- Preserve ids and anchors: nav rails, contents lists, and deep links break when
  ids change.
- Preserve any runtime capability wiring and stored state keys already in the
  page.

### QA

```bash
"$PYTHON" "$SKILL/scripts/inventory.py" "deck.html" -o after.json
"$PYTHON" "$SKILL/scripts/compare.py" before.json after.json --scope 3
```

Then open it and look. Check the nav still reaches every section, the page holds
at phone width, and both color schemes still render. Full gates in
[qa-checklist.md](qa-checklist.md#c-html-gates).

---

## E. Presentation-style dashboards and visuals

Charts, KPI rows, metric tiles, scorecards, status boards, wherever they live.

### Read

Before changing a visual, capture:

- The **data**: values, units, period, and source.
- The **encoding**: what maps to length, position, color, and area.
- The **palette role assignment**: which series owns which color, and what the
  conditional colors mean (good, bad, neutral, target).
- The **sibling formatting**: decimals, unit placement, delta chips, label case.

Load the `dataviz` skill before writing or changing any chart code, in any
medium. It carries the palette, the form heuristic, and the mark specs.

### Edit

- Adding a series or a tile must not silently recolor the existing ones. Extend
  the palette, hold the existing assignments.
- Never change an axis range, a baseline, or a scale to make a change fit. A
  y-axis that no longer starts at zero is a different claim, not a layout tweak.
- Keep number formatting identical across a row. One tile at two decimals in a
  row of integers reads as an error.
- If a new metric does not fit the row, rebalance tile widths rather than
  shrinking one tile or wrapping a label to two lines alone.
- Conditional color logic is content, not style. Do not invert or reassign it
  without saying so.

### QA

Recompute at least one displayed number from the source data by hand. Check
totals still add, percentages still reach 100, and the legend still matches the
marks. Then read the visual cold and ask whether the headline claim is still the
one the data supports.

---

## F. New presentation creation: not this skill

This skill edits decks that already exist. Building one from scratch belongs to
the builder skills, and trying to do both here makes the skill compete with
`metis-pptx` on exactly the requests it should stay out of.

If the ask turns out to be a new deck, say so in one line and hand it over. Do
not plan it, do not outline it, do not start it.

| Output | Skill |
|---|---|
| `.pptx` | `metis-pptx` |
| Browser deck with sidebar nav | `metis-html-slides` |
| Scrolling narrative page, build note, update | `metis-narrative-scroll` |
| SteerCo | `metis-steerco` |
| Proposal or capabilities deck | `metis-premier-proposal` |
| Story structure first, format later | `executive-slide-builder` |

Let that skill's own intake gates run. `metis-pptx` has mandatory gates. Do not
answer them on the user's behalf and do not suppress them.

**One genuine edge case.** A request to add a slide to an existing deck is an
edit, not a build, and it stays here. Clone the closest structural match in the
deck and fill it, per the ladder in
[preservation-rules.md](preservation-rules.md#the-minimum-diff-ladder). Only
hand off when there is no deck yet.

Once a deck exists, every later change is this skill's job again, with the
existing file as the protected baseline.
