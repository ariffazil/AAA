#!/usr/bin/env python3
"""
ACD CLI — acd dream
Thin CLI wrapper around ACD core. Bounded, shadow, auditable.
"""

import sys
import os
import json
import uuid
from pathlib import Path

# Add ACD to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.acd_core import ACDCore, VERSION


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("--help", "-h", "help"):
        print_help()
        return

    # Canonical UX: `acd dream <sub>` — normalize verb; bare `/dream` runs one cycle.
    had_dream = bool(args) and args[0] == "dream"
    if had_dream:
        args = args[1:]

    known = ("status", "once", "inspect", "audit", "propose", "help", "--help", "-h")
    if had_dream and (not args or args[0] not in known):
        args = ["once"] + args
    elif not args or args[0] in ("--help", "-h", "help"):
        print_help()
        return

    command = args[0]
    core = ACDCore()

    if command == "status":
        print(json.dumps(core.status(), indent=2))

    elif command == "once" or command == "dream":
        # One bounded shadow cycle
        request = {
            "request_id": str(uuid.uuid4()),
            "cycle_id": str(uuid.uuid4()),
            "requested_by": "cli",
            "requesting_agent": "acd_cli",
            "command": "dream",
            "mode": "shadow",
            "shadow": True,
            "purpose": args[1] if len(args) > 1 else "general exploration",
            "scope": "bounded_shadow",
            "horizon": "short",
            "evidence_refs": [],
            "constraints": ["shadow_mode", "no_external_actions"],
            "compute_budget": 5,
            "created_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "contract_version": VERSION,
        }
        receipt = core.dream(request)
        print(json.dumps(receipt, indent=2, default=str))
        # Exit non-zero on failure
        if receipt.get("runtime_status") != "COMPLETED":
            sys.exit(1)

    elif command == "inspect":
        if len(args) < 2:
            print("Usage: acd dream inspect <cycle_id>")
            sys.exit(1)
        cycle_id = args[1]
        receipts_dir = Path(os.environ.get("ACD_RECEIPTS_DIR", "/root/AAA/ACD/receipts"))
        for f in sorted(receipts_dir.glob(f"*_{cycle_id[:8]}*"), reverse=True):
            print(f.read_text())
            return
        print(f"No receipt found for cycle_id matching {cycle_id}")
        sys.exit(1)

    elif command == "audit":
        if len(args) < 2:
            print("Usage: acd dream audit <cycle_id>")
            sys.exit(1)
        cycle_id = args[1]
        receipts_dir = Path(os.environ.get("ACD_RECEIPTS_DIR", "/root/AAA/ACD/receipts"))
        for f in sorted(receipts_dir.glob(f"*_{cycle_id[:8]}*"), reverse=True):
            receipt = json.loads(f.read_text())
            from core.acd_core import _hash as _acd_hash
            expected = _acd_hash({k: v for k, v in receipt.items() if k != "content_hash"})
            hash_ok = receipt.get("content_hash") == expected
            # Validate ontology
            valid_ontologies = {"OBSERVED", "INFERRED", "SIMULATED", "NORMATIVE", "UNKNOWN"}
            ontology_ok = receipt.get("ontology") in valid_ontologies
            # Validate no external actions
            no_actions = receipt.get("external_actions_executed", 0) == 0
            # Validate shadow
            shadow_ok = receipt.get("shadow") == True
            print(json.dumps({
                "cycle_id": cycle_id,
                "ontology_valid": ontology_ok,
                "no_external_actions": no_actions,
                "shadow_enforced": shadow_ok,
                "content_hash_valid": hash_ok,
                "constitutional_verdict": receipt.get("constitutional_verdict"),
                "audit_result": "PASS" if all([ontology_ok, no_actions, shadow_ok, hash_ok]) else "FAIL",
            }, indent=2))
            return
        print(f"No receipt found for cycle_id matching {cycle_id}")
        sys.exit(1)

    elif command == "propose":
        # Create a promotion petition from the latest cycle. Never applied — HELD.
        receipts_dir = Path(os.environ.get("ACD_RECEIPTS_DIR", "/root/AAA/ACD/receipts"))
        files = sorted(receipts_dir.glob("*.json"), reverse=True)
        if not files:
            print("No receipts to petition from. Run `acd dream` first.")
            sys.exit(1)
        receipt = json.loads(files[0].read_text())
        branches = receipt.get("branches") or [{}]
        petition = {
            "petition_id": str(uuid.uuid4()),
            "cycle_id": receipt.get("cycle_id", "unknown"),
            "branch_id": branches[-1].get("branch_id", "unknown"),
            "current_status": "CHALLENGED",
            "requested_status": "DECISION_CANDIDATE",
            "burden_of_proof": "Independent review of branch counterfactuals and retained contradictions required before consideration.",
            "supporting_witnesses": ["receipt:" + str(receipt.get("receipt_id"))],
            "residual_risk": "UNKNOWN — bounded deterministic shadow only; no world model",
            "adjudicator": "HUMAN_SOVEREIGN",
            "created_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "held": True,
            "route": "arif_judge -> AIO -> F13 (not applied by ACD)",
        }
        pet_dir = receipts_dir / "petitions"
        pet_dir.mkdir(parents=True, exist_ok=True)
        pet_path = pet_dir / (petition["petition_id"] + ".json")
        pet_path.write_text(json.dumps(petition, indent=2))
        print(json.dumps({
            "status": "888_HOLD",
            "petition_id": petition["petition_id"],
            "petition_path": str(pet_path),
            "message": "Petition created. Not applied. Requires arif_judge verdict + human sovereignty.",
            "contract_version": VERSION,
        }, indent=2))
        sys.exit(0)

    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)


def print_help():
    print(f"""ACD — Constitutional Dream Engine (v{VERSION})

Usage: acd dream <command> [args]

Commands:
  dream [purpose]       Run one bounded shadow cycle (default)
  once [purpose]        Same as dream
  status                Report core health
  inspect <cycle_id>    Read an existing cycle
  audit <cycle_id>      Validate provenance and schema
  propose               Create promotion petition (888_HOLD)
  help                  Show this help

Non-negotiable:
  - Shadow mode only (no external actions)
  - SIMULATED ontology default
  - No self-ratification
  - Production activation requires 888_HOLD
""")


if __name__ == "__main__":
    main()
