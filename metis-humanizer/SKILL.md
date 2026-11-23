---
name: metis-humanizer
description: |
  Rewrite text to sound collaborative and human, not pushy or authoritative,
  free of AI-generated writing patterns, and lightly in Metis Strategy's
  brand voice. Builds on the humanizer skill's detection catalog (inflated
  symbolism, promotional language, -ing tails, vague attribution, em dashes,
  rule of three, AI vocabulary, filler) and adds a Metis brand tint, an
  opt-in advisory register, document-type modes (email, proposal, exec
  summary, memo, slide copy), a consulting cliche ban, and a cinematic
  staging ban. Defaults to plain, peer-to-peer, non-authoritative tone. Use
  for Metis client-facing or internal prose. Trigger on "metis humanizer",
  "humanify", "make it human", "metis voice", "metis tone", "consultant
  tone", "make this sound like Metis", or "humanize for a client".
license: MIT
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
metadata:
  author: Metis Strategy
  version: "1.0.0"
---

# Metis Humanizer: Advisory Voice, On Brand, No AI Tells

Work this sequence, in order: **Situate** (1) who reads it, what artifact; **Find** (2) scan for every AI tell and voice violation, no rewriting yet; **Script** (3, optional) auto-fix the mechanical subset if there's a file; **Rewrite** (4) one pass, straight into consultant + Metis brand voice, clearing whatever's left from Find; **Audit** (5) checklist plus a final script check. Details for each are below; Rewrite is one draft, not a humanize pass followed by a separate voice pass.

## Step 1: Situate the text

Before rewriting, establish two things. If the user has not said and it is not obvious from the text, ask once (one AskUserQuestion covering both); if unanswerable, infer from content and say what you assumed.

**Is it advisory or just collaborative?** Most text is not a formal recommendation. Only use the advisory register in Step 4 (recommendation-first framing, ask hygiene, bad-news sequence) when the piece genuinely carries a recommendation, finding, or decision ask. Everything else, an update, a note, a casual exchange, defaults to the **collaborative register**: plain, warm, peer-to-peer, no forced "we recommend." When in doubt, default to collaborative, that's the more common case and the safer default against sounding pushy or authoritative.

**What artifact is it?** Apply the matching mode from "Document-type modes" below, if one applies.

## Step 2: Find (scan for issues)

Read the text once and list every instance of the patterns below. This is a scan, not a rewrite: produce a findings list (pattern, location, snippet), and hold off on changing anything until Step 4.

### Content patterns

- **Significance inflation**: "stands as a testament", "pivotal moment", "marking a shift", "evolving landscape", "underscores its importance". Cut; state the fact. ("The Institute was established in 1989" beats "marking a pivotal moment in the evolution of...")
- **Notability padding**: listing every outlet that ever mentioned the subject, or follower counts, without context. Keep one citation with real context if the source gives it; drop the rest.
- **Superficial -ing tails**: "...highlighting", "...underscoring", "...reflecting", "...fostering", "...showcasing". These get tacked onto a sentence to fake depth. Cut or convert to a real sentence.
- **Promotional language**: "groundbreaking", "seamless", "robust", "vibrant", "renowned", "commitment to", "nestled in", "must-visit". Replace with specifics or cut.
- **Vague attributions**: "Experts argue", "Industry reports suggest", "Observers have cited". Name the source or drop the claim; never invent one.
- **Formulaic "Challenges and Future Prospects"**: "Despite its... faces several challenges", "Future Outlook" sections that restate the obvious. Cut to the one or two challenges that are actually sourced.

### Language and grammar patterns

- **AI vocabulary**: delve, leverage, unlock, transform, crucial, pivotal, showcase, tapestry, interplay, landscape (abstract), enhance, foster, underscore, align with, garner, intricate/intricacies, testament, valuable. Use plain alternatives.
- **Copula avoidance**: "serves as", "functions as", "boasts", "features", "offers a". Use "is", "has".
- **Negative parallelism and tailing negations**: "It's not just X, it's Y"; clipped tails like "no guessing" instead of a real clause. Rewrite as a direct statement.
- **Rule of three padding**: forced triplets ("innovation, inspiration, and industry insights"). Keep only the items that carry weight.
- **Elegant variation**: cycling synonyms for the same referent (protagonist / main character / central figure / hero) to avoid repetition. Repeat the plain word instead.
- **False ranges**: "from X to Y" where X and Y are not on a meaningful scale. Name the actual items instead.
- **Passive voice and subjectless fragments**: "No configuration file needed", "The results are preserved automatically". Rewrite active when it makes the sentence clearer: "You do not need a configuration file."

### Style patterns

- **Dashes**: zero `—`, `–`, or `--` as punctuation, including spaced em dashes. Rewrite with a period, comma, colon, parentheses, or restructure. Scan literally before delivering; this is a hard constraint, not a style preference.
- **Boldface overuse**: bolding phrases mechanically instead of using it for genuine emphasis. Remove.
- **Inline-header vertical lists**: bullets that open with a bolded label and colon ("**Performance:** Performance has been..."). Convert to prose or plain bullets.
- **Title case in headings**: "## Strategic Negotiations And Global Partnerships". Use sentence case.
- **Emojis**: decorating headings or bullets. Remove.
- **Curly quotation marks**: normalize to straight quotes unless the source already uses curly quotes throughout (an editorial tool default, not an AI tell on its own).

### Communication patterns

- **Chatbot artifacts**: "I hope this helps", "Great question", "Let me know if you'd like me to expand", "Would you like...?". Delete; these are correspondence, not content.
- **Knowledge-cutoff disclaimers and speculative gap-filling**: "As of [date]...", "While specific details are limited...", "it is believed that", "likely grew up in...". State what isn't known, or cut the sentence. Never dress a guess up as fact.
- **Sycophantic tone**: "Great question! You're absolutely right...". Cut the praise, keep the substance.

### Filler and hedging

- **Filler phrases**: "In order to achieve this goal" → "To achieve this"; "Due to the fact that" → "Because"; "At this point in time" → "Now"; "It is important to note that the data shows" → "The data shows".
- **Excessive hedging**: "could potentially possibly be argued" → one hedge maximum, and name what would resolve it.
- **Generic positive conclusions**: "The future looks bright", "exciting times lie ahead". Cut the paragraph, or end on the last concrete fact instead of a send-off.
- **Hyphenated word pair overuse**: third-party, cross-functional, high-quality, data-driven, real-time, end-to-end used uniformly including in predicate position. Keep the hyphen only when the compound is attributive ("a high-quality report"); drop it when the compound follows the noun ("the report is high quality").
- **Persuasive authority tropes**: "The real question is", "at its core", "what really matters", "the heart of the matter". These pretend to cut through noise but usually just restate an ordinary point with extra ceremony. Cut the frame, keep the point.
- **Signposting and announcements**: "Let's dive in", "here's what you need to know", "without further ado". Just start.
- **Fragmented headers**: a heading followed by a one-line paragraph that only restates the heading ("## Performance / Speed matters.") before the real content. Cut the restatement.
- **Diff-anchored writing**: describing something in terms of what changed from a previous version ("This function was added to replace..."), when the document should read coherently on its own. Describe the thing as it is now, unless the document is inherently version-scoped (changelog, release notes).
- **Manufactured punchlines and staccato drama**: stacking short declarative fragments to manufacture drama ("Then it arrived. No preference for symmetry. No aesthetic prior."). One short sentence for emphasis is fine; a run of them is not. Merge into measured prose.
- **Aphorism formulas**: "X is the Y of Z", "X becomes a trap", "the language of X". Replace with the concrete claim being gestured at.
- **Conversational rhetorical openers**: "Honestly?", "Look,", "Here's the thing," used as a fake-candid hook before an ordinary point. Cut the hook; state the point.

### What NOT to flag

Perfect grammar, formal vocabulary, mixed casual and formal registers, common transition words used once, curly quotes alone, a single em dash, or "honestly"/"look" used mid-sentence are not reliable AI tells on their own. Look for **clusters**: several of the above patterns co-occurring is the signal, not any single instance.

**Never rewrite secondhand text.** Do not apply any pattern above inside a direct quotation, a title, a proper name, or an example where the phrase is being discussed rather than used as the writer's own words. A client's exact quoted words, a named case study, or a document title stay untouched even if they contain a watched phrase; editing them changes what was actually said or named, which this skill must never do.

### Signs of human writing (preserve these)

Lean toward leaving prose alone when you see: specific, hard-to-fabricate detail (a real name, date, or figure a model would round off); mixed feelings or unresolved tension the writer didn't try to resolve; first-person editorial choices the writer could defend; genuine variety in sentence length; or a real aside or self-correction. These are evidence of an actual person's judgment behind the text, most often the client's own input or a subject-matter expert quoted in the source. Scrubbing them out to chase a "cleaner" draft destroys the credibility the client's voice was adding.


### Firm voice floor (Metis D18)

Also banned regardless of context: antithesis framing ("it's not X, it's Y"), aphoristic mic-drop closers, "Whether you're X or Y" setups, connective crutches (Indeed, Moreover, Furthermore), hype vocabulary, emoji. Dramatic one-word or eyebrow headings ("The Moment") become plain functional labels ("Where things stand").

## Step 3: Run the mechanical script (optional)

If the text lives in a file (`.md`, `.txt`, `.docx`, `.pptx`, `.pdf`), run `scripts/validate.py` in this skill's folder before rewriting. It auto-fixes the subset of Step 2's findings that are mechanically safe: curly quotes, em/en dashes, emoji, predicate-position hyphens, a fixed list of filler phrases. It does not touch anything semantic (AI vocabulary, cliches, tone, structure); those stay on the findings list for Step 4.

```
python scripts/validate.py check <path> [<path> ...] [--json]
python scripts/validate.py fix   <path> [<path> ...] [--report]
```

`check` reports findings and exits 1 if it found anything. `fix` applies the mechanical fixes in place; `--report` also prints what's left. Requires `python-docx`, `python-pptx`, and `pypdf` for those formats; `.md`/`.txt` need nothing extra. For pasted text with no backing file yet, this pre-rewrite pass is optional, Step 4 handles it by hand; Step 5's post-rewrite run of this same script is not optional (write the output to a file if you have to).

## Step 4: Rewrite in the consultant + Metis brand voice

Rewrite the text now, in one pass, straight into this voice. Resolve every Step 2 finding the script in Step 3 didn't already fix.

While rewriting, flag any sentence or paragraph that gets substantially reworded (framing, claim, or clause structure changes, not just a word swap) and jot the original, the rewrite, and one or two alternate phrasings. This feeds the review table in Output format; don't bother tracking mechanical, single-word fixes.

If Step 1 called this **collaborative**, use only the Metis brand voice below, plus Document-type modes if one applies. If **advisory**, add the register below on top.

### The register (advisory text only)

Write like a colleague talking straight to another: not a lecture, not a pitch.

- Lead with the point, plainly, reason in the same breath. "We recommend X, because Y" beats "One option worth considering might be...".
- Be honest about certainty: facts as facts, judgment as judgment, name what's still open. Don't dress a working view up as settled, and don't hedge the same claim three times.
- No urgency manufacturing ("the window is closing"). Real deadlines get stated as facts with dates.
- Bad news stated early and plainly, cause explained neutrally (systems, not people), then the path forward. Never sugarcoat, never assign blame.
- Pushing back on something the client wants: acknowledge the intent first, then give the evidence-based alternative, without abandoning the point.
- If there's an actual ask, end with one clear, dated ask or an explicit "no action needed." Never end on "thoughts?" or "let me know."
- Plain words over impressive ones: utilize → use, operationalize → put in place, enablement → training. One idea per paragraph, insight first.

### Metis Strategy brand voice

Applies to both registers, as a light tint, not a mandate to sound authoritative or add gravitas. Most text should still read as one person writing plainly to another:

- **Confident and direct**: state established facts plainly, no hedge-stacking. Don't claim more certainty than the evidence supports.
- **Forward-looking**: orient toward possibility and impact where the content genuinely supports it. Never manufacture progress that isn't in the source (that's Step 2's significance-inflation pattern again).
- **Substantive**: grounded in insight, not buzzwords. Say something real or say less.
- **Clear and accessible**: precise, no jargon for its own sake, whoever the reader is.
- **Firm name**: "Metis Strategy" on first reference in externally shared documents (proposals, executive summaries, whitepapers); "we" / "our team" after that. Never substitute a generic placeholder like "the firm" or "the consultancy" when the actual name belongs there.

This is a voice constraint only. It does not cover colors, fonts, logo usage, or graphic devices; this skill never touches visual formatting, only prose.

### BrandLine usage

"Driving change. Elevating leaders." Use only where the document type calls for it, never mid-paragraph or as a substitute for the actual recommendation:

- **Proposal**: cover-page line or closing sign-off.
- **Executive summary**: optional closing line, placed after the recommendation, never before it.
- **Slide copy**: a closing or thank-you slide headline only, never a content-slide headline (content-slide headlines state the insight; see Slide copy mode below).
- **Email, memo, steering-committee status report**: omit. These are working documents, not brand-facing collateral.

Never render the BrandLine in italics, in a non-brand color, or split across a sentence.

## Document-type modes

Apply the register above, then the mode for the artifact at hand:

**Email.** Answer or ask in the first two lines; context after, not before. One topic per email where possible. Under 150 words unless the content forces more. Subject line states the point ("Vendor shortlist: decision needed by Fri 14th"), not the topic ("Vendor update"). Ends per ask hygiene.

**Proposal.** Confident scoping: "we will deliver", not "we could explore". Scope boundaries stated as plainly as the scope itself; what is out is written down. No overpromising and no capability theater; claims about past work carry specifics (client type, outcome, timeframe). Pricing and effort language is exact, never "roughly" in the document itself.

**Executive summary.** Fixed order: finding, implication, recommendation. Three to five paragraphs or equivalent bullets. A reader who reads nothing else must leave knowing what you found, why it matters, and what you advise. No methodology up front; it goes in the appendix or body.

**Steering-committee memo / status report.** Status stated plainly in the first line (on track, at risk, off track) with no color-coding euphemism ("amber trending green" is banned; say what is late and by how much). Risks named early with owner and mitigation. Decisions needed from the committee listed explicitly and separately from FYI items.

**Slide copy.** Headline states the insight as a full sentence ("Consolidation saves $2.1M, mostly from licenses"), never a topic label ("Savings analysis"). Body proves the headline; anything that does not support it moves or dies. Bullets are parallel and short; the speaker adds the connective tissue live.

### Voice calibration

If the user provides a writing sample or names a consultant whose voice profile exists, match sentence length, connector habits, and formality from the sample, layered on top of the register above. The consultant register sets the floor; the sample tunes the fit.

A writing sample overrides the em-dash ban in Step 2: if the sample itself uses em dashes at a given frequency, keep them at roughly that frequency in the rewrite. Matching the client's or consultant's actual hand beats scrubbing the tell.

## Step 5: Final audit

Before delivering:

1. Literal scan for `—`, `–`, and punctuation `--`; rewrite every hit.
2. Run `scripts/validate.py check` on the rewritten output, always, not just when the user handed you a file. If the output isn't already a file, write it to one first (scratchpad is fine), then run `python scripts/validate.py check <path>` on that file. Take the findings list and resolve every one: run `fix` for the mechanical ones, hand-edit the rest, then re-run `check` until it exits clean (0 findings). Don't call Step 5 done with unresolved script findings.
3. Ask: "What makes this read as AI-generated?" List remaining tells; fix them.
4. Ask: "Would a client feel pushed anywhere in this?" Soften manufactured urgency and rhetorical pressure, without diluting the actual recommendation.
5. Ask: "Is the recommendation still unmistakable?" Collaboration must not blur the point of view. If a reader could finish unsure what you advise, sharpen the lead.
6. Ask: "Does it end with a clear ask or an explicit no-action close?" (Ask hygiene.)
7. If bad news is present: fact stated early, impact quantified, no blame language, path forward given.
8. Scan for consulting cliches and firm-voice-floor violations; replace every hit.
9. Ask: "Can I state this piece's one message in a single plain sentence, and is that sentence in the first paragraph?" If not, restructure. Then apply the room test to any sentence that sounds written rather than said.
10. Cinematic staging sweep, headlines first: scene-setting openers, showman transitions, clipped punch rhythm, self-referential bravado. This sweep is judgment, not grep; read every headline and closer aloud and ask whether it performs. Grading a staged line as "acceptable narrative" is the known failure mode; when unsure, rewrite plain.
11. Ask: "Does the voice read as Metis brand-appropriate: confident, forward-looking, substantive, elevated but accessible?" Confirm the BrandLine, if used at all, sits only where the document type calls for it and never stands in for the recommendation itself.

### Independent grading pass (deliverable-scale text only)

For text saved to a file (proposal, exec summary, whitepaper, memo), the writer self-auditing its own draft misses things. Dispatch a fresh subagent (Agent tool) with no context from the rewrite: give it the final draft plus this skill's catalog and voice rules, and ask it to grade PASS/FAIL with a findings list against the same checklist above. Report its findings alongside the draft; this skill does not auto-loop on a FAIL, a human decides whether to send it back to Step 4. Skip this for pasted-text or chat-scale rewrites (a paragraph, a quick email edit), the extra call isn't worth it there.

## Output format

1. Rewritten text.
2. Brief note of the main changes (AI patterns removed, tone shifts made, mode applied, brand-voice or BrandLine adjustments). Skip the note if the user asked only for the rewrite.
3. **Major-rewrite review table**, only for sentences or paragraphs that were substantially reworded, not for mechanical fixes (a dash swapped for a comma, a curly quote straightened, one buzzword replaced). "Major" means the clause structure, framing, or claim changed enough that the writer should sanity-check it before it ships. Columns: Original | Changed to | Alternates (1-2 other phrasings, same meaning, different register or emphasis). Omit the table entirely if nothing in the pass rose to that bar.

   | Original | Changed to | Alternates |
   |---|---|---|
   | ... | ... | 1. ...\<br>2. ... |

## Example

**Before (AI-sounding and pushy):**
> Great news! Our groundbreaking analysis reveals a pivotal opportunity. It's not just about cost savings; it's about transforming your entire operating model. The real question is whether you can afford to wait. Industry experts agree that leaders who delay risk falling behind—permanently. Let's dive into the three key pillars: efficiency, agility, and innovation. The future looks bright!

**After (Metis consultant voice):**
> The analysis points to one clear move: consolidating the three regional service desks into a single tier structure. We estimate this saves $2.1M annually, most of it from license rationalization rather than headcount. The case for waiting is that your ERP migration lands in Q3 and absorbs the same team's attention. Our view is that the consolidation should start now anyway, because the vendor contracts renew in May and the pricing leverage disappears after that. We need your direction on sequencing by the April 4 steering committee; both paths are laid out in the appendix.

Note what changed: the recommendation leads, the reason travels with it, the counterargument gets acknowledged on its merits, the client owns the call, the close is a dated ask, and there is no urgency theater, no triplet, no dash, no "transform".

## Bad-news example

**Before (sugarcoated and blame-shifting):**
> While the team has made tremendous progress, there are some minor timeline considerations. Unfortunately, the vendor's team dropped the ball on the API work, which may impact certain milestones. We remain confident and excited about the path forward!

**After:**
> The integration workstream is six weeks behind plan, which moves go-live from June to mid-August unless we change scope. The delay traces to the vendor API behaving differently in production than documented; we caught it in the first end-to-end test. We see two recovery options: descope the reporting module to hold the June date, or hold scope and accept August. We recommend holding scope; the reporting module is the piece your finance team asked for first. We need your call by Friday so the vendor can replan.
