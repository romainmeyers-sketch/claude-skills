# Motion references from prompt-motion.com

prompt-motion.com collects motion videos made with Claude, each with the prompt or skill behind it, sorted by tag
(Product UI, Phone, Charts, Diagrams, Kinetic type, Shapes, Particles, Characters, Photos, Music, Code). The
prompts are the valuable part: each one names its direction, its structure on a beat grid, how it was built and
the gotchas the author hit.

## How to use it (every video, at script time)

1. Pick 1 or 2 tags that match the video (an agent explainer: `characters`, `product-ui`; a framework piece:
   `kinetic-type`, `diagrams`; numbers: `charts`).
2. List and read 2 or 3 entries:
   ```
   python scripts/motion_refs.py list characters -n 8
   python scripts/motion_refs.py show <slug>
   ```
   Or open the page in the browser to watch the video itself.
3. Write down, in your own words, the 3 to 5 ideas worth taking: a transition, a timing rule, a banned list, a
   gotcha. Map each one to this skill's engine (table below). If an idea needs something new, build it in
   `stage.css` / `stage.js` / `render.py` and add it to this table.
4. Credit the entries you learned from in the project's notes (author + link). Tell the user which ones.

**Rules.** The site allows its content to be used as reference, not for training (robots.txt content signal),
and it blocks bulk crawlers. So read a few pages on demand, never save or bulk-download the prompts, never paste
a prompt into a project or a deliverable, and never copy someone's video. Take techniques, not work.
Downloading a reference MP4 is a file download: ask the user first.

## Techniques already built in (learned from the site, implemented here)

| Idea | In this skill |
|---|---|
| Springs instead of ease curves (closed-form spring response) | `"ease": "spring"` (small overshoot) or `"spring-soft"` (none) in `cam`; `var(--spring)` in CSS |
| A shape floods the frame (overscaled past the corners, about 0.3 to 0.45 s) and contracts into the next scene | motion `"exit": {"flood": "#3bdac0", "from": ".sel" or [x, y], "to": [x, y], "ms": 420, "out_ms": 560}` |
| Text rises out of a mask line, no blur | `class="split mask"` + a `words` event |
| One shape morphs through states (size, radius, colour) while its content swaps with its own mask | `<div class="morph st" ...>` + `{"morph": ".st", "to": {"w", "h", "r", "bg", "color", "x", "y", "html"}, "ms"}` |
| Icons pop from zero on a spring | class `in-s` |
| Real motion blur: several subframes per frame, blended | `"motion_blur": 4` at the storyboard top (render time x4; 2 shows ghost copies on fast moves) |
| A sound on every event, placed by its measured peak | `"sfx": {"click": "assets/sfx/click.wav", "zoom": "...", "flood": "...", "scene": "...", "volume": 0.5}` |
| Scan for single-frame pops (frame-difference spikes) | `qa.py --every 1.5` prints `single-frame pops` |
| Camera zooms so each moment fills the frame, cursor scales with it | motion scenes: the cursor lives in the world (`click` event) |
| Banned lists: crossfades, blur-ins, glows, particles, bouncy easing, holds over 1 s | prefer flood, mask and morph over fades on big turns |

## Ideas seen but not built yet

Liquid-glass refraction (SVG displacement over a cloned scene), goo merges (blur + alpha threshold), an iris
of 6 blades, a wordmark that squeezes into its own period, beat-grid analysis that snaps every event to the
song. Build one when a video needs it, then move it to the table above.

## Sound effects

No sounds ship with the skill. Use free, licensed SFX (for example Mixkit's free sound effects) the user agrees
to download, kept in the project's `assets/sfx/` with a SOURCES.txt. Short and subtle: a click on clicks, a light
whoosh on the 2 or 3 punchy zooms (add `{"at": ..., "cue": "whoosh"}`, not on every camera move), a pop when a
character drops in (`"cue": "pop"`), a transition whoosh on floods. Each key in `"sfx"` can be a file or
`{"file", "volume"}`; levels in references/lessons.md.
