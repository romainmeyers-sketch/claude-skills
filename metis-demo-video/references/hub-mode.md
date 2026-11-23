# Hub mode: rendering a Video Hub job on this computer

The **Video Hub** (https://claude.ai/artifact/H6yLztfVoZyzpH5owCaq3N) is a Claude artifact anyone at Metis opens to brief a video. Claude inside the hub asks the
questions, picks the fork and writes the script with the person. The hub cannot render (that needs Python, a browser
and ffmpeg), so **you render it here**, report progress back to the hub, and pick up revisions the person types there.
The person never has to learn the storyboard format.

## 1. Pairing (one line, the same every time)

The hub tells the person to say, in Claude Code or the Code tab of the Claude desktop app:

```
Check the Video Hub and render my videos: https://claude.ai/artifact/H6yLztfVoZyzpH5owCaq3N
```

or just "check the Video Hub". **You do not need a project id**: list the person's projects and work on every one that
is waiting (section 3, step 0). Older hubs showed a per-project line
(`Video Hub job | <url> | user <id> | project <id>`); if someone pastes one, work on that project only.

You need the `ArtifactData` tool (it reads and writes the hub's data **as this person**) and the `Artifact` tool
(`action: "read"` with `path` to fetch the hub's music files and the person's uploads). Load them with ToolSearch
(`select:ArtifactData,Artifact`) if they are deferred. If either is missing in this Claude app, fall back: ask the
person to click **Download brief** in the hub and hand you the `video-brief.json`, then work from the file and report
in chat.

## 2. The data (all paths relative to the artifact's db)

How to address it with `ArtifactData` (tested Oct 30, 2026):
- `me` stands for the person's own id under `data/users/`, so you never need to type the id.
- Paths alternate collection / document. The person's projects are documents in the **collection** `data/users/me`
  (doc id = project id). A project's sheets are the collection `data/users/me/<pid>/sheets`.
  So: `get` with `collection: "data/users/me", doc_id: "<pid>"`; `list` with `collection: "data/users/me"`.
- Every write to an existing document needs `if_version` = the `version` you last read. Read, then `update` with that
  version; if it fails because the person changed something in the hub meanwhile, re-read and redo the write.

| Path | Who writes | What |
|---|---|---|
| `data/users/<uid>/<pid>` | hub + you (different fields) | The project. Private to this person: nobody else, Rohan included, can read it. |
| `data/users/<uid>/worker` | you | Presence: `heartbeat_at`, `machine`, `watching`, `until`. The hub shows "Your Claude is watching" while `heartbeat_at` is under 5 minutes old, or `watching` is true and `until` is in the future. |
| `data/users/<uid>/<pid>/sheets/v<N>` | you | Contact sheet for version N as a base64 JPEG (under 180 KB) so the person sees frames in the hub. |
| `signals/<uid>/events/<eid>` | hub + you | Learning signal (see `learning.md`). Readable by hub admins only. Also `set` the parent doc `signals/<uid>` to `{"last_at": "<ISO>"}` so admins can list who has signals. **Use the real id here** (the `me` alias works only under `data/users/`; `signals/me/...` silently creates a literal "me" path). Read the real id off any `data/users/me` result. |
| `hub/library/tracks/<tid>` | admins | Music library metadata. The audio is a published file of the artifact at the track's `file` path. |

Project fields. **Write only the fields marked "you", always with `update` (merge), never `set`**, so you never
overwrite what the person is typing in the hub:

```jsonc
{
  "schema": "metis-video-project/1",
  "title": "Onboarding Hub launch",
  "brief": {                       // hub
    "fork": "product-showcase",    // product-showcase | client-launch | character-explainer | informational | social-reel | client-pitch (direct chat only until the hub page offers it)
    "variant": "",                 // e.g. "slide-narrative" | "data-story" for informational
    "purpose": "...", "audience": "...", "branding": "metis",   // metis | client
    "client": {"name": "", "palette": ["#..."], "font": "", "logo_asset": ""},
    "length_s": 75, "formats": ["16:9", "9:16"],
    "product": {"name": "", "access": "html|url|apps-script|repo|screenshots|none", "where": "", "notes": ""},
    "before": "", "key_points": ["..."], "cta": "", "names_policy": "fictional",
    "uploads": [{"asset_id": "...", "url": "...", "name": "...", "kind": "screenshot|logo|doc|image"}],
    "voiceover": false
  },
  "script": {                      // hub (the person approved it there)
    "approved": true, "approved_at": "...",
    "scenes": [{"n": 1, "type_hint": "hook", "seconds": 5, "on_screen": "...", "visual": "...", "camera": "...", "bg": "cool"}]
  },
  "music": {"mode": "library|own|silent", "track_id": "", "file": "music/....mp3", "title": "", "own_name": ""},  // hub
  "render_request": {"version": 2, "at": "...", "kind": "draft|final"},   // hub: bump version = please render
  "revisions": [{"id": "r3", "at": "...", "text": "Make the hook shorter", "scope": "script|video", "for_version": 1}], // hub
  "answers": [{"question_id": "q1", "text": "...", "at": "..."}],          // hub
  "worker": {                      // you
    "status": "connected|building|rendering|qa|done|needs_input|error",
    "stage": "Rendering frames", "progress": 0.45, "eta_min": 6, "note": "...",
    "heartbeat_at": "ISO time",    // update at least every 2 minutes while working or listening
    "machine": "short label the person will recognise",
    "question": {"id": "q1", "text": "...", "options": ["...", "..."]},    // or null
    "applied_revisions": ["r1", "r2"],
    "rendered_version": 2,
    "outputs": [{"version": 2, "path": "/Users/.../Downloads/....mp4", "share_path": ".../...-share.mp4",
                 "duration_s": 74.2, "size_mb": 23.1, "made_at": "...", "notes": "What changed in this version"}]
  }
}
```

## 3. The loop

0. **Find what is waiting.** `list` the collection `data/users/me`. Projects are the documents with
   `schema: "metis-video-project/1"`. A project is waiting when `script.approved` is true and either
   `render_request.version` is higher than `worker.rendered_version` (missing counts as 0), or `revisions` holds ids
   not in `worker.applied_revisions`. Nothing waiting: say so in one line, and offer to keep watching (step 10).
   Several waiting: tell the person the list and the total wall-clock budget, then do them one after another.
   Also `set` the presence document `data/users/me` / `worker`:
   `{"schema": "metis-video-worker/1", "heartbeat_at": "<now>", "machine": "<short label>", "watching": false}`
   (read it first and pass `if_version` when it exists). The hub's sidebar shows "Your Claude is watching" from it.
1. **Connect.** `get` the project (`collection: "data/users/me"`, `doc_id: <project id>`). Write `worker.status = "connected"`, `heartbeat_at`, `machine`. Tell the person in
   one line what you found (title, fork, scene count, music) and the wall-clock budget.
2. **Check setup** with `python3 scripts/setup.py` (first time only on this machine).
3. **Gather inputs.** Fetch uploads (`Artifact` read with `path` = asset id) and the chosen library track
   (`Artifact` read with `path` = the track's `file`) into `<project folder>/assets/`. For `music.mode = "own"`, ask
   the person in chat for the file (it never leaves their computer). Project folder:
   `~/Metis Videos/<title>/` unless the person names another; never a scratchpad.
4. **Need something?** (the app, a login-free copy of a hub, a palette) Write `worker.question` with 2 to 4 options
   and `status: "needs_input"`; the person answers in the hub (`answers`) or in chat. Ask once, batched.
5. **Build.** Read the fork file for `brief.fork`. Turn `script.scenes` into `storyboard.json` (the approved script
   is the contract: same scenes, same on-screen words; you choose scene types, camera and timing). `voiceover` stays
   false. Write `status: "building"`.
6. **Render.** `make.py` with `status: "rendering"`; update `progress` and `heartbeat_at` at each stage. Preview with
   `--until 2` first on version 1.
7. **QA** (`status: "qa"`) with the quality checklist and the fork's QA list. Fix before reporting.
8. **Report.** Copy the MP4 to `~/Downloads/<title> v<N>.mp4`. Run `python scripts/hub_preview.py out/<name>.mp4`,
   which writes a share copy under 18 MB and a contact sheet JPEG as base64. `set` the sheet doc
   `sheets/v<N>`, then `update` the project: `status: "done"`, `rendered_version`, append to `outputs` (send the whole
   array), `applied_revisions`. Write one signal (`learning.md`). Tell the person the path, size and length.
9. **Listen for revisions.** Revisions arrive in `revisions` with ids you have not applied, or as a higher
   `render_request.version`. On a revision: apply it to the storyboard (script scope: also honour the updated
   `script.scenes`), re-render, report as version N+1 with `notes` saying what changed.
10. **Offer to keep watching**, so the person never has to come back and paste anything. Ask once, multiple choice:
    - (Recommended) **Watch while this chat is open**: use the `loop` skill (`/loop 2m check the Video Hub`) or
      `ScheduleWakeup`; each check runs step 0, and `update`s the presence document with `heartbeat_at`,
      `"watching": true` and `"until"` (now + 2 hours). Stop after two hours idle.
    - **Watch in the background**: if the scheduled-tasks tool is available, create a task that runs
      "check the Video Hub and render my videos" every 10 minutes while the computer is on (pin the task to the
      person's video folder). Say plainly that each check uses a little of their Claude usage, and how to turn it off.
    - **No thanks**: tell them to say "check the Video Hub" after they change something.
    When watching stops, `update` the presence document with `"watching": false`.

## 4. Rules

- The project is the person's private space: never copy its contents anywhere except their project folder.
- Never write `brief`, `script`, `music`, `revisions`, `answers` or `render_request`; those belong to the hub.
- Send whole arrays on `update` (`outputs`, `applied_revisions`); there is no array append.
- Every existing document needs its current `version` as `if_version` (in a `batch` too): `get` it first, including
  `signals/<uid>` and `data/users/me/worker`, or the whole batch is refused and writes nothing.
- An `error` status always carries a plain-English `note` saying what the person can do.
- No voiceover on hub jobs. No real client data on screen unless the brief says the client approved it.

## 5. Music

The Metis library lives in the hub (`hub/library/tracks`), each track with mood tags, licence and attribution. Moods:
`launch` (build and drop), `uplift` (bright, corporate), `calm` (piano / ambient bed), `lofi` (laid back, no drops).
When a track's licence needs attribution (CC BY), add it to the end card's small foot line or the post caption, and
say which in the report. Admins add tracks by telling Claude "add this track to the Video Hub library" (see
`learning.md` "Admin tasks").
