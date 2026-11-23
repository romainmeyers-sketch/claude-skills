# Before a course goes to a client

`build_course.py` catches the mechanical faults. This is the rest, and most of
it cannot be automated because it is about whether the course is true and
whether it teaches.

Work through it in order. The content checks come first on purpose: there is
no point polishing the layout of a course that asserts something the client
never said.

---

## The brief was actually asked

- [ ] Whose design system this is in was asked, not assumed, and the answer
      is reflected in the tokens.
- [ ] The outcomes came from the client, not from us reading the source.
- [ ] Someone is named as the person who signs off that the content is
      correct.
- [ ] Any assumption made because a question went unanswered is written down
      at the top of the content file and was said out loud.

## Films: the script

- [ ] The narration was approved as plain text before anything was animated.
- [ ] The approved script, the captions and the `transcript` in the content
      file all match word for word.
- [ ] Nobody is expecting a voice in the MP4 that has not been recorded.

## Content and truth

- [ ] Every claim traces to source material the client gave us. Name the
      source if asked about any sentence in the course.
- [ ] Every number is either sourced or labelled illustrative **in the copy**,
      not in a footnote. A `note` block is the right place.
- [ ] Nothing has been smoothed from "proposed" into "decided". Check the
      tense of every statement about the future.
- [ ] Where the source was silent, the course says so rather than filling the
      gap. A blank is honest; an invention is not recoverable once a hundred
      people have learned it.
- [ ] Terminology is the client's own, spelled their way, and every term is in
      the glossary.
- [ ] The course makes no claim about anyone's job, grade, pay or headcount
      unless the client wrote that claim themselves.

## Teaching

- [ ] Each module's `take` items are the three things you would want someone
      to repeat back a week later.
- [ ] `take` and `recap` carry the same three statements, word for word.
- [ ] Every topic step holds one idea. If a step has two headings, split it.
- [ ] Every check question has a `why` that teaches, not one that restates
      the answer.
- [ ] Wrong options are things a reasonable person believes. No joke options.
- [ ] The correct answer is not in the same position twice in a row.
- [ ] The stated time per module is honest. Read a module aloud and time it.

## Films

- [ ] The narration lines read correctly out loud.
- [ ] Captions match the narration word for word.
- [ ] The transcript in `course.js` matches both.
- [ ] `__FILMRENDER.frame(t)` draws the same frame twice for the same `t`.
- [ ] The film posts `ended`, and the hub advances the step.
- [ ] The film pauses when the learner leaves the step.
- [ ] Captions start on.

## The learner's experience

- [ ] Open it cold, as a learner: start, leave in the middle, close the tab,
      come back. It offers to resume in the right place.
- [ ] The role picker has a "my role is not listed" option, and the course
      still works end to end when that is chosen.
- [ ] Progress and answers survive a reload.
- [ ] Nothing is lost if the browser blocks local storage. The course should
      still run, just without memory.
- [ ] Keyboard only: tab to every control, arrows move between steps.
- [ ] Every screen at 375px wide, with no horizontal scroll.
- [ ] With `prefers-reduced-motion`, nothing animates and nothing disappears.

## Build and delivery

- [ ] `build_course.py` passes with no warnings.
- [ ] The file opens from `file://` with no console errors, not only from a
      server.
- [ ] If it is going to an LMS, `meta.scorm` is true and completion reports.
      If it is going on a link, `meta.scorm` is false.
- [ ] `meta.storageKey` is unique to this course.
- [ ] Films are either inlined or shipped in the same folder, and the links
      resolve from wherever the client will actually put the file.
- [ ] Fonts fall back cleanly with no network. Check with the network off.
- [ ] The file is saved to the Downloads folder.

## The last read

Read the whole course start to finish as a learner who is sceptical about the
change it describes. Note every place you would roll your eyes. Those are the
places that need the honest caveat, not better wording.
