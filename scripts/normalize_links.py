#!/usr/bin/env python3
"""
normalize_links.py  -  Fix broken Obsidian wikilinks for Quartz publishing.

Quartz's "shortest" link resolution turns [[Note]] into a working link ONLY when
exactly one page has that basename. When a tag page shares the name, or the note
name is duplicated across folders, the link falls back to a root slug (/note) and
404s. This script rewrites only those *broken* basename links to the exact page
slug (with a display alias so the visible text is unchanged), leaving working
links and links to not-yet-written notes untouched.

Runs on the content/ COPY only; the source vault is never touched.
Usage:
    python normalize_links.py <content_dir> [--write] [--public <dir>]
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
    out = "/".join(slug_seg(x) for x in p.split("/"))
    return out.rstrip("/")

def rel_no_ext(root, path):
    r = os.path.relpath(path, root).replace("\\", "/")
    return r[:-3] if r.lower().endswith(".md") else r

def is_ignored(relparts):
    return any(part in IGNORE_DIRS for part in relparts)

def collect(content):
    notes = {}          # pageslug -> original relpath (no ext)
    folderslugs = set()
    tagnames = set()     # leaf tag slugs
    md_files = []
    for dirpath, dirnames, filenames in os.walk(content):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for fn in filenames:
            if not fn.lower().endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            rel = rel_no_ext(content, full)
            parts = rel.split("/")
            if is_ignored(parts):
                continue
            md_files.append((full, rel))
            # folder-note merge: file name == parent folder name
            if len(parts) >= 2 and parts[-1] == parts[-2]:
                pageslug = slugify("/".join(parts[:-1]))
            elif len(parts) == 1 and parts[0] == "index":
                pageslug = ""   # homepage
            else:
                pageslug = slugify(rel)
            notes[pageslug] = rel
            # every ancestor directory becomes a folder page
            for i in range(1, len(parts)):
                folderslugs.add(slugify("/".join(parts[:i])))
            # tags from this file
            tagnames.update(extract_tags(full))
    return notes, folderslugs, tagnames, md_files

FM_RE = re.compile(r"^\s*---\r?\n(.*?)\r?\n---", re.S)
def extract_tags(path):
    tags = set()
    try:
        txt = io.open(path, encoding="utf-8").read()
    except Exception:
        return tags
    m = FM_RE.match(txt)
    if m:
        fm = m.group(1)
        # inline list:  tags: [a, b]
        for mm in re.finditer(r"^\s*tags:\s*\[(.*?)\]", fm, re.M):
            for t in mm.group(1).split(","):
                t = t.strip().strip("'\"")
                if t:
                    tags.add(slugify(t).split("/")[-1])
        # block list:   tags:\n  - a
        bm = re.search(r"^\s*tags:\s*\n((?:\s*-\s*.+\n?)+)", fm, re.M)
        if bm:
            for line in bm.group(1).splitlines():
                t = line.strip().lstrip("-").strip().strip("'\"")
                if t:
                    tags.add(slugify(t).split("/")[-1])
    # inline #tags (strip fenced code first)
    body = txt[m.end():] if m else txt
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    for mm in re.finditer(r"(?:^|\s)#([A-Za-z0-9_][\w/-]*)", body):
        tags.add(slugify(mm.group(1)).split("/")[-1])
    return tags

WIKILINK = re.compile(r"(!?)\[\[([^\]]+?)\]\]")

def process_file(full, rel, notes, pageslugset, basename_count, src_slug, write):
    txt = io.open(full, encoding="utf-8").read()
    changes = []

    def repl(mobj):
        bang, inner = mobj.group(1), mobj.group(2)
        # split display alias
        if "|" in inner:
            target, display = inner.split("|", 1)
        else:
            target, display = inner, None
        # split anchor
        if "#" in target:
            tpath, anchor = target.split("#", 1)
        else:
            tpath, anchor = target, None
        tpath = tpath.strip()
        if tpath == "":
            return mobj.group(0)            # same-page anchor
        slugt = slugify(tpath)
        last = slugt.split("/")[-1]
        # already a path with a slash that resolves uniquely -> leave
        if "/" in slugt:
            matches = [s for s in pageslugset if s == slugt or s.endswith("/" + slugt)]
            if len(matches) == 1:
                return mobj.group(0)
            return mobj.group(0)            # ambiguous path: leave, too rare
        # basename link
        matches = [s for s in pageslugset if s.split("/")[-1] == last]
        if len(matches) == 1:
            return mobj.group(0)            # Quartz resolves it fine
        nontag = [s for s in matches if not s.startswith("tags/")]
        if not nontag:
            return mobj.group(0)            # only tags / none -> leave (missing)
        # choose best: same top-level section as source, else shortest path
        def score(s):
            a = s.split("/"); b = src_slug.split("/")
            common = 0
            for x, y in zip(a, b):
                if x == y:
                    common += 1
                else:
                    break
            return (common, -len(a))
        chosen = sorted(nontag, key=score, reverse=True)[0]
        disp = display if display is not None else (tpath.split("/")[-1])
        newtarget = chosen + ("#" + anchor if anchor else "")
        newlink = f"{bang}[[{newtarget}|{disp}]]"
        changes.append((mobj.group(0), newlink, "ambiguous" if len(nontag) > 1 else "tag-collision"))
        return newlink

    newtxt = WIKILINK.sub(repl, txt)
    if write and newtxt != txt:
        with io.open(full, "w", encoding="utf-8", newline="") as f:
            f.write(newtxt)
    return changes

def main():
    if len(sys.argv) < 2:
        print("usage: normalize_links.py <content_dir> [--write] [--public <dir>]")
        sys.exit(2)
    content = sys.argv[1]
    write = "--write" in sys.argv
    public = None
    if "--public" in sys.argv:
        public = sys.argv[sys.argv.index("--public") + 1]

    notes, folderslugs, tagnames, md_files = collect(content)
    pageslugset = set(notes.keys()) | set(folderslugs) | {("tags/" + t) for t in tagnames}
    basename_count = {}
    for s in pageslugset:
        basename_count[s.split("/")[-1]] = basename_count.get(s.split("/")[-1], 0) + 1

    # sanity check vs built site
    if public and os.path.isdir(public):
        real = set()
        for dp, dn, fns in os.walk(public):
            for fn in fns:
                if fn.endswith(".html"):
                    r = os.path.relpath(os.path.join(dp, fn), public).replace("\\", "/")[:-5]
                    if r.endswith("/index"):
                        r = r[:-6]
                    if r in ("404", "index"):
                        r = "" if r == "index" else r
                    if r.startswith("tags"):
                        continue
                    real.add(r)
        mine = set(notes.keys()) | set(folderslugs)
        missing_in_mine = sorted(x for x in real if x and x not in mine)[:15]
        print(f"[verify] computed {len(mine)} note/folder slugs; built site has {len(real)}")
        if missing_in_mine:
            print("  pages in build NOT matched by my slug rule:", missing_in_mine)

    total = {"tag-collision": 0, "ambiguous": 0}
    changed_files = 0
    for full, rel in md_files:
        parts = rel.split("/")
        if parts[-1] == "index" and len(parts) == 1:
            src_slug = ""
        elif len(parts) >= 2 and parts[-1] == parts[-2]:
            src_slug = slugify("/".join(parts[:-1]))
        else:
            src_slug = slugify(rel)
        ch = process_file(full, rel, notes, pageslugset, basename_count, src_slug, write)
        if ch:
            changed_files += 1
            for old, new, kind in ch:
                total[kind] += 1
                if not write:
                    print(f"  [{kind}] {rel}:  {old}  ->  {new}")
    print(f"\n{'WROTE' if write else 'DRY-RUN'}: {sum(total.values())} link(s) fixed "
          f"(tag-collision={total['tag-collision']}, ambiguous={total['ambiguous']}) "
          f"in {changed_files} file(s).")

if __name__ == "__main__":
    main()
