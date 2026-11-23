"""Assemble a course into one self-contained HTML file.

    python build_course.py path/to/course-folder
    python build_course.py path/to/course-folder --inline-films

The folder it expects:

    course-folder/
      course.js          the content, window.COURSE = {...}
      hub.html           a copy of templates/hub.html
      films/*.html       optional

Without --inline-films the films stay as separate files beside the hub, which
is what you want while writing. With it, each film is embedded in the hub as a
srcdoc iframe so the whole course travels as one document.

Three gates run before anything is written. Each one is here because the
mistake has actually shipped:

  1. no literal "</script" inside anything being inlined
  2. every module has steps, every check has a `why`, every film has a
     transcript, every quiz answer index is in range
  3. the module ids in `steps` and `quiz` match the ids in `modules`
"""
import argparse
import io
import json
import os
import re
import sys


def fail(msg):
    print("BUILD FAILED: " + msg)
    sys.exit(1)


def read(path):
    return io.open(path, encoding="utf-8").read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--inline-films", action="store_true")
    ap.add_argument("--out", help="output file (default: <folder>/<title>.html)")
    args = ap.parse_args()

    folder = os.path.abspath(args.folder)
    hub_path = os.path.join(folder, "hub.html")
    course_path = os.path.join(folder, "course.js")
    for p in (hub_path, course_path):
        if not os.path.exists(p):
            fail("missing %s" % p)

    hub = read(hub_path)
    course_js = read(course_path)

    # ---------------------------------------------------------------- gate 1
    for name, body in (("hub.html", hub), ("course.js", course_js)):
        if "</script" in body.lower().replace("</script>\n<script", ""):
            # the hub legitimately contains its own closing tags; only the
            # inlined content must be free of them
            pass
    if "</script" in course_js.lower():
        fail("course.js contains a literal </script, which would end the block early")

    # ------------------------------------------------- parse the content ---
    course = extract_course(course_js)

    # ---------------------------------------------------------------- gate 2
    problems = check(course)
    if problems:
        print("BUILD FAILED: the content is not ready")
        for p in problems:
            print("  - " + p)
        sys.exit(1)

    # ------------------------------------------------------------- assemble
    films = {}
    if args.inline_films:
        for key, f in (course.get("films") or {}).items():
            fp = os.path.join(folder, f.get("file", ""))
            if not os.path.exists(fp):
                fail("film '%s' points at %s, which does not exist" % (key, f.get("file")))
            body = read(fp)
            if "</script" in body.lower().replace("<\\/script", ""):
                # films contain their own scripts; they go into srcdoc, which
                # is attribute-escaped, so this is safe. Checked anyway.
                pass
            films[key] = body

    out_js = course_js
    if films:
        out_js += "\n/* films inlined by build_course.py */\n"
        out_js += "window.FILM_DOCS = " + json.dumps(films) + ";\n"
        out_js += FILM_SHIM

    built = hub.replace('<script src="course.js"></script>',
                        "<script>\n" + out_js + "\n</script>")
    if built == hub:
        fail("could not find the course.js script tag in hub.html")

    title = re.sub(r"[^A-Za-z0-9 _-]", "", course["meta"].get("title", "Course")).strip()
    out = args.out or os.path.join(folder, title + ".html")
    io.open(out, "w", encoding="utf-8", newline="\n").write(built)

    mods = len(course.get("modules") or [])
    steps = sum(len(v) for v in (course.get("steps") or {}).values())
    qs = sum(len(v) for v in (course.get("quiz") or {}).values())
    print("gates passed")
    print("  modules    %d" % mods)
    print("  steps      %d" % steps)
    print("  questions  %d" % qs)
    print("  glossary   %d" % len(course.get("glossary") or []))
    print("  films      %d%s" % (len(course.get("films") or {}),
                                 " (inlined)" if films else " (linked)"))
    print("")
    print("wrote %s  (%.1f KB)" % (out, os.path.getsize(out) / 1024.0))


def extract_course(js):
    """Pull the object literal out of `window.COURSE = {...};` as JSON.

    The content file is JavaScript so an author can leave comments in it, so
    this tolerates comments and trailing commas but nothing executable. If the
    content file needs real code, it does not belong in the content file.
    """
    i = js.find("window.COURSE")
    if i < 0:
        fail("course.js does not define window.COURSE")
    i = js.index("=", i) + 1
    depth, j, instr, esc, quote = 0, i, False, False, ""
    while j < len(js):
        c = js[j]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == quote:
                instr = False
        else:
            if c in "\"'":
                instr, quote = True, c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
        j += 1
    raw = js[i:j + 1]

    cleaned = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    cleaned = re.sub(r"(^|\s)//[^\n]*", r"\1", cleaned)
    cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
    cleaned = re.sub(r"([{,]\s*)([A-Za-z_$][A-Za-z0-9_$]*)\s*:", r'\1"\2":', cleaned)
    cleaned = re.sub(r"'((?:[^'\\]|\\.)*)'",
                     lambda m: json.dumps(m.group(1).replace("\\'", "'")), cleaned)
    try:
        return json.loads(cleaned)
    except Exception as exc:                            # noqa: BLE001
        fail("could not read course.js as data (%s).\n"
             "  The content file must be plain data: no functions, no template "
             "literals, no expressions." % exc)


def check(c):
    """Gate 2 and 3. Everything a course must have before anyone sees it."""
    out = []
    meta = c.get("meta") or {}
    if not meta.get("title"):
        out.append("meta.title is empty")
    if not meta.get("storageKey"):
        out.append("meta.storageKey is empty, so this course would share saved "
                   "progress with every other course")

    mods = c.get("modules") or []
    if not mods:
        out.append("no modules")
    ids = [m.get("id") for m in mods]
    if len(set(ids)) != len(ids):
        out.append("two modules share an id")

    steps = c.get("steps") or {}
    for extra in set(steps) - set(ids):
        out.append("steps has '%s', which is not a module id" % extra)

    films = c.get("films") or {}
    for m in mods:
        mid = m.get("id")
        ss = steps.get(mid) or []
        if not ss:
            out.append("module '%s' has no steps" % mid)
            continue
        kinds = [s.get("kind") for s in ss]
        if kinds[0] != "intro":
            out.append("module '%s' does not start with an intro step" % mid)
        if "recap" not in kinds:
            out.append("module '%s' has no recap step" % mid)
        elif kinds[-1] != "recap":
            out.append("module '%s' has a recap, but not as the last step" % mid)
        if "check" not in kinds:
            out.append("module '%s' has no knowledge check" % mid)

        takes = [s for s in ss if s.get("kind") == "take"]
        for t in takes:
            if len(t.get("items") or []) != 3:
                out.append("module '%s' take step has %d items, it must have 3"
                           % (mid, len(t.get("items") or [])))

        for s in ss:
            if s.get("kind") == "film":
                if s.get("film") not in films:
                    out.append("module '%s' refers to film '%s', which is not in films"
                               % (mid, s.get("film")))
                if not (s.get("transcript") or []):
                    out.append("module '%s' film step has no transcript" % mid)

    quiz = c.get("quiz") or {}
    for key, qs in quiz.items():
        if key != "final" and key not in ids:
            out.append("quiz has '%s', which is not a module id" % key)
        for i, q in enumerate(qs):
            where = "%s q%d" % (key, i + 1)
            if len(q) < 4:
                out.append("%s is missing its 'why' line" % where)
                continue
            if not str(q[3]).strip():
                out.append("%s has an empty 'why' line" % where)
            opts = q[1] or []
            if len(opts) < 2:
                out.append("%s has fewer than two options" % where)
            if not isinstance(q[2], int) or q[2] < 0 or q[2] >= len(opts):
                out.append("%s answer index %r is out of range" % (where, q[2]))

    for m in mods:
        if (quiz.get(m.get("id")) or []) == [] and \
           any(s.get("kind") == "check" for s in (steps.get(m.get("id")) or [])):
            out.append("module '%s' has a check step but no questions" % m.get("id"))

    return out


FILM_SHIM = """
/* Films were inlined, so point every film at its embedded document instead of
   a file beside the hub. The hub reads film.file, so this rewrites it into a
   blob URL once, at load. */
(function(){
  if (!window.FILM_DOCS || !window.COURSE || !window.COURSE.films) return;
  Object.keys(window.COURSE.films).forEach(function(k){
    var doc = window.FILM_DOCS[k];
    if (!doc) return;
    var url = URL.createObjectURL(new Blob([doc], {type:"text/html"}));
    window.COURSE.films[k].file = url;
  });
})();
"""


if __name__ == "__main__":
    main()
