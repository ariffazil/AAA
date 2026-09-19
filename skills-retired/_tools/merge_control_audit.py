#!/usr/bin/env python3
"""Merge the 8-skill control-audit family into governance-audit (F13 order 2026-09-19).

Steps (idempotent-ish, refuses to clobber):
 1. copy support files referenced by the eight SKILL.md bodies into
    /root/AAA/skills/governance-audit/{references,scripts}
 2. sha256 every source SKILL.md BEFORE any move
 3. write .../merges/control-audit/LEDGER.json (schema mirrors merges/zen-router/LEDGER.json)
 4. move each source folder (flattened) into .../merges/control-audit/<leaf>
 5. verify + print
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone

SRC = "/root/AAA/skills"
CANON = "/root/AAA/skills/governance-audit"
DEST = "/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/control-audit"
FROZEN_ROOT = "/root/AAA/skills-retired/2026-09-19-namespace-collapse"

# (orig folder relative to SRC, leaf name under DEST, mode in the canonical skill)
ITEMS = [
    ("audit/control-integrity-audit", "control-integrity-audit", "MODE-CONTROL-INTEGRITY"),
    ("audit/declared-vs-enforced-control-audit", "declared-vs-enforced-control-audit", "MODE-DECLARED-VS-ENFORCED"),
    ("governance/control-mechanism-audit", "control-mechanism-audit", "MODE-NAMED-MECHANISM"),
    ("governance/named-mechanism-audit", "named-mechanism-audit", "MODE-NAMED-MECHANISM"),
    ("audit/name-requires-mechanism", "name-requires-mechanism", "MODE-NAMED-MECHANISM"),
    ("enforcement-coverage-audit", "enforcement-coverage-audit", "MODE-ENFORCEMENT-COVERAGE"),
    ("governance/control-seal-verification", "control-seal-verification", "MODE-SEAL-VERIFICATION"),
    ("court-audit/proxy-verification-audit", "proxy-verification-audit", "MODE-PROXY"),
]

# support files carried into the canonical skill (source relative to SRC -> dest relative to CANON)
SUPPORT = [
    ("audit/control-integrity-audit/references/decoy-catalogue.md", "references/decoy-catalogue.md"),
    ("governance/control-mechanism-audit/references/seal-and-delivery-verification.md", "references/seal-and-delivery-verification.md"),
    ("enforcement-coverage-audit/references/sensor-falsification.md", "references/sensor-falsification.md"),
    ("governance/control-seal-verification/references/sealing-a-control.md", "references/sealing-a-control.md"),
    ("court-audit/proxy-verification-audit/references/metric-derivation-discipline.md", "references/metric-derivation-discipline.md"),
    ("audit/declared-vs-enforced-control-audit/scripts/contract_probe.py", "scripts/contract_probe.py"),
]


def sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main() -> int:
    log: list[str] = []

    # 0. preconditions
    for rel, leaf, _mode in ITEMS:
        src_dir = os.path.join(SRC, rel)
        if not os.path.isdir(src_dir):
            print(f"ABORT: source folder missing: {src_dir}")
            return 2
        if os.path.isdir(os.path.join(DEST, leaf)):
            print(f"ABORT: destination already exists: {os.path.join(DEST, leaf)}")
            return 2
    os.makedirs(DEST, exist_ok=True)

    # 1. copy support files
    for rel_src, rel_dst in SUPPORT:
        s = os.path.join(SRC, rel_src)
        d = os.path.join(CANON, rel_dst)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        log.append(f"support copied: {s} -> {d}")

    # 2. sha256 BEFORE the move + 3. ledger
    merged_from = []
    for rel, leaf, mode in ITEMS:
        s_dir = os.path.join(SRC, rel)
        s_skill = os.path.join(s_dir, "SKILL.md")
        d_dir = os.path.join(DEST, leaf)
        files = sorted(
            os.path.relpath(os.path.join(root, name), s_dir)
            for root, _dirs, names in os.walk(s_dir)
            for name in names
        )
        entry = {
            "original_folder": s_dir,
            "new_folder": d_dir,
            "original_path": s_skill,
            "new_path": os.path.join(d_dir, "SKILL.md"),
            "sha256_skilmd_before_move": sha256(s_skill),
            "size_bytes": os.path.getsize(s_skill),
            "files_moved": files,
            "new_mode": mode,
        }
        merged_from.append(entry)
        log.append(f"hashed {s_skill} {entry['sha256_skilmd_before_move'][:12]}…")

    canon_skill = os.path.join(CANON, "SKILL.md")
    ledger = {
        "ledger": "namespace-collapse-merge",
        "operation": "merge_skill_family",
        "merge_name": "control-audit",
        "canonical_skill": "governance-audit",
        "canonical_path": canon_skill,
        "canonical_sha256": sha256(canon_skill),
        "canonical_size_bytes": os.path.getsize(canon_skill),
        "authority": "F13 sovereign in-chat order 2026-09-19 — eight skills answering one question become one skill with modes",
        "date": "2026-09-19",
        "ts": datetime.now(timezone.utc).isoformat(),
        "canon": SRC,
        "freeze_root": FROZEN_ROOT,
        "undo": "mv <new_folder> <original_folder>   (paths recorded below; parent dirs may need mkdir -p)",
        "merged_from": merged_from,
        "support_files_copied_into_canonical": [
            {"from": os.path.join(SRC, s), "to": os.path.join(CANON, d)} for s, d in SUPPORT
        ],
        "note": (
            "sha256_skilmd_before_move computed on the original SKILL.md prior to relocation; "
            "folder contents were not modified by the move. A copy of each support file also "
            "remains inside its frozen original folder."
        ),
    }
    ledger_path = os.path.join(DEST, "LEDGER.json")
    with open(ledger_path, "w") as fh:
        json.dump(ledger, fh, indent=2)
        fh.write("\n")
    log.append(f"ledger written: {ledger_path}")

    # 4. move (flattened)
    for rel, leaf, _mode in ITEMS:
        s_dir = os.path.join(SRC, rel)
        d_dir = os.path.join(DEST, leaf)
        shutil.move(s_dir, d_dir)
        log.append(f"moved {s_dir} -> {d_dir}")
        # remove now-empty parent category dirs in canon (only if empty)
        parent = os.path.dirname(s_dir)
        if parent != SRC and os.path.isdir(parent) and not os.listdir(parent):
            os.rmdir(parent)
            log.append(f"removed empty category dir {parent}")

    # 5. verify
    ok = True
    print("== copies ==")
    for _s, d in SUPPORT:
        p = os.path.join(CANON, d)
        exists = os.path.isfile(p)
        ok &= exists
        print(f"  {'OK ' if exists else 'MISS'} {p} ({os.path.getsize(p) if exists else 0} bytes)")
    print("== originals gone ==")
    for rel, _leaf, _m in ITEMS:
        p = os.path.join(SRC, rel)
        gone = not os.path.exists(p)
        ok &= gone
        print(f"  {'OK ' if gone else 'STILL THERE'} {p}")
    print("== frozen copies present ==")
    for _rel, leaf, _m in ITEMS:
        p = os.path.join(DEST, leaf, "SKILL.md")
        exists = os.path.isfile(p)
        ok &= exists
        print(f"  {'OK ' if exists else 'MISS'} {p}")
    print("== ledger parses ==")
    try:
        with open(ledger_path) as fh:
            d = json.load(fh)
        print(f"  OK {ledger_path} items={len(d['merged_from'])} canonical_bytes={d['canonical_size_bytes']}")
    except Exception as exc:  # noqa: BLE001
        ok = False
        print(f"  FAIL {exc}")
    print("== log ==")
    for line in log:
        print("  " + line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
