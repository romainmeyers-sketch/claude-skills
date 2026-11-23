# Lessons (problems already solved)

- **Screen recording lags.** Recording a live browser drops frames on heavy pages. That is why
  render.py freezes the clock (`clock.js`) and captures one frame at a time. Do not switch back to
  real-time recording.
- **Animations must use the page clock.** CSS animations, `setTimeout`, `requestAnimationFrame`,
  `Date` and `performance.now` are all virtualised. A library that uses Web Workers or its own
  timer thread will not animate: replace it with CSS or a rAF loop.
- **Measure timing on the timeline sheets, not the scene sheets.** Three frames per scene can make a
  short fade look like seconds of dead air, or catch the camera mid-move. Check claims about gaps or
  cropping on `out/qa/timeline_*.jpg` (or `qa.py --every 0.2` around the moment) before acting on them.
- **Scene changes crossfade.** Each scene starts leaving `XFADE` ms (render.py, 300) before the next one
  comes in, so there is no empty frame between scenes.
- **Smooth scrolling** (`behavior: 'smooth'`) does not run under the frozen clock. Use the
  `scroll`, `scroll_to` and `scroll_el` steps, which animate with rAF.
- **Hidden elements have zero size.** Tabs, filters and drawers hide content, so the camera
  cannot zoom to it. Click to reveal it first.
- **Sticky toolbars intercept clicks.** Clicks are dispatched with JS (`element.click()`), so this
  is handled. A mouse-only handler (`mousedown`) needs a `js` step instead.
- **The stage can be scrolled by the app** (`scrollIntoView` inside the iframe). The stage is
  locked with `overflow: clip` plus a scroll reset, so leave that in `stage.js`.
- **Real backends.** Never point the demo at a live backend. Inject a mock (see storyboard.md) so
  every render is identical and no real data is changed.
- **Fonts.** The stage waits for `document.fonts.ready`. If a font looks wrong, check `brand.font`
  is a Google Font name, or set `font_url`.
- **Color shift on some players.** mix.py converts full-range to TV range and tags it. Keep that
  so QuickTime, Slack and PowerPoint show the same colors.
- **Music too short.** mix.py repeats a beat-matched section before the outro. If the seam is
  audible, try a different `lift_on` or a longer track.
- **Reference videos.** When studying a YouTube example, keep it muted and seek frame by frame;
  hidden browser panes may render video black, so use captions and still frames.
- **Voiceover:** see `voiceover.md`. "..." in the text produces "uhh". Never ask anyone to paste an API key in
  chat, and clone a voice only with that person's consent.
- **Captions that paraphrase the narration feel wrong.** Viewers read and hear at the same time; any difference
  in wording reads as a mismatch. Captions are generated from the spoken words for that reason.
- **Actions before their words feel wrong.** A click that lands before the line describing it looks early. Put the
  `vo` step first and the action after it; check with `timeline.py`.
- **A list of very short sentences in one take sounds rushed.** Split into separate lines with a pause.
- **Grid items stack.** A big-word beat made of text plus a highlighted word (`Hope it <b>sticks.</b>`) became two
  stacked rows in a grid container. Beats are laid out as a flex row for that reason.
- **Recording a page's embedded sign-in wall.** Embedded videos or documents that need a login render as a
  "Sign in" box. Skip the step or keep it off screen.
- **A custom voice key restricted to text-to-speech cannot list voices.** Test with a speech call, not a voice lookup.
- **Do not trust a mono-downmix peak reading.** Measure the final file's peak per channel (`volumedetect`).
- **`voice.py --dry` must never replace real audio.** It refuses when a real manifest exists; test timing in a copy of the project or set `VOICE_DRY_FORCE=1`.
- **Ambiguous words get misread** (read, lead, live, close...). `voice.py` now stops before generating until each is resolved with `say` or `ok`.
- **Never use SSML break tags for pauses**: they produce stray sounds. Inserted silence sounds like a full stop; prefer natural delivery and separate lines with a gap.
- **Voice lines need soft edges.** Fade every line in and out and dip the music slightly before speech and release it slowly.
- **Respelling a line changes its audio.** Locked takes (`seed`) are tied to the exact text; changing the text means auditioning again.
- **Two voices: split by speaking time at section breaks, bookend with the same voice, match line levels, and re-audition any line that changes speaker** (seeds are per voice). See `voiceover.md` 3b.
- **Self-unpacking pages** (bundled "standalone" HTML) navigate once more after load. The phone scene retries its
  setup on a fresh frame; for the main app, make `ready` wait for real content (e.g. a button count).
- **Apps Script web apps** need a Google sign-in. Do not sign in for the user: `clasp list` + `clasp clone <id>`
  gets the source; most pages run standalone when `google.script.run` is missing.
- **ElevenLabs music** needs the Music permission on the API key (and a paid plan). Without it, ask the user to
  enable it or generate a track at elevenlabs.io/music; mix.py fits any track.
- **Motion scenes: position with left/top, not transform.** The camera and the world cursor find elements with
  offsetLeft/offsetTop (so tilts and zooms do not confuse them). An element centred with `translate(-50%)` is
  found off-centre. Use explicit `left`, `top` and `width`.
- **Selectors in motion events are scoped to the scene.** Never use a comma list (`.a, .b`): only the first part is
  scoped. Give elements a shared class instead (`g2`).
- **Content that appears while the camera is away is wasted.** On the timeline sheets, check that every item lands
  on screen; start a `stagger` after the camera arrives, not with it.
- **Pull-backs that go too far make the text tiny**, worst in the vertical cut (about 54% size on a phone). Pull back
  to s 1.1 to 1.2 when you can, keep text at 44 px or more, and keep the bottom 140 px free when a caption shows.
- **Render speed**: about 7 to 8 frames per second, so a 90 s video takes about 11 minutes. Preview with `--until`.
- **Orange and sunset light read as off-brand** (Romain, Oct 2026). The glow takes its colours from the brand;
  set `glow-*` and `cool-*` in `brand` from the client's palette.
- **Text glyphs look cheap.** ✓, ✕ and emoji next to designed cards look amateur; use Lucide icons (`data-lucide`).
- **Class names in motion scenes share one stylesheet with every scene type.** A mascot class `meet` picked up
  the reveal's "Meet" blur, and a mood called `wave` picked up the waveform bars (arms became lines). Give
  scene elements specific names (`planner`, not `meet`), and check new classes against stage.css.
- **Mascot name tags**: sized from `--ms`, so they sit just under the character at any size.
- **Lofi and calm tracks have no drop.** mix.py looks for a loudness jump to land on `app_in`; on a flat bed it picks a
  late one and the track starts in the middle. For `calm` and `lofi` library tracks set `"lift_on": 0, "lift_at": 0`
  (hit on the first Video Hub render, Oct 2026).
- **`me` is only an alias under `data/users/`.** In the Video Hub db, `signals/me/events` creates a literal path called
  "me" that admins never see. Use the person's real id outside `data/users/`.
- **"Still looks like slides" means shapes, not just motion.** Romain's second note on the Lumen POM video: more
  circles, more 3D, more transitions. Rectangles and bar charts read as slides even when the camera travels. The
  circles look (orbs, orbits, rings, portals) fixed it.
- **Counters inside generated HTML**: format the class name (`dv%d % k`); an unformatted `dv%d` left every counter at 0.
- **"Not like slides" means one world.** Romain rejected scene-by-scene cuts for the Lumen POM video ("3D bots
  should be travelling page by page"). The journey pattern (storyboard.md) fixed it: stations in one world, a
  guide that walks between them, the camera travelling with it.
- **Absolutely positioned bubbles far right in the world shrink to one word per line** (their available width is
  measured from the world's 1920 px). Give them `white-space:nowrap`.
- **Brand systems that forbid gradients and shadows**: keep the pages flat in the brand's colours and let only the
  characters carry the 3D look, in brand colours (Lumen: teal body, mint eyes). The user asked for that mix.
- **No motion blur on journeys.** Travelling about 2,200 px in under a second leaves 4 separate copies of every
  character even at `"motion_blur": 4`. Keep blur for zooms and short pans; journeys render with `1`.
- **Calm tracks with no drop**: set `"lift_at": 0` as well as `"lift_on": 0`, or the mixer finds a small "lift"
  mid-track and starts the music there (Lumen POM: it started 17.5 s in).
- **Motion blur needs 4 subframes.** With 2, a fast camera move shows two sharp copies (ghosting), which looks
  worse than no blur. Preview without blur, final render with `"motion_blur": 4`.
- **A flood swaps the scene instantly under it** (`window.__instant`), so the next scene must be fully drawn on its
  first frame: put its starting state in `start`, not in the first event.
- **Sound effect levels**: aim for 8 to 10 dB under the music around each cue. Clicks are short, so they need
  volume 1.0 to be heard; whooshes about 0.5, pops 0.55, floods 0.6 (Agent Office, -14 LUFS master). Below that
  they disappear on a phone. Sounds can be added after a render: append the cues to `out/cues.json` and re-run
  mix.py and vertical.py, no re-render needed.
- **Mixkit sound effects** (free licence, commercial use) used so far: 2568 cool interface click tone, 1490 fast
  whoosh transition, 1492 cinematic whoosh fast transition, 3005 explainer light pop. Preview MP3s download from
  `https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3`. Ask the user before downloading, keep a
  SOURCES.txt next to them.
- **With sound effects, lower the music** to `"volume": 0.55` (from 0.9). The master is normalised afterwards, so this only changes the balance: the sounds come through about 4 dB more (Romain asked for this on Agent Office).
- **Client pitches: agree the look on still mock-ups first.** On the Nov 2026 pharma pitch, two full renders were
  thrown away (a white slide look, then a DNA-helix background) before PNG mock-ups settled it. Render 4 or 5 key
  frames, and when a choice is open (map style) render the same frame in each option side by side.
- **No CSS `backdrop-filter` in rendered frames.** Under the software renderer it paints glass cards white and
  washed out. Use an opaque navy gradient (0.86 to 0.94) with a thin white border instead.
- **Local textures in headless renders** (three.js loading a file:// image) are blocked by CORS unless the browser
  starts with `--allow-file-access-from-files`.
- **Never split narration on every period.** A naive sentence split broke "a one-hundred-billion-dollar U.S.
  commitment" into two takes with a pause in the middle. Split only where the next word starts with a capital, or
  let `voice.py` read the whole line.
- **Satellite imagery must be sharp at 1080p.** NASA Black Marble (13,500 px) held up; a 4K Blue Marble day map,
  upscaled for a U.S. crop, drew "the quality is very bad". The NASA eoimages host times out from some networks;
  `assets.science.nasa.gov` serves the same records.
- **Send the full-quality file for review.** A 720p phone copy got judged on its compression. Label previews as
  previews.
- **Respect refused downloads.** When a client site or Wikimedia refuses a file (403, 429), do not retry with
  another user agent or referer; use what downloaded, or ask the person for the asset.
