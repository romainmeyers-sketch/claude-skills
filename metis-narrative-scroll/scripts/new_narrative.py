"""Scaffolds a new Metis narrative scroll project.

    python3 new_narrative.py "<target folder>" ["Title"]

Creates a self-sufficient project: the source, its own copy of the theme and
the motion engine, the icon sprite, the logos, the build script and the three
QA suites. Nothing in the project reaches back into the skill folder
afterwards, so a project keeps working if the skill moves or changes.

The project's own copies are the point. A deck that needs a different accent,
an extra section pattern or a tweaked entrance edits its own _assets/_theme.css
without touching every other deck built from this skill.
"""
import os
import shutil
import sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__.strip())

    dest = os.path.abspath(os.path.expanduser(sys.argv[1]))
    title = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(dest)

    if os.path.exists(dest) and os.listdir(dest):
        # Never write into a folder that already holds work.
        sys.exit("refusing to scaffold into a non-empty folder:\n  %s\n"
                 "Pick a new folder, or move the existing contents out first." % dest)

    os.makedirs(os.path.join(dest, "_assets"), exist_ok=True)
    os.makedirs(os.path.join(dest, "qa"), exist_ok=True)
    os.makedirs(os.path.join(dest, "_icons"), exist_ok=True)
    os.makedirs(os.path.join(dest, "Editions"), exist_ok=True)

    # ---- the source, with its title filled in -----------------------------
    src = open(os.path.join(SKILL, "templates", "narrative.src.html"),
               encoding="utf-8").read()
    src = src.replace("__TITLE__", title)
    open(os.path.join(dest, "narrative.src.html"), "w", encoding="utf-8").write(src)

    # ---- build inputs. ALL of them live in _assets/ ------------------------
    # They live in one obviously-load-bearing folder because a previous project
    # kept them in a folder named _shots next to disposable QA captures, and
    # they were deleted with the captures. The build then could not run at all.
    for name, target in [
        ("templates/_theme.css", "_assets/_theme.css"),
        ("templates/_engine.js", "_assets/_engine.js"),
        ("assets/sprite.html", "_assets/sprite.html"),
        ("assets/LOGO_WHITE.txt", "_assets/LOGO_WHITE.txt"),
        ("assets/LOGO_NAVY.txt", "_assets/LOGO_NAVY.txt"),
        ("scripts/build.py", "build.py"),
        ("scripts/build_sprite.py", "build_sprite.py"),
        ("scripts/check_template.py", "check_template.py"),
        ("qa/_harness.mjs", "qa/_harness.mjs"),
        ("qa/qa-render.mjs", "qa/qa-render.mjs"),
        ("qa/qa-jumps.mjs", "qa/qa-jumps.mjs"),
        ("qa/qa-spacing.mjs", "qa/qa-spacing.mjs"),
    ]:
        shutil.copy2(os.path.join(SKILL, name), os.path.join(dest, target))

    # Raw Lucide SVGs, so the sprite can be regenerated or extended.
    for f in os.listdir(os.path.join(SKILL, "assets", "icons")):
        if f.endswith(".svg"):
            shutil.copy2(os.path.join(SKILL, "assets", "icons", f),
                         os.path.join(dest, "_icons", f))

    open(os.path.join(dest, "_assets", "images.json"), "w").write("{}\n")

    open(os.path.join(dest, "README.md"), "w", encoding="utf-8").write(
        README.replace("__TITLE__", title))

    print("scaffolded: %s\n" % dest)
    print("  narrative.src.html   the only file you author")
    print("  _assets/             theme, engine, sprite, logos, images.json")
    print("  _icons/              raw Lucide SVGs, for build_sprite.py")
    print("  build.py             inlines everything into Editions/")
    print("  check_template.py    catches a class or icon that does not exist")
    print("  qa/                  three suites, run all three before sending")
    print("\nNext:")
    print("  1. Fill in the __PLACEHOLDERS__ in narrative.src.html")
    print("  2. Add screenshots to _assets/images.json as {\"SHOT_ONE\": \"data:image/...\"}")
    print("  3. python3 build.py --check")
    print("  4. python3 build.py")


README = """# __TITLE__

A Metis narrative scroll. One self-contained HTML file per edition.

## Build

```
python3 build.py --check     # writes nothing, says what it would do
python3 build.py             # writes Editions/__TITLE__ - <Edition>.html
```

The filename comes from `<meta name="edition">` in `narrative.src.html`. Change
that one line to start a new edition: it drives the masthead, the hero
dateline, the colophon and the output filename, so a new edition writes a NEW
file and the previous one is left exactly as it is.

## Verify before sending

All three, against the BUILT file in `Editions/`, never against the source.

```
node qa/qa-render.mjs  "Editions/<file>.html"
node qa/qa-jumps.mjs   "Editions/<file>.html"
node qa/qa-spacing.mjs "Editions/<file>.html"
```

## Layout

| Path | What it is |
|---|---|
| `narrative.src.html` | The authored source. The only file you write. |
| `_assets/` | Every build input. Nothing outside it is read by the build. |
| `_icons/` | Raw Lucide SVGs, for regenerating `_assets/sprite.html` |
| `Editions/` | Every finished edition. One file each. |
| `qa/` | The three verification suites |

Scratch and QA captures go to the OS temp folder, never in here.
"""

if __name__ == "__main__":
    main()
