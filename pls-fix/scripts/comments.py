"""List, snapshot, verify, and reply to comments in .pptx / .docx files.

Never deletes or edits existing comments, and never changes resolved status.

Usage (run with sys.executable / the full Python path):
  comments.py list     <file> [--json out.json] [--all]
  comments.py backup   <file>
  comments.py snapshot <file> <snapshot.json>
  comments.py verify   <file> <snapshot.json>
  comments.py reply    <file> <replies.json> [--author "Claude"] [--initials "AI"]

replies.json: [{"id": "<comment id from list>", "text": "reply text"}, ...]
"""
import argparse
import copy
import datetime as dt
import json
import os
import random
import shutil
import sys
import uuid
import zipfile
from pathlib import Path, PurePosixPath

from lxml import etree

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p188": "http://schemas.microsoft.com/office/powerpoint/2018/8/main",
    "p15": "http://schemas.microsoft.com/office/powerpoint/2012/main",
    "ac": "http://schemas.microsoft.com/office/drawing/2013/main/command",
    "pc": "http://schemas.microsoft.com/office/powerpoint/2013/main/command",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "w16cex": "http://schemas.microsoft.com/office/word/2018/wordml/cex",
}
REL_MODERN_COMMENTS = "http://schemas.microsoft.com/office/2018/10/relationships/comments"
REL_AUTHORS = "http://schemas.microsoft.com/office/2018/10/relationships/authors"
REL_LEGACY_COMMENTS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"
REL_LEGACY_AUTHORS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/commentAuthors"
REL_SLIDE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
REL_W_COMMENTS_EX = "http://schemas.microsoft.com/office/2011/relationships/commentsExtended"
THREADING_URI = "{C676402C-5697-4E1C-873F-D02D1690AC5C}"
BACKUP_DIR = Path.home() / ".claude" / "comment-backups"


def q(tag):
    pre, local = tag.split(":")
    return "{%s}%s" % (NS[pre], local)


# ---------------------------------------------------------------- package io
class Package:
    def __init__(self, path):
        self.path = Path(path)
        with zipfile.ZipFile(self.path) as z:
            self.infos = z.infolist()
            self.data = {i.filename: z.read(i.filename) for i in self.infos}
        self.dirty = {}

    def has(self, name):
        return name in self.data or name in self.dirty

    def xml(self, name):
        if name in self.dirty:
            return self.dirty[name]
        root = etree.fromstring(self.data[name])
        self.dirty[name] = root
        return root

    def peek(self, name):
        return etree.fromstring(self.data[name]) if name in self.data else None

    def rels(self, part):
        p = PurePosixPath(part)
        rp = str(p.parent / "_rels" / (p.name + ".rels"))
        if not self.has(rp):
            return rp, []
        root = self.xml(rp) if rp in self.dirty else self.peek(rp)
        out = []
        for r in root.findall(q("rel:Relationship")):
            tgt = r.get("Target")
            full = os.path.normpath(str(p.parent / tgt)).replace("\\", "/") if r.get("TargetMode") != "External" else tgt
            out.append((r.get("Id"), r.get("Type"), full, tgt))
        return rp, out

    def add_rel(self, part, rtype, target_rel):
        rp, existing = self.rels(part)
        if not self.has(rp):
            self.dirty[rp] = etree.fromstring(
                b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')
        root = self.xml(rp)
        ids = {r.get("Id") for r in root}
        n = 1
        while f"rId{n}" in ids:
            n += 1
        el = etree.SubElement(root, q("rel:Relationship"))
        el.set("Id", f"rId{n}"); el.set("Type", rtype); el.set("Target", target_rel)

    def add_override(self, partname, ctype):
        ct = self.xml("[Content_Types].xml")
        for o in ct.findall(q("ct:Override")):
            if o.get("PartName") == partname:
                return
        el = etree.SubElement(ct, q("ct:Override"))
        el.set("PartName", partname); el.set("ContentType", ctype)

    def save(self, out=None):
        out = Path(out or self.path)
        tmp = out.with_name(out.name + ".tmp_comments")
        names = [i.filename for i in self.infos] + [n for n in self.dirty if n not in self.data]
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for n in names:
                if n in self.dirty:
                    blob = etree.tostring(self.dirty[n], xml_declaration=True, encoding="UTF-8", standalone=True)
                else:
                    blob = self.data[n]
                z.writestr(n, blob)
        os.replace(tmp, out)


def text_of(el, tag="a:t"):
    para = q("a:p") if tag == "a:t" else q("w:p")
    paras = [p for p in el.iter(para)] or [el]
    return "\n".join("".join(t.text or "" for t in p.iter(q(tag))) for p in paras)


def now_iso(ms=True):
    t = dt.datetime.now()
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}" if ms else t.strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- pptx
def pptx_slides(pkg):
    _, rels = pkg.rels("ppt/presentation.xml")
    by_id = {rid: full for rid, t, full, _ in rels if t == REL_SLIDE}
    pres = pkg.peek("ppt/presentation.xml")
    out = []
    lst = pres.find(q("p:sldIdLst"))
    for i, s in enumerate(lst if lst is not None else [], 1):
        out.append((i, by_id[s.get(q("r:id"))]))
    return out


def pptx_authors(pkg):
    names = {}
    if pkg.has("ppt/authors.xml"):
        for a in pkg.peek("ppt/authors.xml"):
            names[a.get("id")] = a.get("name")
    if pkg.has("ppt/commentAuthors.xml"):
        for a in pkg.peek("ppt/commentAuthors.xml"):
            names["legacy:" + a.get("id")] = a.get("name")
    return names


def shape_text(slide_root, sp_id):
    if not sp_id:
        return ""
    for c in slide_root.iter(q("p:cNvPr")):
        if c.get("id") == sp_id:
            return text_of(c.getparent().getparent())
    return ""


def pptx_list(pkg):
    authors = pptx_authors(pkg)
    out = []
    for num, slide in pptx_slides(pkg):
        _, rels = pkg.rels(slide)
        sroot = pkg.peek(slide)
        title = ""
        for sp in sroot.iter(q("p:sp")):
            ph = sp.find(".//" + q("p:ph"))
            if ph is not None and ph.get("type") in ("title", "ctrTitle"):
                title = text_of(sp); break
        for _, t, full, _ in rels:
            if t == REL_MODERN_COMMENTS:
                for cm in pkg.peek(full).findall(q("p188:cm")):
                    sp = cm.find(".//" + q("ac:spMk"))
                    sp_id = sp.get("id") if sp is not None else None
                    anchor = shape_text(sroot, sp_id)
                    tx = cm.find(".//" + q("ac:txMk"))
                    if tx is not None and anchor:
                        cp, ln = int(tx.get("cp", 0)), int(tx.get("len", 0))
                        anchor = anchor[cp:cp + ln] or anchor
                    out.append({
                        "id": cm.get("id"), "format": "pptx-modern", "slide": num, "slide_title": title,
                        "author": authors.get(cm.get("authorId"), cm.get("authorId")),
                        "created": cm.get("created"), "status": cm.get("status", "active"),
                        "anchor_shape_id": sp_id, "anchor_text": anchor[:300],
                        "text": text_of(cm.find(q("p188:txBody"))),
                        "replies": [{"author": authors.get(r.get("authorId"), r.get("authorId")),
                                     "created": r.get("created"), "text": text_of(r)}
                                    for r in cm.iter(q("p188:reply"))],
                        "_part": full,
                    })
            elif t == REL_LEGACY_COMMENTS:
                cms = pkg.peek(full).findall(q("p:cm"))
                children = {}
                for cm in cms:
                    par = cm.find(".//" + q("p15:parentCm"))
                    if par is not None:
                        children.setdefault(f"{par.get('authorId')}-{par.get('idx')}", []).append(cm)
                for cm in cms:
                    if cm.find(".//" + q("p15:parentCm")) is not None:
                        continue
                    cid = f"{cm.get('authorId')}-{cm.get('idx')}"
                    out.append({
                        "id": cid, "format": "pptx-legacy", "slide": num, "slide_title": title,
                        "author": authors.get("legacy:" + cm.get("authorId")), "created": cm.get("dt"),
                        "status": "active", "anchor_shape_id": None, "anchor_text": "",
                        "text": "".join(x.text or "" for x in cm.iter(q("p:text"))),
                        "replies": [{"author": authors.get("legacy:" + c.get("authorId")), "created": c.get("dt"),
                                     "text": "".join(x.text or "" for x in c.iter(q("p:text")))}
                                    for c in children.get(cid, [])],
                        "_part": full,
                    })
    return out


def pptx_modern_author(pkg, name, initials):
    if not pkg.has("ppt/authors.xml"):
        pkg.dirty["ppt/authors.xml"] = etree.fromstring(
            ('<p188:authorLst xmlns:a="%s" xmlns:r="%s" xmlns:p188="%s"/>' % (NS["a"], NS["r"], NS["p188"])).encode())
        pkg.add_rel("ppt/presentation.xml", REL_AUTHORS, "authors.xml")
        pkg.add_override("/ppt/authors.xml", "application/vnd.ms-powerpoint.authors+xml")
    root = pkg.xml("ppt/authors.xml")
    for a in root:
        if a.get("name") == name:
            return a.get("id")
    aid = "{%s}" % str(uuid.uuid4()).upper()
    el = etree.SubElement(root, q("p188:author"))
    for k, v in (("id", aid), ("name", name), ("initials", initials), ("userId", name), ("providerId", "None")):
        el.set(k, v)
    return aid


def pptx_legacy_author(pkg, name, initials):
    root = pkg.xml("ppt/commentAuthors.xml")
    for a in root:
        if a.get("name") == name:
            return a
    nid = max([int(a.get("id")) for a in root] + [-1]) + 1
    el = etree.SubElement(root, q("p:cmAuthor"))
    for k, v in (("id", str(nid)), ("name", name), ("initials", initials), ("lastIdx", "0"), ("clrIdx", str(nid % 8))):
        el.set(k, v)
    return el


def pptx_reply(pkg, comments, replies, author, initials):
    by_id = {c["id"]: c for c in comments}
    for rep in replies:
        c = by_id.get(rep["id"])
        if c is None:
            raise SystemExit(f"Unknown comment id: {rep['id']}")
        part = pkg.xml(c["_part"])
        if c["format"] == "pptx-modern":
            aid = pptx_modern_author(pkg, author, initials)
            cm = next(x for x in part.findall(q("p188:cm")) if x.get("id") == c["id"])
            lst = cm.find(q("p188:replyLst"))
            if lst is None:
                lst = etree.Element(q("p188:replyLst"))
                cm.find(q("p188:txBody")).addprevious(lst)
            r = etree.SubElement(lst, q("p188:reply"))
            r.set("id", "{%s}" % str(uuid.uuid4()).upper()); r.set("authorId", aid); r.set("created", now_iso())
            body = etree.SubElement(r, q("p188:txBody"))
            etree.SubElement(body, q("a:bodyPr")); etree.SubElement(body, q("a:lstStyle"))
            for line in rep["text"].split("\n"):
                p = etree.SubElement(body, q("a:p")); run = etree.SubElement(p, q("a:r"))
                etree.SubElement(run, q("a:rPr")).set("lang", "en-US")
                etree.SubElement(run, q("a:t")).text = line
        else:
            a = pptx_legacy_author(pkg, author, initials)
            idx = int(a.get("lastIdx")) + 1
            a.set("lastIdx", str(idx))
            pa, pidx = c["id"].split("-")
            parent = next(x for x in part.findall(q("p:cm")) if x.get("authorId") == pa and x.get("idx") == pidx)
            cm = etree.SubElement(part, q("p:cm"))
            cm.set("authorId", a.get("id")); cm.set("dt", now_iso()); cm.set("idx", str(idx))
            pos = parent.find(q("p:pos"))
            cm.append(copy.deepcopy(pos) if pos is not None else etree.Element(q("p:pos"), x="10", y="10"))
            etree.SubElement(cm, q("p:text")).text = rep["text"]
            ext = etree.SubElement(etree.SubElement(cm, q("p:extLst")), q("p:ext")); ext.set("uri", THREADING_URI)
            ti = etree.SubElement(ext, q("p15:threadingInfo")); ti.set("timeZoneBias", "0")
            pc = etree.SubElement(ti, q("p15:parentCm")); pc.set("authorId", pa); pc.set("idx", pidx)


# ---------------------------------------------------------------- docx
def docx_list(pkg):
    if not pkg.has("word/comments.xml"):
        return []
    croot = pkg.peek("word/comments.xml")
    ex = {}
    if pkg.has("word/commentsExtended.xml"):
        for e in pkg.peek("word/commentsExtended.xml"):
            ex[e.get(q("w15:paraId"))] = e
    # anchor text
    doc = pkg.peek("word/document.xml")
    open_ids, anchors = set(), {}
    for el in doc.iter():
        if el.tag == q("w:commentRangeStart"):
            open_ids.add(el.get(q("w:id")))
        elif el.tag == q("w:commentRangeEnd"):
            open_ids.discard(el.get(q("w:id")))
        elif el.tag == q("w:t") and open_ids:
            for i in open_ids:
                anchors[i] = anchors.get(i, "") + (el.text or "")
    raw, para_to_id = [], {}
    for c in croot.findall(q("w:comment")):
        ps = c.findall(q("w:p"))
        last = ps[-1].get(q("w14:paraId")) if ps else None
        para_to_id[last] = c.get(q("w:id"))
        e = ex.get(last)
        raw.append((c, last, e))
    out, by = [], {}
    for c, last, e in raw:
        parent = e.get(q("w15:paraIdParent")) if e is not None else None
        item = {"id": c.get(q("w:id")), "author": c.get(q("w:author")), "created": c.get(q("w:date")),
                "text": "\n".join(text_of(p, "w:t") for p in c.findall(q("w:p")))}
        if parent and parent in para_to_id:
            by.setdefault(para_to_id[parent], []).append(item)
            continue
        item.update({"format": "docx", "status": "resolved" if e is not None and e.get(q("w15:done")) == "1" else "active",
                     "anchor_text": anchors.get(item["id"], "")[:300], "_para": last})
        out.append(item)
    for o in out:
        o["replies"] = [{k: r[k] for k in ("author", "created", "text")} for r in by.get(o["id"], [])]
    return out


def para_id():
    return "%08X" % random.randint(0x10000000, 0x7FFFFFFE)


def docx_reply(pkg, comments, replies, author, initials):
    by_id = {c["id"]: c for c in comments}
    croot = pkg.xml("word/comments.xml")
    if not pkg.has("word/commentsExtended.xml"):
        pkg.dirty["word/commentsExtended.xml"] = etree.fromstring(
            ('<w15:commentsEx xmlns:w15="%s" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"/>' % NS["w15"]).encode())
        pkg.add_rel("word/document.xml", REL_W_COMMENTS_EX, "commentsExtended.xml")
        pkg.add_override("/word/commentsExtended.xml",
                         "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtended+xml")
    exroot = pkg.xml("word/commentsExtended.xml")
    known = {e.get(q("w15:paraId")) for e in exroot}
    for c in croot.findall(q("w:comment")):  # make sure parents are registered in commentsEx
        ps = c.findall(q("w:p"))
        pid = ps[-1].get(q("w14:paraId")) if ps else None
        if ps and pid is None:
            pid = para_id(); ps[-1].set(q("w14:paraId"), pid)
        if pid and pid not in known:
            e = etree.SubElement(exroot, q("w15:commentEx")); e.set(q("w15:paraId"), pid); e.set(q("w15:done"), "0")
            known.add(pid)
            if c.get(q("w:id")) in by_id:
                by_id[c.get(q("w:id"))]["_para"] = pid
    doc = pkg.xml("word/document.xml")
    next_id = max([int(c.get(q("w:id"))) for c in croot.findall(q("w:comment"))] + [-1]) + 1
    for rep in replies:
        c = by_id.get(str(rep["id"]))
        if c is None:
            raise SystemExit(f"Unknown comment id: {rep['id']}")
        nid, pid = str(next_id), para_id(); next_id += 1
        cm = etree.SubElement(croot, q("w:comment"))
        cm.set(q("w:id"), nid); cm.set(q("w:author"), author); cm.set(q("w:date"), now_iso(False)); cm.set(q("w:initials"), initials)
        lines = rep["text"].split("\n")
        for i, line in enumerate(lines):
            p = etree.SubElement(cm, q("w:p"))
            if i == len(lines) - 1:
                p.set(q("w14:paraId"), pid); p.set(q("w14:textId"), "77777777")
            etree.SubElement(etree.SubElement(p, q("w:pPr")), q("w:pStyle")).set(q("w:val"), "CommentText")
            if i == 0:
                r0 = etree.SubElement(p, q("w:r"))
                etree.SubElement(etree.SubElement(r0, q("w:rPr")), q("w:rStyle")).set(q("w:val"), "CommentReference")
                etree.SubElement(r0, q("w:annotationRef"))
            t = etree.SubElement(etree.SubElement(p, q("w:r")), q("w:t")); t.text = line
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        e = etree.SubElement(exroot, q("w15:commentEx"))
        e.set(q("w15:paraId"), pid); e.set(q("w15:paraIdParent"), c["_para"]); e.set(q("w15:done"), "0")
        durable = "%08X" % random.randint(0x10000000, 0x7FFFFFFE)
        if pkg.has("word/commentsIds.xml"):
            x = etree.SubElement(pkg.xml("word/commentsIds.xml"), q("w16cid:commentId"))
            x.set(q("w16cid:paraId"), pid); x.set(q("w16cid:durableId"), durable)
        if pkg.has("word/commentsExtensible.xml"):
            x = etree.SubElement(pkg.xml("word/commentsExtensible.xml"), q("w16cex:commentExtensible"))
            x.set(q("w16cex:durableId"), durable); x.set(q("w16cex:dateUtc"), dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        # anchor the reply on the same range as the parent
        for tag in ("w:commentRangeStart", "w:commentRangeEnd"):
            for el in doc.iter(q(tag)):
                if el.get(q("w:id")) == c["id"]:
                    new = etree.Element(q(tag)); new.set(q("w:id"), nid); el.addnext(new); break
        for el in doc.iter(q("w:commentReference")):
            if el.get(q("w:id")) == c["id"]:
                run = el.getparent()
                nr = etree.Element(q("w:r"))
                etree.SubElement(etree.SubElement(nr, q("w:rPr")), q("w:rStyle")).set(q("w:val"), "CommentReference")
                etree.SubElement(nr, q("w:commentReference")).set(q("w:id"), nid)
                run.addnext(nr); break


# ---------------------------------------------------------------- commands
def load(path):
    pkg = Package(path)
    ext = Path(path).suffix.lower()
    if ext == ".pptx":
        return pkg, pptx_list(pkg), pptx_reply
    if ext == ".docx":
        return pkg, docx_list(pkg), docx_reply
    raise SystemExit(f"Unsupported file type: {ext} (supports .pptx, .docx)")


def public(c):
    return {k: v for k, v in c.items() if not k.startswith("_")}


def cmd_list(a):
    _, comments, _ = load(a.file)
    shown = comments if a.all else [c for c in comments if c["status"] != "resolved"]
    if a.json:
        Path(a.json).write_text(json.dumps([public(c) for c in comments], indent=2, ensure_ascii=False), encoding="utf-8")
    res = sum(c["status"] == "resolved" for c in comments)
    print(f"{len(comments)} comment threads ({len(comments) - res} open, {res} resolved){'' if a.all else ' - showing open only'}\n")
    for c in shown:
        loc = f"slide {c['slide']}" + (f" ({c['slide_title'][:50]})" if c.get("slide_title") else "") if "slide" in c else "doc"
        print(f"[{c['id']}] {loc} | {c['author']} | {c['status']}")
        if c.get("anchor_text"):
            print(f"   on: \"{c['anchor_text'][:160]}\"")
        print(f"   >> {c['text']}")
        for r in c["replies"]:
            print(f"      reply ({r['author']}): {r['text']}")
        print()


def cmd_backup(a):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    p = Path(a.file)
    dst = BACKUP_DIR / f"{p.stem}__{dt.datetime.now():%Y%m%d-%H%M%S}{p.suffix}"
    shutil.copy2(p, dst)
    print(dst)


def thread_key(c):
    return {"status": c["status"], "text": c["text"], "replies": [r["text"] for r in c["replies"]]}


def cmd_snapshot(a):
    _, comments, _ = load(a.file)
    Path(a.snapshot).write_text(json.dumps({c["id"]: thread_key(c) for c in comments}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Snapshot of {len(comments)} threads -> {a.snapshot}")


def cmd_verify(a):
    _, comments, _ = load(a.file)
    snap = json.loads(Path(a.snapshot).read_text(encoding="utf-8"))
    now = {c["id"]: thread_key(c) for c in comments}
    problems = []
    for cid, before in snap.items():
        after = now.get(cid)
        if after is None:
            problems.append(f"MISSING thread {cid} ({before['status']}): {before['text'][:80]}"); continue
        if after["status"] != before["status"]:
            problems.append(f"STATUS CHANGED {cid}: {before['status']} -> {after['status']}")
        if after["text"] != before["text"]:
            problems.append(f"TEXT CHANGED {cid}")
        if after["replies"][:len(before["replies"])] != before["replies"]:
            problems.append(f"REPLIES ALTERED {cid}")
    if problems:
        print("FAIL\n" + "\n".join(problems)); sys.exit(1)
    added = sum(len(now[c]["replies"]) - len(snap[c]["replies"]) for c in snap)
    print(f"OK - all {len(snap)} threads intact (incl. resolved); {added} new replies")


def cmd_reply(a):
    pkg, comments, fn = load(a.file)
    replies = json.loads(Path(a.replies).read_text(encoding="utf-8"))
    fn(pkg, comments, replies, a.author, a.initials)
    pkg.save()
    print(f"Added {len(replies)} replies to {a.file}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("file"); s.add_argument("--json"); s.add_argument("--all", action="store_true"); s.set_defaults(f=cmd_list)
    s = sub.add_parser("backup"); s.add_argument("file"); s.set_defaults(f=cmd_backup)
    s = sub.add_parser("snapshot"); s.add_argument("file"); s.add_argument("snapshot"); s.set_defaults(f=cmd_snapshot)
    s = sub.add_parser("verify"); s.add_argument("file"); s.add_argument("snapshot"); s.set_defaults(f=cmd_verify)
    s = sub.add_parser("reply"); s.add_argument("file"); s.add_argument("replies")
    s.add_argument("--author", default="Claude"); s.add_argument("--initials", default="AI"); s.set_defaults(f=cmd_reply)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    a.f(a)


if __name__ == "__main__":
    main()
