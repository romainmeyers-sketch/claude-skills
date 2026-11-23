# Intent Translation

How to turn a one-line ask into a precise change brief. This is the file that
makes short prompts sufficient.

## The core move

A short prompt is not an incomplete prompt. It is a prompt that assumes shared
context: the artifact on screen, the convention already used in the deck, the
last thing discussed. Your job is to recover that context from the deck itself
and from the thread, not to ask the user to type it out.

The order to look for missing detail:

1. **The artifact.** Sibling elements answer almost every formatting question.
2. **The thread.** The last slide shown, the last file opened, the last topic.
3. **The domain.** See [domain-vocabulary.md](domain-vocabulary.md).
4. **The convention.** How this deck already does the same kind of thing elsewhere.
5. **Only then**, ask, and only under the one-question rule in SKILL.md section 3.

---

## Verb taxonomy

Every request maps to one primary verb. The verb sets the default blast radius.

| Verb | User phrasings | Default blast radius | Watch out for |
|---|---|---|---|
| **add / insert** | add, include, put in, we also need, don't forget | The container that receives it, plus siblings that must resize to make room | Never grow the container past its original bounds. Resize siblings instead. |
| **move / reorder** | move, put after, swap, before X, reorder, flip | The two positions involved and any numbering that depends on order | Step numbers, "1 of 5" labels, arrows, and connectors must follow the move. |
| **remove / delete** | drop, take out, remove, kill, we don't need | The removed element, plus siblings that reclaim the space | Ask once if the content exists nowhere else. Never cascade into a relayout. |
| **replace / swap** | replace, use X instead, change to | The element's content only | Keep the original formatting unless the new content cannot fit. |
| **reword** | reword, tighten, shorten, say it better, clearer | The text run only | Do not touch adjacent copy the user did not mention. |
| **compress / declutter** | less crowded, busy, cramped, too much, breathe | The slide's layout, not its content | Cutting content is the last resort. See [density-and-layout.md](density-and-layout.md). |
| **expand** | thin, empty, add detail, feels light | The slide's body region | Do not invent facts. Ask for the specifics or flag placeholders clearly. |
| **restyle** | make it match, on-brand, same as slide 4, bigger, bolder | The named visual properties only | Style changes must not reflow text into a new line count. |
| **align / space** | align, even out, line them up, spacing | Position and size only | Never change text while fixing geometry. |
| **emphasize** | highlight, call out, make it pop, lead with | One element's weight relative to the rest | Emphasis is relative. Prefer strengthening one thing over weakening four. |
| **split / merge** | split into two slides, combine these, one slide | Slide count changes, so this is always a confirmed change | Renumber, refresh agendas or section rails, check cross-references. |

If a request carries two verbs ("move it up and shorten it"), execute them as two
sequenced edits with one brief, and QA each.

---

## Resolving "this", "that", "here"

Priority order for an unqualified pronoun:

1. The element the user just named in the previous turn.
2. The element you just changed.
3. The slide or section you just showed or described.
4. The only element on the current target that matches the verb's type. ("Move
   this" on a slide with one movable group is unambiguous.)
5. The attachment or pasted content in the same message. ("Add this metric" with
   a pasted number means that number.)

If nothing resolves, that is a legitimate one-question case. Ask with candidates,
not open-ended: "The 'Cost to serve' tile or the whole KPI row?"

---

## Worked examples

### "Add System Demo to the E2E view."

| Field | Value |
|---|---|
| Target | The slide whose title or content is the end-to-end flow. Find it by searching titles and shape text for "E2E", "end to end", "end-to-end". If more than one, pick the one showing a ceremony or process sequence. |
| Action | insert |
| Content | A new step labelled "System Demo". Place it by domain order, not at the end: in SAFe, System Demo sits after iteration execution and before Inspect and Adapt. See [domain-vocabulary.md](domain-vocabulary.md). |
| Constraints | Same shape type, fill, font, and gap as the existing steps. Band start and end positions hold. Step numbering, if present, renumbers. |
| Blast radius | The flow group on that one slide, and step number labels inside it. |

Do: clone an existing step shape, retitle it, insert at the right index, then
redistribute all steps evenly across the original band width.

Do not: append it at the right edge because that is where there is room, widen
the band past the slide margin, or shrink only the new shape so it looks bolted on.

### "Move this after Sprint Review."

| Field | Value |
|---|---|
| Target | "This" resolves by the rules above. "Sprint Review" is the anchor, found by text match in the same container. |
| Action | move |
| Content | No content change at all. |
| Constraints | The moved element keeps its exact size, fill, and font. Everything between the old and new position shifts by exactly one slot. |
| Blast radius | Ordering and position within that one container, plus any sequence numbers. |

Check after moving: numbered labels, connector arrows, left-to-right reading
order, and any agenda or rail elsewhere in the deck that lists the same sequence.

### "Add this metric."

| Field | Value |
|---|---|
| Target | The metric container: a KPI row, a table, a scorecard block. |
| Action | add |
| Content | The metric from the same message, the attachment, or the last thing discussed. If none exists, this is the one-question case: ask for the value and label. |
| Constraints | Match the sibling tiles exactly: number format, decimal places, unit placement, label case, color logic for good and bad. |
| Blast radius | The metric container, plus tile widths if the row must rebalance. |

Number formatting is the most common failure here. If siblings read "94%", the
new one is not "94.0 percent". If siblings carry a delta chip, the new one needs
one or a stated reason why it does not.

### "Make this less crowded."

| Field | Value |
|---|---|
| Target | The slide or section named or last shown. |
| Action | compress |
| Content | No content removal without saying so. |
| Constraints | Every fact on the slide survives unless the user approves a cut. Title, source line, and brand frame stay. |
| Blast radius | Geometry and typography on that one slide. |

Work the ladder in [density-and-layout.md](density-and-layout.md) from the top:
whitespace and margins first, grouping second, type scale third, content cuts
last and only as an offer. Report what you did and what you deliberately kept.

---

## Common short asks, decoded

| Ask | Reading | First move |
|---|---|---|
| "Fix the spacing" | Uneven gaps or inconsistent margins, not a redesign | Measure gaps, equalise to the dominant value already in use |
| "Make it match slide 4" | Copy slide 4's visual grammar, not its content | Read slide 4's tokens, apply to structure only |
| "Too wordy" | Reword in place, same layout | Cut hedges and filler, keep every fact |
| "Swap those two" | Reorder two siblings | Move both, then fix numbering and connectors |
| "Bigger" | The one named element grows, nothing else | Grow within its container, never past margins |
| "Clean this up" | Alignment, spacing, and consistency, not content | Run the alignment and consistency gates in [qa-checklist.md](qa-checklist.md) |
| "Make it pop" | Raise one element's contrast or weight | Strengthen the hero, do not gray out everything else |
| "Same as last week" | Carry forward the prior version's structure | Find the prior file, diff the structure, apply |
| "Add a slide on X" | New slide using the deck's existing patterns | Clone the closest structural match, then fill |
| "It's off" | A real defect you have not spotted yet | Render and look before proposing anything |

---

## Stating the assumption

One line, before the work, in plain language. The pattern:

> [Verb] [what] [where], [key constraint]. [What is protected].

Good:
> Adding "System Demo" after "Iteration Execution" on slide 6, matching the other
> four chevrons. Nothing else on the slide changes.

Bad:
> I will add the item you mentioned to the relevant view, making sure everything
> looks good.

The difference matters: the first one is falsifiable in four seconds by the user,
which is the whole point of stating it.
