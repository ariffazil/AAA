#!/usr/bin/env python3
"""
audit_skills.py — re-runnable defect auditor for the Hermes skill library.

Walks /root/.hermes/skills FOLLOWING symlinked category directories
(e.g. skills/capabilities -> /root/AAA/skills/capabilities), because the
skill catalogue resolves names through those links. Cycles are guarded by
a realpath visited-set; extra roots and excluded path prefixes are
configurable via CLI.

Defect classes
  1. DANGLING REFERENCES   SKILL.md names a file under references/ scripts/
                           templates/ assets/ that is not on disk.
                           Classified: linked | cross-skill | illustrative.
  2. DUPLICATE NAMES       same catalogue name in >1 directory.
  3. BROKEN SYMLINKS       symlink under the root whose target is missing.
  4. WEAK TRIGGERS         description whose first 57 chars carry no trigger.
  5. EMPTY / PLACEHOLDER   SKILL.md < MIN_BYTES, no frontmatter, empty
                           description, or genuine placeholder marker.

Usage:
  python3 audit_skills.py                     # human summary
  python3 audit_skills.py --json out.json     # machine-readable report
  python3 audit_skills.py --root /path        # override skills root
  python3 audit_skills.py --no-follow         # do not follow dir symlinks
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

DEFAULT_ROOT = "/root/.hermes/skills"
REF_DIRS = ("references", "scripts", "templates", "assets")
MIN_BYTES = 300

# path-like tokens: references/foo.md, scripts/bar.py, ./references/x, templates/y.yaml
PATH_RE = re.compile(
    r"(?<![\w/.-])(?:\./)?(" + "|".join(REF_DIRS) + r")/([A-Za-z0-9_@+.-]*[A-Za-z0-9_@+-])\.([A-Za-z0-9]+)"
)

# A pointer is a REAL pointer when it appears in a references/scripts listing
# line, a "see <path>" sentence, or a markdown link. It is ILLUSTRATIVE when it
# sits inside a fenced code block or a sentence describing an example command.
FENCE_RE = re.compile(r"^```")

TRIGGER_RE = re.compile(
    r"^(use when|use before|use after|use this|use for|use to|load when|load before|"
    r"invoke when|apply when|run when|read when|call when|trigger|when\b)",
    re.I,
)

# genuine placeholder markers only (word-boundary, not "placeholder" used as a
# legitimate noun in a prompt template)
PLACEHOLDER_RE = re.compile(
    r"(\bTODO\b|\bTBD\b|\bFIXME\b|not yet written|to be written|to be filled|"
    r"coming soon|placeholder content|placeholder skill|lorem ipsum|<insert[^>]*>|"
    r"PLACEHOLDER_TEXT|\[SKILL_TEMPLATE\])"
)

EXCLUDE_PREFIXES = ("/root/.hermes/profiles/",)


def frontmatter_dict(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    d = {}
    cur = None
    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:(.*)$", line)
        if m:
            cur = m.group(1).strip()
            v = m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            d[cur] = v
        elif cur and line[:1] in (" ", "\t"):
            d[cur] = (d.get(cur, "") + " " + line.strip()).strip()
    return d


def walk_skills(root, follow=True):
    """Yield (logical_dir, realpath, skill_md_path). Cycle-safe."""
    seen_dirs = set()
    results = []

    def rec(logical, real, depth):
        if depth > 8:
            return
        try:
            entries = sorted(os.listdir(logical))
        except OSError:
            return
        if "SKILL.md" in entries:
            results.append((logical, real, os.path.join(logical, "SKILL.md")))
            return  # a skill dir does not nest further skills
        for name in entries:
            if name.startswith("."):
                continue
            lp = os.path.join(logical, name)
            rp = os.path.realpath(lp)
            if not os.path.isdir(lp) and not os.path.islink(lp):
                continue
            if not os.path.isdir(lp):
                continue
            if any(rp.startswith(p) for p in EXCLUDE_PREFIXES):
                continue
            if rp in seen_dirs:
                continue
            seen_dirs.add(rp)
            rec(lp, rp, depth + 1)

    if follow:
        seen_dirs.add(os.path.realpath(root))
        rec(root, os.path.realpath(root), 0)
    else:
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            if "SKILL.md" in filenames:
                results.append((dirpath, os.path.realpath(dirpath),
                                os.path.join(dirpath, "SKILL.md")))
    return sorted(set(results))


def build_fs_index(scan_roots=("/root",)):
    """Cache {basename: [paths]} for the whole box so a skill-local pointer can
    be distinguished from a PROJECT-RELATIVE one (a file that exists, but in a
    repo rather than in the skill directory). Pruned dirs keep this fast."""
    idx = defaultdict(list)
    skip = ("/.quarantine", "/skills.backup", "/.git/", "/node_modules/",
            "/.venv/", "/venv/", "/.cache/", "/allfiles.tsv")
    for root in scan_roots:
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            if any(s in dirpath for s in skip):
                dirnames[:] = []
                continue
            for fn in filenames:
                idx[fn].append(os.path.join(dirpath, fn))
    return idx


def classify_path_token(text, idx, token, skill_dir, all_skill_dirs, fs_index=None):
    """Return ('linked'|'cross-skill'|'illustrative'|'project-relative', note)."""
    # surrounding line
    line_start = text.rfind("\n", 0, idx) + 1
    line_end = text.find("\n", idx)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end]

    # inside a fenced code block?
    fences = 0
    for l in text[:idx].splitlines():
        if FENCE_RE.match(l.strip()):
            fences += 1
    if fences % 2 == 1:
        return "illustrative", "inside fenced code block (example command)"

    # cross-skill: line names another skill and says the file lives there
    m = re.search(r"([A-Za-z0-9_-]{3,})\s+skill'?s?\s+`?" + re.escape(token), line)
    if m:
        other = m.group(1).strip("`'\"")
        for d in all_skill_dirs:
            cand = os.path.join(d, token)
            if os.path.exists(cand):
                return "cross-skill", f"resolves under skill '{other}': {cand}"
    for d in all_skill_dirs:
        if d == skill_dir:
            continue
        cand = os.path.join(d, token)
        if os.path.exists(cand):
            return "cross-skill", f"exists in another skill dir: {cand}"

    # PROJECT-RELATIVE: the basename exists somewhere on the box but not in the
    # skill dir. The token is a repo path (e.g. `scripts/deploy-site.sh` inside
    # the site repo), not a skill-linked file. Not a defect of this skill.
    if fs_index is not None:
        hits = [p for p in fs_index.get(os.path.basename(token), [])
                if not p.startswith(skill_dir.rstrip("/") + "/")]
        if hits:
            return "project-relative", (
                "basename exists outside the skill dir (repo path, not a "
                f"skill-linked file): {hits[0]}")

    # illustrative markers in the same line
    if re.search(r"\b(e\.g\.|for example|such as|real path may be|example:)\b", line, re.I):
        return "illustrative", "line reads as an example, not a pointer"

    # templated filename placeholder
    if re.search(r"(HASH|VERSION|<[^>]+>|\{\{)", token):
        return "illustrative", "templated placeholder filename"

    return "linked", "listed as a concrete file pointer"


def audit(root, follow=True, extra_roots=(), use_fs_index=True):
    report = {"root": root, "follow_symlinked_dirs": follow,
              "extra_roots": list(extra_roots),
              "fs_index_used": use_fs_index}
    triples = walk_skills(root, follow=follow)
    all_skill_dirs = [t[0] for t in triples]
    fs_index = build_fs_index() if use_fs_index else None

    entries = []
    for logical, real, path in triples:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            entries.append({"path": path, "logical_dir": logical, "real_dir": real,
                            "read_error": str(exc)})
            continue
        fm = frontmatter_dict(text)
        entries.append({
            "path": path,
            "logical_dir": logical,
            "real_dir": real,
            "dir_name": os.path.basename(logical),
            "name": fm.get("name") or os.path.basename(logical),
            "description": fm.get("description", ""),
            "size": os.path.getsize(path),
            "has_frontmatter": bool(fm),
            "text": text,
        })

    # ---------- [1] dangling references ----------
    dangling, clean_refs = [], []
    for e in entries:
        if "text" not in e:
            continue
        skill_dir = e["logical_dir"]
        missing, cross, illus, proj, ok = [], [], [], [], []
        seen = set()
        for m in PATH_RE.finditer(e["text"]):
            refdir, stem, ext = m.group(1), m.group(2), m.group(3)
            rel = f"{refdir}/{stem}.{ext}".rstrip(".,;:)`\"'")
            if rel in seen:
                continue
            seen.add(rel)
            if os.path.exists(os.path.join(skill_dir, rel)):
                ok.append(rel)
                continue
            kind, note = classify_path_token(
                e["text"], m.start(), rel, skill_dir, all_skill_dirs, fs_index)
            if kind == "cross-skill":
                cross.append({"ref": rel, "note": note})
            elif kind == "project-relative":
                proj.append({"ref": rel, "note": note})
            elif kind == "illustrative":
                illus.append({"ref": rel, "note": note})
            else:
                missing.append(rel)
        if missing or cross or illus or proj:
            dangling.append({
                "skill": e["name"],
                "skill_dir": skill_dir,
                "skill_md": e["path"],
                "missing": sorted(missing),
                "cross_skill": cross,
                "project_relative": proj,
                "illustrative": illus,
                "present": sorted(ok),
            })
        if ok:
            clean_refs.append({"skill": e["name"], "path": e["path"],
                               "present": sorted(ok)})

    # ---------- [2] duplicate names ----------
    by_name = defaultdict(list)
    for e in entries:
        by_name[e["name"]].append(e)
    duplicates = []
    for nm, group in sorted(by_name.items()):
        if len(group) > 1:
            paths = sorted(g["path"] for g in group)
            # resolution heuristic: the catalogue lists same-name skills by
            # category prefix; the entry whose directory sits shallowest under
            # the primary root wins a bare-name lookup.
            ranked = sorted(group, key=lambda g: (
                0 if g["logical_dir"].count("/") == root.count("/") + 1 else 1,
                g["logical_dir"].count("/"),
                g["logical_dir"]))
            duplicates.append({
                "name": nm,
                "count": len(group),
                "paths": paths,
                "logical_dirs": sorted(g["logical_dir"] for g in group),
                "sizes": {g["path"]: g["size"] for g in group},
                "resolves_to": ranked[0]["path"],
                "resolves_reason": "shallowest directory under the skills root "
                                   "(bare-name lookup wins over category-qualified)",
                "is_symlink_alias": len({g["real_dir"] for g in group}) == 1,
            })

    # ---------- [3] broken symlinks ----------
    broken, symlinks = [], []
    seen_links = set()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for n in list(dirnames) + list(filenames):
            p = os.path.join(dirpath, n)
            if os.path.islink(p) and p not in seen_links:
                seen_links.add(p)
                tgt = os.readlink(p)
                ok = os.path.exists(p)
                symlinks.append({"link": p, "target": tgt, "resolves": ok})
                if not ok:
                    broken.append({"link": p, "target": tgt})

    # ---------- [4] weak triggers ----------
    weak = []
    for e in entries:
        if "text" not in e:
            continue
        desc = re.sub(r"^[\s>\"'*-]+", "", (e["description"] or "")).strip()
        if TRIGGER_RE.match(desc):
            continue
        weak.append({
            "skill": e["name"],
            "path": e["path"],
            "desc_len": len(desc),
            "head57": desc[:57],
            "description": desc,
        })
    weak.sort(key=lambda w: (bool(w["description"]),
                             w["desc_len"], w["skill"].lower()))

    # ---------- [5] empty / placeholder ----------
    empty = []
    for e in entries:
        if "text" not in e:
            continue
        reasons = []
        if e["size"] < MIN_BYTES:
            reasons.append(f"size {e['size']}B < {MIN_BYTES}B")
        m = PLACEHOLDER_RE.search(e["text"])
        if m:
            reasons.append(f"placeholder marker: {m.group(0)!r}")
        if "[SKILL_PRUNED]" in e["text"]:
            reasons.append("[SKILL_PRUNED] marker (content lost to compression)")
        if not e["has_frontmatter"]:
            reasons.append("missing YAML frontmatter")
        if not (e["description"] or "").strip():
            reasons.append("empty description")
        if reasons:
            empty.append({"skill": e["name"], "path": e["path"],
                          "size": e["size"], "reasons": reasons})

    report["entries"] = [{k: v for k, v in e.items() if k != "text"} for e in entries]
    report["dangling_references"] = dangling
    report["clean_reference_skills"] = clean_refs
    report["duplicate_names"] = duplicates
    report["symlinks"] = symlinks
    report["broken_symlinks"] = broken
    report["weak_triggers"] = weak
    report["empty_or_placeholder"] = empty
    report["counts"] = {
        "skills": len(entries),
        "skills_with_dangling_refs": len([d for d in dangling if d["missing"]]),
        "dangling_ref_files": sum(len(d["missing"]) for d in dangling),
        "cross_skill_refs": sum(len(d["cross_skill"]) for d in dangling),
        "project_relative_refs": sum(len(d["project_relative"]) for d in dangling),
        "illustrative_tokens": sum(len(d["illustrative"]) for d in dangling),
        "duplicate_groups": len(duplicates),
        "duplicate_entries": sum(d["count"] for d in duplicates),
        "symlinks": len(symlinks),
        "broken_symlinks": len(broken),
        "weak_triggers": len(weak),
        "empty_or_placeholder": len(empty),
    }
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--json", default=None)
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--no-follow", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--dangling-only", action="store_true")
    args = ap.parse_args()

    rep = audit(args.root, follow=not args.no_follow)
    if args.json:
        d = os.path.dirname(os.path.abspath(args.json))
        if d:
            os.makedirs(d, exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=2)

    c = rep["counts"]
    if args.dangling_only:
        for d in rep["dangling_references"]:
            if d["missing"]:
                print(f"{d['skill']}\t{d['skill_dir']}\t{','.join(d['missing'])}")
        return 0

    print(f"=== SKILL AUDIT :: {rep['root']} (follow dir symlinks={rep['follow_symlinked_dirs']}) ===")
    print(f"skills scanned            : {c['skills']}")
    print(f"[1] dangling refs         : {c['skills_with_dangling_refs']} skills / "
          f"{c['dangling_ref_files']} missing files")
    print(f"    cross-skill           : {c['cross_skill_refs']} (not defects)")
    print(f"    project-relative      : {c['project_relative_refs']} (repo path, not a skill file)")
    print(f"    illustrative          : {c['illustrative_tokens']} (not defects)")
    print(f"[2] duplicate name groups : {c['duplicate_groups']} covering "
          f"{c['duplicate_entries']} entries")
    print(f"[3] broken symlinks       : {c['broken_symlinks']} of {c['symlinks']}")
    print(f"[4] weak triggers         : {c['weak_triggers']} of {c['skills']}")
    print(f"[5] empty/placeholder     : {c['empty_or_placeholder']}")

    if args.quiet:
        print(json.dumps(c, indent=2))
        return 0

    print("\n-- [1] DANGLING --")
    for d in rep["dangling_references"]:
        if d["missing"]:
            print(f"  {d['skill']}  ({d['skill_dir']})")
            for m in d["missing"]:
                print(f"      MISSING {m}")
    print("\n-- [2] DUPLICATES --")
    for d in rep["duplicate_names"]:
        print(f"  name={d['name']}  x{d['count']}"
              + ("  (symlink alias - same realpath)" if d["is_symlink_alias"] else ""))
        for p in d["paths"]:
            print(f"      {p}  [{d['sizes'][p]}B]")
        print(f"      -> resolves to: {d['resolves_to']}")
    print("\n-- [3] BROKEN SYMLINKS --")
    for b in rep["broken_symlinks"]:
        print(f"  {b['link']} -> {b['target']}")
    print(f"\n-- [4] WEAK TRIGGERS (worst {args.top}) --")
    for w in rep["weak_triggers"][:args.top]:
        print(f"  [{w['desc_len']:>4}] {w['skill']}: {w['description'][:88]!r}")
    print("\n-- [5] EMPTY/PLACEHOLDER --")
    for e in rep["empty_or_placeholder"]:
        print(f"  {e['size']:>6}B  {e['skill']}: {'; '.join(e['reasons'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
