# Narrative-First Planning

Proposals fail at the planning stage, not the rendering stage. A well-rendered page that argues the wrong thing is still a wasted page. This document defines the planning loop a consultant should work through **before** writing any YAML.

> **Do not start writing YAML until you have a thesis and a sketch. Jumping to YAML first is the single biggest quality trap.**

Fill in `scripts/_brief_template.md` as you go. The brief lives next to the YAML in the working folder.

---

## The Ten Steps

### 1. Audience
Named reader (buyer), or archetypal reader (capabilities piece)? Write down:
- Who will read this?
- What do they already believe about this problem?
- What do they fear (being wrong, being slow, being exposed)?
- What would make them say yes?

Do not proceed until these are answered in writing. If you cannot answer "what would make them say yes" with a concrete outcome, you don't know the audience well enough yet.

### 2. Thesis
The one sentence this document argues. Not a list of capabilities — an argument.

- "Metis can run product management for your AI portfolio, not just advise on it."
- "Your expanded remit is a $2B+ growth opportunity if you build the operating model."
- "This transformation requires a different kind of partner than the one you hired last time."

If you have two theses, you have two documents. Split them.

### 3. Audience–thesis fit check
Does the thesis actually answer something the audience cares about? If the buyer's central anxiety is "how do we move faster" and your thesis is "we have deep capabilities across four modules," your thesis is not aimed at the audience. Loop back to step 1.

### 4. Signature visual
The single diagram, framework, or chart that anchors the thesis. Identify it before anything else. Every other page either:
- builds toward it,
- references it, or
- extends it.

If you can't name the signature visual after the audience and thesis are set, the document probably lacks a spine.

### 5. Source material triage
Read everything — transcripts, prior decks, case briefs, industry research. Then extract **3–5 golden details**:
- specific dollar figures
- exact buyer phrases
- named frameworks
- stage names or phases
- the concrete moment that made the problem real

Cut the rest. Resist the urge to include. If it does not move the thesis forward, it is clutter.

### 6. Natural cleavage points
Where does the story actually break? Phases of work (often 3), operating pillars (often 4), stages of a journey (often 5). Module count follows from the story, not from a template. If the narrative wants 3 modules, do not pad to 4.

### 7. Narrative sketch
A one-page text-only storyboard. Example format:
```
Page 1  — opens with the buyer's expanded remit
Page 2  — reframes as a growth opportunity, not a reporting problem
Page 3  — lands the thesis: the operating model is the unlock
Pages 4-10 — develops the four modules
Pages 11-14 — proves the approach with case studies
Page 15 — closes with the three-step entry
```
No layout thinking yet. Save as `sketch.md` in the working folder.

### 8. Reverse-outline check
Read the page titles from the sketch in sequence. Do they tell the story? If someone only skimmed titles, would they get the thesis? If not, the sketch is wrong. Fix it before writing the YAML.

### 9. Pacing check
Annotate each sketched page with its intended layout. Vary dense/light, text/visual, concept/proof. If 3+ in a row share a layout, break one up. See the layout-repetition rule in `content-rules.md`.

### 10. Kill list
Name the pages you are **not** including even though they are tempting. Writing this list matters. It documents the subtraction discipline that separates a tight deck from a sprawling one. Future-you will thank present-you.

---

## Why this sequence, in this order

- **Audience before thesis.** A thesis in isolation can be clever but unaimed. The audience gives it a target.
- **Thesis before visual.** A signature visual that does not serve the thesis becomes decoration.
- **Visual before sketch.** Knowing the anchor lets the sketch reference and build toward it.
- **Sketch before YAML.** Layout decisions in YAML lock in structure. Locking structure before narrative produces template-shaped output.
- **Kill list last.** Subtraction is easier after the draft shape exists — you can see what earns its place and what doesn't.

---

## Common failures

**"I'll skip straight to the modules."** You will produce a deck that describes capabilities without arguing anything. It will feel generic. It will look like the last one.

**"The thesis is 'Metis can help.'"** That is a pitch, not a thesis. A thesis is falsifiable in principle — someone could disagree with it. "Metis can help" is not disagree-able.

**"Let me include every golden detail."** Every detail included dilutes the others. Five specifics land harder than fifteen.

**"I'll balance the module count by padding Module C."** Unbalanced modules signal an honest read of the work. Padded modules signal a template.

---

## When to skip this process

You never skip this process. A five-page update deck still benefits from naming the audience, the thesis, and the kill list. It takes 15 minutes when you do it first and several hours when you do it after drafting the wrong document.
