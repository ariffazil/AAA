#!/usr/bin/env python3
"""
Human Reality Classifier & Gate — Phase 1 & 2 of APEX::HUMAN_REALITY_GRAPH_ACTIVATION::2026-09-13.

AUTHORITY : ARIF (F13 Sovereign)
DOCTRINE  : /root/AAA/prompts/HUMAN_REALITY_GRAPH_ACTIVATION_20260913.md
SPEC      : /root/AAA/canon/REALITY_CONSEQUENCE_OBJECTS_SPEC_v1.md
GATE      : /root/AAA/scripts/reality_object_gate.py

PRIMARY LAW ENFORCED:
  A name is not a human reality object.
  A mention is not a commitment.
  A memory is not a consequence.
  A person enters governance only when reality and consequence exist.

CLASSIFICATION TAXONOMY (H0..H5):
  H0 = Reference Only      (Archive; no HRO created)
  H1 = Stakeholder         (Contextual attention / recipient)
  H2 = Decision Owner      (Operational ownership)
  H3 = Consequence Owner   (Carries organizational/board risk)
  H4 = Strategic Actor     (National/industry leadership)
  H5 = Sovereign Actor     (ARIF — F13 Sovereign)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FATAL: pyyaml required", file=sys.stderr)
    sys.exit(1)

PEOPLE_DIR = Path("/root/memory/people")
OUT_DIR = Path("/root/AAA/state/reality_objects")
MANIFEST_PATH = OUT_DIR / "human_entity_manifest.json"

# Known entity mapping based on canon & institutional records
CANONICAL_PEOPLE: dict[str, dict] = {
    "ARIF": {
        "tier": "H5",
        "role": "Sovereign Principal & Architect",
        "stakeholders": ["board", "corporate_governance", "federation"],
        "has_active_consequence": True,
        "what_matters": "Preserve human sovereignty, family wellbeing, corporate career standing, and operational AI integrity.",
        "attention_cost": "HIGH",
        "consequence_class": "STRATEGIC",
    },
    "AHMAD-FAISAL-BAKAR": {
        "tier": "H3",
        "role": "Former VP Exploration (PETRONAS Carigali)",
        "stakeholders": ["petronas_exploration", "institutional_witnesses"],
        "has_active_consequence": True,
        "what_matters": "Institutional witness for LAW-FORGE-BALANCE (act of heat met by act of care; protect authorship integrity).",
        "attention_cost": "LOW",
        "consequence_class": "REPUTATIONAL",
    },
    "TENGKU-TAUFIK": {
        "tier": "H4",
        "role": "President & Group CEO, PETRONAS",
        "stakeholders": ["petronas_board", "malaysian_energy_council"],
        "has_active_consequence": True,
        "what_matters": "Corporate direction: capital discipline, energy transition, and governed AI adoption across enterprise.",
        "attention_cost": "MEDIUM",
        "consequence_class": "STRATEGIC",
    },
    "SYED": {
        "tier": "H2",
        "role": "Collaborator / Technical Partner",
        "stakeholders": ["shared_initiatives"],
        "has_active_consequence": True,
        "what_matters": "Symmetric technical collaboration; avoid unilateral epistemic drift.",
        "attention_cost": "MEDIUM",
        "consequence_class": "OPERATIONAL",
    },
    "JUKHRIS": {
        "tier": "H1",
        "role": "Domain Stakeholder",
        "stakeholders": ["domain_team"],
        "has_active_consequence": False,
        "what_matters": "Technical interaction; no direct governance consequence.",
        "attention_cost": "LOW",
        "consequence_class": "PERSONAL",
    },
    "ALIFF": {
        "tier": "H1",
        "role": "Professional Stakeholder",
        "stakeholders": ["colleagues"],
        "has_active_consequence": False,
        "what_matters": "Peer collaboration context.",
        "attention_cost": "LOW",
        "consequence_class": "PERSONAL",
    },
    "IZZU": {
        "tier": "H1",
        "role": "Professional Stakeholder",
        "stakeholders": ["colleagues"],
        "has_active_consequence": False,
        "what_matters": "Peer collaboration context.",
        "attention_cost": "LOW",
        "consequence_class": "PERSONAL",
    },
}

# Family members: Protected Sanctuary Invariant
FAMILY_PEOPLE = ["ABBAH", "MAK", "FARIDAH", "FAZIL", "FAMILY", "NABILAH"]


def discover_entities() -> list[dict]:
    entities = []
    if not PEOPLE_DIR.exists():
        return entities

    for item in PEOPLE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            name = item.name.upper()
            if name in FAMILY_PEOPLE or name == "FAMILY":
                entities.append({
                    "name": name,
                    "tier": "H1",
                    "category": "FAMILY_SANCTUARY",
                    "note": "Sanctuary Invariant protected — no external operational CRO",
                    "is_hro_candidate": False,
                })
            elif name in CANONICAL_PEOPLE:
                meta = CANONICAL_PEOPLE[name]
                entities.append({
                    "name": name,
                    "tier": meta["tier"],
                    "category": "CANONICAL",
                    "meta": meta,
                    "is_hro_candidate": meta["has_active_consequence"],
                })
            else:
                entities.append({
                    "name": name,
                    "tier": "H0",
                    "category": "REFERENCE_ONLY",
                    "note": "Mentioned entity without active consequence chain",
                    "is_hro_candidate": False,
                })
    return entities


def generate_manifest(entities: list[dict]) -> dict:
    summary = {
        "schema": "arifos.human_manifest.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_entities_discovered": len(entities),
        "tiers": {
            "H5_SOVEREIGN": [e["name"] for e in entities if e["tier"] == "H5"],
            "H4_STRATEGIC": [e["name"] for e in entities if e["tier"] == "H4"],
            "H3_CONSEQUENCE_OWNER": [e["name"] for e in entities if e["tier"] == "H3"],
            "H2_DECISION_OWNER": [e["name"] for e in entities if e["tier"] == "H2"],
            "H1_STAKEHOLDER": [e["name"] for e in entities if e["tier"] == "H1"],
            "H0_REFERENCE_ONLY": [e["name"] for e in entities if e["tier"] == "H0"],
        },
        "hro_candidates_count": len([e for e in entities if e.get("is_hro_candidate")]),
        "sanctuary_protected_count": len([e for e in entities if e.get("category") == "FAMILY_SANCTUARY"]),
        "entities": entities,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, "w") as f:
        json.dump(summary, f, indent=2)
    return summary


def main():
    parser = argparse.ArgumentParser(description="Human Reality Classifier (APEX Phase 1 & 2)")
    parser.add_argument("--report", action="store_true", help="Print summary report")
    args = parser.parse_args()

    entities = discover_entities()
    manifest = generate_manifest(entities)

    print(f"Human Reality Classifier — Discovered {manifest['total_entities_discovered']} entities")
    print(f"  H5 Sovereign Actor         : {len(manifest['tiers']['H5_SOVEREIGN'])} ({', '.join(manifest['tiers']['H5_SOVEREIGN'])})")
    print(f"  H4 Strategic Actors        : {len(manifest['tiers']['H4_STRATEGIC'])}")
    print(f"  H3 Consequence Owners      : {len(manifest['tiers']['H3_CONSEQUENCE_OWNER'])}")
    print(f"  H2 Decision Owners         : {len(manifest['tiers']['H2_DECISION_OWNER'])}")
    print(f"  H1 Stakeholders / Sanctuary : {len(manifest['tiers']['H1_STAKEHOLDER'])}")
    print(f"  H0 Reference Only          : {len(manifest['tiers']['H0_REFERENCE_ONLY'])}")
    print(f"\nGoverned Reality Invariant Enforced:")
    print(f"  Qualified HRO Candidates   : {manifest['hro_candidates_count']}")
    print(f"  Sanctuary Invariant Shield : {manifest['sanctuary_protected_count']} (Protected from external CRO)\n")
    print(f"Manifest written to: {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
