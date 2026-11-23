"""Rebuilds _assets/sprite.html from the raw Lucide SVGs in _icons/.

Icons are Lucide, always. Never an emoji, never a hand-drawn path. To add one,
download it into _icons/ and re-run this:

    curl -o _icons/<name>.svg \\
      https://cdn.jsdelivr.net/npm/lucide-static@latest/icons/<name>.svg
    python3 build_sprite.py

The symbol id is the filename, so _icons/shield.svg becomes #i-shield and is
used as <svg class="icn"><use href="#i-shield"/></svg>.

Colour and stroke weight are NOT baked in. The sprite carries currentColor and
one stroke-width, so every icon on the page inherits the surface it sits on and
the whole set stays visually consistent. Size comes from the --ics custom
property, never from font-size.
"""
import os
import re

SRC = "_icons"
OUT_DIR = "_assets"
OUT = os.path.join(OUT_DIR, "sprite.html")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)

    if not os.path.isdir(SRC):
        raise SystemExit("no %s/ folder here. Run this from the project folder." % SRC)

    out = []
    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".svg"):
            continue
        key = name[:-4]
        svg = open(os.path.join(SRC, name), encoding="utf-8").read()
        # Lucide ships a 24x24 viewBox with the stroke attributes on the root
        # <svg>. Keep the geometry, drop the wrapper, and let the sprite's own
        # attributes carry colour and weight for every symbol at once.
        inner = re.sub(r"^.*?<svg[^>]*>", "", svg, flags=re.S)
        inner = inner.replace("</svg>", "").strip()
        inner = re.sub(r"\s+", " ", inner)
        if not inner:
            print("  skipped %s: no geometry found" % name)
            continue
        out.append('<symbol id="i-%s" viewBox="0 0 24 24">%s</symbol>' % (key, inner))

    if not out:
        raise SystemExit("no SVGs in %s/" % SRC)

    sprite = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" '
              'focusable="false" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round">'
              + "".join(out) + "</svg>")

    os.makedirs(OUT_DIR, exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(sprite)
    print("icons: %d   sprite: %d bytes -> %s" % (len(out), len(sprite), OUT))
    print("ids: " + ", ".join("#i-" + n[:-4] for n in sorted(os.listdir(SRC))
                              if n.endswith(".svg")))


if __name__ == "__main__":
    main()
