# Placeholders and Real Bullets

Two defects that make a slide look machine-made and behave badly later. Both
come from building content beside the layout instead of inside it.

---

## 1. Text belongs in the layout's boxes

**The defect.** New text arrives in a free-floating text box dropped on top of
the slide, instead of in the layout's title or content placeholder. It often
sits outside the content area, overlapping the margins or the brand frame.

**Why it matters beyond looks.** A floating text box inherits nothing. It
ignores the template's fonts, sizes, colors and bullet styles, it does not move
when the layout changes, it does not appear in Outline view, and it does not
resize with the placeholder. The deck stops being a template and becomes a pile
of boxes.

**The rule.** Put content in the placeholder that already exists for it. Add a
new text box only when the content genuinely has no placeholder, and say so.

### How to do it right

| Surface | What to do |
|---|---|
| PowerPoint add-in | Add the slide from a named layout, then fill its placeholders. Do not insert a text box and position it. If the layout has no slot for the content, pick a different layout rather than adding a box. |
| python-pptx | `slide.placeholders[idx].text_frame`. Never `shapes.add_textbox()` for content that has a placeholder. `add_slide(layout)` gives the placeholders, use them. |
| Open XML | Keep `<p:ph>` on the shape. A shape without it is a plain box, and the layout no longer drives it. |
| Existing slide | Clone a sibling placeholder's content, or edit the placeholder in place. See the ladder in [preservation-rules.md](preservation-rules.md#the-minimum-diff-ladder). |

### How to check, in PowerPoint

- **View, then Outline.** Only real title and body placeholder text appears
  there. If the text you just added is missing from the outline, it is in a
  floating box.
- **Home, Select, Selection Pane.** Placeholders are named "Title 1",
  "Content Placeholder 2". A floating box is named "TextBox 5".

Both checks take seconds and are worth running before reporting a slide done.

---

## 2. Use PowerPoint's own bullets

**The defect.** Bullets typed as characters: a "•" or a "-" followed by spaces,
at the start of a line.

**Why it matters.** A typed bullet is just text. There is no hanging indent, so
the second line of a long bullet wraps back under the dot instead of lining up
with the words. Levels cannot be demoted or promoted with Tab. The bullet
character does not follow the template, so it stays wrong when the brand
changes. Search, outline view and accessibility tools see a paragraph that
starts with a dot, not a list.

**The rule.** One paragraph per bullet, with no bullet character typed in the
text. The bullet comes from the paragraph's list formatting.

### How to do it right

| Surface | What to do |
|---|---|
| PowerPoint add-in | Type the lines as separate paragraphs into a body placeholder, which already carries the template's bullet style. Never prefix a line with a dot or dash. Use the demote and promote actions for sub-levels, not spaces or tabs. |
| python-pptx | One `paragraph` per bullet. Set `paragraph.level` (0, 1, 2) for depth. A body placeholder inherits its bullet character, indent and spacing from the layout, so nothing else is needed. |
| Open XML | Bullets live in `<a:pPr>`: `<a:buChar char="•"/>` with `<a:buFont>`, or `<a:buAutoNum type="arabicPeriod"/>` for numbers, plus `marL` and `indent` for the hanging indent. Depth is the `lvl` attribute on `<a:pPr>`, not typed spaces. `<a:buNone/>` explicitly turns a bullet off. |

### How to check

- Click into the line and press Tab. A real bullet demotes one level. A typed
  one inserts a tab character.
- Let a bullet wrap to two lines. Real bullets hang, so the second line starts
  under the first word. Typed ones start under the dot.
- Look for a literal `•`, `-` or `*` at the start of the text itself. There
  should be none.

```bash
"$PYTHON" -m markitdown deck.pptx | grep -nE "^\s*[•▪◦·*-]\s"
```

---

## Where this applies

Adding a slide to an existing deck, filling a slide the add-in just created, or
fixing a slide that arrived with floating boxes and typed dots. In every case
the fix is the same: move the text into the placeholder, delete the leftover
box, strip the typed bullet characters, and let the layout supply the dots.

Moving text out of a floating box into a placeholder is a structural change.
Back up first, and say in the report that the box was removed and where its text
went.
