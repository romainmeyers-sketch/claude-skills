---
name: pls-fix
description: Review a deck (.pptx) or document (.docx) where the user has left comments, make the edits the comments ask for, and reply to each comment inside the file, threaded under it, never deleting or resolving any comment (resolved ones included). Use when the user says "review my comments", "I left comments", "address/incorporate my comments", "go through the comments on the deck", "/pls-fix", "pls fix", or replies to an earlier Claude reply inside the file and asks you to pick it up.
argument-hint: "[file path or name — optional; defaults to the most recently edited .pptx/.docx with open comments]"
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Skill
---

# Review comments: edit, then reply in-thread

The commented file is the new base. Do what the comments ask, nothing more,
and answer every open comment inside the file so the conversation stays in the
deck/doc.

Helper script (all comment reads/writes go through it; it never deletes,
edits or resolves existing comments):

```
PY="$(command -v py || command -v python)"   # Windows launcher, else python
CM="$HOME/.claude/skills/pls-fix/scripts/comments.py"
```

Requires Python with `lxml` (`pip install lxml`; already present if
`python-pptx` is installed).

Supported: `.pptx` (modern threaded comments and legacy comments) and `.docx`.
For Google Docs/Slides, `.gdoc` stubs, or `.xlsx`, say so and ask for a
.pptx/.docx export instead of guessing.

## 1. Find the file: the user's last-saved version is the base

The base is always the file as the user last saved it, with their direct
edits and their comments. It is never the version Claude last generated,
a build script's output, or anything held in this conversation's memory.

- `$ARGUMENTS` names it (path or partial name) → use that.
- Otherwise pick the most recently modified `.pptx`/`.docx` in the working
  folder that has open comments (run `list` on the top few candidates). If more
  than one is plausible, ask which one with AskUserQuestion. Don't guess.
- Watch for the user saving a copy under a new name (e.g. "v3 MS edits",
  "(100726)"). If a newer user-saved copy of the deck Claude last produced
  exists, that copy is the base, not Claude's file.
- Re-read the file from disk now, even if Claude built or edited it earlier in
  this session. Assume the user changed things since.
- If a `~$<filename>` lock file sits next to it, the file is open in Office.
  Stop and ask the user to save and close it first, otherwise their unsaved
  edits and yours will collide.

## 2. Back up and snapshot (always, before any edit)

```
"$PY" "$CM" backup   "<file>"              # copy into ~/.claude/comment-backups/
"$PY" "$CM" snapshot "<file>" "<scratch>/snap.json"
"$PY" "$CM" list     "<file>" --all --json "<scratch>/comments.json"
```

## 3. Decide which threads need action

Act on a thread when its status is not `resolved` AND its last word is not
Claude's: either no reply yet, or the user (or a teammate) replied after
Claude's previous reply. That second case is the interactive loop: read the
whole thread and answer the newest message.

Leave alone: resolved threads (never touch, never reply), and threads where
Claude's reply is the last one.

Comments by people other than the user are input too. Treat them as requests
to weigh, but if one conflicts with the user's own comments, or needs a call
only the user can make, reply in the thread and flag it in chat rather than
picking a side.

## 4. Plan in chat before editing

Post a short table: comment # / slide or location / what it asks / what you'll
change. If a comment is ambiguous, the plan entry is "reply with a question,
no edit". Then go straight on (no need to wait) unless something is genuinely
the user's call.

Scope rules:
- Only change what the comment anchors to and asks for. No unprompted
  "improvements", rewording, restructuring or added content elsewhere.
- Use the client's own vocabulary; match the deck's existing terms.
- Group items by conceptual fit, not to balance layouts.

## 5. Make the edits in the commented file itself

The user's direct edits are final. Keep their wording, layout, deletions and
additions exactly as saved, even where they differ from what Claude wrote
before. Don't revert them, "tidy" them, or reapply Claude's earlier text.
If Claude's previous version is available (e.g. the file it last generated),
compare it to the saved file to see what the user changed by hand. Mention
those changes in the step 4 plan as "your edits kept as-is".

- Edit the commented file in place. Do not regenerate it from a `build_*.py`
  script: that would drop the comments and any manual edits made in
  PowerPoint/Word. If a build script must be updated for future runs, change
  it too, but still apply the edit surgically to the commented file.
- `.pptx`: use the `metis-pptx` skill in template-preserving edit mode
  (python-pptx / XML edits to the anchored shapes). Keep fonts, sizes and
  positions; check text still fits.
- `.docx`: edit runs/paragraphs in place with python-docx or XML; don't touch
  the `commentRangeStart/End` markers.
- Render the changed slides/pages and look at them for overflow or breakage
  when the change affects layout.

## 6. Reply to each actioned comment, inside the file

Write `<scratch>/replies.json`:

```json
[{"id": "<comment id from list>", "text": "reply text"}]
```

Reply style: one to three plain sentences, peer-to-peer, no em dashes.
- Done → say concretely what changed ("Retitled to 'Must do now vs. once the
  pilot is live' and split the list into those two groups.").
- Partly done or declined → say what you did and why the rest wasn't.
- Unclear → ask the specific question; make no edit for that comment.

Then:

```
"$PY" "$CM" reply  "<file>" "<scratch>/replies.json"     # author shows as "Claude"
"$PY" "$CM" verify "<file>" "<scratch>/snap.json"
```

`verify` must print OK (every original thread present, resolved status and
text unchanged, earlier replies intact). If it fails, restore from the backup
in `~/.claude/comment-backups/` and redo; never hand back a file that failed
verification.

Never set comments to resolved; the user resolves them after reading the replies.

## 7. Report back in chat

- The absolute file path (plain text) and the backup path.
- Confirmation of which saved file was used as the base (name + last-saved time).
- A compact table: comment → what changed / question asked.
- Any threads where you asked a question or flagged a conflict, so the user
  knows where to reply. Running `/pls-fix` again picks up their answers.
