---
name: metis-steerco
description: >
  Build executive Steering Committee (SteerCo) decks that drive leadership
  decisions. Use this whenever the user mentions a "SteerCo," "steering
  committee," "steerco update/deck," "exec/leadership update deck," "board-style
  status deck," provides last week's SteerCo and asks for this week's, or asks
  to turn a project update into a decision-oriented executive readout, even if
  they do not say the word "SteerCo." The primary mode is a recurring
  week-over-week update: take last week's SteerCo, roll the anchor forward, and
  carry last week's slides into the appendix. Enforces the Metis SteerCo
  Playbook: a decision-first narrative, an anchor summary slide with the SAME
  three columns every week (What We Achieved / What We're Working On / What's
  Next), risks & tradeoffs requiring leadership support, an explicit
  leadership-decisions table, and a strict main-deck/appendix split. Produces a
  Metis-branded .pptx via a bundled generator, then hands richer appendix
  visuals to metis-pptx. Always validates against metis-brand-identity. Do NOT
  use for: generic BD decks or proposals (metis-premier-proposal / metis-pptx);
  HTML presentations (metis-html-slides); PDFs (metis-pdf-creator); whitepapers
  (metis-whitepaper).
metadata:
  author: Metis Strategy
  version: 1.0.0
---

# SteerCo Deck Builder — Metis Strategy

A SteerCo deck exists to help leaders **make decisions**, not to report work.
Every rule below serves that one goal. If a slide does not lead to a leadership
input, decision, or risk they must weigh in on, it belongs in the appendix or
not in the deck at all.

Read `references/playbook.md` for the full rule set, the title-writing guide,
and the final quality checklist. This file is the operating workflow.

---

## 0. The one rule that matters most: the anchor slide

The second slide (right after the cover) is the **anchor**. It answers, in
three columns, the only question a busy executive opens with:

| What We Achieved | What We're Working On | What's Next |
|---|---|---|
| Done since last SteerCo | In flight now | Upcoming + the decisions we need |

Everything else in the deck expands on one of these three. Write this slide
first. If you cannot fill all three columns crisply, you do not yet understand
the update well enough to build the rest.

- **Title** states the conclusion, not the topic. "The Pilot Is On Track to
  Launch, With Three Decisions Needed From You" — not "Status Update."
- **"What's Next"** is where the asks live. It should point at the leadership
  decisions detailed later in the deck.
- **Takeaway** (optional, bottom navy bar): the single sentence that, if the
  room remembers nothing else, is enough.

---

## 1. The canonical structure (main deck)

The main deck is **strictly limited** to what leaders discuss and decide:

```
1. Cover
2. Anchor summary        — Achieved / Working On / What's Next   (§0)
3. Risks & Tradeoffs     — 3-column table needing leadership support
4. Leadership Decisions  — numbered risk -> specific ask/decision
5. (optional) Tradeoffs detail — e.g. "Protecting capacity creates tradeoffs"
6. Next-SteerCo storyline — DRAFT slide: the story we aim to tell next time
--- Appendix divider ---
6+. Appendix             — everything else (model detail, org charts,
                           roadmaps, workplans, pilot deep-dives)
N. Closing
```

**Why the split is strict:** operating detail in the main flow buries the ask.
The generator enforces this by construction — the main deck can only contain
the summary, risks, and decision slides; appendix items are routed after the
Appendix divider. Do not defeat this by stuffing workplans into `main_tables`.

**What goes in the appendix (always):** implementation workplans, pod-level
next steps, role/RACI maps, operating-model diagrams, SAFe/framework
references, per-pilot deep dives, backup data. Point to them from the main
deck ("detail in appendix"); do not promote them.

**The next-SteerCo storyline (slide 6).** Every deck ends its main flow with a
DRAFT slide that lays out the story we intend to tell at the *next* SteerCo: the
headline we are driving toward, what we expect to have done by then, the
decisions we anticipate bringing, and what must go right in between. It is
marked DRAFT because it is a working alignment tool for the team, not a
leadership ask. It appears on every deck by default (`meta.include_next_storyline`,
default true; set false to omit). In the weekly update loop it closes the
figure-eight: **this week's storyline becomes the seed of next week's anchor.**
When you build next week's deck, roll this slide's "By Then We Expect to Have"
into the fresh anchor's *What We Achieved* and its "Decisions We'll Likely
Bring" into the fresh *Leadership Decisions*.

---

## 2. Workflow

**There are two modes. The recurring update is the default.**

| Mode | When | Path |
|---|---|---|
| **Update (default)** | User provides last week's SteerCo and wants this week's | §2.0 |
| **First-time / from scratch** | No prior deck exists | §2.2 onward |

### 2.0 Update mode — the week-over-week loop

This is how a SteerCo actually gets used: it runs on a cadence, and each week's
deck is last week's deck moved forward. When the user gives you last week's
`.pptx` ("build this week's from this"), do this:

**Step A — Read last week's deck.** Extract its content so you can roll it
forward:
```bash
"$PYTHON" ../metis-pptx/scripts/visual_qa.py LAST_WEEK.pptx last_week_imgs/
"$PYTHON" -m markitdown LAST_WEEK.pptx
```
Identify last week's anchor (Achieved / Working On / What's Next), its risks,
and its decisions.

**Step B — Roll the anchor forward.** The three columns are ALWAYS the same;
only the contents move:
- Items from last week's **What's Next** that are now done -> move up into
  **What We Achieved**.
- Items still in flight -> update and keep in **What We're Working On**.
- New upcoming work and any new asks -> add to **What's Next**.
- Drop items that are fully closed and no longer worth leadership attention.
Then refresh the **Risks & Tradeoffs** and **Leadership Decisions** to reflect
what changed: retire resolved risks, add new ones, and re-state the decisions
still open or newly needed. Confirm the rolled-forward anchor with the user
before building the rest.

**Step C — Generate this week's fresh front.** Author the new content JSON
(§2.3) and run the generator (§2.4). Update `meta.date` and the output name.

**Step D — Carry last week's slides into the appendix.** So the room keeps
continuity and can drill into prior detail:
```bash
"$PYTHON" scripts/append_previous.py THIS_WEEK.pptx LAST_WEEK.pptx
```
By default this brings over every slide from last week except its cover and
closing, inserting them after this week's Appendix divider and before the
closing (branding preserved via PowerPoint's InsertFromFile). Pass a
`start end` slide range to bring over only part of it. Requires desktop
PowerPoint (used for the COM insert).

**Step E — QA (§2.6).** Render and inspect. The main deck should read
summary -> risks -> decisions; last week's material should all sit in the
appendix.

> Keep terminology identical week to week (Rule 3). If it was a "value stream"
> and a "pod" last week, keep those exact terms. Consistency is what lets
> leaders track the story across meetings.

### 2.1 Python environment (Windows)

Python is installed but NOT on the git bash PATH. Use the full path:

```bash
PYTHON="C:/Users/$USER/AppData/Local/Programs/Python/Python312/python.exe"
```

Required: `python-pptx`. The generator reads the shared master template at
`G:\Shared drives\Knowledge Management\New Brand Assets\PowerPoint Templates\master.pptx`,
so the G: drive must be mapped (default for Metis staff).

### 2.2 Step 1 — Gather the content, framed as decisions

Before building, extract or ask for:

1. **The three anchor lists** — Achieved, Working On, What's Next. Keep each
   item to one line, outcome-first.
2. **Risks needing leadership support** — for each: what we're working
   through, what we're doing/have done, what's needed, and the implication if
   it is not resolved.
3. **The leadership decisions** — each risk resolved to a *specific* ask.
   Vague asks ("support the team") fail. Good asks name the decision:
   "Approve an interim value stream funding approach."
4. **Appendix material** — everything else.

If the user hands you a prior SteerCo, a status doc, or notes, mine them for
these buckets rather than asking cold. Draft the anchor slide and confirm it
with the user before building the full deck — it is the spine.

### 2.3 Step 2 — Author the content JSON

Copy `assets/steerco_content.example.json` (a complete worked example) to a
working file and replace its content. The schema is documented in
`references/content-schema.md`. Keep the strict structure: summary/risks/
decisions in the main deck, everything else under `appendix`.

**Write executive titles as you go** (Playbook Rule 6). Each slide title is a
conclusion. Run every title through: "Could a reader get the message from the
titles alone?"

### 2.4 Step 3 — Generate the main deck

```bash
"$PYTHON" scripts/build_steerco.py content.json "SteerCo_<Client>_<Date>.pptx"
```

This produces the cover, anchor, risks table, decisions table, optional
tradeoffs table, appendix divider + simple appendix bullets, and closing — all
Metis-branded (green arrow, logo, footer, page numbers) with no shadows and
curved takeaway boxes, per house style.

### 2.5 Step 4 — Build richer appendix visuals

The generator renders appendix items as title + bullets. For content that
needs a real visual — org charts, roadmaps, operating-model diagrams,
timelines, process flows — **first check the bundled visual pattern library**:
`assets/external_slide_templates_master.pptx` (217 pre-built 16:9 template
slides). The index and insertion workflow are in
`references/template-library.md`: insert the chosen template slide via
PowerPoint COM, replace its placeholder text, re-apply house style.

For anything the library doesn't cover, hand off to `metis-pptx` in Editing
mode: open the generated .pptx, insert the visual slides after the Appendix
divider using the metis-pptx patterns/Timesaver library, and keep the master
framing. Do not rebuild the branded shell; edit the deck the generator
produced.

### 2.6 Step 5 — Visual QA (mandatory)

Render and inspect every slide before declaring done:

```bash
"$PYTHON" ../metis-pptx/scripts/visual_qa.py "SteerCo_<Client>_<Date>.pptx" qa_images/
```

Read each PNG. Check: no overflow or clipped table text, titles are
conclusions, the anchor reads left-to-right cleanly, tables fit, no empty
placeholder boxes, brand colors correct. Fix the JSON or hand-edit, then
re-render. Do not declare success until you have done one fix-and-verify cycle.

Then run the **final quality check** in `references/playbook.md` §7.

### 2.7 Output location

Save the finished deck to the user's Downloads folder unless they say
otherwise.

---

## 3. House style (inherited from metis-pptx)

These are non-negotiable and the generator already applies them; preserve them
in any hand-edits:

- **No shadows** on any shape.
- **No accent bars** in front of cards or content.
- **Takeaways are curved** navy rounded boxes with centered white text.
- **Descriptive title + subtitle** on every content slide. The title is the
  claim; the subtitle is the plain-language "so what."
- **Top-to-bottom** argument: title -> subtitle -> body -> takeaway.
- **Calibri only.** Colors: Dark Navy `#20216F`, Metis Blue `#256BA2`,
  Mint `#3CDBC0`, Dark Gray `#4A4A4A`, Light Gray `#F2F2F2`.

No em dashes in any generated copy — use commas, colons, or periods.

---

## 4. Files in this skill

| File | Purpose |
|---|---|
| `scripts/build_steerco.py` | JSON -> Metis-branded main deck generator |
| `assets/steerco_content.example.json` | Complete worked example (fill and adapt) |
| `assets/external_slide_templates_master.pptx` | 217-slide visual pattern library (timelines, flows, pyramids, etc.) |
| `references/playbook.md` | The 7 rules, title guide, final quality checklist |
| `references/content-schema.md` | Field-by-field JSON schema |
| `references/template-library.md` | Pattern-library index + how to insert/restyle template slides |

---

## 5. Common pitfalls

- **Reporting, not deciding.** A wall of "we did X, we did Y" with no ask. Fix:
  every risk resolves to a named decision on the Leadership Decisions slide.
- **Topic titles.** "Team Structure" instead of "The Structure Only Works If
  Capacity Is Protected." Fix: titles state the conclusion.
- **Fat main deck.** Workplans and diagrams up front. Fix: move to appendix,
  reference from the main flow.
- **Vague asks.** "Leadership support needed." Fix: name the specific decision,
  who owns it, and what is blocked without it.
- **Anchor last.** Building the anchor after the detail. Fix: draft it first;
  it is the spine the rest hangs on.
