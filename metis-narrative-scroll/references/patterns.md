# Section patterns

Every pattern below is in `templates/narrative.src.html` already. This is the
reference for what each one is FOR, and the judgement that goes with it.

---

## Hero

The one screen that has to earn the scroll. Two lines saying what this is and
who it is for, then a lede, then the dateline and byline.

```html
<section class="hero deep" id="top">
  <div class="wrap hero-in">
    <img class="hero-logo" src="__LOGO_WHITE__" alt="Metis Strategy" data-anim="up">
    <h1 data-anim="up" data-delay="60">What we built<br><b>this month</b>.</h1>
    <p class="lede" data-anim="up" data-delay="130">...</p>
    <p class="lede dim" data-anim="up" data-delay="190">...</p>
    <div class="dateline" data-anim="up" data-delay="250">...</div>
    <p class="byline" data-anim="up" data-delay="300">...</p>
  </div>
</section>
```

`id="top"` is load-bearing: the masthead watches it to decide when to appear.

The `<b>` inside the `h1` is the weight contrast, not a colour change. Keep the
headline to two lines at desktop. Three lines and it stops reading as a title.

**The lede says what the reader gets, not what you did.** "This is a short note
on the internal tools we have been building. Three of them are live right now"
tells them why to keep going. "We have had a productive month" does not.

---

## Contents rows

Rows, never a card grid. Each row **is** the jump control for its section, so
the contents list and the navigation are one object rather than two things that
can disagree.

```html
<div class="wrap glance" id="inside">
  <h3 class="eyebrow">Inside this note</h3>
  <button class="g-row" data-jump="section-one">
    <span class="g-i"><svg class="icn"><use href="#i-compass"/></svg></span>
    <span>
      <span class="g-n">Name of the thing</span>
      <span class="g-d">One sentence on what it is.</span>
    </span>
    <span class="g-go">Read <svg class="icn"><use href="#i-arrow-right"/></svg></span>
  </button>
</div>
```

They are `<button>` elements, not links, because they scroll rather than
navigate. `data-jump` takes the target's `id`. The engine wires them; there is
no per-row JavaScript to write.

The row lifts its padding-left on hover, which is the affordance. Do not add a
border or a shadow to it.

---

## A section

Three grounds, same structure. Alternate them so neighbours separate without
inventing a new component:

| Class | Ground | Use for |
|---|---|---|
| `.proj` | page background | the default |
| `.proj.alt` | card white, hairline top and bottom | the one after a `.proj` |
| `.proj.deep` | navy, with a radial wash | the one that should land hardest |

```html
<section class="proj alt" id="section-two" data-rail="Short Name">
  <div class="wrap wide proj-in">
    <h3 class="eyebrow">Live. Hosted, restricted to the firm.</h3>
    <h2 data-anim="up">The full name</h2>
    <p class="lede" data-anim="up" data-delay="60">One sentence of framing.</p>
    ...
  </div>
</section>
```

`data-rail` puts it in the section rail with that label. Keep the label to two
or three words: it sits in a chip beside a tick.

The `.eyebrow` draws its own hairline in on arrival, once. It is the status
line: "Live", "In test", "Shipping next week". It is NOT a category label like
"OVERVIEW", which is the uppercase-tracked chrome that reads as AI-written.

---

## Two-column block

What it does, and why that matters. Those two questions, in that order,
answered in a paragraph each.

```html
<div class="two">
  <div class="blk" data-anim="up">
    <h3 class="eyebrow">What it does</h3>
    <p class="body">...</p>
  </div>
  <div class="blk" data-anim="up" data-delay="80">
    <h3 class="eyebrow">Why it matters</h3>
    <p class="body">...</p>
  </div>
</div>
```

`.body` caps at 52ch. The measure does the readability work; do not add a
container around it. Collapses to one column below 860px.

Put the sentence you most want remembered in **bold inside** the "why it
matters" paragraph rather than pulling it out into a callout box.

---

## Stat strip

Two to four counted-up facts on hairlines. Deliberately kept off the display
type scale so it reads as a fact strip rather than a hero metric.

```html
<div class="figs" data-stagger="90">
  <div class="fig" data-anim="up">
    <div class="fig-v fig-n" data-count="99">0</div>
    <div class="fig-l">companies, each with its sources attached</div>
  </div>
  ...
</div>
```

`data-count` is the target; the text content is the start state. The count runs
on an ease-out so it decelerates into the real number instead of ticking at a
constant rate, and it resets when scrolled away so a second pass runs it again.

**One stat on its own** uses `class="figs one"`. Number and label share a
baseline so a lone fact reads as a sentence rather than leaving a column of
dead space beside it. It keeps the same full-width rule as a three-up strip:
only the content is capped.

Two rules learned the hard way, both enforced by `qa-spacing.mjs`:

- **The gutter is spent on BOTH sides of each rule.** The original shipped with
  `padding:22px 26px 22px 0`, so every number except the first sat 2px from the
  rule on its left and 210px from the one on its right.
- **The component draws one rule width in every shape it takes.** Capping the
  rule to the content made the lone-stat strip draw a 660px hairline where its
  neighbours drew 1120px, which reads as an unfinished line.

Labels cap at 22ch. If a label needs more, the fact is too complicated for a
stat strip and belongs in a sentence.

---

## Screenshot frame

A real capture, framed in the page's own hairline rather than fake browser
chrome. See SKILL.md section 4 for how to capture.

```html
<div class="shot" data-anim="clip" data-delay="40">
  <div class="shot-top">
    <span class="shot-dot"></span>Onboarding Hub, live
  </div>
  <figure><img src="__SHOT_ONE__" alt="Describe what is actually visible."></figure>
  <figcaption>What the reader should notice in it.</figcaption>
</div>
```

The dot is a status light, so the top bar reads as "this is running right now".
The figcaption points at what to look at; it does not repeat the alt text.

---

## Next steps

What happens next, as a hairline list. This is usually the part a senior reader
actually reads, so make each item a commitment with an owner or a condition,
not an aspiration.

```html
<div class="next" data-anim="up">
  <h3>What happens next</h3>
  <ul data-stagger="80">
    <li data-anim="up">
      <span class="next-i"><svg class="icn"><use href="#i-target"/></svg></span>
      <span><b>The commitment, in a short bold clause.</b> Then the detail.</span>
    </li>
  </ul>
</div>
```

The bold clause is scannable on its own. Someone reading only the bold text
should still get the plan.

---

## Note panel

The honest caveat. A subtle brand tint, **no left accent bar and no uppercase
label**, because both of those read as machine-written and get removed.

```html
<div class="note" data-anim="up">
  <svg class="icn"><use href="#i-clock"/></svg>
  <span>Document sending is in test mode: every send goes to the sender's own
    inbox and nothing reaches an external company.</span>
</div>
```

Use it where a capability exists but is not live, or where a number needs its
qualification. Do not use it for a tip or an aside. If the content is not a
caveat, it is body copy.

---

## Closing band

Say what you want the reader to do, then give them the doors.

```html
<section class="band deep" id="close" data-rail="Where to start">
  <div class="wrap wide band-in">
    <h2 data-anim="up">Three links, one login.</h2>
    <p class="lede" data-anim="up" data-delay="70">If you only open one, open ...</p>
    <div class="band-links" data-stagger="70">
      <a class="band-l" data-anim="up" href="..." target="_blank" rel="noopener">Name
        <svg class="icn"><use href="#i-arrow-up-right"/></svg></a>
    </div>
    <div class="colophon">...</div>
  </div>
</section>
```

**Name the one thing to open first and why.** A closing band with three equal
links and no recommendation gets none of them clicked.

`.band-in` also carries `.wrap`. `.wrap` sets only `padding-left` and
`padding-right`, never the `padding` shorthand: a shorthand there silently
zeroes the band's own vertical padding at whichever breakpoint declares it
later. That shipped once and only showed up on mobile.
