---
name: spotlight
description: Post something you just made with AI to Spotlight, the EC team showcase. Reads the current session, drafts the card, shows exactly what will post, and posts only after a yes. Invoke with /spotlight, or when the person says "spotlight this", "post this to Spotlight", or "share this with the team".
---

# /spotlight

Turns the work in this session into one card on Spotlight. The person confirms once. Nothing is written before they choose Post.

Board link and settings: read `config.json` in this skill's folder. `board_url` is the only place the link lives. Use it as the `url` in every ArtifactData call below.

## 1. Find out who is posting

- First search for the ArtifactData tool. It may be a deferred tool: load it with ToolSearch (query `select:ArtifactData`) before any call to it. If it is still missing after that search, tell the person this Claude Code session cannot reach the board's database and nothing was posted, and stop. (A headless `claude -p` session has no such tool.) A "no such tool" error is never missing access.
- Call ArtifactData `list` on `data/users/me` (limit 1). The result ends with the person's id (`u_` plus 22 characters). Call this `<uid>`.
- Call ArtifactData `profiles` with `ids: [<uid>]`. Use the returned name. If there is none, the byline reads "your claude.ai account".
- If the calls are refused, tell the person they need Contributor access to the board (Andrew shares it), and stop.
- If the `data/users/me` call works but returns no id, say: "I could not tell who you are on Spotlight, so nothing was posted. Open the board link once in your browser while signed in to claude.ai, then run /spotlight again." Post nothing and stop.

The name is only for the confirmation. It is never written. The board shows the name from the person's claude.ai sign-in.

## 2. Draft the card from the session

Read what happened in this session. Do not ask the person to fill in fields. Pick the most recent finished piece of work. Draft in this order:

- **Type**: `prompt`, `deck`, `skill`, `harness-change`, or `artifact`. Anything else gets one short lowercase word (hyphens allowed).
- **Title**: a noun phrase that names the thing. Under 90 characters.
- **Problem**: the gap before this existed. One or two sentences. Describe it as a gap, never as people failing or doing something wrong.
- **Result**: what is true now. One or two sentences, with a number if the session has one.
- **How it was made**: the interesting part. Which tools, the order of steps, what was tried and dropped. Two to four sentences.
- **The thing itself**, by type (section 3).

Copy rules (deliverable-copy): describe the thing, do not sell it. Short sentences, active voice, one name per thing. No em dashes. No hype words. Do not invent numbers. Facts come from the session.

## 3. Gather the thing

Folders this command uses. It creates every one of them itself, each as a new folder under the system temp directory named `spotlight_` plus random characters (Python `tempfile.mkdtemp(prefix="spotlight_")`). Keep a list of them for this run.

- Export folder: where `export_slides` writes page images. Create it before exporting. Never export next to the source file, and never into a folder the person supplied.
- Prep folder: where `prep_pages.py` writes its documents. The script creates it and prints its path as `out`.
- A folder of images the person supplied is read only. Never write into it and never delete it.

Collect it yourself. Do not ask the person to paste it.

- **Prompt or text harness change**: the exact text, word for word, from the session. `thing = {"kind":"text","label":"Prompt text","text":"..."}`. For a harness change use label `Change text`. Add `"format":"diff"` when it is a diff.
- **Skill or artifact (a link)**: `thing = {"kind":"link","label":"<name, or /command for a skill>","url":"https://...","note":"<where to get it, one line>"}`. Leave `url` out when there is no web link. The board then shows a copy button for the label.
- **Deck or deliverable (page images)**: get one image per page, in page order.
  - A `.pptx`: export it with `export_slides(pptx_path, output_dir)` from `scripts/visual_qa.py` in the metis-pptx skill. Use a new export folder as `output_dir`.
  - A folder of images: use it as is.
  - Then run `scripts/prep_pages.py` from this skill with the image folder and `--open`. It writes the documents the board reads and prints a JSON summary. Run it with the Python that runs the other Metis skills (`python`, `python3` or `py -3`).
  - The script keeps at most 20 pages and about 1.6 MB per card, and every document it writes is under the board's 262,144 byte limit. If it drops pages, `dropped_pages` is above 0. Tell the person, in the card and in the question: "Kept 14 of 32 pages to fit the board." If `thumbnails_dropped` is true, add: "The page strip in the viewer shows numbers, not pictures."
  - The script opens the lead page and the strip pages in the person's image viewer. That is how they check the pages before the question.

## 4. Show the full card, then ask once

Print the card in a fenced block, in the same order as the board. Use the type word in capitals (PROMPT, DECK, SKILL, HARNESS CHANGE, ARTIFACT).

```
DECK
<title>
Posts as <name> (your claude.ai sign-in)

PROBLEM  <problem>
RESULT   <result>

HOW IT WAS MADE
<how it was made>

<the thing>
```

The thing prints in full. Text prints every line, with a line count and "readers get a copy button". A link prints its label, address and note. Pages print `PAGE IMAGES (5 shown on the card, all 14 in the viewer)`, one line per shown page, and a line saying the images were opened on this machine. Add the dropped-pages line when it applies.

Then, on the lines right after the printed card, ask in plain text: "Post this card to Spotlight? Reply Post, Edit, or Cancel." Do not use AskUserQuestion. Give the three meanings, one per line, and wait for the person's reply.

- **Post**: Goes on the board now, under your name.
- **Edit**: Tell me what to change, I show the card again.
- **Cancel**: Nothing posts.

Nothing is written to the board before Post.

- **Edit**: ask "What should change?" in one line. Apply the change. For a deck, re-run `prep_pages.py` if the pages change. Each run makes a new prep folder; keep them all until the end of the command. Print the full card again and ask the same plain-text question.
- **Cancel**: reply "Nothing was posted." Delete every folder this run created (see section 3). Stop.

## 5. Post

Write in this order, so the board never shows a card without its images.

1. **Card id.** Make a new id: local date and time plus four random hex characters, for example `20260930-142501-9f3a`. Call ArtifactData `get` on `spotlight/cards/<uid>` with that id. If a document exists, make another id. Never reuse an id.
2. **Roster.** Call `get` on `roster/<uid>`. If it does not exist, `set` it to `{"t":"person","joined":"<ISO time>"}`. The board finds people through the roster.
3. **Images (decks only).** Write these before the card. `set` each file from the prep folder, one call per file, using `file_path`:
   - `spotlight/media/<uid>` doc `pg__<cardId>__<n>` from `pg_<n>.json`
   - `spotlight/media/<uid>` doc `th__<cardId>` from `th.json`
   - `spotlight/media/<uid>` doc `img__<cardId>` from `img.json`
4. **The card.** `set` on `spotlight/cards/<uid>` doc `<cardId>`:
   `{"t":"card","type":...,"title":...,"date":"YYYY-MM-DD","at":"<ISO UTC time>","problem":...,"result":...,"made":...,"thing":...,"v":1}`
   For a deck, `thing` is the `thing` object from the script summary.
5. Never write under another person's id. Never write a name.

Stop at the first write that fails. Do not write the card, and do not go on to later writes. The card is written last, and only when every earlier write succeeded. Then tell the person, in plain words: which step failed (for example "page 7 of the images" or "the card"), that no card was posted, and offer to try again. Do not print raw errors. Never say "Posted" after a failed write. Leftover image documents do no harm and stay hidden without a card. On a retry, make a new card id and repeat from step 1.

## 6. Show the link

One short screen:

```
Posted.
Board: <board_url>
```

Delete every folder this run created: the export folder and every prep folder. Do this after the person chooses Post (posted or failed and given up) or Cancel. Delete nothing else.
