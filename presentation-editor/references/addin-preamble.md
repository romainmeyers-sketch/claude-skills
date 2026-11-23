# Add-in preamble

The PowerPoint add-in does not load skills from the local Claude Code skills
folder. Until the skill is available there, paste this block ahead of a request
in the add-in panel. It is the compressed version of the skill: the loop, the
preservation contract, and the comment rule.

Keep it short on purpose. A long preamble in a small panel gets skimmed.

---

```
This deck has reviewer comments. Protecting them outranks the edit.

1. Do NOT edit or rewrite slide XML, and do NOT run a script that replaces or
   rebuilds shapes. Those drop comments. Use text edits and single shape
   property edits only. If the change cannot be done that way, tell me instead
   of doing it another way.
2. Read the target slide and list its shapes back to me first. That is the
   baseline.
3. State in one line what you are about to change and what stays untouched.
4. Make ONE change, then check the comments are still there and tell me.
5. New elements copy their siblings: same size, fill, font, spacing.
6. Put text in the slide layout's own boxes. Do not add a floating text box
   and position it. If the layout has no slot for the content, tell me.
7. Use PowerPoint's own bullets. One line per paragraph, no typed dots or
   dashes at the start, and use demote for sub-levels, not spaces.
8. Confirm what changed versus the baseline and that nothing else moved. If you
   notice something else wrong, list it, do not fix it.
```

## When Claude is making the slides, not editing them

The two rules above are the ones that fail most often on a slide built from
scratch in the add-in. Paste this on its own when asking for new slides:

```
Build each slide from a layout and put the text in that layout's own boxes.
No floating text boxes. Use PowerPoint's real bullets, one line per
paragraph, with no dots or dashes typed into the text.
```

Why it matters: a floating box ignores the template's fonts and bullet styles,
does not show in Outline view, and does not move when the layout changes. A
typed dot is not a bullet, so long lines wrap under the dot instead of the
words, and Tab cannot demote them. Details and the checks are in
[placeholders-and-bullets.md](placeholders-and-bullets.md).

---

## Shorter version, decks with no comments

```
Read the slide and list its shapes first. State your change in one line. Make
only that change, no XML rewrites, match sibling formatting, then confirm
nothing else moved.
```

## Why line 1 comes first

Lines 2 to 6 are ordinary care. Line 1 is the one that has actually failed in
practice: the add-in reaches for a slide-XML rewrite, the rewrite drops the
comment relationships, and nothing in the panel reports it. Putting the ban at
the top, before the deck is even read, is the only placement that has held.

Before an add-in edit on a deck that matters: **File, Save a Copy first.** That
one step makes every comment recoverable, whatever the tools do.

| Line | Failure it prevents |
|---|---|
| 1 | Lost reviewer comments, the defect seen in real use |
| 2 | Editing from memory rather than the deck's current state |
| 3 | Silent misreading of a short prompt |
| 4 | Finding out about damage at the end instead of while it is undoable |
| 5 | A new element that is visibly bolted on |
| 6 | Reporting done without checking, and unrequested "improvements" |
