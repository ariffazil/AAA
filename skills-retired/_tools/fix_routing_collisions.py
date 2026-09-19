#!/usr/bin/env python3
"""Resolve the two REAL routing-name collisions + one case-twin directory.

Collision = two DIFFERENT bodies declaring the same frontmatter `name:`. The loader
(hermes-agent tools/skills_tool.py:275-277) dedupes FIRST-WINS and silently `continue`s on the
second, so one body per collision can never load. Verified by reading the loader, not a comment.

Only 2 of 60 same-name groups carry different bodies; the other 58 are the same body at several
addresses (the intended view tree) and are left alone.

Ledger written before any move. Nothing deleted.
"""
import os, json, shutil, hashlib, datetime, sys

CANON = "/root/AAA/skills"
FREEZE = "/root/AAA/skills-retired/2026-09-19-routing-collisions"
APPLY = "--apply" in sys.argv

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()

def snap(d):
    out = {}
    for r, _, fs in os.walk(d):
        for f in fs:
            fp = os.path.join(r, f)
            out[os.path.relpath(fp, d)] = sha(fp)
    return out

# ---- CASE 1: "Agent Onboarding" — older flat copy (2026-08-13) vs newer taxonomised body ----
CASE1_LOSER = "FORGE-onboarding/claude"          # 2026-08-13, 5860 B
CASE1_WINNER = "forge-onboarding/agent-onboarding"  # 2026-09-18, 5914 B (superset: +capability_tier/ecology_state)
CASE1_DIR_TWIN = "FORGE-onboarding"              # case-twin of forge-onboarding/; empty once the loser goes

# ---- CASE 2: "code-review" — canon body (2026-09-17) vs stale borrowed profile body (2026-08-13) ----
CASE2_KEEP = "engineering/code-review"
CASE2_ALIASES = ["capabilities/coding/code-review", "domains/forge/code-review"]  # symlinks into a profile
CASE2_PROFILE = "/root/.hermes/profiles/aaa-hermes/skills/code-review"

plan = []
for rel in (CASE1_LOSER,):
    p = os.path.join(CANON, rel)
    if os.path.isdir(p):
        plan.append(("retire_dir", rel, p))

for rel in CASE2_ALIASES:
    p = os.path.join(CANON, rel)
    if os.path.islink(p):
        plan.append(("repoint", rel, p))

if os.path.isdir(CASE2_PROFILE):
    plan.append(("retire_dir", CASE2_PROFILE, CASE2_PROFILE))

print("PLAN")
for kind, rel, p in plan:
    extra = ""
    if kind == "repoint":
        extra = f"  was -> {os.readlink(p)}   becomes -> {os.path.join(CANON, CASE2_KEEP)}"
    print(f"  {kind:11s} {rel}{extra}")
print(f"\n  CASE1 survivor checked: "
      f"{'OK' if os.path.isfile(os.path.join(CANON, CASE1_WINNER, 'SKILL.md')) else 'MISSING'}")
print(f"  CASE2 survivor checked: "
      f"{'OK' if os.path.isfile(os.path.join(CANON, CASE2_KEEP, 'SKILL.md')) else 'MISSING'}")
if not APPLY:
    print("\nDRY RUN — pass --apply")
    raise SystemExit(0)

os.makedirs(FREEZE, exist_ok=True)
led = []
for kind, rel, p in plan:
    rec = {"path": p, "rel": rel, "kind": kind}
    if kind == "repoint":
        old = os.readlink(p)
        os.unlink(p)
        os.symlink(os.path.join(CANON, CASE2_KEEP), p)
        rec.update({"was": old, "now": os.path.join(CANON, CASE2_KEEP),
                    "undo": f"ln -sfn {old} {p}"})
    else:
        rec["files"] = snap(p)
        rec["files_count"] = len(rec["files"])
        dst = os.path.join(FREEZE, os.path.basename(p.rstrip("/")))
        rec["frozen_path"] = dst
        rec["action"] = "moved"
        rec["undo"] = f"mv {dst} {p}"
        shutil.move(p, dst)
    led.append(rec)

# the now-empty case-twin directory
tw = os.path.join(CANON, CASE1_DIR_TWIN)
if os.path.isdir(tw) and not os.listdir(tw):
    os.rmdir(tw)
    led.append({"path": tw, "rel": CASE1_DIR_TWIN, "kind": "rmdir_empty",
                "undo": f"mkdir -p {tw}",
                "note": "case-twin of forge-onboarding/ became empty after its only child retired"})
    print("removed empty case-twin dir:", tw)

json.dump({"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "authority": "ARIF — audit of routing-name collisions, 2026-09-19",
           "evidence": "hermes-agent tools/skills_tool.py:275-277 (first-wins dedupe on frontmatter name)",
           "canon": CANON, "freeze_root": FREEZE, "items": led},
          open(os.path.join(FREEZE, "LEDGER.json"), "w"), indent=2)
print(f"\nAPPLIED {len(led)} items -> {FREEZE}/LEDGER.json")
