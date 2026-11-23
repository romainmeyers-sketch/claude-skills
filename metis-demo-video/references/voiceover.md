# Voiceover (ElevenLabs, or Kokoro with no key)

Add narration to any storyboard. The renderer makes the picture follow the voice, the captions become the spoken
words, and the music dips under speech. Voiceover is optional: a storyboard without a `voiceover` block makes a
captions-and-music video exactly as before.

Two engines. **ElevenLabs** (the default) needs an account and a key and is the only way to get Rohan's or Romain's
cloned voice. **Kokoro** runs on this computer with no account, no key and no network after its first run, in stock
voices only (section 1b). Everything after section 1b works the same for both.

## 1. One-time ElevenLabs setup

You need an ElevenLabs account and an **API key** (the website login is separate from the API).

1. Sign in at elevenlabs.io. Open **Developers** (profile or bottom-left menu), then **API Keys**.
2. **Create API Key**, name it (for example `video`), and restrict it: turn on **Text to Speech** and leave the rest off.
3. Copy the key when it is shown (it is shown once, usually starting `sk_`).
4. Save it where the scripts look, **without pasting it into a chat or a storyboard**. Either set the environment
   variable `ELEVENLABS_API_KEY`, or put the key alone on one line in `~/.metis/demo-video/elevenlabs.key`.
   Easiest way on macOS/Linux, from a real terminal (not a chat box):
   ```
   read -rs "K?ElevenLabs key: "; echo; printf %s "$K" > ~/.metis/demo-video/elevenlabs.key; chmod 600 ~/.metis/demo-video/elevenlabs.key; unset K
   ```
   (zsh syntax; in bash use `read -rsp "ElevenLabs key: " K`.) Or open the file in a text editor, paste, save.
   A valid key file is about 50 characters. An empty or short file means the paste did not land.
5. **Voices:** use any voice in your account's *My Voices*. Cloned voices need a paid plan for API use and **the
   person's consent**. Copy a voice's ID from its page. A key restricted to Text to Speech cannot list voices; that
   is fine, the scripts only speak.

Never ask anyone to paste a key into chat, commit it to a repository, or put it in a storyboard.

## 1b. No-key voices (Kokoro)

Kokoro-82M is an open-weights text-to-speech model (Apache 2.0) that runs offline on this Mac. Add
`"engine": "kokoro"` to the voiceover block and the pipeline speaks every line locally: no account, no key, nothing
billed per character, and the word timings that drive captions, typed hook words, card reveals and music ducking are
produced the same way.

**Kokoro cannot reproduce Rohan's or Romain's voice, or any cloned voice.** It ships stock voices only. Anything that
must sound like a real person stays on ElevenLabs; use Kokoro for a neutral narrator, a draft to check timing before
spending credits, or a video made on a machine with no key. (Video Hub jobs still carry no narration; see SKILL.md 5.)

**Install once** (about 1 GB into `~/.metis/demo-video/.venv`, mostly PyTorch, plus 330 MB of model files in
`~/.cache/huggingface`; nothing touches the system Python):

```
python3 scripts/setup.py --kokoro
```

**Everything it installs is pinned in `scripts/kokoro.lock.json`, and nothing else gets in.** The lock holds the exact
version of all 94 Python packages Kokoro pulls in (each one a release at least two weeks old when the lock was made),
every sha256 PyPI publishes for those releases, the spaCy English model wheel by hash, and the Kokoro-82M model and
voice files at one git commit of hexgrad/Kokoro-82M with their sha256 from the Hugging Face API. The setup step
downloads with `pip --require-hashes`, looks inside every wheel for startup `.pth` files before installing, fetches
the model files at that commit, checks each one's size and sha256, and scans each pickle so it imports nothing beyond
the three names in the lock's allowlist (kokoro loads them with `torch.load(weights_only=True)` as well). Any
mismatch stops the step with a plain message. `voice.py` runs the same checks before it speaks and refuses to run
otherwise, and it sets Hugging Face offline, so a Kokoro render makes no network request at all.

Seven voices come with the setup (`af_heart`, `af_bella`, `af_sarah`, `am_michael`, `am_adam`, `bf_emma`, `bm_george`).
Any of the 54 voices at the pinned commit can be added, verified the same way:

```
python3 scripts/setup.py --kokoro --voice bm_lewis
```

**The block** is the same as ElevenLabs with `engine` set and Kokoro voice ids under `voices`:

```json
"voiceover": {
  "engine": "kokoro",
  "default": "narrator",
  "voices": {"narrator": "af_heart", "second": "am_michael"},
  "pronounce": {"Metis": "Metiss"},
  "lines": {
    "hook": "Your video, with no key needed.",
    "close": {"text": "Your first day, {pause 0.4} handled.", "voice": "second"}
  }
}
```

- **Voice ids**: the first letter is the language (`a` American, `b` British English; the scripts pick the matching
  pipeline from it), the second is `f` or `m`. Start with the seven installed above. The full list with quality grades
  is `VOICES.md` in the model's Hugging Face repository (hexgrad/Kokoro-82M); a voice that is not in the lock, or not
  yet downloaded, makes `voice.py` stop and name the `setup.py --kokoro --voice` command to run.
- **Ignored with Kokoro**: `model`, `settings` and a line's `seed`. Kokoro is deterministic (same words, same voice,
  same audio every time), so `takes.py` has nothing to audition and says so. To change how a line sounds, change the
  words, a `pronounce` respelling, or the voice id.
- **Unchanged**: `pronounce`, `say`, `{pause N}`, `cadence`, `gap`, per-line `voice`, `--voice`, the heteronym guard,
  captions, ducking and caching (Kokoro audio is cached per voice and text, separately from ElevenLabs audio, so
  switching engines back and forth regenerates nothing).
- **Words the dictionary does not know** (respellings like "Metiss", brand names) are handled by the espeak fallback
  that installs with the package (`espeakng-loader`, a pinned wheel in the lock); no Homebrew.
- **Re-pinning** is a deliberate act, never automatic: `scripts/kokoro_relock.py` rebuilds the lock from PyPI and the
  Hugging Face API (two-week-old releases, fresh hashes, a chosen model commit) and prints what moved; review that,
  run `setup.py --kokoro`, and re-render one storyboard before trusting it.
- **Speed on an M1 Pro**: about 0.6 to 0.7 s per short line, plus about 5 s to load the model once per run. A 65 s
  paragraph took 14 s.

## 2. The storyboard block

```json
"voiceover": {
  "engine": "elevenlabs",
  "model": "eleven_multilingual_v2",
  "default": "alex",
  "voices": {"alex": "<voice id>", "sam": "<voice id>"},
  "pronounce": {"Acme": "Ack-mee"},
  "settings": {"stability": 0.5, "similarity_boost": 0.85, "style": 0.15, "use_speaker_boost": true},
  "lines": {
    "hook": "Your first day used to start with a PDF.",
    "setup": "It starts with a quick setup. Pick your role, and the app adapts to you.",
    "close": {"text": "Your first day, handled.", "voice": "sam"}
  }
},
"music": {"file": "assets/music.mp3", "lift_on": "app_in", "volume": 0.62, "duck": 0.8, "voice_volume": 1.2}
```

`engine` defaults to `elevenlabs` and can be left out; `kokoro` is the no-key engine of section 1b.
Reference a line with `"vo": "<id>"` on a scene or an app step. `voice.py` generates every line once and caches it
per (voice, text, settings), so re-running only pays for lines that changed.

```
python scripts/voice.py storyboard.json            generate (needs the key)
python scripts/voice.py storyboard.json --dry      no API call: estimated lengths, to test timing
python scripts/voice.py storyboard.json --voice sam   the whole video in another speaker's voice
```

## 3. Switching or adding a speaker

Voices are data. To use a second person: add their ID under `voices`, then change `default`, put `"voice": "sam"`
on specific lines, or run `voice.py --voice sam`. Cached audio is keyed by voice, so switching back is free.
Re-run `render.py` and `mix.py` after generating.

## 3b. Two or more speakers: splitting the lines

A video with two voices (a duo, a presenter and a colleague) works when the handoffs feel like a conversation, not alternate-line ping-pong.

1. **Split by speaking time, not by line count.** List every line with its duration (`out/voice_manifest.json`), then give each
   speaker about the same total (aim for 48/52 or closer).
2. **Hand off at section breaks**, where the topic changes ("Meet the product", "Day 1", "Meet people", "Learn the firm"), and
   keep related lines with one voice. Never split a sentence or a short run (a `beats` set) across voices.
3. **Bookend with the same voice**: one speaker opens the video and says the closing line, so it feels framed.
4. **Hand the product reveal to the second voice** ("Meet X..."): it is the natural turn from problem to solution.
5. In the storyboard, give the second speaker's lines `"voice": "<name>"` (the others fall back to `default`):
   `"reveal": {"text": "...", "voice": "sam"}`. Add the voice under `voiceover.voices`.
6. **Locked takes belong to one voice.** A line's `seed` was auditioned in that voice only. When a line changes speaker, drop its
   seed and audition again with `takes.py <storyboard> <line> --voice <name>`, especially for lines with a tricky word.
7. **Match the levels.** `mix.py` brings every line to the same loudness (`voice_match`, default on, at most about 4 dB of
   correction per line), so a handoff between voices does not jump louder or quieter. Check the printed correction range.
8. Check the result: `timeline.py` shows the order; count the handoffs and each speaker's total, and listen to every handoff once.

## 4. Pronunciation

Respell the word the way it should sound in `pronounce`. The voice gets the respelling; captions and on-screen text
keep the real spelling because word timings are mapped back to your original words. Listen, adjust, repeat.

**A voice does not say a word the same way every time.** A respelling that sounds right in one take can come out
wrong in the next (a brand name sliding into the word before it, for example). So audition and lock:

```
python scripts/takes.py storyboard.json hook reveal --n 4
```

This writes `out/takes.mp3`: for each line, four takes announced ("hook, take one", ...). Listen, then lock the take
you like by giving that line a `seed` (take one = seed 101, take two = 202, take three = 303, take four = 404; or pass
your own with `--seeds`):

```json
"lines": {"hook": {"text": "Your first day at Acme started with a PDF.", "seed": 101}}
```

The same text with the same seed gives the same audio every time, so it sounds identical on every re-render. Run
`voice.py` again (only that line is regenerated) and confirm the new line's length matches what you auditioned.
Do this for every line that contains a tricky word, and for any line whose delivery you want to keep.

## 5. Writing narration that sounds human

- Short sentences, one idea each, roughly 2.5 words per second. 60 to 120 s of speech is plenty.
- Say what the viewer sees at the moment they see it ("Pick someone, and see when they are free").
- Write numbers and symbols as you would say them. Avoid "..." (it produces "uhh"), avoid long lists in one breath.
- A run of very short statements ("Read it. Remember it. Hope it sticks.") sounds rushed in one take. Use separate
  lines with a pause between them (see `beats` below).
- Plain words only. No em dashes (they read oddly aloud).

## 5b. Pronunciation guardrail: words that can be said two ways

Some words are spelled the same but said differently by tense or part of speech: **read** (reed / red), lead, live, close, wind,
tear, record, present, content, project, resume, minute, object and more. A short line gives the voice almost no context, so
"Read the guide." can come out as past-tense "red". `voice.py` scans every line before it spends anything and stops with a list
until each flagged word is resolved, one of two ways:

```json
"beats1": {"text": "Read the guide.", "say": "Reed the guide.", "seed": 101}     // the voice is told "Reed"; screen keeps "Read"
"x":      {"text": "...", "ok": ["read"]}                                         // the default reading is already right
```

`say` must have the same number of words as `text` (captions and timings are mapped word for word). Audition with `takes.py`,
lock the good take with `seed`. When you write narration, choose wording that is not ambiguous where you can ("Start with the guide").

## 5c. Cadence, pauses and edges (what worked and what did not)

What was tried on a real video and what the user decided:

- **Leave the voice's own timing alone.** Punctuation and sentence length already give a natural rhythm. Write short sentences.
- **Never send SSML `<break>` tags or breath markers.** They made the voice produce stray sounds and odd extra voices; every
  take sounded wrong.
- **Silence inserted into a finished take (`{pause 0.5}` markers, `voiceover.cadence`) is supported but sounds like a full stop.**
  Use it rarely (0.2 to 0.35 s), audition it in context, and drop it if it feels unnatural. It is off by default.
- **For a deliberate beat, use separate lines** with a gap between them (`"gap"` on the line, or the `beats` scene with `vos` and
  `pause_ms`). Each line keeps its natural delivery.
- **`voiceover.gap`** (default 0.45 s) is the silence between lines. About 0.3 s felt conversational; 0.5 s felt like AI.
- **Edges.** Hard starts and stops make a voiceover feel abrupt. `mix.py` fades every line (`voice_fade_in` 0.05 s,
  `voice_fade_out` 0.18 s) and starts dipping the music 0.3 s before speech (`duck_lead`) and releases it slowly
  (`duck_release` 0.7 s). Tune those four numbers in the `music` block if a line still feels clipped or the music pumps.
- Align the pause with what is on screen: start a line, then the click or camera move it describes (section 6).

## 6. Sync: how picture follows voice

`render.py` handles it; the storyboard just has to be ordered correctly.

- **Captions are the narration.** While a voiceover exists, plain `"caption"` keys are ignored; each spoken
  sentence appears as the caption when it is spoken (long sentences split at commas). To force a caption anyway,
  add `"keep_caption": true` to that step.
- **Line first, then action.** `{"vo": "free"}` as its own step, followed by the `click` / `focus` it describes.
  The click glide takes about 0.8 s, so the action lands just after the first words.
- **No overlap.** Starting a line waits for the previous one to finish. Steps with `wait`/`after` between two lines
  create silence; keep the longest silent run short (about 4 s) unless you want a breather.
- **Scenes wait for the voice** (static scenes hold at least as long as their line), and animated text is timed to
  the words:
  - `hook`: each typed word appears as it is spoken (the line's word count must equal the words in the
    `lines`; keep the on-screen text identical to the spoken words).
  - `reveal`: the logo lands on the word after "Meet the"; the pill words follow the second sentence if its word
    count matches the pill text.
  - `pages` points and `cards`: the k-th point / card appears when the (k+1)-th / k-th spoken sentence starts, so
    write one sentence per point or card, in the order they appear.
  - `statement`: `"foot"` (a small last line) appears when the second sentence starts, or after `foot_ms` if the
    narration has only one sentence. Leave it out of the narration to keep it visual only.
  - `beats`: either `"vo": id` (words appear on the sentence starts) or, for a slower rhythm,
    `"vos": [id, id, id]` with `"pause_ms": 850`: each beat is its own line with a pause between.
- **Check it:** `python scripts/timeline.py storyboard.json` prints every spoken phrase beside every click, zoom and
  scene change, in time order. Look for a CLICK well before the SAY that describes it, and for long runs with no SAY.

## 7. The mix

`mix.py` places each line at its cue, ducks the music while anyone speaks (`duck`: 0.8 means the music drops by 80%
under speech and returns in the gaps; smooth attack and release), adds the voice (`voice_volume`), then
loudness-normalises the whole mix with a limiter, so only the balance matters. Raise `duck` if speech is hard to
hear, lower `volume` if the music is too present in the gaps. The track's biggest loudness jump is placed on the
`app_in` cue, so the drop still lands as the app flies in.

## 8. Cost and safety

Each line is billed once by ElevenLabs (characters). Cached lines are free to re-render. Kokoro lines cost nothing. A restricted key (Text to
Speech only) is safer. Keep the key file out of any folder that syncs or is committed.
