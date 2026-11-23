# Graphical Icons — Lucide Library

Programmatic, royalty-free graphical icons for Metis-branded slides. This is
the supplement to the shared-drive `Icon_Lib.pptx` for any workflow that
needs to insert a real icon (not a number-in-a-circle) directly from a build
script.

**Module:** `scripts/icons.py`
**External library:** Lucide (https://lucide.dev), MIT-licensed, ~1,500 icons
**Catalog:** browse at https://lucide.dev/icons/ (kebab-case names)

---

## When to use icons (and when not to)

| Use a Lucide icon | Use the existing `icon_circle_text` component |
|---|---|
| A real glyph (shield, server, users, clipboard) is the natural visual anchor for the concept | Items are inherently numbered or sequential and a number/letter is the right anchor |
| Multiple cards on the slide each represent a different *category* that benefits from visual differentiation | All cards represent the same kind of thing and a number is sufficient |
| The slide is a process timeline, a capability map, or a categorized list where icons aid scanability | The slide is a list of priorities or pillars where numbering carries the ordering |

**Never** substitute emoji, Wingdings, hand-drawn shapes, or freehand vector
paths for a real icon. If Lucide doesn't have it, fall through the hierarchy
below before going bespoke.

---

## Library hierarchy

1. **Lucide** — default. Use unless missing.
2. **Heroicons** — second choice. Cleaner outlines, two variants (outline + solid).
3. **Tabler Icons** — third. 4,000+ outline icons, useful for niche concepts.
4. **Font Awesome Free** — last. Heavier visual weight; only when none above fit.

All four libraries are SVG-based and can be loaded by the same recolor +
rasterize pipeline. If a future PR adds Heroicons/Tabler support, the module
should expose `heroicon()` / `tabler()` helpers alongside `lucide_icon()`.

---

## Quick reference

```python
from scripts.icons import (
    lucide_icon,          # returns a PNG path
    add_lucide_icon,      # inserts an icon shape on a slide
    lucide_icon_card,     # component: icon + title + body card
)
from pptx.util import Inches

# Get a recolored, rasterized icon as a PNG path
png = lucide_icon("shield-check", color="#20206E", size_px=256)

# Insert an icon directly on a slide
add_lucide_icon(slide, "users",
                left=Inches(1), top=Inches(2),
                size=Inches(0.6),
                color="#256BA2")

# Full Metis-styled icon card
lucide_icon_card(slide,
                 icon="clipboard-check",
                 title="Confirm Requirements",
                 body="Validate de-ID and retention requirements with the data owner.",
                 left=Inches(0.5), top=Inches(2), width=Inches(3.0))
```

---

## Auto-icon selection (concept map)

The module includes `suggest_icon(title)` which scans card titles against
[`references/icon-map.json`](icon-map.json), a 150+ keyword mapping across
8 categories. Use it to auto-select icons without manual lookup:

```python
from scripts.icons import suggest_icon

suggest_icon("Security and Compliance")  # -> "shield-check"
suggest_icon("Claude Agents")             # -> "bot"
suggest_icon("Data Platform")             # -> "layers"
suggest_icon("Unknown Thing")             # -> "circle-dot" (fallback)
```

If `suggest_icon` returns `"circle-dot"`, either pick manually from
https://lucide.dev/icons/ or add the concept to `icon-map.json` for future
reuse.

---

## Icon naming guide

Lucide uses kebab-case. A handful of names that come up often in consulting
decks:

| Concept | Lucide name |
|---|---|
| People / stakeholders | `users`, `users-round`, `user-check`, `user-plus` |
| Data / systems | `database`, `server`, `hard-drive`, `cloud` |
| Security / compliance | `shield`, `shield-check`, `lock`, `key` |
| Process / workflow | `workflow`, `git-branch`, `route`, `arrow-right-circle` |
| Documents / artifacts | `file-text`, `clipboard-check`, `file-cog`, `book-open` |
| Code / engineering | `code`, `terminal`, `terminal-square`, `git-merge` |
| Analysis / insight | `bar-chart-3`, `line-chart`, `pie-chart`, `trending-up` |
| Testing / validation | `flask-conical`, `microscope`, `badge-check`, `check-circle-2` |
| Money / finance | `dollar-sign`, `wallet`, `coins`, `trending-up` |
| Strategy / planning | `target`, `compass`, `flag`, `milestone` |
| Communication | `mail`, `message-circle`, `megaphone`, `phone` |
| Time | `clock`, `calendar`, `hourglass`, `timer` |

When unsure, search https://lucide.dev/icons/ — the search box matches
synonyms (e.g. searching "people" returns "users", "user-round", etc.).

---

## Consistency rules

A deck with mixed icon styles looks unprofessional. Pick once per deck and
hold the line:

1. **Same stroke width** across all icons. Default `2` works for most decks;
   use `2.5` for board-level decks where icons need stronger presence.
2. **Same color** across all icons of the same role. Common roles:
   - Primary content icons → Dark Navy (`#20206E`)
   - Secondary / inline icons → Metis Blue (`#256BA2`)
   - Accent / status icons → Mint (`#3BDAC0`) — sparingly
3. **Same size grid.** Most icon-card layouts use 0.55"–0.65" icons. Hero
   icons (one big icon per section divider) sit at 1.2"–1.8".
4. **All icons from the same library.** Don't mix Lucide with Font Awesome
   within one deck. If Lucide is missing one icon, either fall back the
   whole deck or pick a different Lucide concept.

---

## Recoloring (how the module handles it)

Lucide ships SVGs with `stroke="currentColor"` and `stroke-width="2"`. The
helper rewrites both before rasterizing:

```xml
<!-- Source -->
<svg ... stroke="currentColor" stroke-width="2" ...>

<!-- After recolor to Metis Dark Navy -->
<svg ... stroke="#20206E" stroke-width="2" ...>
```

For client decks where the deck inherits a non-Metis palette (extracted via
`scripts/extract_brand.py`), pass the client's primary color:

```python
client_primary = brand["colors"]["primary_text"]  # from extract_brand.py
lucide_icon_card(slide, "shield-check", "Title", "Body", ...,
                 icon_color=client_primary, title_color=client_primary)
```

---

## Caching

Rendered PNGs are cached under `~/.cache/metis-pptx/lucide/`. The cache key
includes name + color + size + stroke width, so changing any parameter
re-renders. Override the cache location with `METIS_ICON_CACHE` env var if
the home directory is unwritable.

Safe to delete the cache at any time — it rebuilds on next use.

---

## Dependencies

Required: `python-pptx` plus ONE SVG rasterizer (auto-detected at import):

| Renderer | Install | Notes |
|---|---|---|
| **pycairo** (recommended) | `pip install pycairo` | Ships native DLL on Windows/macOS. Zero system deps. Uses built-in SVG path parser. |
| cairosvg | `pip install cairosvg` + system libcairo | Better quality for complex SVGs. Needs libcairo: macOS `brew install cairo`, Linux `apt-get install libcairo2`, Windows GTK runtime. |

The module tries cairosvg first, falls back to pycairo. For most Lucide icons
(simple strokes, no gradients), both produce identical results.

---

## Anti-patterns

- **Drawing icons with `MSO_SHAPE.OVAL` + path freehand.** If you find
  yourself composing an icon from primitives, stop and use Lucide.
- **Emoji substitutes** (📊 🎯 🔒). They render at OS-default font weight,
  break the visual system, and look unprofessional in client decks.
- **Mixing icon libraries within one deck.** A Font Awesome icon next to
  three Lucide icons is immediately visible to anyone who designs for a
  living. Pick a library per deck.
- **Solid-fill Lucide icons.** Lucide is an outline library. The module's
  recolor logic targets `stroke` — calling it on a filled icon (e.g. from
  Heroicons solid set) won't recolor correctly. Stay in Lucide for now.
- **Recoloring at insert time only.** Always recolor before rasterize — once
  rasterized, the PNG is fixed. The helper handles this automatically; don't
  bypass it by inserting raw Lucide SVGs via `add_picture`.
