# Storyboard reference

One JSON file. Every path is relative to the storyboard's folder. Output goes to `out/`.

```json
{
  "output_name": "my-tool-demo",
  "brand": {"bg": "#11294d", "accent": "#f49813", "muted": "#c7d6ee", "font": "Archivo"},
  "pace": 0.82,
  "end_hold": 1200,
  "music": {"file": "assets/music.mp3", "lift_on": "app_in", "volume": 0.9, "duck": 0.8, "voice_volume": 1.2},
  "voiceover": {...},          (optional, see voiceover.md)
  "app": {...},
  "scenes": [...]
}
```

| Field | Meaning |
|---|---|
| `output_name` | Final file is `out/<output_name>.mp4` |
| `brand` | CSS variables: `bg`, `glow1`, `glow2` (soft background lights), `accent`, `text`, `muted`, `font` (any Google Font), optional `font_url` |
| `pace` | Multiplies every `wait`, `after` and camera `ms` in app steps. 0.82 = brisk. Raise to 1.0 to slow down |
| `end_hold` | ms the last frame stays before the end (the fade-out happens here) |
| `auto_bg` | `true`: scenes without their own `"bg"` get one that follows the story (reveal `rise`, app `mesh`, beats `sunrise`, closing statement or end card `blue`; problem scenes keep the brand background). Any of `mesh1..3`, `mesh-bg`, `sun1..5`, `blue`, `blue-hi` not set in `brand` are mixed from `bg` and `accent`, so the look stays on-brand |
| `music.lift_on` | Where the track's biggest loudness jump lands: a cue (`"app_in"`), `"scene:4"`, or seconds |
| `music.lift_at` | Override the detected jump (seconds into the track) |
| `music.volume` | 0 to 1 before loudness normalisation. Default 0.9, or 0.55 when the storyboard has `"sfx"` so the sounds come through |
| `music.duck` | With a voiceover: how far the music dips under speech (0.8 = down 80%) |
| `music.voice_volume` | Voiceover gain in the mix (default 1.15) |
| `voiceover` | Narration lines, voices, pronunciation. See `voiceover.md` |

## Scenes

Text fields accept `**bold**`, which shows in the accent color.

**hook**: typed question that opens the video. Words pop one at a time; the camera follows.
```json
{"type": "hook", "lines": ["Still tracking your rollout", "in a **Word document?**"],
 "cards": [{"image": "assets/doc_p1.png", "crop": [x, y, w, h], "width": 430}],
 "word_ms": 300, "line_pause": 900, "hold": 900, "stack_hold": 900}
```
With two lines, line 1 lifts away while line 2 types; once the last word lands, both lines come back
stacked and centred so the whole question is on screen. `stack_hold` (ms) adds time to read it.
`cards`: up to 4 floating crops of the "old way" (screenshots), placed in the corners.

**reveal**: ("logo": "arc" draws a brand arc above the name) "Meet" focus-pull, then logo + name slide in with motion blur, then a pill.
```json
{"type": "reveal", "intro": "Meet", "name": "Product Name", "logo": "arcs" | "assets/logo.svg",
 "pill": "Tagline · short", "intro_ms": 1300, "hold": 1600}
```

**pages**: the old document as a fanned stack, a highlight box, and 1 to 3 pain points.
```json
{"type": "pages", "kicker": "Before", "title": "A 14-page **Word document.**",
 "images": ["p1.png", "p2.png", "p3.png", "p4.png"],
 "highlight": {"box": [left%, top%, width%, height%], "label": "Ticked by hand", "page": 3},
 "points": [{"title": "...", "body": "...", "icon": "×"}], "duration": 7600}
```

**quote**: a real quote that names the problem (`kicker`, `text`, `who`). Default 5.6 s.

**statement**: one big line + a sub line (`kicker`, `title`, `sub`), plus an optional small last line `foot` (appears after `foot_ms`, or when the 2nd spoken sentence starts). Good as the close. Default 5.6 s.

**cards**: kicker, title and 2 to 4 numbered cards (`cards: [{title, body}]`). Default 7.6 s.

**prompt**: a glass input box that types a request and sends it (great opener: the ask that started it).
```json
{"type": "prompt", "placeholder": "Ask anything", "text": "Can my whole team see what I check off?", "chips": ["+", "Team"], "char_ms": 40}
```

**inset**: a sentence whose words pop in, then a gap opens between two words and a product shot grows inside it.
```json
{"type": "inset", "text": "Every team's **progress** [img] in one place", "image": {"file": "assets/shot.png", "width": "3.4em", "position": "50% 0"},
 "size": 84, "duration": 3800}
```
Keep it under ~1700 px wide: lower `size` (default 96) for longer lines. Product shots can be cropped from `out/frames.mp4` after a first render.

**beats**: one big word or phrase at a time, fast (`words`, `word_ms` 650). Good just before the close.

**Voiceover keys on any scene:** `"vo": "<line id>"` starts that narration line with the scene and holds the scene at least as long as the line. `beats` also takes `"vos": [ids]` with `"pause_ms"` for one spoken line per beat. See `voiceover.md`.

`"anim": "blur"` on beats: each word comes into focus (blur to sharp) instead of popping. The reels look.

**motion** (v1.2, the reels look): a designed 1920x1080 world (your own HTML) under its own camera. This is the scene
for concepts, frameworks and anything that is not a live app: the camera starts on an extreme close-up, tilted,
tracks along the content as it appears, then pulls back to show the whole idea.
```json
{"type": "motion", "bg": "glow", "html": "assets/scenes/checklist.html", "duration": 6200, "exit": "dive",
 "start": {"focus": ".r1", "s": 2.0, "rx": 16, "ry": -22, "rz": 3},
 "events": [
   {"at": 300, "show": ".r1"},
   {"at": 750, "cam": {"focus": ".r2", "ms": 600, "ease": "out"}},
   {"at": 2450, "cam": {"x": 1040, "y": 560, "s": 1.15, "rx": 0, "ry": 0, "rz": 0, "ms": 1500}},
   {"at": 3300, "caption": "It looks like completion."},
   {"at": 4500, "click": ".btn", "ms": 800}]}
```
- `html`: a file (or inline HTML). Position things with `position:absolute; left/top` in world pixels, never with
  `transform` (the camera measures layout offsets). `assets/...` paths inside it are rewritten.
- Camera (`start`, `cam`): `x`, `y` world point to centre, `s` zoom, `rx`/`ry`/`rz` tilt in degrees, `ms`, `ease`
  (`inout`, `out`, `in`, `soft`, `linear`), `at` ([sx, sy] screen point, default centre), `focus` (selector; `x`/`y`
  given with it override). Values you leave out keep their last value.
- Events, each at `at` ms from the scene start: `show` / `hide` (selector, class `cls`, default `in`), `stagger`
  (selector, `gap` ms), `words` (blur the words of a `.split` element in one by one, `gap`), `click` (a big cursor in
  the world glides there in `ms`, presses, ripples: at high zoom it is the macro click look), `count` (`[sel, 78]`,
  `ms`, `pre`, `suf`, `dec`), `style` (`[sel, prop, value]` with a transition of `ms`: bars that fill, dots that
  travel), `caption`, `stage_js`, `cue`.
- Entrance classes: `in-o` (rise), `in-b` (blur to sharp), `in-p` (pop), `split` (word by word, with `words`),
  `faded` (push everything but the point back).
- Components (stage.css): `glass` card, `toast` (OS notification: `.ti` icon, `b`, `span`, `em`), `chk` (checklist
  row with `<i>` tick), `chip` (+ `solid`, `dash`, `on-good`, `on-bad`), `mono`, `tiles` + `tile` (3D tiles that flip
  up and ride a wave; `--w` = wave index; `good`/`bad`), `meter` (`.fill` + `.num`), `track` (`.run`) + `dot3`, `kin`
  (big centred line). Brand colours: `good`, `bad`, `amber`, `sky`, `mono` (font) in `brand`.
- **Icons**: write `<i data-lucide="target"></i>` (any name from lucide.dev/icons, 1,400+, stored in the skill so it
  works offline). It takes the text colour and size (1em). Wrap it as `<span class="ib" style="color:var(--bad)">...</span>`
  for a tinted rounded badge in that colour (`ib lg` for a bigger one). Give every list item, chip and heading an
  icon that says what it means (compass = context drifts, eye-off = unread, crosshair = goal). Never emoji or
  text glyphs like ✓ and ✕: they look cheap next to real icons.
- `exit: "dive"`: the camera flies into the frame and the next scene comes up behind it.
- `references/example-storyboard-reel.json` is a complete example (Agent 404, 12 scenes, 9 of them motion).

## Character look (v1.3): mascots on a pastel studio

For explainers about agents, assistants, teams or processes: each actor is a small character with a face,
on a soft pastel backdrop whose colour changes per beat (the Blender-reel look, done in CSS).

- `"bg": "studio:#dbf6ef"`: pastel seamless backdrop with a floor, in any colour (light scene, dark text). Pick
  pale tints of the brand; change the tint per beat.
- `<mascot class="chief drop" kind="bot" color="#3bdac0" size="400" acc="tie" name="Chief of Staff"
  style="left:740px;top:300px;--eyec:#b9fff2;--ant:#20206e"></mascot>` (expanded by render.py):
  - `kind`: `bot` (screen face, antenna, arms), `box` (cardboard with tape), `blob`.
  - `size`: width in px (height is 1.15x; the floor shadow sits at 0.9x of the height).
  - `acc`: any of `tie`, `hardhat` (`--hat`), `headset`, `glasses`. Give each character one accessory that says
    its job.
  - `name`: a label under it. Colours: `--eyec` (bot eyes), `--ant` (antenna ball), `--tape`, `--tie`.
  - Moods, added and removed with `show` / `hide` events (`"cls": "happy"`): `happy`, `worried`, `surprised`,
    `sleep`, `talk` (mouth moves: use while its bubble is up), `waving`, `hop`, `look-l`, `look-r`, `look-up`.
    `drop` = falls in and squashes when shown. Blinking and breathing run on their own.
- `bubble` (+ `r` for a right tail): what the character says. One short line, 3 to 8 words. This replaces
  captions in a character video.
- `ccard`: a contact or call card (`--cc` header colour, `cc-av`, `cc-h b/span`, `cc-b` with `small`, `.big`,
  `<wave n="26"></wave>` bars that move while the card has class `talking`, `ok-badge`).
- `x3d` + `splitc`: 3D extruded title that drops in letter by letter (use `words` on it).
- `desk`: a small desk with a laptop for a character to sit behind.

Rules: the character is the hero, so 300 to 400 px wide in its own scene and never cropped by the camera.
Expressions follow the story (look at the card it is talking about, surprised on a click, happy when done).
Use fictional names and messages only. Example: `references/example-storyboard-character.json` (Agent Office).

## Motion craft (v1.4)

Learned from prompt-motion.com (see `references/prompt-motion.md` for the full table).
- `"motion_blur": 4` (storyboard top): 4 subframes per frame, blended. Smooth blur on fast moves, 4x render
  time. Preview without it, turn it on for the final render. 2 shows ghost copies.
- `"ease": "spring"` / `"spring-soft"` in any `cam`. CSS can use `var(--spring)`.
- Motion `"exit": {"flood": "#3bdac0", "from": ".k2", "to": [940, 530], "ms": 420, "out_ms": 560}`: a circle
  grows from the element (or [x, y]) past the corners, the scene swaps under it, and it contracts toward `to` in
  the next scene. Use it on the 1 or 2 biggest turns.
- `class="split mask"`: words rise out of a mask line with the `words` event (no blur).
- `<div class="morph st" style="left;top;width:0;height:76px;border-radius:38px;background:#20206e;color:#fff">`
  plus events `{"morph": ".st", "to": {"w": 330, "bg": "#256ba2", "html": "<i data-lucide=\"hammer\"></i>Building 40%"}}`:
  one shape changes size, radius and colour on a spring while its text swaps.
- `in-s`: pops from zero on a spring (icons, badges).
- `"sfx": {"click": "...", "zoom": "...", "flood": "...", "scene": "...", "volume": 0.5}`: sound files placed by
  their peak on every cue of that kind (mix.py). Works with or without music.
- `qa.py --every 1.5` (run by make.py) also lists single-frame pops to check.

## Journey: one world, a guide that travels (v2.4)

When the user says "not like slides" or "make it interactive": put every scene in ONE motion scene as stations
side by side in a single world, and let a character travel between them while the camera follows. Nothing cuts;
the viewer moves through the story.

- Build each station as a normal scene HTML, then wrap it: `<div class="station st3" style="position:absolute;
  left:6600px;top:0;width:1920px;height:1080px;background:#fff">...</div>` (spacing about 2200 px, so a strip of
  plain background passes between pages). Prefix every event selector with the station (`.st3 .k1`) and add the
  station's x to every `cam` x.
- The guide: a `<mascot class="guide drop">` placed in the world, outside the stations. Between stations, at the
  same time: `{"move": ".guide", "to": [X + x, y], "ms": 1700}` (it walks, leans and looks the way it goes),
  a `cam` that eases out to `s` 0.82 halfway, then a `cam` that settles on the next station with `spring-soft`.
- Per station: one standing spot for the guide in empty space (never over text), at most one short bubble
  (`white-space:nowrap`; below the guide when it stands near the top), a mood that reacts to what appears.
- Finale: the other characters join the guide.
- Worked example: `example-journey-make.py` (Lumen POM AI video: 8 stations, 160 events, 85 s, built from a
  normal per-scene storyboard by shifting times, selectors and camera).

Event `move`: `{"move": ".guide", "to": [x, y], "ms": 1600}`. Mood `walk` is added automatically while moving.

## Circles look and portals (v2.5)

When a video "looks like slides", replace rectangles with circles and depth: a glossy 3D orb at the heart of each
idea, things orbiting it, rings that fill instead of bars, and transitions that travel.

- `<div class="orb [glass|pearl] fo in-s" style="left;top;width;height"><div class="oi">~3,670<span>FTE</span></div></div>`:
  3D orb from the brand colours (`accent`, `good`, `bg`). `fo` floats it, `in-s` springs it in.
- `<div class="orbit" style="left:cx;top:cy">` + children at polar positions: a slowly spinning ring (`rev` turns
  the other way). Good for "11 value streams around the POM", "213 teams as a ring of dots".
- Rings instead of bars: an SVG `<circle>` with `stroke-dasharray` = circumference and `stroke-dashoffset` =
  circumference, then a `style` event `[".arc", "strokeDashoffset", "<value>"]` fills it. A second arc rotated to
  start where the first ends shows the "unlocked" share. Wrap the SVG in a div to focus the camera on it.
- People as a ring of dark orbs around a core number; helpers (copilots) sit INSIDE the ring next to their person;
  labels go outside: left-aligned on the right side, right-aligned on the left side, centred top and bottom.
- **Portal transition**: `cam` focus on an orb, `s` 13, `ms` 900, ease `in`; at about 880 ms a `stage_js`
  `floodIn(960,540,colour,0)` hides the cut; jump the camera to the next station (`ms` 0); then
  `floodOut(x, y, 700)` toward the next station's main object. Alternate portals, floods and walks so no two
  transitions in a row are the same.
- Worked example: `references/example-circles-make.py` (Lumen POM AI v2: 8 stations, orbs, orbits, rings, portals,
  floods and walks, 72 s).

## Vertical cut (Instagram, TikTok, LinkedIn mobile)

```json
"vertical": {"title": "Your AI agent said done.\nNobody checked.", "handle": "Metis Strategy", "bg": "plain", "size": 80}
```
make.py then also writes `out/<name>-vertical.mp4` (1080x1920): the hook title fixed in the top third, the
16:9 video with rounded corners below it and the handle under it, on the plain brand background (`"bg"` can name an environment). Each title line stays on one line: keep lines under about 26 characters at `"size": 80`. Text in the video
shows at about 54% size on a phone, so keep scene text at 44 px or more and captions short.

## Environments and brand moments

Any scene can set `"bg"`: `dark` (default), `light`, `shadow` (warm wall, moving blind shadows), `mesh` (moving brand gradient),
`sunrise` (brand blue to warm orange), `rise` (navy that turns into the sunrise while the scene plays), `blue` (solid brand blue),
`desk`, `glow` (dark room lit from below: the reels "screen glow"; colours `glow-top`, `glow-base`, `glow-hot`,
`glow-mid`, `glow-edge`, mixed from `bg` and `accent` when not set), `glow-cool` (a second light: `cool-hot`,
`cool-mid`, `cool-edge`, from `good`; use one for the problem and the other for the answer), or an image file.
Take the light from the brand. Do not default to orange or sunset light: users found it off-brand. Light backgrounds switch the text to dark automatically. Colors come from `brand`:
`mesh1..3`, `mesh-bg`, `sun1..5`, `blue`, `blue-hi`, `accent-light` (highlight color on light scenes).
Use the client's palette (for Workday: blue `#0050b3`/`#0875e1`, orange `#ff9a1f`). Change environment with the story:
cool and flat for the problem, warm for the solution.

`"wipe": true` on a scene: a brand-color arc sweeps up before it starts. Use 2 or 3 times, on the big turns.

**chat**: a team channel; messages appear one by one; a cursor clicks the last link card and the camera dives in.
```json
{"type": "chat", "bg": "mesh", "channel": "# bt-rollout", "subtitle": "BT team", "messages": [
  {"name": "Grace Crozier", "color": "#f08c00", "time": "4:12 PM", "text": "...", "wait": 1900},
  {"divider": "Next day"},
  {"name": "Rohan Ray", "text": "Here you go:", "card": {"title": "Implementation Guide", "url": "script.google.com"}}]}
```
Messages with real people's names are a re-enactment: get their OK.

**device**: a screenshot on a laptop (`"screen"`), on a desk (`"bg": "desk"`) or floating (`"float": true`); the camera
pushes into the screen. Follow it with an app scene using `"enter": "zoomout"` so the push lands in the live app.
Make the screenshot from a first render (the fitted app window in `out/frames.mp4`).

**phone**: the live app on a 3D phone, with an optional laptop screenshot behind it. The phone loads its own copy of
the app before the scene (not filmed): `ready`, then `setup` steps (JS, one at a time, e.g. click through onboarding),
then `scroll_to`. Steps: `caption`, `tap` (selector, shows a touch ripple and clicks), `js`, `wait`.

**endcard**: brand arc drawing itself, a title and a sub line, centred. Good on `"bg": "blue"`.

**More environments**: `black`, `yellow` (`yellow`, `yellow-hi` in brand), `ice` (light frosted, Google-launch look:
`ice1`, `ice2`, `ice-bg`). `"wipe": "stripe"` sweeps a slanted brand band instead of the arc (for brands built on
diagonal stripes, like Stanley Black & Decker).

**pill**: a big glass button with an icon (`play`, `search`, `arrow`, `user`); a hand cursor clicks it and the camera
dives through. `{"type": "pill", "bg": "ice", "icon": "play", "text": "Meet the **playbook**"}`

**float**: up to 6 real pieces of the product (element screenshots) drifting in 3D around the camera, with a title.
`{"type": "float", "bg": "ice", "title": "...", "images": [{"file": "assets/pc_hero.png", "width": 720}, ...]}`
Capture pieces with Playwright `locator(...).screenshot()` at `device_scale_factor=2`.

**Logos**: `reveal` takes `"logo": "assets/logo.png", "stack": true` (logo above the name); `endcard` takes `"logo"`
instead of the arc. Set `logo-h` and `name-size` in `brand` to size them.

**Frameless app**: `"app": {"frame": "none"}` drops the browser bar; the app floats as a clean rounded panel.
Vary devices between videos: laptop, phone, frameless panel, floating pieces. Don't reuse the same one every time.

**app**: the real app in a browser window under a camera.
```json
{"type": "app", "enter": "flyin" | "plain" | {"macro": {"selector": "#x", "scale": 3, "tilt": [34,-28,6]}},
 "exit": "flyout" | "fade" | "stay", "steps": [...]}
```
`flyin` emits the `app_in` cue that the music drop locks to.

**clip**: a pre-rendered image sequence, usually a Remotion insert (charts, maps, Lottie, 3D). One source frame per
video frame, so render it at 1920x1080, 30 fps. See `remotion.md`.
```json
{"type": "clip", "frames": "clips/chart", "vo": "chart_line", "hold": 600, "start": 0, "end": 90}
```
`start`/`end` trim by frame index. With a `vo`, the last frame holds until the line finishes.

Every scene except the last exits automatically. The last scene stays on screen and fades out.

## App steps

Each step is one object. Keys run in this order: vo, caption, notify, dim, js, stage_js, tilt,
select, type, click, focus, fit, scroll_to, scroll, scroll_el, wait, hold, after.

| Key | Example | Does |
|---|---|---|
| `vo` | `"free"` | Starts a narration line (waits for the previous one) and, while a voiceover exists, shows its words as captions |
| `caption` | `"Pick your pod team"` / `null` | Caption pill at the bottom (null hides it). Ignored while a voiceover exists unless `"keep_caption": true` |
| `focus` | `"#team-select"` + `scale`, `ms`, `dx`, `dy`, `cy` | Camera moves to centre that element. `cy` = screen y to put it at (default 540) |
| `fit` | `true` + `ms` | Camera back to the whole window |
| `click` | `"#save"` + `after` | Cursor glides there, ripple, real click. `after` ms wait |
| `select` | `["#team", "Benefits"]` | Cursor + chooses an option |
| `type` | `["#search", "budget"]` | Types into a field |
| `scroll_to` | `"#w2"` + `offset`, `ms` | Scrolls the page so the element is near the top |
| `scroll` | `600` | Scrolls the page by px |
| `scroll_el` | `["#panel", 420]` | Scrolls inside a scrollable element |
| `tilt` | `[4, -7, 0]` + `ms` | 3D tilt of the window (degrees x, y, z). `[0,0,0]` to reset |
| `dim` | `true` | Darkens the stage around the window |
| `notify` | `{"initials": "ST", "title": "...", "body": "..."}` / `false` | Toast in the top right |
| `js` | `"..."` | Runs code in the app (e.g. simulate a teammate's change) |
| `stage_js` | `"..."` | Runs code on the stage |
| `wait` / `hold` / `after` | ms | `wait` and `after` are scaled by `pace`, `hold` is not |

Selectors must be **visible**: an element inside a hidden tab, filtered list or closed drawer
has no size, so the camera cannot find it. render.py prints `selector not visible` when that happens.
Open the tab or drawer first with a `click`. Long pages are scrolled automatically to the target.

## The app block and the demo app

```json
"app": {"page": "assets/app.html", "viewport": [1440, 900], "url_label": "app.example.com",
        "fake_date": "2026-11-04T09:30:00", "ready": "document.querySelector('#main')",
        "setup_js": "/* seed data */", "inject": ["assets/mock-backend.js"]}
```
- `page`: a standalone HTML copy of the app. Relative files next to it still load.
- `inject`: scripts run before the app's own code. Use this for a fake backend
  (replace `google.script.run`, `fetch`, Firebase, etc. with in-memory data) so the demo is
  deterministic and never touches real data.
- `fake_date`: the app sees this date and time (frozen clock), so "this week" and timestamps look right.
- `ready`: JS expression; rendering waits until it is true.
- `setup_js`: runs once when ready. Seed teammates, progress and history so the app looks lived in.
  Use realistic but fictional names, never real client data.
- `url_label`: text in the fake address bar.
- `caption_safe` (default `true`): the fitted window leaves a band at the bottom for the caption pill,
  so captions never sit over the app on a full-window shot. `false` restores the larger fit.

## Pages scene images

`python scripts/make_pages.py --example assets/old_p1.html` writes a starter page (a decisions table with
"TBD" owners). Edit it or write your own small HTML pages, then
`python scripts/make_pages.py assets/old_p1.html assets/old_p2.html --out assets/` renders each to a PNG at
the size the pages scene uses. Use realistic, fictional content. For `highlight.box`, convert the pixel
box on the PNG to percentages of its width and height.
