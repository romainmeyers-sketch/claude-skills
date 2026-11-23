# The Polish Pass

Mechanical QA (overlap checks, content rules, render) tells you whether the document is **structurally sound**. The polish pass tells you whether it **lands**. Both are required before shipping.

Do the polish pass after `verify.py --mode all` has passed. Three reads, in order. Do not shortcut.

---

## Pass 1 — Does it land?

Read the full deck once, cold, start to finish. Do not stop to fix anything. Ask:

- **Do you believe the thesis by page 5?** If not, the opening is too slow or too hedged.
- **Does the argument build, or does it restate?** Each page should move the reader further, not repeat.
- **Is there a moment the deck loses you?** Note the page. That is where the narrative breaks.
- **Do you feel any emotion?** Conviction, curiosity, relief? A technically correct deck that produces no reaction will not close.

If Pass 1 fails, stop. Fix the structure before cleaning up copy.

---

## Pass 2 — Is every word pulling weight?

Read each page slowly. For every sentence:

- **Cut 10% of words.** There is almost always 10% you can remove without loss of meaning.
- **Adjective audit.** "Comprehensive," "robust," "best-in-class," "world-class," "cutting-edge." Strike them. If the noun needs an adjective to land, replace the noun.
- **Buzzword audit.** "Leverage," "utilize," "impactful," "synergies," "delta," "mission-critical." See `content-rules.md` for the full list.
- **Intent check.** Each module page in the YAML carries an `intent:` field — the page's "so what?" Re-read the rendered copy against the intent. Does the copy actually do what the intent claims? If not, rewrite the copy or rewrite the intent.

Pass 2 is about density. Dense writing reads fast and earns trust. Loose writing reads slow and signals a draft.

---

## Pass 3 — Would I hand this to the senior partner?

Read the page titles only, in sequence. Skip the body copy. Ask:

- **Do the titles tell the story?** Someone who only sees titles should get the thesis.
- **Is there a dead page?** A title that says "Our Approach" or "Overview" does not tell a story. Rewrite it to assert something.
- **Does the opening assert the thesis?** If the cover and first two titles do not land the argument, the document buries the lede.
- **Does the closing earn the ask?** The last three page titles should make the buyer ready to say yes.

Run `python scripts/verify.py --print-titles <pdf>` to extract the title list automatically.

If Pass 3 fails, the problem is **structure**, not copy. Fix the sketch, not the prose.

---

## Ship or iterate

- **All three passes clean** → ship.
- **Any pass fails** → fix the issue at its level (structure → Pass 1/3, copy → Pass 2) and re-run all three passes from the top. Do not partial-pass.

The polish pass is where a serviceable deck becomes a persuasive one. It is also where most consultants stop early. Do not stop early.
