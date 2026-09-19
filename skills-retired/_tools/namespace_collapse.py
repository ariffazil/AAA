#!/usr/bin/env python3
"""
namespace_collapse.py — Tier-1 sweep of the canonical skill store.

AUTHORITY: F13 sovereign in-chat order 2026-09-19 ("sila buang benda bangang").
EVIDENCE : /root/AAA/skills (catalog) + /root/scripts/skills-census.py witness.
REVERSIBLE: every removed path is moved OUT of the walked tree with sha256 recorded
            and an undo command in the ledger.

NOTHING IS DELETED. Freeze root is outside the skill walk so a frozen skill cannot load.
"""
import os, sys, json, shutil, hashlib, datetime, subprocess

CANON = "/root/AAA/skills"
FREEZE = "/root/AAA/skills-retired/2026-09-19-namespace-collapse"
APPLY = "--apply" in sys.argv

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()

# ---------------- prune set ------------------------------------------------
# each entry: (relpath, tier, reason, successor_or_None)
# relpath may be a directory OR a single file (SKILL.md of a namespace placeholder)
P = []

# Tier 2 — alias pretending to be a skill (redirect only, no doctrine)
P += [
 ("mcp-shopping-list-2026-09", "T2-alias", "redirect only -> mcp-sota-shopping-list", "mcp-sota-shopping-list"),
 ("forge-mcp-ops/mcp-dual-era-transport", "T2-alias", "redirect only -> mcp-testing", "mcp-testing"),
 ("wisdom-scar-session-audit", "T2-alias", "redirect only -> scar-integration", "scar-integration"),
 ("domains/general/aaa/substrate/reflective/sovereign-recognize", "T2-alias",
  "redirect only -> audience-scoped-disclosure", "audience-scoped-disclosure"),
 ("domains/general/forge/mcp-ops/FORGE-mcp-testing", "T2-alias", "redirect only -> mcp-testing", "mcp-testing"),
 ("domains/general/court/court-audit/cognitive-level-assertion-protocol", "T2-alias",
  "redirect only -> claim-receipt-discipline", "claim-receipt-discipline"),
]

# Tier 1b — stub that declares itself not a skill / archived placeholder
P += [
 ("domains/general/apex/recursive-audit/RSI-recursive-improvement", "T1-stub", "34-byte tombstone, zero procedure", None),
 ("causal555-pywhy", "T1-stub", "self-declared ARCHIVED placeholder, no procedure", None),
 ("wealth-claim-state", "T1-stub", "self-declared placeholder; live lane is wealth-claim-state skill under domains", None),
]

# Tier 4 — vendor / foreign-profile junk inside the AAA catalog
P += [
 (".system/imagegen", "T4-vendor", "foreign harness bundle, not an AAA capability", None),
 (".system/openai-docs", "T4-vendor", "vendor documentation bot, not an AAA capability", None),
 (".system/plugin-creator", "T4-vendor", "foreign harness bundle + carries a ghost script", None),
 (".system/review-agent", "T4-vendor", "foreign harness bundle, not an AAA capability", None),
 (".system/skill-installer", "T4-vendor", "foreign harness bundle, not an AAA capability", None),
 (".system/skill-creator", "T4-dup", "triple body; canonical kept in the taxonomised home", "skill-creator"),
 (".profile-archive", "T4-vendor", "symlink farm into a third-party plugin repo, not AAA doctrine", None),
 ("help", "T4-vendor", "documents a vendor product this federation does not run", None),
 (".archive-2026-09-18", "T3-archive", "archive that was still being loaded as live skill", None),
]

# Tier 6 — case-twin forensics: two bodies, one identity
CASE_TWINS = [
 ("FORGE-federation-manifest", "forge-federation-manifest"),
 ("RSI-federation-mesh", "rsi-federation-mesh"),
]

# namespace placeholder SKILL.md (dir holds real children, only the stub dies)
PLACEHOLDER_FM = ["runtime", "scripts", "docs", "substrate", "warga"]

# orphan symlinks whose target we prune
ORPHAN_LINKS = ["FORGE-mcp-testing", "cognitive-level-assertion-protocol",
                "RSI-recursive-improvement"]

def newest(*dirs):
    best, bt = None, -1
    for d in dirs:
        f = os.path.join(CANON, d, "SKILL.md")
        if os.path.isfile(f):
            t = os.path.getmtime(f)
            if t > bt:
                best, bt = d, t
    return best

for a, b in CASE_TWINS:
    pa, pb = os.path.join(CANON, a), os.path.join(CANON, b)
    if os.path.isdir(pa) and os.path.isdir(pb):
        keep = newest(a, b)
        loser = b if keep == a else a
        P.append((loser, "T6-case-twin", "case is not doctrine; twin of " + keep, keep))

plan, skipped = [], []
for rel, tier, reason, succ in P:
    p = os.path.join(CANON, rel)
    if os.path.islink(p):
        plan.append({"rel": rel, "kind": "symlink", "tier": tier, "reason": reason, "successor": succ})
    elif os.path.isdir(p):
        if os.path.exists(os.path.join(p, "SKILL.md")) or tier in ("T4-vendor", "T3-archive") or any(
                f.endswith("SKILL.md") for _, _, fs in os.walk(p) for f in fs):
            plan.append({"rel": rel, "kind": "dir", "tier": tier, "reason": reason, "successor": succ})
        else:
            skipped.append((rel, "no SKILL.md inside"))
    else:
        skipped.append((rel, "not on disk"))

for rel in PLACEHOLDER_FM:
    f = os.path.join(CANON, rel, "SKILL.md")
    if os.path.isfile(f):
        plan.append({"rel": rel + "/SKILL.md", "kind": "file", "tier": "T1b-placeholder",
                     "reason": "namespace dir stub; dir holds real children", "successor": None})

for rel in ORPHAN_LINKS:
    p = os.path.join(CANON, rel)
    if os.path.islink(p):
        plan.append({"rel": rel, "kind": "symlink", "tier": "T6-orphan-link",
                     "reason": "resolution alias; target is being retired", "successor": None})

print("=== PLAN (%d items) ===" % len(plan))
for d in sorted(plan, key=lambda x: (x["tier"], x["rel"])):
    print(f"  {d['tier']:16s} {d['kind']:7s} {d['rel']}"
          + (f"  -> {d['successor']}" if d["successor"] else ""))
if skipped:
    print("\n=== SKIPPED (not found / no body) ===")
    for s in skipped:
        print("  ", s)

if not APPLY:
    print("\nDRY RUN. re-run with --apply")
    sys.exit(0)

os.makedirs(FREEZE, exist_ok=True)
ledger = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "authority": "F13 sovereign in-chat 2026-09-19",
          "canon": CANON, "freeze_root": FREEZE,
          "undo": "mv <frozen_path> <orig_path>   (paths recorded below)",
          "items": []}

for d in plan:
    src = os.path.join(CANON, d["rel"])
    dst = os.path.join(FREEZE, d["rel"])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    rec = dict(d)
    if os.path.islink(src):
        rec["sha256"] = "symlink:" + (os.readlink(src) or "")
        if APPLY:
            os.unlink(src)
        rec["action"] = "unlink_symlink"
    else:
        if os.path.isdir(src):
            shas = {}
            for dp, dn, fn in os.walk(src):
                for f in fn:
                    fp = os.path.join(dp, f)
                    shas[os.path.relpath(fp, src)] = sha(fp)
            rec["files"] = shas
        else:
            rec["sha256"] = sha(src)
        if APPLY:
            shutil.move(src, dst)
        rec["action"] = "move"
    rec["orig_path"] = src
    rec["frozen_path"] = dst
    ledger["items"].append(rec)

led = os.path.join(FREEZE, "LEDGER.json")
json.dump(ledger, open(led, "w"), indent=2)
print("\nAPPLIED %d items. ledger: %s" % (len(ledger["items"]), led))
