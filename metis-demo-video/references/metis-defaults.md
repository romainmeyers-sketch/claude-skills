# Metis defaults for demo videos

Read this before the first Metis video. It is what was settled while making the Onboarding Hub launch video (Oct 2026).

**Remotion** (added Oct 16, 2026): available as a toolbox for inserts via the `clip` scene, see `remotion.md`. Rohan uses
it under the Free License as an individual.

## Brand (apply `metis-brand-identity`)

```json
"brand": {"bg": "#20216f", "glow1": "rgba(60,219,192,.20)", "glow2": "rgba(0,189,239,.14)",
          "accent": "#3cdbc0", "text": "#ffffff", "muted": "#c9d3ee", "font": "Open Sans"}
```

- Metis Dark Blue `#20216f` and Metis Green `#3cdbc0` are the anchors. Open Sans, never reported as a font problem.
- **The skill's default palette (navy `#11294d` plus orange) is NOT Metis.** Always pass the brand block above.
- **Logo:** never redraw it. Lift the white-on-dark logo from the product itself (in a hub it is the `.brand-logo` / `.wz-logo`
  image, a base64 PNG you can read from the DOM) and pass it to the reveal scene: `"logo": "assets/metis-logo-white.png"`.
  The reveal then reads "METIS STRATEGY | <Product name>".
- Brand line for the close: "Driving change. Elevating leaders." A small credit line (for example "Created by the Building Team")
  goes in the statement scene's `foot`, on screen only, not spoken.

## Voices (ElevenLabs)

- **Key:** `~/.metis/demo-video/elevenlabs.key`, restricted to Text to Speech only. A restricted key cannot read the voice list,
  so test with a speech call, never `/v1/voices`. Never ask Rohan to paste the key in chat; the chat command box cannot take typed
  input. Have him use a Terminal tab (open one with `open_terminal_tab`) or open the key file in TextEdit and paste.
- **Rohan Ray:** voice ID `4hAJ1E6RXuQetYlei6qg` (his own voice, his consent).
- **Romain Meyers:** voice ID `PqVyZ4amIXbQIjxCzDQv` (uploaded by Rohan, Oct 2026). Use him per line with `"voice": "romain"`, or for a whole video with `voice.py --voice romain`.
- **Duo videos:** the Onboarding Hub video split Rohan/Romain about 51/49 by speaking time (`references/voiceover.md` 3b); Rohan opened and closed.
- **Pronunciation:** the voice says "Metis" wrong ("Meetis"). Respell with `"pronounce": {"Metis": "Metiss"}` (option 1 of the test
  clip). The respelling is not enough on its own, because a voice varies from take to take: **audition with `scripts/takes.py` and
  lock the good take per line with `"seed"`** (Rohan picked take 1 = seed 101 for the hook, the reveal and the dictionary lines).
  Do this for every line that contains "Metis", right after the first generation, and regenerate only those lines.
  Adding or changing seeds changes the cache key and regenerates every line: warn him, then ask for one full listen.
- Captions and on-screen text keep the real spelling "Metis".

## House rules for narration and on-screen text

- No em dashes. US spelling. Plain words, one idea per sentence, no consultant phrasing.
- Frame the old way as "PDF files" (what it was), not page counts or "two documents": some pages belong to coaches, not new hires.
- Do not announce your own activity or counts. Say what a thing is, not what it is not.
- When the old material is a set of PDFs, rasterize them with `pdftoppm -r 100 -png`, pick dense pages for the hook and the
  "before" fan, and highlight the part that shows the pain.
- Do not fabricate quotes or attribute pain points to named people. Use the user's own words for the problem.
- Real names on screen: only the roster the hub already shows, and the names Rohan said to use. Fictional or real, never record
  real progress, notes or emails typed by users.

## Music

Rohan supplies the track (Onboarding Hub video used "Next Horizon", 3:00). Find the loudness jump with `mix.py` and put it on
the `app_in` cue; with a voiceover, `duck` 0.8, `volume` about 0.62, `voice_volume` 1.2. Ask him to confirm he has the rights.

If the track is generated with ElevenLabs Music (Agent 404 video, Oct 2026), generate it ONCE and reuse it. Never regenerate it
because the narration or timing changed: loop or trim the existing file instead. A ~4-minute track per call burned the whole
40,000-credit monthly quota in one session and stopped a voice swap halfway. Rohan: "don't spend all the tokens to regenerate
music." Put any regeneration behind an explicit flag, and estimate a paid batch's credits against what is left before running it.

## Length and pacing

Length is a suggestion. Pacing and alignment come first: read `references/voiceover.md` "Sync", run `scripts/timeline.py`, cut
silent runs over about 4 s, give short-sentence runs their own lines with pauses (`beats` with `vos` and `pause_ms`). Do not pad to
reach 3:00. A full 2-minute voiceover video was accepted; he asked for fewer pauses, not more content.

## Hand-back

Open with the absolute path and size of the MP4 (and open or reveal it for him). Then: what changed, what is resolved, what is open,
what needs him. State the wall-clock budget before a long render and report each stage. Put sibling files (instructions, zips) on
the Desktop when he asks, and never write temp or intermediate files into a deliverable folder.

## Learned on the Onboarding Hub video (Oct 2026)

- "Read the guide." came out as past tense; fixed with `"say": "Reed the guide."` and a locked seed. The heteronym guardrail in `voice.py` now catches this class.
- Pause experiments: SSML breaks made the voice produce stray sounds, inserted silence sounded like a full stop. Rohan's final choice was the natural
  delivery with soft line edges (fade in/out, music dips slightly early and releases slowly) and about 0.3 s between lines.
