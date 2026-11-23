/* A worked example of the course content format.

   Two modules, one with a film. Short on purpose: it exists so you can see
   every step kind and every block kind in one place, and so build_course.py
   has something to prove itself against.

   Copy it, delete the content, keep the shape. Everything here is plain
   data: no functions, no template literals, no expressions. If you need
   logic, it belongs in the engine, not here. */

window.COURSE = {

  meta: {
    title: "Working in the product model",
    sub: "A short course on what changes when teams stop forming around projects.",
    client: "Example Co",
    author: "Metis Strategy",
    footer: "© 2026 Example Co. All rights reserved.",
    storageKey: "example-product-model",
    scorm: false,
    roleAsk: true,
    closeTitle: "That is the course",
    closeText: "Work through the modules in order. Your place is saved in this browser."
  },

  objectives: [
    ["Understand the shift",
     "Why work is moving from project handoffs to teams that stay with a product."],
    ["Understand your part",
     "What changes in your week, and what does not change at all."],
    ["Use the vocabulary",
     "The handful of words that now mean something specific."]
  ],

  agenda: [
    ["9:00 to 9:30", "Why we are changing", "The case for change and what we learned"],
    ["9:30 to 10:15", "How the model works", "Teams, products and how work reaches them"]
  ],

  modules: [
    { id: "m1", n: 1, title: "The case for change",
      sub: "Why we are moving from projects to products, and what changes for you.",
      time: "15 min", film: "intro" },
    { id: "m2", n: 2, title: "How work reaches a team",
      sub: "One backlog, one set of priorities, and no side channels.",
      time: "12 min" }
  ],

  steps: {
    m1: [
      { kind: "intro",
        h: "Why we are moving from projects <b>to products</b>",
        lede: "You already live the problem. Work crosses several teams, and every crossing costs time.",
        facts: [["play", "One-minute film"], ["layers", "Three topics"], ["circle-check", "Three-question check"]],
        goals: ["Explain why the shift is happening",
                "Describe what changes for your team",
                "Name what does not change"] },

      { kind: "take",
        items: [
          ["Teams persist. Work flows to them.",
           "Standing teams stay with a product instead of forming around each project."],
          ["Ownership runs end to end.",
           "A team owns what it builds after launch, including run and support."],
          ["Funding follows products.",
           "Not one-off projects, so priorities can change without a new business case."]] },

      { kind: "film", film: "intro",
        transcript: [
          "Every day, the work moves through more hands than anyone planned.",
          "In a project model, teams form around the work.",
          "Every handoff adds time, and the feedback comes late.",
          "The product model flips that. The team stays, and the work comes to it.",
          "Teams persist. Work flows to them."] },

      { kind: "topic",
        kick: "Topic 1 of 3",
        h: "What a <b>handoff</b> actually costs",
        lede: "Not the hour it takes to write the ticket. The week it takes for the next team to pick it up.",
        body: [
          { p: "A handoff is not a transfer of work. It is a transfer of context, and context is the part that does not survive the journey." },
          { two: [
            { t: "Project model", d: "Four teams touch the work. Each one learns it, does its part, and forgets it." },
            { t: "Product model", d: "One team holds the context for as long as the product exists." }] },
          { note: "The numbers people quote for handoff cost vary widely and are usually not measured. Ask for yours before quoting anyone else's." }] },

      { kind: "topic",
        kick: "Topic 2 of 3",
        h: "What changes <b>in your week</b>",
        body: [
          { list: ["You work from one backlog, not three",
                   "You see the same priorities everyone else sees",
                   "You stay with what you build after it ships"],
            icon: "check" },
          { p: "The last one is the change people underestimate. Owning the thing after launch changes what you are willing to build before it." }] },

      { kind: "topic",
        kick: "Topic 3 of 3",
        h: "What does <b>not</b> change",
        body: [
          { cards: [
            { t: "Your pay and level", d: "Unchanged. This is a change to how work is organized, not to grading.", icon: "users" },
            { t: "Your manager", d: "Reporting lines stay as they are.", icon: "target" },
            { t: "The standards", d: "Security, compliance and architecture review all still apply.", icon: "zap" }] },
          { quote: "Nothing about this changes who you report to or what you are paid.",
            by: "Example Co leadership, kickoff" }] },

      { kind: "check" },
      { kind: "recap" }
    ],

    m2: [
      { kind: "intro",
        h: "How work <b>reaches a team</b>",
        lede: "One backlog, visible to everyone, with no side channels.",
        facts: [["layers", "Two topics"], ["circle-check", "Two-question check"]],
        goals: ["Describe how a request becomes work",
                "Explain why side channels are a problem"] },

      { kind: "take",
        items: [
          ["Everything lands in one backlog.", "Including the urgent things, and including the ones from leadership."],
          ["Priority is visible.", "If two things compete, the ranking is written down where everyone can see it."],
          ["If it is not in the backlog, it does not exist.", "This is the rule that makes the other two true."]] },

      { kind: "topic",
        kick: "Topic 1 of 2",
        h: "One <b>front door</b>",
        body: [
          { table: { head: ["Where it used to arrive", "Where it arrives now"],
                     rows: [["A message to someone you know", "The backlog"],
                            ["A steering meeting", "The backlog"],
                            ["A ticket in another system", "The backlog"]] } },
          { p: "The point is not the tool. The point is that there is one queue, so the cost of saying yes is visible at the moment someone says it." }] },

      { kind: "topic",
        kick: "Topic 2 of 2",
        h: "Why side channels <b>break the model</b>",
        body: [
          { p: "A side channel is not faster. It moves one request ahead of the queue and hides the thing it displaced, so the delay lands somewhere nobody is watching." },
          { note: "If you are asked for something outside the backlog, the answer is not no. The answer is to put it in the backlog and say what it would displace." }] },

      { kind: "check" },
      { kind: "recap" }
    ]
  },

  quiz: {
    m1: [
      ["In this model, what is a product?",
       ["Only something a customer pays for",
        "Any value-delivering domain with a defined customer and a measurable outcome",
        "A funded project with a fixed end date",
        "A single application"],
       1,
       "Internal products count. What matters is a defined customer and an outcome you can measure, not whether money changes hands."],

      ["What happens to a team when the work it was doing finishes?",
       ["It disbands and people are reassigned",
        "It stays with the product and picks up the next priority",
        "It becomes a support team",
        "It is re-formed under a new project code"],
       1,
       "The team persisting is the whole change. If teams still disband, nothing else in the model works."],

      ["Which of these does NOT change?",
       ["Where work arrives",
        "Who owns the product after launch",
        "Your pay, level and reporting line",
        "How priorities are set"],
       2,
       "This is an operating model change, not a grading or reporting change."]
    ],

    m2: [
      ["A senior leader asks you directly for something urgent. What does the model say?",
       ["Do it, then record it afterwards",
        "Say no, because it is not in the backlog",
        "Put it in the backlog and say what it would displace",
        "Escalate it to your manager"],
       2,
       "The answer is not no. It is to make the trade-off visible before it is made."],

      ["Why is a side channel a problem even when the request is reasonable?",
       ["It breaks the tooling",
        "It hides what the request displaced",
        "It is against policy",
        "It slows the request down"],
       1,
       "The displaced work is the cost, and a side channel is precisely the thing that stops anyone seeing it."]
    ],

    final: [
      ["What is the shortest statement of the change?",
       ["Teams get bigger",
        "Teams persist, and work flows to them",
        "Projects get shorter",
        "Funding increases"],
       1,
       "Everything else in the model follows from the team staying put."]
    ]
  },

  glossary: [
    ["Product", "Model",
     "Any value-delivering domain with a defined customer and a measurable outcome, internal or external."],
    ["Backlog", "Ways of working",
     "The single ordered list of work for a team. If it is not here, it is not committed."],
    ["Handoff", "Ways of working",
     "A transfer of work between teams. Each one loses context and adds waiting time."],
    ["Side channel", "Ways of working",
     "A request that reaches a team outside the backlog. It hides the work it displaces."],
    ["Standing team", "Model",
     "A team that stays with a product rather than forming around a piece of work."]
  ],

  roles: [
    { id: "po", t: "Product Owner", lay: "Team",
      focus: "Owns the backlog and its order.",
      r: ["Keeps one ordered backlog", "Says what a new request would displace"] },
    { id: "eng", t: "Engineer", lay: "Team",
      focus: "Builds and runs the product.",
      r: ["Owns what they build after launch"] },
    { id: "lead", t: "Leader", lay: "Leadership",
      focus: "Sets direction and protects the model.",
      r: ["Uses the backlog like everyone else"] }
  ],

  films: {
    intro: { file: "films/intro.html",
             len: "0:25",
             name: "Teams persist. Work flows to them." }
  }
};
