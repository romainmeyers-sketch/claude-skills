# Film script: What an AI agent actually is

**Course:** AI 101
**Module:** 1, What we mean by an agent
**Length:** about 65 seconds
**Narration:** synthesized for review, recorded before release
**Status:** draft, not yet approved
**Approver:** [name]

---

## Why this exists

This is the deliverable that gets reviewed and approved **before any
animation is built**. A film is an array of scenes, and each scene is built
around its narration line. Once the animation exists, changing a line means
rebuilding the scene. The script is cheap to change. The animation is not.

Send this file. Get it marked up. Only then open `templates/film.html`.

---

## The script

One line per scene. One claim per line. The time is the scene's duration, and
five to nine seconds is the working range. Notes in square brackets say what
is on screen; they are for the person animating, and they are not narrated.

| # | Time | Narration | On screen |
|---|---|---|---|
| 1 | 5s | Most teams already use AI to answer questions. | A question typed, an answer appears |
| 2 | 7s | An agent is different. It is given a goal, and the tools to reach it. | The word "goal", then three tool shapes |
| 3 | 8s | It reads what it needs, decides what to do next, and does it. | A loop: read, decide, act |
| 4 | 7s | That loop is the whole idea. Everything else is detail. | The loop holds, everything else fades |
| 5 | 9s | Which means the question is never whether it can do something. It is what it is allowed to touch. | The loop shrinks, a boundary is drawn around it |
| 6 | 6s | An agent with no access is safe, and useless. | The boundary tightens to nothing |
| 7 | 8s | So we start by naming the tools, and the limit on each one. | Tools listed, each with a limit beside it |
| 8 | 6s | Goal, tools, limits. That is an agent. | Three words, held |

**Total: 56 seconds.**

The closing line is also the film's `name` in the content file, and it is
what the play cover shows. Make it the sentence you want remembered.

---

## Checks before this is approved

- [ ] Every line read aloud. Any line needing a subordinate clause is rewritten.
- [ ] One claim per line. No line joins two ideas with "and" doing real work.
- [ ] Every claim traces to the source material. No unsourced numbers at all:
      a film goes past too fast to question.
- [ ] The closing line is the one thing to remember.
- [ ] The approver named above has said yes, in writing.

## After approval

1. Copy `templates/film.html` and replace `SCENES` with these lines, in order.
   The `vo` field takes the narration exactly as approved.
2. For a scene with two lines, use `vo1`, `vo2` and `vo2At` rather than
   splitting the scene.
3. Paste the narration, in order, into the module's `film` step as
   `transcript`. It must match the script word for word.
4. If the film needs a voice in an MP4, record the lines now and save them as
   `<film>.vo.wav` beside the film. Without it the MP4 has music and no voice.
