#!/usr/bin/env python3
"""
align_all_agents_pass2.py — Fix partial alignments (only one of apex_zen/apexMasterSeal present).
"""

import json
from collections import OrderedDict
from pathlib import Path

CARDS = sorted(
    {
        f
        for f in [
            *Path("/root/AAA/a2a-server/agent-cards/").rglob("*.json"),
            *[p for p in Path("/root/AAA/agents").rglob("agent-card.json") if "_" not in p.parts[-2]],
        ]
        if not any(
            seg.startswith(".") or seg in ("tombstone", "_superseded", "_external", "_lanes", "_brief", "_docs")
            for seg in f.parts
        )
        and not f.name.endswith(".bak")
        and not f.name.endswith(".applied-20260930T123500Z.json")
        and not f.name.endswith(".bak-pre-fix-20260930")
        and "extensions" not in f.parts
    }
)


def load_preserving_order(path: Path):
    with path.open() as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def dump_preserving_order(doc, path: Path):
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def main():
    fixed = []
    still_partial = []
    intact = []

    for path in CARDS:
        try:
            card = load_preserving_order(path)
        except Exception:
            continue
        has_az = "apex_zen" in card
        has_ams = "apexMasterSeal" in card
        if has_az and has_ams:
            intact.append(str(path))
            continue
        if not has_az:
            # synthesize minimal apex_zen from existing card
            card_id = card.get("id", path.stem)
            card["apex_zen"] = OrderedDict(
                [
                    ("canonical_ref", "/root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md"),
                    ("governance_chain", "BUILD → VERIFY → JUDGE → SEAL → ACT → WITNESS"),
                    ("invariant", "CAPABILITY ≠ AUTHORITY"),
                    ("doctrine", "Govern capabilities, not implementations."),
                    ("motto", "DITEMPA BUKAN DIBERI"),
                    ("capability", "VERIFY"),
                    ("lane", card_id),
                    ("auto_aligned_pass2", True),
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
                    ("auto_aligned_pass2", True),
                ]
            )

        # Re-check
        if "apex_zen" in card and "apexMasterSeal" in card:
            dump_preserving_order(card, path)
            fixed.append(str(path))
        else:
            still_partial.append(str(path))

    print(f"=== Pass-2 fixes ===")
    print(f"  Intact (already both blocks): {len(intact)}")
    print(f"  Fixed (now both blocks):       {len(fixed)}")
    print(f"  Still partial:                 {len(still_partial)}")
    for f in fixed:
        print(f"  ✅ {f}")
    for s in still_partial:
        print(f"  ⚠ {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
