#!/usr/bin/env python3
"""Finish the view sweep for the 2026-09-19 merge pass.

Two defects remain after a merge:
  1. mirror trees still hold symlinks to RETIRED names  -> repoint to the successor
  2. file-level symlinks into a retired skill's references/ -> materialise the file so the
     referencing skill is self-contained again (content, not just a name)

Old -> new map is DERIVED from the merge LEDGERs, never hardcoded.
Writes LEDGER-view-repair.json. --apply to execute.
"""
import os, json, sys, shutil

MERGES = "/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges"
CANON = "/root/AAA/skills"
APPLY = "--apply" in sys.argv

TREES = ["/root/AAA/skills", "/root/.hermes/skills", "/root/.hermes/profiles/aaa-hermes/skills",
         "/root/.qwen/skills", "/root/.claude/skills", "/root/.codex/skills",
         "/root/.config/opencode/skills", "/root/.kimi-code/skills",
         "/root/.arifos/agents/opencode/skills", "/root/.agents/skills",
         "/root/.gemini/skills"]
EXCL = {'.git', '__pycache__', 'node_modules', '.venv'}

# ---------- build old -> new map from the LEDGERs ----------
old2new = {}
for mdir in os.listdir(MERGES):
    lp = os.path.join(MERGES, mdir, "LEDGER.json")
    if not os.path.isfile(lp):
        continue
    try:
        L = json.load(open(lp))
    except Exception:
        continue
    target = (L.get("canonical_skill") or L.get("merged_into"))
    if isinstance(target, str) and "/" in target:
        target = [x for x in target.split("/") if x][-2]
    if not isinstance(target, str):
        target = None
    if not target:
        cp = L.get("canonical_path") or ""
        parts = [x for x in cp.split("/") if x]
        target = parts[-2] if len(parts) >= 2 else None
    if not target:
        target = mdir
    entries = (L.get("merged_from") or L.get("items") or L.get("entries") or [])
    for e in entries:
        if not isinstance(e, dict):
            continue
        orig = (e.get("original_folder") or e.get("folder") or e.get("skill") or e.get("rel")
                or e.get("orig_path") or e.get("original_path") or "")
        name = os.path.basename(str(orig).rstrip("/"))
        if name and name != target:
            old2new[name] = target

# plus the Tier-1 retirements that had explicit successors
old2new.update({
    "mcp-shopping-list-2026-09": "mcp-sota-shopping-list",
    "mcp-dual-era-transport": "mcp-testing",
    "wisdom-scar-session-audit": "scar-integration",
    "sovereign-recognize": "audience-scoped-disclosure",
    "FORGE-mcp-testing": "mcp-testing",
    "cognitive-level-assertion-protocol": "claim-receipt-discipline",
    "forge-federation-manifest": "FORGE-federation-manifest",
    "RSI-federation-mesh": "rsi-federation-mesh",
    "skill-creator": "skill-creator",
})
print(f"old->new map: {len(old2new)} retired names with a live successor")

# ---------- resolve successor to a real dir ----------
byname = {}
for dp, dn, fn in os.walk(CANON):
    if "/." in dp.replace(CANON, ""):
        continue
    if "SKILL.md" in fn:
        byname.setdefault(os.path.basename(dp).lower(), []).append(dp)

def resolve(name):
    c = byname.get(name.lower(), [])
    return c[0] if len(c) == 1 else None

# ---------- walk, classify ----------
plan = []
for root in TREES:
    if not os.path.isdir(root):
        continue
    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = [d for d in dn if d not in EXCL]
        for x in list(dn) + list(fn):
            p = os.path.join(dp, x)
            if not (os.path.islink(p) and not os.path.exists(p)):
                continue
            if any(e["path"] == p for e in plan):
                continue
            tgt = os.readlink(p)
            base = os.path.basename(p)
            is_file = "." in base and not base.lower().startswith(
                ("claude", "qwen", "kimi", "opencode", "copilot", "hermes", "openclaw", "CLAUDE", "QWEN"))
            if is_file:
                # find the same-named file inside the freeze tree
                src = None
                for r2, d2, f2 in os.walk(os.path.dirname(MERGES)):
                    if base in f2 and "merges/" in os.path.join(r2, base):
                        src = os.path.join(r2, base); break
                plan.append({"path": p, "was": tgt, "kind": "file", "frozen_src": src})
            else:
                succ = old2new.get(base) or old2new.get(base.lower())
                dest = resolve(succ) if succ else None
                if not dest:
                    # a link whose target path is inside the freeze root: name retired outright
                    dest = None
                plan.append({"path": p, "was": tgt, "kind": "name", "successor": succ,
                             "dest": dest})

n_rep = sum(1 for e in plan if e.get("dest"))
n_mat = sum(1 for e in plan if e["kind"] == "file" and e.get("frozen_src"))
n_rm = len(plan) - n_rep - n_mat
print(f"dangling: {len(plan)}  | repoint-to-successor: {n_rep}  | materialise-file: {n_mat}  | remove: {n_rm}")
for e in plan:
    tag = "REPOINT" if e.get("dest") else ("MATERIALISE" if e.get("frozen_src") and e["kind"] == "file" else "REMOVE")
    print(f"  {tag:11s} {e['path']}")

if not APPLY:
    print("DRY RUN — pass --apply")
    raise SystemExit(0)

led = []
for e in plan:
    p, kind = e["path"], e["kind"]
    if kind == "file" and e.get("frozen_src"):
        os.unlink(p)
        shutil.copy2(e["frozen_src"], p)
        act, now = "materialised", p
    elif e.get("dest"):
        rel = os.path.relpath(e["dest"], os.path.dirname(p))
        os.unlink(p)
        os.symlink(rel, p)
        act, now = "repointed", e["dest"]
    else:
        os.unlink(p)
        act, now = "removed", None
    led.append({"path": p, "was": e["was"], "action": act, "now": now})

out = "/root/AAA/skills-retired/2026-09-19-namespace-collapse/LEDGER-view-repair.json"
json.dump(led, open(out, "w"), indent=2)
print("ledger:", out)

# verify: any dangling left?
left = []
for root in TREES:
    if not os.path.isdir(root):
        continue
    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = [d for d in dn if d not in EXCL]
        for x in list(dn) + list(fn):
            p = os.path.join(dp, x)
            if os.path.islink(p) and not os.path.exists(p):
                left.append(p)
print("dangling remaining:", len(left))
for l in left[:20]:
    print("  ", l)
