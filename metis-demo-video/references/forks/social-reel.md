# Fork: social-reel

A 20 to 45 s cut for LinkedIn, Instagram or an internal announcement: one fact, one moment, one idea, built to be
understood muted while scrolling. Always ships a 9:16 vertical cut beside the 16:9.

Storyboard: `../example-storyboard-reel.json` (cut it down) and the `"vertical"` block in `../storyboard.md`.

## Settle before scripting

1. The single line someone should remember. Everything else is cut.
2. Where it is posted (LinkedIn company page, a personal post, Slack #general). Public posts need the client's and
   Metis marketing's OK when a client or a product is named.
3. The title that sits on top of the vertical cut (two lines, under 26 characters each).
4. Source material: an existing longer video to cut down, an app, or nothing.

## Structure (20 to 45 s)

| Time | Scene | Notes |
|---|---|---|
| 0 to 2 s | `beats` with `"anim": "blur"` or `motion` close-up | Thumb-stopper: one big word or a tilted close-up of the most striking frame. |
| 2 to 30 s | `motion` x 2 to 3 | Extreme close-up, track, pull back flat; the line blurs in word by word. One idea per scene. |
| last 4 s | `endcard` | Name + one line + handle. |

## Look

- Reels look: `glow` / `glow-cool` lit from below in the brand's colours (never stock orange), big type (60 px or
  more in 16:9 so it survives the vertical cut at about 54%), bottom 140 px free when a caption shows.
- `"vertical": {"title": "...", "handle": "Metis Strategy", "bg": "plain", "size": 80}`.

## Music

Punchy and short: the drop lands in the first 2 s or on the reveal. Library mood: `launch` (trimmed) or `uplift`.

## QA specifics

- Watch the vertical file, not just the 16:9: every line readable on a phone.
- It still makes sense with the sound off.
