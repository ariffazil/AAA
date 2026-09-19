#!/usr/bin/env python3
"""V2 audit — execute the clean retirements. Every item: freeze, never delete.
Class F (profile junk) + Class C false-positive record. Ledger written before/with the move."""
import os, json, shutil, hashlib, datetime, sys

CANON = "/root/AAA/skills"
FREEZE = "/root/AAA/skills-retired/2026-09-19-v2-profile-junk"
APPLY = "--apply" in sys.argv

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()

# CLASS F — vendor profile material that is a REAL DIR inside the canonical library
VENDOR = ["understand", "understand-chat", "understand-dashboard", "understand-diff",
          "understand-domain", "understand-explain", "understand-figma",
          "understand-knowledge", "understand-onboard"]

plan = []
for name in VENDOR:
    p = os.path.join(CANON, name)
    if os.path.isdir(p) and not os.path.islink(p):
        plan.append((name, p))

print("CLASS F — profile junk, real dirs in canon:")
for n, p in plan:
    nf = sum(len(f) for _, _, f in os.walk(p))
    print(f"  {n:22s} {nf:3d} files  {sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(p) for f in fs)/1024:8.1f} KB")
print(f"  total: {len(plan)} identities, "
      f"{sum(os.path.getsize(os.path.join(r,f)) for _,p in plan for r,_,fs in os.walk(p) for f in fs)/1024:.1f} KB of vendor prose")
print("  provenance check: SKILL.md files referencing the vendor plugin ->",
      sum(1 for n, p in plan if "understand-anything" in open(os.path.join(p, 'SKILL.md'), encoding='utf-8', errors='replace').read()))

if not APPLY:
    print("DRY RUN")
    raise SystemExit(0)

os.makedirs(FREEZE, exist_ok=True)
led = []
for n, p in plan:
    files = {}
    for r, _, fs in os.walk(p):
        for f in fs:
            fp = os.path.join(r, f)
            files[os.path.relpath(fp, p)] = sha(fp)
    dst = os.path.join(FREEZE, n)
    rec = {"name": n, "orig_path": p, "frozen_path": dst, "files": files,
           "sha256_of_SKILL": files.get("SKILL.md"), "files_count": len(files),
           "class": "F-PROFILE-JUNK",
           "why": "vendor plugin profile (understand-anything) materialised as a real directory "
                  "inside the canonical store; federation loses no constitutional capability",
           "undo": f"mv {dst} {p}"}
    led.append(rec)
    shutil.move(p, dst)

json.dump({"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "authority": "ARIF — SKILLSTORE_NAMESPACE_COLLAPSE_V2",
           "canon": CANON, "freeze_root": FREEZE, "items": led},
          open(os.path.join(FREEZE, "LEDGER.json"), "w"), indent=2)
print(f"\nAPPLIED {len(led)} freezes -> {FREEZE}")
print("ledger:", os.path.join(FREEZE, "LEDGER.json"))
left = [n for n in VENDOR if os.path.isdir(os.path.join(CANON, n))]
print("still in canon (must be empty):", left)
