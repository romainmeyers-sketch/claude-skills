"""Turn deck page images into the database documents Spotlight reads.

python prep_pages.py PATH [PATH ...] [--open]

PATH is an image file or a folder of images. Writes img.json, th.json and
pg_<n>.json into a new folder under the system temp directory (prefix spotlight_)
and prints one JSON summary. Every document stays under the 262,144 byte limit.
"""
import argparse, base64, io, json, os, re, subprocess, sys, tempfile
from PIL import Image

EXT = (".png", ".jpg", ".jpeg", ".webp")
DOC_MAX = 200_000
HARD_MAX = 250_000
TOTAL_MAX = 1_600_000
MAX_PAGES = 20


def natural(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", os.path.basename(p))]


def collect(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            out += [os.path.join(p, f) for f in os.listdir(p) if f.lower().endswith(EXT)]
        elif p.lower().endswith(EXT):
            out.append(p)
    return sorted(out, key=natural)


def uri(path, width, q):
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def size(doc):
    return len(json.dumps(doc))


def fit(build, widths):
    """build(width, q) -> doc. Returns the first doc under DOC_MAX, else the
    smallest tried doc under HARD_MAX, else None."""
    best = None
    for w in widths:
        for q in range(80, 29, -8):
            doc = build(w, q)
            s = size(doc)
            if s <= DOC_MAX:
                return doc
            if s <= HARD_MAX and (best is None or s < size(best)):
                best = doc
    return best


def pick(n, k):
    return [round(i * (n - 1) / (k - 1)) for i in range(k)] if k > 1 else [0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--open", action="store_true")
    a = ap.parse_args()
    files = collect(a.paths)
    if not files:
        sys.exit("No page images found.")
    total0 = len(files)
    cap = min(total0, MAX_PAGES)
    cache = {}
    while True:
        keep = pick(total0, cap) if cap < total0 else list(range(total0))
        pages = []
        for i in keep:
            if i not in cache:
                cache[i] = fit(lambda w, q, f=files[i]: {"t": "page", "src": uri(f, w, q)}, (1280, 1024, 800, 640))
            d = cache[i]
            if d is not None:
                pages.append((i, d))
        keep = [i for i, _ in pages]
        size_pages = sum(size(d) for _, d in pages)
        if (size_pages <= TOTAL_MAX and keep) or cap <= 4:
            break
        cap -= 2
    if not keep:
        sys.exit("No page fits the board size limit.")
    pages = [d for _, d in pages]
    n = len(keep)
    strip = sorted({round(k * (n - 1) / 5) + 1 for k in range(1, 5)} - {1}) if n > 5 else list(range(2, n + 1))
    src = [files[i] for i in keep]
    out = tempfile.mkdtemp(prefix="spotlight_")
    for i, d in enumerate(pages):
        d["n"] = i + 1
        with open(os.path.join(out, "pg_%d.json" % (i + 1)), "w") as fh:
            json.dump(d, fh)

    th = None
    for w, q in ((200, 60), (160, 50), (120, 45), (96, 40), (72, 35)):
        cand = {"t": "th", "srcs": [uri(f, w, q) for f in src]}
        if size(cand) <= HARD_MAX:
            th = cand
            break
    if th:
        with open(os.path.join(out, "th.json"), "w") as fh:
            json.dump(th, fh)

    img = None
    ks = list(strip)
    while img is None:
        img = fit(lambda w, q: {"t": "img", "lead": {"n": 1, "src": uri(src[0], w, q)},
                                "strip": [{"n": k, "src": uri(src[k - 1], min(w, 320), q)} for k in ks]},
                  (960, 720, 480))
        if img is None:
            if not ks:
                sys.exit("The lead page does not fit the board size limit.")
            ks.pop()
    strip = ks
    with open(os.path.join(out, "img.json"), "w") as fh:
        json.dump(img, fh)

    sizes = {f: os.path.getsize(os.path.join(out, f)) for f in os.listdir(out)}
    if max(sizes.values()) >= 262144:
        sys.exit("A prepared document is over the size limit: %s" % sizes)

    if a.open:
        for f in [src[0]] + [src[k - 1] for k in strip]:
            if sys.platform == "win32":
                os.startfile(f)
            else:
                subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", f])
    print(json.dumps({
        "out": out, "original_pages": total0, "kept_pages": n, "dropped_pages": total0 - n,
        "kept_source_numbers": [i + 1 for i in keep], "lead": 1, "strip": strip,
        "thing": {"kind": "pages", "count": n, "leadN": 1, "stripN": strip},
        "shown_files": [src[0]] + [src[k - 1] for k in strip],
        "thumbnails_dropped": th is None,
        "max_file_bytes": max(sizes.values()),
        "total_kb": round(sum(sizes.values()) / 1024)}))


main()
