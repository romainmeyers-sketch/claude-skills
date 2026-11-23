---
name: metis-demo-video
description: Make a polished Metis video as a 1080p MP4 with music (optional AI voiceover in Rohan's or Romain's voice), rendered frame by frame from HTML so it plays smoothly however slow the app is. It asks a few questions first (what the video is for, who watches, whose brand, who narrates), then forks into six video types - client pitch that sells Metis's work to a client (built from a proposal deck, narrated by the deal owner); product showcase of a web app, hub, tool, dashboard or prototype Metis built (real app under a moving camera); client product launch in the client's brand; character explainer (mascots for agents, assistants, teams, workflows); informational or learning video (frameworks, concepts, data stories, thought leadership); and short social reel or internal announcement with a 9:16 cut. Use it whenever someone asks for a pitch video, proposal video, a video to sell our work to a client, a learning or training lesson video, a demo video, product video, launch video, walkthrough, explainer, promo, teaser, sizzle reel, reel, LinkedIn or Instagram video, "a video like YC / Loom / Linear / Lovable launches", or "can we make a video of this tool". Also use it when someone says "connect to the Video Hub", "render my Video Hub job", "check the Video Hub", pastes a Video Hub pairing line, or hands over a video-brief.json; and when an editor says "update the Video Hub", "edit the hub", "publish the hub", "change the skill" or "pull the Video Hub repo" (follow references/editing-the-hub.md), and for any video that mentions Remotion or needs an animated chart, map, Lottie or 3D insert.
---

# Metis video (v2.0)

You write a **storyboard** (one JSON file) and the scripts turn it into an MP4. The work is the story and the camera;
rendering is automatic.

```
storyboard.json
   |  voice.py     (optional) narration -> audio + word timings     out/voice_manifest.json
   |  render.py    frames, camera, captions, clicks                  out/frames.mp4 + cues.json
   |  mix.py       music, voiceover, ducking, fades, loudness        out/<name>.mp4
   |  vertical.py  (if "vertical") 9:16 cut                          out/<name>-vertical.mp4
   |  qa.py        contact sheets + timeline sheets                  out/qa/*.jpg
make.py runs all of it.
```

## 0a. Before every video: check you are on the latest version

Do this first, every time the skill is used to make or revise a video (hub or not). It takes seconds.
1. `Artifact` tool, `action: "read"`, `url: https://claude.ai/artifact/H6yLztfVoZyzpH5owCaq3N`, `path: "skill/version.json"`
   (load the tool with ToolSearch `select:Artifact` if it is deferred). Save it, then
   `python3 scripts/self_update.py --check <that file>`.
2. Not behind: say nothing and carry on.
3. Behind: ask the person ONCE, with AskUserQuestion (multiple choice): "Update now (Recommended)" naming the new
   version and its one-line notes, or "Not now, use my current version". On "Update now": read
   `path: "skill/metis-demo-video.bundle.json"` from the same artifact, run
   `python3 scripts/self_update.py --install <that file>`, tell them in one line what changed and where the backup is,
   then re-read this SKILL.md (it may have changed) and continue the video. On "Not now": continue, and do not ask again
   in this conversation.
4. The check cannot run (no Artifact tool, offline, not signed in): continue and mention it in one line at the end.
Editors working from the repo (Rohan, Romain) update through `git pull` instead; the check still tells them if the
hub is ahead of their install.

## 0. Where the request came from

- **From the Video Hub** (the Claude artifact Metis people use to brief videos): the user says "check the Video Hub"
  (often with the hub's URL). No ids are needed: you find every video waiting for them. Older hubs gave a per-project
  line (`Video Hub job | <url> | user <id> | project <id>`). **Read
  `references/hub-mode.md` and follow it.** The brief, the approved script and the music choice come from the hub; you
  build, render, report progress back to the hub and pick up revisions from it.
- **From a `video-brief.json` file** (the hub's fallback when a person's Claude cannot connect): same as hub mode, but read
  the brief from the file and report in chat instead of to the hub.
- **Directly in chat**: start with the intake questions in section 1, then run the workflow in section 2.
- **An editor changing the hub or this skill** (Rohan or Romain: "update the Video Hub", "change the skill",
  "publish the hub"): read `references/editing-the-hub.md` first. It points at the GitHub repo and its `CLAUDE.md`;
  never edit the installed copy in `~/.claude/skills` directly.

## 1. Ask first, then pick the fork

### 1a. Intake: four questions before anything else (direct chat only)

Unless the request already answers them, ask these in ONE AskUserQuestion call, multiple choice, before reading
files, opening apps or writing a script. Skip any question the request already settles; skip the whole step for
Video Hub jobs and `video-brief.json` files (the brief already holds the answers).

| Header | Question | Options, in this order |
|---|---|---|
| Video type | What is this video for? | Pitch our work to a client / Teach a lesson or an idea / Show a tool or product working / Short social or internal clip |
| Audience | Who will watch it? | Client executives / Client team or end users / Metis colleagues / Public feed (LinkedIn, Instagram) |
| Brand | Whose brand leads? | Metis, with the client's logo as a guest / The client's brand only / Metis only |
| Narration | Who narrates? | A named person's cloned voice (they agreed) / A stock voice (Kokoro, no key) / No voice: music and on-screen text |

Map the answers to a fork, then say in one line which fork you picked and why:

| Answers | Fork |
|---|---|
| Pitch our work to a client | `client-pitch` |
| Teach a lesson or an idea, where the point is who does what (agents, roles, a team) | `character-explainer` |
| Teach a lesson or an idea, anything else | `informational` |
| Show a tool or product working + the client's brand only | `client-launch` |
| Show a tool or product working + Metis brand | `product-showcase` |
| Short social or internal clip, or "Public feed" with under 45 s | `social-reel` |

Then read the fork file and ask its "Settle before scripting" questions that are still open, again in one batch.
Never ask more than two rounds of questions before showing a script or mock-ups. A person who wants a full
training course with lessons and quizzes, rather than a video, wants `metis-learning-module`: say so in one line.

### 1b. The forks

Every video is one of six forks. Each fork has its own reference file with the structure, look, pacing, music mood,
scene types, worked example and the questions to settle before building. **Read the fork file before writing a script.**
The router with the decision rules is `references/forks/README.md`.

| Fork | Use it when | Look | Reference |
|---|---|---|---|
| `client-pitch` | Selling Metis's work to a client: a proposal, an engagement, a decision we would help them make. Built from the proposal deck and an approved narration script | Metis navy with the client's logo as a guest, real client photography, satellite maps, glass cards, step tracker, 2:30 to 3:30 | `references/forks/client-pitch.md` |
| `product-showcase` | Showing off a web tool, hub or prototype Metis built, mostly to Metis or a client team | classic / brand / light: the real app under a camera | `references/forks/product-showcase.md` |
| `client-launch` | Launching a product or capability for a client, in the client's brand, to client executives or their users | brand look in the client palette, promo structure | `references/forks/client-launch.md` |
| `character-explainer` | Explaining agents, assistants, a team or a workflow where actors hand work to each other | character look: mascots on pastel studios | `references/forks/character-explainer.md` |
| `informational` | Teaching a concept, framework, point of view, lesson or data story; no app needed | reels look: motion scenes on dark brand light, slide-narrative or data-story variant | `references/forks/informational.md` |
| `social-reel` | 20 to 45 s LinkedIn / Instagram cut or internal announcement, often vertical | reels look, short, big type, 9:16 | `references/forks/social-reel.md` |

If two forks fit, pick by **what the viewer must take away**: that Metis should do the work (pitch), a tool they
will use (showcase), a product they will buy or adopt (client-launch), how a system of actors works (character),
an idea (informational), one fact or moment (reel).

## 2. Workflow (direct use)

1. **One-time setup**: `python3 scripts/setup.py` creates `~/.metis/demo-video/.venv` (never the system Python) and
   checks for Chrome or Edge. "python" below means that venv's Python. On Windows it is
   `%USERPROFILE%\.metis\demo-video\.venv\Scripts\python.exe`.
2. **Understand the product and the audience.** Open the app (or read the deck, for a pitch), find the 3 to 5 moments
   that prove its value. Settle the fork's remaining questions (section 1a) in ONE batch, multiple choice, recommended
   option first.
3. **Look up motion references first** on prompt-motion.com: `python scripts/motion_refs.py list <tag>`, then
   `show <slug>` for 2 or 3 entries that match the fork. Take the techniques (transitions, timing, banned lists,
   gotchas), build them with this engine, and credit the entries. Reference use only: never save or paste the
   prompts (`references/prompt-motion.md`).
4. **Write the script first** (`references/script-formula.md` + the fork file): a table of scene, on-screen text, what
   the camera shows, seconds. Get a yes before building. This is the cheapest place to change anything.
5. **Prepare a demo copy of the app** when the fork films one: a single HTML page with no real backend (mock the API,
   seed realistic fictional data, fix the date). Never film a live backend or real customer data.
   `references/storyboard.md` "The app block", `references/apps-script-hubs.md`, `templates/apps-script-mock-backend.js`.
6. **Write `storyboard.json`** in the project folder the user names (never a scratchpad), with `assets/` beside it.
   `references/storyboard.md` has every field; the fork file names the worked example to start from.
7. **Preview, then render**: `python scripts/render.py storyboard.json --until 3`, then `python scripts/make.py storyboard.json`.
   State the wall-clock budget first: about 7 to 8 rendered frames per second, so a 90 s video takes about 11 minutes.
8. **QA before showing anyone**: open every `out/qa/scenes_*.jpg` and `out/qa/timeline_*.jpg`, go through
   `references/quality-checklist.md`, read render.py warnings (`selector not visible` = a skipped camera move).
9. **Deliver**: open the hand-back with the MP4's absolute path, size and length. Iterate by editing the storyboard,
   never by editing frames.

## 3. Style rules shared by every fork

- **Minimal and confident.** One idea per scene, lots of space, one accent colour. No "AI look": glows on text, light
  streaks, lens flares, slam zooms, particle bursts, gradients on text, emoji, ✓/✕ glyphs (use Lucide icons).
- **Word by word, not letter by letter.** Captions are short claims, 4 to 9 words, sentence case, one per idea.
- **The camera does the storytelling**: zoom into the element that matters, hold 1.2 to 2 s, pull back between ideas.
  One tilted close-up per scene at most; the pull-back always lands flat and readable; text 44 px or more.
- **Colour follows the story**: cool for the problem, warm for the answer, brand colour for the close
  (`"auto_bg": true` or `"bg"` per scene). Take every colour from the brand being shown; never default to orange or
  sunset light.
- **Length is a suggestion, pacing is not.** Never pad, never speed up. Over 2 minutes: cut features
  (a `client-pitch` may run 2:30 to 3:30 when the approved script needs it).
- Plain words, US spelling, no em dashes, no buzzwords, no counting your own activity, say what a thing is (never "not X").
- Fictional names and data only, unless the user names real people who agreed to appear.
- **Music** is chosen per fork (mood in the fork file). The Metis library lives in the Video Hub
  (`references/hub-mode.md` "Music"). Users may also bring a licensed track, or choose silence. Never use a track the
  user has no right to use. The big lift lands on the hero moment (`lift_on`, default `app_in`).

## 4. Metis defaults

Read `references/metis-defaults.md` before the first Metis-branded video. Short version: `bg #20216f`,
`accent #3cdbc0`, Open Sans, the real logo lifted from the product (never redrawn), brand line "Driving change.
Elevating leaders." The skill's built-in navy `#11294d` + orange palette is NOT Metis: always pass a `brand` block.
Client videos use the client's palette and fonts, with no Metis colour anywhere on screen.

## 5. Voiceover (optional, off for Video Hub jobs for now)

`references/voiceover.md`: narration whose words, captions and actions are locked together. ElevenLabs (default) only
with a key the user set up themselves (never ask anyone to paste a key in chat) and only cloned voices whose owner
consented. Or `"engine": "kokoro"` for stock voices spoken on this computer with no key (voiceover.md 1b); Kokoro
cannot do Rohan's or Romain's voice.
Video Hub jobs carry `"voiceover": false`; do not add narration to them.

## 6. Learning from every video

Every hub job ends with a feedback record (what was asked, which fork, how many revisions, what people changed, the
final rating). `references/learning.md` explains how those records become proposed skill edits that Rohan or Romain
approve before anything changes. When you hit a problem whose cause is a class of mistake, add it to
`references/lessons.md` in the same session.

## 7. Files

- `references/forks/`: the six video types + `README.md` router
- `references/hub-mode.md`: connecting to the Video Hub, the brief and job schema, progress reporting, revisions
- `references/learning.md`: the self-improvement loop and its approval gate
- `references/storyboard.md`: every storyboard field, scene type, environment and step
- `references/script-formula.md`, `references/quality-checklist.md`, `references/lessons.md`, `references/metis-defaults.md`
- `references/voiceover.md`, `references/apps-script-hubs.md`, `references/remotion.md` + `references/remotion/`
- `scripts/motion_refs.py` + `references/prompt-motion.md`: motion references from prompt-motion.com (reference
  only, stores nothing) and the techniques already built from them (flood, springs, mask text, morph, motion
  blur, sound effects, pop scan)
- `references/example-*`: worked storyboards (classic, promo, light, brand, reel, character, Onboarding Hub)
- `scripts/`: `setup.py`, `make.py`, `render.py`, `mix.py`, `qa.py`, `vertical.py`, `make_pages.py`, `voice.py`,
  `takes.py`, `timeline.py`, `remotion_sync.py`, `hub_preview.py` (720p preview + contact sheet for the hub),
  `self_update.py` (version check and update from the hub)
- `assets/stage/`: `stage.css`, `stage.js`, `clock.js`, `lucide.min.js`

## 8. What it can and cannot do

Can: anything a browser can render (kinetic type, product UI, mockups, cards, SVG, CSS 3D, mascots, the real app
under a camera), plus Remotion inserts for animated charts, maps, Lottie and three.js as `clip` scenes
(`references/remotion.md`). Cannot: live-action footage or real people; use stock or filmed clips and edit them in.
