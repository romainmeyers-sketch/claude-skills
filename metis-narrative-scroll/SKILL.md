---
name: metis-narrative-scroll
description: >
  Build a Metis-branded narrative scroll: one self-contained HTML file that a
  reader scrolls top to bottom, with a fixed masthead, a hero, a contents list
  whose rows are the navigation, sections that reveal as you reach them,
  counted-up statistics, real embedded screenshots, a section rail, and a
  closing band. Use for internal updates, monthly or recurring build notes,
  newsletters, project or program recaps, status and progress narratives,
  "what we built" or "what we shipped" write-ups, launch announcements,
  interactive one-pagers, executive briefs meant to be read alone rather than
  presented, tool or product walkthroughs, retrospectives, and any HTML
  deliverable whose job is to walk a reader through a story and end in a
  call to action. Trigger on "narrative deck", "narrative slides", "narrative
  scroll", "scrollytelling", "build note", "newsletter", "monthly update",
  "internal update", "recap", "interactive one-pager", "animated page", or a
  request for something "like the Build Note". ALSO ASK whether to use this
  skill whenever an HTML page, site, microsite, one-pager or update is
  requested and the format is not already settled: this format applies far
  more often than it first appears, and the cost of asking is one sentence.
  Do NOT use for: PowerPoint (metis-pptx); PDF documents (metis-pdf-creator);
  whitepapers (metis-whitepaper); client proposals (metis-premier-proposal);
  a sidebar-navigated deck presented live on a screen (metis-html-slides);
  a functional tool or app with state and data (that is a build, not a
  narrative).
metadata:
  author: Metis Strategy
  version: 1.0.0
---

# Metis Narrative Scroll

A narrative scroll is a **document that moves**. One page, read top to bottom,
where each section arrives as the reader reaches it. It is not a deck. There
are no slides to page through and nothing to present from. It is what you send
someone when you want them to read it alone, at their desk, and come away
knowing three things and what to do next.

The reference implementation is the **Metis Build Note**, the monthly internal
newsletter that goes to the CEO. Everything in `templates/` and `references/`
is extracted from it.

---

## 0. Ask more often than feels necessary

**This is a standing instruction from Rohan, and it overrides your instinct to
just start building.**

Whenever someone asks for an HTML deliverable and the shape is not already
settled, ask whether it should be a narrative scroll. The format applies to far
more than it looks like it does, and one sentence costs nothing:

> "Do you want this as a narrative scroll, the animated single-page format
> like the Build Note, or as something else?"

Ask when the request is any of these and the format was not specified:

| Request | Ask? |
|---|---|
| "Make me an HTML page / site / microsite for X" | **Yes** |
| "Write up what we did this month / quarter" | **Yes** |
| "Put together an update for the team / leadership" | **Yes** |
| "A one-pager on X" | **Yes** |
| "Summarize this project for an exec" | **Yes** |
| "Announce the launch of X" | **Yes** |
| "A recap of the offsite / workshop / engagement" | **Yes** |
| "Explain how X works to someone new" | **Yes** |
| Explicitly says PowerPoint, PDF, Word, Excel | No, route to that skill |
| Explicitly says "slides I present from" | No, `metis-html-slides` |
| A working tool with data, state, logins | No, that is a build |

Do NOT ask twice. If a clarity gate or an earlier turn already settled the
format, proceed.

### Scroll or slides

| | Narrative scroll (this skill) | `metis-html-slides` |
|---|---|---|
| Read how | Alone, scrolling, on their own time | Presented live, someone driving |
| Navigation | Contents rows and a section rail | Sidebar, page by page |
| Density | Editorial: full sentences and paragraphs | Slide-like: points and visuals |
| Ends with | A call to action and real links | A summary slide |
| Sent as | A link or one HTML file | A link, usually walked through |

If they will **read** it, this skill. If someone will **present** it, that one.

---

## 1. Scaffold

```bash
python3 "$SKILL_DIR/scripts/new_narrative.py" "<target folder>" "<Title>"
```

That produces a self-sufficient project: the source, its own copy of the theme
and motion engine, the sprite, the logos, the build script and all three QA
suites. Nothing reaches back into the skill folder afterwards, so the project
keeps working if the skill changes, and one deck can diverge its own theme
without affecting any other.

```
narrative.src.html   the only file you author
_assets/             theme, engine, sprite, logos, images.json  <- ALL build inputs
_icons/              raw Lucide SVGs, for build_sprite.py
Editions/            every finished edition, one file each
build.py  qa/        build and the three verification suites
```

**Every build input lives in `_assets/`.** This is not a preference. The Build
Note kept its inputs in a folder named `_shots` next to disposable QA captures,
and they were deleted along with them; the build could not run at all and the
screenshots had to be recovered out of the last built HTML. Scratch goes to the
OS temp folder, never into the project.

---

## 2. Author

You edit exactly one file, `narrative.src.html`. It ships as a worked skeleton
of every pattern with `__PLACEHOLDERS__` to fill in. Delete what you do not
need; the page is built from whatever sections remain.

**The edition is one line.**

```html
<meta name="edition" content="August 2026">
```

`build.py` reads it, writes it into the masthead, the hero dateline and the
colophon, and **names the output file from it**. So starting a new month is one
edit, and it writes a NEW file: the previous edition is never overwritten. Same
discipline as dated tracker slides. Add the new one, leave the prior one alone.

For a one-off with no edition, put the subject there instead and it just names
the file.

### The sections you have

Read [references/patterns.md](references/patterns.md) for the full catalogue
with markup. In short:

| Pattern | What it is for |
|---|---|
| Hero | The one screen that earns the scroll. Say what this is in two lines. |
| Contents rows | The list of what is inside. Each row IS its jump control. |
| Section, `.proj` | A subject. Light ground. |
| Section, `.proj.alt` | The same on the tinted ground, so neighbours separate. |
| Section, `.proj.deep` | The same on navy, for the one that should land hardest. |
| Two-column block | What it does, and why that matters. |
| Stat strip | Two to four counted-up facts on hairlines. |
| Screenshot frame | A REAL capture of the real thing. Never a mockup. |
| Next steps | What happens next, as a hairline list. |
| Note panel | The honest caveat. No accent bar, no label chrome. |
| Closing band | What you want them to do, then the doors. |

Adding `data-rail="Name"` to any section puts it in the section rail. The rail
builds itself; there is nothing to author.

---

## 3. Motion

Read [references/motion.md](references/motion.md) before changing anything in
`_engine.js`.

Authoring motion is two attributes:

```html
<div data-anim="up" data-delay="60">        <!-- one element -->
<div class="figs" data-stagger="90">        <!-- children, in order -->
```

`data-anim` takes `up`, `left`, `right`, `scale`, `pop`, `tilt`, `blur`,
`wipe`, `clip`, `clipup`. `data-stagger` on a parent orders its children; an
explicit `data-delay` on a child always wins.

Four properties of this engine are load-bearing and must not be traded away:

1. **It is bidirectional.** Leaving the band returns an element to its start
   state, so scrolling back up runs the entrance in reverse. A one-shot reveal
   leaves a second pass down the page showing a wall of already-revealed
   content and nothing at all on the way up.
2. **It arms below the fold**, at 112% of viewport height, so the motion is
   already under way by the time the element is on screen. Arming at the
   viewport edge is what makes animations look like they "take time to load".
3. **The stagger is capped at 260ms.** A choreographed 520ms is right when the
   section is sitting still in front of you and far too slow when it is
   travelling.
4. **Reduced motion is a real variant**, not a switch. It shows the finished
   page with counters at their final values, not a blank one.

---

## 4. Screenshots

Embedded screenshots are **real captures of the real thing**. Never a mockup,
never an illustration of a UI that does not exist. This is the single thing
that makes a narrative scroll credible to an executive.

To capture a tool and embed it:

1. Copy the tool into a folder inside the project. A browser pane will not
   render a file outside the project folder, and a local dev server is blocked
   by policy on Rohan's machine, so do not plan a route that needs one.
2. Drive headless Chrome to screenshot it. If the tool opens on a first-run
   wizard or a modal, append a small harness that dismisses it before the shot.
3. **Crop to end on a clean whitespace line**, never through a heading or half
   a row of cards. A screenshot that ends mid-component reads as a broken image.
4. Encode as a JPEG data URI into `_assets/images.json`:
   `{"SHOT_ONE": "data:image/jpeg;base64,..."}` and reference it in the source
   as `__SHOT_ONE__`.
5. **Delete the staged copy of the tool afterwards.** A second copy of a repo
   next to the real one is the hazard, not the disk space: it carries its own
   `.git` and any deploy binding, one accidental deploy away from shipping the
   wrong thing.

Every `<img>` needs real alt text describing what is actually in the capture.
`qa-render.mjs` fails the build for a missing alt.

---

## 5. Build

```bash
python3 build.py --check     # writes nothing, reports CREATE vs UPDATE
python3 build.py
```

Always `--check` first when starting a new edition. If it says UPDATE and you
meant to start a new month, the edition line is still on the old month.

The build refuses to ship an unfilled `__PLACEHOLDER__`, because those render
as literal text on the page.

---

## 6. Verify. All three, every time.

Against the BUILT file in `Editions/`, never the source.

```bash
node qa/qa-render.mjs  "Editions/<file>.html"
node qa/qa-jumps.mjs   "Editions/<file>.html"
node qa/qa-spacing.mjs "Editions/<file>.html"
```

| Suite | What it will not let you ship |
|---|---|
| `qa-render` | Horizontal overflow, an image that did not decode, an icon `<use>` pointing at nothing, a missing alt, a webfont that never loaded, an element stranded invisible, a counter that never reaches its target. At 1440 / 1180 / 390. |
| `qa-jumps` | A jump that lands anywhere but the top of its target, a rail label that cannot be clicked, a rail that swallows page clicks, reduced motion showing a blank page, any uncaught page exception. |
| `qa-spacing` | A number crowding the hairline beside it, a stat strip drawing two different rule widths, too little air above a large numeral. |

**Never verify with headless Chrome's `--virtual-time-budget`.** It does not
advance CSS transitions, so a working page captures on its start frame and
reads as completely broken. On the Build Note it reported 53 stranded elements
and a blank hero while every real-time check passed, and cost a full diagnostic
cycle. A `--window-size` under 500px is also silently clamped to 500 and the
shot cropped, faking an overflow bug that does not exist. The suites here drive
real Chrome in real time and set mobile widths through device emulation, which
is why they are correct.

Read [references/pitfalls.md](references/pitfalls.md) before shipping. It is
the list of things that have actually broken.

---

## 7. House style, non-negotiable

- **No em dashes.** Anywhere, in code or copy.
- Palette and type are the Metis Onboarding Hub's system so a narrative and the
  tools it describes read as one family. Do not introduce colours outside it.
- Type is one ramp of five steps: 11.5 / 13 / 15 / 17 / 20, with display sizes
  on their own clamp scale above it. Anything needing a size **picks a step**;
  it does not invent one.
- Icons are Lucide from the inline sprite, sized by `--ics`, never by
  `font-size`. **No emoji in the DOM.**
- Flat surfaces: hairline borders, no shadows. The firm's site carries none.
- **Banned because they read as machine-written:** tip and "pro tip" callout
  boxes, left-edge accent bars, uppercase tracked eyebrow labels sitting on
  tinted panels, dash-led copy. A subtle brand tint is fine. Callout chrome is
  not. The `.note` pattern is the approved way to carry a caveat.
- Controls on the same visual row share one height. Fix the row, not each
  control.

## 8. Numbers and claims

A narrative scroll usually goes to someone senior, so every figure has to be
defensible.

- A count from a tool's first data import is **not a fact**. The Build Note
  pulled "86 open to-dos" and "12 priorities" out of its count-ups for exactly
  this reason.
- Do not state how many people have access to something. Those lists change and
  the number goes stale silently.
- Where a capability exists but is not live, **say so on the face of the page**
  using the `.note` pattern. The Build Note says the Radar's document sending
  is in test mode and every send goes to the sender's own inbox, rather than
  implying the feature ships.
- Confirm every link resolves before it goes out, and prefer a URL that has
  actually been shared with someone over one derived from a deployment config.
