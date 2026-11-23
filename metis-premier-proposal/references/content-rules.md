# Content Rules and Editorial Standards

Editorial conventions for proposal content. These were established through multiple rounds of feedback on the Citi CRS Proposal. Most of them exist because a specific violation was caught and corrected.

---

## Structural Consistency

**Each module should get 2–3 pages. Don't force identical counts. If one module genuinely needs less depth, let it. If one needs more, let it, up to ~5 pages.** Bias toward balance, but do not fabricate filler to hit a symmetric count.

Earlier versions of this rule demanded strict ±1 balance across modules. In practice, that rule forced padding — a third module page that said nothing new, or a fifth deliverable that was really the fourth restated. Balance is a heuristic, not a constraint. Honest unevenness beats padded symmetry.

Typical module structures that work:
- 3-3-3-3 (four balanced modules)
- 3-3-2-2 (two deep, two lighter)
- 4-2-2 (one signature module anchoring two supporting ones)
- 2-2-2 (three concise modules)

**What never works:** padding a 1-page idea to 3 pages because the other modules have 3. The reader notices.

**Module count itself follows the story, not the template.** See `narrative-planning.md` step 6. Three-module narratives are common. Five-module narratives are common. Do not pad a story that wants three into four.

---

## Layout Repetition

**No layout pattern should appear more than 2 times consecutively.** Within a run of module pages, vary the layout. Do not use activities/deliverables on every module's overview page. Do not stack three pillar grids in a row.

At QA, scan the final page sequence. If 3+ adjacent pages share a pattern, break one of them — substitute a signature visual, quote-led page, process timeline, or different module layout.

The reader's eye calibrates to the first two examples of a layout. The third feels repetitive. The fourth feels lazy. This is the single most common failure mode when building from a strong template — the template's patterns propagate without intent.

Use `python scripts/verify.py --check-repetition <pdf>` to flag runs of identical layouts. Human QA should catch the rest.

---

## Intent Per Page

**Every module page in the YAML must carry an `intent:` field — a one-line answer to "what is this page doing?"**

```yaml
pages:
  - content_type: pillars
    intent: "Show that we own PM, not advise on it"
    eyebrow: "Module B"
    title: "Four Pillars of Embedded Product Management"
    # ...
```

The `intent` field does not render. Its purpose is to force the consultant to name the job of the page before drafting its copy. At polish-pass time, re-read each page and ask: "does the copy actually do what intent says?" If not, rewrite one or the other.

Pages without an `intent` trigger a warning at build time. Pages whose copy does not match the declared intent are the polish pass's job to catch.

---

## No Em Dashes

Classic AI writing pattern. Remove all em dashes (`—`, `&mdash;`, `\u2014`).

Replace with:
- Period + capital letter for two independent clauses
- Comma for parenthetical phrases
- Colon for introductions to lists or quotations
- Parentheses for genuine asides

**Wrong:**
> The operating model is the unlock — technology teams are good at getting excited about technology, but the constraining factor is almost always the organizational structure.

**Right:**
> The operating model is the unlock. Technology teams are good at getting excited about technology. The constraining factor is almost always how the organization is structured to make decisions and deliver.

---

## No Contractions

Proposal documents are formal. Do not use contractions as a countermeasure to em dashes.

- "do not" not "don't"
- "we are" not "we're"
- "we will" not "we'll"
- "it is" not "it's" (but you can say "its" as a possessive)

Exception: internal emails (see vault drafts folder for examples) can use contractions freely.

---

## No Absolute Claims

Avoid words like "Zero", "Always", "Never", "Every" unless you can defend the claim with evidence.

**Wrong (what was caught in Citi):**
> Zero digital sales metrics exist today

**Right:**
> Baseline CRS digital sales share to be established

The buyer said during the call that the business didn't have sales metrics "to even guide them." That is not the same as a permanent zero. The metric card should reflect what we will do, not a definitive negative claim about the client.

**General rule:** rewrite any metric card or body claim that uses an absolute word. Replace with a descriptive word like "Baseline", "Dozens", "Complex", "Hyper", or "Ongoing".

---

## No Confidential Product Names from Other Engagements

When describing a past client engagement, do not name specific products, brand lines, or internal division names. Even in a proposal to a non-competitor, this feels careless.

**Wrong:**
> Reinvested savings into Abiliti and DLO product teams

**Right:**
> Reinvested savings into priority product teams to fund new capabilities and high-impact strategic initiatives

The client who sees "Abiliti" knows that's a Fiserv product. They reasonably wonder what we will say about them in future proposals. Keep client details disguised to the level of "a $16B+ financial technology company" or "a Top-25 US bank". Specific financials ($30M savings, 1,750 FTEs) are fine because they're aggregate numbers, not identifying product names.

---

## Mirror the Buyer's Language

The strongest copy element in the Citi proposal was echoing Amresh's actual words from the transcript:
- He said "expanded remit" → proposal title: "Your expanded remit presents a significant growth opportunity..."
- He said "dozens of unique retailer partnerships" → pull quote uses the same phrase
- He described the data visibility gap in specific terms → the framing mirrors those terms

**Process:** Before writing any content, re-read the transcript and extract 5–10 exact phrases the buyer used to describe their situation, challenges, and aspirations. Work those phrases into your titles, subtitles, and callouts.

**The opposite approach (what loses deals):** generic consulting language like "unlock value" or "transform the organization" that could apply to any client. If the proposal could be sent to a different client by changing only the client name, you have not tailored it.

---

## Case Studies Match Industry

A financial services prospect should see financial services proof points. A healthcare prospect should see healthcare proof points.

For the Citi CRS Proposal:
- Ally Bank (AI operating model) — financial services
- Fiserv (product operating model, savings) — financial services adjacent
- A generic AI productivity methodology — industry-agnostic

**Earlier draft had:** a $40B energy company and other cross-industry examples. Andrew specifically requested financial services. The lesson: proof point selection is content, not just decoration.

If you don't have in-industry proof points, either:
1. Disguise the client name to the industry descriptor (e.g., "a top-25 US bank")
2. Use a methodology example (like "our AI productivity assessment methodology") without a specific client

Never stretch a case study to claim industry relevance it doesn't have.

---

## Metrics are Generally-Accurate, Not Precise Claims

Metric cards are visual anchors, not legal attestations. Use round numbers and representative ranges.

**Good:**
- "$30M+ Annual Cost Reduction"
- "8–26% Short-Term Productivity Gain"
- "1,750 Individuals Impacted"
- "$40B+ Combined P&L"

**Avoid:**
- "$30.7M" (false precision)
- "Productivity gains of 13.47%" (implies a specific unfounded claim)
- "100% of our engagements result in savings" (absolute)

When in doubt, round up to the nearest significant figure and use "+" to indicate "at least".

---

## Callout Label Conventions

Every callout box should have a label that:
- Is short (1–4 words)
- Is all caps
- Describes the role of the callout, not a summary

Good labels:
- `KEY INSIGHT`
- `THE SPEED IMPERATIVE`
- `CRS APPLICATION`
- `WHY FOLLOW-THE-SUN`
- `OUR COMMITMENT`
- `SEQUENCING`
- `THE GOAL`
- `METHODOLOGY`
- `RELEVANCE TO CRS`

Avoid labels that summarize the body (e.g., "MODULES ARE FLEXIBLE") — those are redundant. The label sets expectation; the body delivers the content.

---

## Next Steps Page Conventions

The Next Steps page should have exactly three steps:

1. **Administrative unlock** — procurement onboarding, vendor registration, compliance docs. Whatever opens the door.
2. **Scoping / alignment session** — a specific meeting type with a defined duration and attendee list, to convert proposal interest into scoped work.
3. **Forward motion** — kickoff within a defined window, OR a deeper-dive on priority modules if they're not ready to kickoff.

Each step gets a numbered card, a title, and a 2–3 sentence body explaining what happens and what the buyer needs to do.

**Include a commitment callout** at the bottom that addresses fee discussion openly ("Fee estimates will follow in a separate communication") and emphasizes flexibility.

---

## Words to Avoid

These are AI tells or consultant clichés that make writing feel generic:

- "In today's world"
- "Leverage" (as a verb in non-financial contexts)
- "Utilize" (use "use" instead)
- "Impactful"
- "Synergies"
- "Best-in-class"
- "Robust" (as filler)
- "Game-changing"
- "Mission-critical"
- "Delta" (as a noun for change)
- "Drive" (as a verb for making things happen — overused)

If you notice one of these while editing, rewrite the sentence.

---

## Neil Seideman vs. Neil Ciderman

Specific to the Citi engagement: the buyer's colleague is Neil Seideman, not Neil Ciderman. During discovery call transcription, the name was misheard. When a proposal references a stakeholder by name, verify the spelling from the buyer's LinkedIn, email signature, or an authoritative source. Misspelling a stakeholder is a preventable credibility hit.

**General rule:** extract named stakeholders from the transcript, verify all of them, and maintain a "named people check" in your QA pass.

---

## Avoid Overdoing a Specific Reference

The Samsung reference (Amresh's line about 14-day requirement-to-delivery at Samsung vs. banking) was used in 3+ places across early iterations. Andrew caught it as overindexing.

**Rule:** a vivid quote or anecdote from the buyer should appear at most twice in the proposal:
1. Once in the problem framing (where it lands hardest)
2. Optionally once in a module callout (for continuity)

Beyond two uses, the reference becomes a crutch and signals you only have one angle.

---

## Review Checklist for Content

Before declaring content done:

- [ ] No em dashes anywhere (search for `—` and `&mdash;`)
- [ ] No contractions in formal body text
- [ ] No absolute claims ("Zero", "Always", "Never", "Every")
- [ ] No named products from other client engagements
- [ ] Stakeholder names spelled correctly and verified
- [ ] Transcript quotes appear max 2 times
- [ ] Buyer's actual phrases appear in titles/subtitles/callouts
- [ ] Case studies match prospect's industry (or are industry-neutral)
- [ ] Module page counts honest (2–3 typical, no padding)
- [ ] No layout pattern repeats 3+ times in a row
- [ ] Every module page has an `intent:` field
- [ ] Each callout label is 1–4 words, all caps
- [ ] Metric cards use round numbers with "+" or ranges
- [ ] Next Steps page has exactly 3 steps (buyer mode only)
