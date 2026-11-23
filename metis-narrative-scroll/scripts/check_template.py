"""Checks the template against the theme and the engine.

    python3 check_template.py            # check the skill's own template
    python3 check_template.py <folder>   # check a scaffolded project

This exists because the first version of the template was written from memory
of the patterns rather than from the real markup, and used three classes the
stylesheet does not define (`.hero-logo`, `.mast-logo`, `.dim`). Nothing
errored: the hero logo just rendered at its full natural size, four times too
big, and it took a screenshot to notice. A class that does not exist fails
silently, which is exactly the kind of defect worth a mechanical check.

Run it after editing the template or the theme.
"""
import os
import re
import sys

FAILED = []


def report(ok, label, detail=""):
    print("  %s  %s%s" % ("ok  " if ok else "FAIL", label,
                          ("   " + detail) if detail else ""))
    if not ok:
        FAILED.append(label)


def main():
    if len(sys.argv) > 1:
        root = os.path.abspath(os.path.expanduser(sys.argv[1]))
        tpl_path = os.path.join(root, "narrative.src.html")
        theme_path = os.path.join(root, "_assets", "_theme.css")
        engine_path = os.path.join(root, "_assets", "_engine.js")
        sprite_path = os.path.join(root, "_assets", "sprite.html")
    else:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tpl_path = os.path.join(root, "templates", "narrative.src.html")
        theme_path = os.path.join(root, "templates", "_theme.css")
        engine_path = os.path.join(root, "templates", "_engine.js")
        sprite_path = os.path.join(root, "assets", "sprite.html")

    for p in (tpl_path, theme_path, engine_path, sprite_path):
        if not os.path.exists(p):
            sys.exit("missing: " + p)

    tpl = open(tpl_path, encoding="utf-8").read()
    css = open(theme_path, encoding="utf-8").read()
    engine = open(engine_path, encoding="utf-8").read()
    sprite = open(sprite_path, encoding="utf-8").read()

    print("checking %s\n" % os.path.relpath(tpl_path, root))

    # ---- 1. every class used is defined somewhere in the stylesheet -------
    used = set()
    for attr in re.findall(r'class="([^"]+)"', tpl):
        used.update(attr.split())
    defined = set(re.findall(r"\.([a-zA-Z][\w-]*)", css))
    missing = sorted(c for c in used if c not in defined)
    report(not missing, "every class is defined in the theme",
           ", ".join("." + c for c in missing) if missing else
           "%d classes" % len(used))

    # ---- 2. every icon reference exists in the sprite --------------------
    refs = sorted(set(re.findall(r'<use href="#(i-[\w-]+)"', tpl)))
    have = set(re.findall(r'<symbol id="(i-[\w-]+)"', sprite))
    absent = [r for r in refs if r not in have]
    report(not absent, "every icon reference is in the sprite",
           ", ".join("#" + a for a in absent) if absent else
           "%d refs" % len(refs))

    # ---- 3. every data-anim value the engine knows how to run ------------
    kinds = sorted(set(re.findall(r'data-anim="([\w-]+)"', tpl)))
    known = set(re.findall(r"^\s+(\w+):\s+\"", engine, re.M))
    known |= {"clip", "clipup"}          # handled by their own branches
    unknown = [k for k in kinds if k not in known]
    report(not unknown, "every data-anim value is known to the engine",
           ", ".join(unknown) if unknown else ", ".join(kinds))

    # ---- 4. the ids and hooks the engine requires ------------------------
    for need, why in [("id=\"top\"", "the masthead watches it"),
                      ("id=\"mast\"", "masthead root"),
                      ("id=\"mastBar\"", "read progress bar"),
                      ("id=\"rail\"", "the rail mounts into it")]:
        report(need in tpl, "template carries %s" % need, why)

    # ---- 5. every data-jump points at an id that exists -------------------
    jumps = re.findall(r'data-jump="([\w-]+)"', tpl)
    ids = set(re.findall(r'id="([\w-]+)"', tpl))
    broken = [j for j in jumps if j not in ids]
    report(not broken, "every data-jump target exists",
           ", ".join(broken) if broken else "%d jumps" % len(jumps))

    # ---- 6. house style --------------------------------------------------
    body = tpl[tpl.index("<body>"):] if "<body>" in tpl else tpl
    report("—" not in tpl and "–" not in tpl, "no em or en dashes")
    emoji = re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", body)
    report(not emoji, "no emoji in the DOM",
           "".join(sorted(set(emoji))) if emoji else "")
    report("<img" not in tpl or 'alt="' in tpl, "images carry alt text")

    print()
    if FAILED:
        print("%d CHECK(S) FAILED\n" % len(FAILED))
        sys.exit(1)
    print("TEMPLATE OK\n")


if __name__ == "__main__":
    main()
