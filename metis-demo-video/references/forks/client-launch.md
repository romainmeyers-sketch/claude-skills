# Fork: client-launch

A product, capability or tool launched for or by a client, in the client's brand, for the client's executives, users
or customers. Register: agency launch explainer (Burnwe, Lovable, Notion 3.0, Attio): problem first, colour flip at
the reveal, three benefits each with a proof shot, call to action.

Storyboards: `../example-storyboard-brand.json` (Workday brand look with chat, laptop, phone, 76 s),
`../example-storyboard-promo.json` (promo structure: prompt opener, inset sentences, beats, 62 s).

## Settle before scripting

1. The client's brand: palette (hex), font, logo file. (Recommended) lift them from the client's own site or the
   product; never invent a palette. **No Metis colour anywhere on screen.**
2. Is the client named in the video, and has the client agreed to it being shown outside the project team?
3. Who watches it: client executives (lead with the business outcome), end users (lead with the task it saves), or
   the client's customers (lead with the experience).
4. The product: how to reach it (same options as product-showcase) or screenshots.
5. Proof available: a metric, a quote the client approved, a before/after. Never fabricate a stat or a quote.
6. The call to action: a URL, "available in Workday today", "talk to your account team".

## Structure (60 to 80 s)

| Time | Scene | Notes |
|---|---|---|
| 0 to 6 s | `hook` or `prompt` | The pain as a stat or a headline over a visual metaphor (pile of files, falling chart, cluttered inbox). Dark or neutral. |
| 6 to 10 s | `reveal` or `pill` | Client logo + tagline. **Palette flips to the bright brand look here.** Music drop lands here. |
| 10 to 55 s | 3 benefits | Each: `inset` or `beats` headline (3 to 6 words, one accent word) then its proof (`app`, `float`, `device`, `phone`) then a result (counter, status flipping to done). |
| 55 to 65 s | proof | `cards` with an approved quote, a metric, or a logo wall. Optional. |
| last 4 s | `endcard` | Logo, tagline, call-to-action pill or URL, held 3 s. Never end on UI. |

## Look

- 100% client palette, including status colours and chart fills. Map every token before the first render.
- UI as floating cards with soft shadow on a brand gradient (`mesh`, `ice`, `sunrise` coloured from `brand`), or on a
  laptop / phone (`device`, `phone`). `"wipe"` (arc or `stripe`) on the two big turns only.
- Cut density: a new composition every 1 to 2 s in the hook, easing to 3 to 5 s per proof.

## Music

Build in the hook, drop on the reveal (`lift_on` the reveal cue), a lift at the payoff, clean stop on the end card.
Library mood: `launch` or `uplift`.

## QA specifics

- Run a colour audit: list every colour in the storyboard and scene HTML and confirm each maps to the client palette.
- Every number and quote on screen traces to something the client approved.
- The client's logo is the real file, at correct proportions, on a background it was designed for.
