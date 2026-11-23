# Fork: informational

Teach an idea: a concept, framework, definition, point of view or data story. No app needed. Every idea is a
designed `motion` scene: the camera starts close on the first item, tracks along as content appears, then pulls back
to show the whole idea while the takeaway line resolves word by word.

Two variants, pick one:

| Variant | When | Metis reference | Look |
|---|---|---|---|
| **slide narrative** | A named concept with a definition, a taxonomy, a sequence ("the 12 failure codes") | `Example of videos/Infomrational.mp4` (Agent 404, 75 s) | Metis navy, left text column + right visual, eyebrow label, takeaway line in accent |
| **data story** | An argument carried by numbers or relationships ("costs compound", "value sits where tech meets the business") | `Example of videos/Informational : Learning.mp4` (Economics of AI value, 45 s) | Near-black, each idea one chart or diagram that draws itself, one accent colour per idea |

Storyboard: `../example-storyboard-reel.json` + `../example-reel-scenes.py` (Agent 404 in the reels look).
For charts that must be exact (axes, real data), build a Remotion insert (`../remotion.md`) and drop it in as a `clip`.

## Settle before scripting

1. The one-sentence thesis. If it takes two sentences, it is two videos.
2. The 3 to 6 ideas in order, each with its takeaway line (what the viewer should repeat to a colleague).
3. Data: real numbers with a source, or illustrative shapes clearly labelled as illustrative. Never invent figures.
4. Variant: slide narrative or data story (above).
5. Branding and a vertical cut.

## Structure (45 to 90 s)

| Time | Scene | Notes |
|---|---|---|
| 0 to 6 s | `motion` or `hook` | A familiar picture the viewer already understands (a 404 page, a cost curve), framed as the question. |
| 6 to 12 s | `motion` | The definition or thesis, typed word by word, accent on the key term. |
| 12 to 70 s | `motion` x 3 to 6 | Per idea: eyebrow label (small, accent), a headline of 6 to 12 words with the key phrase in accent, a visual that builds item by item (chips, tiles, a line a dot travels, a counter in a pill), a one-line takeaway. Hold the finished frame 1.5 s. |
| 70 to 80 s | `motion` | Recap: the ideas as one stacked diagram (evidence -> drivers -> decisions -> value). |
| last 4 s | `endcard` or `statement` | The thesis restated, the source or "learn more" line held 3 s. |

## Look

- Slide narrative: `bg #20216f` (Metis) with a thin progress line along the bottom and a small footer
  ("In the Event of Agent Failure | Metis Strategy"). Data story: near-black ground, one accent per idea
  (sky, coral, violet, green), hairline footer "Illustrative, not measured data" when shapes are illustrative.
- Real Lucide icons on every list item and chip. Text 44 px or more.
- Nothing moves while a takeaway line is being read.

## Music

Low, warm bed with no drops: lofi or calm piano at about 0.14 volume. Library mood: `lofi` or `calm`.

## QA specifics

- Every number is sourced or labelled illustrative.
- Each idea's finished frame holds long enough to read (about 0.3 s per word on screen, minimum 1.5 s).
- Content never appears while the camera is pointed elsewhere (timeline sheets).
