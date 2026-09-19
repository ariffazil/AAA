#!/usr/bin/env python3
"""Verify the control-audit family merge (F13 order 2026-09-19). Read-only."""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys

CANON = "/root/AAA/skills"
NEW = "/root/AAA/skills/governance-audit/SKILL.md"
DEST = "/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/control-audit"

OLD_DESCRIPTIONS = [
    "auditing whether a control really enforces",
    "a service claims a control you must verify",
    "a named control may not actually enforce",
    "auditing whether a named control actually acts",
    "auditing whether a named control actually controls",
    "auditing whether a control actually controls",
    "verifying a claimed result or sealing a control",
    "auditing an auth/gate control for verification",
]
OLD_TRIGGERS = [
    # named-mechanism-audit
    "is this actually enforced", "does this gate work", "verify this safeguard", "the control is present",
    "privacy filter is on", "0 rejections", "gate passed", "is this wired up", "verify a claimed control",
    "false name", "named but not installed", "hardcoded metric",
    # enforcement-coverage-audit
    "is this gate real", "does the gate actually block", "enforcement coverage", "can this bypass the gate",
    "who actually made this change", "audit trail attribution", "prevented vs detected", "is the guard load-bearing",
]
# noun-level surfaces taken from the predecessors' when-to-use fields
SURFACES = [
    "gate", "validator", "health check", "sandbox", "seal", "drift detector", "shadow mode",
    "authority check", "privacy filter", "promotion ladder", "approval gate", "signature",
    "scope check", "deny list", "rate limit", "authorization tier", "session gate", "authority band",
    "human-approval field", "allow/deny regex",
]
MODES = [
    "MODE-CONTROL-INTEGRITY", "MODE-DECLARED-VS-ENFORCED", "MODE-NAMED-MECHANISM",
    "MODE-ENFORCEMENT-COVERAGE", "MODE-SEAL-VERIFICATION", "MODE-PROXY", "MODE-METRIC-DERIVATION",
]


def sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main() -> int:
    ok = True
    size = os.path.getsize(NEW)
    print(f"1) canonical SKILL.md size: {size} bytes  (>= 15360: {size >= 15360})")
    ok &= size >= 15360

    text = open(NEW).read()
    m = re.search(r'^description: "(.*)"$', text, re.M)
    desc = m.group(1) if m else ""
    print(f"2) description extracted: {len(desc)} chars")
    missing = [p for p in OLD_DESCRIPTIONS + OLD_TRIGGERS if p.lower() not in desc.lower()]
    print(f"   old description strings present: {len(OLD_DESCRIPTIONS) - len([p for p in OLD_DESCRIPTIONS if p in missing])}/{len(OLD_DESCRIPTIONS)}")
    print(f"   old trigger phrases present:     {len(OLD_TRIGGERS) - len([p for p in OLD_TRIGGERS if p in missing])}/{len(OLD_TRIGGERS)}")
    if missing:
        ok = False
        print(f"   MISSING FROM DESCRIPTION: {missing}")
    surf_missing = [s for s in SURFACES if s.lower() not in desc.lower()]
    print(f"   surface nouns in description:    {len(SURFACES) - len(surf_missing)}/{len(SURFACES)}"
          + (f"  missing={surf_missing}" if surf_missing else ""))
    mode_missing = [m_ for m_ in MODES if m_ not in text]
    print(f"3) modes declared in body:          {len(MODES) - len(mode_missing)}/{len(MODES)}"
          + (f"  missing={mode_missing}" if mode_missing else ""))
    ok &= not mode_missing
    for m_ in MODES:
        n = len(re.findall(rf"^## \d+\. {re.escape(m_)}", text, re.M))
        bars = len(re.findall(re.escape(m_), text))
        print(f"   {m_:28s} section headings={n}  mentions={bars}")

    ledger = json.load(open(os.path.join(DEST, "LEDGER.json")))
    print(f"4) ledger parses: items={len(ledger['merged_from'])} canonical_sha256={ledger['canonical_sha256'][:12]}…")
    ok &= len(ledger["merged_from"]) == 8
    ok &= ledger["canonical_sha256"] == sha256(NEW)
    print(f"   ledger canonical_sha256 == on-disk: {ledger['canonical_sha256'] == sha256(NEW)}")

    print("5) per-folder: original gone / frozen SKILL.md / sha256 preserved")
    for e in ledger["merged_from"]:
        gone = not os.path.exists(e["original_folder"])
        frozen = os.path.isfile(e["new_path"])
        same = frozen and sha256(e["new_path"]) == e["sha256_skilmd_before_move"]
        ok &= gone and frozen and same
        print(f"   {'OK ' if (gone and frozen and same) else 'FAIL'} orig_gone={gone} frozen={frozen} "
              f"sha_preserved={same} mode={e['new_mode']:26s} {os.path.basename(e['new_folder'])}")

    print("6) no stray copies left in canon store:")
    for e in ledger["merged_from"]:
        leaf = os.path.basename(e["original_folder"])
        hits = [os.path.join(r, leaf) for r, dirs, _ in os.walk(CANON) if leaf in dirs]
        ok &= not hits
        print(f"   {'OK ' if not hits else 'FAIL'} {leaf}: {hits}")

    print(f"\nRESULT: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
