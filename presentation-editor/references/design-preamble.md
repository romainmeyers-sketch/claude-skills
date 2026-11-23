# Claude Design preamble

Claude Design may not expose the skill picker. When it does not, paste this
block ahead of the request. It is the same discipline as the skill, written for
a canvas rather than a deck file.

Before pasting, check the obvious thing first: the skill has to be **enabled**
in claude.ai Settings, Capabilities, Skills, not only uploaded.

---

## Editing an existing design

```
Before you change anything:
1. Read the current design first and tell me what is there: sections or frames,
   their names, and the design tokens actually in use (colors, type scale,
   spacing, radius).
2. State in one line what you are about to change and what stays untouched.
3. Change the smallest node that does the job. Do NOT regenerate the whole
   document or frame to alter one element.
4. If the tool only accepts a full-document write, rebuild from exactly what you
   just read, apply the one change, and compare your output against it before
   sending. Tell me the section count before and after.
5. Keep every frame, layer and section name, and every id or anchor, unchanged.
6. New elements match their siblings and the existing grid: same spacing, type
   scale, radius, color role. No shadows, no accent bars.
7. Confirm what changed and that nothing else moved. If you spot something else
   wrong, list it, do not fix it.
```

## Creating something new in Design

```
House style: no shadows, no accent bars, curved takeaways, descriptive title
plus subtitle, top to bottom reading flow, no em dashes. Use the tokens already
in this design system rather than inventing colors or sizes. Tell me which
tokens you used.
```

---

## Why line 4 matters most here

The failure mode on a canvas is not a bad edit, it is a **silent full rewrite**.
When the surface only accepts a whole-document write, the model regenerates from
memory rather than from the document, and sections it forgot simply disappear.
Nobody notices until the frame is scrolled.

The count check in line 4 is the cheapest guard: if the design had nine sections
before and eight after, that is a defect, whatever the change was supposed to be.

## The equivalent of the comment rule

On a deck, the irreplaceable thing is a reviewer comment. On a shared design it
is the same: comments, pinned feedback, and anyone else's named layers. None of
it can be rebuilt from the picture. If the tool you are about to use might drop
them, say so before using it, not after.
