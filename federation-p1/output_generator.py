#!/usr/bin/env python3
"""
output_generator.py — Generate all JSON outputs for the federation P1.

Produces:
- tools.json for each organ
- resources.json for each organ
- prompts.json for each organ
- federation_envelope.json
- replay_receipt.json
- manifest signatures + sha256 pins
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "/root/federation-p1")
sys.path.insert(0, "/root/federation-p1/prompts")
sys.path.insert(0, "/root/federation-p1/resources")

# Import from the actual module files
from manifest_generator import GENERATORS, sign_manifest, canonical_json
from canonical_prompts import ALL_PROMPTS
from canonical_resources import ALL_RESOURCES, generate_resource_content

OUTPUT_DIR = Path("/root/federation-p1/outputs")
VERSION = "2026.06.28"


def sha256_content(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False, ensure_ascii=False))
    print(f"  → {path}")


def generate_organ_outputs(organ: str, manifest: dict):
    """Generate tools.json, resources.json, prompts.json for an organ."""
    out_dir = OUTPUT_DIR / organ

    # tools.json
    tools_output = {
        "organ": organ,
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tool_count": len(manifest["tools"]),
        "tools": manifest["tools"],
    }
    write_json(out_dir / "tools.json", tools_output)

    # resources.json
    resources_output = {
        "organ": organ,
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "resource_count": len(manifest["resources"]),
        "resources": manifest["resources"],
    }
    write_json(out_dir / "resources.json", resources_output)

    # prompts.json
    prompts_output = {
        "organ": organ,
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "prompt_count": len(manifest["prompts"]),
        "prompts": manifest["prompts"],
    }
    write_json(out_dir / "prompts.json", prompts_output)


def generate_federation_envelope():
    """Generate a sample federation envelope."""
    envelope = {
        "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "from_organ": "wealth",
        "to_organ": "arifos",
        "intent": "Request constitutional judgment on capital allocation proposal",
        "capability": "wealth_arifos_handoff",
        "authority_required": "888_HOLD",
        "context_capsule": {
            "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "session_id": "session-2026-06-28-001",
            "origin_organ": "wealth",
            "decision_class": "C3",
            "epistemic_state": "DERIVED",
            "timebox": "PT1H",
            "payload_refs": [
                "afwealth://reality/context",
                "afwealth://risk/thresholds",
            ],
        },
        "translation_cards": [
            {
                "card_id": "dtc-wealth-arifos-allocation-v1",
                "from_organ": "wealth",
                "to_organ": "arifos",
                "source_measure": "allocation_memo",
                "target_assumption": "judge_packet",
                "transform_rule": "Convert advisory capital verdict into governed packet with blast radius, reversibility, downside, weakest stakeholder exposure, and receipt references",
                "uncertainty_mapping": {
                    "p10": 0.15,
                    "p50": 0.40,
                    "p90": 0.70,
                },
                "evidence_refs": [
                    "afwealth://reality/context",
                    "receipt://wealth/2026-06-28/abc123",
                ],
                "version": VERSION,
            }
        ],
        "payload": {
            "proposal": "Allocate RM50,000 to emergency fund",
            "verdict": "ADVISORY_PROCEED",
            "blast_radius": "LOCAL",
            "reversibility": "FULLY_REVERSIBLE",
            "downside_p10": 0.05,
            "weakest_stakeholder": "arif",
            "confidence": 0.75,
        },
        "manifest_refs": [
            sha256_content(canonical_json(GENERATORS["wealth"]())),
            sha256_content(canonical_json(GENERATORS["arifos"]())),
        ],
        "hmac_signature": "pending_hmac_signature",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(OUTPUT_DIR / "federation_envelope.json", envelope)


def generate_replay_receipt():
    """Generate a sample replay receipt."""
    receipt = {
        "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "started_at": "2026-06-28T10:00:00Z",
        "ended_at": "2026-06-28T10:05:00Z",
        "caller": "opencode-agent",
        "steps": [
            {
                "organ": "wealth",
                "surface": "tool",
                "name": "wealth_compute_npv",
                "input_hash": sha256_content("npv_input"),
                "output_hash": sha256_content("npv_output"),
                "status": "OK",
                "duration_ms": 150,
                "manifest_ref": sha256_content(canonical_json(GENERATORS["wealth"]())),
            },
            {
                "organ": "wealth",
                "surface": "tool",
                "name": "wealth_risk_downside_loop",
                "input_hash": sha256_content("risk_input"),
                "output_hash": sha256_content("risk_output"),
                "status": "OK",
                "duration_ms": 200,
                "manifest_ref": sha256_content(canonical_json(GENERATORS["wealth"]())),
            },
            {
                "organ": "wealth",
                "surface": "tool",
                "name": "wealth_arifos_handoff_loop",
                "input_hash": sha256_content("handoff_input"),
                "output_hash": sha256_content("handoff_output"),
                "status": "OK",
                "duration_ms": 100,
                "manifest_ref": sha256_content(canonical_json(GENERATORS["wealth"]())),
            },
            {
                "organ": "arifos",
                "surface": "tool",
                "name": "arif_judge",
                "input_hash": sha256_content("judge_input"),
                "output_hash": sha256_content("judge_output"),
                "status": "OK",
                "duration_ms": 300,
                "manifest_ref": sha256_content(canonical_json(GENERATORS["arifos"]())),
            },
        ],
        "result_hash": sha256_content("final_result"),
        "previous_receipt_hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "receipt_hash": sha256_content("this_receipt"),
        "hmac_signature": "pending_hmac_signature",
    }
    write_json(OUTPUT_DIR / "replay_receipt.json", receipt)


def generate_manifest_pins():
    """Generate manifest_pins.json with SHA256 hashes of all manifests."""
    pins = {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pins": {},
    }
    for organ in GENERATORS:
        manifest_path = Path(f"/root/federation-p1/manifests/{organ}/manifest.json")
        if manifest_path.exists():
            content = manifest_path.read_text()
            pins["pins"][organ] = {
                "sha256": sha256_content(content),
                "path": str(manifest_path),
                "size_bytes": len(content),
            }
    write_json(OUTPUT_DIR / "manifest_pins.json", pins)


def main():
    print("═══ Federation P1 Output Generator ═══\n")

    # Generate organ manifests and outputs
    for organ, gen in GENERATORS.items():
        print(f"\n── {organ.upper()} ──")
        manifest = sign_manifest(gen())
        generate_organ_outputs(organ, manifest)

    # Generate federation envelope
    print(f"\n── FEDERATION ENVELOPE ──")
    generate_federation_envelope()

    # Generate replay receipt
    print(f"\n── REPLAY RECEIPT ──")
    generate_replay_receipt()

    # Generate manifest pins
    print(f"\n── MANIFEST PINS ──")
    generate_manifest_pins()

    print(f"\n═══ All outputs in {OUTPUT_DIR} ═══")


if __name__ == "__main__":
    main()
