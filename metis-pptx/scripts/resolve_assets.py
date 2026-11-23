#!/usr/bin/env python3
"""
resolve_assets.py locates Metis brand assets across every place they might live,
and reports which are available. Run this FIRST in the generation workflow so the
build script auto-references the best copy of each asset (and degrades gracefully
when one is missing).

Resolution order for each asset (first existing wins):
  1. Bundled inside this skill            <skill>/assets/
  2. Plugin brand-assets (if installed)   $CLAUDE_PLUGIN_ROOT/brand-assets/
  3. Metis G: shared drive (if mapped)    G:\\Shared drives\\Knowledge Management\\New Brand Assets\\
  4. Manual override                      $METIS_BRAND_ASSETS (point at any folder)

On a Metis machine with the plugin installed or the G: drive mapped, the richer
assets (Timesaver PNG library, firm-overview slides, icon library, logo PNGs)
resolve automatically. On a standalone install (just the .skill), only the
bundled master.pptx resolves and the build degrades:
  - no timesaver_pngs  -> skip Path B reproduction, build diagrams bespoke
  - no intro-slides    -> skip the optional firm-overview section
  - no icon library    -> use drawn shapes instead of library icons
  - no logo PNGs        -> not needed; the bundled master embeds the brand frame

Usage:
  python resolve_assets.py [--skill-dir DIR] [--json]
Prints a human summary, then a JSON block the build script can parse.
"""
import os, sys, json, glob, argparse

def _roots(skill_dir):
    roots = []
    # 1. bundled
    roots.append(("bundled", os.path.join(skill_dir, "assets")))
    # 2. plugin
    plugin = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if plugin:
        roots.append(("plugin", os.path.join(plugin, "brand-assets")))
    # 3. G: shared drive (Windows; harmless elsewhere)
    roots.append(("gdrive", r"G:\Shared drives\Knowledge Management\New Brand Assets"))
    roots.append(("gdrive", r"G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets"))
    # 4. explicit override
    override = os.environ.get("METIS_BRAND_ASSETS")
    if override:
        roots.append(("override", override))
    return roots

# asset -> list of candidate relative paths to probe under each root
ASSETS = {
    "master":        ["master.pptx",
                      "Metis_Intro Slides and Template_2025.potx"],
    "intro_slides":  ["intro-slides.pptx",
                      "Intro Slides.pptx"],
    "icon_lib":      ["Icon_Lib.pptx",
                      "Icon Library.pptx"],
    "logo_white":    [r"Metis Strategy Logo\Metis Strategy White RGB logo.png",
                      "Metis Strategy White RGB logo.png"],
    "logo_black_mint": [r"Metis Strategy Logo\Metis Strategy Black-Mint RGB Logo.png",
                        "Metis Strategy Black-Mint RGB Logo.png"],
    # directory of slide-{N}.png previews
    "timesaver_pngs": ["timesaver_pngs"],
}

def _resolve_file(roots, rels):
    for src, root in roots:
        for rel in rels:
            p = os.path.join(root, rel)
            if os.path.isfile(p):
                return p, src
    return None, None

def _resolve_dir(roots, rels):
    for src, root in roots:
        for rel in rels:
            p = os.path.join(root, rel)
            if os.path.isdir(p) and glob.glob(os.path.join(p, "slide-*.png")):
                return p, src
    return None, None

def resolve(skill_dir):
    roots = _roots(skill_dir)
    out = {}
    for name, rels in ASSETS.items():
        if name == "timesaver_pngs":
            path, src = _resolve_dir(roots, rels)
        else:
            path, src = _resolve_file(roots, rels)
        out[name] = {"path": path, "source": src, "available": path is not None}
    # master must always resolve (bundled fallback); surface a clear error if not
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill-dir", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--json", action="store_true", help="print only the JSON block")
    args = ap.parse_args()
    res = resolve(args.skill_dir)

    if not args.json:
        print("Metis brand-asset resolution")
        print("skill dir:", args.skill_dir)
        print("-" * 60)
        for name, info in res.items():
            status = info["source"] if info["available"] else "MISSING (degrade)"
            print(f"  {name:16} {status:10} {info['path'] or ''}")
        print("-" * 60)
        if not res["master"]["available"]:
            print("ERROR: master template not found. Generation cannot proceed.")
        deg = [k for k, v in res.items() if not v["available"]]
        if deg:
            print("Degrading (assets absent):", ", ".join(deg))
            print("  -> timesaver_pngs missing: skip Path B repro, build diagrams bespoke")
            print("  -> intro_slides missing: skip optional firm-overview section")
            print("  -> icon_lib missing: use drawn shapes instead of library icons")
        print()
        print("JSON:")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
