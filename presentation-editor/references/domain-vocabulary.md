# Domain Vocabulary

Short prompts only work if the terms in them resolve without a question. This is
the decoder. Extend it whenever a new term comes up and gets confirmed.

---

## SAFe and agile ceremonies

The most common source of "add X to the Y view" asks.

| Term | What it is | Where it sits in a sequence |
|---|---|---|
| **PI Planning** | Program Increment planning event | Start of a PI, before iteration execution |
| **Iteration / Sprint** | The delivery timebox, usually two weeks | Repeats through the PI |
| **Iteration Planning** | Planning at the start of each iteration | Start of each iteration |
| **Daily Stand-up** | Daily sync | Inside each iteration |
| **Backlog Refinement** | Grooming upcoming work | Inside each iteration, ongoing |
| **Iteration Review / Sprint Review** | Team-level demo of the iteration's work | End of each iteration |
| **Iteration Retrospective** | Team-level improvement session | After the review, end of iteration |
| **System Demo** | Integrated demo of the full system increment across teams | After iteration execution, typically after the team-level reviews and before Inspect and Adapt |
| **Scrum of Scrums / ART Sync** | Cross-team coordination | Recurring through the PI |
| **PO Sync** | Product owner coordination | Recurring through the PI |
| **Inspect and Adapt (I&A)** | End-of-PI review, problem solving, and improvement | End of the PI |
| **IP Iteration** | Innovation and planning iteration | Last iteration of the PI |
| **ART** | Agile Release Train, the team of teams | Organisational unit, not a ceremony |
| **E2E view** | End-to-end view of the flow, usually the ceremony cadence or the delivery lifecycle across teams | The slide that shows the whole sequence on one line |

**Default insertion order.** When asked to add a ceremony to a sequence without a
stated position, place it where the framework puts it, not at the end of the row.
The canonical cadence:

```
PI Planning -> Iteration Planning -> Daily Stand-up -> Backlog Refinement ->
Iteration Review -> Iteration Retrospective -> System Demo -> Inspect and Adapt
```

Say where you placed it and why, in the one-liner. That is faster than asking.

**The one-ART vs three-ART question is live on Lumen work.** If a change depends
on how many ARTs exist, check the locked decisions before assuming, and flag the
conflict rather than silently picking one.

---

## Delivery and portfolio terms

| Term | Meaning |
|---|---|
| **Pod** | A workstream on the engagement. Pod E is funding and metrics. |
| **Epic / Feature / Story** | The work hierarchy, largest to smallest |
| **Capability** | A business ability in a capability map, levelled L1 to L3 |
| **Value stream** | The end-to-end flow that delivers value to a customer |
| **Intake** | How new demand enters the funding or delivery process |
| **Funding model** | How money is allocated: project, product, or capacity based |
| **Run rate** | Ongoing cost per period |
| **Cost to serve** | Cost attributable to serving a customer or segment |

---

## Metis deliverable terms

| Term | Meaning |
|---|---|
| **SteerCo** | Steering committee deck. Recurring, decision-first, anchor slide with three fixed columns. |
| **Anchor** | The SteerCo summary slide: What We Achieved, What We're Working On, What's Next. Same three columns every week. |
| **Takeaway** | The so-what line. House style is a curved takeaway, not a full-width bar. |
| **Kicker** | A short line in the left margin or at the top carrying the point |
| **Source line** | The small attribution at the bottom of a data slide. Keep it, always. |
| **Leave-behind** | A deck read without a presenter, so denser than a projected deck |
| **Readout** | The deliverable presentation of findings |
| **Pre-read** | Sent before the meeting, so it must stand alone |
| **Appendix** | Where detail goes when the main deck must stay decision-focused |
| **Brand frame** | Logo, page number, graphic device. Inherited from the layout. Never redrawn. |

---

## House style defaults

These apply unless a client template says otherwise:

- No shadows.
- No accent bars.
- Curved takeaways.
- Descriptive title plus subtitle.
- Top-to-bottom reading flow.
- No em dashes in any copy. Use commas, colons, or full stops.
- Plain English: short sentences, no idioms.
- Deliverables save to the Downloads folder, not the Desktop.

---

## Structural nouns, decoded

What the user means when naming a part of a slide:

| Phrase | Element |
|---|---|
| "the view" | The main diagram or framework on the slide, not the slide |
| "the flow" | The left-to-right sequence of steps |
| "the band" | The horizontal strip a sequence sits in |
| "the row" | A set of sibling tiles or columns side by side |
| "the tile" / "the card" | One box in a row of similar boxes |
| "the header" | The title area of the slide, or of a column |
| "the rail" | The nav sidebar in an HTML deck, or a repeated side element |
| "the block" | A bounded region of related content |
| "the callout" | The emphasised box or pull quote |
| "the chip" | A small label, often a delta or a status |

---

## Extending this file

When a new term is used and confirmed, add it here with its meaning and, if it
belongs to a sequence, its position. One line is enough. This file earns its keep
by removing questions from future short prompts.
