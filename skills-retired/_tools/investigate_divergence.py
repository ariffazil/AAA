#!/usr/bin/env python3
"""Investigate skills-census.py `diverged` — detector defect or store defect?

Findings so far (read, not assumed):
  scan() keys its index on the DIRECTORY relpath (skills-census.py:93).
  The divergence block (lines 187-190) then reduces that key with os.path.basename() BEFORE
  matching:  cbase = {os.path.basename(k): v for k, v in canon.items()}
  A leaf folder name is NOT unique across the store (two folders can both be called `claude`,
  `code-review`, `claude`, ...). The dict comprehension keeps ONE per name, so the comparison
  pairs two UNRELATED skills and calls them "the same skill diverged".

This script answers, with evidence:
  Q1  which two skills are being compared RIGHT NOW (the false pair)
  Q2  what the shared set size is (a healthy mesh should match hundreds — a small number proves
      the key is broken)
  Q3  is any REAL divergence hiding behind the broken detector?  (correct comparison below)
  Q4  has this ever been right?  (git history of the block)
"""
import os, re, json, hashlib, subprocess, collections

CANON = "/root/AAA/skills"
HERM = "/root/.hermes/skills"
EXCL = {".git", ".hub", ".archive", ".curator_backups", "__pycache__", "node_modules", "venv", ".venv"}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def scan(root):
    out = {}
    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = [d for d in dn if d not in EXCL and not d.startswith(".")]
        if "SKILL.md" not in fn:
            continue
        p = os.path.join(dp, "SKILL.md")
        if not os.path.exists(p):
            continue
        out[os.path.relpath(dp, root)] = {"sha": sha(p), "abs": dp,
                                          "bytes": os.path.getsize(p)}
    return out

c, h = scan(CANON), scan(HERM)
print(f"canonical entries: {len(c)}   hermes entries: {len(h)}")

# ---- Q1/Q2: reproduce the census's broken match ----
cb = {}
for k, v in c.items():
    cb[os.path.basename(k)] = (k, v)      # last wins — this is the defect
hb = {}
for k, v in h.items():
    hb[os.path.basename(k)] = (k, v)
shared = set(cb) & set(hb)
print(f"\nQ2  basename-matched key set size: {len(shared)}  (a working match should be ~{len(c)})")
div = [k for k in shared if cb[k][1]["sha"] != hb[k][1]["sha"]]
print(f"\nQ1  census reports `diverged` = {len(div)}: {div}")
for k in div:
    print(f"      name key   : {k!r}")
    print(f"      canon side : {cb[k][0]}   ({cb[k][1]['bytes']} B)")
    print(f"      hermes side: {hb[k][0]}   ({hb[k][1]['bytes']} B)")
    print("      -> these are TWO DIFFERENT SKILLS that merely share a leaf folder name")

# how many basenames are ambiguous in each tree (the size of the defect's blast radius)
amb_c = collections.Counter(os.path.basename(k) for k in c)
amb_h = collections.Counter(os.path.basename(k) for k in h)
print(f"\n    ambiguous leaf names in canon  : {sum(1 for v in amb_c.values() if v>1)}"
      f" (affecting {sum(v for v in amb_c.values() if v>1)} entries, collapsed to"
      f" {sum(1 for v in amb_c.values() if v>1)})")
print(f"    ambiguous leaf names in hermes : {sum(1 for v in amb_h.values() if v>1)}")

# ---- Q3: the CORRECT comparison — match by the canonical relative path ----
real = []
for k, v in c.items():
    if k in h and h[k]["sha"] != v["sha"]:
        real.append((k, v, h[k]))
print(f"\nQ3  REAL divergences, matched by relative path: {len(real)}")
for k, a, b in real[:20]:
    print(f"      {k}: canon {a['bytes']}B {a['sha'][:12]}  vs  hermes {b['bytes']}B {b['sha'][:12]}")

# and: canonical paths with NO counterpart at all in the hermes view
missing = [k for k in c if k not in h]
extra = [k for k in h if k not in c]
print(f"\n    canonical paths with no hermes counterpart: {len(missing)}")
for m in missing[:10]:
    print(f"      {m}")
print(f"    hermes paths with no canonical counterpart: {len(extra)}")
for e in extra[:10]:
    print(f"      {e}")

# ---- Q4: git history of the block ----
try:
    out = subprocess.run(["git", "-C", "/root/AAA", "log", "--oneline", "-5",
                          "--", "skills/skill-library-integrity/scripts/skills-census.py"],
                         capture_output=True, text=True, timeout=30).stdout
    print("\nQ4  git log for the census file (in /root/AAA):")
    print("    " + (out.strip().replace("\n", "\n    ") or "(file is not tracked in this repo)"))
except Exception as e:
    print("Q4 unavailable:", e)

json.dump({"canonical": len(c), "hermes": len(h), "broken_shared": len(shared),
           "census_diverged": div, "real_divergences": [k for k, _, _ in real],
           "missing_in_hermes": missing[:50], "extra_in_hermes": extra[:50]},
          open("/root/AAA/skills-retired/2026-09-19-routing-collisions/DIVERGENCE-INVESTIGATION.json", "w"),
          indent=2)
print("\nwrote DIVERGENCE-INVESTIGATION.json")
