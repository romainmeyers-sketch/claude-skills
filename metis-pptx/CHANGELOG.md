# metis-pptx — CHANGELOG

## v4.5.0 (release folder: v1.2.0), 2026-07-28

### Added: Portable asset resolution

- `scripts/resolve_assets.py`: resolves each brand asset across bundled ->
  plugin (`$CLAUDE_PLUGIN_ROOT/brand-assets/`) -> G: shared drive ->
  `$METIS_BRAND_ASSETS` override, so the skill works standalone (just the
  bundled `assets/master.pptx`) and picks up the full asset set automatically
  when installed inside the `metis-skills` plugin or on a Metis machine.
- `assets/master.pptx` bundled (blank 2025 template, 32 layouts).
- `references/asset-resolution.md`: full resolution map and degradation table.
- SKILL.md §2.1 rewritten to run `resolve_assets.py` first and degrade
  gracefully (§2.1.1) instead of failing when an asset is absent.

### Added: Deck-type preset selector

- `references/deck-presets.md`: six deck-type presets (Readout/leave-behind,
  Workshop/training, Presentation, BD/proposal, Current-state assessment,
  Exec/boardroom), each setting the Density/Variance dials, structure, and
  where detail lives (slide vs. speaker notes).
- SKILL.md §0.2 Intake now opens with "pick a deck type" from this selector.

### Added: Speed Gate and Design dials

- SKILL.md §0.1 Speed Gate: Design mode (per-slide approval) vs. Fast mode
  (auto-pick, review at end), asked before any planning.
- SKILL.md §0.3 Design dials: VARIANCE and DENSITY (1-10 each), consulting
  defaults 6/7.

### Changed: Native-layout-first generation, de-slop pre-flight

- SKILL.md §0.5 rewritten: a content slide needs only title + body + brand
  frame; subtitle optional, takeaway bar rare (0/53 slides in the LiveRamp
  reference deliverable use one).
- SKILL.md §0.5.1 (new): native template layouts are the primary build path;
  hand-built recipes and the Timesaver library are fallbacks, in that order.
- SKILL.md §0.7 (new): bias-correction and an 11-point pre-flight checklist
  every content slide must pass (no decorative accent bars, color must encode
  information, organic numbers, 3+ text sizes, source lines, etc).
- `references/metis-layouts.md` (new): catalog of the 32 template layouts with
  placeholder maps, used by the native-layout path.
- `references/metis-brand.md`, `references/patterns.md`: takeaway bar and the
  illustrative tag demoted from "auto-add every slide" to "rare, only when it
  genuinely earns its place."

### Compatibility

- **Additive to the icon feature.** Lucide programmatic icons
  (`scripts/icons.py`, `references/icon-map.json`, `references/icons.md`,
  SKILL.md §2.8, pattern #8b) are untouched by this release, they postdate
  the fork this merge is based on and were carefully preserved through the
  merge.
- **No change** to `scripts/thumbnail.py`, `scripts/visual_qa.py`,
  `scripts/render_timesaver_library.py`, or the brand color constants in
  `metis-brand.md`, verified identical to v1.1.0.

### Test plan

```bash
PYTHON="C:/Users/navan/AppData/Local/Programs/Python/Python312/pythonw.exe"
cd metis-pptx/v1.2.0/metis-pptx

# 1. Asset resolution runs standalone and reports bundled master available
"$PYTHON" scripts/resolve_assets.py --json

# 2. Icon feature still importable and functional (regression check)
# Run from inside scripts/ so a stray "scripts" package in site-packages
# cannot shadow the local namespace package and break the import.
(cd scripts && "$PYTHON" -c "from icons import suggest_icon, lucide_icon_card; print(suggest_icon('Security and Compliance'))")

# 3. Build a smoke deck from the bundled master using a native layout
"$PYTHON" -c "
from pptx import Presentation
prs = Presentation('assets/master.pptx')
total = sum(len(m.slide_layouts) for m in prs.slide_masters)
print(total, 'layouts available')
"
```

Expected: all three commands succeed with no traceback; `suggest_icon` returns
`shield-check`; layout count is 32 (the template ships as two slide masters,
6 layouts on the first, 26 on the second; `Presentation.slide_layouts` alone
only exposes the first master, so sum across `prs.slide_masters` to get the
full count).

## v4.4.0 — 2026-05-29

### Fixed — Windows icon rendering (pycairo fallback)

`icons.py` no longer hard-fails when `cairosvg` cannot find system `libcairo`.
A built-in pycairo SVG path renderer handles download, recolor, and rasterize
using only `pycairo` (which ships its own native DLL on Windows/macOS wheels).

**Renderer priority:** cairosvg (best quality) -> pycairo (zero system deps).
Detected automatically at import time via `_RENDERER` flag.

### Added — Auto-icon selection

Icons are now added **automatically** to card-based slides without explicit
user prompting. Three new pieces:

- `references/icon-map.json` — 150+ concept-to-Lucide-icon mappings across
  8 categories (people, technology, security, process, documents,
  communication, business, structure, actions)
- `suggest_icon(title)` function in `icons.py` — scans card title against
  the concept map, returns best-match Lucide name or fallback
- Auto-icon rules in SKILL.md Section 2.8 — "Card-based slides get icons
  automatically unless items are inherently numbered/ordered"

**New public API:**
```python
from scripts.icons import suggest_icon
icon = suggest_icon("Security and Compliance")  # -> "shield-check"
icon = suggest_icon("Claude Agents")             # -> "bot"
```

### Changed

- SKILL.md Section 2.8 rewritten: auto-icon rules, suggest_icon workflow,
  updated dependency docs (pycairo recommended for Windows)
- Dependencies section: `pycairo` listed as recommended; `cairosvg` as
  alternative

---

## v4.4.0 (release folder: v1.1.0) — 2026-05-22

### Added — Programmatic Lucide icon support

Real graphical icons in build scripts, via a new helper module.

**New files:**
- `scripts/icons.py` — Lucide download + recolor + rasterize + insert helpers
- `references/icons.md` — Catalog guidance, consistency rules, fallback hierarchy

**Public API:**
```python
from scripts.icons import lucide_icon, add_lucide_icon, lucide_icon_card
```

- `lucide_icon(name, color, size_px)` → returns a cached PNG path
- `add_lucide_icon(slide, name, left, top, size, color)` → inserts on slide
- `lucide_icon_card(slide, icon, title, body, left, top, width, ...)` → full
  Metis-styled card component

**SKILL.md changes:**
- Section 2.1 Asset Paths — Icon Library row split into "(manual)" (the
  existing shared-drive `Icon_Lib.pptx`) and "(programmatic)" (the new
  Lucide helper).
- New Section 2.8 "Graphical Icons (Lucide)" — when/how to use, decision
  guide vs. `icon_circle_text`, brand alignment, dependencies, editing-mode
  guidance.

**patterns.md changes:**
- New pattern #8b "Graphical Icon Card (Lucide)" added beside the existing
  #8 "Icon Circle + Text". Both coexist; pick per content.
- Rotation-guidance tables updated to include #8b as a third option for
  3-5 key-points slides.

**metis-brand.md changes:**
- New recipe #8b "Graphical Icon Card (Lucide)" with full code example.
- Existing recipe #8 "Icon Circle + Text" is untouched.

### Compatibility

- **Additive only.** No existing component, recipe, or asset path was
  removed or renamed.
- **No breaking changes** to existing build scripts. The shared-drive
  `Icon_Lib.pptx` workflow still works exactly as before.
- **New deps:** `cairosvg` (Python), `libcairo` (system). See SKILL.md
  Section 2.8 for install commands per platform.

### Why

The existing icon path (shared-drive `Icon_Lib.pptx`) required manual
copy/paste in PowerPoint and was not usable from Python build scripts.
Consultants building decks programmatically either drew icons freehand
from primitives — which always looks unprofessional — or omitted icons
entirely. This release closes the gap with a one-line call:

```python
lucide_icon_card(slide, "shield-check", "Compliance & Risk",
                 "Validate retention rules against regulatory requirements.",
                 left=Inches(0.5), top=Inches(2), width=Inches(3.0))
```

### Test plan

```bash
# After install
cd <skill-root>
pip install cairosvg
# macOS: brew install cairo (one time)
# Linux: apt-get install libcairo2 (one time)

# Smoke test: render one Lucide icon and insert into a blank pptx
python -c "
from scripts.icons import lucide_icon_card
from pptx import Presentation
from pptx.util import Inches
prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
s = prs.slides.add_slide(prs.slide_layouts[6])
lucide_icon_card(s, 'shield-check', 'Test', 'Hello Lucide',
                 left=Inches(1), top=Inches(2), width=Inches(3))
prs.save('icon_smoke.pptx'); print('OK: icon_smoke.pptx')
"
```

---

## v4.3.2 (release folder: v1.0.1) — 2026-05-20

Prior release. See previous changelog history for details.

## v4.3.1 (release folder: v1.0.0) — 2026-05-19

Prior release.
