# Remotion inside a Metis demo video

Remotion (remotion.dev) makes video from React code. This skill's own renderer already does the hard part of a
product demo (the real app under a camera, voiceover sync, captions, music), so Remotion is a **toolbox for
inserts**, not a second engine. Build the insert in Remotion, render it as frames, and drop it into the storyboard
as a `clip` scene. Everything else (voice, captions, mix, QA) stays on this skill's pipeline.

Remotion's own agent skills are vendored at `references/remotion/`. Start at `references/remotion/ROUTER.md`
and load only the reference you need (markup, maps, captions, render, docs). Refresh them with
`python scripts/remotion_sync.py` (it prints the vendored and latest version; `--check` only reports).

## License

Rohan uses Remotion under its **Free License** (individuals and companies of up to 3 people, commercial use
allowed, no sign-up), working as an individual. If a Metis team of 4 or more starts building with it, that needs a
Company License (remotion.pro/license, from $100/month). Say so once if that changes; do not re-raise it otherwise.

## When to reach for Remotion

Use it for things the HTML stage does badly or not at all:

- **Data that moves**: bar or line charts that grow, counters, before/after numbers, a funnel filling.
- **Maps**: routes, markers, flyovers (`remotion-maps`; base them on real coordinates, per Rohan's map rule).
- **Lottie, 3D (three.js), audio visualizers, GIFs**, or editing existing footage (trim, crop, picture in picture).
- **A complex motion piece** that would take many scene types in `render.py` to fake, built as one composition.
- **Studio scrubbing**: when Rohan wants to steer an insert interactively, open Remotion Studio and let him scrub.

Do NOT use it for: the app walkthrough (keep `app` scenes, they film the real product), the hook, the logo reveal,
beats, cards, statements. Those already exist, are voice-synced and are on brand.

## Workflow

1. **Project location**: a `remotion/` folder next to `storyboard.json`, in the project folder, never the
   scratchpad. Scaffold once (follow `references/remotion/remotion-create/REFERENCE.md`):
   ```
   npx create-video@latest --yes --blank --no-tailwind remotion
   cd remotion && npm i
   ```
   Node is at `~/.local/bin/node` on Rohan's Mac.
2. **Composition settings must match the stage**: `width={1920} height={1080} fps={30}`. Any other fps plays at the
   wrong speed, because the clip scene shows exactly one source frame per video frame.
3. **Preview**: `npx remotion studio --no-open`, then open the printed URL with `preview_start` (full URL, including
   `/<composition-id>`). Keep it open while building so Rohan can watch and steer.
4. **Render as an image sequence** into the board's `clips/` folder:
   ```
   npx remotion render <CompositionId> ../clips/<name> --sequence --image-format=jpeg --jpeg-quality=95
   ```
   (`--image-format=png` if the clip needs exact color or transparency.) No audio: narration and music come from
   this skill.
5. **Add the scene** to the storyboard:
   ```json
   {"type": "clip", "frames": "clips/<name>", "vo": "chart_line", "hold": 600}
   ```
   `start` / `end` trim by frame index. With a `vo`, the line starts with the clip, its captions show over it, and
   the last frame holds until the line finishes. The scene fades in and out like every other scene.
6. **Render and QA as usual** (`make.py`, contact sheets, `timeline.py`). Re-render the sequence whenever the
   composition changes; the stage reads frames from disk.

## Metis rules that override Remotion's own guidance

- **Brand**: Metis Dark Blue `#20216f` background, Metis Green `#3cdbc0` accent, white text, muted `#c9d3ee`,
  Open Sans loaded with `@remotion/google-fonts` (otherwise it silently falls back). Same tokens as the storyboard's
  `brand` block. Lucide icons (`lucide-react`), never emoji.
- **Style**: this skill's section 3 wins. Skip Remotion's light leaks, glows, motion blur on text, slam zooms and
  flashy transitions; use plain fades, springs with high damping, one idea per insert.
- **Voiceover**: do NOT follow `remotion-markup/voiceover.md` (it asks for an ElevenLabs key in chat and makes
  per-scene MP3s). Narration goes through `scripts/voice.py` with Rohan's or Romain's voice ID, the key stays in
  `~/.metis/demo-video/elevenlabs.key`.
- **Captions**: use the storyboard's spoken-word captions, not `remotion-captions`, unless the insert is a captioned
  clip of existing footage.
- **Rendering**: Remotion's guide says not to render unless asked. In this skill rendering the sequence is part of
  building the video, so render the clip once the composition is approved in Studio.
- **Numbers on screen** follow the house rules: real data with a stated source, no counts of our own activity, no
  "today" (pin the date).
- **Never `rm` on a compound command line**; to redo a clip, render into a new folder name or let Remotion overwrite.

## Check before delivering

- Clip folder holds the expected frame count (`durationInFrames`), names sort in order (Remotion zero-pads them).
- The contact sheet shows the clip moving (compare two frames a second apart) and the font is Open Sans.
- No visible seam at the fade in or out: the first and last frames should sit on the Metis navy background.
