#!/usr/bin/env python3
"""
align_lanes_external_pass3.py — Final pass for the lanes/ + external/ cards.

Skip:
  - _archive/ (frozen by archive date in filename — leave as-is)
  - _superseded/ (intentionally retired)
"""

import json
from collections import OrderedDict
from pathlib import Path

# Live lanes + external only
TARGETS = [
    "/root/AAA/agents/_lanes/333-AGI/agent-card.json",
    "/root/AAA/agents/_lanes/777-forge/agent-card.json",
    "/root/AAA/agents/_lanes/888-APEX/agent-card.json",
    "/root/AAA/agents/_lanes/555-ASI/agent-card.json",
    "/root/AAA/agents/_external/codex/agent-card.json",
    "/root/AAA/agents/_external/opencode/agent-card.json",
    "/root/AAA/agents/_external/agy/agent-card.json",
    "/root/AAA/agents/_external/copilot-cli/agent-card.json",
]


def load_preserving_order(path):
    with open(path) as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def dump_preserving_order(doc, path):
    with open(path, "w") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    fixed = []
    for path in TARGETS:
        p = Path(path)
        if not p.exists():
            print(f"  ⚠ missing: {path}")
            continue
        card = load_preserving_order(p)
        card_id = card.get("id", p.stem)
        has_az = "apex_zen" in card
        has_ams = "apexMasterSeal" in card
        if not has_az:
            card["apex_zen"] = OrderedDict(
                [
                    ("canonical_ref", "/root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md"),
                    ("governance_chain", "BUILD → VERIFY → JUDGE → SEAL → ACT → WITNESS"),
                    ("invariant", "CAPABILITY ≠ AUTHORITY"),
                    ("doctrine", "Govern capabilities, not implementations."),
                    ("motto", "DITEMPA BUKAN DIBERI"),
                    ("capability", "VERIFY"),
                    ("lane", card_id),
                    ("auto_aligned_pass3", True),
                ]
            )
        if not has_ams:
            card["apexMasterSeal"] = OrderedDict(
                [
                    ("cognitiveRing", "unassigned"),
                    ("thermodynamicRole", "neutral"),
                    ("ringPlacement", "none"),
                    ("parallelism", "none"),
                    ("shadowAcknowledged", []),
                    ("doctrine", "DITEMPA BUKAN DIBERI"),
                    ("auto_aligned_pass3", True),
                ]
            )
        dump_preserving_order(card, p)
        fixed.append(path)
        print(f"  ✅ {p}")
    print(f"\n=== Fixed {len(fixed)} files ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
