#!/usr/bin/env python3
"""Diff two inventory snapshots and flag anything that changed outside scope.

Usage:
    python compare.py before.json after.json --scope 6
    python compare.py before.json after.json --scope 6,7 --tolerance 0.02
    python compare.py before.json after.json --scope all

Units are aligned by content, not by index, so deleting slide 10 does not
report slides 11 to 38 as changed. Pure renumbering after an insert or delete
is reported once as a note instead of once per slide.

Exit codes:
    0  only in-scope changes (or no changes)
    1  at least one out-of-scope change  -> collateral damage, fix it
    2  bad input
"""

import argparse
import hashlib
import json
import re
import sys
from difflib import SequenceMatcher

POS_NAMES = ("left", "top", "width", "height")


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        sys.exit("cannot read %s: %s" % (path, exc))


def h(*parts):
    d = hashlib.sha1()
    for p in parts:
        d.update(repr(p).encode("utf-8", "replace"))
    return d.hexdigest()[:12]


def is_slide_number(el):
    ph = str(el.get("ph") or "").upper()
    name = (el.get("name") or "").lower()
    return "SLIDE_NUMBER" in ph or "slide number" in name


def is_renumber(el, prop, detail):
    """A slide-number placeholder whose text went from one integer to another."""
    if prop != "text" or not is_slide_number(el):
        return False
    return bool(re.match(r"^'\d+' -> '\d+'$", detail))


def align_key(unit):
    """Identity of a unit, ignoring its own page number.

    Page numbers change for every downstream slide when one is inserted or
    removed, so including them would make alignment useless exactly when it
    matters most.
    """
    parts = [e.get("digest") for e in unit.get("elements", [])
             if not is_slide_number(e)]
    return h(parts, unit.get("layout"))


def align(before_units, after_units):
    """Pair up units by content. Returns [(before|None, after|None), ...]."""
    bkeys = [align_key(u) for u in before_units]
    akeys = [align_key(u) for u in after_units]
    pairs = []
    sm = SequenceMatcher(None, bkeys, akeys, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for off in range(i2 - i1):
                pairs.append((before_units[i1 + off], after_units[j1 + off]))
        elif tag == "replace":
            bblock, ablock = before_units[i1:i2], after_units[j1:j2]
            # pair by title first, then by position within the block
            used = set()
            for b in bblock:
                match = None
                for k, a in enumerate(ablock):
                    if k in used:
                        continue
                    if b.get("name") and b["name"] == a.get("name"):
                        match, used = a, used | {k}
                        break
                pairs.append((b, match))
            leftovers = [a for k, a in enumerate(ablock) if k not in used]
            unmatched = [p for p in pairs if p[1] is None and p[0] in bblock]
            for slot, a in zip(unmatched, leftovers):
                pairs[pairs.index(slot)] = (slot[0], a)
                leftovers = leftovers[1:]
            for a in leftovers:
                pairs.append((None, a))
        elif tag == "delete":
            pairs.extend((b, None) for b in before_units[i1:i2])
        elif tag == "insert":
            pairs.extend((None, a) for a in after_units[j1:j2])
    return pairs


def index_elements(unit):
    """Key elements by stable key, falling back to name plus ordinal."""
    by_key, seen = {}, {}
    for el in unit.get("elements", []):
        key = el.get("key")
        if not key or key in by_key:
            base = "%s~%s" % (el.get("name"), el.get("type"))
            seen[base] = seen.get(base, 0) + 1
            key = "%s#%d" % (base, seen[base])
        by_key[key] = el
    return by_key


def match_moved(removed, added):
    """Pair a removed element with an added one that looks like the same thing.

    Editing tools often rewrite a shape rather than mutate it, which changes its
    id. Without this, every such edit reads as delete plus insert.
    """
    pairs, left, right = [], list(removed.items()), list(added.items())
    for rk, rel in list(left):
        best, score = None, 0
        for ak, ael in right:
            s = 0
            if rel.get("name") == ael.get("name"):
                s += 3
            if rel.get("type") == ael.get("type"):
                s += 1
            if rel.get("text_digest") == ael.get("text_digest"):
                s += 3
            if rel.get("pos") == ael.get("pos"):
                s += 2
            if s > score:
                best, score = (ak, ael), s
        if best and score >= 4:
            pairs.append((rel, best[1]))
            right = [(k, v) for k, v in right if k != best[0]]
            left = [(k, v) for k, v in left if k != rk]
    return pairs, dict(left), dict(right)


def diff_element(before, after, tol):
    changes = []

    if before.get("text") != after.get("text"):
        changes.append(("text", "%r -> %r" % (
            (before.get("text") or "")[:60], (after.get("text") or "")[:60])))

    bp, ap = before.get("pos") or [], after.get("pos") or []
    for i, nm in enumerate(POS_NAMES):
        b = bp[i] if i < len(bp) else None
        a = ap[i] if i < len(ap) else None
        if b is None and a is None:
            continue
        if b is None or a is None or abs(a - b) > tol:
            changes.append((nm, "%s -> %s" % (b, a)))

    bf, af = before.get("font") or {}, after.get("font") or {}
    for prop in ("sizes", "bold", "colors"):
        if bf.get(prop) != af.get(prop):
            changes.append(("font.%s" % prop, "%s -> %s" % (
                bf.get(prop), af.get(prop))))

    if before.get("fill") != after.get("fill"):
        changes.append(("fill", "%s -> %s" % (
            before.get("fill"), after.get("fill"))))

    be, ae = before.get("extra") or {}, after.get("extra") or {}
    for key in sorted(set(be) | set(ae)):
        if be.get(key) != ae.get(key):
            changes.append(("extra.%s" % key, "%.60s -> %.60s" % (
                str(be.get(key)), str(ae.get(key)))))

    return changes


def parse_scope(raw, all_indexes):
    if raw is None:
        return set()
    raw = raw.strip().lower()
    if raw in ("all", "*"):
        return set(all_indexes)
    scope = set()
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            scope.update(range(int(a), int(b) + 1))
        else:
            scope.add(int(chunk))
    return scope


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--scope", help="slide/section numbers allowed to change, "
                                    "e.g. 6 or 6,7 or 4-6 or all")
    ap.add_argument("--tolerance", type=float, default=0.01,
                    help="inches of position drift to ignore (default 0.01)")
    ap.add_argument("--quiet", action="store_true",
                    help="only report out-of-scope changes")
    args = ap.parse_args()

    before, after = load(args.before), load(args.after)
    if before.get("kind") != after.get("kind"):
        sys.exit(2)

    label = before.get("unit_label", "unit")
    bunits = before.get("units", [])
    aunits = after.get("units", [])
    all_idx = {u["index"] for u in bunits} | {u["index"] for u in aunits}
    scope = parse_scope(args.scope, all_idx)

    in_scope, out_scope, notes = [], [], []
    structural = len(bunits) != len(aunits)

    def record(idx, line):
        bucket = in_scope if idx in scope else out_scope
        bucket.append("%s %s: %s" % (label, idx, line))

    # document level
    bt, at = before.get("tokens") or {}, after.get("tokens") or {}
    for k in sorted(set(bt) | set(at)):
        if bt.get(k) != at.get(k):
            out_scope.append("document tokens: %s  %s -> %s" % (
                k, bt.get(k), at.get(k)))
    if before.get("slide_size") != after.get("slide_size"):
        out_scope.append("document: slide size %s -> %s" % (
            before.get("slide_size"), after.get("slide_size")))

    # reviewer comments: losing one is always a defect, in scope or not
    bc = before.get("comments") or {}
    ac = after.get("comments") or {}
    if bc.get("total", 0) > ac.get("total", 0):
        lost = []
        for sl, n in sorted((bc.get("by_slide") or {}).items(),
                            key=lambda kv: int(kv[0])):
            after_n = (ac.get("by_slide") or {}).get(sl, 0)
            if after_n < n:
                lost.append("slide %s (%d -> %d)" % (sl, n, after_n))
        out_scope.append(
            "COMMENTS LOST: %d -> %d across the deck%s. Restore the backup: "
            "reviewer comments cannot be rebuilt from the text." % (
                bc.get("total", 0), ac.get("total", 0),
                ", " + "; ".join(lost) if lost else ""))
    elif bc.get("digest") and bc.get("digest") != ac.get("digest"):
        out_scope.append(
            "comments changed (%d -> %d). Check that no thread was edited "
            "or resolved." % (bc.get("total", 0), ac.get("total", 0)))

    # unit level, aligned by content
    moved = []
    for b, a in align(bunits, aunits):
        if b is None:
            record(a["index"], "ADDED (%s)" % (a.get("name") or "untitled"))
            continue
        if a is None:
            record(b["index"], "REMOVED (%s)" % (b.get("name") or "untitled"))
            continue

        idx = a["index"]
        if b["index"] != a["index"]:
            moved.append("%s %d -> %d (%s)" % (
                label, b["index"], a["index"],
                (a.get("name") or "untitled")[:40]))

        if b.get("layout") != a.get("layout"):
            record(idx, "layout %s -> %s" % (b.get("layout"), a.get("layout")))
        if b.get("notes_digest") != a.get("notes_digest"):
            record(idx, "speaker notes changed")

        be, ae = index_elements(b), index_elements(a)
        common = set(be) & set(ae)
        removed = {k: be[k] for k in set(be) - common}
        added = {k: ae[k] for k in set(ae) - common}
        matched, removed, added = match_moved(removed, added)

        real = 0
        for pair in [(be[k], ae[k]) for k in sorted(common)] + matched:
            bel, ael = pair
            for prop, detail in diff_element(bel, ael, args.tolerance):
                if structural and is_renumber(bel, prop, detail):
                    continue          # page numbers following an insert/delete
                real += 1
                record(idx, "%s [%s] %s: %s" % (
                    bel.get("name"), bel.get("type"), prop, detail))

        for el in removed.values():
            real += 1
            record(idx, "REMOVED element %s [%s] %r" % (
                el.get("name"), el.get("type"), (el.get("text") or "")[:50]))
        for el in added.values():
            real += 1
            record(idx, "ADDED element %s [%s] %r" % (
                el.get("name"), el.get("type"), (el.get("text") or "")[:50]))

        # safety net: text can live in wrappers that are not tracked as
        # elements, so a digest move with nothing to explain it still counts.
        if not real and b.get("text_digest") != a.get("text_digest") and not (
                structural and is_slide_number_only(b, a)):
            record(idx, "text changed inside an untracked wrapper "
                        "(%s -> %s chars). Open it and look." % (
                            b.get("text_len", "?"), a.get("text_len", "?")))

    if structural:
        notes.append("%s count %d -> %d" % (label, len(bunits), len(aunits)))
    if moved:
        notes.append("renumbered: %s%s" % (
            "; ".join(moved[:6]), " ..." if len(moved) > 6 else ""))

    # report
    if not in_scope and not out_scope and not notes:
        print("NO CHANGES between the two snapshots.")
        print("If you just made an edit, it did not apply. "
              "Debug that before reporting anything.")
        return 0

    if notes:
        print("STRUCTURE")
        for line in notes:
            print("  " + line)
        print()

    if in_scope and not args.quiet:
        print("IN SCOPE (%d change%s)" % (
            len(in_scope), "" if len(in_scope) == 1 else "s"))
        for line in in_scope:
            print("  " + line)
        print()

    if out_scope:
        print("OUT OF SCOPE (%d change%s)  <-- collateral damage" % (
            len(out_scope), "" if len(out_scope) == 1 else "s"))
        for line in out_scope:
            print("  " + line)
        print()
        print("Fix these or restore the backup. Do not report done.")
        return 1

    print("CLEAN: every change is inside %s %s." % (
        label, args.scope or "(none declared)"))
    if structural:
        print("Structural change: check numbering, agendas, rails and "
              "cross-references before reporting done.")
    return 0


def is_slide_number_only(b, a):
    """True when the only text difference is the page number."""
    def strip_numbers(unit):
        return " ".join(
            e.get("text", "") for e in unit.get("elements", [])
            if not is_slide_number(e))
    return strip_numbers(b) == strip_numbers(a)


if __name__ == "__main__":
    sys.exit(main())
