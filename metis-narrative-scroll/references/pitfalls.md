# Pitfalls

Everything here actually broke. Read it before shipping.

---

## Verification

**Never use headless Chrome's `--virtual-time-budget` on this page.** It does
not advance CSS transitions the way wall clock does, so a page whose entrances
are transitions captures on its start frame and reads as completely broken. On
the Build Note it reported 53 stranded-hidden elements and a blank hero while
every real-time check passed. It cost a full diagnostic cycle chasing a bug
that did not exist.

**`--window-size` below 500px is silently clamped to 500** and the screenshot
cropped, which fakes a horizontal-overflow bug. Mobile widths must come from
`Emulation.setDeviceMetricsOverride`, which is what `_harness.mjs` does.

**`Page.captureScreenshot`'s `clip` is in ABSOLUTE page coordinates**, not
viewport coordinates. Passing a `getBoundingClientRect().top` straight in
captures blank page. Add `window.scrollY`.

**`getComputedStyle` in the in-app Browser pane returns stale values.** For
colour and state work the screenshot is ground truth. A computed-style read
that contradicts the stylesheet is the read being wrong, not the CSS.

**The in-app Browser pane serves a local file from a `data:` URL**, so
`localStorage` throws and scroll-driven reveals may not fire. Use the CDP
suites for anything that depends on scroll state. Localhost is blocked by
policy on Rohan's machine, so do not plan a verification route that needs a
local server.

**A green suite is not coverage of the thing you just changed.** A 125/125 pass
still shipped a dashboard-killing bug five minutes before a presentation,
because the sweep exercised the user-facing pages and the break was behind an
admin gate.

---

## Layout

**Spend a gutter on BOTH sides of a rule.** The stat cells shipped with
`padding:22px 26px 22px 0`, which put 26px before each vertical hairline and
nothing after it. Every number except the first sat **2px** from the rule on
its left against **210px** on its right, and it read as cramped while the
declared padding looked generous. Cells now carry `--fig-gut` on both sides,
with only the outer edges flush so the strip still aligns to the column margin.

**A component draws one rule width in every shape it takes.** The lone-stat
strip carried its hairline on the cell at `max-width:660px`, so the same
component drew a 660px rule in one section where its neighbours drew 1120px. It
reads as an unfinished line. Cap the content, never the rule.

**Optical gap is not declared padding when the type is large.** `.fig-v` is set
at `line-height:1`, so the glyph does not fill its line box: 22px of padding
reads as 29.5px of visible space above a 40px numeral. `qa-spacing.mjs`
measures real ink bounds via canvas `TextMetrics`. Trust it over the box model.

**`.wrap` sets only `padding-left` and `padding-right`, never the `padding`
shorthand.** `.glance` and `.band-in` also carry `.wrap`, and a shorthand there
silently zeroes their own vertical padding at whichever breakpoint declares it
later. This shipped once and only showed up on mobile.

**Controls on the same visual row share one height.** Fix the row container,
not each control. A row that sizes each button off its own content produces
three different heights the moment one label wraps or carries an icon.

**Every view starts and stops at the same vertical position.** When views do
not line up, restructure so they share a layout; do not compensate with a
per-view offset. A measured offset that works at desktop reintroduces the exact
dead space it was fixing once a toolbar wraps on mobile.

---

## The measurement can be wrong before the page is

An element caught mid-entrance measures at its start transform. A `.shot` with
`data-anim="scale"` measured 1182px against its settled 1120px and looked like
a real alignment break. Before reporting a geometry defect, confirm the element
has its `in` class, or measure after a settle.

---

## Rendering

**Resolve every `getElementById` above any branch that can return early.** See
[motion.md](motion.md). This silently removes the rail for reduced-motion
users while looking perfect to you.

**Images settle after first paint and move everything below them**, so rects
measured at load are wrong within a second. The engine re-sweeps on `load` and
again 300ms later for exactly this reason.

**An icon `<use href="#i-name">` pointing at an id the sprite does not carry
renders as an empty box**, silently. `qa-render.mjs` fails on any unresolved
ref. After adding an icon to the markup, re-run `build_sprite.py`.

---

## Content

**A count from a tool's first data import is not a fact.** The Build Note
pulled "86 open to-dos" and "12 priorities" out of its count-ups because they
came off a preliminary import. The screenshot may still show them; the copy
must not assert them.

**Do not state how many people have access to something.** Those lists change
and the number goes stale silently.

**Where a capability exists but is not live, say so on the page** with the
`.note` pattern. Do not let a screenshot imply a feature ships.

**Prefer a URL that has actually been shared with someone** over one derived
from a deployment config, and click every link before the page goes out.

**Text quoted from an official or regulatory document is verbatim.** If it does
not fit, change the layout. Copy-fitting is a layout decision, never an
editorial one, on that category of text.

---

## Things that read as machine-written

These get removed every time they appear, so do not add them:

- Tip and "pro tip" callout boxes
- Left-edge accent bars
- Uppercase tracked eyebrow labels sitting on tinted panels
- Dash-led copy
- Em dashes anywhere, in code or copy
- Emoji in the DOM

De-AI-ing a callout does **not** mean making it stark white. The tell is the
accent bar, the tinted-and-labelled chrome and the uppercase tracked label, not
colour itself. A subtle brand tint with no bar and no label is the target, which
is what `.note` is.

The opposite critique applies at the same time: stripping the tells does not
license unstyled output. Flat, plain text reads as unfinished just as fast as
callout chrome reads as AI-written. The target is designed and legible.
