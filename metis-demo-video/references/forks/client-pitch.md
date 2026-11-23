# Fork: client-pitch

A video that sells **Metis's work** to a client: a proposal, an engagement, a point of view on a decision the client
faces. A Metis partner or manager plays it to the client's executives, or sends it ahead of a meeting. The viewer
should come away understanding the client's situation, why the decision is hard, how Metis would work through it,
and the first concrete step.

This is not `client-launch` (the client's own product, in the client's brand) and not `informational` (a general
idea with no client). The story belongs to one client and one deal.

Built from a Nov 2026 pitch to a pharmaceutical client on where to put a second IT hub (3:26, six rounds of
revisions with the deal team). Every rule below is something that deal team asked for or pushed back on.

## Settle before scripting (ask in ONE batch, recommended option first)

1. **The source of truth.** (Recommended) the proposal deck as a PDF, plus a narration script the deal owner has
   approved, beat by beat, each beat naming the deck slides to show. If there is only a deck, draft the script from
   it and get the deal owner's yes before building. The video follows the deck's storyline; never invent a new one.
2. **Who narrates.** (Recommended) one voice: the deal owner's cloned voice, with their consent (`../voiceover.md`).
   Two narrators were tried and felt disjointed; one voice reads as one argument. Stock voice (Kokoro) or music
   with captions are the fallbacks.
3. **Who plays it to whom**, and whether the client sees it in the room or receives the file. The second means
   every frame must stand on its own.
4. **What the client has decided.** If the engagement exists to make a decision (a location, a vendor, an
   operating model), the video never names the answer. Show how the answer will be reached and keep scores
   labelled "illustrative" or "hypothetical".
5. **Client assets you may use**: the client's official logo file (their site, press kit or Wikimedia Commons;
   never redraw or retype it), photos from the client's own public site (only what the site serves openly; when a
   download is refused, do not work around it, use what you have), and public facts from the client's own
   announcements.
6. **Confidentiality.** Use the deck's own footer line verbatim (for example "Proprietary & Confidential, Metis
   Strategy LLC 2026").
7. **Length.** Pitches run longer than other forks: 2:30 to 3:30 is normal when the narration script calls for
   it. Cut sentences from outside the heart of the argument first.

## Make mock-ups before building

Before any scene is animated, render 4 or 5 still frames (PNG, 1920x1080) of the key moments: the opening, one
method scene, the evidence matrix, the scoring or outcome, the close. Show them in one contact sheet. Two full
renders were thrown away on that pitch because the look had not been agreed on stills first. When the
person is unsure about a visual choice (a map style, a background), render the same frame in each option side
by side and let them pick.

## Structure (11 beats, about 3 minutes)

| # | Beat | What is on screen |
|---|---|---|
| 1 | Where the client is today | Night satellite globe that dives into a flat map of their footprint; HQ pin, arcs to new sites; one counted-up headline number in a glass card; the client's own stated priorities as 2 or 3 chips. |
| 2 | Why it is hard, and why now | Blurred client building photo; 2 stat cards that build (a line that draws, a gap that closes); the question that comes first, in a highlighted card. |
| 3 | The options | Real client photo, the 2 to 4 plays or options as pills that slide in; one-line headline. |
| 4 | The approach | The deck's steps as a row of cards, brackets naming the phases ("outside-in", "inside-out"), a loop arrow if the method iterates. |
| 5 to 7 | The method, step by step | One scene per phase. Build the evidence matrix **column by column** as the narration names each source; tag rows "New" or "Sharpened" as criteria change; weights fill in last. Show a hypothetical (labelled) moving the weights. A pass counter if the method loops. This is the heart: give it the most time. |
| 8 | Scoring or outcome | Back to the map: the shortlist ranked in a card, arcs to the leaders; the ranking re-orders when the weights change ("same scores, different weights, different winner"); the bar line; "if no option clears the bar, that is an answer too". |
| 9 | From decision to running it | Photo half-frame; the rollout in waves as bars that fill; 3 or 4 chips for what is designed (workforce, operating model, sized for AI, led on site). |
| 10 | First move | A 4-week timeline that fills, ending in a sign-off milestone. |
| 11 | Close | Full-bleed client photo, centered line ("A location and a hub design your leaders can defend."), one supporting line. Hold 3 s. |

Each beat runs on its narration line: the scene lasts the line plus about 1.3 s, 0.5 s crossfades between beats.
Time every reveal to the word that names it (`voice_manifest.json` word timings).

## Look

- **Metis brand leads**: navy `#20216f` grounds, `#3cdbc0` accent, secondary `#00bdef`, `#256ba2`, Open Sans. The
  client is a guest: their official logo, white, small, top right on every frame; the Metis logo bottom right; the
  confidentiality line small and centered at the bottom. Do not switch to the client's palette; the deal team
  asked to stay in Metis colours.
- **Real photography**, never illustration: client photos under a navy overlay (0.84 to 0.92) with a slow Ken
  Burns push, or blurred behind cards. Half-frame photos with a left-to-right navy gradient for text scenes.
- **Geography on real satellite imagery**: NASA Black Marble night lights (public domain, 13,500 px wide, sharp at
  1080p) for the globe and the flat map, desaturated and tinted navy, arcs and pins in the accent colours. The
  daytime Blue Marble at 4K was tried and looked soft; only use daytime imagery with a source of at least 8K.
- **Glass cards**: rounded 24 px, a navy gradient at 0.86 to 0.94 opacity, a 1 px white border at 0.16, a deep
  shadow. No CSS `backdrop-filter`: the frame renderer draws it white and washed out.
- **A horizontal step tracker** top left (label plus 6 small dashes that light up). Never full-screen "Step 2"
  title cards: they play as pauses.
- Charts flat with a card shadow; no 3D extruded bars or tubes on data.
- Do not use: molecule or DNA imagery and other industry cliches, white slide-like backgrounds, little people or
  avatar figures, wide letter spacing on headlines, source footnotes on frames (sources stay in the deck).

## Narration

- The approved script, word for word. Numbers written as spoken ("one-hundred-billion-dollar"), outside figures
  rounded ("almost a fifth").
- One ElevenLabs line per beat; let `voice.py` read the whole line. If you ever split a line into sentences
  yourself, never split on a period inside an abbreviation ("U.S.", "Inc."): it put a pause in "U.S.
  commitment". Split only where the next word starts with a capital.
- Calmer than a launch: speed about 0.92, a short beat between sentences.

## Music

A warm, steady bed under the voice at about 0.30, ducked under speech, faded in over 1.5 s and out over 3.5 s.
No drops. Library mood: `calm` or `uplift`.

## Build notes

- Beats 2 to 11 are `motion` scenes (`../storyboard.md`): photos as absolutely positioned `div`s with
  `background-image`, cards as `glass` components, counters with `count`, bars and arcs with `style` events
  (`stroke-dashoffset`). Beat 1 and beat 8 are a map scene: the NASA image as an `img` with SVG arcs and pins over it.
- The globe dive is a three.js `clip` (`../remotion.md`, three.js insert) that ends exactly on the flat map's
  framing, so the cut is invisible.
- Revisions are cheap only if each beat is its own scene: re-voice and re-render the changed beats, reuse the rest.

## QA specifics

- Every number and fact traces to the deck or the client's own public announcements.
- No winner is named if the engagement has not decided; illustrative scores are labelled.
- The client logo is the official file, white, never stretched.
- Listen to the whole narration once for pauses inside phrases.
- Deliver the full 1080p file. The 720p phone copy drew a "quality is very bad" reply; send it only as a preview,
  and say so.
