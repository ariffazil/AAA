#!/usr/bin/env python3
"""Verify every delegated merge against the disk. A subagent's self-report is not evidence."""
import os, json, subprocess, hashlib

CANON = "/root/AAA/skills"
MERGE = "/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges"

JOBS = {
 "agentic-state":    "agentic-state",
 "zen-router":       "zen-router",
 "meta-mesa":        "meta-mesa",
 "propose-seal":     "propose-seal",
 "control-audit":    "governance-audit",
 "voice-lane":       "voice-lane",
 "intel-briefing":   "intelligence-briefing",
 "person-intelligence": "person-intelligence",
 "recovery-playbook": "recovery-playbook",
}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()

summary = []
for mdir, target in JOBS.items():
    mp = os.path.join(MERGE, mdir)
    tp = os.path.join(CANON, target, "SKILL.md")
    row = {"merge_dir": mdir, "target": target}
    row["merge_dir_exists"] = os.path.isdir(mp)
    row["target_exists"] = os.path.isfile(tp)
    if row["target_exists"]:
        row["target_bytes"] = os.path.getsize(tp)
        row["target_sha"] = sha(tp)[:12]
    row["sources_frozen"] = sorted(d for d in os.listdir(mp)
                                   if os.path.isdir(os.path.join(mp, d))) if row["merge_dir_exists"] else []
    row["ledger"] = os.path.isfile(os.path.join(mp, "LEDGER.json"))
    # sources still live in canon?
    still = [s for s in row["sources_frozen"] if os.path.isdir(os.path.join(CANON, s))]
    row["sources_still_in_canon"] = still
    summary.append(row)

print(f"{'merge':22s} {'target':22s} {'KB':>6s} {'frozen':>7s} {'ledger':>7s} {'still_live':>10s}")
for r in summary:
    print(f"{r['merge_dir']:22s} {r['target']:22s} "
          f"{r.get('target_bytes', 0)/1024:6.1f} {len(r['sources_frozen']):7d} "
          f"{str(r['ledger']):>7s} {len(r['sources_still_in_canon']):10d}")

print("\n=== discovery guard on every landed merge ===")
for mdir, target in JOBS.items():
    mp = os.path.join(MERGE, mdir)
    tp = os.path.join(CANON, target)
    if not (os.path.isdir(mp) and os.path.isfile(os.path.join(tp, "SKILL.md"))):
        print(f"  -- {mdir}: not landed yet (target missing)")
        continue
    srcs = [os.path.join(mp, d) for d in os.listdir(mp)
            if os.path.isdir(os.path.join(mp, d))]
    if not srcs:
        print(f"  -- {mdir}: no frozen sources to compare")
        continue
    out = subprocess.run(
        ["python3", "/root/AAA/skills/skill-library-integrity/scripts/discovery_guard.py", tp] + srcs,
        capture_output=True, text=True, timeout=120)
    tail = [l for l in out.stdout.splitlines() if l.strip().startswith(("GAP", "VERDICT", "FAIL"))]
    print(f"  {mdir:22s} -> {target:22s} {' | '.join(tail) or 'no verdict'}")

json.dump(summary, open(os.path.join(MERGE, "_VERIFY.json"), "w"), indent=2)
print("\nwrote", os.path.join(MERGE, "_VERIFY.json"))
