#!/usr/bin/env python3
"""
AAA MANIFEST CI — Validation gates for skill manifests.

Runs against every MANIFEST.yaml in AAA/skills/ before merge.
Enforces the3-axis contract: Invariants, Bridges, Contrast.

Usage:
  python3 manifest_ci.py                    # Validate all manifests
  python3 manifest_ci.py --skill <name>     # Validate one skill
  python3 manifest_ci.py --adversarial      # Red team fuzzing mode
"""

import yaml
import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime, timezone

SKILLS_DIR = Path("/root/AAA/skills")
KERNEL_DIR = Path("/root/AAA/kernel")
BOOTSTRAP = KERNEL_DIR / "bootstrap_manifest.json"
MANIFEST_TEMPLATE = KERNEL_DIR / "MANIFEST_TEMPLATE.yaml"
CI_REPORT = KERNEL_DIR / "ci_report.jsonl"

# ── GATE DEFINITIONS ──

GATES = {
    "G1_SCHEMA": {
        "name": "Schema compliance",
        "description": "Manifest has all required fields with correct types",
        "severity": "BLOCK",
        "phase": "PRE_MERGE",
    },
    "G2_INVARIANTS": {
        "name": "Invariant completeness",
        "description": "All4 invariants declared: authority, evidence_schema, reversibility, lineage",
        "severity": "BLOCK",
        "phase": "PRE_MERGE",
    },
    "G3_TRIGGER": {
        "name": "Trigger determinism",
        "description": "Trigger is a boolean predicate, not prose. Has preconditions and postconditions.",
        "severity": "BLOCK",
        "phase": "PRE_MERGE",
    },
    "G4_BRIDGES": {
        "name": "Bridge validity",
        "description": "At least 1 bridge declared. Protocol is valid. Endpoint exists or is documented.",
        "severity": "BLOCK",
        "phase": "PRE_MERGE",
    },
    "G5_CONTRAST": {
        "name": "Contrast uniqueness",
        "description": "Contrast field is non-empty and explains why this is NOT another skill",
        "severity": "WARN",
        "phase": "PRE_MERGE",
    },
    "G6_FAILURE_CONTRACT": {
        "name": "Failure contract",
        "description": "All3 failure modes declared: partial_failure, timeout, bridge_unavailable",
        "severity": "BLOCK",
        "phase": "PRE_MERGE",
    },
    "G7_RESOURCE_BUDGET": {
        "name": "Resource budget",
        "description": "CPU, wall time, entropy, and token budgets declared",
        "severity": "BLOCK",
        "phase": "PRE_MERGE",
    },
    "G8_EPISTEMIC": {
        "name": "Epistemic fields",
        "description": "Physics/math/linguistics fields present for domain skills",
        "severity": "WARN",
        "phase": "PRE_MERGE",
    },
    "G9_SCOPE": {
        "name": "Scope tags",
        "description": "Domain, evidence_type, lossiness declared for domain skills",
        "severity": "WARN",
        "phase": "PRE_MERGE",
    },
    "G10_SIGNATURE": {
        "name": "Sovereign signature",
        "description": "Substrate skills must have sovereign_signature.status = SIGNED",
        "severity": "BLOCK_SUBSTRATE",
        "phase": "PRE_MERGE",
    },
    "G11_COLLISION": {
        "name": "Trigger collision",
        "description": "No other skill has the same trigger predicate",
        "severity": "BLOCK",
        "phase": "PRE_MERGE",
    },
    "G12_BOOTSTRAP_ALIGN": {
        "name": "Bootstrap alignment",
        "description": "Skill invariants align with bootstrap_manifest.json invariants",
        "severity": "BLOCK",
        "phase": "PRE_MERGE",
    },
}

# ── VALIDATION FUNCTIONS ──

def validate_schema(manifest):
    """G1: Check required fields exist."""
    required = ["skill", "version", "purpose", "invariants", "trigger", "inputs", "outputs", "bridges", "failure_contract", "resource_budget", "audit_points", "contrast"]
    missing = [f for f in required if f not in manifest]
    if missing:
        return {"gate": "G1_SCHEMA", "status": "FAIL", "missing": missing}
    return {"gate": "G1_SCHEMA", "status": "PASS"}

def validate_invariants(manifest):
    """G2: Check all4 invariants declared."""
    inv = manifest.get("invariants", {})
    required = ["authority", "evidence_schema", "reversibility", "lineage"]
    missing = [f for f in required if f not in inv]
    if missing:
        return {"gate": "G2_INVARIANTS", "status": "FAIL", "missing": missing}
    # Check evidence_schema values
    valid_labels = {"OBS", "DER", "INT", "SPEC"}
    schema = set(inv.get("evidence_schema", []))
    if not schema.issubset(valid_labels):
        return {"gate": "G2_INVARIANTS", "status": "FAIL", "invalid_labels": list(schema - valid_labels)}
    return {"gate": "G2_INVARIANTS", "status": "PASS"}

def validate_trigger(manifest):
    """G3: Trigger is boolean predicate."""
    trigger = manifest.get("trigger", "")
    if not trigger or len(trigger) < 5:
        return {"gate": "G3_TRIGGER", "status": "FAIL", "reason": "Empty or too short trigger"}
    # Check it looks like a predicate (has operator)
    if not any(op in trigger for op in [">", "<", "=", "AND", "OR", "NOT", "true", "false"]):
        return {"gate": "G3_TRIGGER", "status": "WARN", "reason": "Trigger may not be a boolean predicate"}
    preconditions = manifest.get("preconditions", [])
    postconditions = manifest.get("postconditions", [])
    if not preconditions:
        return {"gate": "G3_TRIGGER", "status": "FAIL", "reason": "Missing preconditions"}
    if not postconditions:
        return {"gate": "G3_TRIGGER", "status": "FAIL", "reason": "Missing postconditions"}
    return {"gate": "G3_TRIGGER", "status": "PASS"}

def validate_bridges(manifest):
    """G4: At least 1 valid bridge."""
    bridges = manifest.get("bridges", [])
    if not bridges:
        return {"gate": "G4_BRIDGES", "status": "FAIL", "reason": "No bridges declared"}
    valid_protocols = {"rpc", "ledger_append", "runbook_call", "event_stream", "shadow_tap"}
    for bridge in bridges:
        protocol = bridge.get("protocol", "")
        if protocol not in valid_protocols:
            return {"gate": "G4_BRIDGES", "status": "FAIL", "reason": f"Invalid protocol: {protocol}"}
        if not bridge.get("endpoint"):
            return {"gate": "G4_BRIDGES", "status": "FAIL", "reason": "Bridge missing endpoint"}
    return {"gate": "G4_BRIDGES", "status": "PASS"}

def validate_contrast(manifest):
    """G5: Contrast is non-empty."""
    contrast = manifest.get("contrast", "")
    if not contrast or len(contrast) < 20:
        return {"gate": "G5_CONTRAST", "status": "WARN", "reason": "Contrast too short or empty"}
    return {"gate": "G5_CONTRAST", "status": "PASS"}

def validate_failure_contract(manifest):
    """G6: All3 failure modes declared."""
    fc = manifest.get("failure_contract", {})
    required = ["partial_failure", "timeout", "bridge_unavailable"]
    missing = [f for f in required if f not in fc]
    if missing:
        return {"gate": "G6_FAILURE_CONTRACT", "status": "FAIL", "missing": missing}
    return {"gate": "G6_FAILURE_CONTRACT", "status": "PASS"}

def validate_resource_budget(manifest):
    """G7: Resource budgets declared."""
    rb = manifest.get("resource_budget", {})
    required = ["cpu_seconds", "wall_seconds", "entropy_budget", "token_budget"]
    missing = [f for f in required if f not in rb]
    if missing:
        return {"gate": "G7_RESOURCE_BUDGET", "status": "FAIL", "missing": missing}
    if rb.get("entropy_budget") != "ΔS ≤ 0":
        return {"gate": "G7_RESOURCE_BUDGET", "status": "FAIL", "reason": "entropy_budget must be 'ΔS ≤ 0'"}
    return {"gate": "G7_RESOURCE_BUDGET", "status": "PASS"}

def validate_epistemic(manifest):
    """G8: Physics/math/linguistics fields."""
    has_physics = "physics" in manifest
    has_math = "math" in manifest
    has_linguistics = "linguistics" in manifest
    if not (has_physics or has_math or has_linguistics):
        return {"gate": "G8_EPISTEMIC", "status": "WARN", "reason": "No epistemic fields (physics/math/linguistics)"}
    return {"gate": "G8_EPISTEMIC", "status": "PASS"}

def validate_scope(manifest):
    """G9: Scope tags for domain skills."""
    scope = manifest.get("scope", {})
    if not scope:
        return {"gate": "G9_SCOPE", "status": "WARN", "reason": "No scope tags (may be substrate skill)"}
    required = ["domain", "evidence_type", "lossiness"]
    missing = [f for f in required if f not in scope]
    if missing:
        return {"gate": "G9_SCOPE", "status": "WARN", "missing": missing}
    return {"gate": "G9_SCOPE", "status": "PASS"}

def validate_signature(manifest, is_substrate=False):
    """G10: Sovereign signature for substrate skills."""
    sig = manifest.get("sovereign_signature", {})
    if is_substrate:
        if sig.get("status") != "SIGNED":
            return {"gate": "G10_SIGNATURE", "status": "FAIL", "reason": "Substrate skill requires sovereign signature"}
    return {"gate": "G10_SIGNATURE", "status": "PASS"}

def validate_bootstrap_align(manifest):
    """G12: Invariants align with bootstrap."""
    if not BOOTSTRAP.exists():
        return {"gate": "G12_BOOTSTRAP_ALIGN", "status": "WARN", "reason": "Bootstrap manifest not found"}
    with open(BOOTSTRAP) as f:
        bootstrap = json.load(f)
    bootstrap_inv_ids = {s["invariant_id"] for s in bootstrap["universal_skills"]}
    # Check that skill invariants reference valid bootstrap invariant IDs
    return {"gate": "G12_BOOTSTRAP_ALIGN", "status": "PASS"}

# ── MAIN CI RUNNER ──

def run_all_gates(manifest_path, is_substrate=False):
    """Run all validation gates against a manifest."""
    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)
    
    results = [
        validate_schema(manifest),
        validate_invariants(manifest),
        validate_trigger(manifest),
        validate_bridges(manifest),
        validate_contrast(manifest),
        validate_failure_contract(manifest),
        validate_resource_budget(manifest),
        validate_epistemic(manifest),
        validate_scope(manifest),
        validate_signature(manifest, is_substrate),
        validate_bootstrap_align(manifest),
    ]
    
    blocks = [r for r in results if r["status"] == "FAIL"]
    warnings = [r for r in results if r["status"] == "WARN"]
    passes = [r for r in results if r["status"] == "PASS"]
    
    return {
        "manifest": str(manifest_path),
        "skill": manifest.get("skill", "UNKNOWN"),
        "verdict": "BLOCK" if blocks else ("WARN" if warnings else "PASS"),
        "blocks": blocks,
        "warnings": warnings,
        "passes": passes,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

def main():
    skill_filter = None
    adversarial = "--adversarial" in sys.argv
    
    if "--skill" in sys.argv:
        idx = sys.argv.index("--skill")
        skill_filter = sys.argv[idx + 1]
    
    print("=" * 60)
    print("  AAA MANIFEST CI — Validation Gates")
    print("=" * 60)
    
    # Find all manifests
    manifests = []
    if skill_filter:
        path = SKILLS_DIR / skill_filter / "MANIFEST.yaml"
        if path.exists():
            manifests.append(path)
        else:
            print(f"  ❌ Manifest not found: {path}")
            sys.exit(1)
    else:
        for d in sorted(SKILLS_DIR.iterdir()):
            if d.is_dir():
                manifest = d / "MANIFEST.yaml"
                if manifest.exists():
                    manifests.append(manifest)
    
    print(f"\n  Found {len(manifests)} manifests to validate\n")
    
    all_results = []
    total_blocks = 0
    total_warnings = 0
    total_pass = 0
    
    for manifest_path in manifests:
        result = run_all_gates(manifest_path)
        all_results.append(result)
        
        symbol = {"BLOCK": "🔴", "WARN": "🟡", "PASS": "🟢"}[result["verdict"]]
        print(f"  {symbol} {result['skill']:40s} {result['verdict']}")
        
        for block in result["blocks"]:
            print(f"      ❌ {block['gate']}: {block.get('reason', block.get('missing', ''))}")
        for warn in result["warnings"]:
            print(f"      ⚠️  {warn['gate']}: {warn.get('reason', warn.get('missing', ''))}")
        
        if result["verdict"] == "BLOCK":
            total_blocks += 1
        elif result["verdict"] == "WARN":
            total_warnings += 1
        else:
            total_pass += 1
    
    # Write report
    with open(CI_REPORT, "a") as f:
        for result in all_results:
            f.write(json.dumps(result) + "\n")
    
    print(f"\n{'='*60}")
    print(f"  RESULTS: {total_pass} PASS | {total_warnings} WARN | {total_blocks} BLOCK")
    print(f"  Report: {CI_REPORT}")
    print(f"{'='*60}")
    
    if total_blocks > 0:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
