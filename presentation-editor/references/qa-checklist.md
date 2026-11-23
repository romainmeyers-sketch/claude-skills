# QA Checklist

The Quality Controller job. Assume there is a problem and go find it.

Two questions, always, in this order:

1. **Did the intended change land, exactly as briefed?**
2. **Did anything else move?**

Question 2 is the one that gets skipped, and it is the one that matters.

---

## Gate 0: the automated compare (run first)

```bash
PYTHON="C:/Users/romain/AppData/Local/Programs/Python/Python312/python.exe"
SKILL="$HOME/.claude/skills/presentation-editor"

"$PYTHON" "$SKILL/scripts/inventory.py" "deck.pptx" -o after.json
"$PYTHON" "$SKILL/scripts/compare.py" before.json after.json --scope 6
```

Reading the output:

| Result | Meaning | Action |
|---|---|---|
| Exit 0, changes only in scope | Clean edit | Continue to the visual gates |
| Exit 1, out-of-scope change | Collateral damage | Fix it or restore the backup. Do not report done. |
| Slide count changed unintentionally | Structural accident | Restore the backup and redo |
| No changes at all | The edit did not apply | Debug before anything else |

`--scope` takes slide numbers or section indexes, comma separated: `--scope 6,7`.
Use `--scope all` only when the user asked for a deck-wide change, and say so in
the report.

---

## Gate 1: the intended change

- The change is on the **right target**: right slide, right element.
- It is the **right change**: the verb from the brief, nothing more.
- The **content is correct**: spelling of names, correct numbers, correct units,
  correct dates. Check the number against its source, not against your memory.
- It reads correctly **in sequence**: if it joined an ordered set, the order is
  right and any numbering follows.
- It is **complete**: no half-applied change, no leftover placeholder text.

```bash
"$PYTHON" -m markitdown deck.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|TODO|\[insert"
```

---

## Gate 2: the visual pass (never skip)

Code-level checks do not catch overlap, overflow, or ugly. Render and look.

```bash
"$PYTHON" "$HOME/.claude/skills/metis-pptx/scripts/visual_qa.py" deck.pptx qa/
```

Look for:

- Text overflowing its box, or clipped at a slide edge
- Elements overlapping that should not
- Gaps under 0.15 inches between distinct elements
- Uneven gaps in a set that should be evenly spaced
- A new element that is visibly a different size, weight, or color from siblings
- Text that now wraps to a new line, changing the height of a block
- Autofit having silently shrunk a font relative to its siblings
- The new element breaking the left-to-right or top-to-bottom reading order

For a single-slide change, look at the changed slide **and its two neighbours**.
Adjacent slides are where inconsistency shows up.

---

## Gate 3: consistency with the deck

- Font sizes match siblings within a tolerance of one point, or the difference is
  deliberate and reported.
- Colors come from the deck's existing palette, not from your defaults.
- Capitalization matches the pattern already in use (sentence case vs title case).
- Number formatting matches the row: decimals, units, separators, delta chips.
- Terminology matches the deck. If the deck says "iteration", the new element does
  not say "sprint".
- Punctuation style matches, including bullet-end punctuation.
- No em dashes anywhere in copy you wrote.

---

## Gate 4: the cascade sweep

Only needed when the edit was structural. Check the things listed in
[preservation-rules.md](preservation-rules.md#cascade-traps):

- Slide numbers and any agenda, rail, or contents that lists them
- The same sequence repeated on another slide, which now disagrees
- Cross-references in body text and speaker notes
- Connectors and arrows still pointing at the right shapes
- Table of contents, section dividers, appendix references

Search, do not assume:

```bash
"$PYTHON" -m markitdown deck.pptx | grep -niE "sprint review|system demo"
```

---

## Surface-specific gates

### A. pptx gates

- File opens in PowerPoint with no repair prompt.
- **Comment count matches the before snapshot.** `compare.py` fails on comment
  loss even under `--scope all`, because no edit request authorises it. If
  comments went missing, restore the backup and redo the edit by a route that
  carries them. Raw XML rewrites and slide rebuilds are the usual culprits.
- Slide count matches the before snapshot, unless intended.
- No placeholder was converted to a plain text box.
- **New text sits in a placeholder, not a floating box.** Check the Selection
  Pane: a new shape named "TextBox N" holding body content is the defect.
- **No typed bullet characters.** Run the grep below. Any hit is a fake bullet
  that should be a real list paragraph.

```bash
"$PYTHON" -m markitdown deck.pptx | grep -nE "^\s*[•▪◦·*-]\s"
```
- Layout name per slide is unchanged in the compare output.
- Speaker notes intact.
- If the deck uses a client template: theme, masters, and layouts untouched.

### B. add-in gates

- Re-read the slide through the add-in and compare to your written snapshot,
  element by element.
- Confirm no other slide was touched, by checking slide count and the two
  neighbours.
- Tell the user how many undo steps reverse your change.

### C. HTML gates

- Page renders with no console errors.
- Every nav entry still resolves to a section, and every section is reachable.
- Ids and anchors unchanged, unless the change was about them.
- Holds at phone width with no horizontal scroll.
- Both light and dark schemes still legible.
- Republished to the **same URL or same file path**, not a new one.
- Stored state and runtime capability wiring still present.

### D. dashboard and chart gates

- One displayed number recomputed by hand from the source.
- Totals add up; percentages reach 100 where they should.
- Axis range, baseline, and scale unchanged unless that was the ask.
- Legend matches the marks.
- Existing series kept their colors.
- Conditional color logic unchanged and still correct.
- Units and period labels present and correct.

---

## Gate 5: the cold read

Close the loop. Look at the result as if you had not made it.

- Would the user notice anything they did not ask for?
- Does the changed slide still make its point, or did the edit dilute it?
- Is there anything you would be embarrassed to have a client see?

If the answer to the last one is yes, say it in the report, even if it was
already there before your change.

---

## Report format

```
Changed:   [target] [what], [any secondary adjustment and why]
Protected: [what was verified unchanged, with evidence]
Check:     [any assumption made, or anything worth a human eye]
File:      [path or URL]
```

Rules for the report:

- State the evidence, not the intention: "23 slides byte-identical" beats
  "everything else preserved".
- Any assumption goes on the Check line, phrased so a four-word reply corrects it.
- Anything you noticed and did not fix goes on the Check line as an offer.
- If a gate did not run, say which one and why. Never imply a pass you did not get.
