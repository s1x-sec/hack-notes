#!/usr/bin/env python3
"""
normalize_links.py  -  Rewrite Obsidian wikilinks to resolve under Quartz.

Quartz's "shortest" link resolution emits a ROOT slug (e.g. /xss) whenever a
basename matches zero or several pages (a same-named tag page, a duplicated
note, or a folder-note merge). On a project subpath those root slugs 404.
This rewrites every wikilink that points to a real, existing page into that
page's exact slug (with a display alias so the visible text is unchanged).
Links to not-yet-written notes are left untouched.

Runs on the content/ COPY only; the source vault is never modified.
Usage:  python normalize_links.py <content_dir> [--write] [--public <dir>]
"""
import sys, os, re, io

IGNORE_DIRS = {"_TEMPLATES", "00 HOME", ".obsidian", ".git"}

def slug_seg(s):
    s = re.sub(r"\s", "-", s)
    s = s.replace("&", "-and-").replace("%", "-percent")
    s = s.replace("?", "").replace("#", "")
    s = re.sub(r'[<>:"|*]', "", s)
    return s.lower()

def slugify(p):
    p = p.replace("\\", "/")
    return "/".join(slug_seg(x) for x in p.split("/")).rstrip("/")

def collect(content):
    note_ps_rs = []     # (pageslug, relslug)
    pageslugs = set()
    folderslugs = set()
    md_files = []
    for dirpath, dirnames, filenames in os.walk(content):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for fn in filenames:
            if not fn.lower().endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, content).replace("\\", "/")[:-3]
            parts = rel.split("/")
            if any(p in IGNORE_DIRS for p in parts):
                continue
            md_files.append((full, rel))
            relslug = slugify(rel)
            if len(parts) >= 2 and parts[-1] == parts[-2]:      # folder-note merge
                pageslug = slugify("/".join(parts[:-1]))
            elif rel == "index":
                pageslug = ""
            else:
                pageslug = relslug
            note_ps_rs.append((pageslug, relslug))
            pageslugs.add(pageslug)
            for i in range(1, len(parts)):
                folderslugs.add(slugify("/".join(parts[:i])))
    pageset = pageslugs | folderslugs
    return note_ps_rs, folderslugs, pageset, md_files

WIKILINK = re.compile(r"(!?)\[\[([^\]]+?)\]\]")

def make_resolver(note_ps_rs, folderslugs, pageset):
    def best(cands, src_slug):
        def score(s):
            a, b, c = s.split("/"), src_slug.split("/"), 0
            for x, y in zip(a, b):
                if x == y:
                    c += 1
                else:
                    break
            return (c, -len(a))
        return sorted(cands, key=score, reverse=True)[0]

    def resolve(tpath, src_slug):
        slugt = slugify(tpath)
        if slugt == "" or slugt in pageset:
            return None                     # same-page anchor, or already canonical
        # drop relative ./ and ../ segments -> match by path tail (and still
        # rewrite, so the stored link no longer depends on relative resolution)
        segs = [s for s in slugt.split("/") if s not in (".", "..")]
        slugt = "/".join(segs)
        if slugt == "":
            return None
        cands = set()
        if "/" in slugt:
            for ps, rs in note_ps_rs:
                if rs == slugt or rs.endswith("/" + slugt) or ps == slugt or ps.endswith("/" + slugt):
                    cands.add(ps)
            for fs in folderslugs:
                if fs == slugt or fs.endswith("/" + slugt):
                    cands.add(fs)
        else:
            for ps, rs in note_ps_rs:
                if rs.split("/")[-1] == slugt or (ps and ps.split("/")[-1] == slugt):
                    cands.add(ps)
            for fs in folderslugs:
                if fs.split("/")[-1] == slugt:
                    cands.add(fs)
        cands.discard("")
        if not cands:
            return None                     # target not written yet
        chosen = best(cands, src_slug) if len(cands) > 1 else next(iter(cands))
        if "/" not in chosen:
            return None                     # root-level page already resolves
        return (chosen, len(cands) > 1)
    return resolve

def process_file(full, rel, src_slug, resolve, write):
    txt = io.open(full, encoding="utf-8").read()
    changes = []

    def repl(mobj):
        bang, inner = mobj.group(1), mobj.group(2)
        target, display = (inner.split("|", 1) + [None])[:2]
        tpath, anchor = (target.split("#", 1) + [None])[:2]
        tpath = tpath.strip()
        r = resolve(tpath, src_slug)
        if r is None:
            return mobj.group(0)
        chosen, ambiguous = r
        disp = display if display is not None else tpath.split("/")[-1]
        newtarget = chosen + ("#" + anchor if anchor else "")
        newlink = f"{bang}[[{newtarget}|{disp}]]"
        changes.append((mobj.group(0), newlink, "ambiguous" if ambiguous else "fix"))
        return newlink

    newtxt = WIKILINK.sub(repl, txt)
    if write and newtxt != txt:
        with io.open(full, "w", encoding="utf-8", newline="") as f:
            f.write(newtxt)
    return changes

def src_slug_of(rel):
    parts = rel.split("/")
    if rel == "index":
        return ""
    if len(parts) >= 2 and parts[-1] == parts[-2]:
        return slugify("/".join(parts[:-1]))
    return slugify(rel)

def main():
    if len(sys.argv) < 2:
        print("usage: normalize_links.py <content_dir> [--write] [--public <dir>]")
        sys.exit(2)
    content = sys.argv[1]
    write = "--write" in sys.argv
    note_ps_rs, folderslugs, pageset, md_files = collect(content)
    resolve = make_resolver(note_ps_rs, folderslugs, pageset)

    total = {"fix": 0, "ambiguous": 0}
    changed = 0
    for full, rel in md_files:
        ch = process_file(full, rel, src_slug_of(rel), resolve, write)
        if ch:
            changed += 1
            for old, new, kind in ch:
                total[kind] += 1
                if not write:
                    print(f"  [{kind}] {rel}:  {old} -> {new}")
    print(f"{'WROTE' if write else 'DRY-RUN'}: {sum(total.values())} link(s) rewritten "
          f"(unique={total['fix']}, ambiguous-duplicates={total['ambiguous']}) in {changed} file(s).")

if __name__ == "__main__":
    main()
