#!/usr/bin/env python3
"""Repair dangling skill symlinks across every harness tree after the namespace collapse.
Rule: a dangling link whose NAME resolves to a live canonical skill is repointed; otherwise removed.
Every action is written to LEDGER-fix.json (reverse operation included)."""
import os, json, sys

CANON = "/root/AAA/skills"
APPLY = "--apply" in sys.argv
LEDGER = "/root/AAA/skills-retired/2026-09-19-namespace-collapse/LEDGER-alias-repair.json"
EXCL = {'.git', '__pycache__', 'node_modules', '.venv'}

TREES = [CANON,
         "/root/.hermes/skills", "/root/.agents/skills", "/root/.claude/skills",
         "/root/.codex/skills", "/root/.qwen/skills", "/root/.kimi-code/skills",
         "/root/.config/opencode/skills", "/root/.gemini/skills", "/root/.continue/skills"]
TREES += [p for p in sys.argv[1:] if not p.startswith("--")]

# canonical skill name -> abspath (name = folder name, plus id: from frontmatter)
byname = {}
for dp, dn, fn in os.walk(CANON):
    if "/." in dp.replace(CANON, ""):
        continue
    if "SKILL.md" in fn:
        nm = os.path.basename(dp)
        byname.setdefault(nm.lower(), []).append(dp)
print("canonical names indexed:", len(byname))

plan = []
for root in TREES:
    if not os.path.isdir(root):
        continue
    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = [d for d in dn if d not in EXCL]
        for n in list(dn) + list(fn):
            p = os.path.join(dp, n)
            if os.path.islink(p) and not os.path.exists(p):
                tgt = os.readlink(p)
                cand = byname.get(n.lower(), [])
                if any(x[0] == p for x in plan):
                    continue
                plan.append((p, tgt, cand))

print("dangling links found:", len(plan))
for p, t, c in plan:
    print(f"  {p}\n      -> {t}   [{len(c)} resolution candidate(s)]")

if not APPLY:
    print("DRY RUN — pass --apply")
    raise SystemExit(0)

os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
led = []
for p, t, c in plan:
    if len(c) == 1:
        os.unlink(p)
        os.symlink(c[0], p)
        act, new = "repointed", c[0]
        print("repointed", p, "->", c[0])
    else:
        os.unlink(p)
        act, new = "removed", None
        print("removed  ", p, ("(ambiguous: %s)" % c) if c else "(no live skill by that name)")
    led.append({"path": p, "was": t, "action": act, "now": new,
                "undo": ("ln -sfn %s %s" % (t, p)) if act == "repointed" else ("ln -s %s %s" % (t, p))})
json.dump(led, open(LEDGER, "w"), indent=2)
print("ledger:", LEDGER)
