# The design system

Taken from the POM 101 hub, which sits on the Metis narrative-scroll system
with the client's palette swapped in. Flat surfaces, hairlines, one type
ramp, almost no shadow.

---

## Tokens

The POM 101 set, which is Lumen's palette. For a Metis-branded course, swap
the accent block and leave the structure alone.

```css
:root{
  /* surfaces */
  --deep:#0F3133; --deep-2:#0B2628;
  --ink:#111; --gray:#4D5A5C; --line:#E2E5E5;
  --bg:#F7F7F6; --card:#fff; --tint:#F2F0F1;

  /* accents */
  --teal:#36C6C6; --teal-ink:#127373; --teal-soft:rgba(54,198,198,.14);
  --mint:#B2FFF6; --or:#FB8328; --coral:#F85E48;

  /* on dark bands */
  --on-deep:#E6EFEF; --on-deep-dim:#9FB9BA; --line-deep:rgba(255,255,255,.16);

  --r:4px;
  --ease:cubic-bezier(.22,.61,.36,1);
  --ease-out:cubic-bezier(.16,1,.3,1);
  --font:"Avenir Next LT Pro","Avenir Next","Nunito Sans",
         -apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
}
```

Four pounds of restraint hold this together:

- **4px radius.** Everywhere. Not 8, not 12.
- **One accent at a time.** Orange is the action. Teal is the accent. They
  do not appear in the same component.
- **Hairlines, not shadows.** `--line` carries the structure. Shadow is for
  things that genuinely float, which on a learning page is almost nothing.
- **Tabular numerals** on anything that counts or changes in place.

Load Nunito Sans as the web fallback for Avenir Next:

```html
<link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700&display=swap" rel="stylesheet">
```

---

## Type ramp

```css
.lx-h1  { font-size:clamp(30px,3.8vw,44px); font-weight:400;
          line-height:1.08; letter-spacing:-.03em;  max-width:22ch }
.lx-h   { font-size:clamp(25px,2.8vw,32px); font-weight:400;
          line-height:1.12; letter-spacing:-.025em; max-width:26ch }
.lx-sub { font-size:15px; font-weight:600; margin:6px 0 12px }
.lede   { font-size:17px; line-height:1.55; color:var(--gray); max-width:62ch }
.lx-kick{ font-size:13px; color:var(--gray); margin-bottom:10px }
```

Headings are **weight 400 with negative tracking**, not bold. That is the
single most characteristic thing about this system, and the first thing that
goes wrong when someone rebuilds it from memory. Emphasis inside a heading
comes from one `<b>`, which renders at 600.

The measure limits are doing real work. `22ch` on a page heading stops a
title running the full width of a laptop, which is what makes the page feel
composed rather than stretched.

---

## Components

| Class | What it is |
|---|---|
| `.mast` | Sticky masthead, dark, carries the progress bar |
| `.rail` | Fixed right-hand step dots, fade in once the learner scrolls |
| `.lx-kick` | Position line: "Deep dive, 3 of 7" |
| `.lx-facts` | Inline icon and label row under a lede |
| `.lx-take` / `.lx-tk` | The three-takeaway grid and its cards |
| `.note` | The honest caveat. 18px icon column, text column, hairline border |
| `.band` | Full-width dark section, for a module close |
| `.qbar` | The question progress pips in a check |
| `.btn-or` | Primary action, orange on ink |
| `.btn-line` | Secondary, transparent with a hairline |
| `.swap` | The step transition |

### The note

Use it for anything the learner should not take at face value: an
illustrative figure, a decision that is not final, a placeholder. It is the
component that keeps a course honest, so do not quietly drop it to tidy a
layout.

---

## Motion

One job: tell the learner something changed. Never decoration.

```css
@keyframes swapIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:none} }
```

- **Step change** uses `.swap`, around 450ms on `--ease-out`.
- **Reveal on scroll** via `data-anim="up"` with `data-delay` in
  milliseconds, and `data-stagger` on a parent to walk its children.
- **Counters** count up once, and land on the exact value.

Two rules, both learned the hard way:

**Write the final state first, then animate from it.** Anything that only
appears inside a `requestAnimationFrame` callback will never appear in a
background tab, a hidden pane or some remote desktop sessions, because rAF
does not fire there at all. A counter that starts at zero and animates up
will sit at zero forever in those cases.

**A span with a height needs a `display`.** An inline span ignores height
and collapses to nothing, taking its progress bar or its badge with it.

And honor the setting:

```css
@media (prefers-reduced-motion:reduce){
  *{animation-duration:.01ms !important;transition-duration:.01ms !important}
}
```

---

## Responsive

Breakpoints in the original: 1300, 980, 960, 900, 820, 620.

That many is a sign of a layout tuned per component rather than globally.
When building new, prefer container-driven sizing:
`repeat(auto-fit,minmax(min(320px,100%),1fr))`. The `min()` matters, because
`auto-fit` will not shrink a track below its stated minimum and will push the
page sideways on a phone.

Check every screen at 375px. People do training on a train.

---

## House rules that override the source

Two preferences post-date the POM 101 file. Follow these, not the original:

- **No letter-spaced uppercase micro-labels.** Use sentence case.
- **No em dashes** in any generated copy. Commas, colons or periods.
