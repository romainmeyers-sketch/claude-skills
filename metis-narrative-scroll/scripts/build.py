"""Builds a Metis narrative scroll into ONE self-contained HTML file.

Everything is inlined: theme, motion engine, icon sprite, logos and images.
Nothing is fetched at view time except the Google Fonts stylesheet, so the
page works from a Downloads folder, an email attachment or a shared drive.

    python3 build.py              # build the edition named in the source
    python3 build.py --check      # report what it WOULD do, write nothing

Output goes to "<OUT_DIR>/<Title> - <Edition>.html". The filename comes from
the <meta name="edition"> line in the source, so starting a new edition writes
a NEW file and never overwrites the previous one.

Run this from the project folder. It resolves everything relative to its own
location, so it does not matter what the shell's cwd is.
"""
import json
import os
import re
import sys

SRC = "narrative.src.html"
OUT_DIR = "Editions"
ASSETS = "_assets"

# Months that are not abbreviated in the masthead, per AP style.
FULL_MONTHS = {"March", "April", "May", "June", "July"}


def die(msg):
    sys.exit("build: " + msg)


def short_edition(edition):
    """'August 2026' -> 'Aug 2026'. Anything not Month-Year passes through."""
    parts = edition.split()
    if len(parts) != 2 or not parts[1].isdigit():
        return edition
    month, year = parts
    return (month if month in FULL_MONTHS else month[:3]) + " " + year


def main():
    check_only = "--check" in sys.argv

    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)

    if not os.path.exists(SRC):
        die("no %s here. Run this from the project folder." % SRC)
    html = open(SRC, encoding="utf-8").read()

    # ---- the edition, which names the file --------------------------------
    m = re.search(r'<meta name="edition" content="([^"]+)">', html)
    if not m:
        die('no <meta name="edition" content="..."> in ' + SRC)
    edition = m.group(1).strip()

    t = re.search(r"<title>([^<]+)</title>", html)
    title = (t.group(1).strip() if t else "Narrative").replace("/", "-")

    # ---- collect what gets inlined ----------------------------------------
    def asset(name, required=True):
        p = os.path.join(ASSETS, name)
        if not os.path.exists(p):
            if required:
                die("missing build input: %s" % p)
            return ""
        return open(p, encoding="utf-8").read()

    tokens = {
        "__THEME__": asset("_theme.css"),
        "__ENGINE__": asset("_engine.js"),
        "__SPRITE__": asset("sprite.html"),
        "__LOGO_WHITE__": asset("LOGO_WHITE.txt"),
        "__LOGO_NAVY__": asset("LOGO_NAVY.txt", required=False),
        "__EDITION__": edition,
        "__EDITION_SHORT__": short_edition(edition),
    }

    # Images live in _assets/images.json as {token_name: "data:image/..."}.
    img_path = os.path.join(ASSETS, "images.json")
    if os.path.exists(img_path):
        for k, v in json.load(open(img_path)).items():
            tokens["__%s__" % k.upper()] = v

    # Anything still unresolved is reported by name rather than shipped.
    for k, v in tokens.items():
        html = html.replace(k, v)

    survived = [t for t in tokens if t in html]
    if survived:
        die("token(s) survived substitution: " + ", ".join(sorted(survived)))

    stray = sorted(set(re.findall(r"__[A-Z][A-Z0-9_]{2,}__", html)))
    if stray:
        die("unfilled placeholder(s) would ship as literal text on the page:\n"
            "  " + "\n  ".join(stray) +
            "\nFill them in %s, or add them to %s/images.json." % (SRC, ASSETS))

    # ---- write ------------------------------------------------------------
    out_path = os.path.join(OUT_DIR, "%s - %s.html" % (title, edition))
    existed = os.path.exists(out_path)
    same = existed and open(out_path, encoding="utf-8").read() == html

    if check_only:
        print("title      : %s" % title)
        print("edition    : %s  (masthead: %s)" % (edition, short_edition(edition)))
        print("would write: %s" % out_path)
        print("status     : %s" % ("unchanged" if same else
                                   "would UPDATE existing" if existed
                                   else "would CREATE new"))
        print("size       : %.2f MB" % (len(html.encode()) / 1024 / 1024))
        return

    os.makedirs(OUT_DIR, exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(html)
    print("%s  %s  (%.2f MB)" % (
        "unchanged" if same else "updated  " if existed else "created  ",
        out_path, os.path.getsize(out_path) / 1024 / 1024))

    others = sorted(f for f in os.listdir(OUT_DIR)
                    if f.endswith(".html") and f != os.path.basename(out_path))
    if others:
        print("other editions untouched: " + ", ".join(others))

    print("\nVerify before sending:")
    print('  node qa/qa-render.mjs  "%s"' % out_path)
    print('  node qa/qa-jumps.mjs   "%s"' % out_path)
    print('  node qa/qa-spacing.mjs "%s"' % out_path)


if __name__ == "__main__":
    main()
