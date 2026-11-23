# The course content format

Everything a course says lives in one file, `course.js`, as plain data. The
engine in `templates/hub.html` renders it. This file is the contract between
the two.

Read this before writing content. The shapes are small, but the engine will
not guess at a missing field.

---

## The file at a glance

```js
window.COURSE = {
  meta:       {...},   // what the course is called and who made it
  objectives: [...],   // what the learner can do at the end
  agenda:     [...],   // optional, for the instructor-led version
  modules:    [...],   // the spine
  steps:      {...},   // the body of each module
  quiz:       {...},   // the checks
  glossary:   [...],   // the vocabulary
  roles:      [...],   // optional role explorer
  layers:     [...],   // optional structure explorer
  films:      {...}    // optional
};
```

---

## meta

```js
meta: {
  title:    "POM 101",
  sub:      "Product Operating Model foundations",
  client:   "Lumen",
  author:   "Metis Strategy",
  footer:   "© 2026 Lumen Technologies. All rights reserved.",
  storageKey: "pom101",     // namespace for saved progress
  scorm:    false,           // true only when it is going into an LMS
  roleAsk:  true             // ask the learner their role on first open
}
```

`storageKey` must be unique per course. Two courses sharing a key will
overwrite each other's progress.

---

## objectives

What the learner can do at the end. Three to five. Each is a pair of a short
label and a sentence.

```js
objectives: [
  ["Understand the shift",
   "Why the organization is moving from project handoffs to persistent teams, and what that enables."],
  ["Understand the model",
   "How value streams, products and cross-functional squads fit together."]
]
```

Write the sentence so it describes a capability, not a topic. "Why we are
moving" is a capability. "The shift" is a topic.

---

## modules

The spine. Order matters: this is the order the learner walks.

```js
modules: [
  { id:   "m1",                       // stable, never reuse or renumber
    n:    1,                          // display number
    title:"The Case for Change",
    sub:  "Why we are shifting from project to product, and what changes for you.",
    time: "20 min",                   // honest estimate, not aspirational
    film: "intro" }                   // key into films, or omit
]
```

`id` is used for saved progress. Changing an id loses every learner's place
in that module, so treat ids as permanent once a course has shipped.

---

## steps

The body of each module, keyed by module id. An ordered array. Each entry is
one screen.

```js
steps: {
  m1: [
    { kind:"intro",  ... },
    { kind:"take",   ... },
    { kind:"film",   ... },
    { kind:"topic",  ... },
    { kind:"check" },
    { kind:"recap" }
  ]
}
```

### kind: "intro"

Always the first step.

```js
{ kind:"intro",
  h:    "Why we are moving from project <b>to product</b>",
  lede: "You already live the problem. Work moves through several teams, handoffs and decision points.",
  facts:[["play","One-minute film"],
         ["layers","Seven short topics"],
         ["circle-check","Five-question check"]],
  goals:["Explain why the shift is happening",
         "Describe what changes for your team",
         "Name what does not change"] }
```

`h` takes one `<b>` for emphasis, nothing else. `facts` are icon plus label
pairs, icon names from the sprite. `goals` are the module's own objectives,
phrased as things the learner will be able to do.

### kind: "take"

Exactly three. These reappear verbatim in the recap.

```js
{ kind:"take",
  items:[["Teams persist. Work flows to them.",
          "Standing teams are dedicated to products instead of forming around each project."],
         ["Ownership runs end to end.",
          "Teams own what they build after launch, including run and support."],
         ["Funding follows value streams.",
          "Not one-off projects. Funding moves closer to the work."]] }
```

The first string is the claim, short enough to remember. The second explains
it in one sentence.

### kind: "film"

```js
{ kind:"film",
  film:"intro",                 // key into films
  transcript:[ "line one", "line two" ] }   // one entry per narrated line
```

The transcript is not optional. It is the accessible version of the film and
the thing a learner searches.

### kind: "topic"

The workhorse. One idea per step.

```js
{ kind:"topic",
  kick: "Deep dive · 3 of 7",       // optional position line
  h:    "What <b>actually</b> changes",
  lede: "Optional one-paragraph setup.",
  body: [ ...blocks... ] }
```

`body` is a list of blocks. The engine supports these, and no others:

| Block | Shape | Use for |
|---|---|---|
| `p` | `{p:"text"}` | A paragraph |
| `list` | `{list:["a","b"], icon:"check"}` | Points of equal weight |
| `two` | `{two:[{t,d},{t,d}]}` | A comparison, before and after |
| `cards` | `{cards:[{t,d,icon}]}` | Three or four parallel things |
| `table` | `{table:{head:[...], rows:[[...]]}}` | Facts that line up in columns |
| `note` | `{note:"text", kind:"info"}` | A caveat or an aside |
| `quote` | `{quote:"text", by:"name, role"}` | A real quotation only |
| `fig` | `{fig:"<svg .../>", cap:"caption"}` | A diagram |

If content does not fit a block, that is usually a sign it is two steps.

### kind: "check"

No fields. The engine pulls the questions from `quiz[moduleId]`.

### kind: "recap"

No fields. The engine reprints the module's `take` items and offers the next
module.

---

## quiz

Keyed by module id, plus an optional `final`.

```js
quiz: {
  m1: [
    ["In this model, what is a product?",                 // the question
     ["Only an external offering",                        // options
      "Any value-delivering domain with a defined customer and measurable benefit",
      "A funded project with a fixed end date",
      "A single software application"],
     1,                                                   // index of the answer
     "Internal products are governed with the same discipline as external ones."]
  ]
}
```

The fourth element is the `why`. It is shown after the learner answers,
right or wrong. Never leave it out.

Four options. Three to five questions per module. The answer index must not
sit in the same position twice in a row.

---

## glossary

```js
glossary: [
  ["Product", "Model",
   "Any value-delivering domain with a defined customer and measurable benefit."],
  ["Value stream", "Model",
   "The organizing unit of the model."]
]
```

Term, category, definition. Categories become the filter buttons. Every term
the course uses in a specific sense belongs here, including ones that look
ordinary. "Product" and "customer" are the ones learners most often think
they already understand.

---

## roles and layers, both optional

Use these when the subject is an operating model, an org design or anything
where "who does what" is part of the content.

```js
roles: [
  { id:   "po",
    t:    "Product Owner",
    lay:  "Delivery Team",            // which layer it belongs to
    focus:"One paragraph on what this role is for.",
    r:    ["Responsibility one", "Responsibility two"] }
]

layers: [
  { id:  "team",
    t:   "Delivery Team",
    s:   "One line on what this layer does.",
    c:   "#0E3033",                   // band color
    roles:["Product Owner","Scrum Master"],
    does: ["What happens at this layer"],
    ex:   "A worked example, one or two sentences.",
    talk: "Optional: what a facilitator says out loud here." }
]
```

When `meta.roleAsk` is true, the hub asks the learner which role they hold
and highlights the matching entries. Always include a "my role is not
listed" option, and make sure the course still works when they pick it.

---

## films

```js
films: {
  intro: { file:"films/intro.html",
           len: "1:02",
           name:"Teams persist. Work flows to them." }
}
```

`name` is the film's one-line claim, shown on the play cover. Make it the
sentence you want remembered.

---

## Saved progress

The engine writes one object under `meta.storageKey`:

```js
{ step:   {m1: 4},            // furthest step reached per module
  done:   ["m1"],             // modules completed
  answers:{m1:[1,2,0]},       // answers given
  role:   "po",               // chosen role, or null
  name:   "Sam"               // optional first name
}
```

It is read on open to offer "pick up where you left off". It never leaves
the browser unless `meta.scorm` is true.

When `meta.scorm` is true the engine also mirrors completion and score into
the SCORM 1.2 and 2004 APIs if it finds one in a parent window. Outside an
LMS the bridge stays inactive and nothing breaks, which means the same file
works both in an LMS and from a shared link.
