# The brief

Ask these before building anything. Not after a draft, and not halfway
through. A course is expensive to re-cut, and a film is the most expensive
thing in it, so the cost of asking is a few minutes against a day of rework.

Ask in batches, not one at a time. Most people can answer the whole of
section A in a single reply. If someone says "just start", pick the defaults
marked below, say out loud which ones you picked, and keep going.

---

## A. What and who

1. **What is the subject?** One sentence.
2. **Who is the learner?** Role, and what they can already do. "Everyone" is
   not an answer: a course for everyone teaches nobody.
3. **What can they do at the end** that they cannot do now? Three to five
   outcomes. Push for things you could observe. "Understands the model" is
   not observable. "Can say which team owns a request" is.
4. **How long should it take?** Twenty to thirty minutes a module is the
   working range.
   *Default: four modules, about twenty minutes each.*
5. **Is it mandatory?** Mandatory changes the tone, the length and whether
   anyone needs a completion record.

## B. The design system

Never assume this one. It is the question most often skipped and the most
visible when it is wrong.

6. **Whose brand is this in?**
   - The **client's own**, which is the usual answer for anything their staff
     will see. Then ask for their palette, their fonts, and a logo file. If
     they have a brand portal, ask for the link rather than guessing from a
     deck.
   - **Metis**, for anything we present as our work. Then load
     `metis-brand-identity` and follow it.
   - **Neutral**, when it is a prototype or the brand is not settled.
   *Default: ask. Do not pick.*
7. **Is there an existing course or site it has to sit next to?** If yes, get
   the file. Matching something that exists beats inventing something new.
8. **Any constraints you have to live with?** A locked font, a required
   accessibility standard, a corporate template, a banned color.
9. **Where will it be opened?** A laptop, a phone, a training room screen, or
   inside an LMS frame. This changes the layout decisions, not just the
   testing.

## C. Delivery and tracking

10. **Link or LMS?** A shared file, SharePoint, or a SCORM package in a
    learning platform. This sets `meta.scorm`.
11. **Does completion need recording**, and who reads that record?
12. **Does it need to work offline?** If yes, say so now: it rules out the
    3D films, which load a library from a CDN the first time.
13. **What language, and will it be translated?** Translation later means
    keeping every string in the content file, with no copy in the engine. The
    format already does this, but it is worth confirming nobody plans to
    hand-edit the built HTML.

## D. Source material and truth

14. **What is the source?** Decks, a playbook, recordings, an existing
    course, interviews. Get the actual files.
15. **What is decided, and what is still proposed?** Mark both. A course that
    presents a proposal as a decision is the single worst failure mode of this
    format, because people learn it and repeat it.
16. **Who signs off that the content is correct?** Name a person. "The team"
    is not a reviewer.
17. **Is there anything we must not say?** Headcount, timing, named teams,
    anything commercially sensitive.
18. **Whose vocabulary?** Get their terms and their spellings. They go in the
    glossary.

## E. Films

19. **Are films in scope at all?** They are the most expensive part. A course
    works without them.
    *Default: no films in the first cut. Add them once the content is signed
    off, because an approved script that then changes is wasted animation.*
20. **How many, and how long?** Sixty to seventy seconds each is the format.
21. **Narration:** recorded voice, or synthesized?
    - Synthesized is fine for review and for internal use.
    - A client-facing film needs a recorded voice, and that is a booking with
      a lead time. Ask early.
    - A film rendered to MP4 has **no narration at all** unless the lines were
      recorded, because synthesized speech cannot be rendered offline. Say
      this plainly before anyone assumes the video comes with a voice.
22. **Does a video file need to exist**, or is the in-browser film enough?
    MP4 means `render_film.py`, which means recorded narration if the video
    needs a voice.

---

## The film script comes before the animation

This is the rule that saves the most work. **Write the narration as plain
text, get it approved, and only then animate it.**

A film is an array of scenes, and each scene's narration line is the script.
Once the animation is built around those lines, changing a line means
rebuilding the scene. So the script is a separate, cheap deliverable that
gets reviewed on its own.

Write it like this, as a plain file the client can read and mark up:

```
FILM: What an AI agent actually is
Length: about 65 seconds
Narration: synthesized for review, recorded for release

 1  (5s)  Most teams already use AI to answer questions.
 2  (7s)  An agent is different. It is given a goal, and the tools to reach it.
 3  (8s)  It reads what it needs, decides what to do next, and does it.
          [on screen: a loop, read -> decide -> act]
 4  (7s)  That loop is the whole idea. Everything else is detail.
 5  (9s)  Which means the question is never "can it do this".
          It is "what is it allowed to touch".
 6  (6s)  An agent with no access is safe and useless.
 7  (8s)  So we start by naming the tools, and the limits on each one.
 8  (6s)  Goal, tools, limits. That is an agent.
```

Each line is one claim. Read every one aloud before sending it. If a line
needs a subordinate clause to work, it will not survive being spoken.

Then confirm three things before any animation starts:

- [ ] The script is approved by the person named in question 16.
- [ ] Every claim in it traces to the source material.
- [ ] Nobody is expecting a voice in the MP4 that has not been recorded.

`templates/film-script.example.md` is the full version of the example above.

---

## When you cannot get answers

Do not stall. Build the first module against your best reading, write down
the assumptions you made at the top of the content file, and show it. A
concrete draft gets corrections that a list of questions never does.

What you must not do is let an unanswered question become a silent decision.
If nobody said whose brand it is, say "I used neutral styling because the
brand was not settled" rather than quietly shipping Metis colors into a
client's course.
