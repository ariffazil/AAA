#!/usr/bin/env python3
"""store-resolution-probe.py — the three questions a skill-store audit must answer.

1 INVENTORY  what is on disk (symlink-aware, realpath-deduped; namespaces vs shells)
2 OWNERSHIP  which links point OUT of the canonical tree (second writers)
3 RESOLUTION does every name a CONSUMER declares actually resolve in ITS OWN store

Read-only: nothing is moved, linked, or written. Run this BEFORE claiming a store is broken,
and again after any repair to prove the count actually moved.

Usage:
    python3 store-resolution-probe.py --root /root/AAA/skills
    python3 store-resolution-probe.py --root /root/AAA/skills \
        --store canonical=/root/AAA/skills \
        --store hermes=/root/.hermes/skills \
        --consumer /root/.claude/agents --field skills
"""
import argparse
import json
import os
import re
import sys


def index(root):
    """basename -> realpath, and frontmatter-name -> realpath. Symlinks followed, deduped."""
    by_dir, by_name = {}, {}
    if not os.path.isdir(root):
        return by_dir, by_name
    try:
        import yaml
    except ImportError:
        yaml = None
    seen = set()
    for dp, _, fn in os.walk(root, followlinks=True):
        if "SKILL.md" not in fn:
            continue
        rp = os.path.realpath(dp)
        if rp in seen:
            continue
        seen.add(rp)
        by_dir.setdefault(os.path.basename(dp), rp)
        if yaml:
            try:
                t = open(os.path.join(dp, "SKILL.md"), encoding="utf-8", errors="replace").read()
                m = re.match(r"^---\n(.*?)\n---", t, re.S)
                if m:
                    fm = yaml.safe_load(m.group(1)) or {}
                    if isinstance(fm, dict) and fm.get("name"):
                        by_name.setdefault(str(fm["name"]).strip(), rp)
            except Exception:
                pass
    return by_dir, by_name


def resolves(name, store):
    by_dir, by_name = store
    return by_dir.get(name) or by_name.get(name)


def q1_inventory(root):
    """Namespaces vs shells. A dir is a SHELL only if nothing beneath it has a SKILL.md."""
    seen = set()
    for dp, _, fn in os.walk(root, followlinks=True):
        if "SKILL.md" in fn:
            seen.add(os.path.realpath(dp))
    own, namespaces, empty = [], [], []
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d)
        if not os.path.isdir(p) or d.startswith("."):
            continue
        if os.path.exists(os.path.join(p, "SKILL.md")):
            own.append(d)
            continue
        nested = sum(1 for _, _, fn in os.walk(p, followlinks=True) if "SKILL.md" in fn)
        (namespaces.append((d, nested)) if nested else empty.append(d))
    return {"skills_reachable": len(seen), "dirs_that_are_skills": len(own),
            "namespaces": len(namespaces), "skills_under_namespaces": sum(n for _, n in namespaces),
            "truly_empty": len(empty), "truly_empty_list": empty,
            "first_namespaces": namespaces[:10]}


def q2_ownership(root):
    """Links whose realpath leaves the canonical tree = second writers."""
    real_root = os.path.realpath(root)
    out = []
    for dp, dns, fns in os.walk(root, followlinks=False):
        for n in list(dns) + list(fns):
            p = os.path.join(dp, n)
            if not os.path.islink(p):
                continue
            t = os.path.realpath(p)
            if not t.startswith(real_root + os.sep):
                out.append({"path": p.replace(root + "/", ""), "points_to": t})
    return {"outward_symlinks": len(out), "detail": out}


def q3_resolution(consumers, stores, field):
    """Every declared name must resolve in the store that consumer loads."""
    try:
        import yaml
    except ImportError:
        return "pyyaml required for q3"
    rows = []
    for cons in consumers:
        files = ([os.path.join(cons, f) for f in sorted(os.listdir(cons)) if f.endswith(".md")]
                 if os.path.isdir(cons) else [cons])
        for f in files:
            try:
                t = open(f, encoding="utf-8").read()
            except Exception:
                continue
            fm = yaml.safe_load(t.split("---")[1]) if t.startswith("---") else {}
            names = (fm or {}).get(field) or []
            if isinstance(names, str):
                names = [names]
            if not names:
                continue
            rows.append({
                "consumer": os.path.basename(f), "declared": len(names),
                "per_store": {k: sum(1 for n in names if resolves(n, s)) for k, s in stores.items()},
                "dead_in_all": [n for n in names if not any(resolves(n, s) for s in stores.values())],
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/root/AAA/skills")
    ap.add_argument("--store", action="append", default=None, help="label=/path (repeatable)")
    ap.add_argument("--consumer", action="append", default=[],
                    help="dir of *.md declarations, or a single file")
    ap.add_argument("--field", default="skills", help="YAML field holding the name list")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    stores = {}
    for spec in (a.store or [f"canonical={a.root}"]):
        lbl, _, p = spec.partition("=")
        stores[lbl] = index(p)

    report = {"root": a.root,
              "q1_inventory": q1_inventory(a.root),
              "q2_ownership": q2_ownership(a.root),
              "q3_resolution": q3_resolution(a.consumer, stores, a.field) if a.consumer
                               else "no --consumer given"}

    if a.json:
        print(json.dumps(report, indent=1))
        return 0

    q1, q2 = report["q1_inventory"], report["q2_ownership"]
    print(f"Q1 INVENTORY  {a.root}")
    print(f"   reachable skills (links followed, deduped)  {q1['skills_reachable']}")
    print(f"   dirs that ARE skills                        {q1['dirs_that_are_skills']}")
    print(f"   NAMESPACE dirs (hold skills, are not one)   {q1['namespaces']}"
          f"  -> {q1['skills_under_namespaces']} skills inside")
    print(f"   TRULY empty (no SKILL.md at any depth)      {q1['truly_empty']}"
          f"  {q1['truly_empty_list']}")
    print(f"Q2 OWNERSHIP  outward symlinks (second writers): {q2['outward_symlinks']}")
    for d in q2["detail"][:10]:
        print(f"   {d['path']} -> {d['points_to']}")
    print("Q3 RESOLUTION")
    q3 = report["q3_resolution"]
    if isinstance(q3, str):
        print("   " + q3)
    else:
        for r in q3:
            print(f"   {r['consumer']:28s} declared {r['declared']:3d}  {r['per_store']}"
                  f"  DEAD-IN-ALL {len(r['dead_in_all'])}")
            for n in r["dead_in_all"]:
                print(f"        GONE {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
