# Asset resolution: where the skill finds brand assets

This skill is designed to work in three situations without any per-user setup:

1. **Standalone**: someone installed just the `.skill` package (Save skill /
   Settings → Capabilities). Only the bundled template is present.
2. **Inside the `metis-skills` plugin**: the full `brand-assets/` folder is
   available via `$CLAUDE_PLUGIN_ROOT`.
3. **On a Metis machine with the G: drive mapped**: the canonical shared assets
   live on `G:`.

`scripts/resolve_assets.py` handles all three. Run it first in the generation
workflow; it returns the best available path for each asset and flags what is
missing so the build degrades gracefully.

## Resolution order (first existing wins)

For every asset, the resolver probes these roots in order:

| # | Source | Path |
|---|---|---|
| 1 | **Bundled** (always present) | `<skill dir>/assets/` |
| 2 | **Plugin** (if installed) | `$CLAUDE_PLUGIN_ROOT/brand-assets/` |
| 3 | **Metis G: drive** (if mapped) | `G:\Shared drives\Knowledge Management\New Brand Assets\` (and `…\New Brand Assets\PPT Assets\`) |
| 4 | **Manual override** | `$METIS_BRAND_ASSETS` (set this env var to point at any folder) |

So on a Metis machine the richer G:/plugin copies are auto-referenced; with
nothing but the `.skill`, the bundled copy is used and extras are skipped.

## Assets and what each is for

| Asset key | What it is | Bundled? | Needed for | If missing |
|---|---|---|---|---|
| `master` | Blank deck, 32 named layouts, brand frame (logo, green arrow, palette, fonts) | **Yes** | All generation | Never missing |
| `timesaver_pngs` | 260 slide-structure preview PNGs (`slide-{N}.png`) | No | Path B metaphor reproduction (§0.6) | Skip Path B; build diagrams bespoke |
| `intro_slides` | Metis firm-overview slides | No | Optional firm-overview section | Skip that section |
| `icon_lib` | Metis icon library deck | No | Library icons | Use drawn shapes |
| `logo_white` / `logo_black_mint` | Logo PNGs | No | Standalone logo placement | Not needed; master embeds the frame |

## How to share

- **Standalone (`.skill` over Slack):** fully usable. Native-layout decks,
  bespoke diagrams, tables, charts, and the brand frame all work from the bundled
  `master`. Timesaver library, firm overview, and icon library are unavailable
  and the skill skips them automatically.
- **Full parity:** install inside the `metis-skills` plugin, or run on a machine
  with the G: drive mapped, or set `METIS_BRAND_ASSETS` to a folder containing
  `timesaver_pngs/`, `intro-slides.pptx`, and `Icon_Lib.pptx`. The resolver then
  finds and uses them with no other changes.

## If a Metis filename differs

The resolver probes a couple of common filenames per asset (e.g. `master.pptx`
or `Metis_Intro Slides and Template_2025.potx`). If the firm renames or relocates
an asset, add the new relative path to the `ASSETS` dict in
`scripts/resolve_assets.py`, that is the single place to update.
