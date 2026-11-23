# Learning loop: how the skill improves from every video

Nothing changes in the skill without a person approving it. The loop has three steps.

## 1. Signals (automatic)

Each signal is one document at `signals/<uid>/events/<eid>` in the Video Hub db. Only hub admins (Rohan, Romain and
other Editors) can read them. The hub writes one when a person approves a script, asks for a revision, rates a
version, or publishes to the gallery. You (the rendering Claude) write one after every render.

```jsonc
{
  "at": "ISO time", "source": "hub|worker", "kind": "script_approved|revision|rating|render|problem|gallery",
  "project": "<pid>", "fork": "product-showcase", "variant": "", "skill_version": "2.0",
  "length_s": 74, "version": 2,
  "text": "Make the hook shorter, it drags",      // the person's own words (revision, rating comment)
  "scope": "script|video", "rating": 4,           // 1 to 5 when kind = rating
  "render": {"seconds": 610, "warnings": 0, "fixes_before_report": ["caption overlapped the table"]},
  "lesson": ""                                    // worker only: a class-of-mistake lesson, one sentence
}
```

Keep signals free of client data: say "the client's dashboard" instead of naming the client or quoting its numbers.
A person can switch off "share my feedback to improve the skill" in the hub; then the hub writes no `text`.

## 2. Weekly digest (an admin runs it, or a scheduled task does)

An admin says "run the Video Hub learning digest". Claude then:
1. Lists `signals` events since the last digest (`hub/learning` doc, field `last_digest_at`).
2. Groups them by fork and by theme. A theme needs at least 2 independent people, or 3 events, before it becomes a
   proposal. Ratings of 4 to 5 with no revision mark what to keep.
3. Writes each proposal to `hub/learning/proposals/<id>`:
   `{created_at, title, why (evidence: counts, quotes), change (the exact edit: file + before/after text),
   files: ["references/forks/informational.md"], status: "proposed"}`. Typical targets: a fork's structure table,
   its intake questions, default length, music mood, `lessons.md`, `quality-checklist.md`.
4. Updates `hub/learning.last_digest_at` and reports a short summary.

## 3. Approval (a person decides)

Admins see proposals on the hub's **Admin > Learning** tab and click Approve or Reject (with an optional note).
Then an admin says "apply approved Video Hub proposals". Claude applies each approved change to the skill source in
`Video Generation Hub/skill/metis-demo-video/`, bumps the version in `CHANGELOG.md` with one line per proposal,
marks the proposal `applied`, rebuilds the distributable zip (`python _build/package_skill.py`), and says what to
tell colleagues ("re-install the skill from the hub's Setup tab"). Rejected proposals stay as a record so the same
idea is not proposed again.

## Admin tasks (say these to Claude in Rohan's or Romain's session)

- "add this track to the Video Hub library": copy the file to `Video Generation Hub/hub/music/`, add its row to
  `hub/music/library.json` (title, artist, moods, bpm, duration, licence, attribution, source URL), republish the hub
  so the file is served, then `set` its doc in `hub/library/tracks`.
- "run the Video Hub learning digest", "apply approved Video Hub proposals": above.
