# Motion

The engine in `_assets/_engine.js` is the Onboarding Hub's About Metis engine,
ported. Read this before changing it.

## Authoring

Two attributes. That is the whole surface.

```html
<div data-anim="up" data-delay="60">
<div class="figs" data-stagger="90">   <!-- orders its own children -->
```

| `data-anim` | From |
|---|---|
| `up` | `translateY(26px)` |
| `left` / `right` | `translateX(∓30px)` |
| `scale` | `scale(1.055)`, settles down to 1 |
| `pop` | `scale(.9)`, settles up to 1 |
| `tilt` | `perspective(900px) rotateX(9deg) translateY(24px)` |
| `blur` | `blur(9px)` plus a 14px rise |
| `wipe` | `scaleX(0)` from left |
| `clip` | `inset(0 100% 0 0)`, reveals left to right |
| `clipup` | `inset(100% 0 0 0)`, reveals bottom to top |

`data-stagger` on a parent gives each child an index-proportional delay. An
explicit `data-delay` on a child always wins, because the page uses both
together.

Match the entrance to the content. `clip` suits a screenshot because it reads
as the image being drawn. `up` suits text. `scale` suits something that should
feel like it settles into place. Do not use `tilt` more than once on a page.

## Four properties that are load-bearing

**1. It is bidirectional.** Leaving the arming band removes the class and
returns the element to its start state, so scrolling back up runs the entrance
in reverse. A one-shot reveal (the usual `observer.unobserve` pattern) leaves a
second pass down the page showing a wall of already-revealed content, and shows
nothing at all on the way up. Rohan reports this as a bug every time.

**2. It arms below the fold, not at it.** `ARM = 1.12`, so an element is armed
at 112% of viewport height and the motion is already under way by the time it
is actually on screen. Arming at the viewport edge is exactly what produces
"the animations take some time to load".

The release edge sits well outside the arming edge (`gone()` uses
`-(ARM_PX + 90)` and `vh * ARM + ARM_PX`) because an element parked between two
equal edges flips state on every sub-pixel scroll.

**3. The stagger is capped at 260ms** (`DELAY_CAP`). A choreographed 520ms
sequence is right when the section is sitting still in front of you and far too
slow when it is travelling past. Authored delays above the cap are clamped, not
honoured.

**4. Reduced motion is a real variant.** Under `prefers-reduced-motion: reduce`
the engine takes an early return that adds `in` to everything, sets every
counter to its final value, lights every rule and still builds the rail. It
shows the FINISHED page, not a blank one. `qa-jumps.mjs` checks all four.

## Why a scroll handler and not IntersectionObserver

The About Metis deck this came from never received a single observer callback,
and a deck that stays blank is worse than a deck that measures. The sweep also
needs live rects rather than positions cached at init, because images settle
late and move everything below them.

One `requestAnimationFrame`-coalesced sweep per frame serves the entrances, the
counters, the rail and the masthead, so they all read one set of rects rather
than each forcing its own layout.

## The one JavaScript trap in this file

**Resolve every `getElementById` at the top, above any branch that can return
early.** `buildRail()` is called from inside the reduced-motion early return. A
lookup declared further down the file is `undefined` when that fires, which
throws, kills the whole script, and removes the section rail for everyone with
reduced motion turned on. The page looks fine to you and is broken for them.

This is the same temporal-dead-zone class of bug that took the Onboarding Hub's
admin dashboard down twice.

## Counters

```html
<div class="fig-v fig-n" data-count="99">0</div>
```

The run is an ease-out cubic over `1000 + min(target,120) * 5` ms, so it
decelerates into the number rather than ticking at a constant rate. Scrolling
away resets it to 0 and bumps a sequence number, which strands any run still in
flight so a fast scroll cannot leave two runs fighting over the same element.

`.fig-n` sets `font-variant-numeric: tabular-nums`, so the digits do not jitter
horizontally while counting. Any counting number needs it.

## Adding an entrance type

Add it to `FROM` in `_engine.js` and, if it needs a property other than
`transform`, to the init loop and the `.live [data-anim]` transition list in
`_theme.css`. Keep the transition list explicit: a blanket `transition: all`
animates layout properties and thrashes.

## Performance

Transform and opacity only for anything that runs continuously. Never animate
width, top or left in a loop. The parallax and the entrances share the same
frame; adding a second scroll listener that reads rects doubles the layout
cost for no benefit.
