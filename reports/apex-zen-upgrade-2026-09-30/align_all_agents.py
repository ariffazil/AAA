#!/usr/bin/env python3
"""
align_all_agents.py — Add `apex_zen` + `apexMasterSeal` to every AAA agent card.

Reversible (per-file backup at .applied-<date>). Adds blocks additively (no field removed
or restricted). Synthesizes appropriate role-based values from card class + tier + role.

Capability logic (per agent class):
  CORE organ / JUDGE        → capability=JUDGE
  CORE organ / EXECUTE      → capability=BUILD
  METABOLISM               → capability=OBSERVE
  EDGE                     → capability=ACT
  ADVISORY                 → capability=WITNESS
  SUPPORT                  → capability=VERIFY
  DATA                     → capability=STORE
  MEMORY                   → capability=REMEMBER

CognitiveRing (apexMasterSeal):
  CORE organ / JUDGE        → ring=judicator · role=inner · single-threaded
  CORE organ / EXECUTE      → ring=generator · role=outer · multi-model
  METABOLISM               → ring=observer · role=metabolic · pipeline
  EDGE                     → ring=executor · role=outer · parallel
  ADVISORY                 → ring=advisor · role=anchor · single
  SUPPORT                  → ring=auditor · role=inner · single-threaded
  DATA                     → ring=store · data := outer · stream
  MEMORY                   → ring=archivist · role=anchor · append-only
"""

import json
import sys
from collections import OrderedDict
from pathlib import Path
from datetime import datetime, timezone

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


# Map path-pattern to (class, capability, ring, role, parallelism)
def derive_archetype(path: Path, card: dict) -> dict:
    p = str(path)
    # TIER inference
    if "/organs/" in p:
        tier = "ORGAN"
    elif "/harnesses/" in p or "/agents/" in p:
        tier = "Warga"
    elif "/forge/" in p:
        tier = "FI"
    elif "/federation/" in p:
        tier = "FEDERATION"
    elif "/identity/" in p:
        tier = "IDENTITY"
    elif "/roles/" in p:
        tier = "ROLE"
    elif "/functions/" in p:
        tier = "FUNCTION"
    elif p.endswith("aaa-cockpit.json"):
        tier = "COCKPIT"
    else:
        tier = "UNKNOWN"

    # CLASS inference from card content
    cls = card.get("class") or card.get("governance_class") or card.get("agent_class") or "Warga"
    if isinstance(cls, list):
        cls = cls[0] if cls else "Warga"

    # ROLE-specific capability
    role_lower = (card.get("role") or card.get("name") or card.get("id") or path.stem).lower()

    # Capability inference
    if "judge" in role_lower or "apex" in role_lower or "888" in path.name:
        capability = "JUDGE"
    elif "build" in role_lower or "forge" in role_lower or "coder" in role_lower or "code" in role_lower:
        capability = "BUILD"
    elif "memory" in role_lower or "asi" in role_lower or "555" in path.name or "vault" in role_lower:
        capability = "REMEMBER"
    elif "observe" in role_lower or "frame" in role_lower or "meta" in role_lower:
        capability = "OBSERVE"
    elif "witness" in role_lower or "audit" in role_lower or "verify" in role_lower:
        capability = "VERIFY"
    elif "telegram" in role_lower or "kirim" in role_lower or "bot" in role_lower or "hermes" in role_lower:
        capability = "ACT"
    elif "code" in role_lower:
        capability = "BUILD"
    elif "judge" in role_lower:
        capability = "JUDGE"
    elif (
        "searxng" in role_lower
        or "search" in role_lower
        or "store" in role_lower
        or "data" in role_lower
        or "graphiti" in role_lower
        or "qdrant" in role_lower
    ):
        capability = "STORE"
    else:
        # Default per tier
        capability = {
            "ORGAN": "OBSERVE",
            "Warga": "BUILD",
            "FI": "BUILD",
            "FEDERATION": "OBSERVE",
            "IDENTITY": "WITNESS",
            "ROLE": "VERIFY",
            "FUNCTION": "ACT",
            "COCKPIT": "OBSERVE",
            "UNKNOWN": "VERIFY",
        }[tier]

    # Ring inference
    if capability == "JUDGE":
        ring, role, parallel = ("judicator", "inner", "single-threaded")
    elif capability == "BUILD":
        ring, role, parallel = ("generator", "outer", "multi-model")
    elif capability == "REMEMBER":
        ring, role, parallel = ("archivist", "anchor", "append-only")
    elif capability == "OBSERVE":
        ring, role, parallel = ("observer", "metabolic", "pipeline")
    elif capability == "VERIFY":
        ring, role, parallel = ("auditor", "inner", "single-threaded")
    elif capability == "ACT":
        ring, role, parallel = ("executor", "outer", "parallel")
    elif capability == "STORE":
        ring, role, parallel = ("store", "outer", "stream")
    else:
        ring, role, parallel = ("unassigned", "neutral", "none")

    return {
        "tier": tier,
        "class": cls,
        "capability": capability,
        "cognitiveRing": ring,
        "thermodynamicRole": role,
        "parallelism": parallel,
    }


def load_preserving_order(path: Path):
    with path.open() as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def dump_preserving_order(doc, path: Path):
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


APEX_CANON = "/root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md"
GOVERNANCE_CHAIN = "BUILD → VERIFY → JUDGE → SEAL → ACT → WITNESS"
INVARIANT = "CAPABILITY ≠ AUTHORITY"
DOCTRINE = "Govern capabilities, not implementations."
MOTTO = "DITEMPA BUKAN DIBERI"
NOW = datetime.now(timezone.utc).isoformat()


def main():
    applied = []
    skipped = []
    audit_path = Path("/root/AAA/reports/apex-zen-upgrade-2026-09-30/all_agents_aligned_audit.json")

    audit = {
        "applied_at": NOW,
        "applied_by": "333-AGI (FI-001) under user directive 'align all AAA agents'",
        "files_total": len(CARDS),
        "applied": [],
        "skipped": [],
    }

    for path in CARDS:
        try:
            card = load_preserving_order(path)
        except Exception as e:
            skipped.append((str(path), f"load error: {e}"))
            continue

        # Skip if apex_zen + apexMasterSeal already present
        if card.get("apex_zen") and card.get("apexMasterSeal"):
            skipped.append((str(path), "already aligned"))
            continue

        archetype = derive_archetype(path, card)
        card_id = card.get("id", path.stem)

        # Add apexMasterSeal (synthesized)
        if not card.get("apexMasterSeal"):
            card["apexMasterSeal"] = OrderedDict(
                [
                    ("cognitiveRing", archetype["cognitiveRing"]),
                    ("thermodynamicRole", archetype["thermodynamicRole"]),
                    ("ringPlacement", archetype["parallelism"]),  # alias for parallelism
                    ("parallelism", archetype["parallelism"]),
                    ("shadowAcknowledged", []),
                    (
                        "jituGate",
                        OrderedDict(
                            [
                                ("requiresJitu", False),
                                ("jituTriggerPatterns", []),
                                ("autoAbortWithoutJitu", True),
                            ]
                        ),
                    ),
                    ("doctrine", MOTTO),
                    (
                        "hassabisInversion",
                        OrderedDict(
                            [
                                (
                                    "principle",
                                    "Role over Model. Intelligence is constraint satisfaction, not simulation.",
                                ),
                                ("ringPlacement", archetype["parallelism"]),
                                ("parallelism", archetype["parallelism"]),
                                ("shadowAcknowledged", []),
                            ]
                        ),
                    ),
                    ("sealRef", f"VAULT999/apex-zen-aligned-{NOW}"),
                    ("ratifiedAt", NOW),
                    ("auto_aligned_by", "333-AGI (FI-001) under user directive"),
                    ("auto_aligned_reason", f"synthesized from tier={archetype['tier']}, class={archetype['class']}"),
                ]
            )

        # Add apex_zen (canonical anchor)
        if not card.get("apex_zen"):
            card["apex_zen"] = OrderedDict(
                [
                    ("canonical_ref", APEX_CANON),
                    ("governance_chain", GOVERNANCE_CHAIN),
                    ("invariant", INVARIANT),
                    ("doctrine", DOCTRINE),
                    ("motto", MOTTO),
                    ("capability", archetype["capability"]),
                    ("lane", card.get("lane") or card_id),
                    ("auto_aligned_at", NOW),
                    ("auto_aligned_tier", archetype["tier"]),
                    ("auto_aligned_class", archetype["class"]),
                ]
            )

        # Atomic write
        backup = path.with_suffix(path.suffix + f".bak-pre-align-{NOW[:10]}")
        if not backup.exists():
            backup.write_text(path.read_text())

        tmp = path.with_suffix(path.suffix + ".tmp")
        dump_preserving_order(card, tmp)
        tmp.replace(path)

        applied.append(str(path))
        audit["applied"].append(
            {
                "path": str(path),
                "id": card_id,
                "tier": archetype["tier"],
                "class": archetype["class"],
                "capability": archetype["capability"],
                "cognitiveRing": archetype["cognitiveRing"],
            }
        )

    # Skipped summary
    for p, reason in skipped:
        audit["skipped"].append({"path": p, "reason": reason})

    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")

    print(f"=== Apex-Zen alignment: {len(applied)} cards updated, {len(skipped)} skipped ===")
    print(f"Audit: {audit_path}")
    for entry in audit["applied"]:
        print(
            f"  ✅ {entry['id']:24s}  tier={entry['tier']:11s}  class={entry['class']:10s}  capability={entry['capability']:9s}  ring={entry['cognitiveRing']}"
        )
    print(f"\n--- Skipped ({len(skipped)}) ---")
    for entry in audit["skipped"]:
        print(f"  ⚠ {entry['reason']:30s} {entry['path']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
