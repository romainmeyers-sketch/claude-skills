# Fork: product-showcase

A web tool, hub, dashboard or prototype Metis built, shown working. The real app is the hero, under a moving camera.
Audience is usually Metis colleagues or a client team who will use it. Register: product-native (Cursor, v0, Linear):
slow, confident, readable holds.

Metis references: `Example of videos/Hub Showcase : Web Product Showcase.mp4` (BT Operating Model, 76 s),
`Example of videos/Web Product Showcase 2.mp4` (Onboarding Hub, 124 s).
Storyboards: `../example-storyboard.json` (classic), `../example-storyboard-light.json` (frameless app, frosted),
`../example-onboarding-hub-storyboard.json` + `../example-onboarding-hub-make_storyboard.py` (Metis hub).

## Settle before scripting (ask only what is missing, one batch, recommended first)

1. How do we reach the app? (Recommended) a single HTML file or repo folder; a public URL; an Apps Script hub you can
   `clasp clone`; screenshots only (then it becomes a `device`/`float` video, say so).
2. What was the old way? (the "before": PDFs, a spreadsheet, a Slack thread). Without one, open on the problem line.
3. The 3 to 5 moments that prove value, in the user's words ("pick your team, check an item, admins see everyone").
4. Whose names may appear on screen. Default: fictional names only.
5. Where people get the tool (URL or "ask X"), for the end card.

## Structure (60 to 90 s)

| Time | Scene | Notes |
|---|---|---|
| 0 to 5 s | `hook` (two lines) or `chat` (the request in Slack) | The problem in the user's own words. Cool `bg`. |
| 5 to 10 s | `pages` or `beats` | The old way (rasterized pages fanned out, pain highlighted) or three short beats ("Read the guide." "Try to remember it." "Hope it sticks."). |
| 10 to 15 s | `reveal` ("Meet X") | Real logo lifted from the product. Music lift lands here or on `app_in`. Warm `bg`. |
| 15 to 70 s | `app` (3 to 4 features) | Each feature: caption (4 to 9 words), push to the exact control, click, hold 1.2 to 2 s, pull back to `fit`. One gentle tilt for one hero moment. |
| 70 to 80 s | `phone` / `device` | Same tool, every screen (optional). |
| last 4 s | `statement` or `endcard` | Payoff line with one accent word, then where to get it, held 3 s. |

## Look

- Metis tool: Metis brand block (`metis-defaults.md`). `auto_bg: true`. Environments: `dark`/`rise` for the problem,
  `sunrise` or `mesh` for the reveal in the brand's own colours, `blue` for the close.
- Vary the device between videos: browser frame, frameless panel (`"frame": "none"`), laptop, phone, floating pieces.
- Captions on: people watch internal videos muted in Slack.

## Music

Minimal electronic or cinematic build whose lift lands on the reveal or the app flying in (`lift_on: "app_in"`).
Library mood: `launch`. A calm bed (`calm`) for a slower walkthrough over 90 s.

## QA specifics

- Every feature has its proof shot on screen long enough to read (check the timeline sheets, not the scene sheets).
- No `selector not visible` warnings; no real people's data; the date is fixed.
- The end card names where to get the tool and holds at least 3 s.
- Do not personalise a shared tool's video to whoever requested it.
