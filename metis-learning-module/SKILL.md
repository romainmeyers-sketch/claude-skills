---
name: metis-learning-module
description: >
  Build training in the POM 101 format: a self-contained HTML course hub with
  numbered modules, a step-by-step lesson player, animated one-minute films,
  knowledge checks, a role explorer, a glossary and saved progress. Use for
  any request to create training, enablement, onboarding or e-learning:
  "learning module", "training module", "course", "training hub", "enablement
  site", "e-learning", "LMS content", "SCORM", "curriculum", "knowledge
  check", "quiz", "certification path", "onboarding program", "lunch and
  learn", "explainer video", "animated film", "walkthrough video", or
  "something like POM 101". The subject does not matter: AI 101, security
  awareness, compliance refreshers, a client's own methodology, new-hire
  onboarding and product training all use the same engine and differ only
  in the content file. Also use when someone wants to turn a deck,
  playbook, whitepaper or workshop into something people work through on
  their own. Produces two kinds of file: the course hub, and the films that
  sit inside it. Do NOT use for: a recorded MP4 screen demo of a built tool
  (metis-demo-video); a deck presented live (metis-pptx or
  metis-html-slides); a scrolling narrative update with no exercises or
  progress (metis-narrative-scroll); a PDF reference document
  (metis-pdf-creator); reference material nobody completes.
metadata:
  author: Metis Strategy
  version: 1.0.0
---

# Metis Learning Module

The format behind the Lumen POM 101 Transformation Training Hub, generalized
so it can carry any subject.

**POM 101 is where this came from, not what it is for.** The engine renders
whatever is in the content file and knows nothing about any subject. AI 101,
security awareness, a new-hire onboarding program, a client's own
methodology, a compliance refresher: same engine, same films, different
content file. If you find yourself thinking "this is the POM skill", you are
about to hard-code something that belongs in the content.

A course in this format is **one HTML file that a learner opens and works
through**. It is not a deck and not a document. It tracks where they are, it
asks them questions, and it remembers their answers. Films are separate HTML
files, each a short animated explainer that the hub embeds.

## Before writing anything

Load these in order. Do not skip to the template.

1. `references/intake.md` first, always. It is the set of questions to ask
   before building, including whose design system this is in and whether the
   film script has been approved. Skipping it is how a course gets rebuilt.
2. `references/course-format.md` is the authoring contract: every data shape
   the hub renders, and what each field is for.
3. `references/film-format.md` if the course has films. The scene and
   narration contract, and the render hooks that turn a film into a real
   video file.
4. `references/design-system.md` for tokens, type ramp, components and
   motion. It documents the Lumen palette the original used. Swap the accent
   block for whatever the brief named, and leave the structure alone.
5. `metis-brand-identity` whenever the brief said the course is Metis-branded
   rather than client-branded.

## The two artifacts

**The course hub.** One self-contained HTML file. Home screen, then one
screen per module, then a glossary and a final check. Progress is saved in
the browser and optionally reported to an LMS.

**The films.** One HTML file per film. Each is a sixty to seventy second
animated explainer with narration, captions and a transport bar. The hub
embeds them in an iframe with `?embed=1`. They also open on their own.

Keep them separate while authoring. Inline the films into the hub only in
the final build step, and only when the course has to travel as one file.

## Workflow

### 1. Ask the brief first

**Do not open a template until you have asked.** Run `references/intake.md`
and get answers. It is five short groups of questions and most people answer
a whole group in one reply.

The four that are skipped most often, and cost the most when they are wrong:

| Ask | Why it cannot wait |
|---|---|
| **Whose design system?** | The client's brand, Metis, or neutral. Never assume. A course in the wrong brand is rebuilt, not corrected. Get their palette, fonts and logo, or the brand portal link. |
| **What are the outcomes?** | Three to five things the learner can *do* at the end. Everything else follows from these. |
| **Are films in scope, and is the script approved?** | The script is written and signed off as plain text **before** anything is animated. Changing a line after the animation exists means rebuilding the scene. |
| **Recorded voice or synthesized?** | A recorded voice is a booking with a lead time. An MP4 has no narration at all unless the lines were recorded, because synthesized speech cannot be rendered offline. Say that out loud before anyone assumes otherwise. |

Also settle: who the learner is, how long it should take, link or LMS, what
the source material is, what is decided versus still proposed, and who signs
off that the content is correct.

Then write the answers into the content file as `meta`, `objectives` and
`modules` before any lesson copy. They are the table of contents and the
promise to the learner.

If someone will not answer, do not stall. Build the first module against your
best reading, write the assumptions at the top of the content file, and say
which ones you picked. What you must never do is let an unanswered question
become a silent decision.

### 2. Write the content file, not the markup

All copy lives in one JavaScript content file as plain data. The hub renders
it. If you find yourself writing a sentence inside a template literal in the
engine, stop: it belongs in the content file.

This is what makes the format reusable. The same engine runs a POM course, a
security awareness course and a new-hire onboarding course. Only the content
file changes.

### 3. Build each module from the step kit

A module is an ordered list of steps. The learner advances one at a time.
The kit gives you six step types, and they go in this order:

| Step | What it does | Rule |
|---|---|---|
| `intro` | Names the module, how long, what they will be able to do | Always first |
| `take` | Three things to take away, before the detail | Exactly three |
| `film` | The one-minute film, with transcript underneath | Optional |
| `topic` | One idea per step | Five to nine per module |
| `check` | The knowledge check | Always, before the recap |
| `recap` | The three takeaways again, now as confirmation | Always last |

The `take` and `recap` steps carry the same three statements. That repetition
is the design: say it, show it, say it again.

### 4. Write the checks so they teach

Every question needs a `why`: one sentence shown after answering, whether
they got it right or wrong. A check without a `why` is a test. A check with
one is a lesson.

Write distractors that a reasonable person would pick. "A single software
application" is a good wrong answer for "what is a product" because many
people believe it. Joke options waste the learner's attention.

### 5. Films: script first, animation second

If the brief put films in scope, the order is fixed:

1. Write the narration as plain text, using
   `templates/film-script.example.md` as the shape. One line per scene, one
   claim per line, five to nine seconds each.
2. Send it and get it approved by the person named in the brief. This is a
   separate, cheap deliverable. Do not bundle it into a draft of the course.
3. Only then copy `templates/film.html` and build the scenes around the
   approved lines.
4. Paste the same lines into the module's `film` step as `transcript`.
5. For an MP4, run `scripts/render_film.py`. It renders the film frame by
   frame, so the result is clean however slowly the page draws. It carries
   the music bed and no voice unless a recorded `<film>.vo.wav` sits beside
   the film.

Animating before the script is approved is the most expensive mistake
available in this format.

### 6. Build and verify

Run `scripts/build_course.py`. It assembles the content file and the engine
into one HTML file and runs the gates. Never hand over a course that has not
been through it. See `references/quality-checklist.md` for what to check by
hand afterwards.

## Rules that hold for every course

**Content is data.** No copy in the engine. No module-specific branches in
the engine either: if a module needs something the kit cannot express, add a
step type to the kit rather than a special case.

**One idea per step.** If a topic step has two headings, it is two steps.

**Nothing is invented.** Everything a course asserts has to come from source
material the client gave you. Where a figure is illustrative, label it in the
copy, not in a footnote nobody reads. Where the source is silent, leave the
field blank and say the content is still to come. A training course is the
one deliverable where a confident-sounding guess does the most damage,
because people are being asked to learn it.

**Terminology is the client's.** A course teaches vocabulary as much as
content. Use their words for their things, exactly as they spell them, and
put every one of them in the glossary.

**Captions are on by default.** Narration is a convenience. The captions and
the transcript are the content. Every film ships with both.

**Progress is the learner's.** It lives in their browser. Do not send it
anywhere without saying so on screen.

**It works on a phone.** People do training on the train. Check it.

## Handing off

- A recorded MP4 of a **built tool or app** is `metis-demo-video`, not this
  skill. This skill's films are drawn animations of ideas, not screen
  recordings of software.
- To turn one of this skill's films into an MP4, use the render hooks in
  `references/film-format.md`. The film exposes its own frames and audio.
- Slides for the instructor-led version of the same material are
  `metis-pptx`, built from the same content file.
