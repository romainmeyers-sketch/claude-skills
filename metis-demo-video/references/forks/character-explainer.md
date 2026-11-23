# Fork: character-explainer

How a system of actors gets work done: AI agents, assistants, a team, a process with hand-offs. Each actor is a small
mascot with a face, moods and one accessory that says its job, on a pastel studio whose tint changes per beat.
Characters speak in speech bubbles instead of captions; real-looking cards (messages, drafts, bookings) float beside them.

Metis reference: `Example of videos/Product Showcase.mp4` (Agent Office, 63 s).
Storyboard: `../example-storyboard-character.json` + `../example-character-scenes.py` (writes the scene HTML).

## Settle before scripting

1. The cast: 2 to 5 actors, each with a name, a job in four words and the one accessory that says it
   (`tie`, `hardhat`, `headset`, `glasses`). More than 5 and nobody remembers them.
2. The day-in-the-life arc: what arrives (the mess), who takes what, what the human still decides.
3. The work objects each actor produces (a reply draft, a deck, a booking) so cards can show them.
4. Brand: Metis (pastel tints of navy and green) or client (pastel tints of the client palette).
5. Vertical cut needed? (Recommended yes, for LinkedIn.)

## Structure (50 to 75 s)

| Time | Scene | Notes |
|---|---|---|
| 0 to 8 s | `motion` | The mess: a time stamp plus a pile of messages floating in, then the question ("Who answers all of this?"). |
| 8 to 50 s | `motion` per actor | Actor drops in, says hello in a bubble, takes the work, its card shows the result. Look at the card it talks about; surprised on a click; happy when done. 8 to 12 s per actor. |
| 50 to 60 s | `motion` | The team together with live counters (working, waiting on you, done today). The human-in-the-loop line ("They do the work. You make the calls."). |
| 60 to 70 s | `motion` | A closing beat (lights off for the weekend, all asleep). |
| last 4 s | `motion` with `x3d` title | 3D extruded name drops in letter by letter, the cast small beneath it. |

## Look

- `"bg": "studio:#tint"`, a different pale tint per beat, all from the brand. Light scenes, dark text.
- Character 300 to 400 px wide in its own scene, never cropped. Bubbles 3 to 8 words.
- Fictional names and messages only, always.

## Music

Light, playful, low key: lofi or soft electronic, no big drop. Library mood: `calm` or `lofi`.

## QA specifics

- Class names in scene HTML are specific (`planner`, not `meet`); check new classes against stage.css.
- Every bubble is readable at phone size in the vertical cut (text 44 px or more).
- Moods follow the story beat; no actor stays in `talk` after its bubble leaves.
