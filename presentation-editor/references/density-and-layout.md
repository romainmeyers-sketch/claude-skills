# Density and Layout

For "make this less crowded", "it feels busy", "fix the spacing", "too much on
this slide", "it looks empty", and every other geometry ask.

## The principle

Crowding is almost never a content problem. It is a **structure** problem: too
many independent objects competing at the same visual weight. The fix is to
reduce the number of things the eye has to parse, not the number of facts on the
slide.

Work down this ladder. Stop at the first rung that solves it. Only reach the last
rung with the user's agreement.

---

## The declutter ladder

### Rung 1: Reclaim whitespace

Cheapest fixes, no content risk at all.

- Reduce internal padding inside boxes that are half empty.
- Pull elements back to the layout's real margins. Hand-placed shapes usually
  drift inside them.
- Equalise gaps. Uneven spacing reads as crowding even when there is room.
- Remove trailing empty paragraphs and blank table rows.
- Delete invisible leftovers: empty text boxes, zero-height shapes, stray
  duplicates sitting under other shapes.

### Rung 2: Cut decoration, not content

- Remove borders where a gap already separates things.
- Remove fills where the grouping is already clear.
- Remove shadows and accent bars. House style has neither.
- Remove rules and dividers that duplicate an alignment the grid already shows.
- Remove icons that repeat the label next to them.
- Reduce the number of colors in play. Three roles is usually enough: default,
  emphasis, and muted.

### Rung 3: Group

The strongest move, and the most underused. Six items become two groups of three,
and the slide stops feeling busy without losing a single word.

- Find the natural categories in the content and make them visible.
- Add one line of group heading, which costs a little space and buys a lot of
  structure.
- Convert a flat list of nine bullets into three labelled clusters.
- Merge adjacent items that are really one idea split in two.

### Rung 4: Re-encode

Change the form, keep the facts.

| Current form | Denser, calmer form |
|---|---|
| Six text boxes with parallel structure | One table |
| Repeated label and value pairs | Two-column table or a definition list |
| Long sentences in bullets | Noun-phrase bullets with the detail in notes |
| Several small charts | One chart with a series selector, or one small-multiple grid |
| A paragraph of qualifiers | One footnote line |
| Nested bullets three levels deep | Two levels, with level three moved into notes |

### Rung 5: Type and scale

- Drop body type by one step, in every sibling at once, never in one element alone.
- Shorten labels, not the facts: "Iteration Execution" can become "Execution" if
  its siblings are one word too.
- Tighten line spacing before shrinking font size. 0.9 to 1.0 line spacing buys
  real room and costs little legibility.
- Turn off autofit and set the size explicitly, so siblings cannot drift apart.

Never let one element end up at a smaller size than its siblings. If one has to
shrink, they all shrink.

### Rung 6: Split the slide

- Two slides at comfortable density beat one slide at painful density, in every
  deck type except a printed leave-behind with a page budget.
- Split along the content's own seam: by phase, by audience, by time horizon.
- Keep the same title stem on both, with a qualifier: "Roadmap: 2026" and
  "Roadmap: 2027".
- Splitting changes slide count. That is structural: back up, renumber, and check
  the agenda and rails.

### Rung 7: Cut content

**Only with the user's agreement.** Offer it, name exactly what would go and
where it would land, and wait.

```
To get this to comfortable density I would move the three vendor detail rows to
the appendix and keep the summary line on the slide. Say go and I will do it.
```

---

## The opposite problem: a slide that looks empty

- Do not inflate type to fill space. Oversized type is the loudest "AI made this"
  signal there is.
- Do not add padded cards with three words in each.
- Add real content: the number behind the claim, the source, the counter-example,
  the "so what" line.
- If there genuinely is only one idea, let it be a deliberate single-idea slide,
  sized like the rest of the deck, not blown up.
- If you have no more facts, say so and ask for them. Do not invent.

---

## Measurements that usually work

For a 13.33 x 7.5 inch slide:

| Thing | Value |
|---|---|
| Side margins | 0.5 to 0.7 inches, matching the template |
| Gap between distinct elements | 0.15 inches minimum, 0.25 preferred |
| Gap between groups | Roughly double the gap within a group |
| Internal box padding | 0.1 to 0.15 inches |
| Body type | 10 to 12pt in a working deliverable |
| Smallest readable type | 9pt for sources and footnotes, nothing below |
| Items in one row | 3 to 5. Six or more wants two rows or a table. |

The reliable rule behind all of these: **the gap between groups must be clearly
larger than the gap within a group.** Most crowded slides fail exactly this test,
and fixing only this fixes the slide.

---

## Adding an element to a full set

The common case behind "add X to the Y view".

1. Clone a sibling, do not build new.
2. Insert at the position the content dictates, not at the end.
3. **Redistribute all siblings evenly** across the original band. Do not extend
   the band, and do not shrink only the new one.
4. Recheck label fit at the new width. If one label no longer fits, shorten labels
   across the set or drop type size across the set, never one alone.
5. Renumber if the set is numbered.
6. Check arrows and connectors still land on the right shapes.

Even distribution, in inches:

```
width = (band_width - (n - 1) * gap) / n
x_i   = band_left + i * (width + gap)
```

---

## Consistency beats optimality

A slightly suboptimal layout that matches the other 23 slides is better than a
perfect layout that stands out. When in doubt, copy what the deck already does.
