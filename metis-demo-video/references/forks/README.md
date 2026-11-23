# Forks: which video to make

Read this first, pick ONE fork, then read only that fork's file. Every fork uses the same engine
(render.py, stage.css, mix.py); they differ in story structure, look, pacing, music and what you need from the user.

## Decision rules

Ask what the viewer must take away, then match:

| The viewer should come away... | Fork | Default length | Metis reference video |
|---|---|---|---|
| knowing a tool exists, what it does and wanting to open it | `product-showcase` | 60 to 90 s | `Example of videos/Hub Showcase : Web Product Showcase.mp4` (BT Operating Model), `Web Product Showcase 2.mp4` (Onboarding Hub) |
| convinced Metis should do a piece of work for them (a proposal, an engagement, a decision we would help a client make) | `client-pitch` | 2:30 to 3:30 | a Nov 2026 pharma IT-footprint pitch (client material, not in the gallery) |
| ready to adopt or buy a product a client is launching | `client-launch` | 60 to 80 s | BT Operating Model video, re-skinned in the client's brand (`example-storyboard-brand.json`, Workday) |
| understanding how a team of actors (agents, roles, steps) gets work done | `character-explainer` | 50 to 75 s | `Product Showcase.mp4` (Agent Office) |
| understanding an idea, framework, definition or data story | `informational` | 45 to 90 s | `Infomrational.mp4` (Agent 404, slide narrative), `Informational : Learning.mp4` (Economics of AI value, data story) |
| remembering one fact or moment, while scrolling a feed | `social-reel` | 20 to 45 s | the vertical cuts of Agent 404 and Agent Office |

Tie-breakers:
- A real app on screen for more than half the video is `product-showcase` or `client-launch`. Client brand on screen
  means `client-launch`; Metis brand means `product-showcase`.
- An AI agent product is `character-explainer` when the point is *who does what*, and `product-showcase` when the point
  is *the interface*.
- A video that sells Metis's own work to one client (built from a proposal deck, often narrated by the deal owner) is
  `client-pitch`, even when it teaches a method along the way. The client's own product in their brand is `client-launch`.
- A framework with no app is `informational`. Cut it down to one idea for a `social-reel`.
- The brief says "teaser", "LinkedIn post" or "under 45 seconds": `social-reel`.

## Brief fields every fork needs

`fork`, `purpose` (one sentence), `audience`, `branding` (`metis` or `client`, plus palette, font and logo when client),
`length_s`, `formats` (`16:9`, optional `9:16`), `key_points` (3 to 5), `music` (library track, own file, or silent).
Each fork file adds its own required fields and the questions to settle when they are missing.

## Patterns from 12 strong launch videos (Oct 2026 research)

Full notes: `research-2026-10.md`. What holds across all of them:
- One palette per film; every frame stays inside it. Light/dark swaps mark chapters, or one colour flip marks the turn
  from problem to solution.
- Unknown brands show the problem first and reveal the logo at 7 to 10 s; known brands open on the logo or close on it.
- Every claim gets one proof shot: a counter, a status flipping to done, a before/after, a logo wall, a benchmark bar.
- AI products type the prompt on screen word by word, then a short "thinking" beat, then the result.
- Every ending lands on logo plus one line, then a URL or call to action held 2 to 4 s. None ends on UI.
- Two cutting registers: agency explainer (a new composition every 1 to 2 s) and product-native (5 to 10 s UI holds
  with sparse cards). Pick one per video.
