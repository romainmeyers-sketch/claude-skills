# metis-demo-video v2.7: ask first, and a client-pitch fork

1. **Intake questions** (SKILL.md 1a): used directly in chat, the skill first asks what the video is for, who watches,
   whose brand leads and who narrates, in one multiple-choice batch, maps the answers to a fork and says which one.
   Hub jobs and brief files skip it.
2. **New fork `client-pitch`** (`references/forks/client-pitch.md`): videos that sell Metis's work to a client from a
   proposal deck and an approved narration script. 11-beat structure, Metis brand with the client's logo as a guest,
   real client photography, NASA night satellite maps, glass cards, a horizontal step tracker, the confidentiality
   footer, mock-ups before building, never naming an undecided answer. Built from a Nov 2026 pharma pitch.
3. Router, fork table, `hub-mode.md` fork list (client-pitch is direct chat only until the hub page offers it) and
   seven new lessons (backdrop-filter, file:// textures, sentence splits, sharp imagery, review copies, refused
   downloads, mock-ups first).

# metis-demo-video v2.6: narration with no key (Kokoro)

1. **`"engine": "kokoro"`** in the voiceover block speaks every line with Kokoro-82M on this computer: no account, no
   key, no network after the first run. `voices` then maps names to Kokoro voice ids (`af_heart`, `am_michael`,
   `bf_emma`...). Stock voices only: it cannot reproduce Rohan's or Romain's cloned voice, which stays on ElevenLabs.
2. `voice.py` gets `synth_kokoro()` beside the ElevenLabs `synth()`, returning the same mp3 plus `[[word, start, end]]`
   timings, so captions, typed hook words, card reveals, `{pause}` markers, `pronounce` respellings and music ducking
   work unchanged. The default engine is still `elevenlabs`; existing storyboards and their cached audio are untouched.
3. `takes.py` says there is nothing to audition on a Kokoro storyboard (it is deterministic) and stops.
4. `setup.py --kokoro` installs it into the skill's venv (about 1 GB with PyTorch); the status line reports it.
5. voiceover.md section 1b documents the switch; measured on an M1 Pro at 0.6 to 0.7 s per short line.
6. **Everything Kokoro needs is pinned and verified** (`scripts/kokoro.lock.json`, `scripts/kokoro_lock.py`): 94
   packages at releases at least two weeks old, every PyPI sha256 for them, the spaCy model wheel by hash, and the
   Kokoro-82M model plus 54 voices at one Hugging Face commit with per-file sha256. `setup.py --kokoro` installs with
   `pip --require-hashes`, inspects each wheel for startup files, verifies and pickle-scans the model files against an
   allowlist of three names, and stops on any mismatch; `--voice <id>` adds a voice the same way. `voice.py` refuses
   to run outside that verified state and loads only those files, with Hugging Face set offline.
7. `scripts/kokoro_relock.py` rebuilds the lock from PyPI and the Hugging Face API when a newer pin is wanted.

# metis-demo-video v2.5: the circles look

1. **3D orbs** (`orb`, `glass`, `pearl`, from the brand colours), floating (`fo`) and spinning orbits (`orbit`, `rev`).
2. **Rings that fill** (SVG stroke-dashoffset through `style` events) instead of bars.
3. **Portal transition** (dive into an orb, flood hides the cut, come out in the next station), documented with
   floods and walks to alternate.
4. Example: `references/example-circles-make.py` (Lumen POM AI v2). Lessons on label placement around rings.

# metis-demo-video v2.4: journeys, not slides

1. **Journey pattern** (storyboard.md): every scene as a station in one world, a character guide that travels
   between them, the camera following. Example: `references/example-journey-make.py` (Lumen POM AI video).
2. **`move` event** (`{"move": ".guide", "to": [x, y], "ms"}`) and the **`walk`** mood (bob, lean, look ahead).
3. **Counters** format thousands with commas (3,670, not 3670).
4. Lessons: one-world journeys, bubble wrapping far right, flat brand pages with 3D characters.

# metis-demo-video v2.3: motion craft from prompt-motion.com

1. **References**: `scripts/motion_refs.py` lists and shows entries from prompt-motion.com by tag;
   `references/prompt-motion.md` says how to use them (reference only per the site's content signal: nothing
   stored, entries credited, techniques rebuilt here). New workflow step 3.
2. **Flood transition**: motion `"exit": {"flood": colour, "from", "to", "ms", "out_ms"}`; the next scene appears at
   once under it.
3. **Springs** (`"ease": "spring"` / `"spring-soft"`, `var(--spring)`), **mask-line text** (`split mask`),
   **morphing shape** (`morph` event), **spring pop** (`in-s`).
4. **Motion blur**: `"motion_blur": 4` renders 4 subframes per frame and blends them (2 ghosts on fast moves).
5. **Sound effects**: `"sfx"` maps cue kinds to files (or `{file, volume}`), placed by their peak; `{"cue": "pop"}`
   events add your own; music defaults to 0.55 when sfx are on. Works with voiceover and without music.
6. **QA**: `qa.py --every` also scans for single-frame pops.
7. Character example updated (Agent Office v2: floods, morph pill, motion blur, Mixkit sfx); lessons on levels.

# metis-demo-video v2.2: always on the latest version

1. Before every video the skill checks the hub's `skill/version.json`; if a newer version exists it asks the person
   to update (one question), installs it with `scripts/self_update.py` and keeps a backup of the old one.
2. The hub's version label reads the same file, so the page and the download can no longer disagree.

# metis-demo-video v2.1: one line to connect, then it keeps watching

1. "Check the Video Hub" now finds every waiting video in the person's hub projects (no project id to paste).
2. Presence document `data/users/<uid>/worker`, so the hub shows "Your Claude is watching".
3. After a render the skill offers to keep watching (loop while the chat is open, or a background scheduled task),
   so later renders and revisions start on their own.
4. Lessons from the first real hub render: flat lofi/calm tracks need `lift_on: 0`; `me` is only an alias under `data/users/`.

# metis-demo-video v2.0: one skill, five forks, the Video Hub

Merged the two diverged copies (installed Oct 16 with voiceover and Remotion; zip Oct 29 with the v1.1 to v1.3
looks) with a three-way merge against their common ancestor (Downloads/metis-demo-video-skill-v2.zip, Oct 12).
Six conflicts, all resolved keeping both sides; test renders of the character look and the classic hook, reveal,
beats and end card both pass on the merged engine.

1. **Forks**: `references/forks/` with a router and one file per video type: product-showcase, client-launch,
   character-explainer, informational (slide narrative or data story), social-reel. Each has its intake questions,
   structure with second marks, look, music mood and QA list, grounded in the five Metis reference videos and a
   frame-by-frame study of 12 launch videos (`research-2026-10.md`).
2. **Hub mode** (`references/hub-mode.md`): renders a Video Hub job on the person's own computer, reports progress
   and frames back to the hub, and picks up revisions typed there. `scripts/hub_preview.py` makes the share copy
   and contact sheet.
3. **Learning loop** (`references/learning.md`): signals from every brief, revision, rating and render; a weekly
   digest proposes skill edits; an admin approves before anything changes.
4. SKILL.md rewritten as a router. Metis palette is `#20216f` / `#3cdbc0` (the old navy plus orange default is not Metis).
5. Voiceover kept (scripts unchanged) but off for hub jobs.

# metis-demo-video v1.3: the character look

Built from a second Instagram reference (a Blender box character on pastel studios) and tested on the Agent
Office explainer.

1. **Mascots**: `<mascot kind="bot|box|blob" acc="tie|hardhat|headset|glasses" name="...">` in motion scenes,
   with moods (happy, worried, surprised, sleep, talk, wave, hop, look-l/r/up), drop-in, blinking and breathing.
2. **Studio backdrop**: `"bg": "studio:#colour"`, a pastel seamless with a floor, one tint per beat.
3. **Speech bubbles, contact and call cards** (with live waveform), **3D extruded titles** that drop in letter
   by letter (`x3d` + `splitc`), a small desk.
4. **Vertical cut** keeps a plain brand background by default and plays at 30 fps.
5. Example: `references/example-storyboard-character.json` + `example-character-scenes.py`.

# metis-demo-video v1.2: the reels look

Built from an Instagram reference reel (glow-lit screens, word-by-word blur text, 3D glass cards, tile waves,
counting pills, macro cursor clicks) and tested by rebuilding the Agent 404 overview video with it.

1. **`motion` scene type.** A designed HTML world under its own camera (tilt, pan, zoom, ease), driven by timed
   events: show, stagger, word-by-word blur, world cursor click (macro click at high zoom), count up, animated
   style (bars filling, a dot travelling a line), captions. `exit: "dive"` flies into the frame.
2. **`glow` and `glow-cool` environments**: a dark room lit from below, warm or cold, coloured from `brand`.
3. **Reels components** in stage.css: glass card, OS toast, checklist ticks, chips, 3D tile wave, meter, track.
4. **`beats` with `"anim": "blur"`**: words come into focus instead of popping.
5. **Icons**: Lucide (ISC, 1,400+ icons) ships in `assets/stage/lucide.min.js`; `<i data-lucide="name">` in any scene
   HTML becomes an SVG, and `.ib` makes a tinted badge. The glow light is mixed from the brand, never orange.
6. **Vertical cut**: `scripts/vertical.py` (run by make.py when the storyboard has `"vertical"`) writes a 1080x1920
   reel: fixed title on top, the video with rounded corners, a handle, on the same light.
7. Docs: storyboard.md (motion, vertical, glow), SKILL.md (reels look, trigger), lessons.md, a full example
   (`example-storyboard-reel.json` + `example-reel-scenes.py`).

Nothing existing changed behaviour: every addition is opt-in.

# metis-demo-video v1.1

Romain, this is v1.1 of your skill. It keeps what you built and fixes the nine things from the test, each checked on frames from a test render (58.7 s, 0 "selector not visible" warnings, 85 s render). It is a proposal to review, not a replacement. I'd take it, starting with the hook and caption fixes, and check the caption-safe fit against your own examples.

Four changes alter existing videos: the two-line hook (two-line hooks only), the caption look, the window about 8% smaller, and about 0.35 s less per scene change. The rest are opt-in or tooling.

1. **Two-line hook shows the whole question.** `hookStack()` in stage.js brings both lines back, stacked and centred, 500 ms after the last word. Optional hook field `stack_hold` (ms, default 900) adds reading time. One-line hooks are unchanged. Alters two-line hooks.
2. **Look follows the story.** Set `"auto_bg": true` in the storyboard and scenes without their own `"bg"` get a matching background, coloured from your brand (list in references/storyboard.md). Off by default.
3. **Captions no longer go see-through.** The caption pill faded to half-transparent on every change, so the app showed through. The pill now stays solid and the text crossfades (`cap()` in stage.js). Alters existing videos.
4. **Caption-safe fit.** App option `caption_safe` (default true) fits the window to 880 px instead of 960, centred at y=470, leaving room for the caption. `false` restores the old fit. Alters existing videos.
5. **No blank frames between scenes.** `XFADE = 300` in render.py replaces the 650 ms gap (450 ms for beats), so the next scene crossfades in. About 0.15 s less after a beats scene. Alters existing videos.
6. **"Before" pages helper.** `scripts/make_pages.py` renders small HTML files to PNGs at pages-scene size (560 x 725 at 2x); `--example` writes a starter. Tooling.
7. **QA timeline sheets.** `qa.py --every N` makes timestamped sheets of 12 frames, now 960 px wide (was 640). make.py passes `--every 1.5` on full renders. Old sheets are cleared each run. Tooling.
8. **Music note.** mix.py says so when the storyboard has no `"music"`. SKILL.md notes no track ships. Tooling.
9. **Dependency check.** `check_deps()` in common.py lists every missing package and prints one pip line; make.py, render.py and make_pages.py call it first. Tooling.

## Not tested, and rolling back

I didn't test your four example storyboards (assets not in the zip), the phone, chat, device and float scenes, the music path, or hooks with three or more lines. To undo any change, reverse it using metis-demo-video-v1.1.diff (12 files, about 300 lines). `caption_safe: false` restores the old fit, setting `XFADE` back to 650 restores the old scene gap, and leaving out `auto_bg` is its rollback.
